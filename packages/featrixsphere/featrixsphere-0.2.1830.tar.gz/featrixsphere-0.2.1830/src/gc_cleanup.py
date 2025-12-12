#!/usr/bin/env python3
"""
Garbage Collection process for Featrix Sphere.

This process:
1. Walks job directories looking for jobs > 1 week old that didn't finish training → marks for deletion
2. Looks for DELETEME flags in session directories → marks for deletion
3. If markers are > 1 day old AND disk space < 25% free on /sphere, then deletes

Runs continuously, checking every hour.
"""

import os
import sys
import json
import time
import shutil
import logging
import gzip
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)-8s] [PID:%(process)d] %(name)-45s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuration
JOB_OUTPUT_DIR = Path("/sphere/app/featrix_output")
SESSION_DIR = Path("/sphere/app/featrix_sessions")
MARKER_FILE = "MARKED_FOR_DELETE"
DELETEME_FILE = "DELETEME"
JOB_AGE_THRESHOLD_DAYS = 7  # Jobs older than 1 week
MARKER_AGE_THRESHOLD_HOURS = 24  # Markers must be > 1 day old
DISK_FREE_THRESHOLD_PERCENT = 25.0  # Delete if < 25% free
EMERGENCY_DISK_FREE_THRESHOLD_PERCENT = 10.0  # Emergency delete if < 10% free
LOG_DISK_FREE_THRESHOLD_PERCENT = 10.0  # Clean logs if < 10% free on /var/log
CHECK_INTERVAL_SECONDS = 3600  # Full GC check every hour
DISK_CHECK_INTERVAL_SECONDS = 300  # Disk space check every 5 minutes
LOG_DIR = Path("/var/log/featrix")
LOG_FILE_MAX_AGE_DAYS = 7  # Delete log files older than 7 days
LOG_GZIP_AGE_HOURS = 24  # Gzip rotated logs < 24 hours old


def get_disk_free_percent(path: str = "/sphere") -> float:
    """Get percentage of free disk space."""
    try:
        total, used, free = shutil.disk_usage(path)
        free_percent = (free / total) * 100.0
        return free_percent
    except Exception as e:
        logger.error(f"Error checking disk space: {e}")
        return 100.0  # Assume plenty of space if we can't check


def cleanup_log_files():
    """Clean up old log files in /var/log/featrix if disk space is low."""
    disk_free = get_disk_free_percent("/var/log")
    
    if disk_free >= LOG_DISK_FREE_THRESHOLD_PERCENT:
        return 0, 0  # No cleanup needed
    
    logger.warning(f"📋 LOG CLEANUP: Disk free on /var/log ({disk_free:.1f}%) < {LOG_DISK_FREE_THRESHOLD_PERCENT}% - cleaning up logs")
    
    if not LOG_DIR.exists():
        logger.debug(f"Log directory does not exist: {LOG_DIR}")
        return 0, 0
    
    deleted_count = 0
    gzipped_count = 0
    current_time = time.time()
    max_age_seconds = LOG_FILE_MAX_AGE_DAYS * 24 * 3600
    gzip_age_seconds = LOG_GZIP_AGE_HOURS * 3600
    
    try:
        for log_file in LOG_DIR.iterdir():
            if not log_file.is_file():
                continue
            
            # Skip files that end with .log (active logs)
            if log_file.name.endswith('.log'):
                continue
            
            # Security check: ensure file is under /var/log/featrix
            if not is_path_safe_to_delete(log_file, base_path="/var/log/featrix"):
                continue
            
            try:
                file_age_seconds = current_time - log_file.stat().st_mtime
                
                # Delete files older than max age
                if file_age_seconds > max_age_seconds:
                    logger.info(f"🗑️  Deleting old log file: {log_file.name} (age: {file_age_seconds / 86400:.1f} days)")
                    log_file.unlink()
                    deleted_count += 1
                # Gzip rotated logs that are < 24 hours old and not already gzipped
                elif file_age_seconds < gzip_age_seconds and not log_file.name.endswith('.gz'):
                    logger.info(f"📦 Gzipping rotated log: {log_file.name} (age: {file_age_seconds / 3600:.1f} hours)")
                    try:
                        # Preserve original file timestamp
                        original_mtime = log_file.stat().st_mtime
                        
                        with open(log_file, 'rb') as f_in:
                            gzip_path = log_file.parent / f"{log_file.name}.gz"
                            with gzip.open(gzip_path, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        
                        # Restore original timestamp on the gzipped file
                        os.utime(gzip_path, (time.time(), original_mtime))
                        
                        log_file.unlink()
                        gzipped_count += 1
                    except Exception as e:
                        logger.warning(f"Failed to gzip {log_file.name}: {e}")
            except Exception as e:
                logger.debug(f"Error processing log file {log_file.name}: {e}")
    
    except Exception as e:
        logger.error(f"Error during log cleanup: {e}", exc_info=True)
    
    if deleted_count > 0 or gzipped_count > 0:
        logger.info(f"✅ Log cleanup complete: deleted {deleted_count} files, gzipped {gzipped_count} files")
    
    return deleted_count, gzipped_count


def is_path_safe_to_delete(item_path: Path, base_path: str = "/sphere") -> bool:
    """Check if a path is safe to delete by ensuring it's under base_path (resolving symlinks).
    
    Supports base_path being a symlink (e.g., /sphere -> /shared1/sphere).
    Uses realpath() to resolve symlinks and prevent path traversal attacks.
    """
    try:
        # Get realpath of the item (resolves symlinks and .. components)
        item_realpath = os.path.realpath(str(item_path))
        
        # Get realpath of base_path (handles symlinks like /sphere -> /shared1/sphere)
        # This allows base_path to be a symlink, which is supported and expected
        base_realpath = os.path.realpath(base_path)
        
        # Ensure item's realpath starts with base_path's realpath
        # This prevents path traversal attacks like /sphere/../etc/passwd
        if not item_realpath.startswith(base_realpath):
            logger.error(f"🚫 SECURITY: Refusing to delete {item_path} - realpath {item_realpath} is not under {base_realpath}")
            return False
        
        # Additional check: ensure it's not exactly base_path itself
        if item_realpath == base_realpath:
            logger.error(f"🚫 SECURITY: Refusing to delete {item_path} - would delete {base_path} root directory")
            return False
        
        return True
    except Exception as e:
        logger.error(f"Error checking path safety for {item_path}: {e}")
        return False


def is_job_finished(job_dir: Path) -> bool:
    """Check if a job finished training successfully."""
    # Check for pickle file (indicates successful completion)
    if any(job_dir.glob("*.pickle")):
        return True
    
    # Check stdout.log for completion indicators
    log_file = job_dir / "stdout.log"
    if log_file.exists():
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                last_lines = ''.join(lines[-50:]) if len(lines) > 50 else ''.join(lines)
                
                # Completion indicators
                completion_indicators = [
                    "Setting encoder.eval()",
                    "Final model saved",
                    "Training complete",
                    "Embedding space training completed",
                    "returned embedding space",
                ]
                
                for indicator in completion_indicators:
                    if indicator in last_lines:
                        return True
        except Exception as e:
            logger.debug(f"Error reading log file {log_file}: {e}")
    
    return False


def is_job_running(job_dir: Path) -> bool:
    """Check if job is currently running."""
    # Check for RUNNING marker
    if (job_dir / "RUNNING").exists():
        return True
    
    # Check if log file was recently modified (within last 5 minutes)
    log_file = job_dir / "stdout.log"
    if log_file.exists():
        try:
            mtime = log_file.stat().st_mtime
            age_seconds = time.time() - mtime
            if age_seconds < 300:  # 5 minutes
                return True
        except Exception:
            pass
    
    return False


def get_job_age_days(job_dir: Path) -> float:
    """Get age of job directory in days."""
    try:
        mtime = job_dir.stat().st_mtime
        age_seconds = time.time() - mtime
        return age_seconds / (24 * 3600)
    except Exception:
        return 0.0


def create_marker(job_dir: Path, reason: str) -> bool:
    """
    Create MARKED_FOR_DELETE marker file.
    
    Preserves the directory's mtime so ls -lrt in featrix_output/ still shows
    directories in order of when they were actually created/modified, not when
    they were marked for deletion.
    """
    marker_path = job_dir / MARKER_FILE
    if marker_path.exists():
        # Already marked, just update timestamp if needed
        return True
    
    # Save directory's original mtime before modifying it
    try:
        dir_stat = job_dir.stat()
        original_atime = dir_stat.st_atime
        original_mtime = dir_stat.st_mtime
    except Exception as e:
        logger.warning(f"Could not read dir times for {job_dir.name}: {e}")
        original_atime = None
        original_mtime = None
    
    try:
        marker_data = {
            "marked_at": datetime.now().isoformat(),
            "marked_unix_time": time.time(),
            "reason": reason
        }
        with open(marker_path, 'w') as f:
            json.dump(marker_data, f, indent=2)
        
        # Restore directory's original mtime so ls -lrt still works
        if original_atime is not None and original_mtime is not None:
            os.utime(job_dir, (original_atime, original_mtime))
        
        logger.info(f"📌 Marked {job_dir.name} for deletion: {reason}")
        return True
    except Exception as e:
        logger.error(f"Failed to create marker for {job_dir.name}: {e}")
        return False


def get_marker_age_hours(marker_path: Path) -> Optional[float]:
    """Get age of marker in hours."""
    if not marker_path.exists():
        return None
    
    try:
        with open(marker_path, 'r') as f:
            marker_data = json.load(f)
        marked_time = marker_data.get("marked_unix_time", time.time())
        age_seconds = time.time() - marked_time
        return age_seconds / 3600.0
    except Exception as e:
        logger.debug(f"Error reading marker {marker_path}: {e}")
        return None


def delete_job_directory(job_dir: Path) -> bool:
    """Delete a job directory and all its contents."""
    # Security check: ensure path is safe to delete
    if not is_path_safe_to_delete(job_dir):
        return False
    
    try:
        logger.info(f"🗑️  Deleting job directory: {job_dir}")
        shutil.rmtree(job_dir)
        logger.info(f"✅ Deleted {job_dir.name}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete {job_dir}: {e}")
        return False


def scan_job_directories() -> Tuple[List[Path], List[Path]]:
    """Scan job directories and return (to_mark, to_delete) lists."""
    to_mark = []
    to_delete = []
    
    if not JOB_OUTPUT_DIR.exists():
        logger.warning(f"Job output directory does not exist: {JOB_OUTPUT_DIR}")
        return to_mark, to_delete
    
    logger.info(f"🔍 Scanning job directories in {JOB_OUTPUT_DIR}")
    
    for job_dir in JOB_OUTPUT_DIR.iterdir():
        if not job_dir.is_dir():
            continue
        
        # Skip if already marked
        marker_path = job_dir / MARKER_FILE
        if marker_path.exists():
            # Check if marker is old enough and we should delete
            marker_age = get_marker_age_hours(marker_path)
            if marker_age is not None and marker_age >= MARKER_AGE_THRESHOLD_HOURS:
                # Check disk space
                disk_free = get_disk_free_percent()
                if disk_free < DISK_FREE_THRESHOLD_PERCENT:
                    to_delete.append(job_dir)
                else:
                    logger.debug(f"⏳ {job_dir.name}: Marker {marker_age:.1f}h old, but disk free ({disk_free:.1f}%) >= threshold")
            continue
        
        # Check if job should be marked for deletion
        if is_job_running(job_dir):
            continue  # Skip running jobs
        
        job_age_days = get_job_age_days(job_dir)
        if job_age_days >= JOB_AGE_THRESHOLD_DAYS:
            if not is_job_finished(job_dir):
                reason = f"Job > {JOB_AGE_THRESHOLD_DAYS} days old ({job_age_days:.1f} days) and did not finish training"
                to_mark.append((job_dir, reason))
    
    return to_mark, to_delete


def scan_session_directories() -> Tuple[List[Path], List[Path]]:
    """Scan session directories for DELETEME flags and return (to_mark, to_delete) lists."""
    to_mark = []
    to_delete = []
    
    if not SESSION_DIR.exists():
        logger.warning(f"Session directory does not exist: {SESSION_DIR}")
        return to_mark, to_delete
    
    logger.info(f"🔍 Scanning session directories in {SESSION_DIR}")
    
    # Check for DELETEME files next to .session files
    for session_file in SESSION_DIR.glob("*.session"):
        session_id = session_file.stem
        deleteme_path = session_file.parent / f"{session_id}.DELETEME"
        
        # Also check for DELETEME in the session file's directory
        if not deleteme_path.exists():
            deleteme_path = session_file.parent / DELETEME_FILE
        
        if deleteme_path.exists():
            # Found DELETEME flag
            # Check if we should mark or delete
            marker_path = session_file.parent / MARKER_FILE
            
            if marker_path.exists():
                # Already marked, check if old enough to delete
                marker_age = get_marker_age_hours(marker_path)
                if marker_age is not None and marker_age >= MARKER_AGE_THRESHOLD_HOURS:
                    disk_free = get_disk_free_percent()
                    if disk_free < DISK_FREE_THRESHOLD_PERCENT:
                        to_delete.append(session_file)
                continue
            
            # Mark for deletion
            reason = f"DELETEME flag found"
            
            # Save parent directory's original mtime before modifying it
            parent_dir = session_file.parent
            try:
                dir_stat = parent_dir.stat()
                original_atime = dir_stat.st_atime
                original_mtime = dir_stat.st_mtime
            except Exception as e:
                logger.warning(f"Could not read dir times for {parent_dir}: {e}")
                original_atime = None
                original_mtime = None
            
            try:
                marker_data = {
                    "marked_at": datetime.now().isoformat(),
                    "marked_unix_time": time.time(),
                    "reason": reason,
                    "session_id": session_id
                }
                with open(marker_path, 'w') as f:
                    json.dump(marker_data, f, indent=2)
                
                # Restore directory's original mtime so ls -lrt still works
                if original_atime is not None and original_mtime is not None:
                    os.utime(parent_dir, (original_atime, original_mtime))
                
                logger.info(f"📌 Marked session {session_id} for deletion: {reason}")
            except Exception as e:
                logger.error(f"Failed to create marker for session {session_id}: {e}")
        else:
            # Check if session has a marker that's old enough to delete
            marker_path = session_file.parent / MARKER_FILE
            if marker_path.exists():
                marker_age = get_marker_age_hours(marker_path)
                if marker_age is not None and marker_age >= MARKER_AGE_THRESHOLD_HOURS:
                    disk_free = get_disk_free_percent()
                    if disk_free < DISK_FREE_THRESHOLD_PERCENT:
                        to_delete.append(session_file)
    
    return to_mark, to_delete


def delete_session(session_file: Path) -> bool:
    """Delete a session file and associated data."""
    # Security check: ensure path is safe to delete
    if not is_path_safe_to_delete(session_file):
        return False
    
    try:
        session_id = session_file.stem
        
        # Try to delete associated job directories BEFORE deleting session file
        # Find jobs in the session file if we can read it
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            job_plan = session_data.get("job_plan", [])
            for job in job_plan:
                job_id = job.get("job_id")
                if job_id:
                    job_dir = JOB_OUTPUT_DIR / job_id
                    if job_dir.exists():
                        # Security check for job directory too
                        if is_path_safe_to_delete(job_dir):
                            logger.info(f"🗑️  Deleting associated job directory: {job_id}")
                            try:
                                shutil.rmtree(job_dir)
                            except Exception as e:
                                logger.warning(f"Failed to delete job directory {job_id}: {e}")
                        else:
                            logger.warning(f"🚫 Skipping unsafe job directory path: {job_id}")
        except Exception as e:
            logger.debug(f"Could not read session file to find associated jobs: {e}")
        
        # Delete session file
        logger.info(f"🗑️  Deleting session: {session_id}")
        session_file.unlink()
        
        # Also delete marker and DELETEME files if they exist
        marker_path = session_file.parent / MARKER_FILE
        deleteme_path = session_file.parent / DELETEME_FILE
        if marker_path.exists():
            try:
                marker_path.unlink()
            except Exception:
                pass
        if deleteme_path.exists():
            try:
                deleteme_path.unlink()
            except Exception:
                pass
        
        logger.info(f"✅ Deleted session {session_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete session {session_file}: {e}")
        return False


def emergency_cleanup_marked_items():
    """Emergency cleanup: Delete all MARK_FOR_DELETE items if disk space < 10%."""
    disk_free = get_disk_free_percent()
    
    if disk_free >= EMERGENCY_DISK_FREE_THRESHOLD_PERCENT:
        return 0, 0  # No emergency cleanup needed
    
    logger.warning(f"🚨 EMERGENCY: Disk free ({disk_free:.1f}%) < {EMERGENCY_DISK_FREE_THRESHOLD_PERCENT}% - deleting all MARK_FOR_DELETE items")
    
    deleted_jobs = 0
    deleted_sessions = 0
    
    # Find and delete all marked job directories (no age check)
    if JOB_OUTPUT_DIR.exists():
        for job_dir in JOB_OUTPUT_DIR.iterdir():
            if not job_dir.is_dir():
                continue
            
            marker_path = job_dir / MARKER_FILE
            if marker_path.exists():
                logger.info(f"🗑️  Emergency deleting marked job: {job_dir.name}")
                if delete_job_directory(job_dir):
                    deleted_jobs += 1
    
    # Find and delete all marked session files (no age check)
    if SESSION_DIR.exists():
        for session_file in SESSION_DIR.glob("*.session"):
            marker_path = session_file.parent / MARKER_FILE
            if marker_path.exists():
                logger.info(f"🗑️  Emergency deleting marked session: {session_file.stem}")
                if delete_session(session_file):
                    deleted_sessions += 1
    
    if deleted_jobs > 0 or deleted_sessions > 0:
        logger.warning(f"✅ Emergency cleanup complete: deleted {deleted_jobs} jobs, {deleted_sessions} sessions")
    
    return deleted_jobs, deleted_sessions


def run_gc_cycle():
    """Run one GC cycle."""
    logger.info("=" * 80)
    logger.info("🔄 Starting GC cycle")
    
    # Check disk space
    disk_free = get_disk_free_percent()
    logger.info(f"💾 Disk free on /sphere: {disk_free:.1f}%")
    
    # Scan job directories
    job_to_mark, job_to_delete = scan_job_directories()
    
    # Mark jobs for deletion
    for job_dir, reason in job_to_mark:
        create_marker(job_dir, reason)
    
    # Scan session directories
    session_to_mark, session_to_delete = scan_session_directories()
    
    # Delete jobs if conditions are met
    deleted_jobs = 0
    for job_dir in job_to_delete:
        if delete_job_directory(job_dir):
            deleted_jobs += 1
    
    # Delete sessions if conditions are met
    deleted_sessions = 0
    for session_file in session_to_delete:
        if delete_session(session_file):
            deleted_sessions += 1
    
    logger.info(f"✅ GC cycle complete: marked {len(job_to_mark)} jobs, deleted {deleted_jobs} jobs, deleted {deleted_sessions} sessions")
    logger.info("=" * 80)


def main():
    import socket
    hostname = socket.gethostname()
    logger.info("=" * 80)
    logger.info(f"🚀 GC CLEANUP STARTING - {datetime.now().isoformat()}")
    logger.info("=" * 80)
    logger.info(f"Hostname: {hostname}")
    logger.info(f"Check interval: {CHECK_INTERVAL_SECONDS} seconds")
    logger.info(f"Disk check interval: {DISK_CHECK_INTERVAL_SECONDS} seconds")
    logger.info(f"Job age threshold: {JOB_AGE_THRESHOLD_DAYS} days")
    logger.info(f"Emergency disk threshold: {EMERGENCY_DISK_FREE_THRESHOLD_PERCENT}%")
    logger.info("=" * 80)
    """Main GC process loop."""
    logger.info("🚀 Featrix Sphere GC Cleanup Process Starting")
    logger.info(f"   Job output dir: {JOB_OUTPUT_DIR}")
    logger.info(f"   Session dir: {SESSION_DIR}")
    logger.info(f"   Job age threshold: {JOB_AGE_THRESHOLD_DAYS} days")
    logger.info(f"   Marker age threshold: {MARKER_AGE_THRESHOLD_HOURS} hours")
    logger.info(f"   Disk free threshold: {DISK_FREE_THRESHOLD_PERCENT}%")
    logger.info(f"   Emergency disk threshold: {EMERGENCY_DISK_FREE_THRESHOLD_PERCENT}%")
    logger.info(f"   Full GC check interval: {CHECK_INTERVAL_SECONDS} seconds (1 hour)")
    logger.info(f"   Disk space check interval: {DISK_CHECK_INTERVAL_SECONDS} seconds (5 minutes)")
    
    last_full_gc = time.time()
    
    while True:
        current_time = time.time()
        time_since_full_gc = current_time - last_full_gc
        
        # Check disk space every 5 minutes
        try:
            # Check /sphere disk space
            disk_free = get_disk_free_percent()
            if disk_free < EMERGENCY_DISK_FREE_THRESHOLD_PERCENT:
                logger.warning(f"💾 Disk free ({disk_free:.1f}%) < {EMERGENCY_DISK_FREE_THRESHOLD_PERCENT}% - running emergency cleanup")
                emergency_cleanup_marked_items()
            else:
                logger.debug(f"💾 Disk free ({disk_free:.1f}%) >= {EMERGENCY_DISK_FREE_THRESHOLD_PERCENT}% - no emergency cleanup needed")
            
            # Check /var/log disk space and clean up logs if needed
            cleanup_log_files()
        except Exception as e:
            logger.error(f"Error in disk space check: {e}", exc_info=True)
        
        # Run full GC cycle every hour
        if time_since_full_gc >= CHECK_INTERVAL_SECONDS:
            try:
                run_gc_cycle()
                last_full_gc = current_time
            except Exception as e:
                logger.error(f"Error in GC cycle: {e}", exc_info=True)
        
        # Sleep for 5 minutes until next disk check
        logger.debug(f"⏳ Sleeping for {DISK_CHECK_INTERVAL_SECONDS} seconds until next disk check...")
        time.sleep(DISK_CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()

