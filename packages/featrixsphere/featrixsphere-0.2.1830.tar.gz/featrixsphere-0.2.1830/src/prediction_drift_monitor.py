"""
Prediction Drift Monitor - Efficient KL divergence tracking between training data and live queries.

This module tracks distribution drift by:
1. Caching training data statistics at training time
2. Maintaining a rolling window of recent queries
3. Computing KL divergence periodically (not on every prediction)
4. Returning drift metrics with predictions
"""

import json
import logging
import numpy as np
import pandas as pd
import redis
from collections import defaultdict
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from scipy.stats import entropy

logger = logging.getLogger(__name__)


class PredictionDriftMonitor:
    """Monitor distribution drift between training data and live predictions."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0", window_size: int = 100):
        """
        Initialize drift monitor.
        
        Args:
            redis_url: Redis connection URL
            window_size: Number of recent queries to track (default: 100)
        """
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        self.window_size = window_size
        
        # Redis key patterns
        self.TRAINING_STATS_KEY = "training_stats:{session_id}"
        self.QUERY_WINDOW_KEY = "query_window:{session_id}"
        self.DRIFT_CACHE_KEY = "drift_cache:{session_id}"
        self.DRIFT_LAST_COMPUTED_KEY = "drift_last_computed:{session_id}"
    
    def store_training_stats(self, session_id: str, train_df: pd.DataFrame, 
                            ignore_cols: List[str] = None) -> Dict[str, Any]:
        """
        Compute and store training data distribution statistics.
        
        Called once after training to cache the training distribution.
        
        Args:
            session_id: Session ID
            train_df: Training dataframe
            ignore_cols: Columns to ignore
            
        Returns:
            Dictionary of training statistics
        """
        ignore_cols = ignore_cols or []
        training_stats = {
            "computed_at": datetime.utcnow().isoformat(),
            "n_rows": len(train_df),
            "columns": {}
        }
        
        for col in train_df.columns:
            if col in ignore_cols:
                continue
            
            col_stats = {"column": col}
            
            try:
                is_numeric = pd.api.types.is_numeric_dtype(train_df[col])
                
                if is_numeric:
                    # For numeric: store bins and histogram
                    vals = train_df[col].dropna()
                    if len(vals) > 0:
                        n_bins = min(20, len(vals.unique()))
                        bins = np.linspace(vals.min(), vals.max(), n_bins + 1)
                        hist, _ = np.histogram(vals, bins=bins)
                        
                        # Normalize to probabilities
                        epsilon = 1e-10
                        probs = (hist + epsilon) / (hist.sum() + epsilon * len(hist))
                        
                        col_stats["type"] = "numeric"
                        col_stats["bins"] = bins.tolist()
                        col_stats["probs"] = probs.tolist()
                        col_stats["min"] = float(vals.min())
                        col_stats["max"] = float(vals.max())
                        col_stats["n_bins"] = n_bins
                else:
                    # For categorical: store value counts
                    counts = train_df[col].value_counts(normalize=True, dropna=True)
                    
                    col_stats["type"] = "categorical"
                    col_stats["value_probs"] = {str(k): float(v) for k, v in counts.items()}
                    col_stats["unique_values"] = sorted([str(v) for v in counts.index])
                
                training_stats["columns"][col] = col_stats
                
            except Exception as e:
                logger.debug(f"Could not compute training stats for column '{col}': {e}")
                continue
        
        # Store in Redis
        key = self.TRAINING_STATS_KEY.format(session_id=session_id)
        self.redis_client.set(key, json.dumps(training_stats))
        
        logger.info(f"📊 Stored training stats for session {session_id}: {len(training_stats['columns'])} columns")
        return training_stats
    
    def add_query_to_window(self, session_id: str, query_record: Dict[str, Any]):
        """
        Add a query to the rolling window of recent queries.
        
        Args:
            session_id: Session ID
            query_record: Query data
        """
        key = self.QUERY_WINDOW_KEY.format(session_id=session_id)
        
        # Add to list (left push)
        self.redis_client.lpush(key, json.dumps(query_record))
        
        # Trim to window size (keep most recent N)
        self.redis_client.ltrim(key, 0, self.window_size - 1)
    
    def should_compute_drift(self, session_id: str, compute_every_n: int = 10) -> bool:
        """
        Check if drift should be recomputed.
        
        Computes drift every N queries to balance accuracy and performance.
        
        Args:
            session_id: Session ID
            compute_every_n: Recompute every N queries
            
        Returns:
            True if drift should be computed
        """
        window_key = self.QUERY_WINDOW_KEY.format(session_id=session_id)
        window_size = self.redis_client.llen(window_key)
        
        # Need at least 10 queries to compute meaningful drift
        if window_size < 10:
            return False
        
        # Check when last computed
        last_computed_key = self.DRIFT_LAST_COMPUTED_KEY.format(session_id=session_id)
        last_computed = self.redis_client.get(last_computed_key)
        
        if last_computed:
            try:
                last_size = int(last_computed)
                # Compute if we've added N new queries since last computation
                if window_size - last_size >= compute_every_n:
                    return True
            except (ValueError, TypeError):
                return True
        else:
            # Never computed
            return True
        
        return False
    
    def compute_drift(self, session_id: str, force: bool = False) -> Optional[Dict[str, Any]]:
        """
        Compute KL divergence between training data and recent queries.
        
        Args:
            session_id: Session ID
            force: Force recomputation even if cached
            
        Returns:
            Dictionary of drift metrics or None if not enough data
        """
        # Check cache first
        if not force:
            cache_key = self.DRIFT_CACHE_KEY.format(session_id=session_id)
            cached = self.redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        
        # Load training stats
        stats_key = self.TRAINING_STATS_KEY.format(session_id=session_id)
        training_stats_json = self.redis_client.get(stats_key)
        
        if not training_stats_json:
            logger.warning(f"No training stats found for session {session_id}")
            return None
        
        training_stats = json.loads(training_stats_json)
        
        # Load query window
        window_key = self.QUERY_WINDOW_KEY.format(session_id=session_id)
        query_jsons = self.redis_client.lrange(window_key, 0, self.window_size - 1)
        
        if len(query_jsons) < 10:
            logger.debug(f"Not enough queries ({len(query_jsons)}) to compute drift for session {session_id}")
            return None
        
        # Parse queries into dataframe
        queries = [json.loads(q) for q in query_jsons]
        query_df = pd.DataFrame(queries)
        
        # Compute KL divergence for each column
        drift_metrics = {
            "computed_at": datetime.utcnow().isoformat(),
            "n_queries": len(queries),
            "window_size": self.window_size,
            "n_training_rows": training_stats.get("n_rows", 0),
            "kl_divergences": {},
            "drift_detected": False,
            "drift_columns": []
        }
        
        kl_threshold = 0.1  # Same threshold as train/val split
        
        for col, col_stats in training_stats["columns"].items():
            if col not in query_df.columns:
                continue
            
            try:
                if col_stats["type"] == "numeric":
                    # Compute query histogram using training bins
                    query_vals = query_df[col].dropna()
                    if len(query_vals) == 0:
                        continue
                    
                    bins = np.array(col_stats["bins"])
                    train_probs = np.array(col_stats["probs"])
                    
                    query_hist, _ = np.histogram(query_vals, bins=bins)
                    epsilon = 1e-10
                    query_probs = (query_hist + epsilon) / (query_hist.sum() + epsilon * len(query_hist))
                    
                    # KL divergence: entropy(p, q) = sum(p * log(p / q))
                    kl = entropy(train_probs, query_probs)
                    
                elif col_stats["type"] == "categorical":
                    # Compare categorical distributions
                    train_value_probs = col_stats["value_probs"]
                    query_counts = query_df[col].value_counts(normalize=True, dropna=True)
                    
                    # Align values
                    all_values = sorted(set(train_value_probs.keys()) | set(str(v) for v in query_counts.index))
                    
                    epsilon = 1e-10
                    train_probs = np.array([train_value_probs.get(v, 0) + epsilon for v in all_values])
                    query_probs = np.array([query_counts.get(v, 0) + epsilon for v in all_values])
                    
                    # Renormalize
                    train_probs = train_probs / train_probs.sum()
                    query_probs = query_probs / query_probs.sum()
                    
                    # KL divergence: entropy(p, q) = sum(p * log(p / q))
                    kl = entropy(train_probs, query_probs)
                else:
                    continue
                
                drift_metrics["kl_divergences"][col] = float(kl)
                
                # Check if drifted
                if kl > kl_threshold:
                    drift_metrics["drift_detected"] = True
                    drift_metrics["drift_columns"].append(col)
                
            except Exception as e:
                logger.debug(f"Could not compute drift for column '{col}': {e}")
                continue
        
        # Compute aggregate drift metrics
        if drift_metrics["kl_divergences"]:
            kl_values = list(drift_metrics["kl_divergences"].values())
            drift_metrics["mean_kl"] = float(np.mean(kl_values))
            drift_metrics["max_kl"] = float(np.max(kl_values))
            drift_metrics["median_kl"] = float(np.median(kl_values))
        
        # Add reliability indicator
        if len(queries) < 30:
            drift_metrics["reliability"] = "low"
        elif len(queries) < 70:
            drift_metrics["reliability"] = "medium"
        else:
            drift_metrics["reliability"] = "high"
        
        # Cache result (expire after 5 minutes)
        cache_key = self.DRIFT_CACHE_KEY.format(session_id=session_id)
        self.redis_client.setex(cache_key, 300, json.dumps(drift_metrics))
        
        # Update last computed counter
        last_computed_key = self.DRIFT_LAST_COMPUTED_KEY.format(session_id=session_id)
        self.redis_client.set(last_computed_key, len(queries))
        
        if drift_metrics["drift_detected"]:
            logger.warning(f"⚠️  DRIFT DETECTED for session {session_id}: {drift_metrics['drift_columns']}")
        
        return drift_metrics
    
    def get_drift_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Get a summary of drift status (cached or None).
        
        Lightweight method that doesn't trigger computation.
        
        Args:
            session_id: Session ID
            
        Returns:
            Drift summary or None
        """
        cache_key = self.DRIFT_CACHE_KEY.format(session_id=session_id)
        cached = self.redis_client.get(cache_key)
        
        if cached:
            drift = json.loads(cached)
            # Return summary only
            return {
                "drift_detected": drift.get("drift_detected", False),
                "mean_kl": drift.get("mean_kl"),
                "max_kl": drift.get("max_kl"),
                "drift_columns": drift.get("drift_columns", []),
                "n_queries": drift.get("n_queries", 0),
                "window_size": drift.get("window_size", self.window_size),
                "n_training_rows": drift.get("n_training_rows", 0),
                "reliability": drift.get("reliability", "unknown"),
                "computed_at": drift.get("computed_at")
            }
        
        # No cached drift - check if we have any queries at all
        window_key = self.QUERY_WINDOW_KEY.format(session_id=session_id)
        n_queries = self.redis_client.llen(window_key)
        
        if n_queries < 10:
            return {
                "drift_detected": False,
                "n_queries": n_queries,
                "window_size": self.window_size,
                "reliability": "insufficient_data",
                "message": f"Need at least 10 queries to compute drift (have {n_queries})"
            }
        
        return None

