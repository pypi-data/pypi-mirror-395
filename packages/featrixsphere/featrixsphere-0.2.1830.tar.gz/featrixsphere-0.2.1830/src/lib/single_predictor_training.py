#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import asyncio
import copy
import glob
import inspect
import json
import logging
import os
import pickle
import socket
import sys
import time
import traceback

from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from featrix.neural.embedded_space import EmbeddingSpace

from pydantic import BaseModel, ConfigDict

try:
    from featrix.neural import device  # noqa: F401
except ModuleNotFoundError:
    p = Path(__file__).parent
    sys.path.insert(0, str(p))

    from featrix.neural import device  # noqa: F401

from featrix.neural.embedded_space import EmbeddingSpace
from featrix.neural.input_data_file import FeatrixInputDataFile
from featrix.neural.io_utils import load_embedded_space
from featrix.neural.single_predictor import FeatrixSinglePredictor
from featrix.neural.simple_mlp import SimpleMLP
from featrix.neural.device import device, set_device_cpu, reset_device

from featrix.neural.utils import ideal_batch_size, ideal_epochs_predictor 
from lib.job_manager import load_job, save_job, update_job_status, JobStatus
from featrix.neural.training_exceptions import TrainingFailureException
from featrix.neural.exceptions import FeatrixRestartTrainingException

import torch

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s")
logger = logging.getLogger(__name__)

def _log_gpu_memory(context: str = "", log_level=logging.INFO):
    """Quick GPU memory logging for tracing memory usage."""
    try:
        if not torch.cuda.is_available():
            return
        allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
        reserved = torch.cuda.memory_reserved() / (1024**3)  # GB
        max_allocated = torch.cuda.max_memory_allocated() / (1024**3)  # GB
        logger.log(log_level, f"📊 GPU MEMORY [{context}]: Allocated={allocated:.3f} GB, Reserved={reserved:.3f} GB, Peak={max_allocated:.3f} GB")
    except Exception as e:
        logger.debug(f"Could not log GPU memory: {e}")

# Import proper CV function (feature-flagged)
try:
    from lib.single_predictor_cv import train_with_proper_cv
    PROPER_CV_AVAILABLE = True
except ImportError:
    PROPER_CV_AVAILABLE = False
    logger.warning("⚠️  Proper CV module not available - using sequential CV")


def dump_cuda_memory_usage(context: str = ""):
    """
    Dump detailed CUDA memory usage information when OOM occurs.
    This helps debug what's holding VRAM.
    
    Args:
        context: Optional context string describing where the OOM occurred
    """
    try:
        if not torch.cuda.is_available():
            logger.warning(f"⚠️  CUDA not available - cannot dump memory usage")
            return
        
        logger.error("="*80)
        logger.error(f"🔍 CUDA MEMORY DUMP {f'({context})' if context else ''}")
        logger.error("="*80)
        
        # Get memory stats
        allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
        reserved = torch.cuda.memory_reserved() / (1024**3)  # GB
        max_allocated = torch.cuda.max_memory_allocated() / (1024**3)  # GB
        max_reserved = torch.cuda.max_memory_reserved() / (1024**3)  # GB
        
        logger.error(f"📊 Current Memory Usage:")
        logger.error(f"   Allocated: {allocated:.2f} GB")
        logger.error(f"   Reserved: {reserved:.2f} GB")
        logger.error(f"   Max Allocated (peak): {max_allocated:.2f} GB")
        logger.error(f"   Max Reserved (peak): {max_reserved:.2f} GB")
        
        # Get detailed memory summary
        try:
            memory_summary = torch.cuda.memory_summary(abbreviated=False)
            logger.error(f"\n📋 Detailed Memory Summary:")
            logger.error(memory_summary)
        except Exception as summary_err:
            logger.warning(f"⚠️  Could not get detailed memory summary: {summary_err}")
        
        # Get memory snapshot (shows what tensors are allocated)
        try:
            memory_snapshot = torch.cuda.memory_snapshot()
            if memory_snapshot:
                logger.error(f"\n📸 Memory Snapshot Analysis:")
                logger.error(f"   Total active allocations: {len(memory_snapshot)}")
                
                # Group allocations by size to identify patterns
                size_buckets = {
                    '<1MB': 0,
                    '1-10MB': 0,
                    '10-100MB': 0,
                    '100MB-1GB': 0,
                    '>1GB': 0
                }
                total_size_by_bucket = {
                    '<1MB': 0,
                    '1-10MB': 0,
                    '10-100MB': 0,
                    '100MB-1GB': 0,
                    '>1GB': 0
                }
                
                # Find largest allocations
                allocations_with_size = []
                for alloc in memory_snapshot:
                    if isinstance(alloc, dict):
                        total_size = alloc.get('total_size', 0)
                        active_size = alloc.get('active_size', 0)
                        size_mb = total_size / (1024**2)
                        
                        # Bucket by size
                        if size_mb < 1:
                            size_buckets['<1MB'] += 1
                            total_size_by_bucket['<1MB'] += total_size
                        elif size_mb < 10:
                            size_buckets['1-10MB'] += 1
                            total_size_by_bucket['1-10MB'] += total_size
                        elif size_mb < 100:
                            size_buckets['10-100MB'] += 1
                            total_size_by_bucket['10-100MB'] += total_size
                        elif size_mb < 1024:
                            size_buckets['100MB-1GB'] += 1
                            total_size_by_bucket['100MB-1GB'] += total_size
                        else:
                            size_buckets['>1GB'] += 1
                            total_size_by_bucket['>1GB'] += total_size
                        
                        # Track for largest allocations
                        if active_size > 0:
                            allocations_with_size.append((active_size, alloc))
                
                # Show size distribution
                logger.error(f"\n📊 Allocation Size Distribution:")
                for bucket, count in size_buckets.items():
                    if count > 0:
                        size_mb = total_size_by_bucket[bucket] / (1024**2)
                        logger.error(f"   {bucket:12s}: {count:6d} allocations, {size_mb:8.2f} MB total")
                
                # Show top 10 largest allocations
                if allocations_with_size:
                    allocations_with_size.sort(reverse=True, key=lambda x: x[0])
                    logger.error(f"\n🔝 Top 10 Largest Active Allocations:")
                    for i, (active_size, alloc) in enumerate(allocations_with_size[:10], 1):
                        size_mb = active_size / (1024**2)
                        total_size_mb = alloc.get('total_size', 0) / (1024**2)
                        segment_type = alloc.get('segment_type', 'unknown')
                        logger.error(f"   {i:2d}. {size_mb:8.2f} MB active / {total_size_mb:8.2f} MB total ({segment_type} pool)")
                        # Show frames if available
                        frames = alloc.get('frames', [])
                        if frames:
                            logger.error(f"       Stack trace:")
                            for frame in frames[:3]:  # First 3 frames
                                filename = frame.get('filename', 'unknown')
                                line = frame.get('line', 'unknown')
                                func = frame.get('function', 'unknown')
                                logger.error(f"         {filename}:{line} in {func}")
                
                # Show first 5 allocations with details (for debugging)
                logger.error(f"\n🔍 Sample Allocations (first 5):")
                for i, alloc in enumerate(memory_snapshot[:5], 1):
                    if isinstance(alloc, dict):
                        total_size_mb = alloc.get('total_size', 0) / (1024**2)
                        active_size_mb = alloc.get('active_size', 0) / (1024**2)
                        segment_type = alloc.get('segment_type', 'unknown')
                        blocks = alloc.get('blocks', [])
                        active_blocks = [b for b in blocks if b.get('state') == 'active_allocated']
                        logger.error(f"   {i}. {active_size_mb:.2f} MB / {total_size_mb:.2f} MB ({segment_type}, {len(active_blocks)} active blocks)")
                
                if len(memory_snapshot) > 5:
                    logger.error(f"   ... and {len(memory_snapshot) - 5} more allocations")
        except Exception as snapshot_err:
            logger.warning(f"⚠️  Could not get memory snapshot: {snapshot_err}")
        
        # Get nvidia-smi output for comparison
        try:
            import subprocess
            nvidia_smi = subprocess.run(
                ['nvidia-smi', '--query-gpu=memory.used,memory.total,utilization.gpu', '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if nvidia_smi.returncode == 0:
                logger.error(f"\n🖥️  nvidia-smi GPU Status:")
                for line in nvidia_smi.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 3:
                            mem_used = parts[0].strip()
                            mem_total = parts[1].strip()
                            gpu_util = parts[2].strip()
                            logger.error(f"   Memory: {mem_used} MB / {mem_total} MB, Utilization: {gpu_util}%")
        except Exception as smi_err:
            logger.warning(f"⚠️  Could not get nvidia-smi output: {smi_err}")
        
        logger.error("="*80)
        
    except ImportError:
        logger.warning(f"⚠️  PyTorch not available - cannot dump CUDA memory usage")
    except Exception as e:
        logger.warning(f"⚠️  Failed to dump CUDA memory usage: {e}")

# Suppress noisy loggers
for noisy in [
    "aiobotocore",
    "asyncio", 
    "botocore",
    "com",
    "fastapi",
    "dotenv",
    "concurrent",
    "aiohttp",
    "filelock",
    "fsspec",
    "httpcore",
    "httpx",
    "requests",
    "s3fs",
    "tornado",
    "twilio",
    "urllib3",
    "com.supertokens",
    "kombu.pidbox"
]:
    logging.getLogger(noisy).setLevel(logging.WARNING)


def _reconstruct_es_from_checkpoint(pth_file: Path, es_dir: Path) -> Optional['EmbeddingSpace']:
    """
    Reconstruct an EmbeddingSpace from a .pth checkpoint file.
    Returns the EmbeddingSpace if successful, None otherwise.
    """
    try:
        from featrix.neural.input_data_set import FeatrixInputDataSet
        from featrix.neural.input_data_file import FeatrixInputDataFile
        from lib.session_manager import load_session
        from config import config
        
        logger.info(f"🔍 Loading checkpoint from {pth_file}...")
        checkpoint = torch.load(str(pth_file), weights_only=False, map_location='cpu')
        
        if not isinstance(checkpoint, dict) or 'model' not in checkpoint:
            logger.warning(f"⚠️  Checkpoint file doesn't contain a 'model' key")
            return None
        
        logger.info(f"✅ Checkpoint loaded. Epoch: {checkpoint.get('epoch_idx', 'unknown')}")
        
        # Extract session_id from path: {output_dir}/{session_id}/train_es/{job_id}/training_state_BEST.pth
        path_parts = es_dir.parts
        session_id = None
        if 'train_es' in path_parts:
            train_es_idx = path_parts.index('train_es')
            if train_es_idx > 0:
                session_id = path_parts[train_es_idx - 1]
        
        if not session_id:
            logger.warning(f"⚠️  Could not extract session_id from path: {pth_file}")
            return None
        
        logger.info(f"🔍 Found session_id: {session_id}")
        
        # Load the session to get ES config
        logger.info(f"🔍 Loading session {session_id}...")
        session = load_session(session_id)
        
        if not session:
            logger.warning(f"⚠️  Session {session_id} not found")
            return None
        
        # Get input data path from session - try multiple locations
        input_data_path = None
        original_path = session.get('input_data') or session.get('input_filename') or session.get('input_file')
        
        if original_path:
            # Try the original path first
            input_data_path = Path(original_path)
            if input_data_path.exists():
                logger.info(f"✅ Found input data at original path: {input_data_path}")
            else:
                # Try relative to session directory
                session_dir = Path(config.session_dir) / session_id if hasattr(config, 'session_dir') else Path(f"/sphere/app/featrix_output/{session_id}")
                candidate = session_dir / Path(original_path).name
                if candidate.exists():
                    input_data_path = candidate
                    logger.info(f"✅ Found input data in session directory: {input_data_path}")
                else:
                    # Try in the train_es job directory (where training happened)
                    candidate = es_dir / Path(original_path).name
                    if candidate.exists():
                        input_data_path = candidate
                        logger.info(f"✅ Found input data in job directory: {input_data_path}")
                    else:
                        # Try data directory
                        if hasattr(config, 'data_dir'):
                            candidate = Path(config.data_dir) / Path(original_path).name
                            if candidate.exists():
                                input_data_path = candidate
                                logger.info(f"✅ Found input data in data directory: {input_data_path}")
        
        # If still not found, look for SQLite database in the train_es directory (created during training)
        if not input_data_path or not input_data_path.exists():
            sqlite_db = es_dir / "strings.sqlite3"
            if sqlite_db.exists():
                input_data_path = sqlite_db
                logger.info(f"✅ Found SQLite database in job directory: {input_data_path}")
            else:
                # Try session's sqlite_db field
                sqlite_db_path = session.get('sqlite_db')
                if sqlite_db_path:
                    sqlite_db = Path(sqlite_db_path)
                    if sqlite_db.exists():
                        input_data_path = sqlite_db
                        logger.info(f"✅ Found SQLite database from session: {input_data_path}")
        
        # If still not found, look for any CSV/parquet files in the train_es directory
        if not input_data_path or not input_data_path.exists():
            for pattern in ["*.csv", "*.parquet", "*.json", "*.jsonl"]:
                files = list(es_dir.glob(pattern))
                if files:
                    input_data_path = files[0]
                    logger.info(f"✅ Found data file in job directory: {input_data_path}")
                    break
        
        if not input_data_path or not input_data_path.exists():
            logger.warning(f"⚠️  Input data file not found. Tried:")
            logger.warning(f"   - Original path: {original_path}")
            logger.warning(f"   - Session directory: {session_dir if 'session_dir' in locals() else 'N/A'}")
            logger.warning(f"   - Job directory: {es_dir}")
            logger.warning(f"   - SQLite database: {sqlite_db if 'sqlite_db' in locals() else 'N/A'}")
            return None
        
        logger.info(f"🔍 Loading input data from {input_data_path}...")
        input_data_file = FeatrixInputDataFile(str(input_data_path))
        
        # Create train and val datasets
        train_df = input_data_file.df
        train_dataset = FeatrixInputDataSet(
            df=train_df,
            ignore_cols=[],
            limit_rows=None,
            encoder_overrides=session.get('column_overrides', {}),
        )
        val_dataset = FeatrixInputDataSet(
            df=train_df,  # Use same data for validation
            ignore_cols=[],
            limit_rows=None,
            encoder_overrides=session.get('column_overrides', {}),
        )
        
        # Get ES config from session
        logger.info(f"🔍 Creating EmbeddingSpace from session config...")
        es = EmbeddingSpace(
            train_input_data=train_dataset,
            val_input_data=val_dataset,
            output_debug_label=f"Hydrated from {pth_file.name}",
            n_epochs=session.get('n_epochs'),
            d_model=session.get('d_model'),
            encoder_config=None,  # Will be created from column_spec
            string_cache=session.get('strings_cache'),
            json_transformations=session.get('json_transformations', {}),
            version_info=session.get('version_info'),
            output_dir=str(es_dir),
            name=session.get('name'),
            required_child_es_mapping=session.get('required_child_es_mapping', {}),
            sqlite_db_path=session.get('sqlite_db'),
            user_metadata=session.get('user_metadata'),
        )
        
        # Load the checkpoint into the EmbeddingSpace
        logger.info(f"🔄 Loading checkpoint model into EmbeddingSpace...")
        es.encoder = checkpoint["model"]
        epoch_idx = checkpoint.get("epoch_idx", None)
        
        if epoch_idx is not None:
            logger.info(f"   Checkpoint epoch: {epoch_idx}")
            if not hasattr(es, 'training_info'):
                es.training_info = {}
            es.training_info['best_checkpoint_epoch'] = epoch_idx
            es.training_info['best_checkpoint_loaded'] = True
        
        return es
        
    except Exception as e:
        logger.warning(f"⚠️  Error reconstructing ES from checkpoint: {e}")
        logger.debug(traceback.format_exc())
        return None


class SimpleStatus:
    """Simple status object for progress tracking."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class LightSinglePredictorArgs(BaseModel):
    model_config = ConfigDict(protected_namespaces=())  # Allow fields starting with "model_" to avoid Pydantic warnings
    
    n_epochs: int = 0
    batch_size: int = 0 
    target_column: str  # Required
    target_column_type: str  # Required: "set" or "scalar"
    fine_tune: bool = True 
    learning_rate: Optional[float] = 0.001  # Increased from 0.0001 - models need higher LR to avoid dead gradients. None = use existing from resumed predictor
    resume_from_predictor: Optional[str] = None  # Path to existing predictor pickle to resume training from
    input_file: str = "./featrix_data/test.csv"
    job_id: Optional[str] = None
    job_queue: Optional[str] = None
    string_cache: Optional[str] = None
    embedding_space_path: str = "embedded_space.pickle"  # Path to embedding space
    positive_label: Optional[str] = None  # Positive label for binary classification - optional for backward compatibility
    class_imbalance: Optional[dict] = None  # Expected class ratios/counts from real world for sampled data (set codec only)
    use_class_weights: bool = True  # Enable class weighting by default for imbalanced data
    cost_false_positive: Optional[float] = None  # Cost of false positive (only for set columns). If not provided, defaults to 1.0.
    cost_false_negative: Optional[float] = None  # Cost of false negative (only for set columns). If not provided, defaults to negatives/positives ratio.
    session_id: Optional[str] = None  # Session ID for metadata tracking
    name: Optional[str] = None  # Name for the single predictor
    webhooks: Optional[Dict[str, str]] = None  # Webhook configuration (webhook_callback_secret, s3_backup_url, model_id_update_url)
    user_metadata: Optional[dict] = None  # User metadata - arbitrary dict for user identification (max 32KB when serialized)




def load_single_predictor(predictor_path: str):
    """
    Load a single predictor from disk.
    
    Supports:
    - .pickle files: Full pickled FeatrixSinglePredictor object
    - .pth files: PyTorch state_dict checkpoint (requires load_state() to restore)
    """
    if not os.path.exists(predictor_path):
        raise FileNotFoundError(f"Single predictor not found at: {predictor_path}")
    
    # Check file extension to determine loading method
    file_ext = os.path.splitext(predictor_path)[1].lower()
    
    if file_ext == '.pth':
        # This is a PyTorch state_dict checkpoint, not a full pickle
        # We need to load it with torch.load and then use load_state() if available
        logger = logging.getLogger(__name__)
        logger.info(f"📦 Loading PyTorch checkpoint (.pth file): {predictor_path}")
        logger.warning("⚠️  .pth files are state_dict checkpoints, not full predictor objects.")
        logger.warning("   You need to create a new predictor and call load_state() to restore weights.")
        logger.warning("   Or use a .pickle file for a full predictor object.")
        
        try:
            import torch
            checkpoint = torch.load(predictor_path, weights_only=False, map_location='cpu')
            logger.info(f"✅ Checkpoint loaded. Keys: {list(checkpoint.keys()) if isinstance(checkpoint, dict) else 'Not a dict'}")
            return checkpoint  # Return the state_dict, caller can use load_state() if needed
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"❌ Failed to load .pth checkpoint: {e}")
            raise
    
    # For .pickle files, use pickle loading
    with open(predictor_path, "rb") as f:
        try:
            # Try standard pickle.load first
            return pickle.load(f)
        except (AttributeError, pickle.UnpicklingError) as e:
            error_msg = str(e).lower()
            if "persistent_load" in error_msg or "persistent id" in error_msg:
                # If we get a persistent_load error, try with Unpickler
                f.seek(0)  # Reset file pointer
                unpickler = pickle.Unpickler(f)
                # Provide a handler for unknown persistent IDs
                # Protocol 0 requires ASCII strings, so return empty string instead of None
                def persistent_load(saved_id):
                    persistent_logger = logging.getLogger(__name__)
                    # Convert saved_id to string if it's not already
                    saved_id_str = str(saved_id) if saved_id is not None else "unknown"
                    persistent_logger.warning(f"⚠️  Encountered persistent_id {saved_id_str} in pickle file - returning empty string. This may cause issues if the ID is required.")
                    # Protocol 0 requires ASCII strings, not None
                    return ""
                unpickler.persistent_load = persistent_load
                return unpickler.load()
            raise


def write_single_predictor(fsp, local_path: str, model_id: str = None):
    """Save the trained single predictor to disk with metadata and model card."""
    assert os.path.exists(local_path)
    pickle_path = local_path + f"/single_predictor.pickle"
    
    with open(pickle_path, "wb") as f:
        pickle.dump(fsp, f)
    
    # Save model architecture metadata separately (backward compatibility)
    metadata_path = local_path + f"/model_metadata.json"
    try:
        # Count layers in the predictor
        layer_count = 0
        param_count = 0
        
        if hasattr(fsp, 'predictor'):
            for name, module in fsp.predictor.named_modules():
                if len(list(module.children())) == 0:  # Leaf modules only
                    layer_count += 1
            
            # Count parameters
            param_count = sum(p.numel() for p in fsp.predictor.parameters())
        
        metadata = {
            "name": fsp.name if hasattr(fsp, 'name') else None,
            "model_id": model_id,  # Store model_id in metadata
            "model_architecture": {
                "layer_count": layer_count,
                "parameter_count": param_count
            },
            "d_model": fsp.d_model if hasattr(fsp, 'd_model') else None,
            "target_column": fsp.target_col_name if hasattr(fsp, 'target_col_name') else None,
            "target_column_type": fsp.target_col_type if hasattr(fsp, 'target_col_type') else None,
        }
        
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Safe formatting - check type before using format specifier
        param_str = f"{param_count}" if isinstance(param_count, (int, float)) else str(param_count)
        logger.info(f"💾 Model metadata saved: {layer_count} layers, {param_str} parameters")
        if model_id:
            logger.info(f"   Model ID: {model_id}")
    except Exception as e:
        logger.warning(f"Failed to save model metadata: {e}")
    
    # Save comprehensive model card (similar to embedding space)
    model_card_path = local_path + f"/model_card.json"
    try:
        # Find best epoch (lowest validation loss)
        best_epoch_idx = 0
        best_val_loss = float('inf')
        if hasattr(fsp, 'training_info') and fsp.training_info:
            for i, entry in enumerate(fsp.training_info):
                val_loss = entry.get('validation_loss')
                if val_loss and val_loss < best_val_loss:
                    best_val_loss = val_loss
                    best_epoch_idx = entry.get('epoch_idx', i)
        
        # Create model card
        model_card = fsp._create_model_card_json(best_epoch_idx=best_epoch_idx)
        
        with open(model_card_path, "w") as f:
            json.dump(model_card, f, indent=2, default=str)
        
        logger.info(f"💾 Model card saved: {model_card_path}")
    except Exception as e:
        logger.warning(f"Failed to save model card: {e}")
        logger.debug(traceback.format_exc())
    
    return pickle_path


def create_predictor_mlp(d_in: int, d_hidden: int = 256, n_hidden_layers: int = 2, dropout: float = 0.3, use_batch_norm: bool = True, residual: bool = True):
    """
    Create a simple MLP predictor architecture.
    
    Args:
        d_in: Input dimension (embedding space dimension)
        d_hidden: Hidden layer dimension (default 256)
        n_hidden_layers: Number of hidden layers (0 = simple Linear layer)
        dropout: Dropout rate (default 0.3)
        use_batch_norm: Whether to use batch normalization (default True)
        residual: Whether to use residual connections (default True)
    """
    from featrix.neural.model_config import SimpleMLPConfig
    
    config = SimpleMLPConfig(
        d_in=d_in,
        d_out=d_hidden,  # This will be overridden by prep_for_training
        d_hidden=d_hidden,
        n_hidden_layers=n_hidden_layers,
        dropout=dropout,
        normalize=False,
        residual=residual,
        use_batch_norm=use_batch_norm,
    )
    
    return SimpleMLP(config)


def apply_predictor_filter(train_df):
    """
    Filter training data to rows where __featrix_train_predictor == True, then drop the column.
    
    Args:
        train_df: The training dataframe
        
    Returns:
        Filtered dataframe with the filter column removed
    """
    PREDICTOR_FILTER_COLUMN = "__featrix_train_predictor"
    
    logger.info("=" * 80)
    logger.info("🔍 SINGLE PREDICTOR: Checking for __featrix_train_predictor column")
    logger.info(f"📊 Initial data shape: {train_df.shape}")
    logger.info(f"📋 Columns present: {list(train_df.columns)}")
    
    if PREDICTOR_FILTER_COLUMN not in train_df.columns:
        logger.info(f"ℹ️  No {PREDICTOR_FILTER_COLUMN} column found - proceeding with all data as-is")
        logger.info("=" * 80)
        return train_df
    
    logger.info(f"✅ Found {PREDICTOR_FILTER_COLUMN} column in data")
    logger.info(f"📊 Column dtype: {train_df[PREDICTOR_FILTER_COLUMN].dtype}")
    logger.info(f"📊 Column value counts:\n{train_df[PREDICTOR_FILTER_COLUMN].value_counts()}")
    logger.info(f"📊 Column null count: {train_df[PREDICTOR_FILTER_COLUMN].isna().sum()}")
    
    # Filter to only TRUE rows
    rows_before = len(train_df)
    logger.info(f"🔍 Filtering to rows where {PREDICTOR_FILTER_COLUMN} == True")
    
    train_df = train_df[train_df[PREDICTOR_FILTER_COLUMN]]
    rows_after = len(train_df)
    rows_dropped = rows_before - rows_after
    
    logger.info(f"📊 Rows before filter: {rows_before}")
    logger.info(f"📊 Rows after filter: {rows_after}")
    logger.info(f"📊 Rows dropped: {rows_dropped}")
    logger.info(f"📊 Percentage kept: {(rows_after/rows_before*100):.1f}%")
    
    if rows_after == 0:
        raise ValueError(f"❌ After filtering on {PREDICTOR_FILTER_COLUMN}==True, no rows remain! Cannot train single predictor with zero training examples.")
    
    # Warn if filtering drops > 50% of data
    pct_kept = (rows_after/rows_before*100)
    if pct_kept < 50:
        logger.warning(f"⚠️  WARNING: {PREDICTOR_FILTER_COLUMN} filter dropped {100-pct_kept:.1f}% of data!")
        logger.warning(f"   Training on only {rows_after}/{rows_before} rows")
        logger.warning(f"   This may lead to poor performance - consider:")
        logger.warning(f"   1. Remove {PREDICTOR_FILTER_COLUMN} column to use all data")
        logger.warning(f"   2. Or verify this filtering is intentional")
    elif pct_kept < 80:
        logger.info(f"ℹ️  Note: Filtering kept {pct_kept:.1f}% of data ({rows_after} rows)")
    
    logger.info(f"🗑️  Single Predictor: Now dropping {PREDICTOR_FILTER_COLUMN} column")
    train_df = train_df.drop(columns=[PREDICTOR_FILTER_COLUMN])
    
    logger.info(f"✅ Column dropped successfully")
    logger.info(f"📊 Final data shape: {train_df.shape}")
    logger.info(f"📋 Remaining columns: {list(train_df.columns)}")
    logger.info("=" * 80)
    
    return train_df


def resolve_positive_label(user_label, target_column, train_df):
    """
    Validate and fuzzy-match a user-specified positive label to actual values in the dataframe.
    
    Handles type conversions and common boolean representations (True/False, 1/0, Yes/No, etc.)
    
    Args:
        user_label: The positive label specified by the user (any type)
        target_column: Name of the target column in the dataframe
        train_df: The training dataframe
        
    Returns:
        The matched value from the dataframe (with correct type), or the original user_label if no match found
    """
    if user_label is None:
        return None
    
    logger.info("=" * 80)
    logger.info("🔍 POSITIVE LABEL VALIDATION AND FUZZY MATCHING")
    logger.info(f"🏷️  User-specified positive_label: {user_label!r} (type: {type(user_label).__name__})")
    
    # Get unique values from target column
    unique_values = train_df[target_column].dropna().unique()
    logger.info(f"📊 Unique values in target column '{target_column}': {unique_values}")
    logger.info(f"📊 Value types: {[type(v).__name__ for v in unique_values]}")
    
    # Try direct match first
    for val in unique_values:
        if val == user_label:
            logger.info(f"✅ Direct match found: {val!r}")
            logger.info("=" * 80)
            return val
    
    # No direct match - try fuzzy matching
    logger.info("🔍 No direct match - attempting fuzzy matching...")
    
    def fuzzy_match(user_val, df_val):
        """Try to match user_val to df_val with type conversions."""
        user_str = str(user_val).lower().strip()
        df_str = str(df_val).lower().strip()
        
        if user_str == df_str:
            return True
        
        # Common boolean representations
        true_values = {'true', 't', 'yes', 'y', '1', '1.0'}
        false_values = {'false', 'f', 'no', 'n', '0', '0.0'}
        
        # If user specified a "truthy" value, match it to True/1/1.0/Yes
        if user_str in true_values:
            if df_str in true_values:
                return True
            if df_val is True or df_val == 1 or df_val == 1.0:
                return True
        
        # If user specified a "falsy" value, match it to False/0/0.0/No
        if user_str in false_values:
            if df_str in false_values:
                return True
            if df_val is False or df_val == 0 or df_val == 0.0:
                return True
        
        return False
    
    # Try fuzzy matching against each unique value
    for val in unique_values:
        if fuzzy_match(user_label, val):
            logger.info(f"✅ Fuzzy match found: user '{user_label!r}' → dataframe '{val!r}'")
            logger.info(f"✅ Positive label resolved: '{user_label!r}' → '{val!r}' (type: {type(val).__name__})")
            logger.info("=" * 80)
            return val
    
    # No match found
    logger.warning(f"⚠️  Could not match positive_label '{user_label!r}' to any value in target column")
    logger.warning(f"⚠️  Available values: {list(unique_values)}")
    logger.warning(f"⚠️  Proceeding with original value, but metrics may be incorrect")
    logger.info("=" * 80)
    return user_label


def get_predictor_detailed_info(client, session_id, target_column):
    """
    Get detailed information about a trained predictor from the FeatrixSphere API.
    
    Args:
        client: FeatrixSphere client
        session_id: Session ID
        target_column: Target column of the predictor
        
    Returns:
        dict: Detailed predictor information including model stats
    """
    try:
        # Get session info to find predictor details
        session_info = client._get_json(f"/compute/session/{session_id}")
        
        predictor_info = {}
        
        # Extract embedding space ID
        predictor_info['es_id'] = session_info.get('embedding_space_id') or session_info.get('es_id')
        
        # Find the specific predictor for this target column
        predictors = session_info.get('predictors', {})
        predictor_data = None
        predictor_id = None
        
        for pred_id, pred in predictors.items():
            if isinstance(pred, dict) and pred.get('target_column') == target_column:
                predictor_data = pred
                predictor_id = pred_id
                break
        
        if predictor_data:
            predictor_info['predictor_id'] = predictor_id
            predictor_info['status'] = predictor_data.get('status')
            predictor_info['trained_at'] = predictor_data.get('trained_at')
            
            # Extract model architecture info
            model_info = predictor_data.get('model_info', {})
            predictor_info['parameter_count'] = model_info.get('parameter_count') or model_info.get('num_parameters')
            predictor_info['layer_count'] = model_info.get('layer_count') or model_info.get('num_layers')
            
            # Extract training statistics
            training_stats = predictor_data.get('training_stats', {}) or predictor_data.get('stats', {})
            predictor_info['best_epoch'] = training_stats.get('best_epoch')
            predictor_info['best_accuracy'] = training_stats.get('best_accuracy')
            predictor_info['best_loss'] = training_stats.get('best_loss')
            predictor_info['val_loss'] = training_stats.get('val_loss') or training_stats.get('validation_loss')
            predictor_info['val_accuracy'] = training_stats.get('val_accuracy') or training_stats.get('validation_accuracy')
            predictor_info['final_epoch'] = training_stats.get('final_epoch') or training_stats.get('epochs_trained')
            predictor_info['training_time_seconds'] = training_stats.get('training_time') or training_stats.get('elapsed_seconds')
        
        # Get column types from the session
        column_info = session_info.get('columns', {}) or session_info.get('column_types', {})
        if column_info:
            predictor_info['column_types'] = column_info
        
        # Get encoding information
        encoding_info = session_info.get('encoding', {}) or session_info.get('encodings', {})
        if encoding_info:
            predictor_info['column_encodings'] = encoding_info
            
        # Get training host/cluster info
        predictor_info['training_cluster'] = session_info.get('cluster') or session_info.get('compute_cluster')
        predictor_info['training_host'] = session_info.get('host') or session_info.get('compute_host')
        
        return predictor_info
        
    except Exception as e:
        logger.warning(f"⚠️ Failed to get detailed predictor info: {e}")
        return {}


def save_predictor_metadata(
    session_id,
    target_column,
    target_column_type="set",
    epochs=50,
    training_response=None,
    csv_file=None,
    client=None,
    training_start_time=None,
    fsp=None
):
    """
    Save comprehensive predictor training metadata to a JSON file for future reference.
    
    This captures all critical information about the trained model including:
    - Model architecture (parameter count, layer count)
    - Training statistics (best stats, val loss, etc.)
    - Column types and encodings
    - Training environment details
    
    Args:
        session_id: FeatrixSphere session ID
        target_column: Target column being predicted
        target_column_type: Type of target ("set" or "numeric")
        epochs: Number of training epochs requested
        training_response: Initial training API response
        csv_file: Source CSV file path
        client: FeatrixSphere client (for fetching detailed stats)
        training_start_time: When training started (timestamp)
        fsp: FeatrixSinglePredictor instance (for local model info)
        
    Returns:
        str: Path to saved metadata file
    """
    try:
        # Basic metadata
        metadata = {
            "target_column": target_column,
            "session_id": session_id,
            "target_column_type": target_column_type,
            "epochs_requested": epochs,
            "started_at": training_start_time or datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat(),
            "training_response": training_response,
            "source_csv": csv_file,
            "status": "completed",
            "metadata_version": "2.0"
        }
        
        # Add training host information
        try:
            metadata['training_client_host'] = socket.gethostname()
            metadata['training_client_fqdn'] = socket.getfqdn()
        except Exception:
            pass
        
        # Calculate training time if we have start time
        if training_start_time:
            try:
                start_dt = datetime.fromisoformat(training_start_time) if isinstance(training_start_time, str) else training_start_time
                end_dt = datetime.now()
                metadata['training_duration_seconds'] = (end_dt - start_dt).total_seconds()
            except Exception:
                pass
        
        # Get local model info from FeatrixSinglePredictor if available
        if fsp:
            try:
                # Add name if available
                if hasattr(fsp, 'name') and fsp.name:
                    metadata['name'] = fsp.name
                
                # Count layers and parameters
                layer_count = 0
                param_count = 0
                
                if hasattr(fsp, 'predictor'):
                    for name, module in fsp.predictor.named_modules():
                        if len(list(module.children())) == 0:  # Leaf modules only
                            layer_count += 1
                    
                    # Count parameters
                    param_count = sum(p.numel() for p in fsp.predictor.parameters())
                
                metadata['parameter_count'] = param_count
                metadata['layer_count'] = layer_count
                metadata['d_model'] = fsp.d_model if hasattr(fsp, 'd_model') else None
                
                # Get training metrics if available
                if hasattr(fsp, 'training_info') and fsp.training_info:
                    metadata['training_info'] = fsp.training_info
                if hasattr(fsp, 'training_metrics') and fsp.training_metrics:
                    metadata['final_metrics'] = fsp.training_metrics
                    
            except Exception as e:
                logger.warning(f"⚠️ Could not extract local model info: {e}")
        
        # Get detailed predictor information from API if client provided
        if client:
            try:
                detailed_info = get_predictor_detailed_info(client, session_id, target_column)
                # Merge API info (don't override local info if it exists)
                for key, value in detailed_info.items():
                    if key not in metadata or metadata[key] is None:
                        metadata[key] = value
            except Exception as e:
                logger.warning(f"⚠️ Could not fetch detailed predictor info from API: {e}")
        
        # Save to local metadata directory
        metadata_dir = Path("predictor_metadata")
        metadata_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metadata_file = metadata_dir / f"{session_id}_{target_column}_{timestamp}.json"
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        logger.info(f"📝 Metadata saved to: {metadata_file}")
        logger.info(f"   - Target column: {target_column}")
        logger.info(f"   - Session ID: {session_id}")
        if 'es_id' in metadata:
            logger.info(f"   - Embedding space ID: {metadata['es_id']}")
        if 'parameter_count' in metadata:
            param_count = metadata['parameter_count']
            param_str = f"{param_count}" if isinstance(param_count, (int, float)) else str(param_count)
            logger.info(f"   - Parameter count: {param_str}")
        if 'layer_count' in metadata:
            logger.info(f"   - Layer count: {metadata['layer_count']}")
        if 'val_loss' in metadata:
            val_loss = metadata['val_loss']
            val_loss_str = f"{val_loss}" if isinstance(val_loss, (int, float)) else str(val_loss)
            logger.info(f"   - Validation loss: {val_loss_str}")
        if 'training_duration_seconds' in metadata:
            duration = metadata['training_duration_seconds']
            duration_str = f"{duration}" if isinstance(duration, (int, float)) else str(duration)
            logger.info(f"   - Training time: {duration_str}s")
        
        return str(metadata_file)
    except Exception as e:
        logger.error(f"⚠️ Failed to save metadata: {e}")
        traceback.print_exc()
        return None


def train_single_predictor(args: LightSinglePredictorArgs):
    # Print version info at start of training
    try:
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # Add src to path
        from version import print_version_banner, get_version
        print_version_banner("Featrix Sphere Single Predictor Training")
        
        # Explicitly log version to syslog
        version_info = get_version()
        logger.info(f"📦 Single Predictor Training Version: {version_info.semantic_version} (git: {version_info.git_hash[:8] if version_info.git_hash else 'unknown'})")
        logger.info(f"📅 Version Date: {version_info.git_date or 'unknown'}")
    except Exception as e:
        logger.warning(f"⚠️ Could not load version info: {e}")
        print(f"⚠️ Could not load version info: {e}")
    
    # Capture training start time for metadata
    training_start_time = datetime.now()
    
    print(f"🎯 Training single predictor: {args.target_column} ({args.target_column_type})")
    print(f"📊 Args: {args.model_dump_json(indent=2)}")
    
    # Log training start event
    session_id = args.session_id
    if session_id:
        try:
            from event_log import log_training_event
            log_training_event(
                session_id=session_id,
                event_name="training_started",
                predictor_id=args.job_id,
                additional_info={
                    "target_column": args.target_column,
                    "target_column_type": args.target_column_type,
                    "epochs": args.n_epochs,
                    "batch_size": args.batch_size
                }
            )
        except Exception as e:
            logger.debug(f"Failed to log training start event: {e}")

    # DON'T CLEAR HANDLERS - it breaks all logging!
    # logging.getLogger().handlers.clear()
    
    print("@@@@ Starting Single Predictor Training! @@@@")
    
    # Validate required arguments
    if not args.target_column:
        raise ValueError("target_column is required")
    if args.target_column_type not in ["set", "scalar"]:
        raise ValueError("target_column_type must be 'set' or 'scalar'")
    
    logger.info("="*100)
    logger.info("🚀🚀🚀 train_single_predictor() FUNCTION ENTRY POINT")
    logger.info(f"🚀 Args: target_column={args.target_column}, target_column_type={args.target_column_type}")
    logger.info(f"🚀 This file: {__file__}")
    logger.info("="*100)
    
    # Post to Slack that Single Predictor training is starting
    try:
        from pathlib import Path as PathLib
        sys.path.insert(0, str(PathLib(__file__).parent.parent))
        from slack import send_slack_message
        
        slack_msg = f"🎯 **Single Predictor Training Started**\n"
        slack_msg += f"Target Column: {args.target_column}\n"
        slack_msg += f"Target Type: {args.target_column_type}\n"
        slack_msg += f"Session ID: {args.session_id}\n"
        slack_msg += f"Job ID: {args.job_id}\n"
        slack_msg += f"Epochs: {getattr(args, 'n_epochs', getattr(args, 'epochs', 0))}\n"
        slack_msg += f"Batch Size: {getattr(args, 'batch_size', 0)}\n"
        slack_msg += f"Learning Rate: {getattr(args, 'learning_rate', 'N/A')}\n"
        slack_msg += f"Started: {training_start_time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        send_slack_message(slack_msg, throttle=False)  # Critical - don't throttle
        logger.info("✅ Slack notification sent for Single Predictor training start")
    except Exception as slack_error:
        logger.warning(f"Failed to send Slack notification: {slack_error}", exc_info=True)
    
    logger.info(f"Training single predictor for target column: {args.target_column} (type: {args.target_column_type})")
    
    # Enable GPU training for single predictors
    use_gpu = torch.cuda.is_available()
    if use_gpu:
        gpu_memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        logger.info(f"🎮 GPU available: {gpu_memory_gb:.1f} GB - will use GPU for training")
    else:
        logger.info(f"🖥️  No GPU available - will use CPU for training")
    
    # Load the pre-trained embedding space
    logger.info(f"🔍 Step 1: Checking if embedding space exists at {args.embedding_space_path}")
    if not os.path.exists(args.embedding_space_path):
        raise FileNotFoundError(f"{args.embedding_space_path} not found. Train an embedding space first.")
    
    logger.info(f"🔍 Step 2: Loading pre-trained embedding space from {args.embedding_space_path}...")
    _log_gpu_memory("BEFORE LOAD_EMBEDDED_SPACE")
    # Load embedding space - will use GPU if available (now that we fixed double-loading bug)
    logger.info(f"🔧 Loading embedding space (will use GPU if available)")
    es = load_embedded_space(args.embedding_space_path)
    _log_gpu_memory("AFTER LOAD_EMBEDDED_SPACE")
    logger.info(f"🔍 Step 2 DONE: Embedding space loaded, type={type(es)}")
    
    # Validate that es is an EmbeddingSpace object
    from featrix.neural.embedded_space import EmbeddingSpace
    if not isinstance(es, EmbeddingSpace):
        raise TypeError(f"Expected EmbeddingSpace object, got {type(es)}. The file may be a checkpoint dict, not a full embedding space.")
    
    # Move encoder to GPU if available
    _log_gpu_memory("BEFORE CHECKING ENCODER DEVICE")
    if hasattr(es, 'encoder') and es.encoder is not None:
        if list(es.encoder.parameters()):
            encoder_device = next(es.encoder.parameters()).device
            if use_gpu and encoder_device.type != 'cuda':
                logger.info(f"🔄 Moving encoder to GPU for faster training...")
                es.encoder = es.encoder.cuda()
                torch.cuda.empty_cache()
                _log_gpu_memory("AFTER MOVING ENCODER TO GPU")
            logger.info(f"✅ Encoder device: {next(es.encoder.parameters()).device}")
        
        # Move codecs to GPU if available
        if use_gpu and hasattr(es, 'col_codecs') and es.col_codecs:
            codecs_moved = 0
            for col_name, codec in es.col_codecs.items():
                try:
                    if hasattr(codec, 'cuda'):
                        codec.cuda()
                        codecs_moved += 1
                except Exception as e:
                    logger.debug(f"   Could not move {col_name} codec to GPU: {e}")
            if codecs_moved > 0:
                logger.info(f"   ✅ Moved {codecs_moved} codecs to GPU")
                torch.cuda.empty_cache()
        
        # Clear training history/metadata from GPU memory (not needed for inference/training)
        # These are just metadata dicts, but clearing them ensures no accidental GPU tensors
        if hasattr(es, 'training_info') and es.training_info:
            # training_info is just metadata, but check for any GPU tensors
            try:
                # Remove any large lists that might have been accidentally stored
                for key in ['val_losses', 'train_losses', 'gradient_norms', 'learning_rates']:
                    if key in es.training_info:
                        # These are just lists of floats, not GPU tensors, but clear if large
                        if isinstance(es.training_info[key], list) and len(es.training_info[key]) > 1000:
                            logger.debug(f"   Trimming large {key} list ({len(es.training_info[key])} entries)")
                            es.training_info[key] = es.training_info[key][-100:]  # Keep last 100
            except Exception as e:
                logger.debug(f"   Could not trim training_info: {e}")
        
        # Clear training timeline if it's large (just metadata, not needed for training)
        if hasattr(es, '_training_timeline') and isinstance(es._training_timeline, list):
            if len(es._training_timeline) > 1000:
                logger.debug(f"   Trimming large training timeline ({len(es._training_timeline)} entries)")
                es._training_timeline = es._training_timeline[-100:]  # Keep last 100 entries
    
    # CRITICAL: Clear train_input_data and val_input_data - we don't need the ES's original training data
    # We only need the encoder and codecs to encode the NEW training data for the predictor
    if hasattr(es, 'train_input_data') and es.train_input_data is not None:
        logger.info(f"🗑️  Clearing ES train_input_data (not needed for predictor training - only need encoder/codecs)")
        # Check size before clearing
        try:
            if hasattr(es.train_input_data, 'df'):
                df_size = len(es.train_input_data.df) if hasattr(es.train_input_data.df, '__len__') else 'unknown'
                logger.info(f"   train_input_data had {df_size} rows")
        except Exception:
            pass
        es.train_input_data = None
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    if hasattr(es, 'val_input_data') and es.val_input_data is not None:
        logger.info(f"🗑️  Clearing ES val_input_data (not needed for predictor training - only need encoder/codecs)")
        # Check size before clearing
        try:
            if hasattr(es.val_input_data, 'df'):
                df_size = len(es.val_input_data.df) if hasattr(es.val_input_data.df, '__len__') else 'unknown'
                logger.info(f"   val_input_data had {df_size} rows")
        except Exception:
            pass
        es.val_input_data = None
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    # Also clear train_dataset and val_dataset if they exist
    if hasattr(es, 'train_dataset') and es.train_dataset is not None:
        logger.info(f"🗑️  Clearing ES train_dataset (not needed for predictor training)")
        es.train_dataset = None
    
    if hasattr(es, 'val_dataset') and es.val_dataset is not None:
        logger.info(f"🗑️  Clearing ES val_dataset (not needed for predictor training)")
        es.val_dataset = None
    
    _log_gpu_memory("AFTER CLEARING ES TRAINING DATA")
    logger.info(f"✅ Cleared ES training data - only encoder and codecs remain (needed for encoding)")
    
    # FIX: Update embedding space's output_dir to current working directory
    # The ES was trained in a different job directory, so its output_dir points to the wrong place
    current_dir = os.getcwd()
    if hasattr(es, 'output_dir'):
        old_output_dir = es.output_dir
        es.output_dir = current_dir
        logger.info(f"📂 Updated ES output_dir: {old_output_dir} → {current_dir}")
    else:
        es.output_dir = current_dir
        logger.info(f"📂 Set ES output_dir to: {current_dir}")
    
    # Load the training data
    logger.info(f"🔍 Step 3: Loading data from {args.input_file}...")
    input_data_file = FeatrixInputDataFile(args.input_file)
    train_df = input_data_file.df
    logger.info(f"🔍 Step 3 DONE: Data file loaded: {len(train_df)} rows × {len(train_df.columns)} columns")
    
    # Log columns found immediately after loading for debugging
    logger.info(f"📋 Columns found after CSV reading ({len(train_df.columns)} total): {list(train_df.columns)[:50]}{'...' if len(train_df.columns) > 50 else ''}")
    if len(train_df.columns) > 50:
        logger.info(f"   ... and {len(train_df.columns) - 50} more columns")
    
    # Handle __featrix_train_predictor column for single predictor training
    train_df = apply_predictor_filter(train_df)
    
    # Create a proper FeatrixInputDataSet to get detector results
    logger.info("=" * 80)
    logger.info("📊 CREATING INPUT DATA SET FOR DETECTION ANALYSIS")
    logger.info("=" * 80)
    from featrix.neural.input_data_set import FeatrixInputDataSet
    
    # Create dataset with full detection (not standup_only) to get detector results
    training_input_dataset = FeatrixInputDataSet(
        df=train_df,
        ignore_cols=[],
        limit_rows=None,
        encoder_overrides=None,
        project_row_meta_data=None,
        standup_only=False,  # Full detection so we can print detector results
    )
    
    # Print detector results for the training data
    logger.info("=" * 80)
    logger.info("📊 PRINTING DETECTOR RESULTS FOR SINGLE PREDICTOR TRAINING DATA")
    logger.info("=" * 80)
    training_input_dataset._printDetectorResults("SINGLE PREDICTOR TRAINING DATA")
    logger.info("=" * 80)
    
    # DISTRIBUTION SHIFT DETECTION: Compare SP training data to ES training data
    logger.info("")
    logger.info("=" * 80)
    logger.info("🔍 DISTRIBUTION SHIFT DETECTION")
    logger.info("=" * 80)
    logger.info("Comparing single predictor training data to base embedding space...")
    logger.info("")
    try:
        from lib.distribution_shift_detector import detect_distribution_shift
        shift_summary = detect_distribution_shift(
            embedding_space=es,
            sp_train_df=train_df,
            target_column=args.target_column
        )
        
        # Log summary stats
        if shift_summary.get('has_critical_issues'):
            logger.error("🚨 CRITICAL DISTRIBUTION ISSUES DETECTED - training may fail or produce poor results!")
        elif shift_summary.get('warning_columns', 0) > 0:
            logger.warning(f"⚠️  {shift_summary['warning_columns']} columns have distribution warnings")
        else:
            logger.info("✅ No significant distribution shifts detected")
    except Exception as e:
        logger.warning(f"⚠️  Distribution shift detection failed: {e}")
        import traceback
        traceback.print_exc()
    logger.info("=" * 80)
    logger.info("")
    
    # Print label distribution early (before training starts)
    logger.info("=" * 80)
    logger.info("📊 LABEL DISTRIBUTION FOR SINGLE PREDICTOR TRAINING")
    logger.info("=" * 80)
    if args.target_column in train_df.columns:
        label_counts = train_df[args.target_column].value_counts()
        total_rows = len(train_df)
        logger.info(f"📈 TARGET COLUMN: '{args.target_column}'")
        logger.info(f"📈 Total rows: {total_rows:,}")
        logger.info(f"📈 Label distribution:")
        for label, count in label_counts.items():
            percentage = (count / total_rows) * 100 if total_rows > 0 else 0.0
            logger.info(f"   '{label}': {count:,} samples ({percentage:.2f}%)")
        
        # Show null/missing values
        null_count = train_df[args.target_column].isnull().sum()
        if null_count > 0:
            null_pct = (null_count / total_rows) * 100 if total_rows > 0 else 0.0
            logger.warning(f"   ⚠️  NULL/MISSING: {null_count:,} samples ({null_pct:.2f}%)")
        
        # Show unique values count
        unique_count = train_df[args.target_column].nunique()
        logger.info(f"   Unique values: {unique_count}")
    else:
        logger.error(f"❌ Target column '{args.target_column}' not found in data!")
        logger.error(f"   Available columns: {list(train_df.columns)}")
    logger.info("=" * 80)
    
    # Log fill rates for all columns when single predictor is using its own dataset
    # (This is always the case for single predictor training - it loads from args.input_file)
    logger.info("=" * 80)
    logger.info("📊 COLUMN FILL RATES (Single Predictor Training Dataset)")
    logger.info("=" * 80)
    total_rows = len(train_df)
    for col_name in train_df.columns:
        col_data = train_df[col_name]
        non_null_count = col_data.notna().sum()
        null_count = col_data.isnull().sum()
        fill_rate = (non_null_count / total_rows * 100) if total_rows > 0 else 0.0
        logger.info(f"   {col_name:40s}: {fill_rate:6.2f}% ({non_null_count:,}/{total_rows:,} non-null)")
    logger.info("=" * 80)
    
    # Validate that target column exists (with fuzzy matching for special characters)
    logger.info(f"🔍 Step 4: Validating target column '{args.target_column}' exists")
    if args.target_column not in train_df.columns:
        # Try fuzzy matching by removing special characters
        # This handles cases like "Love's" vs "Loves"
        import re
        def normalize_column_name(name):
            """Remove special characters except underscores for matching"""
            return re.sub(r"[^\w]", "", name)
        
        normalized_target = normalize_column_name(args.target_column)
        matches = []
        for col in train_df.columns:
            if normalize_column_name(col) == normalized_target:
                matches.append(col)
        
        if len(matches) == 1:
            actual_column = matches[0]
            logger.info(f"✅ Fuzzy match found: '{args.target_column}' → '{actual_column}'")
            logger.info(f"   (Normalized matching: special characters ignored)")
            args.target_column = actual_column
        elif len(matches) > 1:
            raise ValueError(f"Target column '{args.target_column}' not found. Multiple fuzzy matches found: {matches}. Please specify exact column name.")
        else:
            error_msg = (
                f"❌ CRITICAL ERROR: Target column '{args.target_column}' NOT FOUND in data!\n"
                f"   Data has {len(train_df)} rows and {len(train_df.columns)} columns\n"
                f"   Available columns: {list(train_df.columns)}\n"
                f"   This indicates the target column was lost during CSV reading.\n"
                f"   Check CSV reading logs (TRACE CSV messages) to see what columns were actually loaded.\n"
                f"   The CSV file may have been parsed incorrectly (wrong quotechar, delimiter issues, etc.)"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    logger.info(f"🔍 Step 4 DONE: Data loaded: {len(train_df)} rows, {len(train_df.columns)} columns")
    
    # CRITICAL: Prime string cache with strings from the new training file
    # The embedding space was trained on a different file, so we need to populate
    # the cache with strings from this new training file before training starts
    logger.info("🔍 Step 5: Priming string cache with training data strings...")
    string_cache_path = es.string_cache if hasattr(es, 'string_cache') and es.string_cache else None
    if string_cache_path:
        logger.info(f"   Using string cache from embedding space: {string_cache_path}")
        try:
            from featrix.neural.input_data_set import FeatrixInputDataSet
            # Create dataset to detect string columns and populate cache
            training_dataset = FeatrixInputDataSet(
                df=train_df,
                ignore_cols=[],
                limit_rows=None,  # Use all rows to populate cache completely
                encoder_overrides=None,
                project_row_meta_data=None,
                standup_only=True,  # Skip detection/enrichment, just need column types
            )
            # Prime the cache with all strings from training data
            logger.info(f"🔥 Priming string cache with {len(train_df)} rows of training data...")
            training_dataset.create_string_caches(string_cache_path)
            logger.info(f"✅ String cache primed successfully")
        except Exception as cache_err:
            logger.warning(f"⚠️  Failed to prime string cache: {cache_err}")
            logger.warning(f"   Training will continue but may encounter cache misses")
    else:
        logger.warning(f"⚠️  No string cache path found in embedding space - skipping cache priming")
    
    # Handle positive_label fuzzy matching and type conversion
    args.positive_label = resolve_positive_label(args.positive_label, args.target_column, train_df)
    
    # Progress callback for job system integration
    # Track last epoch posted to avoid duplicate posts
    last_posted_epoch = [-1]  # Use list to allow modification in closure
    
    def progress_callback(progress_dict):
        try:
            # Import here to avoid circular imports
            from training_monitor import post_training_progress
            
            # LOG TRAINING PROGRESS (like ES training does)
            epoch_idx = progress_dict.get('epoch_idx', 0)
            current_loss = progress_dict.get('current_loss', 0)
            validation_loss = progress_dict.get('validation_loss', 0)
            lr_raw = progress_dict.get('lr', 0)
            progress = progress_dict.get('progress_counter', 0)
            progress_max = progress_dict.get('max_progress', 1)
            
            # Handle learning rate - might be a list from scheduler
            if isinstance(lr_raw, list) and lr_raw:
                lr = lr_raw[0]  # Take first element if it's a list
            else:
                lr = lr_raw if lr_raw else 0
            
            # Log training progress every epoch like ES training
            # Note: progress_max is total BATCHES (epochs × batches_per_epoch), not epochs
            # So progress/progress_max gives batch-level progress, not epoch-level progress
            epoch_total = progress_dict.get('epoch_total', 0)
            # Safe formatting - check types before using format specifiers
            loss_str = f"{current_loss}" if isinstance(current_loss, (int, float)) else str(current_loss)
            val_loss_str = f"{validation_loss}" if isinstance(validation_loss, (int, float)) else str(validation_loss)
            lr_str = f"{lr}" if isinstance(lr, (int, float)) else str(lr)
            logger.info(f"🎯 SP Epoch {epoch_idx}/{epoch_total}: training_loss={loss_str}, validation_loss={val_loss_str}, lr={lr_str}")
            if progress_max > 0:
                logger.info(f"   Batch Progress: {progress}/{progress_max} ({(progress/progress_max*100):.1f}%)")
            else:
                logger.info(f"   Batch Progress: {progress}/{progress_max}")
            
            # Log metrics if available
            metrics = progress_dict.get('metrics', {})
            if metrics and metrics != {}:
                accuracy = metrics.get('accuracy', 0)
                f1 = metrics.get('f1', 0) 
                auc = metrics.get('auc', 0)
                # Safe formatting - check types before using format specifiers
                acc_str = f"{accuracy}" if isinstance(accuracy, (int, float)) else str(accuracy)
                f1_str = f"{f1}" if isinstance(f1, (int, float)) else str(f1)
                auc_str = f"{auc}" if isinstance(auc, (int, float)) else str(auc)
                logger.info(f"   Metrics: accuracy={acc_str}, f1={f1_str}, auc={auc_str}")
            
            # Post progress to monitor (only on epoch completion, not every batch)
            # Only post when epoch_idx changes (new epoch completed)
            if epoch_idx > 0 and epoch_total > 0 and epoch_idx != last_posted_epoch[0]:
                try:
                    # Check if GPU is being used
                    ran_on_gpu = torch.cuda.is_available() and torch.cuda.current_device() is not None
                    
                    # Determine training type from target column type
                    training_type = "classification"
                    if args.target_column_type == "numeric":
                        training_type = "regression"
                    
                    # Calculate estimated time remaining if we have timing info
                    estimated_time_remaining = None
                    time_now = progress_dict.get('time_now')
                    if time_now and epoch_idx > 0:
                        # Estimate based on batch progress rate
                        if progress_max > 0 and progress > 0:
                            elapsed = time_now - progress_dict.get('start_time', time_now)
                            if elapsed > 0:
                                rate = progress / elapsed  # batches per second
                                remaining_batches = progress_max - progress
                                if rate > 0:
                                    total_seconds = remaining_batches / rate
                                    minutes = int(total_seconds / 60)
                                    if minutes > 0:
                                        estimated_time_remaining = f"{minutes}m"
                                    else:
                                        estimated_time_remaining = f"{int(total_seconds)}s"
                    
                    # Get session_id from args (prefer session_id, fallback to job_id, or generate one)
                    session_id = (
                        getattr(args, 'session_id', None) or 
                        args.job_id if hasattr(args, 'job_id') and args.job_id else 
                        f"sp-{id(progress_dict)}"
                    )
                    
                    post_training_progress(
                        session_id=session_id,
                        training_type=training_type,
                        current_epoch=int(epoch_idx),
                        total_epochs=int(epoch_total),
                        current_training_loss=float(current_loss) if current_loss else None,
                        current_validation_loss=float(validation_loss) if validation_loss else None,
                        estimated_time_remaining=estimated_time_remaining,
                        ran_on_gpu=ran_on_gpu,
                    )
                    # Mark this epoch as posted
                    last_posted_epoch[0] = epoch_idx
                except Exception as monitor_err:
                    # Don't let monitor errors break training
                    logger.debug(f"Monitor progress post failed: {monitor_err}")
            
            if args.job_queue and args.job_id:
                # Try Redis first for fast progress updates (partial updates)
                try:
                    from redis_job_progress import get_redis_job_progress
                    redis_progress = get_redis_job_progress()
                    if redis_progress.redis_available:
                        # Update progress in Redis (fast partial update)
                        redis_progress.update_progress(
                            job_type=args.job_queue,
                            job_id=args.job_id,
                            progress=progress / progress_max if progress_max > 0 else 0,
                            current_epoch=epoch_idx,
                            current_loss=current_loss,
                            validation_loss=validation_loss,
                            metrics=metrics,
                            time_now=progress_dict.get('time_now', None),
                        )
                        # Still update Redis job data periodically (every 10 batches or on epoch boundaries)
                        if epoch_idx > 0 and (progress % 10 == 0 or epoch_idx != last_posted_epoch[0]):
                            from lib.job_manager import load_job, save_job
                            job_data = load_job(args.job_id)
                            if job_data:
                                job_data['progress'] = progress / progress_max if progress_max > 0 else 0
                                job_data['current_epoch'] = epoch_idx
                                job_data['current_loss'] = current_loss
                                job_data['validation_loss'] = validation_loss
                                job_data['metrics'] = metrics
                                job_data['time_now'] = progress_dict.get('time_now', None)
                                session_id = job_data.get('session_id') or args.session_id
                                job_type = job_data.get('job_type') or args.job_queue
                                save_job(args.job_id, job_data, session_id, job_type)
                    else:
                        # Redis not available - update job data directly
                        from lib.job_manager import load_job, save_job
                        job_data = load_job(args.job_id)
                        if job_data:
                            job_data['progress'] = progress / progress_max if progress_max > 0 else 0
                            job_data['current_epoch'] = epoch_idx
                            job_data['current_loss'] = current_loss
                            job_data['validation_loss'] = validation_loss
                            job_data['metrics'] = metrics
                            job_data['time_now'] = progress_dict.get('time_now', None)
                            session_id = job_data.get('session_id') or args.session_id
                            job_type = job_data.get('job_type') or args.job_queue
                            save_job(args.job_id, job_data, session_id, job_type)
                except Exception as redis_err:
                    # Redis failed - try to update job data directly
                    logger.debug(f"Redis progress update failed: {redis_err}")
                    try:
                        from lib.job_manager import load_job, save_job
                        job_data = load_job(args.job_id)
                        if job_data:
                            job_data['progress'] = progress / progress_max if progress_max > 0 else 0
                            job_data['current_epoch'] = epoch_idx
                            job_data['current_loss'] = current_loss
                            job_data['validation_loss'] = validation_loss
                            job_data['metrics'] = metrics
                            job_data['time_now'] = progress_dict.get('time_now', None)
                            session_id = job_data.get('session_id') or args.session_id
                            job_type = job_data.get('job_type') or args.job_queue
                            save_job(args.job_id, job_data, session_id, job_type)
                    except Exception as job_err:
                        logger.debug(f"Failed to update job data: {job_err}")
                
                epoch_idx = progress_dict.get('epoch_idx', 0)
                current_loss = progress_dict.get('current_loss', 'N/A')
                # Safe formatting - check types before using format specifiers
                if isinstance(progress, (int, float)) and isinstance(progress_max, (int, float)) and progress_max > 0:
                    pct = progress / progress_max * 100
                    pct_str = f"{pct}"
                else:
                    pct_str = "N/A"
                loss_str = f"{current_loss}" if isinstance(current_loss, (int, float)) else str(current_loss)
                logger.info(f"Progress: {progress}/{progress_max} ({pct_str}%) - Epoch {epoch_idx}, Loss: {loss_str}")
                
        except Exception as err:
            logger.error(f"Error during saving job progress: {err}")
            traceback.print_exc()
    
    training_worked = False
    batch_size = args.batch_size or 0 
    epochs = args.n_epochs or 0
    logger.info(f"... input batch_size = {batch_size}, epochs = {epochs}")
    
    if batch_size == 0:
        batch_size = ideal_batch_size(len(train_df))
    
    if epochs == 0:
        # Calculate class imbalance ratio for classification tasks
        imbalance_ratio = 1.0
        if args.target_column_type == "set" and args.target_column in train_df.columns:
            value_counts = train_df[args.target_column].value_counts()
            if len(value_counts) >= 2:
                majority_count = value_counts.iloc[0]
                minority_count = value_counts.iloc[-1]
                imbalance_ratio = majority_count / max(minority_count, 1)
                logger.info(f"📊 Class imbalance detected: {majority_count}:{minority_count} (ratio: {imbalance_ratio:.1f}:1)")
        
        if epochs == 0:
            epochs = ideal_epochs_predictor(len(train_df), batch_size, imbalance_ratio=imbalance_ratio)
            logger.info(f"📊 Auto-calculated epochs: {epochs} (based on {len(train_df)} rows, imbalance ratio {imbalance_ratio:.1f})")
        else:
            logger.info(f"📊 Using specified epochs: {epochs} (user provided, not auto-calculated)")

    logger.info(f"... will use batch_size = {batch_size}, epochs = {epochs}")
    
    # Check if we're resuming from an existing predictor (continuation training)
    resume_from_predictor = getattr(args, 'resume_from_predictor', None)
    if resume_from_predictor:
        logger.info(f"🔄 RESUME MODE: Loading existing predictor from {resume_from_predictor}")
        logger.info(f"   Will continue training for {epochs} additional epochs")


    worked = False
    # FORCE CPU - don't reset to GPU
    # Note: Device will be determined automatically based on CUDA availability
    
    while not worked and batch_size >= 8:
        try:
            # Don't use CUDA - we're forcing CPU
            # if torch.cuda.is_available():
            #     torch.cuda.empty_cache()
            #     torch.cuda.synchronize()
            
            logger.info(f"Attempting training with batch_size = {batch_size}")
            
            # Analyze dataset complexity FIRST
            from featrix.neural.utils import analyze_dataset_complexity
            
            logger.info("\n" + "="*100)
            logger.info("STEP 1: DATASET COMPLEXITY ANALYSIS")
            logger.info("="*100)
            
            complexity_analysis = analyze_dataset_complexity(
                train_df=train_df,
                target_column=args.target_column,
                target_column_type=args.target_column_type
            )
            
            logger.info("\n" + "="*100)
            logger.info("STEP 2: ARCHITECTURE SELECTION")
            logger.info("="*100)
            
            # Initialize predictor_base (will be set if creating new predictor)
            predictor_base = None
            predictor_name = args.name or f"{args.target_column}_predictor"
            
            # Check if we're resuming from an existing predictor
            resume_from_predictor = getattr(args, 'resume_from_predictor', None)
            if resume_from_predictor:
                logger.info(f"🔄 RESUME MODE: Loading existing predictor from {resume_from_predictor}")
                _log_gpu_memory("BEFORE LOAD_SINGLE_PREDICTOR")
                fsp = load_single_predictor(resume_from_predictor)
                _log_gpu_memory("AFTER LOAD_SINGLE_PREDICTOR")
                logger.info(f"✅ Loaded existing predictor: {fsp.name if hasattr(fsp, 'name') else 'unnamed'}")
                logger.info(f"   Will continue training for {epochs} additional epochs")
                
                # Update embedding space reference (may have changed)
                fsp.embedding_space = es
                fsp.embedding_space.output_dir = current_dir
                
                # Use existing batch_size and learning_rate if not specified
                if batch_size == 0 and hasattr(fsp, 'train_df') and len(fsp.train_df) > 0:
                    batch_size = ideal_batch_size(len(fsp.train_df))
                    logger.info(f"   Using existing predictor's batch_size: {batch_size}")
                if args.learning_rate is None and hasattr(fsp, 'training_metrics') and fsp.training_metrics:
                    # Try to get last learning rate from training history
                    logger.info(f"   Using existing predictor's learning rate (will be set during training)")
            else:
                # NEW TRAINING: Create new predictor
                # Auto-calculate optimal configuration based on dataset characteristics AND complexity analysis
                n_rows = len(train_df)
                from featrix.neural.utils import ideal_single_predictor_config
                
                config = ideal_single_predictor_config(
                    n_rows=n_rows,
                    d_model=es.d_model,
                    n_cols=len(train_df.columns),
                    fine_tune=args.fine_tune,
                    complexity_analysis=complexity_analysis
                )
                
                d_hidden = config.get("d_hidden", 256)
                n_hidden_layers = config.get("n_hidden_layers", 2)
                dropout = config.get("dropout", 0.3)
                use_batch_norm = config.get("use_batch_norm", True)
                use_residual = config.get("residual", True)
                
                logger.info(f"📊 Dataset size: {n_rows} rows - configuration:")
                if d_hidden is None:
                    logger.info(f"   • Architecture: Simple Linear layer (no hidden layers)")
                else:
                    logger.info(f"   • Hidden dimension: {d_hidden}")
                    logger.info(f"   • Hidden layers: {n_hidden_layers}")
                logger.info(f"   • Dropout: {dropout}")
                logger.info(f"   • Batch normalization: {use_batch_norm}")
                logger.info(f"   • Residual connections: {use_residual}")
                
                # Create the predictor architecture
                predictor_base = create_predictor_mlp(
                    d_in=es.d_model, 
                    d_hidden=d_hidden if d_hidden is not None else 256,  # Fallback for linear head
                    n_hidden_layers=n_hidden_layers,
                    dropout=dropout,
                    use_batch_norm=use_batch_norm,
                    residual=use_residual
                )
                logger.info("🔧 Creating FeatrixSinglePredictor instance...")
                fsp = FeatrixSinglePredictor(es, predictor_base, name=predictor_name, user_metadata=args.user_metadata)
                logger.info(f"🔧 FeatrixSinglePredictor created with name: {predictor_name}")
            logger.info(f"🔧 FeatrixSinglePredictor created from module: {fsp.__class__.__module__}")
            
            # Get file location safely
            try:
                module_name = fsp.__class__.__module__
                if module_name in sys.modules:
                    mod = sys.modules[module_name]
                    file_loc = getattr(mod, '__file__', 'unknown')
                    logger.info(f"🔧 FeatrixSinglePredictor file location: {file_loc}")
            except Exception as e:
                logger.warning(f"Could not determine file location: {e}")
            
            # Check prep_for_training signature
            sig = inspect.signature(fsp.prep_for_training)
            logger.info(f"🔧 prep_for_training signature: {sig}")
            logger.info(f"🔧 prep_for_training parameters: {list(sig.parameters.keys())}")
            
            # Only call prep_for_training if not resuming (resumed predictor is already prepared)
            if not resume_from_predictor:
                # AUTO-ENABLE class weights if complexity analysis recommends it
                use_class_weights = args.use_class_weights
                if complexity_analysis and not args.use_class_weights:
                    # Check if complexity analysis recommends class weights
                    recommendations = complexity_analysis.get('recommendations', [])
                    imbalance_ratio = complexity_analysis.get('class_imbalance_ratio', 1.0)
                    
                    # Auto-enable if recommendation mentions class weights or if imbalance is significant
                    should_enable = False
                    for rec in recommendations:
                        if 'class weight' in rec.lower() or 'imbalance' in rec.lower():
                            should_enable = True
                            logger.info(f"✅ AUTO-ENABLING class weights based on complexity analysis recommendation: {rec}")
                            break
                    
                    # Also auto-enable for significant imbalance even if not explicitly recommended
                    if not should_enable and imbalance_ratio > 3.0:
                        should_enable = True
                        logger.info(f"✅ AUTO-ENABLING class weights due to class imbalance ratio: {imbalance_ratio:.1f}:1")
                    
                    if should_enable:
                        use_class_weights = True
                
                logger.info("="*100)
                logger.info(f"🔧 ABOUT TO CALL prep_for_training with target_col_name='{args.target_column}', target_col_type='{args.target_column_type}'")
                logger.info(f"🔧 prep_for_training method object: {fsp.prep_for_training}")
                logger.info(f"🔧 use_class_weights: {use_class_weights} {'(AUTO-ENABLED from complexity analysis)' if use_class_weights and not args.use_class_weights else ''}")
                if args.class_imbalance:
                    logger.info(f"🔧 class_imbalance provided: {args.class_imbalance}")
                logger.info("="*100)
                
                fsp.prep_for_training(
                    train_df=train_df,
                    target_col_name=args.target_column,
                    target_col_type=args.target_column_type,
                    use_class_weights=use_class_weights,
                    class_imbalance=args.class_imbalance,
                    cost_false_positive=args.cost_false_positive,
                    cost_false_negative=args.cost_false_negative
                )
                
                logger.info("="*100)
                logger.info(f"🔧 COMPLETED prep_for_training call")
                logger.info(f"🔧 Target codec after prep: {type(fsp.target_codec).__name__}")
                logger.info("="*100)
            else:
                logger.info("🔄 RESUME MODE: Skipping prep_for_training (predictor already prepared)")
                # Update train_df if needed (in case data changed)
                if hasattr(fsp, 'train_df'):
                    logger.info(f"   Updating train_df reference (keeping existing data)")
            
            logger.info(f"Predictor prepared. Target codec: {type(fsp.target_codec).__name__}")
            
            # Check if we should use cross-validation (5-fold)
            use_cross_validation = True  # Always use CV for single predictors
            n_folds = 5
            
            # Check feature flag for proper CV (only for new training, not resuming)
            use_proper_cv = (
                PROPER_CV_AVAILABLE and
                not resume_from_predictor and
                predictor_base is not None and
                os.getenv("USE_PROPER_CV", "true").lower() == "true"
            )
            
            if use_cross_validation and len(train_df) >= n_folds:
                if use_proper_cv:
                    # PROPER CROSS-VALIDATION: Train 5 independent predictors and select best
                    logger.info("="*100)
                    logger.info("✅ PROPER CV ENABLED: Training 5 independent predictors")
                    logger.info("   Set USE_PROPER_CV=false to use sequential CV (old behavior)")
                    logger.info("="*100)
                    
                    # Use proper CV function (creates predictors internally)
                    # Note: predictor_base and predictor_name are already set above
                    fsp = train_with_proper_cv(
                        embedding_space=es,
                        train_df=train_df,
                        args=args,
                        epochs=epochs,
                        batch_size=batch_size,
                        predictor_base=predictor_base,
                        predictor_name=predictor_name,
                        progress_callback=progress_callback,
                    )
                    
                    logger.info("="*80)
                    logger.info(f"✅ PROPER K-FOLD CROSS-VALIDATION COMPLETE")
                    logger.info("="*80)
                else:
                    # SEQUENTIAL CROSS-VALIDATION (old behavior): train one predictor across folds
                    from sklearn.model_selection import KFold
                    
                    logger.info("="*100)
                    logger.info("🔀 K-FOLD CROSS-VALIDATION (SEQUENTIAL): Training across 5 data folds")
                    logger.info(f"   Epochs specified: {epochs}")
                    logger.info("   Each fold continues from previous, ensuring predictor sees all data patterns")
                    if PROPER_CV_AVAILABLE:
                        logger.info("   💡 Set USE_PROPER_CV=true to train 5 independent predictors and select best")
                    logger.info("="*100)
                    
                    # Each fold gets the FULL epoch count (not divided)
                    epochs_per_fold = epochs
                    logger.info(f"📊 Training plan: {epochs_per_fold} epochs per fold × {n_folds} folds = {epochs_per_fold * n_folds} total epochs")
                    
                    # K-Fold splitter (shuffle for randomness, fixed seed for reproducibility)
                    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
                    
                    # Track total epochs trained across all folds
                    total_epochs_trained = 0
                    
                    for fold_idx, (train_idx, val_idx) in enumerate(kf.split(train_df)):
                        logger.info("="*80)
                        logger.info(f"🔀 FOLD {fold_idx + 1}/{n_folds}: Training on {len(train_idx)} rows, validating on {len(val_idx)} rows")
                        if fold_idx == 0:
                            logger.info(f"   Starting fresh training")
                        else:
                            logger.info(f"   Continuing from fold {fold_idx}")
                        logger.info("="*80)
                        
                        # Create fold-specific train/val data
                        fold_train_df = train_df.iloc[train_idx].copy().reset_index(drop=True)
                        fold_val_df = train_df.iloc[val_idx].copy().reset_index(drop=True)
                        
                        # Update train_df for this fold (codecs already set up from full dataset prep)
                        # This allows the predictor to use fold-specific training data while keeping
                        # the same codec structure (all classes from full dataset)
                        logger.info(f"   Updating train_df for fold {fold_idx + 1}...")
                        fsp.train_df = fold_train_df
                        logger.info(f"   ✅ Train_df updated: {len(fold_train_df)} rows for fold {fold_idx + 1}")
                        
                        # Train this fold (continues from previous fold's state)
                        logger.info(f"🏋️  Training fold {fold_idx + 1} for {epochs_per_fold} epochs...")
                        logger.info(f"🏋️  FINE_TUNE SETTING: {args.fine_tune} ({'ENABLED - training encoder + predictor' if args.fine_tune else 'DISABLED - encoder frozen, only predictor trains'})")
                        
                        # Create validation DataFrame for this fold
                        asyncio.run(fsp.train(
                            n_epochs=epochs_per_fold,
                            batch_size=batch_size,
                            fine_tune=args.fine_tune,
                            val_df=fold_val_df,  # Use fold-specific validation set
                            optimizer_params={"lr": args.learning_rate},
                            val_pos_label=args.positive_label,
                            print_callback=progress_callback,
                            print_progress_step=10,
                            job_id=args.job_id,
                        ))
                        
                        # Update total epochs trained
                        total_epochs_trained += epochs_per_fold
                        
                        logger.info(f"✅ Fold {fold_idx + 1} completed (total epochs so far: {total_epochs_trained})")
                    
                    logger.info("="*80)
                    logger.info(f"✅ K-FOLD CROSS-VALIDATION COMPLETE: Predictor trained on all {len(train_df)} rows across {n_folds} different splits")
                    logger.info(f"   Total epochs trained: {total_epochs_trained}")
                    logger.info("="*80)
            else:
                # Standard training (no cross-validation)
                if len(train_df) < n_folds:
                    logger.info(f"⚠️  Dataset too small ({len(train_df)} rows) for {n_folds}-fold CV. Using standard training.")
                
                logger.info("="*100)
                logger.info("🏋️ ABOUT TO START TRAINING by calling fsp.train()")
                logger.info(f"🏋️ Training params: n_epochs={epochs}, batch_size={batch_size}, learning_rate={args.learning_rate}")
                logger.info(f"🏋️ FINE_TUNE SETTING: {args.fine_tune} ({'ENABLED - training encoder + predictor' if args.fine_tune else 'DISABLED - encoder frozen, only predictor trains'})")
                if args.positive_label:
                    logger.info(f"🏋️ Positive label: {args.positive_label}")
                logger.info("="*100)
                
                asyncio.run(fsp.train(
                    n_epochs=epochs,
                    batch_size=batch_size,
                    fine_tune=args.fine_tune,
                    optimizer_params={"lr": args.learning_rate},
                    val_pos_label=args.positive_label,  # Pass positive label for binary classification
                    print_callback=progress_callback,
                    print_progress_step=10,
                    job_id=args.job_id,  # Pass job_id for ABORT/FINISH detection
                ))
            
            logger.info("@@@ Single predictor training completed successfully! @@@")
            worked = True
            
            # Load session to get model_id before saving predictor
            model_id = None
            session_id = args.session_id or args.job_id
            session = None
            if session_id:
                try:
                    from lib.session_manager import load_session
                    session = load_session(session_id)
                    if session:
                        # Check session metadata first
                        metadata = session.get("metadata", {})
                        if isinstance(metadata, dict):
                            model_id = metadata.get("model_id")
                        
                        # Fallback to session name if it looks like a model_id
                        if not model_id:
                            session_name = session.get("name", "")
                            if session_name and session_name.startswith("dot_model_"):
                                model_id = session_name
                except Exception as e:
                    logger.warning(f"⚠️  Could not load session to get model_id: {e}")
            
            # Check if simple linear layer performed poorly and log recommendation
            if n_hidden_layers == 0 and hasattr(fsp, 'training_metrics') and fsp.training_metrics:
                metrics = fsp.training_metrics
                accuracy = metrics.get('accuracy', 0)
                f1 = metrics.get('f1', 0)
                val_loss = metrics.get('validation_loss', float('inf'))
                
                # Detect poor performance indicators
                poor_performance = False
                reasons = []
                
                if accuracy < 0.5:  # Less than 50% accuracy
                    poor_performance = True
                    reasons.append(f"Low accuracy ({accuracy:.2%})")
                
                if f1 < 0.3:  # F1 score below 0.3
                    poor_performance = True
                    reasons.append(f"Low F1 score ({f1:.3f})")
                
                if val_loss > 1.0:  # High validation loss
                    poor_performance = True
                    reasons.append(f"High validation loss ({val_loss:.3f})")
                
                if poor_performance:
                    logger.warning("=" * 80)
                    logger.warning("⚠️  SIMPLE LINEAR LAYER PERFORMANCE WARNING")
                    logger.warning("=" * 80)
                    logger.warning(f"   The simple Linear(d_model, d_out) architecture may be insufficient.")
                    logger.warning(f"   Performance indicators:")
                    for reason in reasons:
                        logger.warning(f"     • {reason}")
                    logger.warning(f"")
                    logger.warning(f"   💡 RECOMMENDATION:")
                    logger.warning(f"     Consider retraining with a hidden layer:")
                    logger.warning(f"     • Architecture: Linear(d_model→64) → GELU → Dropout(0.2) → Linear(64→d_out)")
                    logger.warning(f"     • This adds nonlinearity and may improve performance")
                    logger.warning(f"     • Small datasets (<1000 rows) can still benefit from 1 hidden layer")
                    logger.warning("=" * 80)
                    
                    # Store recommendation in training metrics for later reference
                    if not hasattr(metrics, '__dict__'):
                        metrics = dict(metrics) if isinstance(metrics, dict) else {}
                    metrics['architecture_recommendation'] = {
                        "current_architecture": "Linear(d_model, d_out)",
                        "recommended_architecture": "Linear(d_model→64) → GELU → Dropout(0.2) → Linear(64→d_out)",
                        "reason": "Poor performance detected with simple linear layer",
                        "indicators": reasons,
                        "accuracy": accuracy,
                        "f1": f1,
                        "validation_loss": val_loss
                    }
            
            # Save the trained predictor with model_id
            write_single_predictor(fsp, ".", model_id=model_id)
            
            # Mark training as complete in status metadata
            try:
                import glob
                # Find and update any training status files
                status_files = glob.glob("*_training_status.json")
                for status_file in status_files:
                    try:
                        with open(status_file, 'r') as f:
                            status = json.load(f)
                        status['is_training'] = False
                        status['completed_at'] = time.time()
                        status['final_epoch'] = status.get('epoch', epochs)
                        with open(status_file, 'w') as f:
                            json.dump(status, f, indent=2, default=str)
                        logger.info(f"✅ Marked training as complete in {status_file}")
                    except Exception as e:
                        logger.warning(f"⚠️  Failed to update training status file {status_file}: {e}")
            except Exception as e:
                logger.warning(f"⚠️  Failed to mark training as complete: {e}")
            
            # Handle webhook callbacks if configured
            if args.webhooks:
                try:
                    logger.info("="*80)
                    logger.info("🔔 PROCESSING WEBHOOK CALLBACKS")
                    logger.info("="*80)
                    
                    from lib.webhook_helpers import (
                        call_s3_backup_webhook,
                        upload_file_to_s3_url,
                        call_model_id_update_webhook
                    )
                    from lib.session_manager import load_session
                    
                    # Get session to extract model_id and org_id (reuse if already loaded)
                    if not model_id and session_id:
                        try:
                            if not session:
                                session = load_session(session_id)
                            # Try to extract model_id from session metadata or name
                            if session:
                                # Check session metadata first
                                metadata = session.get("metadata", {})
                                if isinstance(metadata, dict):
                                    model_id = metadata.get("model_id")
                                
                                # Fallback to session name if it looks like a model_id
                                if not model_id:
                                    session_name = session.get("name", "")
                                    if session_name and session_name.startswith("dot_model_"):
                                        model_id = session_name
                                
                                # If still no model_id, use session_id as fallback
                                if not model_id:
                                    model_id = session_id
                        except Exception as e:
                            logger.warning(f"⚠️  Could not load session for webhooks: {e}")
                            model_id = session_id
                    
                    if not model_id:
                        model_id = args.job_id or "unknown"
                    
                    org_id = args.webhooks.get("webhook_callback_secret")
                    if not org_id:
                        logger.warning("⚠️  No webhook_callback_secret provided, skipping webhooks")
                    else:
                        # Upload model assets to S3 if s3_backup_url is configured
                        s3_backup_url = args.webhooks.get("s3_backup_url")
                        if s3_backup_url:
                            logger.info("📤 Uploading model assets to S3...")
                            
                            # Upload single_predictor.pickle
                            predictor_path = Path(".") / "single_predictor.pickle"
                            if predictor_path.exists():
                                upload_result = call_s3_backup_webhook(
                                    webhook_url=s3_backup_url,
                                    model_id=model_id,
                                    org_id=org_id,
                                    file_name="single_predictor.pickle",
                                    content_type="application/octet-stream",
                                    webhook_secret=org_id
                                )
                                
                                if upload_result and upload_result.get("upload_url"):
                                    if upload_file_to_s3_url(predictor_path, upload_result["upload_url"]):
                                        logger.info(f"✅ Uploaded single_predictor.pickle to {upload_result.get('storage_path', 'S3')}")
                            
                            # Upload training_metrics.json
                            metrics_path = Path(".") / "training_metrics.json"
                            if metrics_path.exists():
                                upload_result = call_s3_backup_webhook(
                                    webhook_url=s3_backup_url,
                                    model_id=model_id,
                                    org_id=org_id,
                                    file_name="training_metrics.json",
                                    content_type="application/json",
                                    webhook_secret=org_id
                                )
                                
                                if upload_result and upload_result.get("upload_url"):
                                    if upload_file_to_s3_url(metrics_path, upload_result["upload_url"]):
                                        logger.info(f"✅ Uploaded training_metrics.json to {upload_result.get('storage_path', 'S3')}")
                        else:
                            logger.info("ℹ️  No s3_backup_url configured, skipping S3 upload")
                        
                        # Call model_id_update webhook when training completes successfully
                        model_id_update_url = args.webhooks.get("model_id_update_url")
                        if model_id_update_url:
                            # Extract metrics from the trained predictor
                            metrics = {}
                            if hasattr(fsp, 'training_metrics') and fsp.training_metrics:
                                metrics = fsp.training_metrics
                            
                            # Get featrix IDs
                            featrix_model_id = args.job_id or "unknown"
                            
                            # CRITICAL: Use the session_id (which should be the NEW predictor session ID)
                            # NOT the foundation_model_id. The session_id comes from args.session_id
                            # which is set when the job is created with the correct new session ID.
                            featrix_session_id = session_id or "unknown"
                            
                            # Defensive check: ensure we're not accidentally using foundation_model_id
                            foundation_model_id = None
                            if session:
                                foundation_model_id = session.get("foundation_model_id")
                                if foundation_model_id and featrix_session_id == foundation_model_id:
                                    logger.error(f"❌ CRITICAL BUG: featrix_session_id matches foundation_model_id!")
                                    logger.error(f"   This means the webhook would send the foundation's ID instead of the new session ID")
                                    logger.error(f"   session_id from args: {args.session_id}")
                                    logger.error(f"   job_id: {args.job_id}")
                                    logger.error(f"   featrix_session_id: {featrix_session_id}")
                                    logger.error(f"   foundation_model_id: {foundation_model_id}")
                                    # This should never happen, but if it does, log it and use session_id anyway
                            
                            logger.info(f"📤 Webhook sending: featrix_session_id={featrix_session_id} (foundation={foundation_model_id})")
                            
                            featrix_es_id = None
                            if session:
                                es_path = session.get("embedding_space")
                                if es_path:
                                    # Try to extract ES ID from path or session
                                    featrix_es_id = Path(es_path).stem if es_path else None
                            
                            call_model_id_update_webhook(
                                webhook_url=model_id_update_url,
                                model_id=model_id,
                                org_id=org_id,
                                featrix_model_id=featrix_model_id,
                                featrix_session_id=featrix_session_id,
                                featrix_es_id=featrix_es_id,
                                status="succeeded",
                                metrics=metrics,
                                webhook_secret=org_id
                            )
                        else:
                            logger.info("ℹ️  No model_id_update_url configured, skipping completion webhook")
                    
                    logger.info("="*80)
                    
                    # Log training completion event
                    if session_id:
                        try:
                            from event_log import log_training_event
                            metrics_dict = {}
                            if hasattr(fsp, 'training_metrics') and fsp.training_metrics:
                                metrics_dict = fsp.training_metrics
                            
                            log_training_event(
                                session_id=session_id,
                                event_name="training_completed",
                                predictor_id=args.job_id,
                                additional_info={
                                    "target_column": args.target_column,
                                    "target_column_type": args.target_column_type,
                                    "metrics": metrics_dict,
                                    "status": "succeeded"
                                }
                            )
                        except Exception as e:
                            logger.debug(f"Failed to log training completion event: {e}")
                    
                except Exception as e:
                    logger.error(f"❌ Error processing webhooks: {e}")
                    logger.debug(f"   Full traceback: {traceback.format_exc()}")
                    # Don't fail training if webhooks fail
            
            # Post training data to monitor.featrix.com
            training_end_time = datetime.now()
            try:
                logger.info("="*80)
                logger.info("📊 POSTING SP TRAINING DATA TO MONITOR")
                logger.info("="*80)
                
                from training_monitor import collect_sp_training_data, post_training_data
                
                # SP training creates an internal validation split (20% by default)
                # We don't have direct access to the split after training, so we'll use train_df
                # and note in metadata that SP uses internal validation
                # The actual validation size is approximately 20% of train_df
                val_df = train_df  # SP uses internal validation split, approximate size is 20% of train_df
                
                # Get session_id from args (prefer session_id, fallback to job_id)
                session_id = getattr(args, 'session_id', None) or getattr(args, 'job_id', None)
                
                training_data = collect_sp_training_data(
                    single_predictor=fsp,
                    embedding_space=es,
                    train_df=train_df,
                    val_df=val_df,
                    target_column=args.target_column,
                    target_column_type=args.target_column_type,
                    training_start_time=training_start_time,
                    training_end_time=training_end_time,
                    epochs=epochs,
                    batch_size=batch_size,
                    learning_rate=args.learning_rate,
                    customer_id=getattr(args, 'customer_id', None),
                    remote_hostname=getattr(args, 'remote_hostname', None),
                    s3_path=getattr(args, 's3_path', None),
                    session_id=session_id,
                )
                
                post_training_data(training_data)
                
                logger.info("="*80)
            except Exception as e:
                logger.warning(f"⚠️  Failed to post SP training data to monitor: {e}")
                logger.debug(f"   Full traceback: {traceback.format_exc()}")
                # Don't fail training if monitor posting fails
            
            # Save comprehensive training metadata JSON
            try:
                logger.info("="*80)
                logger.info("📝 SAVING COMPREHENSIVE TRAINING METADATA")
                logger.info("="*80)
                
                metadata_file = save_predictor_metadata(
                    session_id=args.session_id or args.job_id or "no_session",
                    target_column=args.target_column,
                    target_column_type=args.target_column_type,
                    epochs=epochs,
                    training_response=None,  # Could add initial API response if available
                    csv_file=args.input_file,
                    client=None,  # No API client available in local training
                    training_start_time=training_start_time,
                    fsp=fsp  # Pass the trained predictor for local model info
                )
                
                if metadata_file:
                    logger.info(f"✅ Training metadata successfully saved to: {metadata_file}")
                else:
                    logger.warning("⚠️ Failed to save training metadata")
                    
                logger.info("="*80)
            except Exception as e:
                logger.error(f"❌ Error saving training metadata: {e}")
                traceback.print_exc()
                # Don't fail the training if metadata save fails
            
            # Save training metrics
            metrics_path = "./training_metrics.json"
            with open(metrics_path, "w") as f:
                json.dump({
                    "training_info": getattr(fsp, 'training_info', []),
                    "target_column": args.target_column,
                    "target_column_type": args.target_column_type,
                    "final_metrics": getattr(fsp, 'training_metrics', {}),
                    "class_distribution": getattr(fsp, 'class_distribution', {}),  # Include validation set distribution
                    "args": args.model_dump()
                }, f, indent=2, default=str)
            
            logger.info(f"Training metrics saved to {metrics_path}")
            
            training_worked = True
            break
            
        except (TrainingFailureException, FeatrixRestartTrainingException) as e:
            # Only retry on Featrix-specific exceptions (these are retryable)
            traceback.print_exc(file=sys.stdout)
            logger.error(f"Training failed with batch_size {batch_size}: {type(e).__name__}: {e}")
            
            # Post exception to Slack for visibility
            try:
                from pathlib import Path  # Import here to ensure it's available in exception handler
                sys.path.insert(0, str(Path(__file__).parent.parent))
                from slack import send_slack_message
                
                slack_msg = f"⚠️ **Single Predictor Training Exception (Retrying)**\n"
                slack_msg += f"Target Column: {args.target_column}\n"
                slack_msg += f"Session ID: {args.session_id}\n"
                slack_msg += f"Job ID: {args.job_id}\n"
                slack_msg += f"Batch Size: {batch_size}\n"
                slack_msg += f"Exception: {type(e).__name__}: {str(e)}\n"
                slack_msg += f"Action: Reducing batch size to {int(batch_size / 2)} and retrying"
                
                send_slack_message(slack_msg)
                logger.info("✅ Slack notification sent for Single Predictor training exception")
            except Exception as slack_error:
                logger.warning(f"Failed to send Slack notification: {slack_error}")
            
            batch_size = int(batch_size / 2)
            logger.info(f"Reducing batch size to {batch_size} and retrying...")
            
        except (AssertionError, TypeError, AttributeError, ValueError, RuntimeError, OSError) as e:
            # Non-Featrix exceptions (AssertionError, etc.) - abort immediately, don't retry
            # Check if it's a CUDA OOM error and dump memory if so
            error_msg = str(e).lower()
            if isinstance(e, RuntimeError) and "cuda" in error_msg and ("out of memory" in error_msg or "oom" in error_msg):
                dump_cuda_memory_usage(context=f"training loop (batch_size={batch_size})")
            
            traceback.print_exc(file=sys.stdout)
            logger.error(f"❌ Non-Featrix exception during training with batch_size {batch_size}: {type(e).__name__}: {e}")
            logger.error(f"   Aborting immediately - these errors are not retryable with different batch sizes")
            
            # Post exception to Slack
            try:
                from pathlib import Path
                sys.path.insert(0, str(Path(__file__).parent.parent))
                from slack import send_slack_message
                
                slack_msg = f"💥 **Single Predictor Training Failed (Non-Featrix Exception)**\n"
                slack_msg += f"Target Column: {args.target_column}\n"
                slack_msg += f"Session ID: {args.session_id}\n"
                slack_msg += f"Job ID: {args.job_id}\n"
                slack_msg += f"Batch Size: {batch_size}\n"
                slack_msg += f"Exception: {type(e).__name__}: {str(e)}\n"
                slack_msg += f"Action: Aborting - not retrying with different batch sizes"
                
                send_slack_message(slack_msg)
                logger.info("✅ Slack notification sent for Single Predictor training failure")
            except Exception as slack_error:
                logger.warning(f"Failed to send Slack notification: {slack_error}")
            
            # Re-raise to abort training
            raise
            
        except Exception as e:
            # Any other exception - also abort (not a Featrix exception)
            traceback.print_exc(file=sys.stdout)
            logger.error(f"❌ Unexpected exception during training with batch_size {batch_size}: {type(e).__name__}: {e}")
            logger.error(f"   Aborting immediately - not a Featrix exception, not retryable")
            
            # Post exception to Slack
            try:
                from pathlib import Path
                sys.path.insert(0, str(Path(__file__).parent.parent))
                from slack import send_slack_message
                
                slack_msg = f"💥 **Single Predictor Training Failed (Unexpected Exception)**\n"
                slack_msg += f"Target Column: {args.target_column}\n"
                slack_msg += f"Session ID: {args.session_id}\n"
                slack_msg += f"Job ID: {args.job_id}\n"
                slack_msg += f"Batch Size: {batch_size}\n"
                slack_msg += f"Exception: {type(e).__name__}: {str(e)}\n"
                slack_msg += f"Action: Aborting - not retrying with different batch sizes"
                
                send_slack_message(slack_msg)
                logger.info("✅ Slack notification sent for Single Predictor training failure")
            except Exception as slack_error:
                logger.warning(f"Failed to send Slack notification: {slack_error}")
            
            # Re-raise to abort training
            raise
    
    if not worked:
        # Post training failure to Slack
        try:
            from pathlib import Path  # Import here to ensure it's available (defensive)
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from slack import send_slack_message
            
            slack_msg = f"💥 **Single Predictor Training Failed**\n"
            slack_msg += f"Target Column: {args.target_column}\n"
            slack_msg += f"Target Type: {args.target_column_type}\n"
            slack_msg += f"Session ID: {args.session_id}\n"
            slack_msg += f"Job ID: {args.job_id}\n"
            slack_msg += f"Reason: Training failed with all attempted batch sizes"
            
            send_slack_message(slack_msg)
            logger.info("✅ Slack notification sent for Single Predictor training failure")
        except Exception as slack_error:
            logger.warning(f"Failed to send Slack notification for failure: {slack_error}")
        
        # Set job status to FAILED before raising
        try:
            job_id = getattr(args, 'job_id', None)
            if job_id:
                logger.error(f"❌ Setting job {job_id} status to FAILED due to training failure")
                update_job_status(job_id=job_id, status=JobStatus.FAILED)
            else:
                logger.warning(f"⚠️  Cannot set job status to FAILED: job_id not available")
        except Exception as status_err:
            logger.error(f"⚠️  Failed to set job status to FAILED: {status_err}")
        
        # Call failure webhook if configured
        if args.webhooks:
            try:
                from lib.webhook_helpers import call_model_id_update_webhook
                from lib.session_manager import load_session
                
                model_id_update_url = args.webhooks.get("model_id_update_url")
                if model_id_update_url:
                    org_id = args.webhooks.get("webhook_callback_secret")
                    if org_id:
                        session_id = args.session_id or args.job_id
                        session = None
                        model_id = None
                        
                        if session_id:
                            try:
                                session = load_session(session_id)
                                if session:
                                    metadata = session.get("metadata", {})
                                    if isinstance(metadata, dict):
                                        model_id = metadata.get("model_id")
                                    if not model_id:
                                        session_name = session.get("name", "")
                                        if session_name and session_name.startswith("dot_model_"):
                                            model_id = session_name
                                    if not model_id:
                                        model_id = session_id
                            except Exception:
                                model_id = session_id
                        
                        if not model_id:
                            model_id = args.job_id or "unknown"
                        
                        # CRITICAL: Use the session_id (which should be the NEW predictor session ID)
                        # NOT the foundation_model_id
                        featrix_session_id = session_id or "unknown"
                        
                        # Defensive check: ensure we're not accidentally using foundation_model_id
                        foundation_model_id = None
                        if session:
                            foundation_model_id = session.get("foundation_model_id")
                            if foundation_model_id and featrix_session_id == foundation_model_id:
                                logger.error(f"❌ CRITICAL BUG: featrix_session_id matches foundation_model_id in failure webhook!")
                                logger.error(f"   session_id from args: {args.session_id}")
                                logger.error(f"   featrix_session_id: {featrix_session_id}")
                                logger.error(f"   foundation_model_id: {foundation_model_id}")
                        
                        logger.info(f"📤 Failure webhook sending: featrix_session_id={featrix_session_id} (foundation={foundation_model_id})")
                        
                        call_model_id_update_webhook(
                            webhook_url=model_id_update_url,
                            model_id=model_id,
                            org_id=org_id,
                            featrix_model_id=args.job_id or "unknown",
                            featrix_session_id=featrix_session_id,
                            featrix_es_id=None,
                            status="failed",
                            metrics={},
                            webhook_secret=org_id
                        )
            except Exception as webhook_err:
                logger.warning(f"⚠️  Failed to call failure webhook: {webhook_err}")
        
        raise Exception("Single predictor training failed with all attempted batch sizes")
    
    logger.info(f"training_worked = {training_worked}")
    
    if not training_worked:
        # Set job status to FAILED before raising
        try:
            job_id = getattr(args, 'job_id', None)
            if job_id:
                logger.error(f"❌ Setting job {job_id} status to FAILED due to training failure")
                update_job_status(job_id=job_id, status=JobStatus.FAILED)
            else:
                logger.warning(f"⚠️  Cannot set job status to FAILED: job_id not available")
        except Exception as status_err:
            logger.error(f"⚠️  Failed to set job status to FAILED: {status_err}")
        
        # Call failure webhook if configured
        if args.webhooks:
            try:
                from lib.webhook_helpers import call_model_id_update_webhook
                from lib.session_manager import load_session
                
                model_id_update_url = args.webhooks.get("model_id_update_url")
                if model_id_update_url:
                    org_id = args.webhooks.get("webhook_callback_secret")
                    if org_id:
                        session_id = args.session_id or args.job_id
                        session = None
                        model_id = None
                        
                        if session_id:
                            try:
                                session = load_session(session_id)
                                if session:
                                    metadata = session.get("metadata", {})
                                    if isinstance(metadata, dict):
                                        model_id = metadata.get("model_id")
                                    if not model_id:
                                        session_name = session.get("name", "")
                                        if session_name and session_name.startswith("dot_model_"):
                                            model_id = session_name
                                    if not model_id:
                                        model_id = session_id
                            except Exception:
                                model_id = session_id
                        
                        if not model_id:
                            model_id = args.job_id or "unknown"
                        
                        call_model_id_update_webhook(
                            webhook_url=model_id_update_url,
                            model_id=model_id,
                            org_id=org_id,
                            featrix_model_id=args.job_id or "unknown",
                            featrix_session_id=session_id or "unknown",
                            featrix_es_id=None,
                            status="failed",
                            metrics={},
                            webhook_secret=org_id
                        )
            except Exception as webhook_err:
                logger.warning(f"⚠️  Failed to call failure webhook: {webhook_err}")
        
        # Send Slack alert for training failure
        try:
            from pathlib import Path as PathLib
            sys.path.insert(0, str(PathLib(__file__).parent.parent))
            from slack import send_slack_message
            
            error_msg = f"🚨 *Single Predictor Training FAILED*\n"
            error_msg += f"• Session: `{args.session_id or 'unknown'}`\n"
            error_msg += f"• Job: `{args.job_id or 'unknown'}`\n"
            error_msg += f"• Target: `{args.target_column}` ({args.target_column_type})\n"
            error_msg += f"• Error: Training failed after all batch size retries"
            
            send_slack_message(error_msg, throttle=False)  # Critical - don't throttle
            logger.info("✅ Slack alert sent for training failure")
        except Exception as slack_error:
            logger.warning(f"Failed to send Slack alert: {slack_error}")
        
        raise Exception("Single predictor training failed")
    
    return 0


if __name__ == "__main__":
    print("Starting Single Predictor Training!")
    
    # Example usage
    args = LightSinglePredictorArgs(
        target_column="target_column_name",  # Replace with actual target column
        target_column_type="set",  # or "scalar"
        n_epochs=0,
        batch_size=0,
    )
    
    train_single_predictor(args=args) 
