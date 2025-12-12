#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2024, Featrix, Inc. All rights reserved.
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import copy
import json
import logging
import warnings
import math
import os
import pickle
import sys
import time
import traceback
import warnings
from typing import Dict
from typing import Optional
from typing import List

import pandas as pd
import numpy as np
import torch
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split

from sklearn.metrics import precision_recall_curve, average_precision_score

from torch import nn
from torch.optim.lr_scheduler import CosineAnnealingLR, SequentialLR, ConstantLR
from torch.utils.data import DataLoader

from featrix.neural.exceptions import FeatrixRestartTrainingException, RestartConfig
from featrix.neural.training_exceptions import TrainingFailureException

# from featrix.models import JobIncrementalStatus
from featrix.neural.device import device
from featrix.neural.data_frame_data_set import collate_tokens
from featrix.neural.data_frame_data_set import SuperSimpleSelfSupervisedDataset
from featrix.neural.embedded_space import EmbeddingSpace
from featrix.neural.dataloader_utils import create_dataloader_kwargs
from featrix.neural.encoders import create_scalar_codec
from featrix.neural.encoders import create_set_codec
from featrix.neural.featrix_token import Token
from featrix.neural.featrix_token import TokenBatch
from featrix.neural.featrix_token import TokenStatus
from featrix.neural.scalar_codec import ScalarCodec
from featrix.neural.set_codec import SetCodec, FocalLoss

from featrix.neural.training_context_manager import PredictorTrainingContextManager, TrainingState, PredictorEvalModeContextManager
from featrix.neural.utils import ideal_batch_size, ideal_epochs_predictor

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],  
    force=True
)

logger = logging.getLogger(__name__)


def _walk_model_for_gpu(model, name="model", depth=0, indent="  "):
    """Recursively walk through entire model and report ANYTHING on GPU."""
    gpu_items = []
    
    # Check if it's a module
    if isinstance(model, torch.nn.Module):
        # Check all parameters
        for param_name, param in model.named_parameters(recurse=False):
            if param.device.type == 'cuda':
                full_name = f"{name}.{param_name}" if name != "model" else param_name
                gpu_items.append((full_name, "parameter", param.shape, param.numel(), param.device))
        
        # Check all buffers
        for buffer_name, buffer in model.named_buffers(recurse=False):
            if buffer.device.type == 'cuda':
                full_name = f"{name}.{buffer_name}" if name != "model" else buffer_name
                gpu_items.append((full_name, "buffer", buffer.shape, buffer.numel(), buffer.device))
        
        # Recursively check all child modules
        for child_name, child_module in model.named_children():
            child_full_name = f"{name}.{child_name}" if name != "model" else child_name
            child_gpu = _walk_model_for_gpu(child_module, child_full_name, depth + 1, indent)
            gpu_items.extend(child_gpu)
        
        # Check all attributes that might be tensors or modules
        for attr_name in dir(model):
            if attr_name.startswith('_'):
                continue
            try:
                attr = getattr(model, attr_name)
                if isinstance(attr, torch.nn.Module):
                    attr_full_name = f"{name}.{attr_name}" if name != "model" else attr_name
                    attr_gpu = _walk_model_for_gpu(attr, attr_full_name, depth + 1, indent)
                    gpu_items.extend(attr_gpu)
                elif isinstance(attr, torch.Tensor):
                    if attr.device.type == 'cuda':
                        attr_full_name = f"{name}.{attr_name}" if name != "model" else attr_name
                        gpu_items.append((attr_full_name, "tensor", attr.shape, attr.numel(), attr.device))
            except Exception:
                pass
    
    # Check if it's a tensor
    elif isinstance(model, torch.Tensor):
        if model.device.type == 'cuda':
            gpu_items.append((name, "tensor", model.shape, model.numel(), model.device))
    
    return gpu_items


def _log_gpu_memory(context: str = "", log_level=logging.INFO):
    """Quick GPU memory logging for tracing memory usage."""
    if not torch.cuda.is_available():
        return
    try:
        allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
        reserved = torch.cuda.memory_reserved() / (1024**3)  # GB
        max_allocated = torch.cuda.max_memory_allocated() / (1024**3)  # GB
        logger.log(log_level, f"📊 GPU MEMORY [{context}]: Allocated={allocated:.3f} GB, Reserved={reserved:.3f} GB, Peak={max_allocated:.3f} GB")
    except Exception as e:
        logger.debug(f"Could not log GPU memory: {e}")

def _dump_cuda_memory_usage(context: str = ""):
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
        
    except Exception as e:
        logger.warning(f"⚠️  Failed to dump CUDA memory usage: {e}")


def compute_binary_lift_bands(y_pred, y_true, n_bins=10):
    """
    Compute positive:negative ratio across probability bands (lift-style metric).
    
    This metric bins predictions by probability and computes the ratio of positive:negative
    class instances in each band. For a well-calibrated model, higher predicted probabilities
    should correspond to higher positive:negative ratios.
    
    Args:
        y_pred: array-like of predicted probabilities for positive class (float in [0,1])
        y_true: array-like of ground truth binary labels (1 = positive, 0 = negative)
        n_bins: number of probability bands (e.g. deciles)
    
    Returns:
        pandas.DataFrame with one row per band:
            - band: band label (interval)
            - avg_pred: mean predicted prob in band
            - n: number of samples in band
            - n_positive: count of positive class instances (y=1)
            - n_negative: count of negative class instances (y=0)
            - positive_negative_ratio: n_positive / n_negative (NaN if n_negative=0)
    """
    df = pd.DataFrame({
        "y_true": np.asarray(y_true),
        "y_pred": np.asarray(y_pred),
    })
    
    # Bin by predicted probability into quantiles (deciles by default)
    df["band"] = pd.qcut(df["y_pred"], q=n_bins, duplicates="drop")
    
    grouped = (
        df.groupby("band")
          .apply(lambda g: pd.Series({
              "avg_pred": g["y_pred"].mean(),
              "n": len(g),
              "n_positive": (g["y_true"] == 1).sum(),
              "n_negative": (g["y_true"] == 0).sum(),
          }))
    )
    
    # Avoid div-by-zero when no negative class instances in a band
    grouped["positive_negative_ratio"] = grouped["n_positive"] / grouped["n_negative"].replace(0, np.nan)
    
    # Sort by average predicted probability so the plot is monotone in x
    grouped = grouped.sort_values("avg_pred").reset_index()
    
    return grouped


class SPIdentifierFilter(logging.Filter):
    """Logging filter that prepends SP identifier and epoch to all log messages."""
    def __init__(self, identifier, sp_instance):
        super().__init__()
        self.identifier = identifier
        self.sp_instance = sp_instance  # Reference to FeatrixSinglePredictor for epoch tracking
    
    def filter(self, record):
        # Get current epoch and total epochs from the SP instance
        epoch = getattr(self.sp_instance, '_current_epoch', None)
        total_epochs = getattr(self.sp_instance, '_total_epochs', None)
        # ALWAYS prepend identifier and epoch to ALL messages
        if epoch is not None and epoch >= 0:
            if total_epochs is not None and total_epochs > 0:
                record.msg = f"[epoch={epoch}/{total_epochs}] {record.msg}"
            else:
                record.msg = f"[epoch={epoch}] {record.msg}"
        else:
            record.msg = f"[epoch=setup] {record.msg}"
        return True


class LearningRateTooLowError(Exception):
    """
    Exception raised when the model shows signs of learning too slowly 
    (zero gradients + constant probability outputs) and needs a higher learning rate.
    """
    def __init__(self, message, current_lr, suggested_lr_multiplier=2.0):
        self.current_lr = current_lr
        self.suggested_lr_multiplier = suggested_lr_multiplier
        super().__init__(message)


class TrainingFailureException(Exception):
    """Custom exception for training failures with retry recommendations."""
    def __init__(self, message, failure_type, retry_params=None):
        super().__init__(message)
        self.failure_type = failure_type
        self.retry_params = retry_params or {}


# async def dump_training_status(
#     status: Optional[JobIncrementalStatus], epoch_idx, batch_idx, status_callback=None
# ):
#     try:
#         logger.info(f"dump status: epoch_idx={epoch_idx} batch_idx={batch_idx} status= {json.dumps(status, indent=4, default=str)}")
#     except:
#         traceback.print_exc()
#         pass

#     # Why are we caching the status callback? 
#     # This can produce unexpected behavior on subsequent calls because
#     #  what happens on subsequent calls depends on earlier calls. 
#     if status_callback is not None:
#         setattr(dump_training_status, "status_callback", status_callback)

#     scb = getattr(dump_training_status, "status_callback", None)

#     if status:
#         try:
#             status.fix_times()
#             status.summarize_status()
#             if scb:
#                 await scb(status)
#                 logger.info(f".... scb ==> {status}")
#             else:
#                 logger.debug(status.message)
#                 sys.stdout.write(status.message)
#                 sys.stdout.flush()
#         except Exception:  # noqa
#             traceback.print_exc()
#             pass


class FeatrixSinglePredictor:
    def __init__(self, embedding_space: EmbeddingSpace, predictor, name: str = None, user_metadata: dict = None):
        self.d_model = embedding_space.d_model
        self.embedding_space = embedding_space
        # predictor_base should not have the final linear layer because the target
        # variable is not yet known, and we need to create the codec in order to figure
        # out its dimensionality.
        self.predictor_base = predictor
        # predictor is the full downstream prediction model, including the final output.
        self.predictor = None

        # Store name for identification and tracking
        self.name = name
        
        # Store user metadata for identification and tracking
        self.user_metadata = user_metadata
        
        self.target_col_type = None
        self.target_codec = None
        self.train_df = None
        self.target_type = None
        self.target_col_name = None

        # A dictionary to hold codecs from the embeddings space AND  the codec
        # for the target column.
        self.all_codecs = {}

        self.train_dataset = None
        self.is_target_scalar = None

        self.sm = nn.Softmax(dim=-1)
        self.training_metrics = None

        self.metrics_had_error = {}

        self.metrics_time = 0

        self.run_binary_metrics = True
        
        # Metadata about categories excluded from validation during training
        self.validation_excluded_categories = None
        
        # Distribution metadata for hyperparameter selection
        self.distribution_metadata = None
        
        # Training warnings tracker
        # Structure: {"warning_type": {"epochs": [list of epochs], "details": [list of detail dicts]}}
        self.training_warnings = {}
        
        # Run identifier for logging (set by test scripts)
        self.run_identifier = None
        
        # Track current epoch for logging
        self._current_epoch = -1  # -1 means pre-training/setup phase
        
        self.best_epoch_warnings = []  # Warnings that occurred at the best epoch
        
        # Adaptive FocalLoss parameters
        self.adaptive_loss_enabled = True  # Enable adaptive loss adjustment
        self.focal_gamma_history = []  # Track gamma adjustments
        self.focal_min_weight_history = []  # Track min_weight adjustments
        self.loss_adjustment_count = 0  # How many times we've adjusted
        self.last_loss_adjustment_epoch = -1  # Prevent too-frequent adjustments
        
        # Training timeline tracking (like ES training)
        self._training_timeline = []
        self._corrective_actions = []
        self._output_dir = None  # Will be set during training
        
        # Warning state tracking - track active warnings to detect start/stop
        self._active_warnings = {}  # {warning_type: {'start_epoch': int, 'details': dict}}
        
        # Dead gradient detection and restart mechanism
        self.dead_gradient_threshold = 1e-6  # Gradients below this are considered "dead"
        self.dead_gradient_epochs = []  # Track epochs with dead gradients
        self.training_restart_count = 0  # How many times we've restarted
        self.max_training_restarts = 2  # Maximum restarts allowed
        self.last_restart_epoch = -1  # Prevent too-frequent restarts
        
        # Class distribution metadata (for classification tasks)
        self.class_distribution = None  # Will store {'train': {...}, 'val': {...}, 'total': {...}}
        
        # Optimal threshold for binary classification (computed during training, used during prediction)
        self.optimal_threshold = None  # Threshold that maximizes F1 score on validation set (saved from best AUC epoch)
        self.optimal_threshold_history = []  # Track threshold over epochs: [(epoch, threshold, f1_score, auc), ...]
        self._pos_label = None  # Rare class label for binary classification (typically the minority class) - kept as _pos_label for pickle compatibility
        
        # Track best metrics for threshold selection (only save threshold when metrics improve)
        self._best_auc = -1.0  # Best AUC seen so far
        self._best_auc_epoch = -1  # Epoch with best AUC
        self._best_f1_at_best_auc = -1.0  # Best F1 score at the epoch with best AUC
        self._best_threshold_at_best_auc = None  # Threshold at the epoch with best AUC
        
        # Cost-based optimization parameters
        self.cost_false_positive = None  # Cost of false positive (set during prep_for_training)
        self.cost_false_negative = None  # Cost of false negative (set during prep_for_training)
        self._best_cost = float('inf')  # Best cost seen so far (for cost-based checkpoint selection)
        
        # Calibration parameters (automatically fitted after training)
        self.calibration_method = None  # 'temperature_scaling', 'platt', 'isotonic', or None
        self.calibration_temperature = None  # Temperature parameter (if method is 'temperature_scaling')
        self.calibration_platt_model = None  # Platt scaling model (if method is 'platt')
        self.calibration_isotonic_model = None  # Isotonic regression model (if method is 'isotonic')
        self.calibration_metrics = None  # Full calibration metrics including candidate_scores
    
    def __getstate__(self):
        """
        Custom pickle state - save only essential data using state_dict for models.
        Excludes large data (dataframes, queries, targets, datasets) to keep checkpoints small.
        Similar to EmbeddingSpace encoder state_dict approach.
        """
        # Large data attributes to exclude (should be loaded from original source, not checkpoint)
        EXCLUDE_LARGE_DATA = {
            'train_df', 'val_df', 'train_queries', 'val_queries', 
            'train_targets', 'val_targets', 'train_dataset', 'val_dataset',
            'embedding_space'  # Should be loaded separately
        }
        
        # Model attributes that should be saved as state_dict
        MODEL_ATTRIBUTES = {'predictor_base', 'predictor'}
        
        state = {}
        saved_keys = []
        skipped_keys = []
        
        for key, value in self.__dict__.items():
            # Skip None values
            if value is None:
                state[key] = None
                continue
            
            # Skip large data - these should not be in checkpoints
            if key in EXCLUDE_LARGE_DATA:
                logger.debug(f"Skipping {key} in checkpoint (large data - should be loaded separately)")
                skipped_keys.append(key)
                continue

            # Save models as state_dict (PyTorch-approved method)
            if key in MODEL_ATTRIBUTES and value is not None:
                if hasattr(value, 'state_dict'):
                    try:
                        state[key] = {
                            '__model_state_dict__': value.state_dict(),
                            '__model_class__': value.__class__.__name__
                        }
                        logger.debug(f"Saving {key} as state_dict()")
                        saved_keys.append(f"{key} (state_dict)")
                        continue
                    except Exception as e:
                        logger.warning(f"Failed to save {key} as state_dict(): {e}")
                        # Fall through to try other methods
                else:
                    logger.warning(f"{key} is not a PyTorch model, cannot save as state_dict")
                    # Fall through to try normal copy
            
            # For other attributes, try to copy (but skip if it's too large)
            try:
                # Check if it's a pandas DataFrame or similar large object
                if hasattr(value, '__class__'):
                    class_name = value.__class__.__name__
                    if 'DataFrame' in class_name or 'Series' in class_name:
                        logger.debug(f"Skipping {key} (DataFrame/Series - should not be in checkpoint)")
                        continue
                
                state[key] = copy.deepcopy(value)
            except (TypeError, AttributeError, NotImplementedError) as e:
                # For models that failed deepcopy, try state_dict
                if hasattr(value, 'state_dict'):
                    try:
                        state[key] = {
                            '__model_state_dict__': value.state_dict(),
                            '__model_class__': value.__class__.__name__
                        }
                        logger.debug(f"Saving {key} as state_dict() (deepcopy failed: {str(e)[:100]})")
                        continue
                    except Exception as save_err:
                        logger.warning(f"Failed to save {key} as state_dict(): {save_err}")
                
                # For other errors, try shallow copy as fallback
                try:
                    state[key] = copy.copy(value)
                except (TypeError, AttributeError, NotImplementedError):
                    logger.warning(f"Could not pickle {key}, excluding from state: {e}")
                    # Skip this attribute - it will be missing after unpickling
                    continue
        
        return state
    
    def __setstate__(self, state):
        """
        Custom unpickle state - restore models from state_dict.
        Models (predictor_base, predictor) are saved as state_dict to keep checkpoints small.
        Embedding_space and large data (dataframes, queries, targets) are excluded and should be loaded separately.
        """
        import torch.nn as nn
        
        # Store pending state_dicts for models that need to be restored
        pending_state_dicts = {}
        
        # First, restore all normal attributes (excluding models saved as state_dict)
        for key, value in state.items():
            # Check if this is a model saved as state_dict()
            if isinstance(value, dict) and '__model_state_dict__' in value:
                # Store the state_dict temporarily - we'll load it after all attributes are set
                pending_state_dicts[key] = value['__model_state_dict__']
                logger.debug(f"Storing state_dict for {key} (will load after attributes restored)")
                continue
            elif key == 'embedding_space':
                # embedding_space is excluded from checkpoint - should be loaded separately
                # Don't set it here, it will be set by the caller
                logger.debug(f"Skipping embedding_space in __setstate__ (should be loaded separately)")
                continue
            else:
                # Normal attribute - just set it
                self.__dict__[key] = value
        
        # Now restore models from state_dict() if they exist
        for key, state_dict in pending_state_dicts.items():
            if key in self.__dict__ and self.__dict__[key] is not None:
                if hasattr(self.__dict__[key], 'load_state_dict'):
                    try:
                        self.__dict__[key].load_state_dict(state_dict)
                        logger.info(f"✅ Restored {key} from state_dict()")
                    except Exception as e:
                        logger.warning(f"⚠️  Failed to restore {key} from state_dict(): {e}")
                        import traceback
                        logger.debug(traceback.format_exc())
                        # Model object exists but couldn't load state - keep existing model
                else:
                    logger.warning(f"⚠️  {key} exists but doesn't have load_state_dict method")
            else:
                # Model doesn't exist yet - store state_dict for later loading
                # This can happen if embedding_space is None and predictor_base wasn't created
                if not hasattr(self, '_pending_state_dicts'):
                    self._pending_state_dicts = {}
                self._pending_state_dicts[key] = state_dict
                logger.info(f"📦 Stored state_dict for {key} (model not yet created, will load when available)")
        
        # BACKWARD COMPATIBILITY: Set defaults for new attributes if missing from old pickles
        if 'optimal_threshold' not in state:
            self.optimal_threshold = None
        if 'optimal_threshold_history' not in state:
            self.optimal_threshold_history = []
        if '_pos_label' not in state:
            self._pos_label = None
        if '_best_auc' not in state:
            self._best_auc = -1.0
        if '_best_auc_epoch' not in state:
            self._best_auc_epoch = -1
        if '_best_f1_at_best_auc' not in state:
            self._best_f1_at_best_auc = -1.0
        if '_best_threshold_at_best_auc' not in state:
            self._best_threshold_at_best_auc = None
    
    def _log(self, level, msg, *args, **kwargs):
        """Log with optional run identifier prefix."""
        if self.run_identifier:
            msg = f"{self.run_identifier} {msg}"
        getattr(logger, level)(msg, *args, **kwargs)
    
    def _get_log_prefix(self, epoch_idx=None):
        """Generate consistent log prefix with epoch and target information."""
        parts = []
        if epoch_idx is not None:
            parts.append(f"epoch={epoch_idx}")
        if self.target_col_name:
            parts.append(f"target={self.target_col_name}")
        return ", ".join(parts) + ": " if parts else ""

    def record_training_warning(self, warning_type, epoch, details=None):
        """
        Record a training warning for later retrieval.
        
        Args:
            warning_type: Type of warning (e.g., "SINGLE_CLASS_BIAS", "LOW_AUC", etc.)
            epoch: Epoch number where warning occurred
            details: Optional dict with additional details about the warning
        """
        if warning_type not in self.training_warnings:
            self.training_warnings[warning_type] = {
                "epochs": [],
                "details": [],
                "first_seen": epoch,
                "last_seen": epoch,
                "count": 0
            }
        
        self.training_warnings[warning_type]["epochs"].append(epoch)
        self.training_warnings[warning_type]["details"].append(details or {})
        self.training_warnings[warning_type]["last_seen"] = epoch
        self.training_warnings[warning_type]["count"] += 1
    
    def adjust_focal_loss_for_bias(self, pred_counts, y_true_counts, epoch_idx):
        """
        Adaptively adjust FocalLoss parameters when detecting class prediction bias.
        
        This handles both over-correction (reverse bias) and under-learning scenarios:
        - REVERSE BIAS: Model predicts minority class too frequently → reduce gamma
        - UNDER-LEARNING: Model predicts minority class too rarely → increase gamma
        
        Args:
            pred_counts: dict of predicted class counts
            y_true_counts: dict of ground truth class counts  
            epoch_idx: current epoch number
            
        Returns:
            bool: True if adjustment was made, False otherwise
        """
        if not self.adaptive_loss_enabled:
            return False
        
        # Only adjust if we're using FocalLoss
        if not isinstance(self.target_codec.loss_fn, FocalLoss):
            return False
        
        # Prevent adjustments too frequently (need at least 5 epochs between adjustments)
        if epoch_idx - self.last_loss_adjustment_epoch < 5:
            return False
        
        # Max 5 adjustments per training run (increased from 3 to allow bidirectional adjustments)
        if self.loss_adjustment_count >= 5:
            return False
        
        # Calculate prediction distribution
        total_preds = sum(pred_counts.values())
        if total_preds == 0:
            return False
        pred_pcts = {k: (v / total_preds * 100) for k, v in pred_counts.items()}
        
        # Calculate ground truth distribution
        total_true = sum(y_true_counts.values())
        if total_true == 0:
            return False
        true_pcts = {k: (v / total_true * 100) for k, v in y_true_counts.items()}
        
        # Identify minority and majority classes in ground truth
        minority_class = min(true_pcts, key=true_pcts.get)
        majority_class = max(true_pcts, key=true_pcts.get)
        
        minority_true_pct = true_pcts[minority_class]
        minority_pred_pct = pred_pcts.get(minority_class, 0)
        majority_true_pct = true_pcts[majority_class]
        majority_pred_pct = pred_pcts.get(majority_class, 0)
        
        # Calculate bias ratios
        reverse_bias_ratio = minority_pred_pct / max(minority_true_pct, 0.1)  # Minority over-predicted
        under_learning_ratio = minority_true_pct / max(minority_pred_pct, 0.1)  # Minority under-predicted
        
        log_prefix = self._get_log_prefix(epoch_idx)
        logger.info(f"{log_prefix}📊 Bias Analysis at Epoch {epoch_idx}:")
        logger.info(f"{log_prefix}   Minority class '{minority_class}': {minority_true_pct:.1f}% in truth, {minority_pred_pct:.1f}% in predictions")
        logger.info(f"{log_prefix}   Majority class '{majority_class}': {majority_true_pct:.1f}% in truth, {majority_pred_pct:.1f}% in predictions")
        logger.info(f"{log_prefix}   Reverse bias ratio: {reverse_bias_ratio:.2f}x (>2.0 suggests over-correction)")
        logger.info(f"{log_prefix}   Under-learning ratio: {under_learning_ratio:.2f}x (>2.0 suggests under-learning)")
        
        current_loss = self.target_codec.loss_fn
        old_gamma = current_loss.gamma
        old_min_weight = current_loss.min_weight
        adjustment_made = False
        adjustment_type = None
        adjustment_details = {}
        
        # CASE 1: REVERSE BIAS - Model over-predicts minority class
        # Trigger if: minority predicted 2x+ more than ground truth AND minority >80% of predictions
        if reverse_bias_ratio > 2.0 and minority_pred_pct > 80:
            adjustment_type = "REVERSE_BIAS"
            
            # REDUCE gamma: Less focus on hard examples (minority class)
            # gamma=2.0 → 1.5 → 1.0 → 0.5 (approaches standard cross-entropy)
            new_gamma = max(0.5, old_gamma * 0.75)
            
            # INCREASE min_weight: Give more credit to easy examples (majority class)
            # min_weight=0.1 → 0.2 → 0.3 → 0.4 (up to 0.4 max)
            new_min_weight = min(0.4, old_min_weight + 0.1)
            
            logger.warning(f"{log_prefix}" + "=" * 80)
            logger.warning(f"{log_prefix}🔧 ADAPTIVE LOSS ADJUSTMENT #{self.loss_adjustment_count + 1} at Epoch {epoch_idx}")
            logger.warning(f"{log_prefix}" + "=" * 80)
            logger.warning(f"{log_prefix}⚠️  REVERSE BIAS DETECTED: Model over-predicts minority class")
            logger.warning(f"{log_prefix}   Minority class '{minority_class}' predicted {reverse_bias_ratio:.2f}x more than ground truth")
            logger.warning(f"{log_prefix}   Adjusting FocalLoss to reduce class weight effect:")
            logger.warning(f"{log_prefix}   • gamma: {old_gamma:.2f} → {new_gamma:.2f} (less focus on hard/minority examples)")
            logger.warning(f"{log_prefix}   • min_weight: {old_min_weight:.2f} → {new_min_weight:.2f} (more credit to easy/majority examples)")
            logger.warning(f"{log_prefix}" + "=" * 80)
            
            adjustment_details = {
                "reverse_bias_ratio": float(reverse_bias_ratio),
                "minority_class": str(minority_class),
                "minority_true_pct": float(minority_true_pct),
                "minority_pred_pct": float(minority_pred_pct),
            }
            adjustment_made = True
        
        # CASE 2: UNDER-LEARNING - Model under-predicts minority class
        # Trigger if: minority predicted <50% of ground truth AND minority <20% of predictions
        # AND we haven't already reduced gamma too much (gamma > 1.0)
        elif under_learning_ratio > 2.0 and minority_pred_pct < 20 and old_gamma < 3.5:
            adjustment_type = "UNDER_LEARNING"
            
            # INCREASE gamma: More focus on hard examples (minority class)
            # gamma=2.0 → 2.5 → 3.0 → 3.5 (increases focus on minority class)
            new_gamma = min(3.5, old_gamma * 1.25)
            
            # DECREASE min_weight: Give less credit to easy examples (majority class)
            # min_weight=0.1 → 0.05 (down to 0.05 min) - but only if it's above 0.1
            new_min_weight = max(0.05, old_min_weight - 0.05) if old_min_weight > 0.1 else old_min_weight
            
            logger.warning(f"{log_prefix}" + "=" * 80)
            logger.warning(f"{log_prefix}🔧 ADAPTIVE LOSS ADJUSTMENT #{self.loss_adjustment_count + 1} at Epoch {epoch_idx}")
            logger.warning(f"{log_prefix}" + "=" * 80)
            logger.warning(f"{log_prefix}⚠️  UNDER-LEARNING DETECTED: Model under-predicts minority class")
            logger.warning(f"{log_prefix}   Minority class '{minority_class}' predicted {under_learning_ratio:.2f}x less than ground truth")
            logger.warning(f"{log_prefix}   Adjusting FocalLoss to increase focus on minority class:")
            logger.warning(f"{log_prefix}   • gamma: {old_gamma:.2f} → {new_gamma:.2f} (more focus on hard/minority examples)")
            logger.warning(f"{log_prefix}   • min_weight: {old_min_weight:.2f} → {new_min_weight:.2f} (less credit to easy/majority examples)")
            logger.warning(f"{log_prefix}" + "=" * 80)
            
            adjustment_details = {
                "under_learning_ratio": float(under_learning_ratio),
                "minority_class": str(minority_class),
                "minority_true_pct": float(minority_true_pct),
                "minority_pred_pct": float(minority_pred_pct),
            }
            adjustment_made = True
        
        if adjustment_made:
            # Create new FocalLoss with adjusted parameters
            # Keep the same alpha (class weights) but adjust gamma and min_weight
            new_loss = FocalLoss(
                alpha=current_loss.alpha,
                gamma=new_gamma,
                min_weight=new_min_weight
            )
            
            # Move to same device as current loss
            if current_loss.alpha is not None:
                new_loss.alpha = current_loss.alpha.to(current_loss.alpha.device)
            
            # Update the loss function
            self.target_codec.loss_fn = new_loss
            
            # Track the adjustment
            self.focal_gamma_history.append((epoch_idx, old_gamma, new_gamma))
            self.focal_min_weight_history.append((epoch_idx, old_min_weight, new_min_weight))
            self.loss_adjustment_count += 1
            self.last_loss_adjustment_epoch = epoch_idx
            
            # LOG CORRECTIVE ACTION (like ES training does)
            corrective_action = {
                "epoch": epoch_idx,
                "trigger": adjustment_type,
                "action_type": "FOCAL_LOSS_ADJUSTMENT",
                "details": {
                    **adjustment_details,
                    "gamma_old": float(old_gamma),
                    "gamma_new": float(new_gamma),
                    "min_weight_old": float(old_min_weight),
                    "min_weight_new": float(new_min_weight),
                    "adjustment_number": self.loss_adjustment_count,
                    "pred_distribution": {str(k): int(v) for k, v in pred_counts.items()},
                    "true_distribution": {str(k): int(v) for k, v in y_true_counts.items()}
                }
            }
            self._corrective_actions.append(corrective_action)
            
            # Add to training timeline
            timeline_entry = {
                "epoch": epoch_idx,
                "event_type": "hyperparameter_change",
                "hyperparameter": "focal_loss",
                "changes": {
                    "gamma": {"old": float(old_gamma), "new": float(new_gamma)},
                    "min_weight": {"old": float(old_min_weight), "new": float(new_min_weight)}
                },
                "trigger": adjustment_type,
                "details": adjustment_details
            }
            if hasattr(self, '_training_timeline'):
                self._training_timeline.append(timeline_entry)
            
            logger.info(f"{log_prefix}✅ FocalLoss adjusted successfully. Will monitor for {5} more epochs before next adjustment.")
            
            return True
        
        return False
        
    def check_for_dead_gradients_and_raise(self, unclipped_norm, epoch_idx, current_lr):
        """
        Check for dead gradients and raise FeatrixRestartTrainingException if detected.
        
        This allows the training loop to catch the exception and restart training
        with modified parameters (boosted LR, reset optimizer state, etc.)
        
        Args:
            unclipped_norm: Unclipped gradient norm
            epoch_idx: Current epoch number
            current_lr: Current learning rate
            
        Raises:
            FeatrixRestartTrainingException: When dead gradients detected and restart needed
        """
        log_prefix = self._get_log_prefix(epoch_idx)
        
        # Check if gradients are dead
        if unclipped_norm >= self.dead_gradient_threshold:
            # Gradients are alive, clear history if any
            if self.dead_gradient_epochs:
                logger.info(f"{log_prefix}✅ Gradients recovered! Clearing dead gradient history.")
                self.dead_gradient_epochs = []
                # Track warning resolution
                self._track_warning_in_timeline(
                    epoch_idx=epoch_idx,
                    warning_type="DEAD_GRADIENTS",
                    is_active=False,
                    details={
                        "gradient_norm": float(unclipped_norm),
                        "lr": current_lr,
                        "recovered": True
                    }
                )
            return
        
        # Track dead gradient epochs
        was_dead = len(self.dead_gradient_epochs) > 0
        self.dead_gradient_epochs.append(epoch_idx)
        logger.warning(f"{log_prefix}⚠️  Dead gradient detected at epoch {epoch_idx} (norm={unclipped_norm:.6e})")
        
        # Track warning start if this is the first detection
        if not was_dead:
            self._track_warning_in_timeline(
                epoch_idx=epoch_idx,
                warning_type="DEAD_GRADIENTS",
                is_active=True,
                details={
                    "gradient_norm": float(unclipped_norm),
                    "lr": current_lr,
                    "threshold": self.dead_gradient_threshold
                }
            )
        
        # Check if we have consecutive dead gradients (3+ in a row = trigger restart)
        if len(self.dead_gradient_epochs) < 3:
            logger.info(f"{log_prefix}   Dead gradient count: {len(self.dead_gradient_epochs)}/3 (need 3 consecutive to restart)")
            return
        
        recent_dead = self.dead_gradient_epochs[-3:]
        # Check if last 3 dead gradient epochs are consecutive (within 2 epochs)
        if recent_dead[-1] - recent_dead[0] > 2:
            logger.info(f"{log_prefix}   Last 3 dead gradients not consecutive: {recent_dead} (skipping restart)")
            return
        
        # Check restart limits
        if self.training_restart_count >= self.max_training_restarts:
            logger.error(f"{log_prefix}💀 Dead gradients detected but max restarts ({self.max_training_restarts}) reached - cannot restart")
            logger.error(f"{log_prefix}   Training will continue with dead gradients (likely to fail)")
            return
        
        # Need cooldown between restarts (skip cooldown if never restarted before)
        if self.last_restart_epoch >= 0 and epoch_idx - self.last_restart_epoch < 5:
            logger.info(f"{log_prefix}   Too soon since last restart (epoch {self.last_restart_epoch}) - need 5 epoch cooldown")
            return
        
        # All conditions met - prepare restart!
        logger.error(f"{log_prefix}💀 DEAD GRADIENTS: {len(self.dead_gradient_epochs)} total, last 3 consecutive {recent_dead}")
        logger.error(f"{log_prefix}   🔄 Raising FeatrixRestartTrainingException to restart training...")
        
        # Create restart configuration
        restart_config = RestartConfig(
            reason="DEAD_GRADIENTS",
            epoch_detected=epoch_idx,
            lr_multiplier=5.0,
            max_lr=0.01,
            reset_optimizer_state=True,
            reset_scheduler=False,
            load_best_checkpoint=False,  # Continue from current weights
            additional_epochs=None,  # Don't extend training
            metadata={
                "dead_gradient_epochs": list(self.dead_gradient_epochs[-5:]),  # Last 5
                "gradient_norm": float(unclipped_norm),
                "current_lr": float(current_lr),
                "restart_number": self.training_restart_count + 1
            }
        )
        
        # Raise exception - training loop will catch and restart
        raise FeatrixRestartTrainingException(
            f"Dead gradients detected at epoch {epoch_idx} ({len(recent_dead)} consecutive)",
            restart_config=restart_config
        )
    
    def _track_warning_in_timeline(self, epoch_idx, warning_type, is_active, details=None):
        """
        Track warnings in timeline - add entries when warnings start/stop.
        
        Args:
            epoch_idx: Current epoch number
            warning_type: Type of warning (e.g., 'DEAD_GRADIENTS', 'NO_LEARNING')
            is_active: True if warning is currently active, False if resolved
            details: Dict with warning-specific details (loss values, gradients, etc.)
        """
        if not hasattr(self, '_active_warnings'):
            self._active_warnings = {}
        
        if details is None:
            details = {}
        
        was_active = warning_type in self._active_warnings
        
        if is_active and not was_active:
            # Warning just started
            from datetime import datetime
            from zoneinfo import ZoneInfo
            warning_entry = {
                "epoch": epoch_idx,
                "timestamp": datetime.now(tz=ZoneInfo("America/New_York")).isoformat(),
                "event_type": "warning_start",
                "warning_type": warning_type,
                "description": f"{warning_type} warning detected",
                "details": details.copy()
            }
            self._training_timeline.append(warning_entry)
            self._active_warnings[warning_type] = {
                'start_epoch': epoch_idx,
                'details': details.copy()
            }
            logger.info(f"📊 Timeline: {warning_type} warning started at epoch {epoch_idx}")
            
        elif not is_active and was_active:
            # Warning just resolved
            from datetime import datetime
            from zoneinfo import ZoneInfo
            start_epoch = self._active_warnings[warning_type]['start_epoch']
            duration = epoch_idx - start_epoch
            
            warning_entry = {
                "epoch": epoch_idx,
                "timestamp": datetime.now(tz=ZoneInfo("America/New_York")).isoformat(),
                "event_type": "warning_resolved",
                "warning_type": warning_type,
                "description": f"{warning_type} warning resolved",
                "start_epoch": start_epoch,
                "duration_epochs": duration,
                "details": details.copy() if details else {}
            }
            self._training_timeline.append(warning_entry)
            del self._active_warnings[warning_type]
            logger.info(f"📊 Timeline: {warning_type} warning resolved at epoch {epoch_idx} (duration: {duration} epochs)")
            
        elif is_active and was_active:
            # Warning still active - update details but don't add new entry
            self._active_warnings[warning_type]['details'].update(details)
    
    def save_training_timeline(self, output_dir=None, current_epoch=None, total_epochs=None):
        """
        Save training timeline and corrective actions to JSON file (like ES training).
        
        Args:
            output_dir: Directory to save timeline JSON (default: self._output_dir)
            current_epoch: Current epoch number for logging
            total_epochs: Total number of epochs
        """
        import json
        import pandas as pd
        
        if output_dir is None:
            output_dir = self._output_dir
        
        if output_dir is None:
            # No output directory set, skip saving
            return
        
        try:
            # Build metadata
            metadata = {
                "total_epochs": total_epochs,
                "adaptive_loss_enabled": self.adaptive_loss_enabled,
                "loss_adjustments": self.loss_adjustment_count,
                "training_restarts": self.training_restart_count,
                "dead_gradient_threshold": self.dead_gradient_threshold,
                "target_col_name": self.target_col_name,
                "target_col_type": str(self.target_col_type) if self.target_col_type else None
            }
            
            # Add detailed target column distribution information
            if self.train_df is not None and self.target_col_name and self.target_col_name in self.train_df.columns:
                target_col = self.train_df[self.target_col_name]
                
                # Common info for both set and scalar
                total_rows = len(self.train_df)
                notna_count = target_col.notna().sum()
                notna_pct = (notna_count / total_rows * 100) if total_rows > 0 else 0.0
                null_count = target_col.isnull().sum()
                null_pct = (null_count / total_rows * 100) if total_rows > 0 else 0.0
                
                metadata["target_column_distribution"] = {
                    "total_rows": int(total_rows),
                    "notna_count": int(notna_count),
                    "notna_percentage": float(notna_pct),
                    "null_count": int(null_count),
                    "null_percentage": float(null_pct)
                }
                
                # For set targets: add value_counts() info
                if self.target_col_type == "set" or (hasattr(self, 'is_target_scalar') and not self.is_target_scalar):
                    value_counts = target_col.value_counts()
                    # Convert to dict with string keys for JSON serialization
                    value_counts_dict = {}
                    for label, count in value_counts.items():
                        # Convert label to string for JSON compatibility
                        label_str = str(label)
                        value_counts_dict[label_str] = {
                            "count": int(count),
                            "percentage": float((count / notna_count * 100) if notna_count > 0 else 0.0)
                        }
                    
                    metadata["target_column_distribution"]["value_counts"] = value_counts_dict
                    metadata["target_column_distribution"]["unique_values"] = int(target_col.nunique())
                
                # For scalar targets: add distribution statistics
                elif self.target_col_type == "scalar" or (hasattr(self, 'is_target_scalar') and self.is_target_scalar):
                    # Get non-null values for statistics
                    non_null_values = target_col.dropna()
                    if len(non_null_values) > 0:
                        metadata["target_column_distribution"]["statistics"] = {
                            "mean": float(non_null_values.mean()),
                            "std": float(non_null_values.std()) if len(non_null_values) > 1 else 0.0,
                            "min": float(non_null_values.min()),
                            "max": float(non_null_values.max()),
                            "median": float(non_null_values.median()),
                            "q25": float(non_null_values.quantile(0.25)),
                            "q75": float(non_null_values.quantile(0.75)),
                            "unique_values": int(non_null_values.nunique())
                        }
                    else:
                        metadata["target_column_distribution"]["statistics"] = {
                            "mean": None,
                            "std": None,
                            "min": None,
                            "max": None,
                            "median": None,
                            "q25": None,
                            "q75": None,
                            "unique_values": 0
                        }
            
            timeline_path = os.path.join(output_dir, "sp_training_timeline.json")
            with open(timeline_path, 'w') as f:
                json.dump({
                    "timeline": self._training_timeline,
                    "corrective_actions": self._corrective_actions,
                    "metadata": metadata
                }, f, indent=2)
            
            if current_epoch is not None:
                logger.debug(f"💾 SP training timeline saved to {timeline_path} (epoch {current_epoch})")
        except Exception as e:
            logger.warning(f"⚠️  Failed to save SP training timeline: {e}")
            import traceback
            logger.debug(traceback.format_exc())
        
    def get_model_warnings(self, include_epoch_details=False):
        """
        Get all training warnings that were recorded during model training.
        
        Args:
            include_epoch_details: If True, includes the full list of epochs and details.
                                  If False, returns a summary.
        
        Returns:
            dict: Dictionary of warnings with their metadata
        """
        if not self.training_warnings:
            return {}
        
        if include_epoch_details:
            return {
                "warnings": self.training_warnings,
                "best_epoch_warnings": self.best_epoch_warnings
            }
        else:
            # Return summary without full epoch lists
            summary = {}
            for warning_type, data in self.training_warnings.items():
                summary[warning_type] = {
                    "first_seen": data["first_seen"],
                    "last_seen": data["last_seen"],
                    "count": data["count"],
                    "occurred_at_best_epoch": warning_type in [w["type"] for w in self.best_epoch_warnings]
                }
            return summary
    
    def has_warnings(self):
        """Check if any warnings were recorded during training."""
        return len(self.training_warnings) > 0 or self.has_training_quality_issues()
    
    def has_training_quality_issues(self):
        """Check if final training metrics indicate quality issues."""
        if not self.training_metrics:
            return False
        return self.training_metrics.get('failure_detected', False)
    
    def get_training_quality_warning(self):
        """Get training quality warning message if any."""
        if not self.has_training_quality_issues():
            return None
        
        failure_label = self.training_metrics.get('failure_label', 'UNKNOWN')
        recommendations = list(self.training_metrics.get('recommendations', []))  # Make a copy
        
        warning = {
            "type": "TRAINING_QUALITY_ISSUE",
            "severity": "HIGH",
            "failure_mode": failure_label,
            "message": f"Model training completed with quality issues: {failure_label}",
            "recommendations": recommendations,
            "details": {
                "auc": self.training_metrics.get('auc', 0),
                "accuracy": self.training_metrics.get('accuracy', 0),
                "f1": self.training_metrics.get('f1', 0),
            }
        }
        
        # Add class distribution if available (for classification tasks)
        if self.class_distribution:
            warning["class_distribution"] = self.class_distribution
            
            # Add a human-readable summary of the class imbalance
            if self.training_metrics.get('is_binary', False):
                # For binary classification, compute imbalance ratio
                total_counts = self.class_distribution['total']
                labels = sorted(total_counts.keys())
                if len(labels) == 2:
                    majority_count = max(total_counts.values())
                    minority_count = min(total_counts.values())
                    if minority_count > 0:
                        imbalance_ratio = majority_count / minority_count
                        warning["imbalance_ratio"] = round(imbalance_ratio, 2)
                        warning["minority_class_count"] = minority_count
                        warning["majority_class_count"] = majority_count
                        
                        # Add contextual message
                        if minority_count < 10:
                            warning["data_sufficiency"] = "INSUFFICIENT - Need at least 50-100 examples of minority class"
                            recommendations.append(f"→ Training data has only {minority_count} positive examples (out of {self.class_distribution['total_total']} total) - need at least 50-100 for reliable training")
                        elif minority_count < 50:
                            warning["data_sufficiency"] = "LOW - Model may struggle with so few minority examples"
                            recommendations.append(f"→ Training data has only {minority_count} positive examples (out of {self.class_distribution['total_total']} total) - consider collecting more data")
                        elif imbalance_ratio > 20:
                            warning["data_sufficiency"] = "IMBALANCED - Large class imbalance may affect performance"
                            recommendations.append(f"→ Class imbalance is {imbalance_ratio:.1f}:1 ({majority_count} vs {minority_count} examples) - model may be biased toward majority class")
                        else:
                            warning["data_sufficiency"] = "ADEQUATE"
                        
                        # Update recommendations in the warning
                        warning["recommendations"] = recommendations
        
        return warning
    
    def get_warning_summary(self):
        """Get a human-readable summary of warnings."""
        if not self.training_warnings:
            return "No warnings recorded during training."
        
        lines = [f"Training completed with {len(self.training_warnings)} warning type(s):"]
        for warning_type, data in self.training_warnings.items():
            count = data["count"]
            first = data["first_seen"]
            last = data["last_seen"]
            lines.append(f"  - {warning_type}: occurred {count} time(s) (epochs {first}-{last})")
            
            # Check if warning was at best epoch
            if warning_type in [w["type"] for w in self.best_epoch_warnings]:
                lines.append(f"    ⚠️  Warning persisted at best model epoch!")
        
        return "\n".join(lines)


    def hydrate_to_cpu_if_needed(self):
        if self.predictor:
            logger.info("predictor going to cpu")
            self.predictor.to(torch.device("cpu"))
        else:
            logger.info("no predictor for cpu")
        return

    def hydrate_to_gpu_if_needed(self):
        # ENABLED: Move predictor to GPU if available
        if torch.cuda.is_available():
            if self.predictor is not None:
                current_device = next(self.predictor.parameters()).device if list(self.predictor.parameters()) else None
                if current_device is None or current_device.type != 'cuda':
                    logger.info("🔄 Moving predictor to GPU...")
                    self.predictor = self.predictor.cuda()
                    logger.info(f"✅ Predictor moved to GPU: {next(self.predictor.parameters()).device}")
                else:
                    logger.debug(f"✅ Predictor already on GPU: {current_device}")
            
            # Also move predictor_base if it exists
            if hasattr(self, 'predictor_base') and self.predictor_base is not None:
                current_device = next(self.predictor_base.parameters()).device if list(self.predictor_base.parameters()) else None
                if current_device is None or current_device.type != 'cuda':
                    self.predictor_base = self.predictor_base.cuda()
        else:
            logger.debug("CPU mode - CUDA not available")

    def cleanup_gpu_memory(self):
        """
        Clean up GPU memory used by this single predictor.
        This should be called after training or prediction to free GPU resources.
        """
        try:
            # Move models to CPU first to free GPU memory
            if self.predictor is not None:
                logger.info("Moving predictor to CPU for cleanup")
                self.predictor.cpu()
            
            if self.predictor_base is not None:
                logger.info("Moving predictor_base to CPU for cleanup")
                self.predictor_base.cpu()
            
            # Move codecs to CPU if they have tensors
            if hasattr(self, 'target_codec') and self.target_codec is not None:
                if hasattr(self.target_codec, 'cpu'):
                    self.target_codec.cpu()
            
            if hasattr(self, 'all_codecs') and self.all_codecs:
                for codec_name, codec in self.all_codecs.items():
                    if hasattr(codec, 'cpu'):
                        codec.cpu()
            
            # Force PyTorch GPU memory cleanup
            try:
                # torch is already imported at module level
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    torch.cuda.synchronize()
                    logger.info("GPU memory cache cleared")
            except ImportError:
                pass  # PyTorch not available
            
            # Force garbage collection
            import gc
            gc.collect()
            logger.info("Python garbage collection completed")
            
        except Exception as cleanup_error:
            logger.warning(f"GPU cleanup failed: {cleanup_error}")
            import traceback
            traceback.print_exc()

    def _probs_dict(self, probs) -> Dict:
        return {
            self.target_codec.detokenize(Token(value=i, status=2)): prob.item()
            for i, prob in enumerate(probs)
        }

    def _compute_class_weights(self, target_col, class_imbalance=None):
        """
        Compute class weights for imbalanced classification.
        
        Uses square root of inverse frequency weighting to prevent over-correction:
        weight = sqrt(1 / frequency)
        
        This is gentler than full inverse frequency and prevents models from 
        over-predicting the minority class.
        
        Args:
            target_col: pandas Series containing the target column values
            class_imbalance: Optional dict with expected class ratios/counts from real world.
                           If provided, uses these instead of the training data distribution.
                           Can be ratios (e.g., {"good": 0.97, "bad": 0.03}) or counts (e.g., {"good": 9700, "bad": 300})
            
        Returns:
            dict mapping class names to weights
        """
        try:
            # If class_imbalance is provided, use it instead of training data distribution
            if class_imbalance is not None:
                logger.info("📊 Using provided class_imbalance for class weighting")
                logger.info(f"   Provided class_imbalance: {class_imbalance}")
                
                # Convert to frequencies (normalize if needed)
                total = sum(class_imbalance.values())
                class_frequencies = {k: v / total for k, v in class_imbalance.items()}
                
                # Log the expected class distribution
                logger.info("📊 Expected Class Distribution (from class_imbalance):")
                for class_name, freq in class_frequencies.items():
                    logger.info(f"   '{class_name}': {freq*100:.1f}%")
                
                # Compute SQRT of inverse frequency weights (gentler than full inverse)
                class_weights_dict = {}
                for class_name, freq in class_frequencies.items():
                    weight = np.sqrt(1.0 / freq)
                    class_weights_dict[class_name] = weight
                
                # Normalize weights so they average to 1.0
                avg_weight = sum(class_weights_dict.values()) / len(class_weights_dict)
                class_weights_dict = {k: v / avg_weight for k, v in class_weights_dict.items()}
                
                # Log computed weights
                logger.info("⚖️  Computed Class Weights (sqrt method, from class_imbalance):")
                for class_name, weight in class_weights_dict.items():
                    logger.info(f"   '{class_name}': {weight:.4f}")
                
                return class_weights_dict
            
            # Otherwise use the training data distribution (original behavior)
            # Get value counts directly from the target column
            value_counts = target_col.astype(str).value_counts()
            
            # Filter out NaN-like values
            nan_variants = {'nan', 'NaN', 'Nan', 'NAN', 'None', '', ' '}
            value_counts = value_counts[~value_counts.index.isin(nan_variants)]
            
            if len(value_counts) == 0:
                logger.warning("⚠️  No valid class values found for class weighting")
                return {}
            
            # Compute total samples
            total_samples = value_counts.sum()
            
            # Compute class frequencies
            class_frequencies = value_counts / total_samples
            
            # Log class distribution
            logger.info("📊 Class Distribution for Target Column:")
            for class_name, freq in class_frequencies.items():
                count = value_counts[class_name]
                logger.info(f"   '{class_name}': {count} samples ({freq*100:.1f}%)")
            
            # Compute SQRT of inverse frequency weights (gentler than full inverse)
            # For 5:1 imbalance (84%/16%), this gives ~2.35x ratio instead of 5.5x
            class_weights_dict = {}
            for class_name in value_counts.index:
                freq = class_frequencies[class_name]
                weight = np.sqrt(1.0 / freq)
                class_weights_dict[class_name] = weight
            
            # Normalize weights so they average to 1.0
            avg_weight = sum(class_weights_dict.values()) / len(class_weights_dict)
            class_weights_dict = {k: v / avg_weight for k, v in class_weights_dict.items()}
            
            # Log computed weights with comparison to full inverse frequency
            logger.info("⚖️  Computed Class Weights (sqrt method, normalized):")
            for class_name, weight in class_weights_dict.items():
                freq = class_frequencies[class_name]
                full_inverse = (1.0 / freq) / ((1.0 / class_frequencies).sum() / len(class_frequencies))
                logger.info(f"   '{class_name}': {weight:.4f} (vs {full_inverse:.4f} with full inverse)")
            
            return class_weights_dict
            
        except Exception as e:
            logger.warning(f"⚠️  Failed to compute class weights: {e}")
            logger.warning("   Continuing without class weighting")
            return {}

    def prep_for_training(self, train_df, target_col_name, target_col_type, use_class_weights=True, loss_type="focal", class_imbalance=None, cost_false_positive=None, cost_false_negative=None):
        # we need to get the target codec set up and the predictor mapped to the right dimensionality.
        logger.info("=" * 80)
        logger.info("🎯 PREP_FOR_TRAINING CALLED - START")
        logger.info(f"🎯 Module: {self.__class__.__module__}")
        logger.info(f"🎯 File: {__file__}")
        logger.info(f"🎯 target_col_name: {target_col_name}")
        logger.info(f"🎯 target_col_type: {target_col_type}")
        logger.info(f"🎯 use_class_weights: {use_class_weights}")
        logger.info(f"🎯 class_imbalance: {class_imbalance}")
        logger.info(f"🎯 cost_false_positive: {cost_false_positive}")
        logger.info(f"🎯 cost_false_negative: {cost_false_negative}")
        logger.info("=" * 80)
        
        # For set (classification) columns, compute default costs if not provided
        if target_col_type == "set":
            if cost_false_positive is None or cost_false_negative is None:
                # Compute default costs based on class imbalance
                target_col = train_df[target_col_name]
                
                # Count positives and negatives
                # Positive is typically the minority class (rare_label_value)
                # For now, we'll use the class with fewer samples as positive
                value_counts = target_col.value_counts()
                if len(value_counts) == 2:
                    # Binary classification
                    pos_count = value_counts.min()  # Minority class
                    neg_count = value_counts.max()  # Majority class
                    imbalance_ratio = neg_count / pos_count if pos_count > 0 else 1.0
                    
                    # Default cost calculation: cost_fp = 1.0, cost_fn = imbalance_ratio
                    cost_false_positive = 1.0
                    cost_false_negative = imbalance_ratio
                    
                    logger.info(f"💰 Default cost calculation (Bayes-optimal for imbalanced data):")
                    logger.info(f"   Positive class count: {pos_count}")
                    logger.info(f"   Negative class count: {neg_count}")
                    logger.info(f"   Imbalance ratio: {imbalance_ratio:.2f}")
                    logger.info(f"   cost_false_positive = {cost_false_positive:.2f}")
                    logger.info(f"   cost_false_negative = {cost_false_negative:.2f}")
                else:
                    # Multi-class: use symmetric costs
                    cost_false_positive = 1.0
                    cost_false_negative = 1.0
                    logger.info(f"💰 Multi-class classification: using symmetric costs (FP=1.0, FN=1.0)")
            else:
                # Validate provided costs
                if cost_false_positive <= 0 or cost_false_negative <= 0:
                    raise ValueError("cost_false_positive and cost_false_negative must be positive numbers")
                logger.info(f"💰 User-provided costs: FP cost={cost_false_positive}, FN cost={cost_false_negative}")
            
            self.cost_false_positive = cost_false_positive
            self.cost_false_negative = cost_false_negative
        else:
            # Scalar (regression): costs don't apply
            self.cost_false_positive = None
            self.cost_false_negative = None
        
        # Always use focal loss for classification (better for imbalanced data)
        if target_col_type == "set":
            loss_type = "focal"
        
        logger.debug(
            "prep_for_training: %s is a %s" % (target_col_name, target_col_type)
        )

        # CRITICAL: Normalize target column to consistent type BEFORE any processing
        # This prevents "1" vs "1.0" from being treated as different classes
        target_col = train_df[target_col_name].copy()
        
        # Convert to string first, then normalize numeric strings
        # This handles: 1, 1.0, "1", "1.0" all becoming "1"
        target_col_str = target_col.astype(str)
        
        # Normalize numeric strings: "1.0" -> "1", "0.0" -> "0"
        def normalize_numeric_string(val):
            if pd.isna(val) or val in ['nan', 'NaN', 'None', '', ' ']:
                return val
            try:
                # Try to convert to float, then back to int if it's a whole number
                float_val = float(val)
                if float_val.is_integer():
                    return str(int(float_val))
                return str(float_val)
            except (ValueError, TypeError):
                # Not numeric, return as-is
                return str(val)
        
        target_col_normalized = target_col_str.apply(normalize_numeric_string)
        
        # Update the dataframe with normalized target column
        train_df = train_df.copy()
        train_df[target_col_name] = target_col_normalized
        
        logger.info(f"🔧 Normalized target column '{target_col_name}' to consistent string type")
        logger.info(f"   Unique values after normalization: {sorted(target_col_normalized.unique())}")
        
        self.train_df = train_df
        self.target_col_name = target_col_name

        assert target_col_name in train_df.columns.values, (
            "__%s__ is not found in the list of columns __%s__"
            % (
                target_col_name,
                train_df.columns.values,
            )
        )

        if target_col_name in self.embedding_space.col_codecs:
            warnings.warn(
                f"""Overwriting an existing codec for column {target_col_name} from the training dataset. This may cause unexpected behavior. Also, presence of the target column in the training dataset may lead to data leakage and poor inference results."""
            )

        # The DF for downstream training must have at least one independent variable to base
        # the predictions on. We exclude the target column from the count since we need
        # feature columns to predict the target.
        cols_for_coding_count = self.embedding_space.get_columns_with_codec_count(exclude_target_column=target_col_name)
        
        # Log debug info
        total_codecs = len(self.embedding_space.col_codecs) if self.embedding_space.col_codecs else 0
        target_in_codecs = target_col_name in (self.embedding_space.col_codecs or {})
        logger.warning(f"🔍 Column codec check: total_codecs={total_codecs}, target_in_codecs={target_in_codecs}, feature_codecs={cols_for_coding_count}")
        if self.embedding_space.col_codecs:
            logger.warning(f"   Available codec columns: {list(self.embedding_space.col_codecs.keys())[:20]}{'...' if len(self.embedding_space.col_codecs) > 20 else ''}")
        
        if cols_for_coding_count < 1:
            raise Exception(
                f"Input data does not contain at least 1 feature column we can encode (found {cols_for_coding_count} feature columns, {total_codecs} total codecs). "
                f"Target column '{target_col_name}' {'is' if target_in_codecs else 'is not'} in codecs. "
                f"Please ensure the embedding space was trained on data with at least one feature column besides the target."
            )

        self.target_col_type = target_col_type

        # compute the target codec
        # TODO: I don't think we need a full-on codec here, just a tokenizer should be sufficient.
        #       But this means we need to create a separate tokenizer class.
        # Target column is already normalized above - use it directly
        target_col = self.train_df[target_col_name]
        if target_col_type == "set":
            # Compute class weights for imbalanced datasets (if enabled)
            class_weights_dict = {}
            if use_class_weights:
                class_weights_dict = self._compute_class_weights(target_col, class_imbalance=class_imbalance)
                logger.info(f"⚖️  Class weighting: ENABLED")
            else:
                logger.info(f"⚖️  Class weighting: DISABLED")
            
            # Create the codec with configurable loss type
            # FocalLoss: Better for imbalanced classification tasks (default)
            # CrossEntropyLoss: More stable for balanced data
            self.target_codec = create_set_codec(target_col, embed_dim=self.d_model, loss_type=loss_type)
            # Keep on GPU if available
            if torch.cuda.is_available():
                self.target_codec = self.target_codec.cuda()
            logger.info(f"SET target members = {self.target_codec.members}")
            
            # Now convert class weights dict to tensor indexed by token ID
            if class_weights_dict and use_class_weights:
                n_classes = len(self.target_codec.members)
                class_weights_tensor = torch.ones(n_classes, dtype=torch.float32)
                
                for class_name, weight in class_weights_dict.items():
                    # Get the token ID for this class
                    if class_name in self.target_codec.members_to_tokens:
                        token_id = self.target_codec.members_to_tokens[class_name]
                        class_weights_tensor[token_id] = weight
                
                # Set <UNKNOWN> weight to 0 so it doesn't contribute to loss
                # (we should never predict UNKNOWN in training)
                unknown_token = self.target_codec.members_to_tokens.get('<UNKNOWN>', 0)
                class_weights_tensor[unknown_token] = 0.0
                
                # Keep class weights on same device as model
                if torch.cuda.is_available():
                    class_weights_tensor = class_weights_tensor.cuda()
                
                # Apply class weights to the appropriate loss function
                if loss_type == "focal":
                    # Update FocalLoss with class weights via alpha parameter
                    self.target_codec.loss_fn = FocalLoss(alpha=class_weights_tensor, gamma=2.0, min_weight=0.1)
                    logger.info("🎯 Using FocalLoss with class weights")
                elif loss_type == "cross_entropy":
                    # Compute adaptive label smoothing based on dataset size and class distribution
                    # Label smoothing helps prevent overconfidence and improves generalization
                    label_smoothing = 0.0  # Default: no smoothing
                    
                    # Use distribution metadata if available for smart smoothing
                    if hasattr(self, 'distribution_metadata') and self.distribution_metadata is not None:
                        train_samples = self.distribution_metadata.get('train_samples', len(train_df))
                        n_classes = self.distribution_metadata.get('n_classes', 2)
                        imbalance_score = self.distribution_metadata.get('imbalance_score', 1.0)
                        
                        # Apply label smoothing for:
                        # 1. Small datasets (< 1000 samples) - helps prevent overfitting
                        # 2. Imbalanced datasets (score < 0.5) - prevents overconfidence on majority class
                        # 3. Many classes (>10) - smooths decision boundaries
                        
                        if train_samples < 500:
                            # Very small dataset - more aggressive smoothing
                            label_smoothing = 0.1
                            logger.info(f"📊 Small dataset ({train_samples} samples) → label_smoothing=0.1")
                        elif train_samples < 1000:
                            # Small dataset - moderate smoothing
                            label_smoothing = 0.05
                            logger.info(f"📊 Small dataset ({train_samples} samples) → label_smoothing=0.05")
                        elif imbalance_score < 0.33:
                            # Imbalanced dataset - light smoothing to prevent overconfidence
                            label_smoothing = 0.05
                            logger.info(f"📊 Imbalanced dataset (score={imbalance_score:.3f}) → label_smoothing=0.05")
                        elif n_classes > 10:
                            # Many classes - very light smoothing
                            label_smoothing = 0.02
                            logger.info(f"📊 Many classes ({n_classes}) → label_smoothing=0.02")
                        else:
                            logger.info(f"📊 Balanced dataset → no label smoothing")
                    
                    # Update CrossEntropyLoss with class weights and label smoothing
                    self.target_codec.loss_fn = nn.CrossEntropyLoss(
                        weight=class_weights_tensor,
                        label_smoothing=label_smoothing
                    )
                    logger.info(f"🎯 Using CrossEntropyLoss with class weights and label_smoothing={label_smoothing}")
                
                # Log class weights for transparency
                logger.info("⚖️  Class Weights Applied:")
                for member, token in self.target_codec.members_to_tokens.items():
                    if token < len(class_weights_tensor):
                        logger.info(f"   '{member}' (token {token}): weight = {class_weights_tensor[token].item():.4f}")
            
            target_dim = len(self.target_codec.members)
        elif target_col_type == "scalar":
            self.target_codec = create_scalar_codec(target_col, embed_dim=self.d_model)
            # Keep on GPU if available
            if torch.cuda.is_available():
                self.target_codec = self.target_codec.cuda()
            target_dim = 1
        else:
            raise ValueError(
                f"Cannot create codec for column of type {target_col_type}."
            )

        self.target_type = self.target_codec.token_dtype
        logger.debug(f"self.target_type...{target_col_name} -> {self.target_type}")
        # figure out the dimensionality of the last layer of the predictor.
        # we know the input dimensionality
        # Create dummy input on device
        dummy_input = torch.randn(1, self.d_model)
        if torch.cuda.is_available():
            dummy_input = dummy_input.cuda()
        # Use eval mode on the predictor to prevent contaminating the
        # batch norm stats with the dummy data.
        # This is also needed since we're passing in a batch of size 1,
        # which doesn't work with batch norm in training mode.

        # Keep predictor_base on device
        if torch.cuda.is_available():
            self.predictor_base = self.predictor_base.cuda()
        logger.info("Setting predictor_base.eval()")
        self.predictor_base.eval()
        dummy_output = self.predictor_base(dummy_input)
        output_dim = dummy_output.shape[1]

        # Create a new set of codecs that contains the target, so entire DF records
        # can be tokenized. We don't want to add the target codec to the EmbeddingSpaces
        # codecs, so we create an entirely new dictionary.
        self.all_codecs = {
            col: codec for col, codec in self.embedding_space.col_codecs.items()
        }

        if self.all_codecs.get('target_col_name') is None:
            # Do not overwrite existing targets unless you want to spend a few days
            # looking for this line of code. :-P
            self.all_codecs[target_col_name] = self.target_codec

        self.is_target_scalar = isinstance(self.target_codec, ScalarCodec)

        self.predictor = nn.Sequential(
            self.predictor_base, nn.Linear(output_dim, target_dim)
        )
        # Keep predictor on device
        if torch.cuda.is_available():
            self.predictor = self.predictor.cuda()
        return
    
    @staticmethod
    def _create_marginal_token_batch_for_target(target_token_batch):
        """
        Replace the original token with marginal token. The values are set
        to 0 because that's a value all encoders can process, and the exact
        value doesn't matter for tokens with MARGINAL status.

        Args:
            target_token_batch:

        Returns:

        """
        batch_status = target_token_batch.status
        marginal_status = [TokenStatus.MARGINAL] * batch_status.shape[0]
        # Create tensors on same device as target_token_batch
        target_device = target_token_batch.status.device if hasattr(target_token_batch, 'status') and hasattr(target_token_batch.status, 'device') else torch.device('cpu')
        marginal_status_tensor = torch.tensor(marginal_status, device=target_device)

        marginal_values = [0] * batch_status.shape[0]
        marginal_values_tensor = torch.tensor(marginal_values, device=target_device)

        return TokenBatch.from_tensors(
            status=marginal_status_tensor,
            value=marginal_values_tensor,
        )
    

    def safe_split_train_val(self, df, target_col, test_size=0.2, random_state=None):
        logger.info(f"🔍 SPLIT DEBUG: Starting safe_split_train_val for target_col='{target_col}'")
        logger.info(f"🔍 SPLIT DEBUG: Input dataframe shape: {df.shape}")
        logger.info(f"🔍 SPLIT DEBUG: test_size={test_size}, random_state={random_state}")
        
        # DETAILED DISTRIBUTION ANALYSIS
        logger.info(f"📊 TARGET COLUMN ANALYSIS: '{target_col}'")
        
        # Check for NA/null values
        total_rows = len(df)
        null_count = df[target_col].isnull().sum()
        none_count = (df[target_col] == 'None').sum()
        empty_count = (df[target_col] == '').sum()
        
        logger.info(f"📊 Total rows: {total_rows}")
        logger.info(f"📊 Null values: {null_count} ({null_count/total_rows*100:.1f}%)")
        logger.info(f"📊 'None' string values: {none_count} ({none_count/total_rows*100:.1f}%)")
        logger.info(f"📊 Empty string values: {empty_count} ({empty_count/total_rows*100:.1f}%)")
        
        # Filter out problematic values
        valid_mask = ~(df[target_col].isnull() | (df[target_col] == 'None') | (df[target_col] == ''))
        valid_rows = valid_mask.sum()
        filtered_df = df[valid_mask].copy()
        
        logger.info(f"📊 Valid (non-null/non-empty) rows: {valid_rows} ({valid_rows/total_rows*100:.1f}%)")
        logger.info(f"📊 Rows excluded due to missing/invalid targets: {total_rows - valid_rows}")
        
        if valid_rows == 0:
            raise ValueError(f"No valid target values found in column '{target_col}' after filtering nulls/empties")
        
        # Analyze the filtered data distribution
        unique_categories = filtered_df[target_col].unique()
        value_counts = filtered_df[target_col].value_counts()
        
        logger.info(f"🔍 SPLIT DEBUG: After filtering - Found {len(unique_categories)} unique categories: {unique_categories}")
        logger.info(f"🔍 SPLIT DEBUG: After filtering - Category counts: {value_counts.to_dict()}")
        
        # Work with filtered dataframe for all subsequent analysis
        df = filtered_df
        
        # Analyze category distribution and identify validation-suitable categories
        categories_with_sufficient_samples = []
        categories_excluded_from_validation = []
        single_sample_categories = []
        
        # Identify categories that can be safely split for validation
        for category, count in value_counts.items():
            min_samples_needed = max(2, int(1 / test_size))  # Need at least 2 samples, or enough for test_size split
            if count >= min_samples_needed:
                categories_with_sufficient_samples.append((category, count))
            elif count == 1:
                single_sample_categories.append((category, count))
            else:
                categories_excluded_from_validation.append((category, count))
        
        # Log the analysis
        logger.info(f"📊 SPLIT ANALYSIS: Categories with sufficient samples for validation (>={max(2, int(1/test_size))}): {len(categories_with_sufficient_samples)}")
        if categories_with_sufficient_samples:
            sorted_sufficient = sorted(categories_with_sufficient_samples, key=lambda x: x[1], reverse=True)
            top_categories = sorted_sufficient[:3]  # Show top 3 most frequent
            logger.info(f"📊 Top categories with sufficient samples: {[(cat, count) for cat, count in top_categories]}")
        
        if single_sample_categories:
            logger.warning(f"⚠️  Categories with only 1 sample (will use for training only): {len(single_sample_categories)} categories")
            logger.warning(f"⚠️  Single sample categories: {[(cat, count) for cat, count in single_sample_categories[:5]]}")  # Show first 5
        
        if categories_excluded_from_validation:
            logger.warning(f"⚠️  Categories with insufficient samples for validation: {len(categories_excluded_from_validation)} categories")
            logger.warning(f"⚠️  Excluded categories: {[(cat, count) for cat, count in categories_excluded_from_validation[:5]]}")  # Show first 5

        train_df = pd.DataFrame()
        val_df = pd.DataFrame()
        
        # Store metadata about excluded categories for later use
        self.validation_excluded_categories = {
            'single_sample': [cat for cat, _ in single_sample_categories],
            'insufficient_samples': [cat for cat, _ in categories_excluded_from_validation],
            'total_excluded_samples': sum(count for _, count in single_sample_categories + categories_excluded_from_validation)
        }

        # Iterate over each unique category in the target column
        for i, category in enumerate(unique_categories):
            logger.info(f"🔍 SPLIT DEBUG: Processing category {i+1}/{len(unique_categories)}: '{category}'")
            
            category_df = df[df[target_col] == category]
            category_count = len(category_df)
            
            # Determine minimum samples needed for splitting
            min_samples_for_split = max(2, int(1 / test_size))
            
            if category_count < min_samples_for_split:
                # Add all samples to training set - cannot validate on categories with insufficient samples
                logger.warning(f"🔍 SPLIT DEBUG: Category '{category}' has {category_count} samples (< {min_samples_for_split} needed) - adding all to training set")
                train_df = pd.concat([train_df, category_df])
                categories_excluded_from_validation.append((category, category_count))
                continue
            
            logger.info(f"🔍 SPLIT DEBUG: Category '{category}' has {category_count} samples - splitting for validation")

            try:
                logger.info(f"🔍 SPLIT DEBUG: About to call train_test_split for category '{category}'")
                # Use sklearn's split for categories with sufficient samples
                category_train, category_val = train_test_split(
                    category_df,
                    test_size=test_size,
                    random_state=random_state,
                    stratify=None
                )
                logger.info(f"🔍 SPLIT DEBUG: train_test_split succeeded for category '{category}': train={len(category_train)}, val={len(category_val)}")

                train_df = pd.concat([train_df, category_train])
                val_df = pd.concat([val_df, category_val])
                logger.info(f"🔍 SPLIT DEBUG: After concat for category '{category}': total_train={len(train_df)}, total_val={len(val_df)}")
                
            except ValueError as e:
                logger.warning(f"🔍 SPLIT DEBUG: ValueError for category '{category}': {e}")
                if "empty" in str(e).lower():
                    # If split fails, add all samples to training set
                    logger.info(f"🔍 SPLIT DEBUG: Split failed for category '{category}', adding all {category_count} samples to training set")
                    train_df = pd.concat([train_df, category_df])
                    categories_excluded_from_validation.append((category, category_count))
                else:
                    logger.error(f"🔍 SPLIT DEBUG: Unexpected ValueError for category '{category}': {e}")
                    raise e
            except Exception as e:
                logger.error(f"🔍 SPLIT DEBUG: Unexpected exception for category '{category}': {type(e).__name__}: {e}")
                raise e

        # Log final validation coverage
        total_samples = len(df)
        validation_samples = len(val_df)
        excluded_samples = self.validation_excluded_categories['total_excluded_samples']
        validation_coverage = (validation_samples / total_samples) * 100 if total_samples > 0 else 0
        
        logger.info(f"🔍 SPLIT DEBUG: Completed safe_split_train_val - final train={len(train_df)}, val={len(val_df)}")
        logger.info(f"📊 VALIDATION COVERAGE: {validation_samples}/{total_samples} samples ({validation_coverage:.1f}%) can be validated")
        logger.info(f"📊 EXCLUDED FROM VALIDATION: {excluded_samples} samples across {len(self.validation_excluded_categories['single_sample']) + len(self.validation_excluded_categories['insufficient_samples'])} categories")
        
        # Compute distribution metadata for hyperparameter selection
        self.distribution_metadata = {
            'n_classes': len(unique_categories),
            'total_samples': total_samples,
            'train_samples': len(train_df),
            'val_samples': len(val_df),
            'validation_coverage': validation_coverage,
            'test_size': test_size
        }
        
        # Add class distribution for classification tasks
        if len(train_df) > 0:
            train_value_counts = train_df[target_col].value_counts()
            self.distribution_metadata['train_class_counts'] = train_value_counts.to_dict()
            self.distribution_metadata['train_class_ratios'] = (train_value_counts / len(train_df)).to_dict()
            
            # Compute imbalance metrics
            if len(train_value_counts) >= 2:
                majority_count = train_value_counts.iloc[0]
                minority_count = train_value_counts.iloc[-1]
                
                # Traditional ratio format (e.g., 7.0 means "7:1 ratio")
                imbalance_ratio = majority_count / max(minority_count, 1)
                self.distribution_metadata['imbalance_ratio'] = imbalance_ratio
                
                # Normalized imbalance score [0,1] where:
                # 1.0 = perfectly balanced (50/50)
                # 0.5 = moderate imbalance (e.g., 67/33 or 2:1)
                # 0.1 = severe imbalance (e.g., 91/9 or 10:1)
                # 0.0 = extreme imbalance (one class completely dominates)
                minority_ratio = minority_count / max(majority_count, 1)
                self.distribution_metadata['imbalance_score'] = minority_ratio
                
                self.distribution_metadata['majority_class'] = train_value_counts.index[0]
                self.distribution_metadata['minority_class'] = train_value_counts.index[-1]
        
        if len(val_df) > 0:
            val_value_counts = val_df[target_col].value_counts()
            self.distribution_metadata['val_class_counts'] = val_value_counts.to_dict()
            self.distribution_metadata['val_class_ratios'] = (val_value_counts / len(val_df)).to_dict()
        
        # Log availability of distribution metadata for hyperparameter selection
        logger.info(f"📊 DISTRIBUTION METADATA: Available for hyperparameter selection")
        logger.info(f"📊   → n_classes={self.distribution_metadata['n_classes']}, train_samples={self.distribution_metadata['train_samples']}")
        if 'imbalance_ratio' in self.distribution_metadata:
            logger.info(f"📊   → imbalance_ratio={self.distribution_metadata['imbalance_ratio']:.2f}:1, imbalance_score={self.distribution_metadata['imbalance_score']:.3f}")
            logger.info(f"📊   → {self.distribution_metadata['majority_class']} / {self.distribution_metadata['minority_class']}")
        
        # DETAILED FINAL DISTRIBUTION ANALYSIS
        logger.info(f"")
        logger.info(f"📊 ============== FINAL DISTRIBUTION ANALYSIS ==============")
        
        # Training set distribution
        if len(train_df) > 0:
            train_value_counts = train_df[target_col].value_counts()
            logger.info(f"📈 TRAINING SET ({len(train_df)} samples):")
            for category, count in train_value_counts.items():
                percentage = (count / len(train_df)) * 100
                logger.info(f"📈   '{category}': {count} samples ({percentage:.1f}%)")
        else:
            logger.warning(f"📈 TRAINING SET: EMPTY!")
        
        # Validation set distribution  
        if len(val_df) > 0:
            val_value_counts = val_df[target_col].value_counts()
            logger.info(f"📉 VALIDATION SET ({len(val_df)} samples):")
            for category, count in val_value_counts.items():
                percentage = (count / len(val_df)) * 100
                logger.info(f"📉   '{category}': {count} samples ({percentage:.1f}%)")
                
            # Check if validation maintains class balance
            if len(train_df) > 0:
                logger.info(f"⚖️  CLASS BALANCE ANALYSIS:")
                train_ratios = train_df[target_col].value_counts(normalize=True)
                val_ratios = val_df[target_col].value_counts(normalize=True)
                
                for category in train_ratios.index:
                    train_pct = train_ratios[category] * 100
                    val_pct = val_ratios.get(category, 0) * 100
                    balance_diff = abs(train_pct - val_pct)
                    
                    balance_status = "✅" if balance_diff < 10 else "⚠️" if balance_diff < 20 else "❌"
                    logger.info(f"⚖️    '{category}': Train {train_pct:.1f}% vs Val {val_pct:.1f}% (diff: {balance_diff:.1f}%) {balance_status}")
        else:
            logger.warning(f"📉 VALIDATION SET: EMPTY!")
        
        logger.info(f"📊 ========================================================")
        logger.info(f"")
        
        # Provide context-appropriate warning about low validation coverage
        # Expected validation coverage is test_size * 100, but warn only if significantly lower (less than 50% of expected)
        expected_validation_coverage = test_size * 100
        coverage_threshold = expected_validation_coverage * 0.5  # Warn if we get less than half the expected validation data
        
        if validation_coverage < coverage_threshold:
            num_excluded_categories = len(self.validation_excluded_categories['single_sample']) + len(self.validation_excluded_categories['insufficient_samples'])
            num_total_categories = len(unique_categories)
            
            if num_excluded_categories > 0:
                if num_total_categories > 10:
                    # Many categories scenario
                    logger.warning(f"⚠️  LOW VALIDATION COVERAGE: Only {validation_coverage:.1f}% of data can be validated (expected {expected_validation_coverage:.1f}%) - {num_excluded_categories}/{num_total_categories} categories have insufficient samples")
                elif num_total_categories <= 2:
                    # Binary or very few classes - different message
                    logger.warning(f"⚠️  LOW VALIDATION COVERAGE: Only {validation_coverage:.1f}% of data can be validated (expected {expected_validation_coverage:.1f}%) - one or more classes have insufficient samples for splitting")
                else:
                    # Few categories but some excluded
                    logger.warning(f"⚠️  LOW VALIDATION COVERAGE: Only {validation_coverage:.1f}% of data can be validated (expected {expected_validation_coverage:.1f}%) - {num_excluded_categories} categories have insufficient samples")
            else:
                # Coverage is low but no categories were explicitly excluded - might be due to split ratio or data distribution
                logger.warning(f"⚠️  LOW VALIDATION COVERAGE: Only {validation_coverage:.1f}% of data in validation set (expected {expected_validation_coverage:.1f}%)")
        
        return train_df, val_df
    
    def get_validation_metadata(self):
        """
        Returns metadata about which categories were excluded from validation.
        
        Returns:
            dict: Contains information about categories that couldn't be validated:
                - 'single_sample': List of categories with only 1 sample
                - 'insufficient_samples': List of categories with too few samples for splitting  
                - 'total_excluded_samples': Total number of samples excluded from validation
                - 'excluded_categories_count': Total number of categories excluded
        """
        if self.validation_excluded_categories is None:
            return None
            
        metadata = self.validation_excluded_categories.copy()
        metadata['excluded_categories_count'] = (
            len(metadata['single_sample']) + len(metadata['insufficient_samples'])
        )
        return metadata
    
    def get_distribution_metadata(self):
        """
        Returns class distribution metadata for hyperparameter selection.
        
        This metadata can be used by models to automatically select optimal hyperparameters
        based on dataset characteristics such as class imbalance, sample size, etc.
        
        Returns:
            dict: Contains distribution information including:
                - 'n_classes': Number of unique classes
                - 'total_samples': Total number of samples
                - 'train_samples': Number of training samples
                - 'val_samples': Number of validation samples
                - 'validation_coverage': Percentage of data in validation set
                - 'test_size': Test size ratio used for splitting
                - 'train_class_counts': Dict of class counts in training set
                - 'train_class_ratios': Dict of class ratios in training set
                - 'val_class_counts': Dict of class counts in validation set (if available)
                - 'val_class_ratios': Dict of class ratios in validation set (if available)
                - 'imbalance_ratio': Ratio of majority to minority class (e.g., 7.0 = "7:1 ratio")
                - 'imbalance_score': Normalized imbalance [0,1] where 1.0=balanced, 0.0=extreme
                - 'majority_class': Name of the majority class (if binary/multiclass)
                - 'minority_class': Name of the minority class (if binary/multiclass)
                
            None: If distribution metadata hasn't been computed yet (before training split)
            
        Example usage for hyperparameter selection:
            ```python
            dist = predictor.get_distribution_metadata()
            
            # Use normalized score for clean threshold logic
            if dist['imbalance_score'] < 0.1:  # < 10% minority
                use_focal_loss = True
                focal_gamma = 3.0
            elif dist['imbalance_score'] < 0.33:  # < 33% minority  
                use_focal_loss = True
                focal_gamma = 2.0
            else:  # Relatively balanced
                use_focal_loss = False
            ```
        """
        return self.distribution_metadata

    def get_good_val_pos_label(self, val_targets):
        """
        Very chatty logging but I want to leave it so we can debug this stuff.
        """
        val_pos_label = None
        try:
            value_counts = val_targets.value_counts(ascending=True)
            logger.info(f">>> target column value_counts = {value_counts.to_dict()}")
            for vv, _ in value_counts.items():
                if val_pos_label is not None:
                    break
                logger.info(f"here we go... checking __{vv}__...")
                if (vv != vv) or (vv is None):
                    logger.info(f"got NaN/None")
                    continue
                if type(vv) == str:
                    logger.info(f"got a str")
                    if len(vv) == 0:
                        logger.info(f"got a str... but it's empty")
                        continue
                    try:
                        if len(vv.strip()) == 0:
                            logger.info(f"got a str... but it's whitespace")
                            continue
                        val_pos_label = vv
                        logger.info(f"set val_pos_label = {val_pos_label}")
                        break   # this breaks out of the try, !@&#*(# python)
                    except:
                        traceback.print_exc()
                else:
                    val_pos_label = vv
                    logger.info(f"set val_pos_label = {val_pos_label}... type() = {type(val_pos_label)}")
                    break

            # least_popular_value = val_targets.value_counts().idxmin()
            # print("The least popular value is:", least_popular_value)
        except:
            traceback.print_exc()
            logger.info(f"CHECK STDOUT FOR CRASH (stderr now redirected to stdout)")
            # Pick the first non-nan unique value as the positive label, arbitrarily.
            val_list = val_targets.unique().tolist()
            logger.info(f">>> target values found in target: {val_list}")
            for vv in val_list:
                if val_pos_label is not None:
                    break
                # vv != vv checks whether vv is NaN. In principle, math.isnan could be used,
                # but that fails on string input, so for the sake of clarity we use a simple comparison.
                if type(vv) == str:
                    if len(vv) == 0:
                        continue
                    try:
                        if len(vv.strip()) == 0:
                            continue
                    except:
                        traceback.print_exc()
                        print("Continuing...")
                if (vv != vv) or (vv is None):
                    val_pos_label = vv
                    break

        return val_pos_label
    
    def should_compute_binary_metrics(self):
        """Returns True if binary metrics should be computed, False otherwise.

        This essentially checks whether the target variable is a categorical 
        variable with 2 options. 
        """
        is_set = isinstance(self.target_codec, SetCodec)

        if is_set:
            members = self.target_codec.members
            # There's always unknown, so the codec
            # for a binary variable has 3 members
            is_binary = len(members) == 3
        else:
            is_binary = False

        return is_binary


    def print_label_distribution(self, train_df, val_df, target_col):
        """Print the distribution of labels in train and validation datasets"""
        logger.info(f"📊 ============== LABEL DISTRIBUTION ANALYSIS ==============")
        
        # Train distribution
        train_counts = train_df[target_col].value_counts()
        train_total = len(train_df)
        logger.info(f"📈 TRAINING SET ({train_total} samples):")
        for label, count in train_counts.items():
            percentage = (count / train_total) * 100
            logger.info(f"📈   '{label}': {count} samples ({percentage:.1f}%)")
        
        # Validation distribution - handle empty val_df case
        val_total = len(val_df)
        if val_total > 0 and len(val_df.columns) > 0 and target_col in val_df.columns:
            val_counts = val_df[target_col].value_counts()
            logger.info(f"📉 VALIDATION SET ({val_total} samples):")
            for label, count in val_counts.items():
                percentage = (count / val_total) * 100
                logger.info(f"📉   '{label}': {count} samples ({percentage:.1f}%)")
        else:
            # Empty val_df - create empty Series for consistency
            val_counts = pd.Series(dtype='int64')
            logger.info(f"📉 VALIDATION SET ({val_total} samples):")
            if val_total == 0:
                logger.warning(f"📉 VALIDATION SET: EMPTY (0 samples)")
        
        # Class balance analysis
        logger.info(f"⚖️  CLASS BALANCE ANALYSIS:")
        for label in train_counts.index:
            train_pct = (train_counts[label] / train_total) * 100
            val_pct = (val_counts[label] / val_total) * 100 if label in val_counts and val_total > 0 else 0
            diff = abs(train_pct - val_pct)
            status = "✅" if diff < 5.0 else "⚠️"
            logger.info(f"⚖️    '{label}': Train {train_pct:.1f}% vs Val {val_pct:.1f}% (diff: {diff:.1f}%) {status}")
        
        logger.info(f"📊 ========================================================")
        
        # Store class distribution for later use (e.g., in warnings)
        # Convert to regular dicts with native Python types for JSON serialization
        # Convert all labels to strings before sorting to avoid TypeError when mixing str and int
        # Create a mapping from original labels to string labels for lookup
        train_label_set = {str(label) for label in train_counts.index}
        val_label_set = {str(label) for label in val_counts.index} if len(val_counts) > 0 else set()
        all_labels_str = sorted(train_label_set | val_label_set)
        
        # Build mapping from string labels back to original labels for lookup
        train_label_map = {str(label): label for label in train_counts.index}
        val_label_map = {str(label): label for label in val_counts.index} if len(val_counts) > 0 else {}
        
        total_counts = {}
        for label_str in all_labels_str:
            # Look up using original label type, fallback to 0 if not found
            train_orig = train_label_map.get(label_str)
            val_orig = val_label_map.get(label_str)
            train_count = train_counts.get(train_orig, 0) if train_orig is not None else 0
            val_count = val_counts.get(val_orig, 0) if val_orig is not None else 0
            total_counts[label_str] = train_count + val_count
        
        self.class_distribution = {
            'train': {label_str: int(train_counts.get(train_label_map.get(label_str), 0)) for label_str in all_labels_str},
            'val': {label_str: int(val_counts.get(val_label_map.get(label_str), 0)) for label_str in all_labels_str},
            'total': {label_str: int(count) for label_str, count in total_counts.items()},
            'train_total': int(train_total),
            'val_total': int(val_total),
            'total_total': int(train_total + val_total),
        }
        
        return


    async def train(
        self,
        n_epochs=0,
        batch_size=0,
        fine_tune=True,
        val_df=None,
        val_queries=None,
        val_targets=None,
        val_pos_label=None,
        print_progress_step=10,
        optimizer_params=None,
        use_lr_scheduler=True,
        print_callback=None,
        job_id=None,
        network_viz_identifier=None,
        sp_identifier=None,
        use_auc_for_best_epoch=None,  # None = auto-detect (True for binary, False for scalar)
        use_pairwise_ranking_loss=True,  # Default True for testing
        pairwise_loss_weight=0.1,  # Weight for pairwise ranking loss component
    ):
        """
        # fine_tune: whether the encoder should be fine-tuned for this task.
        # val_df: if provided, it's used to report validation error during training
        # print_callback: callback function that receives progress dictionary like ES.train
        # job_id: job ID for ABORT/FINISH file detection (optional)
        # sp_identifier: identifier for this SP (e.g., target column name) used in logs and filenames
        """
        
        # Set the identifier for this training run
        if sp_identifier:
            self.run_identifier = f"[SP:{sp_identifier}]"
            
            # Add filter to the logger for this module
            sp_filter = SPIdentifierFilter(self.run_identifier, self)
            logger.addFilter(sp_filter)
            
            # Store filter reference so we can remove it later if needed
            self._sp_log_filter = sp_filter
        
        # Set output directory for timeline saving (from embedding space)
        if hasattr(self.embedding_space, 'output_dir') and self.embedding_space.output_dir:
            self._output_dir = self.embedding_space.output_dir
            logger.info(f"📊 SP training timeline will be saved to: {self._output_dir}")
        
        #dump_logging_tree()
        
        # Suppress harmless "Bad file descriptor" errors from DataLoader worker cleanup
        # These occur when multiprocessing queues close during worker shutdown
        # They're harmless PyTorch internal cleanup errors
        # Note: Can't filter OSError with warnings.filterwarnings (OSError is not a Warning subclass)
        # Instead, suppress at logging level
        logging.getLogger('multiprocessing').setLevel(logging.ERROR)  # Suppress QueueFeederThread errors
            
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
            force=True,
        )
        logger.info(f"@@@@@@@@@@ SINGLE PREDICTOR INPUT n_epochs = {n_epochs}, batch_size = {batch_size}, fine_tune = {fine_tune}")
        
        # Track training start for hourly checkpoints
        training_start_time = time.time()
        last_checkpoint_time = [0.0]  # Use list for closure mutability
        
        # Auto-calculate batch_size if not specified
        if batch_size is None or batch_size == 0:
            batch_size = ideal_batch_size(len(self.train_df))
            logger.info(f"Auto-calculated batch_size: {batch_size}")
        
        # Auto-calculate n_epochs if not specified
        if n_epochs is None or n_epochs == 0:
            n_epochs = ideal_epochs_predictor(len(self.train_df), batch_size)
            logger.info(f"Auto-calculated n_epochs: {n_epochs}")
        
        # Store total epochs for logging filter
        self._total_epochs = n_epochs

        if print_progress_step == 0:
            print_progress_step = 1

        if self.predictor is None:
            raise Exception("Need to call `prep_for_training` first.")

        # 
        # Choose which parameters to train and set the optimizer
        # 
        logger.info(f"🔧 Training configuration: fine_tune={fine_tune}")
        
        # Count total parameters for logging
        predictor_params = list(self.predictor.parameters())
        encoder_params = list(self.embedding_space.encoder.parameters())
        
        predictor_count = sum(p.numel() for p in predictor_params)
        encoder_count = sum(p.numel() for p in encoder_params)
        total_count = predictor_count + encoder_count
        
        if fine_tune:
            logger.info(f"   ✅ FINE-TUNING ENABLED: training both predictor AND encoder parameters")
            logger.info(f"   🔓 Encoder is trainable - will adapt to your target column")
            params = predictor_params + encoder_params
            trainable_count = total_count
            frozen_count = 0
        else:
            logger.info(f"   ⚠️  FINE-TUNING DISABLED: training ONLY predictor parameters (encoder frozen)")
            logger.info(f"   🔒 Encoder is frozen - only predictor will learn")
            # CRITICAL: Convert to list to ensure it's iterable and not consumed
            # Using generator directly can cause issues when iterating multiple times
            params = predictor_params
            trainable_count = predictor_count
            frozen_count = encoder_count
            
            # Actually freeze encoder parameters
            for param in encoder_params:
                param.requires_grad = False
            logger.info(f"   🔒 Encoder parameters frozen: {encoder_count:,} params ({encoder_count/total_count:.1%} of model)")
        
        logger.info(f"   📊 Parameter breakdown:")
        logger.info(f"      Predictor: {predictor_count:,} params ({predictor_count/total_count:.1%})")
        logger.info(f"      Encoder: {encoder_count:,} params ({encoder_count/total_count:.1%})")
        logger.info(f"      Trainable: {trainable_count:,} params ({trainable_count/total_count:.1%})")
        logger.info(f"      Frozen: {frozen_count:,} params ({frozen_count/total_count:.1%})")

        # CRITICAL FIX: Increase default LR from 0.001 to 0.01 to prevent dead gradients
        # Dead gradients (norm=0.0) occur when LR is too small and model gets stuck in flat regions
        # Higher initial LR helps escape flat regions and provides stronger gradient signal
        optimizer_params = optimizer_params or {"lr": 0.01, "weight_decay": 0.0}
        optimizer = torch.optim.AdamW(params, **optimizer_params)
        
        # CRITICAL: Store optimizer reference so we can clear its state later
        # This is needed because optimizer state (momentum, variance) can be on GPU even if params are on CPU
        self._current_optimizer = optimizer
        # Also store for LR adjustment during training
        self._training_optimizer = optimizer

        logger.info(f">>> fsp params = {optimizer_params}...")

        # 
        # Set up the learning rate scheduler with warmup period
        # 
        # PROBLEM: CosineAnnealingLR starts decaying immediately from epoch 0, causing:
        # - LR too small too early → dead gradients (norm=0.0)
        # - Model stuck in flat regions with no gradient signal
        # 
        # SOLUTION: Add warmup period (hold LR constant) before cosine annealing
        # - First 10% of epochs: Hold LR constant at initial value
        # - Remaining epochs: Cosine annealing to eta_min
        # This gives model time to learn before LR decays
        n_batches_per_epoch = math.ceil(len(self.train_df) / batch_size)

        if use_lr_scheduler:
            # Calculate warmup period: 10% of total epochs, minimum 3 epochs, maximum 10 epochs
            # Shorter warmup for long training runs (300+ epochs) to start annealing sooner
            warmup_epochs = min(max(3, int(n_epochs * 0.1)), 10)
            cosine_epochs = n_epochs - warmup_epochs
            
            logger.info(f"📈 LR Schedule: {warmup_epochs} epochs warmup (constant LR), then {cosine_epochs} epochs cosine annealing")
            logger.info(f"   Initial LR: {optimizer_params.get('lr', 0.01):.6e}, Final LR (eta_min): 1.000000e-06")
            
            if warmup_epochs >= n_epochs:
                # If warmup is longer than total epochs, just use constant LR
                scheduler = ConstantLR(optimizer, factor=1.0, total_iters=n_epochs)
            else:
                # Warmup: Hold LR constant
                warmup_scheduler = ConstantLR(optimizer, factor=1.0, total_iters=warmup_epochs)
                
                # Cosine annealing: Decay from initial LR to eta_min
                cosine_scheduler = CosineAnnealingLR(
                    optimizer,
                    T_max=cosine_epochs,
                    eta_min=1e-6
                )
                
                # Combine: warmup first, then cosine annealing
                scheduler = SequentialLR(
                    optimizer,
                    schedulers=[warmup_scheduler, cosine_scheduler],
                    milestones=[warmup_epochs]
                )
        else:
            scheduler = None

        def get_lr():
            if scheduler is not None:
                return scheduler.get_last_lr()
            else:
                return optimizer_params["lr"]

        loss_fn = self.target_codec.loss_fn

        # 
        # Set up validation batch for computing validation loss,
        # and validation queries for computing metrics.
        # 
        # Create the validation batch, if the validation data is provided.
        validation_batch = None
        if val_df is None:
            # NOTE: (24/03/01, pjz) We should draw a random seed and save it in the database, but
            # for now a fixed seed will do.
            split_seed = 0
            validation_set_fraction = 0.2

            # The function is called train_test_split, but we're using it to break out a validation set
            # from the train set.
            print(f"@@@@ No passed val_df -- splitting the train data with split_seed = {split_seed} and validation_set_fraction = {validation_set_fraction} @@@@")
            logger.info(f"🔍 TRAIN DEBUG: About to check target_col_type")
            logger.info(f"🔍 TRAIN DEBUG: self.target_col_type = {repr(self.target_col_type)}")
            logger.info(f"🔍 TRAIN DEBUG: type(self.target_col_type) = {type(self.target_col_type)}")
            if self.target_col_type == 'set':
                logger.info(f"🔍 TRAIN DEBUG: Taking 'set' branch for target_col_type")
                train_df, val_df = self.safe_split_train_val(
                    self.train_df,
                    target_col=self.target_col_name,
                    test_size=validation_set_fraction,
                    random_state=split_seed,
                )
                logger.info(f"🔍 TRAIN DEBUG: Completed safe_split_train_val call")
            elif self.target_col_type == 'scalar':
                logger.info(f"🔍 TRAIN DEBUG: Taking 'scalar' branch for target_col_type")
                # use sklearn's function
                train_df, val_df = train_test_split(
                    self.train_df,
                    test_size=validation_set_fraction,
                    random_state=split_seed,
                )
                logger.info(f"🔍 TRAIN DEBUG: Completed train_test_split call")
            else:
                logger.error(f"🔍 TRAIN DEBUG: Unknown target column type: {self.target_col_type}")
                raise Exception(f"Unknown target column type: {self.target_col_type}")

            # Reset the indices after train_test_split to make sure we can index into them
            # independently from what the indices were in the original dataframes.
            logger.info(f"🔍 TRAIN DEBUG: About to reset indices - train_df shape: {train_df.shape}, val_df shape: {val_df.shape}")
            train_df.reset_index(drop=True, inplace=True)
            val_df.reset_index(drop=True, inplace=True)
            logger.info(f"🔍 TRAIN DEBUG: Completed index reset")
            
            # Duplicate rows if dataset is too small (similar to ES training)
            # This ensures we have enough data for proper batching and training dynamics
            MIN_DATASET_SIZE = 1024
            original_train_size = len(train_df)
            original_val_size = len(val_df)
            total_size = original_train_size + original_val_size
            
            if total_size < MIN_DATASET_SIZE:
                logger.info(f"📊 Small dataset detected: {total_size} samples < {MIN_DATASET_SIZE}")
                logger.info(f"   Train: {original_train_size}, Val: {original_val_size}")
                
                # Calculate duplication factor needed to reach >= MIN_DATASET_SIZE
                duplication_factor = math.ceil(MIN_DATASET_SIZE / total_size)
                logger.info(f"   Duplicating each set {duplication_factor}x to reach >= {MIN_DATASET_SIZE} samples")
                
                # Duplicate train set
                train_duplicates = [train_df] * duplication_factor
                train_df = pd.concat(train_duplicates, ignore_index=True)
                
                # Duplicate val set
                val_duplicates = [val_df] * duplication_factor
                val_df = pd.concat(val_duplicates, ignore_index=True)
                
                new_total = len(train_df) + len(val_df)
                logger.info(f"✅ Dataset augmented: {total_size} → {new_total} samples")
                logger.info(f"   Train: {original_train_size} → {len(train_df)}, Val: {original_val_size} → {len(val_df)}")
        else:
            print("@@@@ We handed ourselves a val_df -- very good -- DEFINITELY NOT SPLITTING @@@@")
            train_df = self.train_df
            train_df.reset_index(drop=True, inplace=True)
            val_df.reset_index(drop=True, inplace=True)

        self.print_label_distribution(train_df=train_df, val_df=val_df, target_col=self.target_col_name)

        # Setup info for validation metrics.
        # CRITICAL: Check if val_df is empty or missing target column BEFORE accessing it
        if len(val_df) == 0 or len(val_df.columns) == 0:
            logger.warning(f"⚠️  VALIDATION SET IS EMPTY: {len(val_df)} rows, {len(val_df.columns)} columns")
            logger.warning(f"   This means all data was used for training (no validation split possible)")
            logger.warning(f"   Skipping validation metrics setup")
            val_queries = []
            val_targets = pd.Series(dtype='object')
        else:
            # Validate target column exists in val_df
            if self.target_col_name not in val_df.columns:
                available_cols = list(val_df.columns)[:20]
                error_msg = (
                    f"❌ CRITICAL ERROR: Target column '{self.target_col_name}' NOT FOUND in validation set!\n"
                    f"   Validation set has {len(val_df)} rows and {len(val_df.columns)} columns\n"
                    f"   Available columns (first 20): {available_cols}\n"
                    f"   This indicates the target column was lost during train/val split or CSV reading.\n"
                    f"   Check CSV reading logs to see what columns were actually loaded."
                )
                logger.error(error_msg)
                raise KeyError(f"Target column '{self.target_col_name}' not found in validation set. Available columns: {available_cols}")
            
        if val_queries is None:
            val_queries = val_df.to_dict("records")
            # Remove the target column from the queries.
            for q in val_queries:
                del q[self.target_col_name]
        if val_targets is None:
            val_targets = val_df[self.target_col_name]
            
            # Only try to get val_pos_label if we have validation targets
            if val_pos_label is None and len(val_targets) > 0:
                val_pos_label = self.get_good_val_pos_label(val_targets=val_targets)
                
                logger.warning(
                    f"Choosing label '{val_pos_label}' as the positive label for validation metrics"
                )
                
                assert val_pos_label is not None, "couldn't auto pick a val_pos_label, apparently."
            elif val_pos_label is None and len(val_targets) == 0:
                logger.warning(f"⚠️  Cannot determine val_pos_label: validation set is empty")
                val_pos_label = None

        # 
        # Construct dataloaders
        # 
        # Construct training dataloader
        
        # CRITICAL: Move predictor to GPU BEFORE training starts
        if torch.cuda.is_available():
            predictor_device = next(self.predictor.parameters()).device if list(self.predictor.parameters()) else None
            if predictor_device is None or predictor_device.type != 'cuda':
                logger.info(f"🚀 Moving predictor to GPU for training...")
                self.predictor = self.predictor.cuda()
                predictor_device = next(self.predictor.parameters()).device
                logger.info(f"✅ Predictor device: {predictor_device}")
            else:
                logger.info(f"✅ Predictor already on GPU: {predictor_device}")
        
        # CRITICAL: Move embedding space encoder to GPU for training
        # This is the MAIN model that does all the heavy lifting!
        if torch.cuda.is_available() and self.embedding_space is not None:
            if hasattr(self.embedding_space, 'encoder') and self.embedding_space.encoder is not None:
                encoder_params = list(self.embedding_space.encoder.parameters())
                if encoder_params:
                    encoder_device = next(iter(encoder_params)).device
                    if encoder_device.type != 'cuda':
                        logger.info(f"🚀 Moving embedding space ENCODER to GPU (was on {encoder_device})...")
                        self.embedding_space.encoder = self.embedding_space.encoder.cuda()
                        encoder_device = next(self.embedding_space.encoder.parameters()).device
                        logger.info(f"✅ Encoder device: {encoder_device}")
                        encoder_param_count = sum(p.numel() for p in self.embedding_space.encoder.parameters())
                        logger.info(f"   Encoder params on GPU: {encoder_param_count:,}")
                    else:
                        logger.info(f"✅ Encoder already on GPU: {encoder_device}")
                else:
                    logger.warning(f"⚠️  Encoder has no parameters to move to GPU")
        
        # Move all codecs to GPU if available
        codecs_on_gpu = 0
        if torch.cuda.is_available():
            for codec_name, codec in self.all_codecs.items():
                try:
                    if hasattr(codec, 'cuda'):
                        codec.cuda()
                        # Verify it's actually on GPU
                        if hasattr(codec, 'parameters') and list(codec.parameters()):
                            codec_device = next(codec.parameters()).device
                            if codec_device.type == 'cuda':
                                codecs_on_gpu += 1
                    elif hasattr(codec, 'to'):
                        codec.to('cuda')
                        codecs_on_gpu += 1
                except Exception as e:
                    logger.debug(f"Could not move {codec_name} codec to GPU: {e}")
            if codecs_on_gpu > 0:
                logger.info(f"✅ Moved {codecs_on_gpu}/{len(self.all_codecs)} codecs to GPU")
            
        train_dataset = SuperSimpleSelfSupervisedDataset(train_df, self.all_codecs)
        
        # Validate dataset is not empty
        if len(train_df) == 0:
            raise ValueError(f"❌ Training dataframe is EMPTY (0 rows)! Cannot train with no data.")
        
        # Limit batch_size to max(len(data) / 8, rounded down to nearest power of 2)
        # This ensures we have at least 8 batches per epoch for proper training dynamics
        dataset_size = len(train_df)
        max_batch_size_float = dataset_size / 8.0
        # Round down to nearest power of 2 (math is already imported at top of file)
        if max_batch_size_float >= 1:
            max_batch_size = int(2 ** math.floor(math.log2(max_batch_size_float)))
        else:
            max_batch_size = 1  # Minimum batch size of 1
        
        # Cap batch_size if it exceeds the limit
        original_batch_size = batch_size
        if batch_size > max_batch_size:
            batch_size = max_batch_size
            logger.warning(
                f"⚠️  batch_size ({original_batch_size}) capped to {batch_size} "
                f"(max = len(data)/8 = {dataset_size}/8 = {max_batch_size_float:.1f}, "
                f"rounded down to power of 2 = {max_batch_size})"
            )
        
        # CRITICAL: Force num_workers=0 for single predictor training
        # Multiprocessing causes StringCodec cache miss issues in workers
        # 
        # CRITICAL: If batch_size > len(train_df) and drop_last=True, dataloader will be EMPTY (0 batches)!
        # This causes 0% GPU usage and 0.0000 losses. Auto-adjust drop_last to prevent this.
        use_drop_last = True  # Default: drop incomplete batches to prevent batch_size=1 (breaks BatchNorm)
        if batch_size > dataset_size:
            logger.warning(
                f"⚠️  batch_size ({batch_size}) > train_df size ({dataset_size})! "
                f"Setting drop_last=False to prevent empty dataloader. "
                f"Will use single batch of size {dataset_size}."
            )
            use_drop_last = False  # Must keep the incomplete batch or we'll have 0 batches
        
        train_dl_kwargs = create_dataloader_kwargs(
            batch_size=batch_size,
            shuffle=True,
            drop_last=use_drop_last,  # Auto-adjusted: False if batch_size > dataset_size
            num_workers=0,  # Force single-process to avoid worker cache miss issues
            dataset_size=len(train_df),
        )
        train_dataloader = DataLoader(
            train_dataset,
            collate_fn=collate_tokens,
            **train_dl_kwargs
        )
        
        # Validate dataloader is not empty
        dataloader_len = len(train_dataloader)
        if dataloader_len == 0:
            raise ValueError(
                f"❌ Training dataloader is EMPTY (0 batches)! "
                f"This means no training data is available.\n"
                f"   train_df size: {len(train_df)}\n"
                f"   batch_size: {batch_size}\n"
                f"   drop_last: {train_dl_kwargs.get('drop_last', False)}\n"
                f"   Dataset length: {len(train_dataset)}\n"
                f"   If drop_last=True and batch_size > len(train_df), all batches will be dropped.\n"
                f"   Consider reducing batch_size or setting drop_last=False."
            )
        
        logger.info(f"✅ Training dataloader created: {dataloader_len} batches (dataset_size={len(train_df)}, batch_size={batch_size})")

        # TODO: check that val_df has the same columns as train_df.
        # Construct the validation batch. Validation uses a single, so we can
        # draw it from the dataloader immediately. The validation dataloder
        # is just used to make sure that the validation batch is formatted properly.
        
        validation_dataset = SuperSimpleSelfSupervisedDataset(
            val_df,
            self.all_codecs,
        )
        validation_dataloader = DataLoader(
            validation_dataset,
            batch_size=len(val_df),
            # Don't need to shuffle because we're using the whole dataset in one batch.
            shuffle=False,
            collate_fn=collate_tokens,
        )
        validation_batch = next(iter(validation_dataloader))
        
        # Move validation batch to same device as encoder
        encoder_device = next(self.embedding_space.encoder.parameters()).device
        for tokenbatch in validation_batch.values():
            tokenbatch.to(encoder_device)
        
        val_target_token_batch = validation_batch.pop(self.target_col_name)
        validation_targets = val_target_token_batch.value
        
        # Move validation targets to GPU if available
        if torch.cuda.is_available():
            validation_targets = validation_targets.to(torch.device('cuda'))
        
        if self.is_target_scalar:
            validation_targets = validation_targets.float().unsqueeze(dim=1)
        else:
            # For set/categorical targets, CrossEntropyLoss expects integer class indices
            validation_targets = validation_targets.long()

        # Auto-detect use_auc_for_best_epoch if not specified
        if use_auc_for_best_epoch is None:
            # Use AUC for binary classification, validation loss for scalar/regression
            is_binary = (hasattr(self, 'target_codec') and 
                        isinstance(self.target_codec, SetCodec) and
                        len(self.target_codec.members) == 2)  # Binary = 2 classes (excluding <UNKNOWN>)
            use_auc_for_best_epoch = is_binary and not self.is_target_scalar
            logger.info(f"🎯 Auto-detected best epoch selection: {'AUC' if use_auc_for_best_epoch else 'validation_loss'}")
        else:
            logger.info(f"🎯 Best epoch selection: {'AUC' if use_auc_for_best_epoch else 'validation_loss'} (explicitly set)")

        # Validation set size warning
        val_size = len(val_df) if val_df is not None else 0
        if val_size > 0:
            if val_size < 200:
                logger.warning(f"⚠️  Small validation set ({val_size} samples) - threshold estimates may be noisy")
            else:
                logger.info(f"✅ Validation set size: {val_size} samples (sufficient for stable threshold estimation)")
        
        # Log pairwise ranking loss configuration
        if use_pairwise_ranking_loss:
            is_binary_for_pairwise = (hasattr(self, 'target_codec') and 
                                     isinstance(self.target_codec, SetCodec) and
                                     len(self.target_codec.members) == 2 and
                                     not self.is_target_scalar)
            if is_binary_for_pairwise:
                logger.info(f"📊 Pairwise ranking loss: ENABLED (weight={pairwise_loss_weight:.3f})")
            else:
                logger.warning(f"⚠️  Pairwise ranking loss requested but target is not binary - disabling")
                use_pairwise_ranking_loss = False
        else:
            logger.info(f"📊 Pairwise ranking loss: DISABLED")

        # 
        # Compute pre-training metrics, and initialize progress dictionary
        # 
        try:
            self.training_metrics = self.compute_classification_metrics(
                val_queries, val_targets, val_pos_label, epoch_idx=0, n_epochs=n_epochs
            )
        except:
            logger.exception("error with compute_classification_metrics")

        # Initialize progress tracking dictionary (ES.train style)
        timeStart = time.time()
        max_progress = n_epochs * len(train_dataloader)
        
        progress_dict = {
            "status": "training",
            "start_time": timeStart,
            "time_now": timeStart,
            "epoch_total": n_epochs,
            "batch_total": len(train_dataloader),
            "batch_idx": 0,
            "epoch_idx": 0,
            "max_progress": max_progress,
            "progress_counter": 0,
            "validation_loss": 0,
            "metrics": self.training_metrics,
            "lr": get_lr(),
        }

        # Initial progress callback
        if print_callback is not None:
            print_callback(progress_dict)

        encode_time = 0
        loop_start = time.time()
        last_metrics_time = time.time()

        # 
        # Main training loop
        # 
        # Make sure the encoder is in eval mode, to avoid introducing randomness from e.g.
        # dropout or batch norm.
        # NOTE: (23/12/07, pjz) if we allow fine-tuning of the embedding_space model, we may want to
        # keep the encoder in training mode.
        encoder_mode = TrainingState.TRAIN if fine_tune else TrainingState.EVAL
        with PredictorTrainingContextManager(
            fsp=self, 
            predictor_mode=TrainingState.TRAIN, 
            encoder_mode=encoder_mode, 
            debugLabel="FeatrixSinglePredictor.train"):
            
            self.training_info = []
            
            # Track best model for checkpointing
            best_val_loss = float('inf')
            best_epoch = -1
            best_auc = -1.0  # Track best AUC separately
            best_auc_epoch = -1  # Track epoch with best AUC
            best_pr_auc = -1.0  # Track best PR-AUC (for imbalanced datasets)
            best_pr_auc_epoch = -1  # Track epoch with best PR-AUC
            self._best_composite_score = -1.0  # Track best composite score (when costs available)
            self._best_composite_score_epoch = -1  # Track epoch with best composite score
            best_model_state = None
            best_embedding_space_state = None
            best_checkpoint_path = None  # Track the path for logging
            
            # TRAINING RESTART LOOP
            # Wrap main training in try/except to catch FeatrixRestartTrainingException
            # This allows us to restart training with modified parameters when issues detected
            restart_loop_active = True
            restart_attempts = 0
            max_restart_attempts = self.max_training_restarts
            
            # ============================================================================
            # START: RESTART WHILE LOOP
            # ============================================================================
            while restart_loop_active and restart_attempts <= max_restart_attempts:
                try:
                    # ========================================================================
                    # START: EPOCH FOR LOOP (range(n_epochs))
                    # ========================================================================
                    _log_gpu_memory("START TRAINING LOOP")
                    for epoch_idx in range(n_epochs):
                        # Track current epoch for logging
                        self._current_epoch = epoch_idx
                        
                        training_info_entry = {}
                        training_info_entry['loss'] = None
                        training_info_entry['validation_loss'] = None

                        training_info_entry['start_time'] = time.time()
                        training_info_entry['epoch_idx'] = epoch_idx
                        
                        # Track hyperparameters at start of epoch
                        training_info_entry['hyperparameters'] = {}
                        # Get current learning rate
                        current_lr = get_lr()
                        lr_value = current_lr[0] if isinstance(current_lr, list) else current_lr
                        training_info_entry['hyperparameters']['learning_rate'] = float(lr_value) if lr_value is not None else None
                        
                        # Get current FocalLoss parameters if using FocalLoss
                        if isinstance(self.target_codec.loss_fn, FocalLoss):
                            training_info_entry['hyperparameters']['focal_gamma'] = float(self.target_codec.loss_fn.gamma)
                            training_info_entry['hyperparameters']['focal_min_weight'] = float(self.target_codec.loss_fn.min_weight)
                        else:
                            training_info_entry['hyperparameters']['focal_gamma'] = None
                            training_info_entry['hyperparameters']['focal_min_weight'] = None
                        # progress_dict.batch_idx = 0
                        # logger.debug("epoch_idx = ", epoch_idx)
                        
                        # ====================================================================
                        # START: BATCH FOR LOOP (enumerate(train_dataloader))
                        # ====================================================================
                        for batch_idx, column_batch in enumerate(train_dataloader):
                            # print("METADUDE: ", batch_idx, type(column_batch), column_batch)
                            progress_dict["batch_idx"] += 1
    
                            # Check for ABORT file periodically during batch processing (like ES training)
                            if batch_idx % 10 == 0 and job_id:
                                from featrix.neural.embedded_space import check_abort_files
                                abort_file_path = check_abort_files(job_id)
                                if abort_file_path:
                                    logger.error(f"🚫 ABORT file detected for job {job_id} during batch {batch_idx} - exiting single predictor training")
                                    logger.error(f"🚫 ABORT file path: {abort_file_path}")
                                    progress_dict["interrupted"] = "ABORT file detected"
                                
                                    # Mark job as FAILED before exiting
                                    try:
                                        from lib.job_manager import JobStatus
                                        from lib.job_manager import load_job, update_job_status
                                        from datetime import datetime
                                        from zoneinfo import ZoneInfo
                                        job_data = load_job(job_id)
                                        if job_data:
                                            update_job_status(job_id, JobStatus.FAILED, {
                                                "error_message": f"Training aborted due to ABORT file at {abort_file_path}"
                                            })
                                        logger.info(f"🚫 Job {job_id} marked as FAILED due to ABORT file")
                                    except Exception as e:
                                        logger.error(f"Failed to update job status before exit: {e}")
                                
                                    # Raise exception with the actual path found
                                    from featrix.neural.exceptions import FeatrixTrainingAbortedException
                                    raise FeatrixTrainingAbortedException(
                                        f"Single predictor training aborted due to ABORT file at {abort_file_path}",
                                        job_id=job_id,
                                        abort_file_path=abort_file_path
                                    )
                        
                            # Check for FINISH file periodically during batch processing (like ES training)
                            if batch_idx % 10 == 0 and job_id:
                                from featrix.neural.embedded_space import check_finish_files
                                if check_finish_files(job_id):
                                    logger.warning(f"⏹️  FINISH file detected for job {job_id} during batch {batch_idx} - graceful early stop")
                                    progress_dict["interrupted"] = "FINISH file detected"
                                    progress_dict["early_stop_reason"] = "User requested early stop via FINISH flag"
                                    # Break out of training loops to save model
                                    break
    
                            # Move data to same device as encoder
                            encoder_device = next(self.embedding_space.encoder.parameters()).device
                            for tokenbatch in column_batch.values():
                                tokenbatch.to(encoder_device)
    
                            # CRITICAL: Verify predictor is on GPU before training
                            predictor_device = next(self.predictor.parameters()).device if list(self.predictor.parameters()) else None
                            if epoch_idx == 0 and batch_idx == 0:
                                if torch.cuda.is_available():
                                    if predictor_device is None or predictor_device.type != 'cuda':
                                        logger.error(f"❌ PREDICTOR IS ON CPU! Moving to GPU...")
                                        self.predictor = self.predictor.cuda()
                                        predictor_device = next(self.predictor.parameters()).device
                                    logger.info(f"✅ PREDICTOR DEVICE VERIFICATION: {predictor_device}")
                                else:
                                    logger.info(f"⚠️  Running on CPU (CUDA not available)")
                            
                            # Make absolutely sure that the embedding space and predictor
                            # are in the right training state
                            assert self.predictor.training is True, f"epoch = {epoch_idx}; batch = {batch_idx} - training = {self.predictor.training}"
                            if fine_tune:
                                assert self.embedding_space.encoder.training is True
                            else:
                                assert self.embedding_space.encoder.training is False
    
                            # 
                            # Handle the presence of the target variable in the training batch.
                            # 
                            # Remove the target column from the batch to be encoded, so that we don't
                            # presume the present of the target when making the prediction.
                            # We need to create the marginal token batch to get the joint encoding that
                            # correspond to any possible value for the target value.
                            target_token_batch = column_batch.pop(self.target_col_name)  # noqa
    
                            # If the target column is in the original set of codecs for the embedding_space space,
                            # we need to replace the token we just took out with a token batch that has all the
                            # status values set to MARGINAL because we want to get a representation where the
                            # target column's value is not known.
                            target_column_in_original_df = (
                                self.target_col_name in self.embedding_space.col_codecs
                            )
                            if target_column_in_original_df:
                                marginal_token_batch = self._create_marginal_token_batch_for_target(
                                    target_token_batch
                                )
                                column_batch[self.target_col_name] = marginal_token_batch
    
                            # We are interested in direct values of the tokens, not their status, so we
                            # keep just the values.
                            targets = target_token_batch.value
    
                            # If the target is a scalar variable, add another dimension to match
                            # the overall shape of the predictions, and cast to a simple float.
                            # Predictions for scalars are outputs from MLPs, so they have a (B, 1) dimension, not
                            # just (B). We must add the additional dimension.
                            # NOTE: (23/12/07, pjx) this should be handles via polymorphism on the Codec class itself
                            if self.is_target_scalar:
                                targets = targets.float().unsqueeze(dim=1)
                            else:
                                # For set/categorical targets, CrossEntropyLoss expects integer class indices
                                targets = targets.long()
    
                            # 
                            # Encode the batch using the ES encoder
                            # 
                            enc_time = time.time()
                            # Encoder
                            # Apply noise so that some column embeddings are masked out with MARGINAL
                            # tokens. This helps regularize the downstream model, and make it robust
                            # to missing data at query time.
                            # Only use full-dimensional embeddings for the predictor.
                            try:
                                # CRITICAL: Verify encoder is in correct mode
                                encoder_device = next(self.embedding_space.encoder.parameters()).device if list(self.embedding_space.encoder.parameters()) else None
                                encoder_training = self.embedding_space.encoder.training
                                
                                # DIAGNOSTIC: Log encoder state on first batch
                                if epoch_idx == 0 and batch_idx == 0:
                                    logger.info(f"🔍 ENCODER DIAGNOSTIC [epoch={epoch_idx}, batch={batch_idx}]:")
                                    logger.info(f"   Encoder device: {encoder_device}")
                                    logger.info(f"   Encoder training mode: {encoder_training}")
                                    logger.info(f"   Fine-tune enabled: {fine_tune}")
                                    logger.info(f"   Column batch keys: {list(column_batch.keys())[:10]}... ({len(column_batch)} total)")
                                    
                                    # Check if column_batch has valid data
                                    for col_name, token_batch in list(column_batch.items())[:3]:
                                        if hasattr(token_batch, 'value'):
                                            val = token_batch.value
                                            logger.info(f"   Column '{col_name}': shape={val.shape}, device={val.device}, dtype={val.dtype}, min={val.min().item():.4f}, max={val.max().item():.4f}, mean={val.mean().item():.4f}")
                                
                                _, batch_full = self.embedding_space.encoder.encode(
                                    column_batch, apply_noise=True
                                )
                                
                                # CRITICAL DIAGNOSTIC: Check if encoding produced valid, varied outputs
                                if epoch_idx == 0 and batch_idx == 0:
                                    batch_std = batch_full.std().item()
                                    batch_min = batch_full.min().item()
                                    batch_max = batch_full.max().item()
                                    batch_mean = batch_full.mean().item()
                                    logger.info(f"🔍 ENCODING RESULT [epoch={epoch_idx}, batch={batch_idx}]:")
                                    logger.info(f"   Encoded batch shape: {batch_full.shape}, device: {batch_full.device}, dtype: {batch_full.dtype}")
                                    logger.info(f"   Encoded batch stats: min={batch_min:.4f}, max={batch_max:.4f}, mean={batch_mean:.4f}, std={batch_std:.6f}")
                                    
                                    if batch_std < 0.001:
                                        logger.error(f"⚠️  WARNING: Encoded batch has nearly zero std ({batch_std:.6f})!")
                                        logger.error(f"   This means the encoder is producing identical embeddings for all samples")
                                        logger.error(f"   Check if encoder is frozen and producing constant outputs")
                                    else:
                                        logger.info(f"   ✅ Encoded batch has variation (std={batch_std:.6f})")
                                
                                # CRITICAL FIX: Ensure all tensor dtypes are float32 before hitting linear layers
                                # SetCodec produces int64, StringCodec produces float32, causing dtype mismatch
                                if hasattr(batch_full, 'dtype') and batch_full.dtype != torch.float32:
                                    batch_full = batch_full.to(dtype=torch.float32)
                            
                                # CRITICAL FIX: If not fine-tuning, detach embeddings so gradients don't vanish
                                # When fine_tune=False, encoder params aren't in the optimizer, so gradients
                                # trying to flow through them just disappear, causing zero gradient bug
                                if not fine_tune:
                                    batch_full = batch_full.detach()
                                
                            except Exception as err:
                                print("self.embedding_space.encoder.encode failed:")
                                print(f"Error: {err}")
                                print(f"column_batch type: {type(column_batch)}")
                            
                                # Show device information for each column's tensors
                                if isinstance(column_batch, dict):
                                    print("Device information for column_batch:")
                                    for col_name, token_batch in column_batch.items():
                                        if hasattr(token_batch, 'values') and hasattr(token_batch.values, 'device'):
                                            values_device = token_batch.values.device
                                            print(f"  {col_name}: values on {values_device}")
                                        elif hasattr(token_batch, 'value') and hasattr(token_batch.value, 'device'):
                                            value_device = token_batch.value.device  
                                            print(f"  {col_name}: value on {value_device}")
                                        else:
                                            print(f"  {col_name}: no device info available ({type(token_batch)})")
                            
                                print(f"embedding_space.encoder device: {next(self.embedding_space.encoder.parameters()).device}")
                                print("------------------------------------------------------")
                                raise(err)
                        
                            batch = batch_full
                            enc_delta = time.time() - enc_time
                            encode_time += enc_delta
                            
                            # CRITICAL: Move batch to same device as predictor
                            # Encoder might be on CPU (force_cpu=True) but predictor is on GPU
                            predictor_device = next(self.predictor.parameters()).device
                            if batch.device != predictor_device:
                                batch = batch.to(predictor_device)
                            
                            # CRITICAL: Move targets to same device as predictor
                            if targets.device != predictor_device:
                                targets = targets.to(predictor_device)
                            
                            # DIAGNOSTIC: Check if batch embeddings are varying (should be different for each sample)
                            if epoch_idx == 0 and batch_idx == 0:
                                batch_std = batch.std().item()
                                batch_min = batch.min().item()
                                batch_max = batch.max().item()
                                batch_mean = batch.mean().item()
                                logger.info(f"🔍 BATCH EMBEDDING DIAGNOSTIC [epoch={epoch_idx}, batch={batch_idx}]:")
                                logger.info(f"   Batch shape: {batch.shape}, device: {batch.device}")
                                logger.info(f"   Batch stats: min={batch_min:.4f}, max={batch_max:.4f}, mean={batch_mean:.4f}, std={batch_std:.6f}")
                                if batch_std < 0.001:
                                    logger.error(f"⚠️  WARNING: Batch embeddings are nearly constant! std={batch_std:.6f}")
                                    logger.error(f"   This means encoder is producing identical embeddings for all samples")
                                    logger.error(f"   First 3 batch rows (first 5 dims): {batch[:3, :5].tolist()}")
                                else:
                                    logger.info(f"   ✅ Batch embeddings are varying (std={batch_std:.6f})")
    
                            # 
                            # MAIN STEP
                            # 
                            out = self.predictor(batch)
                            
                            # CRITICAL: Verify output is on correct device
                            if out.device != predictor_device:
                                logger.error(f"❌ MODEL OUTPUT ON WRONG DEVICE! out.device={out.device}, predictor_device={predictor_device}")
                                out = out.to(predictor_device)
                            
                            # DIAGNOSTIC: Log first batch and periodically to catch constant outputs
                            should_log_diagnostic = (epoch_idx == 0 and batch_idx == 0) or (batch_idx % 50 == 0 and epoch_idx < 3)
                            if should_log_diagnostic:
                                out_std = out.std().item()
                                out_min = out.min().item()
                                out_max = out.max().item()
                                out_mean = out.mean().item()
                                
                                logger.info(f"🔍 BATCH DIAGNOSTIC [epoch={epoch_idx}, batch={batch_idx}]:")
                                logger.info(f"   Output shape: {out.shape}, device: {out.device}")
                                logger.info(f"   Output stats: min={out_min:.4f}, max={out_max:.4f}, mean={out_mean:.4f}, std={out_std:.6f}")
                                logger.info(f"   Targets shape: {targets.shape}, device: {targets.device}, dtype: {targets.dtype}")
                                logger.info(f"   Batch device: {batch.device}, Predictor device: {predictor_device}")
                                
                                # Check if output is constant (bad sign)
                                if out_std < 0.001:
                                    logger.error(f"⚠️  WARNING: Model output is nearly constant! std={out_std:.6f}")
                                    logger.error(f"   This suggests the model isn't learning or inputs are constant")
                                    logger.error(f"   First 5 outputs: {out[:5].tolist()}")
                                    logger.error(f"   First 5 targets: {targets[:5].tolist()}")
                                
                                if epoch_idx == 0 and batch_idx == 0:
                                    if hasattr(self.target_codec, 'tokens_to_members'):
                                        logger.info(f"   Target codec mapping: {self.target_codec.tokens_to_members}")
                                    # Show raw logits before softmax
                                    logger.info(f"   First 3 raw logits (before softmax):")
                                    for i in range(min(3, out.shape[0])):
                                        logger.info(f"     Sample {i}: logits={out[i].tolist()}, target_token={targets[i].item()}")
    
                            main_loss = loss_fn(out, targets)
                            
                            # Add pairwise ranking loss for binary classification (if enabled)
                            total_loss = main_loss
                            if use_pairwise_ranking_loss and not self.is_target_scalar:
                                # Check if this is binary classification
                                is_binary_batch = (hasattr(self, 'target_codec') and 
                                                  isinstance(self.target_codec, SetCodec) and
                                                  len(self.target_codec.members) == 2)
                                
                                if is_binary_batch:
                                    # Extract logits for positive class (index 1) and negative class (index 0)
                                    # out shape: [batch_size, num_classes]
                                    # For binary: num_classes = 2 (negative=0, positive=1)
                                    pos_class_idx = 1
                                    neg_class_idx = 0
                                    
                                    # Get logits for positive and negative classes
                                    pos_logits = out[:, pos_class_idx]  # [batch_size]
                                    neg_logits = out[:, neg_class_idx]  # [batch_size]
                                    
                                    # Create binary labels: 1 for positive class, 0 for negative
                                    # targets contains class indices (0 or 1 for binary)
                                    y_binary = (targets == pos_class_idx).float()  # [batch_size]
                                    
                                    # Get positive and negative logits
                                    pos_mask = y_binary == 1
                                    neg_mask = y_binary == 0
                                    
                                    if pos_mask.sum() > 0 and neg_mask.sum() > 0:
                                        s_pos = pos_logits[pos_mask]  # [P] where P = number of positives
                                        s_neg = neg_logits[neg_mask]  # [N] where N = number of negatives
                                        
                                        # Compute pairwise differences: s_pos[i] - s_neg[j] for all pairs
                                        # Shape: [P, N]
                                        diff = s_pos.unsqueeze(1) - s_neg.unsqueeze(0)
                                        
                                        # Pairwise ranking loss: log(1 + exp(-diff))
                                        # This encourages positive examples to have higher scores than negative examples
                                        pairwise_loss = torch.log1p(torch.exp(-diff)).mean()
                                        
                                        # Combine with main loss
                                        total_loss = main_loss + pairwise_loss_weight * pairwise_loss
                                        
                                        # Log pairwise loss occasionally for debugging
                                        if batch_idx % 100 == 0:
                                            logger.debug(f"📊 Pairwise loss: {pairwise_loss.item():.6f}, main loss: {main_loss.item():.6f}, total: {total_loss.item():.6f}")
                            
                            loss = total_loss
    
                            optimizer.zero_grad()
                            
                            # CRITICAL FIX: Check loss value BEFORE backward pass
                            # This prevents gradient corruption from propagating
                            if torch.isnan(loss) or torch.isinf(loss):
                                logger.error(f"💥 FATAL: NaN/Inf loss detected BEFORE backward! loss={loss.item()}")
                                logger.error(f"   Epoch: {epoch_idx}, Batch: {batch_idx}")
                                logger.error(f"   Output stats: min={out.min().item():.4f}, max={out.max().item():.4f}, mean={out.mean().item():.4f}")
                                logger.error(f"   Target stats: min={targets.min().item()}, max={targets.max().item()}")
                                # Skip this batch entirely - don't corrupt gradients
                                logger.error("   ⚠️  SKIPPING THIS BATCH to prevent gradient corruption")
                                continue  # Skip to next batch
                            
                            loss.backward()
                        
                            # Compute unclipped gradient norm for diagnostics WITHOUT modifying gradients
                            # CRITICAL: Don't use clip_grad_norm_ with inf - it modifies gradients in-place!
                            # Use predictor parameters directly to ensure we're checking the right parameters
                            total_norm_squared = 0.0
                            for p in self.predictor.parameters():
                                if p.grad is not None:
                                    param_norm = p.grad.data.norm(2)
                                    total_norm_squared += param_norm.item() ** 2
                            # If fine-tuning, also include encoder parameters
                            if fine_tune:
                                for p in self.embedding_space.encoder.parameters():
                                    if p.grad is not None:
                                        param_norm = p.grad.data.norm(2)
                                        total_norm_squared += param_norm.item() ** 2
                            unclipped_norm = total_norm_squared ** 0.5
                        
                            # CRITICAL FIX: Gradient clipping to prevent parameter corruption in single predictor
                            # Set to 20.0 to prevent NaN/Inf explosions while allowing healthy gradient flow
                            max_grad_norm = 20.0
                            total_norm = torch.nn.utils.clip_grad_norm_(params, max_grad_norm)
                        
                            # Log gradient norms every 100 batches to diagnose learning issues
                            # Also check on first batch of each epoch if we've been seeing dead gradients
                            should_check_gradients = (batch_idx % 100 == 0) or (batch_idx == 0 and len(self.dead_gradient_epochs) > 0)
                            
                            if should_check_gradients:
                                current_lr = get_lr()
                                # get_lr() returns a list if scheduler is used, or a float otherwise
                                lr_value = current_lr[0] if isinstance(current_lr, list) else current_lr
                                clipped_ratio = (unclipped_norm / max_grad_norm) if unclipped_norm > max_grad_norm else 1.0
                                logger.info(f"📊 Gradients: unclipped={unclipped_norm:.6f}, clipped={total_norm:.6f}, ratio={clipped_ratio:.2f}x, lr={lr_value:.6e}")
                            
                            # Log LR at start of each epoch to track scheduler
                            if batch_idx == 0:
                                current_lr = get_lr()
                                lr_value = current_lr[0] if isinstance(current_lr, list) else current_lr
                                initial_lr = optimizer_params.get("lr", 0.001)
                                if scheduler is not None:
                                    # Check if we're in warmup (LR should be constant) or cosine annealing (LR should be decreasing)
                                    if epoch_idx < warmup_epochs:
                                        logger.info(f"📈 LR Schedule [epoch={epoch_idx}]: Warmup period (LR constant at {lr_value:.6e} for {warmup_epochs} epochs)")
                                    else:
                                        cosine_epoch = epoch_idx - warmup_epochs
                                        logger.info(f"📈 LR Schedule [epoch={epoch_idx}]: Cosine annealing (epoch {cosine_epoch}/{cosine_epochs}, LR={lr_value:.6e}, started at {initial_lr:.6e})")
                                else:
                                    logger.info(f"📈 LR Schedule [epoch={epoch_idx}]: No scheduler (LR fixed at {lr_value:.6e})")
                            
                                # DEAD GRADIENT DETECTION & RESTART MECHANISM
                                # This will raise FeatrixRestartTrainingException if conditions met
                                
                                # ENHANCED DEBUGGING: If gradients are dead, diagnose why
                                if unclipped_norm < self.dead_gradient_threshold:
                                    logger.error(f"🔍 DEAD GRADIENT DIAGNOSTICS (epoch={epoch_idx}, batch={batch_idx}):")
                                    logger.error(f"   Loss value: {loss.item():.6f}")
                                    logger.error(f"   Loss requires_grad: {loss.requires_grad}")
                                    logger.error(f"   Output stats: min={out.min().item():.4f}, max={out.max().item():.4f}, mean={out.mean().item():.4f}")
                                    logger.error(f"   Target stats: min={targets.min().item()}, max={targets.max().item()}")
                                    
                                    # Check which parameters have gradients
                                    params_with_grads = []
                                    params_without_grads = []
                                    params_not_requiring_grad = []
                                    total_params = 0
                                    
                                    for name, param in self.predictor.named_parameters():
                                        total_params += 1
                                        if not param.requires_grad:
                                            params_not_requiring_grad.append(name)
                                        elif param.grad is None:
                                            params_without_grads.append(name)
                                        else:
                                            grad_norm = param.grad.data.norm(2).item()
                                            if grad_norm > 0:
                                                params_with_grads.append((name, grad_norm))
                                    
                                    logger.error(f"   Total predictor parameters: {total_params}")
                                    logger.error(f"   Parameters requiring grad: {total_params - len(params_not_requiring_grad)}")
                                    logger.error(f"   Parameters with gradients: {len(params_with_grads)}")
                                    logger.error(f"   Parameters without gradients: {len(params_without_grads)}")
                                    
                                    if params_not_requiring_grad:
                                        logger.error(f"   ⚠️  Parameters NOT requiring grad (first 5): {params_not_requiring_grad[:5]}")
                                    if params_without_grads:
                                        logger.error(f"   ⚠️  Parameters with None gradients (first 5): {params_without_grads[:5]}")
                                    if params_with_grads:
                                        logger.error(f"   ✅ Parameters with non-zero gradients (first 5): {[(n, f'{v:.6e}') for n, v in params_with_grads[:5]]}")
                                    
                                    # Check embedding space encoder if fine-tuning
                                    if fine_tune:
                                        encoder_params_with_grads = []
                                        encoder_params_without_grads = []
                                        encoder_params_not_requiring_grad = []
                                        encoder_total = 0
                                        
                                        for name, param in self.embedding_space.encoder.named_parameters():
                                            encoder_total += 1
                                            if not param.requires_grad:
                                                encoder_params_not_requiring_grad.append(name)
                                            elif param.grad is None:
                                                encoder_params_without_grads.append(name)
                                            else:
                                                grad_norm = param.grad.data.norm(2).item()
                                                if grad_norm > 0:
                                                    encoder_params_with_grads.append((name, grad_norm))
                                        
                                        logger.error(f"   Encoder total parameters: {encoder_total}")
                                        logger.error(f"   Encoder parameters with gradients: {len(encoder_params_with_grads)}")
                                        logger.error(f"   Encoder parameters without gradients: {len(encoder_params_without_grads)}")
                                        
                                        if encoder_params_not_requiring_grad:
                                            logger.error(f"   ⚠️  Encoder parameters NOT requiring grad (first 5): {encoder_params_not_requiring_grad[:5]}")
                                    
                                    # Check if batch_full was detached
                                    if hasattr(batch_full, 'requires_grad'):
                                        logger.error(f"   Batch embeddings require_grad: {batch_full.requires_grad}")
                                    else:
                                        logger.error(f"   Batch embeddings type: {type(batch_full)}")
                                    
                                    # Check model training mode
                                    logger.error(f"   Predictor training mode: {self.predictor.training}")
                                    logger.error(f"   Encoder training mode: {self.embedding_space.encoder.training}")
                                
                                self.check_for_dead_gradients_and_raise(
                                    unclipped_norm=unclipped_norm,
                                    epoch_idx=epoch_idx,
                                    current_lr=lr_value
                                )
                        
                            # CRITICAL FIX: Detect NaN/Inf gradients BEFORE they corrupt parameters
                            # Changed from CRASH to SKIP to allow training to continue
                            if torch.isnan(total_norm) or torch.isinf(total_norm):
                                logger.error(f"💥 FATAL: NaN/Inf gradients in single predictor! total_norm={total_norm}")
                                logger.error(f"   Loss value: {loss.item()}")
                                logger.error(f"   Epoch: {epoch_idx}, Batch: {batch_idx}")
                                
                                # Check individual parameter gradients to identify the source
                                nan_params = []
                                for name, param in self.predictor.named_parameters():
                                    if param.grad is not None and (torch.isnan(param.grad).any() or torch.isinf(param.grad).any()):
                                        nan_params.append(name)
                                
                                if nan_params:
                                    logger.error(f"   Parameters with NaN/Inf gradients: {nan_params[:5]}...")
                                
                                # CRITICAL: Zero out corrupted gradients and skip this step
                                logger.error("   ⚠️  ZEROING corrupted gradients and SKIPPING optimizer step")
                                optimizer.zero_grad()
                                continue  # Skip to next batch
                        
                            optimizer.step()
                            # Note: Scheduler.step() moved to end of epoch for CosineAnnealingLR
    
                            progress_dict["time_now"] = time.time()
    
                            # NOTE: (pjz) We should rename this to `progress_dict.training_loss`.
                            progress_dict["current_loss"] = loss.item()
                            training_info_entry['loss'] = progress_dict["current_loss"]
    
                            progress_dict["lr"] = get_lr()
                            
                            # Update hyperparameters in training_info_entry after potential changes
                            current_lr = get_lr()
                            lr_value = current_lr[0] if isinstance(current_lr, list) else current_lr
                            training_info_entry['hyperparameters']['learning_rate'] = float(lr_value) if lr_value is not None else None
                            
                            # Update FocalLoss parameters if they changed during this epoch
                            if isinstance(self.target_codec.loss_fn, FocalLoss):
                                training_info_entry['hyperparameters']['focal_gamma'] = float(self.target_codec.loss_fn.gamma)
                                training_info_entry['hyperparameters']['focal_min_weight'] = float(self.target_codec.loss_fn.min_weight)
    
                            # 
                            # After each batch, run validation.
                            # 
                            if validation_batch is not None:
                                val_loss = self.compute_val_loss(
                                    validation_batch,
                                    val_target_token_batch,
                                    validation_targets,
                                    loss_fn,
                                )
                                progress_dict["validation_loss"] = val_loss
                                training_info_entry['validation_loss'] = progress_dict["validation_loss"]
    
                                # Removed: in-batch metrics calculation (was every 5 minutes)
                                # Now only calculate metrics at end of each epoch for consistency
                                # print(progress_dict.model_dump())
    
                            # TODO: dump the validation loss to metadata in a way that preserves
                            # the history for all training epochs.
    
                            # Update progress without recalculating metrics (done once per epoch now)
                            if progress_dict["progress_counter"] % print_progress_step == 0:
                                if print_callback is not None:
                                    print_callback(progress_dict)
    
                            progress_dict["progress_counter"] += 1
                        # ====================================================================
                        # END: BATCH FOR LOOP (enumerate(train_dataloader))
                        # ====================================================================
                    
                        # Check if FINISH flag caused early break from batch loop
                        if progress_dict.get("interrupted") == "FINISH file detected":
                            logger.info(f"⏹️  Breaking epoch loop due to FINISH flag")
                            break
    
                        # ALWAYS compute validation metrics at least once per epoch
                        # This is critical for detecting overfitting and monitoring training health
                        # We compute the full metrics every epoch, but may log them less frequently
                        # to reduce noise in progress callbacks
                    
                        # ASSERT: Before calling metrics, we should still be in training mode
                        # (The metrics function will temporarily switch to eval mode)
                        assert self.predictor.training == True, f"❌ TRAINING BUG: predictor should be in train mode before metrics but training={self.predictor.training}"
                    
                        try:
                            self.training_metrics = self.compute_classification_metrics(
                                val_queries, val_targets, val_pos_label, epoch_idx=epoch_idx, n_epochs=n_epochs
                            )
                        except:
                            logger.exception("error with compute_classification_metrics")
                        _log_gpu_memory(f"AFTER COMPUTE_CLASSIFICATION_METRICS (epoch {epoch_idx})", log_level=logging.DEBUG)
                    
                        # Check for resolved warnings at end of epoch
                        # DEAD_GRADIENTS is checked during batch loop, so if we got here without dead gradients
                        # and it was active before, it's resolved
                        if hasattr(self, '_active_warnings') and "DEAD_GRADIENTS" in self._active_warnings:
                            # If dead_gradient_epochs is empty, gradients recovered
                            if not self.dead_gradient_epochs:
                                # Already tracked in check_for_dead_gradients_and_raise, but double-check
                                pass  # Already handled in the check method
                        
                        # Save timeline every 10 epochs (like ES training saves every 5)
                        if epoch_idx % 10 == 0 or epoch_idx == n_epochs - 1:
                            _log_gpu_memory(f"BEFORE SAVE_TRAINING_TIMELINE (epoch {epoch_idx})", log_level=logging.DEBUG)
                            self.save_training_timeline(
                                output_dir=self._output_dir,
                                current_epoch=epoch_idx,
                                total_epochs=n_epochs
                            )
                            _log_gpu_memory(f"AFTER SAVE_TRAINING_TIMELINE (epoch {epoch_idx})", log_level=logging.DEBUG)
                    
                        # ASSERT: After metrics, we should be back in training mode
                        assert self.predictor.training == True, f"❌ TRAINING BUG: predictor should be back in train mode after metrics but training={self.predictor.training}"
                        logger.debug("✓ Training loop: Models correctly restored to TRAIN mode after metrics")
                    
                        progress_dict["metrics"] = self.training_metrics
    
                        _log_gpu_memory(f"BEFORE COPY.DEEPCOPY METRICS (epoch {epoch_idx})", log_level=logging.INFO)
                        training_info_entry['metrics'] = copy.deepcopy(progress_dict["metrics"])
                        _log_gpu_memory(f"AFTER COPY.DEEPCOPY METRICS (epoch {epoch_idx})", log_level=logging.INFO)
                        
                        # Add comprehensive epoch snapshot to timeline for this epoch (include ALL metrics)
                        if hasattr(self, '_training_timeline'):
                            epoch_entry = {
                                "epoch": epoch_idx,
                                "event_type": "epoch_summary",
                                "hyperparameters": training_info_entry['hyperparameters'].copy(),
                                "train_loss": training_info_entry.get('loss'),
                                "validation_loss": training_info_entry.get('validation_loss'),
                                "metrics": copy.deepcopy(progress_dict.get("metrics", {})),  # Include ALL calculated metrics
                                "learning_rate": training_info_entry['hyperparameters'].get('learning_rate'),
                                "time_now": progress_dict.get("time_now"),
                            }
                            # Add any other progress_dict fields that might be useful
                            if "lr" in progress_dict:
                                epoch_entry["lr"] = progress_dict["lr"]
                            self._training_timeline.append(epoch_entry)
    
                        self.training_info.append(training_info_entry)
                    
                        # 🎯 CHECKPOINT: Save best model after epoch 3
                        current_val_loss = progress_dict.get("validation_loss", float('inf'))
                        current_auc = -1.0
                        current_pr_auc = -1.0
                        if progress_dict.get("metrics") and progress_dict["metrics"].get("auc") is not None:
                            current_auc = progress_dict["metrics"]["auc"]
                        if progress_dict.get("metrics") and progress_dict["metrics"].get("pr_auc") is not None:
                            current_pr_auc = progress_dict["metrics"]["pr_auc"]
                        
                        # Log validation loss at end of each epoch
                        current_train_loss = progress_dict.get("current_loss", 0)
                        if current_val_loss != float('inf'):
                            if use_auc_for_best_epoch and current_auc >= 0:
                                pr_auc_str = f", PR-AUC: {current_pr_auc:.4f}" if current_pr_auc >= 0 else ""
                                logger.info(f"📊 [epoch={epoch_idx + 1}/{n_epochs}] Train Loss: {current_train_loss:.4f} | Val Loss: {current_val_loss:.4f} | ROC-AUC: {current_auc:.4f}{pr_auc_str}")
                            else:
                                logger.info(f"📊 [epoch={epoch_idx + 1}/{n_epochs}] Train Loss: {current_train_loss:.4f} | Val Loss: {current_val_loss:.4f}")
                        else:
                            logger.info(f"📊 [epoch={epoch_idx + 1}/{n_epochs}] Train Loss: {current_train_loss:.4f} | Val Loss: N/A")
                        
                        # Determine if this is a new best epoch based on selection metric
                        is_new_best = False
                        if epoch_idx >= 3:
                            # Check if we have cost parameters - if so, use composite score
                            use_composite_score = (
                                self.cost_false_positive is not None and 
                                self.cost_false_negative is not None and
                                use_auc_for_best_epoch and 
                                current_auc >= 0
                            )
                            
                            if use_composite_score:
                                # Use composite score (PR-AUC + cost savings + ROC-AUC)
                                current_composite_score = progress_dict.get("metrics", {}).get("composite_score")
                                if current_composite_score is not None:
                                    if not hasattr(self, '_best_composite_score') or self._best_composite_score < 0:
                                        self._best_composite_score = -1.0
                                        self._best_composite_score_epoch = -1
                                    
                                    if current_composite_score > self._best_composite_score + 1e-4:
                                        previous_best_score = self._best_composite_score
                                        previous_best_score_epoch = self._best_composite_score_epoch if self._best_composite_score_epoch >= 0 else -1
                                        self._best_composite_score = current_composite_score
                                        self._best_composite_score_epoch = epoch_idx
                                        
                                        # Also update individual metric tracking
                                        best_auc = current_auc
                                        best_auc_epoch = epoch_idx
                                        if current_pr_auc >= 0:
                                            best_pr_auc = current_pr_auc
                                            best_pr_auc_epoch = epoch_idx
                                        
                                        is_new_best = True
                                        score_components = progress_dict.get("metrics", {}).get("score_components", {})
                                        if previous_best_score_epoch >= 0:
                                            logger.info(f"   ⭐ New best composite score: {current_composite_score:.4f} (previous: {previous_best_score:.4f} @ epoch {previous_best_score_epoch})")
                                            logger.info(f"      ROC-AUC: {current_auc:.4f}, PR-AUC: {current_pr_auc:.4f if current_pr_auc >= 0 else 'N/A'}, Cost savings: {score_components.get('cost_savings', 0):.3f}")
                                            logger.info(f"      Weights: α={score_components.get('alpha', 0):.2f}, β={score_components.get('beta', 0):.2f}, γ={score_components.get('gamma', 0):.2f}")
                                        else:
                                            logger.info(f"   ⭐ New best composite score: {current_composite_score:.4f} (first valid score)")
                                            logger.info(f"      ROC-AUC: {current_auc:.4f}, PR-AUC: {current_pr_auc:.4f if current_pr_auc >= 0 else 'N/A'}")
                            elif use_auc_for_best_epoch and current_auc >= 0:
                                # Use AUC for binary classification (fallback when no costs)
                                # For imbalanced datasets, PR-AUC is often more informative than ROC-AUC
                                # Check if dataset is imbalanced (positive rate < 0.3 or > 0.7)
                                is_imbalanced = False
                                if hasattr(self, 'distribution_metadata') and self.distribution_metadata:
                                    imbalance_score = self.distribution_metadata.get('imbalance_score', 1.0)
                                    # imbalance_score is minority_ratio, so < 0.3 means imbalanced
                                    is_imbalanced = imbalance_score < 0.3
                                
                                # For imbalanced datasets, prefer PR-AUC; otherwise use ROC-AUC
                                use_pr_auc = is_imbalanced and current_pr_auc >= 0
                                
                                if use_pr_auc:
                                    # Use PR-AUC for imbalanced datasets
                                    if current_pr_auc > best_pr_auc:
                                        previous_best_pr_auc = best_pr_auc
                                        previous_best_pr_auc_epoch = best_pr_auc_epoch if best_pr_auc_epoch >= 0 else -1
                                        best_pr_auc = current_pr_auc
                                        best_pr_auc_epoch = epoch_idx
                                        # Also update ROC-AUC tracking
                                        best_auc = current_auc
                                        best_auc_epoch = epoch_idx
                                        is_new_best = True
                                        if previous_best_pr_auc_epoch >= 0:
                                            logger.info(f"   ⭐ New best PR-AUC: {best_pr_auc:.4f} (ROC-AUC: {current_auc:.4f}, previous PR-AUC: {previous_best_pr_auc:.4f} @ epoch {previous_best_pr_auc_epoch})")
                                        else:
                                            logger.info(f"   ⭐ New best PR-AUC: {best_pr_auc:.4f} (ROC-AUC: {current_auc:.4f}, first valid PR-AUC)")
                                else:
                                    # Use ROC-AUC for balanced datasets
                                    if current_auc > best_auc:
                                        previous_best_auc = best_auc
                                        previous_best_auc_epoch = best_auc_epoch if best_auc_epoch >= 0 else -1
                                        best_auc = current_auc
                                        best_auc_epoch = epoch_idx
                                        # Also track PR-AUC if available
                                        if current_pr_auc >= 0:
                                            best_pr_auc = current_pr_auc
                                            best_pr_auc_epoch = epoch_idx
                                        is_new_best = True
                                        if previous_best_auc_epoch >= 0:
                                            logger.info(f"   ⭐ New best ROC-AUC: {best_auc:.4f} (PR-AUC: {current_pr_auc:.4f if current_pr_auc >= 0 else 'N/A'}, previous: {previous_best_auc:.4f} @ epoch {previous_best_auc_epoch})")
                                        else:
                                            logger.info(f"   ⭐ New best ROC-AUC: {best_auc:.4f} (PR-AUC: {current_pr_auc:.4f if current_pr_auc >= 0 else 'N/A'}, first valid AUC)")
                            else:
                                # Use validation loss for scalar/regression or when AUC not available
                                if current_val_loss < best_val_loss:
                                    previous_best = best_val_loss
                                    best_val_loss = current_val_loss
                                    best_epoch = epoch_idx
                                    is_new_best = True
                                    if epoch_idx >= 20:
                                        logger.info(f"   ⭐ New best validation loss: {best_val_loss:.4f} (previous best: {previous_best:.4f})")
                                    else:
                                        logger.debug(f"   ⭐ New best val loss: {best_val_loss:.4f} (epoch {epoch_idx} < 20, not saving checkpoint)")
                        
                        # Check /NODUMP file - skip best checkpoint saves unless last fold
                        nodump_exists = os.path.exists('/NODUMP')
                        is_last_fold = getattr(self, 'is_last_fold', True)  # Assume True if not set
                        
                        should_save_best = is_new_best and epoch_idx >= 20 and (not nodump_exists or is_last_fold)
                        
                        if is_new_best and epoch_idx >= 20:
                            if nodump_exists and not is_last_fold:
                                logger.info(f"   ⏭️  /NODUMP exists and not last fold - skipping best checkpoint save")
                            elif nodump_exists and is_last_fold:
                                logger.info(f"   ✅ /NODUMP exists BUT this is last fold - saving best checkpoint anyway")
                        
                        if should_save_best:
                            _log_gpu_memory(f"BEFORE BEST CHECKPOINT SAVE (epoch {epoch_idx})", log_level=logging.INFO)
                            
                            # Update best_epoch to the appropriate one
                            if use_composite_score and hasattr(self, '_best_composite_score_epoch') and self._best_composite_score_epoch >= 0:
                                # Use composite score epoch
                                best_epoch = self._best_composite_score_epoch
                            elif use_auc_for_best_epoch and current_auc >= 0:
                                # Use PR-AUC epoch if we're using PR-AUC for selection, otherwise ROC-AUC epoch
                                if hasattr(self, 'distribution_metadata') and self.distribution_metadata:
                                    imbalance_score = self.distribution_metadata.get('imbalance_score', 1.0)
                                    is_imbalanced = imbalance_score < 0.3
                                    if is_imbalanced and best_pr_auc_epoch >= 0:
                                        best_epoch = best_pr_auc_epoch
                                    else:
                                        best_epoch = best_auc_epoch
                                else:
                                    best_epoch = best_auc_epoch
                            else:
                                # best_epoch already set above for validation loss case
                                pass
                        
                            # Track warnings at best epoch
                            self.best_epoch_warnings = []
                            metrics = progress_dict.get("metrics", {})
                            if metrics and metrics.get("failure_detected"):
                                self.best_epoch_warnings.append({
                                    "type": metrics.get("failure_label", "UNKNOWN"),
                                    "epoch": epoch_idx,
                                    "details": {
                                        "recommendations": metrics.get("recommendations", []),
                                        "auc": metrics.get("auc"),
                                        "accuracy": metrics.get("accuracy")
                                    }
                                })
                        
                            _log_gpu_memory(f"BEFORE STATE_DICT CALLS (epoch {epoch_idx})", log_level=logging.INFO)
                            # Save model states
                            # Note: state_dict() returns a regular dict, so no need for deepcopy
                            best_model_state = self.predictor.state_dict()
                            best_embedding_space_state = self.embedding_space.encoder.state_dict()
                            _log_gpu_memory(f"AFTER STATE_DICT CALLS (epoch {epoch_idx})", log_level=logging.INFO)
                        
                            # Build filename with optional identifier
                            id_suffix = f"_{sp_identifier}" if sp_identifier else ""
                        
                            # Save full pickle checkpoint - USE OUTPUT DIRECTORY to avoid cross-job conflicts!
                            checkpoint_dir = self._output_dir if self._output_dir else "."
                            
                            # Build checkpoint filename with appropriate metric
                            if use_auc_for_best_epoch and current_auc >= 0:
                                checkpoint_path = os.path.join(checkpoint_dir, f"best_single_predictor{id_suffix}_epoch_{epoch_idx}_auc_{current_auc:.4f}.pickle")
                                metric_info = f"AUC={current_auc:.4f}"
                            else:
                                checkpoint_path = os.path.join(checkpoint_dir, f"best_single_predictor{id_suffix}_epoch_{epoch_idx}_valloss_{current_val_loss:.4f}.pickle")
                                metric_info = f"val_loss={current_val_loss:.4f}"
                            
                            best_checkpoint_path = checkpoint_path  # Track for later restore message
                            try:
                                _log_gpu_memory(f"BEFORE BEST CHECKPOINT PICKLE.DUMP (epoch {epoch_idx})", log_level=logging.INFO)
                                # Try saving on GPU first
                                with open(checkpoint_path, "wb") as f:
                                    pickle.dump(self, f)
                                _log_gpu_memory(f"AFTER BEST CHECKPOINT PICKLE.DUMP (epoch {epoch_idx})", log_level=logging.INFO)
                                logger.info(f"💾 BEST MODEL CHECKPOINT: Saved to {checkpoint_path}")
                                if use_auc_for_best_epoch and current_auc >= 0:
                                    logger.info(f"   Epoch {epoch_idx}: {metric_info} (previous best AUC: {best_auc:.4f})")
                                else:
                                    logger.info(f"   Epoch {epoch_idx}: {metric_info} (previous best: {best_val_loss:.4f})")
                            
                                # Also save just the state dicts for easier loading
                                state_dict_path = os.path.join(checkpoint_dir, f"best_model_state{id_suffix}_epoch_{epoch_idx}.pt")
                                checkpoint_metadata = {
                                    'epoch': epoch_idx,
                                    'predictor_state_dict': best_model_state,
                                    'embedding_space_state_dict': best_embedding_space_state,
                                    'val_loss': current_val_loss,
                                    'optimizer_state_dict': optimizer.state_dict(),
                                    'metrics': self.training_metrics,
                                    'sp_identifier': sp_identifier,
                                }
                                # Add AUC if using AUC-based selection
                                if use_auc_for_best_epoch and current_auc >= 0:
                                    checkpoint_metadata['auc'] = current_auc
                                    checkpoint_metadata['best_metric'] = 'auc'
                                else:
                                    checkpoint_metadata['best_metric'] = 'val_loss'
                                
                                torch.save(checkpoint_metadata, state_dict_path)
                                logger.info(f"💾 Model state dicts saved to {state_dict_path}")
                            except RuntimeError as save_error:
                                # Handle CUDA OOM during best checkpoint save
                                error_msg = str(save_error).lower()
                                if "cuda" in error_msg and ("out of memory" in error_msg or "oom" in error_msg):
                                    logger.warning(f"⚠️  Failed to save best checkpoint due to CUDA OOM, trying CPU...")
                                    try:
                                        # Store original device locations
                                        predictor_device = next(self.predictor.parameters()).device if list(self.predictor.parameters()) else None
                                        encoder_device = next(self.embedding_space.encoder.parameters()).device if list(self.embedding_space.encoder.parameters()) else None
                                        
                                        # Move models to CPU for checkpoint saving (to avoid GPU memory issues)
                                        if predictor_device and predictor_device.type == 'cuda':
                                            self.predictor = self.predictor.cpu()
                                        if encoder_device and encoder_device.type == 'cuda':
                                            self.embedding_space.encoder = self.embedding_space.encoder.cpu()
                                        
                                        # Clear CUDA cache
                                        if torch.cuda.is_available():
                                            torch.cuda.empty_cache()
                                            torch.cuda.synchronize()
                                        
                                        # Try saving again on CPU
                                        with open(checkpoint_path, "wb") as f:
                                            pickle.dump(self, f)
                                        
                                        logger.info(f"✅ Best checkpoint saved on CPU: {checkpoint_path}")
                                        
                                        # Move models back to original device
                                        if predictor_device and predictor_device.type == 'cuda':
                                            self.predictor = self.predictor.to(predictor_device)
                                        if encoder_device and encoder_device.type == 'cuda':
                                            self.embedding_space.encoder = self.embedding_space.encoder.to(encoder_device)
                                    except Exception as cpu_save_error:
                                        logger.error(f"❌ Failed to save best checkpoint on CPU: {cpu_save_error}")
                                        # Try to move models back
                                        try:
                                            if predictor_device and predictor_device.type == 'cuda':
                                                self.predictor = self.predictor.to(predictor_device)
                                            if encoder_device and encoder_device.type == 'cuda':
                                                self.embedding_space.encoder = self.embedding_space.encoder.to(encoder_device)
                                        except Exception:
                                            pass
                                else:
                                    logger.error(f"❌ Failed to save checkpoint: {save_error}")
                            except Exception as e:
                                logger.error(f"❌ Failed to save checkpoint: {e}")
    
                        # Determine if we should send progress callback this epoch
                        # Use smart frequency for callbacks to reduce noise, but always callback on last epoch
                        should_send_callback = False
                        if n_epochs <= 10:
                            # Short training: send every epoch
                            should_send_callback = True
                        elif n_epochs <= 50:
                            # Medium training: send every 2 epochs or ~10% intervals
                            should_send_callback = (epoch_idx % 2 == 0) or (epoch_idx == n_epochs - 1)
                        elif n_epochs <= 100:
                            # Long training: send every 5 epochs or ~10% intervals  
                            should_send_callback = (epoch_idx % 5 == 0) or (epoch_idx == n_epochs - 1)
                        else:
                            # Very long training: send every 10 epochs or ~10% intervals
                            interval = max(10, n_epochs // 10)  # At least every 10 epochs, or 10% of total
                            should_send_callback = (epoch_idx % interval == 0) or (epoch_idx == n_epochs - 1)
                    
                        # End of every epoch where we want to send update
                        if should_send_callback and print_callback is not None:
                            print_callback(progress_dict)
    
                        # Update last_metrics_time at end of epoch
                        time_now = time.time()
                        last_metrics_time = time_now
                        progress_dict["epoch_idx"] += 1
                        
                        # Step the learning rate scheduler at the end of each epoch
                        # (CosineAnnealingLR steps per epoch, not per batch like OneCycleLR)
                        if scheduler is not None:
                            scheduler.step()
                        
                        # Check for /NODUMP file - skip all checkpoints if it exists
                        nodump_exists = os.path.exists('/NODUMP')
                        
                        # PERIODIC CHECKPOINT: Save every 2 epochs for inference
                        # This allows users to test the model during training
                        checkpoint_interval = 2  # Save every 2 epochs
                        should_save_periodic = (
                            not nodump_exists and
                            epoch_idx > 0 and  # Don't save at epoch 0
                            epoch_idx % checkpoint_interval == 0  # Every 2 epochs
                        )
                        
                        # Save hourly checkpoint (only after 59 min, then every 60 min)
                        elapsed_minutes = (time.time() - training_start_time) / 60.0
                        minutes_since_last = (time.time() - last_checkpoint_time[0]) / 60.0
                        
                        logger.debug(f"🕐 Checkpoint check (epoch {epoch_idx}): elapsed={elapsed_minutes:.1f}min, since_last={minutes_since_last:.1f}min, /NODUMP={'EXISTS' if nodump_exists else 'not found'}")
                        
                        should_save_hourly = (
                            not nodump_exists and  # Skip if /NODUMP exists
                            elapsed_minutes >= 59.0 and 
                            minutes_since_last >= 60.0
                        )
                        
                        # Save checkpoint if periodic OR hourly
                        should_save_checkpoint = should_save_periodic or should_save_hourly
                        
                        if nodump_exists:
                            logger.debug(f"⏭️  SKIPPING checkpoint: /NODUMP file exists")
                        elif should_save_periodic:
                            logger.info(f"✅ PERIODIC CHECKPOINT: epoch {epoch_idx} (every {checkpoint_interval} epochs)")
                        elif should_save_hourly:
                            logger.info(f"✅ HOURLY CHECKPOINT: elapsed={elapsed_minutes:.1f}min >= 59, since_last={minutes_since_last:.1f}min >= 60")
                        else:
                            logger.debug(f"⏭️  SKIPPING checkpoint: elapsed={elapsed_minutes:.1f}min (need 59+), since_last={minutes_since_last:.1f}min (need 60+)")
                        
                        if should_save_checkpoint:
                            checkpoint_type = "PERIODIC" if should_save_periodic else "HOURLY"
                            logger.info(f"")
                            if should_save_periodic:
                                logger.info(f"💾 PERIODIC CHECKPOINT (epoch {epoch_idx}, every {checkpoint_interval} epochs)")
                            else:
                                logger.info(f"💾 HOURLY CHECKPOINT (elapsed: {elapsed_minutes:.1f} min, since last: {minutes_since_last:.1f} min)")
                            checkpoint_start_time = time.time()
                            try:
                                _log_gpu_memory(f"BEFORE EPOCH CHECKPOINT SAVE (epoch {epoch_idx})", log_level=logging.INFO)
                                
                                # Clear CUDA cache before saving checkpoint to free up memory
                                if torch.cuda.is_available():
                                    torch.cuda.empty_cache()
                                    torch.cuda.synchronize()
                                
                                checkpoint_dir = self._output_dir if self._output_dir else "."
                                id_suffix = f"_{sp_identifier}" if sp_identifier else ""
                                # Use different naming for periodic vs hourly checkpoints
                                if should_save_periodic:
                                    epoch_checkpoint_path = os.path.join(checkpoint_dir, f"single_predictor{id_suffix}_epoch_{epoch_idx}.pickle")
                                else:
                                    epoch_checkpoint_path = os.path.join(checkpoint_dir, f"single_predictor{id_suffix}_epoch_{epoch_idx}_hourly.pickle")
                                
                                _log_gpu_memory(f"BEFORE FIRST EPOCH CHECKPOINT PICKLE.DUMP (epoch {epoch_idx})", log_level=logging.INFO)
                                # Save checkpoint with training status metadata
                                with open(epoch_checkpoint_path, "wb") as f:
                                    pickle.dump(self, f)
                                _log_gpu_memory(f"AFTER FIRST EPOCH CHECKPOINT PICKLE.DUMP (epoch {epoch_idx})", log_level=logging.INFO)
                                
                                checkpoint_time = time.time() - checkpoint_start_time
                                logger.info(f"💾 Epoch checkpoint saved: {epoch_checkpoint_path} ({checkpoint_time:.3f}s)")
                                last_checkpoint_time[0] = time.time()
                                
                                # Also save a "latest" checkpoint for easy access
                                latest_checkpoint_path = os.path.join(checkpoint_dir, f"single_predictor{id_suffix}_latest.pickle")
                                with open(latest_checkpoint_path, "wb") as f:
                                    pickle.dump(self, f)
                                
                                # Save training status metadata JSON for quick access without loading pickle
                                # Get current metrics if available
                                current_metrics = None
                                if hasattr(self, 'training_metrics') and self.training_metrics:
                                    current_metrics = self.training_metrics.copy()
                                
                                status_metadata = {
                                    "epoch": epoch_idx,
                                    "total_epochs": n_epochs,
                                    "progress_percent": (epoch_idx + 1) / n_epochs * 100 if n_epochs > 0 else 0,
                                    "training_loss": progress_dict.get("current_loss"),
                                    "validation_loss": progress_dict.get("validation_loss"),
                                    "metrics": current_metrics,
                                    "checkpoint_path": epoch_checkpoint_path,
                                    "latest_checkpoint_path": latest_checkpoint_path,
                                    "checkpoint_save_time_secs": checkpoint_time,
                                    "is_training": True,
                                    "timestamp": time.time(),
                                    "data_passes": epoch_idx + 1  # Number of data passes completed
                                }
                                status_metadata_path = os.path.join(checkpoint_dir, f"single_predictor{id_suffix}_training_status.json")
                                with open(status_metadata_path, "w") as f:
                                    json.dump(status_metadata, f, indent=2, default=str)
                                
                            except RuntimeError as checkpoint_error:
                                # Handle CUDA OOM during checkpoint save
                                error_msg = str(checkpoint_error).lower()
                                checkpoint_time = time.time() - checkpoint_start_time
                                if "cuda" in error_msg and ("out of memory" in error_msg or "oom" in error_msg):
                                    # Dump memory usage to understand what's holding VRAM
                                    _dump_cuda_memory_usage(context=f"checkpoint save (epoch {epoch_idx})")
                                logger.warning(f"⚠️  Failed to save epoch checkpoint due to CUDA OOM (took {checkpoint_time:.3f}s)")
                                
                                # Try saving on CPU instead - save full pickle after moving everything to CPU
                                logger.info(f"🔄 Attempting to save checkpoint on CPU to avoid CUDA OOM...")
                                try:
                                    force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
                                    
                                    # DETAILED DEVICE CHECK - log what's on GPU before moving
                                    logger.error("="*80)
                                    logger.error("🔍 DETAILED DEVICE CHECK BEFORE MOVING TO CPU:")
                                    logger.error("="*80)
                                    
                                    # Check predictor
                                    if list(self.predictor.parameters()):
                                        predictor_device = next(self.predictor.parameters()).device
                                        predictor_params = sum(p.numel() for p in self.predictor.parameters())
                                        logger.error(f"   Predictor: {predictor_device.type} (device: {predictor_device}), {predictor_params:,} params")
                                    else:
                                        predictor_device = None
                                        logger.error(f"   Predictor: No parameters")
                                    
                                    # Check encoder
                                    if hasattr(self.embedding_space, 'encoder') and self.embedding_space.encoder is not None:
                                        if list(self.embedding_space.encoder.parameters()):
                                            encoder_device = next(self.embedding_space.encoder.parameters()).device
                                            encoder_params = sum(p.numel() for p in self.embedding_space.encoder.parameters())
                                            logger.error(f"   Encoder: {encoder_device.type} (device: {encoder_device}), {encoder_params:,} params")
                                        else:
                                            encoder_device = None
                                            logger.error(f"   Encoder: No parameters")
                                    else:
                                        encoder_device = None
                                        logger.error(f"   Encoder: Not found")
                                    
                                    # Check codecs for GPU state - only log if found (StringCodec has parameters!)
                                    gpu_codecs_found = []
                                    if hasattr(self.embedding_space, 'col_codecs'):
                                        for col_name, codec in self.embedding_space.col_codecs.items():
                                            codec_has_gpu = False
                                            codec_params = 0
                                            
                                            # Check parameters (StringCodec, JsonCodec have these!)
                                            if hasattr(codec, 'parameters') and list(codec.parameters()):
                                                codec_device = next(codec.parameters()).device
                                                codec_params = sum(p.numel() for p in codec.parameters())
                                                if codec_device.type == 'cuda':
                                                    codec_has_gpu = True
                                                    gpu_codecs_found.append((col_name, codec_device, codec_params, 'params'))
                                            
                                            # Check buffers
                                            if not codec_has_gpu and hasattr(codec, 'buffers') and isinstance(codec, torch.nn.Module):
                                                for buffer in codec.buffers():
                                                    if buffer.device.type == 'cuda':
                                                        codec_has_gpu = True
                                                        buffer_size = sum(b.numel() for b in codec.buffers() if b.device.type == 'cuda')
                                                        gpu_codecs_found.append((col_name, buffer.device, buffer_size, 'buffers'))
                                                        break
                                            
                                            # Check embedded modules (StringCodec: bert_projection, feature_embedding_mlp, merge_mlp)
                                            for attr_name in ['bert_projection', 'feature_embedding_mlp', 'merge_mlp', 'projection', 'encoder']:
                                                if hasattr(codec, attr_name):
                                                    embedded_module = getattr(codec, attr_name)
                                                    if embedded_module is not None and hasattr(embedded_module, 'parameters'):
                                                        if list(embedded_module.parameters()):
                                                            embedded_device = next(embedded_module.parameters()).device
                                                            if embedded_device.type == 'cuda':
                                                                embedded_params = sum(p.numel() for p in embedded_module.parameters())
                                                                if not any(c[0] == col_name for c in gpu_codecs_found):
                                                                    gpu_codecs_found.append((col_name, embedded_device, embedded_params, f'{attr_name}'))
                                    
                                    if gpu_codecs_found:
                                        logger.error(f"   🚨 Found {len(gpu_codecs_found)} codecs with GPU state:")
                                        total_gpu_params = sum(params for _, _, params, _ in gpu_codecs_found)
                                        logger.error(f"   Total GPU params in codecs: {total_gpu_params:,}")
                                        for col_name, device, params, source in gpu_codecs_found:
                                            logger.error(f"      - {col_name}: {params:,} params on {device} ({source})")
                                    logger.error("="*80)
                                    
                                    # Move models to CPU (only if not already in CPU mode)
                                    if not force_cpu:
                                        if predictor_device and predictor_device.type == 'cuda':
                                            logger.info(f"   Moving predictor to CPU...")
                                            self.predictor = self.predictor.cpu()
                                        if encoder_device and encoder_device.type == 'cuda':
                                            logger.info(f"   Moving encoder to CPU...")
                                            self.embedding_space.encoder = self.embedding_space.encoder.cpu()
                                    
                                    # CRITICAL: Move ALL codecs to CPU - check parameters, buffers, and embedded modules
                                    if hasattr(self.embedding_space, 'col_codecs'):
                                        moved_count = 0
                                        for col_name, codec in self.embedding_space.col_codecs.items():
                                            codec_has_gpu = False
                                            
                                            # Check if codec has GPU parameters (StringCodec, JsonCodec have these!)
                                            if hasattr(codec, 'parameters') and list(codec.parameters()):
                                                if next(codec.parameters()).device.type == 'cuda':
                                                    codec_has_gpu = True
                                            
                                            # Check buffers
                                            if not codec_has_gpu and hasattr(codec, 'buffers') and isinstance(codec, torch.nn.Module):
                                                for buffer in codec.buffers():
                                                    if buffer.device.type == 'cuda':
                                                        codec_has_gpu = True
                                                        break
                                            
                                            # Check embedded modules (StringCodec: bert_projection, feature_embedding_mlp, merge_mlp)
                                            for attr_name in ['bert_projection', 'feature_embedding_mlp', 'merge_mlp', 'projection', 'encoder']:
                                                if hasattr(codec, attr_name):
                                                    embedded_module = getattr(codec, attr_name)
                                                    if embedded_module is not None and hasattr(embedded_module, 'parameters'):
                                                        if list(embedded_module.parameters()):
                                                            if next(embedded_module.parameters()).device.type == 'cuda':
                                                                codec_has_gpu = True
                                                                break
                                            
                                            # Move entire codec to CPU if it has any GPU components
                                            if codec_has_gpu:
                                                codec.cpu()  # This moves parameters, buffers, and all submodules
                                                moved_count += 1
                                                logger.info(f"   Moved codec '{col_name}' to CPU")
                                        
                                        if moved_count > 0:
                                            logger.info(f"   ✅ Moved {moved_count} codecs to CPU")
                                    
                                    # CRITICAL: Clear optimizer state from GPU - optimizer states can be HUGE (AdamW stores 2x params)
                                    # Optimizer state is on same device as parameters, but we need to explicitly clear it
                                    try:
                                        # Get optimizer from training loop if available
                                        if hasattr(self, '_current_optimizer') and self._current_optimizer is not None:
                                            optimizer = self._current_optimizer
                                            # Check if any optimizer state tensors are on GPU
                                            for param_group in optimizer.param_groups:
                                                for param in param_group['params']:
                                                    if param in optimizer.state:
                                                        state = optimizer.state[param]
                                                        for key, value in state.items():
                                                            if isinstance(value, torch.Tensor) and value.device.type == 'cuda':
                                                                logger.error(f"🚨 Optimizer state '{key}' for param is on GPU! Moving to CPU...")
                                                                state[key] = value.to('cpu')
                                    except Exception as e:
                                        logger.warning(f"Could not check optimizer state: {e}")
                                    
                                    # CRITICAL: No local sentence transformer to clear - using string server
                                    try:
                                        # Removed sentence_model import - no longer exists
                                        sentence_model = None
                                        if False:  # Disabled - no local model
                                            # Check device
                                            if hasattr(sentence_model, 'device'):
                                                if sentence_model.device.type == 'cuda':
                                                    logger.error(f"🚨 Sentence transformer is on GPU! Moving to CPU...")
                                                    sentence_model = sentence_model.to('cpu')
                                            # Check parameters
                                            elif hasattr(sentence_model, 'parameters'):
                                                if list(sentence_model.parameters()):
                                                    if next(sentence_model.parameters()).device.type == 'cuda':
                                                        logger.error(f"🚨 Sentence transformer parameters on GPU! Moving to CPU...")
                                                        sentence_model = sentence_model.to('cpu')
                                            # Check all submodules
                                            for module_name, module in sentence_model.named_modules():
                                                if hasattr(module, 'parameters') and list(module.parameters()):
                                                    if next(module.parameters()).device.type == 'cuda':
                                                        logger.error(f"🚨 Sentence transformer submodule {module_name} on GPU! Moving to CPU...")
                                                        sentence_model = sentence_model.to('cpu')
                                                        break
                                    except Exception as e:
                                        logger.warning(f"Could not check sentence transformer: {e}")
                                    
                                    # DUMP WHAT'S ACTUALLY USING GPU MEMORY
                                    if torch.cuda.is_available():
                                        allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
                                        reserved = torch.cuda.memory_reserved() / (1024**3)  # GB
                                        logger.error(f"📊 GPU MEMORY BEFORE PICKLE: Allocated={allocated:.2f} GB, Reserved={reserved:.2f} GB")
                                        if allocated > 0.1:  # More than 100MB
                                            logger.error(f"🚨 WARNING: {allocated:.2f} GB still allocated on GPU even though model params are on CPU!")
                                            logger.error(f"   This might be cached tensors, sentence transformer, or other GPU state")
                                            _dump_cuda_memory_usage(context="before pickle.dump")
                                    
                                    # CRITICAL: Force optimizer state to CPU if it exists
                                    # AdamW optimizer state can be 2x the size of parameters (momentum + variance)
                                    # Even if params are on CPU, optimizer state might be on GPU
                                    try:
                                        if hasattr(self, '_current_optimizer') and self._current_optimizer is not None:
                                            optimizer = self._current_optimizer
                                            optimizer_state_moved = 0
                                            for param_group in optimizer.param_groups:
                                                for param in param_group['params']:
                                                    if param in optimizer.state:
                                                        state = optimizer.state[param]
                                                        for key, value in state.items():
                                                            if isinstance(value, torch.Tensor) and value.device.type == 'cuda':
                                                                state[key] = value.to('cpu')
                                                                optimizer_state_moved += 1
                                            if optimizer_state_moved > 0:
                                                logger.error(f"🚨 Moved {optimizer_state_moved} optimizer state tensors from GPU to CPU")
                                    except Exception as e:
                                        logger.warning(f"Could not move optimizer state to CPU: {e}")
                                    
                                    # Clear CUDA cache aggressively
                                    if torch.cuda.is_available():
                                        torch.cuda.empty_cache()
                                        torch.cuda.synchronize()
                                        # Force garbage collection to free up any lingering references
                                        import gc
                                        gc.collect()
                                        torch.cuda.empty_cache()
                                        # Clear again after GC
                                        torch.cuda.empty_cache()
                                        # Try to release reserved memory by resetting peak stats
                                        torch.cuda.reset_peak_memory_stats()
                                    
                                    # WALK THE ENTIRE MODEL BEFORE PICKLE.DUMP - CHECK FOR ANY GPU STATE
                                    logger.error("="*80)
                                    logger.error("🔍 WALKING ENTIRE MODEL BEFORE PICKLE.DUMP - CHECKING FOR GPU STATE:")
                                    logger.error("="*80)
                                    
                                    all_gpu_items = []
                                    
                                    # Check predictor
                                    if hasattr(self, 'predictor') and self.predictor is not None:
                                        predictor_gpu = _walk_model_for_gpu(self.predictor, "predictor")
                                        all_gpu_items.extend(predictor_gpu)
                                    
                                    # Check encoder
                                    if hasattr(self.embedding_space, 'encoder') and self.embedding_space.encoder is not None:
                                        encoder_gpu = _walk_model_for_gpu(self.embedding_space.encoder, "embedding_space.encoder")
                                        all_gpu_items.extend(encoder_gpu)
                                    
                                    # Check target_codec
                                    if hasattr(self, 'target_codec') and self.target_codec is not None:
                                        target_codec_gpu = _walk_model_for_gpu(self.target_codec, "target_codec")
                                        all_gpu_items.extend(target_codec_gpu)
                                    
                                    # Check all col_codecs
                                    if hasattr(self.embedding_space, 'col_codecs'):
                                        for col_name, codec in self.embedding_space.col_codecs.items():
                                            codec_gpu = _walk_model_for_gpu(codec, f"embedding_space.col_codecs['{col_name}']")
                                            all_gpu_items.extend(codec_gpu)
                                    
                                    # Report findings
                                    if all_gpu_items:
                                        logger.error(f"🚨 FOUND {len(all_gpu_items)} GPU ITEMS:")
                                        total_elements = 0
                                        for item_name, item_type, shape, numel, device in all_gpu_items:
                                            total_elements += numel
                                            logger.error(f"   - {item_name}: {item_type}, shape={shape}, elements={numel:,}, device={device}")
                                        logger.error(f"   📊 TOTAL GPU ELEMENTS: {total_elements:,}")
                                        logger.error("="*80)
                                        raise RuntimeError(f"FOUND {len(all_gpu_items)} GPU ITEMS BEFORE PICKLE.DUMP! Cannot save checkpoint with GPU state.")
                                    else:
                                        logger.error("✅ NO GPU STATE FOUND - Safe to pickle.dump")
                                        logger.error("="*80)
                                    
                                    # CRITICAL: Clear ALL GPU memory before pickle.dump
                                    # pickle.dump might trigger GPU allocation if there are any references
                                    if torch.cuda.is_available():
                                        # Delete optimizer to free its state
                                        if hasattr(self, '_current_optimizer'):
                                            del self._current_optimizer
                                            self._current_optimizer = None
                                        
                                        # Clear sentence transformer from GPU
                                        try:
                                            from featrix.neural.string_codec import sentence_model
                                            if sentence_model is not None:
                                                # Force move to CPU
                                                sentence_model = sentence_model.to('cpu')
                                                # Clear any cached embeddings
                                                if hasattr(sentence_model, '_modules'):
                                                    for module in sentence_model.modules():
                                                        if hasattr(module, 'eval'):
                                                            module.eval()
                                        except Exception:
                                            pass
                                        
                                        # AGGRESSIVE GPU clearing - PyTorch's allocator can hold onto memory even after tensors are deleted
                                        # Do multiple passes to try to force release of reserved memory
                                        allocated_before = torch.cuda.memory_allocated() / (1024**3)
                                        reserved_before = torch.cuda.memory_reserved() / (1024**3)
                                        logger.error(f"📊 BEFORE CLEARING: Allocated={allocated_before:.3f} GB, Reserved={reserved_before:.3f} GB")
                                        
                                        # Pass 1: Standard clearing
                                        torch.cuda.empty_cache()
                                        torch.cuda.synchronize()
                                        import gc
                                        gc.collect()
                                        
                                        # Pass 2: Clear again after GC
                                        torch.cuda.empty_cache()
                                        torch.cuda.synchronize()
                                        gc.collect()
                                        
                                        # Pass 3: Try to force release by resetting stats and clearing again
                                        torch.cuda.reset_peak_memory_stats()
                                        torch.cuda.empty_cache()
                                        torch.cuda.synchronize()
                                        
                                        # Pass 4: Final aggressive clear
                                        gc.collect()
                                        torch.cuda.empty_cache()
                                        
                                        # Check results
                                        allocated_after = torch.cuda.memory_allocated() / (1024**3)
                                        reserved_after = torch.cuda.memory_reserved() / (1024**3)
                                        logger.error(f"📊 AFTER CLEARING: Allocated={allocated_after:.3f} GB, Reserved={reserved_after:.3f} GB")
                                        logger.error(f"   Change: Allocated {allocated_before - allocated_after:.3f} GB, Reserved {reserved_before - reserved_after:.3f} GB")
                                        
                                        if allocated_after > 0.1:
                                            logger.error(f"🚨 WARNING: {allocated_after:.2f} GB still ALLOCATED on GPU after clearing!")
                                        if reserved_after > 1.0:
                                            logger.error(f"🚨 WARNING: {reserved_after:.2f} GB still RESERVED on GPU (fragmentation)!")
                                            logger.error(f"   PyTorch's memory allocator is holding onto {reserved_after:.2f} GB even though only {allocated_after:.2f} GB is allocated")
                                            logger.error(f"   This fragmentation prevents pickle.dump from allocating even 2MB")
                                        
                                        if allocated_after > 1.0 or reserved_after > 1.0:
                                            logger.error(f"🚨 CRITICAL: Cannot clear GPU memory - will skip checkpoint save to avoid OOM")
                                            raise RuntimeError(f"Cannot save checkpoint: {allocated_after:.2f} GB allocated, {reserved_after:.2f} GB reserved on GPU")
                                    
                                    # Save full pickle (not just state dicts) - everything is now on CPU
                                    checkpoint_dir = self._output_dir if self._output_dir else "."
                                    id_suffix = f"_{sp_identifier}" if sp_identifier else ""
                                    epoch_checkpoint_path = os.path.join(checkpoint_dir, f"single_predictor{id_suffix}_epoch_{epoch_idx}.pickle")
                                    
                                    _log_gpu_memory(f"BEFORE PICKLE.DUMP (epoch {epoch_idx})", log_level=logging.ERROR)
                                    
                                    # Use map_location='cpu' context to prevent any GPU allocation during pickle
                                    _log_gpu_memory(f"BEFORE PICKLE.DUMP FILE OPEN (epoch {epoch_idx})", log_level=logging.ERROR)
                                    with open(epoch_checkpoint_path, "wb") as f:
                                        _log_gpu_memory(f"BEFORE PICKLE.DUMP CALL (epoch {epoch_idx})", log_level=logging.ERROR)
                                        # Temporarily disable CUDA to prevent any GPU allocation during pickle
                                        cuda_was_available = torch.cuda.is_available()
                                        if cuda_was_available:
                                            # Set environment to prevent CUDA allocation
                                            old_cuda_visible = os.environ.get('CUDA_VISIBLE_DEVICES')
                                            os.environ['CUDA_VISIBLE_DEVICES'] = ''
                                            # Force PyTorch to think CUDA is unavailable
                                            torch.cuda._initialized = False
                                        
                                        try:
                                            pickle.dump(self, f)
                                        finally:
                                            # Restore CUDA
                                            if cuda_was_available:
                                                if old_cuda_visible is not None:
                                                    os.environ['CUDA_VISIBLE_DEVICES'] = old_cuda_visible
                                                else:
                                                    del os.environ['CUDA_VISIBLE_DEVICES']
                                                torch.cuda._initialized = True
                                    _log_gpu_memory(f"AFTER PICKLE.DUMP FILE CLOSE (epoch {epoch_idx})", log_level=logging.ERROR)
                                    
                                    # Also save latest checkpoint
                                    latest_checkpoint_path = os.path.join(checkpoint_dir, f"single_predictor{id_suffix}_latest.pickle")
                                    with open(latest_checkpoint_path, "wb") as f:
                                        pickle.dump(self, f)
                                    
                                    # Save metadata
                                    current_metrics = None
                                    if hasattr(self, 'training_metrics') and self.training_metrics:
                                        current_metrics = self.training_metrics.copy()
                                    
                                    status_metadata = {
                                        "epoch": epoch_idx,
                                        "total_epochs": n_epochs,
                                        "progress_percent": (epoch_idx + 1) / n_epochs * 100 if n_epochs > 0 else 0,
                                        "training_loss": progress_dict.get("current_loss"),
                                        "validation_loss": progress_dict.get("validation_loss"),
                                        "metrics": current_metrics,
                                        "checkpoint_path": epoch_checkpoint_path,
                                        "latest_checkpoint_path": latest_checkpoint_path,
                                        "checkpoint_save_time_secs": time.time() - checkpoint_start_time,
                                        "is_training": True,
                                        "timestamp": time.time(),
                                        "data_passes": epoch_idx + 1,
                                        "saved_on_cpu": True  # Mark that this was saved on CPU
                                    }
                                    status_metadata_path = os.path.join(checkpoint_dir, f"single_predictor{id_suffix}_training_status.json")
                                    with open(status_metadata_path, "w") as f:
                                        json.dump(status_metadata, f, indent=2, default=str)
                                    
                                    logger.info(f"✅ Epoch checkpoint saved on CPU: {epoch_checkpoint_path} (took {time.time() - checkpoint_start_time:.3f}s total)")
                                    
                                    # Move models back to original device ONLY if not in CPU mode
                                    if not force_cpu:
                                        if predictor_device and predictor_device.type == 'cuda':
                                            logger.info(f"   Moving predictor back to {predictor_device}...")
                                            self.predictor = self.predictor.to(predictor_device)
                                        if encoder_device and encoder_device.type == 'cuda':
                                            logger.info(f"   Moving encoder back to {encoder_device}...")
                                            self.embedding_space.encoder = self.embedding_space.encoder.to(encoder_device)
                                    else:
                                        logger.info(f"   Models staying on CPU (CPU mode enabled)")
                                    
                                except Exception as cpu_save_error:
                                    logger.error(f"❌ Failed to save checkpoint on CPU: {cpu_save_error}")
                                    # Try to move models back to GPU even if save failed (only if not in CPU mode)
                                    force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
                                    if not force_cpu:
                                        try:
                                            if predictor_device and predictor_device.type == 'cuda':
                                                self.predictor = self.predictor.to(predictor_device)
                                            if encoder_device and encoder_device.type == 'cuda':
                                                self.embedding_space.encoder = self.embedding_space.encoder.to(encoder_device)
                                        except Exception:
                                            pass
                                    # Clear cache and continue training
                                    if torch.cuda.is_available():
                                        torch.cuda.empty_cache()
                                        torch.cuda.synchronize()
                                        logger.warning(f"   Skipping checkpoint save for this epoch")
                                else:
                                    # Other RuntimeError - log and continue
                                    logger.warning(f"⚠️  Failed to save epoch checkpoint (took {checkpoint_time:.3f}s): {checkpoint_error}")
                            except Exception as checkpoint_error:
                                checkpoint_time = time.time() - checkpoint_start_time
                                logger.warning(f"⚠️  Failed to save epoch checkpoint (took {checkpoint_time:.3f}s): {checkpoint_error}")
                                # Don't re-raise - continue training even if checkpoint save fails
                        else:
                            # Skip checkpoint - not time yet
                            logger.debug(f"⏭️  Skipping checkpoint: {elapsed_minutes:.1f} min elapsed (need 59+ min and 60+ since last)")
                        
                        # print("train loop: epoch = ", progress_dict.epoch_idx)
                    # ========================================================================
                    # END: EPOCH FOR LOOP (range(n_epochs))
                    # ========================================================================
                
                    # Normal completion - training finished without restart
                    restart_loop_active = False
                    logger.info("✅ Training completed successfully without restarts")
                
                except FeatrixRestartTrainingException as e:
                    # Caught restart exception - apply restart configuration
                    restart_config = e.restart_config
                    restart_attempts += 1
                    
                    logger.warning("=" * 80)
                    logger.warning(f"🔄 TRAINING RESTART #{restart_attempts} TRIGGERED")
                    logger.warning("=" * 80)
                    logger.warning(f"⚠️  Exception: {e}")
                    logger.warning(f"⚠️  Reason: {restart_config.reason}")
                    logger.warning(f"⚠️  Detected at epoch: {restart_config.epoch_detected}")
                    
                    # Get current learning rate
                    def get_current_lr_from_optimizer(opt):
                        if hasattr(opt, 'param_groups') and len(opt.param_groups) > 0:
                            return opt.param_groups[0]['lr']
                        return None
                    
                    current_lr = get_current_lr_from_optimizer(optimizer)
                    if current_lr is None:
                        logger.error("❌ Could not get current LR from optimizer - using default 0.01")
                        current_lr = 0.01
                    
                    # Calculate new learning rate
                    new_lr = current_lr * restart_config.lr_multiplier
                    if new_lr > restart_config.max_lr:
                        new_lr = restart_config.max_lr
                        logger.warning(f"   LR capped at maximum: {restart_config.max_lr:.6e}")
                    
                    logger.warning(f"   Old LR: {current_lr:.6e}")
                    logger.warning(f"   New LR: {new_lr:.6e} ({restart_config.lr_multiplier}x boost)")
                    
                    # Reset optimizer state if requested
                    if restart_config.reset_optimizer_state:
                        logger.warning(f"   Resetting optimizer state (clearing momentum/adaptive terms)...")
                        # CRITICAL: Can't just assign optimizer.state = {} - must use clear() or recreate
                        # PyTorch optimizer uses WeakKeyDictionary for state, need to properly clear it
                        optimizer.state.clear()
                        logger.warning(f"   ✅ Optimizer state cleared")
                    
                    # Update learning rate for all parameter groups
                    for group in optimizer.param_groups:
                        group['lr'] = new_lr
                    logger.warning(f"   ✅ Learning rate updated to {new_lr:.6e}")
                    
                    # Reset scheduler if requested
                    if restart_config.reset_scheduler and use_lr_scheduler:
                        logger.warning(f"   Recreating LR scheduler...")
                        remaining_epochs = n_epochs - epoch_idx
                        # For restarts, skip warmup (we're already mid-training) and go straight to cosine
                        scheduler = CosineAnnealingLR(
                            optimizer,
                            T_max=remaining_epochs,
                            eta_min=1e-6
                        )
                        logger.warning(f"   ✅ LR scheduler reset (cosine annealing for {remaining_epochs} remaining epochs)")
                    
                    # Load best checkpoint if requested
                    if restart_config.load_best_checkpoint and best_model_state is not None:
                        logger.warning(f"   Reloading best checkpoint from epoch {best_epoch}...")
                        self.predictor.load_state_dict(best_model_state)
                        self.embedding_space.encoder.load_state_dict(best_embedding_space_state)
                        
                        # CRITICAL: After loading checkpoint, model parameters are NEW objects
                        # We must recreate the optimizer to track the new parameters
                        logger.warning(f"   Recreating optimizer to track reloaded parameters...")
                        old_lr = optimizer.param_groups[0]['lr']
                        if self.embedding_space_training:
                            params = [
                                {'params': self.predictor.parameters()},
                                {'params': self.embedding_space.encoder.parameters(), 
                                 'lr': old_lr * self.embedding_space_training_lr_multiplier}
                            ]
                        else:
                            params = self.predictor.parameters()
                        
                        optimizer = torch.optim.AdamW(params, lr=old_lr, weight_decay=optimizer.param_groups[0].get('weight_decay', 0.0))
                        logger.warning(f"   ✅ Optimizer recreated with new parameters")
                        
                        logger.warning(f"   ✅ Best model weights restored (epoch {best_epoch})")
                    else:
                        logger.warning(f"   Continuing from current weights (no checkpoint reload)")
                    
                    # Log corrective action
                    corrective_action = {
                        "epoch": restart_config.epoch_detected,
                        "trigger": restart_config.reason,
                        "action_type": "TRAINING_RESTART",
                        "details": {
                            "old_lr": float(current_lr),
                            "new_lr": float(new_lr),
                            "lr_boost_multiplier": float(restart_config.lr_multiplier),
                            "restart_number": restart_attempts,
                            "optimizer_state_reset": restart_config.reset_optimizer_state,
                            "scheduler_reset": restart_config.reset_scheduler,
                            "checkpoint_reloaded": restart_config.load_best_checkpoint and best_model_state is not None,
                            **restart_config.metadata
                        }
                    }
                    self._corrective_actions.append(corrective_action)
                    
                    # Update tracking
                    self.training_restart_count = restart_attempts
                    self.last_restart_epoch = restart_config.epoch_detected
                    self.dead_gradient_epochs = []  # Clear dead gradient history
                    
                    logger.warning(f"   ✅ Corrective action logged")
                    logger.warning(f"   🔄 Training will restart from epoch {restart_config.epoch_detected}")
                    logger.warning("=" * 80)
                    
                    # Continue the while loop to restart training
                    continue
            # ============================================================================
            # END: RESTART WHILE LOOP
            # ============================================================================

            # 
            # Dump final training status.
            # 
            logger.info(f"@@@@@@@ >> encoding time took {encode_time} seconds")
            logger.info(
                f"@@@@@@@ >> encoding time vs a total of {time.time() - loop_start} seconds"
            )

            progress_dict["time_now"] = progress_dict["end_time"] = time.time()
            progress_dict["progress_counter"] = progress_dict["max_progress"]
            progress_dict["batch_idx"] = progress_dict["batch_total"]
            if print_callback is not None:
                print_callback(progress_dict)
            # self.training_info['progress_info'] = d

        # Restore best model if we found one
        if best_model_state is not None:
            if use_auc_for_best_epoch and best_auc >= 0:
                logger.info(f"🔄 RESTORING BEST MODEL from epoch {best_epoch} (AUC={best_auc:.4f})")
            else:
                logger.info(f"🔄 RESTORING BEST MODEL from epoch {best_epoch} (val_loss={best_val_loss:.4f})")
            logger.info(f"   Checkpoint path: {best_checkpoint_path if best_checkpoint_path else '(state dict only)'}")
            self.predictor.load_state_dict(best_model_state)
            self.embedding_space.encoder.load_state_dict(best_embedding_space_state)
            logger.info(f"✅ Best model restored successfully from epoch {best_epoch}")
        else:
            logger.warning(f"⚠️  No best model found - using final epoch weights")

        logger.info("Setting predictor.eval()")
        self.predictor.eval()
        
        # Fit calibration automatically after training completes
        # Only for classification tasks (SetCodec), not regression (ScalarCodec)
        if isinstance(self.target_codec, SetCodec) and val_queries is not None and val_targets is not None:
            logger.info("🔍 Auto-fitting calibration on validation set...")
            try:
                from featrix.neural.calibration_utils import auto_fit_calibration
                # torch is already imported at module level
                
                # Collect validation logits
                self.predictor.eval()
                self.embedding_space.encoder.eval()
                val_logits_list = []
                val_labels_list = []
                
                # Process validation data in batches
                # val_queries should be a DataFrame with the target column removed
                # Create a DataFrame from val_queries if it's not already one
                if not isinstance(val_queries, pd.DataFrame):
                    val_queries = pd.DataFrame(val_queries)
                
                val_dataset = SuperSimpleSelfSupervisedDataset(
                    val_queries,
                    self.all_codecs
                )
                val_dataloader = DataLoader(
                    val_dataset,
                    batch_size=min(256, len(val_dataset)),
                    shuffle=False,
                    collate_fn=collate_tokens,
                    **create_dataloader_kwargs(num_workers=0, dataset_size=len(val_dataset))  # Force single-process for single predictor
                )
                
                with torch.no_grad():
                    batch_idx = 0
                    for batch in val_dataloader:
                        queries_batch = batch
                        
                        # Encode queries
                        encoding = self.embedding_space.encode_batch(
                            queries_batch,
                            squeeze=False,
                            short=False,
                            output_device=device
                        )
                        
                        # Get logits
                        logits = self.predictor(encoding)
                        val_logits_list.append(logits.cpu())
                        
                        # Get labels from val_targets (not from batch)
                        # Calculate which indices in val_targets correspond to this batch
                        batch_start = batch_idx * val_dataloader.batch_size
                        batch_end = min(batch_start + len(queries_batch), len(val_targets))
                        batch_targets = val_targets.iloc[batch_start:batch_end] if hasattr(val_targets, 'iloc') else val_targets[batch_start:batch_end]
                        
                        # Convert targets to class indices
                        labels = []
                        for target_val in batch_targets:
                            if isinstance(target_val, Token):
                                label_idx = target_val.value
                                labels.append(label_idx)
                            else:
                                # Convert target value to token, then to index
                                target_token = self.target_codec.tokenize(target_val)
                                if isinstance(target_token, Token):
                                    label_idx = target_token.value
                                    labels.append(label_idx)
                                else:
                                    # Fallback: try to get index directly
                                    logger.warning(f"Could not convert target value {target_val} to token index")
                                    labels.append(0)  # Default to first class
                        val_labels_list.extend(labels)
                
                if val_logits_list:
                    # Concatenate all logits
                    val_logits = torch.cat(val_logits_list, dim=0)
                    val_labels = torch.tensor(val_labels_list, dtype=torch.long)
                    
                    # Fit calibration
                    best_method, temp, platt_model, isotonic_model, cal_metrics = auto_fit_calibration(
                        val_logits, val_labels, validation_split=0.0  # Use all validation data
                    )
                    
                    # Store calibration info
                    self.calibration_method = best_method
                    self.calibration_temperature = temp
                    self.calibration_platt_model = platt_model
                    self.calibration_isotonic_model = isotonic_model
                    self.calibration_metrics = cal_metrics
                    
                    logger.info(f"✅ Calibration fitted: method={best_method}")
                    if best_method == 'temperature':
                        logger.info(f"   Temperature: {temp:.4f}")
                else:
                    logger.warning("⚠️  No validation logits collected for calibration")
            except Exception as e:
                logger.warning(f"⚠️  Failed to fit calibration: {e}")
                import traceback
                logger.debug(traceback.format_exc())
        
        # Generate GraphViz visualization of network architecture
        logger.info("🔷 Generating GraphViz network architecture visualization...")
        try:
            from lib.featrix.neural.network_viz import generate_graphviz_for_single_predictor
            
            # Use custom identifier if provided, otherwise default
            output_path = None
            if network_viz_identifier:
                output_path = f"network_architecture_sp_{network_viz_identifier}"
            
            graphviz_path = generate_graphviz_for_single_predictor(self, output_path=output_path)
            if graphviz_path:
                logger.info(f"✅ Network architecture visualization saved to {graphviz_path}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to generate GraphViz visualization: {e}")
        
        # Clean up GPU memory after training
        logger.info("Cleaning up GPU memory after training")
        self.cleanup_gpu_memory()
        
        return self.training_info

    def compute_val_loss(
        self, val_batch, val_target_token_batch, validation_targets, loss_fn
    ):
        with PredictorEvalModeContextManager(fsp=self, debugLabel="compute_val_loss"):
            assert self.predictor.training == False, "where's my eval man [p]"
            assert self.embedding_space.encoder.training == False, "where's my eval man [es]"

            # Move val_batch to same device as encoder
            encoder_device = next(self.embedding_space.encoder.parameters()).device
            for tokenbatch in val_batch.values():
                tokenbatch.to(encoder_device)

            # CRITICAL: Move validation_targets to CPU if we're in CPU mode
            force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
            if force_cpu:
                validation_targets = validation_targets.to(torch.device('cpu'))

            # This mimicks the training loop, but with the validation data.
            target_column_in_original_df = (
                self.target_col_name in self.embedding_space.col_codecs
            )
            if target_column_in_original_df:
                marginal_token_batch = self._create_marginal_token_batch_for_target(
                    val_target_token_batch
                )
                val_batch[self.target_col_name] = marginal_token_batch

            # NOTE: (24/03/01, pjz) If we're not fine-tuning the encoder, we can
            # pre-encode the validation data and then just run the predictor on it.
            # But if we are fine-tuning the encoder, we need to encode the validation
            # data at each step, because the encoder's weights are changing.

            # Don't apply noise to validation branch - no need for feature dropout
            # at vaildate time.
            _, input_batch_full = self.embedding_space.encoder.encode(
                val_batch, apply_noise=False
            )
            
            # CRITICAL: Move batch to same device as predictor  
            # Encoder might be on CPU (force_cpu=True) but predictor is on GPU
            predictor_device = next(self.predictor.parameters()).device
            if input_batch_full.device != predictor_device:
                input_batch_full = input_batch_full.to(predictor_device)
            
            input_batch = input_batch_full
            prediction = self.predictor(input_batch)

            # CRITICAL: Ensure validation_targets are on the same device as prediction
            # Prediction's device depends on where encoder put things (can be CPU if string codecs moved tokens)
            # Also ensure prediction is on the same device as validation_targets if validation_targets is on GPU
            # This handles the case where prediction ends up on CPU but targets are on GPU
            if prediction.device != validation_targets.device:
                # Prefer moving targets to prediction device (prediction device is authoritative)
                # But log a warning if prediction is on CPU when targets are on GPU (might indicate a bug)
                if prediction.device.type == 'cpu' and validation_targets.device.type == 'cuda':
                    logger.warning(f"⚠️  Prediction is on CPU but validation_targets is on GPU - moving targets to CPU")
                validation_targets = validation_targets.to(prediction.device)
                # Don't log device moves - too noisy

            val_loss = loss_fn(prediction, validation_targets).item()
            
            # Check for NaN/Inf in validation loss
            if torch.isnan(torch.tensor(val_loss)) or torch.isinf(torch.tensor(val_loss)):
                logger.warning(f"⚠️  NaN/Inf validation loss detected: {val_loss}")
                logger.warning(f"   Prediction stats: min={prediction.min().item():.4f}, max={prediction.max().item():.4f}")
                # Return a large but finite value to avoid breaking progress tracking
                return 1e6
            
            return val_loss

    def has_error_for_metric(self, metric_name):
        return self.metrics_had_error.get(metric_name) is not None

    def handle_metrics_error(self, metric_name, ex):
        existing = self.metrics_had_error.get(metric_name)
        if existing is None:
            # first time!
            edict = {
                "message": "Failed to compute %s: %s" % (metric_name, ex),
                "count": 1,
            }

            logger.warning(
                "Failed to compute %s. Error: %s ... further instances are not logged but counts will be stored in the database."
                % (metric_name, ex)
            )
        else:
            edict = existing
            edict["count"] = edict.get("count", 0) + 1
        self.metrics_had_error[metric_name] = edict
        return

    def clear_binary_metrics_errors(self):
        self.metrics_had_error = {}
        return

    def _find_best_threshold(self, y_ground, y_scores, pos_label):
        """
        Finds the threshold that maximizes the accuracy for binary classification.

        Args:
        y_true (array-like): True binary labels.
        y_scores (array-like): Scores or probabilities associated with the positive class.

        Returns:
        float: The threshold that gives the best accuracy.
        float: The best accuracy achieved with the best threshold.
        """

        y_true = [y_ground[i] == pos_label for i in range(len(y_ground))]

        # Compute FPR, TPR, and thresholds
        fpr, tpr, thresholds = roc_curve(y_true, y_scores)

        # Calculate accuracy for each threshold
        accuracies = [(y_true == (y_scores >= t)).mean() for t in thresholds]

        # Find the threshold that gives the highest accuracy
        max_index = np.argmax(accuracies)
        best_threshold = thresholds[max_index]
        best_accuracy = accuracies[max_index]

        # If y_true contains all 0s, i.e. the predictions y_true are never positive,
        # then the ROC curve will have a single point at (0, 0) and the threshold will be np.inf.
        # We fix this by setting the threshold to 1.0 and the accuracy to 0.0.
        # threshold=1 means everything is negative, so a simple deterministic classifier
        # does a perfect job.
        if best_threshold == np.inf:
            best_threshold = 1.0
            best_accuracy = 1.0

        return best_threshold, best_accuracy

    def strip_queries(self, queries, ground_truth):
        assert len(queries) == len(ground_truth)

        new_q = []
        new_gt = []
        for idx in range(len(queries)):
            gt = ground_truth[idx]
            if gt != gt: #is_nan(gt):
                continue
            new_q.append(queries[idx])
            new_gt.append(ground_truth[idx])
        return new_q, new_gt



    def best_threshold_for_cost(self, y_true, y_prob, cost_fp, cost_fn, 
                                 min_pred_pos_frac=None, max_pred_pos_frac=None, n_thresholds=201):
        """
        Find the optimal threshold that minimizes cost: cost_fp * FP + cost_fn * FN.
        
        Args:
            y_true: Binary ground truth labels (0 or 1)
            y_prob: Predicted probabilities for positive class
            cost_fp: Cost of false positive
            cost_fn: Cost of false negative
            min_pred_pos_frac: Optional minimum predicted positive rate (0.0-1.0)
            max_pred_pos_frac: Optional maximum predicted positive rate (0.0-1.0)
            n_thresholds: Number of thresholds to evaluate (default: 201)
        
        Returns:
            tuple: (optimal_threshold, min_cost, (tp, fp, tn, fn), f1_at_cost_optimal)
        """
        import numpy as np
        from sklearn.metrics import f1_score
        
        y_true = np.array(y_true)
        y_prob = np.array(y_prob)
        thresholds = np.linspace(0.0, 1.0, num=n_thresholds)
        N = len(y_true)
        
        best_tau = 0.5
        best_cost = float('inf')
        best_stats = None
        
        for tau in thresholds:
            y_pred = (y_prob >= tau).astype(int)
            
            tp = np.sum((y_true == 1) & (y_pred == 1))
            fn = np.sum((y_true == 1) & (y_pred == 0))
            fp = np.sum((y_true == 0) & (y_pred == 1))
            tn = np.sum((y_true == 0) & (y_pred == 0))
            
            pred_pos_rate = (tp + fp) / N if N > 0 else 0.0
            
            # Apply constraints if provided
            if min_pred_pos_frac is not None and pred_pos_rate < min_pred_pos_frac:
                continue
            if max_pred_pos_frac is not None and pred_pos_rate > max_pred_pos_frac:
                continue
            
            cost = cost_fp * fp + cost_fn * fn
            
            if cost < best_cost:
                best_cost = cost
                best_tau = tau
                best_stats = (tp, fp, tn, fn)
        
        # Fallback: if constraints killed all thresholds, ignore constraints
        if best_stats is None:
            for tau in thresholds:
                y_pred = (y_prob >= tau).astype(int)
                tp = np.sum((y_true == 1) & (y_pred == 1))
                fn = np.sum((y_true == 1) & (y_pred == 0))
                fp = np.sum((y_true == 0) & (y_pred == 1))
                tn = np.sum((y_true == 0) & (y_pred == 0))
                cost = cost_fp * fp + cost_fn * fn
                if cost < best_cost:
                    best_cost = cost
                    best_tau = tau
                    best_stats = (tp, fp, tn, fn)
        
        tp, fp, tn, fn = best_stats
        y_pred_best = (y_prob >= best_tau).astype(int)
        f1_best = f1_score(y_true, y_pred_best, zero_division=0)
        
        return float(best_tau), float(best_cost), (int(tp), int(fp), int(tn), int(fn)), float(f1_best)
    
    def best_threshold_for_f1(self, y_true, y_prob, predicted_positive_rate_bounds=None):
        """
        Find the optimal threshold for F1 score using precision-recall curve (optimized).
        
        Args:
            y_true: Binary ground truth labels (0 or 1)
            y_prob: Predicted probabilities for positive class
            predicted_positive_rate_bounds: Optional tuple (min_rate, max_rate) to constrain
                the predicted positive rate. If None, no constraints are applied.
                Example: (0.2, 0.5) means predicted positive rate must be between 20% and 50%.
        
        Returns:
            tuple: (optimal_threshold, optimal_f1_score)
        """
        try:
            # Ensure y_prob is a numpy array for proper comparison
            y_prob = np.array(y_prob)
            y_true = np.array(y_true)
            
            # OPTIMIZATION: Use precision_recall_curve which is already efficient
            p, r, t = precision_recall_curve(y_true, y_prob)
            # PR returns thresholds of len-1 vs p/r; align safely:
            thresholds = t if len(t) > 0 else [0.5]
            
            # OPTIMIZATION: Vectorized F1 calculation using precision and recall from curve
            # F1 = 2 * (precision * recall) / (precision + recall)
            # This avoids calling f1_score in a loop
            f1s = 2 * (p * r) / (p + r + 1e-10)  # Add small epsilon to avoid division by zero
            
            # Also check threshold 1.0 (all negative predictions)
            threshold_1_0_f1 = f1_score(y_true, (y_prob >= 1.0).astype(int), zero_division=0)
            
            # Combine with edge case
            all_f1s = np.concatenate([f1s, [threshold_1_0_f1]])
            all_thresholds = np.concatenate([thresholds, [1.0]])
            
            # Apply constraints on predicted positive rate if provided
            if predicted_positive_rate_bounds is not None:
                min_rate, max_rate = predicted_positive_rate_bounds
                valid_indices = []
                
                for idx, threshold in enumerate(all_thresholds):
                    # Compute predicted positive rate at this threshold
                    pred_pos_rate = (y_prob >= threshold).mean()
                    if min_rate <= pred_pos_rate <= max_rate:
                        valid_indices.append(idx)
                
                if valid_indices:
                    # Only consider thresholds that meet the constraint
                    constrained_f1s = all_f1s[valid_indices]
                    constrained_thresholds = all_thresholds[valid_indices]
                    best_idx = int(np.argmax(constrained_f1s))
                    best_threshold = float(constrained_thresholds[best_idx])
                    best_f1 = float(constrained_f1s[best_idx])
                    
                    # Log constraint info
                    pred_pos_rate = (y_prob >= best_threshold).mean()
                    logger.debug(f"📊 Threshold constraint applied: predicted positive rate {pred_pos_rate:.1%} (bounds: [{min_rate:.1%}, {max_rate:.1%}])")
                    
                    return best_threshold, best_f1
                else:
                    # No threshold meets constraints - fall back to multi-objective optimization
                    logger.warning(f"⚠️  No threshold meets predicted positive rate bounds [{min_rate:.1%}, {max_rate:.1%}]. Using multi-objective optimization.")
                    
                    # Multi-objective: maximize F1 subject to specificity >= 0.6 or accuracy >= argmax_accuracy - 0.05
                    argmax_preds = (y_prob >= 0.5).astype(int)
                    argmax_accuracy = (y_true == argmax_preds).mean()
                    min_accuracy = argmax_accuracy - 0.05
                    
                    best_f1_constrained = -1.0
                    best_threshold_constrained = 0.5
                    
                    for idx, threshold in enumerate(all_thresholds):
                        preds = (y_prob >= threshold).astype(int)
                        f1 = all_f1s[idx]
                        
                        # Compute specificity and accuracy
                        tn = ((y_true == 0) & (preds == 0)).sum()
                        fp = ((y_true == 0) & (preds == 1)).sum()
                        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
                        accuracy = (y_true == preds).mean()
                        
                        # Check constraints: specificity >= 0.6 OR accuracy >= min_accuracy
                        if (specificity >= 0.6 or accuracy >= min_accuracy) and f1 > best_f1_constrained:
                            best_f1_constrained = f1
                            best_threshold_constrained = threshold
                    
                    if best_f1_constrained > 0:
                        logger.info(f"   Multi-objective solution: threshold={best_threshold_constrained:.4f}, F1={best_f1_constrained:.3f}")
                        return float(best_threshold_constrained), float(best_f1_constrained)
                    else:
                        # Last resort: use unconstrained best
                        logger.warning(f"   Multi-objective optimization failed, using unconstrained best threshold")
            
            # No constraints or constraints failed - use unconstrained best
            best_idx = int(np.argmax(all_f1s))
            return float(all_thresholds[best_idx]), float(all_f1s[best_idx])
        except Exception as e:
            logger.warning(f"Error computing best threshold: {e}")
            return 0.5, 0.0
    
    def _compute_baseline_cost(self, y_true, cost_fp, cost_fn):
        """
        Compute baseline cost: always predict negative (no one is bad).
        Cost = FN for all positives, no FP.
        
        Args:
            y_true: Binary ground truth labels (0 or 1)
            cost_fp: Cost of false positive
            cost_fn: Cost of false negative
        
        Returns:
            float: Baseline cost
        """
        import numpy as np
        y_true = np.array(y_true)
        n_pos = np.sum(y_true == 1)
        cost_all_negative = cost_fn * n_pos  # all positives missed
        return float(cost_all_negative)
    
    def _choose_metric_weights(self, pos_rate):
        """
        Decide α, β, γ weights for composite score based on class prevalence.
        
        Args:
            pos_rate: Positive class rate (0.0-1.0)
        
        Returns:
            tuple: (alpha, beta, gamma) weights for (PR-AUC, cost_savings, ROC-AUC)
        """
        if pos_rate < 0.05:
            # Very rare – lean hard on PR-AUC + cost
            return 0.6, 0.3, 0.1
        elif pos_rate < 0.2:
            # Moderate imbalance
            return 0.5, 0.3, 0.2
        else:
            # Roughly balanced (like credit-g at 30%)
            return 0.4, 0.3, 0.3
    
    def _compute_composite_score(self, metrics, baseline_cost):
        """
        Compute composite score: α * PR-AUC + β * CostSavings + γ * ROC-AUC
        
        Args:
            metrics: dict with keys: roc_auc, pr_auc, cost_min, pos_rate
            baseline_cost: scalar baseline cost for normalization
        
        Returns:
            tuple: (composite_score, score_components_dict)
        """
        import numpy as np
        
        roc_auc = metrics.get("roc_auc", 0.5)
        pr_auc = metrics.get("pr_auc", 0.0)
        cost_min = metrics.get("cost_min", float('inf'))
        pos_rate = metrics.get("pos_rate", 0.5)
        
        # Handle NaNs gracefully
        if np.isnan(roc_auc):
            roc_auc = 0.5
        if np.isnan(pr_auc):
            pr_auc = 0.0
        
        # Normalize cost -> savings in [0, 1]
        # CostSavings = 0 means no better than 'always negative'; 1 means zero cost.
        if baseline_cost > 0:
            cost_savings = (baseline_cost - cost_min) / baseline_cost
        else:
            cost_savings = 0.0
        cost_savings = float(np.clip(cost_savings, 0.0, 1.0))
        
        alpha, beta, gamma = self._choose_metric_weights(pos_rate)
        
        score = (alpha * pr_auc) + (beta * cost_savings) + (gamma * roc_auc)
        
        return float(score), {
            "roc_auc": float(roc_auc),
            "pr_auc": float(pr_auc),
            "cost_savings": cost_savings,
            "alpha": alpha,
            "beta": beta,
            "gamma": gamma,
        }
    
    def best_threshold_for_cost(self, y_true, y_prob, cost_fp, cost_fn, 
                                 min_pred_pos_frac=None, max_pred_pos_frac=None, n_thresholds=201):
        """
        Find the optimal threshold that minimizes cost: cost_fp * FP + cost_fn * FN.
        
        Args:
            y_true: Binary ground truth labels (0 or 1)
            y_prob: Predicted probabilities for positive class
            cost_fp: Cost of false positive
            cost_fn: Cost of false negative
            min_pred_pos_frac: Optional minimum predicted positive rate (0.0-1.0)
            max_pred_pos_frac: Optional maximum predicted positive rate (0.0-1.0)
            n_thresholds: Number of thresholds to evaluate (default: 201)
        
        Returns:
            tuple: (optimal_threshold, min_cost, (tp, fp, tn, fn), f1_at_cost_optimal)
        """
        import numpy as np
        from sklearn.metrics import f1_score
        
        y_true = np.array(y_true)
        y_prob = np.array(y_prob)
        thresholds = np.linspace(0.0, 1.0, num=n_thresholds)
        N = len(y_true)
        
        best_tau = 0.5
        best_cost = float('inf')
        best_stats = None
        
        for tau in thresholds:
            y_pred = (y_prob >= tau).astype(int)
            
            tp = np.sum((y_true == 1) & (y_pred == 1))
            fn = np.sum((y_true == 1) & (y_pred == 0))
            fp = np.sum((y_true == 0) & (y_pred == 1))
            tn = np.sum((y_true == 0) & (y_pred == 0))
            
            pred_pos_rate = (tp + fp) / N if N > 0 else 0.0
            
            # Apply constraints if provided
            if min_pred_pos_frac is not None and pred_pos_rate < min_pred_pos_frac:
                continue
            if max_pred_pos_frac is not None and pred_pos_rate > max_pred_pos_frac:
                continue
            
            cost = cost_fp * fp + cost_fn * fn
            
            if cost < best_cost:
                best_cost = cost
                best_tau = tau
                best_stats = (tp, fp, tn, fn)
        
        # Fallback: if constraints killed all thresholds, ignore constraints
        if best_stats is None:
            for tau in thresholds:
                y_pred = (y_prob >= tau).astype(int)
                tp = np.sum((y_true == 1) & (y_pred == 1))
                fn = np.sum((y_true == 1) & (y_pred == 0))
                fp = np.sum((y_true == 0) & (y_pred == 1))
                tn = np.sum((y_true == 0) & (y_pred == 0))
                cost = cost_fp * fp + cost_fn * fn
                if cost < best_cost:
                    best_cost = cost
                    best_tau = tau
                    best_stats = (tp, fp, tn, fn)
        
        tp, fp, tn, fn = best_stats
        y_pred_best = (y_prob >= best_tau).astype(int)
        f1_best = f1_score(y_true, y_pred_best, zero_division=0)
        
        return float(best_tau), float(best_cost), (int(tp), int(fp), int(tn), int(fn)), float(f1_best)
        """
        Compute baseline cost: always predict negative (no one is bad).
        Cost = FN for all positives, no FP.
        
        Args:
            y_true: Binary ground truth labels (0 or 1)
            cost_fp: Cost of false positive
            cost_fn: Cost of false negative
        
        Returns:
            float: Baseline cost
        """
        import numpy as np
        y_true = np.array(y_true)
        n_pos = np.sum(y_true == 1)
        cost_all_negative = cost_fn * n_pos  # all positives missed
        return float(cost_all_negative)
    
    def _choose_metric_weights(self, pos_rate):
        """
        Decide α, β, γ weights for composite score based on class prevalence.
        
        Args:
            pos_rate: Positive class rate (0.0-1.0)
        
        Returns:
            tuple: (alpha, beta, gamma) weights for (PR-AUC, cost_savings, ROC-AUC)
        """
        if pos_rate < 0.05:
            # Very rare – lean hard on PR-AUC + cost
            return 0.6, 0.3, 0.1
        elif pos_rate < 0.2:
            # Moderate imbalance
            return 0.5, 0.3, 0.2
        else:
            # Roughly balanced (like credit-g at 30%)
            return 0.4, 0.3, 0.3
    
    def _compute_composite_score(self, metrics, baseline_cost):
        """
        Compute composite score: α * PR-AUC + β * CostSavings + γ * ROC-AUC
        
        Args:
            metrics: dict with keys: roc_auc, pr_auc, cost_min, pos_rate
            baseline_cost: scalar baseline cost for normalization
        
        Returns:
            tuple: (composite_score, score_components_dict)
        """
        import numpy as np
        
        roc_auc = metrics.get("roc_auc", 0.5)
        pr_auc = metrics.get("pr_auc", 0.0)
        cost_min = metrics.get("cost_min", float('inf'))
        pos_rate = metrics.get("pos_rate", 0.5)
        
        # Handle NaNs gracefully
        if np.isnan(roc_auc):
            roc_auc = 0.5
        if np.isnan(pr_auc):
            pr_auc = 0.0
        
        # Normalize cost -> savings in [0, 1]
        # CostSavings = 0 means no better than 'always negative'; 1 means zero cost.
        if baseline_cost > 0:
            cost_savings = (baseline_cost - cost_min) / baseline_cost
        else:
            cost_savings = 0.0
        cost_savings = float(np.clip(cost_savings, 0.0, 1.0))
        
        alpha, beta, gamma = self._choose_metric_weights(pos_rate)
        
        score = (alpha * pr_auc) + (beta * cost_savings) + (gamma * roc_auc)
        
        return float(score), {
            "roc_auc": float(roc_auc),
            "pr_auc": float(pr_auc),
            "cost_savings": cost_savings,
            "alpha": alpha,
            "beta": beta,
            "gamma": gamma,
        }



    def normalize_types(self, ground_truth, preds, pos_label):
        """Normalize all inputs to the same type for sklearn compatibility"""
        logger.debug(f"🔍 NORMALIZING TYPES:")
        logger.debug(f"   Original pos_label: {pos_label} (type: {type(pos_label)})")
        logger.debug(f"   Original ground_truth sample: {ground_truth[:5]} (types: {[type(gt) for gt in ground_truth[:5]]})")
        logger.debug(f"   Original predictions sample: {preds[:5]} (types: {[type(p) for p in preds[:5]]})")
        
        # Determine the target type based on ground_truth
        if ground_truth:
            gt_sample = ground_truth[0]
            
            # Convert pos_label to match ground_truth type (use numpy types for consistency)
            try:
                if isinstance(gt_sample, (bool, np.bool_)):
                    # Boolean type: convert string to bool
                    if isinstance(pos_label, str):
                        pos_label_normalized = pos_label.lower() in ('true', '1', 'yes', 't', 'y')
                    else:
                        pos_label_normalized = bool(pos_label)
                elif isinstance(gt_sample, (int, float, np.integer, np.floating)):
                    pos_label_normalized = np.float64(pos_label)
                elif isinstance(gt_sample, str):
                    pos_label_normalized = str(pos_label)
                else:
                    pos_label_normalized = pos_label
            except (ValueError, TypeError):
                pos_label_normalized = str(pos_label)
            
            # Convert predictions to match ground_truth type (use numpy types for consistency)
            preds_normalized = []
            for pred in preds:
                try:
                    if isinstance(gt_sample, (bool, np.bool_)):
                        # Boolean type: convert string to bool
                        if isinstance(pred, str):
                            preds_normalized.append(pred.lower() in ('true', '1', 'yes', 't', 'y'))
                        else:
                            preds_normalized.append(bool(pred))
                    elif isinstance(gt_sample, (int, float, np.integer, np.floating)):
                        preds_normalized.append(np.float64(pred))
                    elif isinstance(gt_sample, str):
                        preds_normalized.append(str(pred))
                    else:
                        preds_normalized.append(pred)
                except (ValueError, TypeError):
                    preds_normalized.append(str(pred))
            
            logger.debug(f"   Normalized pos_label: {pos_label_normalized} (type: {type(pos_label_normalized)})")
            logger.debug(f"   Normalized predictions sample: {preds_normalized[:5]} (types: {[type(p) for p in preds_normalized[:5]]})")
            logger.debug(f"   Unique normalized ground_truth: {set(ground_truth)}")
            logger.debug(f"   Unique normalized predictions: {set(preds_normalized)}")
            
            return ground_truth, preds_normalized, pos_label_normalized
        else:
            return ground_truth, preds, pos_label

    def validate_metrics_inputs(self, ground_truth, preds, pos_label):
        """Validate inputs before calling sklearn metrics to catch issues early"""
        logger.info(f":mag: VALIDATING METRICS INPUTS:")
        logger.info(f"   pos_label: {pos_label} (type: {type(pos_label)})")
        logger.info(f"   ground_truth sample: {ground_truth[:5]} (types: {[type(gt) for gt in ground_truth[:5]]})")
        logger.info(f"   predictions sample: {preds[:5]} (types: {[type(p) for p in preds[:5]]})")
        logger.info(f"   unique ground_truth values: {set(ground_truth)}")
        logger.info(f"   unique prediction values: {set(preds)}")
        logger.info(f"   pos_label in ground_truth: {pos_label in ground_truth}")
        logger.info(f"   pos_label in predictions: {pos_label in preds}")

        # Check for type mismatches
        if ground_truth and preds:
            gt_sample = ground_truth[0]
            pred_sample = preds[0]

            if type(pos_label) != type(gt_sample):
                logger.warning(f":warning:  TYPE MISMATCH: pos_label is {type(pos_label)} but ground_truth contains {type(gt_sample)}")
                logger.warning(f"   pos_label: {pos_label}")
                logger.warning(f"   ground_truth sample: {gt_sample}")

            if type(gt_sample) != type(pred_sample):
                logger.warning(f":warning:  TYPE MISMATCH: ground_truth is {type(gt_sample)} but predictions contain {type(pred_sample)}")

        # Check if pos_label exists in data
        if pos_label not in ground_truth:
            logger.warning(f":warning:  pos_label '{pos_label}' {type(pos_label)} not found in ground_truth values: {set(ground_truth)}")

        if pos_label not in preds:
            logger.warning(f":warning:  pos_label '{pos_label}' not found in predictions: {set(preds)}")
            logger.warning(f"   This will cause 'Precision is ill-defined' warnings")

        return True

    def detect_training_failure_mode(self, raw_logits_array, pos_probs_array, pred_counts, 
                                      y_true_binary, auc, accuracy, optimal_threshold, epoch_idx, n_epochs=None, log_prefix=""):
        """
        Detect and diagnose training failure modes.
        Returns: (failure_detected: bool, failure_label: str, recommendations: list)
        
        Args:
            epoch_idx: current epoch number
            n_epochs: total number of epochs (used to skip diagnostics if too early)
            log_prefix: prefix to include in all log messages (e.g., "epoch=N, target=col: ")
        """
        
        # Skip diagnostics until we're at least 5% through training or past epoch 5
        min_epoch_threshold = max(5, int(n_epochs * 0.05)) if n_epochs else 5
        if epoch_idx < min_epoch_threshold:
            logger.debug(f"Skipping failure diagnostics at epoch {epoch_idx} - waiting until epoch {min_epoch_threshold} ({min_epoch_threshold/n_epochs*100:.1f}% complete)")
            return False, "TOO_EARLY", []
        
        failures = []
        recommendations = []
        
        # Calculate key statistics
        prob_std = pos_probs_array.std()
        prob_range = pos_probs_array.max() - pos_probs_array.min()
        prob_mean = pos_probs_array.mean()
        
        # Count predictions near decision boundary (0.4-0.6)
        near_boundary = np.sum((pos_probs_array >= 0.4) & (pos_probs_array <= 0.6))
        pct_near_boundary = near_boundary / len(pos_probs_array) * 100
        
        # Get class imbalance in predictions
        total_preds = sum(pred_counts.values())
        max_pred_pct = max(pred_counts.values()) / total_preds * 100 if total_preds > 0 else 0
        
        # Get class imbalance in ground truth
        pos_count = sum(y_true_binary)
        true_pos_pct = pos_count / len(y_true_binary) * 100
        
        # Raw logits analysis
        logits_std = raw_logits_array.std() if raw_logits_array is not None else None
        logits_range = (raw_logits_array.max() - raw_logits_array.min()) if raw_logits_array is not None else None
        
        # FAILURE MODE 1: Dead Network (Raw logits have no variation)
        if logits_std is not None and logits_std < 0.01:
            failures.append("DEAD_NETWORK")
            recommendations.extend([
                "🔥 CRITICAL: Network outputs are frozen (std < 0.01)",
                "   → STOP TRAINING - Network is not learning",
                "   → Check if gradients are flowing (may need gradient logging)",
                "   → Increase learning rate by 10x and restart",
                "   → Verify embedding space is producing varied embeddings",
                "   → Check for NaN/Inf in loss or gradients"
            ])
        
        # FAILURE MODE 2: Constant Probability Output
        elif prob_std < 0.03 or prob_range < 0.05:
            failures.append("CONSTANT_PROBABILITY")
            recommendations.extend([
                f"⚠️  WARNING: Model produces nearly identical probabilities (std={prob_std:.4f}, range={prob_range:.4f})",
                "   → Increase learning rate by 3-5x",
                f"   → Current epoch {epoch_idx} may be too early - consider training longer",
                "   → Check if loss is decreasing - if not, restart with higher LR",
                "   → Verify input embeddings have variation"
            ])
        
        # FAILURE MODE 3: Always Predicts One Class
        elif max_pred_pct > 95:
            dominant_class = max(pred_counts, key=pred_counts.get)
            failures.append("SINGLE_CLASS_BIAS")
            recommendations.extend([
                f"⚠️  WARNING: Model predicts '{dominant_class}' {max_pred_pct:.1f}% of the time",
                f"   → Ground truth is {true_pos_pct:.1f}% positive class",
                "   → If classes are imbalanced in data, this may be expected initially",
                "   → Consider using class weights in loss function",
                "   → May need to train longer to learn minority class",
                f"   → Optimal threshold is {optimal_threshold:.3f} - very extreme suggests poor calibration"
            ])
        
        # FAILURE MODE 4: Random Predictions (AUC ~0.5)
        elif auc < 0.55:
            failures.append("RANDOM_PREDICTIONS")
            recommendations.extend([
                f"⚠️  WARNING: Model is guessing randomly (AUC={auc:.3f})",
                "   → Network has not learned to discriminate between classes",
                f"   → At epoch {epoch_idx}, may need significantly more training",
                "   → Verify embedding space is trained and meaningful",
                "   → Check if target column has predictive signal in the data",
                "   → Consider checking feature importance/correlations"
            ])
        
        # FAILURE MODE 5: Clustered Near Decision Boundary
        elif pct_near_boundary > 70:
            failures.append("UNDERCONFIDENT")
            recommendations.extend([
                f"⚠️  WARNING: {pct_near_boundary:.1f}% of predictions are between 0.4-0.6",
                "   → Model is very uncertain/underconfident",
                f"   → May need more training (currently at epoch {epoch_idx})",
                "   → Consider if validation set is too different from training",
                "   → This can also indicate the problem is genuinely difficult"
            ])
        
        # FAILURE MODE 6: Poor Performance Despite Good Variation
        elif auc < 0.65 and accuracy < 0.6 and prob_std > 0.1:
            failures.append("POOR_DISCRIMINATION")
            recommendations.extend([
                f"⚠️  WARNING: Model has variation (std={prob_std:.3f}) but poor metrics (AUC={auc:.3f})",
                "   → Network is producing varied outputs but wrong predictions",
                "   → May be learning spurious patterns",
                "   → Check if training loss is decreasing properly",
                "   → Consider data quality or feature engineering issues"
            ])
        
        # SUCCESS: Model seems to be learning
        elif auc > 0.7 and prob_std > 0.1:
            return False, "HEALTHY", ["✅ Model appears to be learning normally"]
        
        # Log all detected failures
        if failures:
            failure_label = "_".join(failures)
            logger.error(f"{log_prefix}" + "=" * 80)
            logger.error(f"{log_prefix}🚨 TRAINING FAILURE DETECTED: {failure_label}")
            logger.error(f"{log_prefix}" + "=" * 80)
            for rec in recommendations:
                logger.error(f"{log_prefix}{rec}")
            logger.error(f"{log_prefix}" + "=" * 80)
            
            # Record the warning
            self.record_training_warning(
                warning_type=failure_label,
                epoch=epoch_idx if epoch_idx is not None else -1,
                details={
                    "auc": auc,
                    "accuracy": accuracy,
                    "optimal_threshold": optimal_threshold,
                    "recommendations": recommendations,
                    "prediction_distribution": dict(pred_counts) if pred_counts else {}
                }
            )
            
            return True, failure_label, recommendations
        
        return False, "UNKNOWN", []

    def compute_classification_metrics(self, queries, ground_truth, pos_label, epoch_idx=0, n_epochs=None):
        """Compute classification metrics for both binary and multi-class problems.

        Args:
            queries: list of queries
            ground_truth: list of ground truth labels
            pos_label: label of the positive class (for binary) or main class (for multi-class)
            epoch_idx: current epoch number (for failure detection)
            n_epochs: total number of epochs (for failure detection)
        """
        if self.run_binary_metrics == False:
            return {}
        
        # Skip metrics computation for scalar/regression targets
        if not isinstance(self.target_codec, SetCodec):
            return {}
        
        is_binary = self.should_compute_binary_metrics()
        
        log_prefix = self._get_log_prefix(epoch_idx)
        logger.info(f"{log_prefix}Computing {'binary' if is_binary else 'multi-class'} classification metrics")
        logger.info(f"{log_prefix}Number of target classes: {len(self.target_codec.members)} (including <UNKNOWN>)")

        # print(f"...compute_binary_metrics ... type(queries) = {type(queries)}... {type(queries[0])}")
        # print(f"...compute_binary_metrics ... type(ground_truth) = {type(ground_truth)}")
        # print(f"...compute_binary_metrics ... type(pos_label) = {type(pos_label)}.. pos_label = {pos_label}")

        queries, ground_truth = self.strip_queries(queries=queries, ground_truth=ground_truth)

        # print(f"pos_label = {pos_label}; type = {type(pos_label)}")
        if pos_label != pos_label:
            return {
                "accuracy": -1,
                "precision": -1,
                "recall": -1,
                "auc": -1,
                "_had_error": True,
                "metrics_secs": -1,
                "_reason": "pos_label is None",
            }

        # Put the model in eval model for evaluation, but save the entry training state
        # so it can be restored at exit.
        with PredictorEvalModeContextManager(fsp=self, debugLabel="compute_classification_metrics"):
            # ASSERT: We must be in eval mode for metrics computation
            assert self.predictor.training == False, f"❌ METRICS BUG: predictor should be in eval mode but training={self.predictor.training}"
            assert self.embedding_space.encoder.training == False, f"❌ METRICS BUG: encoder should be in eval mode but training={self.embedding_space.encoder.training}"
            logger.debug("✓ compute_classification_metrics: Models correctly in EVAL mode")
            
            # Log BatchNorm statistics at the start of metrics computation (only on first few epochs)
            if epoch_idx is not None and epoch_idx <= 3:
                # self.predictor is nn.Sequential(predictor_base, final_layer)
                # We need to access predictor_base (SimpleMLP) to get log_batchnorm_stats
                if hasattr(self.predictor_base, 'log_batchnorm_stats'):
                    logger.info(f"🔍 BatchNorm Stats at Epoch {epoch_idx} (EVAL MODE):")
                    self.predictor_base.log_batchnorm_stats()
                else:
                    logger.warning(f"⚠️  predictor_base ({type(self.predictor_base)}) doesn't have log_batchnorm_stats method")
            
            ts = time.time()
            if queries is None:
                queries = []

            f1 = 0
            accuracy = 0
            precision = 0
            recall = 0
            auc = 0
            
            # Multi-class specific metrics
            macro_f1 = 0
            weighted_f1 = 0

            # OPTIMIZATION: Use batched prediction instead of sequential predict() calls
            # This provides 10-100x speedup by processing all queries in GPU batches
            results = []
            raw_logits_list = []  # Track raw model outputs before softmax
            
            if not queries:
                return {}
            
            # Use internal batching logic for maximum performance
            try:
                import pandas as pd
                from torch.utils.data import DataLoader
                from featrix.neural.data_frame_data_set import SuperSimpleSelfSupervisedDataset, collate_tokens
                
                # Process queries in batches for GPU efficiency
                batch_size = 256  # Same as predict_batch default
                total_batches = (len(queries) + batch_size - 1) // batch_size
                
                for batch_start in range(0, len(queries), batch_size):
                    batch_end = min(batch_start + batch_size, len(queries))
                    batch_queries = queries[batch_start:batch_end]
                    
                    # Convert queries to DataFrame for batching
                    batch_df = pd.DataFrame(batch_queries)
                    
                    # Create dataset and dataloader for efficient batching
                    dataset = SuperSimpleSelfSupervisedDataset(batch_df, self.all_codecs)
                    dataloader = DataLoader(
                        dataset,
                        batch_size=len(batch_df),  # Process entire batch at once
                        shuffle=False,
                        collate_fn=collate_tokens,
                    )
                    
                    # Get the single batch
                    column_batch = next(iter(dataloader))
                    
                    # Move data to same device as encoder
                    encoder_device = next(self.embedding_space.encoder.parameters()).device
                    for tokenbatch in column_batch.values():
                        tokenbatch.to(encoder_device)
                    
                    # Remove target column if present (for marginal encoding)
                    if self.target_col_name in column_batch:
                        target_token_batch = column_batch.pop(self.target_col_name)
                        
                        # Add marginal tokens if target was in original embedding space
                        if self.target_col_name in self.embedding_space.col_codecs:
                            marginal_token_batch = self._create_marginal_token_batch_for_target(target_token_batch)
                            column_batch[self.target_col_name] = marginal_token_batch
                    
                    # Encode the entire batch at once - MASSIVE SPEEDUP!
                    _, batch_encoding = self.embedding_space.encoder.encode(column_batch, apply_noise=False)
                    
                    # Move batch_encoding to same device as predictor
                    predictor_device = next(self.predictor.parameters()).device
                    batch_encoding = batch_encoding.to(predictor_device)
                    
                    # Run predictor on entire batch
                    batch_output = self.predictor(batch_encoding)  # Raw logits [batch_size, num_classes]
                    
                    # Extract raw logits before softmax (for diagnostics)
                    raw_logits_batch = batch_output.detach().cpu().numpy()
                    raw_logits_list.extend([raw_logits_batch[i] for i in range(len(batch_queries))])
                    
                    # Convert batch output to individual predictions
                    for i in range(len(batch_queries)):
                        single_output = batch_output[i:i+1]  # Keep batch dimension
                        prediction = self._convert_output_to_prediction(single_output)
                        
                        if type(prediction) != dict:
                            # not a classifier.
                            return {}
                        results.append(prediction)
                        
            except Exception as e:
                logger.warning(f"Batched prediction failed, falling back to sequential: {e}")
                logger.debug(f"  Full traceback:\n{traceback.format_exc()}")
                # Fallback to old method if batching fails
                for q in queries:
                    try:
                        prediction = self.predict(q, ignore_unknown=True, debug_print=False)
                        if type(prediction) != dict:
                            return {}
                        results.append(prediction)
                        # For fallback, we skip raw_logits extraction to save time
                    except Exception as e2:
                        def short_dict(d):
                            dd = {}
                            if d is None:
                                return "None"
                            for k, v in d.items():
                                v = str(v)
                                if len(v) > 32:
                                    v = v[:32] + "..."
                                dd[k] = v
                            return dd
                        logger.warning(f"PREDICTION FAILED: q = {short_dict(q)}")
                        logger.warning(f"  Exception: {type(e2).__name__}: {str(e2)}")
                        logger.debug(f"  Full traceback:\n{traceback.format_exc()}")
            
            # DIAGNOSTIC: Log raw logits distribution (moved to DEBUG level for performance)
            if raw_logits_list and len(raw_logits_list) > 0:
                raw_logits_array = np.vstack(raw_logits_list)
                logger.debug(f"📊 RAW LOGITS (before softmax):")
                logger.debug(f"   Shape: {raw_logits_array.shape}")
                logger.debug(f"   Min: {raw_logits_array.min():.4f}, Max: {raw_logits_array.max():.4f}")
                logger.debug(f"   Mean: {raw_logits_array.mean():.4f}, Std: {raw_logits_array.std():.4f}")
                if raw_logits_array.shape[1] >= 2:
                    # For binary or multi-class, show per-class stats
                    for class_idx in range(raw_logits_array.shape[1]):
                        class_logits = raw_logits_array[:, class_idx]
                        logger.debug(f"   Class {class_idx}: mean={class_logits.mean():.4f}, std={class_logits.std():.4f}")
                
                # Check if logits are suspiciously constant (keep as ERROR for important issues)
                if raw_logits_array.std() < 0.01:
                    logger.error(f"🚨 RAW LOGITS ARE NEARLY CONSTANT (std={raw_logits_array.std():.6f})")
                    logger.error("   This suggests the model is not learning properly")
                    if hasattr(self.predictor_base, 'log_batchnorm_stats'):
                        logger.error("   Logging BatchNorm stats to diagnose:")
                        self.predictor_base.log_batchnorm_stats()
                    else:
                        logger.error(f"   predictor_base ({type(self.predictor_base)}) doesn't have log_batchnorm_stats")


            if isinstance(self.target_codec, SetCodec):
                # Ensure pos_label is string for consistency
                #if type(pos_label) != str:
                #    pos_label = str(pos_label)
                # Ensure pos_label matches the data type in ground_truth
                # Convert pos_label to match the most common type in ground_truth
                if ground_truth:
                    sample_gt = ground_truth[0]
                    if type(pos_label) != type(sample_gt):
                        # Convert pos_label to match the ground_truth type
                        if isinstance(sample_gt, str):
                            pos_label = str(pos_label)
                        elif isinstance(sample_gt, (int, float)):
                            try:
                                pos_label = type(sample_gt)(pos_label)
                            except (ValueError, TypeError):
                                pos_label = str(pos_label)


            try:
                # OPTIMIZATION: Vectorized prediction extraction
                preds = [max(d, key=d.get) for d in results]
                logger.debug(f"PREDS = {preds[:10]}...")  # Show first 10
                
                # DIAGNOSTIC: Show unique predicted classes (moved to DEBUG for performance)
                from collections import Counter
                pred_counts = Counter(preds)
                logger.debug(f"{log_prefix}📊 PREDICTED CLASS DISTRIBUTION:")
                for pred_class, count in pred_counts.most_common():
                    logger.debug(f"{log_prefix}   {pred_class}: {count} ({count/len(preds)*100:.1f}%)")
                
                # DIAGNOSTIC: Show ground truth class distribution for comparison (moved to DEBUG)
                gt_counts = Counter(ground_truth)
                logger.debug(f"{log_prefix}📊 GROUND TRUTH CLASS DISTRIBUTION:")
                for gt_class, count in gt_counts.most_common():
                    logger.debug(f"{log_prefix}   {gt_class}: {count} ({count/len(ground_truth)*100:.1f}%)")
                    
            except Exception as e:
                logger.error(f"Error in computing predictions: {e}")
                return {}

            num_tests_worked = 0
            ground_truth, preds, pos_label = self.normalize_types(ground_truth, preds, pos_label)
            self.validate_metrics_inputs(ground_truth, preds, pos_label)

            # Overall accuracy (works for both binary and multi-class)
            try:
                from sklearn.metrics import accuracy_score
                accuracy = accuracy_score(ground_truth, preds)
                num_tests_worked += 1
                logger.info(f"{log_prefix}Overall accuracy: {accuracy:.3f}")
            except Exception as e:
                accuracy = 0
                self.handle_metrics_error("accuracy", e)

            if is_binary:
                # Binary classification metrics
                try:
                    from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
                    
                    # OPTIMIZATION: Vectorized probability extraction with type mismatch handling
                    # Prediction dicts may have string keys, but pos_label might be float/int
                    
                    pos_probs = []
                    extraction_method = None
                    sample_dict_keys = list(results[0].keys()) if results else []
                    
                    # Pre-determine extraction strategy from first result to avoid per-item checks
                    if results:
                        first_dict = results[0]
                        # Try strategies in order of preference
                        if pos_label in first_dict:
                            extraction_method = f"exact_match (key type: {type(pos_label).__name__})"
                            pos_probs = [d.get(pos_label, 0.0) for d in results]
                        elif str(pos_label) in first_dict:
                            extraction_method = f"string_conversion ('{pos_label}' -> '{str(pos_label)}')"
                            pos_label_str = str(pos_label)
                            pos_probs = [d.get(pos_label_str, 0.0) for d in results]
                            logger.warning(f"⚠️  TYPE MISMATCH: pos_label is {type(pos_label).__name__} but dict keys are strings")
                            logger.warning(f"   Using string conversion: {pos_label} -> '{pos_label_str}'")
                            logger.warning(f"   Dict keys: {sample_dict_keys}")
                        else:
                            # Fuzzy match: try converting keys to pos_label type
                            found_key = None
                            for key in first_dict.keys():
                                try:
                                    if type(pos_label)(key) == pos_label:
                                        found_key = key
                                        extraction_method = f"fuzzy_match (key '{key}' converted to {type(pos_label).__name__})"
                                        logger.warning(f"⚠️  FUZZY MATCH: Found pos_label by converting key '{key}' -> {type(pos_label)(key)}")
                                        logger.warning(f"   Dict keys: {sample_dict_keys}")
                                        break
                                except (ValueError, TypeError):
                                    continue
                            
                            if found_key:
                                pos_probs = [d.get(found_key, 0.0) for d in results]
                            else:
                                # Last resort: all failed
                                logger.error(f"🚨 FAILED to extract probability for pos_label={pos_label} (type={type(pos_label).__name__})")
                                logger.error(f"   Dict keys: {sample_dict_keys}")
                                logger.error(f"   Tried: exact match, string conversion, type conversion")
                                logger.error(f"   Using 0.0 as fallback - METRICS WILL BE WRONG!")
                                pos_probs = [0.0] * len(results)
                    
                    # Log which extraction method was used (only once)
                    if extraction_method:
                        logger.debug(f"{log_prefix}📊 Probability extraction method: {extraction_method}")
                    
                    # DIAGNOSTIC: Check if we're getting valid probabilities (keep as ERROR for important issues)
                    if all(p == 0 for p in pos_probs):
                        logger.error(f"🚨 BUG: All probabilities are 0!")
                        logger.error(f"   pos_label={pos_label} (type={type(pos_label).__name__})")
                        logger.error(f"   Sample dict keys: {sample_dict_keys}")
                        logger.error(f"   Sample dict: {results[0] if results else 'no results'}")
                        logger.error(f"   This indicates a type mismatch between pos_label and prediction dict keys")
                    
                    # OPTIMIZATION: Vectorized binary conversion
                    pos_probs_array = np.array(pos_probs)
                    y_true_binary = np.array([1 if gt == pos_label else 0 for gt in ground_truth])
                    
                    # DIAGNOSTIC: Log probability distribution (moved to DEBUG for performance)
                    logger.debug(f"{log_prefix}📊 PROBABILITY DISTRIBUTION:")
                    logger.debug(f"{log_prefix}   Min: {pos_probs_array.min():.4f}, Max: {pos_probs_array.max():.4f}")
                    logger.debug(f"{log_prefix}   Mean: {pos_probs_array.mean():.4f}, Median: {np.median(pos_probs_array):.4f}")
                    logger.debug(f"{log_prefix}   Std: {pos_probs_array.std():.4f}")
                    logger.debug(f"{log_prefix}   Percentiles [10%, 25%, 50%, 75%, 90%]: {np.percentile(pos_probs_array, [10, 25, 50, 75, 90])}")
                    
                    # DIAGNOSTIC: Class distribution (moved to DEBUG)
                    pos_count = int(y_true_binary.sum())
                    neg_count = len(y_true_binary) - pos_count
                    ground_truth_pos_rate = pos_count / len(y_true_binary) if len(y_true_binary) > 0 else 0.0
                    
                    # Determine negative class label from target_codec
                    neg_label = None
                    if self.target_codec and hasattr(self.target_codec, 'members'):
                        # Find the other class that's not pos_label
                        # Handle type mismatches (e.g., pos_label='1.0' vs member='1')
                        pos_label_normalized = str(pos_label).strip()
                        for member in self.target_codec.members:
                            member_str = str(member).strip()
                            # Compare normalized strings and also check if they represent the same value
                            if member_str != pos_label_normalized and member != "<UNKNOWN>":
                                # Double-check: if both convert to same float/int, they're the same class
                                try:
                                    pos_val = float(pos_label_normalized)
                                    member_val = float(member_str)
                                    if pos_val == member_val:
                                        continue  # Same value, skip
                                except (ValueError, TypeError):
                                    pass  # Can't convert, use string comparison
                                neg_label = member
                                break
                        # If not found (shouldn't happen for binary), use a default
                        if neg_label is None:
                            neg_label = "other"
                    
                    logger.debug(f"{log_prefix}📊 CLASS DISTRIBUTION:")
                    logger.debug(f"{log_prefix}   Positive class = '{pos_label}': {pos_count} ({pos_count/len(y_true_binary)*100:.1f}%)")
                    logger.debug(f"{log_prefix}   Negative class = '{neg_label}': {neg_count} ({neg_count/len(y_true_binary)*100:.1f}%)")
                    
                    # Compute constraint bounds on predicted positive rate (C: Constraints)
                    # Rule: [ground_truth_rate * 0.5, ground_truth_rate * 1.5] with min 0.1, max 0.9
                    if ground_truth_pos_rate > 0:
                        min_rate = max(0.1, ground_truth_pos_rate * 0.5)
                        max_rate = min(0.9, ground_truth_pos_rate * 1.5)
                        # Ensure min < max and reasonable bounds
                        if min_rate >= max_rate:
                            min_rate = max(0.1, ground_truth_pos_rate - 0.1)
                            max_rate = min(0.9, ground_truth_pos_rate + 0.1)
                        predicted_positive_rate_bounds = (min_rate, max_rate)
                    else:
                        predicted_positive_rate_bounds = None
                    
                    # Find optimal threshold for F1 score with constraints
                    optimal_threshold, optimal_f1 = self.best_threshold_for_f1(
                        y_true_binary, 
                        pos_probs,
                        predicted_positive_rate_bounds=predicted_positive_rate_bounds
                    )
                    
                    # Compute predicted positive rate at optimal threshold for logging
                    pred_pos_rate_at_optimal = (pos_probs_array >= optimal_threshold).mean()
                    
                    # Log constraint info if constraints were applied
                    if predicted_positive_rate_bounds:
                        logger.debug(f"{log_prefix}📊 Threshold Search Constraints:")
                        logger.debug(f"{log_prefix}   Ground truth positive rate: {ground_truth_pos_rate:.1%}")
                        logger.debug(f"{log_prefix}   Allowed predicted positive rate: [{predicted_positive_rate_bounds[0]:.1%}, {predicted_positive_rate_bounds[1]:.1%}]")
                        logger.debug(f"{log_prefix}   Selected threshold: {optimal_threshold:.4f} → predicted rate: {pred_pos_rate_at_optimal:.1%}")
                    
                    # TRACK: Record threshold history over epochs (always track for debugging)
                    self.optimal_threshold_history.append({
                        'epoch': epoch_idx,
                        'threshold': optimal_threshold,
                        'f1_score': optimal_f1,
                        'accuracy_at_optimal': None,  # Will be set below
                        'auc': None  # Will be set below
                    })
                    
                    # OPTIMIZATION: Vectorized threshold application
                    optimal_preds = (pos_probs_array >= optimal_threshold).astype(int).tolist()
                    
                    # DIAGNOSTIC: Prediction distribution at optimal threshold (moved to DEBUG)
                    pred_pos_count = int(sum(optimal_preds))
                    pred_neg_count = len(optimal_preds) - pred_pos_count
                    logger.debug(f"{log_prefix}📊 PREDICTIONS AT OPTIMAL THRESHOLD {optimal_threshold:.4f}:")
                    logger.debug(f"{log_prefix}   Predicted positive = '{pos_label}': {pred_pos_count} ({pred_pos_count/len(optimal_preds)*100:.1f}%)")
                    logger.debug(f"{log_prefix}   Predicted negative = '{neg_label}': {pred_neg_count} ({pred_neg_count/len(optimal_preds)*100:.1f}%)")
                    
                    # Compute metrics with optimal threshold
                    precision = precision_score(y_true_binary, optimal_preds, zero_division=0)
                    recall = recall_score(y_true_binary, optimal_preds, zero_division=0)
                    f1 = f1_score(y_true_binary, optimal_preds, zero_division=0)
                    
                    # Compute confusion matrix
                    from sklearn.metrics import confusion_matrix
                    tn, fp, fn, tp = confusion_matrix(y_true_binary, optimal_preds).ravel()
                    
                    # Compute accuracy at optimal threshold
                    accuracy_at_optimal = (tp + tn) / (tp + tn + fp + fn)
                    
                    # Update threshold history with accuracy
                    if self.optimal_threshold_history:
                        self.optimal_threshold_history[-1]['accuracy_at_optimal'] = accuracy_at_optimal
                    
                    # Specificity (True Negative Rate)
                    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
                    
                    # TPR (True Positive Rate / Recall / Sensitivity)
                    tpr = recall  # Already computed above
                    
                    # Balanced Accuracy = (TPR + TNR) / 2
                    balanced_accuracy = (tpr + specificity) / 2.0
                    
                    # MCC (Matthews Correlation Coefficient) - gold standard for imbalanced data
                    from sklearn.metrics import matthews_corrcoef
                    mcc = matthews_corrcoef(y_true_binary, optimal_preds)
                    
                    # Brier Score (mean squared error of probabilities) - calibration metric
                    from sklearn.metrics import brier_score_loss
                    brier_score = brier_score_loss(y_true_binary, pos_probs_array)
                    
                    # Calibration metrics: ECE (Expected Calibration Error) and MCE (Maximum Calibration Error)
                    # Also compute reliability curve data
                    ece = None
                    mce = None
                    reliability_curve = None
                    sharpness = None
                    
                    try:
                        # Compute calibration metrics using probability bins
                        n_bins = 10
                        bin_boundaries = np.linspace(0, 1, n_bins + 1)
                        bin_lowers = bin_boundaries[:-1]
                        bin_uppers = bin_boundaries[1:]
                        
                        # Compute calibration errors per bin
                        ece_sum = 0.0
                        mce_max = 0.0
                        total_samples = len(y_true_binary)
                        reliability_data = []
                        
                        for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
                            # Find samples in this bin
                            in_bin = (pos_probs_array > bin_lower) & (pos_probs_array <= bin_upper)
                            prop_in_bin = in_bin.mean()
                            
                            if prop_in_bin > 0:
                                # Mean predicted probability in this bin
                                mean_pred_prob = pos_probs_array[in_bin].mean()
                                
                                # Actual event frequency in this bin
                                actual_freq = y_true_binary[in_bin].mean()
                                
                                # Calibration error for this bin
                                bin_error = abs(mean_pred_prob - actual_freq)
                                
                                # Weight by proportion of samples in bin
                                ece_sum += bin_error * prop_in_bin
                                
                                # Track maximum error
                                if bin_error > mce_max:
                                    mce_max = bin_error
                                
                                # Store reliability curve data
                                reliability_data.append({
                                    'bin_center': (bin_lower + bin_upper) / 2.0,
                                    'mean_pred_prob': float(mean_pred_prob),
                                    'actual_freq': float(actual_freq),
                                    'prop_in_bin': float(prop_in_bin),
                                    'bin_error': float(bin_error)
                                })
                            else:
                                # Empty bin - still record for completeness
                                reliability_data.append({
                                    'bin_center': (bin_lower + bin_upper) / 2.0,
                                    'mean_pred_prob': None,
                                    'actual_freq': None,
                                    'prop_in_bin': 0.0,
                                    'bin_error': None
                                })
                        
                        ece = float(ece_sum)
                        mce = float(mce_max)
                        reliability_curve = reliability_data
                        
                        # Sharpness: variance of predicted probabilities
                        sharpness = float(pos_probs_array.var())
                        
                    except Exception as e:
                        logger.warning(f"{log_prefix}⚠️  Failed to compute calibration metrics: {e}")
                    
                    # Binary AUC (doesn't depend on threshold)
                    auc = roc_auc_score(y_true_binary, pos_probs)
                    
                    # PR-AUC (Average Precision) - often better for imbalanced datasets
                    pr_auc = average_precision_score(y_true_binary, pos_probs)
                    
                    # Update threshold history with AUC
                    if self.optimal_threshold_history:
                        self.optimal_threshold_history[-1]['auc'] = auc
                        self.optimal_threshold_history[-1]['pr_auc'] = pr_auc
                    
                    # Compute banding/lift-style metric (positive:negative ratio across probability bands)
                    bands_data = None
                    try:
                        bands_df = compute_binary_lift_bands(pos_probs, y_true_binary, n_bins=10)
                        # Convert DataFrame to dict format for JSON serialization
                        bands_list = []
                        for idx, row in bands_df.iterrows():
                            band_interval = row['band']
                            band_dict = {
                                'band_lower': float(band_interval.left) if pd.notna(band_interval.left) else None,
                                'band_upper': float(band_interval.right) if pd.notna(band_interval.right) else None,
                                'avg_pred': float(row['avg_pred']),
                                'n': int(row['n']),
                                'n_positive': int(row['n_positive']),
                                'n_negative': int(row['n_negative']),
                                'positive_negative_ratio': float(row['positive_negative_ratio']) if pd.notna(row['positive_negative_ratio']) else None,
                            }
                            bands_list.append(band_dict)
                        bands_data = {'bands': bands_list}
                        logger.info(f"{log_prefix}📊 Binary Lift Bands (Positive:Negative Ratio by Predicted Probability):")
                        logger.info(f"{log_prefix}   {'Band Range':<25} {'Avg Pred':>9} {'Count':>7} {'Pos':>6} {'Neg':>6} {'Pos:Neg Ratio':>14}")
                        logger.info(f"{log_prefix}   {'-'*25} {'-'*9} {'-'*7} {'-'*6} {'-'*6} {'-'*14}")
                        for band in bands_list:
                            band_str = f"[{band['band_lower']:.3f}, {band['band_upper']:.3f}]"
                            avg_pred = band['avg_pred']
                            n = band['n']
                            n_pos = band['n_positive']
                            n_neg = band['n_negative']
                            ratio = band['positive_negative_ratio']
                            ratio_str = f"{ratio:.3f}" if ratio is not None else "N/A"
                            logger.info(f"{log_prefix}   {band_str:<25} {avg_pred:9.3f} {n:7d} {n_pos:6d} {n_neg:6d} {ratio_str:>14}")
                    except Exception as e:
                        logger.warning(f"{log_prefix}⚠️  Failed to compute binary lift bands metric: {e}")
                        logger.debug(f"{log_prefix}   Full traceback:\n{traceback.format_exc()}")
                    
                    # Cost-based metrics (if costs are available)
                    cost_min = None
                    tau_cost = None
                    f1_cost = None
                    cost_metrics = None
                    if self.cost_false_positive is not None and self.cost_false_negative is not None:
                        try:
                            # Compute cost-optimal threshold
                            tau_cost, cost_min, (tp_cost, fp_cost, tn_cost, fn_cost), f1_cost = self.best_threshold_for_cost(
                                y_true_binary,
                                pos_probs,
                                self.cost_false_positive,
                                self.cost_false_negative,
                                min_pred_pos_frac=predicted_positive_rate_bounds[0] if predicted_positive_rate_bounds else None,
                                max_pred_pos_frac=predicted_positive_rate_bounds[1] if predicted_positive_rate_bounds else None,
                            )
                            
                            # Compute baseline cost for normalization
                            baseline_cost = self._compute_baseline_cost(y_true_binary, self.cost_false_positive, self.cost_false_negative)
                            
                            # Store cost metrics
                            cost_metrics = {
                                "cost_min": cost_min,
                                "tau_cost": tau_cost,
                                "f1_cost": f1_cost,
                                "tp_cost": tp_cost,
                                "fp_cost": fp_cost,
                                "tn_cost": tn_cost,
                                "fn_cost": fn_cost,
                                "baseline_cost": baseline_cost,
                            }
                            
                            logger.debug(f"{log_prefix}💰 Cost-optimal threshold: {tau_cost:.4f}, cost: {cost_min:.2f}, F1: {f1_cost:.3f}")
                            logger.debug(f"{log_prefix}💰 Cost confusion matrix: TP={tp_cost}, FP={fp_cost}, TN={tn_cost}, FN={fn_cost}")
                        except Exception as e:
                            logger.warning(f"{log_prefix}⚠️  Failed to compute cost metrics: {e}")
                    
                    num_tests_worked += 3
                    
                    # USE OPTIMAL THRESHOLD METRICS AS PRIMARY (since we use threshold for prediction)
                    # Store argmax metrics for comparison (B: Log what you're optimizing)
                    argmax_preds = (pos_probs_array >= 0.5).astype(int)
                    argmax_accuracy = (y_true_binary == argmax_preds).mean()
                    argmax_precision = precision_score(y_true_binary, argmax_preds, zero_division=0)
                    argmax_recall = recall_score(y_true_binary, argmax_preds, zero_division=0)
                    argmax_f1 = f1_score(y_true_binary, argmax_preds, zero_division=0)
                    
                    # Compute deltas for logging
                    delta_f1 = f1 - argmax_f1
                    delta_accuracy = accuracy_at_optimal - argmax_accuracy
                    
                    # Update main metrics to use optimal threshold values
                    accuracy = accuracy_at_optimal
                    
                    # A: Only save threshold when AUC improves (or AUC ties and F1 improves)
                    auc_epsilon = 0.001  # Minimum improvement to count as "better"
                    should_save_threshold = False
                    threshold_update_msg = ""
                    
                    # First epoch: always save (best_auc is -1.0 initially)
                    if self._best_auc < 0:
                        self._best_auc = auc
                        self._best_auc_epoch = epoch_idx
                        self._best_f1_at_best_auc = f1
                        self._best_threshold_at_best_auc = optimal_threshold
                        self.optimal_threshold = optimal_threshold
                        should_save_threshold = True
                        threshold_update_msg = f"⭐ Initial threshold saved: AUC={auc:.3f}, F1={f1:.3f} (epoch {epoch_idx})"
                    elif auc > self._best_auc + auc_epsilon:
                        # New best AUC - always save
                        previous_auc = self._best_auc
                        self._best_auc = auc
                        self._best_auc_epoch = epoch_idx
                        self._best_f1_at_best_auc = f1
                        self._best_threshold_at_best_auc = optimal_threshold
                        self.optimal_threshold = optimal_threshold
                        should_save_threshold = True
                        threshold_update_msg = f"⭐ New best AUC: {auc:.3f} (previous: {previous_auc:.3f}, epoch {epoch_idx})"
                    elif abs(auc - self._best_auc) <= auc_epsilon and f1 > self._best_f1_at_best_auc:
                        # AUC ties (within epsilon) but F1 improved - save
                        previous_f1 = self._best_f1_at_best_auc
                        self._best_f1_at_best_auc = f1
                        self._best_threshold_at_best_auc = optimal_threshold
                        self.optimal_threshold = optimal_threshold
                        should_save_threshold = True
                        threshold_update_msg = f"⭐ Tied AUC ({auc:.3f}) but improved F1: {f1:.3f} (previous: {previous_f1:.3f}, epoch {epoch_idx})"
                    else:
                        # Metrics didn't improve - don't save threshold
                        threshold_update_msg = f"📊 Metrics: AUC={auc:.3f} (best: {self._best_auc:.3f} @ epoch {self._best_auc_epoch}), F1={f1:.3f} (best: {self._best_f1_at_best_auc:.3f}) - threshold not updated"
                    
                    # B: Enhanced logging showing what we're optimizing and tradeoffs
                    logger.info(f"{log_prefix}📊 Threshold Optimization Summary:")
                    logger.info(f"{log_prefix}   F1: argmax={argmax_f1:.3f}, optimal={f1:.3f}, ΔF1={delta_f1:+.3f}")
                    logger.info(f"{log_prefix}   Accuracy: argmax={argmax_accuracy:.3f}, optimal={accuracy_at_optimal:.3f}, ΔAcc={delta_accuracy:+.3f}")
                    if abs(delta_accuracy) > 0.01:  # Only show tradeoff if significant
                        tradeoff_direction = "cost" if delta_accuracy < 0 else "gain"
                        logger.info(f"{log_prefix}   Tradeoff: F1 improved by {delta_f1:.3f} at {tradeoff_direction} of {abs(delta_accuracy):.3f} accuracy")
                    
                    logger.info(f"{log_prefix}Binary metrics (optimal threshold {optimal_threshold:.3f}) - Precision: {precision:.3f}, Recall: {recall:.3f}, F1: {f1:.3f}, ROC-AUC: {auc:.3f}, PR-AUC: {pr_auc:.3f}")
                    logger.info(f"{log_prefix}Imbalanced data metrics - Balanced Accuracy: {balanced_accuracy:.3f}, MCC: {mcc:.3f}, Specificity: {specificity:.3f}")
                    ece_str = f"{ece:.4f}" if ece is not None else "N/A"
                    mce_str = f"{mce:.4f}" if mce is not None else "N/A"
                    sharpness_str = f"{sharpness:.4f}" if sharpness is not None else "N/A"
                    logger.info(f"{log_prefix}Calibration metrics - Brier Score: {brier_score:.4f}, ECE: {ece_str}, MCE: {mce_str}, Sharpness: {sharpness_str}")
                    if cost_metrics:
                        logger.info(f"{log_prefix}💰 Cost metrics (cost-optimal threshold {tau_cost:.3f}) - Cost: {cost_min:.2f}, F1: {f1_cost:.3f}, TP: {cost_metrics['tp_cost']}, FP: {cost_metrics['fp_cost']}, TN: {cost_metrics['tn_cost']}, FN: {cost_metrics['fn_cost']}")
                    logger.info(f"{log_prefix}Confusion Matrix - TP: {tp}, FP: {fp}, TN: {tn}, FN: {fn}, Specificity: {specificity:.3f}")
                    
                    if should_save_threshold:
                        logger.info(f"{log_prefix}{threshold_update_msg}")
                        logger.info(f"{log_prefix}💾 Saved optimal threshold {optimal_threshold:.4f} for use during prediction")
                    else:
                        logger.debug(f"{log_prefix}{threshold_update_msg}")
                        logger.debug(f"{log_prefix}   Using saved threshold from epoch {self._best_auc_epoch}: {self.optimal_threshold:.4f}")
                    
                    # FAILURE DETECTION: Analyze training and detect common failure modes
                    failure_detected, failure_label, recommendations = self.detect_training_failure_mode(
                        raw_logits_array=raw_logits_array if 'raw_logits_array' in locals() else None,
                        pos_probs_array=pos_probs_array,
                        pred_counts=pred_counts,
                        y_true_binary=y_true_binary,
                        auc=auc,
                        accuracy=accuracy,
                        optimal_threshold=optimal_threshold,
                        epoch_idx=epoch_idx,
                        n_epochs=n_epochs,
                        log_prefix=log_prefix
                    )
                    
                    # SAVE: Store rare label for use during prediction
                    self._pos_label = pos_label
                    
                    # Note: optimal threshold info will be added to metrics_result below
                    
                    # CRITICAL FAILURE DETECTION: Raise specific exceptions for different failure modes
                    if failure_detected:
                        from featrix.neural.training_exceptions import (
                            RandomPredictionsError,
                            DeadNetworkError,
                            ConstantProbabilityError,
                            SingleClassBiasError,
                            PoorDiscriminationError,
                            UnderconfidentError,
                        )
                        
                        # Define which failures should immediately stop training
                        immediate_stop_failures = ["DEAD_NETWORK", "CONSTANT_PROBABILITY"]
                        
                        # Define failures that should stop if they persist beyond a threshold
                        # RANDOM_PREDICTIONS: Should stop only if we're past 80% of training and still random
                        late_stage_threshold = 0.80  # 80% through training
                        is_late_stage = n_epochs and epoch_idx > (n_epochs * late_stage_threshold)
                        
                        should_stop = False
                        exception_to_raise = None
                        
                        # Check immediate stop conditions and create appropriate exceptions
                        if "DEAD_NETWORK" in failure_label:
                            should_stop = True
                            exception_to_raise = DeadNetworkError(
                                message=f"Network outputs frozen at epoch {epoch_idx}",
                                epoch=epoch_idx,
                                recommendations=recommendations
                            )
                        
                        elif "CONSTANT_PROBABILITY" in failure_label:
                            # Don't stop until epoch 50 - early epochs often have low variance
                            if epoch_idx >= 50:
                                should_stop = True
                                exception_to_raise = ConstantProbabilityError(
                                    message=f"Model produces constant probabilities at epoch {epoch_idx}",
                                    epoch=epoch_idx,
                                    recommendations=recommendations
                                )
                            else:
                                logger.warning(f"⚠️  CONSTANT_PROBABILITY detected at epoch {epoch_idx} but continuing (need epoch 50+ to abort)")
                                
                                # AUTOMATIC LR INCREASE: If we haven't increased LR yet, do it now
                                if not hasattr(self, '_lr_increased_for_constant_prob'):
                                    self._lr_increased_for_constant_prob = False
                                
                                if not self._lr_increased_for_constant_prob and epoch_idx >= 5:
                                    # Increase LR by 5x (as recommended by ConstantProbabilityError)
                                    # Get current LR from optimizer (get_lr() is not in scope here)
                                    optimizer = self._training_optimizer
                                    if optimizer and len(optimizer.param_groups) > 0:
                                        lr_value = optimizer.param_groups[0]['lr']
                                    else:
                                        # Fallback: use a reasonable default
                                        lr_value = 0.01
                                    new_lr = lr_value * 5.0
                                    
                                    logger.error("="*80)
                                    logger.error("🚨 AUTOMATIC LEARNING RATE INCREASE")
                                    logger.error("="*80)
                                    logger.error(f"   Detected CONSTANT_PROBABILITY at epoch {epoch_idx}")
                                    logger.error(f"   Current LR: {lr_value:.6e}")
                                    logger.error(f"   Increasing LR by 5x to: {new_lr:.6e}")
                                    logger.error(f"   This should help the model escape the flat region")
                                    logger.error("="*80)
                                    
                                    # Update optimizer learning rate for all parameter groups
                                    optimizer = self._training_optimizer
                                    for param_group in optimizer.param_groups:
                                        param_group['lr'] = new_lr
                                    
                                    # If scheduler exists, we need to update its base_lrs
                                    scheduler = self._training_scheduler
                                    if scheduler is not None:
                                        # For SequentialLR, update both schedulers
                                        if hasattr(scheduler, 'schedulers'):
                                            for sub_scheduler in scheduler.schedulers:
                                                if hasattr(sub_scheduler, 'base_lrs'):
                                                    sub_scheduler.base_lrs = [new_lr] * len(sub_scheduler.base_lrs)
                                                if hasattr(sub_scheduler, 'eta_min'):
                                                    # Update eta_min proportionally for cosine annealing
                                                    sub_scheduler.eta_min = new_lr * 1e-4  # Keep same ratio
                                        elif hasattr(scheduler, 'base_lrs'):
                                            scheduler.base_lrs = [new_lr] * len(scheduler.base_lrs)
                                    
                                    self._lr_increased_for_constant_prob = True
                                    logger.info(f"✅ Learning rate increased to {new_lr:.6e} - will take effect on next batch")
                                
                                should_stop = False
                        
                        # Check late-stage failures (only stop if we're far into training)
                        elif "RANDOM_PREDICTIONS" in failure_label and is_late_stage:
                            should_stop = True
                            exception_to_raise = RandomPredictionsError(
                                message=f"Model still random at epoch {epoch_idx}/{n_epochs} (>{late_stage_threshold*100:.0f}% complete)",
                                epoch=epoch_idx,
                                recommendations=recommendations
                            )
                        
                        if should_stop and exception_to_raise:
                            error_message = f"💥 STOPPING TRAINING: {str(exception_to_raise)}\n"
                            error_message += "\n".join(recommendations)
                            logger.error(error_message)
                            raise exception_to_raise
                    
                    # ADAPTIVE LOSS ADJUSTMENT: If reverse bias detected, adjust FocalLoss
                    if failure_detected and "SINGLE_CLASS_BIAS" in failure_label:
                        # Calculate ground truth counts from original labels
                        from collections import Counter
                        y_true_counts = Counter(ground_truth)
                        
                        # FIX TYPE MISMATCH: Normalize keys to strings for both dicts
                        # pred_counts has string keys (from dict keys), y_true_counts may have float keys
                        normalized_pred_counts = {str(k): v for k, v in pred_counts.items()}
                        normalized_true_counts = {str(k): v for k, v in y_true_counts.items()}
                        
                        # Try adaptive adjustment
                        adjustment_made = self.adjust_focal_loss_for_bias(
                            pred_counts=normalized_pred_counts,
                            y_true_counts=normalized_true_counts,
                            epoch_idx=epoch_idx
                        )
                        
                        if adjustment_made:
                            logger.info(f"🔧 Adaptive FocalLoss adjustment applied at epoch {epoch_idx}")
                    
                except TrainingFailureException as e:
                    # Re-raise training failure exceptions - these should stop training, not be swallowed
                    logger.error(f"🚨 Training failure exception detected: {type(e).__name__}")
                    raise  # Re-raise to stop training
                except Exception as e:
                    # For other exceptions, log as warning and continue
                    logger.warning(f"Binary metrics failed: {e}")
                    precision = recall = f1 = auc = 0
                    tp = fp = tn = fn = 0
                    specificity = 0
                    self.handle_metrics_error("binary_metrics", e)
            else:
                # Multi-class classification metrics
                try:
                    from sklearn.metrics import precision_score, recall_score, f1_score
                    
                    # Multi-class averages
                    precision = precision_score(ground_truth, preds, average='weighted', zero_division=0)
                    recall = recall_score(ground_truth, preds, average='weighted', zero_division=0)
                    f1 = f1_score(ground_truth, preds, average='weighted', zero_division=0)
                    macro_f1 = f1_score(ground_truth, preds, average='macro', zero_division=0)
                    weighted_f1 = f1  # Same as f1 above
                    
                    # Multi-class AUC (if possible)
                    try:
                        from sklearn.preprocessing import LabelBinarizer
                        from sklearn.metrics import roc_auc_score
                        
                        # Create probability matrix for multi-class AUC
                        unique_labels = sorted(set(ground_truth))
                        prob_matrix = []
                        for result in results:
                            prob_row = [result.get(label, 0) for label in unique_labels]
                            prob_matrix.append(prob_row)
                        
                        lb = LabelBinarizer()
                        y_true_binarized = lb.fit_transform(ground_truth)
                        
                        if len(unique_labels) > 2:
                            auc = roc_auc_score(y_true_binarized, prob_matrix, multi_class='ovr', average='weighted')
                        else:
                            auc = 0  # Fall back for edge cases
                            
                    except Exception:
                        auc = 0  # Multi-class AUC can be complex, skip if it fails
                    
                    num_tests_worked += 3
                    logger.info(f"{log_prefix}Multi-class metrics - Precision: {precision:.3f}, Recall: {recall:.3f}, F1: {f1:.3f}")
                    logger.info(f"{log_prefix}Multi-class F1 scores - Macro: {macro_f1:.3f}, Weighted: {weighted_f1:.3f}")
                    
                except Exception as e:
                    logger.warning(f"Multi-class metrics failed: {e}")
                    precision = recall = f1 = macro_f1 = weighted_f1 = 0
                    self.handle_metrics_error("multiclass_metrics", e)

            dt = time.time() - ts
            self.metrics_time += dt

            if num_tests_worked == 0:
                logger.warning(f"No classification metrics could be computed... skipping computation going forward.")
                self.run_binary_metrics = False

            logger.info(f"{log_prefix}Finished computing {'binary' if is_binary else 'multi-class'} metrics. Time: {dt:.2f}s")
            
            # Collect failure detection info if available (from binary path)
            failure_info = {}
            if 'failure_detected' in locals():
                failure_info = {
                    "failure_detected": failure_detected,
                    "failure_label": failure_label if failure_detected else None,
                    "recommendations": recommendations if failure_detected else []
                }
            
            # Return comprehensive metrics for both binary and multi-class
            metrics_result = {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "auc": auc,
                "pr_auc": pr_auc if is_binary and 'pr_auc' in locals() else None,  # PR-AUC (only for binary)
                "is_binary": is_binary,
                "num_classes": len(self.target_codec.members) - 1,  # Exclude <UNKNOWN>
                "_had_error": self.metrics_had_error,
                "metrics_secs": self.metrics_time,
            }
            
            # Add optimal threshold info for binary classification (if computed)
            if is_binary and hasattr(self, 'optimal_threshold') and self.optimal_threshold is not None:
                metrics_result['optimal_threshold'] = self.optimal_threshold
                # Get F1 and accuracy from history if available
                if self.optimal_threshold_history:
                    last_entry = self.optimal_threshold_history[-1]
                    metrics_result['optimal_threshold_f1'] = last_entry.get('f1_score', f1)
                    # Note: accuracy, precision, recall, f1 in metrics_result are already optimal threshold values
                    metrics_result['accuracy_at_optimal_threshold'] = last_entry.get('accuracy_at_optimal', accuracy)
                metrics_result['pos_label'] = getattr(self, '_pos_label', None)
                
                # Store argmax metrics (0.5 threshold) for comparison if available
                # These show what metrics would be with default threshold
                if 'argmax_accuracy' in locals():
                    metrics_result['argmax_accuracy'] = argmax_accuracy
                    metrics_result['argmax_precision'] = argmax_precision
                    metrics_result['argmax_recall'] = argmax_recall
                    metrics_result['argmax_f1'] = argmax_f1
                
                # Add imbalanced data metrics
                if 'balanced_accuracy' in locals():
                    metrics_result['balanced_accuracy'] = balanced_accuracy
                if 'mcc' in locals():
                    metrics_result['mcc'] = mcc
                if 'specificity' in locals():
                    metrics_result['specificity'] = specificity
                if 'tpr' in locals():
                    metrics_result['tpr'] = tpr
                
                # Add calibration metrics
                if 'brier_score' in locals():
                    metrics_result['brier_score'] = brier_score
                if 'ece' in locals() and ece is not None:
                    metrics_result['ece'] = ece
                if 'mce' in locals() and mce is not None:
                    metrics_result['mce'] = mce
                if 'sharpness' in locals() and sharpness is not None:
                    metrics_result['sharpness'] = sharpness
                if 'reliability_curve' in locals() and reliability_curve is not None:
                    metrics_result['reliability_curve'] = reliability_curve
                
                # Add banding/lift-style metric (positive:negative ratio across probability bands)
                if 'bands_data' in locals() and bands_data is not None:
                    metrics_result['binary_lift_bands'] = bands_data
                
                # Add cost metrics if available
                if 'cost_metrics' in locals() and cost_metrics:
                    metrics_result['cost_min'] = cost_metrics['cost_min']
                    metrics_result['tau_cost'] = cost_metrics['tau_cost']
                    metrics_result['f1_cost'] = cost_metrics['f1_cost']
                    metrics_result['baseline_cost'] = cost_metrics['baseline_cost']
                    metrics_result['pos_rate'] = ground_truth_pos_rate if 'ground_truth_pos_rate' in locals() else 0.0
                    
                    # Compute composite score
                    cost_metrics_for_score = {
                        "roc_auc": auc,
                        "pr_auc": pr_auc,
                        "cost_min": cost_metrics['cost_min'],
                        "pos_rate": ground_truth_pos_rate if 'ground_truth_pos_rate' in locals() else 0.0,
                    }
                    composite_score, score_components = self._compute_composite_score(
                        cost_metrics_for_score,
                        cost_metrics['baseline_cost']
                    )
                    metrics_result['composite_score'] = composite_score
                    metrics_result['score_components'] = score_components
            
            # Add failure detection info if present
            if failure_info:
                metrics_result.update(failure_info)
            
            # Add multi-class specific metrics
            if not is_binary:
                metrics_result.update({
                    "macro_f1": macro_f1,
                    "weighted_f1": weighted_f1,
                })
            else:
                # Add binary-specific metrics (like threshold)
                metrics_result.update({
                    "accuracy_threshold": getattr(self, '_last_accuracy_threshold', None),
                })
                
                # Add confusion matrix if available (binary classification only)
                if 'tp' in locals() and 'fp' in locals() and 'tn' in locals() and 'fn' in locals():
                    metrics_result.update({
                        "tp": int(tp),
                        "fp": int(fp),
                        "tn": int(tn),
                        "fn": int(fn),
                        "specificity": float(specificity) if 'specificity' in locals() else None,
                    })
                
                # Add positive prediction probabilities for distribution analysis
                if 'pos_probs_array' in locals() and pos_probs_array is not None:
                    metrics_result['pos_probs'] = pos_probs_array.tolist()
            
            return metrics_result
    
    def compute_binary_metrics(self, queries, ground_truth, pos_label):
        """
        Legacy compatibility method - redirects to compute_classification_metrics.
        
        This method is deprecated. Use compute_classification_metrics instead.
        """
        logger.warning("compute_binary_metrics is deprecated. Use compute_classification_metrics instead.")
        return self.compute_classification_metrics(queries, ground_truth, pos_label)

    def predict(self, input_dict: Dict, print_top: bool = False, ignore_unknown=False, debug_print=True, extended_result=False):

        if input_dict.get(self.target_col_name) is not None:
            raise RuntimeError(
                "The query input contains the target column of the model"
            )

        if self.target_codec is None:
            raise Exception("Cannot predict before the predictor is trained.")


        with PredictorEvalModeContextManager(fsp=self, debugLabel="predict"):
            # ASSERT: We must be in eval mode for prediction
            assert self.predictor.training == False, f"❌ PREDICT BUG: predictor should be in eval mode but training={self.predictor.training}"
            assert self.embedding_space.encoder.training == False, f"❌ PREDICT BUG: encoder should be in eval mode but training={self.embedding_space.encoder.training}"

            ####################################################### DO THE ACTUAL PREDICTION!!!
            # Only use full-dimensional embeddings for predictions.
            encoding = self.embedding_space.encode_record(input_dict, 
                                                          squeeze=False,
                                                          short=False,
                                                          output_device=device)
            out = self.predictor(encoding)
            
            ###################################################################################

            # TODO: how to handle nans in the domain?
            #       they should probably not even enter in the domain of the codec.
            # logger.debug("self.target_type... --> ", self.target_type)

            if isinstance(self.target_codec, SetCodec):
                # Apply calibration if available
                if self.calibration_method == 'temperature' and self.calibration_temperature is not None:
                    from featrix.neural.calibration_utils import apply_temperature_scaling
                    calibrated_out = apply_temperature_scaling(out, self.calibration_temperature)
                    probs = self.sm(calibrated_out).squeeze(dim=0)
                elif self.calibration_method == 'platt' and self.calibration_platt_model is not None:
                    from featrix.neural.calibration_utils import apply_platt_scaling
                    calibrated_probs_np = apply_platt_scaling(out, self.calibration_platt_model)
                    # Convert back to tensor for consistency (already probabilities, not logits)
                    probs = torch.from_numpy(calibrated_probs_np[0]).to(out.device)
                elif self.calibration_method == 'isotonic' and self.calibration_isotonic_model is not None:
                    from featrix.neural.calibration_utils import apply_isotonic_regression
                    calibrated_probs_np = apply_isotonic_regression(out, self.calibration_isotonic_model)
                    # Convert back to tensor for consistency (already probabilities, not logits)
                    probs = torch.from_numpy(calibrated_probs_np[0]).to(out.device)
                else:
                    # No calibration or calibration method not available
                    probs = self.sm(out).squeeze(dim=0)
                
                # DIAGNOSTIC: Log token mapping for debugging backwards predictions
                debug_count = getattr(self, '_predict_debug_count', 0)
                if debug_count < 3:  # Only log first 3 predictions
                    logger.info(f"🔍 PREDICTION DEBUG #{debug_count}:")
                    logger.info(f"   Raw logits: {out.squeeze(dim=0).tolist()}")
                    logger.info(f"   Softmax probs: {probs.tolist()}")
                    logger.info(f"   Token mapping: {self.target_codec.tokens_to_members}")
                    self._predict_debug_count = debug_count + 1
                
                # Build probability dictionary first (needed for both threshold and argmax)
                probs_dict = {
                    self.target_codec.detokenize(
                        Token(value=i, status=TokenStatus.OK)
                    ): prob.item()
                    for i, prob in enumerate(probs)
                }
                
                # Check if this is binary classification and we have an optimal threshold
                is_binary = self.should_compute_binary_metrics()
                use_optimal_threshold = is_binary and self.optimal_threshold is not None
                
                if use_optimal_threshold:
                    # USE OPTIMAL THRESHOLD: For binary classification, use the threshold that maximizes F1
                    # Find the rare class label (stored from training)
                    pos_label = getattr(self, '_pos_label', None)
                    
                    if pos_label is None:
                        # Try to infer from training metrics
                        if self.training_metrics and 'pos_label' in self.training_metrics:
                            pos_label = self.training_metrics['pos_label']
                            self._pos_label = pos_label
                    
                    if pos_label is not None and pos_label in probs_dict:
                        # Get positive class probability
                        pos_prob = probs_dict[pos_label]
                        
                        # Apply optimal threshold: predict positive if prob >= threshold
                        if pos_prob >= self.optimal_threshold:
                            # Predict positive class - keep probabilities as-is
                            result_dict = probs_dict
                        else:
                            # Predict negative class - swap probabilities
                            # Find negative class (the other class that's not <UNKNOWN>)
                            neg_label = None
                            for label in probs_dict.keys():
                                if label != pos_label and label != "<UNKNOWN>":
                                    neg_label = label
                                    break
                            
                            if neg_label:
                                # Swap probabilities: negative gets higher prob, positive gets lower
                                neg_prob = probs_dict[neg_label]
                                result_dict = {
                                    pos_label: pos_prob,
                                    neg_label: neg_prob
                                }
                                # Normalize to sum to 1 (excluding <UNKNOWN> if present)
                                if "<UNKNOWN>" in probs_dict:
                                    result_dict["<UNKNOWN>"] = probs_dict["<UNKNOWN>"]
                                    total = sum(v for k, v in result_dict.items() if k != "<UNKNOWN>")
                                    if total > 0:
                                        result_dict = {k: (v / total if k != "<UNKNOWN>" else v) for k, v in result_dict.items()}
                            else:
                                # Fallback: couldn't find negative class, use original probs
                                result_dict = probs_dict
                    else:
                        # Couldn't find positive class label, fallback to argmax
                        logger.debug(f"⚠️  Optimal threshold available ({self.optimal_threshold:.4f}) but couldn't find pos_label. Using argmax.")
                        result_dict = probs_dict
                else:
                    # DEFAULT: Use argmax (original behavior for multi-class or when threshold not available)
                    result_dict = probs_dict
                
                if ignore_unknown:
                    # Use None to avoid throwing an exception in case <UNKNOWN> is not in the result set.
                    result_dict.pop("<UNKNOWN>", None)
                    # Rebalance the probabilities of remaining keys to sum to 1.
                    # An alternative would be to leave the probabilities as-is, but
                    # the fact that they don't sum to 1 could be confusing to the user.
                    prob_total = sum(result_dict.values())
                    if prob_total > 0:
                        result_dict = {k: v / prob_total for k, v in result_dict.items()}
            elif isinstance(self.target_codec, ScalarCodec):
                theValue = self.target_codec.detokenize(
                    Token(value=out[0].item(), status=TokenStatus.OK)
                )
                result_dict = {self.target_col_name: theValue}
            else:
                assert False, "Unknown target codec: %s" % self.target_codec

        # Build calibration metadata
        calibration_meta = None
        if self.calibration_metrics is not None:
            # Map internal method names to user-facing names
            method_map = {
                'temperature': 'temperature_scaling',
                'platt': 'platt',
                'isotonic': 'isotonic',
                'none': None
            }
            method_name = method_map.get(self.calibration_method, None)
            
            # Always include calibration metadata if we have candidate scores
            candidate_scores = self.calibration_metrics.get('candidate_scores', {})
            if candidate_scores:
                calibration_meta = {
                    "method": method_name if method_name else None,
                    "params": {},
                    "candidate_scores": {}
                }
                
                # Add method-specific parameters
                if self.calibration_method == 'temperature' and self.calibration_temperature is not None:
                    calibration_meta["params"]["T"] = float(self.calibration_temperature)
                
                # Add candidate scores (NLL for each method)
                for method_key, scores in candidate_scores.items():
                    if 'nll' in scores:
                        calibration_meta["candidate_scores"][method_key] = {
                            "nll": float(scores['nll'])
                        }
        
        if extended_result:
            import copy
            import socket
            from datetime import datetime
            
            original_query = copy.copy(input_dict)
            actual_query = {}
            ignored_query_columns = []
            available_query_columns = list(self.all_codecs.keys())
            # codec_keys = list(self.all_codecs.keys())
            for k, v in original_query.items():
                if k in available_query_columns:
                    actual_query[k] = v
                else:
                    ignored_query_columns.append(k)
            
            result = {
                "_meta": {
                    "compute_cluster": socket.gethostname(),
                    "compute_cluster_time": datetime.utcnow().isoformat() + "Z",
                    "model_warnings": self.get_model_warnings(include_epoch_details=False) if self.has_warnings() else None,
                    "training_quality_warning": self.get_training_quality_warning(),
                },
                "original_query": original_query,
                "actual_query": actual_query,
                "ignored_query_columns": ignored_query_columns,
                "available_query_columns": available_query_columns,
                "results": result_dict,
            }
            
            # Add calibration metadata if available
            if calibration_meta:
                result["calibration"] = calibration_meta
            
            return result
        else:
            # Simple result - include calibration if available
            if calibration_meta:
                return {
                    **result_dict,
                    "calibration": calibration_meta
                }
            else:
                return result_dict

    def predict_batch(self, records_list: List[Dict], batch_size: int = 256, debug_print: bool = False, extended_result: bool = False, progress_callback = None):
        """
        Predict on a batch of records efficiently using GPU batching.
        
        Args:
            records_list: List of dictionaries to predict on
            batch_size: Number of records to process in each GPU batch
            debug_print: Whether to print debug info
            extended_result: Whether to return extended metadata including guardrails
            progress_callback: Optional callback function(current, total, message) for progress updates
            
        Returns:
            List of prediction results (same order as input)
        """
        if not records_list:
            return []
            
        if self.target_codec is None:
            raise Exception("Cannot predict before the predictor is trained.")
        
        # Check for target column in any record
        for record in records_list:
            if record.get(self.target_col_name) is not None:
                raise RuntimeError("Query input contains the target column of the model")
        
        all_predictions = []
        
        # Run guardrails analysis on all records if extended_result is requested
        guardrails_results = None
        if extended_result:
            from featrix.neural.guardrails import RunGuardrails
            guardrails_results = RunGuardrails(records_list, self, issues_only=False)
        
        with PredictorEvalModeContextManager(fsp=self, debugLabel="predict_batch"):
            # Process records in batches for GPU efficiency
            total_batches = (len(records_list) + batch_size - 1) // batch_size
            for batch_idx, batch_start in enumerate(range(0, len(records_list), batch_size)):
                batch_end = min(batch_start + batch_size, len(records_list))
                batch_records = records_list[batch_start:batch_end]
                
                if debug_print:
                    logger.info(f"Processing batch {batch_start}-{batch_end} ({len(batch_records)} records)")
                
                # Report progress if callback provided
                if progress_callback:
                    progress_callback(batch_idx, total_batches, f"Processing batch {batch_idx + 1}/{total_batches} ({batch_end}/{len(records_list)} records)")
                
                # Convert records to DataFrame for batching
                batch_df = pd.DataFrame(batch_records)
                
                # Create dataset and dataloader for efficient batching
                dataset = SuperSimpleSelfSupervisedDataset(batch_df, self.all_codecs)
                dataloader = DataLoader(
                    dataset,
                    batch_size=len(batch_df),  # Process entire batch at once
                    shuffle=False,
                    collate_fn=collate_tokens,
                )
                
                # Get the single batch
                column_batch = next(iter(dataloader))
                
                # Move to device
                for tokenbatch in column_batch.values():
                    tokenbatch.to(device)
                
                # Remove target column if present (for marginal encoding)
                if self.target_col_name in column_batch:
                    target_token_batch = column_batch.pop(self.target_col_name)
                    
                    # Add marginal tokens if target was in original embedding space
                    if self.target_col_name in self.embedding_space.col_codecs:
                        marginal_token_batch = self._create_marginal_token_batch_for_target(target_token_batch)
                        column_batch[self.target_col_name] = marginal_token_batch
                
                # Encode the entire batch at once - MASSIVE SPEEDUP!
                _, batch_encoding = self.embedding_space.encoder.encode(column_batch, apply_noise=False)
                
                # CRITICAL: Move batch_encoding to same device as predictor to avoid tensor device mismatch
                predictor_device = next(self.predictor.parameters()).device
                batch_encoding = batch_encoding.to(predictor_device)
                
                # Run predictor on entire batch
                batch_output = self.predictor(batch_encoding)
                
                # Convert batch output to individual predictions
                predictions = []
                for i, record in enumerate(batch_records):
                    single_output = batch_output[i:i+1]  # Keep batch dimension
                    prediction = self._convert_output_to_prediction(single_output)
                    
                    if extended_result:
                        # Add extended metadata for this record
                        import copy
                        original_query = copy.copy(record)
                        actual_query = {}
                        ignored_query_columns = []
                        available_query_columns = list(self.all_codecs.keys())
                        
                        for k, v in original_query.items():
                            if k in available_query_columns:
                                actual_query[k] = v
                            else:
                                ignored_query_columns.append(k)
                        
                        extended_prediction = {
                            "original_query": original_query,
                            "actual_query": actual_query,
                            "ignored_query_columns": ignored_query_columns,
                            "available_query_columns": available_query_columns,
                            "results": prediction,
                            "guardrails": guardrails_results,  # Guardrails for all records (could be optimized per record)
                            "model_warnings": self.get_model_warnings(include_epoch_details=False) if self.has_warnings() else None,
                        }
                        predictions.append(extended_prediction)
                    else:
                        predictions.append(prediction)
                
                all_predictions.extend(predictions)
        
        return all_predictions
    
    def _convert_output_to_prediction(self, model_output):
        """
        Convert raw model output to prediction dictionary.
        """
        if isinstance(self.target_codec, SetCodec):
            # Classification: convert to probabilities
            probs = self.sm(model_output).squeeze(dim=0)
            probs_dict = {
                self.target_codec.detokenize(Token(value=i, status=TokenStatus.OK)): prob.item()
                for i, prob in enumerate(probs)
            }
            return probs_dict
            
        elif isinstance(self.target_codec, ScalarCodec):
            # Regression: extract scalar value
            value = self.target_codec.detokenize(
                Token(value=model_output[0].item(), status=TokenStatus.OK)
            )
            return {self.target_col_name: value}
        else:
            raise ValueError(f"Unknown target codec: {self.target_codec}")

    def get_accuracy(self, test_df):
        # compute accuracy on the specified df
        # (which should be different from the train df)
        pass
    
    def _create_model_card_json(self, best_epoch_idx=None, metadata=None):
        """
        Create comprehensive model card JSON for single predictor.
        
        Similar format to EmbeddingSpace model card but focused on classification/regression metrics.
        """
        import socket
        from datetime import datetime
        
        # Determine best epoch if not provided
        if best_epoch_idx is None:
            # Find best epoch from training_info (lowest validation loss)
            best_epoch_idx = 0
            best_val_loss = float('inf')
            if hasattr(self, 'training_info') and self.training_info:
                for i, entry in enumerate(self.training_info):
                    val_loss = entry.get('validation_loss')
                    if val_loss and val_loss < best_val_loss:
                        best_val_loss = val_loss
                        best_epoch_idx = entry.get('epoch_idx', i)
        
        # Get best epoch metrics
        best_epoch_metrics = {}
        if hasattr(self, 'training_info') and self.training_info:
            for entry in self.training_info:
                if entry.get('epoch_idx') == best_epoch_idx:
                    best_epoch_metrics = entry.get('metrics', {})
                    break
        
        # Get training dataset info
        train_rows = len(self.train_df) if hasattr(self, 'train_df') and self.train_df is not None else 0
        val_rows = 0
        if hasattr(self, 'training_info') and self.training_info:
            # Try to get validation rows from first entry
            first_entry = self.training_info[0] if self.training_info else {}
            val_rows = first_entry.get('val_rows', 0)
        
        # Get feature columns (all codecs except target)
        feature_columns = []
        if hasattr(self, 'all_codecs'):
            feature_columns = [col for col in self.all_codecs.keys() if col != self.target_col_name]
        
        # Get optimal threshold info
        optimal_threshold_info = {}
        if hasattr(self, 'optimal_threshold') and self.optimal_threshold is not None:
            optimal_threshold_info = {
                "optimal_threshold": self.optimal_threshold,
                "pos_label": getattr(self, '_pos_label', None),
            }
            if hasattr(self, 'optimal_threshold_history') and self.optimal_threshold_history:
                last_entry = self.optimal_threshold_history[-1]
                optimal_threshold_info.update({
                    "optimal_threshold_f1": last_entry.get('f1_score'),
                    "accuracy_at_optimal_threshold": last_entry.get('accuracy_at_optimal'),
                })
        
        # Get model architecture info
        predictor_param_count = 0
        predictor_layer_count = 0
        if hasattr(self, 'predictor') and self.predictor is not None:
            predictor_param_count = sum(p.numel() for p in self.predictor.parameters())
            for name, module in self.predictor.named_modules():
                if len(list(module.children())) == 0:
                    predictor_layer_count += 1
        
        # Get version info
        version_string = "unknown"
        try:
            from config import config
            version_string = config.get('version', 'unknown')
        except:
            pass
        
        model_card = {
            "model_identification": {
                "session_id": getattr(self, 'session_id', None),
                "job_id": getattr(self, 'job_id', None),
                "name": getattr(self, 'name', None),
                "target_column": self.target_col_name if hasattr(self, 'target_col_name') else None,
                "target_column_type": self.target_col_type if hasattr(self, 'target_col_type') else None,
                "compute_cluster": socket.gethostname().split('.')[0].upper(),
                "training_date": datetime.now().strftime('%Y-%m-%d'),
                "status": "DONE",
                "model_type": "Single Predictor",
                "framework": f"FeatrixSphere {version_string}"
            },
            
            "training_dataset": {
                "train_rows": train_rows,
                "val_rows": val_rows,
                "total_rows": train_rows + val_rows,
                "total_features": len(feature_columns),
                "feature_names": feature_columns,
                "target_column": self.target_col_name if hasattr(self, 'target_col_name') else None,
            },
            
            "training_configuration": {
                "epochs_total": len(self.training_info) if hasattr(self, 'training_info') and self.training_info else 0,
                "best_epoch": best_epoch_idx,
                "d_model": self.d_model if hasattr(self, 'd_model') else None,
                "batch_size": self.training_info[0].get('batch_size') if hasattr(self, 'training_info') and self.training_info else None,
                "learning_rate": self.training_info[0].get('lr') if hasattr(self, 'training_info') and self.training_info else None,
                "optimizer": "Adam",  # Default, could extract from training_info
            },
            
            "training_metrics": {
                "best_epoch": {
                    "epoch": best_epoch_idx,
                    "validation_loss": self.training_info[best_epoch_idx].get('validation_loss') if hasattr(self, 'training_info') and best_epoch_idx < len(self.training_info) else None,
                    "train_loss": self.training_info[best_epoch_idx].get('loss') if hasattr(self, 'training_info') and best_epoch_idx < len(self.training_info) else None,
                },
                "classification_metrics": {
                    "accuracy": best_epoch_metrics.get('accuracy'),
                    "precision": best_epoch_metrics.get('precision'),
                    "recall": best_epoch_metrics.get('recall'),
                    "f1": best_epoch_metrics.get('f1'),
                    "auc": best_epoch_metrics.get('auc'),
                    "is_binary": best_epoch_metrics.get('is_binary', False),
                },
                "optimal_threshold": optimal_threshold_info,
                "argmax_metrics": {
                    "accuracy": best_epoch_metrics.get('argmax_accuracy'),
                    "precision": best_epoch_metrics.get('argmax_precision'),
                    "recall": best_epoch_metrics.get('argmax_recall'),
                    "f1": best_epoch_metrics.get('argmax_f1'),
                } if best_epoch_metrics.get('argmax_accuracy') is not None else None,
            },
            
            "model_architecture": {
                "predictor_layers": predictor_layer_count,
                "predictor_parameters": predictor_param_count,
                "embedding_space_d_model": self.d_model if hasattr(self, 'd_model') else None,
            },
            
            "model_quality": {
                "warnings": self.best_epoch_warnings if hasattr(self, 'best_epoch_warnings') else [],
                "training_quality_warning": self.get_training_quality_warning() if hasattr(self, 'get_training_quality_warning') else None,
            },
            
            "technical_details": {
                "pytorch_version": torch.__version__ if torch else "unknown",
                "device": "GPU" if torch.cuda.is_available() else "CPU",
                "precision": "float32",
                "loss_function": "CrossEntropyLoss" if self.target_col_type == "set" else "MSELoss",
            },
            
            "provenance": {
                "created_at": datetime.now().isoformat(),
                "training_duration_minutes": self.training_info[-1].get('duration_minutes') if hasattr(self, 'training_info') and self.training_info else None,
            }
        }
        
        return model_card
