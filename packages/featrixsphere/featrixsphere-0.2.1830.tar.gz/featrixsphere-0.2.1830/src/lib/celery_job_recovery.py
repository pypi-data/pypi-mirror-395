"""
Celery Job Recovery

Scans Redis for incomplete jobs (RUNNING or recently FAILED) and re-dispatches them.
This replaces the old file-based worker recovery mechanism.
"""
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from zoneinfo import ZoneInfo

from celery_app import app
from lib.job_manager import (
    get_redis_client, load_job, save_job, update_job_status,
    JobStatus, get_job_output_path
)
from lib.session_chains import dispatch_next_job_in_chain
from utils import convert_from_iso, convert_to_iso

logger = logging.getLogger(__name__)


def _determine_restart_reason(upgrade_flag_path: Path) -> str:
    """
    Determine why the server restarted.
    
    Returns:
        'upgrade', 'crash', or 'dev'
    """
    if upgrade_flag_path.exists():
        return 'upgrade'
    
    # Check if we're in a dev environment (based on hostname or other indicators)
    import socket
    hostname = socket.gethostname().lower()
    if 'dev' in hostname or 'test' in hostname or 'local' in hostname:
        return 'dev'
    
    return 'crash'


def _should_retry_failed_job(job: dict) -> bool:
    """
    Check if a FAILED job should be retried.
    
    Only retry jobs that failed within the last hour.
    """
    finished_at = job.get('finished_at')
    if not finished_at:
        return False
    
    # Convert to datetime if it's a string
    if isinstance(finished_at, str):
        finished_at = convert_from_iso(finished_at)
    
    # Only retry if failed within last hour
    now = datetime.now(tz=ZoneInfo("America/New_York"))
    time_since_failure = now - finished_at
    
    if time_since_failure > timedelta(hours=1):
        return False
    
    # Check if job was manually killed (don't retry those)
    recovery_info = job.get("recovery_info", [])
    for recovery in recovery_info:
        if recovery.get("manual_kill", False) or recovery.get("reason") == "manual_kill":
            logger.info(f"Job {job.get('job_id')} has manual_kill in recovery history - will not retry")
            return False
    
    return True


def _should_recover_job(job: dict, restart_reason: str) -> bool:
    """
    Check if a job should be recovered based on retry limits.
    
    Args:
        job: Job data dict
        restart_reason: 'upgrade', 'crash', or 'dev'
        
    Returns:
        True if job should be recovered
    """
    # Always recover for upgrades and dev restarts
    if restart_reason in ['upgrade', 'dev']:
        return True
    
    # For crashes, check retry limits
    recovery_info = job.get("recovery_info", [])
    if not recovery_info:
        return True  # No previous recovery attempts
    
    # Count recovery attempts in last 24 hours
    now = datetime.now(tz=ZoneInfo("America/New_York"))
    recent_recoveries = 0
    
    for recovery in recovery_info:
        recovered_at = recovery.get("recovered_at")
        if recovered_at:
            if isinstance(recovered_at, str):
                recovered_at = convert_from_iso(recovered_at)
            
            if (now - recovered_at) < timedelta(hours=24):
                recent_recoveries += 1
    
    # Limit to 3 retries per 24 hours for crash recovery
    max_retries = 3
    if recent_recoveries >= max_retries:
        logger.warning(f"Job {job.get('job_id')} has {recent_recoveries} recent recoveries - blocking retry")
        return False
    
    return True


def _add_recovery_info(job: dict, restart_reason: str):
    """Add recovery info to job metadata."""
    if "recovery_info" not in job:
        job["recovery_info"] = []
    
    job["recovery_info"].append({
        "recovered_at": convert_to_iso(datetime.now(tz=ZoneInfo("America/New_York"))),
        "restart_reason": restart_reason,
        "previous_status": job.get("status"),
        "previous_job_id": job.get("job_id")
    })


def _recover_job(job: dict, restart_reason: str) -> Optional[str]:
    """
    Recover a single job by re-dispatching it.
    
    Args:
        job: Job data dict
        restart_reason: 'upgrade', 'crash', or 'dev'
        
    Returns:
        New task ID if successful, None otherwise
    """
    job_id = job.get('job_id')
    job_type = job.get('job_type')
    session_id = job.get('session_id')
    job_spec = job.get('job_spec', {})
    
    # Try to infer job_type from job_spec or other fields if missing/unknown
    if not job_type or job_type == 'unknown':
        # Try to infer from job_spec keys or queue_name
        queue_name = job.get('queue_name') or job_spec.get('queue_name')
        if queue_name:
            # Map queue names to job types
            queue_to_type = {
                'cpu_data_tasks': 'create_structured_data',
                'train_es': 'train_es',
                'train_knn': 'train_knn',
                'gpu_training': 'train_single_predictor',  # Most common GPU job
                'cpu_worker': 'run_clustering',  # Most common CPU job
            }
            inferred_type = queue_to_type.get(queue_name)
            if inferred_type:
                logger.info(f"🔍 Inferred job_type '{inferred_type}' from queue_name '{queue_name}' for job {job_id}")
                job_type = inferred_type
            else:
                logger.warning(f"⚠️  Could not infer job_type from queue_name '{queue_name}' for job {job_id}")
        
        # Try to infer from job_spec structure
        if (not job_type or job_type == 'unknown') and job_spec:
            if 'data_file' in job_spec or 'sqlite_db' in job_spec:
                if 'target_column' in job_spec:
                    inferred_type = 'train_single_predictor'
                elif 'embedding_space' in job_spec:
                    inferred_type = 'train_knn'
                else:
                    inferred_type = 'create_structured_data'
                logger.info(f"🔍 Inferred job_type '{inferred_type}' from job_spec structure for job {job_id}")
                job_type = inferred_type
        
        # Try to infer from job_id pattern (last resort)
        if (not job_type or job_type == 'unknown') and job_id:
            inferred_type = None
            # Job IDs sometimes contain job type in the name
            job_id_lower = job_id.lower()
            if 'train_es' in job_id_lower or job_id_lower.startswith('es_'):
                inferred_type = 'train_es'
            elif 'train_single_predictor' in job_id_lower or job_id_lower.startswith('sp_'):
                inferred_type = 'train_single_predictor'
            elif 'create_structured_data' in job_id_lower or job_id_lower.startswith('csd_'):
                inferred_type = 'create_structured_data'
            elif 'train_knn' in job_id_lower or job_id_lower.startswith('knn_'):
                inferred_type = 'train_knn'
            
            if inferred_type:
                logger.info(f"🔍 Inferred job_type '{inferred_type}' from job_id pattern for job {job_id}")
                job_type = inferred_type
        
        # Try to infer from session's job_plan (if session_id is available)
        if (not job_type or job_type == 'unknown') and session_id and session_id != 'unknown':
            try:
                from lib.session_manager import load_session
                session = load_session(session_id)
                if session and hasattr(session, 'job_plan'):
                    # Look for this job_id in the job_plan
                    for planned_job in session.job_plan:
                        if planned_job.get('job_id') == job_id:
                            planned_type = planned_job.get('job_type') or planned_job.get('type')
                            if planned_type:
                                logger.info(f"🔍 Inferred job_type '{planned_type}' from session job_plan for job {job_id}")
                                job_type = planned_type
                                break
            except Exception as e:
                logger.debug(f"Could not load session {session_id} to infer job_type: {e}")
    
    if not job_type or job_type == 'unknown':
        logger.warning(f"⚠️  Job {job_id} missing or unknown job_type - cannot recover")
        logger.warning(f"   Job data: job_type={job.get('job_type')}, queue_name={job.get('queue_name')}, session_id={session_id}")
        logger.warning(f"   job_spec keys: {list(job_spec.keys()) if job_spec else 'None'}")
        logger.warning(f"   All job keys: {list(job.keys())}")
        return None
    
    if not session_id:
        logger.warning(f"⚠️  Job {job_id} missing session_id - cannot recover")
        return None
    
    # CRITICAL: Check if this job already has a job_id in the session's job_plan
    # If it does, and it's different from the current job_id, another process may have
    # already recovered or re-dispatched it. Don't create duplicates.
    try:
        from lib.session_manager import load_session
        session = load_session(session_id)
        job_plan = session.get("job_plan", [])
        
        # Check if any job in the plan has this job_id or a different job_id for the same job_type
        for job_desc in job_plan:
            if job_desc.get("job_type") == job_type:
                existing_job_id = job_desc.get("job_id")
                if existing_job_id and existing_job_id != job_id:
                    # This job type already has a different job_id - it may have been re-dispatched
                    logger.info(f"⏭️  Job {job_id} (type: {job_type}) already has job_id {existing_job_id} in session - skipping recovery to prevent duplicates")
                    return existing_job_id  # Return the existing job_id
    except Exception as check_err:
        logger.warning(f"⚠️  Could not check session job_plan for job {job_id}: {check_err}")
        # Continue with recovery anyway - better to recover than skip
    
    try:
        # Add recovery info
        _add_recovery_info(job, restart_reason)
        
        # Determine which Celery task to call
        task_name_map = {
            'create_structured_data': 'celery_app.create_structured_data',
            'train_es': 'celery_app.train_es',
            'train_knn': 'celery_app.train_knn',
            'train_single_predictor': 'celery_app.train_single_predictor',
            'run_clustering': 'celery_app.run_clustering',
            'project_training_movie_frame': 'celery_app.project_training_movie_frame',
        }
        
        task_name = task_name_map.get(job_type)
        if not task_name:
            logger.warning(f"⚠️  Unknown job_type {job_type} for job {job_id}")
            return None
        
        # For create_structured_data, we need data_file
        data_file = None
        if job_type == 'create_structured_data':
            # Try to get data_file from job_spec or session
            data_file = job_spec.get('data_file')
            if not data_file:
                try:
                    from lib.session_manager import load_session
                    session = load_session(session_id)
                    input_data = session.get('input_data')
                    if input_data and not input_data.startswith('s3://'):
                        input_path = Path(input_data)
                        if input_path.is_absolute():
                            data_file = str(input_path)
                        else:
                            from config import config
                            data_file = str(config.data_dir / input_data)
                except Exception as e:
                    logger.warning(f"⚠️  Could not get data_file for job {job_id}: {e}")
                    # Continue anyway - task may handle missing data_file
        
        # Re-dispatch the task
        logger.info(f"🔄 Re-dispatching job {job_id} (type: {job_type}, session: {session_id})")
        
        # Determine queue
        if job_type in ['train_es', 'train_single_predictor']:
            queue = 'gpu_training'
        else:
            queue = 'cpu_worker'
        
        # Match actual task signatures from celery_app.py
        if job_type == 'create_structured_data':
            logger.info(f"🔄 RESTARTING JOB: {job_type} (Job ID: {job_id}, Session: {session_id if session_id else 'N/A'}, Reason: {restart_reason})")
            new_task = app.send_task(
                task_name,
                args=[job_spec, job_id, data_file, session_id],
                queue=queue
            )
            logger.info(f"✅ Job {job_id} restarted with new task ID: {new_task.id}")
        elif job_type == 'train_es':
            # Check if train_es job already completed successfully before re-dispatching
            try:
                # First check job status - if it's DONE, don't re-dispatch
                job_data = load_job(job_id)
                if job_data:
                    job_status = job_data.get('status')
                    if isinstance(job_status, JobStatus):
                        status_value = job_status.value
                    else:
                        status_value = str(job_status) if job_status else None
                    
                    if status_value == JobStatus.DONE.value:
                        logger.info(f"⏭️  Skipping train_es recovery for job {job_id} - job status is DONE")
                        return None  # Don't re-dispatch if job already completed
                
                # Also check if embedding space already exists (even if job status is unclear)
                from lib.session_manager import load_session
                from pathlib import Path
                session = load_session(session_id)
                if session:
                    embedding_space_path = session.get("embedding_space")
                    foundation_model_id = session.get("foundation_model_id")
                    if foundation_model_id or (embedding_space_path and Path(embedding_space_path).exists()):
                        logger.info(f"⏭️  Skipping train_es recovery for job {job_id} - embedding space already exists")
                        logger.info(f"   foundation_model_id: {foundation_model_id}")
                        logger.info(f"   embedding_space_path: {embedding_space_path}")
                        logger.info(f"   embedding_space exists: {Path(embedding_space_path).exists() if embedding_space_path else False}")
                        logger.info(f"   job status: {status_value if job_data else 'unknown'}")
                        return None  # Don't re-dispatch if ES already exists
            except Exception as check_err:
                logger.warning(f"⚠️  Could not check if train_es job completed for job {job_id}: {check_err}")
                # Continue with recovery - better to recover than skip if we can't check
            
            # train_es signature: (job_spec, job_id, session_id, data_file=None, strings_cache='')
            data_file = job_spec.get('data_file') or job_spec.get('sqlite_db')
            strings_cache = job_spec.get('strings_cache', '')
            logger.info(f"🔄 RESTARTING JOB: {job_type} (Job ID: {job_id}, Session: {session_id}, Reason: {restart_reason})")
            new_task = app.send_task(
                task_name,
                args=[job_spec, job_id, session_id, data_file, strings_cache],
                queue=queue
            )
            logger.info(f"✅ Job {job_id} restarted with new task ID: {new_task.id}")
        elif job_type == 'train_knn':
            # train_knn signature: (job_spec, job_id, session_id)
            logger.info(f"🔄 RESTARTING JOB: {job_type} (Job ID: {job_id}, Session: {session_id}, Reason: {restart_reason})")
            new_task = app.send_task(
                task_name,
                args=[job_spec, job_id, session_id],
                queue=queue
            )
            logger.info(f"✅ Job {job_id} restarted with new task ID: {new_task.id}")
        elif job_type == 'train_single_predictor':
            logger.info(f"🔄 RESTARTING JOB: {job_type} (Job ID: {job_id}, Session: {session_id}, Reason: {restart_reason})")
            # train_single_predictor signature: (job_spec, job_id, session_id)
            new_task = app.send_task(
                task_name,
                args=[job_spec, job_id, session_id],
                queue=queue
            )
            logger.info(f"✅ Job {job_id} restarted with new task ID: {new_task.id}")
        elif job_type == 'run_clustering':
            logger.info(f"🔄 RESTARTING JOB: {job_type} (Job ID: {job_id}, Session: {session_id if session_id else 'N/A'}, Reason: {restart_reason})")
            # run_clustering signature: (job_spec)
            new_task = app.send_task(
                task_name,
                args=[job_spec],
                queue=queue
            )
            logger.info(f"✅ Job {job_id} restarted with new task ID: {new_task.id}")
        elif job_type == 'project_training_movie_frame':
            logger.info(f"🔄 RESTARTING JOB: {job_type} (Job ID: {job_id}, Session: {session_id if session_id else 'N/A'}, Reason: {restart_reason})")
            # project_training_movie_frame signature: (job_spec)
            new_task = app.send_task(
                task_name,
                args=[job_spec],
                queue=queue
            )
            logger.info(f"✅ Job {job_id} restarted with new task ID: {new_task.id}")
        else:
            logger.warning(f"⚠️  Unknown job_type {job_type} - cannot re-dispatch")
            return None
        
        new_job_id = new_task.id
        logger.info(f"✅ Re-dispatched job {job_id} as new task {new_job_id}")
        
        # CRITICAL: Update session's job_plan with new job_id to prevent duplicate dispatches
        # If we don't update the session, dispatch_next_job_in_chain will see the old job_id
        # and dispatch the job again, creating duplicates
        try:
            from lib.session_manager import load_session, save_session
            session = load_session(session_id)
            job_plan = session.get("job_plan", [])
            
            # Find the job in job_plan that matches the old job_id
            updated = False
            for job_desc in job_plan:
                if job_desc.get("job_id") == job_id:
                    # Update to new job_id
                    job_desc["job_id"] = new_job_id
                    updated = True
                    logger.info(f"✅ Updated session job_plan: {job_id} → {new_job_id}")
                    break
            
            if updated:
                save_session(session_id, session, exist_ok=True)
                logger.info(f"✅ Session {session_id} job_plan updated with recovered job_id")
            else:
                logger.warning(f"⚠️  Could not find job_id {job_id} in session {session_id} job_plan - may cause duplicate dispatch")
        except Exception as session_err:
            logger.error(f"❌ CRITICAL: Failed to update session job_plan: {session_err}")
            logger.error(f"   This may cause duplicate job dispatches!")
            import traceback
            logger.error(f"   Traceback: {traceback.format_exc()}")
            # Continue anyway - job is already dispatched
        
        # Update job metadata with new task ID
        job['recovered_job_id'] = new_job_id
        job['status'] = JobStatus.READY.value
        job['recovered_at'] = convert_to_iso(datetime.now(tz=ZoneInfo("America/New_York")))
        save_job(new_job_id, job, session_id, job_type)
        
        return new_job_id
        
    except Exception as e:
        logger.error(f"❌ Failed to recover job {job_id}: {e}")
        import traceback
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return None


def recover_interrupted_jobs() -> Dict[str, Any]:
    """
    Scan Redis for incomplete jobs and recover them.
    
    This function:
    1. Finds all RUNNING jobs (interrupted by restart)
    2. Finds recently FAILED jobs (within last hour)
    3. Re-dispatches them via Celery
    
    Returns:
        dict with recovery summary
    """
    recovery_summary = {
        "restart_reason": None,
        "jobs_checked": 0,
        "jobs_recovered": [],
        "jobs_blocked": [],
        "total_recovered": 0
    }
    
    # Determine restart reason
    upgrade_flag_path = Path("/tmp/UPGRADE_SPHERE")
    restart_reason = _determine_restart_reason(upgrade_flag_path)
    recovery_summary["restart_reason"] = restart_reason
    
    logger.info(f"🔍 Celery job recovery started - Reason: {restart_reason}")
    
    # Clean up upgrade flag if it exists
    if upgrade_flag_path.exists():
        try:
            with open(upgrade_flag_path, 'r') as f:
                flag_content = f.read().strip()
            logger.info(f"📋 Upgrade flag contents:\n{flag_content}")
            upgrade_flag_path.unlink()
            logger.info("🗑️  Upgrade flag cleaned up")
        except Exception as e:
            logger.warning(f"Failed to read/remove upgrade flag: {e}")
    
    try:
        client = get_redis_client()
        
        # Scan for all job keys
        jobs_to_recover = []
        cursor = 0
        
        while True:
            cursor, keys = client.scan(cursor, match="job:*", count=100)
            
            for key in keys:
                job_id = key.replace("job:", "")
                job = load_job(job_id)
                
                if not job:
                    continue
                
                recovery_summary["jobs_checked"] += 1
                status = job.get("status")
                
                # Check if status is a JobStatus enum or string
                if hasattr(status, 'value'):
                    status = status.value
                
                # Include RUNNING jobs
                if status == JobStatus.RUNNING.value:
                    jobs_to_recover.append(job)
                    logger.info(f"🔄 Found RUNNING job {job_id} (type: {job.get('job_type')})")
                
                # Include recently FAILED jobs
                elif status == JobStatus.FAILED.value:
                    if _should_retry_failed_job(job):
                        jobs_to_recover.append(job)
                        logger.info(f"🔄 Found recently FAILED job {job_id} (type: {job.get('job_type')})")
                    else:
                        finished_at = job.get('finished_at')
                        if finished_at:
                            if isinstance(finished_at, str):
                                finished_at = convert_from_iso(finished_at)
                            now = datetime.now(tz=ZoneInfo("America/New_York"))
                            age = now - finished_at
                            logger.debug(f"⏭️  Skipping FAILED job {job_id} - failed {age} ago (too old)")
                
                # Log other statuses for debugging
                elif status in [JobStatus.DONE.value, JobStatus.READY.value]:
                    logger.debug(f"⏭️  Skipping {status} job {job_id} (type: {job.get('job_type')}) - not recoverable")
            
            if cursor == 0:
                break
        
        # Recover each job
        for job in jobs_to_recover:
            job_id = job.get('job_id')
            
            # Check if should recover based on retry limits
            if not _should_recover_job(job, restart_reason):
                recovery_summary["jobs_blocked"].append({
                    "job_id": job_id,
                    "reason": "retry_limit_exceeded"
                })
                logger.warning(f"🚫 Job {job_id} exceeded retry limit - not recovering")
                continue
            
            # Recover the job
            new_job_id = _recover_job(job, restart_reason)
            if new_job_id:
                recovery_summary["jobs_recovered"].append({
                    "old_job_id": job_id,
                    "new_job_id": new_job_id,
                    "job_type": job.get('job_type'),
                    "session_id": job.get('session_id')
                })
                recovery_summary["total_recovered"] += 1
        
        # Log summary
        if recovery_summary["total_recovered"] > 0:
            logger.info(f"🎯 Job recovery complete: {recovery_summary['total_recovered']} jobs recovered")
            logger.info(f"   Restart reason: {restart_reason}")
            logger.info(f"   Jobs checked: {recovery_summary['jobs_checked']}")
            logger.info(f"   Jobs blocked: {len(recovery_summary['jobs_blocked'])}")
        else:
            logger.info(f"✅ No jobs needed recovery")
        
    except Exception as e:
        logger.error(f"❌ Error during job recovery: {e}")
        import traceback
        logger.error(f"   Traceback: {traceback.format_exc()}")
    
    return recovery_summary

