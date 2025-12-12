#!/usr/bin/env python3
"""
Celery app for async batch prediction jobs.
Training jobs continue to use the existing featrix_queue system.
"""

from celery import Celery
from celery.signals import worker_ready
from config import config
import json
import traceback
import sys
import pickle
import gc
import logging
import os
import contextlib
import traceback
import subprocess
import json as json_module
import tempfile
import signal
from pathlib import Path
from datetime import datetime

# Set up proper logging for Celery
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Install Featrix exception hook for better error tracking
try:
    from lib.featrix_debug import install_featrix_excepthook
    install_featrix_excepthook()
except Exception:
    pass  # Don't fail if debug module not available

# CRITICAL: Set up Python path BEFORE any featrix imports to avoid circular dependencies
lib_path = Path(__file__).parent / "lib"
current_path = Path(__file__).parent

if str(lib_path.resolve()) not in sys.path:
    sys.path.insert(0, str(lib_path.resolve()))
if str(current_path.resolve()) not in sys.path:
    sys.path.insert(0, str(current_path.resolve()))

logger.info(f"🔧 Celery module loading - Python paths set up")
logger.info(f"  lib_path: {lib_path.resolve()}")
logger.info(f"  current_path: {current_path.resolve()}")

# Import NON-CUDA modules at module level only
# CRITICAL: Do NOT import torch here - causes CUDA fork issues
try:
    import numpy as np  # noqa: F401
    import pandas as pd  # noqa: F401
    logger.info(f"✅ Non-CUDA modules imported at module level")
except ImportError as e:
    logger.warning(f"⚠️ Core modules not available: {e}")

# Will check torch availability inside tasks after fork
TORCH_AVAILABLE = False

try:
    from lib.session_manager import load_session
    FEATRIX_QUEUE_AVAILABLE = True
    logger.info(f"✅ session_manager imported at module level")
except ImportError as e:
    FEATRIX_QUEUE_AVAILABLE = False
    logger.warning(f"⚠️ session_manager not available: {e}")

# CRITICAL: Do NOT import featrix modules at module level
# They contain torch imports which cause CUDA fork issues in Celery
# Will import them inside tasks after the fork happens
logger.info(f"🔧 Skipping featrix imports at module level to avoid CUDA fork issues")
logger.info(f"🔧 Will import torch and featrix modules inside task after fork")

# Initialize Celery app
app = Celery('sphere_predictions')

# Configure Celery to use Redis as broker and result backend
app.conf.update(
    broker_url='redis://localhost:6379/1',
    result_backend='redis://localhost:6379/1',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/New_York',
    enable_utc=True,
    result_expires=3600,  # Results expire after 1 hour
    task_routes={
        'celery_app.predict_batch': {'queue': 'cpu_worker'},
        'celery_app.project_training_movie_frame': {'queue': 'cpu_worker'},
        'celery_app.create_structured_data': {'queue': 'cpu_worker'},
        'celery_app.run_clustering': {'queue': 'cpu_worker'},
        'celery_app.train_single_predictor': {'queue': 'gpu_training'},
        'celery_app.train_es': {'queue': 'gpu_training'},
        'celery_app.train_knn': {'queue': 'cpu_worker'},
        'celery_app.dump_to_backplane': {'queue': 'cpu_worker'},
        'celery_app.ping': {'queue': 'cpu_worker'},  # Default to cpu_worker, but can be overridden
    },
    worker_prefetch_multiplier=1,  # One task at a time for GPU jobs
    task_acks_late=True,
    worker_disable_rate_limits=True,
    # Logging configuration
    worker_log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    worker_task_log_format='%(asctime)s - %(name)s - %(levelname)s - [%(task_name)s(%(task_id)s)] %(message)s',
    worker_hijack_root_logger=False,  # Let our logging config work
)

# ============================================================================
# STANDARD JOB SETUP - Used by ALL Celery tasks
# ============================================================================

@contextlib.contextmanager
def setup_job_logging(job_id: str, session_id: str, job_type: str):
    """
    Standard job setup for ALL Celery tasks.
    
    Creates job directory, logs directory, and redirects stdout/stderr to logs/stdout.log.
    This ensures all job output is captured and visible via ffsh tail.
    
    Args:
        job_id: Job ID (Celery task ID)
        session_id: Session ID
        job_type: Job type (create_structured_data, train_es, etc.)
        
    Yields:
        tuple: (job_dir, original_cwd) - job directory and original working directory
    """
    from lib.job_manager import get_job_output_path
    import stat
    import socket
    
    job_dir = get_job_output_path(job_id, session_id, job_type)
    original_cwd = os.getcwd()
    
    # Ensure job directory exists
    job_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"📁 Job directory: {job_dir} (exists: {job_dir.exists()})")
    
    # Create logs directory IMMEDIATELY (before chdir) to ensure it exists
    logs_dir = job_dir / "logs"
    logger.info(f"📁 Attempting to create logs directory: {logs_dir}")
    
    try:
        # Force creation - don't rely on exist_ok silently failing
        if not logs_dir.exists():
            logs_dir.mkdir(parents=True, exist_ok=False, mode=0o755)
            logger.info(f"✅ Created logs directory: {logs_dir}")
        else:
            logger.info(f"✅ Logs directory already exists: {logs_dir}")
        
        # Verify it was created and is accessible
        if not logs_dir.exists():
            raise RuntimeError(f"logs_dir.mkdir() succeeded but directory doesn't exist: {logs_dir}")
        if not logs_dir.is_dir():
            raise RuntimeError(f"logs_dir exists but is not a directory: {logs_dir}")
        
        # Ensure directory is writable - fix permissions if needed
        current_mode = logs_dir.stat().st_mode
        if not (current_mode & stat.S_IWRITE):
            logger.warning(f"⚠️  Logs directory not writable, fixing permissions: {logs_dir}")
            logs_dir.chmod(0o755)
        
        # Test write access
        test_file = logs_dir / ".test_write"
        try:
            test_file.write_text("test")
            test_file.unlink()
            logger.info(f"✅ Logs directory is writable: {logs_dir}")
        except Exception as e:
            logger.error(f"❌ Logs directory is NOT writable: {e}")
            # Try to fix permissions on parent directory
            try:
                job_dir.chmod(0o755)
                logs_dir.chmod(0o755)
                # Try again
                test_file.write_text("test")
                test_file.unlink()
                logger.info(f"✅ Fixed permissions and verified writability")
            except Exception as e2:
                logger.error(f"❌ Still cannot write to logs directory after fixing permissions: {e2}")
                raise
        
        logger.info(f"📁 Logs directory ready: {logs_dir} (mode: {oct(logs_dir.stat().st_mode)})")
    except Exception as e:
        logger.error(f"❌ CRITICAL: Failed to create logs directory {logs_dir}: {e}")
        logger.error(f"   Exception type: {type(e).__name__}")
        logger.error(f"   job_dir: {job_dir} (exists: {job_dir.exists()})")
        logger.error(f"   job_dir parent: {job_dir.parent} (exists: {job_dir.parent.exists() if job_dir.parent else 'N/A'})")
        logger.error(f"   Traceback: {traceback.format_exc()}")
        # CRITICAL: This is a fatal error - we MUST have logs
        raise RuntimeError(f"Failed to create logs directory {logs_dir}: {e}") from e
    
    # Set up stdout_path
    stdout_path = logs_dir / "stdout.log"
    logger.info(f"📝 Log file will be: {stdout_path}")
    
    # Rotate old log file if it exists
    if stdout_path.exists():
        n = 1
        while (logs_dir / f"stdout.log.{n}").exists():
            n += 1
        stdout_path.rename(logs_dir / f"stdout.log.{n}")
    
    # Create README.txt documenting supported flags (if it doesn't exist)
    readme_path = job_dir / "README.txt"
    if not readme_path.exists():
        readme_content = """Job Control Flags
==================

This directory supports the following control flags:

ABORT
-----
Purpose: Stop a running job immediately and prevent automatic restart.
Usage: Create a file named "ABORT" in this directory.
Effect:
  - Job exits immediately when detected
  - Job is marked as FAILED
  - Job will NOT restart automatically
  - Recovery is blocked permanently

RESTART
-------
Purpose: Restart a job from scratch on next system startup.
Usage: Create a file named "RESTART" in this directory.
Effect (on worker startup):
  - Job is reset to READY status
  - All progress and recovery info is cleared
  - Job runs from the beginning
  - RESTART flag is renamed to started.RESTART.<date>
  - Jobs are processed newest first (by file modification time)

FINISH
------
Purpose: Gracefully stop training after current epoch completes.
Usage: Create a file named "FINISH" in this directory.
Effect:
  - Training completes current epoch
  - Model is saved
  - Job exits gracefully
  - FINISHED flag is created when done

NO_STOP
-------
Purpose: Disable early stopping for this job.
Usage: Create a file named "NO_STOP" in this directory.
Effect:
  - Early stopping mechanisms are disabled
  - Job will run for full number of epochs

PUBLISH
-------
Purpose: Save embedding_space.pickle during training for single predictor training.
Usage: Create a file named "PUBLISH" in this directory.
Effect:
  - Embedding space is saved as embedding_space.pickle in the job directory
  - Saved at the start of each epoch when flag is present
  - Can be used to train a single predictor before training completes
  - Flag can remain present - it will save once per epoch

PAUSE
-----
Purpose: Pause a running job gracefully (saves checkpoint and marks as PAUSED).
Usage: Create a file named "PAUSE" in this directory.
Effect:
  - Training completes current epoch/batch
  - Checkpoint is saved (if save_state_after_every_epoch is enabled)
  - Job is marked as PAUSED
  - Job exits gracefully (can be resumed later)
  - To resume: Remove PAUSE file and set job status to READY

Creating Flags
--------------
You can create flags using ffsh:

  ffsh jobs abort <job_path>
  ffsh jobs finish <job_path>
  ffsh jobs restart <job_path>
  ffsh jobs pause <job_path>
  ffsh jobs resume <job_path>

Where <job_path> can be:
  - <session_id>/<job_type>_<job_id> (full path)
  - <job_id> (just the job ID - will search all queues)

Or manually:
  touch <job_directory>/ABORT
  touch <job_directory>/RESTART
  touch <job_directory>/FINISH
  touch <job_directory>/PAUSE
  touch <job_directory>/NO_STOP
  touch <job_directory>/PUBLISH
"""
        try:
            readme_path.write_text(readme_content)
            logger.debug(f"📝 Created README.txt in job directory: {readme_path}")
        except Exception as e:
            logger.warning(f"⚠️  Failed to create README.txt: {e}")
    
    # Change to job directory AFTER logs directory is created
    os.chdir(job_dir)
    logger.info(f"📁 Changed to job directory: {os.getcwd()}")
    
    # Redirect stdout/stderr to log file
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers.copy()
    stdout_file = None
    
    try:
        stdout_file = open(stdout_path, 'w', buffering=1)
        sys.stdout = stdout_file
        sys.stderr = stdout_file
        
        # Update logging to use the file
        root_logger.handlers = []
        handler = logging.StreamHandler(stdout_file)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            f'%(asctime)s [{socket.gethostname()}] [%(levelname)-8s] %(name)-45s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)
        
        yield (job_dir, original_cwd)
    finally:
        # Flush before restoring
        if stdout_file:
            stdout_file.flush()
            os.fsync(stdout_file.fileno())  # Force write to disk
        
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        root_logger.handlers = original_handlers
        
        if stdout_file:
            stdout_file.close()
        
        # Change back to original directory
        os.chdir(original_cwd)
        logger.info(f"📁 Changed back to: {original_cwd}")
        
        # Verify file was created and write a marker if it's empty
        if stdout_path.exists():
            file_size = stdout_path.stat().st_size
            if file_size > 0:
                logger.debug(f"✅ Log file created: {stdout_path} ({file_size} bytes)")
            else:
                # File exists but is empty - write a marker
                try:
                    with open(stdout_path, 'a') as f:
                        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [{socket.gethostname()}] [INFO    ] celery_app: Log file initialized (no output captured)\n")
                        f.flush()
                        os.fsync(f.fileno())
                except Exception as e:
                    logger.warning(f"⚠️  Could not write to log file: {e}")
        else:
            logger.warning(f"⚠️  Log file was not created: {stdout_path}")


def log_task_return_value(result: dict, task_name: str, max_size: int = 10000):
    """
    Safely log task return values, truncating large values to avoid log spam.
    
    Args:
        result: The return value from a task (should be a dict)
        task_name: Name of the task for logging
        max_size: Maximum size of value to log (in characters)
    """
    if not isinstance(result, dict):
        logger.info(f"📤 {task_name} returning: {type(result).__name__} (not a dict, size: {len(str(result))})")
        return
    
    logger.info(f"📤 {task_name} RETURN VALUE:")
    logger.info(f"   success: {result.get('success', 'N/A')}")
    
    # Log output keys but truncate large values
    if 'output' in result:
        output = result['output']
        if isinstance(output, dict):
            logger.info(f"   output keys: {list(output.keys())}")
            for key, value in output.items():
                if isinstance(value, (str, Path)):
                    # Check if it's a file path
                    path_obj = Path(value) if isinstance(value, str) else value
                    if path_obj.exists():
                        size = path_obj.stat().st_size / 1024 / 1024  # MB
                        logger.info(f"      {key}: {value} ({size:.2f} MB)")
                    else:
                        logger.info(f"      {key}: {value} (file not found)")
                else:
                    value_str = str(value)
                    if len(value_str) > max_size:
                        logger.info(f"      {key}: {value_str[:max_size]}... (truncated, {len(value_str)} chars)")
                    else:
                        logger.info(f"      {key}: {value_str}")
        else:
            output_str = str(output)
            if len(output_str) > max_size:
                logger.info(f"   output: {output_str[:max_size]}... (truncated, {len(output_str)} chars)")
            else:
                logger.info(f"   output: {output_str}")
    
    # Log other important fields
    for key in ['job_id', 'session_id', 'error', 'traceback']:
        if key in result:
            value = result[key]
            value_str = str(value)
            if len(value_str) > max_size:
                logger.info(f"   {key}: {value_str[:max_size]}... (truncated, {len(value_str)} chars)")
            else:
                logger.info(f"   {key}: {value_str}")


def verify_output_files_exist(output: dict, task_name: str) -> bool:
    """
    Verify that output files exist before updating session.
    
    Args:
        output: Dict of output file paths
        task_name: Name of task for logging
        
    Returns:
        True if all file paths exist, False otherwise
    """
    all_exist = True
    logger.info(f"🔍 {task_name}: Verifying output files exist before session update...")
    
    for key, path in output.items():
        if path and isinstance(path, (str, Path)):
            path_obj = Path(path) if isinstance(path, str) else path
            if path_obj.exists():
                size = path_obj.stat().st_size / 1024 / 1024  # MB
                logger.info(f"   ✅ {key}: {path} ({size:.2f} MB)")
            else:
                logger.error(f"   ❌ {key}: {path} (FILE NOT FOUND)")
                all_exist = False
        elif path:
            # Not a path, just log it
            logger.info(f"   ℹ️  {key}: {path} (not a file path)")
    
    if all_exist:
        logger.info(f"✅ All output files verified")
    else:
        logger.error(f"❌ Some output files are missing - session update may fail!")
    
    return all_exist


# Worker startup hook - run job recovery when workers start
@worker_ready.connect
def on_worker_ready(sender=None, **kwargs):
    """
    Called when a Celery worker is ready to accept tasks.
    This is where we run job recovery to re-dispatch interrupted jobs.
    """
    # Only run recovery on one worker to avoid duplicate dispatches
    # Use a simple lock mechanism: first worker to check wins
    try:
        import redis
        redis_client = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
        
        # Try to acquire lock (expires in 60 seconds)
        lock_key = "celery:recovery:lock"
        lock_acquired = redis_client.set(lock_key, "locked", nx=True, ex=60)
        
        if lock_acquired:
            logger.info("🔍 Worker ready - running job recovery...")
            try:
                from lib.celery_job_recovery import recover_interrupted_jobs
                recovery_summary = recover_interrupted_jobs()
                logger.info(f"✅ Job recovery complete: {recovery_summary.get('total_recovered', 0)} jobs recovered")
            except Exception as recovery_error:
                logger.error(f"❌ Job recovery failed: {recovery_error}")
                logger.error(f"   Traceback: {traceback.format_exc()}")
        else:
            logger.debug("⏭️  Another worker is handling job recovery, skipping...")
    except Exception as e:
        logger.warning(f"⚠️  Could not run job recovery on worker startup: {e}")
        # Don't fail worker startup if recovery fails


@app.task(bind=True, name='celery_app.ping')
def ping(self, timestamp: float, queue_name: str = "unknown", echo_data: str = None):
    """
    Ping task for queue connectivity testing.
    
    This task can be sent to any queue to verify end-to-end connectivity.
    It echoes back the original request data to confirm the task was received and processed.
    
    Args:
        timestamp: Original request timestamp (to verify round-trip)
        queue_name: Name of queue this ping was sent to
        echo_data: Optional data to echo back (for verification)
        
    Returns:
        dict with ping response, original timestamp, and echoed data
    """
    import time
    response_time = time.time()
    round_trip = response_time - timestamp
    
    logger.info(f"🏓 PING received on queue '{queue_name}' - round trip: {round_trip*1000:.2f}ms")
    
    return {
        'status': 'pong',
        'queue': queue_name,
        'request_timestamp': timestamp,
        'response_timestamp': response_time,
        'round_trip_ms': round_trip * 1000,
        'worker': self.request.hostname if hasattr(self.request, 'hostname') else 'unknown',
        'echo': echo_data  # Echo back the original data
    }

@app.task(bind=True)
def predict_batch(self, session_id: str, records: list, prediction_options: dict = None):
    """
    Celery task for batch predictions.
    
    Args:
        session_id: Session ID with trained single predictor
        records: List of record dictionaries to predict
        prediction_options: Optional parameters (batch_size, etc.)
    
    Returns:
        dict with predictions or error info
    """
    import pickle
    from pathlib import Path
    
    logger.info(f"🚀 CELERY TASK STARTED - Session: {session_id}, Records: {len(records)}")
    
    try:
        # Update task state to indicate processing has started
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 0,
                'total': len(records),
                'status': 'Loading model...'
            }
        )
        
        # Paths already set up at module level - no need to repeat
        logger.info(f"🔧 Python paths already configured at module level")
        
        # Load the session and single predictor
        if not FEATRIX_QUEUE_AVAILABLE:
            raise ImportError("featrix_queue module not available")
            
        logger.info(f"🔧 Loading session {session_id}...")
        try:
            session = load_session(session_id)
            logger.info(f"✅ Session loaded successfully")
        except Exception as session_error:
            logger.error(f"❌ SESSION LOAD FAILED: {session_error}")
            logger.error(f"❌ Session traceback: {traceback.format_exc()}")
            raise
        
        # Get the single predictor path (backwards compatible)
        single_predictors = session.get("single_predictors")
        single_predictor = session.get("single_predictor")
        
        # Set prediction options (need this before accessing it below)
        options = prediction_options or {}
        
        # Helper function to generate predictor ID
        def generate_predictor_id(predictor_path: str) -> str:
            import hashlib
            import os
            filename = os.path.basename(predictor_path) if predictor_path else 'unknown'
            # Remove .pickle extension from user-facing ID
            if filename.endswith('.pickle'):
                filename = filename[:-7]
            path_hash = hashlib.md5(predictor_path.encode('utf-8')).hexdigest()[:8]
            return f"{filename}_{path_hash}"
        
        # NEW: Check if predictor_id or target_column specified in options
        requested_predictor_id = options.get('predictor_id')
        requested_target_column = options.get('target_column')
        logger.info(f"🔍 CELERY PREDICT_BATCH - predictor_id='{requested_predictor_id}', target_column='{requested_target_column}'")
        
        predictor_path = None
        if single_predictors and isinstance(single_predictors, list):
            # NEW: If multiple predictors exist, REQUIRE target_column or predictor_id
            if len(single_predictors) > 1 and not requested_predictor_id and not requested_target_column:
                # Get available targets for error message
                available_targets = []
                available_ids = []
                for pred_path in single_predictors:
                    # Get predictor_id
                    if Path(pred_path).exists():
                        available_ids.append(generate_predictor_id(pred_path))
                    
                    # Get target_column from metadata
                    metadata_path = str(Path(pred_path).parent / "model_metadata.json")
                    if Path(metadata_path).exists():
                        try:
                            import json
                            with open(metadata_path, 'r') as f:
                                metadata = json.load(f)
                                target_col = metadata.get('target_column')
                                if target_col:
                                    available_targets.append(target_col)
                        except Exception:
                            pass
                
                error_msg = f"Multiple predictors found ({len(single_predictors)}) - must specify 'target_column' or 'predictor_id'. Available targets: {available_targets}, Available IDs: {available_ids}"
                logger.error(f"❌ CELERY PREDICT_BATCH - {error_msg}")
                raise ValueError(error_msg)
            
            # PRIORITY 1: predictor_id (most precise)
            if requested_predictor_id:
                logger.info(f"🔍 CELERY PREDICT_BATCH - Looking for predictor with predictor_id='{requested_predictor_id}'")
                predictor_found = False
                available_predictor_ids = []
                
                for pred_path in single_predictors:
                    if Path(pred_path).exists():
                        current_predictor_id = generate_predictor_id(pred_path)
                        available_predictor_ids.append(current_predictor_id)
                        
                        if current_predictor_id == requested_predictor_id:
                            predictor_path = pred_path
                            predictor_found = True
                            logger.info(f"✅ CELERY PREDICT_BATCH - Found matching predictor by ID: {pred_path}")
                            break
                
                if not predictor_found:
                    raise ValueError(f"No predictor found for predictor_id '{requested_predictor_id}'. Available IDs: {available_predictor_ids}")
            
            # PRIORITY 2: target_column (semantic match)
            elif requested_target_column:
                logger.info(f"🔍 CELERY PREDICT_BATCH - Looking for predictor with target_column='{requested_target_column}'")
                predictor_found = False
                
                for pred_path in single_predictors:
                    # Skip None or invalid paths
                    if not pred_path:
                        logger.warning(f"⚠️  CELERY PREDICT_BATCH - Skipping None predictor path in list")
                        continue
                    
                    # Load predictor metadata to check target_column
                    metadata_path = str(Path(pred_path).parent / "model_metadata.json")
                    if Path(metadata_path).exists():
                        try:
                            import json
                            with open(metadata_path, 'r') as f:
                                metadata = json.load(f)
                                target_col = metadata.get('target_column')
                                
                                logger.info(f"🔍 CELERY PREDICT_BATCH - Checking predictor {pred_path}: target_column='{target_col}'")
                                
                                if target_col == requested_target_column:
                                    predictor_path = pred_path
                                    predictor_found = True
                                    logger.info(f"✅ CELERY PREDICT_BATCH - Found matching predictor: {pred_path}")
                                    break
                        except Exception as metadata_error:
                            logger.warning(f"⚠️  CELERY PREDICT_BATCH - Could not read metadata for {pred_path}: {metadata_error}")
                            continue
                
                if not predictor_found:
                    raise ValueError(f"No predictor found for target column '{requested_target_column}'")
            
            # PRIORITY 3: Single predictor fallback (backwards compatibility)
            else:
                # Only allow fallback if there's exactly one predictor
                if len(single_predictors) == 1:
                    predictor_path = single_predictors[0]
                    logger.info(f"🔍 CELERY PREDICT_BATCH - Single predictor session, using: {predictor_path}")
                else:
                    # This should never be reached due to check above, but keep for safety
                    raise ValueError(f"Multiple predictors found ({len(single_predictors)}) but no target_column or predictor_id specified")
        elif single_predictor:
            predictor_path = single_predictor
        else:
            raise ValueError("No single predictor found in session")
        
        if not predictor_path or not Path(predictor_path).exists():
            raise ValueError(f"Single predictor not found at: {predictor_path}")
        
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 0,
                'total': len(records),
                'status': 'Loading single predictor model...'
            }
        )
        
        # NEW APPROACH: Use subprocess to avoid all import/fork/CUDA issues
        logger.info(f"🚀 Using subprocess approach to avoid fork/CUDA issues")
        logger.info(f"📦 Predictor path: {predictor_path}")
        
        # Create temporary files for input/output
        import tempfile
        import uuid
        import subprocess
        import json
        import redis
        import time
        
        # Initialize Redis for progress monitoring
        try:
            redis_client = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
            redis_available = True
            logger.info(f"✅ Redis connected for progress monitoring")
        except Exception as redis_error:
            logger.warning(f"⚠️ Redis not available for progress monitoring: {redis_error}")
            redis_available = False
        
        temp_dir = Path("/tmp") / f"celery_prediction_{uuid.uuid4().hex[:8]}"
        temp_dir.mkdir(exist_ok=True)
        
        input_file = temp_dir / "input.json"
        output_file = temp_dir / "output.json"
        
        logger.info(f"📁 Created temp directory: {temp_dir}")
        
        # Set prediction options
        options = prediction_options or {}
        
        try:
            # Write input data to file
            with open(input_file, 'w') as f:
                json.dump({
                    'session_id': session_id,
                    'predictor_path': predictor_path,
                    'records': records,
                    'batch_size': options.get('batch_size', 256)
                }, f)
            logger.info(f"✅ Written {len(records)} records to {input_file}")
            
            # Run subprocess prediction
            script_path = Path(__file__).parent / "standalone_prediction.py"
            
            logger.info(f"🔧 Running subprocess: python {script_path} {input_file} {output_file}")
            
            # Use subprocess to call the standalone prediction script
            import sys
            
            # Get task ID for Redis progress tracking
            task_id = self.request.id
            redis_key = f"prediction_progress:{task_id}"
            
            # Start subprocess asynchronously - write output to log file to avoid pipe deadlock
            logger.info(f"🚀 Starting subprocess with Redis progress tracking...")
            
            # Create log files in temp directory
            subprocess_log = temp_dir / "subprocess.log"
            subprocess_err = temp_dir / "subprocess_error.log"
            
            with open(subprocess_log, 'w') as stdout_file, open(subprocess_err, 'w') as stderr_file:
                process = subprocess.Popen(
                    [sys.executable, str(script_path), str(input_file), str(output_file), task_id],
                    stdout=stdout_file,
                    stderr=stderr_file,
                    text=True
                )
                
                # Poll for subprocess completion while monitoring Redis progress
                start_time = time.time()
                last_progress_percentage = 0
                
                while process.poll() is None:
                    # Check for timeout (1 hour)
                    if time.time() - start_time > 3600:
                        process.terminate()
                        process.wait()
                        raise Exception("Prediction subprocess timed out after 1 hour")
                    
                    # Check Redis for progress updates
                    if redis_available:
                        try:
                            progress_data = redis_client.get(redis_key)
                            if progress_data:
                                progress_info = json.loads(progress_data)
                                current = progress_info.get('current', 0)
                                total = progress_info.get('total', 100)
                                status = progress_info.get('status', 'Processing...')
                                percentage = progress_info.get('percentage', 0)
                                
                                # Only update Celery state if progress percentage has changed
                                if percentage != last_progress_percentage:
                                    self.update_state(
                                        state='PROGRESS',
                                        meta={
                                            'current': current,
                                            'total': total,
                                            'status': status,
                                            'percentage': percentage,
                                            'timestamp': progress_info.get('timestamp')
                                        }
                                    )
                                    last_progress_percentage = percentage
                                    logger.info(f"📊 Relayed progress: {percentage}% - {status}")
                        except Exception as redis_err:
                            logger.warning(f"Failed to read progress from Redis: {redis_err}")
                    
                    # Sleep briefly to avoid busy polling
                    time.sleep(2)
            
            # Check final return code
            if process.returncode != 0:
                # Read error logs
                with open(subprocess_err, 'r') as f:
                    stderr_content = f.read()
                logger.error(f"❌ Subprocess failed with return code {process.returncode}")
                logger.error(f"❌ STDERR: {stderr_content}")
                raise Exception(f"Prediction subprocess failed: {stderr_content}")
            
            logger.info(f"✅ Subprocess completed successfully")
            
            # Log subprocess output for debugging
            if subprocess_log.exists():
                with open(subprocess_log, 'r') as f:
                    stdout_content = f.read()
                    if stdout_content:
                        logger.info(f"📊 Subprocess output logged to {subprocess_log}")
            
            # Read results from output file
            if not output_file.exists():
                raise Exception(f"Output file not created: {output_file}")
            
            with open(output_file, 'r') as f:
                result_data = json.load(f)
            
            logger.info(f"✅ Results loaded: {result_data.get('successful_predictions', 0)} successful predictions")
            
            # Handle both JSON Tables and legacy formats
            output_format = result_data.get('format', 'legacy')
            logger.info(f"📊 Output format: {output_format}")
            
            if output_format == 'json_tables' and 'results_table' in result_data:
                # Convert JSON Tables to legacy format for backward compatibility
                # But KEEP the results_table too for consistent API format
                try:
                    from jsontables import JSONTablesDecoder
                    
                    results_table = result_data['results_table']
                    records_with_predictions = JSONTablesDecoder.to_records(results_table)
                    
                    # Convert to legacy prediction format for backward compatibility
                    predictions = []
                    for i, record in enumerate(records_with_predictions):
                        # Extract prediction data from the enhanced record
                        prediction_obj = {
                            'row_index': record.get('row_index', i),
                            'prediction_id': None,  # Not stored in JSON Tables format
                            'error': record.get('prediction_error'),
                            'metadata': {}
                        }
                        
                        # Extract the actual prediction probabilities
                        if record.get('prediction_error') is None:
                            # Look for pred_* columns
                            prediction_probs = {}
                            for key, value in record.items():
                                if key.startswith('pred_') and key != 'pred_':
                                    class_name = key[5:]  # Remove 'pred_' prefix
                                    prediction_probs[class_name] = value
                            
                            if prediction_probs:
                                prediction_obj['prediction'] = prediction_probs
                            elif 'prediction' in record:
                                prediction_obj['prediction'] = record['prediction']
                            else:
                                prediction_obj['prediction'] = None
                                prediction_obj['error'] = "No prediction data found"
                            
                            # Add guardrails if available
                            if 'guardrails' in record:
                                prediction_obj['metadata']['guardrails'] = record['guardrails']
                        else:
                            prediction_obj['prediction'] = None
                        
                        predictions.append(prediction_obj)
                    
                    # Add legacy format alongside JSON Tables format
                    result_data['predictions'] = predictions
                    # Keep results_table as-is for consistent API format
                    logger.info(f"✅ Added legacy predictions format alongside JSON Tables: {len(predictions)} predictions")
                    
                except ImportError:
                    logger.warning(f"⚠️ JSON Tables not available for conversion, keeping raw format")
                except Exception as convert_error:
                    logger.warning(f"⚠️ Failed to convert JSON Tables format: {convert_error}")
                    # Keep the original format but log the issue
            
            elif output_format == 'legacy' and 'predictions' in result_data:
                logger.info(f"✅ Using legacy prediction format")
            else:
                logger.warning(f"⚠️ Unknown output format: {output_format}")
            
            # DON'T call update_state(state='SUCCESS') - Celery does this automatically
            # when the task returns. Calling it manually overwrites the return value!
            # Just update progress one final time with PROGRESS state
            self.update_state(
                state='PROGRESS',  # Use PROGRESS, not SUCCESS!
                meta={
                    'current': len(records),
                    'total': len(records),
                    'status': f"Completed: {result_data.get('successful_predictions', 0)} successful, {result_data.get('failed_predictions', 0)} failed",
                    'output_format': output_format,
                    'percentage': 100
                }
            )
            
            # Log what we're returning for debugging
            logger.info(f"📦 Returning result_data keys: {list(result_data.keys())}")
            logger.info(f"📦 results_table type: {type(result_data.get('results_table'))}")
            logger.info(f"📦 predictions count: {len(result_data.get('predictions', []))}")
            
            # Return the full result - Celery will automatically set state to SUCCESS
            return result_data
            
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Subprocess timed out after 1 hour")
            raise Exception("Prediction subprocess timed out")
            
        except Exception as subprocess_error:
            logger.error(f"❌ Subprocess error: {subprocess_error}")
            logger.error(f"❌ Subprocess traceback: {traceback.format_exc()}")
            raise Exception(f"Prediction subprocess failed: {subprocess_error}")
            
        finally:
            # Cleanup temp files
            try:
                if input_file.exists():
                    input_file.unlink()
                if output_file.exists():
                    output_file.unlink()
                temp_dir.rmdir()
                logger.info(f"✅ Cleaned up temp directory: {temp_dir}")
            except Exception as cleanup_err:
                logger.warning(f"⚠️ Failed to cleanup temp files: {cleanup_err}")

        
    except Exception as e:
        # Log the full error
        error_msg = str(e)
        error_traceback = traceback.format_exc()
        
        # Log to worker logs for debugging
        logger.error(f"CELERY WORKER ERROR: {error_msg}")
        logger.error(f"CELERY WORKER TRACEBACK:\n{error_traceback}")
        
        # Return error state instead of re-raising
        return {
            'success': False,
            'error': error_msg,
            'traceback': error_traceback,
            'session_id': session_id,
            'total_records': len(records) if 'records' in locals() else 0,
            'exc_type': type(e).__name__,
            'exc_message': str(e)
        }
        
    finally:
        # Minimal cleanup since subprocess handles GPU/model cleanup
        try:
            import gc
            gc.collect()
            logger.info(f"✅ Python garbage collection completed")
        except Exception as cleanup_error:
            logger.warning(f"Cleanup failed: {cleanup_error}")

@app.task(bind=True)
def project_training_movie_frame(self, job_spec: dict):
    """
    Celery task to generate a training movie frame from an embedding space checkpoint on CPU.
    
    This is triggered every time an ES checkpoint is saved (best model or epoch checkpoint).
    It loads the checkpoint, encodes points using the embedding space, and saves a single frame.
    
    Args:
        job_spec: Dict containing:
            - checkpoint_path: Path to model checkpoint (.pt file)
            - data_snapshot_path: Path to saved data sample (.json)
            - output_dir: Where to save the projection
            - session_id: Session ID
            - epoch: Epoch number
    
    Returns:
        dict with success status and output file path
    """
    from pathlib import Path
    from lib.featrix.neural.movie_frame_task import generate_movie_frame_on_cpu
    
    logger.info(f"🎬 CELERY PROJECT_TRAINING_MOVIE_FRAME STARTED - Session: {job_spec.get('session_id')}, Epoch: {job_spec.get('epoch')}")
    
    # Extract parameters early (needed for save_job)
    checkpoint_path = job_spec.get('checkpoint_path')
    data_snapshot_path = job_spec.get('data_snapshot_path')
    output_dir = job_spec.get('output_dir')
    session_id = job_spec.get('session_id', 'unknown')
    epoch = job_spec.get('epoch')
    
    # Save job to Redis for tracking (so ffsh can show job_type)
    job_id = self.request.id
    try:
        from lib.job_manager import save_job, JobStatus
        from datetime import datetime
        from zoneinfo import ZoneInfo
        save_job(
            job_id=job_id,
            job_data={
                'status': JobStatus.READY,
                'created_at': datetime.now(tz=ZoneInfo("America/New_York")),
                'job_spec': job_spec,
            },
            session_id=session_id,
            job_type='project_training_movie_frame'
        )
        logger.debug(f"✅ Saved project_training_movie_frame job {job_id} to Redis")
    except Exception as redis_err:
        logger.warning(f"⚠️  Could not save job to Redis: {redis_err}")
        # Continue anyway - job tracking is non-critical
    
    try:
        # Update task state
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Loading checkpoint...',
                'epoch': epoch,
                'session_id': session_id
            }
        )
        
        # Validate parameters
        if not checkpoint_path or not data_snapshot_path:
            raise ValueError("Missing required parameters in job_spec")
        
        # Validate checkpoint exists
        # NOTE: During recovery after restart/upgrade, checkpoint files may not exist
        # (cleaned up, never saved, or from old version). Movie frames are non-critical
        # visualizations - gracefully skip rather than crash.
        if not Path(checkpoint_path).exists():
            logger.warning(f"⚠️  Checkpoint not found: {checkpoint_path}")
            logger.warning(f"   This is normal during recovery after restart/upgrade")
            logger.warning(f"   Skipping movie frame generation for epoch {epoch}")
            return {
                'success': False,
                'error': 'Checkpoint not found (skipped during recovery)',
                'epoch': epoch,
                'session_id': session_id,
                'skipped': True  # Indicates graceful skip, not a failure
            }
        
        # Validate data snapshot exists
        if not Path(data_snapshot_path).exists():
            logger.warning(f"⚠️  Data snapshot not found: {data_snapshot_path}")
            logger.warning(f"   Skipping movie frame generation for epoch {epoch}")
            return {
                'success': False,
                'error': 'Data snapshot not found (skipped during recovery)',
                'epoch': epoch,
                'session_id': session_id,
                'skipped': True
            }
        
        logger.info(f"   Checkpoint: {checkpoint_path}")
        logger.info(f"   Data snapshot: {data_snapshot_path}")
        logger.info(f"   Output dir: {output_dir}")
        
        # Update job status to RUNNING
        try:
            from lib.job_manager import update_job_status, JobStatus
            update_job_status(job_id=job_id, status=JobStatus.RUNNING)
        except Exception as status_err:
            logger.debug(f"Could not update job status: {status_err}")
        
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Building projections...',
                'epoch': epoch
            }
        )
        
        # Call the existing movie frame generation function
        # This handles loading checkpoint, encoding points, and saving projections
        output_file = generate_movie_frame_on_cpu(
            checkpoint_path=checkpoint_path,
            data_snapshot_path=data_snapshot_path,
            epoch=epoch,
            output_dir=output_dir,
            session_id=session_id
        )
        
        if output_file:
            logger.info(f"✅ Projections built successfully: {output_file}")
            
            # Update job status to DONE
            try:
                from lib.job_manager import update_job_status, JobStatus
                update_job_status(job_id=job_id, status=JobStatus.DONE)
            except Exception as status_err:
                logger.debug(f"Could not update job status: {status_err}")
            
            return {
                'success': True,
                'output_file': output_file,
                'epoch': epoch,
                'session_id': session_id
            }
        else:
            raise Exception("Projection building returned None")
            
    except Exception as e:
        logger.error(f"❌ PROJECT_TRAINING_MOVIE_FRAME FAILED: {e}")
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        
        # Update job status to FAILED
        try:
            from lib.job_manager import update_job_status, JobStatus
            update_job_status(job_id=job_id, status=JobStatus.FAILED, metadata={'error': str(e)})
        except Exception as status_err:
            logger.debug(f"Could not update job status: {status_err}")
        
        return {
            'success': False,
            'error': str(e),
            'epoch': epoch,
            'session_id': session_id,
            'traceback': traceback.format_exc()
        }

@app.task(bind=True)
def create_structured_data(self, job_spec: dict, job_id: str, data_file: str = None, session_id: str = None):
    """
    Celery task to create structured data from raw input (CSV/JSON).
    
    This processes the input data file, creates the SQLite database, and prepares
    the data for embedding space training.
    
    Args:
        job_spec: Dict containing job parameters (column_overrides, s3 paths, etc.)
        job_id: Job identifier
        data_file: Path to input data file (CSV/JSON)
        session_id: Session ID
    
    Returns:
        dict with output paths (sqlite_db, structured_data, etc.)
    """
    from pathlib import Path
    
    import time
    import uuid
    import datetime
    task_start = time.time()
    celery_trace_id = f"CELERY-{uuid.uuid4().hex[:8]}"
    # Use Celery task ID if job_id not provided
    if not job_id:
        job_id = self.request.id
        logger.info(f"   Using Celery task ID as job_id: {job_id}")
    
    logger.info(f"\n{'='*80}")
    logger.info(f"🔵 [CELERY] {celery_trace_id} CREATE_STRUCTURED_DATA TASK STARTED")
    logger.info(f"   Timestamp: {datetime.datetime.now().isoformat()}")
    logger.info(f"   Job ID: {job_id}")
    logger.info(f"   Session ID: {session_id}")
    logger.info(f"   Data file: {data_file}")
    logger.info(f"   Job spec keys: {list(job_spec.keys()) if job_spec else 'None'}")
    logger.info(f"   Task ID: {self.request.id}")
    logger.info(f"{'='*80}")
    
    # CRITICAL: Wrap entire task in try/except to catch ANY unhandled exceptions
    try:
        logger.info(f"   📍 TRACE: Entered main try block")
        # Update task state
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Loading data...',
                'job_id': job_id,
                'session_id': session_id
            }
        )
        
        # Import here to avoid CUDA fork issues
        from lib.structureddata import CSVtoDB
        import boto3
        from urllib.parse import urlparse
        
        # Check if this is an embedding space job with S3 datasets
        s3_training_path = job_spec.get("s3_training_dataset")
        s3_validation_path = job_spec.get("s3_validation_dataset")
        name = job_spec.get("name", "embedding_space")
        
        # Handle S3 datasets for embedding space sessions
        if s3_training_path and s3_validation_path:
            logger.info(f"📥 Downloading S3 data for embedding space: {name}")
            
            # Check if paths are local files (not S3)
            if not s3_training_path.startswith('s3://') or not s3_validation_path.startswith('s3://'):
                # Local files - use them directly
                training_local_path = Path(s3_training_path)
                validation_local_path = Path(s3_validation_path)
                
                if not training_local_path.exists():
                    raise ValueError(f"Training file not found: {training_local_path}")
                if not validation_local_path.exists():
                    raise ValueError(f"Validation file not found: {validation_local_path}")
                
                logger.info(f"Using local training file: {training_local_path}")
                logger.info(f"Using local validation file: {validation_local_path}")
                
                # Use the training data as the data_file for processing
                data_file = str(training_local_path)
            else:
                # S3 paths - download them
                training_parsed = urlparse(s3_training_path)
                validation_parsed = urlparse(s3_validation_path)
                
                if training_parsed.scheme != 's3' or validation_parsed.scheme != 's3':
                    raise ValueError("S3 URLs must start with 's3://'")
                
                training_bucket = training_parsed.netloc
                training_key = training_parsed.path.lstrip('/')
                validation_bucket = validation_parsed.netloc
                validation_key = validation_parsed.path.lstrip('/')
                
                # Get session directory for downloads
                from lib.session_manager import load_session
                session = load_session(session_id)
                session_dir = Path(session.get('input_data', '')).parent if session.get('input_data') else Path(config.data_dir) / "es_train" / session_id
                session_dir.mkdir(parents=True, exist_ok=True)
                
                # Set up local file paths
                training_local_path = session_dir / f"{name}_training_data.csv"
                validation_local_path = session_dir / f"{name}_validation_data.csv"
                
                try:
                    # Initialize S3 client
                    s3_client = boto3.client('s3')
                    
                    # Download training dataset
                    logger.info(f"📥 Downloading training dataset from s3://{training_bucket}/{training_key}")
                    s3_client.download_file(training_bucket, training_key, str(training_local_path))
                    logger.info(f"✅ Training dataset downloaded to {training_local_path}")
                    
                    # Download validation dataset
                    logger.info(f"📥 Downloading validation dataset from s3://{validation_bucket}/{validation_key}")
                    s3_client.download_file(validation_bucket, validation_key, str(validation_local_path))
                    logger.info(f"✅ Validation dataset downloaded to {validation_local_path}")
                    
                    # Use the downloaded training data as the data_file for processing
                    data_file = str(training_local_path)
                    
                except Exception as e:
                    logger.error(f"❌ Error downloading S3 data: {e}")
                    raise
        
        # Check if data_file is an S3 URL and download it first
        elif data_file and isinstance(data_file, str) and data_file.startswith('s3://'):
            logger.info(f"📥 Downloading S3 data: {data_file}")
            
            # Parse S3 URL
            parsed = urlparse(data_file)
            if parsed.scheme != 's3':
                raise ValueError("S3 URL must start with 's3://'")
            
            bucket = parsed.netloc
            key = parsed.path.lstrip('/')
            
            # Set up local file path - preserve original extension
            local_filename = Path(key).name
            # Keep original extension if it's a supported format, otherwise default to .csv
            if not local_filename.lower().endswith(('.csv', '.parquet', '.json', '.jsonl')):
                local_filename += '.csv'
            
            # Get session directory for download
            from lib.session_manager import load_session
            session = load_session(session_id)
            session_dir = Path(session.get('input_data', '')).parent if session.get('input_data') else Path(config.data_dir) / session_id
            session_dir.mkdir(parents=True, exist_ok=True)
            
            data_file_path = session_dir / local_filename
            
            try:
                # Initialize S3 client and download
                s3_client = boto3.client('s3')
                logger.info(f"📥 Downloading from s3://{bucket}/{key} to {data_file_path}")
                s3_client.download_file(bucket, key, str(data_file_path))
                logger.info(f"✅ S3 download completed: {data_file_path}")
                data_file = str(data_file_path)
                
            except Exception as e:
                logger.error(f"❌ Error downloading S3 data: {e}")
                raise
        
        # Convert data_file to Path if provided
        data_file_path = Path(data_file) if data_file else None
        
        if not data_file_path or not data_file_path.exists():
            raise FileNotFoundError(f"Data file not found: {data_file_path}")
        
        # Extract JSON analysis configuration from job spec (if provided)
        json_analysis_config = job_spec.get("json_analysis_config", {})
        
        # STANDARD JOB SETUP - creates job dir, logs dir, and redirects stdout/stderr
        with setup_job_logging(job_id, session_id, 'create_structured_data') as (job_dir, original_cwd):
                # Call CSVtoDB directly (replaces run_create_structured_data from featrix_queue)
                logger.info(f"🔄 STEP 1/3: Initializing CSVtoDB processor...")
                c2d = CSVtoDB(
                    column_overrides=job_spec.get("column_overrides", {}),
                    json_analysis_config=json_analysis_config
                )
                
                # Set db_path to current directory (job directory)
                c2d.db_path = str(Path.cwd() / "embedding_space.db")
                
                logger.info(f"🔄 STEP 2/3: Starting CSV/JSON to SQLite conversion...")
                logger.info(f"   📄 Input file: {data_file_path}")
                logger.info(f"   💾 Output DB: {c2d.db_path}")
                file_size_mb = data_file_path.stat().st_size / 1024 / 1024
                logger.info(f"   📊 File size: {file_size_mb:.2f} MB ({data_file_path.stat().st_size:,} bytes)")
                
                # Update task state to show we're processing
                self.update_state(
                    state='PROGRESS',
                    meta={
                        'status': f'Processing {file_size_mb:.1f} MB file...',
                        'job_id': job_id,
                        'session_id': session_id,
                        'input_file': str(data_file_path),
                        'stage': 'Reading and processing data file'
                    }
                )
                
                logger.info(f"📊 Processing data file (reading, parsing, cleaning, expanding JSON columns, writing to SQLite)...")
                logger.info(f"   This may take a while for large files - watch for progress updates below...")
                c2d.csv_to_sqlite(csv_path=str(data_file_path))
                
                logger.info(f"✅ STEP 2/3 COMPLETE: CSV to SQLite conversion finished")
                logger.info(f"🔄 STEP 3/3: Gathering output files...")
                logger.info(f"   📍 TRACE: About to call c2d.get_output_files()...")
                output = c2d.get_output_files()
                logger.info(f"   📍 TRACE: c2d.get_output_files() returned, type: {type(output)}")
                logger.info(f"✅ Output files generated: {list(output.keys())}")
                logger.info(f"   📍 TRACE: About to iterate over {len(output)} output items...")
                # Only check file paths, not metadata (lists/dicts)
                file_path_keys = ['sqlite_db', 'strings_cache', 'vector_db_path']
                try:
                    for key, value in output.items():
                        try:
                            if key in file_path_keys:
                                # This is a file path - check if it exists
                                if value and isinstance(value, (str, Path)):
                                    path_obj = Path(value)
                                    if path_obj.exists():
                                        size = path_obj.stat().st_size / 1024 / 1024
                                        logger.info(f"   • {key}: {value} ({size:.2f} MB)")
                                    else:
                                        logger.info(f"   • {key}: {value} (file not found)")
                                else:
                                    logger.info(f"   • {key}: {value} (invalid path type: {type(value).__name__})")
                            else:
                                # This is metadata (list/dict) - just log the type and size
                                if isinstance(value, (list, dict)):
                                    if isinstance(value, list):
                                        logger.info(f"   • {key}: list with {len(value)} items")
                                    else:
                                        logger.info(f"   • {key}: dict with {len(value)} keys")
                                else:
                                    logger.info(f"   • {key}: {type(value).__name__} = {value}")
                        except Exception as file_err:
                            logger.error(f"   ❌ Error logging output item {key}: {file_err}")
                            logger.error(f"   Traceback: {traceback.format_exc()}")
                    logger.info(f"   📍 TRACE: Finished iterating over output items")
                except Exception as loop_err:
                    logger.error(f"   ❌ CRITICAL: Exception in output items loop: {loop_err}")
                    logger.error(f"   Traceback: {traceback.format_exc()}")
                    raise
                logger.info(f"   📍 TRACE: Finished logging output files, about to exit with block")
                logger.info(f"   📍 TRACE: Flushing logs before exiting with block...")
                import sys
                sys.stdout.flush()
                sys.stderr.flush()
                logger.info(f"   📍 TRACE: Logs flushed, exiting with block now...")
        
        logger.info(f"   📍 TRACE: Exited with block, checking if output variable exists...")
        logger.info(f"   📍 TRACE: output variable exists: {'output' in locals()}")
        if 'output' not in locals():
            logger.error(f"   ❌ CRITICAL: output variable does not exist after with block!")
            raise RuntimeError("output variable was not set - this should never happen")
        logger.info(f"   📍 TRACE: About to verify output files exist...")
        # Verify output files exist before updating session
        verify_output_files_exist(output, "CREATE_STRUCTURED_DATA")
        logger.info(f"   📍 TRACE: Output files verified, about to update session...")
        
        # Update session with output (matching file-based queue behavior)
        # CRITICAL: Wrap in try/except to ensure dispatch happens even if session update fails
        logger.info(f"   📍 TRACE: Starting session update block...")
        session_updated = False
        try:
            logger.info(f"   📍 TRACE: About to import load_session, save_session...")
            from lib.session_manager import load_session, save_session
            logger.info(f"   📍 TRACE: Imports successful, about to load session...")
            logger.info(f"🔄 Loading session {session_id} to update with output files...")
            logger.info(f"   📍 TRACE: Calling load_session({session_id})...")
            session = load_session(session_id)
            logger.info(f"   📍 TRACE: load_session() returned, type: {type(session)}")
            logger.info(f"   ✅ Session loaded successfully")
            logger.info(f"   Session keys before update: {list(session.keys())}")
            logger.info(f"   Updating with output keys: {list(output.keys())}")
            logger.info(f"   📍 TRACE: About to merge session and output...")
            session = {**session, **output}
            logger.info(f"   📍 TRACE: Session merged, about to save...")
            logger.info(f"   Saving session...")
            logger.info(f"   📍 TRACE: Calling save_session(session_id={session_id}, exist_ok=True)...")
            save_session(session_id=session_id, session_doc=session, exist_ok=True)
            logger.info(f"   📍 TRACE: save_session() returned successfully")
            session_updated = True
            logger.info(f"✅ Session updated with structured data output")
            logger.info(f"   sqlite_db: {output.get('sqlite_db')}")
            logger.info(f"   strings_cache: {output.get('strings_cache')}")
            # Verify the update worked
            logger.info(f"   📍 TRACE: About to verify session update by reloading...")
            session_check = load_session(session_id)
            logger.info(f"   📍 TRACE: Session reloaded for verification")
            if session_check.get('sqlite_db'):
                logger.info(f"   ✅ Verified: sqlite_db is now in session")
            else:
                logger.error(f"   ❌ WARNING: sqlite_db NOT found in session after update!")
            logger.info(f"   📍 TRACE: Session update block completed successfully")
        except Exception as session_error:
            logger.error(f"   📍 TRACE: EXCEPTION in session update block!")
            logger.error(f"   📍 TRACE: Exception type: {type(session_error).__name__}")
            logger.error(f"   📍 TRACE: Exception message: {str(session_error)}")
            logger.error(f"❌ CRITICAL: Failed to update session with output: {session_error}")
            logger.error(f"   Error type: {type(session_error).__name__}")
            logger.error(f"   Full traceback: {traceback.format_exc()}")
            logger.error(f"   Output files were generated but session was not updated!")
            logger.error(f"   This may prevent next job from being dispatched.")
            # Continue anyway - we'll try to dispatch with what we have
        logger.info(f"   📍 TRACE: Exited session update try/except, session_updated={session_updated}")
        
        # Automatically dispatch next job in chain
        # CRITICAL: Always try to dispatch, even if session update failed
        # The dispatch function will reload the session, so it may still work
        logger.info(f"   📍 TRACE: About to start dispatch block...")
        try:
            logger.info(f"   📍 TRACE: Inside dispatch try block...")
            logger.info(f"🔄 Attempting to dispatch next job in chain for session {session_id}...")
            logger.info(f"   Session was updated: {session_updated}")
            logger.info(f"   📍 TRACE: About to import dispatch_next_job_in_chain...")
            from lib.session_chains import dispatch_next_job_in_chain
            logger.info(f"   📍 TRACE: Import successful, about to call dispatch_next_job_in_chain...")
            logger.info(f"   📍 TRACE: Calling dispatch_next_job_in_chain(session_id={session_id}, completed_job_type='create_structured_data')...")
            next_task_id = dispatch_next_job_in_chain(session_id, completed_job_type='create_structured_data')
            logger.info(f"   📍 TRACE: dispatch_next_job_in_chain() returned: {next_task_id}")
            if next_task_id:
                logger.info(f"✅ Successfully dispatched next job in chain (task_id: {next_task_id})")
            else:
                logger.info(f"ℹ️  No next job to dispatch (all jobs complete or no more jobs in plan)")
                # Log job_plan for debugging
                try:
                    logger.info(f"   📍 TRACE: About to load session for debugging...")
                    from lib.session_manager import load_session
                    session_debug = load_session(session_id)
                    job_plan = session_debug.get('job_plan', [])
                    logger.info(f"   Debug: job_plan has {len(job_plan)} jobs")
                    for idx, job_desc in enumerate(job_plan):
                        job_type = job_desc.get('job_type', 'unknown')
                        job_id = job_desc.get('job_id', 'None')
                        logger.info(f"     {idx}: {job_type} - job_id: {job_id}")
                except Exception as debug_err:
                    logger.warning(f"   Could not load session for debugging: {debug_err}")
            logger.info(f"   📍 TRACE: Dispatch block completed successfully")
        except Exception as chain_error:
            logger.error(f"   📍 TRACE: EXCEPTION in dispatch block!")
            logger.error(f"   📍 TRACE: Exception type: {type(chain_error).__name__}")
            logger.error(f"   📍 TRACE: Exception message: {str(chain_error)}")
            logger.error(f"❌ CRITICAL: Failed to dispatch next job in chain: {chain_error}")
            logger.error(f"   Full traceback: {traceback.format_exc()}")
            # Don't fail the entire task if chain dispatch fails - job completed successfully
        logger.info(f"   📍 TRACE: Exited dispatch try/except block")
        
        # CRITICAL: Verify output files actually exist in job directory before marking as DONE
        # This prevents jobs from being marked SUCCESS when they didn't actually write files
        logger.info(f"   📍 TRACE: Verifying output files exist in job directory before marking as DONE...")
        from lib.job_manager import get_job_output_path
        try:
            job_dir = get_job_output_path(job_id, session_id, 'create_structured_data')
            sqlite_db_path = job_dir / "embedding_space.db"
            strings_cache_path = job_dir / "strings.sqlite3"
            
            files_exist = True
            if not sqlite_db_path.exists():
                logger.error(f"❌❌❌ CRITICAL: sqlite_db file does not exist: {sqlite_db_path}")
                logger.error(f"   Job directory: {job_dir}")
                logger.error(f"   Job will be marked as FAILED, not DONE")
                files_exist = False
            else:
                size_mb = sqlite_db_path.stat().st_size / 1024 / 1024
                logger.info(f"   ✅ sqlite_db exists: {sqlite_db_path} ({size_mb:.2f} MB)")
            
            # strings.sqlite3 is optional (only created if there are string columns)
            if strings_cache_path.exists():
                size_mb = strings_cache_path.stat().st_size / 1024 / 1024
                logger.info(f"   ✅ strings_cache exists: {strings_cache_path} ({size_mb:.2f} MB)")
            else:
                logger.info(f"   ℹ️  strings_cache not found (expected if no string columns): {strings_cache_path}")
            
            if not files_exist:
                # Mark job as FAILED if critical files don't exist
                logger.error(f"❌❌❌ JOB FAILED: Output files do not exist in job directory")
                try:
                    from lib.job_manager import update_job_status, JobStatus
                    update_job_status(job_id=job_id, status=JobStatus.FAILED, metadata={
                        'error': 'Output files not found in job directory',
                        'expected_sqlite_db': str(sqlite_db_path),
                        'job_dir': str(job_dir)
                    })
                    logger.error(f"✅ Updated job {job_id} status to FAILED")
                except Exception as status_err:
                    logger.error(f"❌ Failed to update job status to FAILED: {status_err}")
                
                # Raise exception to mark Celery task as FAILED
                raise FileNotFoundError(
                    f"Output files not found in job directory {job_dir}. "
                    f"Expected sqlite_db at {sqlite_db_path} but file does not exist. "
                    f"Job cannot be marked as successful."
                )
        except FileNotFoundError:
            # Re-raise if it's our validation error
            raise
        except Exception as verify_err:
            logger.error(f"❌ Error verifying output files: {verify_err}")
            logger.error(f"   Traceback: {traceback.format_exc()}")
            # Don't fail the job if verification itself fails - but log loudly
            logger.error(f"⚠️  WARNING: Could not verify output files, but continuing anyway")
        
        logger.info(f"   📍 TRACE: About to log 'Structured data created successfully'...")
        logger.info(f"✅ Structured data created successfully")
        
        # Update job status to DONE when completed successfully
        logger.info(f"   📍 TRACE: About to update job status to DONE...")
        try:
            logger.info(f"   📍 TRACE: About to import update_job_status...")
            from lib.job_manager import update_job_status, JobStatus
            logger.info(f"   📍 TRACE: Import successful, about to call update_job_status...")
            update_job_status(job_id=job_id, status=JobStatus.DONE)
            logger.info(f"   📍 TRACE: update_job_status() returned")
            logger.info(f"✅ Updated job {job_id} status to DONE")
        except Exception as status_err:
            logger.warning(f"⚠️  Failed to update job {job_id} status to DONE: {status_err}")
            logger.warning(f"   Error: {traceback.format_exc()}")
        logger.info(f"   📍 TRACE: Job status update block completed")
        
        task_elapsed = time.time() - task_start
        logger.info(f"   📍 TRACE: About to log 'JOB FINISHED'...")
        logger.info(f"🏁 JOB {job_id} FINISHED")
        logger.info(f"🔵 [CELERY] {celery_trace_id} CREATE_STRUCTURED_DATA TASK COMPLETED")
        logger.info(f"   Elapsed time: {task_elapsed:.2f} seconds")
        logger.info(f"   Job ID: {job_id}")
        logger.info(f"   Session ID: {session_id}")
        logger.info(f"{'='*80}\n")
        
        logger.info(f"   📍 TRACE: About to create return value dict...")
        result = {
            'success': True,
            'output': output,
            'job_id': job_id,
            'session_id': session_id
        }
        logger.info(f"   📍 TRACE: Return value dict created, about to log it...")
        log_task_return_value(result, "CREATE_STRUCTURED_DATA")
        logger.info(f"   📍 TRACE: Return value logged, about to return...")
        logger.info(f"   📍 TRACE: RETURNING FROM create_structured_data TASK")
        return result
        
    except Exception as e:
        # SCREAM LOUDLY - This is a critical failure that needs immediate attention
        logger.error(f"")
        logger.error(f"╔════════════════════════════════════════════════════════════════════════════════╗")
        logger.error(f"║                                                                                ║")
        logger.error(f"║  💥💥💥 CRITICAL TASK FAILURE - CREATE_STRUCTURED_DATA CRASHED 💥💥💥          ║")
        logger.error(f"║                                                                                ║")
        logger.error(f"╚════════════════════════════════════════════════════════════════════════════════╝")
        logger.error(f"")
        logger.error(f"❌❌❌ CREATE_STRUCTURED_DATA FAILED WITH UNHANDLED EXCEPTION ❌❌❌")
        logger.error(f"")
        logger.error(f"   Job ID: {job_id}")
        logger.error(f"   Session ID: {session_id}")
        logger.error(f"   Exception Type: {type(e).__name__}")
        logger.error(f"   Exception Message: {str(e)}")
        logger.error(f"")
        logger.error(f"   📍 TRACE: Exception caught in outer try/except block")
        logger.error(f"   📍 TRACE: This means the task crashed before completing")
        logger.error(f"")
        logger.error(f"   FULL TRACEBACK:")
        logger.error(f"   {'='*100}")
        logger.error(f"   {traceback.format_exc()}")
        logger.error(f"   {'='*100}")
        logger.error(f"")
        
        # Update job status to FAILED when it fails
        try:
            logger.error(f"   📍 TRACE: Attempting to update job status to FAILED...")
            from lib.job_manager import update_job_status, JobStatus
            update_job_status(job_id=job_id, status=JobStatus.FAILED)
            logger.error(f"   ✅ Updated job {job_id} status to FAILED")
        except Exception as status_err:
            logger.error(f"   ❌❌❌ FAILED TO UPDATE JOB STATUS TO FAILED ❌❌❌")
            logger.error(f"   Error: {status_err}")
            logger.error(f"   Traceback: {traceback.format_exc()}")
        
        logger.error(f"")
        logger.error(f"🏁 JOB {job_id} FINISHED (WITH ERRORS)")
        logger.error(f"")
        
        result = {
            'success': False,
            'error': str(e),
            'job_id': job_id,
            'session_id': session_id,
            'traceback': traceback.format_exc()
        }
        log_task_return_value(result, "CREATE_STRUCTURED_DATA")
        return result

@app.task(bind=True)
def run_clustering(self, job_spec: dict):
    """
    Celery task to run clustering/projections for an embedding space.
    
    This generates the final projections and preview image for a trained embedding space.
    
    Args:
        job_spec: Dict containing:
            - model_path: Path to embedding space model (.pickle)
            - sqlite_db: Path to SQLite database
            - strings_cache: Path to strings cache (optional)
    
    Returns:
        dict with output paths (projections, preview_png)
    """
    from pathlib import Path
    
    logger.info(f"🔍 CELERY RUN_CLUSTERING STARTED")
    
    try:
        # Update task state
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Loading embedding space...',
                'model_path': job_spec.get('model_path')
            }
        )
        
        # Import here to avoid CUDA fork issues
        from lib.es_projections import run_clustering
        
        # Extract parameters
        model_path = job_spec['model_path']
        sqlite_db = job_spec['sqlite_db']
        strings_cache = job_spec.get('strings_cache')
        
        logger.info(f"   Model path: {model_path}")
        logger.info(f"   SQLite DB: {sqlite_db}")
        
        # Get job_id and session_id for logging setup
        job_id = job_spec.get('job_id') or self.request.id
        session_id = job_spec.get('session_id')
        
        # STANDARD JOB SETUP - creates job dir, logs dir, and redirects stdout/stderr
        with setup_job_logging(job_id, session_id, 'run_clustering') as (job_dir, original_cwd):
            # Update progress
            self.update_state(
                state='PROGRESS',
                meta={
                    'status': 'Running clustering...',
                }
            )
            
            # Call run_clustering directly (replaces run_clustering_job from featrix_queue)
            output = run_clustering(
                model_path=model_path,
                sqlite_db_path=sqlite_db
            )
        
        # Update session with output (matching file-based queue behavior)
        session_id = job_spec.get('session_id')
        if session_id:
            from lib.session_manager import load_session, save_session
            try:
                session = load_session(session_id)
                session = {**session, **output}
                save_session(session_id=session_id, session_doc=session, exist_ok=True)
                logger.info(f"✅ Session updated with clustering output")
                
                # Automatically dispatch next job in chain
                try:
                    logger.info(f"🔄 Attempting to dispatch next job in chain for session {session_id}...")
                    from lib.session_chains import dispatch_next_job_in_chain
                    next_task_id = dispatch_next_job_in_chain(session_id, completed_job_type='run_clustering')
                    if next_task_id:
                        logger.info(f"✅ Successfully dispatched next job in chain (task_id: {next_task_id})")
                    else:
                        logger.info(f"ℹ️  No next job to dispatch (all jobs complete or no more jobs in plan)")
                except Exception as chain_error:
                    logger.error(f"❌ CRITICAL: Failed to dispatch next job in chain: {chain_error}")
                    logger.error(f"   Full traceback: {traceback.format_exc()}")
            except Exception as session_error:
                logger.error(f"❌ CRITICAL: Failed to update session {session_id} with output: {session_error}")
                logger.error(f"   Full traceback: {traceback.format_exc()}")
                logger.error(f"   Output files were generated but session was not updated!")
        
        logger.info(f"✅ Clustering completed successfully")
        
        # Update job status to DONE when completed successfully
        try:
            job_id = job_spec.get('job_id') or self.request.id
            if job_id:
                from lib.job_manager import update_job_status, JobStatus
                update_job_status(job_id=job_id, status=JobStatus.DONE)
                logger.info(f"✅ Updated job {job_id} status to DONE")
        except Exception as status_err:
            logger.warning(f"⚠️  Failed to update job status to DONE: {status_err}")
            logger.warning(f"   Error: {traceback.format_exc()}")
        
        result = {
            'success': True,
            'output': output
        }
        log_task_return_value(result, "RUN_CLUSTERING")
        return result
        
    except Exception as e:
        # SCREAM LOUDLY - This is a critical failure that needs immediate attention
        job_id = job_spec.get('job_id') or self.request.id
        logger.error(f"")
        logger.error(f"╔════════════════════════════════════════════════════════════════════════════════╗")
        logger.error(f"║                                                                                ║")
        logger.error(f"║  💥💥💥 CRITICAL TASK FAILURE - RUN_CLUSTERING CRASHED 💥💥💥                    ║")
        logger.error(f"║                                                                                ║")
        logger.error(f"╚════════════════════════════════════════════════════════════════════════════════╝")
        logger.error(f"")
        logger.error(f"❌❌❌ RUN_CLUSTERING FAILED WITH UNHANDLED EXCEPTION ❌❌❌")
        logger.error(f"")
        logger.error(f"   Job ID: {job_id}")
        logger.error(f"   Exception Type: {type(e).__name__}")
        logger.error(f"   Exception Message: {str(e)}")
        logger.error(f"")
        logger.error(f"   FULL TRACEBACK:")
        logger.error(f"   {'='*100}")
        logger.error(f"   {traceback.format_exc()}")
        logger.error(f"   {'='*100}")
        logger.error(f"")
        
        # Update job status to FAILED when it fails
        try:
            if job_id:
                from lib.job_manager import update_job_status, JobStatus
                update_job_status(job_id=job_id, status=JobStatus.FAILED)
                logger.error(f"   ✅ Updated job {job_id} status to FAILED")
        except Exception as status_err:
            logger.error(f"   ❌❌❌ FAILED TO UPDATE JOB STATUS TO FAILED ❌❌❌")
            logger.error(f"   Error: {status_err}")
            logger.error(f"   Traceback: {traceback.format_exc()}")
        
        logger.error(f"")
        
        result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        log_task_return_value(result, "RUN_CLUSTERING")
        return result

@app.task(bind=True)
def train_single_predictor(self, *args, **kwargs):
    """
    Celery task to train a single predictor on a foundation model.
    
    This trains a supervised learning model on top of a pre-trained embedding space.
    
    When called in a chain, receives: (previous_result, job_spec, job_id, session_id)
    When called directly, receives: (job_spec, job_id, session_id)
    
    Returns:
        dict with output paths (single_predictor, training_metrics)
    """
    from pathlib import Path
    
    # Handle both chain and direct call patterns
    # Chain: (previous_result, job_spec, job_id, session_id)
    # Direct: (job_spec, job_id, session_id)
    if len(args) == 4:
        # Called from chain: (previous_result, job_spec, job_id, session_id)
        previous_result, job_spec, job_id, session_id = args
        logger.info(f"📥 Called from chain - previous task result: {type(previous_result)}")
    elif len(args) == 3:
        # Called directly: (job_spec, job_id, session_id)
        job_spec, job_id, session_id = args
        previous_result = None
    else:
        # Try to get from kwargs or use defaults
        job_spec = kwargs.get('job_spec') or (args[0] if len(args) > 0 else None)
        job_id = kwargs.get('job_id') or (args[1] if len(args) > 1 else None)
        session_id = kwargs.get('session_id') or (args[2] if len(args) > 2 else None)
        previous_result = kwargs.get('previous_result') or (args[0] if len(args) > 0 and isinstance(args[0], dict) and 'success' in args[0] else None)
    
    logger.info(f"🎯 CELERY TRAIN_SINGLE_PREDICTOR STARTED")
    logger.info(f"   Job ID: {job_id}")
    logger.info(f"   Session ID: {session_id}")
    logger.info(f"   Job spec keys: {list(job_spec.keys()) if job_spec else 'None'}")
    logger.info(f"   Previous result: {type(previous_result).__name__ if previous_result else 'None'}")
    
    try:
        # Update task state
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Loading embedding space...',
                'job_id': job_id,
                'session_id': session_id
            }
        )
        
        # Import here to avoid CUDA fork issues
        from lib.session_manager import load_session, save_session
        from lib.single_predictor_training import train_single_predictor, LightSinglePredictorArgs
        
        # Load session to get paths
        session = load_session(session_id)
        sqlite_db_path = session.get('sqlite_db')
        strings_cache = session.get('strings_cache')
        embedding_space_path = session.get('embedding_space')
        
        if not sqlite_db_path or not Path(sqlite_db_path).exists():
            raise FileNotFoundError(f"SQLite database not found: {sqlite_db_path}")
        if not embedding_space_path or not Path(embedding_space_path).exists():
            raise FileNotFoundError(f"Embedding space not found: {embedding_space_path}")
        
        logger.info(f"   SQLite DB: {sqlite_db_path}")
        logger.info(f"   Embedding space: {embedding_space_path}")
        logger.info(f"   Strings cache: {strings_cache}")
        
        # STANDARD JOB SETUP - creates job dir, logs dir, and redirects stdout/stderr
        with setup_job_logging(job_id, session_id, 'train_single_predictor') as (job_dir, original_cwd):
            # Update progress
            self.update_state(
                state='PROGRESS',
                meta={
                    'status': 'Training predictor...',
                    'job_id': job_id,
                    'session_id': session_id
                }
            )
            
            # Call train_single_predictor directly (replaces run_train_single_predictor_job from featrix_queue)
            args = LightSinglePredictorArgs(
                embedding_space_path=embedding_space_path,
                sqlite_db_path=sqlite_db_path,
                strings_cache=strings_cache or "",
                target_column=job_spec.get('target_column'),
                target_column_type=job_spec.get('target_column_type', 'set'),
                job_id=job_id,
                session_id=session_id,
                **{k: v for k, v in job_spec.items() if k not in ['target_column', 'target_column_type']}
            )
            train_single_predictor(args)
        # Get output paths from session
        session = load_session(session_id)
        output = {
            'single_predictor': session.get('single_predictor'),
            'training_metrics': session.get('training_metrics')
        }
        
        # Verify output files exist before updating session
        verify_output_files_exist(output, "TRAIN_SINGLE_PREDICTOR")
        
        # Update session with output
        session_updated = False
        try:
            from lib.session_manager import load_session, save_session
            logger.info(f"🔄 Updating session {session_id} with predictor output...")
            logger.info(f"   Output keys: {list(output.keys())}")
            session = load_session(session_id)
            logger.info(f"   ✅ Session loaded successfully")
            session = {**session, **output}
            logger.info(f"   Saving session...")
            save_session(session_id=session_id, session_doc=session, exist_ok=True)
            session_updated = True
            logger.info(f"✅ Session updated with predictor output")
            # Verify the update worked
            session_check = load_session(session_id)
            if session_check.get('single_predictor'):
                logger.info(f"   ✅ Verified: single_predictor is now in session")
            else:
                logger.error(f"   ❌ WARNING: single_predictor NOT found in session after update!")
        except Exception as session_error:
            logger.error(f"❌ CRITICAL: Failed to update session with output: {session_error}")
            logger.error(f"   Error type: {type(session_error).__name__}")
            logger.error(f"   Full traceback: {traceback.format_exc()}")
            logger.error(f"   Output files were generated but session was not updated!")
        
        # Automatically dispatch next job in chain
        try:
            logger.info(f"🔄 Attempting to dispatch next job in chain for session {session_id}...")
            logger.info(f"   Session was updated: {session_updated}")
            from lib.session_chains import dispatch_next_job_in_chain
            next_task_id = dispatch_next_job_in_chain(session_id, completed_job_type='train_single_predictor')
            if next_task_id:
                logger.info(f"✅ Successfully dispatched next job in chain (task_id: {next_task_id})")
            else:
                logger.info(f"ℹ️  No next job to dispatch (all jobs complete or no more jobs in plan)")
        except Exception as chain_error:
            logger.error(f"❌ CRITICAL: Failed to dispatch next job in chain: {chain_error}")
            logger.error(f"   Full traceback: {traceback.format_exc()}")
        
        logger.info(f"✅ Single predictor training completed successfully")
        
        # Update job status to DONE when completed successfully
        try:
            from lib.job_manager import update_job_status, JobStatus
            update_job_status(job_id=job_id, status=JobStatus.DONE)
            logger.info(f"✅ Updated job {job_id} status to DONE")
        except Exception as status_err:
            logger.warning(f"⚠️  Failed to update job {job_id} status to DONE: {status_err}")
        
        logger.info(f"🏁 JOB {job_id} FINISHED")
        
        result = {
            'success': True,
            'output': output,
            'job_id': job_id,
            'session_id': session_id
        }
        log_task_return_value(result, "TRAIN_SINGLE_PREDICTOR")
        return result
        
    except Exception as e:
        # SCREAM LOUDLY - This is a critical failure that needs immediate attention
        logger.error(f"")
        logger.error(f"╔════════════════════════════════════════════════════════════════════════════════╗")
        logger.error(f"║                                                                                ║")
        logger.error(f"║  💥💥💥 CRITICAL TASK FAILURE - TRAIN_SINGLE_PREDICTOR CRASHED 💥💥💥            ║")
        logger.error(f"║                                                                                ║")
        logger.error(f"╚════════════════════════════════════════════════════════════════════════════════╝")
        logger.error(f"")
        logger.error(f"❌❌❌ TRAIN_SINGLE_PREDICTOR FAILED WITH UNHANDLED EXCEPTION ❌❌❌")
        logger.error(f"")
        logger.error(f"   Job ID: {job_id}")
        logger.error(f"   Session ID: {session_id}")
        logger.error(f"   Exception Type: {type(e).__name__}")
        logger.error(f"   Exception Message: {str(e)}")
        logger.error(f"")
        logger.error(f"   FULL TRACEBACK:")
        logger.error(f"   {'='*100}")
        logger.error(f"   {traceback.format_exc()}")
        logger.error(f"   {'='*100}")
        logger.error(f"")
        
        # Send Slack alert for critical failure
        try:
            from slack import send_slack_message
            
            error_msg = f"🚨 *CELERY TASK CRASHED - train_single_predictor*\n"
            error_msg += f"• Job ID: `{job_id}`\n"
            error_msg += f"• Session ID: `{session_id}`\n"
            error_msg += f"• Exception: `{type(e).__name__}: {str(e)[:300]}`\n"
            
            # Get last few lines of traceback
            tb_lines = traceback.format_exc().split('\n')
            if len(tb_lines) > 5:
                error_msg += f"• Traceback:\n```\n{chr(10).join(tb_lines[-6:-1])}```"
            
            send_slack_message(error_msg, throttle=False)  # Critical - don't throttle
            logger.info("✅ Slack alert sent for Celery task failure")
        except Exception as slack_error:
            logger.warning(f"Failed to send Slack alert: {slack_error}")
        
        # Update job status to FAILED when it fails
        try:
            from lib.job_manager import update_job_status, JobStatus
            update_job_status(job_id=job_id, status=JobStatus.FAILED)
            logger.error(f"   ✅ Updated job {job_id} status to FAILED")
        except Exception as status_err:
            logger.error(f"   ❌❌❌ FAILED TO UPDATE JOB STATUS TO FAILED ❌❌❌")
            logger.error(f"   Error: {status_err}")
            logger.error(f"   Traceback: {traceback.format_exc()}")
        
        logger.error(f"")
        logger.error(f"🏁 JOB {job_id} FINISHED (WITH ERRORS)")
        logger.error(f"")
        
        result = {
            'success': False,
            'error': str(e),
            'job_id': job_id,
            'session_id': session_id,
            'traceback': traceback.format_exc()
        }
        log_task_return_value(result, "TRAIN_SINGLE_PREDICTOR")
        return result

@app.task(bind=True)
def train_es(self, job_spec: dict, job_id: str, session_id: str, data_file: str = None, strings_cache: str = None):
    """
    Celery task to train an embedding space.
    
    Args:
        job_spec: Job specification dict with training parameters
        job_id: Celery task ID (used as job ID)
        session_id: Session ID
        data_file: Path to SQLite database or CSV file
        strings_cache: Path to strings cache file
        
    Returns:
        dict with output paths (embedding_space)
    """
    from pathlib import Path
    
    # Use Celery task ID if job_id not provided
    if not job_id:
        job_id = self.request.id
        logger.info(f"   Using Celery task ID as job_id: {job_id}")
    
    logger.info(f"🎯 CELERY TRAIN_ES STARTED")
    logger.info(f"   Job ID: {job_id}")
    logger.info(f"   Session ID: {session_id}")
    logger.info(f"   Data file: {data_file}")
    logger.info(f"   Strings cache: {strings_cache}")
    logger.info(f"   Job spec keys: {list(job_spec.keys()) if job_spec else 'None'}")
    
    # STANDARD JOB SETUP - MUST BE FIRST to capture all output including errors
    with setup_job_logging(job_id, session_id, 'train_es') as (job_dir, original_cwd):
        try:
            # Update progress
            self.update_state(
                state='PROGRESS',
                meta={
                    'status': 'Starting embedding space training...',
                    'job_id': job_id,
                    'session_id': session_id
                }
            )
            
            # Import here to avoid CUDA fork issues
            from lib.session_manager import load_session, save_session
            from lib.es_training import train_es, LightTrainingArgs
            
            # Load session to get paths if not provided
            session = load_session(session_id)
            
            # Use provided data_file or get from session
            if not data_file:
                data_file = session.get('sqlite_db')
                if not data_file:
                    raise ValueError(f"No data_file provided and session {session_id} has no sqlite_db")
            
            if not strings_cache:
                strings_cache = session.get('strings_cache')
            
            if not Path(data_file).exists():
                raise FileNotFoundError(f"Data file not found: {data_file}")
            
            logger.info(f"   Data file: {data_file}")
            logger.info(f"   Strings cache: {strings_cache}")
            if strings_cache:
                cache_path = Path(strings_cache)
                if cache_path.exists():
                    cache_size = cache_path.stat().st_size / 1024 / 1024
                    logger.info(f"   ✅ Cache file exists: {cache_path.resolve()} ({cache_size:.2f} MB)")
                else:
                    logger.warning(f"   ⚠️  Cache file does not exist: {cache_path.resolve()}")
            else:
                logger.warning(f"   ⚠️  No strings_cache provided - training will run without string cache")
            # Update progress
            self.update_state(
                state='PROGRESS',
                meta={
                    'status': 'Training embedding space...',
                    'job_id': job_id,
                    'session_id': session_id
                }
            )
            
            # CRITICAL: Fork/exec training in a non-daemon session leader process
            # Celery workers are daemon processes and cannot spawn children (DataLoader workers)
            # We fork/exec a new process that becomes a session leader, allowing DataLoader workers
            # The Celery job monitors the new PID and waits until it exits
            import subprocess
            import json as json_module
            import tempfile
            import signal
            
            # Serialize args to pass to subprocess
            args_dict = {
                'input_file': str(data_file),
                'string_cache': strings_cache or "",  # FIXED: Use 'string_cache' (singular) to match LightTrainingArgs field name
                'job_id': job_id,
                'session_id': session_id,
                'column_overrides': session.get('column_overrides', {}),
                'json_transformations': session.get('json_transformations', {}),
                **{k: v for k, v in job_spec.items() if k not in ['column_overrides', 'json_transformations']}
            }
            
            # Create a temporary file to pass args
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json_file = f.name
                json_module.dump(args_dict, f)
            
            try:
                # Fork/exec training in a new session leader process
                # This allows DataLoader workers to spawn for maximum GPU utilization
                python_cmd = sys.executable
                train_script = Path(__file__).parent / "lib" / "es_training_wrapper.py"
                
                logger.info(f"🚀 Forking training process as session leader for maximum GPU utilization...")
                logger.info(f"   Python: {python_cmd}")
                logger.info(f"   Script: {train_script}")
                
                # Fork/exec with setsid to create new session leader (non-daemon)
                # This allows the process to spawn DataLoader worker children
                # CRITICAL: Open log file in append mode so subprocess writes to same file
                # The log file path is: job_dir/logs/stdout.log
                log_file_path = job_dir / "logs" / "stdout.log"
                
                # Open log file in append mode (line buffered) for subprocess
                # This ensures all output from the forked process goes to the same log file
                # Add --job-id argument so it's visible in /proc/<pid>/cmdline for process identification
                with open(log_file_path, 'a', buffering=1) as log_file:
                    process = subprocess.Popen(
                        [python_cmd, str(train_script), json_file, '--job-id', job_id],
                        cwd=str(job_dir),
                        stdout=log_file,  # Write to same log file
                        stderr=subprocess.STDOUT,  # Merge stderr to stdout
                        preexec_fn=os.setsid,  # Create new session - becomes session leader (non-daemon)
                    )
                    
                    training_pid = process.pid
                    celery_worker_pid = os.getpid()
                    
                    # Write Celery worker mapping file for admin monitoring
                    # This lets us correlate Celery worker PIDs with training job PIDs
                    mapping_file = Path(f"/tmp/featrix-celery-{celery_worker_pid}.json")
                    try:
                        mapping_data = {
                            "timestamp_started": datetime.now().isoformat(),
                            "celery_worker_pid": celery_worker_pid,
                            "training_pid": training_pid,
                            "job_id": job_id,
                            "session_id": session_id,
                            "job_type": "train_es",
                        }
                        with open(mapping_file, 'w') as f:
                            json_module.dump(mapping_data, f, indent=2)
                        logger.info(f"📝 Wrote Celery worker mapping: {mapping_file}")
                    except Exception as e:
                        logger.warning(f"Failed to write Celery worker mapping: {e}")
                    
                    logger.info(f"✅ Training process forked with PID {training_pid} (session leader)")
                    logger.info(f"   Celery worker PID: {celery_worker_pid}")
                    logger.info(f"   Training PID: {training_pid}")
                    logger.info(f"   Logging to: {log_file_path}")
                    logger.info(f"   Monitoring PID {training_pid} until it exits...")
                    
                    # Monitor the process - wait until it crashes or exits
                    try:
                        return_code = process.wait()
                        
                        # Clean up mapping file when training completes
                        try:
                            if mapping_file.exists():
                                mapping_file.unlink()
                                logger.info(f"🗑️  Cleaned up Celery worker mapping: {mapping_file}")
                        except Exception as e:
                            logger.debug(f"Could not remove mapping file: {e}")
                        
                        if return_code == 0:
                            logger.info(f"✅ Training process {training_pid} completed successfully")
                        else:
                            logger.error(f"❌ Training process {training_pid} exited with code {return_code}")
                            raise RuntimeError(f"Training process exited with code {return_code}")
                    except KeyboardInterrupt:
                        logger.warning(f"⚠️  Received interrupt signal, terminating training process {training_pid}")
                        
                        # Clean up mapping file on interrupt
                        try:
                            if mapping_file.exists():
                                mapping_file.unlink()
                        except Exception:
                            pass
                        
                        # Send SIGTERM to the process group (kills session leader and all children)
                        try:
                            os.killpg(os.getpgid(training_pid), signal.SIGTERM)
                            process.wait(timeout=10)
                        except subprocess.TimeoutExpired:
                            logger.warning(f"⚠️  Process {training_pid} did not terminate, sending SIGKILL")
                            os.killpg(os.getpgid(training_pid), signal.SIGKILL)
                            process.wait()
                        except ProcessLookupError:
                            pass  # Process already dead
                        raise
                    
            finally:
                # Clean up temp file
                try:
                    os.unlink(json_file)
                except Exception:
                    pass
            
            # Get output paths from session (updated by es_training.py before exit)
            session = load_session(session_id)
            embedding_space_path = session.get('embedding_space')
            
            # GUARD: If session wasn't updated (old code or error), construct path as fallback
            if not embedding_space_path:
                logger.warning(f"⚠️  Session not updated with embedding_space path - constructing from job_dir")
                embedding_space_path = str(job_dir / "embedded_space.pickle")
                if not Path(embedding_space_path).exists():
                    logger.error(f"❌ CRITICAL: Embedding space pickle not found at: {embedding_space_path}")
                    raise FileNotFoundError(f"Embedding space pickle not found: {embedding_space_path}")
                logger.info(f"✅ Found embedding space pickle at fallback location: {embedding_space_path}")
            
            output = {
                'embedding_space': embedding_space_path,
                'training_metrics': session.get('training_metrics')
            }
            
            # Update session with output
            session_updated = False
            try:
                logger.info(f"🔄 Updating session {session_id} with embedding space output...")
                logger.info(f"   Output keys: {list(output.keys())}")
                session = {**session, **output}
                save_session(session_id=session_id, session_doc=session, exist_ok=True)
                session_updated = True
                logger.info(f"✅ Session updated with embedding space output")
                logger.info(f"   embedding_space: {output.get('embedding_space')}")
            except Exception as session_error:
                logger.error(f"❌ CRITICAL: Failed to update session with output: {session_error}")
                logger.error(f"   Full traceback: {traceback.format_exc()}")
                logger.error(f"   Output files were generated but session was not updated!")
            
            # Automatically dispatch next job in chain
            try:
                logger.info(f"🔄 Attempting to dispatch next job in chain for session {session_id}...")
                logger.info(f"   Session was updated: {session_updated}")
                from lib.session_chains import dispatch_next_job_in_chain
                next_task_id = dispatch_next_job_in_chain(session_id, completed_job_type='train_es')
                if next_task_id:
                    logger.info(f"✅ Successfully dispatched next job in chain (task_id: {next_task_id})")
                else:
                    logger.info(f"ℹ️  No next job to dispatch (all jobs complete or no more jobs in plan)")
            except Exception as chain_error:
                logger.error(f"❌ CRITICAL: Failed to dispatch next job in chain: {chain_error}")
                logger.error(f"   Full traceback: {traceback.format_exc()}")
            
            logger.info(f"✅ Embedding space training completed successfully")
            
            # Update job status to DONE when completed successfully
            try:
                from lib.job_manager import update_job_status, JobStatus
                update_job_status(job_id=job_id, status=JobStatus.DONE)
                logger.info(f"✅ Updated job {job_id} status to DONE")
            except Exception as status_err:
                logger.warning(f"⚠️  Failed to update job {job_id} status to DONE: {status_err}")
                logger.warning(f"   Error: {traceback.format_exc()}")
            
            logger.info(f"🏁 JOB {job_id} FINISHED")
            
            result = {
                'success': True,
                'output': output,
                'job_id': job_id,
                'session_id': session_id
            }
            log_task_return_value(result, "TRAIN_ES")
            return result
            
        except Exception as e:
            # SCREAM LOUDLY - This is a critical failure that needs immediate attention
            logger.error(f"")
            logger.error(f"╔════════════════════════════════════════════════════════════════════════════════╗")
            logger.error(f"║                                                                                ║")
            logger.error(f"║  💥💥💥 CRITICAL TASK FAILURE - TRAIN_ES CRASHED 💥💥💥                        ║")
            logger.error(f"║                                                                                ║")
            logger.error(f"╚════════════════════════════════════════════════════════════════════════════════╝")
            logger.error(f"")
            logger.error(f"❌❌❌ TRAIN_ES FAILED WITH UNHANDLED EXCEPTION ❌❌❌")
            logger.error(f"")
            logger.error(f"   Job ID: {job_id}")
            logger.error(f"   Session ID: {session_id}")
            logger.error(f"   Exception Type: {type(e).__name__}")
            logger.error(f"   Exception Message: {str(e)}")
            logger.error(f"")
            logger.error(f"   FULL TRACEBACK:")
            logger.error(f"   {'='*100}")
            logger.error(f"   {traceback.format_exc()}")
            logger.error(f"   {'='*100}")
            logger.error(f"")
            
            # Update job status to FAILED when it fails
            try:
                from lib.job_manager import update_job_status, JobStatus
                update_job_status(job_id=job_id, status=JobStatus.FAILED)
                logger.error(f"   ✅ Updated job {job_id} status to FAILED")
            except Exception as status_err:
                logger.error(f"   ❌❌❌ FAILED TO UPDATE JOB STATUS TO FAILED ❌❌❌")
                logger.error(f"   Error: {status_err}")
                logger.error(f"   Traceback: {traceback.format_exc()}")
            
            logger.error(f"")
            logger.error(f"🏁 JOB {job_id} FINISHED (WITH ERRORS)")
            logger.error(f"")
            
            result = {
                'success': False,
                'error': str(e),
                'job_id': job_id,
                'session_id': session_id,
                'traceback': traceback.format_exc()
            }
            log_task_return_value(result, "TRAIN_ES")
            return result

@app.task(bind=True)
def train_knn(self, job_spec: dict, job_id: str, session_id: str):
    """
    Celery task to train KNN index (vector database).
    
    Args:
        job_spec: Job specification dict (should contain model_path, sqlite_db_path, strings_cache)
        job_id: Celery task ID (used as job ID)
        session_id: Session ID
        
    Returns:
        dict with output paths (vector_db)
    """
    from pathlib import Path
    
    # Use Celery task ID if job_id not provided
    if not job_id:
        job_id = self.request.id
        logger.info(f"   Using Celery task ID as job_id: {job_id}")
    
    logger.info(f"🎯 CELERY TRAIN_KNN STARTED")
    logger.info(f"   Job ID: {job_id}")
    logger.info(f"   Session ID: {session_id}")
    logger.info(f"   Job spec keys: {list(job_spec.keys()) if job_spec else 'None'}")
    
    try:
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Starting KNN training...',
                'job_id': job_id,
                'session_id': session_id
            }
        )
        
        # Import here to avoid CUDA fork issues
        from lib.session_manager import load_session, save_session
        from lib.knn_training import train_knn
        
        # Load session to get paths
        session = load_session(session_id)
        
        # Get paths from job_spec or session
        model_path = job_spec.get('model_path') or session.get('embedding_space')
        sqlite_db_path = job_spec.get('sqlite_db_path') or session.get('sqlite_db')
        strings_cache = job_spec.get('strings_cache') or session.get('strings_cache')
        
        if not model_path or not Path(model_path).exists():
            raise FileNotFoundError(f"Embedding space not found: {model_path}")
        if not sqlite_db_path or not Path(sqlite_db_path).exists():
            raise FileNotFoundError(f"SQLite database not found: {sqlite_db_path}")
        
        logger.info(f"   Embedding space: {model_path}")
        logger.info(f"   SQLite DB: {sqlite_db_path}")
        logger.info(f"   Strings cache: {strings_cache}")
        
        # STANDARD JOB SETUP - creates job dir, logs dir, and redirects stdout/stderr
        with setup_job_logging(job_id, session_id, 'train_knn') as (job_dir, original_cwd):
            # Update progress
            self.update_state(
                state='PROGRESS',
                meta={
                    'status': 'Building vector database...',
                    'job_id': job_id,
                    'session_id': session_id
                }
            )
            
            # Call train_knn directly (replaces run_train_knn_job from featrix_queue)
            output = train_knn(
                es_path=Path(model_path),
                sqlite_db_path=Path(sqlite_db_path),
                job_id=job_id
            )
        
        # Verify output files exist before updating session
        verify_output_files_exist(output, "TRAIN_KNN")
        
        # Update session with output
        session_updated = False
        try:
            from lib.session_manager import load_session, save_session
            logger.info(f"🔄 Updating session {session_id} with KNN output...")
            logger.info(f"   Output keys: {list(output.keys())}")
            session = load_session(session_id)
            logger.info(f"   ✅ Session loaded successfully")
            session = {**session, **output}
            logger.info(f"   Saving session...")
            save_session(session_id=session_id, session_doc=session, exist_ok=True)
            session_updated = True
            logger.info(f"✅ Session updated with KNN output")
            # Verify the update worked
            session_check = load_session(session_id)
            if session_check.get('vector_db'):
                logger.info(f"   ✅ Verified: vector_db is now in session")
            else:
                logger.error(f"   ❌ WARNING: vector_db NOT found in session after update!")
        except Exception as session_error:
            logger.error(f"❌ CRITICAL: Failed to update session with output: {session_error}")
            logger.error(f"   Error type: {type(session_error).__name__}")
            logger.error(f"   Full traceback: {traceback.format_exc()}")
            logger.error(f"   Output files were generated but session was not updated!")
        
        # Automatically dispatch next job in chain
        try:
            logger.info(f"🔄 Attempting to dispatch next job in chain for session {session_id}...")
            logger.info(f"   Session was updated: {session_updated}")
            from lib.session_chains import dispatch_next_job_in_chain
            next_task_id = dispatch_next_job_in_chain(session_id, completed_job_type='train_knn')
            if next_task_id:
                logger.info(f"✅ Successfully dispatched next job in chain (task_id: {next_task_id})")
            else:
                logger.info(f"ℹ️  No next job to dispatch (all jobs complete or no more jobs in plan)")
        except Exception as chain_error:
            logger.error(f"❌ CRITICAL: Failed to dispatch next job in chain: {chain_error}")
            logger.error(f"   Full traceback: {traceback.format_exc()}")
        
        logger.info(f"✅ KNN training completed successfully")
        
        # Update job status to DONE when completed successfully
        try:
            from lib.job_manager import update_job_status, JobStatus
            update_job_status(job_id=job_id, status=JobStatus.DONE)
            logger.info(f"✅ Updated job {job_id} status to DONE")
        except Exception as status_err:
            logger.warning(f"⚠️  Failed to update job {job_id} status to DONE: {status_err}")
        
        logger.info(f"🏁 JOB {job_id} FINISHED")
        
        result = {
            'success': True,
            'output': output,
            'job_id': job_id,
            'session_id': session_id
        }
        log_task_return_value(result, "TRAIN_KNN")
        return result
        
    except Exception as e:
        # SCREAM LOUDLY - This is a critical failure that needs immediate attention
        logger.error(f"")
        logger.error(f"╔════════════════════════════════════════════════════════════════════════════════╗")
        logger.error(f"║                                                                                ║")
        logger.error(f"║  💥💥💥 CRITICAL TASK FAILURE - TRAIN_KNN CRASHED 💥💥💥                        ║")
        logger.error(f"║                                                                                ║")
        logger.error(f"╚════════════════════════════════════════════════════════════════════════════════╝")
        logger.error(f"")
        logger.error(f"❌❌❌ TRAIN_KNN FAILED WITH UNHANDLED EXCEPTION ❌❌❌")
        logger.error(f"")
        logger.error(f"   Job ID: {job_id}")
        logger.error(f"   Session ID: {session_id}")
        logger.error(f"   Exception Type: {type(e).__name__}")
        logger.error(f"   Exception Message: {str(e)}")
        logger.error(f"")
        logger.error(f"   FULL TRACEBACK:")
        logger.error(f"   {'='*100}")
        logger.error(f"   {traceback.format_exc()}")
        logger.error(f"   {'='*100}")
        logger.error(f"")
        
        # Update job status to FAILED when it fails
        try:
            from lib.job_manager import update_job_status, JobStatus
            update_job_status(job_id=job_id, status=JobStatus.FAILED)
            logger.error(f"   ✅ Updated job {job_id} status to FAILED")
        except Exception as status_err:
            logger.error(f"   ❌❌❌ FAILED TO UPDATE JOB STATUS TO FAILED ❌❌❌")
            logger.error(f"   Error: {status_err}")
            logger.error(f"   Traceback: {traceback.format_exc()}")
        
        logger.error(f"")
        logger.error(f"🏁 JOB {job_id} FINISHED (WITH ERRORS)")
        logger.error(f"")
        
        result = {
            'success': False,
            'error': str(e),
            'job_id': job_id,
            'session_id': session_id,
            'traceback': traceback.format_exc()
        }
        log_task_return_value(result, "TRAIN_KNN")
        return result

@app.task(bind=True)
def dump_to_backplane(self, session_id: str):
    """
    Celery task to copy a session's workspace to /backplane/backplane1.
    
    This task:
    1. Verifies /backplane/backplane1 is mounted and different from /backplane
    2. Rsyncs the session workspace to the backplane
    3. Creates a LAST_HOST_DUMP.json marker file with metadata
    
    Args:
        session_id: Session ID to dump
    
    Returns:
        dict with success status and dump metadata
    """
    import os
    import subprocess
    import socket
    import json
    from pathlib import Path
    from datetime import datetime
    
    logger.info(f"💾 CELERY DUMP_TO_BACKPLANE STARTED - Session: {session_id}")
    
    try:
        # Update task state
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Verifying filesystem...',
                'session_id': session_id
            }
        )
        
        # Verify /backplane/backplane1 exists and is a directory
        backplane1 = Path("/backplane/backplane1")
        backplane = Path("/backplane")
        
        if not backplane1.exists():
            raise FileNotFoundError(f"/backplane/backplane1 does not exist")
        
        if not backplane1.is_dir():
            raise ValueError(f"/backplane/backplane1 is not a directory")
        
        # Verify it's mounted (check if it's a different filesystem from /backplane)
        try:
            stat_backplane = os.statvfs(str(backplane))
            stat_backplane1 = os.statvfs(str(backplane1))
            
            # Compare filesystem IDs (f_fsid on Linux, f_fsid on macOS)
            if hasattr(stat_backplane, 'f_fsid') and hasattr(stat_backplane1, 'f_fsid'):
                if stat_backplane.f_fsid == stat_backplane1.f_fsid:
                    raise ValueError(f"/backplane/backplane1 is the same filesystem as /backplane - not a separate mount")
        except Exception as fs_check_error:
            logger.warning(f"⚠️  Could not verify filesystem mount: {fs_check_error}")
            # Continue anyway - might be a different OS or permission issue
        
        # Get session workspace path
        if not FEATRIX_QUEUE_AVAILABLE:
            raise ImportError("featrix_queue module not available")
        
        from config import config
        source_dir = config.output_dir / session_id
        
        if not source_dir.exists():
            raise FileNotFoundError(f"Session workspace not found: {source_dir}")
        
        # Destination path
        dest_dir = backplane1 / session_id
        
        logger.info(f"   Source: {source_dir}")
        logger.info(f"   Destination: {dest_dir}")
        
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Copying files...',
            }
        )
        
        # Run rsync
        rsync_cmd = [
            'rsync',
            '-a',  # Archive mode (preserves permissions, timestamps, etc.)
            '--progress',
            f"{source_dir}/",
            str(dest_dir)
        ]
        
        logger.info(f"   Running: {' '.join(rsync_cmd)}")
        result = subprocess.run(rsync_cmd, capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            raise Exception(f"Rsync failed with exit code {result.returncode}: {result.stderr}")
        
        # Count files and calculate size
        file_count = 0
        total_size = 0
        for root, dirs, files in os.walk(dest_dir):
            file_count += len(files)
            for f in files:
                try:
                    total_size += os.path.getsize(os.path.join(root, f))
                except OSError:
                    pass
        
        # Get training status and epochs from session
        training_status = "unknown"
        epochs = None
        try:
            from lib.session_manager import load_session
            session = load_session(session_id)
            training_status = session.get('status', 'unknown')
            # Try to get epoch count from training logs or model checkpoints
            # This is approximate - we'd need to parse logs or checkpoints
        except Exception as session_error:
            logger.warning(f"Could not load session for metadata: {session_error}")
        
        # Create marker file
        marker_file = dest_dir / "LAST_HOST_DUMP.json"
        marker_data = {
            "host": socket.gethostname(),
            "session_id": session_id,
            "dumped_at": datetime.utcnow().isoformat() + "Z",
            "training_status": training_status,
            "epochs": epochs,
            "source_path": str(source_dir),
            "destination_path": str(dest_dir),
            "rsync_exit_code": result.returncode,
            "file_count": file_count,
            "total_size_bytes": total_size
        }
        
        with open(marker_file, 'w') as f:
            json.dump(marker_data, f, indent=2)
        
        logger.info(f"✅ Dump completed successfully")
        logger.info(f"   Files: {file_count}, Size: {total_size / 1024 / 1024:.2f} MB")
        logger.info(f"   Marker file: {marker_file}")
        
        return {
            'success': True,
            'session_id': session_id,
            'destination': str(dest_dir),
            'file_count': file_count,
            'total_size_bytes': total_size,
            'marker_file': str(marker_file)
        }
        
    except Exception as e:
        logger.error(f"❌ DUMP_TO_BACKPLANE FAILED: {e}")
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return {
            'success': False,
            'error': str(e),
            'session_id': session_id,
            'traceback': traceback.format_exc()
        }

if __name__ == '__main__':
    app.start() 