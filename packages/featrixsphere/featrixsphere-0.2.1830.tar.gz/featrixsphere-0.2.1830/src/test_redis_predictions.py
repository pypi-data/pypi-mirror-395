#!/usr/bin/env python3
"""
Test script for Redis-based prediction storage system.
"""

import time
import json
from redis_prediction_store import RedisPredictionStore

def test_redis_predictions():
    """Test the Redis prediction storage system."""
    print("🧪 Testing Redis Prediction Storage System")
    print("=" * 50)
    
    # Initialize Redis store
    store = RedisPredictionStore()
    
    # Test 1: Store predictions
    print("\n1. 📝 Testing prediction storage...")
    session_id = "test_session_123"
    
    predictions = []
    for i in range(3):
        input_data = {"feature1": f"value_{i}", "feature2": i * 10}
        prediction_result = {"class_A": 0.7 - i * 0.1, "class_B": 0.3 + i * 0.1}
        predicted_class = "class_A" if i < 2 else "class_B"
        confidence = max(prediction_result.values())
        
        prediction_id = store.store_prediction(
            session_id=session_id,
            input_data=input_data,
            prediction_result=prediction_result,
            predicted_class=predicted_class,
            confidence=confidence
        )
        
        predictions.append(prediction_id)
        print(f"   ✅ Stored prediction {prediction_id[:8]}... with class {predicted_class}")
    
    # Test 2: Retrieve predictions
    print("\n2. 🔍 Testing prediction retrieval...")
    for pred_id in predictions:
        prediction = store.get_prediction(pred_id)
        if prediction:
            print(f"   ✅ Retrieved {pred_id[:8]}... - Class: {prediction['predicted_class']}")
        else:
            print(f"   ❌ Failed to retrieve {pred_id[:8]}...")
    
    # Test 3: Get session predictions
    print("\n3. 📋 Testing session prediction listing...")
    session_predictions = store.get_session_predictions(session_id)
    print(f"   Found {len(session_predictions)} predictions for session {session_id}")
    
    # Test 4: Update prediction labels
    print("\n4. 🏷️  Testing label updates...")
    first_prediction_id = predictions[0]
    success = store.update_prediction_label(first_prediction_id, "corrected_class")
    if success:
        updated_pred = store.get_prediction(first_prediction_id)
        print(f"   ✅ Updated label: {updated_pred.get('user_label')}")
        print(f"   ✅ Is corrected: {updated_pred.get('is_corrected')}")
    else:
        print(f"   ❌ Failed to update label")
    
    # Test 5: Check pending persistence
    print("\n5. ⏳ Testing pending persistence queue...")
    pending = store.get_pending_predictions(5)
    print(f"   Found {len(pending)} predictions pending persistence")
    for pred_id in pending[:3]:  # Show first 3
        print(f"   - {pred_id[:8]}...")
    
    # Put them back for the persistence worker
    for pred_id in pending:
        store.redis_client.lpush(store.PENDING_PERSISTENCE_KEY, pred_id)
    
    # Test 6: Statistics
    print("\n6. 📊 Testing statistics...")
    stats = store.get_stats()
    print(f"   Total predictions: {stats['total_predictions']}")
    print(f"   Pending persistence: {stats['pending_persistence']}")
    
    print("\n✅ All tests completed successfully!")
    print(f"Session ID used: {session_id}")
    print("You can now test the persistence worker to see predictions moved to SQLite.")

if __name__ == "__main__":
    try:
        test_redis_predictions()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 