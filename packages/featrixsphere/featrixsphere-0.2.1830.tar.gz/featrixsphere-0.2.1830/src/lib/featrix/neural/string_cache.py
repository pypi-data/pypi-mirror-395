#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import base64
import hashlib
import io
import logging
import math
import os
import sqlite3
import sys
import traceback
import functools
from typing import List, Tuple

import pandas as pd
import numpy as np
import torch
import torch.nn as nn

# Import logging configuration FIRST to ensure timestamps
from featrix.neural.logging_config import configure_logging
configure_logging()

from featrix.neural.device import device
from featrix.neural.featrix_token import set_not_present
from featrix.neural.featrix_token import Token
from featrix.neural.featrix_token import TokenStatus
from featrix.neural.model_config import ColumnType
from featrix.neural.model_config import SimpleMLPConfig
from featrix.neural.model_config import StringEncoderConfig
from featrix.neural.simple_mlp import SimpleMLP

logger = logging.getLogger(__name__)

from functools import lru_cache

def _log_gpu_memory_string_cache(context: str = ""):
    """Quick GPU memory logging for tracing memory usage in string_cache."""
    try:
        import torch
        if not torch.cuda.is_available():
            return
        allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
        reserved = torch.cuda.memory_reserved() / (1024**3)  # GB
        max_allocated = torch.cuda.max_memory_allocated() / (1024**3)  # GB
        logger.info(f"📊 GPU MEMORY [string_cache: {context}]: Allocated={allocated:.3f} GB, Reserved={reserved:.3f} GB, Peak={max_allocated:.3f} GB")
    except Exception as e:
        logger.debug(f"Could not log GPU memory: {e}")

def _log_gpu_memory_string_cache(context: str = "", log_level=logging.INFO):
    """Quick GPU memory logging for tracing memory usage in string_cache."""
    try:
        import torch
        if not torch.cuda.is_available():
            return
        allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
        reserved = torch.cuda.memory_reserved() / (1024**3)  # GB
        max_allocated = torch.cuda.max_memory_allocated() / (1024**3)  # GB
        logger.log(log_level, f"📊 GPU MEMORY [string_cache: {context}]: Allocated={allocated:.3f} GB, Reserved={reserved:.3f} GB, Peak={max_allocated:.3f} GB")
    except Exception as e:
        logger.debug(f"Could not log GPU memory: {e}")


# Set this to True for debugging the cache.
CACHE_MISS_LOGGING_ENABLED = False


def cache_logging(func):
    """Decorator to log cache hits and misses.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        if CACHE_MISS_LOGGING_ENABLED:
            # Check if the result is in cache
            cache_info = func.cache_info()
            result = func(*args, **kwargs)
            
            # Compare cache info before and after to detect hit/miss
            new_cache_info = func.cache_info()
            
            if new_cache_info.misses > cache_info.misses:
                logger.info(f"String cache miss for args: {args}, kwargs: {kwargs}")
        else:
            result = func(*args, **kwargs)
        
        return result
    
    return wrapper

import os

try:
    import lancedb
    LANCEDB_AVAILABLE = True
except ImportError:
    # CRITICAL: LanceDB is REQUIRED for performance - crash with VERY prominent error
    error_msg = """
    
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║              🚨🚨🚨  CRITICAL ERROR: LANCEDB MISSING  🚨🚨🚨                    ║
    ║                                                                              ║
    ║  ⚠️  LanceDB is REQUIRED for fast string similarity search!                  ║
    ║                                                                              ║
    ║  ❌ Without LanceDB, string decoding will be EXTREMELY SLOW                  ║
    ║     (SQLite brute force search - 100-1000x slower!)                          ║
    ║                                                                              ║
    ║  ✅ INSTALL IT NOW:                                                           ║
    ║                                                                              ║
    ║      pip install lancedb>=0.21.0                                             ║
    ║                                                                              ║
    ║  Or install all requirements:                                               ║
    ║                                                                              ║
    ║      pip install -r requirements.txt                                        ║
    ║                                                                              ║
    ║  ⚡ This is a HARD REQUIREMENT - system will NOT run efficiently without it! ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    
    """
    # Print to stderr with emphasis (will show in console)
    print(error_msg, file=sys.stderr)
    # Also log as CRITICAL (highest level) - will show in logs
    logger.critical(error_msg)
    logger.critical("=" * 80)
    logger.critical("LanceDB is REQUIRED but not installed!")
    logger.critical("Install with: pip install lancedb>=0.21.0")
    logger.critical("Or: pip install -r requirements.txt")
    logger.critical("=" * 80)
    # Crash immediately - this is a hard requirement
    raise ImportError(
        "LanceDB is REQUIRED but not installed. "
        "Install with: pip install lancedb>=0.21.0 "
        "or: pip install -r requirements.txt"
    )

class StringCache:
    """ 
    We hold this just during training. 
    We do not save it off for now. 
    But we should... if we saved it at upload processing time, for example.. though that might be too much complexity.
    """
    def __init__(self, initial_values=[], debugName="no_debug_name_string_cache", sentence_model=None, string_cache_filename=None):
        assert debugName is not None

        # CRITICAL: Workers should NEVER compute embeddings - they only read from cache
        # All encoding is done via string server client (no local sentence transformer)
        # sentence_model parameter is ignored - kept for backward compatibility
        if sentence_model is not None:
            logger.warning(f"⚠️  StringCache: sentence_model parameter is ignored - using string server client instead")
            
        # sentence_model is no longer used - all encoding via string server client
        # Removed all sentence_model device checking code
        self.sentence_model = None  # No longer used - kept for backward compatibility only
        # CRITICAL: Resolve to absolute path so workers can find it regardless of working directory
        raw_filename = string_cache_filename or "strings.sqlite3"
        if not os.path.isabs(raw_filename):
            # Relative path - resolve to absolute based on current working directory
            self.filename = os.path.abspath(raw_filename)
        else:
            # Already absolute
            self.filename = raw_filename
        self.cache_miss_count = 0  # Track individual cache misses for GPU efficiency monitoring
        
        # RAM cache fallback: in-memory dict if SQLite is unavailable
        # CRITICAL: This should ONLY be used if SQLite fails - if you see this being used, SQLite is broken!
        # Limited to 8000 entries (matching @lru_cache limit) to match method-level cache size
        self._ram_cache = {}  # {string_value: torch.Tensor}
        self._use_ram_cache_only = False  # Set to True if SQLite fails
        self._ram_cache_max_entries = 8192  # Match @lru_cache limit (2**13 = 8192)
        self._ram_cache_warning_logged = False  # Track if we've warned about RAM cache usage
        
        # LanceDB for nearest neighbor search (lazy initialization)
        self._lancedb_table = None
        self._lancedb_initialized = False
        self._lancedb_path = None
        if LANCEDB_AVAILABLE:
            # LanceDB path: same directory as SQLite cache, with .lancedb suffix
            cache_dir = os.path.dirname(os.path.abspath(self.filename)) or os.getcwd()
            cache_basename = os.path.basename(self.filename).replace('.sqlite3', '')
            self._lancedb_path = os.path.join(cache_dir, f"{cache_basename}.lancedb")
        
        # XXX: handle if the file exists already??

        logger.info(f"🔍 STRINGCACHE DEBUG: string_cache_filename parameter = {string_cache_filename}")
        logger.info(f"🔍 STRINGCACHE DEBUG: resolved filename = {self.filename}")
        logger.info(f"🔍 STRINGCACHE DEBUG: current working directory = {os.getcwd()}")
        logger.info(f"🔍 STRINGCACHE DEBUG: resolved path = {os.path.abspath(self.filename)}")

        load_existing = os.path.exists(self.filename) and os.path.getsize(self.filename) > 0
        logger.info(f"StringCache: load_existing = {load_existing}; filename = {self.filename}")
        
        # CRITICAL: Workers should open cache in read-only mode to avoid:
        # 1. Loading sentence model to compute missing embeddings
        # 2. Lock contention on SQLite file
        # 3. Memory waste from duplicate caches
        is_worker = os.environ.get('PYTORCH_DATALOADER_WORKER') == '1'
        
        if is_worker and load_existing:
            # Worker process - open read-only
            # Worker process - open cache read-only (no logging to reduce spam)
            logger.info(f"   Absolute path: {os.path.abspath(self.filename)}")
            logger.info(f"   File exists: {os.path.exists(self.filename)}")
            try:
                self.conn = sqlite3.connect(f"file:{self.filename}?mode=ro", uri=True)
                self.is_readonly = True
                # No memory limits - let SQLite use what it needs
                # self.conn.execute("PRAGMA cache_size = -262144")  # 1GB limit
                # self.conn.execute("PRAGMA mmap_size = 268435456")  # 256MB limit
                # self.conn.commit()
                # Verify we can read from the cache
                test_cursor = self.conn.cursor()
                test_cursor.execute("SELECT COUNT(*) FROM cache")
                cache_count = test_cursor.fetchone()[0]
                logger.info(f"✅ Worker: Successfully opened cache with {cache_count:,} entries")
            except Exception as e:
                error_str = str(e).lower()
                is_corruption = (
                    "database disk image is malformed" in error_str or
                    "file is encrypted or is not a database" in error_str or
                    "not a database" in error_str or
                    "corrupt" in error_str or
                    "integrity" in error_str
                )
                
                if is_corruption:
                    logger.critical(f"🚨 WORKER: SQLite Database Corruption Detected: {self.filename}")
                    logger.critical(f"   Error: {e}")
                    
                    # Send Slack alert for corruption (don't throttle - this is critical)
                    try:
                        from slack import send_slack_message
                        import socket
                        hostname = socket.gethostname()
                        slack_msg = (
                            f"🚨 **SQLite Database Corruption (Worker Process)**\n"
                            f"Host: {hostname}\n"
                            f"File: {self.filename}\n"
                            f"Error: {str(e)}\n"
                            f"Debug Name: {debugName}\n"
                            f"\n"
                            f"Worker process cannot read corrupted SQLite file.\n"
                            f"**Action Required:** Check disk health and restore from backup."
                        )
                        send_slack_message(slack_msg, throttle=False, skip_hostname_prefix=True)
                        logger.info("✅ Slack alert sent for SQLite corruption (worker)")
                    except Exception as slack_err:
                        logger.warning(f"⚠️  Failed to send Slack alert for corruption: {slack_err}")
                
                logger.error(f"❌ Worker: Failed to open cache file {self.filename}: {e}")
                logger.error(f"   Absolute path: {os.path.abspath(self.filename)}")
                logger.error(f"   File exists: {os.path.exists(self.filename)}")
                logger.error(f"   Current working directory: {os.getcwd()}")
                raise
        else:
            # Main process - try to open read-write, fall back to RAM cache if it fails
            try:
                self.conn = sqlite3.connect(self.filename)
                self.is_readonly = False
                self.cursor = self.conn.cursor()
            except Exception as e:
                error_str = str(e).lower()
                is_corruption = (
                    "database disk image is malformed" in error_str or
                    "file is encrypted or is not a database" in error_str or
                    "not a database" in error_str or
                    "corrupt" in error_str or
                    "integrity" in error_str
                )
                
                if is_corruption:
                    logger.critical(f"🚨 SQLITE DATABASE CORRUPTION DETECTED: {self.filename}")
                    logger.critical(f"   Error: {e}")
                    logger.critical(f"   ⚠️  FALLING BACK TO IN-MEMORY RAM CACHE (NOT PERSISTENT, LIMITED TO 8192 ENTRIES)")
                    logger.critical(f"   The SQLite file appears to be corrupted - this is a CRITICAL issue!")
                    
                    # Send Slack alert for corruption (don't throttle - this is critical)
                    try:
                        from slack import send_slack_message
                        import socket
                        hostname = socket.gethostname()
                        slack_msg = (
                            f"🚨 **SQLite Database Corruption Detected**\n"
                            f"Host: {hostname}\n"
                            f"File: {self.filename}\n"
                            f"Error: {str(e)}\n"
                            f"Debug Name: {debugName}\n"
                            f"\n"
                            f"⚠️  System is falling back to in-memory RAM cache (8192 entry limit).\n"
                            f"This is NOT persistent and will lose data on restart.\n"
                            f"\n"
                            f"**Action Required:**\n"
                            f"1. Check disk health and space\n"
                            f"2. Verify file permissions\n"
                            f"3. Consider restoring from backup\n"
                            f"4. May need to rebuild string cache"
                        )
                        send_slack_message(slack_msg, throttle=False, skip_hostname_prefix=True)
                        logger.info("✅ Slack alert sent for SQLite corruption")
                    except Exception as slack_err:
                        logger.warning(f"⚠️  Failed to send Slack alert for corruption: {slack_err}")
                else:
                    logger.error(f"❌ CRITICAL: Failed to open SQLite cache {self.filename}: {e}")
                    logger.error(f"   ⚠️  FALLING BACK TO IN-MEMORY RAM CACHE (NOT PERSISTENT, LIMITED TO 8192 ENTRIES)")
                    logger.error(f"   This is a fallback mode - SQLite should be working! Check disk space, permissions, etc.")
                    
                    # Send Slack alert for non-corruption errors too (but throttle these)
                    try:
                        from slack import send_slack_message
                        import socket
                        hostname = socket.gethostname()
                        slack_msg = (
                            f"⚠️  **SQLite Cache Open Failed**\n"
                            f"Host: {hostname}\n"
                            f"File: {self.filename}\n"
                            f"Error: {str(e)}\n"
                            f"Debug Name: {debugName}\n"
                            f"\n"
                            f"Falling back to in-memory RAM cache (8192 entry limit).\n"
                            f"Check disk space, permissions, file locks, etc."
                        )
                        send_slack_message(slack_msg, throttle=True, skip_hostname_prefix=True)
                        logger.info("✅ Slack alert sent for SQLite open failure")
                    except Exception as slack_err:
                        logger.warning(f"⚠️  Failed to send Slack alert: {slack_err}")
                
                self._use_ram_cache_only = True
                self.conn = None
                self.cursor = None
                self.is_readonly = False
        
        if not self._use_ram_cache_only:
            self.cursor = self.conn.cursor()
            
            # Check if table exists - if not, we need to create it (even if file exists)
            table_exists = False
            try:
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cache'")
                table_exists = self.cursor.fetchone() is not None
            except Exception:
                # If we can't check, assume table doesn't exist
                table_exists = False
            
            # If table doesn't exist, create it (even if file exists)
            if not table_exists:
                logger.info(f"StringCache: Table 'cache' not found, creating it...")
                self.cursor.execute("CREATE TABLE IF NOT EXISTS cache (string_value TEXT, embeddings_blob BLOB)")
                self.conn.commit()
                load_existing = False  # Treat as new cache since table was just created
                logger.info("StringCache: ✅ Created cache table")
            
            # Check database integrity (quick check - catches corruption early)
            try:
                integrity_result = self.conn.execute("PRAGMA quick_check").fetchone()
                if integrity_result and integrity_result[0] != "ok":
                    # Database integrity check failed - corruption detected!
                    integrity_msg = integrity_result[0]
                    logger.critical(f"🚨 SQLite Integrity Check FAILED: {self.filename}")
                    logger.critical(f"   Integrity result: {integrity_msg}")
                    
                    # Send Slack alert for corruption
                    try:
                        from slack import send_slack_message
                        import socket
                        hostname = socket.gethostname()
                        slack_msg = (
                            f"🚨 **SQLite Database Integrity Check Failed**\n"
                            f"Host: {hostname}\n"
                            f"File: {self.filename}\n"
                            f"Integrity Result: {integrity_msg}\n"
                            f"Debug Name: {debugName}\n"
                            f"\n"
                            f"Database corruption detected during integrity check.\n"
                            f"**Action Required:** Check disk health, restore from backup, or rebuild cache."
                        )
                        send_slack_message(slack_msg, throttle=False, skip_hostname_prefix=True)
                        logger.info("✅ Slack alert sent for SQLite integrity failure")
                    except Exception as slack_err:
                        logger.warning(f"⚠️  Failed to send Slack alert: {slack_err}")
                    
                    # Close corrupted connection and fall back to RAM cache
                    self.conn.close()
                    logger.critical(f"   ⚠️  FALLING BACK TO IN-MEMORY RAM CACHE (NOT PERSISTENT, LIMITED TO 8192 ENTRIES)")
                    self._use_ram_cache_only = True
                    self.conn = None
                    self.cursor = None
                else:
                    logger.debug(f"StringCache: Integrity check passed for {self.filename}")
            except Exception as integrity_err:
                # Integrity check itself failed - could be corruption or other issue
                logger.warning(f"⚠️  Integrity check failed with error: {integrity_err}")
                logger.warning(f"   Continuing anyway, but database may be corrupted")
            
            if not self._use_ram_cache_only:
                # No memory limits - let SQLite use what it needs for performance
                # self.conn.execute("PRAGMA cache_size = -262144")  # Removed limit
                self.conn.execute("PRAGMA temp_store = MEMORY")  # Use memory for temp tables (faster)
                # self.conn.execute("PRAGMA mmap_size = 268435456")  # Removed limit
                self.conn.commit()
                logger.debug(f"StringCache: SQLite memory limits removed for better performance")
        
        # CRITICAL: Initialize string server client early for non-readonly caches
        # This ensures it's available when needed and fails fast if it can't be initialized
        self._string_server_client = None
        if not getattr(self, 'is_readonly', False) and not self._use_ram_cache_only:
            logger.info("🔌 Initializing string server client for cache...")
            try:
                from featrix.neural.string_codec import _init_string_server_client
                
                self._string_server_client = _init_string_server_client()
                if self._string_server_client is None:
                    error_msg = (
                        "String server client initialization failed.\n"
                        "Check that:\n"
                        "  1. featrix-string-server-client package is installed\n"
                        "  2. String server is running and accessible (taco.local:9000 or sphere-api.featrix.com)\n"
                        "  3. Network connectivity to string server"
                    )
                    logger.error(f"❌ {error_msg}")
                    raise RuntimeError(error_msg)
                
                # Test the client with a simple encoding to verify it works
                try:
                    test_embedding = self._string_server_client.encode("test")
                    if test_embedding is None or len(test_embedding) == 0:
                        raise RuntimeError("String server returned empty embedding")
                    server_url = self._string_server_client.base_url
                    logger.info(f"✅ String server client initialized and verified: {server_url}")
                except Exception as test_err:
                    error_msg = (
                        f"String server client test failed: {test_err}\n"
                        f"Server URL: {self._string_server_client.base_url}\n"
                        "The string server may not be responding correctly."
                    )
                    logger.error(f"❌ {error_msg}")
                    raise RuntimeError(error_msg) from test_err
                    
            except ImportError:
                error_msg = (
                    "featrix-string-server-client package not installed.\n"
                    "Install it with: pip install featrix-string-server-client\n"
                    "String cache requires string server for encoding operations."
                )
                logger.error(f"❌ {error_msg}")
                raise RuntimeError(error_msg)
            except Exception as e:
                if isinstance(e, RuntimeError):
                    raise  # Re-raise our custom RuntimeErrors
                error_msg = (
                    f"Failed to initialize string server client: {e}\n"
                    "String cache requires string server for encoding operations."
                )
                logger.error(f"❌ {error_msg}")
                raise RuntimeError(error_msg) from e

        if not load_existing:
            self.conn.execute("CREATE TABLE IF NOT EXISTS cache (string_value TEXT, embeddings_blob BLOB)")            
            self.conn.commit()
            logger.info("StringCache: >>> running warm-up encoding")
            try:
                import sys
                sys.stdout.flush()
                sys.stderr.flush()
                logger.info("StringCache: >>> calling run_batch for warm-up...")
                # Use a non-empty placeholder - string server rejects empty strings
                self.run_batch(initial_values=["<UNKNOWN>"])
                logger.info("StringCache: >>> run_batch completed successfully")
                self.conn.commit()
                logger.info("StringCache: >>> saved.")
            except Exception as e:
                logger.error(f"StringCache: ❌ WARM-UP FAILED: {type(e).__name__}: {e}")
                import traceback
                logger.error(f"StringCache: Traceback:\n{traceback.format_exc()}")
                raise
        else:
            # Log existing cache statistics
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM cache")
                existing_count = cursor.fetchone()[0]
                logger.info(f"StringCache: ✅ Loaded existing cache with {existing_count:,} embeddings")
                
                # Log cache file size
                if os.path.exists(self.filename):
                    file_size = os.path.getsize(self.filename)
                    logger.info(f"StringCache: 📦 Cache file size: {file_size / 1024:.1f} KB ({file_size / (1024*1024):.2f} MB)")
                    logger.info(f"StringCache: 📁 Cache file path: {os.path.abspath(self.filename)}")
                
                # Check if we have a sample of the initial values already cached
                sample_values = initial_values[:10] if len(initial_values) > 0 else []
                cached_sample = 0
                for val in sample_values:
                    cursor.execute("SELECT COUNT(*) FROM cache WHERE string_value = ?", (str(val).strip(),))
                    if cursor.fetchone()[0] > 0:
                        cached_sample += 1
                
                if len(sample_values) > 0:
                    cache_hit_pct = (cached_sample / len(sample_values)) * 100
                    logger.info(f"StringCache: 📊 Cache hit rate on sample (first 10 values): {cached_sample}/{len(sample_values)} ({cache_hit_pct:.1f}%)")
                    logger.info(f"StringCache:    (This is a sample check - full cache has {existing_count:,} embeddings)")
                    
            except Exception as e:
                logger.warning(f"StringCache: Warning - could not read cache stats: {e}")

        logger.info(f"StringCache: >>>> initial_values = {len(initial_values)} values")
        # traceback.print_stack()

        # Only add initial values that aren't already in cache
        if not self._use_ram_cache_only:
            logger.info(f"StringCache: Adding {len(initial_values)} initial values to cache...")
            self.run_batch(initial_values=initial_values)
            self.conn.commit()
            
            # Log final cache size
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM cache")
                final_count = cursor.fetchone()[0]
                logger.info(f"StringCache: 📦 Final cache size: {final_count:,} embeddings")
                if os.path.exists(self.filename):
                    file_size = os.path.getsize(self.filename)
                    logger.info(f"StringCache: 📁 Cache file size: {file_size / 1024:.1f} KB ({file_size / (1024*1024):.2f} MB)")
                    logger.info(f"StringCache: 📁 Cache file path: {os.path.abspath(self.filename)}")
            except Exception as e:
                logger.warning(f"StringCache: Could not get final cache size: {e}")

        # warm up the cache
        logger.info(f"Warming up the in-memory string cache for {len(initial_values)} initial_values.")
        for _initial_value in initial_values:

            # If the value is NaN, skip it.
            if _initial_value != _initial_value:
                continue

            try:
                self.get_embedding_from_cache(_initial_value)
            except Exception:
                logging.debug(f"Error warming up cache for value {_initial_value}")
        logger.info("Finished warming up string cache...")
        

        logger.info(f"Done committing {debugName}!")
        
        # Populate shared memory cache for workers (if not readonly)
        if not getattr(self, 'is_readonly', False):
            try:
                from featrix.neural.string_codec import _populate_shared_memory_cache
                _populate_shared_memory_cache(self)
            except Exception as e:
                logger.debug(f"Could not populate shared memory cache: {e}")
        #conn.close()
    
    def _ensure_lancedb_index(self):
        """
        Ensure LanceDB index exists for nearest neighbor search.
        Lazy initialization - only builds index when needed.
        """
        if not LANCEDB_AVAILABLE:
            return False
        
        if self._lancedb_initialized:
            return True
        
        try:
            # Connect to LanceDB
            db = lancedb.connect(self._lancedb_path)
            table_name = "string_embeddings"
            
            # Check if table exists
            try:
                self._lancedb_table = db.open_table(table_name)
                logger.debug(f"✅ Loaded existing LanceDB index for string cache: {self._lancedb_path}")
                self._lancedb_initialized = True
                return True
            except Exception:
                # Table doesn't exist, need to build it
                pass
            
            # Build LanceDB index from SQLite cache
            logger.info(f"🔨 Building LanceDB index for string cache from SQLite...")
            
            # Load all embeddings from SQLite
            cursor = self.conn.cursor()
            cursor.execute("SELECT string_value, embeddings_blob FROM cache")
            rows = cursor.fetchall()
            
            if len(rows) == 0:
                logger.warning("No embeddings in SQLite cache to index")
                return False
            
            # Convert to list of dicts for LanceDB
            records = []
            for string_value, embedding_blob in rows:
                embedding = np.frombuffer(embedding_blob, dtype=np.float32)
                records.append({
                    'string_value': string_value,
                    'vector': embedding.tolist()
                })
            
            # Create LanceDB table
            import pyarrow as pa
            schema = pa.schema([
                pa.field('string_value', pa.string()),
                pa.field('vector', pa.list_(pa.float32(), len(records[0]['vector']) if records else 384))
            ])
            
            self._lancedb_table = db.create_table(table_name, records, schema=schema, mode='overwrite')
            logger.info(f"✅ Built LanceDB index with {len(records)} embeddings: {self._lancedb_path}")
            self._lancedb_initialized = True
            return True
            
        except Exception as e:
            logger.warning(f"Failed to build LanceDB index for string cache: {e}")
            return False
    
    def find_nearest_neighbors(self, query_embedding: np.ndarray, k: int = 3) -> List[Tuple[str, float]]:
        """
        Find k nearest neighbors in the string cache using LanceDB.
        
        Args:
            query_embedding: Query embedding vector (numpy array, should be 384 dims for BERT)
            k: Number of neighbors to return (default 3)
            
        Returns:
            List of (string_value, distance) tuples, sorted by distance (closest first)
        """
        if not self._ensure_lancedb_index():
            # Fallback to SQLite brute force search if LanceDB unavailable
            return self._find_nearest_neighbors_sqlite(query_embedding, k)
        
        try:
            # Ensure query is numpy array and correct shape
            if isinstance(query_embedding, torch.Tensor):
                query_embedding = query_embedding.cpu().numpy()
            query_embedding = np.array(query_embedding, dtype=np.float32).flatten()
            
            # Search LanceDB
            results = (
                self._lancedb_table.search(query_embedding.tolist())
                .limit(k)
                .to_pandas()
            )
            
            # Convert to list of (string_value, distance) tuples
            neighbors = []
            for _, row in results.iterrows():
                string_value = row['string_value']
                distance = row.get('_distance', float('inf'))
                neighbors.append((string_value, float(distance)))
            
            return neighbors
            
        except Exception as e:
            logger.warning(f"LanceDB search failed, falling back to SQLite: {e}")
            return self._find_nearest_neighbors_sqlite(query_embedding, k)
    
    def _find_nearest_neighbors_sqlite(self, query_embedding: np.ndarray, k: int = 3) -> List[Tuple[str, float]]:
        """
        Fallback: Find nearest neighbors using SQLite (brute force).
        Slower but works without LanceDB.
        """
        # Ensure query is numpy array
        if isinstance(query_embedding, torch.Tensor):
            query_embedding = query_embedding.cpu().numpy()
        query_embedding = np.array(query_embedding, dtype=np.float32).flatten()
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT string_value, embeddings_blob FROM cache")
        rows = cursor.fetchall()
        
        distances = []
        for string_value, embedding_blob in rows:
            embedding = np.frombuffer(embedding_blob, dtype=np.float32)
            # Cosine similarity (higher is better, so we use 1 - cosine_distance)
            dot_product = np.dot(query_embedding, embedding)
            norm_query = np.linalg.norm(query_embedding)
            norm_embedding = np.linalg.norm(embedding)
            if norm_query > 0 and norm_embedding > 0:
                cosine_sim = dot_product / (norm_query * norm_embedding)
                distance = 1.0 - cosine_sim  # Convert similarity to distance
            else:
                distance = 1.0  # Max distance for zero vectors
            distances.append((string_value, distance))
        
        # Sort by distance and return top k
        distances.sort(key=lambda x: x[1])
        return distances[:k]


    def run_batch(self, initial_values):
        # Workers should NEVER run batch operations
        if getattr(self, 'is_readonly', False):
            logger.debug("StringCache: Skipping run_batch in readonly worker mode")
            return
        
        logger.debug("StringCache: run batch called.")

        # Find values not in cache
        reduced_values = []
        for v in initial_values:
            r = self.get_embedding_from_cache(v, add_if_missing=False, do_not_log_if_missing=True)
            if r is None:
                reduced_values.append(v)  # FIX: append the actual value, not None

        if len(reduced_values) == 0:
            logger.info(f"StringCache: ✅ All {len(initial_values)} values already in cache - skipping string server encoding")
            return
        
        already_cached = len(initial_values) - len(reduced_values)
        if already_cached > 0:
            logger.info(f"StringCache: 📊 Cache filter: {already_cached} already cached, {len(reduced_values)} need encoding via string server")

        df = pd.DataFrame({"string_value": reduced_values })
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        
        # Filter out empty/whitespace strings BEFORE encoding - string server rejects them
        # Empty strings will return None from get_embedding_from_cache, caller handles
        original_count = len(df)
        df = df[df['string_value'].str.strip() != ""]
        skipped_empty = original_count - len(df)
        if skipped_empty > 0:
            logger.info(f"StringCache: ⏭️  Skipped {skipped_empty} empty/whitespace strings (caller will get None)")
        
        if len(df) == 0:
            logger.info(f"StringCache: ✅ No non-empty strings to encode")
            return

        batch_size = 256  # Increase batch size for better GPU utilization
        all_embeddings = []
        
        # Initialize string server client once
        from featrix.neural.string_codec import _init_string_server_client
        client = _init_string_server_client()
        if client is None:
            raise RuntimeError(
                "String server client not available for batch encoding. "
                "Set 'string_server_host' in config.json to 'taco', 'taco.local', or 'localhost'."
            )

        logger.info(f"StringCache: 🚀 Encoding {len(df)} unique strings via string server (batches of {batch_size})...")
        for i in range(0, len(df), batch_size):
            batch = df['string_value'][i:i + batch_size].tolist()
            for j in range(0, len(batch)):
                try:
                    batch[j] = batch[j].strip()
                except:
                    logger.error(f"StringCache: error stripping `{batch[j]}`")
                    traceback.print_exc()
            
            logger.debug(f"StringCache: run_batch: calling encode_batch with {len(batch)} strings...")
            import sys
            sys.stdout.flush()
            sys.stderr.flush()
            batch_embeddings = client.encode_batch(batch)
            logger.debug(f"StringCache: run_batch: encode_batch returned {len(batch_embeddings)} embeddings")
            
            # Convert to numpy arrays for storage
            all_embeddings.extend([np.array(emb, dtype=np.float32) for emb in batch_embeddings])

        df['embeddings_blob'] = [np.array(embedding, dtype=np.float32).tobytes() for embedding in all_embeddings]

        # XXX: ideally we'd filter before doing all the embedding work.
        existing_strings = pd.read_sql(
                                        'SELECT string_value FROM cache', 
                                        self.conn
                                    )['string_value'].tolist()
        filtered_df = df[~df['string_value'].isin(existing_strings)]

        filtered_df[['string_value', 'embeddings_blob']].to_sql('cache', 
                                                       self.conn, 
                                                       if_exists='append', 
                                                       index=False,  # Don't include DataFrame index
                                                       dtype={'string_value': 'text', 'embeddings_blob': 'blob'})

        self.conn.execute("DROP INDEX IF EXISTS cache_string_value")
        self.conn.execute("CREATE INDEX cache_string_value ON cache(string_value)")

        self.conn.commit()
        # Ensure the file is synced to disk before workers start
        self.conn.execute("PRAGMA synchronous = FULL")
        self.conn.commit()
        # Force SQLite to flush to disk
        self.conn.execute("PRAGMA wal_checkpoint(FULL)")
        self.conn.commit()
        logger.info("StringCache: saved and synced to disk...")
        
        # Add newly added embeddings directly to shared memory cache (more efficient than re-reading)
        if not getattr(self, 'is_readonly', False):
            try:
                from featrix.neural.string_codec import _add_to_shared_memory_cache
                added_count = 0
                skipped_count = 0
                for _, row in filtered_df.iterrows():
                    added = _add_to_shared_memory_cache(row['string_value'], row['embeddings_blob'])
                    if added:
                        added_count += 1
                    else:
                        skipped_count += 1
                if added_count > 0:
                    logger.debug(f"StringCache: Added {added_count:,} entries to shared memory cache")
                if skipped_count > 0:
                    logger.debug(f"StringCache: Skipped {skipped_count:,} entries due to memory limit")
            except Exception as e:
                logger.debug(f"Could not add to shared memory cache after run_batch: {e}")
        
        # String server handles GPU memory management - no local model to clean up
        return
    

    @cache_logging
    @lru_cache(maxsize=8192)  # LRU cache for frequently accessed embeddings (2**13 = 8192 entries)
    def get_embedding_from_cache(self, sentence_text, add_if_missing=True, do_not_log_if_missing=False):
        # CRITICAL: Don't try to add if cache is readonly or database is readonly
        if getattr(self, 'is_readonly', False):
            add_if_missing = False
        elif hasattr(self, 'conn') and self.conn:
            # Check if database is actually readonly by testing a simple query
            try:
                # Try to detect readonly by checking if we can write (without actually writing)
                # If we can't, set add_if_missing=False
                import sqlite3
                test_cursor = self.conn.cursor()
                test_cursor.execute("PRAGMA query_only")
                query_only = test_cursor.fetchone()
                if query_only and query_only[0]:
                    add_if_missing = False
            except Exception:
                # If we can't check, assume it might be readonly - don't try to write
                add_if_missing = False
        """
        Get embedding from cache with LRU eviction.
        
        The @lru_cache decorator limits this to 8192 entries (~12-13 MB).
        The shared memory cache has a separate 32 GB limit with LRU eviction.
        """
        # Workers should NEVER add missing embeddings
        if getattr(self, 'is_readonly', False):
            add_if_missing = False
        
        if sentence_text is None:
            sentence_text = ""
        if type(sentence_text) != str:
            sentence_text = str(sentence_text)

        if sentence_text == "":
            logger.debug("StringCache: @@@@ --> get_embedding on an empty string...")
            # traceback.print_stack(file=sys.stdout)

        sentence_text = sentence_text.strip()
        # print(f"@@@....get_embedding for __{sentence_text}__")

        # Check RAM cache first (if using RAM cache only mode)
        # WARNING: This should only be used if SQLite failed - if you see this, SQLite is broken!
        if self._use_ram_cache_only:
            # Log warning once when RAM cache is first used
            if not self._ram_cache_warning_logged:
                logger.warning(f"⚠️  RAM CACHE MODE ACTIVE - SQLite failed! Using in-memory fallback (limit: {self._ram_cache_max_entries:,} entries)")
                logger.warning(f"   This is NOT normal - check SQLite file: {self.filename}")
                self._ram_cache_warning_logged = True
            
            if sentence_text in self._ram_cache:
                return self._ram_cache[sentence_text].clone()
            elif add_if_missing:
                # Empty strings - return None, let caller handle (e.g., use UNKNOWN)
                if sentence_text is None or sentence_text.strip() == "":
                    return None
                
                # Limit RAM cache size - evict oldest if at limit
                if len(self._ram_cache) >= self._ram_cache_max_entries:
                    # Evict first (oldest) entry - simple FIFO eviction
                    oldest_key = next(iter(self._ram_cache))
                    del self._ram_cache[oldest_key]
                    logger.warning(f"⚠️  RAM CACHE FULL: Evicted '{oldest_key[:50]}...' (limit: {self._ram_cache_max_entries:,} entries)")
                    logger.warning(f"   This means SQLite is broken and we're losing cache entries!")
                
                # ALWAYS use string server client for cache misses
                # Use pre-initialized client if available, otherwise initialize
                client = getattr(self, '_string_server_client', None)
                if client is None:
                    logger.warning("⚠️  String server client not pre-initialized in RAM cache mode, initializing now...")
                    from featrix.neural.string_codec import _init_string_server_client
                    client = _init_string_server_client()
                    if client is None:
                        raise RuntimeError(
                            "String server client not available for cache miss encoding.\n"
                            "Set 'string_server_host' in config.json to 'taco', 'taco.local', or 'localhost'."
                        )
                    self._string_server_client = client
                
                # Encode via string server - ALWAYS use string server for cache misses
                embedding_list = client.encode(sentence_text)
                embedding = torch.tensor(embedding_list, dtype=torch.float32)
                self._ram_cache[sentence_text] = embedding
                return embedding.clone()
            else:
                return None

        # SQLite mode - query database
        # Get a fresh cursor to ensure we see committed data
        cursor = self.conn.cursor()
        cursor.execute("SELECT embeddings_blob FROM cache WHERE string_value = ?", (sentence_text,))
        row = cursor.fetchone()
        
        if row:
            # Convert the BLOB back to a numpy array
            embedding = np.frombuffer(row[0], dtype=np.float32)
            # Keep on CPU for DataLoader workers - will move to GPU in training loop via tokenbatch.to(device)
            embedding_tensor = torch.tensor(embedding, dtype=torch.float32)
            # DEBUG: Check string cache output
            assert embedding_tensor.dtype == torch.float32, f"String cache returned {embedding_tensor.dtype}, expected float32"
            return embedding_tensor
        else:
            # CACHE MISS - use string server to encode
            if add_if_missing and not getattr(self, 'is_readonly', False):
                # Cache miss: use string server to encode and add to cache (only if not readonly)
                embedding = self._add_single_cache_entry(sentence_text)
                return embedding
            else:
                # Cache miss and add_if_missing=False - just return None
                # (Don't try to encode - caller doesn't want us to add to cache)
                return None

    def _add_single_cache_entry(self, value):
        """
        Add a single cache entry for a cache miss.
        
        CRITICAL: This ALWAYS uses the string server - there is no fallback.
        The string server client is initialized during cache creation, so it should always be available.
        """
        # Workers should NEVER add cache entries
        if getattr(self, 'is_readonly', False):
            logger.error(f"❌ Worker tried to add cache entry but cache is readonly: {value}")
            return None
        
        # Empty strings - return None, let caller handle (e.g., use UNKNOWN)
        if value is None or value.strip() == "":
            return None
        
        # ALWAYS use string server for cache misses - no fallback, no local model
        # Use pre-initialized string server client (initialized in __init__)
        # This should never be None because we fail fast during initialization
        client = getattr(self, '_string_server_client', None)
        if client is None:
            # Fallback: try to initialize (shouldn't happen if __init__ worked correctly)
            logger.warning("⚠️  String server client not pre-initialized, attempting late initialization...")
            from featrix.neural.string_codec import _init_string_server_client
            client = _init_string_server_client()
            if client is None:
                raise RuntimeError(
                        "String server client not available for cache miss encoding.\n"
                        "This should have been caught during cache initialization.\n"
                        "Set 'string_server_host' in config.json to 'taco', 'taco.local', or 'localhost'.\n"
                        "Cache misses ALWAYS require the string server - there is no fallback."
                )
            self._string_server_client = client
        
        # WARNING: This is inefficient for individual strings during training
        # Consider batching cache misses for better performance
        self.cache_miss_count += 1
        if self.cache_miss_count % 50 == 0:
            logger.warning(f"StringCache: {self.cache_miss_count} individual encodings so far (consider larger initial_values)")
        
        # ALWAYS encode via string server - no fallback, no local model
        embedding_list = client.encode(value)
        embedding_numpy = np.array(embedding_list, dtype=np.float32)
            
        embedding_blob = embedding_numpy.astype(np.float32).tobytes()
        
        # Try to insert into cache, but handle read-only database gracefully
        try:
            self.cursor.execute(
                "INSERT INTO cache (string_value, embeddings_blob) VALUES (?, ?)", 
                (value, embedding_blob)
            )
            self.conn.commit()
        except sqlite3.OperationalError as e:
            if "readonly" in str(e).lower() or "read-only" in str(e).lower():
                # Database is read-only - can't cache, but we can still return the embedding
                # Only log once to avoid spam
                if not getattr(self, '_readonly_warning_logged', False):
                    logger.debug(f"⚠️  String cache database is read-only, encoding without caching (this is OK)")
                    self._readonly_warning_logged = True
                # Return the embedding tensor directly without caching
                embedding_tensor = torch.tensor(embedding_numpy, dtype=torch.float32)
                return embedding_tensor
            else:
                # Some other database error - re-raise
                raise
        
        # Add to shared memory cache if available (with memory limit checking)
        if not getattr(self, 'is_readonly', False):
            try:
                from featrix.neural.string_codec import _add_to_shared_memory_cache
                added = _add_to_shared_memory_cache(value, embedding_blob)
                if not added:
                    logger.debug(f"StringCache: Skipped adding '{value}' to shared memory cache (memory limit)")
            except Exception as e:
                logger.debug(f"Could not add to shared memory cache: {e}")
        
        # Keep on CPU for DataLoader workers - will move to GPU in training loop
        result_tensor = torch.tensor(embedding_numpy, dtype=torch.float32)
        # DEBUG: Check single cache entry output
        assert result_tensor.dtype == torch.float32, f"Single cache entry returned {result_tensor.dtype}, expected float32"
        return result_tensor
    
    def get_gpu_efficiency_stats(self):
        """Return statistics about GPU usage efficiency."""
        total_cache_calls = self.get_embedding_from_cache.cache_info().hits + self.get_embedding_from_cache.cache_info().misses
        cache_hit_rate = self.get_embedding_from_cache.cache_info().hits / max(total_cache_calls, 1)
        
        return {
            'cache_hits': self.get_embedding_from_cache.cache_info().hits,
            'cache_misses': self.get_embedding_from_cache.cache_info().misses,
            'individual_gpu_encodings': self.cache_miss_count,
            'cache_hit_rate': cache_hit_rate,
            'gpu_efficiency': 'Good' if cache_hit_rate > 0.8 else 'Poor' if cache_hit_rate < 0.5 else 'Fair'
        }