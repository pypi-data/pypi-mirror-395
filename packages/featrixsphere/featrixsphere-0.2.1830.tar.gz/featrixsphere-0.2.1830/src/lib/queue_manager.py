"""
Queue Management Module

Handles queue operations using Redis-based job storage.
"""
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from lib.job_manager import JobStatus, get_session_jobs, load_job, get_redis_client

logger = logging.getLogger(__name__)


def iterate_over_jobs_in_queue(job_type: str):
    """
    Iterate over all jobs of a given job_type.
    
    Note: This queries Redis for jobs by job_type, not file-based queues.
    """
    # Query Redis for all jobs with this job_type
    # We need to scan Redis keys - this is not efficient but works
    try:
        from lib.job_manager import get_redis_client
        client = get_redis_client()
        
        # Scan for all job keys
        cursor = 0
        while True:
            cursor, keys = client.scan(cursor, match="job:*", count=100)
            for key in keys:
                job_data = load_job(key.replace("job:", ""))
                if job_data and job_data.get("job_type") == job_type:
                    yield job_data
            if cursor == 0:
                break
    except Exception as e:
        logger.error(f"Failed to iterate over jobs of type {job_type}: {e}")
        return


def get_ready_jobs(job_type: str, order: str = "oldest_first"):
    """Get all ready jobs of a given job_type, sorted by creation time."""
    if order not in ['oldest_first', 'newest_first']:
        raise ValueError(f"Unsupported order: {order}")

    ready_jobs = []

    for job in iterate_over_jobs_in_queue(job_type):
        if job.get("status") == JobStatus.READY:
            ready_jobs.append(job)

    # Handle None values by treating them as epoch time (very old)
    epoch = datetime(1970, 1, 1, tzinfo=ZoneInfo("America/New_York"))
    reverse = order == 'newest_first'
    ready_jobs = sorted(ready_jobs, key=lambda x: x.get("created_at") or epoch, reverse=reverse)

    return ready_jobs


def load_session_jobs(session_doc: dict):
    """Load all jobs referenced in a session document from Redis.
    Also cleans up orphaned job IDs from the session set."""
    jobs = dict()
    session_id = session_doc.get("session_id")

    if session_id:
        # Get all jobs for this session from Redis
        redis_jobs = get_session_jobs(session_id)
        for job in redis_jobs:
            jobs[job.get("job_id")] = job
        
        # CLEANUP: Remove orphaned job IDs from the session set
        # These are job IDs that exist in the set but have no job data (expired or failed to save)
        try:
            redis_client = get_redis_client()
            session_key = f"session:{session_id}:jobs"
            all_job_ids_in_set = redis_client.smembers(session_key)
            
            orphaned_ids = []
            for job_id_bytes in all_job_ids_in_set:
                job_id = job_id_bytes.decode('utf-8') if isinstance(job_id_bytes, bytes) else job_id_bytes
                if job_id not in jobs:
                    # Job ID in set but no job data - orphaned
                    orphaned_ids.append(job_id)
            
            if orphaned_ids:
                logger.warning(f"🧹 Found {len(orphaned_ids)} orphaned job IDs in session {session_id} - removing from Redis set")
                for orphaned_id in orphaned_ids:
                    redis_client.srem(session_key, orphaned_id)
                    logger.debug(f"   Removed orphaned job_id: {orphaned_id}")
        except Exception as cleanup_err:
            logger.warning(f"⚠️  Failed to cleanup orphaned job IDs: {cleanup_err}")

    # Also check job_plan for any jobs not yet in Redis
    # Only include jobs that actually exist in Redis - skip stale job IDs
    for job_info in session_doc.get("job_plan", []):
        job_id = job_info.get("job_id")
        if job_id and job_id not in jobs:
            # Try to load from Redis
            job = load_job(job_id)
            if job:
                jobs[job_id] = job
            else:
                # Job not found in Redis - skip it entirely
                # This happens when:
                # 1. Job ID was assigned but job was never saved to Redis
                # 2. Job was deleted from Redis but job_id remains in job_plan
                # 3. Race condition where job_id added before job saved
                # Don't create placeholders - they just confuse clients
                logger.debug(f"⏭️  Skipping job_id {job_id} from job_plan - not found in Redis (likely stale or never created)")

    return jobs

