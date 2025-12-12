#!/usr/bin/env python3
"""
Centralized Error Tracking System for Featrix Sphere

This module provides a centralized way to track, collect, and display
all errors and failures across the sphere system.
"""

import json
import time
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import threading
import traceback

class ErrorTracker:
    """
    Centralized error tracking system that collects errors from across 
    the Featrix Sphere system and makes them easy to view in dashboards.
    """
    
    def __init__(self, error_log_path: str = None):
        """Initialize the error tracker with an error log file path."""
        if error_log_path is None:
            try:
                from config import config
                self.error_log_path = config.output_dir / "sphere_errors.jsonl"
            except:
                self.error_log_path = Path("./featrix_output/sphere_errors.jsonl")
        else:
            self.error_log_path = Path(error_log_path)
        
        # Ensure the directory exists
        self.error_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Thread lock for safe concurrent writing
        self._lock = threading.Lock()
        
        # In-memory recent errors for fast dashboard access
        self._recent_errors = []
        self._max_recent = 100
    
    def log_error(self, 
                  error_type: str,
                  message: str, 
                  job_id: str = None,
                  session_id: str = None,
                  component: str = None,
                  exception: Exception = None,
                  context: Dict[str, Any] = None):
        """
        Log an error to the centralized error tracking system.
        
        Args:
            error_type: Type of error (training_failed, validation_error, etc.)
            message: Human-readable error message
            job_id: Associated job ID if applicable
            session_id: Associated session ID if applicable  
            component: System component where error occurred
            exception: Original exception object if available
            context: Additional context information
        """
        
        error_entry = {
            "timestamp": time.time(),
            "datetime": datetime.now(timezone.utc).isoformat(),
            "error_type": error_type,
            "message": message,
            "job_id": job_id,
            "session_id": session_id,
            "component": component or "unknown",
            "severity": self._determine_severity(error_type, message),
            "context": context or {},
            "traceback": None,
            "pid": os.getpid(),
            "hostname": os.uname().nodename if hasattr(os, 'uname') else "unknown"
        }
        
        # Add traceback if exception provided
        if exception:
            error_entry["exception_type"] = type(exception).__name__
            error_entry["traceback"] = traceback.format_exception(
                type(exception), exception, exception.__traceback__
            )
        
        # Thread-safe logging
        with self._lock:
            # Add to recent errors in memory
            self._recent_errors.append(error_entry)
            if len(self._recent_errors) > self._max_recent:
                self._recent_errors.pop(0)
            
            # Append to persistent log file (JSONL format)
            try:
                with open(self.error_log_path, 'a') as f:
                    f.write(json.dumps(error_entry) + '\n')
            except Exception as e:
                # Fallback: at least print to stderr if file writing fails
                print(f"❌ ERROR TRACKER FAILED: {e}", file=sys.stderr)
                print(f"   Original error: {message}", file=sys.stderr)
    
    def _determine_severity(self, error_type: str, message: str) -> str:
        """Determine error severity based on type and message content."""
        message_lower = message.lower()
        
        # Critical errors that stop training/processing
        if any(keyword in message_lower for keyword in ['failed to create', 'out of memory', 'cuda error', 'fatal']):
            return "critical"
        
        # High priority errors
        if any(keyword in message_lower for keyword in ['training failed', 'validation failed', 'model failed']):
            return "high"
        
        # Medium priority warnings
        if any(keyword in message_lower for keyword in ['warning', 'deprecated', 'fallback']):
            return "medium"
        
        # Default to high for unclassified errors
        return "high"
    
    def get_recent_errors(self, limit: int = 50) -> List[Dict]:
        """Get recent errors from memory (fast access for dashboards)."""
        with self._lock:
            return self._recent_errors[-limit:] if limit else self._recent_errors.copy()
    
    def get_errors_for_job(self, job_id: str) -> List[Dict]:
        """Get all errors associated with a specific job ID."""
        with self._lock:
            return [error for error in self._recent_errors if error.get('job_id') == job_id]
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get a summary of errors by type and severity."""
        with self._lock:
            summary = {
                "total_errors": len(self._recent_errors),
                "by_severity": {"critical": 0, "high": 0, "medium": 0, "low": 0},
                "by_component": {},
                "by_error_type": {},
                "recent_critical": []
            }
            
            for error in self._recent_errors:
                severity = error.get("severity", "high")
                component = error.get("component", "unknown")
                error_type = error.get("error_type", "unknown")
                
                summary["by_severity"][severity] += 1
                summary["by_component"][component] = summary["by_component"].get(component, 0) + 1
                summary["by_error_type"][error_type] = summary["by_error_type"].get(error_type, 0) + 1
                
                # Track recent critical errors
                if severity == "critical":
                    summary["recent_critical"].append({
                        "timestamp": error["timestamp"],
                        "message": error["message"],
                        "job_id": error.get("job_id")
                    })
            
            # Keep only last 10 critical errors
            summary["recent_critical"] = summary["recent_critical"][-10:]
            
            return summary
    
    def clear_old_errors(self, days_old: int = 7):
        """Clear errors older than specified days from the log file."""
        if not self.error_log_path.exists():
            return
        
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        temp_file = self.error_log_path.with_suffix('.tmp')
        
        with self._lock:
            try:
                with open(self.error_log_path, 'r') as infile, open(temp_file, 'w') as outfile:
                    for line in infile:
                        try:
                            error = json.loads(line.strip())
                            if error.get('timestamp', 0) > cutoff_time:
                                outfile.write(line)
                        except json.JSONDecodeError:
                            continue  # Skip malformed lines
                
                # Replace original with cleaned file
                temp_file.replace(self.error_log_path)
                
            except Exception as e:
                # Clean up temp file if something went wrong
                if temp_file.exists():
                    temp_file.unlink()
                raise e


# Global error tracker instance
_global_error_tracker = None
_tracker_lock = threading.Lock()

def get_error_tracker() -> ErrorTracker:
    """Get the global error tracker instance (singleton)."""
    global _global_error_tracker
    
    if _global_error_tracker is None:
        with _tracker_lock:
            if _global_error_tracker is None:
                _global_error_tracker = ErrorTracker()
    
    return _global_error_tracker

def log_sphere_error(error_type: str, 
                    message: str, 
                    job_id: str = None,
                    session_id: str = None,
                    component: str = None,
                    exception: Exception = None,
                    context: Dict[str, Any] = None):
    """
    Convenience function to log errors to the global tracker.
    
    Example usage:
        log_sphere_error(
            error_type="training_failed",
            message="EmbeddingSpace object has no attribute 'output_dir'",
            job_id="train_es_20241210_abc123",
            component="embedded_space",
            exception=e
        )
    """
    tracker = get_error_tracker()
    tracker.log_error(
        error_type=error_type,
        message=message,
        job_id=job_id,
        session_id=session_id,
        component=component,
        exception=exception,
        context=context
    )

# Convenience functions for common error types
def log_training_error(message: str, job_id: str = None, exception: Exception = None, **kwargs):
    """Log a training-related error."""
    log_sphere_error("training_error", message, job_id=job_id, component="training", exception=exception, **kwargs)

def log_validation_error(message: str, job_id: str = None, exception: Exception = None, **kwargs):
    """Log a validation-related error."""
    log_sphere_error("validation_error", message, job_id=job_id, component="validation", exception=exception, **kwargs)

def log_data_error(message: str, job_id: str = None, exception: Exception = None, **kwargs):
    """Log a data processing error."""
    log_sphere_error("data_error", message, job_id=job_id, component="data_processing", exception=exception, **kwargs)

def log_system_error(message: str, component: str = None, exception: Exception = None, **kwargs):
    """Log a system-level error."""
    log_sphere_error("system_error", message, component=component or "system", exception=exception, **kwargs)


if __name__ == "__main__":
    # Test the error tracker
    tracker = ErrorTracker("test_errors.jsonl")
    
    # Test logging various types of errors
    tracker.log_error(
        error_type="test_error",
        message="This is a test error",
        component="test_component",
        context={"test_key": "test_value"}
    )
    
    # Test with exception
    try:
        raise ValueError("Test exception")
    except Exception as e:
        tracker.log_error(
            error_type="test_exception",
            message="Test exception handling",
            component="test_component",
            exception=e
        )
    
    # Test summary
    summary = tracker.get_error_summary()
    print("Error Summary:", json.dumps(summary, indent=2))
    
    # Test recent errors
    recent = tracker.get_recent_errors(limit=5)
    print(f"Recent errors: {len(recent)}") 