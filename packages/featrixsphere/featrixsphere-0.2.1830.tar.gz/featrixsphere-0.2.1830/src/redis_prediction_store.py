"""
Redis-based prediction storage system.

This module provides utilities for storing prediction results in Redis
and managing the persistence to SQLite databases.
"""

import redis
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class RedisPredictionStore:
    """Redis-based prediction storage with automatic persistence to SQLite."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        """Initialize Redis connection."""
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        
        # Redis key patterns
        self.PREDICTION_KEY = "prediction:{prediction_id}"
        self.SESSION_PREDICTIONS_KEY = "session_predictions:{session_id}"
        self.PENDING_PERSISTENCE_KEY = "pending_persistence"
        
    def store_prediction(self, session_id: str, input_data: Dict[str, Any], 
                        prediction_result: Dict[str, Any], predicted_class: str = None, 
                        confidence: float = None, model_version: str = "v1") -> str:
        """
        Store a prediction in Redis with automatic persistence queuing.
        
        Args:
            session_id: Session ID
            input_data: Input data for prediction
            prediction_result: Prediction result
            predicted_class: Predicted class (for classification)
            confidence: Prediction confidence
            model_version: Model version
            
        Returns:
            prediction_id: UUID for the prediction
        """
        prediction_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        # Create prediction record
        prediction_record = {
            "prediction_id": prediction_id,
            "session_id": session_id,
            "input_data": json.dumps(input_data),
            "prediction_result": json.dumps(prediction_result),
            "predicted_class": predicted_class or "",
            "confidence": str(confidence) if confidence is not None else "",
            "created_at": now,
            "model_version": model_version,
            "persisted": "False"
        }
        
        # Store in Redis
        prediction_key = self.PREDICTION_KEY.format(prediction_id=prediction_id)
        self.redis_client.hset(prediction_key, mapping=prediction_record)
        
        # Add to session's prediction list
        session_key = self.SESSION_PREDICTIONS_KEY.format(session_id=session_id)
        self.redis_client.lpush(session_key, prediction_id)
        
        # Add to pending persistence queue
        self.redis_client.lpush(self.PENDING_PERSISTENCE_KEY, prediction_id)
        
        logger.info(f"Stored prediction {prediction_id} for session {session_id}")
        return prediction_id
    
    def get_prediction(self, prediction_id: str) -> Optional[Dict[str, Any]]:
        """Get a prediction by ID from Redis."""
        prediction_key = self.PREDICTION_KEY.format(prediction_id=prediction_id)
        prediction_data = self.redis_client.hgetall(prediction_key)
        
        if not prediction_data:
            return None
            
        # Parse JSON fields
        if prediction_data.get('input_data'):
            prediction_data['input_data'] = json.loads(prediction_data['input_data'])
        if prediction_data.get('prediction_result'):
            prediction_data['prediction_result'] = json.loads(prediction_data['prediction_result'])
            
        # Convert string booleans
        prediction_data['persisted'] = prediction_data.get('persisted', 'False').lower() == 'true'
        
        # Convert confidence to float if present
        if prediction_data.get('confidence'):
            try:
                prediction_data['confidence'] = float(prediction_data['confidence'])
            except (ValueError, TypeError):
                prediction_data['confidence'] = None
                
        return prediction_data
    
    def get_session_predictions(self, session_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get predictions for a session from Redis."""
        session_key = self.SESSION_PREDICTIONS_KEY.format(session_id=session_id)
        prediction_ids = self.redis_client.lrange(session_key, 0, limit - 1)
        
        predictions = []
        for prediction_id in prediction_ids:
            prediction = self.get_prediction(prediction_id)
            if prediction:
                predictions.append(prediction)
                
        return predictions
    
    def update_prediction_label(self, prediction_id: str, user_label: str) -> bool:
        """Update a prediction's user label."""
        prediction_key = self.PREDICTION_KEY.format(prediction_id=prediction_id)
        
        # Check if prediction exists
        if not self.redis_client.exists(prediction_key):
            return False
            
        # Update the label and mark as corrected
        now = datetime.utcnow().isoformat()
        self.redis_client.hset(prediction_key, mapping={
            "user_label": user_label,
            "is_corrected": "True",
            "updated_at": now
        })
        
        # Add back to persistence queue in case it was already persisted
        self.redis_client.lpush(self.PENDING_PERSISTENCE_KEY, prediction_id)
        
        logger.info(f"Updated prediction {prediction_id} with label: {user_label}")
        return True
    
    def get_pending_predictions(self, batch_size: int = 50) -> List[str]:
        """Get prediction IDs that need to be persisted to SQLite."""
        # Get batch of prediction IDs from the pending queue
        prediction_ids = []
        for _ in range(batch_size):
            prediction_id = self.redis_client.rpop(self.PENDING_PERSISTENCE_KEY)
            if not prediction_id:
                break
            prediction_ids.append(prediction_id)
        
        return prediction_ids
    
    def mark_as_persisted(self, prediction_id: str):
        """Mark a prediction as persisted to SQLite."""
        prediction_key = self.PREDICTION_KEY.format(prediction_id=prediction_id)
        self.redis_client.hset(prediction_key, "persisted", "True")
    
    def cleanup_old_predictions(self, days: int = 30):
        """Clean up old persisted predictions from Redis."""
        # This would be implemented to remove old predictions that have been persisted
        # and are older than the specified number of days
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get Redis store statistics."""
        total_predictions = len(self.redis_client.keys(self.PREDICTION_KEY.format(prediction_id="*")))
        pending_persistence = self.redis_client.llen(self.PENDING_PERSISTENCE_KEY)
        
        return {
            "total_predictions": total_predictions,
            "pending_persistence": pending_persistence,
            "redis_info": self.redis_client.info()
        } 