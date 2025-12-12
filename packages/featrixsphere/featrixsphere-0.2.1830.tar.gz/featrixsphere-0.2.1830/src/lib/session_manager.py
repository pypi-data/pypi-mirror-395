"""
Session Management Module

Extracted from featrix_queue.py to provide clean session management interface.
Handles all session file operations, creation, loading, saving, and iteration.
"""
import fcntl
import json
import logging
import socket
import sys
from copy import deepcopy
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional
from uuid import uuid4
from zoneinfo import ZoneInfo

from config import config
from utils import convert_from_iso, convert_to_iso

logger = logging.getLogger(__name__)


class SessionStatus(Enum):
    READY = "ready"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"


def serialize_session(session_doc: dict):
    """Serialize session document for storage (convert dates, enums, etc.)."""
    session_doc = deepcopy(session_doc)

    # Convert datetime objects to ISO strings
    if "created_at" in session_doc:
        session_doc["created_at"] = convert_to_iso(session_doc["created_at"])
    if "started_at" in session_doc:
        session_doc["started_at"] = convert_to_iso(session_doc["started_at"])
    if "finished_at" in session_doc:
        session_doc["finished_at"] = convert_to_iso(session_doc["finished_at"])
    if "published_at" in session_doc:
        session_doc["published_at"] = convert_to_iso(session_doc["published_at"])
    if "deprecated_at" in session_doc:
        session_doc["deprecated_at"] = convert_to_iso(session_doc["deprecated_at"])

    # Convert status enum to string
    if "status" in session_doc:
        if hasattr(session_doc["status"], "value"):
            session_doc["status"] = session_doc["status"].value

    return session_doc


def save_session(session_id: str, session_doc: dict, exist_ok: bool = False):
    """Save session document to disk with file locking."""
    session_path = config.session_dir / f"{session_id}.session"
    lock_path = config.session_dir / f"{session_id}.lock"

    # If the session already exists and we're not overwriting, raise an error.
    if session_path.exists() and not exist_ok:
        raise FileExistsError(f"Session {session_id} already exists")

    serialized_session = serialize_session(session_doc)

    # Use file locking to prevent concurrent writes
    lock_file = None
    try:
        logger.debug(f"🔒 Acquiring EXCLUSIVE lock for session {session_id}")
        lock_file = open(lock_path, 'w')
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)  # Exclusive lock
        logger.debug(f"✅ Acquired EXCLUSIVE lock for session {session_id}")
    except PermissionError as perm_err:
        logger.warning(f"⚠️  Cannot create lock file for session {session_id}: {perm_err}")
        lock_file = None

    try:
        # Use temp file and atomic rename
        temp_session_filename = session_id + ".tmp"
        temp_session_path = config.session_dir / temp_session_filename

        # Write JSON to temp file
        json_str = json.dumps(serialized_session, indent=4)
        temp_session_path.write_text(json_str)

        # Verify the temp file is valid JSON before atomically renaming
        try:
            json.loads(temp_session_path.read_text())
        except json.JSONDecodeError as e:
            logger.error(f"💥 Serialization created invalid JSON for session {session_id}")
            logger.error(f"   Error: {e}")
            if temp_session_path.exists():
                temp_session_path.unlink()
            raise ValueError(f"Failed to serialize session {session_id} to valid JSON") from e

        # Atomic rename
        temp_session_path.rename(session_path)
        logger.info(f"Session {session_id} saved to {session_path}")

    except Exception:
        # Clean up temp file if anything goes wrong
        temp_session_path = config.session_dir / f"{session_id}.tmp"
        if temp_session_path.exists():
            try:
                temp_session_path.unlink()
            except:
                pass
        raise
    finally:
        if lock_file:
            try:
                logger.debug(f"🔓 Releasing EXCLUSIVE lock for session {session_id}")
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
                lock_file.close()
                logger.debug(f"✅ Released EXCLUSIVE lock for session {session_id}")
            except Exception as unlock_err:
                logger.warning(f"⚠️  Error releasing lock for session {session_id}: {unlock_err}")


def load_session(session_id: str):
    """Load a session by session_id. Checks both regular and published locations."""
    session_path = config.session_dir / f"{session_id}.session"
    lock_path = config.session_dir / f"{session_id}.lock"

    # Check if it's a symlink to published location
    if session_path.is_symlink():
        session_path = session_path.resolve()
        logger.debug(f"📦 Session {session_id} is symlinked to published location: {session_path}")

    # If not found in regular location, check published location
    if not session_path.is_file():
        published_session_file = Path("/sphere/published") / session_id / f"{session_id}.session"
        if published_session_file.exists():
            session_path = published_session_file
            logger.debug(f"📦 Loading session {session_id} from published location: {session_path}")
        else:
            raise FileNotFoundError(f"Session {session_id} does not exist")

    # Use file locking to prevent reading while another process is writing
    lock_file = None
    try:
        logger.debug(f"🔒 Acquiring SHARED lock for session {session_id}")
        lock_file = open(lock_path, 'w')
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_SH)  # Shared lock for reading
        logger.debug(f"✅ Acquired SHARED lock for session {session_id}")
    except PermissionError as perm_err:
        logger.warning(f"⚠️  Cannot create lock file for session {session_id}: {perm_err}")
        logger.warning("   Reading session file without lock (may cause issues if another process is writing)")
        lock_file = None

    try:
        try:
            session_doc = json.loads(session_path.read_text())
        except json.JSONDecodeError as e:
            logger.warning(f"⚠️ Corrupted session file: {session_path} (session_id: {session_id})")
            logger.warning(f"   JSON error: {e}")
            logger.warning(f"   File size: {session_path.stat().st_size} bytes")
            raise ValueError(f"Session {session_id} file is corrupted. JSON parse error at line {e.lineno}, column {e.colno}") from e

        session_doc['created_at'] = convert_from_iso(session_doc['created_at'])
        session_doc['status'] = SessionStatus(session_doc['status'])

        return session_doc
    finally:
        if lock_file:
            try:
                logger.debug(f"🔓 Releasing SHARED lock for session {session_id}")
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
                lock_file.close()
                logger.debug(f"✅ Released SHARED lock for session {session_id}")
            except Exception as unlock_err:
                logger.warning(f"⚠️  Error releasing lock for session {session_id}: {unlock_err}")


def resolve_session_path(session_id: str, path_from_session: str) -> Path:
    """
    Resolve a path stored in a session document to an absolute Path.
    
    Handles:
    - Relative paths (relative to session output directory)
    - Absolute paths
    - Published session paths
    - Symlinked sessions
    """
    if not path_from_session:
        raise ValueError("path_from_session cannot be empty")

    # Try to load session to check if it's published
    try:
        session = load_session(session_id)
        published = session.get("published", False)
        published_path = session.get("published_path")
    except FileNotFoundError:
        # Session doesn't exist yet, assume not published
        published = False
        published_path = None

    # If path is already absolute, check if it exists
    original_path = Path(path_from_session)
    if original_path.is_absolute():
        if original_path.exists():
            return original_path
        # Path doesn't exist, but it's absolute - return as-is
        return original_path

    # Path is relative - resolve based on session location
    if published and published_path:
        # Session is published - resolve relative to published output directory
        published_output_dir = Path(published_path) / "output"
        resolved = published_output_dir / path_from_session
    else:
        # Regular session - resolve relative to output directory
        resolved = config.output_dir / session_id / path_from_session

    # If resolved path doesn't exist, try the original path
    if not resolved.exists() and original_path.exists():
        logger.warning(f"⚠️  Resolved path {resolved} doesn't exist, using original {original_path}")
        return original_path

    return resolved


def get_session_info(session_id: str):
    """
    Get session information from Redis/Celery (no file-based queues).
    
    Returns dict with:
    - session: The session document
    - jobs: Dict of job_id -> job data from Redis
    - job_queue_positions: Dict of job_id -> None (not applicable for Celery)
    - detailed_queue_info: Enhanced queue information per job
    """
    from lib.queue_manager import load_session_jobs
    from lib.job_manager import JobStatus, update_job_status, get_session_jobs
    
    session = load_session(session_id)
    session_jobs = load_session_jobs(session)
    session_jobs_queue_positions = dict()
    detailed_queue_info = {}
    
    # Check Celery active tasks to see which jobs are actually running
    # CRITICAL: Add timeout to prevent hanging if Celery workers don't respond
    active_task_ids = set()
    try:
        from celery_app import app
        # Use timeout parameter to prevent hanging (1 second max)
        # If workers don't respond, this will return None/empty dict instead of hanging
        inspect = app.control.inspect(timeout=1.0)
        active = inspect.active() or {}
        for worker, tasks in active.items():
            if tasks:  # Check if tasks list exists and is not empty
                for task in tasks:
                    task_id = task.get('id')
                    if task_id:
                        active_task_ids.add(task_id)
    except Exception as e:
        # Celery inspection failed or timed out - continue without it (non-critical)
        logger.debug(f"Celery inspection failed/timed out (non-critical): {type(e).__name__}: {e}")
        pass
    
    # Process each job - collect job IDs to remove (deleted placeholders)
    jobs_to_remove = []
    
    for job_id, job in session_jobs.items():
        job_type = job.get("job_type") or job.get("type")
        
        # CRITICAL: Add 'type' alias for client compatibility
        # Clients expect 'type' but we save as 'job_type' in Redis
        if job_type and 'type' not in job:
            job['type'] = job_type
        
        # CRITICAL: Ensure 'progress' field exists for client progress bars
        # Default to 0 if not present (newly created jobs)
        if 'progress' not in job:
            job['progress'] = 0
        
        job_status = job.get("status")
        
        # Handle JobStatus enum - convert to string value immediately
        if isinstance(job_status, JobStatus):
            job_status_value = job_status.value
            job['status'] = job_status_value  # CRITICAL: Update the dict to use string value
        elif hasattr(job_status, 'value'):
            job_status_value = job_status.value
            job['status'] = job_status_value  # CRITICAL: Update the dict to use string value
        else:
            job_status_value = str(job_status) if job_status else "unknown"
            job['status'] = job_status_value  # CRITICAL: Ensure it's always a string
        
        # Skip deleted/placeholder jobs immediately - these are job IDs in job_plan that don't exist in Redis
        # They clutter the response and confuse clients
        if job_status_value == "deleted" or job_status == "deleted":
            # Mark for removal - don't include these in the response at all
            jobs_to_remove.append(job_id)
            logger.debug(f"⏭️  Skipping deleted/placeholder job {job_id} (not in Redis)")
            continue
        
        # Aggregate movie frame jobs into summary (don't show individual jobs to client)
        # These are background visualization jobs - show aggregated progress instead
        if job_type == 'project_training_movie_frame':
            jobs_to_remove.append(job_id)  # Remove from main jobs list
            # We'll add aggregated summary later
            continue
        
        # Check if job is actually running in Celery (even if status says READY)
        is_running_in_celery = job_id in active_task_ids
        
        # CRITICAL: Check if job has actually completed by looking for output files
        # This detects jobs that completed but status wasn't updated in Redis
        job_completed_by_files = False
        if job_status_value in ["ready", "running"] and not is_running_in_celery:
            # Job says ready/running but not in Celery - check if output files exist
            try:
                from lib.job_manager import get_job_output_path
                session_id_for_check = session.get('session_id') or session_id
                job_output_dir = get_job_output_path(job_id, session_id=session_id_for_check, job_type=job_type)
                
                # Check for completion indicators based on job type
                if job_type == "create_structured_data":
                    # Check for embedding_space.db or data.db
                    if (job_output_dir / "embedding_space.db").exists() or (job_output_dir / "data.db").exists():
                        job_completed_by_files = True
                        logger.info(f"🔧 Detected completed job {job_id} (create_structured_data): output files exist")
                elif job_type == "train_es":
                    # Check for embedding_space.pickle
                    if (job_output_dir / "embedding_space.pickle").exists():
                        job_completed_by_files = True
                        logger.info(f"🔧 Detected completed job {job_id} (train_es): embedding_space.pickle exists")
                elif job_type == "train_knn":
                    # Check for vector_db or similar
                    if (job_output_dir / "vector_db").exists() or list(job_output_dir.glob("*.index")):
                        job_completed_by_files = True
                        logger.info(f"🔧 Detected completed job {job_id} (train_knn): vector_db files exist")
            except Exception as e:
                # If we can't find the output directory, that's okay - job might not have started yet
                logger.debug(f"Could not check output files for job {job_id}: {e}")
        
        # CRITICAL: If job is actually running in Celery but status says "ready", update the status
        # This fixes the issue where jobs are running but status isn't updated in Redis yet
        if is_running_in_celery:
            # Job is detected as running in Celery - always update status to running
            # Check current status for logging, but always update if running in Celery
            current_status_str = str(job_status_value).lower()
            if current_status_str != "running":
                # Job is actually running - update the status in Redis AND the returned dict
                try:
                    update_job_status(job_id, JobStatus.RUNNING)
                    logger.info(f"🔧 Updated job {job_id} status in Redis: {current_status_str} → running (detected in Celery active tasks)")
                except Exception as e:
                    logger.warning(f"⚠️  Failed to update job {job_id} status in Redis: {e}")
                    # Still update the returned dict even if Redis update fails
                
                # Update the status in the returned dict
                job['status'] = JobStatus.RUNNING.value
                job_status = JobStatus.RUNNING
                job_status_value = JobStatus.RUNNING.value
        
        # CRITICAL: If job completed but status wasn't updated, fix it
        elif job_completed_by_files:
            # Job has output files indicating completion - update status to done
            try:
                update_job_status(job_id, JobStatus.DONE)
                logger.info(f"🔧 Updated job {job_id} status in Redis: {job_status_value} → done (detected completion via output files)")
            except Exception as e:
                logger.warning(f"⚠️  Failed to update job {job_id} status in Redis: {e}")
            
            # Update the status in the returned dict
            job['status'] = JobStatus.DONE.value
            job_status = JobStatus.DONE
            job_status_value = JobStatus.DONE.value
        
        # Skip deleted/placeholder jobs - these are job IDs in job_plan that don't exist in Redis
        # They clutter the response and confuse clients
        if job_status_value == "deleted" or job_status == "deleted":
            # Don't include these in the response at all - they're just stale job IDs
            logger.debug(f"⏭️  Skipping deleted/placeholder job {job_id} (not in Redis)")
            continue
        
        # Celery doesn't have queue positions - jobs are either waiting, running, or done
        session_jobs_queue_positions[job_id] = None
        
        # Collect detailed information
        # Use the updated job_status_value (which may have been corrected above)
        detailed_info = {
            "position": None,  # Not applicable for Celery
            "status": job_status_value,  # This should be "running" if job was detected as running
            "queue_name": job_type or "unknown",
        }
        
        # Add detailed status information based on job state
        if is_running_in_celery or (job_status == JobStatus.RUNNING) or (job_status_value == JobStatus.RUNNING.value) or (job_status_value == "running"):
            # Job is currently running
            started_at = job.get("started_at")
            progress = job.get("progress", 0)
            
            detailed_info.update({
                "queue_status": "running",
                "started_at": convert_to_iso(started_at) if started_at else None,
                "progress": progress,
                "progress_percent": round(progress * 100, 1) if progress else 0,
                "estimated_wait_message": "Currently running",
                "current_epoch": job.get("current_epoch"),
                "current_loss": job.get("current_loss"),
                "validation_loss": job.get("validation_loss"),
            })
            
        elif (job_status == JobStatus.READY) or (job_status_value == JobStatus.READY.value) or (job_status_value == "ready"):
            # Job is ready/waiting to be picked up
            detailed_info.update({
                "queue_status": "waiting",
                "estimated_wait_message": "Waiting for worker to pick up",
                "worker_available": True,  # Simplified
            })
            
        elif (job_status == JobStatus.DONE) or (job_status_value == JobStatus.DONE.value) or (job_status_value == "done"):
            finished_at = job.get("finished_at")
            detailed_info.update({
                "queue_status": "completed",
                "finished_at": convert_to_iso(finished_at) if finished_at else None,
                "estimated_wait_message": "Completed successfully",
                "progress_percent": 100,
            })
            
        elif (job_status == JobStatus.FAILED) or (job_status_value == JobStatus.FAILED.value) or (job_status_value == "failed"):
            finished_at = job.get("finished_at")
            detailed_info.update({
                "queue_status": "failed",
                "finished_at": convert_to_iso(finished_at) if finished_at else None,
                "estimated_wait_message": "Job failed - check logs",
                "progress_percent": 0,
            })
        
        elif (job_status == JobStatus.PAUSED) or (job_status_value == JobStatus.PAUSED.value) or (job_status_value == "paused"):
            paused_at = job.get("paused_at")
            pause_reason = job.get("pause_reason", "Paused by user")
            detailed_info.update({
                "queue_status": "paused",
                "paused_at": paused_at,
                "pause_reason": pause_reason,
                "estimated_wait_message": f"Job paused: {pause_reason}",
                "progress_percent": job.get("progress", 0) * 100 if job.get("progress") else 0,
            })
        
        detailed_queue_info[job_id] = detailed_info
    
    # Remove deleted/placeholder jobs from the response
    for job_id in jobs_to_remove:
        session_jobs.pop(job_id, None)
        detailed_queue_info.pop(job_id, None)
        session_jobs_queue_positions.pop(job_id, None)
    
    # CRITICAL: Check if all jobs are done and update session status accordingly
    # This ensures the session file status reflects the actual completion state
    # CRITICAL: Only mark as done if we actually have jobs that completed
    # If no jobs exist, session should stay in 'ready' or 'running' state
    all_jobs_done = len(session_jobs) > 0  # Start as True only if we have jobs
    any_job_failed = False
    any_job_running = False
    
    for job_id, job in session_jobs.items():
        job_status = job.get("status")
        if isinstance(job_status, JobStatus):
            job_status_value = job_status.value
            job['status'] = job_status_value  # CRITICAL: Update the dict to use string value
        else:
            job_status_value = str(job_status) if job_status else "unknown"
            job['status'] = job_status_value  # CRITICAL: Ensure it's always a string
        
        if job_status_value not in ["done", "failed", "deleted"]:
            all_jobs_done = False
            if job_status_value == "running":
                any_job_running = True
        elif job_status_value == "failed":
            any_job_failed = True
    
    # Update session status if all jobs are complete
    # CRITICAL: Only mark as done if we actually had jobs that completed
    # If no jobs exist, session should stay in 'ready' or 'running' state
    current_session_status = session.get("status")
    if isinstance(current_session_status, SessionStatus):
        current_session_status_value = current_session_status.value
    else:
        current_session_status_value = str(current_session_status) if current_session_status else "ready"
    
    if all_jobs_done and current_session_status_value != "done":
        # GUARD: Check job_plan to see if jobs SHOULD exist
        # Don't mark as DONE if job_plan has jobs but Redis doesn't (indicates tracking failure)
        job_plan = session.get('job_plan', [])
        jobs_with_ids = [j for j in job_plan if j.get('job_id') and j.get('job_id') not in ['null', 'None', '']]
        
        if len(jobs_with_ids) > 0 and len(session_jobs) == 0:
            logger.error(f"❌ CRITICAL BUG DETECTED: Session {session_id} has job_plan with {len(jobs_with_ids)} job_ids but ZERO jobs in Redis!")
            logger.error(f"   This means jobs were dispatched but never tracked - Redis save failed")
            logger.error(f"   Job IDs from job_plan: {[j.get('job_id') for j in jobs_with_ids]}")
            logger.error(f"   Session will NOT be marked as DONE - manual investigation required")
            # Don't mark as DONE - this is a bug, not completion
        elif len(session_jobs) == 0 and len(job_plan) > 0:
            logger.warning(f"⚠️  Session {session_id} has job_plan but no jobs in Redis yet - jobs may not have started")
            # Don't mark as DONE - jobs haven't started yet
        else:
            # All jobs are done - update session status
            if any_job_failed:
                new_status = SessionStatus.FAILED
            else:
                new_status = SessionStatus.DONE
            
            try:
                session["status"] = new_status
                save_session(session_id, session, exist_ok=True)
                logger.info(f"🔧 Updated session {session_id} status: {current_session_status_value} → {new_status.value} (all jobs complete)")
            except Exception as e:
                logger.warning(f"⚠️  Failed to update session {session_id} status: {e}")
    elif any_job_running and current_session_status_value == "ready":
        # At least one job is running - update session status to running
        try:
            session["status"] = SessionStatus.RUNNING
            save_session(session_id, session, exist_ok=True)
            logger.debug(f"🔧 Updated session {session_id} status: ready → running (jobs in progress)")
        except Exception as e:
            logger.warning(f"⚠️  Failed to update session {session_id} status: {e}")

    # Create aggregated movie frame progress from individual movie frame jobs
    movie_frame_summary = None
    if session_id:
        try:
            # Get all movie frame jobs for this session from Redis
            redis_jobs = get_session_jobs(session_id)
            movie_frame_jobs = [j for j in redis_jobs if j.get('job_type') == 'project_training_movie_frame']
            
            if movie_frame_jobs:
                total_frames = len(movie_frame_jobs)
                done_frames = len([j for j in movie_frame_jobs if j.get('status') == JobStatus.DONE.value or j.get('status') == 'done'])
                failed_frames = len([j for j in movie_frame_jobs if j.get('status') == JobStatus.FAILED.value or j.get('status') == 'failed'])
                running_frames = len([j for j in movie_frame_jobs if j.get('status') == JobStatus.RUNNING.value or j.get('status') == 'running'])
                
                # Calculate progress percentage
                progress_pct = (done_frames / total_frames * 100) if total_frames > 0 else 0
                
                # Determine overall status
                if done_frames == total_frames:
                    overall_status = 'done'
                elif running_frames > 0:
                    overall_status = 'running'
                elif failed_frames > 0 and done_frames == 0:
                    overall_status = 'failed'
                else:
                    overall_status = 'ready'
                
                movie_frame_summary = {
                    'job_id': 'movie_frames_summary',  # Virtual job ID
                    'type': 'training_movie_generation',
                    'status': overall_status,
                    'progress': progress_pct,
                    'frames_total': total_frames,
                    'frames_done': done_frames,
                    'frames_failed': failed_frames,
                    'frames_running': running_frames,
                    'description': f'Rendering training movie: {done_frames}/{total_frames} frames',
                }
                
                # Add to jobs dict as a virtual job
                session_jobs['movie_frames_summary'] = movie_frame_summary
                logger.debug(f"✅ Aggregated {total_frames} movie frame jobs into summary: {done_frames} done, {failed_frames} failed")
        except Exception as agg_err:
            logger.warning(f"⚠️  Failed to aggregate movie frame jobs: {agg_err}")
    
    return {
        "session": session,
        "jobs": session_jobs,
        "job_queue_positions": session_jobs_queue_positions,
        "detailed_queue_info": detailed_queue_info,
    }


def iterate_over_sessions():
    """Iterate over all sessions in the session directory."""
    if not config.session_dir.exists():
        return

    for session_file in config.session_dir.glob("*.session"):
        # Skip temp files
        if session_file.name.endswith(".tmp"):
            continue

        # Skip lock files
        if session_file.name.endswith(".lock"):
            continue

        session_id = session_file.stem

        try:
            yield load_session(session_id)
        except (ValueError, json.JSONDecodeError) as e:
            # Skip corrupted sessions
            logger.warning(f"⚠️  Skipping corrupted session {session_id}: {e}")
            continue
        except Exception as e:
            logger.warning(f"⚠️  Error loading session {session_id}: {e}")
            continue


# ============================================================================
# Exception Classes
# ============================================================================

class NodeUpgradingException(Exception):
    """Exception raised when a node is currently upgrading and cannot accept training requests."""
    pass


# ============================================================================
# Helper Functions
# ============================================================================

def ensure_directories_exist():
    """Ensure all necessary featrix directories exist."""
    directories_to_create = [
        config.output_dir, 
        config.data_dir,
        config.session_dir,
    ]
    
    for directory in directories_to_create:
        if directory and not directory.exists():
            logger.info(f"Creating directory: {directory}")
            directory.mkdir(parents=True, exist_ok=True)


def get_version_info() -> dict:
    """Get version information for tracking in jobs and recovery info."""
    try:
        from version import get_version
        version_info = get_version()
        version_dict = version_info.dict()
        return {
            "version": version_dict.get("semantic_version", "unknown"),
            "git_hash": version_dict.get("git_hash"),
            "git_date": version_dict.get("git_date"),
        }
    except Exception as e:
        logger.warning(f"Failed to get version info: {e}")
        return {
            "version": "unknown",
            "git_hash": None,
            "git_date": None,
        }


def _generate_wait_message(position: int, running_jobs: list, job_type: str) -> str:
    """Generate a human-readable wait message for a job in queue."""
    if position is None:
        return "Position unknown"
    
    if position == 0:
        if running_jobs:
            return f"Next in queue (1 job currently running)"
        else:
            return "Next in queue (will start soon)"
    
    ahead = position
    running = len(running_jobs)
    
    if running > 0:
        return f"Position {position + 1} in queue ({ahead} jobs ahead, {running} running)"
    else:
        return f"Position {position + 1} in queue ({ahead} jobs ahead)"


# ============================================================================
# Session Creation Functions
# ============================================================================

def create_sphere_session(session_id: str, created_at: datetime, input_filename: str | None = None, name: str = None, single_predictors: list = None, epochs: int = None, column_overrides: dict = None, string_list_delimiter: str = "|", movie_frame_interval: int = 3, weightwatcher_save_every: int = 5, important_columns_for_visualization: list = None, user_metadata: dict = None):
    """Create a sphere session (embedding space + optional predictors)."""
    # Allow sphere sessions without input_filename for testing/API usage
    if not input_filename:
        logger.info(f"Creating sphere session {session_id} without input file (API/testing mode)")
        input_filename = "api_created_session.csv"  # Placeholder filename
    single_predictors = single_predictors or []
    important_columns_for_visualization = important_columns_for_visualization or []

    # Import here to avoid circular dependencies
    from lib.sphere_config import get_row_limit
    
    # Get row limit from config
    default_row_limit = get_row_limit()

    # Build job plan with basic sphere jobs
    job_plan = [
        dict(
            job_type="create_structured_data",
            spec={
                "column_overrides": column_overrides or {},
                "string_list_delimiter": string_list_delimiter,
            },
            job_id=None,
        ),
        dict(
            job_type= "train_es",
            spec={
                # Use provided epochs or default to auto-calculate
                "epochs": epochs if epochs is not None else 0,
                # Row limit from config (customizable via /sphere/app/config.json)
                "row_limit": default_row_limit,
                "is_production": True,
                "ignore_cols": [],
                "learning_rate": 0.0003,
                "batch_size": 0,  # Auto-calculate based on dataset size
                # DropoutScheduler parameters
                "enable_dropout_scheduler": True,
                "dropout_schedule_type": "linear_decay",
                "initial_dropout": 0.5,
                "final_dropout": 0.1,
                # Movie frame and WeightWatcher intervals (configurable via API)
                "movie_frame_interval": movie_frame_interval,
                "weightwatcher_save_every": weightwatcher_save_every,
                # VISUALIZATION ONLY: Prefer rows with non-null values in these columns for epoch projections
                # ⚠️ IMPORTANT: Has NO EFFECT on model training, only affects visualization sampling
                "important_columns_for_visualization": important_columns_for_visualization,
                # User metadata for identification
                "user_metadata": user_metadata,
            },
            job_id=None,
        ),
        dict(
            job_type="train_knn",
            spec={},
            job_id=None,
        ),
        dict(
            job_type="run_clustering",
            spec={},
            job_id=None,
        ), 
    ]
    
    # Add single predictor training jobs to the plan
    single_predictors_artifacts = []
    training_metrics_artifacts = []
    
    for i, predictor_spec in enumerate(single_predictors):
        # Convert pydantic model to dict if needed
        if hasattr(predictor_spec, 'dict'):
            spec_dict = predictor_spec.dict()
        else:
            spec_dict = predictor_spec
        
        # Add user_metadata to predictor spec if not already present
        if user_metadata and 'user_metadata' not in spec_dict:
            spec_dict['user_metadata'] = user_metadata
            
        # Add job to plan
        job_plan.append(dict(
            job_type="train_single_predictor",
            spec=spec_dict,
            job_id=None,
            predictor_index=i,  # Track which predictor this is
        ))
        
        # Initialize artifact paths (will be filled when jobs complete)
        single_predictors_artifacts.append(None)
        training_metrics_artifacts.append(None)

    session_doc = dict(
        created_at=created_at,
        session_type="sphere",
        session_id=session_id,
        name=name,  # Optional name for identification and metadata
        status=SessionStatus.READY,
        job_plan=job_plan,
        # Paths to artifacts that are shared across jobs.
        input_data=input_filename,
        embedding_space=None,
        sqlite_db=None,
        vector_db=None,
        projections=None,
        preview_png=None,
        strings_cache=None,
        # Support multiple single predictors
        single_predictors=single_predictors_artifacts,
        training_metrics=training_metrics_artifacts,
        # User metadata for identification
        user_metadata=user_metadata,
    )

    return session_doc


def create_cloned_session(session_id: str, created_at: datetime, embedding_space_path: str, strings_cache_path: str | None = None,
                         source_session_id: str = None, source_compute: str = None, validation_loss: float | None = None,
                         epoch: int | None = None, training_metadata: dict | None = None, name: str | None = None) -> dict:
    """Create a ready session from a cloned embedding space."""
    session_doc = dict(
        created_at=created_at,
        session_type="sphere",
        session_id=session_id,
        name=name,
        status=SessionStatus.READY,  # Ready - no job_plan needed
        job_plan=[],  # Empty - session is ready to use
        input_data=None,  # No input data for cloned sessions
        embedding_space=embedding_space_path,
        sqlite_db=None,
        vector_db=None,
        projections=None,
        preview_png=None,
        strings_cache=strings_cache_path,
        single_predictors=[],
        training_metrics=[],
        clone_metadata={
            "source_session_id": source_session_id,
            "source_compute": source_compute,
            "validation_loss": validation_loss,
            "epoch": epoch,
            "training_metadata": training_metadata,
            "cloned_at": created_at.isoformat() if created_at else None,
        }
    )
    
    return session_doc


def create_embedding_space_session(name: str, s3_training_path: str, s3_validation_path: str, session_id: str = None, user_metadata: dict = None):
    """Create a session specifically for training an embedding space from S3 datasets."""
    # Check if node is upgrading
    upgrade_lock_file = Path("/tmp/auto-upgrade.lock")
    if upgrade_lock_file.exists():
        hostname = socket.gethostname()
        raise NodeUpgradingException(f"Node {hostname} is currently upgrading and cannot accept training requests. Please try again in a few minutes or use a different node.")

    # Ensure all necessary directories exist before creating sessions
    ensure_directories_exist()

    created_at = datetime.now(tz=ZoneInfo("America/New_York"))

    if session_id is None:
        unique_string = str(uuid4())[:6]
        session_timestamp = created_at.strftime('%Y%m%d-%H%M%S')
        # New format: {uuid}-{yyyy}{mm}{dd}-{hh}{mm}{ss}
        session_id = f"{unique_string}-{session_timestamp}"

    # Create job plan for embedding space training
    job_plan = [
        {
            "job_type": "create_structured_data",
            "spec": {
                "s3_training_dataset": s3_training_path,
                "s3_validation_dataset": s3_validation_path,
                "name": name
            },
            "job_id": None,
        },
        {
            "job_type": "train_es",
            "spec": {
                "user_metadata": user_metadata,
            },
            "job_id": None,
        },
        {
            "job_type": "train_knn",
            "spec": {},
            "job_id": None,
        },
        {
            "job_type": "run_clustering",
            "spec": {},
            "job_id": None,
        }
    ]

    # Create session directory and data path
    # New structure: es_train/{session_id}/
    es_train_dir = config.data_dir / "es_train"
    es_train_dir.mkdir(parents=True, exist_ok=True)
    session_dir = es_train_dir / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    
    # For embedding space sessions, the data will be downloaded by the first job
    input_data_path = session_dir / f"{name}_training_data.csv"

    session_doc = {
        "session_id": session_id,
        "session_type": "embedding_space",
        "name": name,
        "status": SessionStatus.READY,
        "created_at": created_at,
        "input_data": str(input_data_path),
        "s3_training_dataset": s3_training_path,
        "s3_validation_dataset": s3_validation_path,
        "job_plan": job_plan,
        "projected_points": str(session_dir / "projection.json"),
        "preview_png": str(session_dir / "preview.png"),
        "embedding_space": str(session_dir / "embedding_space.json"),
        "sqlite_db": str(session_dir / "embedding_space.db"),
        "vector_db": str(session_dir / "vector_db.lance"),
        "projections": str(session_dir / "projections.json"),
        "strings_cache": str(session_dir / "strings_cache.pkl"),
        "user_metadata": user_metadata,  # User metadata for identification
    }

    return session_doc


def create_fine_tune_embedding_space_session(
    name: str,
    parent_session_id: str | None = None,
    parent_embedding_space_path: str | None = None,
    s3_training_path: str = None,
    s3_validation_path: str = None,
    session_id: str = None,
    user_metadata: dict = None
):
    """Create a session for fine-tuning an existing embedding space on new data."""
    logger.info(f"🔧 Creating fine-tuning session for embedding space: {name}")
    
    # Check if node is upgrading
    upgrade_lock_file = Path("/tmp/auto-upgrade.lock")
    if upgrade_lock_file.exists():
        hostname = socket.gethostname()
        raise NodeUpgradingException(f"Node {hostname} is currently upgrading and cannot accept training requests. Please try again in a few minutes or use a different node.")
    
    # Ensure all necessary directories exist
    ensure_directories_exist()
    
    created_at = datetime.now(tz=ZoneInfo("America/New_York"))
    
    if session_id is None:
        unique_string = str(uuid4())[:6]
        session_timestamp = created_at.strftime('%Y%m%d-%H%M%S')
        session_id = f"{unique_string}-{session_timestamp}"
    
    # Load parent embedding space to get original training info
    parent_es_path = None
    if parent_session_id:
        logger.info(f"📂 Loading parent embedding space from session: {parent_session_id}")
        parent_session = load_session(parent_session_id)
        if not parent_session:
            raise ValueError(f"Parent session {parent_session_id} not found")
        parent_es_path = parent_session.get("embedding_space")
        if not parent_es_path or not Path(parent_es_path).exists():
            raise FileNotFoundError(f"Parent embedding space not found at: {parent_es_path}")
    elif parent_embedding_space_path:
        parent_es_path = parent_embedding_space_path
        if not Path(parent_es_path).exists():
            raise FileNotFoundError(f"Parent embedding space not found at: {parent_embedding_space_path}")
    
    if not parent_es_path:
        raise ValueError("Either parent_session_id or parent_embedding_space_path must be provided")
    
    logger.info(f"📂 Loading parent embedding space from: {parent_es_path}")
    
    # Load the parent embedding space
    from featrix.neural.io_utils import load_embedded_space
    parent_es = load_embedded_space(parent_es_path, force_cpu=True)
    
    if not parent_es:
        raise ValueError(f"Failed to load parent embedding space from: {parent_es_path}")
    
    # Get original dataset size and epoch count
    original_train_size = len(parent_es.train_input_data) if hasattr(parent_es, 'train_input_data') else 0
    original_epochs = parent_es.n_epochs if hasattr(parent_es, 'n_epochs') and parent_es.n_epochs else 0
    
    # If n_epochs is not set, try to get from training_info
    if not original_epochs:
        training_info = getattr(parent_es, 'training_info', {})
        progress_info = training_info.get('progress_info', {})
        original_epochs = progress_info.get('epoch_total', 0)
        if not original_epochs:
            # Try to get from loss_history length
            loss_history = progress_info.get('loss_history', [])
            if loss_history:
                original_epochs = len(loss_history)
    
    logger.info(f"📊 Parent embedding space info:")
    logger.info(f"   Original training dataset size: {original_train_size} rows")
    logger.info(f"   Original epochs: {original_epochs}")
    
    if original_epochs == 0:
        logger.warning(f"⚠️  Could not determine original epoch count, defaulting to 100")
        original_epochs = 100
    
    # Download new datasets to get their sizes
    logger.info(f"📥 Downloading new datasets to calculate size...")
    
    import boto3
    import pandas as pd
    
    s3_client = boto3.client('s3')
    
    def download_and_count_rows(s3_url: str) -> int:
        """Download S3 file temporarily and count rows."""
        import tempfile
        import os
        
        # Parse S3 URL
        if not s3_url.startswith('s3://'):
            raise ValueError(f"Invalid S3 URL: {s3_url}")
        
        s3_path = s3_url[5:]  # Remove 's3://'
        bucket, key = s3_path.split('/', 1)
        
        # Download to temp file
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.csv', delete=False) as tmp_file:
            tmp_path = tmp_file.name
            try:
                s3_client.download_file(bucket, key, tmp_path)
                
                # Count rows (read CSV)
                df = pd.read_csv(tmp_path, nrows=0)  # Just get header
                # Count non-header rows by reading file
                with open(tmp_path, 'r') as f:
                    row_count = sum(1 for line in f) - 1  # Subtract header
                return row_count
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
    
    try:
        new_train_size = download_and_count_rows(s3_training_path)
        new_val_size = download_and_count_rows(s3_validation_path)
        new_total_size = new_train_size + new_val_size
    except Exception as e:
        logger.warning(f"⚠️  Could not download datasets to count rows: {e}")
        logger.warning(f"   Will use default F=1.0 (same dataset size)")
        new_total_size = original_train_size
        new_train_size = int(original_train_size * 0.8)
        new_val_size = int(original_train_size * 0.2)
    
    logger.info(f"📊 New dataset info:")
    logger.info(f"   New training dataset size: {new_train_size} rows")
    logger.info(f"   New validation dataset size: {new_val_size} rows")
    logger.info(f"   New total size: {new_total_size} rows")
    
    # Calculate F = len(new_dataset) / len(old_dataset)
    F = new_total_size / original_train_size if original_train_size > 0 else 1.0
    logger.info(f"📐 Dataset size ratio F = {new_total_size} / {original_train_size} = {F:.4f}")
    
    # Calculate new epochs = original_epochs / F
    new_epochs = int(original_epochs / F) if F > 0 else original_epochs
    if new_epochs < 1:
        new_epochs = 1
    elif new_epochs > 1000:
        logger.warning(f"⚠️  Calculated epochs ({new_epochs}) is very high, capping at 1000")
        new_epochs = 1000
    
    logger.info(f"🎯 Fine-tuning will use {new_epochs} epochs (original: {original_epochs}, F: {F:.4f})")
    
    # Create job plan for fine-tuning
    job_plan = [
        {
            "job_type": "create_structured_data",
            "spec": {
                "s3_training_dataset": s3_training_path,
                "s3_validation_dataset": s3_validation_path,
                "name": name
            },
            "job_id": None,
        },
        {
            "job_type": "train_es",
            "spec": {
                "epochs": new_epochs,
                "parent_embedding_space_path": str(Path(parent_es_path).resolve()),
                "fine_tune": True,
                "user_metadata": user_metadata,
            },
            "job_id": None,
        },
        {
            "job_type": "train_knn",
            "spec": {},
            "job_id": None,
        },
        {
            "job_type": "run_clustering",
            "spec": {},
            "job_id": None,
        }
    ]
    
    # Create session directory
    es_train_dir = config.data_dir / "es_train"
    es_train_dir.mkdir(parents=True, exist_ok=True)
    session_dir = es_train_dir / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    
    input_data_path = session_dir / f"{name}_training_data.csv"
    
    session_doc = {
        "session_id": session_id,
        "session_type": "embedding_space_finetune",
        "name": name,
        "status": SessionStatus.READY,
        "created_at": created_at,
        "input_data": str(input_data_path),
        "s3_training_dataset": s3_training_path,
        "s3_validation_dataset": s3_validation_path,
        "parent_session_id": parent_session_id,
        "parent_embedding_space_path": str(Path(parent_es_path).resolve()),
        "fine_tune_info": {
            "original_train_size": original_train_size,
            "original_epochs": original_epochs,
            "new_train_size": new_train_size,
            "new_val_size": new_val_size,
            "new_total_size": new_total_size,
            "F": F,
            "calculated_epochs": new_epochs,
        },
        "job_plan": job_plan,
        "projected_points": str(session_dir / "projection.json"),
        "preview_png": str(session_dir / "preview.png"),
        "embedding_space": str(session_dir / "embedding_space.json"),
        "sqlite_db": str(session_dir / "embedding_space.db"),
        "vector_db": str(session_dir / "vector_db.lance"),
        "projections": str(session_dir / "projections.json"),
        "strings_cache": str(session_dir / "strings_cache.pkl"),
        "user_metadata": user_metadata,
    }
    
    logger.info(f"✅ Created fine-tuning session: {session_id}")
    
    return session_doc


def create_foundation_model_session(session_id: str, created_at: datetime, foundation_model_id: str, target_spec: dict, input_filename: str | None = None, name: str | None = None, user_metadata: dict | None = None):
    """Create a session that trains a predictor on a foundation model (existing embedding space)."""
    logger.info(f"🏗️  Creating foundation model session {session_id} based on foundation {foundation_model_id}")
    
    # Load the foundation model session to get its embedding space
    foundation_session = load_session(foundation_model_id)
    embedding_space_path = foundation_session.get("embedding_space")
    strings_cache_path = foundation_session.get("strings_cache")
    
    # Resolve to absolute path and validate
    if embedding_space_path:
        embedding_space_path = str(Path(embedding_space_path).resolve())
        if not Path(embedding_space_path).exists():
            raise FileNotFoundError(f"Foundation model embedding space not found at: {embedding_space_path}")
    else:
        raise ValueError(f"Foundation model {foundation_model_id} does not have an embedding_space path set")
    
    # Validate target_spec
    if "target_column" not in target_spec:
        raise ValueError("target_column is required in target_spec")
    if "target_column_type" not in target_spec:
        raise ValueError("target_column_type is required in target_spec")
    
    # Use foundation model's input data if not provided
    if input_filename is None:
        input_filename = foundation_session.get("input_data")
        logger.info(f"📁 Using foundation model's input data: {input_filename}")
    
    # Create job plan: ONLY create_structured_data and train_single_predictor
    job_plan = [
        dict(
            job_type="create_structured_data",
            spec={},
            job_id=None,
        ),
        dict(
            job_type="train_single_predictor",
            spec=target_spec,
            job_id=None,
            predictor_index=0,
        ),
    ]
    
    session_doc = dict(
        created_at=created_at,
        session_type="predictor",
        session_id=session_id,
        name=name,
        status=SessionStatus.READY,
        job_plan=job_plan,
        embedding_space=embedding_space_path,
        strings_cache=strings_cache_path,
        input_data=input_filename,
        sqlite_db=None,
        vector_db=None,
        projections=None,
        preview_png=None,
        single_predictors=[None],
        training_metrics=[None],
        foundation_model_id=foundation_model_id,
        user_metadata=user_metadata,
    )
    
    logger.info(f"✅ Foundation model session created: {session_id}")
    
    return session_doc


def create_session(session_type: str, session_id: str = None, start: bool = True, input_filename: str | None = None, name: str = None, session_name_prefix: str = None, target_spec: dict = None, single_predictors: list = None, epochs: int = None, column_overrides: dict = None, string_list_delimiter: str = "|", movie_frame_interval: int = 3, weightwatcher_save_every: int = 5, important_columns_for_visualization: list = None, user_metadata: dict = None):
    """Create a new session of the specified type."""
    # Check if node is upgrading
    upgrade_lock_file = Path("/tmp/auto-upgrade.lock")
    if upgrade_lock_file.exists():
        hostname = socket.gethostname()
        raise NodeUpgradingException(f"Node {hostname} is currently upgrading and cannot accept training requests. Please try again in a few minutes or use a different node.")

    # Ensure all necessary directories exist before creating sessions
    ensure_directories_exist()

    created_at = datetime.now(tz=ZoneInfo("America/New_York"))

    # Sanitize session_name_prefix: replace slashes and dots with underscores
    if session_name_prefix:
        session_name_prefix = session_name_prefix.replace('/', '_').replace('.', '_')
        logger.debug(f"📋 Sanitized session_name_prefix: {session_name_prefix}")

    if session_id is None:
        # Generate full UUID
        full_uuid = str(uuid4())
        
        # If prefix is provided, format as <prefix>-<full-uuid>
        # For embedding_space sessions, always use new format: <uuid6>-<timestamp>
        # Otherwise, use the original format: <timestamp>_<uuid6>
        if session_name_prefix:
            session_id = f"{session_name_prefix}-{full_uuid}"
        elif session_type == "embedding_space":
            # Embedding space sessions use new format: {uuid}-{timestamp}
            unique_string = full_uuid[:6]
            session_timestamp = created_at.strftime('%Y%m%d-%H%M%S')
            session_id = f"{unique_string}-{session_timestamp}"
        else:
            unique_string = full_uuid[:6]
            session_timestamp = created_at.strftime('%Y%m%d-%H%M%S')
            session_id = "_".join([session_timestamp, unique_string])
    else:
        # session_id was provided - if prefix is also provided, ensure session_id uses it with UUID
        if session_name_prefix:
            # Prefix is provided - session_id MUST be in format {prefix}-{uuid}
            # If it's not, create a new one with the prefix
            if not session_id.startswith(f"{session_name_prefix}-"):
                full_uuid = str(uuid4())
                session_id = f"{session_name_prefix}-{full_uuid}"
                logger.info(f"📋 Created session_id with prefix and UUID: {session_id}")
            # If it does start with prefix, verify it has UUID-like suffix (contains dashes after prefix)
            elif len(session_id) <= len(session_name_prefix) + 1:
                # Too short - probably just the prefix, add UUID
                full_uuid = str(uuid4())
                session_id = f"{session_name_prefix}-{full_uuid}"
                logger.info(f"📋 Added UUID suffix to session_id: {session_id}")

    if session_type == "sphere":
        session_doc = create_sphere_session(
            session_id=session_id,
            created_at=created_at,
            input_filename=input_filename,
            name=name,
            single_predictors=single_predictors,
            epochs=epochs,
            column_overrides=column_overrides,
            string_list_delimiter=string_list_delimiter,
            movie_frame_interval=movie_frame_interval,
            weightwatcher_save_every=weightwatcher_save_every,
            important_columns_for_visualization=important_columns_for_visualization,
            user_metadata=user_metadata,
        )
    elif session_type == "embedding_space":
        session_doc = create_embedding_space_session(
            name=name or input_filename or "embedding_space",
            s3_training_path=target_spec.get("training_dataset") if target_spec else None,
            s3_validation_path=target_spec.get("validation_dataset") if target_spec else None,
            session_id=session_id,
            user_metadata=user_metadata,
        )
    else:
        raise ValueError(f"Unsupported session type {session_type}")

    save_session(session_id=session_id, session_doc=session_doc, exist_ok=False)

    # Dispatch first job in chain if start=True
    if start:
        from lib.session_chains import dispatch_next_job_in_chain
        dispatch_next_job_in_chain(session_id=session_id)

    return session_doc


def find_closest_points(session_id: str, query_record: Dict[str, Any], k: int = 5) -> Dict[str, Any]:
    """Find the k closest points to a query record in the embedding space."""
    logger.debug(sys.path)
    pp = str(Path("./lib").resolve())
    if pp not in sys.path:
        sys.path.insert(0, pp)
    from featrix.neural.io_utils import load_embedded_space
    from lib.vector_db import CSVtoLanceDB

    session = load_session(session_id)

    # validate faiss index path
    vector_db_path = session.get("vector_db")
    if vector_db_path is None:
        raise ValueError(f"Session {session_id} does not have a vector_db")
    
    vector_db_path = Path(vector_db_path)
    if not vector_db_path.is_dir():
        raise FileNotFoundError(f"LanceDB data at {vector_db_path} does not exist")

    # validate embedding space path
    embedding_space_path = session.get("embedding_space")
    if embedding_space_path is None:
        raise ValueError(f"Session {session_id} does not have an embedding space")

    embedding_space_path = Path(embedding_space_path)
    if not embedding_space_path.is_file():
        raise FileNotFoundError(f"Embedding space {embedding_space_path} does not exist")

    # load the embedding space
    try: 
        embedded_space = load_embedded_space(embedding_space_path)
    except Exception as e:
        raise ValueError(f"Error loading embedding space: {e}")

    # validate sqlite_db_path
    sqlite_db_path = session.get("sqlite_db")
    if sqlite_db_path is None:
        raise ValueError(f"Session {session_id} does not have an sqlite db")
    
    sqlite_db_path = Path(sqlite_db_path)
    if not sqlite_db_path.is_file():
        raise FileNotFoundError(f"Sqlite db at {sqlite_db_path} does not exist")

    # load the faiss index
    try:
        vec_db = CSVtoLanceDB(
            featrix_es=embedded_space, 
            sqlite_db_path=sqlite_db_path, 
            lancedb_path=vector_db_path)
        vec_db.load_existing()
    except Exception as e:
        raise ValueError(f"Error loading faiss index: {e}")

    # get the nearest neighbors
    try:
        result = vec_db.search(query_record, k=k)
    except Exception as e:
        raise ValueError(f"Error querying nearest neighbors: {e}")

    # Add server metadata for debugging    
    result["_meta"] = {
        "compute_cluster": socket.gethostname(),
        "compute_cluster_time": datetime.utcnow().isoformat() + "Z",
    }
    
    return result


def get_queue_summary() -> dict:
    """Get a summary of all queue states for admin/debugging purposes."""
    from lib.queue_manager import iterate_over_jobs_in_queue
    from lib.job_manager import JobStatus
    
    queue_summary = {}
    
    # Check all known queue types
    known_queues = [
        "create_structured_data",
        "train_es", 
        "train_knn",
        "run_clustering",
        "train_single_predictor"
    ]
    
    for job_type in known_queues:
        ready_jobs = []
        running_jobs = []
        total_jobs = 0
        
        try:
            for job in iterate_over_jobs_in_queue(job_type):
                total_jobs += 1
                status = job.get("status")
                
                if status == JobStatus.READY:
                    ready_jobs.append(job)
                elif status == JobStatus.RUNNING:
                    running_jobs.append(job)
        except Exception as e:
            queue_summary[job_type] = {
                "exists": True,
                "error": str(e),
                "status": "error_reading_queue"
            }
            continue
        
        queue_summary[job_type] = {
            "exists": True,
            "ready_jobs": len(ready_jobs),
            "running_jobs": len(running_jobs),
            "total_jobs": total_jobs,
            "status": "active" if len(running_jobs) > 0 else "idle",
            "next_job_id": ready_jobs[0].get("job_id") if ready_jobs else None,
            "currently_running": [job.get("job_id") for job in running_jobs],
        }
    
    return queue_summary


def add_notification_email_to_session(session_id: str, email: str):
    """Add a notification email to a session."""
    session_doc = load_session(session_id)

    if "notification_email" not in session_doc:
        session_doc["notification_email"] = []

    session_doc["notification_email"].append(email)

    save_session(session_id, session_doc, exist_ok=True)

    logger.info(f"Notification email {email} added to session {session_id}")


# Import publish/deprecate functions - these need to be migrated from featrix_queue
# For now, provide stubs
def publish_session(*args, **kwargs):
    raise NotImplementedError("publish_session not yet migrated from featrix_queue")
def deprecate_session(*args, **kwargs):
    raise NotImplementedError("deprecate_session not yet migrated from featrix_queue")
def unpublish_session(*args, **kwargs):
    raise NotImplementedError("unpublish_session not yet migrated from featrix_queue")

# Re-export SessionStatus for backward compatibility
__all__ = [
    'SessionStatus',
    'NodeUpgradingException',
    'load_session',
    'save_session',
    'resolve_session_path',
    'get_session_info',
    'iterate_over_sessions',
    'serialize_session',
    'ensure_directories_exist',
    'get_version_info',
    'create_session',
    'create_sphere_session',
    'create_embedding_space_session',
    'create_fine_tune_embedding_space_session',
    'create_foundation_model_session',
    'create_cloned_session',
    'find_closest_points',
    'get_queue_summary',
    'add_notification_email_to_session',
    'publish_session',
    'deprecate_session',
    'unpublish_session',
]

