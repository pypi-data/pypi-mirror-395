#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
"""
Event logging system for tracking events on sessions.

This module provides functions to log events such as:
- Training events
- Prediction events
- Webhook events
- __featrix field updates
"""

import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


def get_session_event_log_db_path(session_id: str) -> Path:
    """
    Get the path to the event log database for a session.
    
    Args:
        session_id: Session ID
        
    Returns:
        Path to the event log database file
    """
    from config import config
    
    session_dir = config.session_dir / session_id
    return session_dir / "event_log.db"


def init_session_event_log_db(session_id: str):
    """
    Initialize the event log database for a specific session.
    
    Args:
        session_id: Session ID
    """
    db_path = get_session_event_log_db_path(session_id)
    
    # Ensure directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        # Enable WAL mode for better concurrent access
        conn.execute("PRAGMA journal_mode=WAL")
        
        cursor = conn.cursor()
        
        # Create event_log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_time TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_name TEXT NOT NULL,
                event_target TEXT,
                payload_json TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        # Create indexes for efficient querying
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_event_log_session_id ON event_log(event_target)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_event_log_event_type ON event_log(event_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_event_log_event_name ON event_log(event_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_event_log_event_time ON event_log(event_time)")
        
        conn.commit()


def log_event(
    session_id: str,
    event_type: str,
    event_name: str,
    event_target: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None
):
    """
    Log an event to the session's event log database.
    
    Args:
        session_id: Session ID
        event_type: Type of event (e.g., "training", "prediction", "webhook", "__featrix_field_update")
        event_name: Name of the event (e.g., "training_started", "webhook_sent", "__featrix_row_id_set")
        event_target: Target of the event (e.g., predictor_id, webhook_url, field_name)
        payload: Optional JSON-serializable payload with additional event data
    """
    try:
        # Initialize database if it doesn't exist
        init_session_event_log_db(session_id)
        
        db_path = get_session_event_log_db_path(session_id)
        
        # Get current timestamp
        event_time = datetime.now(tz=ZoneInfo("America/New_York"))
        created_at = event_time.isoformat()
        
        # Serialize payload to JSON
        payload_json = json.dumps(payload) if payload else None
        
        # Use session_id as default event_target if not provided
        if event_target is None:
            event_target = session_id
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO event_log (event_time, event_type, event_name, event_target, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                event_time.isoformat(),
                event_type,
                event_name,
                event_target,
                payload_json,
                created_at
            ))
            conn.commit()
            
        logger.debug(f"📝 Logged event: {event_type}/{event_name} for session {session_id}")
        
    except Exception as e:
        # Don't fail the main operation if event logging fails
        logger.warning(f"⚠️  Failed to log event for session {session_id}: {e}")


def log_featrix_field_update(
    session_id: str,
    field_name: str,
    row_id: Optional[int] = None,
    additional_info: Optional[Dict[str, Any]] = None
):
    """
    Log when a __featrix field is updated in the database.
    
    Args:
        session_id: Session ID
        field_name: Name of the __featrix field (e.g., "__featrix_row_id", "__featrix_sentence_embedding_384d")
        row_id: Optional row ID that was updated
        additional_info: Optional additional information about the update
    """
    payload = {
        "field_name": field_name,
    }
    if row_id is not None:
        payload["row_id"] = row_id
    if additional_info:
        payload.update(additional_info)
    
    log_event(
        session_id=session_id,
        event_type="__featrix_field_update",
        event_name=f"__featrix_field_set",
        event_target=field_name,
        payload=payload
    )


def log_training_event(
    session_id: str,
    event_name: str,
    predictor_id: Optional[str] = None,
    additional_info: Optional[Dict[str, Any]] = None
):
    """
    Log a training-related event.
    
    Args:
        session_id: Session ID
        event_name: Name of the training event (e.g., "training_started", "training_completed", "training_failed")
        predictor_id: Optional predictor ID
        additional_info: Optional additional information about the event
    """
    payload = additional_info or {}
    if predictor_id:
        payload["predictor_id"] = predictor_id
    
    log_event(
        session_id=session_id,
        event_type="training",
        event_name=event_name,
        event_target=predictor_id or session_id,
        payload=payload
    )


def log_webhook_event(
    session_id: str,
    event_name: str,
    webhook_url: str,
    additional_info: Optional[Dict[str, Any]] = None
):
    """
    Log a webhook-related event.
    
    Args:
        session_id: Session ID
        event_name: Name of the webhook event (e.g., "webhook_sent", "webhook_failed", "webhook_received")
        webhook_url: URL of the webhook
        additional_info: Optional additional information about the event
    """
    payload = additional_info or {}
    payload["webhook_url"] = webhook_url
    
    log_event(
        session_id=session_id,
        event_type="webhook",
        event_name=event_name,
        event_target=webhook_url,
        payload=payload
    )


def log_prediction_event(
    session_id: str,
    event_name: str,
    prediction_id: Optional[str] = None,
    additional_info: Optional[Dict[str, Any]] = None
):
    """
    Log a prediction-related event.
    
    Args:
        session_id: Session ID
        event_name: Name of the prediction event (e.g., "prediction_made", "prediction_corrected")
        prediction_id: Optional prediction ID
        additional_info: Optional additional information about the event
    """
    payload = additional_info or {}
    if prediction_id:
        payload["prediction_id"] = prediction_id
    
    log_event(
        session_id=session_id,
        event_type="prediction",
        event_name=event_name,
        event_target=prediction_id or session_id,
        payload=payload
    )

