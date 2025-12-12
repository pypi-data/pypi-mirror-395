#!/usr/bin/env python3
"""
Redis Prediction CLI Tool

Command-line interface for managing the Redis-based prediction storage system.
"""

import typer
import json
from typing import Optional
from redis_prediction_store import RedisPredictionStore

app = typer.Typer(help="Redis Prediction System Management CLI")

def get_redis_store(redis_url: str = "redis://localhost:6379/0") -> RedisPredictionStore:
    """Get Redis store instance."""
    return RedisPredictionStore(redis_url)

@app.command()
def stats(redis_url: str = "redis://localhost:6379/0"):
    """Show Redis prediction store statistics."""
    store = get_redis_store(redis_url)
    stats = store.get_stats()
    
    typer.echo(f"📊 Redis Prediction Store Statistics")
    typer.echo(f"{'='*50}")
    typer.echo(f"Total predictions: {stats['total_predictions']}")
    typer.echo(f"Pending persistence: {stats['pending_persistence']}")
    typer.echo()
    typer.echo("Redis Info:")
    redis_info = stats['redis_info']
    typer.echo(f"  Memory used: {redis_info.get('used_memory_human', 'N/A')}")
    typer.echo(f"  Connected clients: {redis_info.get('connected_clients', 'N/A')}")
    typer.echo(f"  Uptime: {redis_info.get('uptime_in_seconds', 0)} seconds")

@app.command()
def get_prediction(prediction_id: str, redis_url: str = "redis://localhost:6379/0"):
    """Get a specific prediction by ID."""
    store = get_redis_store(redis_url)
    prediction = store.get_prediction(prediction_id)
    
    if not prediction:
        typer.echo(f"❌ Prediction {prediction_id} not found")
        raise typer.Exit(1)
    
    typer.echo(f"🔍 Prediction {prediction_id}")
    typer.echo(f"{'='*50}")
    typer.echo(json.dumps(prediction, indent=2, default=str))

@app.command()
def list_session_predictions(
    session_id: str, 
    limit: int = 10,
    redis_url: str = "redis://localhost:6379/0"
):
    """List predictions for a session."""
    store = get_redis_store(redis_url)
    predictions = store.get_session_predictions(session_id, limit)
    
    typer.echo(f"📋 Predictions for session {session_id} (limit: {limit})")
    typer.echo(f"{'='*50}")
    
    if not predictions:
        typer.echo("No predictions found")
        return
    
    for i, pred in enumerate(predictions, 1):
        created_at = pred.get('created_at', 'N/A')
        predicted_class = pred.get('predicted_class', 'N/A')
        confidence = pred.get('confidence', 'N/A')
        is_corrected = pred.get('is_corrected', False)
        user_label = pred.get('user_label', 'N/A')
        
        status = "✅ Corrected" if is_corrected else "⏳ Pending"
        
        typer.echo(f"{i:2d}. {pred['prediction_id'][:8]}... | {predicted_class} ({confidence}) | {status}")
        typer.echo(f"    Created: {created_at}")
        if is_corrected:
            typer.echo(f"    User label: {user_label}")
        typer.echo()

@app.command()
def update_label(
    prediction_id: str, 
    user_label: str,
    redis_url: str = "redis://localhost:6379/0"
):
    """Update a prediction's user label."""
    store = get_redis_store(redis_url)
    success = store.update_prediction_label(prediction_id, user_label)
    
    if success:
        typer.echo(f"✅ Updated prediction {prediction_id} with label: {user_label}")
    else:
        typer.echo(f"❌ Failed to update prediction {prediction_id}")
        raise typer.Exit(1)

@app.command()
def pending_persistence(redis_url: str = "redis://localhost:6379/0"):
    """Show predictions pending persistence to SQLite."""
    store = get_redis_store(redis_url)
    
    # Get a sample of pending predictions
    prediction_ids = store.get_pending_predictions(10)
    
    if not prediction_ids:
        typer.echo("✅ No predictions pending persistence")
        return
    
    typer.echo(f"⏳ Predictions pending persistence (showing first 10):")
    typer.echo(f"{'='*50}")
    
    for i, pred_id in enumerate(prediction_ids, 1):
        prediction = store.get_prediction(pred_id)
        if prediction:
            session_id = prediction.get('session_id', 'N/A')
            created_at = prediction.get('created_at', 'N/A')
            typer.echo(f"{i:2d}. {pred_id[:8]}... | Session: {session_id} | Created: {created_at}")
        else:
            typer.echo(f"{i:2d}. {pred_id[:8]}... | ❌ Not found in Redis")
    
    # Put them back in the queue
    for pred_id in prediction_ids:
        store.redis_client.lpush(store.PENDING_PERSISTENCE_KEY, pred_id)

@app.command()
def test_connection(redis_url: str = "redis://localhost:6379/0"):
    """Test Redis connection."""
    try:
        store = get_redis_store(redis_url)
        # Test with a simple ping
        result = store.redis_client.ping()
        if result:
            typer.echo("✅ Redis connection successful")
            typer.echo(f"   URL: {redis_url}")
        else:
            typer.echo("❌ Redis connection failed")
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Redis connection error: {e}")
        raise typer.Exit(1)

@app.command()
def clear_session(
    session_id: str,
    redis_url: str = "redis://localhost:6379/0",
    confirm: bool = typer.Option(False, "--confirm", help="Confirm deletion")
):
    """Clear all predictions for a session from Redis."""
    if not confirm:
        typer.echo("❌ This will delete all predictions for the session from Redis")
        typer.echo("Use --confirm to proceed")
        raise typer.Exit(1)
    
    store = get_redis_store(redis_url)
    
    # Get session predictions
    session_key = store.SESSION_PREDICTIONS_KEY.format(session_id=session_id)
    prediction_ids = store.redis_client.lrange(session_key, 0, -1)
    
    if not prediction_ids:
        typer.echo(f"No predictions found for session {session_id}")
        return
    
    # Delete individual predictions
    deleted_count = 0
    for pred_id in prediction_ids:
        pred_key = store.PREDICTION_KEY.format(prediction_id=pred_id)
        if store.redis_client.delete(pred_key):
            deleted_count += 1
    
    # Clear session prediction list
    store.redis_client.delete(session_key)
    
    typer.echo(f"✅ Deleted {deleted_count} predictions for session {session_id}")

if __name__ == "__main__":
    app() 