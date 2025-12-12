#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

import json
import sqlite3
import logging
import queue
import threading
import time

logger = logging.getLogger(__name__)


class TrainingHistoryDB:
    """
    SQLite-based storage for training history to prevent memory leaks.
    Stores loss_history, mutual_information, and training_timeline to disk.
    Uses a background thread for async writes to avoid blocking training.
    Keeps only recent entries in memory for immediate access.
    """
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None  # Will be created in write thread
        # Use bounded queue to prevent memory issues if background thread falls behind
        self.write_queue = queue.Queue(maxsize=1000)
        self.stop_event = threading.Event()
        self.write_thread = None
        self.db_initialized = threading.Event()  # Signal when DB is ready
        # Keep only last 20 epochs in memory for quick access
        self.memory_cache_size = 20
        # Start background write thread (will initialize DB there)
        self._start_write_thread()
        
    def _init_db(self):
        """Initialize SQLite database with required tables (called from write thread)."""
        # Create connection in the write thread (SQLite is thread-local)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")  # Better concurrent access
        
        cursor = self.conn.cursor()
        
        # Loss history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loss_history (
                epoch INTEGER PRIMARY KEY,
                current_learning_rate REAL,
                loss REAL,
                validation_loss REAL,
                time_now REAL,
                duration REAL,
                spread REAL,
                joint REAL,
                marginal REAL,
                marginal_weighted REAL
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_loss_history_epoch ON loss_history(epoch)")
        
        # Mutual information table (stored as JSON blob)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mutual_information (
                epoch INTEGER PRIMARY KEY,
                columns_json TEXT,
                joint_json TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mi_epoch ON mutual_information(epoch)")
        
        # Training timeline table (stored as JSON blob for flexibility)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS training_timeline (
                epoch INTEGER PRIMARY KEY,
                timeline_entry_json TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_timeline_epoch ON training_timeline(epoch)")
        
        self.conn.commit()
        self.db_initialized.set()  # Signal that DB is ready
        
    def _start_write_thread(self):
        """Start background thread for async SQLite writes."""
        self.write_thread = threading.Thread(target=self._write_worker, daemon=True)
        self.write_thread.start()
        logger.debug("TrainingHistoryDB: Background write thread started")
        
    def _write_worker(self):
        """Background worker thread that processes write queue."""
        # Initialize DB in this thread (SQLite connections are thread-local)
        self._init_db()
        
        while not self.stop_event.is_set():
            try:
                # Wait for items with timeout to allow checking stop_event
                try:
                    item = self.write_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                    
                item_type = item.get("type")
                
                if item_type == "loss_history":
                    self._save_loss_history_sync(item["data"])
                elif item_type == "mutual_information":
                    self._save_mutual_information_sync(item["data"]["epoch"], item["data"]["entry"])
                elif item_type == "timeline_entry":
                    self._save_timeline_entry_sync(item["data"]["epoch"], item["data"]["entry"])
                elif item_type == "flush":
                    # Explicit flush request - commit any pending writes
                    if self.conn:
                        self.conn.commit()
                    logger.debug("TrainingHistoryDB: Flush completed")
                elif item_type == "stop":
                    break
                    
                self.write_queue.task_done()
            except Exception as e:
                logger.error(f"TrainingHistoryDB write worker error: {e}", exc_info=True)
                
    def _save_loss_history_sync(self, loss_entry: dict):
        """Synchronous save of loss history (called from write thread)."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO loss_history 
            (epoch, current_learning_rate, loss, validation_loss, time_now, duration, 
             spread, joint, marginal, marginal_weighted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            loss_entry.get("epoch"),
            loss_entry.get("current_learning_rate"),
            loss_entry.get("loss"),
            loss_entry.get("validation_loss"),
            loss_entry.get("time_now"),
            loss_entry.get("duration"),
            loss_entry.get("spread"),
            loss_entry.get("joint"),
            loss_entry.get("marginal"),
            loss_entry.get("marginal_weighted")
        ))
        self.conn.commit()
        
    def _save_mutual_information_sync(self, epoch: int, mi_entry: dict):
        """Synchronous save of mutual information (called from write thread)."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO mutual_information (epoch, columns_json, joint_json)
            VALUES (?, ?, ?)
        """, (
            epoch,
            json.dumps(mi_entry.get("columns", {})),
            json.dumps(mi_entry.get("joint", {}))
        ))
        self.conn.commit()
        
    def _save_timeline_entry_sync(self, epoch: int, timeline_entry: dict):
        """Synchronous save of timeline entry (called from write thread)."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO training_timeline (epoch, timeline_entry_json)
            VALUES (?, ?)
        """, (epoch, json.dumps(timeline_entry)))
        self.conn.commit()
        
    def push_loss_history(self, loss_entry: dict):
        """Push loss history entry to write queue (non-blocking)."""
        try:
            self.write_queue.put_nowait({"type": "loss_history", "data": loss_entry})
        except queue.Full:
            logger.warning("TrainingHistoryDB: Write queue full, dropping loss_history entry")
        
    def push_mutual_information(self, epoch: int, mi_entry: dict):
        """Push mutual information entry to write queue (non-blocking)."""
        try:
            self.write_queue.put_nowait({
                "type": "mutual_information",
                "data": {"epoch": epoch, "entry": mi_entry}
            })
        except queue.Full:
            logger.warning("TrainingHistoryDB: Write queue full, dropping mutual_information entry")
            
    def push_timeline_entry(self, epoch: int, timeline_entry: dict):
        """Push timeline entry to write queue (non-blocking)."""
        try:
            self.write_queue.put_nowait({
                "type": "timeline_entry",
                "data": {"epoch": epoch, "entry": timeline_entry}
            })
        except queue.Full:
            logger.warning("TrainingHistoryDB: Write queue full, dropping timeline_entry")
            
    def flush(self):
        """Request a flush of pending writes (waits for completion)."""
        self.write_queue.put({"type": "flush"})
        # Wait a bit for flush to complete (not blocking indefinitely)
        time.sleep(0.1)
        
    def get_recent_loss_history(self, num_epochs: int = None) -> list:
        """Get recent loss history from database."""
        # Wait for DB to be initialized
        if not self.db_initialized.wait(timeout=5.0):
            logger.warning("TrainingHistoryDB: Database not initialized yet")
            return []
        
        if num_epochs is None:
            num_epochs = self.memory_cache_size
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT epoch, current_learning_rate, loss, validation_loss, time_now, duration,
                   spread, joint, marginal, marginal_weighted
            FROM loss_history
            ORDER BY epoch DESC
            LIMIT ?
        """, (num_epochs,))
        rows = cursor.fetchall()
        # Convert back to dict format, in ascending epoch order
        result = []
        for row in reversed(rows):
            result.append({
                "epoch": row[0],
                "current_learning_rate": row[1],
                "loss": row[2],
                "validation_loss": row[3],
                "time_now": row[4],
                "duration": row[5],
                "spread": row[6],
                "joint": row[7],
                "marginal": row[8],
                "marginal_weighted": row[9]
            })
        return result
        
    def get_all_loss_history(self) -> list:
        """Get all loss history from database (for final summary)."""
        # Wait for DB to be initialized
        if not self.db_initialized.wait(timeout=5.0):
            logger.warning("TrainingHistoryDB: Database not initialized yet")
            return []
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT epoch, current_learning_rate, loss, validation_loss, time_now, duration,
                   spread, joint, marginal, marginal_weighted
            FROM loss_history
            ORDER BY epoch ASC
        """)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "epoch": row[0],
                "current_learning_rate": row[1],
                "loss": row[2],
                "validation_loss": row[3],
                "time_now": row[4],
                "duration": row[5],
                "spread": row[6],
                "joint": row[7],
                "marginal": row[8],
                "marginal_weighted": row[9]
            })
        return result
        
    def close(self):
        """Close database connection and stop background thread."""
        # Signal stop to background thread
        self.stop_event.set()
        # Send stop message to queue
        try:
            self.write_queue.put_nowait({"type": "stop"})
        except queue.Full:
            pass
        
        # Wait for write thread to finish (with timeout)
        if self.write_thread and self.write_thread.is_alive():
            self.write_thread.join(timeout=5.0)
            if self.write_thread.is_alive():
                logger.warning("TrainingHistoryDB: Write thread did not stop gracefully")
        
        # Close database connection (connection is in write thread, but we can close it here
        # since check_same_thread=False was used)
        if self.conn:
            try:
                self.conn.close()
                self.conn = None
                logger.debug("TrainingHistoryDB: Database connection closed")
            except Exception as e:
                logger.warning(f"TrainingHistoryDB: Error closing connection: {e}")

