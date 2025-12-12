#!/usr/bin/env python3
"""
Prediction Persistence Worker

This worker monitors Redis for new predictions and persists them to SQLite databases.
It runs as a background process managed by supervisor.
"""

import time
import logging
import sqlite3
import json
import traceback
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from redis_prediction_store import RedisPredictionStore

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s'
)
logger = logging.getLogger(__name__)

class PredictionPersistenceWorker:
    """Worker that persists predictions from Redis to SQLite."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0", batch_size: int = 50, 
                 poll_interval: int = 5):
        """
        Initialize the persistence worker.
        
        Args:
            redis_url: Redis connection URL
            batch_size: Number of predictions to process in each batch
            poll_interval: Seconds between polling for new predictions
        """
        self.redis_store = RedisPredictionStore(redis_url)
        self.batch_size = batch_size
        self.poll_interval = poll_interval
        
    def get_session_predictions_db_path(self, session_id: str) -> Path:
        """Get the SQLite database path for a session."""
        return Path("jobs") / session_id / "predictions.db"
    
    def init_session_predictions_db(self, session_id: str):
        """Initialize the predictions database for a specific session."""
        db_path = self.get_session_predictions_db_path(session_id)
        
        # Ensure directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(db_path) as conn:
            # Enable WAL mode for better concurrent access
            conn.execute("PRAGMA journal_mode=WAL")
            
            cursor = conn.cursor()
            
            # Create predictions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    prediction_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    input_data TEXT NOT NULL,
                    prediction_result TEXT NOT NULL,
                    predicted_class TEXT,
                    confidence REAL,
                    user_label TEXT,
                    is_corrected BOOLEAN DEFAULT FALSE,
                    created_at TEXT NOT NULL,
                    updated_at TEXT,
                    model_version TEXT,
                    embedding_space_hash TEXT,
                    persisted_at TEXT
                )
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_session_id ON predictions(session_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_corrected ON predictions(is_corrected)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_persisted_at ON predictions(persisted_at)")
            
            # Create retraining_batches table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS retraining_batches (
                    batch_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    prediction_count INTEGER DEFAULT 0,
                    correction_count INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    status TEXT DEFAULT 'pending'
                )
            """)
            
            # Create indexes for retraining_batches
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_batches_session_id ON retraining_batches(session_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_batches_status ON retraining_batches(status)")
            
            conn.commit()
            logger.info(f"Initialized SQLite database for session {session_id}")
    
    def persist_prediction(self, prediction_data: Dict[str, Any]) -> bool:
        """
        Persist a single prediction to SQLite.
        
        Args:
            prediction_data: Prediction data from Redis
            
        Returns:
            True if successfully persisted, False otherwise
        """
        try:
            session_id = prediction_data["session_id"]
            prediction_id = prediction_data["prediction_id"]
            
            # Initialize database for this session if it doesn't exist
            self.init_session_predictions_db(session_id)
            
            db_path = self.get_session_predictions_db_path(session_id)
            
            with sqlite3.connect(db_path, timeout=10.0) as conn:
                # Enable WAL mode for better concurrent access
                conn.execute("PRAGMA journal_mode=WAL")
                
                cursor = conn.cursor()
                
                # Check if prediction already exists (for updates)
                cursor.execute("SELECT prediction_id FROM predictions WHERE prediction_id = ?", 
                             (prediction_id,))
                exists = cursor.fetchone()
                
                persisted_at = datetime.utcnow().isoformat()
                
                # Ensure input_data and prediction_result are JSON strings for SQLite
                input_data = prediction_data.get("input_data", "{}")
                if isinstance(input_data, dict):
                    input_data = json.dumps(input_data)
                    
                prediction_result = prediction_data.get("prediction_result", "{}")
                if isinstance(prediction_result, dict):
                    prediction_result = json.dumps(prediction_result)
                
                if exists:
                    # Update existing prediction
                    cursor.execute("""
                        UPDATE predictions SET
                            input_data = ?, prediction_result = ?, predicted_class = ?,
                            confidence = ?, user_label = ?, is_corrected = ?,
                            updated_at = ?, model_version = ?, persisted_at = ?
                        WHERE prediction_id = ?
                    """, (
                        input_data,
                        prediction_result,
                        prediction_data.get("predicted_class"),
                        prediction_data.get("confidence"),
                        prediction_data.get("user_label"),
                        prediction_data.get("is_corrected", "False").lower() == "true",
                        prediction_data.get("updated_at"),
                        prediction_data.get("model_version", "v1"),
                        persisted_at,
                        prediction_id
                    ))
                    logger.info(f"Updated prediction {prediction_id} in SQLite")
                else:
                    # Insert new prediction
                    cursor.execute("""
                        INSERT INTO predictions (
                            prediction_id, session_id, input_data, prediction_result,
                            predicted_class, confidence, user_label, is_corrected,
                            created_at, updated_at, model_version, persisted_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        prediction_id,
                        session_id,
                        input_data,
                        prediction_result,
                        prediction_data.get("predicted_class"),
                        prediction_data.get("confidence"),
                        prediction_data.get("user_label"),
                        prediction_data.get("is_corrected", "False").lower() == "true",
                        prediction_data.get("created_at"),
                        prediction_data.get("updated_at"),
                        prediction_data.get("model_version", "v1"),
                        persisted_at
                    ))
                    logger.info(f"Inserted prediction {prediction_id} into SQLite")
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error persisting prediction {prediction_data.get('prediction_id', 'unknown')}: {e}")
            traceback.print_exc()
            return False
    
    def process_batch(self) -> int:
        """
        Process a batch of predictions from Redis to SQLite.
        
        Returns:
            Number of predictions successfully processed
        """
        try:
            # Get batch of prediction IDs to process
            prediction_ids = self.redis_store.get_pending_predictions(self.batch_size)
            
            if not prediction_ids:
                return 0
            
            processed_count = 0
            
            for prediction_id in prediction_ids:
                try:
                    # Get prediction data from Redis
                    prediction_data = self.redis_store.get_prediction(prediction_id)
                    
                    if not prediction_data:
                        logger.warning(f"Prediction {prediction_id} not found in Redis")
                        continue
                    
                    # Persist to SQLite
                    if self.persist_prediction(prediction_data):
                        # Mark as persisted in Redis
                        self.redis_store.mark_as_persisted(prediction_id)
                        processed_count += 1
                    else:
                        # Put back in queue for retry
                        self.redis_store.redis_client.lpush(
                            self.redis_store.PENDING_PERSISTENCE_KEY, 
                            prediction_id
                        )
                        
                except Exception as e:
                    logger.error(f"Error processing prediction {prediction_id}: {e}")
                    # Put back in queue for retry
                    self.redis_store.redis_client.lpush(
                        self.redis_store.PENDING_PERSISTENCE_KEY, 
                        prediction_id
                    )
            
            if processed_count > 0:
                logger.info(f"Processed {processed_count}/{len(prediction_ids)} predictions")
            
            return processed_count
            
        except Exception as e:
            logger.error(f"Error in process_batch: {e}")
            traceback.print_exc()
            return 0
    
    def run(self):
        """Main worker loop."""
        logger.info("Starting prediction persistence worker")
        
        try:
            while True:
                start_time = time.time()
                
                # Process a batch of predictions
                processed = self.process_batch()
                
                # Sleep if no work was done
                if processed == 0:
                    time.sleep(self.poll_interval)
                else:
                    # Brief pause between batches when there's work
                    time.sleep(1)
                    
                # Log stats periodically
                elapsed = time.time() - start_time
                if elapsed > 60:  # Every minute
                    stats = self.redis_store.get_stats()
                    logger.info(f"Stats: {stats['total_predictions']} total predictions, "
                              f"{stats['pending_persistence']} pending persistence")
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down")
        except Exception as e:
            logger.error(f"Fatal error in worker: {e}")
            traceback.print_exc()
            raise


def main():
    """Entry point for the worker."""
    import os
    
    # Get configuration from environment
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    batch_size = int(os.getenv("BATCH_SIZE", "50"))
    poll_interval = int(os.getenv("POLL_INTERVAL", "5"))
    
    logger.info(f"Starting with Redis URL: {redis_url}, batch size: {batch_size}, "
               f"poll interval: {poll_interval}s")
    
    # Create and run worker
    worker = PredictionPersistenceWorker(
        redis_url=redis_url,
        batch_size=batch_size,
        poll_interval=poll_interval
    )
    
    worker.run()


if __name__ == "__main__":
    main() 