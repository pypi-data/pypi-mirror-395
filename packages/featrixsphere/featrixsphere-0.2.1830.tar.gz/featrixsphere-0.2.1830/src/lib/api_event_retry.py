"""
API Event Retry System

Logs failed API calls and webhooks for retry with exponential backoff.
Events are stored in Redis and retried by a background process.
"""
import json
import logging
import time
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from enum import Enum
from zoneinfo import ZoneInfo

import requests

from lib.job_manager import get_redis_client

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of API events that can be retried."""
    TRAINING_PROGRESS = "training_progress"
    TRAINING_DATA = "training_data"
    WEBHOOK = "webhook"
    COMPUTE_NODE_ANNOUNCE = "compute_node_announce"
    JOB_COMPLETION = "job_completion"
    CUSTOM = "custom"


class APIEventRetry:
    """Manages retry queue for failed API calls."""
    
    REDIS_KEY_PREFIX = "api_event_retry:"
    MAX_RETRIES = 10
    MAX_AGE_DAYS = 7  # Delete events older than 7 days
    
    def __init__(self, redis_client=None):
        """Initialize the retry system."""
        self.redis = redis_client or get_redis_client()
    
    def _get_event_key(self, event_id: str) -> str:
        """Get Redis key for an event."""
        return f"{self.REDIS_KEY_PREFIX}{event_id}"
    
    def _get_index_key(self) -> str:
        """Get Redis key for the event index (sorted set by next_retry_time)."""
        return f"{self.REDIS_KEY_PREFIX}index"
    
    def log_failed_event(
        self,
        event_type: EventType,
        url: str,
        method: str = "POST",
        payload: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        timeout: int = 30,
        error: str = None,
        metadata: Dict[str, Any] = None,
        event_id: str = None
    ) -> str:
        """
        Log a failed API call for retry.
        
        Args:
            event_type: Type of event
            url: URL to call
            method: HTTP method (POST, GET, PUT, etc.)
            payload: Request payload (for POST/PUT)
            headers: Request headers
            timeout: Request timeout in seconds
            error: Error message from the failed attempt
            metadata: Additional metadata about the event
            event_id: Optional event ID (auto-generated if not provided)
            
        Returns:
            Event ID
        """
        import uuid
        
        if event_id is None:
            event_id = str(uuid.uuid4())
        
        event_data = {
            "event_id": event_id,
            "event_type": event_type.value,
            "url": url,
            "method": method.upper(),
            "payload": payload or {},
            "headers": headers or {},
            "timeout": timeout,
            "error": error,
            "metadata": metadata or {},
            "created_at": datetime.now(tz=ZoneInfo("America/New_York")).isoformat(),
            "retry_count": 0,
            "next_retry_time": datetime.now(tz=ZoneInfo("America/New_York")).isoformat(),
            "last_attempt": None,
            "last_error": error,
            "status": "pending"
        }
        
        try:
            # Store event data
            event_key = self._get_event_key(event_id)
            self.redis.setex(
                event_key,
                self.MAX_AGE_DAYS * 86400,  # TTL in seconds
                json.dumps(event_data)
            )
            
            # Add to index (sorted set by next_retry_time timestamp)
            index_key = self._get_index_key()
            next_retry_ts = datetime.now(tz=ZoneInfo("America/New_York")).timestamp()
            self.redis.zadd(index_key, {event_id: next_retry_ts})
            
            logger.info(f"📝 Logged failed API event for retry: {event_type.value} -> {url}")
            logger.info(f"   Event ID: {event_id[:8]}...")
            logger.info(f"   Error: {error[:200] if error else 'Unknown error'}")
            
            return event_id
            
        except Exception as e:
            logger.error(f"❌ Failed to log API event for retry: {e}")
            logger.error(f"   Traceback: {traceback.format_exc()}")
            return event_id
    
    def get_pending_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get events that are ready for retry.
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List of event data dictionaries
        """
        try:
            index_key = self._get_index_key()
            now_ts = datetime.now(tz=ZoneInfo("America/New_York")).timestamp()
            
            # Get events with next_retry_time <= now
            event_ids = self.redis.zrangebyscore(
                index_key,
                "-inf",  # Min score
                now_ts,  # Max score (current time)
                start=0,
                num=limit
            )
            
            events = []
            for event_id_bytes in event_ids:
                event_id = event_id_bytes.decode('utf-8') if isinstance(event_id_bytes, bytes) else event_id_bytes
                event_key = self._get_event_key(event_id)
                event_data_json = self.redis.get(event_key)
                
                if event_data_json:
                    try:
                        event_data = json.loads(event_data_json)
                        events.append(event_data)
                    except json.JSONDecodeError:
                        logger.warning(f"⚠️  Failed to parse event data for {event_id}")
                        # Remove corrupted event
                        self.redis.delete(event_key)
                        self.redis.zrem(index_key, event_id)
            
            return events
            
        except Exception as e:
            logger.error(f"❌ Failed to get pending events: {e}")
            logger.error(f"   Traceback: {traceback.format_exc()}")
            return []
    
    def _calculate_next_retry_time(self, retry_count: int) -> datetime:
        """
        Calculate next retry time using exponential backoff.
        
        Args:
            retry_count: Number of retries so far
            
        Returns:
            Next retry datetime
        """
        # Exponential backoff: 1s, 2s, 4s, 8s, 16s, 32s, 60s, 120s, 300s, 600s
        delays = [1, 2, 4, 8, 16, 32, 60, 120, 300, 600]
        if retry_count < len(delays):
            delay_seconds = delays[retry_count]
        else:
            delay_seconds = 600  # Max 10 minutes
        
        return datetime.now(tz=ZoneInfo("America/New_York")) + timedelta(seconds=delay_seconds)
    
    def retry_event(self, event_data: Dict[str, Any]) -> bool:
        """
        Retry a single API event.
        
        Args:
            event_data: Event data dictionary
            
        Returns:
            True if successful, False otherwise
        """
        event_id = event_data["event_id"]
        url = event_data["url"]
        method = event_data["method"]
        payload = event_data.get("payload", {})
        headers = event_data.get("headers", {})
        timeout = event_data.get("timeout", 30)
        retry_count = event_data.get("retry_count", 0)
        
        logger.info(f"🔄 Retrying API event {event_id[:8]}... (attempt {retry_count + 1}/{self.MAX_RETRIES})")
        logger.info(f"   URL: {url}")
        logger.info(f"   Method: {method}")
        
        try:
            # Make the API call
            if method == "POST":
                response = requests.post(url, json=payload, headers=headers, timeout=timeout)
            elif method == "GET":
                response = requests.get(url, params=payload, headers=headers, timeout=timeout)
            elif method == "PUT":
                response = requests.put(url, json=payload, headers=headers, timeout=timeout)
            elif method == "PATCH":
                response = requests.patch(url, json=payload, headers=headers, timeout=timeout)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=timeout)
            else:
                logger.error(f"❌ Unsupported HTTP method: {method}")
                return False
            
            response.raise_for_status()
            
            # Success! Remove from retry queue
            logger.info(f"✅ API event {event_id[:8]} succeeded on retry {retry_count + 1}")
            self._mark_event_success(event_id)
            return True
            
        except requests.exceptions.Timeout as e:
            error_msg = f"Timeout after {timeout}s"
            logger.warning(f"⚠️  API event {event_id[:8]} timeout: {error_msg}")
            self._mark_event_retry(event_id, error_msg, retry_count)
            return False
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if hasattr(e, 'response') and e.response else None
            
            # Don't retry 4xx errors (client errors) except 408, 429
            if status_code and 400 <= status_code < 500 and status_code not in [408, 429]:
                logger.warning(f"⚠️  API event {event_id[:8]} failed with client error {status_code}: {e}")
                logger.warning(f"   Not retrying client errors (except 408, 429)")
                self._mark_event_failed(event_id, f"Client error {status_code}: {str(e)}")
                return False
            
            error_msg = f"HTTP {status_code}: {str(e)}"
            logger.warning(f"⚠️  API event {event_id[:8]} HTTP error: {error_msg}")
            self._mark_event_retry(event_id, error_msg, retry_count)
            return False
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {str(e)}"
            logger.warning(f"⚠️  API event {event_id[:8]} request error: {error_msg}")
            self._mark_event_retry(event_id, error_msg, retry_count)
            return False
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"❌ API event {event_id[:8]} unexpected error: {error_msg}")
            logger.error(f"   Traceback: {traceback.format_exc()}")
            self._mark_event_retry(event_id, error_msg, retry_count)
            return False
    
    def _mark_event_success(self, event_id: str):
        """Mark an event as successfully completed."""
        try:
            event_key = self._get_event_key(event_id)
            event_data_json = self.redis.get(event_key)
            
            if event_data_json:
                event_data = json.loads(event_data_json)
                event_data["status"] = "success"
                event_data["last_attempt"] = datetime.now(tz=ZoneInfo("America/New_York")).isoformat()
                
                self.redis.setex(
                    event_key,
                    self.MAX_AGE_DAYS * 86400,
                    json.dumps(event_data)
                )
            
            # Remove from index
            index_key = self._get_index_key()
            self.redis.zrem(index_key, event_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to mark event as success: {e}")
    
    def _mark_event_retry(self, event_id: str, error: str, retry_count: int):
        """Mark an event for retry with updated retry count."""
        try:
            event_key = self._get_event_key(event_id)
            event_data_json = self.redis.get(event_key)
            
            if not event_data_json:
                logger.warning(f"⚠️  Event {event_id} not found in Redis")
                return
            
            event_data = json.loads(event_data_json)
            new_retry_count = retry_count + 1
            
            if new_retry_count >= self.MAX_RETRIES:
                # Max retries reached - mark as failed
                logger.error(f"❌ API event {event_id[:8]} exceeded max retries ({self.MAX_RETRIES})")
                self._mark_event_failed(event_id, f"Max retries exceeded: {error}")
                return
            
            event_data["retry_count"] = new_retry_count
            event_data["last_attempt"] = datetime.now(tz=ZoneInfo("America/New_York")).isoformat()
            event_data["last_error"] = error
            event_data["status"] = "pending"
            event_data["next_retry_time"] = self._calculate_next_retry_time(new_retry_count).isoformat()
            
            # Update event data
            self.redis.setex(
                event_key,
                self.MAX_AGE_DAYS * 86400,
                json.dumps(event_data)
            )
            
            # Update index with new retry time
            index_key = self._get_index_key()
            next_retry_ts = self._calculate_next_retry_time(new_retry_count).timestamp()
            self.redis.zadd(index_key, {event_id: next_retry_ts})
            
            logger.info(f"   Scheduled retry {new_retry_count + 1} for {event_data['next_retry_time']}")
            
        except Exception as e:
            logger.error(f"❌ Failed to mark event for retry: {e}")
            logger.error(f"   Traceback: {traceback.format_exc()}")
    
    def _mark_event_failed(self, event_id: str, error: str):
        """Mark an event as permanently failed."""
        try:
            event_key = self._get_event_key(event_id)
            event_data_json = self.redis.get(event_key)
            
            if event_data_json:
                event_data = json.loads(event_data_json)
                event_data["status"] = "failed"
                event_data["last_attempt"] = datetime.now(tz=ZoneInfo("America/New_York")).isoformat()
                event_data["last_error"] = error
                
                self.redis.setex(
                    event_key,
                    self.MAX_AGE_DAYS * 86400,
                    json.dumps(event_data)
                )
            
            # Remove from index
            index_key = self._get_index_key()
            self.redis.zrem(index_key, event_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to mark event as failed: {e}")
    
    def process_retry_queue(self, max_events: int = 50) -> Dict[str, int]:
        """
        Process pending events in the retry queue.
        
        Args:
            max_events: Maximum number of events to process in this batch
            
        Returns:
            Dictionary with stats: {"processed": N, "succeeded": M, "failed": K, "retried": L}
        """
        stats = {
            "processed": 0,
            "succeeded": 0,
            "failed": 0,
            "retried": 0
        }
        
        events = self.get_pending_events(limit=max_events)
        
        if not events:
            return stats
        
        logger.info(f"🔄 Processing {len(events)} pending API events...")
        
        for event_data in events:
            stats["processed"] += 1
            
            if self.retry_event(event_data):
                stats["succeeded"] += 1
            else:
                stats["retried"] += 1
                
                # Check if it exceeded max retries
                if event_data.get("retry_count", 0) + 1 >= self.MAX_RETRIES:
                    stats["failed"] += 1
        
        if stats["processed"] > 0:
            logger.info(f"✅ Processed {stats['processed']} events: {stats['succeeded']} succeeded, {stats['retried']} retried, {stats['failed']} failed")
        
        return stats
    
    def cleanup_old_events(self):
        """Remove events older than MAX_AGE_DAYS."""
        try:
            index_key = self._get_index_key()
            cutoff_ts = (datetime.now(tz=ZoneInfo("America/New_York")) - timedelta(days=self.MAX_AGE_DAYS)).timestamp()
            
            # Get old event IDs
            old_event_ids = self.redis.zrangebyscore(index_key, "-inf", cutoff_ts)
            
            if old_event_ids:
                logger.info(f"🧹 Cleaning up {len(old_event_ids)} old API events...")
                
                for event_id_bytes in old_event_ids:
                    event_id = event_id_bytes.decode('utf-8') if isinstance(event_id_bytes, bytes) else event_id_bytes
                    event_key = self._get_event_key(event_id)
                    
                    # Delete event data
                    self.redis.delete(event_key)
                    # Remove from index
                    self.redis.zrem(index_key, event_id)
                
                logger.info(f"✅ Cleaned up {len(old_event_ids)} old events")
            
        except Exception as e:
            logger.error(f"❌ Failed to cleanup old events: {e}")


# Global instance
_retry_manager = None

def get_retry_manager() -> APIEventRetry:
    """Get the global retry manager instance."""
    global _retry_manager
    if _retry_manager is None:
        _retry_manager = APIEventRetry()
    return _retry_manager

