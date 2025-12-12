#!/usr/bin/env python3
"""
Local crash tracking for admin monitor display.

Stores crashes in SQLite for persistence and retrieval.
Integrates with existing TracebackMonitor from system_monitor.py.
"""
import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

CRASH_DB_PATH = Path("/tmp/featrix-crashes.db")


def _init_crash_db():
    """Initialize crash tracking database."""
    conn = sqlite3.connect(CRASH_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crashes (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            hostname TEXT,
            process_name TEXT,
            exception_type TEXT,
            exception_message TEXT,
            traceback_json TEXT NOT NULL,
            acknowledged INTEGER DEFAULT 0,
            acknowledged_at TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Index for quick lookups
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON crashes(timestamp DESC)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_acknowledged ON crashes(acknowledged)")
    
    conn.commit()
    conn.close()


def save_crash(traceback_data: Dict) -> bool:
    """
    Save crash to local SQLite database.
    
    Args:
        traceback_data: Enhanced traceback dict from TracebackMonitor
        
    Returns:
        True if saved, False on error
    """
    try:
        _init_crash_db()
        
        crash_id = traceback_data.get("__id__")
        if not crash_id:
            logger.warning("Traceback has no ID, cannot save")
            return False
        
        timestamp = traceback_data.get("__timestamp__", datetime.now().isoformat())
        metadata = traceback_data.get("__monitor_metadata__", {})
        hostname = metadata.get("hostname") or traceback_data.get("__hostname__", "unknown")
        process_name = metadata.get("process", "unknown")
        exception_type = traceback_data.get("exception_type", "unknown")
        exception_message = traceback_data.get("exception_message", "")
        
        conn = sqlite3.connect(CRASH_DB_PATH)
        cursor = conn.cursor()
        
        # Insert or replace (in case same crash reported multiple times)
        cursor.execute("""
            INSERT OR REPLACE INTO crashes 
            (id, timestamp, hostname, process_name, exception_type, exception_message, traceback_json, acknowledged)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            crash_id,
            timestamp,
            hostname,
            process_name,
            exception_type,
            exception_message[:500],  # Truncate long messages
            json.dumps(traceback_data)
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"💾 Saved crash {crash_id[:8]} to local database")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save crash to database: {e}")
        return False


def get_recent_crashes(limit: int = 50, include_acknowledged: bool = False) -> List[Dict]:
    """
    Get recent crashes from database.
    
    Args:
        limit: Maximum number of crashes to return
        include_acknowledged: If True, include acknowledged crashes
        
    Returns:
        List of crash dicts
    """
    try:
        if not CRASH_DB_PATH.exists():
            return []
        
        conn = sqlite3.connect(CRASH_DB_PATH)
        cursor = conn.cursor()
        
        if include_acknowledged:
            cursor.execute("""
                SELECT id, timestamp, hostname, process_name, exception_type, exception_message, 
                       acknowledged, acknowledged_at, traceback_json
                FROM crashes
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
        else:
            cursor.execute("""
                SELECT id, timestamp, hostname, process_name, exception_type, exception_message,
                       acknowledged, acknowledged_at, traceback_json
                FROM crashes
                WHERE acknowledged = 0
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        crashes = []
        for row in rows:
            crash = {
                'id': row[0],
                'timestamp': row[1],
                'hostname': row[2],
                'process_name': row[3],
                'exception_type': row[4],
                'exception_message': row[5],
                'acknowledged': bool(row[6]),
                'acknowledged_at': row[7],
                'traceback_json': json.loads(row[8]) if row[8] else None,
            }
            crashes.append(crash)
        
        return crashes
        
    except Exception as e:
        logger.error(f"Failed to get recent crashes: {e}")
        return []


def acknowledge_crash(crash_id: str) -> bool:
    """
    Mark a crash as acknowledged.
    
    Args:
        crash_id: UUID of the crash to acknowledge
        
    Returns:
        True if acknowledged, False on error
    """
    try:
        if not CRASH_DB_PATH.exists():
            return False
        
        conn = sqlite3.connect(CRASH_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE crashes
            SET acknowledged = 1, acknowledged_at = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), crash_id))
        
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        
        if affected > 0:
            logger.info(f"✅ Acknowledged crash {crash_id[:8]}")
            return True
        else:
            logger.warning(f"Crash {crash_id[:8]} not found")
            return False
        
    except Exception as e:
        logger.error(f"Failed to acknowledge crash: {e}")
        return False


def get_crash_stats() -> Dict:
    """
    Get crash statistics.
    
    Returns:
        Dict with total, unacknowledged, by_type counts
    """
    try:
        if not CRASH_DB_PATH.exists():
            return {'total': 0, 'unacknowledged': 0, 'by_type': {}}
        
        conn = sqlite3.connect(CRASH_DB_PATH)
        cursor = conn.cursor()
        
        # Total crashes
        cursor.execute("SELECT COUNT(*) FROM crashes")
        total = cursor.fetchone()[0]
        
        # Unacknowledged
        cursor.execute("SELECT COUNT(*) FROM crashes WHERE acknowledged = 0")
        unacked = cursor.fetchone()[0]
        
        # By exception type
        cursor.execute("""
            SELECT exception_type, COUNT(*) 
            FROM crashes 
            WHERE acknowledged = 0
            GROUP BY exception_type
        """)
        by_type = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total': total,
            'unacknowledged': unacked,
            'by_type': by_type
        }
        
    except Exception as e:
        logger.error(f"Failed to get crash stats: {e}")
        return {'total': 0, 'unacknowledged': 0, 'by_type': {}}


if __name__ == '__main__':
    # Test the crash tracker
    logging.basicConfig(level=logging.INFO)
    
    print("\n" + "=" * 80)
    print("CRASH TRACKER TEST")
    print("=" * 80 + "\n")
    
    # Create a fake crash
    fake_crash = {
        "__id__": "test-crash-123",
        "__timestamp__": datetime.now().isoformat(),
        "__hostname__": "test-host",
        "exception_type": "TestException",
        "exception_message": "This is a test crash",
        "frames": [],
        "__monitor_metadata__": {
            "process": "test-process",
            "log_file": "/tmp/test.log"
        }
    }
    
    # Save it
    if save_crash(fake_crash):
        print("✅ Saved test crash")
    
    # Retrieve recent
    crashes = get_recent_crashes(limit=10)
    print(f"\n📋 Recent crashes: {len(crashes)}")
    for crash in crashes:
        print(f"   • {crash['exception_type']}: {crash['exception_message'][:50]}")
    
    # Get stats
    stats = get_crash_stats()
    print(f"\n📊 Stats: {stats}")
    
    print("\n✅ Test complete!\n")

