#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
"""
File-based cache for JSON encoder API queries.

Uses file locking (fcntl) for thread-safe and process-safe concurrent access.
Cache persists across server restarts and works across multiple workers.
"""
import fcntl
import json
import logging
import time
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class JsonEncoderCache:
    """
    Thread-safe and process-safe file-based cache for JSON encoder queries.
    
    Uses fcntl file locking to ensure safe concurrent access across multiple
    processes and threads. Cache persists across server restarts.
    """
    
    def __init__(self, cache_file: Path, ttl_seconds: int = 60):
        """
        Initialize the cache.
        
        Args:
            cache_file: Path to the JSON cache file
            ttl_seconds: Time-to-live for cache entries in seconds
        """
        self.cache_file = cache_file
        self.lock_file = cache_file.with_suffix('.json.lock')
        self.ttl_seconds = ttl_seconds
        
        # Ensure cache directory exists
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get a cached value by key.
        
        Args:
            key: Cache key (e.g., sorted comma-separated schema fields)
            
        Returns:
            Cached result dict if found and not expired, None otherwise
        """
        if not self.cache_file.exists():
            return None
        
        # Use file locking for safe concurrent access
        lock_file = open(self.lock_file, 'w')
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_SH)  # Shared lock for reading
        
        try:
            cache_data = json.loads(self.cache_file.read_text())
            cache_entry = cache_data.get(key)
            
            if cache_entry:
                cache_time = cache_entry.get('timestamp', 0)
                age = time.time() - cache_time
                if age < self.ttl_seconds:
                    logger.debug(f"✅ JSON encoder cache HIT for key '{key[:50]}...' (age: {age:.1f}s)")
                    return cache_entry.get('result')
                else:
                    logger.debug(f"🔄 JSON encoder cache EXPIRED for key '{key[:50]}...' (age: {age:.1f}s, TTL: {self.ttl_seconds}s)")
            
            return None
        except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
            logger.debug(f"Cache read error (non-critical): {e}")
            return None
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            lock_file.close()
    
    def set(self, key: str, value: Dict[str, Any]) -> None:
        """
        Set a cached value by key.
        
        Args:
            key: Cache key (e.g., sorted comma-separated schema fields)
            value: Result dict to cache
        """
        # Use file locking for safe concurrent access
        lock_file = open(self.lock_file, 'w')
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)  # Exclusive lock for writing
        
        try:
            # Load existing cache
            if self.cache_file.exists():
                try:
                    cache_data = json.loads(self.cache_file.read_text())
                except (json.JSONDecodeError, FileNotFoundError):
                    cache_data = {}
            else:
                cache_data = {}
            
            # Clean up expired entries
            current_time = time.time()
            expired_keys = []
            for k, entry in cache_data.items():
                if current_time - entry.get('timestamp', 0) >= self.ttl_seconds:
                    expired_keys.append(k)
            for k in expired_keys:
                del cache_data[k]
            
            # Add new entry
            cache_data[key] = {
                'result': value,
                'timestamp': current_time
            }
            
            # Write cache file
            self.cache_file.write_text(json.dumps(cache_data, indent=2))
            logger.debug(f"💾 Cached JSON encoder result for key '{key[:50]}...' (TTL: {self.ttl_seconds}s)")
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            lock_file.close()
    
    def clear(self) -> None:
        """
        Clear all cache entries.
        """
        # Use file locking for safe concurrent access
        lock_file = open(self.lock_file, 'w')
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)  # Exclusive lock for writing
        
        try:
            if self.cache_file.exists():
                self.cache_file.unlink()
            logger.info(f"🗑️  Cleared JSON encoder cache")
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            lock_file.close()

