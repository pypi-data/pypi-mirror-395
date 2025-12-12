#!/usr/bin/env python3
"""
Simple training job watcher - monitors active training jobs and shows key metrics.

Uses inotify to watch /sphere/app/featrix_output/ for train_es jobs and displays:
- Last few lines of log
- First validation loss
- Current validation loss
"""

import os
import re
import time
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent
except ImportError:
    print("❌ ERROR: watchdog is required but not installed")
    print("   Install with: pip install watchdog")
    sys.exit(1)

# Configuration
OUTPUT_DIR = Path("/sphere/app/featrix_output")
TAIL_LINES = 10  # Show last 10 lines of log

# Patterns to extract from logs
VAL_LOSS_PATTERN = re.compile(r'VAL LOSS:\s+([\d.]+)')
EPOCH_VAL_PATTERN = re.compile(r'\[epoch=(\d+)\].*?VAL LOSS:\s+([\d.]+)')
TRAIN_EPOCH_PATTERN = re.compile(r'Epoch (\d+)/\d+.*?validation_loss=([\d.]+)')
SP_EPOCH_PATTERN = re.compile(r'SP Epoch (\d+)/\d+.*?validation_loss=([\d.]+)')


def load_session_metadata(session_id):
    """Load session metadata from session file."""
    session_file = Path("/sphere/app/featrix_sessions") / f"{session_id}.session"
    if not session_file.exists():
        return {}
    
    try:
        import json
        with open(session_file, 'r') as f:
            return json.load(f)
    except:
        return {}


def get_training_metadata(job_dir, session_id):
    """Get metadata about the training job."""
    metadata = {
        'name': None,
        'input_filename': None,
        'num_rows': None,
        'num_columns': None,
        'column_names': None
    }
    
    # Try to load from session file
    session_data = load_session_metadata(session_id)
    if session_data:
        metadata['name'] = session_data.get('name')
        metadata['input_filename'] = session_data.get('input_filename') or session_data.get('input_data')
        # Try to get column info from session
        if 'column_spec' in session_data:
            metadata['column_names'] = list(session_data['column_spec'].keys())
            metadata['num_columns'] = len(metadata['column_names'])
    
    # Try to get data info from structured data output
    session_dir = job_dir.parent.parent
    create_sd_dir = session_dir / "create_structured_data"
    if create_sd_dir.exists():
        # Find most recent create_structured_data job
        sd_jobs = sorted(create_sd_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
        for sd_job in sd_jobs[:1]:  # Just check most recent
            schema_file = sd_job / "schema_metadata.json"
            if schema_file.exists():
                try:
                    import json
                    with open(schema_file, 'r') as f:
                        schema = json.load(f)
                        if metadata['num_rows'] is None:
                            metadata['num_rows'] = schema.get('total_rows')
                        if metadata['num_columns'] is None:
                            metadata['num_columns'] = schema.get('total_columns')
                        if metadata['column_names'] is None and 'columns' in schema:
                            metadata['column_names'] = list(schema['columns'].keys())
                        if metadata['input_filename'] is None:
                            metadata['input_filename'] = schema.get('original_file')
                except:
                    pass
    
    # Try to get ES name from embedded_space.json if it exists
    es_file = job_dir / "embedded_space.json"
    if es_file.exists():
        try:
            import json
            with open(es_file, 'r') as f:
                es_data = json.load(f)
                if metadata['name'] is None:
                    metadata['name'] = es_data.get('name')
        except:
            pass
    
    return metadata


def find_training_jobs():
    """Find all active train_es training jobs."""
    jobs = []
    
    if not OUTPUT_DIR.exists():
        return jobs
    
    # Look for train_es job directories
    for session_dir in OUTPUT_DIR.iterdir():
        if not session_dir.is_dir():
            continue
        
        train_es_dir = session_dir / "train_es"
        if not train_es_dir.exists():
            continue
        
        # Find job directories
        for job_dir in train_es_dir.iterdir():
            if not job_dir.is_dir():
                continue
            
            log_file = job_dir / "logs" / "stdout.log"
            if log_file.exists():
                session_id = session_dir.name
                metadata = get_training_metadata(job_dir, session_id)
                
                jobs.append({
                    'session_id': session_id,
                    'job_id': job_dir.name,
                    'log_file': log_file,
                    'job_dir': job_dir,
                    'metadata': metadata
                })
    
    return jobs


def extract_losses(log_file):
    """Extract first and current validation loss from log file."""
    first_val_loss = None
    current_val_loss = None
    current_epoch = 0
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Try different patterns
                match = EPOCH_VAL_PATTERN.search(line)
                if match:
                    epoch = int(match.group(1))
                    val_loss = float(match.group(2))
                    if first_val_loss is None:
                        first_val_loss = val_loss
                    if epoch >= current_epoch:
                        current_epoch = epoch
                        current_val_loss = val_loss
                    continue
                
                match = TRAIN_EPOCH_PATTERN.search(line)
                if match:
                    epoch = int(match.group(1))
                    val_loss = float(match.group(2))
                    if first_val_loss is None:
                        first_val_loss = val_loss
                    if epoch >= current_epoch:
                        current_epoch = epoch
                        current_val_loss = val_loss
                    continue
                
                match = SP_EPOCH_PATTERN.search(line)
                if match:
                    epoch = int(match.group(1))
                    val_loss = float(match.group(2))
                    if first_val_loss is None:
                        first_val_loss = val_loss
                    if epoch >= current_epoch:
                        current_epoch = epoch
                        current_val_loss = val_loss
                    continue
                
                # Fallback: just look for VAL LOSS
                if first_val_loss is None:
                    match = VAL_LOSS_PATTERN.search(line)
                    if match:
                        first_val_loss = float(match.group(1))
                        current_val_loss = first_val_loss
    except Exception as e:
        pass
    
    return first_val_loss, current_val_loss, current_epoch


def get_tail_lines(log_file, n=TAIL_LINES):
    """Get last n lines from log file."""
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            return lines[-n:] if len(lines) > n else lines
    except Exception:
        return []


def format_job_summary(job):
    """Format a job summary for display."""
    log_file = job['log_file']
    first_val, current_val, epoch = extract_losses(log_file)
    meta = job.get('metadata', {})
    
    summary = f"\n{'='*80}\n"
    summary += f"📊 {job['session_id']} / {job['job_id']}\n"
    summary += f"{'='*80}\n"
    
    # Metadata section
    if meta.get('name'):
        summary += f"   Name:            {meta['name']}\n"
    if meta.get('input_filename'):
        filename = Path(meta['input_filename']).name
        summary += f"   File:            {filename}\n"
    if meta.get('num_rows') is not None:
        summary += f"   Rows:            {meta['num_rows']:,}\n"
    if meta.get('num_columns') is not None:
        summary += f"   Columns:         {meta['num_columns']}\n"
    if meta.get('column_names'):
        cols = meta['column_names']
        if len(cols) <= 10:
            summary += f"   Column Names:    {', '.join(cols)}\n"
        else:
            summary += f"   Column Names:    {', '.join(cols[:10])} ... (+{len(cols)-10} more)\n"
    
    summary += f"\n   Training Progress:\n"
    if first_val is not None:
        summary += f"   First Val Loss:  {first_val:.4f}\n"
    if current_val is not None:
        summary += f"   Current Val Loss: {current_val:.4f}"
        if first_val is not None and first_val > 0:
            improvement = ((first_val - current_val) / first_val) * 100
            summary += f" ({improvement:+.1f}% improvement)"
        summary += "\n"
    if epoch > 0:
        summary += f"   Current Epoch:   {epoch}\n"
    
    summary += f"\n   Last {TAIL_LINES} lines:\n"
    summary += f"   {'-'*76}\n"
    tail = get_tail_lines(log_file)
    for line in tail:
        # Indent log lines
        summary += f"   {line.rstrip()}\n"
    
    return summary


class TrainingJobHandler(FileSystemEventHandler):
    """Handle file system events for training jobs."""
    
    def __init__(self):
        self.displayed_jobs = set()
        self.last_update = {}
    
    def should_display(self, log_file):
        """Check if we should display this job (new or recently updated)."""
        try:
            mtime = log_file.stat().st_mtime
            job_key = str(log_file)
            
            # Display if new or updated in last 5 seconds
            if job_key not in self.last_update or mtime > self.last_update[job_key] + 2:
                self.last_update[job_key] = mtime
                return True
            return False
        except:
            return False
    
    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
        
        if 'stdout.log' in event.src_path or 'stderr.log' in event.src_path:
            log_file = Path(event.src_path)
            if self.should_display(log_file):
                self.display_jobs()
    
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        if 'stdout.log' in event.src_path:
            log_file = Path(event.src_path)
            if self.should_display(log_file):
                self.display_jobs()
    
    def display_jobs(self):
        """Display all active training jobs."""
        jobs = find_training_jobs()
        
        # Clear screen
        os.system('clear')
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Active Training Jobs: {len(jobs)}")
        print(f"   Monitoring: {OUTPUT_DIR}\n")
        
        if not jobs:
            print("   No active training jobs found")
        else:
            for job in jobs:
                print(format_job_summary(job))


def main():
    """Main watch loop."""
    print("🔍 Watching for active training jobs...")
    print(f"   Monitoring: {OUTPUT_DIR}")
    print("   Press Ctrl+C to stop\n")
    
    # Initial display
    jobs = find_training_jobs()
    if jobs:
        handler = TrainingJobHandler()
        handler.display_jobs()
    else:
        print("   No active training jobs found")
    
    # Use inotify via watchdog
    event_handler = TrainingJobHandler()
    observer = Observer()
    
    # Watch the output directory recursively
    observer.schedule(event_handler, str(OUTPUT_DIR), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n\n👋 Stopped watching")
    
    observer.join()


if __name__ == "__main__":
    main()

