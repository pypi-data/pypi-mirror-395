#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import sqlite3
import json
import logging
import os
import numpy as np
import torch
from pathlib import Path
from typing import Dict, List, Optional, Any
from featrix.neural.device import device

# Import logging configuration
from featrix.neural.logging_config import configure_logging
configure_logging()

logger = logging.getLogger(__name__)


class JsonCache:
    """
    Cache for JSON embeddings, similar to StringCache but:
    - Uses embedding spaces to encode JSON values
    - Creates a table per column for caching
    - Queries API to find matching ES for schema
    """
    
    def __init__(self, column_name: str, json_cache_filename: str = None, 
                 embedding_space=None, schema_fields: List[str] = None,
                 child_es_session_id: str = None, api_base_url: str = None):
        """
        Initialize JSON cache for a specific column.
        
        Args:
            column_name: Name of the column this cache is for
            json_cache_filename: Path to SQLite database file (default: json_cache.sqlite3)
            embedding_space: Pre-loaded embedding space to use for encoding (legacy, prefer child_es_session_id)
            schema_fields: List of field names in the JSON schema
            child_es_session_id: Session ID of the child ES to use for encoding (via API)
            api_base_url: Base URL for the API server (default: http://localhost:8000)
        """
        assert column_name is not None, "column_name is required for JsonCache"
        
        self.column_name = column_name
        self.filename = json_cache_filename or "json_cache.sqlite3"
        self.embedding_space = embedding_space  # Legacy support
        self.child_es_session_id = child_es_session_id
        self.schema_fields = schema_fields or []
        self.cache_miss_count = 0
        
        # Get API base URL
        if api_base_url:
            self.api_base_url = api_base_url
        else:
            try:
                from config import config as app_config
                self.api_base_url = getattr(app_config, 'api_base_url', 'http://localhost:8000')
            except:
                self.api_base_url = 'http://localhost:8000'
        
        if not self.api_base_url.startswith('http'):
            self.api_base_url = f"http://{self.api_base_url}"
        
        logger.info(f"🔍 JSONCACHE DEBUG: column_name = {column_name}")
        logger.info(f"🔍 JSONCACHE DEBUG: json_cache_filename = {json_cache_filename}")
        logger.info(f"🔍 JSONCACHE DEBUG: resolved filename = {self.filename}")
        logger.info(f"🔍 JSONCACHE DEBUG: current working directory = {os.getcwd()}")
        logger.info(f"🔍 JSONCACHE DEBUG: resolved path = {os.path.abspath(self.filename)}")
        
        load_existing = os.path.exists(self.filename)
        logger.info(f"JsonCache[{column_name}]: load_existing = {load_existing}; filename = {self.filename}")
        
        self.conn = sqlite3.connect(self.filename)
        self.cursor = self.conn.cursor()
        
        # Create table for this column if it doesn't exist
        table_name = self._get_table_name(column_name)
        if not load_existing:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    json_value TEXT PRIMARY KEY,
                    embeddings_blob BLOB
                )
            """)
            self.conn.commit()
            logger.info(f"JsonCache[{column_name}]: Created table {table_name}")
        else:
            # Log existing cache statistics
            try:
                self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                existing_count = self.cursor.fetchone()[0]
                logger.info(f"JsonCache[{column_name}]: ✅ Loaded existing cache with {existing_count:,} embeddings")
            except sqlite3.OperationalError:
                # Table doesn't exist yet, create it
                self.cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        json_value TEXT PRIMARY KEY,
                        embeddings_blob BLOB
                    )
                """)
                self.conn.commit()
                logger.info(f"JsonCache[{column_name}]: Created table {table_name}")
        
        # Create index for faster lookups
        try:
            self.cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_json_value ON {table_name}(json_value)")
            self.conn.commit()
        except sqlite3.OperationalError:
            pass  # Index might already exist
    
    def _get_table_name(self, column_name: str) -> str:
        """Get safe table name for column (sanitize for SQL)."""
        # Replace special characters with underscores
        safe_name = "".join(c if c.isalnum() or c == '_' else '_' for c in column_name)
        return f"json_cache_{safe_name}"
    
    def _normalize_json_value(self, value: Any) -> str:
        """Normalize JSON value to string for caching."""
        if isinstance(value, (dict, list)):
            # Sort dict keys for consistent representation
            return json.dumps(value, sort_keys=True)
        return json.dumps(value) if value is not None else ""
    
    def get_embedding_from_cache(self, json_value: Any, add_if_missing: bool = True) -> Optional[torch.Tensor]:
        """
        Get embedding from cache for a JSON value.
        
        Args:
            json_value: The JSON value (dict, list, or string)
            add_if_missing: If True, encode and cache if not found
            
        Returns:
            Embedding tensor or None if not found and add_if_missing=False
        """
        if json_value is None:
            json_value = {}
        
        # Normalize JSON value to string
        json_str = self._normalize_json_value(json_value)
        
        table_name = self._get_table_name(self.column_name)
        self.cursor.execute(f"SELECT embeddings_blob FROM {table_name} WHERE json_value = ?", (json_str,))
        row = self.cursor.fetchone()
        
        if row:
            # Convert BLOB back to tensor
            embedding = np.frombuffer(row[0], dtype=np.float32)
            # Keep on CPU for DataLoader workers
            embedding_tensor = torch.tensor(embedding, dtype=torch.float32)
            return embedding_tensor
        else:
            if add_if_missing and self.embedding_space:
                # Encode and cache
                embedding = self._encode_and_cache(json_value, json_str)
                return embedding
            else:
                logger.debug(f"JsonCache[{self.column_name}]: Cache miss for {json_str[:50]}...")
                self.cache_miss_count += 1
                return None
    
    def _encode_and_cache(self, json_value: Any, json_str: str) -> torch.Tensor:
        """Encode JSON value using child ES via API and cache it."""
        try:
            # Convert JSON value to record format for encoding
            if isinstance(json_value, str):
                # Try to parse if it's a string
                try:
                    json_value = json.loads(json_value)
                except:
                    pass
            
            # Ensure it's a dict for encoding
            if isinstance(json_value, list) and len(json_value) > 0 and isinstance(json_value[0], dict):
                # For lists of dicts, encode the first dict (or we could encode all and average)
                record = json_value[0]
            elif isinstance(json_value, dict):
                record = json_value
            else:
                # Fallback: create empty dict
                record = {}
            
            # Encode using child ES via API
            if self.child_es_session_id:
                # Use API call to child ES
                import requests
                url = f"{self.api_base_url}/session/{self.child_es_session_id}/encode_records"
                payload = {"query_record": record}
                
                logger.debug(f"JsonCache[{self.column_name}]: Encoding via API: {url}")
                response = requests.post(url, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    # Use embedding_long (full embedding) for training
                    embedding_list = result.get("embedding_long", result.get("embedding", []))
                    # Keep on CPU for DataLoader workers
                    embedding = torch.tensor(embedding_list, dtype=torch.float32)
                else:
                    logger.error(f"JsonCache[{self.column_name}]: API encoding failed: {response.status_code} - {response.text}")
                    # Keep on CPU for DataLoader workers
                    embedding = torch.zeros(384, dtype=torch.float32)
            elif self.embedding_space:
                # Legacy: use local embedding space directly
                embedding = self.embedding_space.encode_record(record, squeeze=True)
            else:
                logger.warning(f"JsonCache[{self.column_name}]: No child ES session ID or embedding space available")
                # Keep on CPU for DataLoader workers
                embedding = torch.zeros(384, dtype=torch.float32)
            
            # Cache the embedding
            table_name = self._get_table_name(self.column_name)
            embedding_blob = embedding.cpu().numpy().astype(np.float32).tobytes()
            self.cursor.execute(
                f"INSERT OR REPLACE INTO {table_name} (json_value, embeddings_blob) VALUES (?, ?)",
                (json_str, embedding_blob)
            )
            self.conn.commit()
            
            return embedding
            
        except Exception as e:
            logger.error(f"JsonCache[{self.column_name}]: Error encoding JSON value: {e}")
            import traceback
            logger.error(traceback.format_exc())
            # Return zero embedding as fallback - keep on CPU for DataLoader workers
            return torch.zeros(384, dtype=torch.float32)
    
    def run_batch(self, initial_values: List[Any]):
        """
        Pre-compute and cache embeddings for a batch of JSON values.
        
        Args:
            initial_values: List of JSON values to cache
        """
        logger.info(f"JsonCache[{self.column_name}]: Caching batch of {len(initial_values)} values")
        
        if not self.embedding_space:
            logger.warning(f"JsonCache[{self.column_name}]: No embedding space - skipping batch caching")
            return
        
        table_name = self._get_table_name(self.column_name)
        cached_count = 0
        new_count = 0
        
        for json_value in initial_values:
            if json_value is None:
                continue
            
            json_str = self._normalize_json_value(json_value)
            
            # Check if already cached
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE json_value = ?", (json_str,))
            if self.cursor.fetchone()[0] > 0:
                cached_count += 1
                continue
            
            # Encode and cache
            try:
                self._encode_and_cache(json_value, json_str)
                new_count += 1
            except Exception as e:
                logger.warning(f"JsonCache[{self.column_name}]: Failed to cache value: {e}")
        
        self.conn.commit()
        logger.info(f"JsonCache[{self.column_name}]: Batch complete - {cached_count} already cached, {new_count} newly cached")
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

