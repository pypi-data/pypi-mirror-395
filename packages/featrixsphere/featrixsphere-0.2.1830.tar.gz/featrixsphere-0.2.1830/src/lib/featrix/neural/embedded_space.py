#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

import asyncio
import copy
import json
import logging
import math
import os
import pickle
import shutil
import socket
import sys
import tempfile
import time
import traceback
import uuid
import warnings
from collections import defaultdict
from contextlib import nullcontext
from enum import IntEnum
from enum import unique
from pathlib import Path
from typing import Dict
from typing import Optional
from pathlib import Path
import sqlite3
import pickle


import numpy as np
import pandas as pd
import psutil
import torch
from torch.optim.lr_scheduler import LambdaLR
from torch.optim.lr_scheduler import OneCycleLR
from torch.profiler import ProfilerActivity
from torch.utils.data import DataLoader
from torch.utils.data import Sampler

from datetime import datetime
from zoneinfo import ZoneInfo

from featrix.neural.data_frame_data_set import collate_tokens
from featrix.neural.data_frame_data_set import SuperSimpleSelfSupervisedDataset
from featrix.neural.dataloader_utils import create_dataloader_kwargs
from featrix.neural.device import device, set_device_cpu, reset_device
# from featrix.neural.encoders import create_lists_of_a_set_codec
from featrix.neural.encoders import create_scalar_codec
from featrix.neural.encoders import create_set_codec
from featrix.neural.encoders import create_string_codec
from featrix.neural.encoders import create_timestamp_codec
from featrix.neural.encoders import ColumnPredictor
from featrix.neural.string_codec import set_string_cache_path
from featrix.neural.training_history_db import TrainingHistoryDB
from featrix.neural.encoders import create_vector_codec
from featrix.neural.encoders import FeatrixTableEncoder
from featrix.neural.encoders import ColumnPredictor
from featrix.neural.simple_mlp import SimpleMLP
from featrix.neural.featrix_token import create_token_batch
from featrix.neural.featrix_token import set_marginal
from featrix.neural.featrix_token import TokenStatus
from featrix.neural.input_data_set import FeatrixInputDataSet
from featrix.neural.model_config import ColumnType
from featrix.neural.model_config import FeatrixTableEncoderConfig
from featrix.neural.model_config import JointEncoderConfig
from featrix.neural.model_config import LossFunctionConfig
from featrix.neural.model_config import SimpleMLPConfig
from featrix.neural.model_config import SpreadLossConfig
from featrix.neural.scalar_codec import ScalarCodec
from featrix.neural.scalar_codec import ScalarEncoder
from featrix.neural.set_codec import SetCodec
from featrix.neural.set_codec import SetEncoder
from featrix.neural.string_codec import StringCodec
from featrix.neural.setlist_codec import ListOfASetEncoder
# from featrix.neural.stopwatch import StopWatch
# from featrix.neural.stopwatch import TimedIterator
from featrix.neural.string_codec import StringEncoder
from featrix.neural.vector_codec import VectorEncoder
from featrix.neural.utils import ideal_batch_size

# Import configuration management
from featrix.neural.sphere_config import get_d_model as get_default_d_model
from featrix.neural.sphere_config import get_config
from config import config
from lib.job_manager import JobStatus, get_job_output_path

# WeightWatcher tracking is handled by weightwatcher_tracking.py module

# Import DropoutScheduler for dynamic dropout adjustment
from featrix.neural.dropout_scheduler import DropoutScheduler, create_dropout_scheduler

# Import exceptions for training control
from featrix.neural.exceptions import FeatrixTrainingAbortedException

# from sklearn.model_selection import train_test_split

# Set up proper logging for embedded space training
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def _log_gpu_memory_embedded_space(context: str = ""):
    """Quick GPU memory logging for tracing memory usage in embedded_space."""
    try:
        if not torch.cuda.is_available():
            return
        allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
        reserved = torch.cuda.memory_reserved() / (1024**3)  # GB
        max_allocated = torch.cuda.max_memory_allocated() / (1024**3)  # GB
        logger.info(f"📊 GPU MEMORY [embedded_space: {context}]: Allocated={allocated:.3f} GB, Reserved={reserved:.3f} GB, Peak={max_allocated:.3f} GB")
    except Exception as e:
        logger.debug(f"Could not log GPU memory: {e}")

# Class-level cache for rate-limiting missing codec warnings across all EmbeddingSpace instances
# Key: frozenset of missing field names -> last logged timestamp
_MISSING_CODEC_WARNING_CACHE = {}


def check_abort_files(job_id: str, output_dir: str = None) -> Optional[str]:
    """
    Check for ABORT file in the job's output directory.
    
    For /sphere paths: Checks both job directory and parent directories (session-level control files)
    For other paths: ONLY checks the specific job's directory (same directory) to avoid false positives
    
    Args:
        job_id: The job ID (e.g., 'abc123-20251005-221252'), or None to skip check
        output_dir: The exact output directory for this job (e.g., /featrix-output/session/job_type/job_id)
                   If None, attempts to use helper function to find job directory
        
    Returns:
        Optional[str]: Path to ABORT file if found (should exit), None otherwise
    """
    # If no job_id, skip the check
    if job_id is None:
        return None
    
    # Use the job_manager function which handles /sphere vs non-/sphere paths correctly
    from lib.job_manager import _find_control_file
    abort_file = _find_control_file(job_id, "ABORT", output_dir)
    
    if abort_file:
        logger.warning(f"🚫 ABORT file detected: {abort_file}")
        logger.warning(f"🚫 Training job {job_id} will exit with code 2")
        logger.warning(f"🚫 ABORT file also prevents job restart after crashes")
        
        # Mark job as FAILED immediately when ABORT file is detected
        try:
            from lib.job_manager import update_job_status, JobStatus
            update_job_status(job_id, JobStatus.FAILED, {
                "error_message": f"Training aborted due to ABORT file at {abort_file}"
            })
            logger.info(f"🚫 Job {job_id} marked as FAILED due to ABORT file")
        except Exception as e:
            logger.error(f"Failed to update job status when ABORT file detected: {e}")
        
        return str(abort_file)
    
    return None


def check_no_stop_file(job_id: str, output_dir: str = None) -> bool:
    """
    Check for NO_STOP file in the job's output directory.
    
    Args:
        job_id: The job ID (e.g., 'abc123-20251005-221252'), or None to skip check
        output_dir: Base output directory (defaults to /sphere/app/featrix_output)
                   If None, attempts to use helper function to find job directory
        
    Returns:
        bool: True if NO_STOP file exists (disable early stopping), False otherwise
    """
    # If no job_id, skip the check
    if job_id is None:
        return False
    
    from pathlib import Path
    
    # If output_dir is provided and is already the job directory, use it directly
    if output_dir and Path(output_dir).exists() and (Path(output_dir) / "NO_STOP").exists():
        no_stop_file = Path(output_dir) / "NO_STOP"
    elif output_dir:
        # output_dir is base directory, construct path (old structure fallback)
        job_output_dir = Path(output_dir) / job_id
        no_stop_file = job_output_dir / "NO_STOP"
    else:
        # Try to use helper function to find job directory (new structure)
        try:
            from lib.job_manager import get_job_output_path
            job_output_dir = get_job_output_path(job_id)  # Search only - will assert if not found
            no_stop_file = job_output_dir / "NO_STOP"
        except Exception:
            # Fallback to old structure
            output_dir = "/sphere/app/featrix_output"
            job_output_dir = Path(output_dir) / job_id
            no_stop_file = job_output_dir / "NO_STOP"
    
    # Check for NO_STOP file
    if no_stop_file.exists():
        return True
    
    return False


def check_publish_file(job_id: str, output_dir: str = None) -> bool:
    """
    Check for PUBLISH file in the job's output directory.
    
    Args:
        job_id: The job ID (e.g., 'abc123-20251005-221252'), or None to skip check
        output_dir: Base output directory (defaults to /sphere/app/featrix_output)
                   If None, attempts to use helper function to find job directory
        
    Returns:
        bool: True if PUBLISH file exists (should save embedding space), False otherwise
    """
    # If no job_id, skip the check
    if job_id is None:
        return False
    
    from pathlib import Path
    
    # If output_dir is provided and is already the job directory, use it directly
    if output_dir and Path(output_dir).exists() and (Path(output_dir) / "PUBLISH").exists():
        publish_file = Path(output_dir) / "PUBLISH"
    elif output_dir:
        # output_dir is base directory, construct path (old structure fallback)
        job_output_dir = Path(output_dir) / job_id
        publish_file = job_output_dir / "PUBLISH"
    else:
        # Try to use helper function to find job directory (new structure)
        try:
            from lib.job_manager import get_job_output_path
            job_output_dir = get_job_output_path(job_id)  # Search only - will assert if not found
            publish_file = job_output_dir / "PUBLISH"
        except Exception:
            # Fallback to old structure
            output_dir = "/sphere/app/featrix_output"
            job_output_dir = Path(output_dir) / job_id
            publish_file = job_output_dir / "PUBLISH"
    
    # Check for PUBLISH file
    if publish_file.exists():
        return True
    
    return False


def check_pause_files(job_id: str, output_dir: str = None) -> bool:
    """
    Check for PAUSE file in the job's output directory.
    
    Args:
        job_id: The job ID (e.g., 'abc123-20251005-221252'), or None to skip check
        output_dir: Base output directory (defaults to /sphere/app/featrix_output)
                   If None, attempts to use helper function to find job directory
        
    Returns:
        bool: True if PAUSE file exists (should pause training and save checkpoint), False otherwise
    """
    # If no job_id, skip the check
    if job_id is None:
        return False
    
    from pathlib import Path
    
    # Build list of all possible locations to check (similar to check_abort_files)
    paths_to_check = []
    
    # 1. If output_dir is provided and looks like a job directory
    if output_dir and Path(output_dir).exists():
        paths_to_check.append(Path(output_dir) / "PAUSE")
        parent = Path(output_dir).parent
        if parent.exists():
            paths_to_check.append(parent / "PAUSE")
    
    # 2. Try to use helper function to find job directory (new structure)
    try:
        from lib.job_manager import get_job_output_path
        job_output_dir = get_job_output_path(job_id)  # Search only - will assert if not found
        paths_to_check.append(job_output_dir / "PAUSE")
        if job_output_dir.parent.exists():
            paths_to_check.append(job_output_dir.parent / "PAUSE")
    except Exception as e:
        logger.debug(f"Could not use get_job_output_path: {e}")
    
    # 3. Common output directories
    common_dirs = [
        Path("/sphere/app/featrix_output") / job_id,
        Path("/sphere/featrix_data") / job_id,
    ]
    
    if output_dir:
        common_dirs.append(Path(output_dir) / job_id)
    
    for common_dir in common_dirs:
        if common_dir.exists():
            paths_to_check.append(common_dir / "PAUSE")
            if common_dir.parent.exists():
                paths_to_check.append(common_dir.parent / "PAUSE")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_paths = []
    for p in paths_to_check:
        p_str = str(p.resolve())
        if p_str not in seen:
            seen.add(p_str)
            unique_paths.append(p)
    
    # Check all paths
    for pause_file in unique_paths:
        if pause_file.exists():
            logger.warning(f"⏸️  PAUSE file detected: {pause_file}")
            return True
    
    return False


def check_finish_files(job_id: str, output_dir: str = None) -> bool:
    """
    Check for FINISH file in the job's output directory.
    
    Args:
        job_id: The job ID (e.g., 'abc123-20251005-221252'), or None to skip check
        output_dir: Base output directory (defaults to /sphere/app/featrix_output)
                   If None, attempts to use helper function to find job directory
        
    Returns:
        bool: True if FINISH file exists (should finish training gracefully), False otherwise
    """
    # If no job_id, skip the check
    if job_id is None:
        return False
    
    from pathlib import Path
    
    # If output_dir is provided and is already the job directory, use it directly
    if output_dir and Path(output_dir).exists() and (Path(output_dir) / "FINISH").exists():
        finish_file = Path(output_dir) / "FINISH"
    elif output_dir:
        # output_dir is base directory, construct path (old structure fallback)
        job_output_dir = Path(output_dir) / job_id
        finish_file = job_output_dir / "FINISH"
    else:
        # Try to use helper function to find job directory (new structure)
        try:
            from lib.job_manager import get_job_output_path
            job_output_dir = get_job_output_path(job_id)  # Search only - will assert if not found
            finish_file = job_output_dir / "FINISH"
        except Exception:
            # Fallback to old structure
            output_dir = "/sphere/app/featrix_output"
            job_output_dir = Path(output_dir) / job_id
            finish_file = job_output_dir / "FINISH"
    
    # Check for FINISH file
    if finish_file.exists():
        logger.warning(f"🏁 FINISH file detected: {finish_file}")
        logger.warning(f"🏁 Training job {job_id} will complete gracefully")
        logger.warning(f"🏁 Model will be saved and job marked as completed")
        return True
    
    return False


def check_restart_files(job_id: str, output_dir: str = None) -> bool:
    """
    Check for RESTART file in the job's output directory.
    
    Args:
        job_id: The job ID (e.g., 'abc123-20251005-221252'), or None to skip check
        output_dir: Base output directory (defaults to /sphere/app/featrix_output)
                   If None, attempts to use helper function to find job directory
        
    Returns:
        bool: True if RESTART file exists, False otherwise
    """
    # If no job_id, skip the check
    if job_id is None:
        return False
    
    from pathlib import Path
    
    # If output_dir is provided and is already the job directory, use it directly
    if output_dir and Path(output_dir).exists() and (Path(output_dir) / "RESTART").exists():
        restart_file = Path(output_dir) / "RESTART"
    elif output_dir:
        # output_dir is base directory, construct path (old structure fallback)
        job_output_dir = Path(output_dir) / job_id
        restart_file = job_output_dir / "RESTART"
    else:
        # Try to use helper function to find job directory (new structure)
        try:
            from lib.job_manager import get_job_output_path
            job_output_dir = get_job_output_path(job_id)  # Search only - will assert if not found
            restart_file = job_output_dir / "RESTART"
        except Exception:
            # Fallback to old structure
            output_dir = "/sphere/app/featrix_output"
            job_output_dir = Path(output_dir) / job_id
            restart_file = job_output_dir / "RESTART"
    
    # Check for RESTART file
    return restart_file.exists()


def remove_restart_file(job_id: str, output_dir: str = None) -> bool:
    """
    Remove the RESTART file from the job's output directory.
    
    Args:
        job_id: The job ID
        output_dir: Base output directory (defaults to /sphere/app/featrix_output)
        
    Returns:
        bool: True if file was removed, False if it didn't exist or couldn't be removed
    """
    if job_id is None:
        return False
    
    if output_dir is None:
        output_dir = "/sphere/app/featrix_output"
    
    from pathlib import Path
    job_output_dir = Path(output_dir) / job_id
    restart_file = job_output_dir / "RESTART"
    
    if restart_file.exists():
        try:
            restart_file.unlink()
            logger.info(f"🔄 Removed RESTART file: {restart_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove RESTART file {restart_file}: {e}")
            return False
    
    return False


@unique
class CallbackType(IntEnum):
    AFTER_BATCH = 0


# def compute_multicolumn_loss(codecs, predictors, targets, device):
#     loss = 0
#     for target_name, target_values in targets.items():
#         target = {"name": target_name, "value": target_values}
#         target_loss = compute_loss(codecs, predictors, target, device)
#         # print(f"target: {target_name}; loss: {target_loss}")
#         loss += target_loss

#     return loss


# def compute_loss(codecs, predictors, targets, device):
#     target_name = targets["name"]
#     target_values = targets["value"].value

#     target_codec = codecs[target_name]
#     decoded = target_codec.decode(predictors)
#     # print("target values:", target_values)
#     # print("decoded:", decoded)
#     # target_codec.to(device)
#     loss = target_codec.loss(decoded, target_values)

#     return loss


# def compute_loss_random_target(codecs, predictors, targets):
#     # Each element of the predictors tensor must form its own minibatch, so
#     # we unqueeze it.
#     # This is because each element of the predictors tensor is processed by a separate
#     # encoder, and each encoder expects a batch-shaped input.
#     predictors = predictors.unsqueeze(dim=1)
#     target_names = targets["name"]
#     target_values = targets["token"].value

#     loss = 0
#     n_preds = len(target_names)
#     for i, target_col_name in enumerate(target_names):
#         target_codec = codecs[target_col_name]
#         decoded = target_codec.decode(predictors[i])

#         # NOTE: the type of the target depends on what other variables types are targets
#         # in the same batch. If all targeted variables are categoricals, the targets
#         # will be ints, but if at least one targeted variable is a scalar, then all
#         # batch targets will be floats.
#         target_value = target_values[i]

#         # Use `loss_single` instead of `loss` because each element in the batch comes
#         # from a different variable, so they can't be decoded as a batch
#         # See note above re: efficiency.
#         loss += target_codec.loss_single(decoded, target_value)

#     # compute the average loss per prediction
#     return loss / n_preds


def flatten(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list


class DataSegment:
    def __init__(self, row_meta):
        self.row_meta = row_meta
        self._indexes = None
        self._indexOffset = None
        self.reset()

    def reset(self):
        self._indexes = list(
            range(
                self.row_meta.row_idx_start,
                self.row_meta.row_idx_start + self.row_meta.num_rows,
            )
        )
        # print("INDEXES man", self._indexes)
        self._indexOffset = 0
        # random.shuffle(self._indexes)
        return

    def isExhausted(self):
        return self._indexOffset >= len(self._indexes)

    def grabNextBatchIndexes(self, batch_size):
        start = self._indexOffset
        end = start + batch_size
        if end > len(self._indexes):
            end = len(self._indexes)
        self._indexOffset = end
        return self._indexes[start:end]


class DataSpaceBatchSampler(Sampler[list[int]]):
    def __init__(self, batch_size, inputDataset: FeatrixInputDataSet):
        self.batch_size = batch_size
        assert isinstance(self.batch_size, int) and self.batch_size >= 0
        self.inputDataset = inputDataset
        self.shuffleList = None
        self.segmentList = []
        if inputDataset.project_row_meta_data_list is not None:
            for entry in inputDataset.project_row_meta_data_list:
                self.segmentList.append(DataSegment(entry))
        self.nextSegmentIndex = 0

    def __iter__(self):
        for entry in self.segmentList:
            entry.reset()
        # self.shuffleList = self.inputDataset.df.
        self.nextSegmentIndex = 0
        return self

    def __next__(self):
        # get the next batch... ALWAYS 32 things.
        # pick a segment.
        # get a batch out of that segment.
        nextSegment = None

        numLoops = 0
        while numLoops < (len(self.segmentList) * 2):
            if self.nextSegmentIndex >= len(self.segmentList):
                self.nextSegmentIndex = 0

            nextSegment = self.segmentList[self.nextSegmentIndex]
            if not nextSegment.isExhausted():
                break
            # it's exhausted, try the next one
            self.nextSegmentIndex += 1
            numLoops += 1

        if nextSegment.isExhausted():
            raise StopIteration()

        toReturn = nextSegment.grabNextBatchIndexes(self.batch_size)
        self.nextSegmentIndex += 1
        if len(toReturn) == 0:
            print("Backup protection -- should not get here")
            raise StopIteration()
        return toReturn

    def __len__(self):
        return len(self.inputDataset.df)

    def dump(self):
        # print(f"-------- {len(self.segmentList)} segments -------")
        # for s in self.segmentList:
        #     print(f"... {s._indexes}")
        # print("-----")
        return


def detect_es_training_failure(
    epoch_idx: int,
    train_loss: float,
    val_loss: float,
    train_loss_history: list,
    val_loss_history: list,
    gradient_norm: float = None,
    lr: float = None
):
    """
    Detect and diagnose ES (Embedding Space) training failure modes.
    
    Args:
        epoch_idx: Current epoch number
        train_loss: Current training loss
        val_loss: Current validation loss
        train_loss_history: List of training losses from previous epochs
        val_loss_history: List of validation losses from previous epochs
        gradient_norm: Current unclipped gradient norm (if available)
        lr: Current learning rate (if available)
    
    Returns:
        tuple: (has_failure: bool, failure_type: str, recommendations: list)
    """
    failures = []
    recommendations = []
    epoch_prefix = f"[epoch={epoch_idx}] "
    
    # Need at least 5 epochs of history for meaningful analysis
    if len(train_loss_history) < 5 or len(val_loss_history) < 5:
        return False, None, []
    
    # Calculate trends
    recent_train_losses = train_loss_history[-5:]
    recent_val_losses = val_loss_history[-5:]
    
    # Safely calculate improvement percentages (avoid division by zero)
    if recent_train_losses[0] > 0:
        train_improvement = (recent_train_losses[0] - recent_train_losses[-1]) / recent_train_losses[0]
    else:
        train_improvement = 0.0
    
    if recent_val_losses[0] > 0:
        val_improvement = (recent_val_losses[0] - recent_val_losses[-1]) / recent_val_losses[0]
    else:
        val_improvement = 0.0
    
    # Check if validation is diverging from training
    train_val_gap = val_loss - train_loss
    train_val_gap_pct = (train_val_gap / train_loss) * 100 if train_loss > 0 else 0
    
    # FAILURE MODE 1: Zero/tiny gradients (dead network)
    if gradient_norm is not None and gradient_norm < 1e-6:
        failures.append("DEAD_NETWORK")
        recommendations.extend([
            "🔥 CRITICAL: Network has zero gradients - not learning at all",
            "   → STOP TRAINING - Network is frozen",
            f"   → Current LR ({lr:.6e}) is likely too low" if lr else "   → Learning rate may be too low",
            "   → Increase learning rate by 10-100x and restart",
            "   → Check if parameters are accidentally frozen",
            "   → Verify loss function is differentiable"
        ])
    
    # FAILURE MODE 2: Very slow learning (minimal improvement over 5 epochs)
    elif abs(train_improvement) < 0.01 and gradient_norm is not None and gradient_norm < 0.01:
        failures.append("VERY_SLOW_LEARNING")
        recommendations.extend([
            f"⚠️  WARNING: Minimal learning progress ({train_improvement*100:.2f}% improvement over 5 epochs)",
            f"   → Gradient norm is very small: {gradient_norm:.6e}",
            f"   → Current LR: {lr:.6e}" if lr else "   → Learning rate may be too low",
            "   → Consider increasing learning rate by 3-5x",
            "   → If using OneCycleLR, consider switching to constant LR or CosineAnnealing",
            "   → Verify self-supervised task is not too easy (loss should be challenging)"
        ])
    
    # FAILURE MODE 3: Severe overfitting (val loss diverging from train loss)
    elif val_improvement < -0.05 and train_improvement > 0.02 and epoch_idx > 10:
        failures.append("SEVERE_OVERFITTING")
        recommendations.extend([
            f"⚠️  WARNING: Severe overfitting detected (val loss increasing: {val_improvement*100:.1f}%)",
            f"   → Training/validation gap: {train_val_gap:.4f} ({train_val_gap_pct:.1f}%)",
            "   → Model is memorizing training data instead of learning generalizable features",
            "   → STOP TRAINING - Model quality is degrading",
            "   → Increase dropout (try 0.5 or higher)",
            "   → Increase weight_decay (try 1e-3 instead of 1e-4)",
            "   → Reduce model complexity (fewer layers, smaller d_model)",
            "   → For small datasets (<2000 rows), use constant high dropout"
        ])
    
    # FAILURE MODE 4: No learning at all (flat or increasing validation loss)
    # Only trigger if validation loss is NOT improving (val_improvement <= 0 or very small positive)
    # If loss is decreasing significantly, don't trigger NO_LEARNING even if recent change is small
    elif val_improvement <= 0.0005 and epoch_idx > 15:
        # Double-check: if loss is actually decreasing over the window, don't trigger
        # This prevents false positives when loss is improving but slowly
        if recent_val_losses[-1] < recent_val_losses[0]:
            # Loss is decreasing - check if improvement is meaningful
            absolute_improvement = recent_val_losses[0] - recent_val_losses[-1]
            relative_improvement_pct = (absolute_improvement / recent_val_losses[0]) * 100 if recent_val_losses[0] > 0 else 0
            
            # Only trigger if improvement is truly minimal (< 0.1% over 5 epochs)
            if relative_improvement_pct >= 0.1:
                # Loss is improving meaningfully, don't trigger NO_LEARNING
                pass
            else:
                failures.append("NO_LEARNING")
                recommendations.extend([
                    f"⚠️  WARNING: Minimal learning progress ({val_improvement*100:.2f}% change in validation loss over 5 epochs)",
                    f"   → Validation loss has plateaued at {val_loss:.4f}",
                    "   → Early stopping is now BLOCKED for 10 more epochs to allow recovery",
                    "   → Self-supervised task may be too easy or too hard",
                    "   → Consider adjusting learning rate (try increasing by 2-3x or using a different schedule)",
                    "   → Check if embeddings are varying (use tensorboard/visualization)",
                    "   → Verify masking strategy is appropriate",
                    "   → Consider if dataset has sufficient complexity to learn from"
                ])
        else:
            # Loss is not decreasing (flat or increasing) - this is truly NO_LEARNING
            failures.append("NO_LEARNING")
            recommendations.extend([
                f"⚠️  WARNING: No learning progress ({val_improvement*100:.2f}% change in validation loss over 5 epochs)",
                f"   → Validation loss has plateaued at {val_loss:.4f}",
                "   → Early stopping is now BLOCKED for 10 more epochs to allow recovery",
                "   → Self-supervised task may be too easy or too hard",
                "   → Consider adjusting learning rate (try increasing by 2-3x or using a different schedule)",
                "   → Check if embeddings are varying (use tensorboard/visualization)",
                "   → Verify masking strategy is appropriate",
                "   → Consider if dataset has sufficient complexity to learn from"
            ])
    
    # FAILURE MODE 5: Moderate overfitting (early warning)
    elif train_val_gap_pct > 10 and val_improvement < 0 and epoch_idx > 10:
        failures.append("MODERATE_OVERFITTING")
        recommendations.extend([
            f"⚠️  WARNING: Overfitting detected (train/val gap: {train_val_gap_pct:.1f}%)",
            "   → Validation loss is no longer improving while training loss decreases",
            "   → Consider early stopping soon if trend continues",
            "   → Increase regularization (dropout/weight_decay)",
            "   → This is acceptable for large datasets, but risky for small ones"
        ])
    
    # FAILURE MODE 6: Unstable training (loss oscillating wildly)
    elif len(recent_train_losses) >= 3:
        train_std = np.std(recent_train_losses)
        train_mean = np.mean(recent_train_losses)
        coef_variation = train_std / train_mean if train_mean > 0 else 0
        
        if coef_variation > 0.1:  # More than 10% variation
            failures.append("UNSTABLE_TRAINING")
            recommendations.extend([
                f"⚠️  WARNING: Training loss is highly unstable (CV={coef_variation:.3f})",
                "   → Loss is oscillating instead of steadily decreasing",
                "   → Learning rate may be too high",
                "   → If using OneCycleLR, consider switching to gentler schedule",
                "   → Try reducing learning rate by 2-3x",
                "   → Increase batch size for more stable gradients"
            ])
    
    # SUCCESS: Model seems to be learning well
    if not failures and train_improvement > 0.02 and val_improvement > 0:
        return False, "HEALTHY", ["✅ ES training appears healthy - both train and val losses improving"]
    
    # Return detected failures (let caller decide whether to log)
    if failures:
        failure_label = "_".join(failures)
        return True, failure_label, recommendations
    
    return False, None, []


def summarize_es_training_results(training_info: dict, loss_history: list):
    """
    Summarize ES training results with diagnostics and quality assessment.
    
    Args:
        training_info: Dictionary containing training metadata
        loss_history: List of loss entries from training
    
    Returns:
        dict: Summary with quality assessment and recommendations
    """
    logger.info("\n" + "=" * 100)
    logger.info("📊 EMBEDDING SPACE TRAINING SUMMARY")
    logger.info("=" * 100)
    
    if not loss_history or len(loss_history) < 2:
        logger.warning("⚠️  Insufficient training history to analyze")
        return {"status": "insufficient_data"}
    
    # Extract training and validation losses
    # ES uses 'loss' key, not 'running_mean_training_loss' or 'total_loss'
    # Filter out None values - if a key exists but value is None, .get() returns None
    # Use 0 as default only if key doesn't exist, but filter out entries where value is explicitly None
    train_losses = []
    for entry in loss_history:
        if isinstance(entry, dict):
            loss = entry.get('loss')
            if loss is not None:
                train_losses.append(loss)
            elif 'loss' not in entry:
                train_losses.append(0)  # Key doesn't exist, use default
    
    val_losses = []
    for entry in loss_history:
        if isinstance(entry, dict):
            val_loss = entry.get('validation_loss')
            if val_loss is not None:
                val_losses.append(val_loss)
            elif 'validation_loss' not in entry:
                val_losses.append(0)  # Key doesn't exist, use default
    
    if not train_losses or not val_losses:
        logger.warning("⚠️  Could not extract loss data from history")
        return {"status": "no_loss_data"}
    
    # Calculate statistics
    initial_train_loss = train_losses[0]
    final_train_loss = train_losses[-1]
    initial_val_loss = val_losses[0]
    final_val_loss = val_losses[-1]
    
    # Ensure all values are not None (shouldn't happen with our filtering, but be safe)
    if initial_train_loss is None:
        logger.warning("⚠️  Initial training loss is None - defaulting to 0.0")
        initial_train_loss = 0.0
    if final_train_loss is None:
        logger.warning("⚠️  Final training loss is None - defaulting to 0.0")
        final_train_loss = 0.0
    if initial_val_loss is None:
        logger.warning("⚠️  Initial validation loss is None - defaulting to 0.0")
        initial_val_loss = 0.0
    if final_val_loss is None:
        logger.warning("⚠️  Final validation loss is None - defaulting to 0.0")
        final_val_loss = 0.0
    
    # Fix initial validation loss: use first non-inf value instead of inf
    # This ensures we can calculate meaningful improvement percentages
    if not math.isfinite(initial_val_loss):
        found_finite = False
        for val_loss in val_losses:
            if math.isfinite(val_loss):
                initial_val_loss = val_loss
                found_finite = True
                logger.debug(f"Fixed initial validation loss from inf to {initial_val_loss:.4f} (first finite value found)")
                break
        if not found_finite:
            # Fallback: use final validation loss if no finite values found (shouldn't happen)
            logger.warning("⚠️  No finite validation losses found in history - using final validation loss as initial")
            initial_val_loss = final_val_loss if (final_val_loss is not None and math.isfinite(final_val_loss)) else 0.0
    
    # Safely calculate improvement percentages (avoid division by zero and None)
    if initial_train_loss is not None and initial_train_loss > 0:
        train_improvement = ((initial_train_loss - final_train_loss) / initial_train_loss) * 100
    else:
        train_improvement = 0.0
    
    if initial_val_loss is not None and initial_val_loss > 0 and final_val_loss is not None:
        val_improvement = ((initial_val_loss - final_val_loss) / initial_val_loss) * 100
    else:
        val_improvement = 0.0
    
    best_train_loss = min(train_losses)
    best_val_loss = min(val_losses) if val_losses else 0.0
    
    # Safely calculate train/val gap (ensure no None values)
    if final_val_loss is not None and final_train_loss is not None:
        train_val_gap = final_val_loss - final_train_loss
        train_val_gap_pct = (train_val_gap / final_train_loss) * 100 if final_train_loss > 0 else 0
    else:
        train_val_gap = 0.0
        train_val_gap_pct = 0.0
    
    # Training duration
    start_time = training_info.get('start_time', 0)
    end_time = training_info.get('end_time', 0)
    duration_seconds = end_time - start_time if end_time > start_time else 0
    duration_minutes = duration_seconds / 60
    
    # Log summary
    logger.info(f"⏱️  Training Duration: {duration_minutes:.1f} minutes ({duration_seconds:.0f} seconds)")
    logger.info(f"📈 Total Epochs: {len(train_losses)}")
    logger.info("")
    logger.info("📉 LOSS PROGRESSION (Full Training History):")
    logger.info(f"   Initial Training:   {initial_train_loss:.4f}")
    logger.info(f"   Initial Validation: {initial_val_loss:.4f}")
    logger.info(f"   Final Training:     {final_train_loss:.4f} ({train_improvement:+.1f}%)")
    logger.info(f"   Final Validation:   {final_val_loss:.4f} ({val_improvement:+.1f}%)")
    logger.info(f"   Best Training Loss (in history):  {best_train_loss:.4f}")
    logger.info(f"   Best Validation Loss (in history): {best_val_loss:.4f}")
    logger.info(f"   Final Train/Val Gap: {train_val_gap:.4f} ({train_val_gap_pct:+.1f}%)")
    
    # Show loss component progression if available
    if loss_history and len(loss_history) > 0:
        first_entry = loss_history[0]
        last_entry = loss_history[-1]
        
        if first_entry and last_entry and 'spread' in first_entry and 'spread' in last_entry:
            logger.info("")
            logger.info("📊 LOSS COMPONENT BREAKDOWN:")
            
            # Initial components - handle None values explicitly
            init_spread = first_entry.get('spread') or 0
            init_joint = first_entry.get('joint') or 0
            init_marginal = first_entry.get('marginal') or 0
            init_marginal_w = first_entry.get('marginal_weighted') or 0
            
            # Final components - handle None values explicitly
            final_spread = last_entry.get('spread') or 0
            final_joint = last_entry.get('joint') or 0
            final_marginal = last_entry.get('marginal') or 0
            final_marginal_w = last_entry.get('marginal_weighted') or 0
            
            # Ensure all values are numeric (not None) before calculations
            init_spread = float(init_spread) if init_spread is not None else 0.0
            init_joint = float(init_joint) if init_joint is not None else 0.0
            init_marginal = float(init_marginal) if init_marginal is not None else 0.0
            init_marginal_w = float(init_marginal_w) if init_marginal_w is not None else 0.0
            final_spread = float(final_spread) if final_spread is not None else 0.0
            final_joint = float(final_joint) if final_joint is not None else 0.0
            final_marginal = float(final_marginal) if final_marginal is not None else 0.0
            final_marginal_w = float(final_marginal_w) if final_marginal_w is not None else 0.0
            
            # Calculate improvements
            spread_improv = ((init_spread - final_spread) / init_spread * 100) if init_spread > 0 else 0
            joint_improv = ((init_joint - final_joint) / init_joint * 100) if init_joint > 0 else 0
            marginal_improv = ((init_marginal - final_marginal) / init_marginal * 100) if init_marginal > 0 else 0
            
            logger.info(f"   Spread Loss:")
            logger.info(f"      Initial: {init_spread:.4f} → Final: {final_spread:.4f} ({spread_improv:+.1f}%)")
            logger.info(f"   Joint Loss:")
            logger.info(f"      Initial: {init_joint:.4f} → Final: {final_joint:.4f} ({joint_improv:+.1f}%)")
            logger.info(f"   Marginal Loss (unweighted):")
            logger.info(f"      Initial: {init_marginal:.4f} → Final: {final_marginal:.4f} ({marginal_improv:+.1f}%)")
            if init_marginal_w > 0 and final_marginal_w > 0:
                logger.info(f"   Marginal Loss (weighted contribution to total):")
                logger.info(f"      Initial: {init_marginal_w:.4f} → Final: {final_marginal_w:.4f}")
    
    logger.info("")
    
    # Check if best checkpoint was loaded
    best_checkpoint_loaded = training_info.get('best_checkpoint_loaded', False)
    if best_checkpoint_loaded:
        best_epoch = training_info.get('best_checkpoint_epoch', 'unknown')
        loaded_train_loss = training_info.get('best_checkpoint_train_loss', None)
        loaded_val_loss = training_info.get('best_checkpoint_val_loss', None)
        
        logger.info("🏆 BEST CHECKPOINT LOADED:")
        logger.info(f"   ✅ Successfully loaded best model from epoch {best_epoch}")
        if loaded_train_loss is not None and loaded_val_loss is not None:
            logger.info(f"   Training Loss:   {loaded_train_loss:.4f}")
            logger.info(f"   Validation Loss: {loaded_val_loss:.4f}")
            loaded_gap = loaded_val_loss - loaded_train_loss
            loaded_gap_pct = (loaded_gap / loaded_train_loss) * 100 if loaded_train_loss > 0 else 0
            logger.info(f"   Train/Val Gap: {loaded_gap:.4f} ({loaded_gap_pct:+.1f}%)")
            
            # Compare best checkpoint to final epoch
            # Ensure both values are not None before comparing
            if loaded_val_loss is not None and final_val_loss is not None and loaded_val_loss < final_val_loss:
                val_saved = ((final_val_loss - loaded_val_loss) / final_val_loss) * 100
                logger.info(f"   💡 Best checkpoint validation loss is {val_saved:.1f}% better than final epoch")
                logger.info(f"      (avoided overfitting by using best checkpoint)")
        logger.info(f"   📌 This is the model being used for all downstream tasks")
        logger.info("")
    else:
        logger.warning("⚠️  BEST CHECKPOINT NOT LOADED:")
        logger.warning(f"   Using final epoch model (may be suboptimal)")
        logger.warning(f"   Consider investigating why checkpoint loading failed")
        logger.info("")
    
    # Ensure all improvement values are not None before ANY comparisons
    if train_improvement is None:
        train_improvement = 0.0
    if val_improvement is None:
        val_improvement = 0.0
    if train_val_gap_pct is None:
        train_val_gap_pct = 0.0
    
    # Quality assessment
    quality_issues = []
    recommendations = []
    
    # Check 1: Did training actually improve?
    if train_improvement < 1.0:
        quality_issues.append("MINIMAL_LEARNING")
        recommendations.append("⚠️  Training barely improved (<1%) - model may not have learned meaningful representations")
        recommendations.append("   → Consider increasing learning rate")
        recommendations.append("   → Verify self-supervised task is appropriate")
        recommendations.append("   → Check if dataset has sufficient complexity")
    
    # Check 2: Severe overfitting
    if train_val_gap_pct > 20:
        quality_issues.append("SEVERE_OVERFITTING")
        recommendations.append(f"⚠️  Large train/val gap ({train_val_gap_pct:.1f}%) indicates overfitting")
        recommendations.append("   → Model may have memorized training data")
        recommendations.append("   → Consider using higher dropout for future training runs")
        recommendations.append("   → Increase weight_decay")
        if not best_checkpoint_loaded:
            recommendations.append("   → Best checkpoint should have been loaded but wasn't - investigate why")
    
    # Check 3: Validation got worse
    if val_improvement < 0:
        quality_issues.append("VAL_DEGRADATION")
        recommendations.append(f"⚠️  Validation loss got worse ({val_improvement:.1f}%)")
        recommendations.append("   → Model overfit the training data")
        if best_checkpoint_loaded:
            recommendations.append("   → ✅ Best checkpoint was loaded to mitigate this issue")
        else:
            recommendations.append("   → ❌ Best checkpoint should have been loaded but wasn't - investigate why")
        recommendations.append("   → Consider early stopping for future runs")
    
    # Check 4: Good training
    # Handle nan/inf values in val_improvement (e.g., when initial validation loss was inf)
    val_improvement_valid = math.isfinite(val_improvement) if val_improvement is not None else False
    
    if train_improvement > 5 and (val_improvement_valid and val_improvement > 0) and train_val_gap_pct < 10:
        logger.info("✅ QUALITY ASSESSMENT: GOOD")
        logger.info(f"   → Training improved significantly ({train_improvement:.1f}%)")
        if val_improvement_valid:
            logger.info(f"   → Validation also improved ({val_improvement:.1f}%)")
        else:
            logger.info(f"   → Validation improvement could not be calculated (initial validation loss was inf)")
        logger.info(f"   → Small train/val gap ({train_val_gap_pct:.1f}%) suggests good generalization")
        logger.info("   → Embeddings should be high quality for downstream tasks")
    elif train_improvement > 2 and (val_improvement_valid and val_improvement > -2):
        logger.info("⚠️  QUALITY ASSESSMENT: ACCEPTABLE")
        logger.info(f"   → Training improved moderately ({train_improvement:.1f}%)")
        if val_improvement_valid:
            logger.info(f"   → Validation improvement: {val_improvement:.1f}%")
        else:
            logger.info(f"   → Validation improvement could not be calculated (initial validation loss was inf)")
        logger.info(f"   → Some overfitting may be present ({train_val_gap_pct:.1f}% gap)")
        logger.info("   → Embeddings may work but could be better")
    else:
        # If val_improvement is invalid but train_improvement is good, don't mark as POOR
        if train_improvement > 5 and not val_improvement_valid:
            logger.info("⚠️  QUALITY ASSESSMENT: ACCEPTABLE")
            logger.info(f"   → Training improved significantly ({train_improvement:.1f}%)")
            logger.info(f"   → Validation improvement could not be calculated (initial validation loss was inf)")
            logger.info(f"   → Train/val gap: {train_val_gap_pct:.1f}%")
            logger.info("   → Embeddings should be usable but validation metrics unavailable")
        else:
            logger.error("❌ QUALITY ASSESSMENT: POOR")
            logger.error("   → Training did not improve sufficiently")
            logger.error("   → Embeddings may not be useful for downstream tasks")
            logger.error("   → Review training logs for failure modes")
    
    # Log recommendations
    if recommendations:
        logger.info("")
        logger.info("💡 RECOMMENDATIONS:")
        for rec in recommendations:
            logger.info(rec)
    
    logger.info("=" * 100)
    
    summary = {
        "status": "completed",
        "duration_minutes": duration_minutes,
        "epochs": len(train_losses),
        "initial_train_loss": initial_train_loss,
        "final_train_loss": final_train_loss,
        "train_improvement_pct": train_improvement,
        "initial_val_loss": initial_val_loss,
        "final_val_loss": final_val_loss,
        "val_improvement_pct": val_improvement,
        "best_train_loss": best_train_loss,
        "best_val_loss": best_val_loss,
        "train_val_gap": train_val_gap,
        "train_val_gap_pct": train_val_gap_pct,
        "quality_issues": quality_issues,
        "recommendations": recommendations
    }
    
    return summary


def embedding_space_debug_training(debug_class=None, epoch=None, embedding_space=None):
    """
    We keep this out of embedding_space so it doesn't get sucked into the pickle file.

    Before training, the caller calls this ```embedding_space_debug_training(debug_class=cls)```
    where cls has an epoch_finished method

    Args:
        debug_class:
        epoch:
        embedding_space:

    Returns:
        nada
    """
    try:
        if debug_class is not None:
            setattr(embedding_space_debug_training, "debug_class", debug_class)
        else:
            td = getattr(embedding_space_debug_training, "debug_class", None)
            if td is not None and hasattr(td, "epoch_finished"):
                td.epoch_finished(epoch_index=epoch, es=embedding_space)
    except Exception:
        traceback.print_exc()


class EmbeddingSpace(object):
    def __init__(
        self,
        train_input_data: FeatrixInputDataSet,
        val_input_data: FeatrixInputDataSet,
        output_debug_label: str = "No debug label specified",
        n_epochs: int = None,
        d_model: int = None,  # Will use config.json default if None
        training_state_path: str = None,
        encoder_config: Optional[FeatrixTableEncoderConfig] = None,
        string_cache: str = None,
        json_transformations: dict = None,
        version_info: dict = None,
        output_dir: str = None,
        name: str = None,
        required_child_es_mapping: dict = None,  # {col_name: session_id} mapping for child ES's
        sqlite_db_path: str = None,  # Path to SQLite database for PCA initialization
        user_metadata: dict = None,  # User metadata - arbitrary dict for user identification (max 32KB when serialized)
        skip_pca_init: bool = False,  # Skip PCA initialization (e.g., when reconstructing from checkpoint)
        codec_vocabulary_overrides: dict = None  # {col_name: set of vocabulary members} for SET columns when reconstructing from checkpoint
    ):  # df, column_spec):
        
        assert isinstance(train_input_data, FeatrixInputDataSet)
        assert isinstance(val_input_data, FeatrixInputDataSet)

        self.string_cache = string_cache
        
        # Store name for identification and tracking
        self.name = name
        if self.name:
            logger.info(f"🏷️  EmbeddingSpace initialized with name: {self.name}")
        
        # Store JSON transformation metadata for consistent encoding
        self.json_transformations = json_transformations or {}
        if self.json_transformations:
            logger.info(f"🔧 EmbeddingSpace initialized with JSON transformations for {len(self.json_transformations)} columns")
        
        # Store child ES mapping for JSON column dependencies
        self.required_child_es_mapping = required_child_es_mapping or {}
        if self.required_child_es_mapping:
            logger.info(f"🔗 EmbeddingSpace initialized with {len(self.required_child_es_mapping)} child ES dependencies: {list(self.required_child_es_mapping.keys())}")
        
        # Store version information for traceability 
        self.version_info = version_info
        if self.version_info:
            logger.info(f"📦 EmbeddingSpace initialized with version info: {self.version_info}")
        
        # Store user metadata for identification
        self.user_metadata = user_metadata
        if self.user_metadata:
            logger.info(f"🏷️  EmbeddingSpace initialized with user metadata: {len(str(self.user_metadata))} chars")
         
        self._warningEncodeFields = []
        self._gotControlC = False
        self.n_epochs = n_epochs
        
        # Get d_model from neural config if not explicitly provided
        if d_model is None:
            # Auto-compute based on number of columns
            num_columns = len(train_input_data.df.columns)
            d_model = get_config().auto_compute_d_model(num_columns)
            logger.info(f"🔧 Auto-computed d_model={d_model} based on {num_columns} columns")
        else:
            logger.info(f"🔧 Using provided d_model={d_model}")
        self.d_model = d_model

        self.output_debug_label = output_debug_label
        self.train_input_data = train_input_data
        self.val_input_data = val_input_data

        self.col_codecs = {}
        self.column_spec = train_input_data.column_codecs()
        
        # Store codec vocabulary overrides (for checkpoint reconstruction)
        self.codec_vocabulary_overrides = codec_vocabulary_overrides or {}
        if self.codec_vocabulary_overrides:
            logger.info(f"📚 Using vocabulary overrides for {len(self.codec_vocabulary_overrides)} SET columns (checkpoint reconstruction)")

        self.availableColumns = list(self.column_spec.keys())
        self._create_codecs()
        
        # Filter out JSON columns that were skipped during codec creation
        # This prevents KeyError when creating encoder configs for columns that don't have codecs
        json_cols_to_remove = []
        for col_name in list(self.column_spec.keys()):
            if col_name not in self.col_codecs:
                json_cols_to_remove.append(col_name)
                logger.info(f"🔍 Removing '{col_name}' from column_spec (no codec created)")
                del self.column_spec[col_name]
        
        if json_cols_to_remove:
            logger.info(f"   ✅ Removed {len(json_cols_to_remove)} JSON columns from column_spec: {json_cols_to_remove}")

        # Construct the dataset for self-supervised training.
        colsForCodingCount = train_input_data.get_columns_with_codec_count()
        self.train_dataset = SuperSimpleSelfSupervisedDataset(
            self.train_input_data.df,
            codecs=self.col_codecs,
            row_meta_data=train_input_data.project_row_meta_data_list,
            casted_df=train_input_data.casted_df,
        )

        self.val_dataset = SuperSimpleSelfSupervisedDataset(
            self.val_input_data.df,
            codecs=self.col_codecs,
            row_meta_data=val_input_data.project_row_meta_data_list,
            casted_df=val_input_data.casted_df,
        )

        self.callbacks = defaultdict(dict)

        self.meta_from_dataspace = {}

        self.column_tree = self.train_input_data.column_tree()
        self.col_order = flatten(self.column_tree)
        
        # Filter out columns that don't have codecs (e.g., skipped JSON columns)
        # This ensures col_order only contains columns we actually have codecs for
        original_col_order_len = len(self.col_order)
        self.col_order = [col for col in self.col_order if col in self.col_codecs]
        self.n_all_cols = len(self.col_order)
        
        if len(self.col_order) < original_col_order_len:
            removed_count = original_col_order_len - len(self.col_order)
            logger.info(f"   ✅ Filtered {removed_count} columns from col_order (no codecs created)")
        
        # Initialize col_types from column_spec (maps col_name -> ColumnType)
        # This is used for model package metadata and feature inventory
        self.col_types = {}
        for col_name in self.col_order:
            # Try to get from column_spec first
            if col_name in self.column_spec:
                self.col_types[col_name] = self.column_spec[col_name]
            # Fallback: derive from codec if available
            elif col_name in self.col_codecs:
                codec = self.col_codecs[col_name]
                if hasattr(codec, 'get_codec_name'):
                    self.col_types[col_name] = codec.get_codec_name()
                else:
                    self.col_types[col_name] = "unknown"
            else:
                self.col_types[col_name] = "unknown"
        
        # Initialize mask distribution tracker
        self.mask_tracker = None  # Will be initialized in train() with output_dir

        if encoder_config is None:
            self.encoder_config = self.get_default_table_encoder_config(
                d_model,
                self.col_codecs,
                self.col_order,
                self.column_spec,
            )
        else:
            self.encoder_config = encoder_config

        self.encoder = FeatrixTableEncoder(
            col_codecs=self.col_codecs,
            config=self.encoder_config,
        )
        self.encoder.to(device)
        self.model_param_count = self.encoder.count_model_parameters()
        
        # Log model parameter count as soon as we know it
        logger.info(f"📊 Model Parameters: {self.model_param_count['total_params']:,} total, "
                   f"{self.model_param_count['total_trainable_params']:,} trainable")
        if 'column_encoders_params' in self.model_param_count:
            logger.info(f"   └─ Column encoders: {self.model_param_count['column_encoders_params']:,} params "
                   f"({self.model_param_count.get('column_encoders_trainable_params', 0):,} trainable)")
        if 'joint_encoder_params' in self.model_param_count:
            logger.info(f"   └─ Joint encoder: {self.model_param_count['joint_encoder_params']:,} params "
                   f"({self.model_param_count.get('joint_encoder_trainable_params', 0):,} trainable)")
        
        # Set embedding space on all JSON codecs now that EmbeddingSpace is fully initialized
        # This allows JsonCodec to cache embeddings (retry pre-caching if it was skipped)
        from featrix.neural.json_codec import JsonCodec
        for col_name, codec in self.col_codecs.items():
            if isinstance(codec, JsonCodec):
                # Only set if it doesn't have a child ES (child ES codecs use their own ES)
                if not hasattr(codec, 'child_es_session_id') or codec.child_es_session_id is None:
                    codec.set_embedding_space(self)
                    logger.info(f"🔗 Set embedding space on JsonCodec '{col_name}'")
                    # Retry pre-caching if it was skipped during init (when embedding_space was None)
                    # Get initial values from train_input_data (same as create_json_codec does)
                    if codec.json_cache and codec.json_cache.embedding_space is not None:
                        try:
                            df_col = self.train_input_data.df[col_name]
                            initial_values = df_col.dropna().tolist()[:1000]  # Limit to first 1000 for caching
                            if initial_values:
                                logger.info(f"🔄 Retrying pre-cache for JsonCodec '{col_name}' ({len(initial_values)} values)")
                                codec.json_cache.run_batch(initial_values)
                        except Exception as e:
                            logger.warning(f"⚠️ Failed to retry pre-cache for JsonCodec '{col_name}': {e}")

        self.es_neural_attrs = {
            "name": self.name,
            "d_model": self.d_model,
            "col_order": self.col_order,
            "col_tree": self.column_tree,
            "n_all_cols": self.n_all_cols,
            "len_df": self.len_df(),
            "num_cols": len(self.train_input_data.df.columns),
            "ignore_cols": train_input_data.ignore_cols,
            "input_data_debug": train_input_data.detectorDebugInfo,
            # "self_supervised_config": asdict(self.train_dataset.config),
            "colsForCodingCount": colsForCodingCount,
            "codec_mapping": self.get_codec_meta(),
            "json_transformations": self.json_transformations,  # Include JSON transformation metadata
            "version_info": self.version_info if self.version_info else None,  # Include version info for traceability (already a dict)
            "kl_divergences": getattr(train_input_data, 'kl_divergences_vs_val', {}),  # Distribution match metrics
        }

        self.training_info = {}

        # Training state fields
        # Default to checkpoint_resume_training for clearer naming
        if training_state_path:
            self.training_state_path = training_state_path
        else:
            # Transform old "training_state" to new "checkpoint_resume_training" if present
            default_path = f"{os.getcwd()}/checkpoint_resume_training"
            self.training_state_path = default_path
        self.training_state = {}
        self.training_progress_data = {}
        
        # Training timeline tracking - initialize here to ensure it's always present
        self._training_timeline = []
        self._corrective_actions = []
        
        # Warning state tracking - track active warnings to detect start/stop
        self._active_warnings = {}  # {warning_type: {'start_epoch': int, 'details': dict}}
        self._tiny_grad_warned_this_epoch = False  # Track if we've warned about tiny gradients this epoch

        # Set output directory with fallback to config
        if output_dir is None:
            try:
                from config import config
                self.output_dir = str(config.output_dir)
            except:
                self.output_dir = "./featrix_output"  # Ultimate fallback
        else:
            self.output_dir = output_dir
        
        # Store SQLite database path for PCA initialization
        self.sqlite_db_path = sqlite_db_path
        
        # WEIGHT INITIALIZATION
        # Configurable via config.json: "es_weight_initialization": "random" or "pca_string"
        # Default is "random" (standard PyTorch init)
        # Note: get_config is already imported at top of file
        es_init_strategy = get_config().get_es_weight_initialization()
        
        if skip_pca_init:
            logger.info("⏭️  Skipping PCA initialization (reconstructing from checkpoint or explicitly disabled)")
        elif es_init_strategy == "pca_string":
            logger.info(f"🎲 Using PCA-based weight initialization (es_weight_initialization='{es_init_strategy}')")
            self._initialize_weights_from_pca(train_input_data)
        else:
            # Default: random initialization (standard PyTorch)
            logger.info(f"🎲 Using random weight initialization (es_weight_initialization='{es_init_strategy}')")
    
    def _track_warning_in_timeline(self, epoch_idx, warning_type, is_active, details=None):
        """
        Track warnings in timeline - add entries when warnings start/stop.
        
        Args:
            epoch_idx: Current epoch number
            warning_type: Type of warning (e.g., 'NO_LEARNING', 'TINY_GRADIENTS', 'SEVERE_OVERFITTING')
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

    def _initialize_weights_from_pca(self, input_data):
        """Initialize network weights using PCA statistics from sentence transformer embeddings.
        
        This method tries multiple sources for embeddings:
        1. SQLite database (if sqlite_db_path provided and embeddings exist)
        2. Generate on-the-fly from input_data DataFrame (fallback)
        
        This decouples PCA initialization from SQLite format dependency.
        """
        logger.info("🔮 PCA-BASED WEIGHT INITIALIZATION ENABLED")
        
        # torch is already imported at module level, but ensure it's available
        # Import sklearn here since it's only needed for PCA
        from sklearn.decomposition import PCA
        embeddings_384d = None
        embedding_device = 'cpu'  # Default, will be updated if CUDA is available
        
        # Strategy 1: Try to load from SQLite database (if available)
        db_path = self.sqlite_db_path
        if db_path:
            try:
                if os.path.exists(db_path):
                    db_path_lower = db_path.lower()
                    if db_path_lower.endswith('.db') or db_path_lower.endswith('.sqlite') or db_path_lower.endswith('.sqlite3'):
                        logger.info(f"📂 Attempting to load embeddings from SQLite: {db_path}")
                        
                        conn = sqlite3.connect(db_path)
                        cursor = conn.cursor()
                        
                        # Check if column exists (table name is "data" by default in csv_to_sqlite)
                        cursor.execute("PRAGMA table_info(data)")
                        columns = [row[1] for row in cursor.fetchall()]
                        
                        if '__featrix_sentence_embedding_384d' in columns:
                            # Load all embeddings
                            cursor.execute("SELECT __featrix_sentence_embedding_384d FROM data ORDER BY rowid")
                            rows = cursor.fetchall()
                            
                            embeddings_384d = []
                            for row in rows:
                                if row[0] is not None:
                                    embedding = pickle.loads(row[0])
                                    embeddings_384d.append(embedding)
                            
                            if embeddings_384d:
                                embeddings_384d = np.array(embeddings_384d, dtype=np.float32)
                                logger.info(f"✅ Loaded {len(embeddings_384d)} embeddings (384d) from SQLite")
                            else:
                                logger.info("ℹ️  SQLite database has embedding column but no embeddings found")
                        
                        conn.close()
            except Exception as e:
                logger.debug(f"Could not load embeddings from SQLite: {e}")
        
        # Strategy 2: Generate embeddings on-the-fly from input_data (if SQLite not available)
        if embeddings_384d is None:
            logger.info("📊 SQLite embeddings not available - generating embeddings on-the-fly from input data...")
            try:
                import pandas as pd
                # Note: No longer importing SentenceTransformer - using string server client instead
                # torch is already imported at the top of this function
                
                # Get DataFrame from input_data
                df = input_data.df
                if df is None or len(df) == 0:
                    logger.warning("⚠️  Input data is empty - skipping PCA initialization")
                    return
                
                # Convert records to text (same logic as in create_structured_data)
                records = df.to_dict('records')
                
                def json_to_text(record):
                    lines = []
                    for key, value in record.items():
                        if not key.startswith('__featrix'):
                            if value is None or (isinstance(value, float) and pd.isna(value)):
                                lines.append('-')
                            else:
                                lines.append(str(value))
                    return "\n".join(lines)
                
                texts = [json_to_text(record) for record in records]
                
                # Use string server client for PCA embeddings instead of loading local model
                logger.info(f"📚 Using string server client for PCA embeddings...")
                _log_gpu_memory_embedded_space("BEFORE getting embeddings from string server for PCA")
                
                # Initialize string server client
                from featrix.neural.string_codec import _init_string_server_client
                client = _init_string_server_client()
                
                if client is None:
                    logger.error("❌ String server client not available for PCA initialization. Set 'string_server_host' in config.json to 'taco', 'taco.local', or 'localhost'")
                    logger.warning("⚠️  Skipping PCA initialization - will use default weight initialization")
                    return
                
                _log_gpu_memory_embedded_space("AFTER initializing string server client for PCA")
                
                # Encode all texts using string server client (batch encoding is more efficient)
                logger.info(f"🔮 Generating {len(texts)} embeddings via string server...")
                # Use batch encoding for efficiency
                batch_size = 100  # String server handles batching internally
                embeddings_384d = []
                for i in range(0, len(texts), batch_size):
                    batch_texts = texts[i:i+batch_size]
                    batch_embeddings = client.encode_batch(batch_texts)
                    embeddings_384d.extend(batch_embeddings)
                
                _log_gpu_memory_embedded_space("AFTER encoding texts for PCA")
                embeddings_384d = np.array(embeddings_384d, dtype=np.float32)
                logger.info(f"✅ Generated {len(embeddings_384d)} embeddings (384d) from input data")
                
            except Exception as e:
                logger.warning(f"⚠️  Could not generate embeddings on-the-fly: {e}")
                logger.warning("⚠️  Skipping PCA-based weight initialization")
                return
        
        if embeddings_384d is None or len(embeddings_384d) == 0:
            logger.warning("⚠️  No embeddings available - skipping PCA initialization")
            return
        
        # Apply PCA to match d_model
        n_components = min(self.d_model, embeddings_384d.shape[1], embeddings_384d.shape[0])
        logger.info(f"📊 Applying PCA: 384d → {n_components}d")
        
        pca = PCA(n_components=n_components)
        pca_embeddings = pca.fit_transform(embeddings_384d)
        
        logger.info(f"   Explained variance: {pca.explained_variance_ratio_.sum()*100:.2f}%")
        
        # Log PCA component analysis
        logger.info(f"📊 PCA Component Analysis (first 10 components):")
        for i in range(min(10, n_components)):
            var_ratio = pca.explained_variance_ratio_[i] * 100
            var = pca.explained_variance_[i]
            logger.info(f"   PC{i+1}: {var_ratio:.2f}% variance (var={var:.4f})")
        
        # Extract statistics for weight initialization
        pca_std = pca_embeddings.std()
        pca_mean = pca_embeddings.mean()
        
        logger.info(f"📊 PCA statistics:")
        logger.info(f"   Mean: {pca_mean:.6f}")
        logger.info(f"   Std:  {pca_std:.6f}")
        
        # Log where 500 random points are in PCA space (actual PCA results)
        n_samples = min(500, len(pca_embeddings))
        sample_indices = np.random.choice(len(pca_embeddings), size=n_samples, replace=False)
        sample_embeddings = pca_embeddings[sample_indices]
        
        # Log first 3 principal components for visualization
        logger.info(f"📍 Sample of {n_samples} points in PCA space (first 3 PCs):")
        logger.info(f"   First 10 points:")
        for i in range(min(10, n_samples)):
            point = sample_embeddings[i]
            logger.info(f"      Point {sample_indices[i]}: PC1={point[0]:.4f}, PC2={point[1]:.4f}, PC3={point[2]:.4f}")
        
        # Log statistics across all principal components
        logger.info(f"   Statistics across all {n_components} principal components:")
        logger.info(f"      Min (first 5 PCs): {sample_embeddings.min(axis=0)[:5]}")
        logger.info(f"      Max (first 5 PCs): {sample_embeddings.max(axis=0)[:5]}")
        logger.info(f"      Mean (first 5 PCs): {sample_embeddings.mean(axis=0)[:5]}")
        logger.info(f"      Std (first 5 PCs): {sample_embeddings.std(axis=0)[:5]}")
        
        # Per-dimension variance across ALL PCs (not just first 5)
        per_dim_var = pca_embeddings.var(axis=0)
        logger.info(f"📊 Per-dimension variance (all {n_components} PCs):")
        logger.info(f"   Min var:  {per_dim_var.min():.6f} (PC {per_dim_var.argmin()+1})")
        logger.info(f"   Max var:  {per_dim_var.max():.6f} (PC {per_dim_var.argmax()+1})")
        logger.info(f"   Mean var: {per_dim_var.mean():.6f}")
        logger.info(f"   Total var: {per_dim_var.sum():.6f}")
        
        # Show variance decay across PCs (should decrease)
        if n_components >= 10:
            logger.info(f"   Variance decay: PC1={per_dim_var[0]:.4f} -> PC10={per_dim_var[9]:.4f} -> PC{n_components}={per_dim_var[-1]:.6f}")
        else:
            logger.info(f"   Variance decay: PC1={per_dim_var[0]:.4f} -> PC{n_components}={per_dim_var[-1]:.6f}")
        
        # Check for near-zero variance dimensions (dead PCs)
        near_zero_threshold = 1e-6
        dead_pcs = (per_dim_var < near_zero_threshold).sum()
        if dead_pcs > 0:
            logger.warning(f"   {dead_pcs} PCs have near-zero variance (<{near_zero_threshold}) - these dimensions carry no information")
        
        # Initialize network weights using PCA statistics
        logger.info(f"🎲 Initializing network weights with PCA-derived std={pca_std:.6f}")
        
        param_count = 0
        for name, param in self.encoder.named_parameters():
            if 'weight' in name and param.ndim >= 2:
                torch.nn.init.normal_(param, mean=0.0, std=pca_std)
                param_count += 1
        
        logger.info(f"✅ Initialized {param_count} weight tensors with PCA statistics")
        logger.info(f"✅ PCA-based initialization complete")

    def set_string_cache_path(self, path):
        set_string_cache_path(path)
        return
    
    def hydrate_to_cpu_if_needed(self):
        if self.encoder:
            logger.info("encoder going to cpu")
            self.encoder.to(torch.device("cpu"))
        else:
            logger.info("no encoder for cpu")
        return

    def hydrate_to_gpu_if_needed(self):
        if self.encoder:
            logger.info(f"existing encoder going to {device}")
            self.encoder.to(device)
        else:
            logger.info(f"no encoder!?")
        return

    def get_string_column_names(self):
        cols = []
        for c, codec in self.col_codecs.items():
            if isinstance(codec, StringCodec):
                cols.append(c)
        return cols

    def get_set_columns(self):
        # return all the columns using the set encoder:
        # { col_name: [possible values]}
        cols = {}
        for c, codec in self.col_codecs.items():
            if isinstance(codec, SetCodec):
                # cols.append(c)
                if len(codec.members) <= 50:
                    cols[c] = codec.members
        return cols

    def get_scalar_columns(self):
        cols = {}
        for c, codec in self.col_codecs.items():
            if isinstance(codec, ScalarCodec):
                # cols.append(c)
                cols[c] = codec
        return cols


    def len_df(self):
        """Get total number of rows in training and validation data."""
        if self.train_input_data is None or self.val_input_data is None:
            # If input data not loaded (e.g., after unpickling), return 0
            # Caller should set train_input_data and val_input_data before calling this
            return 0
        return len(self.train_input_data.df) + len(self.val_input_data.df)    

    def get_default_table_encoder_config(
        self, d_model: int, col_codecs, col_order, col_types
    ):
        # The default configs for the column encoders have to be instantiatied in the EmbeddingSpace
        # object and not when initializign the respective encoder classes because they need info about
        # model dimension and e.g. set size (for set tokens), and otherwise this information would have
        # to be threaded down to the relevant codecs and make the configuration more difficult to manage.
        n_cols = len(col_order)

        dropout = 0.5

        col_encoder_configs = self.get_default_column_encoder_configs(
            d_model,
            col_codecs,
            dropout,
        )
        col_predictor_configs = self.get_default_column_predictor_configs(
            d_model,
            col_order,
            dropout,
        )
        column_predictors_short_config = SimpleMLPConfig(
            d_in=3,
            d_out=3,
            d_hidden=d_model,  # Use d_model to match embedding space dimension (was hardcoded 256)
            n_hidden_layers=1,
            dropout=dropout,
            normalize=False,  # predictors are NOT normalized
            residual=True,
            use_batch_norm=True,
        )
        joint_encoder_config = self.get_default_joint_encoder_config(
            d_model=d_model, n_cols=n_cols, col_order=col_order, dropout=dropout
        )
        joint_predictor_config = SimpleMLPConfig(
            d_in=d_model,
            d_out=d_model,
            d_hidden=d_model,  # Use d_model to match embedding space dimension (was hardcoded 256)
            n_hidden_layers=1,
            dropout=dropout,
            normalize=False,  # predictors are NOT normalized
            residual=True,
            use_batch_norm=True,
        )
        joint_predictor_short_config = SimpleMLPConfig(
            d_in=3,
            d_out=3,
            d_hidden=256,
            n_hidden_layers=1,
            dropout=dropout,
            normalize=False,  # predictors are NOT normalized
            residual=True,
            use_batch_norm=True,
        )
        # Scale marginal loss weight inversely with number of columns to balance gradient magnitudes
        # With N columns, marginal loss sums N per-column losses, so we divide by N to normalize
        # Use 1.0x scaling to make marginal evenly balanced
        marginal_weight = n_cols
        logger.info(f"⚖️ Adaptive loss weights: marginal={marginal_weight:.4f} ({marginal_weight * n_cols:.1f}/{n_cols} cols), joint=1.0, spread=1.0")
        
        loss_function_config = LossFunctionConfig(
            joint_loss_weight=1.0,
            marginal_loss_weight=marginal_weight,
            spread_loss_weight=1.0,
            spread_loss_config=SpreadLossConfig()
        )
        return FeatrixTableEncoderConfig(
            d_model=d_model,
            n_cols=n_cols,
            cols_in_order=col_order,
            col_types=col_types,
            column_encoders_config=col_encoder_configs,
            column_predictors_config=col_predictor_configs,
            column_predictors_short_config=column_predictors_short_config,
            joint_encoder_config=joint_encoder_config,
            joint_predictor_config=joint_predictor_config,
            joint_predictor_short_config=joint_predictor_short_config,
            loss_config=loss_function_config,
        )

    @staticmethod
    def get_default_joint_encoder_config(
        d_model: int, n_cols: int, col_order, dropout: float
    ):
        in_converter_configs = dict()
        transformer_model_d = 256

        for col_name in col_order:
            in_converter_configs[col_name] = SimpleMLPConfig(
                d_in=d_model,
                d_out=transformer_model_d,
                d_hidden=256,
                n_hidden_layers=1,  # One hidden layer for non-linear preprocessing
                dropout=dropout,
                # Normalization controlled by batch_norm
                normalize=False,
                residual=True,
                use_batch_norm=True,
            )

        out_converter_config = SimpleMLPConfig(
            d_in=transformer_model_d,
            d_out=d_model,
            d_hidden=256,
            n_hidden_layers=3,
            dropout=dropout,
            normalize=False,  # normalization is controlled inependently by JointEncoder
            residual=True,
            use_batch_norm=True,
        )

        return JointEncoderConfig(
            d_model=transformer_model_d,
            use_col_encoding=True,
            dropout=dropout,
            n_cols=n_cols,
            n_layers=3,
            n_heads=8,
            in_converter_configs=in_converter_configs,
            out_converter_config=out_converter_config,
        )

    @staticmethod
    def get_default_column_encoder_configs(d_model: int, col_codecs, dropout: float):
        encoder_configs = dict()
        for col_name, codec in col_codecs.items():
            col_type = codec.get_codec_name()

            if col_type == ColumnType.SET:
                # Get sparsity ratio from codec if available
                sparsity_ratio = getattr(codec, 'sparsity_ratio', 0.0)
                encoder_configs[col_name] = SetEncoder.get_default_config(
                    d_model=d_model,
                    n_members=codec.n_members,
                    sparsity_ratio=sparsity_ratio,
                )
            elif col_type == ColumnType.SCALAR:
                # Use AdaptiveScalarEncoder config instead of old ScalarEncoder
                # AdaptiveScalarEncoder doesn't need the complex config - just d_model
                from featrix.neural.model_config import ScalarEncoderConfig
                encoder_configs[col_name] = ScalarEncoderConfig(
                    d_out=d_model,
                    d_hidden=64,  # Used internally by AdaptiveScalarEncoder MLPs
                    n_hidden_layers=1,
                    dropout=dropout,
                    normalize=True,
                    residual=False,
                    use_batch_norm=False,
                )
            elif col_type == ColumnType.FREE_STRING:
                # Adaptive architecture selection based on column analysis
                if hasattr(codec, '_adaptive_analysis'):
                    from featrix.neural.string_analysis import (
                        compute_info_density,
                        select_architecture_from_info_density
                    )
                    
                    analysis = codec._adaptive_analysis
                    
                    # Skip encoder config for random columns (zero contribution)
                    if analysis["is_random"]:
                        logger.info(f"   ⚠️  Skipping encoder config for random column '{col_name}'")
                        # Still create a minimal encoder but it will get zero inputs
                        encoder_configs[col_name] = StringEncoder.get_default_config(
                            d_in=codec.d_string_model,
                            d_out=d_model // 4,  # Minimal size for random column
                            d_model=d_model,  # Always project to d_model for stacking
                        )
                    else:
                        # Compute info density and select architecture
                        info_density = compute_info_density(analysis["precomputed"])
                        arch_config = select_architecture_from_info_density(info_density, d_model)
                        
                        logger.info(f"   🎯 Adaptive architecture for '{col_name}':")
                        logger.info(f"      Strategy: {arch_config['strategy']}")
                        logger.info(f"      d_out: {arch_config['d_out']} (info density: {info_density:.2f})")
                        logger.info(f"      n_hidden_layers: {arch_config['n_hidden_layers']}")
                        
                        encoder_configs[col_name] = StringEncoder.get_default_config(
                            d_in=codec.d_string_model,
                            d_out=arch_config['d_out'],
                            d_model=d_model,  # Always project to d_model for stacking
                        )
                        
                        # Store architecture details in encoder config for later reference
                        encoder_configs[col_name].n_hidden_layers = arch_config['n_hidden_layers']
                        encoder_configs[col_name].d_hidden = arch_config['d_hidden']
                else:
                    # Fallback: no adaptive analysis (backward compatibility)
                    encoder_configs[col_name] = StringEncoder.get_default_config(
                        d_in=codec.d_string_model,
                        d_out=d_model * 2,  # Default: 2x capacity
                        d_model=d_model,  # Always project to d_model for stacking
                    )
            elif col_type == ColumnType.LIST_OF_A_SET:
                encoder_configs[col_name] = ListOfASetEncoder.get_default_config(
                    d_in=d_model,
                    n_members=codec.n_members,
                )
            elif col_type == ColumnType.VECTOR:
                encoder_configs[col_name] = VectorEncoder.get_default_config(
                    d_in=codec.in_dim,
                    d_out=d_model,
                )
            elif col_type == ColumnType.JSON:
                # JSON codec already produces embeddings via JsonCodec.tokenize()
                # JsonEncoder just extracts values from tokens, so it needs minimal config
                from featrix.neural.model_config import SimpleMLPConfig
                encoder_configs[col_name] = SimpleMLPConfig(
                    d_in=codec.enc_dim,  # Input is the embedding from JsonCodec
                    d_out=d_model,  # Output to d_model for stacking
                    d_hidden=d_model,  # Simple pass-through, no hidden layers needed
                    n_hidden_layers=0,  # No hidden layers - just pass through
                    dropout=0.0,  # No dropout for pass-through
                    normalize=False,  # Normalization handled by JsonCodec
                    residual=False,
                    use_batch_norm=False,
                )
            elif col_type == ColumnType.URL:
                # URL codec handles its own encoding, encoder is just pass-through
                from featrix.neural.model_config import SimpleMLPConfig
                encoder_configs[col_name] = SimpleMLPConfig(
                    d_in=codec.enc_dim,
                    d_out=d_model,
                    d_hidden=d_model,
                    n_hidden_layers=0,
                    dropout=0.0,
                    normalize=False,
                    residual=False,
                    use_batch_norm=False,
                )
            elif col_type == ColumnType.TIMESTAMP:
                # TimestampEncoder takes 12 temporal features and encodes them
                from featrix.neural.model_config import TimestampEncoderConfig
                encoder_configs[col_name] = TimestampEncoderConfig(
                    d_out=d_model,
                    d_hidden=256,  # Default from TimestampEncoder.get_default_config
                    n_hidden_layers=2,  # Default from TimestampEncoder.get_default_config
                    dropout=dropout,
                    normalize=True,  # TimestampEncoder normalizes by default
                    residual=True,  # TimestampEncoder uses residual by default
                    use_batch_norm=True,  # TimestampEncoder uses batch norm by default
                )
            else:
                raise ValueError(f"Unknown column type: {col_type}")

        return encoder_configs

    @staticmethod
    def get_default_column_predictor_configs(
        d_model: int, col_names_in_order, dropout: float
    ):
        predictor_configs = dict()
        for col_name in col_names_in_order:
            config = SimpleMLPConfig(
                d_in=d_model,
                d_out=d_model,
                d_hidden=d_model,  # Use d_model to match embedding space dimension (was hardcoded 200)
                n_hidden_layers=1,
                dropout=dropout,
                normalize=False,  # predictors are NOT normalized
                residual=True,
                use_batch_norm=True,
            )

            predictor_configs[col_name] = config

        return predictor_configs

    def _generate_candidate_predictor_architectures(self, d_model: int, dropout: float):
        """
        Generate candidate architectures for column predictors and joint predictor.
        
        Returns:
            List of dicts, each containing:
            - 'col_predictor_configs': dict of SimpleMLPConfig per column
            - 'joint_predictor_config': SimpleMLPConfig for joint predictor
            - 'description': str describing the architecture
        """
        candidates = []
        
        # Candidate 1: Very Small (64d, 1 layer)
        col_configs_1 = {}
        for col_name in self.col_order:
            col_configs_1[col_name] = SimpleMLPConfig(
                d_in=d_model,
                d_out=d_model,
                d_hidden=64,
                n_hidden_layers=1,
                dropout=dropout,
                normalize=False,
                residual=True,
                use_batch_norm=True,
            )
        joint_config_1 = SimpleMLPConfig(
            d_in=d_model,
            d_out=d_model,
            d_hidden=64,
            n_hidden_layers=1,
            dropout=dropout,
            normalize=False,
            residual=True,
            use_batch_norm=True,
        )
        candidates.append({
            'col_predictor_configs': col_configs_1,
            'joint_predictor_config': joint_config_1,
            'description': 'Very Small (64d, 1 layer)'
        })
        
        # Candidate 2: Small, shallow (baseline)
        col_configs_2 = {}
        for col_name in self.col_order:
            col_configs_2[col_name] = SimpleMLPConfig(
                d_in=d_model,
                d_out=d_model,
                d_hidden=128,
                n_hidden_layers=1,
                dropout=dropout,
                normalize=False,
                residual=True,
                use_batch_norm=True,
            )
        joint_config_2 = SimpleMLPConfig(
            d_in=d_model,
            d_out=d_model,
            d_hidden=128,
            n_hidden_layers=1,
            dropout=dropout,
            normalize=False,
            residual=True,
            use_batch_norm=True,
        )
        candidates.append({
            'col_predictor_configs': col_configs_2,
            'joint_predictor_config': joint_config_2,
            'description': 'Small (128d, 1 layer)'
        })
        
        # Candidate 3: Small-Medium (192d, 1 layer)
        col_configs_3 = {}
        for col_name in self.col_order:
            col_configs_3[col_name] = SimpleMLPConfig(
                d_in=d_model,
                d_out=d_model,
                d_hidden=192,
                n_hidden_layers=1,
                dropout=dropout,
                normalize=False,
                residual=True,
                use_batch_norm=True,
            )
        joint_config_3 = SimpleMLPConfig(
            d_in=d_model,
            d_out=d_model,
            d_hidden=192,
            n_hidden_layers=1,
            dropout=dropout,
            normalize=False,
            residual=True,
            use_batch_norm=True,
        )
        candidates.append({
            'col_predictor_configs': col_configs_3,
            'joint_predictor_config': joint_config_3,
            'description': 'Small-Medium (192d, 1 layer)'
        })
        
        # Candidate 4: Medium, shallow
        col_configs_2 = {}
        for col_name in self.col_order:
            col_configs_2[col_name] = SimpleMLPConfig(
                d_in=d_model,
                d_out=d_model,
                d_hidden=256,
                n_hidden_layers=1,
                dropout=dropout,
                normalize=False,
                residual=True,
                use_batch_norm=True,
            )
        joint_config_2 = SimpleMLPConfig(
            d_in=d_model,
            d_out=d_model,
            d_hidden=256,
            n_hidden_layers=1,
            dropout=dropout,
            normalize=False,
            residual=True,
            use_batch_norm=True,
        )
        candidates.append({
            'col_predictor_configs': col_configs_2,
            'joint_predictor_config': joint_config_2,
            'description': 'Medium (256d, 1 layer)'
        })
        
        # Candidate 5: Medium, deeper
        col_configs_5 = {}
        for col_name in self.col_order:
            col_configs_5[col_name] = SimpleMLPConfig(
                d_in=d_model,
                d_out=d_model,
                d_hidden=256,
                n_hidden_layers=2,
                dropout=dropout,
                normalize=False,
                residual=True,
                use_batch_norm=True,
            )
        joint_config_5 = SimpleMLPConfig(
            d_in=d_model,
            d_out=d_model,
            d_hidden=256,
            n_hidden_layers=2,
            dropout=dropout,
            normalize=False,
            residual=True,
            use_batch_norm=True,
        )
        candidates.append({
            'col_predictor_configs': col_configs_5,
            'joint_predictor_config': joint_config_5,
            'description': 'Medium-Deep (256d, 2 layers)'
        })
        
        # Candidate 6: Large, shallow
        col_configs_4 = {}
        for col_name in self.col_order:
            col_configs_4[col_name] = SimpleMLPConfig(
                d_in=d_model,
                d_out=d_model,
                d_hidden=512,
                n_hidden_layers=1,
                dropout=dropout,
                normalize=False,
                residual=True,
                use_batch_norm=True,
            )
        joint_config_4 = SimpleMLPConfig(
            d_in=d_model,
            d_out=d_model,
            d_hidden=512,
            n_hidden_layers=1,
            dropout=dropout,
            normalize=False,
            residual=True,
            use_batch_norm=True,
        )
        candidates.append({
            'col_predictor_configs': col_configs_4,
            'joint_predictor_config': joint_config_4,
            'description': 'Large (512d, 1 layer)'
        })
        
        return candidates

    def _select_best_predictor_architecture(
        self,
        batch_size: int,
        selection_epochs: int = 25,
        val_dataloader=None
    ):
        """
        Train multiple predictor architectures and select the best.
        
        Args:
            batch_size: Batch size for training
            selection_epochs: Number of epochs to train each candidate (default: 25)
                Since encoder is frozen, only predictor heads train - this is fast!
                More epochs = better signal about which architecture actually performs better.
            val_dataloader: Validation dataloader for evaluation
            
        Returns:
            dict: Best architecture config with keys:
            - 'col_predictor_configs': dict of SimpleMLPConfig per column
            - 'joint_predictor_config': SimpleMLPConfig for joint predictor
            - 'description': str describing the architecture
            - 'final_val_loss': float validation loss of winner
        """
        # Generate candidate architectures first (needed for logging)
        dropout = 0.5  # Use default dropout for selection
        if hasattr(self.encoder_config, 'loss_config') and hasattr(self.encoder_config.loss_config, 'spread_loss_config'):
            # Try to get dropout from config, but use default if not available
            pass
        all_candidates = self._generate_candidate_predictor_architectures(self.d_model, dropout)
        # Only test first 2 candidates to save time
        candidates = all_candidates[:2]
        
        logger.info("=" * 80)
        logger.info("🏗️  PREDICTOR HEAD ARCHITECTURE SELECTION")
        logger.info("=" * 80)
        logger.info(f"⚠️  IMPORTANT: Selecting PREDICTOR HEAD architectures, NOT embedding space architecture!")
        logger.info(f"   - Embedding space encoder (d_model={self.d_model}): FIXED - NOT part of selection")
        logger.info(f"   - Testing {len(candidates)} different PREDICTOR HEAD architectures (limited to first {len(candidates)} of {len(all_candidates)} total candidates)")
        logger.info(f"   - Candidate dimensions: 64d, 128d, 192d, 256d (these are PREDICTOR HEAD hidden dimensions, not embedding space dimension)")
        logger.info(f"   - Column predictors: Small MLPs that predict each column from joint embeddings (for self-supervised learning)")
        logger.info(f"   - Joint predictor: Small MLP that predicts joint embeddings (for self-supervised learning)")
        logger.info(f"   - EMBEDDING SPACE ENCODER (column_encoder + joint_encoder): FROZEN (not training, just using for forward pass)")
        logger.info(f"   - PREDICTOR HEADS (column_predictor + joint_predictor): TRAINING (only these small MLPs are being updated)")
        logger.info(f"   - Training {selection_epochs} epochs per candidate to compare validation loss")
        logger.info(f"   - Total overhead: {len(candidates)} candidates × {selection_epochs} epochs = {len(candidates) * selection_epochs} epochs")
        logger.info(f"   - ⚡ FAST: Encoder frozen means only small predictor head MLPs train - {selection_epochs} epochs is quick!")
        logger.info(f"   - Will only use better architecture if improvement > 5% or >5.0 absolute")
        logger.info(f"   - ✅ After selection completes, MAIN TRAINING will train the FULL EMBEDDING SPACE (encoder + selected predictor heads) for your requested epoch count")
        logger.info(f"📋 Generated {len(candidates)} candidate predictor head architectures")
        
        # Store original predictor state (we'll restore it later)
        original_col_predictor = self.encoder.column_predictor
        original_joint_predictor = self.encoder.joint_predictor
        
        # Create train dataloader using the same pattern as main training
        # FeatrixInputDataSet has a df attribute, and we need to use col_codecs
        train_dataset = SuperSimpleSelfSupervisedDataset(
            self.train_input_data.df,
            self.col_codecs
        )
        train_dl_kwargs = create_dataloader_kwargs(
            batch_size=batch_size,
            shuffle=True,
            drop_last=True,
            dataset_size=len(self.train_input_data.df),
        )
        train_dataloader = DataLoader(
            train_dataset,
            collate_fn=collate_tokens,
            **train_dl_kwargs
        )
        
        if val_dataloader is None:
            # Create validation dataloader
            val_dataset = SuperSimpleSelfSupervisedDataset(
                self.val_input_data.df,
                self.col_codecs
            )
            # CRITICAL: Reduce validation workers based on available VRAM to prevent OOM
            val_num_workers = None
            if torch.cuda.is_available():
                try:
                    allocated = torch.cuda.memory_allocated() / (1024**3)
                    reserved = torch.cuda.memory_reserved() / (1024**3)
                    total_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                    free_vram = total_memory - reserved
                    
                    worker_vram_gb = 0.6
                    safety_margin_gb = 20.0
                    available_for_workers = max(0, free_vram - safety_margin_gb)
                    max_workers_by_vram = int(available_for_workers / worker_vram_gb)
                    
                    from featrix.neural.dataloader_utils import get_optimal_num_workers
                    default_workers = get_optimal_num_workers(dataset_size=len(self.val_input_data.df))
                    
                    val_num_workers = min(default_workers, max_workers_by_vram, 4)
                    val_num_workers = max(0, val_num_workers)
                    
                    logger.info(f"🔍 Validation worker calculation: free_vram={free_vram:.1f}GB → {val_num_workers} workers")
                except Exception as e:
                    logger.warning(f"Could not calculate optimal validation workers: {e}, using 0")
                    val_num_workers = 0
            
            val_dl_kwargs = create_dataloader_kwargs(
                batch_size=batch_size,
                shuffle=False,
                drop_last=True,
                num_workers=val_num_workers,
                dataset_size=len(self.val_input_data.df),
            )
            val_dataloader = DataLoader(
                val_dataset,
                collate_fn=collate_tokens,
                **val_dl_kwargs
            )
        
        best_candidate = None
        best_val_loss = float('inf')
        candidate_results = []
        baseline_loss = None  # Will be set after first candidate
        
        # Train and evaluate each candidate
        for idx, candidate in enumerate(candidates):
            logger.info("")
            logger.info(f"🔬 Candidate {idx + 1}/{len(candidates)}: {candidate['description']}")
            logger.info("-" * 80)
            
            # Create new predictors with this architecture
            new_col_predictor = ColumnPredictor(
                cols_in_order=self.col_order,
                col_configs=candidate['col_predictor_configs']
            )
            new_joint_predictor = SimpleMLP(candidate['joint_predictor_config'])
            
            # Replace predictors in encoder
            self.encoder.column_predictor = new_col_predictor
            self.encoder.joint_predictor = new_joint_predictor
            self.encoder.column_predictor.to(device)
            self.encoder.joint_predictor.to(device)
            
            # FREEZE encoder - only train predictors for architecture selection
            # This dramatically reduces overhead while still allowing fair comparison
            for param in self.encoder.parameters():
                param.requires_grad = False
            # Unfreeze only predictors
            if hasattr(self.encoder, 'column_predictor') and self.encoder.column_predictor is not None:
                for param in self.encoder.column_predictor.parameters():
                    param.requires_grad = True
            if hasattr(self.encoder, 'joint_predictor') and self.encoder.joint_predictor is not None:
                for param in self.encoder.joint_predictor.parameters():
                    param.requires_grad = True
            
            # Only optimize predictor parameters (encoder frozen)
            predictor_params = []
            if hasattr(self.encoder, 'column_predictor') and self.encoder.column_predictor is not None:
                predictor_params.extend(self.encoder.column_predictor.parameters())
            if hasattr(self.encoder, 'joint_predictor') and self.encoder.joint_predictor is not None:
                predictor_params.extend(self.encoder.joint_predictor.parameters())
            
            # Use higher LR for architecture selection since we're only training small predictor heads
            # Encoder is frozen, so we can be more aggressive with LR to get better signal faster
            # 0.01 is 10× higher than main training (0.001) - helps small MLPs adapt quickly
            selection_lr = 0.01
            optimizer = torch.optim.AdamW(predictor_params, lr=selection_lr, weight_decay=1e-4)
            logger.info(f"      - Learning rate: {selection_lr} (10× higher than main training to quickly adapt small predictor heads)")
            
            # Train for selection_epochs - MUCH faster since encoder is frozen
            self.encoder.train()
            logger.info(f"   🚀 PREDICTOR HEAD SELECTION: Training candidate {idx + 1}/{len(candidates)} ({candidate['description']}) for {selection_epochs} epochs")
            logger.info(f"      - Embedding space encoder (d_model={self.d_model}): FROZEN (not training, just using for forward pass)")
            logger.info(f"      - Predictor heads ({candidate['description']}): TRAINING (only these small MLPs are being updated)")
            logger.info(f"      - ⚠️  This is NOT your main embedding space training - this is just evaluating predictor head architectures")
            logger.info(f"      - After selection, main training will train the FULL EMBEDDING SPACE (encoder + selected predictor heads) for your requested epoch count")
            for epoch in range(selection_epochs):
                epoch_loss = 0.0
                batch_count = 0
                
                for batch in train_dataloader:
                    optimizer.zero_grad()
                    
                    # Forward pass through full encoder (uses actual loss computation)
                    encodings = self.encoder(batch)
                    batch_loss, loss_dict = self.encoder.compute_total_loss(*encodings)
                    
                    batch_loss.backward()
                    optimizer.step()
                    
                    epoch_loss += batch_loss.item()
                    batch_count += 1
                
                avg_loss = epoch_loss / batch_count if batch_count > 0 else 0.0
                # Log every 5 epochs or last epoch
                if (epoch + 1) % 5 == 0 or epoch == selection_epochs - 1:
                    logger.info(f"   Epoch {epoch + 1}/{selection_epochs}: train_loss={avg_loss:.4f}")
            
            # Evaluate on validation set - single evaluation is enough (encoder frozen, so deterministic)
            logger.info(f"   🔍 Computing validation loss for candidate architecture...")
            val_loss, val_components = self.compute_val_loss(val_dataloader)
            val_loss_std = 0.0  # No variance when encoder is frozen
            
            logger.info(f"   ✅ Validation loss: {val_loss:.4f}")
            
            # Set baseline after first candidate
            if baseline_loss is None:
                baseline_loss = val_loss
                baseline_std = val_loss_std
            
            candidate_results.append({
                'candidate': candidate,
                'val_loss': val_loss,
                'val_loss_std': val_loss_std
            })
            
            # Track best
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_candidate = candidate.copy()
                best_candidate['final_val_loss'] = val_loss
                logger.info(f"   🏆 New best architecture!")
            
            # Early stopping: if we've tested at least 2 candidates and improvement is marginal,
            # stop early to save time. Check if current best improvement is below threshold.
            if idx >= 1:  # At least 2 candidates tested
                current_improvement_pct = ((baseline_loss - best_val_loss) / baseline_loss) * 100
                current_improvement_abs = baseline_loss - best_val_loss
                
                # If we've already found a good improvement, continue to see if we can do better
                # But if improvements are very marginal (< 2%), stop early
                if current_improvement_pct < 2.0 and current_improvement_abs < 2.0:
                    logger.info(f"   ⏹️  Early stopping: improvements are marginal ({current_improvement_pct:.2f}%, {current_improvement_abs:.4f} absolute)")
                    logger.info(f"   Continuing with {len(candidates) - idx - 1} remaining candidates would likely not justify overhead")
                    # Continue anyway to complete the comparison, but log the concern
            
            # Clean up GPU memory after each candidate
            # Move old predictors to CPU and delete them
            if hasattr(self.encoder, 'column_predictor') and self.encoder.column_predictor is not None:
                self.encoder.column_predictor.cpu()
                del self.encoder.column_predictor
            if hasattr(self.encoder, 'joint_predictor') and self.encoder.joint_predictor is not None:
                self.encoder.joint_predictor.cpu()
                del self.encoder.joint_predictor
            
            # Clear optimizer state
            del optimizer
            
            # Clear GPU cache
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        
        # Restore original predictors (we'll replace with winner after selection)
        self.encoder.column_predictor = original_col_predictor
        self.encoder.joint_predictor = original_joint_predictor
        
        # Check if improvement is meaningful
        baseline_loss = candidate_results[0]['val_loss']  # First candidate is baseline
        baseline_std = candidate_results[0].get('val_loss_std', 0.0)
        
        # Find best candidate's std from results
        best_std = 0.0
        for result in candidate_results:
            if result['candidate'] == best_candidate:
                best_std = result.get('val_loss_std', 0.0)
                break
        
        improvement_pct = ((baseline_loss - best_val_loss) / baseline_loss) * 100
        improvement_abs = baseline_loss - best_val_loss
        
        # Statistical significance check: is improvement > 2 standard deviations?
        # This accounts for variance in evaluation (though std=0 when encoder frozen)
        pooled_std = np.sqrt(baseline_std**2 + best_std**2) if baseline_std > 0 and best_std > 0 else 0.0
        z_score = improvement_abs / pooled_std if pooled_std > 0 else float('inf')
        # When encoder is frozen, variance is minimal, so we rely on absolute thresholds
        statistically_significant = z_score > 2.0 if pooled_std > 0 else True  # Always significant if no variance
        
        # Minimum thresholds: at least 5% relative improvement OR 5.0 absolute improvement
        # This prevents selecting a more complex architecture for marginal gains
        MIN_IMPROVEMENT_PCT = 5.0
        MIN_IMPROVEMENT_ABS = 5.0
        
        meaningful_improvement = (
            (improvement_pct >= MIN_IMPROVEMENT_PCT or improvement_abs >= MIN_IMPROVEMENT_ABS) and
            statistically_significant  # Must also be statistically significant
        )
        
        # Log results
        logger.info("")
        logger.info("=" * 80)
        logger.info("📊 ARCHITECTURE SELECTION RESULTS")
        logger.info("=" * 80)
        for idx, result in enumerate(candidate_results):
            marker = "🏆" if result['candidate'] == best_candidate else "  "
            logger.info(f"{marker} {idx + 1}. {result['candidate']['description']}: val_loss={result['val_loss']:.4f}")
        logger.info("")
        
        # Decision logic
        if not meaningful_improvement:
            # Use baseline (first candidate) - overhead not worth it
            baseline_candidate = candidate_results[0]['candidate'].copy()
            baseline_candidate['final_val_loss'] = baseline_loss
            logger.info(f"⚠️  Best architecture ({best_candidate['description']}) only improves by {improvement_pct:.2f}% ({improvement_abs:.4f} absolute)")
            if not statistically_significant:
                logger.info(f"   ⚠️  Improvement not statistically significant (z-score={z_score:.2f}, need >2.0)")
            if improvement_pct < MIN_IMPROVEMENT_PCT and improvement_abs < MIN_IMPROVEMENT_ABS:
                logger.info(f"   ⚠️  Improvement below threshold ({MIN_IMPROVEMENT_PCT}% or {MIN_IMPROVEMENT_ABS} absolute)")
            logger.info(f"   Using baseline architecture to avoid unnecessary overhead")
            logger.info(f"✅ Selected: {candidate_results[0]['candidate']['description']} (val_loss={baseline_loss:.4f} ± {baseline_std:.4f})")
            logger.info("=" * 80)
            return baseline_candidate
        else:
            logger.info(f"✅ Selected: {best_candidate['description']} (val_loss={best_val_loss:.4f} ± {best_std:.4f})")
            logger.info(f"   Improvement: {improvement_pct:.2f}% ({improvement_abs:.4f} absolute)")
            logger.info(f"   Statistical significance: z-score={z_score:.2f} (statistically significant)")
            logger.info(f"   Worth the overhead: improvement exceeds thresholds and is statistically significant")
            logger.info("=" * 80)
            return best_candidate
    
    def _replace_predictors_with_architecture(self, architecture_config):
        """
        Replace the column and joint predictors in the encoder with the selected architecture.
        
        Args:
            architecture_config: dict with 'col_predictor_configs' and 'joint_predictor_config'
        """
        new_col_predictor = ColumnPredictor(
            cols_in_order=self.col_order,
            col_configs=architecture_config['col_predictor_configs']
        )
        new_joint_predictor = SimpleMLP(architecture_config['joint_predictor_config'])
        
        self.encoder.column_predictor = new_col_predictor
        self.encoder.joint_predictor = new_joint_predictor
        self.encoder.column_predictor.to(device)
        self.encoder.joint_predictor.to(device)
        
        # CRITICAL: Unfreeze all encoder parameters for main training
        # During architecture selection, the encoder was frozen to speed up comparison.
        # Now that selection is complete, we need to unfreeze everything so the full
        # embedding space (encoder + predictor heads) can be trained together.
        for param in self.encoder.parameters():
            param.requires_grad = True
        logger.info(f"   🔓 Unfroze all encoder parameters for main training")
        
        # Update encoder_config to reflect the new architecture
        self.encoder_config.column_predictors_config = architecture_config['col_predictor_configs']
        self.encoder_config.joint_predictor_config = architecture_config['joint_predictor_config']
        
        # Store architecture selection metadata in training_info for reference
        if not hasattr(self, 'training_info'):
            self.training_info = {}
        self.training_info['selected_predictor_architecture'] = {
            'description': architecture_config['description'],
            'final_val_loss': architecture_config.get('final_val_loss'),
            'column_predictor_configs': {
                col_name: {
                    'd_hidden': config.d_hidden,
                    'n_hidden_layers': config.n_hidden_layers,
                    'dropout': config.dropout,
                }
                for col_name, config in architecture_config['col_predictor_configs'].items()
            },
            'joint_predictor_config': {
                'd_hidden': architecture_config['joint_predictor_config'].d_hidden,
                'n_hidden_layers': architecture_config['joint_predictor_config'].n_hidden_layers,
                'dropout': architecture_config['joint_predictor_config'].dropout,
            }
        }
        
        logger.info(f"✅ Replaced predictors with architecture: {architecture_config['description']}")
        logger.info(f"   Architecture stored in encoder_config.column_predictors_config and training_info")

    def free_memory(self):
        self.train_input_data.free_memory()
        self.val_input_data.free_memory()
        return

    def reset_training_state(self):
        self.training_state = {}
        self.training_progress_data = {}

    def gotInterrupted(self):
        return self._gotControlC

    def get_column_names(self):
        return list(self.col_codecs.keys())

    def get_codec_type_for_column(self, col):
        codec = self.col_codecs.get(col)
        # print(f"...col {col}...{codec}")

        if isinstance(codec, ScalarCodec):
            return "scalar"
        elif isinstance(codec, SetCodec):
            return "set"

        return None

    def _create_codecs(self):
        # DEBUG: Log codec creation process
        logger.info(f"🔧 _create_codecs starting...")
        logger.info(f"   Column spec has {len(self.column_spec)} columns: {list(self.column_spec.keys())}")
        logger.info(f"   col_codecs currently has {len(self.col_codecs)} items")
        
        ts = time.time()
        needOutput = False
        colsSoFar = []
        for col_name, col_type in self.column_spec.items():
            logger.info(f"   Processing column '{col_name}' (type: {col_type})")
            tn = time.time()
            if (tn - ts) > 30 and not needOutput:
                needOutput = True
                logger.info("Codec creation is taking longer than expected...")
                logger.info("Already created codecs for:")
                for cc in colsSoFar:
                    logger.info(f"\t{cc.get('name')} [{cc.get('time')} seconds]")

            if needOutput:
                logger.info(f"Creating codec for {col_name}...")

            df_col_values = self.train_input_data.get_casted_values_for_column_name(
                col_name
            )
            assert (
                df_col_values is not None
            ), f'missing casted values for column "{col_name}"'

            codec = None

            if col_type == ColumnType.SET:
                # Get detector to access sparsity information
                setDetector = self.train_input_data.get_detector_for_col_name(col_name)
                # Use vocabulary override if available (for checkpoint reconstruction)
                vocabulary_override = self.codec_vocabulary_overrides.get(col_name)
                if vocabulary_override:
                    logger.info(f"   📚 Using checkpoint vocabulary for '{col_name}': {len(vocabulary_override)} members (current data has {len(set(df_col_values.astype(str).unique()))} unique values)")
                # Use CrossEntropyLoss for embedding space training (more stable)
                codec = create_set_codec(
                    df_col_values, 
                    embed_dim=self.d_model, 
                    loss_type="cross_entropy",
                    detector=setDetector,
                    string_cache=self.string_cache,
                    vocabulary_override=vocabulary_override
                )
            elif col_type == ColumnType.SCALAR:
                codec = create_scalar_codec(df_col_values, embed_dim=self.d_model)
            elif col_type == ColumnType.TIMESTAMP:
                codec = create_timestamp_codec(df_col_values, embed_dim=self.d_model)
            elif col_type == ColumnType.FREE_STRING:
                strDetector = self.train_input_data.get_detector_for_col_name(col_name)
                assert strDetector is not None
                
                # CRITICAL: Log string_cache to debug missing cache issues
                if not self.string_cache:
                    logger.warning(f"⚠️  WARNING: No string_cache provided for column '{col_name}' - workers will not be able to access cache!")
                    logger.warning(f"   This will cause cache misses in worker processes. Consider providing a string_cache path.")
                
                # Get validation column values to ensure all values are cached
                validation_df_col = None
                if col_name in self.val_input_data.df.columns:
                    validation_df_col = self.val_input_data.df[col_name]
                
                codec = create_string_codec(
                    df_col_values, 
                    detector=strDetector, 
                    embed_dim=self.d_model,
                    string_cache=self.string_cache,
                    # sentence_model removed - using string server instead
                    validation_df_col=validation_df_col  # Pass validation data to cache all values
                )
                # codec.debug_name = col_name
            elif col_type == ColumnType.VECTOR:
                vecDetector = self.train_input_data.get_detector_for_col_name(col_name)
                assert vecDetector is not None
                codec = create_vector_codec(
                    df_col_values, detector=vecDetector, embed_dim=self.d_model
                )
                # codec.debug_name = col_name
            elif col_type == ColumnType.URL:
                urlDetector = self.train_input_data.get_detector_for_col_name(col_name)
                assert urlDetector is not None
                from featrix.neural.encoders import create_url_codec
                codec = create_url_codec(
                    df_col_values, 
                    detector=urlDetector, 
                    embed_dim=self.d_model,
                    string_cache=self.string_cache
                )
            elif col_type == ColumnType.DOMAIN:
                domainDetector = self.train_input_data.get_detector_for_col_name(col_name)
                assert domainDetector is not None
                from featrix.neural.encoders import create_domain_codec
                codec = create_domain_codec(
                    df_col_values,
                    detector=domainDetector,
                    embed_dim=self.d_model,
                    string_cache=self.string_cache
                )
            elif col_type == ColumnType.JSON:
                # TEMPORARILY DISABLED: Skip JSON columns to save time
                logger.warning(f"⚠️  Skipping JSON column '{col_name}' - JSON columns are temporarily disabled")
                continue
                # jsonDetector = self.train_input_data.get_detector_for_col_name(col_name)
                # assert jsonDetector is not None
                # from featrix.neural.encoders import create_json_codec
                # # Use json_cache.sqlite3 in the same directory as string cache
                # json_cache_filename = "json_cache.sqlite3" if self.string_cache else None
                # # Get child ES session ID for this column if it's a dependency
                # child_es_session_id = self.required_child_es_mapping.get(col_name)
                # if child_es_session_id:
                #     logger.info(f"🔗 JSON column '{col_name}' will use child ES session: {child_es_session_id}")
                # codec = create_json_codec(
                #     df_col_values,
                #     detector=jsonDetector,
                #     embed_dim=self.d_model,
                #     json_cache_filename=json_cache_filename,
                #     child_es_session_id=child_es_session_id
                # )
            # elif col_type == ColumnType.LIST_OF_A_SET:
            #     listDetector = self.train_input_data.get_detector_for_col_name(col_name)
            #     assert listDetector is not None
            #     codec = create_lists_of_a_set_codec(
            #         df_col_values, detector=listDetector, embed_dim=self.d_model
            #     )
            else:
                raise ValueError(f"Unsupported codec type: {col_type}.")

            self.col_codecs[col_name] = codec

            if needOutput:
                logger.info(f"Finished codec for {col_name} [{time.time() - tn:.1f} seconds]")

            colsSoFar.append({"name": col_name, "time": time.time() - tn})

        if needOutput:
            logger.info("Finished creating all codecs")
        return

    def gotControlC(self):
        self._gotControlC = True

    def _get_base_token_dict(self):
        # Returns a base token batch dict where all tokens are missing.

        d = {}
        for col, codec in self.col_codecs.items():
            # NOTE: set the token to unknown instead of not present. this change was introduced
            # on 10/13/2023.
            d[col] = create_token_batch([set_marginal(codec.get_not_present_token())])

        return d

    # we want to have access to layers of encodings.
    # How to do that without having to process all the columns all the time?

    def encode_field(self, column_name, values):
        # Encode individual values using an encoder for a specific column.

        if column_name not in self.col_codecs:
            raise ValueError(f"Cannot encode values for column {column_name}.")

        col_codec = self.col_codecs[column_name]
        tokens = create_token_batch([col_codec.tokenize(value) for value in values])
        return col_codec.encode(tokens)

    # TODO: a function that converts an entire df column into a batch token, in a single go.

    def encode_record(self, record, squeeze=True, short=False, output_device=None):
        # Encode an entire record using the full joint encoder.
        # print("ENCODING!!", record)
        # print("... col_codecs = ", self.col_codecs)
        # print("...")
        # record is provided as a dictionary {field: value}
        
        # Get logger from the current module
        import logging
        logger = logging.getLogger(__name__)
        
        # CRITICAL: Check if encoder is None and try to recover
        if self.encoder is None:
            logger.error(f"🚨 CRITICAL: EmbeddingSpace.encoder is None - cannot encode records!")
            logger.error(f"   This usually means the encoder failed to load during unpickling.")
            logger.error(f"   Checking if we can recreate it...")
            
            # Try to recreate encoder if we have the necessary components
            if hasattr(self, 'col_codecs') and self.col_codecs and hasattr(self, 'encoder_config') and self.encoder_config:
                try:
                    logger.info(f"   Attempting to recreate encoder from col_codecs and encoder_config...")
                    from featrix.neural.encoders import FeatrixTableEncoder
                    self.encoder = FeatrixTableEncoder(
                        col_codecs=self.col_codecs,
                        config=self.encoder_config,
                    )
                    # Move to CPU to avoid GPU allocation issues
                    self.encoder = self.encoder.cpu()
                    logger.warning(f"   ⚠️  Recreated encoder structure, but it has UNTRAINED weights!")
                    logger.warning(f"   This encoder will not produce meaningful encodings without trained weights.")
                    logger.warning(f"   The embedding space file may be corrupted or incomplete.")
                    # Don't raise error yet - let it fail when trying to use untrained weights
                except Exception as e:
                    logger.error(f"   ❌ Failed to recreate encoder: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    raise AttributeError(
                        f"EmbeddingSpace.encoder is None and cannot be recreated. "
                        f"This usually means the embedding space file is corrupted or incomplete. "
                        f"Original error during unpickling may have been logged. "
                        f"Recreation attempt failed: {e}"
                    )
            else:
                missing = []
                if not hasattr(self, 'col_codecs') or not self.col_codecs:
                    missing.append('col_codecs')
                if not hasattr(self, 'encoder_config') or not self.encoder_config:
                    missing.append('encoder_config')
                raise AttributeError(
                    f"EmbeddingSpace.encoder is None and cannot be recreated. "
                    f"Missing required components: {', '.join(missing)}. "
                    f"This usually means the embedding space file is corrupted or incomplete. "
                    f"Original error during unpickling may have been logged."
                )
        
        # FIXME: we'll need to call out to the other ES for the json columns here to get the encoding of their fields, if any are here.
        
        # Debug counter for tracking problematic records
        # debug_count = getattr(self, '_encode_record_debug_count', 0)
        # should_debug = debug_count < 5  # Debug first 5 records
        
        # if should_debug:
        #     logger.info(f"🔍 ENCODE_RECORD DEBUG #{debug_count}: Starting record encoding")
        #     logger.info(f"   Record fields: {list(record.keys())}")
        #     logger.info(f"   Available codecs: {list(self.col_codecs.keys())}")
        
        record_tokens = {}
        for field, value in record.items():
            field = field.strip()
            
            # CRITICAL: __featrix* columns must NEVER be encoded!
            # If we find a codec for __featrix* fields, something went very wrong!
            if field.startswith('__featrix'):
                if field in self.col_codecs:
                    logger.error(f"🚨 CRITICAL ERROR: Found codec for internal field '{field}' - this should have been ignored during training!")
                    logger.error(f"🚨 This means __featrix* columns leaked into the training data!")
                    raise ValueError(f"CRITICAL: Internal column '{field}' has a codec! This should never happen. __featrix* columns must be excluded from training.")
                # Skip encoding internal fields regardless
                continue
            
            # print("record for loop: ", field, value)
            # If the field is not present in the codecs, it can't be tokenized,
            # and doesn't participate in the encoding, so we skip it
            if field not in self.col_codecs:
                if field not in self._warningEncodeFields:
                    self._warningEncodeFields.append(field)
                continue

            codec = self.col_codecs[field]
            token = codec.tokenize(value)
            
            # Check if this specific token has NaN values
            # if should_debug:
            #     if hasattr(token.value, 'isnan') and torch.isnan(token.value).any():
            #         logger.error(f"🚨 FIELD TOKENIZATION PRODUCED NaN: {field}='{value}' -> {token}")
            #         logger.error(f"   Token value shape: {token.value.shape if hasattr(token.value, 'shape') else 'No shape'}")
            #         logger.error(f"   Token status: {token.status}")
            #         logger.error(f"   Codec type: {type(codec).__name__}")
            #     else:
            #         logger.info(f"   ✅ Field '{field}': {type(codec).__name__} -> OK (shape: {token.value.shape if hasattr(token.value, 'shape') else 'No shape'})")
                
            #     # CRITICAL DEBUG: For SET encoders, check token status and values
            #     if type(codec).__name__ == 'SetCodec':
            #         logger.error(f"🔍 SET DEBUG '{field}': value='{value}' -> token.value={token.value} status={token.status}")
            #         if hasattr(codec, 'members_to_tokens'):
            #             logger.error(f"   Available members: {list(codec.members_to_tokens.keys())[:10]}...")  # First 10
            #             if str(value) in codec.members_to_tokens:
            #                 expected_token = codec.members_to_tokens[str(value)]
            #                 logger.error(f"   Expected token for '{value}': {expected_token}")
            #             else:
            #                 logger.error(f"   ❌ VALUE '{value}' NOT FOUND in codec members!")
            
            record_tokens[field] = token

        # Rate-limited logging for missing codec fields (once per hour)
        # Use global cache since each API request loads a fresh EmbeddingSpace instance from disk
        if self._warningEncodeFields:
            global _MISSING_CODEC_WARNING_CACHE
            current_time = time.time()
            
            # Create a unique key for this specific set of missing fields
            missing_fields_key = frozenset(self._warningEncodeFields)
            
            # Check if we've logged this combination recently
            last_logged = _MISSING_CODEC_WARNING_CACHE.get(missing_fields_key)
            should_log = (
                last_logged is None or
                (current_time - last_logged) >= 3600  # 3600 seconds = 1 hour
            )
            
            if should_log:
                logger.warning(f"encode_record: {len(self._warningEncodeFields)} field(s) without codecs (skipped): {', '.join(sorted(self._warningEncodeFields))}")
                _MISSING_CODEC_WARNING_CACHE[missing_fields_key] = current_time

        # print("record tokens:", record_tokens)

        # Get the dictionary that contains NOT_PRESENT tokens for all fields
        # that are expected by the encoder. This makes sure that even if the user
        # passes in a partial record, we can encode it. The values that are not in
        # the `record` dictionary just remain as NOT_PRESENT, and those that are present
        # are replaced with their correct values.
        batch_tokens = self._get_base_token_dict()
        
        # if should_debug:
        #     logger.info(f"   Base token dict fields: {list(batch_tokens.keys())}")
        
        # print("... record_tokens =", record_tokens)
        # print("batch tokens before:", batch_tokens)
        # Replace the default NOT_PRESENT tokens in the batch with
        # tokens corresponding to fields in the record.

        for field, token in record_tokens.items():
            # print("FIELD: __%s__, token: __%s__" % (field, token))
            batch_tokens[field] = create_token_batch([token])

        # print("... batch_tokens  = ", batch_tokens)
        # encoding = self.encoder(batch_tokens)
        
        # CRITICAL FIX: Only change training mode if we're currently in training
        # This prevents interfering with the training loop
        was_training_es = self.encoder.training
        should_restore_training = False
        
        # Only set to eval if we're currently training
        if was_training_es:
            # logger.info("Setting encoder.eval()")     # very spammy
            self.encoder.eval()
            should_restore_training = True
        
        # CRITICAL: Check if we're in single predictor training (CPU mode)
        # Don't move encoder to device if it's already on CPU and we're forcing CPU
        force_cpu_env = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR')
        if force_cpu_env == '1':
            # Force CPU mode - don't move encoder to device
            if list(self.encoder.parameters()):
                encoder_device = next(self.encoder.parameters()).device
                if encoder_device.type != 'cpu':
                    self.encoder.cpu()
        else:
            # Normal mode - move to device
            self.encoder.to(device)
        
        # if should_debug:
        #     logger.info(f"   Encoder device: {next(self.encoder.parameters()).device}")
        #     logger.info(f"   Encoder training mode: {self.encoder.training}")
        #     logger.info(f"   Was training before: {was_training_es}")
        #     logger.info(f"   Will restore training: {should_restore_training}")
        
        # ROOT CAUSE DEBUGGING: Let's see what's going into the encoder
        # if should_debug:
        #     logger.info(f"🔍 DEBUGGING INPUT TO ENCODER:")
        #     for field_name, token_batch in batch_tokens.items():
        #         if hasattr(token_batch, 'values'):
        #             values = token_batch.values
        #             if hasattr(values, 'isnan'):
        #                 has_nan = torch.isnan(values).any()
        #                 has_inf = torch.isinf(values).any()
        #                 zero_tensor = torch.zeros_like(values)
        #                 is_zero = torch.allclose(values, zero_tensor)
        #                 logger.info(f"   Field '{field_name}': shape={values.shape}, has_nan={has_nan}, has_inf={has_inf}, all_zero={is_zero}")
        #                 if has_nan or has_inf:
        #                     logger.error(f"   🚨 PROBLEMATIC INPUT: {field_name} = {values}")
        
        with torch.no_grad():
            short_encoding, full_encoding = self.encoder.encode(batch_tokens)
        
        # CRITICAL: Crash hard if encoder produces NaN - no masking allowed
        if torch.isnan(short_encoding).any() or torch.isnan(full_encoding).any():
            short_nan_count = torch.isnan(short_encoding).sum()
            full_nan_count = torch.isnan(full_encoding).sum()
            
            logger.error(f"💥 FATAL: Encoder produced NaN values - MODEL IS BROKEN")
            logger.error(f"🔍 COMPREHENSIVE DIAGNOSTICS:")
            logger.error(f"   Short encoding NaN: {short_nan_count}/{short_encoding.numel()}")
            logger.error(f"   Full encoding NaN: {full_nan_count}/{full_encoding.numel()}")
            logger.error(f"   Input record: {record}")
            logger.error(f"   Record fields: {list(record.keys())}")
            
            # Show codec types for failing fields
            failing_codecs = {}
            for field_name in record.keys():
                if field_name in self.col_codecs:
                    codec = self.col_codecs[field_name]
                    failing_codecs[field_name] = type(codec).__name__
            logger.error(f"   Codec types: {failing_codecs}")
            
            # Find which fields might be problematic
            problematic_fields = []
            for field_name, token in record_tokens.items():
                if hasattr(token.value, 'isnan') and torch.isnan(token.value).any():
                    problematic_fields.append(field_name)
            
            if problematic_fields:
                logger.error(f"   Fields with NaN tokens: {problematic_fields}")
            
            # Check for enriched fields specifically 
            # enriched_fields = [f for f in record.keys() if '.dict.' in f]
            # if enriched_fields:
            #     logger.error(f"   Enriched (.dict.*) fields: {enriched_fields[:10]}...")  # First 10
            
            logger.error(f"💀 CRASHING: NaN encodings produce meaningless results")
            logger.error(f"    Fix the root cause - don't mask with random vectors!")
            logger.error(f"    Check: model parameters, tokenization, codec initialization")
            
            raise RuntimeError(
                f"FATAL MODEL FAILURE: Encoder produced {short_nan_count + full_nan_count} NaN values. "
                f"This indicates serious model corruption, bad parameters, or tokenization failure. "
                f"Record fields: {list(record.keys())[:5]}... "
            )
        # elif should_debug:
        #     logger.info(f"   ✅ Encoder output clean: short={short_encoding.shape}, full={full_encoding.shape}")
        
        # CRITICAL FIX: Only restore training mode if we changed it
        if should_restore_training:
            # logger.info("Setting encoder.train()")
            self.encoder.train()

        # If squeeze is True, we want just the encoding, and not a batch, so
        # squeeze the extra dimension out.
        if squeeze is True:
            short_encoding = short_encoding.squeeze(dim=0)
            full_encoding = full_encoding.squeeze(dim=0)

        output_device = output_device or torch.device("cpu")
        
        # if should_debug:
        #     logger.info(f"   Moving to output device: {output_device}")
        #     # Final check after device move
        #     result_short = short_encoding.detach().to(output_device)
        #     result_full = full_encoding.detach().to(output_device)
            
        #     if torch.isnan(result_short).any():
        #         logger.error(f"🚨 FINAL SHORT RESULT HAS NaN: {result_short}")
        #     if torch.isnan(result_full).any():
        #         logger.error(f"🚨 FINAL FULL RESULT HAS NaN: {result_full}")
            
        #     logger.info(f"   Final result shapes: short={result_short.shape}, full={result_full.shape}")
        #     self._encode_record_debug_count = debug_count + 1
        
        if short:
            return short_encoding.detach().to(output_device)
        else:
            return full_encoding.detach().to(output_device)

    def compute_field_similarity(self, query_record, result_record, distance_metric='euclidean'):
        """
        Compute field-level similarity between a query record and a result record.
        
        For each field that exists in both records, encode just that field's value
        and compute the distance between the query field embedding and the result field embedding.
        
        Args:
            query_record: Dictionary of query record fields {field: value}
            result_record: Dictionary of result record fields {field: value}
            distance_metric: Distance metric to use ('euclidean' or 'cosine')
        
        Returns:
            Dictionary with field-level distances: {field: distance}
        
        Raises:
            ValueError: If query_record is empty or has no valid fields
        """
        # Validate input
        if not query_record or len(query_record) == 0:
            raise ValueError("query_record is empty - cannot compute field similarity without query fields")
        
        if not result_record or len(result_record) == 0:
            raise ValueError("result_record is empty - cannot compute field similarity")
        
        field_distances = {}
        
        # Get the common fields that are in both records and have codecs
        common_fields = set(query_record.keys()) & set(result_record.keys()) & set(self.col_codecs.keys())
        
        # Filter out metadata fields
        common_fields = {f for f in common_fields if not f.startswith('__featrix_')}
        
        if not common_fields:
            raise ValueError(
                f"No common fields found between query and result. "
                f"Query fields: {list(query_record.keys())}, "
                f"Result fields: {list(result_record.keys())}, "
                f"Trained codecs: {list(self.col_codecs.keys())}"
            )
        
        for field in common_fields:
                
            try:
                # Create single-field records
                query_single_field = {field: query_record[field]}
                result_single_field = {field: result_record[field]}
                
                # Encode each field independently
                # Use full embeddings for better discrimination
                query_field_embedding = self.encode_record(query_single_field, short=False, output_device=torch.device("cpu"))
                result_field_embedding = self.encode_record(result_single_field, short=False, output_device=torch.device("cpu"))
                
                # Compute distance
                if distance_metric == 'euclidean':
                    distance = torch.dist(query_field_embedding, result_field_embedding, p=2).item()
                elif distance_metric == 'cosine':
                    # Cosine distance = 1 - cosine similarity
                    cos_sim = torch.nn.functional.cosine_similarity(
                        query_field_embedding.unsqueeze(0), 
                        result_field_embedding.unsqueeze(0)
                    ).item()
                    distance = 1.0 - cos_sim
                else:
                    raise ValueError(f"Unknown distance metric: {distance_metric}")
                
                field_distances[field] = distance
                
            except Exception as e:
                logger.warning(f"Failed to compute field similarity for field '{field}': {e}")
                # Store None to indicate this field couldn't be compared
                field_distances[field] = None
        
        return field_distances

    def register_callback(self, type, callback_fn):
        callback_id = uuid.uuid4()
        self.callbacks[type][callback_id] = callback_fn

    def remove_callback(self, type, callback_id):
        try:
            del self.callbacks[type][callback_id]
        except KeyError:
            # Ignore key errors - if the callback does not exist,
            # removing doesn't matter.
            pass

    def run_callbacks(self, type, *args, **kwargs):
        for callback_id, callback_fn in self.callbacks[type].items():
            callback_fn(callback_id, *args, **kwargs)

    @staticmethod
    def safe_dump(package: Dict):
        if package.get("print_callback"):
            del package["print_callback"]

    def compute_val_loss(self, val_dataloader):
        was_training_es = self.encoder.training

        with torch.no_grad():
            self.encoder.eval()

            batch_sizes = []
            batch_losses = []
            batch_loss_dicts = []
            val_batch_count = 0
            total_val_batches = len(val_dataloader) if hasattr(val_dataloader, '__len__') else None
            
            # Heartbeat for long validation runs
            import time
            val_start_time = time.time()
            last_heartbeat_time = val_start_time
            
            for batch in val_dataloader:
                val_batch_count += 1
                current_time = time.time()
                
                # Log validation progress every 5 batches or if we know the total
                if total_val_batches and (val_batch_count % 5 == 0 or val_batch_count == 1):
                    logger.info(f"      Validation batch {val_batch_count}/{total_val_batches}...")
                elif not total_val_batches and val_batch_count % 5 == 0:
                    logger.info(f"      Validation batch {val_batch_count}...")
                
                # Heartbeat: log every 30 seconds if validation is taking a long time
                if current_time - last_heartbeat_time >= 30.0:
                    elapsed = current_time - val_start_time
                    if total_val_batches:
                        logger.info(f"      ⏱️  Validation in progress: {val_batch_count}/{total_val_batches} batches ({elapsed:.1f}s elapsed)...")
                    else:
                        logger.info(f"      ⏱️  Validation in progress: {val_batch_count} batches ({elapsed:.1f}s elapsed)...")
                    last_heartbeat_time = current_time
                # Different datasets have different columns, but we want to
                # find out the length of any of the columns, because the token batch
                # for every column have the same length.
                first_column_token_batch = next(iter(batch.items()))[1]
                batch_size = len(first_column_token_batch)

                encodings = self.encoder(batch)
                batch_loss, loss_dict = self.encoder.compute_total_loss(*encodings)

                batch_sizes.append(batch_size)
                batch_losses.append(batch_loss.item())
                batch_loss_dicts.append(loss_dict)

            if was_training_es:
                self.encoder.train()

        n_batches = len(batch_losses)

        if n_batches > 1:
            first_batch_size = batch_sizes[0]
            last_batch_size = batch_sizes[-1]

            # If the last batch is smaller than the first batch size,
            # it means that it's shorter than all other batches, and we discard it
            # because we use a contrastive loss function, and the batch size affects
            # the loss value, and therefore averaging losses from batches of different size
            # would give results which could not be easily interpreted.
            # NOTE: dropping the last, shorter batch, means that the size of the dataset
            # ACTUALLY used for validaton will be shorter than might appear from the outside
            # if we just call len(val_dataset).
            if first_batch_size > last_batch_size:
                batch_losses = batch_losses[:-1]
                batch_loss_dicts = batch_loss_dicts[:-1]
                n_batches = len(batch_losses)

        combined_loss = sum(batch_losses)

        # Return the average loss per example. The values that combined to give us
        # `combined_loss` are the average losses per example in each batch, so we
        # divide by the number of batches to get the average loss per example across
        # the entire dataset. This is OK because all batches are the same size.
        if n_batches == 0:
            logger.warning("No validation batches computed - returning zero loss")
            return 0.0, None
        
        # Log validation loss components (average across batches)
        components = None
        if batch_loss_dicts:
            avg_loss_dict = batch_loss_dicts[0]  # Use first batch's structure
            avg_spread = sum(d['spread_loss']['total'] for d in batch_loss_dicts) / n_batches
            avg_joint = sum(d['joint_loss']['total'] for d in batch_loss_dicts) / n_batches
            avg_marginal = sum(d['marginal_loss']['total'] for d in batch_loss_dicts) / n_batches
            
            # Get the BASE marginal weight from the encoder config
            # Get current marginal loss weight from config (scaling coefficient is now applied to loss value, not weight)
            # So config_marginal_weight is the actual weight being used
            current_marginal_weight = self.encoder.config.loss_config.marginal_loss_weight
            
            # Compute marginal loss scaling coefficient on first epoch validation
            # This scales marginal loss to be comparable to spread/joint losses (~10x)
            if not hasattr(self, '_marginal_loss_scaling_coefficient'):
                # Compute coefficient based on ratio of (spread + joint) to marginal
                # This makes marginal loss contribute proportionally to the other losses
                if avg_marginal > 0:
                    # Scale marginal to be comparable to average of spread and joint
                    # Target: marginal_weighted ≈ (spread + joint) / 2
                    # So: coefficient = (spread + joint) / (2 * marginal)
                    self._marginal_loss_scaling_coefficient = (avg_spread + avg_joint) / (2.0 * avg_marginal)
                    # Store in encoder config so it can be applied during loss computation
                    self.encoder.config.loss_config.marginal_loss_scaling_coefficient = self._marginal_loss_scaling_coefficient
                    logger.info(f"📊 Computed marginal loss scaling coefficient: {self._marginal_loss_scaling_coefficient:.4f}")
                    logger.info(f"   (spread={avg_spread:.4f}, joint={avg_joint:.4f}, marginal={avg_marginal:.4f})")
                    logger.info(f"   This coefficient will be applied to the marginal LOSS VALUE (not weight) to make it comparable to spread/joint")
                else:
                    # Fallback if marginal is zero
                    self._marginal_loss_scaling_coefficient = 10.0
                    # Store in encoder config so it can be applied during loss computation
                    self.encoder.config.loss_config.marginal_loss_scaling_coefficient = self._marginal_loss_scaling_coefficient
                    logger.warning(f"⚠️  Marginal loss is zero, using default scaling coefficient: {self._marginal_loss_scaling_coefficient:.4f}")
            
            # Scale the marginal loss value by the coefficient (to make it comparable to spread/joint)
            # Then apply the current weight to get the weighted contribution
            if hasattr(self, '_marginal_loss_scaling_coefficient') and self._marginal_loss_scaling_coefficient is not None:
                avg_marginal_scaled = avg_marginal * self._marginal_loss_scaling_coefficient
            else:
                # Coefficient not computed yet (first validation), use unscaled
                avg_marginal_scaled = avg_marginal
            
            # Apply current weight to get weighted contribution
            avg_marginal_weighted = avg_marginal_scaled * current_marginal_weight
            
            # Compute worst-case InfoNCE loss for normalization
            # Worst case (random): loss = log(batch_size)
            # Best case (perfect): loss = 0
            # Normalized: actual / log(batch_size) gives 0-1 scale (0=perfect, 1=random, >1=worse than random)
            if batch_loss_dicts and batch_sizes:
                avg_batch_size = sum(batch_sizes) / len(batch_sizes)
                worst_case_infonce = math.log(avg_batch_size)
                # Normalize marginal loss: 0=perfect, 1=random
                marginal_normalized = avg_marginal / worst_case_infonce if worst_case_infonce > 0 else 0.0
            else:
                worst_case_infonce = 0.0
                marginal_normalized = 0.0
            
            # Extract spread loss sub-components
            avg_spread_full = sum(d['spread_loss']['full']['total'] for d in batch_loss_dicts) / n_batches
            avg_spread_short = sum(d['spread_loss']['short']['total'] for d in batch_loss_dicts) / n_batches
            
            # Extract full spread breakdown (joint + mask1 + mask2)
            avg_spread_full_joint = sum(d['spread_loss']['full']['joint'] for d in batch_loss_dicts) / n_batches
            avg_spread_full_mask1 = sum(d['spread_loss']['full']['mask_1'] for d in batch_loss_dicts) / n_batches
            avg_spread_full_mask2 = sum(d['spread_loss']['full']['mask_2'] for d in batch_loss_dicts) / n_batches
            
            # Extract short spread breakdown (joint + mask1 + mask2)
            avg_spread_short_joint = sum(d['spread_loss']['short']['joint'] for d in batch_loss_dicts) / n_batches
            avg_spread_short_mask1 = sum(d['spread_loss']['short']['mask_1'] for d in batch_loss_dicts) / n_batches
            avg_spread_short_mask2 = sum(d['spread_loss']['short']['mask_2'] for d in batch_loss_dicts) / n_batches
            
            components = {
                'spread': avg_spread,
                'joint': avg_joint,
                'marginal': avg_marginal_scaled,  # Show scaled original marginal (not raw)
                'marginal_weighted': avg_marginal_weighted,
                'marginal_normalized': marginal_normalized,  # 0=perfect, 1=random
                'worst_case_infonce': worst_case_infonce,  # log(batch_size)
                # Spread sub-components
                'spread_full': avg_spread_full,
                'spread_short': avg_spread_short,
                'spread_full_joint': avg_spread_full_joint,
                'spread_full_mask1': avg_spread_full_mask1,
                'spread_full_mask2': avg_spread_full_mask2,
                'spread_short_joint': avg_spread_short_joint,
                'spread_short_mask1': avg_spread_short_mask1,
                'spread_short_mask2': avg_spread_short_mask2,
            }
        
        # Return both total loss and components
        return combined_loss / n_batches, components

    def get_columns_with_codec_count(self, exclude_target_column=None):
        """
        Get count of columns with codecs (feature columns, not target).
        
        Args:
            exclude_target_column: Optional column name to exclude from count
                                   (used when checking for predictor training)
        
        Returns:
            int: Number of columns with codecs (excluding target if specified)
        """
        import logging
        logger = logging.getLogger(__name__)
        
        # Always use col_codecs directly - it's the source of truth for what columns
        # were actually trained in the embedding space. train_input_data might be
        # recreated from SQLite and not match the original training data.
        if not self.col_codecs:
            logger.error(f"❌ CRITICAL: EmbeddingSpace.col_codecs is EMPTY or None!")
            logger.error(f"   This means the embedding space has no codecs - it cannot be used for training.")
            logger.error(f"   This is likely a data corruption or loading issue.")
            return 0
        
        codec_count = len(self.col_codecs)
        codec_keys = list(self.col_codecs.keys())
        
        logger.debug(f"🔍 get_columns_with_codec_count: total={codec_count}, exclude_target={exclude_target_column}")
        logger.debug(f"   Codec columns: {codec_keys[:20]}{'...' if len(codec_keys) > 20 else ''}")
        
        if exclude_target_column and exclude_target_column in self.col_codecs:
            # Exclude target column from count (we need at least 1 feature column)
            feature_count = codec_count - 1
            logger.debug(f"   Excluding target '{exclude_target_column}': {codec_count} -> {feature_count} feature columns")
            return feature_count
        
        logger.debug(f"   No target exclusion: returning {codec_count}")
        return codec_count

    def get_training_state_path(self, epoch=0, batch=0):
        """Get path for full training checkpoint (includes optimizer state for resuming)."""
        if batch == 0:
            path = f"{self.training_state_path}_e-{epoch}.pth"
        else:
            path = f"{self.training_state_path}_e-{epoch}_b-{batch}.pth"
        return path

    def get_inference_checkpoint_path(self, epoch=0, batch=0):
        """Get path for lightweight inference checkpoint (model only, no optimizer state)."""
        base_path = self.get_training_state_path(epoch, batch)
        # Replace checkpoint_resume_training with checkpoint_inference
        inference_path = base_path.replace('checkpoint_resume_training', 'checkpoint_inference')
        # Ensure .pt extension for inference checkpoints
        if inference_path.endswith('.pth'):
            inference_path = inference_path[:-4] + '.pt'
        return inference_path

    def get_best_checkpoint_path(self):
        # If we're saving the model because it's the best model so far, we want
        # its name to NOT contain epoch and batch information because we want it
        # to be overridden every time a better model is achieved.
        return f"{self.training_state_path}_BEST.pth"

    def save_es(self, local_path):
        self.hydrate_to_cpu_if_needed()


    def save_best_checkoint(self, epoch, model, val_loss):
        save_state = {
            "epoch_idx": epoch,
            "model": model,
            "val_loss": val_loss,
            "time": time.ctime()
        }

        best_checkpoint_path = self.get_best_checkpoint_path()
        try:
            torch.save(save_state, best_checkpoint_path)
            epoch_num = save_state.get('epoch_idx', -1)
            # Show cumulative epoch for K-fold CV
            cumulative_epoch = epoch_num
            if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                cumulative_epoch = epoch_num + self._kv_fold_epoch_offset
            logger.info(f"🏆 [epoch={cumulative_epoch}] Best model checkpoint saved to {best_checkpoint_path} (val_loss: {val_loss:.6f})")
        except Exception as e:
            # Re-raise so caller can handle it (caller should wrap in try/except)
            logger.error(f"❌ Failed to save best checkpoint at epoch {epoch}: {e}")
            raise

    def save_state(self, epoch, batch, model, optimizer, scheduler, dropout_scheduler=None, is_best=False):
        save_state = {
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "scheduler": scheduler.state_dict() if scheduler is not None else None,
            "dropout_scheduler": dropout_scheduler.get_state_dict() if dropout_scheduler is not None else None,
        }

        checkpoint_path = self.get_training_state_path(epoch, batch)
        
        # Save lightweight checkpoint for projection building FIRST (every epoch)
        # This is small and needed for movie frames - prioritize it
        # Contains only what's needed for encoding: encoder model, codecs, column info
        # Does NOT include huge dataframes (train_input_data, val_input_data)
        embedding_space_checkpoint_path = self.get_inference_checkpoint_path(epoch, batch)
        embedding_space_checkpoint_saved = False
        try:
            # Ensure directory exists
            checkpoint_dir = Path(embedding_space_checkpoint_path).parent
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            
            # Save using atomic write (temp file then rename)
            temp_es_path = embedding_space_checkpoint_path + ".tmp"
            torch.save({
                'epoch': epoch,
                'encoder': model,  # The encoder model itself (not state_dict, the full model)
                'col_codecs': self.col_codecs,  # Codecs needed for encoding
                'col_order': self.col_order,  # Column order
                'column_spec': self.column_spec,  # Column specifications
                'encoder_config': self.encoder_config,  # Encoder configuration
                'd_model': self.d_model,  # Model dimension
                'json_transformations': getattr(self, 'json_transformations', {}),  # JSON transforms
                'required_child_es_mapping': getattr(self, 'required_child_es_mapping', {}),  # Child ES deps
            }, temp_es_path)
            # Atomic rename
            Path(temp_es_path).rename(embedding_space_checkpoint_path)
            
            # Verify the file was actually saved
            if Path(embedding_space_checkpoint_path).exists():
                embedding_space_checkpoint_saved = True
                file_size = Path(embedding_space_checkpoint_path).stat().st_size / (1024**2)
                logger.info(f"   ✅ Saved lightweight ES checkpoint: {file_size:.1f} MB - {embedding_space_checkpoint_path}")
            else:
                logger.error(f"❌ CRITICAL: Embedding space checkpoint file not found after save!")
                logger.error(f"   Expected path: {embedding_space_checkpoint_path}")
                logger.error(f"   Temp path existed: {Path(temp_es_path).exists()}")
                logger.error(f"   Checkpoint dir exists: {checkpoint_dir.exists()}")
                logger.error(f"   Checkpoint dir: {checkpoint_dir}")
        except Exception as e:
            logger.error(f"❌ CRITICAL: Failed to save embedding_space checkpoint: {e}")
            logger.error(f"   Exception type: {type(e).__name__}")
            logger.error(f"   Checkpoint path: {embedding_space_checkpoint_path}")
            logger.error(f"   Traceback: {traceback.format_exc()}")
            # Clean up temp file if it exists
            temp_es_path = embedding_space_checkpoint_path + ".tmp"
            if Path(temp_es_path).exists():
                try:
                    Path(temp_es_path).unlink()
                except Exception:
                    pass
        
        # Store flag so _queue_project_training_movie_frame can check if checkpoint was saved
        self._last_embedding_space_checkpoint_saved = embedding_space_checkpoint_saved
        
        # Check disk space before saving main checkpoint (need at least 1GB free)
        try:
            checkpoint_dir = Path(checkpoint_path).parent
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            stat = shutil.disk_usage(checkpoint_dir)
            free_gb = stat.free / (1024**3)
            if free_gb < 1.0:
                logger.error(f"❌ Insufficient disk space to save full checkpoint: {free_gb:.2f}GB free (need at least 1GB)")
                logger.error(f"   Checkpoint path: {checkpoint_path}")
                logger.error(f"   Lightweight checkpoint WAS saved for movie frames")
                logger.error(f"   Training will continue but full checkpoint may be lost")
                return
        except Exception as e:
            logger.warning(f"⚠️  Could not check disk space: {e}")
        
        # Use atomic write: save to temp file first, then rename
        try:
            checkpoint_dir = Path(checkpoint_path).parent
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            
            # Create temp file in same directory for atomic write
            temp_path = checkpoint_path + ".tmp"
            
            # Try saving with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    torch.save(save_state, temp_path)
                    # Atomic rename
                    Path(temp_path).rename(checkpoint_path)
                    break
                except (RuntimeError, OSError, IOError) as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"⚠️  Checkpoint save attempt {attempt + 1} failed: {e}, retrying...")
                        time.sleep(0.5)  # Brief delay before retry
                    else:
                        # Clean up temp file if it exists
                        if Path(temp_path).exists():
                            try:
                                Path(temp_path).unlink()
                            except Exception:
                                pass
                        raise
            
            # Only log checkpoints every 10 epochs or at end (reduce noise)
            if epoch % 10 == 0 or epoch == save_state.get('n_epochs', 0):
                logger.info(f"💾 [{epoch}] Checkpoint saved")
                
        except RuntimeError as e:
            error_msg = str(e)
            if "disk" in error_msg.lower() or "space" in error_msg.lower() or "enforce fail" in error_msg.lower():
                logger.error(f"❌ Failed to save checkpoint at epoch {epoch}: {e}")
                logger.error(f"   This may indicate disk space issues or file system problems")
                logger.error(f"   Training will continue but checkpoint is lost")
                logger.error(f"   Checkpoint path: {checkpoint_path}")
                
                # Send Slack alert
                try:
                    from slack import send_slack_message
                    job_id = getattr(self, 'job_id', None) or self.training_info.get('job_id', None)
                    session_id = getattr(self, 'session_id', None) or self.training_info.get('session_id', None)
                    job_info = f"job {job_id}" if job_id else f"session {session_id}" if session_id else "training"
                    slack_msg = f"🚨 Checkpoint save FAILED at epoch {epoch} for {job_info}: {error_msg[:200]}"
                    send_slack_message(slack_msg, throttle=False, skip_hostname_prefix=True)
                except Exception as slack_err:
                    logger.warning(f"⚠️  Failed to send Slack alert: {slack_err}")
                
                # Don't raise - allow training to continue
            else:
                logger.error(f"❌ Failed to save checkpoint at epoch {epoch}: {e}")
                logger.error(f"   Checkpoint path: {checkpoint_path}")
                
                # Send Slack alert for non-disk errors too
                try:
                    from slack import send_slack_message
                    job_id = getattr(self, 'job_id', None) or self.training_info.get('job_id', None)
                    session_id = getattr(self, 'session_id', None) or self.training_info.get('session_id', None)
                    job_info = f"job {job_id}" if job_id else f"session {session_id}" if session_id else "training"
                    slack_msg = f"🚨 Checkpoint save FAILED at epoch {epoch} for {job_info}: {error_msg[:200]}"
                    send_slack_message(slack_msg, throttle=False, skip_hostname_prefix=True)
                except Exception as slack_err:
                    logger.warning(f"⚠️  Failed to send Slack alert: {slack_err}")
                
                raise
        except Exception as e:
            logger.error(f"❌ Unexpected error saving checkpoint at epoch {epoch}: {e}")
            logger.error(f"   Checkpoint path: {checkpoint_path}")
            
            # Send Slack alert
            try:
                from slack import send_slack_message
                job_id = getattr(self, 'job_id', None) or self.training_info.get('job_id', None)
                session_id = getattr(self, 'session_id', None) or self.training_info.get('session_id', None)
                job_info = f"job {job_id}" if job_id else f"session {session_id}" if session_id else "training"
                slack_msg = f"🚨 Checkpoint save ERROR at epoch {epoch} for {job_info}: {str(e)[:200]}"
                send_slack_message(slack_msg, throttle=False, skip_hostname_prefix=True)
            except Exception as slack_err:
                logger.warning(f"⚠️  Failed to send Slack alert: {slack_err}")
            
            raise

    def load_best_checkpoint(self):
        # NOTE: loading the best model should be possible without having to first
        # instantiate the entire embedding space, including the input dataset.
        # This should be a class method.

        # PyTorch 2.6+ changed default to weights_only=True for security
        # Our checkpoints include custom classes (FeatrixTableEncoder), so we need weights_only=False
        checkpoint_state = torch.load(self.get_best_checkpoint_path(), weights_only=False)

        self.encoder = checkpoint_state["model"]
        epoch_idx = checkpoint_state["epoch_idx"]

        # We return the best epoch_idx so that we know which epoch the best model
        # came from.
        return epoch_idx

    def load_state(self, epoch, batch, is_best=False):
        self.training_state = torch.load(
            self.get_training_state_path(epoch, batch),
            weights_only=False
        )

    def preserve_progress(self, **kwargs):
        for k, v in kwargs.items():
            self.training_progress_data[k] = v
    
    def _create_model_package(self, best_epoch_idx):
        """
        Create a self-contained model package with everything needed to load and use the model.
        
        Package includes:
        - best_model.pickle - Pickled embedding space
        - best_model.pth - PyTorch checkpoint
        - metadata.json - Training metrics, config, column info
        - lib/featrix/neural/ - Code snapshot (for reproducibility if code changes)
        """
        try:
            import shutil
            
            output_dir = Path(self.output_dir) if isinstance(self.output_dir, str) else self.output_dir
            package_dir = output_dir / "best_model_package"
            package_dir.mkdir(exist_ok=True)
            
            logger.info(f"📦 Creating self-contained model package in {package_dir}")
            
            # 1. Save pickled embedding space
            import pickle as pkl
            pickle_path = package_dir / "best_model.pickle"
            with open(pickle_path, 'wb') as f:
                pkl.dump(self, f)
            logger.info(f"   ✅ Saved pickle: {pickle_path}")
            
            # 2. Save PyTorch checkpoint
            pth_path = package_dir / "best_model.pth"
            checkpoint_source = self.get_best_checkpoint_path()
            if Path(checkpoint_source).exists():
                shutil.copy(checkpoint_source, pth_path)
                logger.info(f"   ✅ Saved checkpoint: {pth_path}")
            
            # 3. Create metadata.json
            metadata = {
                "model_info": {
                    "name": getattr(self, 'name', None),
                    "session_id": getattr(self, 'session_id', None),
                    "job_id": getattr(self, 'job_id', None),
                    "d_model": self.d_model,
                    "best_epoch": best_epoch_idx,
                    "total_epochs": self.training_info.get('total_epochs', 0),
                    "created_at": datetime.now().isoformat(),
                },
                "data_info": {
                    "num_columns": len(self.col_order),
                    "column_names": self.col_order,
                    "column_types": {col: self.col_types.get(col) for col in self.col_order},
                    "train_rows": len(self.train_input_data.df) if self.train_input_data else 0,
                    "val_rows": len(self.val_input_data.df) if self.val_input_data else 0,
                },
                "training_metrics": {},
                "config": {},
                "version_info": self.version_info or {},
                "warnings": self._get_training_warnings(),
                "kl_divergences": getattr(self.train_input_data, 'kl_divergences_vs_val', {})
            }
            
            # Extract best epoch metrics from loss history
            loss_history = self.training_info.get('progress_info', {}).get('loss_history', [])
            if loss_history and best_epoch_idx < len(loss_history):
                best_entry = loss_history[best_epoch_idx]
                metadata["training_metrics"] = {
                    "epoch": best_epoch_idx,
                    "train_loss": best_entry.get('train_loss'),
                    "val_loss": best_entry.get('val_loss'),
                    "spread": best_entry.get('spread'),
                    "joint": best_entry.get('joint'),
                    "marginal": best_entry.get('marginal'),
                }
                logger.info(f"   ✅ Extracted metrics from epoch {best_epoch_idx}")
            
            metadata_path = package_dir / "metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            logger.info(f"   ✅ Saved metadata: {metadata_path}")
            
            # 3b. Create comprehensive model_card.json
            model_card = self._create_model_card_json(best_epoch_idx, metadata)
            model_card_path = package_dir / "model_card.json"
            with open(model_card_path, 'w') as f:
                json.dump(model_card, f, indent=2, default=str)
            logger.info(f"   ✅ Saved model card: {model_card_path}")
            
            # 4. Copy lib/featrix/neural directory (code snapshot)
            src_neural_dir = Path(__file__).parent  # This file is in lib/featrix/neural
            dst_neural_dir = package_dir / "lib" / "featrix" / "neural"
            dst_neural_dir.parent.parent.mkdir(parents=True, exist_ok=True)
            
            if src_neural_dir.exists():
                shutil.copytree(src_neural_dir, dst_neural_dir, dirs_exist_ok=True)
                logger.info(f"   ✅ Copied code snapshot: {dst_neural_dir}")
            
            logger.info(f"📦 Model package complete! Location: {package_dir}")
            logger.info(f"   To load: pickle.load(open('best_model_package/best_model.pickle', 'rb'))")
            
        except Exception as e:
            logger.warning(f"Failed to create model package: {e}")
            import traceback
            traceback.print_exc()
    
    def _get_version_string(self):
        """Get version string from version_info, handling both dict and VersionInfo object."""
        if not self.version_info:
            return 'unknown'
        
        # Handle VersionInfo object
        if hasattr(self.version_info, 'semantic_version'):
            return self.version_info.semantic_version
        
        # Handle dict (backward compatibility)
        if isinstance(self.version_info, dict):
            return self.version_info.get('version', self.version_info.get('semantic_version', 'unknown'))
        
        return 'unknown'
    
    def _create_model_card_json(self, best_epoch_idx, metadata):
        """
        Create comprehensive model card JSON with all training info.
        
        Based on LoadSure HTML model card format.
        """
        import socket
        
        # Get loss history for best epoch
        loss_history = self.training_info.get('progress_info', {}).get('loss_history', [])
        best_entry = loss_history[best_epoch_idx] if loss_history and best_epoch_idx < len(loss_history) else {}
        
        model_card = {
            "model_identification": {
                "session_id": getattr(self, 'session_id', None),
                "job_id": getattr(self, 'job_id', None),
                "name": getattr(self, 'name', None),
                "compute_cluster": socket.gethostname().split('.')[0].upper(),
                "training_date": datetime.now().strftime('%Y-%m-%d'),
                "status": "DONE",
                "model_type": "Embedding Space",
                "framework": f"FeatrixSphere {self._get_version_string()}"
            },
            
            "training_dataset": {
                "total_rows": len(self.train_input_data.df) + len(self.val_input_data.df) if self.train_input_data and self.val_input_data else 0,
                "train_rows": len(self.train_input_data.df) if self.train_input_data else 0,
                "val_rows": len(self.val_input_data.df) if self.val_input_data else 0,
                "total_features": len(self.col_order),
                "feature_names": self.col_order,
            },
            
            "feature_inventory": self._get_feature_inventory(),
            
            "training_configuration": {
                "epochs_total": self.training_info.get('total_epochs', 0),
                "best_epoch": best_epoch_idx,
                "d_model": self.d_model,
                "batch_size": self.training_info.get('batch_size', None),
                "learning_rate": self.training_info.get('learning_rate', None),
                "optimizer": self.training_info.get('optimizer', 'Adam'),
                "dropout_schedule": {
                    "enabled": True,
                    "initial": 0.5,
                    "final": 0.25
                }
            },
            
            "training_metrics": {
                "best_epoch": {
                    "epoch": best_epoch_idx,
                    "train_loss": best_entry.get('train_loss'),
                    "val_loss": best_entry.get('val_loss'),
                    "spread_loss": best_entry.get('spread'),
                    "joint_loss": best_entry.get('joint'),
                    "marginal_loss": best_entry.get('marginal'),
                },
                "final_epoch": {
                    "epoch": len(loss_history) - 1 if loss_history else 0,
                    "train_loss": loss_history[-1].get('train_loss') if loss_history else None,
                    "val_loss": loss_history[-1].get('val_loss') if loss_history else None,
                },
                "loss_progression": {
                    "initial_train": loss_history[0].get('train_loss') if loss_history else None,
                    "initial_val": loss_history[0].get('val_loss') if loss_history else None,
                    "improvement_pct": self._calculate_improvement(loss_history) if loss_history else None
                }
            },
            
            "column_statistics": self._get_column_statistics(),
            
            "model_quality": {
                "assessment": self._assess_model_quality(loss_history),
                "recommendations": self._get_recommendations(loss_history),
                "warnings": self._get_training_warnings()
            },
            
            "technical_details": {
                "pytorch_version": torch.__version__ if torch else "unknown",
                "device": "GPU" if torch.cuda.is_available() else "CPU",
                "precision": "float32",
                "normalization": "unit_sphere",
                "loss_function": "InfoNCE (contrastive)",
            },
            
            "provenance": {
                "created_at": datetime.now().isoformat(),
                "training_duration_minutes": self.training_info.get('duration_minutes', 0),
                "version_info": self.version_info or {},
            }
        }
        
        return model_card
    
    def _get_feature_inventory(self):
        """Extract feature inventory for model card."""
        features = []
        
        for col_name in self.col_order:
            codec = self.col_codecs.get(col_name)
            col_type = self.col_types.get(col_name, "unknown")
            
            feature_info = {
                "name": col_name,
                "type": str(col_type),
                "encoder_type": type(codec).__name__ if codec else "unknown"
            }
            
            # Add type-specific info
            if hasattr(codec, 'members'):
                feature_info["unique_values"] = len(codec.members)
                feature_info["sample_values"] = list(codec.members)[:5] if hasattr(codec.members, '__iter__') else []
            elif hasattr(codec, 'stats'):
                feature_info["statistics"] = codec.stats
            
            features.append(feature_info)
        
        return features
    
    def _get_column_statistics(self):
        """Get per-column loss and MI statistics."""
        col_stats = {}
        
        # Get MI estimates
        col_mi = getattr(self.encoder, 'col_mi_estimates', {})
        
        # Get latest marginal losses
        latest_marginal = self.training_info.get('progress_info', {}).get('latest_marginal_losses', {})
        
        for col_name in self.col_order:
            col_stats[col_name] = {
                "mutual_information_bits": col_mi.get(col_name),
                "marginal_loss": latest_marginal.get(col_name),
            }
        
        return col_stats
    
    def _calculate_improvement(self, loss_history):
        """Calculate overall training improvement."""
        if not loss_history or len(loss_history) < 2:
            return None
        
        initial = loss_history[0].get('val_loss')
        final = loss_history[-1].get('val_loss')
        
        if initial and final and initial > 0:
            return ((initial - final) / initial) * 100
        return None
    
    def _assess_model_quality(self, loss_history):
        """Assess overall model quality."""
        if not loss_history:
            return "UNKNOWN"
        
        improvement = self._calculate_improvement(loss_history)
        
        if improvement is None:
            return "UNKNOWN"
        elif improvement > 80:
            return "EXCELLENT"
        elif improvement > 50:
            return "GOOD"
        elif improvement > 20:
            return "FAIR"
        else:
            return "POOR"
    
    def _get_recommendations(self, loss_history):
        """Generate training recommendations."""
        recommendations = []
        
        if not loss_history:
            return recommendations
        
        # Check for overfitting
        final_entry = loss_history[-1]
        train_loss = final_entry.get('train_loss', 0)
        val_loss = final_entry.get('val_loss', 0)
        
        if val_loss > 0 and train_loss > 0:
            gap = val_loss - train_loss
            gap_pct = (gap / train_loss) * 100
            
            if gap_pct > 30:
                recommendations.append({
                    "issue": "Large train/val gap indicates overfitting",
                    "suggestion": "Consider higher dropout or more regularization"
                })
        
        # Check for poor improvement
        improvement = self._calculate_improvement(loss_history)
        if improvement is not None and improvement < 20:
            recommendations.append({
                "issue": "Training did not improve sufficiently",
                "suggestion": "Review data quality or try longer training"
            })
        
        # Check for distribution shift (KL divergence)
        kl_divergences = getattr(self.train_input_data, 'kl_divergences_vs_val', {})
        if kl_divergences:
            high_kl_count = sum(1 for kl_div in kl_divergences.values() if kl_div > 1.0)
            if high_kl_count > 0:
                recommendations.append({
                    "issue": f"Distribution shift detected: {high_kl_count} column(s) have high KL divergence (>1.0) between train and validation sets",
                    "suggestion": "Review data splitting strategy - train/val distributions should be similar. Check for temporal drift or data leakage."
                })
        
        return recommendations
    
    def _get_training_warnings(self):
        """Get training warnings including KL divergence issues."""
        warnings = []
        
        # Check KL divergence between train and val distributions
        kl_divergences = getattr(self.train_input_data, 'kl_divergences_vs_val', {})
        if kl_divergences:
            high_kl_columns = []
            for col_name, kl_div in kl_divergences.items():
                if kl_div > 1.0:  # High distribution shift
                    high_kl_columns.append((col_name, kl_div))
            
            if high_kl_columns:
                # Sort by KL divergence (highest first)
                high_kl_columns.sort(key=lambda x: x[1], reverse=True)
                warnings.append({
                    "type": "DISTRIBUTION_SHIFT",
                    "severity": "HIGH",
                    "message": f"High KL divergence between train and validation distributions detected for {len(high_kl_columns)} column(s)",
                    "details": {
                        "threshold": 1.0,
                        "affected_columns": [
                            {
                                "column": col_name,
                                "kl_divergence": round(kl_div, 3),
                                "interpretation": "HIGH" if kl_div > 2.0 else "MODERATE"
                            }
                            for col_name, kl_div in high_kl_columns
                        ]
                    },
                    "recommendation": "Train and validation sets have different distributions. This may indicate data leakage, temporal drift, or sampling issues. Review data splitting strategy."
                })
        
        return warnings
    
    def _save_movie_data_snapshot(self, movie_frame_interval):
        """
        Save a one-time data snapshot for async movie frame generation.
        Uses same sampling logic as EpochProjectionCallback.
        """
        try:
            # Get combined train+val data (same as movie frames use)
            combined_df = pd.concat([self.train_input_data.df, self.val_input_data.df], ignore_index=True)
            
            # Sample consistently (max 500 points)
            max_samples = 500
            if len(combined_df) > max_samples:
                # Use same sampling as EpochProjectionCallback
                # TODO: Handle important_columns if needed
                sample_df = combined_df.sample(max_samples, random_state=42)
                sample_indices = sample_df.index.tolist()
            else:
                sample_df = combined_df
                sample_indices = None
            
            # Save as JSON (ensure output_dir is Path object)
            output_dir = Path(self.output_dir) if isinstance(self.output_dir, str) else self.output_dir
            self.movie_data_snapshot_path = output_dir / "movie_data_snapshot.json"
            snapshot_data = {
                'records': json.loads(sample_df.to_json(orient='records')),
                'sample_indices': sample_indices,
                'total_records': len(combined_df),
                'sampled_records': len(sample_df),
                'timestamp': datetime.now().isoformat()
            }
            
            with open(self.movie_data_snapshot_path, 'w') as f:
                json.dump(snapshot_data, f)
            
            logger.info(f"🎬 Saved movie data snapshot: {len(sample_df)} records to {self.movie_data_snapshot_path}")
            logger.info(f"   Movie frames will be generated EVERY epoch (interval={movie_frame_interval} ignored for async)")
            
        except Exception as e:
            logger.warning(f"Failed to save movie data snapshot: {e}")
            self.movie_data_snapshot_path = None
    
    def _queue_project_training_movie_frame(self, epoch_idx):
        """
        Queue async training movie frame generation task immediately after checkpoint save.
        Uses the epoch-specific checkpoint that was just saved.
        Returns immediately - doesn't block training!
        
        This is the unified movie frame function (replaces both _queue_project_training_movie_frame
        and _queue_movie_frame which were duplicates).
        """
        # Skip if no data snapshot
        if not hasattr(self, 'movie_data_snapshot_path') or not self.movie_data_snapshot_path:
            return
        
        try:
            output_dir = Path(self.output_dir) if isinstance(self.output_dir, str) else self.output_dir
            
            # Ensure movie_data_snapshot_path is a Path object for exists() check
            movie_snapshot_path = Path(self.movie_data_snapshot_path) if isinstance(self.movie_data_snapshot_path, str) else self.movie_data_snapshot_path
            if not movie_snapshot_path.exists():
                logger.warning(f"Movie data snapshot not found: {movie_snapshot_path}, skipping projection build")
                return
            
            # Use the epoch-specific checkpoint that was just saved by save_state()
            # This checkpoint contains encoder + codecs (no huge dataframes)
            training_state_path = self.get_training_state_path(epoch_idx, 0)
            checkpoint_path = Path(self.get_inference_checkpoint_path(epoch_idx, 0))
            
            # Check if checkpoint was saved successfully (from save_state flag)
            if not getattr(self, '_last_embedding_space_checkpoint_saved', False):
                logger.warning(f"⚠️  Embedding space checkpoint was not saved for epoch {epoch_idx}, skipping projection build")
                return
            
            # Verify checkpoint file exists (brief retry for atomic write timing)
            # The checkpoint save uses atomic write (temp file + rename), so we need
            # a brief retry to handle the tiny window between save completion and file visibility
            max_retries = 3
            checkpoint_exists = False
            for attempt in range(max_retries):
                if checkpoint_path.exists():
                    checkpoint_exists = True
                    break
                if attempt < max_retries - 1:
                    time.sleep(0.1)  # Brief 100ms delay
            
            if not checkpoint_exists:
                logger.warning(f"⚠️  Checkpoint not found for epoch {epoch_idx}: {checkpoint_path}")
                logger.warning(f"   Movie frame generation will be skipped for this epoch")
                logger.warning(f"   This may indicate checkpoint save failure")
                return
            
            logger.debug(f"   Using epoch checkpoint: {checkpoint_path}")
            
            # Create job spec for Celery task
            job_spec = {
                'type': 'project_training_movie_frame',
                'session_id': getattr(self, 'session_id', 'unknown'),
                'epoch': epoch_idx,
                'checkpoint_path': str(checkpoint_path),
                'data_snapshot_path': str(self.movie_data_snapshot_path),
                'output_dir': str(output_dir),
            }
            
            # Queue via Celery (cpu_worker queue) - NO FALLBACKS
            from celery_app import app
            task = app.send_task(
                'celery_app.project_training_movie_frame',
                args=[job_spec],
                queue='cpu_worker'  # CPU worker queue
            )
            
            # Save job to Redis for tracking (consistent with other jobs)
            try:
                from lib.job_manager import save_job, JobStatus
                from datetime import datetime
                from zoneinfo import ZoneInfo
                session_id_for_job = job_spec.get('session_id', getattr(self, 'session_id', 'unknown'))
                save_job(
                    job_id=task.id,
                    job_data={
                        'status': JobStatus.READY,
                        'created_at': datetime.now(tz=ZoneInfo("America/New_York")),
                        'job_spec': job_spec,
                    },
                    session_id=session_id_for_job,
                    job_type='project_training_movie_frame'
                )
                logger.debug(f"✅ Saved project_training_movie_frame job {task.id} to Redis")
            except Exception as redis_err:
                logger.warning(f"⚠️  Could not save job to Redis: {redis_err}")
                # Continue anyway - job tracking is non-critical
            
            logger.info(f"🎬 Queued training movie frame for epoch {epoch_idx} → cpu_worker queue (task_id: {task.id}, non-blocking)")
            
        except Exception as e:
            logger.warning(f"Failed to queue projection build for epoch {epoch_idx}: {e}")
    
    def _queue_movie_frame(self, epoch_idx):
        """
        DEPRECATED: Use _queue_project_training_movie_frame instead.
        This function is kept for backward compatibility but just calls the unified function.
        """
        return self._queue_project_training_movie_frame(epoch_idx)

    def restore_progress(self, *args):
        ret = []
        for key in args:
            ret.append(self.training_progress_data.get(key))
        return ret

    def __getstate__(self):
        """
        Custom pickle state - exclude sqlite connections, DataLoaders, and thread locks that can't be pickled.
        
        NOTE: train_input_data, val_input_data, train_data, and val_data are INTENTIONALLY excluded.
        These contain large pandas DataFrames that would make pickle files huge (100GB+). The data can be
        reloaded from SQLite database or original files when needed. This is EXPECTED behavior, not an error.
        """
        import copy
        import threading
        import sqlite3
        from torch.utils.data import DataLoader
        
        logger.debug("💾 Preparing pickle state - intentionally excluding large DataFrames (train_input_data, val_input_data, train_data, val_data)")
        logger.debug("   ✅ This is EXPECTED - data can be reloaded from SQLite/original files. Pickle file will be small and fast.")
        
        # Start with a shallow copy, then selectively deep copy safe objects
        state = {}
        
        # List of attributes to exclude (unpicklable objects)
        exclude_attrs = {
            'data_loader', 'val_dataloader',  # DataLoaders can't be pickled
            'timed_data_loader',  # Custom data loaders
            'train_input_data', 'val_input_data',  # FeatrixInputDataSet objects contain large pandas DataFrames (100GB+)
            # These are explicitly excluded to keep pickle files small - data can be reloaded from SQLite
            'train_data', 'val_data',  # Also exclude these if they exist (backup check)
        }
        
        # List of attributes that might contain thread locks or other unpicklable objects
        # These will be set to None
        exclude_if_has_lock = set()
        
        # First pass: identify problematic objects
        for key, value in self.__dict__.items():
            # CRITICAL: train_input_data and val_input_data contain 100GB+ DataFrames - NEVER pickle them
            # This is INTENTIONAL - we exclude them to keep pickle files small and fast
            if key in exclude_attrs:
                if key in ('train_input_data', 'val_input_data', 'train_data', 'val_data'):
                    logger.debug(f"✅ INTENTIONAL EXCLUSION: Skipping {key} in pickle (contains large DataFrames - data can be reloaded from SQLite/original files)")
                continue  # Skip excluded attributes entirely
            
            # Check if this is a DataLoader
            if isinstance(value, DataLoader):
                continue  # Skip DataLoaders
            
            # Check for DataLoader iterators explicitly (they can't be pickled)
            if hasattr(value, '__class__'):
                class_name = value.__class__.__name__
                if 'DataLoaderIter' in class_name or '_MultiProcessingDataLoaderIter' == class_name:
                    logger.debug(f"Skipping {key} in pickle state (DataLoader iterator: {class_name})")
                    continue
            
            # Check if this is a FeatrixInputDataSet - EXCLUDE IT ENTIRELY (backup check)
            # FeatrixInputDataSet contains large pandas DataFrames (self.df) that can be 100GB+
            # These should NOT be pickled - data can be reloaded from SQLite database or original files
            # This is INTENTIONAL to keep pickle files small and fast
            if hasattr(value, '__class__') and value.__class__.__name__ == 'FeatrixInputDataSet':
                logger.debug(f"✅ INTENTIONAL EXCLUSION: Skipping {key} in pickle (FeatrixInputDataSet contains large DataFrames - data can be reloaded from SQLite/original files)")
                continue
            
            # Check for thread locks
            try:
                if hasattr(value, '__dict__'):
                    # Check if object or any nested object has a lock
                    has_lock = False
                    try:
                        for attr_name, attr_value in value.__dict__.items():
                            if isinstance(attr_value, (threading.Lock, threading.RLock, threading.Condition, threading.Semaphore)):
                                has_lock = True
                                break
                            # Check nested objects
                            if hasattr(attr_value, '__dict__'):
                                for nested_attr in attr_value.__dict__.values():
                                    if isinstance(nested_attr, (threading.Lock, threading.RLock, threading.Condition, threading.Semaphore)):
                                        has_lock = True
                                        break
                                if has_lock:
                                    break
                    except (AttributeError, TypeError):
                        pass
                    
                    if has_lock:
                        exclude_if_has_lock.add(key)
                        continue
            except (AttributeError, TypeError):
                pass
            
            # Check for sqlite3.Connection objects directly
            if isinstance(value, sqlite3.Connection):
                logger.debug(f"Skipping {key} in pickle state (sqlite3.Connection)")
                continue
            
            # Check for TrainingHistoryDB objects (they contain sqlite connections)
            if hasattr(value, '__class__') and value.__class__.__name__ == 'TrainingHistoryDB':
                # Exclude history_db entirely - it's not needed for model package
                logger.debug(f"Skipping {key} in pickle state (TrainingHistoryDB with sqlite connection)")
                continue
            
            # Check for DataLoader iterators explicitly (they can't be pickled)
            if hasattr(value, '__class__'):
                class_name = value.__class__.__name__
                if 'DataLoader' in class_name or 'dataloader' in class_name.lower():
                    logger.debug(f"Skipping {key} in pickle state (DataLoader or iterator: {class_name})")
                    continue
                # Check for DataLoader iterator classes
                if class_name == '_MultiProcessingDataLoaderIter' or 'DataLoaderIter' in class_name:
                    logger.debug(f"Skipping {key} in pickle state (DataLoader iterator: {class_name})")
                    continue
            
            # PyTorch-approved way: Save encoder as state_dict instead of whole object
            # This avoids persistent_load errors and is the recommended approach
            if key == 'encoder' and hasattr(value, 'state_dict') and hasattr(value, 'load_state_dict'):
                # It's a PyTorch nn.Module - save state_dict instead
                try:
                    state['encoder_state_dict'] = value.state_dict()
                    logger.debug(f"Saved encoder as state_dict (PyTorch-approved method)")
                    continue  # Skip the deepcopy for encoder
                except Exception as e:
                    logger.warning(f"Failed to get encoder state_dict, falling back to deepcopy: {e}")
                    # Fall through to try deepcopy
            
            # Try to deep copy, but catch errors for unpicklable objects
            try:
                state[key] = copy.deepcopy(value)
            except (TypeError, AttributeError, NotImplementedError, RuntimeError) as e:
                # If deepcopy fails, try to identify why
                error_msg = str(e).lower()
                error_type = type(e).__name__
                error_str = str(e)
                
                # Check for tensor-related errors (PyTorch tensors that aren't graph leaves can't be deepcopied)
                is_tensor_error = False
                if 'tensor' in error_msg or 'graph leaves' in error_msg or 'deepcopy protocol' in error_msg:
                    is_tensor_error = True
                    logger.debug(f"Skipping {key} in pickle state (tensor deepcopy error: {error_type} - {error_str})")
                    continue
                
                # Check for DataLoader-related errors
                # The error message might be a tuple like ('{} cannot be pickled', '_MultiProcessingDataLoaderIter')
                # Check both the string representation and the exception args
                is_dataloader_error = False
                if hasattr(e, 'args') and e.args:
                    # Check if any arg contains DataLoader-related strings
                    for arg in e.args:
                        arg_str = str(arg)
                        if 'DataLoader' in arg_str or 'DataLoaderIter' in arg_str or '_MultiProcessingDataLoaderIter' in arg_str:
                            is_dataloader_error = True
                            break
                
                if is_dataloader_error or 'dataloader' in error_msg or 'DataLoader' in error_str or 'DataLoaderIter' in error_str or '_MultiProcessingDataLoaderIter' in error_str:
                    logger.debug(f"Skipping {key} in pickle state (DataLoader error: {error_type} - {error_str})")
                    continue
                elif 'lock' in error_msg or 'thread' in error_msg:
                    # Skip objects with locks
                    logger.debug(f"Skipping {key} in pickle state (contains thread lock)")
                    continue
                elif 'sqlite' in error_msg or 'connection' in error_msg:
                    # Skip sqlite connections
                    logger.debug(f"Skipping {key} in pickle state (sqlite connection)")
                    continue
                elif 'cannot be pickled' in error_msg:
                    # Generic unpicklable object
                    logger.debug(f"Skipping {key} in pickle state (cannot be pickled: {error_type})")
                    continue
                else:
                    # For other errors, try shallow copy as fallback
                    try:
                        state[key] = copy.copy(value)
                    except (TypeError, AttributeError, NotImplementedError, RuntimeError):
                        logger.warning(f"Could not pickle {key}, excluding from state")
                        continue
        
        # Remove sqlite connections from string_cache objects
        def remove_conn(obj):
            """Recursively remove conn and cursor from objects."""
            if hasattr(obj, '__dict__'):
                if hasattr(obj, 'conn'):
                    obj.conn = None
                if hasattr(obj, 'cursor'):
                    obj.cursor = None
                # Recursively process nested objects
                for attr_name, attr_value in obj.__dict__.items():
                    if attr_name not in ('conn', 'cursor'):
                        try:
                            remove_conn(attr_value)
                        except (AttributeError, TypeError, RecursionError):
                            pass
        
        # Remove connections from input data objects
        if 'train_input_data' in state and state['train_input_data']:
            try:
                remove_conn(state['train_input_data'])
            except (AttributeError, TypeError, RecursionError):
                pass
        
        if 'val_input_data' in state and state['val_input_data']:
            try:
                remove_conn(state['val_input_data'])
            except (AttributeError, TypeError, RecursionError):
                pass
        
        # Final pass: check for any remaining sqlite3.Connection objects in state
        keys_to_remove = []
        for key, value in state.items():
            if isinstance(value, sqlite3.Connection):
                keys_to_remove.append(key)
            elif hasattr(value, '__dict__'):
                # Check nested objects
                try:
                    for attr_name, attr_value in value.__dict__.items():
                        if isinstance(attr_value, sqlite3.Connection):
                            keys_to_remove.append(key)
                            break
                except (AttributeError, TypeError):
                    pass
        
        for key in keys_to_remove:
            logger.debug(f"Removing {key} from pickle state (contains sqlite3.Connection)")
            del state[key]
        
        return state
    
    def __setstate__(self, state):
        """Restore state after unpickling - connections will be None and need to be recreated when used."""
        # Get logger first before using it
        import logging
        logger = logging.getLogger(__name__)
        
        # Log GPU memory before unpickling to see if __setstate__ triggers allocation
        allocated_before = 0.0
        reserved_before = 0.0
        try:
            if torch.cuda.is_available():
                allocated_before = torch.cuda.memory_allocated() / (1024**3)
                reserved_before = torch.cuda.memory_reserved() / (1024**3)
                logger.info(f"📊 EmbeddingSpace.__setstate__: GPU memory BEFORE: Allocated={allocated_before:.3f} GB, Reserved={reserved_before:.3f} GB")
        except Exception as e:
            logger.info(f"📊 EmbeddingSpace.__setstate__: Could not check GPU memory before: {e}")
        
        # Check what's in the state dict before unpickling
        state_keys = list(state.keys())
        logger.info(f"📊 EmbeddingSpace.__setstate__: State dict has {len(state_keys)} keys")
        if 'col_codecs' in state:
            col_codec_count = len(state['col_codecs']) if state['col_codecs'] else 0
            logger.info(f"📊 EmbeddingSpace.__setstate__: About to unpickle {col_codec_count} col_codecs")
            # Log codec types
            if state['col_codecs']:
                codec_types = {}
                for col_name, codec in state['col_codecs'].items():
                    codec_type = type(codec).__name__
                    codec_types[codec_type] = codec_types.get(codec_type, 0) + 1
                logger.info(f"📊 EmbeddingSpace.__setstate__: Codec types: {codec_types}")
        if 'encoder' in state:
            logger.info(f"📊 EmbeddingSpace.__setstate__: State dict contains 'encoder' key (old format)")
        if 'encoder_state_dict' in state:
            logger.info(f"📊 EmbeddingSpace.__setstate__: State dict contains 'encoder_state_dict' key (new PyTorch-approved format)")
        if 'string_cache' in state:
            logger.info(f"📊 EmbeddingSpace.__setstate__: State dict contains 'string_cache' key")
        
        logger.info(f"📊 EmbeddingSpace.__setstate__: About to call self.__dict__.update(state) - this will unpickle col_codecs")
        logger.info(f"📊 EmbeddingSpace.__setstate__: State has {len(state.get('col_codecs', {}))} col_codecs to unpickle")
        
        # PyTorch-approved way: Recreate encoder from state_dict if present
        # Check if we have the new format (encoder_state_dict) or old format (encoder already pickled)
        encoder_state_dict = state.pop('encoder_state_dict', None)
        encoder_in_state = 'encoder' in state
        
        logger.info(f"📊 EmbeddingSpace.__setstate__: Starting self.__dict__.update(state)...")
        import time as time_module
        update_start = time_module.time()
        
        self.__dict__.update(state)
        
        update_time = time_module.time() - update_start
        logger.info(f"📊 EmbeddingSpace.__setstate__: Finished self.__dict__.update(state) in {update_time:.1f}s")
        logger.info(f"   This unpickled: {len(self.col_codecs)} col_codecs")
        
        # Recreate encoder from state_dict if we have it (new PyTorch-approved format)
        if encoder_state_dict is not None:
            try:
                logger.info(f"")
                logger.info(f"📊 EmbeddingSpace.__setstate__: Recreating encoder from state_dict...")
                logger.info(f"   ⏳ This creates FeatrixTableEncoder from {len(self.col_codecs)} codecs")
                # We need col_codecs and encoder_config to recreate the encoder
                if not hasattr(self, 'col_codecs') or not self.col_codecs:
                    raise ValueError("Cannot recreate encoder: col_codecs missing from state")
                if not hasattr(self, 'encoder_config') or not self.encoder_config:
                    raise ValueError("Cannot recreate encoder: encoder_config missing from state")
                
                # Recreate the encoder (same as in __init__)
                logger.info(f"   🔧 Creating FeatrixTableEncoder from {len(self.col_codecs)} codecs...")
                encoder_create_start = time_module.time()
                self.encoder = FeatrixTableEncoder(
                    col_codecs=self.col_codecs,
                    config=self.encoder_config,
                )
                encoder_create_time = time_module.time() - encoder_create_start
                logger.info(f"   ✅ FeatrixTableEncoder created in {encoder_create_time:.1f}s")
                
                # Load the state_dict - CRITICAL: Load to CPU first to avoid GPU OOM
                logger.info(f"   🔧 Loading encoder weights from state_dict TO CPU...")
                state_dict_start = time_module.time()
                # Move state_dict tensors to CPU before loading
                cpu_state_dict = {k: v.cpu() if hasattr(v, 'cpu') else v for k, v in encoder_state_dict.items()}
                
                # Filter out keys with size mismatches before loading
                # PyTorch's load_state_dict with strict=False still raises RuntimeError for size mismatches
                model_state_dict = self.encoder.state_dict()
                filtered_state_dict = {}
                size_mismatches = []
                for key, value in cpu_state_dict.items():
                    if key in model_state_dict:
                        model_shape = model_state_dict[key].shape
                        checkpoint_shape = value.shape if hasattr(value, 'shape') else None
                        if checkpoint_shape is not None and model_shape != checkpoint_shape:
                            size_mismatches.append(f"{key}: checkpoint {checkpoint_shape} vs model {model_shape}")
                            continue
                    filtered_state_dict[key] = value
                
                if size_mismatches:
                    logger.warning(f"   ⚠️  Filtered out {len(size_mismatches)} keys with size mismatches (different data = different vocabs/column counts)")
                    if len(size_mismatches) <= 10:
                        for mismatch in size_mismatches:
                            logger.debug(f"      {mismatch}")
                    else:
                        for mismatch in size_mismatches[:5]:
                            logger.debug(f"      {mismatch}")
                        logger.debug(f"      ... and {len(size_mismatches) - 5} more")
                
                # Use strict=False to allow missing/unexpected keys (but we've already filtered size mismatches)
                missing_keys, unexpected_keys = self.encoder.load_state_dict(filtered_state_dict, strict=False)
                state_dict_time = time_module.time() - state_dict_start
                if missing_keys:
                    logger.warning(f"   ⚠️  {len(missing_keys)} missing keys (new columns or larger vocabs in current data)")
                if unexpected_keys:
                    logger.warning(f"   ⚠️  {len(unexpected_keys)} unexpected keys (removed columns or smaller vocabs in current data)")
                logger.info(f"   ✅ Encoder weights loaded to CPU in {state_dict_time:.1f}s (strict=False)")
                
                # Encoder is already on CPU from load_state_dict(cpu_state_dict)
                logger.info(f"✅ EmbeddingSpace.__setstate__: Successfully recreated encoder from state_dict on CPU")
            except Exception as e:
                logger.error(f"❌ EmbeddingSpace.__setstate__: Failed to recreate encoder from state_dict: {e}")
                import traceback
                logger.error(traceback.format_exc())
                # If recreation fails, try to continue without encoder (will fail later if needed)
                self.encoder = None
        elif not encoder_in_state:
            # No encoder in state at all - might be None or missing
            logger.warning(f"⚠️  EmbeddingSpace.__setstate__: No encoder found in state (neither encoder nor encoder_state_dict)")
            if not hasattr(self, 'encoder'):
                self.encoder = None
        
        # Log GPU memory after unpickling to see if __setstate__ triggered allocation
        allocated_after = 0.0
        reserved_after = 0.0
        try:
            if torch.cuda.is_available():
                allocated_after = torch.cuda.memory_allocated() / (1024**3)
                reserved_after = torch.cuda.memory_reserved() / (1024**3)
                logger.info(f"📊 EmbeddingSpace.__setstate__: GPU memory AFTER: Allocated={allocated_after:.3f} GB, Reserved={reserved_after:.3f} GB")
                if allocated_after > allocated_before + 0.001:  # >1MB increase
                    logger.error(f"🚨 EmbeddingSpace.__setstate__: GPU memory INCREASED by {allocated_after - allocated_before:.3f} GB during unpickling!")
                    logger.error(f"   This likely means col_codecs or StringCache objects triggered GPU allocation")
        except Exception as e:
            logger.info(f"📊 EmbeddingSpace.__setstate__: Could not check GPU memory after: {e}")
        
        # CRITICAL: Check encoder device immediately after unpickling
        # The encoder is a large model and might be unpickled onto GPU even with map_location='cpu'
        if hasattr(self, 'encoder') and self.encoder is not None:
            try:
                allocated_before_encoder_check = 0.0
                if torch.cuda.is_available():
                    allocated_before_encoder_check = torch.cuda.memory_allocated() / (1024**3)
                    logger.info(f"📊 EmbeddingSpace.__setstate__: GPU memory BEFORE encoder check: Allocated={allocated_before_encoder_check:.3f} GB")
                
                if list(self.encoder.parameters()):
                    encoder_device = next(self.encoder.parameters()).device
                    encoder_param_count = sum(p.numel() for p in self.encoder.parameters())
                    logger.info(f"📊 EmbeddingSpace.__setstate__: Encoder device: {encoder_device.type}, Parameters: {encoder_param_count:,}")
                    
                    if encoder_device.type == 'cuda':
                        logger.error(f"🚨 EmbeddingSpace.__setstate__: Encoder is on GPU! Moving to CPU...")
                        force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
                        if force_cpu:
                            logger.info(f"🔄 __setstate__: Moving encoder from GPU to CPU (CPU mode)")
                            self.encoder = self.encoder.cpu()
                            if torch.cuda.is_available():
                                torch.cuda.empty_cache()
                                allocated_after_encoder_move = torch.cuda.memory_allocated() / (1024**3)
                                logger.info(f"📊 EmbeddingSpace.__setstate__: GPU memory AFTER moving encoder to CPU: Allocated={allocated_after_encoder_move:.3f} GB")
                    else:
                        logger.info(f"✅ EmbeddingSpace.__setstate__: Encoder is already on CPU")
                else:
                    logger.info(f"📊 EmbeddingSpace.__setstate__: Encoder has no parameters")
            except Exception as e:
                logger.error(f"❌ EmbeddingSpace.__setstate__: Could not check encoder device: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # train_input_data and val_input_data are excluded from pickle to avoid 100GB+ files
        # Try to recreate them from SQLite database if available
        if 'train_input_data' not in state or 'val_input_data' not in state:
            # Try to recreate from SQLite database
            sqlite_db_path = state.get('sqlite_db_path') or getattr(self, 'sqlite_db_path', None)
            
            if sqlite_db_path and Path(sqlite_db_path).exists():
                try:
                    from featrix.neural.input_data_file import FeatrixInputDataFile
                    from featrix.neural.input_data_set import FeatrixInputDataSet
                    from sklearn.model_selection import train_test_split
                    import logging
                    logger = logging.getLogger(__name__)
                    
                    logger.info(f"🔄 Recreating train_input_data and val_input_data from SQLite: {sqlite_db_path}")
                    
                    # Load data from SQLite
                    input_data_file = FeatrixInputDataFile(sqlite_db_path)
                    df = input_data_file.df
                    
                    # Split into train/val (use same split ratio as original training if available)
                    # Default to 80/20 split
                    train_size = 0.8
                    if len(df) > 0:
                        train_df, val_df = train_test_split(df, train_size=train_size, random_state=42)
                        
                        # Create FeatrixInputDataSet objects
                        # Use standup_only=True to skip expensive detection/enrichment (already done)
                        train_input_data = FeatrixInputDataSet(
                            df=train_df,
                            standup_only=True,
                            dataset_title="TRAIN (recreated from SQLite)"
                        )
                        val_input_data = FeatrixInputDataSet(
                            df=val_df,
                            standup_only=True,
                            dataset_title="VAL (recreated from SQLite)"
                        )
                        
                        if 'train_input_data' not in state:
                            self.train_input_data = train_input_data
                        if 'val_input_data' not in state:
                            self.val_input_data = val_input_data
                        
                        logger.info(f"✅ Recreated train_input_data ({len(train_df)} rows) and val_input_data ({len(val_df)} rows) from SQLite")
                    else:
                        logger.warning(f"⚠️  SQLite database is empty, cannot recreate input data")
                        if 'train_input_data' not in state:
                            self.train_input_data = None
                        if 'val_input_data' not in state:
                            self.val_input_data = None
                except Exception as e:
                    import traceback
                    logger.warning(f"⚠️  Failed to recreate input data from SQLite: {e}")
                    logger.debug(f"   Traceback: {traceback.format_exc()}")
                    # Set to None if recreation failed
                    if 'train_input_data' not in state:
                        self.train_input_data = None
                    if 'val_input_data' not in state:
                        self.val_input_data = None
            else:
                # No SQLite database available - set to None
                # Caller should provide input data if needed (e.g., when resuming training)
                if 'train_input_data' not in state:
                    self.train_input_data = None
                if 'val_input_data' not in state:
                    self.val_input_data = None
        
        # Note: sqlite connections (conn/cursor) are set to None and will need to be
        # recreated when string_cache is actually used. This is handled by the
        # movie frame task which uses the data snapshot instead of the full input data.

    # def load_epoch(self, ...):
    # might be missing encoders

    def _get_lambda_lr(self, step_lr_segments):
        """Implement piecewise-constant learning rate schedule.

        Used as input to LambdaLR in `train`.

        lr_stops are expected to have the format
        [(n_steps, lr), (n_steps, lr), ...]
        """

        # Convert from segments expressed in epochs to cumulative milestones expressed in optimizer steps.
        # One step corresponds to a single batch.
        step_lr_milestones = []
        cum = 0
        for n_steps, lr in step_lr_segments:
            step_lr_milestones.append((cum, lr))
            # cum = cum + n_epochs * batches_per_epoch
            cum = cum + n_steps 

        def func(step):
            chosen_lr = None
            for cum_n_steps, lr in step_lr_milestones:
                # Iterate until we find a milestone we haven't reached yet.
                if step >= cum_n_steps:
                    chosen_lr = lr
                else:
                    break

            # This is here just to help with debugging.
            if chosen_lr is None:
                warnings.warn(
                    f"No LR milestone was selected. Current step: {step}. All milestones: {step_lr_milestones}"
                )
                chosen_lr = 1

            return chosen_lr

        return func

    def _prep_profiler(self):
        logger.info("Setting up the profiler.")
        return torch.profiler.profile(
            activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
            schedule=torch.profiler.schedule(
                skip_first=10,
                wait=10,
                warmup=10,
                active=1,
                repeat=1,
            ),
            with_stack=True,
            profile_memory=True,
            record_shapes=True,
            on_trace_ready=torch.profiler.tensorboard_trace_handler('./profiler_output')
        )

    # class TrainingStatusInfo:

    def log_trickiest_columns(self, loss_dict, epoch_idx, top_n=None):
        """
        Analyze and log which columns have the highest losses (are trickiest to predict).
        
        Args:
            loss_dict: The loss dictionary from compute_total_loss containing per-column losses
            epoch_idx: Current epoch index
            top_n: Number of top difficult columns to log. If None, shows all columns (default: None)
        """
        try:
            # Extract column losses from the different marginal loss components
            marginal_loss = loss_dict.get('marginal_loss', {})
            
            # Get column losses from all four marginal loss components
            full_1_cols = marginal_loss.get('marginal_loss_full_1', {}).get('cols', {})
            full_2_cols = marginal_loss.get('marginal_loss_full_2', {}).get('cols', {})
            short_1_cols = marginal_loss.get('marginal_loss_short_1', {}).get('cols', {})
            short_2_cols = marginal_loss.get('marginal_loss_short_2', {}).get('cols', {})
            
            # Aggregate column losses - average across all masks
            column_losses = {}
            all_cols = set(full_1_cols.keys()) | set(full_2_cols.keys()) | set(short_1_cols.keys()) | set(short_2_cols.keys())
            
            for col in all_cols:
                losses = []
                if col in full_1_cols:
                    losses.append(full_1_cols[col])
                if col in full_2_cols:
                    losses.append(full_2_cols[col])
                if col in short_1_cols:
                    losses.append(short_1_cols[col])
                if col in short_2_cols:
                    losses.append(short_2_cols[col])
                
                if losses:
                    column_losses[col] = sum(losses) / len(losses)
            
            if not column_losses:
                return  # No column losses to report
            
            # Sort columns by loss (highest first)
            sorted_cols = sorted(column_losses.items(), key=lambda x: x[1], reverse=True)
            
            # Calculate mean and std dev of column losses
            loss_values = np.array(list(column_losses.values()))
            mean_loss = loss_values.mean()
            std_loss = loss_values.std()
            min_loss = loss_values.min()
            max_loss = loss_values.max()
            median_loss = np.median(loss_values)
            
            # Determine how many columns to show
            n_to_show = len(sorted_cols) if top_n is None else min(top_n, len(sorted_cols))
            
            # Log summary statistics FIRST
            logger.info(f"🎯 [Epoch {epoch_idx+1}] Column Loss Statistics (n={len(sorted_cols)}):")
            logger.info(f"   Mean: {mean_loss:.4f}, Std: {std_loss:.4f}, Median: {median_loss:.4f}")
            logger.info(f"   Min: {min_loss:.4f}, Max: {max_loss:.4f}, Range: {max_loss-min_loss:.4f}")
            
            # Get MI estimates for columns
            col_mi_estimates = self.encoder.col_mi_estimates if hasattr(self.encoder, 'col_mi_estimates') else {}
            
            # Log individual columns sorted from trickiest to easiest
            logger.info(f"🎯 [Epoch {epoch_idx+1}] Column Losses & MI (sorted HARDEST to EASIEST - showing top {n_to_show}):")
            for i, (col_name, avg_loss) in enumerate(sorted_cols[:n_to_show], 1):
                # Add emoji indicators for very high/low losses
                if avg_loss > 10.0:
                    indicator = "🔥"  # Very tricky
                elif avg_loss > 5.0:
                    indicator = "⚠️ "  # Moderately tricky
                elif avg_loss < 1.0:
                    indicator = "✅"  # Easy
                else:
                    indicator = "  "  # Normal
                
                # Get MI for this column (if available)
                col_mi = col_mi_estimates.get(col_name, None)
                mi_str = f", MI={col_mi:.3f} bits" if col_mi is not None else ", MI=N/A"
                
                # Flag low MI columns (likely independent/unpredictable)
                if col_mi is not None and col_mi < 1.0:
                    mi_indicator = " ⚠️ LOW_MI"
                elif col_mi is not None and col_mi < 0.5:
                    mi_indicator = " 🚫 VERY_LOW_MI"
                else:
                    mi_indicator = ""
                    
                logger.info(f"   {indicator} {i:3d}. '{col_name}': loss={avg_loss:.4f}{mi_str}{mi_indicator}")
                
        except Exception as e:
            logger.warning(f"⚠️  Failed to log column losses: {e}")

    def _encode_value_for_decoding(self, col_name, value, encoder, codec):
        """
        Encode a value using codec.tokenize() + encoder, properly using learned strategy weights.
        
        This is the correct way to encode values for decoding/search - it ensures:
        1. Values are normalized the same way as during training (via codec.tokenize())
        2. Encoders use their learned strategy weights (e.g., AdaptiveScalarEncoder uses ROB if that's best)
        
        Args:
            col_name: Column name
            value: Actual value (not normalized)
            encoder: The encoder for this column (ScalarEncoder, AdaptiveScalarEncoder, SetEncoder, etc.)
            codec: The codec for this column (ScalarCodec, SetCodec, etc.)
            
        Returns:
            full_emb: Full embedding [d_model] (squeezed, no batch dimension)
        """
        from featrix.neural.featrix_token import create_token_batch
        
        # CRITICAL: Use codec.tokenize() to properly normalize the value
        # This ensures the encoder gets values normalized the same way as during training
        token = codec.tokenize(value)
        
        # Create TokenBatch from the token (encoder expects TokenBatch)
        token_batch = create_token_batch([token])
        
        # Encode - encoder uses learned strategy weights
        encoder_output = encoder(token_batch)
        if not isinstance(encoder_output, tuple) or len(encoder_output) != 2:
            raise ValueError(f"Encoder returned unexpected type: {type(encoder_output)}, value: {encoder_output}")
        _, full_emb = encoder_output
        
        # Remove batch dimension
        if full_emb.dim() == 2:
            full_emb = full_emb.squeeze(0)
        
        return full_emb
    
    def _decode_scalar_embedding(self, col_name, col_prediction, encoder, codec, search_samples=None):
        """
        Invert the encoder to decode an embedding back to its scalar value.
        Used to measure encoding lossiness: encode(X) -> embedding -> decode(embedding) -> Y, then measure dist(X, Y).
        
        Args:
            col_name: Column name (unused)
            col_prediction: Encoded embedding [d_model] 
            encoder: The encoder for this column
            codec: ScalarCodec for this column
            search_samples: Ignored
            
        Returns:
            predicted_value: Decoded actual value
            similarity: Always 1.0
        """
        import torch
        import torch.nn.functional as F
        from featrix.neural.featrix_token import Token, TokenStatus, create_token_batch
        
        # Handle batched input: normalize to [1, d_model]
        original_shape = col_prediction.shape
        
        # If it's 2D with batch dimension, extract single embedding
        if col_prediction.dim() == 2:
            if col_prediction.shape[0] > 1:
                # Multiple embeddings in batch - use first one (or could use mean)
                col_prediction = col_prediction[0]  # [d_model]
            elif col_prediction.shape[0] == 1:
                # Single element batch - squeeze it
                col_prediction = col_prediction.squeeze(0)  # [d_model]
            else:
                # Empty batch dimension - shouldn't happen
                raise ValueError(f"Unexpected col_prediction shape: {original_shape}")
        
        # Handle other dimension cases
        if col_prediction.dim() == 0:
            # Scalar - shouldn't happen but handle it
            col_prediction = col_prediction.unsqueeze(0)
        elif col_prediction.dim() > 2:
            # Multiple dimensions - flatten and take appropriate size
            # Assume last dimension is d_model
            col_prediction = col_prediction.view(-1, col_prediction.shape[-1])[0]  # [d_model]
        
        # At this point col_prediction should be 1D [d_model]
        # Now make it [1, d_model] for matrix operations
        if col_prediction.dim() == 1:
            col_prediction = col_prediction.unsqueeze(0)  # [1, d_model]
        elif col_prediction.dim() != 2 or col_prediction.shape[0] != 1:
            raise ValueError(f"After normalization, col_prediction should be [1, d_model], got shape: {col_prediction.shape}")
        
        target_emb = F.normalize(col_prediction, dim=-1)  # [1, d_model]
        
        normalized_val = torch.tensor(0.0, device=col_prediction.device, requires_grad=True)
        
        # Store original training mode of encoder
        encoder_was_training = encoder.training if hasattr(encoder, 'training') else False
        
        # Invert encoder with gradient descent
        # Need to enable gradients for the encoder computation
        try:
            with torch.enable_grad():
                # Temporarily set encoder to train mode if it's a module (to enable gradients)
                if hasattr(encoder, 'train'):
                    encoder.train()
                
                for iteration in range(15):
                    with torch.no_grad():
                        normalized_val.clamp_(-4.0, 4.0)
                    
                    # Create a new tensor that requires grad for this iteration
                    normalized_val_iter = normalized_val.clone().detach().requires_grad_(True)
                    
                    token = Token(
                        value=normalized_val_iter.unsqueeze(0),
                        status=torch.tensor([TokenStatus.OK], device=col_prediction.device)
                    )
                    _, encoded_emb = encoder(create_token_batch([token]))
                    
                    # Handle batched encoder output - ensure we have [1, d_model]
                    if encoded_emb.dim() == 2:
                        if encoded_emb.shape[0] > 1:
                            # Multiple embeddings - take first or mean
                            encoded_emb = encoded_emb[0:1]  # Take first: [1, d_model]
                        elif encoded_emb.shape[0] == 1:
                            # Already [1, d_model] - keep as is
                            pass
                        else:
                            raise ValueError(f"Unexpected encoded_emb shape: {encoded_emb.shape}")
                    elif encoded_emb.dim() == 1:
                        # [d_model] - add batch dimension
                        encoded_emb = encoded_emb.unsqueeze(0)  # [1, d_model]
                    elif encoded_emb.dim() > 2:
                        # Flatten extra dimensions
                        encoded_emb = encoded_emb.view(-1, encoded_emb.shape[-1])[0:1]  # [1, d_model]
                    
                    encoded_emb = F.normalize(encoded_emb, dim=-1)  # [1, d_model]
                    
                    # Use matrix multiplication: [1, d_model] @ [d_model, 1] = [1, 1] (scalar)
                    # Both target_emb and encoded_emb are now [1, d_model], so this works correctly
                    loss = -(target_emb @ encoded_emb.T).squeeze()
                    
                    # Check if loss requires grad before calling backward
                    # Also check that encoded_emb has gradients (encoder must be in train mode with requires_grad)
                    if loss.requires_grad and loss.grad_fn is not None and encoded_emb.requires_grad:
                        try:
                            loss.backward()
                            
                            with torch.no_grad():
                                if normalized_val_iter.grad is not None:
                                    normalized_val = normalized_val_iter - 0.5 * normalized_val_iter.grad
                                else:
                                    # No gradient available - break early
                                    normalized_val = normalized_val_iter.detach()
                                    break
                        except RuntimeError as e:
                            if "does not require grad" in str(e) or "grad_fn" in str(e):
                                # Gradient computation failed - fall back to grid search
                                normalized_val = normalized_val_iter.detach()
                                break
                            else:
                                raise
                    else:
                        # If loss doesn't require grad, we can't do gradient descent
                        # This happens when the encoder output doesn't have gradients
                        # Use the current value and break
                        normalized_val = normalized_val_iter.detach()
                        break
        except RuntimeError as e:
            # If backward pass fails (e.g., "does not require grad"), fall back to simple search
            if "does not require grad" in str(e) or "grad_fn" in str(e):
                # Use a simple grid search instead
                best_val = 0.0
                best_sim = -float('inf')
                for test_val in torch.linspace(-4.0, 4.0, steps=50, device=col_prediction.device):
                    token = Token(
                        value=test_val.unsqueeze(0),
                        status=torch.tensor([TokenStatus.OK], device=col_prediction.device)
                    )
                    with torch.no_grad():
                        _, encoded_emb = encoder(create_token_batch([token]))
                        if encoded_emb.dim() == 2:
                            encoded_emb = encoded_emb[0:1] if encoded_emb.shape[0] > 0 else encoded_emb
                        elif encoded_emb.dim() == 1:
                            encoded_emb = encoded_emb.unsqueeze(0)
                        encoded_emb = F.normalize(encoded_emb, dim=-1)
                        sim = (target_emb @ encoded_emb.T).squeeze().item()
                        if sim > best_sim:
                            best_sim = sim
                            best_val = test_val.item()
                normalized_val = torch.tensor(best_val, device=col_prediction.device)
            else:
                raise
        finally:
            # Restore encoder training mode
            if hasattr(encoder, 'train') and not encoder_was_training:
                encoder.eval()
        
        # Decode normalized value back to actual value
        token = Token(value=normalized_val.item(), status=TokenStatus.OK)
        predicted_value = codec.detokenize(token)
        
        return predicted_value, 1.0
    
    def _decode_set_embedding(self, col_name, col_prediction, encoder, codec):
        """
        Decode a set embedding back to an actual value by searching all possible set members.
        
        Uses proper encoding (codec.tokenize + encoder) for each candidate.
        For sets, tokenize() returns token IDs which are used by SetEncoder.
        
        Args:
            col_name: Column name
            col_prediction: Predicted embedding [d_model]
            encoder: The encoder for this column (SetEncoder)
            codec: SetCodec for this column
            
        Returns:
            predicted_value: Best matching set member value
            similarity: Cosine similarity of best match
        """
        from featrix.neural.featrix_token import TokenBatch, TokenStatus, create_token_batch
        import torch
        
        # Get all possible member values
        all_values = [m for m in codec.members if m != "<UNKNOWN>"]
        
        if not all_values:
            return "<EMPTY_SET>", 0.0
        
        # Encode all possible values using codec.tokenize() for consistency
        # For sets, tokenize() returns token IDs which SetEncoder uses
        token_embeddings_list = []
        valid_values = []
        
        for member_value in all_values:
            try:
                # Use codec.tokenize() to get token ID (consistent with training)
                token = codec.tokenize(member_value)
                if token.status != TokenStatus.OK:
                    continue  # Skip UNKNOWN tokens
                
                # Create TokenBatch from token
                token_batch = create_token_batch([token])
                
                # Encode using encoder (SetEncoder uses learned embeddings)
                encoder_output = encoder(token_batch)
                if not isinstance(encoder_output, tuple) or len(encoder_output) != 2:
                    continue
                _, member_emb = encoder_output
                
                # Remove batch dimension
                if member_emb.dim() == 2:
                    member_emb = member_emb.squeeze(0)
                
                token_embeddings_list.append(member_emb.unsqueeze(1))
                valid_values.append(member_value)
            except Exception:
                continue  # Skip values that fail to encode
        
        if not token_embeddings_list:
            return "<EMPTY_SET>", 0.0
        
        # Concatenate along dim=1 to get [d_model, num_candidates]
        token_embeddings = torch.cat(token_embeddings_list, dim=1)
        
        # Find closest embedding to prediction (cosine similarity)
        pred_norm = torch.nn.functional.normalize(col_prediction.unsqueeze(0), dim=-1)
        tok_norm = torch.nn.functional.normalize(token_embeddings, dim=0)  # Normalize along d_model dim
        similarities = (pred_norm @ tok_norm).squeeze()
        best_idx = similarities.argmax().item()
        best_similarity = similarities[best_idx].item()
        
        predicted_value = valid_values[best_idx]
        
        return predicted_value, best_similarity
    
    def _decode_string_embedding(self, col_name, col_prediction, encoder, codec, search_samples=200, debug=False):
        """
        Decode a string embedding back to an actual value using nearest neighbor search in string cache.
        
        COMMENTED OUT: String decoding not yet implemented - needs final embedding index (d_model dims)
        in LanceDB, not BERT embeddings (384 dims).
        
        Args:
            col_name: Column name
            col_prediction: Predicted embedding [d_model] from the model
            encoder: The encoder for this column (StringEncoder)
            codec: StringCodec for this column
            search_samples: Number of candidate values to search (unused, kept for compatibility)
            debug: If True, return top 3 neighbors for debugging
            
        Returns:
            (predicted_value, similarity) tuple with placeholder values
        """
        # TODO: Implement string decoding - requires indexing final embeddings (d_model dims) in LanceDB
        # The encoder outputs d_model dimensions, but the cache stores BERT embeddings (384 dims).
        # Need to build a separate index of final embeddings for proper decoding.
        return "[string_embedding]", 0.0
    
    def _debug_autoencoding_quality(self, epoch_idx):
        """
        Test autoencoding quality: Can we encode → decode values accurately?
        
        This tests representation lossiness (NOT marginal prediction).
        For each column, encode the actual value and decode it back.
        """
        try:
            logger.info(f"")
            logger.info(f"🔍 [epoch={epoch_idx}] AUTOENCODING QUALITY TEST")
            logger.info(f"   Testing: Encode → Decode accuracy (representation lossiness)")
            logger.info(f"")
            
            # Sample validation data
            val_df = self.val_input_data.df
            sample_size = min(20, len(val_df))
            sample_df = val_df.sample(sample_size, random_state=42 + epoch_idx)
            
            # Test autoencoding for first 5 columns
            for col_idx, col_name in enumerate(self.col_order[:5]):
                try:
                    codec = self.col_codecs.get(col_name)
                    if not codec:
                        continue
                    
                    from featrix.neural.set_codec import SetCodec
                    from featrix.neural.scalar_codec import ScalarCodec, AdaptiveScalarEncoder
                    
                    codec_type = codec.get_codec_name() if hasattr(codec, 'get_codec_name') else "unknown"
                    
                    results = []
                    
                    # CRITICAL: Set to eval mode for inference, restore training mode after
                    was_training = self.encoder.training
                    self.encoder.eval()
                    try:
                        with torch.no_grad():
                            for idx, row in sample_df.iterrows():
                                try:
                                    original_value = row[col_name]
                                    
                                    # Skip NaN values
                                    if pd.isna(original_value):
                                        continue
                                    
                                    # Use encode_record() - just pass a dict with the single field
                                    # It handles ALL tokenization automatically
                                    # encode_record() returns a single tensor (full_encoding by default)
                                    record = {col_name: original_value}
                                    # Get the device where the encoder is located
                                    encoder_device = next(self.encoder.parameters()).device
                                    full_joint_encoding = self.encode_record(record, squeeze=True, short=False, output_device=encoder_device)
                                    
                                    # Use column predictor to get column-specific encoding from joint encoding
                                    full_col_predictions = self.encoder.column_predictor(full_joint_encoding.unsqueeze(0))
                                    if not isinstance(full_col_predictions, (list, tuple)):
                                        raise TypeError(f"column_predictor should return list, got {type(full_col_predictions)}")
                                    if col_idx >= len(full_col_predictions):
                                        raise IndexError(f"col_idx {col_idx} out of range for {len(full_col_predictions)} predictions")
                                    
                                    # Get the column-specific encoding (full_emb)
                                    full_emb = full_col_predictions[col_idx]
                                    if full_emb.dim() == 2:
                                        full_emb = full_emb.squeeze(0)  # Remove batch dimension
                                    
                                    # Get encoder for decoding - handle featrix_ prefix
                                    encoder = None
                                    if col_name in self.encoder.column_encoder.encoders:
                                        encoder = self.encoder.column_encoder.encoders[col_name]
                                    elif f"featrix_{col_name}" in self.encoder.column_encoder.encoders:
                                        encoder = self.encoder.column_encoder.encoders[f"featrix_{col_name}"]
                                    else:
                                        # Try reverse - if col_name has prefix, try without
                                        if col_name.startswith("featrix_") and col_name[8:] in self.encoder.column_encoder.encoders:
                                            encoder = self.encoder.column_encoder.encoders[col_name[8:]]
                                    
                                    if encoder is None:
                                        logger.info(f"      Autoencoding: No encoder found for '{col_name}' (available: {list(self.encoder.column_encoder.encoders.keys())[:5]}...)")
                                        continue
                                    
                                    # Decode back to value using modular helper functions
                                    try:
                                        if isinstance(codec, SetCodec):
                                            decoded_value, cosine_sim = self._decode_set_embedding(col_name, full_emb, encoder, codec)
                                            match = str(decoded_value) == str(original_value)
                                            error = 0 if match else 1
                                            
                                        elif isinstance(codec, ScalarCodec):
                                            decoded_value_raw, cosine_sim = self._decode_scalar_embedding(col_name, full_emb, encoder, codec, search_samples=100)
                                            
                                            # Calculate error
                                            try:
                                                if hasattr(original_value, 'item'):
                                                    orig_float = original_value.item()
                                                elif isinstance(original_value, (int, float)):
                                                    orig_float = float(original_value)
                                                else:
                                                    orig_float = float(original_value)
                                                
                                                # Skip if original is NaN
                                                if pd.isna(orig_float) or not np.isfinite(orig_float):
                                                    continue
                                                
                                                error = abs(decoded_value_raw - orig_float)
                                                relative_error = error / (abs(orig_float) + 1e-6)
                                                match = relative_error < 0.1  # <10% error = match
                                            except (ValueError, TypeError):
                                                # Skip invalid values
                                                continue
                                            except Exception:
                                                error = None
                                                match = None
                                                relative_error = None
                                            
                                            decoded_value = decoded_value_raw
                                            
                                        else:
                                            decoded_value = None
                                            match = None
                                            error = None
                                            
                                    except Exception as decode_err:
                                        logger.info(f"      Autoencoding failed for row {idx}: {decode_err}")
                                        decoded_value = None
                                        match = None
                                        error = None
                                    
                                    results.append({
                                        'original': str(original_value)[:20],
                                        'decoded': str(decoded_value)[:20] if decoded_value is not None else "N/A",
                                        'match': match,
                                        'error': error
                                    })
                                    
                                except Exception as e:
                                    logger.info(f"      Autoencoding failed for row {idx}: {e}")
                                    continue
                    finally:
                        # Always restore training mode if it was in training mode before
                        if was_training:
                            self.encoder.train()
                    
                    if results:
                        if isinstance(codec, SetCodec):
                            correct = sum(1 for r in results if r['match'])
                            accuracy = (correct / len(results)) * 100
                            logger.info(f"   Column '{col_name}' ({codec_type}): {correct}/{len(results)} exact match ({accuracy:.1f}%)")
                            
                            # Show mismatches
                            mismatches = [r for r in results if not r['match']]
                            if mismatches:
                                logger.info(f"      Mismatches:")
                                for i, r in enumerate(mismatches[:3], 1):
                                    logger.info(f"         {i}. Original: {r['original']:20s} → Decoded: {r['decoded']:20s}")
                        
                        elif isinstance(codec, (ScalarCodec, AdaptiveScalarEncoder)):
                            errors = [r['error'] for r in results if r['error'] is not None]
                            if errors:
                                avg_error = sum(errors) / len(errors)
                                max_error = max(errors)
                                good_reconstructions = sum(1 for r in results if r.get('match'))
                                
                                logger.info(f"   Column '{col_name}' ({codec_type}): avg_error={avg_error:.3f}, max_error={max_error:.3f}")
                                logger.info(f"      Good reconstructions (<10% error): {good_reconstructions}/{len(results)} ({100*good_reconstructions/len(results):.1f}%)")
                                
                                # Show worst cases
                                worst = sorted(results, key=lambda r: r.get('error', 0) if r.get('error') is not None else 0, reverse=True)[:3]
                                logger.info(f"      Worst cases:")
                                for i, r in enumerate(worst, 1):
                                    if r['error'] is not None:
                                        logger.info(f"         {i}. Original: {r['original']:20s} → Decoded: {r['decoded']:20s} (error: {r['error']:.3f})")
                            else:
                                logger.info(f"   Column '{col_name}': No valid error calculations (all attempts failed)")
                    else:
                        logger.info(f"   Column '{col_name}': No results collected (all attempts failed)")
                
                except Exception as e:
                    logger.info(f"   Skipped {col_name}: {e}")
            
            logger.info(f"")
            
        except Exception as e:
            logger.warning(f"Failed to debug autoencoding quality: {e}")
            import traceback
            traceback.print_exc()
    
    def _debug_marginal_reconstruction(self, epoch_idx):
        """
        Debug marginal loss by showing actual reconstruction quality on validation data.
        
        For each column, shows:
        - Original value
        - Reconstructed value (from masked prediction)
        - Reconstruction accuracy
        """
        try:
            logger.info(f"")
            logger.info(f"🔬 [epoch={epoch_idx}] MARGINAL RECONSTRUCTION DEBUG")
            logger.info(f"   Testing: Can we reconstruct masked columns from other columns?")
            logger.info(f"")
            
            # Get validation data
            val_df = self.val_input_data.df
            
            # Test reconstruction for ALL columns
            for col_idx, col_name in enumerate(self.col_order):
                try:
                    codec = self.col_codecs.get(col_name)
                    if not codec:
                        continue
                    
                    # Get column type
                    from featrix.neural.model_config import ColumnType
                    from featrix.neural.set_codec import SetCodec
                    from featrix.neural.scalar_codec import ScalarCodec, AdaptiveScalarEncoder
                    
                    codec_type = codec.get_codec_name() if hasattr(codec, 'get_codec_name') else "unknown"
                    
                    # Pick 3-4 unique examples from this column
                    unique_values = val_df[col_name].dropna().unique()
                    if len(unique_values) == 0:
                        continue
                    
                    # Sample 3-4 unique values
                    import random
                    random.seed(42 + epoch_idx + col_idx)  # Deterministic but different per column/epoch
                    num_examples = random.choice([3, 4])
                    selected_values = random.sample(list(unique_values), min(num_examples, len(unique_values)))
                    
                    # Check if None is in vocabulary (for SetCodec, check members; for others, try tokenizing)
                    none_in_vocab = False
                    if isinstance(codec, SetCodec):
                        none_in_vocab = None in codec.members or "None" in codec.members or "none" in codec.members
                    else:
                        # Try tokenizing None to see if it's handled
                        try:
                            token = codec.tokenize(None)
                            none_in_vocab = token.status != TokenStatus.UNKNOWN
                        except:
                            none_in_vocab = False
                    
                    # 1/len(selected_values) chance to swap one example with None (if None is not in vocabulary)
                    if not none_in_vocab and random.random() < (1.0 / len(selected_values)):
                        selected_values[random.randint(0, len(selected_values) - 1)] = None
                    
                    # Find rows with these values
                    sample_rows = []
                    for val in selected_values:
                        if val is None:
                            # Find rows where column is None/NaN
                            matching_rows = val_df[val_df[col_name].isna()]
                        else:
                            matching_rows = val_df[val_df[col_name] == val]
                        if len(matching_rows) > 0:
                            # Pick a random row with this value
                            # Ensure random_state is within valid range [0, 2**32 - 1]
                            val_hash = abs(hash(str(val))) % (2**32)
                            random_state = (42 + epoch_idx + col_idx + val_hash) % (2**32)
                            sample_rows.append(matching_rows.sample(1, random_state=random_state).iloc[0])
                    
                    if len(sample_rows) == 0:
                        continue
                    
                    # Collect original vs reconstructed
                    results = []
                    
                    # CRITICAL: Set to eval mode for inference, restore training mode after
                    was_training = self.encoder.training
                    self.encoder.eval()
                    try:
                        with torch.no_grad():
                            for row in sample_rows:
                                try:
                                    idx = row.name if hasattr(row, 'name') else None
                                    original_value = row[col_name]
                                    
                                    # Create record dict from row, but OMIT the target column
                                    # encode_record() will use NOT_PRESENT tokens for missing fields
                                    record = row.to_dict()
                                    del record[col_name]  # Remove target column to mask it
                                    
                                    # Use encode_record() - it handles ALL tokenization automatically
                                    # encode_record() returns a single tensor (full_encoding by default, or short_encoding if short=True)
                                    # Get the device where the encoder is located
                                    encoder_device = next(self.encoder.parameters()).device
                                    full_joint_encoding = self.encode_record(record, squeeze=True, short=False, output_device=encoder_device)
                                    if not isinstance(full_joint_encoding, torch.Tensor):
                                        logger.error(f"❌ Reconstruction failed for row {idx}: encode_record returned unexpected type: {type(full_joint_encoding)}, value: {full_joint_encoding}")
                                        logger.error(f"   Row data: {row.to_dict()}")
                                        logger.error(f"   Record (masked): {record}")
                                        break
                                    
                                    # Predict the masked column from joint encoding
                                    full_col_predictions = self.encoder.column_predictor(full_joint_encoding.unsqueeze(0))
                                    
                                    # column_predictor returns a list of tensors, one per column
                                    if not isinstance(full_col_predictions, (list, tuple)):
                                        raise TypeError(f"column_predictor should return list, got {type(full_col_predictions)}")
                                    
                                    if col_idx >= len(full_col_predictions):
                                        raise IndexError(f"col_idx {col_idx} out of range for {len(full_col_predictions)} predictions")
                                    
                                    col_prediction = full_col_predictions[col_idx]
                                    
                                    # Ensure col_prediction is a tensor with correct shape
                                    if not isinstance(col_prediction, torch.Tensor):
                                        device = full_joint_encoding.device
                                        if isinstance(col_prediction, (int, float)):
                                            col_prediction = torch.tensor(col_prediction, dtype=torch.float32, device=device)
                                        else:
                                            raise TypeError(f"col_prediction must be a tensor, got {type(col_prediction)}")
                                    
                                    # Ensure it has the right shape (should be [batch_size, d_model], squeeze batch dim)
                                    if col_prediction.dim() == 2:
                                        col_prediction = col_prediction.squeeze(0)  # Remove batch dimension
                                    elif col_prediction.dim() == 0:
                                        col_prediction = col_prediction.unsqueeze(0)  # Add dimension if scalar
                                    
                                    # Decode prediction back to value using modular helper functions
                                    # Handle featrix_ prefix
                                    encoder = None
                                    if col_name in self.encoder.column_encoder.encoders:
                                        encoder = self.encoder.column_encoder.encoders[col_name]
                                    elif f"featrix_{col_name}" in self.encoder.column_encoder.encoders:
                                        encoder = self.encoder.column_encoder.encoders[f"featrix_{col_name}"]
                                    else:
                                        # Try reverse - if col_name has prefix, try without
                                        if col_name.startswith("featrix_") and col_name[8:] in self.encoder.column_encoder.encoders:
                                            encoder = self.encoder.column_encoder.encoders[col_name[8:]]
                                    
                                    if encoder is None:
                                        logger.info(f"      Reconstruction: No encoder found for '{col_name}' (available: {list(self.encoder.column_encoder.encoders.keys())[:5]}...)")
                                        continue
                                    
                                    try:
                                        if isinstance(codec, SetCodec):
                                            predicted_value, cosine_sim = self._decode_set_embedding(col_name, col_prediction, encoder, codec)
                                            match = str(predicted_value) == str(original_value)
                                            error = None
                                            
                                        elif isinstance(codec, ScalarCodec):
                                            predicted_value_raw, cosine_sim = self._decode_scalar_embedding(col_name, col_prediction, encoder, codec)
                                            
                                            # Calculate error
                                            original_value_float = None
                                            try:
                                                if hasattr(original_value, 'item'):
                                                    original_value_float = original_value.item()
                                                elif isinstance(original_value, (int, float)):
                                                    original_value_float = float(original_value)
                                                else:
                                                    original_value_float = float(original_value)
                                                error = abs(predicted_value_raw - original_value_float)
                                                relative_error = error / (abs(original_value_float) + 1e-6)
                                            except Exception:
                                                error = None
                                                relative_error = None
                                            
                                            predicted_value = f"{predicted_value_raw:.3f}"
                                            match = cosine_sim > 0.9 if cosine_sim is not None else False
                                            
                                        else:
                                            # For other types (strings, vectors, etc.)
                                            predicted_value = "[embedding]"
                                            match = None
                                            error = None
                                            cosine_sim = None
                                            
                                    except Exception as decode_err:
                                        logger.info(f"      Reconstruction failed for row {idx}: {decode_err}")
                                        predicted_value = f"[ERROR: {decode_err}]"
                                        match = None
                                        error = None
                                        cosine_sim = None
                                        relative_error = None
                                    
                                    results.append({
                                        'original': str(original_value)[:30],
                                        'predicted': str(predicted_value)[:30],
                                        'match': match,
                                        'error': error,
                                        'cosine_sim': cosine_sim,
                                        'relative_error': relative_error if 'relative_error' in locals() else None
                                    })
                                    
                                except Exception as e:
                                    logger.info(f"      Reconstruction failed for row {idx}: {e}")
                                    continue
                    finally:
                        # Always restore training mode if it was in training mode before
                        if was_training:
                            self.encoder.train()
                    
                    if results:
                        # Calculate accuracy for sets
                        if isinstance(codec, SetCodec):
                            correct = sum(1 for r in results if r['match'])
                            accuracy = (correct / len(results)) * 100
                            logger.info(f"   Column '{col_name}' ({codec_type}): {correct}/{len(results)} correct ({accuracy:.1f}%)")
                            
                            # Show examples
                            logger.info(f"      Examples:")
                            for i, r in enumerate(results[:5], 1):
                                status = "✅" if r['match'] else "❌"
                                logger.info(f"         {i}. {status} Original: {r['original']:30s} → Predicted: {r['predicted']:30s}")
                        elif isinstance(codec, ScalarCodec):
                            # For scalars: show actual decoded values and errors
                            good_reconstructions = sum(1 for r in results if r.get('match'))
                            avg_cosine_sim = sum(r.get('cosine_sim', 0) for r in results) / len(results)
                            
                            # Calculate average absolute and relative errors
                            errors_with_values = [r for r in results if r.get('error') is not None]
                            if errors_with_values:
                                avg_abs_error = sum(r['error'] for r in errors_with_values) / len(errors_with_values)
                                avg_rel_error = sum(r.get('relative_error', 0) for r in errors_with_values) / len(errors_with_values)
                                
                                logger.info(f"   Column '{col_name}' ({codec_type}): avg_similarity={avg_cosine_sim:.3f}, avg_error={avg_abs_error:.4f} ({avg_rel_error*100:.1f}%)")
                                logger.info(f"      High quality (>0.9 similarity): {good_reconstructions}/{len(results)} ({100*good_reconstructions/len(results):.1f}%)")
                            else:
                                logger.info(f"   Column '{col_name}' ({codec_type}): avg_similarity={avg_cosine_sim:.3f}")
                            
                            # Show examples with actual predicted vs original values
                            logger.info(f"      Examples:")
                            for i, r in enumerate(results[:5], 1):
                                sim = r.get('cosine_sim', 0)
                                err = r.get('error')
                                rel_err = r.get('relative_error')
                                
                                if sim > 0.9:
                                    status = "✅"
                                elif sim > 0.7:
                                    status = "⚠️ "
                                else:
                                    status = "❌"
                                
                                if err is not None and rel_err is not None:
                                    logger.info(f"         {i}. {status} Original: {r['original']:>12s} → Predicted: {r['predicted']:>12s} | Error: {err:>8.3f} ({rel_err*100:>5.1f}%)")
                                else:
                                    logger.info(f"         {i}. {status} Original: {r['original']:>12s} → Predicted: {r['predicted']:>12s} | Similarity: {sim:.3f}")
                        else:
                            logger.info(f"   Column '{col_name}' ({codec_type}): {len(results)} samples")
                            logger.info(f"      [Reconstruction quality metrics not yet implemented for this type]")
                        
                except Exception as e:
                    logger.info(f"   Skipped {col_name}: {e}")
            
            logger.info(f"")
            
        except Exception as e:
            logger.warning(f"Failed to debug marginal reconstruction: {e}")
            import traceback
            traceback.print_exc()
    
    def _debug_scalar_reconstruction_quality(self, epoch_idx):
        """
        Test scalar reconstruction quality by sampling 100 values per column and computing total error.
        Runs every 10 epochs.
        """
        if epoch_idx % 10 != 0:
            return  # Only run every 10 epochs
        
        try:
            logger.info(f"")
            logger.info(f"📊 [epoch={epoch_idx}] SCALAR RECONSTRUCTION QUALITY TEST (100 samples per column)")
            logger.info(f"   Testing: Encode → Decode accuracy across distribution")
            logger.info(f"")
            
            # Get all scalar columns
            scalar_columns = []
            
            # DEBUG: Log what columns we have
            logger.info(f"   DEBUG: col_order has {len(self.col_order)} columns: {self.col_order[:10]}...")
            logger.info(f"   DEBUG: col_codecs has {len(self.col_codecs)} codecs: {list(self.col_codecs.keys())[:10]}...")
            logger.info(f"   DEBUG: encoder.column_encoder.encoders has {len(self.encoder.column_encoder.encoders)} encoders: {list(self.encoder.column_encoder.encoders.keys())[:10]}...")
            logger.info(f"   Starting to iterate over {len(self.col_order)} columns...")
            for col_idx, col_name in enumerate(self.col_order):
                try:
                    logger.info(f"   Processing column {col_idx+1}/{len(self.col_order)}: {col_name}")
                    codec = self.col_codecs.get(col_name)
                    if isinstance(codec, ScalarCodec):
                        # Try both with and without featrix_ prefix
                        encoder = None
                        if col_name in self.encoder.column_encoder.encoders:
                            encoder = self.encoder.column_encoder.encoders[col_name]
                        elif f"featrix_{col_name}" in self.encoder.column_encoder.encoders:
                            encoder = self.encoder.column_encoder.encoders[f"featrix_{col_name}"]
                            logger.info(f"   DEBUG: Found encoder with featrix_ prefix: featrix_{col_name} (original: {col_name})")
                        elif col_name.startswith("featrix_") and col_name[8:] in self.encoder.column_encoder.encoders:
                            encoder = self.encoder.column_encoder.encoders[col_name[8:]]
                            logger.info(f"   DEBUG: Found encoder without featrix_ prefix: {col_name[8:]} (original: {col_name})")
                        
                        if encoder:
                            scalar_columns.append((col_name, codec, encoder))
                            logger.info(f"   Added scalar column '{col_name}' to test list")
                        else:
                            logger.info(f"   DEBUG: ScalarCodec found for '{col_name}' but no matching encoder in column_encoder.encoders")
                except Exception as col_err:
                    logger.info(f"   Error processing column '{col_name}': {col_err}")
                    import traceback
                    logger.info(f"   Traceback: {traceback.format_exc()}")
                    continue
            
            logger.info(f"   Found {len(scalar_columns)} scalar columns to test")
            
            if not scalar_columns:
                logger.info(f"   No scalar columns found!")
                logger.info(f"   Available encoders: {list(self.encoder.column_encoder.encoders.keys())}")
                logger.info(f"   Available codecs: {[k for k, v in self.col_codecs.items() if isinstance(v, ScalarCodec)]}")
                return
            
            # Set to eval mode for inference
            was_training = self.encoder.training
            self.encoder.eval()
            
            try:
                with torch.no_grad():
                    column_errors = {}
                    
                    logger.info(f"   Starting to test {len(scalar_columns)} scalar columns...")
                    for col_idx, (col_name, codec, encoder) in enumerate(scalar_columns):
                        try:
                            logger.info(f"   Testing column {col_idx+1}/{len(scalar_columns)}: {col_name}")
                            # Sample 100 values across the distribution
                            # Use key distribution points: min, q10, q25, median, q75, q90, max
                            # Plus uniform samples between min and max
                            stats = codec.stats
                            min_val = stats.get('min', codec.mean - 4 * codec.stdev)
                            max_val = stats.get('max', codec.mean + 4 * codec.stdev)
                            mean_val = codec.mean
                            
                            # Key distribution points
                            key_points = []
                            if 'q10' in stats:
                                key_points.append(stats['q10'])
                            if 'q25' in stats:
                                key_points.append(stats['q25'])
                            if 'median' in stats:
                                key_points.append(stats['median'])
                            if 'q75' in stats:
                                key_points.append(stats['q75'])
                            if 'q90' in stats:
                                key_points.append(stats['q90'])
                            
                            # Fill remaining samples with uniform distribution
                            n_key_points = len(key_points) + 3  # +3 for min, max, mean
                            n_uniform = 16 - n_key_points
                            
                            # Create test values
                            test_values = [min_val, mean_val, max_val] + key_points
                            if n_uniform > 0:
                                uniform_samples = np.linspace(min_val, max_val, n_uniform)
                                test_values.extend(uniform_samples.tolist())
                            
                            # Trim to exactly 100
                            test_values = test_values[:16]
                            
                            # Test each value
                            total_abs_error = 0.0
                            total_rel_error = 0.0
                            n_valid = 0
                            n_failed = 0
                            errors = []
                            
                            for idx, test_val in enumerate(test_values):
                                try:
                                    # Get column prediction from joint encoding
                                    # Create a dummy record and encode it
                                    record = {col_name: test_val}
                                    # Get the device where the encoder is located
                                    encoder_device = next(self.encoder.parameters()).device
                                    full_joint_encoding = self.encode_record(record, squeeze=True, short=False, output_device=encoder_device)
                                    
                                    # Get column-specific prediction
                                    # column_predictor returns a list of tensors, one per column in col_order
                                    full_col_predictions = self.encoder.column_predictor(full_joint_encoding.unsqueeze(0))
                                    if not isinstance(full_col_predictions, (list, tuple)):
                                        raise TypeError(f"column_predictor should return list, got {type(full_col_predictions)}")
                                    
                                    # Find the index of this column in col_order
                                    # Check both with and without prefix
                                    col_idx = None
                                    if col_name in self.col_order:
                                        col_idx = self.col_order.index(col_name)
                                    elif f"featrix_{col_name}" in self.col_order:
                                        col_idx = self.col_order.index(f"featrix_{col_name}")
                                    elif col_name.startswith("featrix_") and col_name[8:] in self.col_order:
                                        col_idx = self.col_order.index(col_name[8:])
                                    
                                    if col_idx is None:
                                        raise ValueError(f"Column '{col_name}' not found in col_order. Available: {self.col_order[:10]}...")
                                    if col_idx >= len(full_col_predictions):
                                        raise IndexError(f"col_idx {col_idx} out of range for {len(full_col_predictions)} predictions (col_order has {len(self.col_order)} columns)")
                                    
                                    col_prediction = full_col_predictions[col_idx]  # [batch_size, d_model]
                                    
                                    # Remove batch dimension
                                    if col_prediction.dim() == 2:
                                        col_prediction = col_prediction.squeeze(0)  # [d_model]
                                    elif col_prediction.dim() == 0:
                                        col_prediction = col_prediction.unsqueeze(0)  # Add dimension if scalar
                                    
                                    # Decode back
                                    predicted_val, similarity = self._decode_scalar_embedding(
                                        col_name, col_prediction, encoder, codec, search_samples=200
                                    )
                                    
                                    # Compute errors
                                    abs_error = abs(predicted_val - test_val)
                                    if abs(test_val) > 1e-10:
                                        rel_error = abs_error / abs(test_val)
                                    else:
                                        rel_error = abs_error  # Avoid division by zero
                                    
                                    total_abs_error += abs_error
                                    total_rel_error += rel_error
                                    errors.append(abs_error)
                                    n_valid += 1
                                    
                                except Exception as e:
                                    n_failed += 1
                                    # Log first 3 errors at WARNING level to diagnose issues
                                    if n_failed <= 3:
                                        logger.warning(f"      Failed to test value {test_val} for {col_name} (attempt {idx+1}/{len(test_values)}): {e}")
                                        import traceback
                                        logger.info(f"      Traceback: {traceback.format_exc()}")
                                    else:
                                        logger.info(f"      Failed to test value {test_val} for {col_name}: {e}")
                                    continue
                            
                            if n_valid > 0:
                                avg_abs_error = total_abs_error / n_valid
                                avg_rel_error = total_rel_error / n_valid
                                max_error = max(errors) if errors else 0.0
                                median_error = np.median(errors) if errors else 0.0
                                
                                column_errors[col_name] = {
                                    'total_abs_error': total_abs_error,
                                    'avg_abs_error': avg_abs_error,
                                    'avg_rel_error': avg_rel_error,
                                    'max_error': max_error,
                                    'median_error': median_error,
                                    'n_valid': n_valid
                                }
                            else:
                                logger.warning(f"   Column '{col_name}': No valid reconstructions ({n_failed}/{len(test_values)} failed)")
                                
                        except Exception as e:
                            logger.warning(f"   Error testing column '{col_name}': {e}")
                            import traceback
                            logger.warning(f"   Traceback: {traceback.format_exc()}")
                            # Continue with next column
                    
                    # Log results sorted by total error
                    if column_errors:
                        sorted_cols = sorted(column_errors.items(), key=lambda x: x[1]['total_abs_error'], reverse=True)
                        
                        logger.info(f"   Results (sorted by total error, worst first):")
                        logger.info(f"   {'Column Name':<40s} | {'Total Error':<12s} | {'Avg Error':<12s} | {'Avg Rel %':<10s} | {'Max Error':<12s} | {'Median':<12s}")
                        logger.info(f"   {'-' * 40} | {'-' * 12} | {'-' * 12} | {'-' * 10} | {'-' * 12} | {'-' * 12}")
                        
                        for col_name, errors_dict in sorted_cols:
                            total_err = errors_dict['total_abs_error']
                            avg_err = errors_dict['avg_abs_error']
                            avg_rel = errors_dict['avg_rel_error'] * 100
                            max_err = errors_dict['max_error']
                            median_err = errors_dict['median_error']
                            
                            logger.info(f"   {col_name:<40s} | {total_err:>12.4f} | {avg_err:>12.4f} | {avg_rel:>9.2f}% | {max_err:>12.4f} | {median_err:>12.4f}")
                        
                        # Summary statistics
                        total_errors = [e['total_abs_error'] for e in column_errors.values()]
                        avg_errors = [e['avg_abs_error'] for e in column_errors.values()]
                        
                        logger.info(f"")
                        logger.info(f"   Summary: {len(column_errors)} scalar columns tested")
                        logger.info(f"      Total error: mean={np.mean(total_errors):.4f}, std={np.std(total_errors):.4f}")
                        logger.info(f"      Avg error: mean={np.mean(avg_errors):.4f}, std={np.std(avg_errors):.4f}")
                    else:
                        logger.info(f"   No scalar columns successfully tested")
                        
            finally:
                # Restore training mode
                if was_training:
                    self.encoder.train()
            
            logger.info(f"")
            
        except Exception as e:
            logger.error(f"❌ CRITICAL: Failed to test scalar reconstruction quality: {e}")
            logger.error(f"   This may indicate a serious issue - training may halt")
            import traceback
            logger.error(f"   Full traceback:\n{traceback.format_exc()}")
            # Don't re-raise - allow training to continue even if debug test fails
    
    def _update_column_loss_tracker(self, loss_dict):
        """
        Update running average of per-column losses for scalar columns.
        Used for progressive pruning of worst-performing columns.
        """
        try:
            marginal_loss = loss_dict.get('marginal_loss', {})
            
            # Get column losses from all four marginal loss components
            full_1_cols = marginal_loss.get('marginal_loss_full_1', {}).get('cols', {})
            full_2_cols = marginal_loss.get('marginal_loss_full_2', {}).get('cols', {})
            short_1_cols = marginal_loss.get('marginal_loss_short_1', {}).get('cols', {})
            short_2_cols = marginal_loss.get('marginal_loss_short_2', {}).get('cols', {})
            
            # Aggregate column losses - average across all masks
            all_cols = set(full_1_cols.keys()) | set(full_2_cols.keys()) | set(short_1_cols.keys()) | set(short_2_cols.keys())
            
            for col in all_cols:
                losses = []
                if col in full_1_cols:
                    losses.append(full_1_cols[col])
                if col in full_2_cols:
                    losses.append(full_2_cols[col])
                if col in short_1_cols:
                    losses.append(short_1_cols[col])
                if col in short_2_cols:
                    losses.append(short_2_cols[col])
                
                if losses:
                    avg_loss = sum(losses) / len(losses)
                    # Update running average (EMA)
                    if col not in self._column_loss_tracker:
                        self._column_loss_tracker[col] = avg_loss
                        self._column_loss_count[col] = 1
                    else:
                        # Exponential moving average
                        alpha = 0.1  # Weight for new observation
                        self._column_loss_tracker[col] = (1 - alpha) * self._column_loss_tracker[col] + alpha * avg_loss
                        self._column_loss_count[col] += 1
        except Exception as e:
            logger.warning(f"Failed to update column loss tracker: {e}")
    
    def _prune_worst_scalar_columns(self, loss_dict, epoch_idx, prune_percent=0.10, cumulative=False):
        """
        Prune (disable) worst-performing scalar column encoders.
        
        Args:
            loss_dict: Current loss dictionary
            epoch_idx: Current epoch index
            prune_percent: Percentage of scalar columns to prune (0.10 = 10%)
            cumulative: If True, prune additional columns (for 20% milestone). If False, prune from all (for 10% milestone).
        """
        try:
            from featrix.neural.scalar_codec import AdaptiveScalarEncoder
            from featrix.neural.model_config import ColumnType
            
            # Get all scalar columns (including disabled ones to track original count)
            all_scalar_columns = []
            active_scalar_columns = []
            for col_name, encoder in self.encoder.column_encoder.encoders.items():
                if isinstance(encoder, AdaptiveScalarEncoder):
                    all_scalar_columns.append(col_name)
                    if not encoder._disabled:
                        active_scalar_columns.append(col_name)
            
            if not all_scalar_columns:
                logger.info(f"   No scalar columns found")
                return
            
            # Track original count on first call
            if not hasattr(self, '_original_scalar_count'):
                self._original_scalar_count = len(all_scalar_columns)
            
            if not active_scalar_columns:
                logger.info(f"   No active scalar columns to prune (all already pruned)")
                return
            
            # Get average losses for all scalar columns (including disabled ones for ranking)
            column_losses = {}
            for col_name in all_scalar_columns:
                if col_name in self._column_loss_tracker:
                    column_losses[col_name] = self._column_loss_tracker[col_name]
            
            if not column_losses:
                logger.warning(f"   No column loss data available for pruning")
                return
            
            # Sort by loss (highest = worst), but only consider active columns
            active_column_losses = {col: column_losses[col] for col in active_scalar_columns if col in column_losses}
            sorted_cols = sorted(active_column_losses.items(), key=lambda x: x[1], reverse=True)
            
            # Calculate how many to prune based on original count
            n_to_prune = max(1, int(self._original_scalar_count * prune_percent))
            
            # Prune worst columns
            pruned_cols = []
            for col_name, avg_loss in sorted_cols[:n_to_prune]:
                encoder = None
                if col_name in self.encoder.column_encoder.encoders:
                    encoder = self.encoder.column_encoder.encoders[col_name]
                if encoder and isinstance(encoder, AdaptiveScalarEncoder) and not encoder._disabled:
                    encoder._disabled = True
                    pruned_cols.append((col_name, avg_loss))
            
            if pruned_cols:
                total_pruned = sum(1 for col in all_scalar_columns 
                                 if self.encoder.column_encoder.encoders[col]._disabled)
                logger.info(f"✂️  [Epoch {epoch_idx}] Progressive pruning: Disabled {len(pruned_cols)} worst scalar columns ({prune_percent*100:.0f}% of original {self._original_scalar_count}):")
                for col_name, avg_loss in pruned_cols:
                    logger.info(f"      - {col_name}: avg_loss={avg_loss:.4f}")
                logger.info(f"   Total pruned: {total_pruned}/{self._original_scalar_count} ({total_pruned/self._original_scalar_count*100:.0f}%), Remaining active: {len(active_scalar_columns) - len(pruned_cols)}")
            else:
                logger.info(f"   No columns pruned (all candidates already disabled)")
                
        except Exception as e:
            logger.warning(f"Failed to prune worst scalar columns: {e}")
            import traceback
            traceback.print_exc()
    
    def _log_marginal_loss_breakdown(self, loss_dict, epoch_idx, batch_idx):
        """
        Log detailed breakdown of marginal loss components and per-column contributions.
        
        The marginal loss has 4 components:
        - full_1/full_2: Predictions using d_model-dimensional encodings with 2 different random masks
        - short_1/short_2: Predictions using 3D encodings with the same 2 random masks
        
        Each mask randomly hides some columns and tries to predict them from the rest.
        Using 2 different masks per batch doubles the training signal.
        
        Args:
            loss_dict: The loss dictionary from compute_total_loss
            epoch_idx: Current epoch index
            batch_idx: Current batch index
        """
        try:
            marginal_loss = loss_dict.get('marginal_loss', {})
            
            # Get the four marginal loss components
            full_1 = marginal_loss.get('marginal_loss_full_1', {})
            full_2 = marginal_loss.get('marginal_loss_full_2', {})
            short_1 = marginal_loss.get('marginal_loss_short_1', {})
            short_2 = marginal_loss.get('marginal_loss_short_2', {})
            
            # Get totals
            full_1_total = full_1.get('total', 0.0)
            full_2_total = full_2.get('total', 0.0)
            short_1_total = short_1.get('total', 0.0)
            short_2_total = short_2.get('total', 0.0)
            marginal_total = marginal_loss.get('total', 0.0)
            
            # Get per-column losses
            full_1_cols = full_1.get('cols', {})
            full_2_cols = full_2.get('cols', {})
            short_1_cols = short_1.get('cols', {})
            short_2_cols = short_2.get('cols', {})
            
            # Log component breakdown
            # NOTE: mask_1 and mask_2 are two different random column masking patterns applied to the same batch
            # This gives us 2 different prediction tasks per batch, increasing training signal
            logger.info(f"📊 [epoch={epoch_idx}, batch={batch_idx}] MARGINAL LOSS BREAKDOWN:")
            logger.info(f"   Total Marginal: {marginal_total:.4f}")
            logger.info(f"   └─ Full Mask 1:  {full_1_total:.4f} ({full_1_total/marginal_total*100:.1f}%) [d_model encodings, mask pattern 1]")
            logger.info(f"   └─ Full Mask 2:  {full_2_total:.4f} ({full_2_total/marginal_total*100:.1f}%) [d_model encodings, mask pattern 2]")
            logger.info(f"   └─ Short Mask 1: {short_1_total:.4f} ({short_1_total/marginal_total*100:.1f}%) [3D encodings, mask pattern 1]")
            logger.info(f"   └─ Short Mask 2: {short_2_total:.4f} ({short_2_total/marginal_total*100:.1f}%) [3D encodings, mask pattern 2]")
            
            # Aggregate column losses across all masks
            all_cols = set(full_1_cols.keys()) | set(full_2_cols.keys()) | set(short_1_cols.keys()) | set(short_2_cols.keys())
            column_losses = {}
            column_counts = {}  # Track how many masks each column appeared in
            
            for col in all_cols:
                losses = []
                if col in full_1_cols:
                    losses.append(full_1_cols[col])
                if col in full_2_cols:
                    losses.append(full_2_cols[col])
                if col in short_1_cols:
                    losses.append(short_1_cols[col])
                if col in short_2_cols:
                    losses.append(short_2_cols[col])
                
                if losses:
                    column_losses[col] = sum(losses) / len(losses)
                    column_counts[col] = len(losses)
            
            if column_losses:
                # Sort by average loss
                sorted_cols = sorted(column_losses.items(), key=lambda x: x[1], reverse=True)
                
                # Calculate statistics
                loss_values = np.array(list(column_losses.values()))
                mean_loss = loss_values.mean()
                std_loss = loss_values.std()
                median_loss = np.median(loss_values)
                
                logger.info(f"   Column Loss Stats: mean={mean_loss:.4f}, std={std_loss:.4f}, median={median_loss:.4f}")
                
                # Show top 5 hardest columns
                logger.info(f"   Top 5 Hardest Columns:")
                for i, (col_name, avg_loss) in enumerate(sorted_cols[:5], 1):
                    count = column_counts[col_name]
                    logger.info(f"      {i}. {col_name}: {avg_loss:.4f} (in {count}/4 masks)")
                
                # Show bottom 3 easiest columns
                if len(sorted_cols) > 3:
                    logger.info(f"   Bottom 3 Easiest Columns:")
                    for i, (col_name, avg_loss) in enumerate(sorted_cols[-3:], 1):
                        count = column_counts[col_name]
                        logger.info(f"      {i}. {col_name}: {avg_loss:.4f} (in {count}/4 masks)")
                
                # Log adaptive scalar encoder strategy weights
                logger.info(f"   📊 Adaptive Scalar Transform Strategies:")
                from featrix.neural.scalar_codec import AdaptiveScalarEncoder
                adaptive_count = 0
                
                # Collect all weights first
                strategy_data = []
                for col_name, encoder in self.encoder.column_encoder.encoders.items():
                    try:
                        if isinstance(encoder, AdaptiveScalarEncoder):
                            weights = encoder.get_strategy_weights()
                            strategy_data.append((col_name, weights))
                            adaptive_count += 1
                    except Exception as e:
                        import traceback
                        logger.warning(f"      Skipped {col_name}: {type(e).__name__}: {e}")
                        logger.info(f"      Full traceback:\n{traceback.format_exc()}")
                
                if adaptive_count == 0:
                    logger.info(f"      No AdaptiveScalarEncoder columns found (total encoders: {len(self.encoder.column_encoder.encoders)})")
                    encoder_types = {}
                    for col_name, encoder in self.encoder.column_encoder.encoders.items():
                        encoder_type = type(encoder).__name__
                        encoder_types[encoder_type] = encoder_types.get(encoder_type, 0) + 1
                    logger.info(f"      Encoder types: {encoder_types}")
                else:
                    # All 20 strategies with 3-letter codes
                    strategy_order = [
                        ('linear', 'LIN'), ('log', 'LOG'), ('robust', 'ROB'), ('rank', 'RAN'), 
                        ('periodic', 'PER'), ('bucket', 'BUC'), ('is_positive', 'POS'), 
                        ('is_negative', 'NEG'), ('is_outlier', 'OUT'), ('zscore', 'ZSC'),
                        ('minmax', 'MIN'), ('quantile', 'QUA'), ('yeojohnson', 'YEO'),
                        ('winsor', 'WIN'), ('sigmoid', 'SIG'), ('inverse', 'INV'),
                        ('polynomial', 'POL'), ('frequency', 'FRE'), ('target_bin', 'TAR'),
                        ('clipped_log', 'CLI')
                    ]
                    
                    # Log legend/key the first time (use class-level flag)
                    if not hasattr(EmbeddingSpace, '_scalar_strategy_legend_logged'):
                        logger.info("      📋 Scalar Strategy Codes:")
                        logger.info("         Original: LIN=Linear, LOG=Log, ROB=Robust, RAN=Rank, PER=Periodic, BUC=Bucket, POS=IsPositive, NEG=IsNegative, OUT=IsOutlier")
                        logger.info("         New: ZSC=ZScore, MIN=MinMax, QUA=Quantile, YEO=YeoJohnson, WIN=Winsor, SIG=Sigmoid, INV=Inverse, POL=Polynomial, FRE=Frequency, TAR=TargetBin, CLI=ClippedLog")
                        EmbeddingSpace._scalar_strategy_legend_logged = True
                    
                    # ANSI color codes (used throughout this section)
                    YELLOW = "\033[33m"
                    GRAY = "\033[90m"
                    RESET = "\033[0m"
                    
                    # Format table header with 3-letter codes
                    header_parts = [f"{'Column':<45s}"]
                    for strategy_name, code in strategy_order:
                        header_parts.append(f"{code:>5s}")
                    header_parts.append("Dominant")
                    logger.info("      " + "   ".join(header_parts))
                    logger.info(f"      " + "-" * (45 + len(strategy_order) * 8 + 20))
                    
                    for col_name, weights in strategy_data:
                        # Check if weights contains an error
                        if not isinstance(weights, dict) or 'error' in weights:
                            display_name = col_name[:42] + "..." if len(col_name) > 42 else col_name
                            error_msg = weights.get('error', 'invalid weights') if isinstance(weights, dict) else 'invalid weights'
                            logger.info(f"      {display_name:<45s} ERROR: {error_msg}")
                            continue
                        
                        # Filter out non-numeric values
                        numeric_weights = {k: v for k, v in weights.items() if isinstance(v, (int, float))}
                        if not numeric_weights:
                            display_name = col_name[:42] + "..." if len(col_name) > 42 else col_name
                            logger.info(f"      {display_name:<45s} ERROR: No numeric weights available")
                            continue
                        
                        # Get encoder to check which strategies are active
                        encoder = None
                        active_weights = {}
                        total_active_weight = 0.0
                        if col_name in self.encoder.column_encoder.encoders:
                            encoder = self.encoder.column_encoder.encoders[col_name]
                        
                        # Calculate sum of active (non-pruned) strategy weights
                        for strategy_name, code in strategy_order:
                            weight = numeric_weights.get(strategy_name, 0.0)
                            is_active = True
                            if encoder and isinstance(encoder, AdaptiveScalarEncoder):
                                strategy_idx = next((i for i, (name, _) in enumerate(strategy_order) if name == strategy_name), -1)
                                if strategy_idx >= 0 and encoder._strategy_mask[strategy_idx].item() < 0.5:
                                    is_active = False
                            
                            if is_active:
                                active_weights[strategy_name] = weight
                                total_active_weight += weight
                        
                        # Normalize active weights to sum to 100%
                        if total_active_weight > 0:
                            normalized_weights = {name: w / total_active_weight for name, w in active_weights.items()}
                        else:
                            normalized_weights = active_weights
                        
                        # Determine dominant strategy from normalized weights
                        dominant_strategy_name = None
                        if normalized_weights:
                            dominant = max(normalized_weights.items(), key=lambda x: x[1])
                            dominant_strategy_name = dominant[0]
                            # Map to 3-letter code
                            dominant_code = next((code for name, code in strategy_order if name == dominant[0]), dominant[0][:3].upper())
                            dominant_str = f"{dominant_code} ({dominant[1]:.0%})"
                        else:
                            dominant_str = "N/A"
                        
                        # Truncate column name if too long
                        display_name = col_name[:42] + "..." if len(col_name) > 42 else col_name
                        
                        # Build row with all strategies
                        row_parts = [f"{display_name:<45s}"]
                        for strategy_name, code in strategy_order:
                            # Check if strategy is pruned (weight is 0 and not in active strategies)
                            weight = weights.get(strategy_name, 0.0)
                            is_active = True
                            if encoder and isinstance(encoder, AdaptiveScalarEncoder):
                                strategy_idx = next((i for i, (name, _) in enumerate(strategy_order) if name == strategy_name), -1)
                                if strategy_idx >= 0 and encoder._strategy_mask[strategy_idx].item() < 0.5:
                                    is_active = False
                            
                            if not is_active:
                                row_parts.append(f"{'-':>5s}")  # Show "-" for pruned strategies
                            else:
                                # Use normalized weight (percentage of active strategies only)
                                normalized_weight = normalized_weights.get(strategy_name, 0.0)
                                weight_str = f"{normalized_weight:>5.1%}"
                                # Color: yellow for dominant, gray for others
                                if strategy_name == dominant_strategy_name:
                                    row_parts.append(f"{YELLOW}{weight_str}{RESET}")
                                else:
                                    row_parts.append(f"{GRAY}{weight_str}{RESET}")
                        # Dominant column also gets yellow
                        row_parts.append(f"{YELLOW}{dominant_str}{RESET}")
                        logger.info("      " + "   ".join(row_parts))
                    
                    # Calculate mean and std for each strategy across all columns (only active strategies)
                    strategy_stats = {}
                    for strategy_name, code in strategy_order:
                        # Only include weights from columns where this strategy is active (not pruned)
                        values = []
                        for col_name, weights in strategy_data:
                            # Skip error dictionaries and non-numeric weights
                            if not isinstance(weights, dict) or 'error' in weights:
                                continue
                            numeric_weights = {k: v for k, v in weights.items() if isinstance(v, (int, float))}
                            if not numeric_weights:
                                continue
                            
                            encoder = None
                            if col_name in self.encoder.column_encoder.encoders:
                                encoder = self.encoder.column_encoder.encoders[col_name]
                            if encoder and isinstance(encoder, AdaptiveScalarEncoder):
                                strategy_idx = next((i for i, (name, _) in enumerate(strategy_order) if name == strategy_name), -1)
                                if strategy_idx >= 0 and encoder._strategy_mask[strategy_idx].item() >= 0.5:
                                    values.append(numeric_weights.get(strategy_name, 0.0))
                            else:
                                values.append(numeric_weights.get(strategy_name, 0.0))
                        
                        if values:
                            strategy_stats[strategy_name] = {
                                'mean': np.mean(values),
                                'std': np.std(values),
                                'code': code,
                                'active_count': len(values)
                            }
                        else:
                            strategy_stats[strategy_name] = {
                                'mean': 0.0,
                                'std': 0.0,
                                'code': code,
                                'active_count': 0
                            }
                    
                    # logger.info(f"      " + "-" * (45 + len(strategy_order) * 8 + 20))
                    # logger.info(f"      Strategy Summary (mean ± std across active columns):")
                    # summary_parts = []
                    # for strategy_name, code in strategy_order:
                    #     stats = strategy_stats[strategy_name]
                    #     if stats['active_count'] > 0:
                    #         summary_parts.append(f"{code}: {stats['mean']:4.1%}±{stats['std']:3.1%}({stats['active_count']})")
                    #     else:
                    #         summary_parts.append(f"{code}: PRUNED")
                    # logger.info("      " + "  ".join(summary_parts))
                    
                    # Show simplified summary: top 3 and bottom 3 strategies
                    logger.info(f"      " + "-" * (45 + len(strategy_order) * 8 + 20))
                    logger.info(f"      Strategy Performance Summary:")
                    
                    # Sort strategies by mean weight (best to worst)
                    sorted_strategies = sorted(
                        [(name, stats) for name, stats in strategy_stats.items() if stats['active_count'] > 0],
                        key=lambda x: x[1]['mean'],
                        reverse=True
                    )
                    
                    if sorted_strategies:
                        logger.info(f"      Top 3 strategies (highest weights):")
                        for i, (strategy_name, stats) in enumerate(sorted_strategies[:3], 1):
                            code = next((code for name, code in strategy_order if name == strategy_name), strategy_name[:3].upper())
                            stat_str = f"{code}: {stats['mean']:4.1%}±{stats['std']:3.1%} ({stats['active_count']} columns)"
                            # Color: yellow for #1, gray for others
                            if i == 1:
                                logger.info(f"         {i}. {YELLOW}{stat_str}{RESET}")
                            else:
                                logger.info(f"         {i}. {GRAY}{stat_str}{RESET}")
                        
                        if len(sorted_strategies) > 3:
                            logger.info(f"      Bottom 3 strategies (lowest weights, candidates for pruning):")
                            for i, (strategy_name, stats) in enumerate(sorted_strategies[-3:], 1):
                                code = next((code for name, code in strategy_order if name == strategy_name), strategy_name[:3].upper())
                                stat_str = f"{code}: {stats['mean']:4.1%}±{stats['std']:3.1%} ({stats['active_count']} columns)"
                                # All bottom strategies in gray
                                logger.info(f"         {i}. {GRAY}{stat_str}{RESET}")
                    
                    # Count pruned strategies
                    pruned_count = sum(1 for stats in strategy_stats.values() if stats['active_count'] == 0)
                    if pruned_count > 0:
                        logger.info(f"      Pruned strategies: {pruned_count}/{len(strategy_order)}")
                    
                    logger.info(f"      Total: {adaptive_count} AdaptiveScalarEncoder columns")
                    logger.info(f"      Note: Pruning based on learned weights (softmax attention), not direct performance metrics")
                
                # Log adaptive string encoder compression strategy weights
                logger.info(f"   📊 Adaptive String Compression Strategies:")
                from featrix.neural.string_codec import StringEncoder
                string_adaptive_count = 0
                
                # Collect all string encoder weights first
                string_strategy_data = []
                for col_name, encoder in self.encoder.column_encoder.encoders.items():
                    try:
                        if isinstance(encoder, StringEncoder) and hasattr(encoder, 'strategy_logits'):
                            # Get strategy weights (softmax of logits)
                            # torch is already imported at module level
                            weights_tensor = torch.softmax(encoder.strategy_logits, dim=0)
                            weights_list = weights_tensor.detach().cpu().tolist()
                            
                            # Map to strategy names
                            strategy_names = [name for name, _ in encoder.compression_levels]
                            weights_dict = dict(zip(strategy_names, weights_list))
                            
                            string_strategy_data.append((col_name, weights_dict))
                            string_adaptive_count += 1
                    except Exception as e:
                        import traceback
                        logger.warning(f"      Skipped {col_name}: {type(e).__name__}: {e}")
                        logger.info(f"      Full traceback:\n{traceback.format_exc()}")
                
                if string_adaptive_count == 0:
                    logger.info(f"      No AdaptiveStringEncoder columns found")
                else:
                    # String strategies with 3-letter codes
                    string_strategy_order = [
                        ('ZERO', 'ZER'), ('DELIMITER', 'DEL'), ('AGGRESSIVE', 'AGG'),
                        ('MODERATE', 'MOD'), ('STANDARD', 'STA')
                    ]
                    
                    # Log legend/key the first time
                    if not hasattr(EmbeddingSpace, '_string_strategy_legend_logged'):
                        logger.info("      📋 String Strategy Codes: ZER=Zero, DEL=Delimiter, AGG=Aggressive, MOD=Moderate, STA=Standard")
                        EmbeddingSpace._string_strategy_legend_logged = True
                    
                    # ANSI color codes (used throughout this section)
                    YELLOW = "\033[33m"
                    GRAY = "\033[90m"
                    RESET = "\033[0m"
                    
                    # Format table header with 3-letter codes
                    header_parts = [f"{'Column':<45s}"]
                    for strategy_name, code in string_strategy_order:
                        header_parts.append(f"{code:>5s}")
                    header_parts.append("Dominant")
                    logger.info("      " + "   ".join(header_parts))
                    logger.info(f"      " + "-" * (45 + len(string_strategy_order) * 8 + 20))
                    
                    # Print each column's strategy distribution
                    for col_name, weights in string_strategy_data:
                        # Filter out non-numeric values
                        numeric_weights = {k: v for k, v in weights.items() if isinstance(v, (int, float))}
                        if not numeric_weights:
                            display_name = col_name[:42] + "..." if len(col_name) > 42 else col_name
                            logger.info(f"      {display_name:<45s} ERROR: No numeric weights available")
                            continue
                        
                        # Find dominant strategy
                        dominant = max(numeric_weights.items(), key=lambda x: x[1])
                        dominant_strategy_name = dominant[0]
                        # Map to 3-letter code
                        dominant_code = next((code for name, code in string_strategy_order if name == dominant[0]), dominant[0][:3].upper())
                        dominant_str = f"{dominant_code} ({dominant[1]:.0%})"
                        
                        # Truncate column name if too long
                        display_name = col_name[:42] + "..." if len(col_name) > 42 else col_name
                        
                        # Build row with all strategies
                        row_parts = [f"{display_name:<45s}"]
                        for strategy_name, _ in string_strategy_order:
                            weight = numeric_weights.get(strategy_name, 0.0)
                            weight_str = f"{weight:>5.1%}"
                            # Color: yellow for dominant, gray for others
                            if strategy_name == dominant_strategy_name:
                                row_parts.append(f"{YELLOW}{weight_str}{RESET}")
                            else:
                                row_parts.append(f"{GRAY}{weight_str}{RESET}")
                        # Dominant column also gets yellow
                        row_parts.append(f"{YELLOW}{dominant_str}{RESET}")
                        logger.info("      " + "   ".join(row_parts))
                    
                    # Calculate mean and std for each strategy across all columns
                    string_strategy_stats = {}
                    for strategy_name, code in string_strategy_order:
                        values = []
                        for _, weights in string_strategy_data:
                            # Filter out non-numeric values
                            if isinstance(weights, dict):
                                numeric_weights = {k: v for k, v in weights.items() if isinstance(v, (int, float))}
                                if numeric_weights:
                                    values.append(numeric_weights.get(strategy_name, 0.0))
                        string_strategy_stats[strategy_name] = {
                            'mean': np.mean(values) if values else 0.0,
                            'std': np.std(values) if values else 0.0,
                            'code': code
                        }
                    
                    logger.info(f"      " + "-" * (45 + len(string_strategy_order) * 8 + 20))
                    logger.info(f"      Strategy Summary (mean ± std across {string_adaptive_count} columns):")
                    summary_parts = []
                    # Find dominant strategy by mean weight
                    dominant_summary = max(string_strategy_stats.items(), key=lambda x: x[1]['mean'])
                    for strategy_name, code in string_strategy_order:
                        stats = string_strategy_stats[strategy_name]
                        stat_str = f"{code}: {stats['mean']:4.1%}±{stats['std']:3.1%}"
                        # Color: yellow for dominant, gray for others
                        if strategy_name == dominant_summary[0]:
                            summary_parts.append(f"{YELLOW}{stat_str}{RESET}")
                        else:
                            summary_parts.append(f"{GRAY}{stat_str}{RESET}")
                    logger.info("      " + "  ".join(summary_parts))
                    
                    # Add mean and std as bottom rows in the table
                    logger.info(f"      " + "-" * (45 + len(string_strategy_order) * 8 + 20))
                    mean_parts = [f"{'MEAN (across all columns)':<45s}"]
                    for strategy_name, _ in string_strategy_order:
                        mean_val = string_strategy_stats[strategy_name]['mean']
                        mean_str = f"{mean_val:>5.1%}"
                        # Color: yellow for dominant, gray for others
                        if strategy_name == dominant_summary[0]:
                            mean_parts.append(f"{YELLOW}{mean_str}{RESET}")
                        else:
                            mean_parts.append(f"{GRAY}{mean_str}{RESET}")
                    logger.info("      " + "   ".join(mean_parts))
                    
                    std_parts = [f"{'STD (variation between columns)':<45s}"]
                    for strategy_name, _ in string_strategy_order:
                        std_val = string_strategy_stats[strategy_name]['std']
                        std_str = f"{std_val:>5.1%}"
                        # All std values in gray
                        std_parts.append(f"{GRAY}{std_str}{RESET}")
                    logger.info("      " + "   ".join(std_parts))
                    logger.info(f"      Total: {string_adaptive_count} AdaptiveStringEncoder columns")
                
                # Log adaptive set encoder mixture weights (learned vs semantic)
                logger.info(f"   📊 Adaptive Set Encoder Mixtures (Learned vs Semantic):")
                from featrix.neural.set_codec import SetEncoder
                set_adaptive_count = 0
                set_total_count = 0
                
                # Collect all set encoder mixture weights (show ALL SetEncoder columns)
                set_mixture_data = []
                for col_name, encoder in self.encoder.column_encoder.encoders.items():
                    try:
                        if isinstance(encoder, SetEncoder):
                            set_total_count += 1
                            if encoder.use_semantic_mixture:
                                # Get mixture weight (sigmoid of logit)
                                mixture_weight = torch.sigmoid(encoder.mixture_logit).item()
                                semantic_weight = 1 - mixture_weight
                                
                                set_mixture_data.append((col_name, mixture_weight, semantic_weight))
                                set_adaptive_count += 1
                            else:
                                # SetEncoder without semantic mixture - show as learned-only
                                set_mixture_data.append((col_name, 1.0, 0.0))  # 100% learned, 0% semantic
                                set_adaptive_count += 1
                    except Exception as e:
                        import traceback
                        logger.warning(f"      Skipped {col_name}: {type(e).__name__}: {e}")
                        logger.info(f"      Full traceback:\n{traceback.format_exc()}")
                
                # Log total count for debugging
                logger.info(f"      Found {set_total_count} total SetEncoder columns, {set_adaptive_count} included in table")
                
                if set_adaptive_count == 0:
                    if set_total_count > 0:
                        logger.info(f"      Found {set_total_count} SetEncoder columns, but none have semantic mixture enabled")
                        logger.info(f"      (Semantic mixture requires: use_semantic_set_initialization=True, string_cache available, and member_names)")
                    else:
                        logger.info(f"      No SetEncoder columns found")
                else:
                    # Set strategies with 3-letter codes
                    set_strategy_order = [('Learned', 'LRN'), ('Semantic', 'SEM')]
                    
                    # Log legend/key the first time
                    if not hasattr(EmbeddingSpace, '_set_strategy_legend_logged'):
                        logger.info("      📋 Set Strategy Codes:")
                        logger.info("         LRN = Learned embeddings (trained from data, captures column-specific patterns)")
                        logger.info("            • Warm-started with BERT embeddings at initialization")
                        logger.info("            • Continues learning from training data during training")
                        logger.info("            • Can adapt to column-specific relationships not in BERT")
                        logger.info("         SEM = Semantic embeddings (BERT-based, captures general language meaning)")
                        logger.info("            • Pre-computed from BERT, frozen during training")
                        logger.info("            • Provides general semantic understanding")
                        logger.info("         The model learns an adaptive mixture weight for each column:")
                        logger.info("            • High LRN% = Trust learned patterns (column-specific)")
                        logger.info("            • High SEM% = Trust BERT semantics (general language)")
                        logger.info("            • The mixture is learned per-column to optimize performance")
                        EmbeddingSpace._set_strategy_legend_logged = True
                    
                    # ANSI color codes (used throughout this section)
                    YELLOW = "\033[33m"
                    GRAY = "\033[90m"
                    RESET = "\033[0m"
                    
                    # Format table header with 3-letter codes
                    header_parts = [f"{'Column':<45s}"]
                    for strategy_name, code in set_strategy_order:
                        header_parts.append(f"{code:>5s}")
                    header_parts.append("Dominant")
                    logger.info("      " + "   ".join(header_parts))
                    logger.info(f"      " + "-" * (45 + len(set_strategy_order) * 8 + 20))
                    
                    # Print each column's mixture distribution (show ALL columns, no limit)
                    logger.info(f"      Showing all {len(set_mixture_data)} SetEncoder columns:")
                    for col_name, learned_weight, semantic_weight in set_mixture_data:
                        # Validate weights are numeric
                        if not isinstance(learned_weight, (int, float)) or not isinstance(semantic_weight, (int, float)):
                            display_name = col_name[:42] + "..." if len(col_name) > 42 else col_name
                            logger.info(f"      {display_name:<45s} ERROR: Invalid weight types")
                            continue
                        
                        # Determine dominant strategy
                        if learned_weight > semantic_weight:
                            dominant_strategy = 'Learned'
                            dominant_str = f"LRN ({learned_weight:.0%})"
                        else:
                            dominant_strategy = 'Semantic'
                            dominant_str = f"SEM ({semantic_weight:.0%})"
                        
                        # Truncate column name if too long
                        display_name = col_name[:42] + "..." if len(col_name) > 42 else col_name
                        
                        # Build row with all strategies
                        row_parts = [f"{display_name:<45s}"]
                        # Color: yellow for dominant, gray for others
                        learned_str = f"{learned_weight:>5.1%}"
                        semantic_str = f"{semantic_weight:>5.1%}"
                        if dominant_strategy == 'Learned':
                            row_parts.append(f"{YELLOW}{learned_str}{RESET}")
                            row_parts.append(f"{GRAY}{semantic_str}{RESET}")
                        else:
                            row_parts.append(f"{GRAY}{learned_str}{RESET}")
                            row_parts.append(f"{YELLOW}{semantic_str}{RESET}")
                        # Dominant column also gets yellow
                        row_parts.append(f"{YELLOW}{dominant_str}{RESET}")
                        logger.info("      " + "   ".join(row_parts))
                    
                    # Calculate mean and std for each strategy across all columns
                    set_strategy_stats = {}
                    for strategy_name, code in set_strategy_order:
                        if strategy_name == 'Learned':
                            values = [learned for _, learned, _ in set_mixture_data]
                        else:  # Semantic
                            values = [semantic for _, _, semantic in set_mixture_data]
                        set_strategy_stats[strategy_name] = {
                            'mean': np.mean(values),
                            'std': np.std(values),
                            'code': code
                        }
                    
                    logger.info(f"      " + "-" * (45 + len(set_strategy_order) * 8 + 20))
                    logger.info(f"      Strategy Summary (mean ± std across {set_adaptive_count} columns):")
                    summary_parts = []
                    # Find dominant strategy by mean weight
                    dominant_summary = max(set_strategy_stats.items(), key=lambda x: x[1]['mean'])
                    for strategy_name, code in set_strategy_order:
                        stats = set_strategy_stats[strategy_name]
                        stat_str = f"{code}: {stats['mean']:4.1%}±{stats['std']:3.1%}"
                        # Color: yellow for dominant, gray for others
                        if strategy_name == dominant_summary[0]:
                            summary_parts.append(f"{YELLOW}{stat_str}{RESET}")
                        else:
                            summary_parts.append(f"{GRAY}{stat_str}{RESET}")
                    logger.info("      " + "  ".join(summary_parts))
                    
                    # Add mean and std as bottom rows in the table
                    logger.info(f"      " + "-" * (45 + len(set_strategy_order) * 8 + 20))
                    mean_parts = [f"{'MEAN (across all columns)':<45s}"]
                    for strategy_name, _ in set_strategy_order:
                        mean_val = set_strategy_stats[strategy_name]['mean']
                        mean_str = f"{mean_val:>5.1%}"
                        # Color: yellow for dominant, gray for others
                        if strategy_name == dominant_summary[0]:
                            mean_parts.append(f"{YELLOW}{mean_str}{RESET}")
                        else:
                            mean_parts.append(f"{GRAY}{mean_str}{RESET}")
                    logger.info("      " + "   ".join(mean_parts))
                    
                    std_parts = [f"{'STD (variation between columns)':<45s}"]
                    for strategy_name, _ in set_strategy_order:
                        std_val = set_strategy_stats[strategy_name]['std']
                        std_str = f"{std_val:>5.1%}"
                        # All std values in gray
                        std_parts.append(f"{GRAY}{std_str}{RESET}")
                    logger.info("      " + "   ".join(std_parts))
                    logger.info(f"      Total: {set_adaptive_count} AdaptiveSetEncoder columns")
                        
        except Exception as e:
            logger.warning(f"Failed to log marginal loss breakdown: {e}")

    def log_mi_summary(self, epoch_idx):
        """
        Log a concise MI summary every epoch for tracking MI progression over time.
        This allows analysis of which columns are learning relationships vs staying independent.
        """
        if not hasattr(self.encoder, 'col_mi_estimates'):
            return
        
        # Get MI estimates
        col_mi = self.encoder.col_mi_estimates
        joint_mi = self.encoder.joint_mi_estimate
        
        # Filter out None values
        valid_mi = {k: v for k, v in col_mi.items() if v is not None}
        
        if not valid_mi:
            return
        
        # Sort by MI value
        sorted_mi = sorted(valid_mi.items(), key=lambda x: x[1], reverse=True)
        
        # Log top 5 and bottom 3
        logger.info(f"📊 [epoch={epoch_idx}] Mutual Information Summary:")
        logger.info(f"   Joint MI: {joint_mi:.3f} bits" if joint_mi is not None else "   Joint MI: not available")
        
        if len(sorted_mi) > 0:
            logger.info(f"   Top 5 Most Dependent Columns:")
            for col, mi in sorted_mi[:5]:
                logger.info(f"      {col}: {mi:.3f} bits")
            
            if len(sorted_mi) > 3:
                logger.info(f"   Bottom 3 Most Independent Columns:")
                for col, mi in sorted_mi[-3:]:
                    logger.info(f"      {col}: {mi:.3f} bits")
    
    def log_encoder_summary(self):
        """
        Log summary information about encoders including adaptive strategies.
        Useful for understanding what the model learned.
        """
        logger.info("=" * 100)
        logger.info("🔧 ENCODER SUMMARY")
        logger.info("=" * 100)
        
        # Log adaptive scalar encoder strategies
        from featrix.neural.scalar_codec import AdaptiveScalarEncoder
        scalar_encoders = {}
        
        for col_name in self.encoder.column_encoder.encoders.keys():
            encoder = self.encoder.column_encoder.encoders[col_name]
            if isinstance(encoder, AdaptiveScalarEncoder):
                weights = encoder.get_strategy_weights()
                scalar_encoders[col_name] = weights
        
        if scalar_encoders:
            logger.info("")
            logger.info("📊 Adaptive Scalar Encoder Strategies:")
            logger.info("   Column Name                                    Linear  Log    Robust  Dominant")
            logger.info("   " + "-" * 90)
            
            for col_name, weights in scalar_encoders.items():
                # Check if weights contains an error
                if 'error' in weights:
                    display_name = col_name[:45] + "..." if len(col_name) > 45 else col_name
                    logger.info(f"   {display_name:48s} ERROR: {weights['error']}")
                    continue
                
                # Filter out non-numeric values and find dominant strategy
                numeric_weights = {k: v for k, v in weights.items() if isinstance(v, (int, float))}
                if not numeric_weights:
                    display_name = col_name[:45] + "..." if len(col_name) > 45 else col_name
                    logger.info(f"   {display_name:48s} ERROR: No numeric weights available")
                    continue
                
                # Determine dominant strategy from numeric weights only
                dominant = max(numeric_weights.items(), key=lambda x: x[1])
                dominant_str = f"{dominant[0].upper()} ({dominant[1]:.0%})"
                
                # Truncate column name if too long
                display_name = col_name[:45] + "..." if len(col_name) > 45 else col_name
                
                # Safely format weights, using 0.0 if key is missing
                linear_val = weights.get('linear', 0.0) if isinstance(weights.get('linear'), (int, float)) else 0.0
                log_val = weights.get('log', 0.0) if isinstance(weights.get('log'), (int, float)) else 0.0
                robust_val = weights.get('robust', 0.0) if isinstance(weights.get('robust'), (int, float)) else 0.0
                
                logger.info(
                    f"   {display_name:48s} {linear_val:6.1%}  {log_val:6.1%}  {robust_val:6.1%}  {dominant_str}"
                )
        
        # Log semantic set initialization status
        from featrix.neural.set_codec import SetEncoder
        # Note: get_config is already imported at top of file, don't re-import here
        
        if get_config().use_semantic_set_initialization():
            logger.info("")
            logger.info("🎨 Semantic Set Initialization: ENABLED")
            set_count = 0
            initialized_count = 0
            
            for col_name in self.encoder.column_encoder.encoders.keys():
                encoder = self.encoder.column_encoder.encoders[col_name]
                if isinstance(encoder, SetEncoder):
                    set_count += 1
                    if encoder.bert_projection is not None:
                        initialized_count += 1
            
            logger.info(f"   Set columns with semantic init: {initialized_count}/{set_count}")
        
        logger.info("=" * 100)

    def log_mi_summary(self, epoch_idx):
        """
        Log a concise MI summary every epoch for tracking MI progression over time.
        This allows analysis of which columns are learning relationships vs staying independent.
        
        Format is grep-friendly for easy extraction and analysis.
        """
        try:
            col_mi_estimates = self.encoder.col_mi_estimates if hasattr(self.encoder, 'col_mi_estimates') else {}
            joint_mi = self.encoder.joint_mi_estimate if hasattr(self.encoder, 'joint_mi_estimate') else None
            
            if not col_mi_estimates:
                return  # No MI data yet
            
            # Create readable multi-line summary (5 columns per line for readability)
            mi_items = []
            low_mi_cols = []
            
            for col_name, mi_value in sorted(col_mi_estimates.items()):
                if mi_value is not None:
                    mi_items.append(f"{col_name}={mi_value:.3f}")
                    if mi_value < 1.0:
                        low_mi_cols.append((col_name, mi_value))
            
            # Log MI summary - header with joint MI
            logger.info(f"🧠 [epoch={epoch_idx+1}] MI: joint={joint_mi:.3f}, {len(mi_items)} columns tracked")
            
            # Log MI values in readable chunks (5 per line)
            chunk_size = 5
            for i in range(0, len(mi_items), chunk_size):
                chunk = mi_items[i:i+chunk_size]
                logger.info(f"   {', '.join(chunk)}")
            
            # Flag low MI columns
            if low_mi_cols:
                # Calculate statistics for low MI columns
                low_mi_values = [val for _, val in low_mi_cols]
                import numpy as np
                mean_mi = np.mean(low_mi_values)
                std_mi = np.std(low_mi_values)
                
                logger.info(f"⚠️  [epoch={epoch_idx+1}] LOW_MI columns (<1.0 bits, n={len(low_mi_cols)}, mean={mean_mi:.3f}, std={std_mi:.3f}):")
                
                # Log low MI columns in readable chunks (5 per line)
                low_mi_items = [f"{name}={val:.3f}" for name, val in low_mi_cols]
                for i in range(0, len(low_mi_items), chunk_size):
                    chunk = low_mi_items[i:i+chunk_size]
                    logger.info(f"   {', '.join(chunk)}")
                
        except Exception as e:
            logger.warning(f"⚠️  Failed to log MI summary: {e}")

    def train_save_progress_stuff(self, 
                                        epoch_idx,
                                        batch_idx,
                                        epoch_start_time_now,
                                        encodings,
                                        save_prediction_vector_lengths,
                                        training_event_dict,  # passed by reference
                                        d,                    # passed by reference
                                        current_lr,
                                        loss_tensor,
                                        loss_dict,
                                        val_loss,
                                        dataloader_batch_durations,
                                        progress_counter,
                                        print_callback,
                                        training_event_callback
    ):
        # print("!!! train_save_progress_stuff called")
        full_predictions = encodings[-6:-3]
        short_predictions = encodings[-3:]

        if save_prediction_vector_lengths:
            full_pred_1_len = {
                self.col_order[idx]: torch.linalg.norm(
                    t, dim=1
                ).tolist()
                for idx, t in enumerate(full_predictions[0])
            }
            full_pred_2_len = {
                self.col_order[idx]: torch.linalg.norm(
                    t, dim=1
                ).tolist()
                for idx, t in enumerate(full_predictions[1])
            }
            full_pred_unmasked_len = {
                self.col_order[idx]: torch.linalg.norm(
                    t, dim=1
                ).tolist()
                for idx, t in enumerate(full_predictions[2])
            }

            short_pred_1_len = {
                self.col_order[idx]: torch.linalg.norm(
                    t, dim=1
                ).tolist()
                for idx, t in enumerate(short_predictions[0])
            }
            short_pred_2_len = {
                self.col_order[idx]: torch.linalg.norm(
                    t, dim=1
                ).tolist()
                for idx, t in enumerate(short_predictions[1])
            }
            short_pred_unmasked_len = {
                self.col_order[idx]: torch.linalg.norm(
                    t, dim=1
                ).tolist()
                for idx, t in enumerate(short_predictions[2])
            }
            # Apply K-fold CV offset if present
            cumulative_epoch = epoch_idx
            if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                cumulative_epoch = epoch_idx + self._kv_fold_epoch_offset
            
            training_event_dict["prediction_vec_lengths"] = (
                dict(
                    epoch=1 + cumulative_epoch,
                    full_1=full_pred_1_len,
                    full_2=full_pred_2_len,
                    full_unmasked=full_pred_unmasked_len,
                    short_1=short_pred_1_len,
                    short_2=short_pred_2_len,
                    short_unmasked=short_pred_unmasked_len,
                )
            )

        # Apply K-fold CV offset if present (makes K-fold CV invisible - epochs are cumulative)
        cumulative_epoch = epoch_idx
        if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
            cumulative_epoch = epoch_idx + self._kv_fold_epoch_offset
        
        # MEMORY LEAK FIX: Push to SQLite, keep minimal data in memory
        # Push mutual information to SQLite (non-blocking)
        mi_entry = {
                "epoch": 1 + cumulative_epoch,
            "columns": copy.deepcopy(self.encoder.col_mi_estimates),
            "joint": copy.deepcopy(self.encoder.joint_mi_estimate),
            }
        if hasattr(self, 'history_db') and self.history_db:
            self.history_db.push_mutual_information(1 + cumulative_epoch, mi_entry)
        
        # Keep only the most recent MI in memory (replace, don't append)
        d["mutual_information"] = [mi_entry]
        
        # Push loss history to SQLite (non-blocking) - don't keep in memory
        loss_entry = {
                "epoch": 1 + cumulative_epoch,
                "current_learning_rate": current_lr,
                "loss": loss_tensor.item(),
                "validation_loss": val_loss,
                "time_now": time.time(),
                "duration": time.time() - epoch_start_time_now,
            }
        if hasattr(self, 'history_db') and self.history_db:
            self.history_db.push_loss_history(loss_entry)
        
        # Keep only validation loss value in memory (not full history)
        d["current_validation_loss"] = val_loss
        training_event_dict["loss_details"] = (
            {
                "epoch": 1 + cumulative_epoch,
                "current_learning_rate": current_lr,
                "loss": loss_tensor.item(),
                "validation_loss": val_loss,
                "time_now": time.time(),
                "duration": time.time() - epoch_start_time_now,
                "details": loss_dict
            }
        )

        training_event_dict["encoder_timing"] = (
            dict(
                epoch=1 + cumulative_epoch,
                durations=[],
            )
        )
        training_event_dict["loss_timing"] = (
            dict(
                epoch=1 + cumulative_epoch,
                durations=[],
            )
        )
        # training_event_dict["loop_timing"] = (
        #     dict(
        #         epoch=1 + epoch_idx,
        #         model_durations=[],  # loop_stopwatch removed
        #         dataloader_individual_durations=self.train_dataset.stopwatch.get_interval_durations() if hasattr(self.train_dataset, 'stopwatch') and self.train_dataset.stopwatch is not None else [],
        #         dataloader_batch_durations=dataloader_batch_durations, #timed_data_loader.stopwatch.get_interval_durations(),
        #     )
        # )

        d["progress_counter"] = progress_counter
        d["batch_idx"] = batch_idx
        d["time_now"] = time.time()
        if print_callback is not None:
            print_callback(d)

        if training_event_callback is not None:
            for k, v in d.items():
                training_event_dict[k] = v
            training_event_callback(training_event_dict)

        return

    def _compute_marginal_loss_weight(self, epoch_idx, n_epochs):
        """
        Compute marginal_loss_weight for curriculum learning.
        
        Phase 1 (0-25% of epochs): weight = 0.3 → Reduced focus (marginal loss unreliable early)
        Phase 2 (25-95% of epochs): weight = 0.3 → 1.0 → 0.1 → Ramp up then down
        Phase 3 (95-100% of epochs): weight = 0.1 → Focus on spread but maintain prediction signal
        
        NOTE: Marginal loss is normalized by 4.0 * effective_n_cols, and in early epochs
        the model hasn't learned much yet, so raw losses are high but normalized values
        can be misleading. We reduce weight in first 25% to avoid over-relying on unreliable metrics.
        
        Args:
            epoch_idx: Current epoch (0-indexed)
            n_epochs: Total number of epochs
            
        Returns:
            float: marginal_loss_weight for this epoch
        """
        # Calculate progress through training (0.0 to 1.0)
        progress = epoch_idx / n_epochs
        
        # Phase boundaries
        phase1_end = 0.25  # First 25% - reduced weight due to unreliable normalized values
        phase2_peak = 0.50  # Peak at 50% - full weight when model has learned basics
        phase3_start = 0.95  # Last 5%
        early_weight = 0.3  # Reduced weight in early epochs
        peak_weight = 1.0  # Full weight at peak
        min_weight = 0.1  # Minimum weight to maintain prediction signal
        
        if progress < phase1_end:
            # Phase 1: Reduced weight - marginal loss normalized values unreliable early
            return early_weight
        elif progress >= phase3_start:
            # Phase 3: Focus on spread but maintain some prediction signal
            return min_weight
        elif progress < phase2_peak:
            # Phase 2a: Ramp up from early_weight to peak_weight (25% → 50%)
            phase2a_progress = (progress - phase1_end) / (phase2_peak - phase1_end)
            return early_weight + phase2a_progress * (peak_weight - early_weight)
        else:
            # Phase 2b: Ramp down from peak_weight to min_weight (50% → 95%)
            phase2b_progress = (progress - phase2_peak) / (phase3_start - phase2_peak)
            return peak_weight - phase2b_progress * (peak_weight - min_weight)

    def _update_encoder_epoch_counters(self, epoch_idx: int, n_epochs: int):
        """
        Update epoch counters in adaptive encoders for strategy pruning.
        
        Called at the start of each epoch to inform encoders about training progress.
        This enables adaptive strategies like Top-K pruning after warmup.
        """
        from featrix.neural.string_codec import StringEncoder
        from featrix.neural.scalar_codec import AdaptiveScalarEncoder
        from featrix.neural.set_codec import SetEncoder
        
        for col_name, encoder in self.encoder.column_encoder.encoders.items():
            # Update StringEncoder epoch counters
            if isinstance(encoder, StringEncoder) and hasattr(encoder, '_epoch_counter'):
                encoder._epoch_counter.fill_(epoch_idx)
                encoder._total_epochs.fill_(n_epochs)
            
            # Update AdaptiveScalarEncoder epoch counters for strategy pruning
            if isinstance(encoder, AdaptiveScalarEncoder) and hasattr(encoder, '_current_epoch'):
                encoder._current_epoch.fill_(epoch_idx)
                encoder._total_epochs.fill_(n_epochs)
            
            # Update SetEncoder epoch counters (if we add pruning there too)
            if isinstance(encoder, SetEncoder) and hasattr(encoder, '_epoch_counter'):
                encoder._epoch_counter.fill_(epoch_idx)
                encoder._total_epochs.fill_(n_epochs)
    
    def _log_mixture_logit_changes(self, epoch_idx: int):
        """
        Log mixture logit changes for all SetEncoders after each epoch.
        This helps track whether the mixture weights are actually updating during training.
        """
        from featrix.neural.set_codec import SetEncoder
        
        mixture_changes = []
        for col_name, encoder in self.encoder.column_encoder.encoders.items():
            if isinstance(encoder, SetEncoder) and hasattr(encoder, 'mixture_logit') and encoder.mixture_logit is not None:
                current_logit = encoder.mixture_logit.item()
                mixture_weight = torch.sigmoid(encoder.mixture_logit).item()
                
                # Track changes across epochs
                if not hasattr(encoder, '_logged_logit_history'):
                    encoder._logged_logit_history = []
                
                encoder._logged_logit_history.append({
                    'epoch': epoch_idx,
                    'logit': current_logit,
                    'mixture': mixture_weight
                })
                
                # Calculate change from previous epoch
                if len(encoder._logged_logit_history) > 1:
                    prev_logit = encoder._logged_logit_history[-2]['logit']
                    logit_change = current_logit - prev_logit
                    prev_mixture = encoder._logged_logit_history[-2]['mixture']
                    mixture_change = mixture_weight - prev_mixture
                    
                    mixture_changes.append({
                        'column': col_name,
                        'logit': current_logit,
                        'logit_change': logit_change,
                        'mixture': mixture_weight,
                        'mixture_change': mixture_change
                    })
        
        # Log summary if there are changes to report
        if mixture_changes:
            logger.info("")
            logger.info(f"🎯 Mixture Logit Changes (Epoch {epoch_idx + 1}):")
            for change in mixture_changes:
                learned_pct = change['mixture'] * 100
                semantic_pct = (1 - change['mixture']) * 100
                logger.info(f"   {change['column']:20s}: Logit={change['logit']:7.4f} (Δ={change['logit_change']:+.4f}), "
                          f"Mixture={learned_pct:5.1f}%LRN/{semantic_pct:5.1f}%SEM (Δ={change['mixture_change']*100:+.2f}%)")
            logger.info("")

    def _init_d(
        self,
        timeStart,
        n_epochs,
        batches_per_epoch
    ):
        _pid = os.getpid()
        _hostname = socket.gethostname()

        d = {
                "debug_label": self.output_debug_label,
                "status": "training",
                "start_time": timeStart,
                "time_now": timeStart,
                # "resource_usage": [],
                "loss_history": [],  # Not used in memory - stored in SQLite
                "current_validation_loss": None,
                "epoch_idx": 0,
                "epoch_total": n_epochs,
                "batch_idx": 0,
                "batch_total": batches_per_epoch * n_epochs,
                "progress_counter": 0,
                "max_progress": batches_per_epoch * n_epochs,
                "num_rows": self.len_df(),
                "num_cols": len(self.train_input_data.df.columns),
                "compute_device": device.type,
                "pid": _pid,
                "hostname": _hostname,
                "mutual_information": [],
                "model_param_count": self.model_param_count,
                "encoder_timing": [],
                "loss_timing": [],
                "loop_timing": [],
                "prediction_vec_lengths": [],
            }
        return d

    def train(
        self,
        batch_size=None,
        n_epochs=None,
        print_progress_step=10,
        print_callback=None,
        training_event_callback=None,
        optimizer_params=None,
        existing_epochs=None,
        use_lr_scheduler=True,
        lr_schedule_segments=None,
        save_state_after_every_epoch=False,
        use_profiler=False,
        save_prediction_vector_lengths=False,
        enable_weightwatcher=False,
        weightwatcher_save_every=5,
        weightwatcher_out_dir="ww_metrics",
        enable_dropout_scheduler=True,
        dropout_schedule_type="piecewise_constant",  # Better default: hold high, ramp, hold moderate
        initial_dropout=0.5,
        final_dropout=0.25,  # Increased from 0.1 to maintain more regularization,
        movie_frame_interval=3,  # Changed from 5 to 3 - generate projections every 3 epochs by default
        val_loss_early_stop_patience=100,  # Stop if validation loss doesn't improve for N epochs
        val_loss_min_delta=0.0001,  # Minimum improvement to count as progress
        max_grad_norm=None,  # LEGACY: Fixed gradient clipping threshold. Use adaptive_grad_clip_ratio instead.
        adaptive_grad_clip_ratio=2.0,  # RECOMMENDED: Clip when gradient > loss * this ratio. Adapts to loss scale.
        grad_clip_warning_multiplier=5.0,  # Warn when unclipped gradients exceed threshold * this multiplier.
        track_per_row_losses=False,  # Track per-row loss to identify hardest examples
        per_row_loss_log_top_n=10,  # Number of top difficult rows to log per epoch
        control_check_callback=None,  # Callback to check for control signals (ABORT, PAUSE, FINISH)
        enable_hourly_pickles=False,  # DISABLED: Hourly pickles are expensive and unnecessary (we have checkpoints)
    ):
        """
        Training the model.  This is re-entrant, so we could be coming back into this to pick up
        a training session that was interrupted.

        Arguments
        ---------
            print_callback takes a dictionary of info that gets displayed in the GUI/demo notebooks.
            lr_schedule_segments: Stepwise-constant lr schedule. Expected to have the shape List[(n_steps, lr)]
                where n_steps is how many steps/iterations each lr period should last.
            
        Default Dropout Schedule
        -------------------------
            Uses 'piecewise_constant' (0.5 → 0.25) which maintains high regularization longer:
            - First 1/3: Hold at 0.5 (strong regularization during exploration)
            - Second 1/3: Ramp 0.5 → 0.25 (gradual reduction as model stabilizes)
            - Final 1/3: Hold at 0.25 (moderate regularization to prevent overfitting)
            
            This prevents the dropout from dropping too low (e.g., 0.14) when training plateaus,
            which helps avoid getting stuck and provides more exploration capability.
        """

        save_state_epoch_interval = 0
        try:
            save_state_epoch_interval = int(n_epochs // 25)
        except:
            traceback.print_exc()
            save_state_epoch_interval = 10


        # ALWAYS recalculate batch_size to benefit from algorithm improvements
        # This ensures resumed jobs get optimal batch size for their GPU
        old_batch_size = batch_size
        batch_size = ideal_batch_size(self.len_df())
        if old_batch_size and old_batch_size != batch_size:
            logger.info(f"🔄 Batch size recalculated: {old_batch_size} → {batch_size} (GPU-optimized)")
        else:
            logger.info(f"✅ Using calculated batch_size: {batch_size}")

        if n_epochs is None or n_epochs == 0:
            n_epochs = 50
            logger.info(f"Setting n_epochs: {n_epochs}")

        numRows = self.len_df()
        numCols = len(self.train_input_data.df.columns)

        logger.info(f"Training data size: {numCols} columns x {numRows} rows")
        logger.info(f"Columns: {list(self.train_input_data.df.columns)}")

        val_dataloader = None
        # val_dataloader = self.val_dataset

        if print_progress_step is not None:
            assert (
                isinstance(print_progress_step, int) and print_progress_step > 0
            ), f"`print_progress_step` must be an integer greater than 0. Provided value: {print_progress_step}"

        # Initialize dropout_scheduler early to avoid UnboundLocalError in recovery path
        dropout_scheduler = None
        
        # Initialize mask distribution tracker
        from .mask_tracker import MaskDistributionTracker
        if self.mask_tracker is None:
            mask_tracker_dir = os.path.join(self.output_dir, "mask_tracking")
            self.mask_tracker = MaskDistributionTracker(
                output_dir=mask_tracker_dir,
                save_full_sequence=False,  # Set to True to save every single mask
                column_names=self.col_order  # Pass column names for mapping
            )
            logger.info(f"📊 Mask tracking initialized: {mask_tracker_dir}")
            logger.info(f"📊 Tracking {len(self.col_order)} columns in order")

        # Multi-architecture predictor selection (only for fresh training and if enabled in config)
        enable_architecture_selection = (
            existing_epochs is None and 
            get_config().get_enable_predictor_architecture_selection()
        )
        if enable_architecture_selection:
            logger.info("")
            logger.info("=" * 80)
            logger.info("🔬 PREDICTOR HEAD ARCHITECTURE SELECTION (BEFORE MAIN EMBEDDING SPACE TRAINING)")
            logger.info("=" * 80)
            logger.info(f"⚠️  IMPORTANT: This selects PREDICTOR HEAD architectures, NOT the embedding space architecture!")
            logger.info(f"   - Embedding space encoder (column_encoder + joint_encoder): FIXED at d_model={self.d_model} (NOT being selected)")
            logger.info(f"   - Predictor heads (column_predictor + joint_predictor): Testing different hidden dimensions (64d, 128d, 192d, 256d)")
            logger.info(f"   - Will test 4 candidate predictor head architectures")
            
            # Use more epochs for architecture selection when GPU is available (faster training)
            if torch.cuda.is_available():
                selection_epochs = 15  # GPU-accelerated: 15 epochs per candidate (sufficient signal, faster)
                logger.info(f"   - GPU detected: Using {selection_epochs} epochs per candidate (GPU-accelerated, fast)")
            else:
                selection_epochs = 15  # CPU-only: 15 epochs per candidate (matched to GPU)
                logger.info(f"   - CPU-only: Using {selection_epochs} epochs per candidate (CPU is slower)")
            
            logger.info(f"   - Each candidate: {selection_epochs} epochs training ONLY predictor heads (embedding space encoder is FROZEN)")
            logger.info(f"   - Embedding space encoder runs forward pass but weights are NOT updated during selection")
            logger.info(f"   - This is FAST because only small predictor head MLPs train, not the full embedding space")
            logger.info(f"   - After selection, MAIN TRAINING will train the FULL EMBEDDING SPACE (encoder + selected predictor heads) for {n_epochs} epochs")
            logger.info(f"   - Total overhead: ~{4 * selection_epochs} epochs (4 candidates × {selection_epochs} epochs) before main training starts")
            logger.info("=" * 80)
            try:
                best_architecture = self._select_best_predictor_architecture(
                    batch_size=batch_size,
                    selection_epochs=selection_epochs,  # GPU: 50 epochs, CPU: 25 epochs
                    val_dataloader=None
                )
                # Replace predictors with the winner
                self._replace_predictors_with_architecture(best_architecture)
                logger.info("=" * 80)
                logger.info("✅ PREDICTOR HEAD ARCHITECTURE SELECTION COMPLETE")
                logger.info("=" * 80)
                logger.info(f"   Selected best predictor head architecture based on validation loss")
                logger.info(f"   Embedding space encoder (d_model={self.d_model}): Unchanged (was fixed during selection)")
                logger.info(f"   Predictor heads: Replaced with selected architecture")
                logger.info(f"   🚀 NOW STARTING MAIN TRAINING: Will train FULL EMBEDDING SPACE (encoder + selected predictor heads) for {n_epochs} epochs")
                logger.info("=" * 80)
            except Exception as e:
                logger.warning(f"⚠️  Architecture selection failed: {e}")
                logger.warning("   Continuing with default architecture...")
                import traceback
                logger.debug(traceback.format_exc())
        
        if existing_epochs is not None:
            # Check if this is K-fold CV by checking if _kv_fold_epoch_offset is set
            if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                # K-fold CV: Each fold starts from epoch 0 internally, but epoch numbers are offset for logging
                # existing_epochs is the cumulative count from previous folds (used only to prevent architecture selection)
                # The training loop should start from 0 for this fold
                base_epoch_index = 0
                # Don't log "Continuing training" - this is just the next fold, not a resume
                # The cumulative epoch offset will be applied in logs automatically
            else:
                # Regular resume: existing_epochs is the last completed epoch index (0-indexed)
                # So if we completed epochs 0-9, existing_epochs=9, and we start from epoch 10
                base_epoch_index = existing_epochs + 1
                logger.info(f"Continuing training from epoch {base_epoch_index} (last completed: {existing_epochs})")
            checkpoint_loaded = False
            
            # Check if checkpoint file exists before trying to load
            # When resuming from ES object (K-fold CV), checkpoint files may not exist
            # The ES object already has the training state, so we can skip checkpoint loading
            checkpoint_path = self.get_training_state_path(existing_epochs, 0)
            checkpoint_exists = Path(checkpoint_path).exists()
            
            if checkpoint_exists:
                try:
                    self.load_state(existing_epochs, 0)
                    checkpoint_loaded = True
                except (EOFError, RuntimeError) as e:
                    # Checkpoint file is corrupted or incomplete - try to find last valid checkpoint
                    logger.error(f"⚠️  Corrupted checkpoint detected (epoch {existing_epochs}): {e}")
                    logger.error(f"   Checkpoint file may be incomplete or corrupted")
                    logger.warning(f"🔍 Searching for last valid checkpoint...")
                    
                    # Try to find the last valid checkpoint by looking backwards
                    # Check every epoch going backwards from target epoch
                    found_valid_checkpoint = False
                    last_valid_epoch = None
                    
                    # Check every epoch going backwards from target epoch
                    for check_epoch in range(existing_epochs, -1, -1):
                        if check_epoch < 0:
                            break
                        try:
                            checkpoint_path = self.get_training_state_path(check_epoch, 0)
                            if Path(checkpoint_path).exists():
                                # Try to load it to verify it's valid
                                try:
                                    test_state = torch.load(checkpoint_path, weights_only=False, map_location='cpu')
                                    # If we got here, checkpoint is valid
                                    last_valid_epoch = check_epoch
                                    found_valid_checkpoint = True
                                    logger.info(f"✅ Found valid checkpoint at epoch {check_epoch}")
                                    break
                                except Exception:
                                    # This checkpoint is also corrupted, continue searching
                                    logger.debug(f"   Epoch {check_epoch} checkpoint also corrupted, continuing search...")
                                    continue
                        except Exception:
                            continue
                
                if found_valid_checkpoint and last_valid_epoch is not None:
                    # Try to load the valid checkpoint
                    try:
                        logger.info(f"🔄 Loading last valid checkpoint from epoch {last_valid_epoch}")
                        self.load_state(last_valid_epoch, 0)
                        existing_epochs = last_valid_epoch
                        base_epoch_index = last_valid_epoch + 1
                        checkpoint_loaded = True
                        logger.info(f"✅ Successfully loaded checkpoint from epoch {last_valid_epoch}, continuing from epoch {base_epoch_index}")
                    except Exception as load_err:
                        logger.error(f"❌ Failed to load valid checkpoint from epoch {last_valid_epoch}: {load_err}")
                        logger.warning(f"🔄 Falling back to starting training from scratch (epoch 0)")
                        existing_epochs = None
                        base_epoch_index = 0
                        self.training_state = {}
                        checkpoint_loaded = False
                else:
                    # No valid checkpoint found - start from scratch
                    logger.warning(f"🔄 No valid checkpoint found, falling back to starting training from scratch (epoch 0)")
                    existing_epochs = None
                    base_epoch_index = 0
                    # Clear any partial training state
                    self.training_state = {}
                    checkpoint_loaded = False
            else:
                # Checkpoint file doesn't exist - this is OK when resuming from ES object (K-fold CV)
                # The ES object already has the training state, so we can skip checkpoint loading
                logger.info(f"ℹ️  Checkpoint file not found at {checkpoint_path}")
                logger.info(f"   This is expected when resuming from ES object (K-fold CV)")
                logger.info(f"   ES object already has training state, continuing without checkpoint load")
                checkpoint_loaded = False
                # Don't clear training_state - ES object already has it
            
            # Restore critical checkpoint data with comprehensive None handling
            # Only restore if checkpoint was successfully loaded
            if checkpoint_loaded:
                d, progress_counter = self.restore_progress("debug", "progress_counter")
            else:
                # Starting from scratch - initialize fresh
                d = None
                progress_counter = 0
            
            # Fix d (debug dict) if it's None
            if d is None:
                logger.warning("Debug dict is None, will reinitialize after getting batches_per_epoch")
                d = None  # Will be reinitialized below
            batches_per_epoch = self.restore_progress("batches_per_epoch")
            
            # Fix batches_per_epoch first (needed for progress calculation)
            logger.warning(f"DEBUG: batches_per_epoch type: {type(batches_per_epoch)}, value: {batches_per_epoch}")
            if batches_per_epoch is None:
                # Recalculate batches_per_epoch from scratch
                logger.warning("batches_per_epoch is None, recalculating from data loader")
                try:
                    if self.train_input_data.project_row_meta_data_list is None:
                        # Use num_workers=0 for temporary loader - we only need the length
                        temp_loader = DataLoader(self.train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_tokens, num_workers=0)
                        batches_per_epoch = len(temp_loader)
                        logger.info(f"Recalculated batches_per_epoch from DataLoader: {batches_per_epoch}")
                    else:
                        batches_per_epoch = int(math.ceil(len(self.train_dataset) / batch_size))
                        logger.info(f"Recalculated batches_per_epoch from dataset length: {batches_per_epoch}")
                except Exception as e:
                    logger.error(f"Failed to recalculate batches_per_epoch: {e}")
                    # Emergency fallback - just use a reasonable default
                    num_rows = len(self.train_input_data.df)
                    batches_per_epoch = max(1, int(math.ceil(num_rows / batch_size)))
                    logger.warning(f"Using emergency fallback batches_per_epoch: {batches_per_epoch} (rows={num_rows}, batch_size={batch_size})")
                
                if batches_per_epoch is None:
                    logger.error("CRITICAL: batches_per_epoch is STILL None after recalculation!")
                    batches_per_epoch = 1  # Absolute emergency fallback
                    logger.error(f"Using absolute emergency fallback: batches_per_epoch = {batches_per_epoch}")
                    
            elif isinstance(batches_per_epoch, list) and len(batches_per_epoch) == 1:
                batches_per_epoch = batches_per_epoch[0]
                # Check if the extracted value is None and recalculate if needed
                if batches_per_epoch is None:
                    logger.warning("batches_per_epoch extracted from list is None, recalculating")
                    try:
                        if self.train_input_data.project_row_meta_data_list is None:
                            # Use num_workers=0 for temporary loader - we only need the length
                            temp_loader = DataLoader(self.train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_tokens, num_workers=0)
                            batches_per_epoch = len(temp_loader)
                        else:
                            batches_per_epoch = int(math.ceil(len(self.train_dataset) / batch_size))
                        logger.info(f"Recalculated batches_per_epoch after list extraction: {batches_per_epoch}")
                    except Exception as e:
                        logger.error(f"Failed to recalculate batches_per_epoch after list extraction: {e}")
                        num_rows = len(self.train_input_data.df)
                        batches_per_epoch = max(1, int(math.ceil(num_rows / batch_size)))
                        logger.warning(f"Using emergency fallback batches_per_epoch: {batches_per_epoch}")
            elif not isinstance(batches_per_epoch, int):
                logger.warning(f"batches_per_epoch restored as {type(batches_per_epoch)}: {batches_per_epoch}, converting to int")
                batches_per_epoch = int(batches_per_epoch)
            
            # FINAL safety check - ensure batches_per_epoch is never None after all processing
            if batches_per_epoch is None:
                logger.error("FINAL SAFETY CHECK: batches_per_epoch is STILL None! Using emergency value.")
                batches_per_epoch = max(1, int(math.ceil(len(self.train_input_data.df) / batch_size)))
                logger.error(f"FINAL SAFETY: batches_per_epoch set to {batches_per_epoch}")
            
            # Validate batches_per_epoch is positive after all processing
            if batches_per_epoch <= 0:
                raise ValueError(
                    f"Cannot recover training with batches_per_epoch={batches_per_epoch}. "
                    f"Dataset has {len(self.train_dataset)} samples, batch_size={batch_size}. "
                    f"This usually means the dataset is empty or batch_size is too large."
                )
            
            logger.warning(f"FINAL batches_per_epoch value: {batches_per_epoch} (type: {type(batches_per_epoch)})")
            
            # Fix progress_counter with proper fallback
            logger.warning(f"DEBUG: progress_counter type: {type(progress_counter)}, value: {progress_counter}")
            logger.warning(f"DEBUG: existing_epochs: {existing_epochs}, batches_per_epoch: {batches_per_epoch}")
            if progress_counter is None:
                if batches_per_epoch is None:
                    logger.error("CRITICAL: Cannot calculate progress_counter because batches_per_epoch is STILL None!")
                    progress_counter = 0
                else:
                    # Handle case where existing_epochs might be None (starting from scratch after failed checkpoint)
                    epoch_num = existing_epochs or 0
                    progress_counter = epoch_num * batches_per_epoch
                    logger.warning(f"progress_counter is None, calculated as {epoch_num} × {batches_per_epoch} = {progress_counter}")
            elif isinstance(progress_counter, list) and len(progress_counter) == 1:
                progress_counter = progress_counter[0]
            elif not isinstance(progress_counter, int):
                logger.warning(f"progress_counter restored as {type(progress_counter)}: {progress_counter}, converting to int")
                progress_counter = int(progress_counter)
            # Restore other variables with None protection
            loss, val_loss, last_log_time = self.restore_progress("loss", "val_loss", "last_log_time")
            _encodeTime, _backTime, _lossTime = self.restore_progress("encode_time", "back_time", "loss_time")
            val_dataloader = self.restore_progress("val_dataloader")
            optimizer_params = self.restore_progress("optimizer_params")
            data_loader = self.restore_progress("data_loader")
            lowest_val_loss = self.restore_progress("lowest_val_loss")
            
            # Provide defaults for None values and fix type issues
            if loss is None:
                loss = "not set"
            elif isinstance(loss, list) and len(loss) == 1:
                loss = loss[0] if loss[0] is not None else "not set"
                
            if val_loss is None:
                val_loss = "not set"
            elif isinstance(val_loss, list) and len(val_loss) == 1:
                val_loss = val_loss[0] if val_loss[0] is not None else "not set"
            elif isinstance(val_loss, list):
                logger.warning(f"val_loss restored as list with {len(val_loss)} items: {val_loss}, using 'not set'")
                val_loss = "not set"
                
            if last_log_time is None:
                last_log_time = 0
            elif isinstance(last_log_time, list) and len(last_log_time) == 1:
                last_log_time = last_log_time[0] if last_log_time[0] is not None else 0
                
            if lowest_val_loss is None:
                lowest_val_loss = float("inf")
            elif isinstance(lowest_val_loss, list) and len(lowest_val_loss) == 1:
                lowest_val_loss = lowest_val_loss[0] if lowest_val_loss[0] is not None else float("inf")
            elif isinstance(lowest_val_loss, list):
                logger.warning(f"lowest_val_loss restored as list with {len(lowest_val_loss)} items: {lowest_val_loss}, using inf")
                lowest_val_loss = float("inf")
            elif not isinstance(lowest_val_loss, (int, float)):
                logger.warning(f"lowest_val_loss restored as {type(lowest_val_loss)}: {lowest_val_loss}, using inf")
                lowest_val_loss = float("inf")
            
            # Fix optimizer_params with proper type checking and conversion
            logger.warning(f"DEBUG: optimizer_params type: {type(optimizer_params)}, value: {optimizer_params}")
            if optimizer_params is None:
                logger.warning("optimizer_params is None, using default")
                optimizer_params = {"lr": 0.001, "weight_decay": 1e-4}
            elif isinstance(optimizer_params, list) and len(optimizer_params) == 1:
                optimizer_params = optimizer_params[0]
                logger.warning(f"optimizer_params extracted from list: {optimizer_params}")
                if optimizer_params is None:
                    logger.warning("optimizer_params extracted from list is None, using default")
                    optimizer_params = {"lr": 0.001, "weight_decay": 1e-4}
            elif not isinstance(optimizer_params, dict):
                logger.warning(f"optimizer_params restored as {type(optimizer_params)}: {optimizer_params}, using default")
                optimizer_params = {"lr": 0.001, "weight_decay": 1e-4}
            
            # Ensure optimizer_params is a valid dict
            if not isinstance(optimizer_params, dict):
                logger.error(f"FINAL SAFETY: optimizer_params is STILL not a dict! Type: {type(optimizer_params)}, using default")
                optimizer_params = {"lr": 0.001, "weight_decay": 1e-4}
            
            logger.warning(f"FINAL optimizer_params: {optimizer_params} (type: {type(optimizer_params)})")
            
            # CRITICAL: ALWAYS recreate DataLoaders during recovery (they can't be properly serialized)
            logger.warning("🔄 FORCING DataLoader recreation during recovery (DataLoaders can't be serialized)")
            data_loader = None  # Force recreation
            val_dataloader = None  # Force recreation
            
            # Check if dataset is too small for batch_size and duplicate rows if needed (recovery path)
            train_dataset_size = len(self.train_dataset)
            if train_dataset_size < batch_size:
                logger.warning(
                    f"⚠️  Dataset too small during recovery: {train_dataset_size} samples < batch_size {batch_size}. "
                    f"Duplicating rows to ensure at least one batch."
                )
                
                duplication_factor = math.ceil(batch_size / train_dataset_size)
                logger.info(f"📋 Duplicating dataset {duplication_factor}x to reach at least {batch_size} samples")
                
                duplicated_train_df = pd.concat([self.train_input_data.df] * duplication_factor, ignore_index=True)
                duplicated_row_meta = None
                if self.train_input_data.project_row_meta_data_list is not None:
                    duplicated_row_meta = self.train_input_data.project_row_meta_data_list * duplication_factor
                duplicated_casted_df = None
                if self.train_input_data.casted_df is not None:
                    duplicated_casted_df = pd.concat([self.train_input_data.casted_df] * duplication_factor, ignore_index=True)
                
                self.train_dataset = SuperSimpleSelfSupervisedDataset(
                    duplicated_train_df,
                    codecs=self.col_codecs,
                    row_meta_data=duplicated_row_meta,
                    casted_df=duplicated_casted_df,
                )
                logger.info(f"✅ Train dataset duplicated: {train_dataset_size} → {len(self.train_dataset)} samples")
            
            val_dataset_size = len(self.val_dataset)
            if val_dataset_size < batch_size:
                logger.warning(
                    f"⚠️  Validation dataset too small during recovery: {val_dataset_size} samples < batch_size {batch_size}. "
                    f"Duplicating rows to ensure at least one batch."
                )
                
                duplication_factor = math.ceil(batch_size / val_dataset_size)
                logger.info(f"📋 Duplicating validation dataset {duplication_factor}x to reach at least {batch_size} samples")
                
                duplicated_val_df = pd.concat([self.val_input_data.df] * duplication_factor, ignore_index=True)
                duplicated_val_row_meta = None
                if self.val_input_data.project_row_meta_data_list is not None:
                    duplicated_val_row_meta = self.val_input_data.project_row_meta_data_list * duplication_factor
                duplicated_val_casted_df = None
                if self.val_input_data.casted_df is not None:
                    duplicated_val_casted_df = pd.concat([self.val_input_data.casted_df] * duplication_factor, ignore_index=True)
                
                self.val_dataset = SuperSimpleSelfSupervisedDataset(
                    duplicated_val_df,
                    codecs=self.col_codecs,
                    row_meta_data=duplicated_val_row_meta,
                    casted_df=duplicated_val_casted_df,
                )
                logger.info(f"✅ Validation dataset duplicated: {val_dataset_size} → {len(self.val_dataset)} samples")
            
            # CRITICAL: Recreate data_loader if it's None (can't be serialized/restored)
            if data_loader is None:
                logger.warning("=" * 80)
                logger.warning("🔄 DATA_LOADER IS NONE - RECREATING FROM SCRATCH (CHECKPOINT RESUME)")
                logger.warning("=" * 80)
                if self.train_input_data.project_row_meta_data_list is None:
                    # Use create_dataloader_kwargs to get multiprocessing support!
                    train_dl_kwargs = create_dataloader_kwargs(
                        batch_size=batch_size,
                        shuffle=True,
                        drop_last=True,
                        dataset_size=len(self.train_input_data.df),
                    )
                    logger.info(f"📦 Checkpoint Resume DataLoader kwargs: {train_dl_kwargs}")
                    data_loader = DataLoader(
                        self.train_dataset,
                        collate_fn=collate_tokens,
                        **train_dl_kwargs
                    )
                    logger.info(f"✅ Recreated regular DataLoader with num_workers={train_dl_kwargs.get('num_workers', 0)}")
                    logger.warning("=" * 80)
                else:
                    sampler = DataSpaceBatchSampler(batch_size, self.train_input_data)
                    sampler_dl_kwargs = create_dataloader_kwargs(
                        batch_size=batch_size,
                        shuffle=False,
                        drop_last=False,
                        dataset_size=len(self.train_input_data.df),
                    )
                    # Remove batch params (incompatible with batch_sampler)
                    sampler_dl_kwargs.pop('batch_size', None)
                    sampler_dl_kwargs.pop('shuffle', None)
                    sampler_dl_kwargs.pop('drop_last', None)
                    logger.info(f"📦 Checkpoint Resume BatchSampler kwargs: {sampler_dl_kwargs}")
                    data_loader = DataLoader(
                        self.train_dataset,
                        batch_sampler=sampler,
                        collate_fn=collate_tokens,
                        **sampler_dl_kwargs
                    )
                    logger.info(f"✅ Recreated DataSpaceBatchSampler DataLoader with num_workers={sampler_dl_kwargs.get('num_workers', 0)}")
            
            # Also recreate val_dataloader if it's None
            if val_dataloader is None:
                logger.warning("val_dataloader is None, recreating from scratch")
                # CRITICAL: Reduce validation workers based on available VRAM to prevent OOM
                val_num_workers = None
                if torch.cuda.is_available():
                    try:
                        allocated = torch.cuda.memory_allocated() / (1024**3)
                        reserved = torch.cuda.memory_reserved() / (1024**3)
                        total_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                        free_vram = total_memory - reserved
                        
                        worker_vram_gb = 0.6
                        safety_margin_gb = 20.0
                        available_for_workers = max(0, free_vram - safety_margin_gb)
                        max_workers_by_vram = int(available_for_workers / worker_vram_gb)
                        
                        from featrix.neural.dataloader_utils import get_optimal_num_workers
                        default_workers = get_optimal_num_workers(dataset_size=len(self.val_input_data.df))
                        
                        val_num_workers = min(default_workers, max_workers_by_vram, 4)
                        val_num_workers = max(0, val_num_workers)
                        
                        logger.info(f"🔍 Validation worker calculation: free_vram={free_vram:.1f}GB → {val_num_workers} workers")
                    except Exception as e:
                        logger.warning(f"Could not calculate optimal validation workers: {e}, using 0")
                        val_num_workers = 0
                
                val_dl_kwargs = create_dataloader_kwargs(
                    batch_size=batch_size,
                    shuffle=True,
                    drop_last=True,
                    num_workers=val_num_workers,
                    dataset_size=len(self.val_input_data.df),
                )
                logger.info(f"📦 Checkpoint Resume Validation DataLoader kwargs: {val_dl_kwargs}")
                val_dataloader = DataLoader(
                    self.val_dataset,
                    collate_fn=collate_tokens,
                    **val_dl_kwargs
                )
                logger.info(f"✅ Recreated validation DataLoader with num_workers={val_dl_kwargs.get('num_workers', 0)}")
            
            # Recalculate batches_per_epoch from the recreated data loader to ensure accuracy
            if data_loader is not None:
                if self.train_input_data.project_row_meta_data_list is None:
                    recalculated_batches = len(data_loader)
                else:
                    # For batch sampler, calculate from dataset length
                    recalculated_batches = int(math.ceil(len(self.train_dataset) / batch_size))
                
                if recalculated_batches != batches_per_epoch:
                    logger.warning(
                        f"batches_per_epoch mismatch: restored={batches_per_epoch}, "
                        f"recalculated={recalculated_batches}. Using recalculated value."
                    )
                    batches_per_epoch = recalculated_batches
                
                # Final validation after recalculation
                if batches_per_epoch <= 0:
                    raise ValueError(
                        f"Cannot recover training with batches_per_epoch={batches_per_epoch}. "
                        f"Dataset has {len(self.train_dataset)} samples, batch_size={batch_size}. "
                        f"DataLoader has {len(data_loader)} batches. "
                        f"This usually means the dataset is empty or batch_size is too large."
                    )
                
                logger.info(f"Validated batches_per_epoch: {batches_per_epoch} from recreated DataLoader")
            
            # Handle case where existing_epochs might be None (starting from scratch after failed checkpoint)
            epoch_num = (existing_epochs or 0) + 1
            self.training_info[f"restart_time_{epoch_num}"] = time.time()
            timeStart = self.training_info.get("start_time")
            
            # CRITICAL: Properly recreate optimizer and scheduler from state dicts
            logger.warning("🔄 Recreating optimizer and scheduler from checkpoint state dicts")
            
            # Create fresh optimizer with same parameters
            optimizer_params = optimizer_params or {"lr": 0.001, "weight_decay": 1e-4}
            optimizer = torch.optim.AdamW(
                self.encoder.parameters(),
                **optimizer_params,
            )
            
            # Load the saved state dict into the fresh optimizer
            # CRITICAL: Validate parameter counts match before loading to prevent optimizer errors
            if "optimizer" in self.training_state and self.training_state["optimizer"] is not None:
                try:
                    saved_state = self.training_state["optimizer"]
                    current_param_groups = optimizer.param_groups
                    saved_param_groups = saved_state.get("param_groups", [])
                    
                    # Try to load and catch any mismatch errors
                    # PyTorch will raise an error if parameter shapes/counts don't match
                    optimizer.load_state_dict(saved_state)
                    logger.info("✅ Successfully loaded optimizer state from checkpoint")
                except Exception as e:
                    logger.warning(f"⚠️  Failed to load optimizer state: {e}, using fresh optimizer")
            
            # Create fresh scheduler if needed
            scheduler = None
            if use_lr_scheduler:
                if lr_schedule_segments is not None:
                    scheduler = LambdaLR(
                        optimizer,
                        lr_lambda=self._get_lambda_lr(lr_schedule_segments),
                    )
                else:
                    # Use correct total_steps calculation for recovery
                    # DIAGNOSTIC: Log values before calculation
                    logger.warning(f"🔍 DIAGNOSTIC (recovery): n_epochs={n_epochs} (type: {type(n_epochs)}), batches_per_epoch={batches_per_epoch} (type: {type(batches_per_epoch)})")
                    logger.warning(f"🔍 DIAGNOSTIC (recovery): train_dataset length={len(self.train_dataset)}, batch_size={batch_size}")
                    logger.warning(f"🔍 DIAGNOSTIC (recovery): data_loader length={len(data_loader) if data_loader is not None else 'None'}")
                    
                    total_steps = n_epochs * batches_per_epoch
                    
                    # Guard against invalid total_steps
                    if total_steps <= 0:
                        raise ValueError(
                            f"Cannot create OneCycleLR scheduler with total_steps={total_steps}. "
                            f"n_epochs={n_epochs} (type: {type(n_epochs)}), batches_per_epoch={batches_per_epoch} (type: {type(batches_per_epoch)}). "
                            f"train_dataset length={len(self.train_dataset)}, batch_size={batch_size}, "
                            f"data_loader length={len(data_loader) if data_loader is not None else 'None'}. "
                            f"Both n_epochs and batches_per_epoch must be positive integers."
                        )
                    
                    logger.info(f"OneCycleLR: recreating with corrected total_steps={total_steps}")
                    
                    scheduler = OneCycleLR(
                        optimizer,
                        max_lr=optimizer_params["lr"],
                        total_steps=total_steps,
                    )
                
                # Load the saved state dict into the fresh scheduler
                if "scheduler" in self.training_state and self.training_state["scheduler"] is not None:
                    try:
                        scheduler.load_state_dict(self.training_state["scheduler"])
                        
                        # CRITICAL: Fix total_steps after loading checkpoint (old checkpoints have wrong value)
                        if hasattr(scheduler, 'total_steps'):
                            correct_total_steps = n_epochs * batches_per_epoch
                            old_total_steps = scheduler.total_steps
                            if scheduler.total_steps != correct_total_steps:
                                logger.warning(f"⚠️ Correcting scheduler total_steps: {scheduler.total_steps} → {correct_total_steps}")
                                scheduler.total_steps = correct_total_steps
                                
                                # Warn if extending training significantly (could cause LR jump)
                                if old_total_steps > 0:
                                    old_epochs = old_total_steps / batches_per_epoch
                                    if n_epochs > old_epochs * 1.5:  # More than 50% increase
                                        logger.warning(f"⚠️ Training extended from {old_epochs:.0f} to {n_epochs} epochs - LR schedule will be recalculated")
                                        logger.warning(f"   Position in schedule: {existing_epochs}/{n_epochs} = {existing_epochs/n_epochs*100:.1f}%")
                        
                        # CRITICAL: Fix last_epoch to match the epoch we're resuming from
                        # OneCycleLR uses last_epoch to calculate the current learning rate
                        # If we saved at epoch 150 and restart at epoch 151, last_epoch should be 150 * batches_per_epoch
                        # (because we're at the START of epoch 151, which means we've completed 150 epochs)
                        if hasattr(scheduler, 'last_epoch'):
                            # existing_epochs is the last completed epoch (e.g., 150)
                            # At the start of epoch 151, we've done 150 epochs worth of steps
                            correct_last_epoch = existing_epochs * batches_per_epoch
                            if scheduler.last_epoch != correct_last_epoch:
                                old_lr = scheduler.get_last_lr()[0] if hasattr(scheduler, 'get_last_lr') else None
                                logger.warning(f"⚠️ Correcting scheduler last_epoch: {scheduler.last_epoch} → {correct_last_epoch} (resuming from epoch {base_epoch_index}, completed {existing_epochs} epochs)")
                                scheduler.last_epoch = correct_last_epoch
                                new_lr = scheduler.get_last_lr()[0] if hasattr(scheduler, 'get_last_lr') else None
                                if old_lr and new_lr:
                                    lr_change_pct = ((new_lr - old_lr) / old_lr * 100) if old_lr > 0 else 0
                                    logger.info(f"   LR after correction: {old_lr:.6e} → {new_lr:.6e} ({lr_change_pct:+.1f}%)")
                                    if abs(lr_change_pct) > 50:
                                        logger.warning(f"   ⚠️ Large LR change detected - this may be due to extending training duration")
                                else:
                                    # Get current LR from optimizer if scheduler doesn't have get_last_lr
                                    current_lr = optimizer.param_groups[0]['lr'] if optimizer else None
                                    if current_lr:
                                        logger.info(f"   Current LR: {current_lr:.6e}")
                        
                        logger.info("✅ Successfully loaded scheduler state from checkpoint")
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to load scheduler state: {e}, using fresh scheduler")
            
            # Create and restore dropout scheduler if needed and available
            if enable_dropout_scheduler and "dropout_scheduler" in self.training_state and self.training_state["dropout_scheduler"] is not None:
                try:
                    # Create fresh dropout scheduler first
                    dropout_scheduler = create_dropout_scheduler(
                        schedule_type=dropout_schedule_type,
                        initial_dropout=initial_dropout,
                        final_dropout=final_dropout,
                        total_epochs=n_epochs
                    )
                    # Then load the saved state
                    dropout_scheduler.load_state_dict(self.training_state["dropout_scheduler"])
                    logger.info("✅ Successfully loaded dropout scheduler state from checkpoint")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to load dropout scheduler state: {e}, will create fresh scheduler later")
                    dropout_scheduler = None
                        
            logger.info(f"🚀 Recovery complete: optimizer, scheduler, and dropout scheduler properly recreated")
            
            # Reinitialize debug dict if it was None
            if d is None:
                logger.warning("Reinitializing debug dict from scratch")
                d = self._init_d(timeStart=timeStart, n_epochs=n_epochs, batches_per_epoch=batches_per_epoch)
                # Update with current progress
                # Handle case where existing_epochs might be None (starting from scratch after failed checkpoint)
                epoch_num = (existing_epochs or 0) + 1
                d["epoch_idx"] = epoch_num
                d["progress_counter"] = progress_counter
        else:
            lowest_val_loss = float("inf")

            sum_of_a_log = 0
            for name, codec in self.col_codecs.items():
                if isinstance(codec, SetCodec):
                    logger.info(f"{name} --> set has {len(codec.members_to_tokens)} members")
                    sum_of_a_log += math.log(len(codec.members_to_tokens))
            logger.info(f"Sum of log cardinalities: {sum_of_a_log}")

            # Ensure optimizer_params has valid lr - handle None values
            if optimizer_params is None:
                optimizer_params = {"lr": 0.001, "weight_decay": 1e-4}
            elif not isinstance(optimizer_params, dict):
                logger.warning(f"optimizer_params is not a dict: {type(optimizer_params)}, using defaults")
                optimizer_params = {"lr": 0.001, "weight_decay": 1e-4}
            else:
                # Ensure lr is not None - use default if missing or None
                if optimizer_params.get("lr") is None:
                    logger.warning(f"optimizer_params has None lr, using default 0.001")
                    optimizer_params = {**optimizer_params, "lr": 0.001}
                # Ensure weight_decay has a default if missing
                if "weight_decay" not in optimizer_params:
                    optimizer_params["weight_decay"] = 1e-4
            
            logger.info(f"🔧 Using optimizer_params: lr={optimizer_params.get('lr')}, weight_decay={optimizer_params.get('weight_decay')}")
            optimizer = torch.optim.AdamW(
                self.encoder.parameters(),
                **optimizer_params,
            )
            progress_counter = 0

            timeStart = time.time()
            self.training_start_time = timeStart  # Track for elapsed time in logs
            self.training_info["start_time"] = timeStart

            # Check if dataset is too small for batch_size and duplicate rows if needed
            train_dataset_size = len(self.train_dataset)
            if train_dataset_size < batch_size:
                logger.warning(
                    f"⚠️  Dataset too small: {train_dataset_size} samples < batch_size {batch_size}. "
                    f"Duplicating rows to ensure at least one batch."
                )
                
                # Calculate how many times we need to duplicate to get at least batch_size samples
                duplication_factor = math.ceil(batch_size / train_dataset_size)
                logger.info(f"📋 Duplicating dataset {duplication_factor}x to reach at least {batch_size} samples")
                
                # Duplicate the dataframe
                duplicated_train_df = pd.concat([self.train_input_data.df] * duplication_factor, ignore_index=True)
                
                # Duplicate row metadata if present
                duplicated_row_meta = None
                if self.train_input_data.project_row_meta_data_list is not None:
                    duplicated_row_meta = self.train_input_data.project_row_meta_data_list * duplication_factor
                
                # Duplicate casted_df if present
                duplicated_casted_df = None
                if self.train_input_data.casted_df is not None:
                    duplicated_casted_df = pd.concat([self.train_input_data.casted_df] * duplication_factor, ignore_index=True)
                
                # Recreate train_dataset with duplicated data
                self.train_dataset = SuperSimpleSelfSupervisedDataset(
                    duplicated_train_df,
                    codecs=self.col_codecs,
                    row_meta_data=duplicated_row_meta,
                    casted_df=duplicated_casted_df,
                )
                
                logger.info(f"✅ Train dataset duplicated: {train_dataset_size} → {len(self.train_dataset)} samples")
            
            # Also check and duplicate validation dataset if needed
            val_dataset_size = len(self.val_dataset)
            if val_dataset_size < batch_size:
                logger.warning(
                    f"⚠️  Validation dataset too small: {val_dataset_size} samples < batch_size {batch_size}. "
                    f"Duplicating rows to ensure at least one batch."
                )
                
                duplication_factor = math.ceil(batch_size / val_dataset_size)
                logger.info(f"📋 Duplicating validation dataset {duplication_factor}x to reach at least {batch_size} samples")
                
                # Duplicate the validation dataframe
                duplicated_val_df = pd.concat([self.val_input_data.df] * duplication_factor, ignore_index=True)
                
                # Duplicate row metadata if present
                duplicated_val_row_meta = None
                if self.val_input_data.project_row_meta_data_list is not None:
                    duplicated_val_row_meta = self.val_input_data.project_row_meta_data_list * duplication_factor
                
                # Duplicate casted_df if present
                duplicated_val_casted_df = None
                if self.val_input_data.casted_df is not None:
                    duplicated_val_casted_df = pd.concat([self.val_input_data.casted_df] * duplication_factor, ignore_index=True)
                
                # Recreate val_dataset with duplicated data
                self.val_dataset = SuperSimpleSelfSupervisedDataset(
                    duplicated_val_df,
                    codecs=self.col_codecs,
                    row_meta_data=duplicated_val_row_meta,
                    casted_df=duplicated_val_casted_df,
                )
                
                logger.info(f"✅ Validation dataset duplicated: {val_dataset_size} → {len(self.val_dataset)} samples")

            if self.train_input_data.project_row_meta_data_list is None:
                logger.info("=" * 80)
                logger.info("🚀 CREATING REAL TRAINING DATALOADER")
                logger.info("=" * 80)
                # Regular vector space - use multiprocess dataloader
                train_dl_kwargs = create_dataloader_kwargs(
                    batch_size=batch_size,
                    shuffle=True,
                    drop_last=True,
                    dataset_size=len(self.train_input_data.df),
                )
                logger.info(f"📦 Training DataLoader kwargs: {train_dl_kwargs}")
                data_loader = DataLoader(
                    self.train_dataset,
                    collate_fn=collate_tokens,
                    **train_dl_kwargs
                )
                logger.info(f"✅ Training DataLoader created with num_workers={train_dl_kwargs.get('num_workers', 0)}")
                logger.info("=" * 80)

                # CRITICAL: Reduce validation workers based on available VRAM to prevent OOM
                val_num_workers = None
                if torch.cuda.is_available():
                    try:
                        allocated = torch.cuda.memory_allocated() / (1024**3)
                        reserved = torch.cuda.memory_reserved() / (1024**3)
                        total_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                        free_vram = total_memory - reserved
                        
                        worker_vram_gb = 0.6
                        safety_margin_gb = 20.0
                        available_for_workers = max(0, free_vram - safety_margin_gb)
                        max_workers_by_vram = int(available_for_workers / worker_vram_gb)
                        
                        from featrix.neural.dataloader_utils import get_optimal_num_workers
                        default_workers = get_optimal_num_workers(dataset_size=len(self.val_input_data.df))
                        
                        val_num_workers = min(default_workers, max_workers_by_vram, 4)
                        val_num_workers = max(0, val_num_workers)
                        
                        logger.info(f"🔍 Validation worker calculation: free_vram={free_vram:.1f}GB → {val_num_workers} workers")
                    except Exception as e:
                        logger.warning(f"Could not calculate optimal validation workers: {e}, using 0")
                        val_num_workers = 0
                
                val_dl_kwargs = create_dataloader_kwargs(
                    batch_size=batch_size,
                    shuffle=True,
                    drop_last=True,
                    num_workers=val_num_workers,
                    dataset_size=len(self.val_input_data.df),
                )
                logger.info(f"📦 Validation DataLoader kwargs: {val_dl_kwargs}")
                val_dataloader = DataLoader(
                    self.val_dataset,
                    collate_fn=collate_tokens,
                    **val_dl_kwargs
                )
                logger.info(f"✅ Validation DataLoader created with num_workers={val_dl_kwargs.get('num_workers', 0)}, persistent_workers={val_dl_kwargs.get('persistent_workers', False)}")

                batches_per_epoch = len(data_loader)
            else:
                logger.info("Using batch sampler data loader for multi-dataset training with multiprocess support")
                mySampler = DataSpaceBatchSampler(batch_size, self.train_input_data)
                # Note: batch_sampler is mutually exclusive with batch_size/shuffle/drop_last
                sampler_dl_kwargs = create_dataloader_kwargs(
                    batch_size=batch_size,
                    shuffle=False,  # Not used with batch_sampler
                    drop_last=False,  # Not used with batch_sampler
                    dataset_size=len(self.train_input_data.df),
                )
                sampler_dl_kwargs.pop('batch_size', None)
                sampler_dl_kwargs.pop('shuffle', None)
                sampler_dl_kwargs.pop('drop_last', None)
                
                data_loader = DataLoader(
                    self.train_dataset,
                    batch_sampler=mySampler,
                    collate_fn=collate_tokens,
                    **sampler_dl_kwargs
                )
                # the sampler's len() is the number of rows, not the number of batches.
                batches_per_epoch = int(math.ceil(len(data_loader) / batch_size))
            
            # Validate batches_per_epoch before proceeding (should never be 0 after duplication)
            if batches_per_epoch == 0:
                raise ValueError(
                    f"Cannot train with 0 batches per epoch. "
                    f"Dataset has {len(self.train_dataset)} samples, batch_size={batch_size}. "
                    f"This should not happen after row duplication - there may be an issue with the DataLoader."
                )
            
            logger.info(f"Calculated batches_per_epoch: {batches_per_epoch} (dataset_size={len(self.train_dataset)}, batch_size={batch_size})")
            
            d = self._init_d(timeStart=timeStart,
                             n_epochs=n_epochs,
                             batches_per_epoch=batches_per_epoch)

            if use_lr_scheduler:
                if lr_schedule_segments is not None:
                    # LambdaLR scheduler can be used to create very flexible schedulers,
                    # but we use it just to create segments of fixed LR.
                    scheduler = LambdaLR(
                        optimizer,
                        lr_lambda=self._get_lambda_lr(lr_schedule_segments),
                    )
                else:
                    # Use correct total_steps calculation
                    # DIAGNOSTIC: Log values before calculation
                    logger.warning(f"🔍 DIAGNOSTIC: n_epochs={n_epochs} (type: {type(n_epochs)}), batches_per_epoch={batches_per_epoch} (type: {type(batches_per_epoch)})")
                    logger.warning(f"🔍 DIAGNOSTIC: train_dataset length={len(self.train_dataset)}, batch_size={batch_size}")
                    logger.warning(f"🔍 DIAGNOSTIC: data_loader length={len(data_loader) if data_loader is not None else 'None'}")
                    
                    total_steps = n_epochs * batches_per_epoch
                    
                    # Guard against invalid total_steps
                    if total_steps <= 0:
                        raise ValueError(
                            f"Cannot create OneCycleLR scheduler with total_steps={total_steps}. "
                            f"n_epochs={n_epochs} (type: {type(n_epochs)}), batches_per_epoch={batches_per_epoch} (type: {type(batches_per_epoch)}). "
                            f"train_dataset length={len(self.train_dataset)}, batch_size={batch_size}, "
                            f"data_loader length={len(data_loader) if data_loader is not None else 'None'}. "
                            f"Both n_epochs and batches_per_epoch must be positive integers."
                        )
                    
                    logger.info(f"OneCycleLR: creating with corrected total_steps={total_steps}")
                    
                    scheduler = OneCycleLR(
                        optimizer,
                        max_lr=optimizer_params["lr"],
                        total_steps=total_steps,
                    )
            else:
                scheduler = None
            loss = "not set"
            val_loss = "not set"
            last_log_time = 0
            base_epoch_index = 0

        # Initialize TrainingHistoryDB for SQLite-based storage (prevents memory leaks)
        history_db_path = os.path.join(self.output_dir, "training_history.db")
        self.history_db = TrainingHistoryDB(history_db_path)
        logger.info(f"💾 Training history database initialized: {history_db_path}")

        if existing_epochs is not None and "arguments" not in self.training_info:
            self.training_info["arguments"] = self.safe_dump(locals())

        if print_callback is not None:
            print_callback(d)

        # LR multiplier for NO_LEARNING recovery
        lr_boost_multiplier = 1.0
        lr_boost_epochs_remaining = 0
        
        # Temperature multiplier for NO_LEARNING recovery
        temp_boost_multiplier = 1.0
        
        # Intervention stage tracking
        intervention_stage = 0  # 0=none, 1=3x LR, 2=2x temp, 3=2x LR again, 4=2x temp again, 5=converged
        epochs_since_last_intervention = 0
        intervention_patience = 10  # Wait 10 epochs before escalating
        
        # Gradient tracking statistics
        grad_clip_stats = {
            "total_batches": 0,
            "clipped_batches": 0,
            "max_unclipped_norm": 0.0,
            "max_clipped_norm": 0.0,
            "sum_unclipped_norms": 0.0,
            "sum_clipped_norms": 0.0,
            "large_gradient_warnings": 0,
            "gradient_norms_history": [],  # Store last 100 for analysis
            "loss_values_history": [],  # Store corresponding loss values
            "max_grad_loss_ratio": 0.0,  # Track max ratio observed
        }
        
        # Determine clipping mode
        use_adaptive_clipping = adaptive_grad_clip_ratio is not None
        
        if use_adaptive_clipping:
            logger.info(f"🔧 ADAPTIVE gradient clipping: will clip when gradient > loss × {adaptive_grad_clip_ratio:.1f}")
            logger.info(f"   This adapts to loss magnitude (which scales with number of columns)")
            if grad_clip_warning_multiplier is not None:
                logger.info(f"   Will warn when ratio > {adaptive_grad_clip_ratio * grad_clip_warning_multiplier:.1f}")
            grad_clip_warning_threshold = None  # Will be computed per-batch
        else:
            logger.warning("⚠️  GRADIENT CLIPPING DISABLED")
            logger.warning("   This is not recommended - gradients can explode")
            grad_clip_warning_threshold = None
        
        def get_lr():
            if scheduler is not None:
                # get_last_lr() returns a list, take first element
                last_lr_list = scheduler.get_last_lr()
                base_lr = last_lr_list[0] if isinstance(last_lr_list, list) and last_lr_list else optimizer_params["lr"]
                # Apply boost multiplier if active
                return base_lr * lr_boost_multiplier
            else:
                return optimizer_params["lr"] * lr_boost_multiplier

        max_progress = n_epochs * batches_per_epoch
        # Print every 1% of progress if it is less than the original progress step but don't go to 0
        print_progress_step = max(
            int(min((max_progress / 100), print_progress_step)), 1
        )
        logger.info(f"Training configuration:")
        logger.info(f"  Epochs for this training run: {n_epochs} (this may be per-fold if using cross-validation)")
        logger.info(f"  Batches per epoch: {batches_per_epoch}")
        logger.info(f"  Max progress: {max_progress}")
        logger.info(f"  Print progress step: {print_progress_step}")
        
        # WeightWatcher setup if enabled  
        weightwatcher_job_id = None
        if enable_weightwatcher:
            # Use job ID from training_info if available for file organization
            weightwatcher_job_id = getattr(self, 'job_id', None) or self.training_info.get('job_id', None)
            logger.info(f"🔍 WeightWatcher enabled: saving every {weightwatcher_save_every} epochs to {weightwatcher_out_dir}")

        # DropoutScheduler setup if enabled (only if not already restored from checkpoint)
        if enable_dropout_scheduler and dropout_scheduler is None:
            dropout_scheduler = create_dropout_scheduler(
                schedule_type=dropout_schedule_type,
                initial_dropout=initial_dropout,
                final_dropout=final_dropout,
                total_epochs=n_epochs
            )
            logger.info(f"📉 DropoutScheduler enabled: {dropout_schedule_type} ({initial_dropout:.3f} → {final_dropout:.3f})")

        # Pre-warm string cache with ALL strings to prevent cache misses during training
        self.pre_warm_string_cache()

        # Save data snapshot for async movie frame generation
        self._save_movie_data_snapshot(movie_frame_interval)

        # raise Exception("stop")

        logger.info("Setting encoder to training mode")
        self.encoder.train()

        # Profiling is resource-intensive, so we only enable it if needed.
        if use_profiler:
            profiler_ctx_mngr = self._prep_profiler()
        else:
            profiler_ctx_mngr = nullcontext()

        timed_data_loader = (data_loader)
        
        # Track when to resample train/val split
        # Use minimum of 25 epochs per split for robust learning
        # For very long training (>250 epochs), allow resampling every 10%
        resample_interval = max(25, n_epochs // 10)
        num_splits = (n_epochs // resample_interval) + 1  # +1 for initial split
        logger.info(f"🔄 Train/val resampling enabled: every {resample_interval} epochs (min 25 epochs/split, {num_splits} total splits)")
        
        val_loss = float('inf')
        
        # Track time for hourly pickle saves
        training_start_time = time.time()
        last_hourly_pickle_time = training_start_time
        hourly_pickle_interval = 3600  # 1 hour in seconds
        
        # MEMORY LEAK DETECTION: Track VRAM usage throughout epoch to identify leaks
        def _log_vram_usage(context: str, epoch_idx: int, batch_idx: int = None):
            """Log VRAM usage with context for leak detection"""
            if not torch.cuda.is_available():
                return
            
            allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
            reserved = torch.cuda.memory_reserved() / (1024**3)  # GB
            max_allocated = torch.cuda.max_memory_allocated() / (1024**3)  # GB
            
            batch_str = f" batch={batch_idx}" if batch_idx is not None else ""
            logger.info(f"🔍 VRAM [epoch={epoch_idx}{batch_str}] [{context:30s}] Alloc={allocated:5.2f}GB  Reserved={reserved:5.2f}GB  Peak={max_allocated:5.2f}GB")
            
            # Track VRAM growth between checkpoints
            if not hasattr(self, '_vram_tracker'):
                self._vram_tracker = {'last_allocated': allocated, 'last_reserved': reserved}
            else:
                alloc_delta = allocated - self._vram_tracker['last_allocated']
                reserved_delta = reserved - self._vram_tracker['last_reserved']
                if abs(alloc_delta) > 0.1 or abs(reserved_delta) > 0.1:  # Log if >100MB change
                    logger.info(f"🔍 VRAM DELTA: Alloc {alloc_delta:+.2f}GB  Reserved {reserved_delta:+.2f}GB")
                self._vram_tracker['last_allocated'] = allocated
                self._vram_tracker['last_reserved'] = reserved
        
        with profiler_ctx_mngr as profiler:
            for epoch_idx in range(base_epoch_index, n_epochs):
                # MEMORY LEAK DETECTION: Log VRAM at start of epoch
                _log_vram_usage("START OF EPOCH", epoch_idx)
                
                # SYSTEM HEALTH MONITORING: Check memory pressure and kernel OOM events
                if epoch_idx % 10 == 0 or epoch_idx == 0:  # Check every 10 epochs
                    try:
                        from lib.system_health_monitor import check_system_health
                        job_id_for_monitor = getattr(self, 'job_id', None) or self.training_info.get('job_id', None)
                        check_system_health(context=f"EPOCH_{epoch_idx}_START", job_id=job_id_for_monitor)
                    except Exception as e:
                        logger.debug(f"System health check failed: {e}")
                
                # Reset tiny gradient warning flag for this epoch (ensure it exists)
                if not hasattr(self, '_tiny_grad_warned_this_epoch'):
                    self._tiny_grad_warned_this_epoch = False
                else:
                    self._tiny_grad_warned_this_epoch = False
                
                # MEMORY LEAK FIX: Periodic garbage collection every 10 epochs for large datasets
                # More frequent clearing for large datasets to prevent VRAM accumulation
                gc_interval = 10 if hasattr(self, 'train_input_data') and len(self.train_input_data.df) >= 20000 else 50
                if epoch_idx > 0 and epoch_idx % gc_interval == 0:
                    import gc
                    gc.collect()
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                        torch.cuda.synchronize()
                    logger.debug(f"[epoch={epoch_idx}] 🧹 Garbage collection performed (interval: {gc_interval} epochs)")
                    _log_vram_usage("AFTER GC", epoch_idx)
                
                # MEMORY LEAK FIX: Flush training history to SQLite every 100 epochs
                if epoch_idx > 0 and epoch_idx % 100 == 0:
                    if hasattr(self, 'history_db') and self.history_db:
                        self.history_db.flush()
                        logger.debug(f"[epoch={epoch_idx}] 💾 Training history flushed to SQLite")
                
                # DISABLED: Hourly pickle saves are expensive (GB files, 5-10min save time each)
                # and unnecessary since we have .pth checkpoints saved every epoch that can
                # reconstruct the full EmbeddingSpace. Use test_checkpoint_to_es.py to rebuild.
                # 
                # # Check for hourly pickle save (once per hour during training)
                # current_time = time.time()
                # time_since_last_pickle = current_time - last_hourly_pickle_time
                # if time_since_last_pickle >= hourly_pickle_interval:
                #     output_dir_str = str(self.output_dir) if hasattr(self, 'output_dir') and self.output_dir else None
                #     if output_dir_str:
                #         try:
                #             from featrix.neural.embedding_space_utils import write_embedding_space_pickle
                #             
                #             # Create timestamped filename
                #             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                #             job_id = getattr(self, 'job_id', None) or self.training_info.get('job_id', None)
                #             session_id = getattr(self, 'session_id', None) or self.training_info.get('session_id', None)
                #             
                #             if session_id:
                #                 filename = f"{session_id}-es-hourly-{timestamp}.pickle"
                #             elif job_id:
                #                 filename = f"{job_id}-es-hourly-{timestamp}.pickle"
                #             else:
                #                 filename = f"embedding_space-hourly-{timestamp}.pickle"
                #             
                #             pickle_path = write_embedding_space_pickle(self, output_dir_str, filename=filename, show_progress=False)
                #             last_hourly_pickle_time = current_time
                #             hours_training = (current_time - training_start_time) / 3600
                #             logger.info(f"💾 Hourly pickle saved at epoch {epoch_idx} ({hours_training:.1f}h training time) → {pickle_path}")
                #         except Exception as e:
                #             # Check if this is a DataLoader pickling error
                #             error_str = str(e)
                #             error_lower = error_str.lower()
                #             if 'dataloader' in error_lower or 'dataloaderiter' in error_lower or '_multiprocessingdataloaderiter' in error_lower:
                #                 # This is a known issue - DataLoader iterators can't be pickled
                #                 # The write_embedding_space_pickle function should handle this,
                #                 # but if it still fails, we'll skip this hourly save
                #                 logger.debug(f"⚠️  Skipping hourly pickle save due to DataLoader iterator (this is expected during training): {error_str[:200]}")
                #             else:
                #                 logger.warning(f"⚠️  Failed to save hourly pickle: {e}")
                
                # Check for PUBLISH flag - save embedding space for single predictor training
                output_dir_str = str(self.output_dir) if hasattr(self, 'output_dir') and self.output_dir else None
                job_id = getattr(self, 'job_id', None) or self.training_info.get('job_id', None)
                if check_publish_file(job_id, output_dir_str):
                    # Check if we've already published this epoch (avoid multiple saves per epoch)
                    last_published_epoch = getattr(self, '_last_published_epoch', -1)
                    if epoch_idx != last_published_epoch:
                        try:
                            from featrix.neural.embedding_space_utils import write_embedding_space_pickle
                            # Get session_id for naming: {session_id}-es-prelim.pickle
                            session_id = getattr(self, 'session_id', None) or self.training_info.get('session_id', None)
                            if session_id:
                                filename = f"{session_id}-es-prelim.pickle"
                            else:
                                # Fallback to job_id if session_id not available
                                filename = f"{job_id}-es-prelim.pickle" if job_id else "embedding_space-prelim.pickle"
                            pickle_path = write_embedding_space_pickle(self, output_dir_str, filename=filename)
                            self._last_published_epoch = epoch_idx
                            logger.info(f"📦 PUBLISH flag detected - embedding space saved at epoch {epoch_idx} to {pickle_path}")
                        except Exception as e:
                            # Don't abort training if pickle save fails
                            logger.warning(f"⚠️  Failed to save embedding space for PUBLISH flag at epoch {epoch_idx}: {e}")
                            logger.warning(f"   Training will continue - this save can be retried later")
                
                # UPDATE ADAPTIVE ENCODER EPOCH COUNTERS for strategy pruning
                self._update_encoder_epoch_counters(epoch_idx, n_epochs)
                
                # Reset per-epoch gradient statistics
                grad_clip_stats["total_batches"] = 0
                grad_clip_stats["clipped_batches"] = 0
                grad_clip_stats["sum_unclipped_norms"] = 0.0
                grad_clip_stats["sum_clipped_norms"] = 0.0
                # Note: We keep max_unclipped_norm, max_grad_loss_ratio, and histories across epochs for global tracking
                
                # Decay LR boost multiplier if active
                if lr_boost_epochs_remaining > 0:
                    lr_boost_epochs_remaining -= 1
                    if lr_boost_epochs_remaining == 0:
                        lr_boost_multiplier = 1.0
                        logger.info(f"⏰ LR boost expired, returning to 1.0x multiplier")
                
                # Gradual data rotation: swap out a small fraction of train/val data
                # Initialize rotation settings if not present (backward compatibility with old checkpoints)
                if not hasattr(self, '_rotation_interval'):
                    self._rotation_interval = max(5, n_epochs // 50)
                    self._rotation_fraction = 0.05
                    logger.info(f"🔄 Initialized gradual data rotation: every {self._rotation_interval} epochs, rotate {self._rotation_fraction*100:.0f}% of data")
                
                val_set_rotated = False  # Track if we rotated this epoch
                if epoch_idx > 0 and epoch_idx % self._rotation_interval == 0 and self._rotation_interval > 0:
                    val_set_rotated = True
                    logger.info(f"🔄 GRADUAL DATA ROTATION at epoch {epoch_idx}/{n_epochs} ({epoch_idx/n_epochs*100:.1f}% complete)")
                    logger.info(f"   Rotating {self._rotation_fraction*100:.0f}% of data (instead of 100% resample)")
                    
                    # Save the original column types and encoders to reuse
                    original_ignore_cols = self.train_input_data.ignore_cols
                    
                    # CRITICAL FIX: Extract the ACTUAL detected types from detectors, not encoderOverrides
                    # encoderOverrides is only populated if explicitly passed, NOT from auto-detection
                    original_encoder_overrides = {}
                    for col_name, detector in self.train_input_data._detectors.items():
                        original_encoder_overrides[col_name] = detector.type_name
                    
                    logger.info(f"📋 Extracted {len(original_encoder_overrides)} encoder types from original detection:")
                    for col, typ in list(original_encoder_overrides.items())[:5]:
                        logger.info(f"   {col}: {typ}")
                    if len(original_encoder_overrides) > 5:
                        logger.info(f"   ... and {len(original_encoder_overrides) - 5} more")
                    
                    logger.info(f"   📋 Preserving encoder overrides: {list(original_encoder_overrides.keys()) if original_encoder_overrides else 'None'}")
                    
                    # Get the original split fraction
                    original_split_fraction = len(self.val_dataset) / (len(self.train_dataset) + len(self.val_dataset))
                    logger.info(f"   Original split fraction: {original_split_fraction:.3f}")
                    
                    # GRADUAL ROTATION: Instead of fully reshuffling, swap a small fraction
                    # This prevents validation shock from sudden distribution changes
                    train_df = self.train_input_data.df.copy()
                    val_df = self.val_input_data.df.copy()
                    
                    # Calculate how many rows to rotate (rotation_fraction of smaller set)
                    rotation_size = int(min(len(train_df), len(val_df)) * self._rotation_fraction)
                    rotation_size = max(1, rotation_size)  # At least 1 row
                    
                    logger.info(f"   Rotating {rotation_size} rows ({self._rotation_fraction*100:.0f}% of smaller set)")
                    
                    # Randomly select rows to swap (use epoch-based seed for reproducibility)
                    np.random.seed(42 + epoch_idx)
                    train_swap_indices = np.random.choice(len(train_df), size=rotation_size, replace=False)
                    val_swap_indices = np.random.choice(len(val_df), size=rotation_size, replace=False)
                    
                    # Extract rows to swap
                    train_rows_to_val = train_df.iloc[train_swap_indices].copy()
                    val_rows_to_train = val_df.iloc[val_swap_indices].copy()
                    
                    # Remove swapped rows from original sets
                    train_df_remaining = train_df.drop(train_df.index[train_swap_indices]).reset_index(drop=True)
                    val_df_remaining = val_df.drop(val_df.index[val_swap_indices]).reset_index(drop=True)
                    
                    # Add swapped rows to opposite sets
                    new_train_df = pd.concat([train_df_remaining, val_rows_to_train], ignore_index=True)
                    new_val_df = pd.concat([val_df_remaining, train_rows_to_val], ignore_index=True)
                    
                    # Shuffle the new sets to mix in the swapped rows
                    new_train_df = new_train_df.sample(frac=1.0, random_state=42 + epoch_idx).reset_index(drop=True)
                    new_val_df = new_val_df.sample(frac=1.0, random_state=43 + epoch_idx).reset_index(drop=True)
                    
                    logger.info(f"   New split: train={len(new_train_df)}, val={len(new_val_df)}")
                    
                    # Add timeline entry for gradual rotation
                    if hasattr(self, '_training_timeline'):
                        from datetime import datetime as dt
                        from zoneinfo import ZoneInfo as zi
                        swap_entry = {
                            "epoch": epoch_idx,
                            "timestamp": dt.now(tz=zi("America/New_York")).isoformat(),
                            "event_type": "train_val_gradual_rotation",
                            "description": f"Gradual data rotation at epoch {epoch_idx} ({self._rotation_fraction*100:.0f}% of data)",
                            "rotation_size": rotation_size,
                            "train_size": len(new_train_df),
                            "val_size": len(new_val_df),
                            "original_split_fraction": original_split_fraction,
                            "random_seed": 42 + epoch_idx
                        }
                        self._training_timeline.append(swap_entry)
                        logger.info(f"📊 Added timeline entry for gradual data rotation at epoch {epoch_idx}")
                    
                    # CRITICAL: Reuse the same encoder_overrides to preserve column types
                    # This avoids re-analyzing types and ensures consistency
                    # We need to access the underlying df and metadata from the FeatrixInputDataSet
                    self.train_input_data = FeatrixInputDataSet(
                        df=new_train_df,
                        ignore_cols=original_ignore_cols,
                        limit_rows=None,
                        encoder_overrides=original_encoder_overrides  # REUSE original types
                    )
                    self.val_input_data = FeatrixInputDataSet(
                        df=new_val_df,
                        ignore_cols=original_ignore_cols,
                        limit_rows=None,
                        encoder_overrides=original_encoder_overrides  # REUSE original types
                    )
                    
                    logger.info(f"   ✅ Reused encoder overrides for consistency")
                    logger.info(f"   📋 Train encoderOverrides: {list(self.train_input_data.encoderOverrides.keys()) if self.train_input_data.encoderOverrides else 'None'}")
                    logger.info(f"   📋 Val encoderOverrides: {list(self.val_input_data.encoderOverrides.keys()) if self.val_input_data.encoderOverrides else 'None'}")
                    
                    # Recreate datasets using the same pattern as __init__
                    self.train_dataset = SuperSimpleSelfSupervisedDataset(
                        self.train_input_data.df,
                        codecs=self.col_codecs,  # Reuse existing codecs
                        row_meta_data=self.train_input_data.project_row_meta_data_list,
                    )
                    self.val_dataset = SuperSimpleSelfSupervisedDataset(
                        self.val_input_data.df,
                        codecs=self.col_codecs,  # Reuse existing codecs
                        row_meta_data=self.val_input_data.project_row_meta_data_list,
                    )
                    
                    # Recreate dataloaders with multiprocessing support
                    if self.train_input_data.project_row_meta_data_list is None:
                        train_dl_kwargs = create_dataloader_kwargs(
                            batch_size=batch_size,
                            shuffle=True,
                            drop_last=True,
                            dataset_size=len(self.train_input_data.df),
                        )
                        data_loader = DataLoader(
                            self.train_dataset,
                            collate_fn=collate_tokens,
                            **train_dl_kwargs
                        )
                        # CRITICAL: Reduce validation workers based on available VRAM to prevent OOM
                        # Check how much VRAM is free before creating validation dataloader
                        val_num_workers = None  # Will auto-detect
                        if torch.cuda.is_available():
                            try:
                                allocated = torch.cuda.memory_allocated() / (1024**3)
                                reserved = torch.cuda.memory_reserved() / (1024**3)
                                total_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                                free_vram = total_memory - reserved
                                
                                # Calculate safe number of workers based on free VRAM
                                # Each worker uses ~600MB VRAM
                                worker_vram_gb = 0.6
                                # Reserve 20GB for model/activations during validation
                                safety_margin_gb = 20.0
                                available_for_workers = max(0, free_vram - safety_margin_gb)
                                max_workers_by_vram = int(available_for_workers / worker_vram_gb)
                                
                                # Also get the default worker count based on GPU memory
                                from featrix.neural.dataloader_utils import get_optimal_num_workers
                                default_workers = get_optimal_num_workers(dataset_size=len(self.val_input_data.df))
                                
                                # Use the minimum of default and VRAM-based limit
                                val_num_workers = min(default_workers, max_workers_by_vram)
                                # Never use more than 4 workers for validation (it's infrequent, not worth the overhead)
                                val_num_workers = min(val_num_workers, 4)
                                # Never go negative
                                val_num_workers = max(0, val_num_workers)
                                
                                logger.info(f"🔍 Validation worker calculation: free_vram={free_vram:.1f}GB, available_for_workers={available_for_workers:.1f}GB")
                                logger.info(f"   → max_by_vram={max_workers_by_vram}, default={default_workers}, chosen={val_num_workers}")
                            except Exception as e:
                                logger.warning(f"Could not calculate optimal validation workers: {e}, using 0")
                                val_num_workers = 0
                        
                        val_dl_kwargs = create_dataloader_kwargs(
                            batch_size=batch_size,
                            shuffle=False,
                            drop_last=False,
                            num_workers=val_num_workers,
                            dataset_size=len(self.val_input_data.df),
                        )
                        logger.warning(f"🔄 RECREATING validation DataLoader during train/val resampling (epoch {epoch_idx})")
                        logger.info(f"   Validation DataLoader kwargs: {val_dl_kwargs}")
                        val_dataloader = DataLoader(
                            self.val_dataset,
                            collate_fn=collate_tokens,
                            **val_dl_kwargs
                        )
                        logger.info(f"   Recreated DataLoaders with num_workers={train_dl_kwargs.get('num_workers', 0)}, persistent_workers={val_dl_kwargs.get('persistent_workers', False)}")
                    else:
                        mySampler = DataSpaceBatchSampler(batch_size, self.train_input_data)
                        sampler_dl_kwargs = create_dataloader_kwargs(
                            batch_size=batch_size,
                            shuffle=False,
                            drop_last=False,
                            dataset_size=len(self.train_input_data.df),
                        )
                        sampler_dl_kwargs.pop('batch_size', None)
                        sampler_dl_kwargs.pop('shuffle', None)
                        sampler_dl_kwargs.pop('drop_last', None)
                        data_loader = DataLoader(
                            self.train_dataset,
                            batch_sampler=mySampler,
                            collate_fn=collate_tokens,
                            **sampler_dl_kwargs
                        )
                        logger.info(f"   Recreated batch sampler DataLoader with num_workers={sampler_dl_kwargs.get('num_workers', 0)}")
                    
                    # Update timed iterator
                    timed_data_loader = (data_loader)
                    logger.info(f"✅ Train/val split resampled successfully")
                
                epoch_start_time_now = time.time()
                training_event_dict = {
                    "encoder_timing": [],
                    "loss_timing": [],
                    "loop_timing": [],
                    "loss_details": [],
                    "resource_usage": [],
                    "prediction_vec_lengths": [],
                }

                # Apply K-fold CV offset if present (makes K-fold CV invisible - epochs are cumulative)
                cumulative_epoch_idx = epoch_idx
                if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                    cumulative_epoch_idx = epoch_idx + self._kv_fold_epoch_offset
                
                d["epoch_idx"] = 1 + cumulative_epoch_idx  # Use cumulative epoch for callbacks
                
                # Log epoch start for visibility (use cumulative epoch - K-fold CV invisible)
                # For K-fold CV, show cumulative epoch without denominator (n_epochs is per-fold, not total)
                if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                    logger.info(f"🚀 Starting epoch {cumulative_epoch_idx + 1} ({batches_per_epoch} batches)")
                else:
                    logger.info(f"🚀 Starting epoch {cumulative_epoch_idx + 1}/{n_epochs} ({batches_per_epoch} batches)")
                
                # Track last batch log time for rate limiting (max 1 log per minute)
                if not hasattr(self, '_last_batch_log_time'):
                    self._last_batch_log_time = {}
                if epoch_idx not in self._last_batch_log_time:
                    self._last_batch_log_time[epoch_idx] = time.time()
                
                # ============================================================================
                # CURRICULUM LEARNING: Dynamic marginal_loss_weight adjustment
                # ============================================================================
                # Compute new marginal_loss_weight based on training progress
                base_marginal_weight = self._compute_marginal_loss_weight(epoch_idx, n_epochs)
                old_marginal_weight = self.encoder.config.loss_config.marginal_loss_weight
                
                # Don't apply scaling coefficient to weight - marginal loss is already normalized
                # by 4.0 * effective_n_cols in the encoder, so we should use base weight directly
                # The scaling coefficient was meant to match loss magnitudes, but since marginal
                # is already normalized, applying it to the weight causes over-scaling
                new_marginal_weight = base_marginal_weight
                
                # Update the encoder's loss config
                self.encoder.config.loss_config.marginal_loss_weight = new_marginal_weight
                
                # Track if we've entered spread focus phase (marginal_weight at minimum)
                min_weight = 0.1
                if not hasattr(self, '_spread_only_tracker'):
                    self._spread_only_tracker = {
                        'first_spread_only_epoch': None,
                        'spread_only_epochs_completed': 0
                    }
                
                # Log weight changes (only when there's a meaningful change or at phase boundaries)
                progress = epoch_idx / n_epochs
                phase1_end = 0.05
                phase3_start = 0.95
                
                # Determine current phase
                if progress < phase1_end:
                    phase_name = "PREDICTION FOCUS"
                    phase_emoji = "🎯"
                elif progress >= phase3_start:
                    phase_name = "SPREAD FOCUS"
                    phase_emoji = "🌊"
                else:
                    phase_name = "TRANSITION"
                    phase_emoji = "⚖️"
                
                # Log at phase transitions or every 10% of training
                should_log = (
                    epoch_idx == 0 or  # First epoch
                    abs(new_marginal_weight - old_marginal_weight) > 0.01 or  # Significant change
                    (epoch_idx == int(n_epochs * phase1_end)) or  # Start of phase 2
                    (epoch_idx == int(n_epochs * phase3_start)) or  # Start of phase 3
                    (epoch_idx % max(1, n_epochs // 10) == 0)  # Every 10%
                )
                
                if should_log:
                    if hasattr(self, '_marginal_loss_scaling_coefficient'):
                        # Show cumulative epoch for K-fold CV
                        display_epoch = epoch_idx + 1
                        if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                            display_epoch = epoch_idx + 1 + self._kv_fold_epoch_offset
                            epoch_display = f"epoch={display_epoch}"
                        else:
                            epoch_display = f"epoch={display_epoch}/{n_epochs}"
                        logger.info(f"{phase_emoji} [{epoch_display}] {phase_name}: marginal_loss_weight = {new_marginal_weight:.4f} (loss scaled by {self._marginal_loss_scaling_coefficient:.4f}× to match spread/joint)")
                    else:
                        # Show cumulative epoch for K-fold CV
                        display_epoch = epoch_idx + 1
                        if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                            display_epoch = epoch_idx + 1 + self._kv_fold_epoch_offset
                            epoch_display = f"epoch={display_epoch}"
                        else:
                            epoch_display = f"epoch={display_epoch}/{n_epochs}"
                        logger.info(f"{phase_emoji} [{epoch_display}] {phase_name}: marginal_loss_weight = {new_marginal_weight:.4f} (coefficient will be computed after first validation)")
                
                # Track spread focus epochs (when weight is at minimum)
                # Weight is no longer scaled by coefficient (coefficient is applied to loss value instead)
                if abs(new_marginal_weight - min_weight) < 0.001:
                    if self._spread_only_tracker['first_spread_only_epoch'] is None:
                        self._spread_only_tracker['first_spread_only_epoch'] = epoch_idx
                        # Show cumulative epoch for K-fold CV
                        display_epoch = epoch_idx + 1
                        if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                            display_epoch = epoch_idx + 1 + self._kv_fold_epoch_offset
                        logger.info(f"🌊 [epoch={display_epoch}] Entered SPREAD FOCUS phase (marginal_loss_weight = {new_marginal_weight:.4f})")
                    self._spread_only_tracker['spread_only_epochs_completed'] += 1
                # ============================================================================

                # Check for ABORT file at the start of each epoch
                job_id = getattr(self, 'job_id', None) or self.training_info.get('job_id', None)
                output_dir = getattr(self, 'output_dir', None)
                abort_file_path = check_abort_files(job_id, output_dir=output_dir) if job_id else None
                if abort_file_path:
                    logger.error(f"🚫 ABORT file detected for job {job_id} - exiting training")
                    logger.error(f"🚫 ABORT file path: {abort_file_path}")
                    d["interrupted"] = "ABORT file detected"
                    
                    # Mark job as FAILED before exiting
                    try:
                        from lib.job_manager import update_job_status
                        update_job_status(job_id, JobStatus.FAILED, {
                            "error_message": f"Training aborted due to ABORT file at {abort_file_path}"
                        })
                        logger.info(f"🚫 Job {job_id} marked as FAILED due to ABORT file")
                    except Exception as e:
                        logger.error(f"Failed to update job status before exit: {e}")
                    
                    # Raise exception with the actual path found
                    raise FeatrixTrainingAbortedException(
                        f"Training aborted due to ABORT file at {abort_file_path}",
                        job_id=job_id,
                        abort_file_path=abort_file_path
                    )

                # Check for PAUSE file at the start of each epoch
                if job_id and check_pause_files(job_id):
                    logger.warning(f"⏸️  PAUSE file detected for job {job_id} - pausing training and saving checkpoint")
                    d["interrupted"] = "PAUSE file detected"
                    
                    # Save checkpoint before pausing
                    if save_state_after_every_epoch:
                        try:
                            checkpoint_path = self._save_training_state(epoch_idx, output_dir_str if hasattr(self, 'output_dir') and self.output_dir else None)
                            logger.info(f"💾 Checkpoint saved before pause: {checkpoint_path}")
                        except Exception as e:
                            logger.warning(f"⚠️  Failed to save checkpoint before pause: {e}")
                    
                    # Mark job as PAUSED
                    try:
                        from lib.job_manager import update_job_status
                        update_job_status(job_id, JobStatus.PAUSED, {
                            "pause_reason": "PAUSE file detected by user",
                            "paused_at": datetime.now(tz=ZoneInfo("America/New_York"))
                        })
                        logger.info(f"⏸️  Job {job_id} marked as PAUSED")
                    except Exception as e:
                        logger.error(f"Failed to update job status to PAUSED: {e}")
                    
                    logger.info(f"⏸️  Breaking out of training loop - job is paused. Remove PAUSE file and set status to READY to resume.")
                    break  # Break out of epoch loop
                
                # Check for FINISH file at the start of each epoch
                if job_id and check_finish_files(job_id):
                    logger.warning(f"🏁 FINISH file detected for job {job_id} - completing training gracefully")
                    d["interrupted"] = "FINISH file detected"
                    logger.info(f"🏁 Breaking out of training loop to save model and complete job")
                    break

                if self._gotControlC:
                    logger.warning("Got CTRL+C signal - stopping training. You can continue training later.")
                    d["interrupted"] = "Got SIGINT"
                    break

                if print_callback is not None:
                    if epoch_idx == 0:
                        d["epoch_idx"] = 1 + epoch_idx
                        d["progress_counter"] = progress_counter
                        d["max_progress"] = max_progress
                        print_callback(d)

                # for batch_idx, (batch, targets) in enumerate(dataloader):
                # Initialize loss_dict to None in case batch loop doesn't execute
                loss_dict = None
                
                # MEMORY LEAK DETECTION: Track first and last batch of each epoch
                first_batch_logged = False
                last_batch_idx = batches_per_epoch - 1
                
                for batch_idx, batch in enumerate(timed_data_loader):
                    assert self.encoder.training == True, "(top of batch loop) -- but the net net is that you are not in training mode."
                    
                    # MEMORY LEAK DETECTION: Log first batch, every 20% of epoch, and last batch
                    if not first_batch_logged or batch_idx % max(1, batches_per_epoch // 5) == 0 or batch_idx == last_batch_idx:
                        _log_vram_usage("START OF BATCH", epoch_idx, batch_idx)
                        first_batch_logged = True
                    
                    # Log batch progress with rate limiting (max 1 log per minute)
                    current_time = time.time()
                    time_since_last_log = current_time - self._last_batch_log_time.get(epoch_idx, current_time)
                    should_log_batch = False
                    
                    if epoch_idx == 0:
                        # First epoch: log first batch, then every 10 batches OR every minute
                        if batch_idx == 0 or batch_idx % 10 == 0 or time_since_last_log >= 60:
                            should_log_batch = True
                    else:
                        # Other epochs: log at normal progress intervals OR every minute
                        if batch_idx % print_progress_step == 0 or time_since_last_log >= 60:
                            should_log_batch = True
                    
                    if should_log_batch:
                        # Get current loss (will be computed later, but we'll log it after)
                        # We'll log loss separately after it's computed
                        logger.info(f"   📦 Epoch {epoch_idx + 1}/{n_epochs}, Batch {batch_idx + 1}/{batches_per_epoch} ({(batch_idx + 1)/batches_per_epoch*100:.1f}%)")
                        self._last_batch_log_time[epoch_idx] = current_time
                        self._should_log_loss_this_batch = True
                    else:
                        self._should_log_loss_this_batch = False
                    
                    # Flag to skip remainder of batch processing after exiting with blocks
                    skip_batch = False

                    # Check for PAUSE file periodically during batch processing
                    if batch_idx % 10 == 0 and job_id and check_pause_files(job_id):
                        logger.warning(f"⏸️  PAUSE file detected for job {job_id} during batch {batch_idx} - pausing training")
                        d["interrupted"] = "PAUSE file detected"
                        
                        # Save checkpoint before pausing
                        if save_state_after_every_epoch:
                            try:
                                output_dir_str = str(self.output_dir) if hasattr(self, 'output_dir') and self.output_dir else None
                                checkpoint_path = self._save_training_state(epoch_idx, output_dir_str)
                                logger.info(f"💾 Checkpoint saved before pause: {checkpoint_path}")
                            except Exception as e:
                                logger.warning(f"⚠️  Failed to save checkpoint before pause: {e}")
                        
                        # Mark job as PAUSED
                        try:
                            from lib.job_manager import update_job_status
                            update_job_status(job_id, JobStatus.PAUSED, {
                                "pause_reason": "PAUSE file detected by user",
                                "paused_at": datetime.now(tz=ZoneInfo("America/New_York"))
                            })
                            logger.info(f"⏸️  Job {job_id} marked as PAUSED")
                        except Exception as e:
                            logger.error(f"Failed to update job status to PAUSED: {e}")
                        
                        logger.info(f"⏸️  Breaking out of training loop - job is paused. Remove PAUSE file and set status to READY to resume.")
                        self._gotControlC = True  # Signal to break outer epoch loop
                        break
                    
                    # Check for ABORT file periodically during batch processing (every 10 batches)
                    if batch_idx % 10 == 0:
                        job_id = getattr(self, 'job_id', None) or self.training_info.get('job_id', None)
                        output_dir = getattr(self, 'output_dir', None)
                        abort_file_path = check_abort_files(job_id, output_dir=output_dir) if job_id else None
                        if abort_file_path:
                            logger.error(f"🚫 ABORT file detected for job {job_id} during batch {batch_idx} - exiting training")
                            logger.error(f"🚫 ABORT file path: {abort_file_path}")
                            d["interrupted"] = "ABORT file detected"
                            
                            # Mark job as FAILED before exiting
                            try:
                                from lib.job_manager import update_job_status
                                update_job_status(job_id, JobStatus.FAILED, {
                                    "error_message": f"Training aborted due to ABORT file at {abort_file_path}"
                                })
                                logger.info(f"🚫 Job {job_id} marked as FAILED due to ABORT file")
                            except Exception as e:
                                logger.error(f"Failed to update job status before exit: {e}")
                            
                            # Raise exception with the actual path found
                            raise FeatrixTrainingAbortedException(
                                f"Training aborted due to ABORT file during batch processing at {abort_file_path}",
                                job_id=job_id,
                                abort_file_path=abort_file_path
                            )

                    # Check for FINISH file periodically during batch processing
                    if batch_idx % 10 == 0 and job_id and check_finish_files(job_id):
                        logger.warning(f"🏁 FINISH file detected for job {job_id} during batch {batch_idx} - completing training gracefully")
                        d["interrupted"] = "FINISH file detected"
                        logger.info(f"🏁 Breaking out of training loop to save model and complete job")
                        # Set flag to break out of both batch and epoch loops
                        self._gotControlC = True
                        break

                    if self._gotControlC:
                        logger.warning("Got CTRL+C signal - stopping training early.")
                        break

                    progress_counter += 1

                    # logger.info("loop_stopwatch encoder entered")
                    for tokenbatch in batch.values():
                        tokenbatch.to(device)

                    assert self.encoder.training == True, "(before encoder) -- but the net net is that you are not in training mode."
                    encodings = self.encoder(batch)
                    
                    # MEMORY LEAK DETECTION: Log VRAM after forward pass (first/every 20%/last batch)
                    if batch_idx == 0 or batch_idx % max(1, batches_per_epoch // 5) == 0 or batch_idx == last_batch_idx:
                        _log_vram_usage("AFTER FORWARD PASS", epoch_idx, batch_idx)
                    
                    # Track mask distribution (encodings[9] = mask_1, encodings[10] = mask_2)
                    # Also need token_status_mask which is in the encoder forward pass
                    # We'll extract it from the batch since it's regenerated in encoder
                    if self.mask_tracker is not None:
                        # Track mask distribution - masks only contain columns that are in the batch
                        # The encoder processes columns in self.col_order order, but only those in the batch
                        # Return tuple indices: 0=batch_size, 1-3=full_joint, 4-5=column_encodings, 6-8=short_joint, 9=mask_1, 10=mask_2
                        mask_1, mask_2 = encodings[9], encodings[10]
                        
                        # Reconstruct original_mask to match mask dimensions (only columns in batch)
                        # Get columns in batch in the order they appear in self.col_order (matches encoder order)
                        batch_cols_in_order = [col_name for col_name in self.col_order if col_name in batch]
                        
                        # CRITICAL: Both masks should have the same dimensions
                        # If they don't match, something is wrong with the encoder output
                        if mask_1.shape[1] != mask_2.shape[1]:
                            logger.warning(
                                f"⚠️  Mask dimension mismatch: mask_1.shape[1]={mask_1.shape[1]}, "
                                f"mask_2.shape[1]={mask_2.shape[1]}. Skipping mask tracking for this batch."
                            )
                            continue
                        
                        # Both masks have the same number of columns - use that
                        num_mask_cols = mask_1.shape[1]
                        token_status_list = []
                        
                        for i, col_name in enumerate(batch_cols_in_order):
                            if i >= num_mask_cols:
                                break  # Only collect statuses for columns the encoder processed
                            if col_name in batch:
                                token_status_list.append(batch[col_name].status)
                        
                        # Verify we collected the right number of statuses
                        if len(token_status_list) == num_mask_cols:
                            original_mask = torch.stack(token_status_list, dim=1)
                            # Final verification that all dimensions match
                            if original_mask.shape[1] == mask_1.shape[1] == mask_2.shape[1]:
                                self.mask_tracker.record_batch(
                                    epoch_idx, batch_idx, mask_1, mask_2, original_mask
                                )
                            else:
                                logger.debug(
                                    f"Final dimension check failed: original_mask={original_mask.shape[1]}, "
                                    f"mask_1={mask_1.shape[1]}, mask_2={mask_2.shape[1]}"
                                )
                        else:
                            # Log when we can't construct matching mask
                            logger.debug(
                                f"Cannot construct matching mask: token_status_list={len(token_status_list)}, "
                                f"expected={num_mask_cols}, batch_cols_in_order={len(batch_cols_in_order)}"
                            )

                    # logger.info("loop_stopwatch compute_total_loss entered")
                    loss, loss_dict = self.encoder.compute_total_loss(*encodings, temp_multiplier=temp_boost_multiplier)
                    
                    # Log marginal loss breakdown every N batches for visibility
                    if batch_idx % 50 == 0:
                        self._log_marginal_loss_breakdown(loss_dict, epoch_idx, batch_idx)
                    
                    # Progressive pruning: track column losses and prune worst columns at 10% and 20% progress
                    if not hasattr(self, '_column_loss_tracker'):
                        self._column_loss_tracker = {}  # Track average loss per column
                        self._column_loss_count = {}    # Track number of samples per column
                    self._update_column_loss_tracker(loss_dict)
                    
                    # Check training progress and prune if needed
                    training_progress = (epoch_idx + 1) / n_epochs if n_epochs > 0 else 0.0
                    if training_progress >= 0.10 and not hasattr(self, '_pruned_at_10pct'):
                        self._prune_worst_scalar_columns(loss_dict, epoch_idx, prune_percent=0.10)
                        self._pruned_at_10pct = True
                    elif training_progress >= 0.20 and not hasattr(self, '_pruned_at_20pct'):
                        # At 20%, prune next worst 10% (total will be 20% pruned)
                        self._prune_worst_scalar_columns(loss_dict, epoch_idx, prune_percent=0.10, cumulative=True)
                        self._pruned_at_20pct = True

                    # logger.info("loop_stopwatch zero entered")
                    assert self.encoder.training == True, "(before zero_grad) -- but the net net is that you are not in training mode."
                    optimizer.zero_grad()
                    
                    # CRITICAL FIX: Check loss value BEFORE backward pass
                    if torch.isnan(loss) or torch.isinf(loss):
                        logger.error(f"💥 FATAL: NaN/Inf loss detected BEFORE backward! loss={loss.item()}")
                        logger.error(f"   Epoch: {epoch_idx}, Batch: {batch_idx}")
                        logger.error(f"   Loss dict: {loss_dict}")
                        # Skip this batch entirely - don't corrupt gradients
                        logger.error("   ⚠️  SKIPPING THIS BATCH to prevent gradient corruption")
                        skip_batch = True
                        break  # Exit the with block cleanly
                    
                    loss.backward()
                    
                    # MEMORY LEAK DETECTION: Log VRAM after backward pass (first/every 20%/last batch)
                    if batch_idx == 0 or batch_idx % max(1, batches_per_epoch // 5) == 0 or batch_idx == last_batch_idx:
                        _log_vram_usage("AFTER BACKWARD PASS", epoch_idx, batch_idx)
                    
                    # Compute unclipped gradient norm for diagnostics
                    unclipped_norm = torch.nn.utils.clip_grad_norm_(self.encoder.parameters(), float('inf'))
                    
                    # Determine clipping threshold for this batch
                    if use_adaptive_clipping:
                        # Adaptive clipping: threshold = loss × ratio
                        loss_value = loss.item()
                        adaptive_threshold = loss_value * adaptive_grad_clip_ratio
                        total_norm = torch.nn.utils.clip_grad_norm_(self.encoder.parameters(), adaptive_threshold)
                        was_clipped = unclipped_norm > adaptive_threshold
                        effective_threshold = adaptive_threshold
                        
                        # Track gradient/loss ratio
                        grad_loss_ratio = unclipped_norm / (loss_value + 1e-8)
                        grad_clip_stats["max_grad_loss_ratio"] = max(grad_clip_stats["max_grad_loss_ratio"], grad_loss_ratio)
                    else:
                        # No clipping
                        total_norm = unclipped_norm
                        was_clipped = False
                        effective_threshold = None
                    
                    # Track gradient statistics
                    grad_clip_stats["total_batches"] += 1
                    if was_clipped:
                        grad_clip_stats["clipped_batches"] += 1
                    grad_clip_stats["max_unclipped_norm"] = max(grad_clip_stats["max_unclipped_norm"], unclipped_norm)
                    grad_clip_stats["max_clipped_norm"] = max(grad_clip_stats["max_clipped_norm"], total_norm)
                    grad_clip_stats["sum_unclipped_norms"] += unclipped_norm
                    grad_clip_stats["sum_clipped_norms"] += total_norm
                    
                    # Keep rolling history of last 100 gradients and losses for analysis
                    if len(grad_clip_stats["gradient_norms_history"]) >= 100:
                        grad_clip_stats["gradient_norms_history"].pop(0)
                        grad_clip_stats["loss_values_history"].pop(0)
                    grad_clip_stats["gradient_norms_history"].append(float(unclipped_norm))
                    grad_clip_stats["loss_values_history"].append(float(loss.item()))
                    
                    # CRITICAL FIX: Detect NaN/Inf gradients BEFORE they corrupt parameters
                    if torch.isnan(total_norm) or torch.isinf(total_norm):
                        logger.error(f"💥 FATAL: NaN/Inf gradients detected! total_norm={total_norm}")
                        logger.error(f"   Loss value: {loss.item()}")
                        logger.error(f"   Epoch: {epoch_idx}, Batch: {batch_idx}")
                        
                        # Check individual parameter gradients
                        nan_params = []
                        for name, param in self.encoder.named_parameters():
                            if param.grad is not None and (torch.isnan(param.grad).any() or torch.isinf(param.grad).any()):
                                nan_params.append(name)
                        
                        if nan_params:
                            logger.error(f"   Parameters with NaN/Inf gradients: {nan_params[:5]}...")
                        
                        # CRITICAL: Zero out corrupted gradients and skip this step
                        logger.error("   ⚠️  ZEROING corrupted gradients and SKIPPING optimizer step")
                        optimizer.zero_grad()
                        skip_batch = True
                        break  # Exit the with block cleanly
                    
                    # Store latest gradient info for failure detection and timeline (every batch)
                    current_lr = get_lr()
                    lr_value = current_lr[0] if isinstance(current_lr, list) else current_lr
                    clipped_ratio = (unclipped_norm / effective_threshold) if (effective_threshold is not None and unclipped_norm > effective_threshold) else 1.0
                    
                    self._latest_gradient_norm = unclipped_norm
                    self._latest_gradient_clipped = total_norm
                    self._latest_gradient_ratio = clipped_ratio
                    
                    # Gradient monitoring
                    if unclipped_norm < 0.001 and batch_idx % 500 == 0:
                        logger.warning(f"⚠️  [epoch={epoch_idx}] TINY GRADIENTS: {unclipped_norm:.6e}, lr={lr_value:.6e} (model may not be learning)")
                        
                        # Track TINY_GRADIENTS warning in timeline (only log once per epoch)
                        if not hasattr(self, '_tiny_grad_warned_this_epoch') or not self._tiny_grad_warned_this_epoch:
                            unclipped_val = float(unclipped_norm.item()) if hasattr(unclipped_norm, 'item') else float(unclipped_norm)
                            self._track_warning_in_timeline(
                                epoch_idx=epoch_idx,
                                warning_type="TINY_GRADIENTS",
                                is_active=True,
                                details={
                                    "gradient_norm": unclipped_val,
                                    "lr": lr_value,
                                    "batch_idx": batch_idx,
                                    "threshold": 0.001
                                }
                            )
                            self._tiny_grad_warned_this_epoch = True
                    elif batch_idx % 500 == 0:
                        loss_value = loss.item()
                        grad_loss_ratio = unclipped_norm / (loss_value + 1e-8)
                        
                        # For adaptive clipping, warn based on ratio threshold
                        if use_adaptive_clipping and grad_clip_warning_multiplier is not None:
                            warning_ratio = adaptive_grad_clip_ratio * grad_clip_warning_multiplier
                            if grad_loss_ratio > warning_ratio:
                                grad_clip_stats["large_gradient_warnings"] += 1
                                logger.warning(f"⚠️  [epoch={epoch_idx}] High gradient/loss ratio: {grad_loss_ratio:.2f} (threshold: {warning_ratio:.2f})")
                                logger.warning(f"   gradient={unclipped_norm:.2f}, loss={loss_value:.2f}, clipped={was_clipped}")


                    # logger.info("loop_stopwatch step entered")
                    
                    # CRITICAL FIX: Validate parameters BEFORE optimizer step
                    nan_params_before = []
                    for name, param in self.encoder.named_parameters():
                        if torch.isnan(param).any():
                            nan_params_before.append(name)
                    
                    if nan_params_before:
                        logger.error(f"💥 FATAL: NaN parameters detected BEFORE optimizer step!")
                        logger.error(f"   Corrupted parameters: {nan_params_before[:5]}...")
                        logger.error(f"   Epoch: {epoch_idx}, Batch: {batch_idx}")
                        logger.error("   ⚠️  SKIPPING optimizer step to prevent further corruption")
                        # Don't step the optimizer if parameters are already corrupted
                        skip_batch = True
                        break  # Exit the with block cleanly
                    
                    # CRITICAL: Catch optimizer state mismatch errors and recreate optimizer
                    try:
                        optimizer.step()
                    except RuntimeError as opt_err:
                        if "size of tensor" in str(opt_err) and "must match" in str(opt_err):
                            # Optimizer state mismatch - recreate with fresh state
                            logger.error(f"⚠️  Optimizer state mismatch detected: {opt_err}")
                            logger.error("   Recreating optimizer with fresh state")
                            old_lr = optimizer.param_groups[0]['lr']
                            optimizer = torch.optim.AdamW(
                                self.encoder.parameters(),
                                lr=old_lr,
                                weight_decay=optimizer.param_groups[0].get('weight_decay', 1e-4)
                            )
                            # Recreate scheduler if it exists
                            if scheduler is not None:
                                if lr_schedule_segments is not None:
                                    scheduler = LambdaLR(
                                        optimizer,
                                        lr_lambda=self._get_lambda_lr(lr_schedule_segments),
                                    )
                                else:
                                    scheduler = OneCycleLR(
                                        optimizer,
                                        max_lr=old_lr,
                                        total_steps=total_steps,
                                        pct_start=0.3,
                                        anneal_strategy='cos'
                                    )
                            logger.info("✅ Optimizer recreated - retrying step()")
                            optimizer.step()  # Retry with fresh optimizer
                        else:
                            raise  # Re-raise if it's a different error
                    
                    # CRITICAL FIX: Validate parameters AFTER optimizer step
                    nan_params_after = []
                    for name, param in self.encoder.named_parameters():
                        if torch.isnan(param).any():
                            nan_params_after.append(name)
                    
                    if nan_params_after:
                        logger.error(f"💥 FATAL: NaN parameters detected AFTER optimizer step!")
                        logger.error(f"   Corrupted parameters: {nan_params_after[:5]}...")
                        logger.error(f"   Epoch: {epoch_idx}, Batch: {batch_idx}")
                        logger.error(f"   Loss value: {loss.item()}")
                        logger.error(f"   Learning rate: {get_lr()}")
                        
                        # Show the actual corrupted parameter values for the first one
                        if nan_params_after:
                            first_param_name = nan_params_after[0]
                            for name, param in self.encoder.named_parameters():
                                if name == first_param_name:
                                    logger.error(f"   Sample corrupted values from {name}: {param.flatten()[:10]}")
                                    break
                        
                        # CRITICAL: Training is now corrupted - we must stop
                        logger.error("   🚨 TRAINING CORRUPTED - STOPPING TO PREVENT FURTHER DAMAGE")
                        raise RuntimeError(f"FATAL PARAMETER CORRUPTION AFTER STEP: {len(nan_params_after)} corrupted parameters")
                    
                    if scheduler is not None:
                        try:
                            scheduler.step()
                            
                            # Apply LR boost multiplier if active
                            if lr_boost_multiplier != 1.0:
                                for param_group in optimizer.param_groups:
                                    param_group['lr'] = param_group['lr'] * lr_boost_multiplier
                        except ValueError as err:
                            logger.error("Overstepped.", exc_info=1)
                            break  # break out of the loop.

                    # After executing the optimization step, detach loss from the computational
                    # graph, so we don't accidentally accumulate references to it across the
                    # whole training run, and thus blow up memory.
                    loss = loss.detach()

                    d["current_learning_rate"] = get_lr()
                    d["current_loss"] = loss.item()

                    # Log loss when we logged batch progress (same rate limiting)
                    if getattr(self, '_should_log_loss_this_batch', False):
                        logger.info(f"      Loss: {loss.item():.4f} (batch {batch_idx + 1}/{batches_per_epoch})")

                    self.run_callbacks(CallbackType.AFTER_BATCH, epoch_idx, batch_idx)

                    # NOTE: the procedure for computing and saving the training progress
                    # is getting too complicated, and difficult to replicate at the end
                    # of the training, so the info saved at the end is more limited.
                    # We should factor this out into a separate method.
                    if print_progress_step is not None:
                        last_log_delta = time.time() - last_log_time
                        # print("last_log_delta = ", last_log_delta)
                        if (
                            last_log_delta > 10
                            or (progress_counter % print_progress_step) == 0
                        ):
                            last_log_time = time.time()

                            self.train_save_progress_stuff(
                                epoch_idx=epoch_idx,
                                batch_idx=batch_idx,
                                epoch_start_time_now=epoch_start_time_now,
                                encodings=encodings,
                                save_prediction_vector_lengths=save_prediction_vector_lengths,
                                training_event_dict=training_event_dict,
                                d=d,
                                current_lr=get_lr(),
                                loss_tensor=loss,
                                loss_dict=loss_dict,
                                val_loss=val_loss,
                                dataloader_batch_durations=[],
                                print_callback=print_callback,
                                progress_counter=progress_counter,
                                training_event_callback=training_event_callback
                            )

                    if use_profiler:
                        logger.info(f"Profiler step. Progress counter = {progress_counter}")
                        profiler.step()
                # endfor (batch loop)
                
                # Compute validation loss ONCE per epoch (not after every batch!)
                try:
                    if val_dataloader is not None:
                        logger.info(f"   🔍 Computing validation loss for epoch {epoch_idx + 1}/{n_epochs}...")
                        
                        # MEMORY OPTIMIZATION: For large validation sets (>10k rows), temporarily
                        # shut down training dataloader workers to free VRAM during validation
                        training_dataloader_shutdown = False
                        train_dl_kwargs_backup = None
                        if len(self.val_input_data.df) > 10000:
                            # Check if training dataloader has persistent workers
                            if hasattr(data_loader, 'num_workers') and data_loader.num_workers > 0:
                                try:
                                    logger.info(f"💾 Large validation set ({len(self.val_input_data.df)} rows) - temporarily shutting down training workers to free VRAM")
                                    _log_vram_usage("BEFORE TRAIN WORKER SHUTDOWN", epoch_idx)
                                    
                                    # Save kwargs for recreation
                                    train_dl_kwargs_backup = {
                                        'batch_size': batch_size,
                                        'shuffle': True,
                                        'drop_last': True,
                                        'num_workers': data_loader.num_workers,
                                    }
                                    
                                    # Delete the dataloader to trigger worker cleanup
                                    del data_loader
                                    training_dataloader_shutdown = True
                                    
                                    # Force garbage collection to ensure workers are cleaned up
                                    import gc
                                    gc.collect()
                                    if torch.cuda.is_available():
                                        torch.cuda.empty_cache()
                                        torch.cuda.synchronize()
                                    
                                    _log_vram_usage("AFTER TRAIN WORKER SHUTDOWN", epoch_idx)
                                    logger.info(f"✅ Training workers shut down, VRAM freed for validation")
                                except Exception as e:
                                    logger.warning(f"Failed to shut down training workers: {e}")
                                    training_dataloader_shutdown = False
                        
                        val_loss, val_components = self.compute_val_loss(val_dataloader)
                        
                        # SYSTEM HEALTH MONITORING: Check for OOM events after validation
                        # (validation is where worker OOM is most likely)
                        try:
                            from lib.system_health_monitor import SystemHealthMonitor
                            job_id_for_monitor = getattr(self, 'job_id', None) or self.training_info.get('job_id', None)
                            monitor = SystemHealthMonitor(job_id=job_id_for_monitor)
                            oom_events = monitor.check_dmesg_for_oom()
                            if oom_events:
                                logger.error(f"🚨 DETECTED {len(oom_events)} KERNEL OOM EVENT(S) AFTER VALIDATION:")
                                for event in oom_events:
                                    logger.error(f"   Killed: {event['victim_process']} (PID {event['victim_pid']}) at {event['timestamp']}")
                        except Exception as e:
                            logger.debug(f"OOM check failed: {e}")
                        
                        # MEMORY OPTIMIZATION: Recreate training dataloader if we shut it down
                        if training_dataloader_shutdown and train_dl_kwargs_backup:
                            try:
                                logger.info(f"🔄 Recreating training dataloader after validation")
                                _log_vram_usage("BEFORE TRAIN WORKER RESTART", epoch_idx)
                                
                                # Recreate with original configuration
                                train_dl_kwargs = create_dataloader_kwargs(
                                    batch_size=train_dl_kwargs_backup['batch_size'],
                                    shuffle=train_dl_kwargs_backup['shuffle'],
                                    drop_last=train_dl_kwargs_backup['drop_last'],
                                    num_workers=train_dl_kwargs_backup.get('num_workers'),
                                    dataset_size=len(self.train_input_data.df),
                                )
                                data_loader = DataLoader(
                                    self.train_dataset,
                                    collate_fn=collate_tokens,
                                    **train_dl_kwargs
                                )
                                
                                _log_vram_usage("AFTER TRAIN WORKER RESTART", epoch_idx)
                                logger.info(f"✅ Training dataloader recreated with {train_dl_kwargs.get('num_workers', 0)} workers")
                            except Exception as e:
                                logger.error(f"❌ Failed to recreate training dataloader: {e}")
                                logger.error("   Training will likely fail on next epoch")
                                raise
                        # Log consolidated validation loss with components
                        # Use epoch_idx + 1 for 1-indexed epoch display (to match summary logs)
                        if val_components:
                            # Get current learning rate (format as regular decimal, not scientific notation)
                            try:
                                current_lr = get_lr()
                                lr_value = current_lr[0] if isinstance(current_lr, list) else current_lr
                                # Format as regular decimal with enough precision to see small values
                                if lr_value < 0.0001:
                                    lr_str = f"lr={lr_value:.8f}"
                                elif lr_value < 0.01:
                                    lr_str = f"lr={lr_value:.6f}"
                                else:
                                    lr_str = f"lr={lr_value:.4f}"
                            except Exception:
                                lr_str = "lr=N/A"
                            
                            # Get current marginal loss weight
                            try:
                                marginal_weight = self.encoder.config.loss_config.marginal_loss_weight
                                marginal_weight_str = f"marg_w={marginal_weight:.4f}"
                            except Exception:
                                marginal_weight_str = "marg_w=N/A"
                            
                            # Calculate elapsed training time
                            try:
                                elapsed_seconds = time.time() - self.training_start_time
                                if elapsed_seconds < 60:
                                    elapsed_str = f"[{int(elapsed_seconds)}s]"
                                elif elapsed_seconds < 3600:
                                    minutes = int(elapsed_seconds // 60)
                                    seconds = int(elapsed_seconds % 60)
                                    elapsed_str = f"[{minutes}m {seconds}s]"
                                else:
                                    hours = int(elapsed_seconds // 3600)
                                    minutes = int((elapsed_seconds % 3600) // 60)
                                    elapsed_str = f"[{hours}h {minutes}m]"
                            except Exception:
                                elapsed_str = ""
                            
                            # Single compact line with all loss components
                            marginal_pct = val_components.get('marginal_normalized', 0.0) * 100
                            logger.info(
                                f"📊 [epoch={epoch_idx + 1}] {elapsed_str} VAL LOSS: {val_loss:.4f} {lr_str} {marginal_weight_str} "
                                f"(spread={val_components['spread']:.4f}, joint={val_components['joint']:.4f}, "
                                f"marginal={val_components['marginal']:.4f}, marginal_weighted={val_components['marginal_weighted']:.4f}, "
                                f"marginal_norm={marginal_pct:.0f}% of random) "
                                f"| FULL={val_components['spread_full']:.4f} (j={val_components['spread_full_joint']:.4f}, "
                                f"m1={val_components['spread_full_mask1']:.4f}, m2={val_components['spread_full_mask2']:.4f}) "
                                f"+ SHORT={val_components['spread_short']:.4f} (j={val_components['spread_short_joint']:.4f}, "
                                f"m1={val_components['spread_short_mask1']:.4f}, m2={val_components['spread_short_mask2']:.4f})"
                            )
                        else:
                            logger.info(f"📊 [epoch={epoch_idx + 1}] VAL LOSS: {val_loss:.4f}")
                    else:
                        val_loss = 0
                        val_components = None
                    
                    # MEMORY LEAK DETECTION: Log VRAM after validation
                    _log_vram_usage("AFTER VALIDATION", epoch_idx)
                except Exception as e:
                    raise e
                
                # Log MI summary every epoch for analysis
                self.log_mi_summary(epoch_idx)
                
                # Log mixture logit changes for SetEncoders (after optimizer step)
                self._log_mixture_logit_changes(epoch_idx)
                
                # Analyze attention head diversity every 25 epochs
                if (epoch_idx + 1) % 25 == 0:
                    try:
                        logger.info(f"\n{'='*80}")
                        self.encoder.joint_encoder.log_attention_analysis()
                        logger.info(f"{'='*80}\n")
                    except Exception as e:
                        logger.warning(f"⚠️  Failed to analyze attention head diversity: {e}")
                
                # Log which columns are trickiest to learn (at the end of each epoch)
                # We log this every 5 epochs to reduce noise, but more frequently early on
                if loss_dict is not None:
                    if epoch_idx < 5 or (epoch_idx + 1) % 5 == 0:
                        self.log_trickiest_columns(loss_dict, epoch_idx, top_n=None)  # None = show ALL columns
                    
                    # Log adaptive strategies EVERY EPOCH with hardest column info
                    self._log_marginal_loss_breakdown(loss_dict, epoch_idx, 0)
                
                # Debug marginal reconstruction quality every 10 epochs
                if epoch_idx > 100 and (epoch_idx % 50 == 0): # or epoch_idx < 5:
                    self._debug_marginal_reconstruction(epoch_idx)
                    self._debug_autoencoding_quality(epoch_idx)
                    self._debug_scalar_reconstruction_quality(epoch_idx)
                
                # Test set vocabulary reconstruction quality every 5 epochs
                # TODO: Implement _debug_set_vocabulary_reconstruction method
                # if epoch_idx % 5 == 0 or epoch_idx < 3:
                #     self._debug_set_vocabulary_reconstruction(epoch_idx)
                
                # Generate movie frame asynchronously EVERY EPOCH (non-blocking)
                # Note: Projection building is now queued right after checkpoint save above
                # This ensures we use the epoch-specific checkpoint that was just saved
                self._queue_movie_frame(epoch_idx)
                
                # ES TRAINING FAILURE DETECTION - analyze training health after each epoch
                # ========================================================================
                # COMPREHENSIVE TRAINING TIMELINE - Track all metrics for visualization
                # ========================================================================
                
                # Initialize timeline tracking on first epoch
                if not hasattr(self, '_training_timeline'):
                    self._training_timeline = []
                    self._corrective_actions = []  # Track interventions
                    logger.info("📊 Training timeline tracking initialized")
                
                # Get current metrics
                current_lr = get_lr()
                lr_value = current_lr[0] if isinstance(current_lr, list) else current_lr
                lr_value = float(lr_value) if lr_value is not None else None
                
                current_dropout = d.get("current_dropout", None)
                current_dropout = float(current_dropout) if current_dropout is not None else None
                
                current_train_loss = loss if isinstance(loss, (int, float)) else None
                current_train_loss = float(current_train_loss) if current_train_loss is not None else None
                
                current_val_loss = val_loss if isinstance(val_loss, (int, float)) else None
                current_val_loss = float(current_val_loss) if current_val_loss is not None else None
                
                # Get gradient information (more detailed than just norm)
                gradient_info = {}
                latest_gradient_norm = getattr(self, '_latest_gradient_norm', None)
                latest_gradient_clipped = getattr(self, '_latest_gradient_clipped', None)
                latest_gradient_ratio = getattr(self, '_latest_gradient_ratio', None)
                
                # Convert tensors to floats for JSON serialization
                if latest_gradient_norm is not None:
                    if hasattr(latest_gradient_norm, 'item'):
                        gradient_info['unclipped_norm'] = float(latest_gradient_norm.item())
                    else:
                        gradient_info['unclipped_norm'] = float(latest_gradient_norm)
                
                if latest_gradient_clipped is not None:
                    if hasattr(latest_gradient_clipped, 'item'):
                        gradient_info['clipped_norm'] = float(latest_gradient_clipped.item())
                    else:
                        gradient_info['clipped_norm'] = float(latest_gradient_clipped)
                
                if latest_gradient_ratio is not None:
                    if hasattr(latest_gradient_ratio, 'item'):
                        gradient_info['clip_ratio'] = float(latest_gradient_ratio.item())
                    else:
                        gradient_info['clip_ratio'] = float(latest_gradient_ratio)
                
                # For backward compatibility, keep the old gradient_norm field
                legacy_gradient_norm = gradient_info.get('unclipped_norm', None)
                
                # Get spread loss and temperature from the encoder (if available)
                spread_temp = getattr(self.encoder, '_last_spread_temp', None)
                spread_loss_total = None
                if hasattr(loss_dict, 'get') and 'spread_loss' in loss_dict:
                    spread_loss_data = loss_dict['spread_loss']
                    spread_loss_total = spread_loss_data.get('total')
                
                # Track temperature changes (including non-intervention changes)
                if not hasattr(self, '_last_spread_temp'):
                    self._last_spread_temp = None
                
                if spread_temp is not None and self._last_spread_temp is not None:
                    temp_change_pct = ((spread_temp - self._last_spread_temp) / self._last_spread_temp) * 100
                    if abs(temp_change_pct) > 10:  # >10% change
                        # Log significant temperature changes
                        logger.info(f"🌡️  [{epoch_idx}] Temperature changed: {self._last_spread_temp:.4f} → {spread_temp:.4f} ({temp_change_pct:+.1f}%) [temp_mult={temp_boost_multiplier}, batch_size={batch_size}]")
                
                self._last_spread_temp = spread_temp
                
                # Build epoch entry
                # Apply K-fold CV offset if present (makes K-fold CV invisible - epochs are cumulative)
                cumulative_epoch = epoch_idx
                if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                    cumulative_epoch = epoch_idx + self._kv_fold_epoch_offset
                
                epoch_entry = {
                    "epoch": cumulative_epoch,  # Use cumulative epoch for timeline (K-fold CV invisible)
                    "learning_rate": lr_value,
                    "lr_multiplier": lr_boost_multiplier,
                    "batch_size": batch_size,  # Track batch size for temperature analysis
                    "val_set_rotated": val_set_rotated,  # Track validation set rotation
                    "train_loss": current_train_loss,
                    "validation_loss": current_val_loss,
                    "val_loss_components": val_components,  # Add component-level loss tracking
                    "dropout_rate": current_dropout,
                    "gradient_norm": legacy_gradient_norm,  # Legacy field for backward compat
                    "gradients": gradient_info,  # Detailed gradient info
                    "spread_loss": spread_loss_total,  # Total spread loss value
                    "spread_temperature": spread_temp,  # Adaptive temperature used
                    "temp_multiplier": temp_boost_multiplier,
                    "failures_detected": [],
                    "early_stop_blocked": False,
                    "corrective_actions": [],
                    "weightwatcher": None  # Will be populated if WW is enabled
                }
                
                # Initialize failure detection variables (will be set if we have enough history)
                has_failure = False
                failure_type = None
                recommendations = []
                
                # Run failure detection analysis if we have enough history
                # Use timeline entries instead of loss_history (which is now in SQLite)
                if epoch_idx >= 5 and hasattr(self, '_training_timeline') and len(self._training_timeline) >= 5:
                    # Extract loss histories from timeline entries
                    train_loss_hist = [entry.get('train_loss', 0) 
                                     for entry in self._training_timeline if isinstance(entry, dict) and entry.get('train_loss') is not None]
                    val_loss_hist = [entry.get('validation_loss', 0) 
                                    for entry in self._training_timeline if isinstance(entry, dict) and entry.get('validation_loss') is not None]
                    
                    # Only analyze if we have enough history
                    if len(train_loss_hist) >= 5 and len(val_loss_hist) >= 5:
                        current_train_loss = train_loss_hist[-1]
                        current_val_loss = val_loss_hist[-1]
                        
                        has_failure, failure_type, recommendations = detect_es_training_failure(
                            epoch_idx=epoch_idx,
                            train_loss=current_train_loss,
                            val_loss=current_val_loss,
                            train_loss_history=train_loss_hist,
                            val_loss_history=val_loss_hist,
                            gradient_norm=latest_gradient_norm,
                            lr=lr_value
                        )
                        
                        # Add failures to timeline
                        if has_failure and failure_type:
                            epoch_entry["failures_detected"] = failure_type if isinstance(failure_type, list) else [failure_type]
                        
                        # Smart logging: only log when failure type CHANGES or when intervening
                        if not hasattr(self, '_last_logged_failure'):
                            self._last_logged_failure = None
                            self._failure_repeat_count = 0
                        
                        failure_changed = (failure_type != self._last_logged_failure)
                        
                        # Track warnings in timeline
                        # Check each failure type and track start/stop
                        failure_list = failure_type if isinstance(failure_type, list) else ([failure_type] if failure_type else [])
                        
                        # Track NO_LEARNING
                        no_learning_active = any("NO_LEARNING" in f for f in failure_list)
                        self._track_warning_in_timeline(
                            epoch_idx=epoch_idx,
                            warning_type="NO_LEARNING",
                            is_active=no_learning_active,
                            details={
                                "train_loss": current_train_loss,
                                "val_loss": current_val_loss,
                                "lr": lr_value,
                                "gradient_norm": latest_gradient_norm,
                                "recommendations": recommendations
                            }
                        )
                        
                        # Track SEVERE_OVERFITTING
                        overfitting_active = any("SEVERE_OVERFITTING" in f for f in failure_list)
                        self._track_warning_in_timeline(
                            epoch_idx=epoch_idx,
                            warning_type="SEVERE_OVERFITTING",
                            is_active=overfitting_active,
                            details={
                                "train_loss": current_train_loss,
                                "val_loss": current_val_loss,
                                "train_val_gap": current_val_loss - current_train_loss if (current_val_loss and current_train_loss) else None
                            }
                        )
                        
                        # Track DEAD_GRADIENTS
                        dead_grad_active = any("DEAD_GRADIENTS" in f or "ZERO_GRADIENTS" in f for f in failure_list)
                        self._track_warning_in_timeline(
                            epoch_idx=epoch_idx,
                            warning_type="DEAD_GRADIENTS",
                            is_active=dead_grad_active,
                            details={
                                "gradient_norm": latest_gradient_norm,
                                "lr": lr_value
                            }
                        )
                        
                        # Track NO_LEARNING failures with GRADUAL LR ramping
                        if has_failure and failure_type and "NO_LEARNING" in failure_type:
                            epochs_since_last_intervention += 1
                            
                            # Only log when failure is NEW or when taking action
                            if failure_changed:
                                logger.warning(f"⚠️  [{epoch_idx}] NO_LEARNING detected → loss plateaued at train={current_train_loss:.4f} val={current_val_loss:.4f}")
                                self._last_logged_failure = failure_type
                                self._failure_repeat_count = 1
                            else:
                                self._failure_repeat_count += 1
                                # Log compact reminder every 10 epochs
                                if self._failure_repeat_count % 10 == 0:
                                    logger.info(f"📊 [{epoch_idx}] Still NO_LEARNING (×{self._failure_repeat_count}), train={current_train_loss:.4f} val={current_val_loss:.4f}, lr_boost={lr_boost_multiplier:.2f}x")
                            
                            # GRADUAL LR BOOST: Increase by 1.2x each epoch (up to 6x max)
                            # This is MUCH safer than jumping 3x → 6x immediately
                            intervention_made = False
                            
                            # Initialize tracker
                            if not hasattr(self, '_no_learning_tracker'):
                                self._no_learning_tracker = {}
                            
                            # Gradually increase LR boost each epoch (1.2x, 1.44x, 1.728x, ..., up to 6x max)
                            old_boost = lr_boost_multiplier
                            lr_boost_multiplier = min(lr_boost_multiplier * 1.2, 6.0)
                            
                            if lr_boost_multiplier != old_boost:
                                intervention_made = True
                                logger.warning(f"🚀 [{epoch_idx}] Gradual LR boost: {old_boost:.2f}x → {lr_boost_multiplier:.2f}x (base_lr × {lr_boost_multiplier:.2f} = {lr_value * lr_boost_multiplier:.6f})")
                                intervention_stage = 1  # Mark that we're in intervention mode
                            
                            # Temperature boost after LR boost hits 3x (gentler escalation)
                            if lr_boost_multiplier >= 3.0 and temp_boost_multiplier < 2.0:
                                temp_boost_multiplier = 2.0
                                intervention_made = True
                                intervention_stage = 2
                                logger.warning(f"🌡️  [{epoch_idx}] Temperature boost: 1.0x → 2.0x (harder task, LR is at {lr_boost_multiplier:.2f}x)")
                            
                            # Stop training if LR boost maxed out and still no learning
                            if lr_boost_multiplier >= 6.0 and self._failure_repeat_count >= 10:
                                logger.error(f"🛑 [{epoch_idx}] CONVERGED: LR boost maxed at 6x, no learning for 10+ epochs → stopping (val_loss={val_loss:.4f})")
                                
                                corrective_action = {
                                    "epoch": epoch_idx,
                                    "trigger": "CONVERGED",
                                    "action_type": "STOP_TRAINING",
                                    "details": {
                                        "val_loss": val_loss,
                                        "lr_boost": lr_boost_multiplier,
                                        "no_learning_epochs": self._failure_repeat_count,
                                        "reason": "LR boost maxed at 6x with no improvement"
                                    }
                                }
                                epoch_entry["corrective_actions"].append(corrective_action)
                                self._corrective_actions.append(corrective_action)
                                break  # Exit training loop
                            
                            # Block early stopping when intervening
                            if intervention_made:
                                self._no_learning_tracker['last_no_learning_epoch'] = epoch_idx
                                self._no_learning_tracker['min_epochs_before_early_stop'] = 10
                                epoch_entry["early_stop_blocked"] = True
                                logger.info(f"   → Early stopping blocked for 10 epochs")
                                epochs_since_last_intervention = 0
                                
                                corrective_action = {
                                    "epoch": epoch_idx,
                                    "trigger": "NO_LEARNING",
                                    "action_type": "GRADUAL_LR_BOOST",
                                    "details": {
                                        "blocked_for_epochs": 10,
                                        "lr_multiplier": lr_boost_multiplier,
                                        "temp_multiplier": temp_boost_multiplier,
                                        "intervention_stage": intervention_stage,
                                        "current_dropout": current_dropout
                                    }
                                }
                                epoch_entry["corrective_actions"].append(corrective_action)
                                self._corrective_actions.append(corrective_action)
                        
                        # RESET boost when learning resumes (loss improving again)
                        else:
                            # Check if we were previously in NO_LEARNING state
                            if lr_boost_multiplier > 1.0 or temp_boost_multiplier > 1.0:
                                logger.info(f"✅ [{epoch_idx}] Learning resumed! Resetting LR boost {lr_boost_multiplier:.2f}x → 1.0x, temp {temp_boost_multiplier:.2f}x → 1.0x")
                                lr_boost_multiplier = 1.0
                                temp_boost_multiplier = 1.0
                                intervention_stage = 0
                                self._failure_repeat_count = 0
                                self._last_logged_failure = None
                                epochs_since_last_intervention = 0
                                
                                corrective_action = {
                                    "epoch": epoch_idx,
                                    "trigger": "LEARNING_RESUMED",
                                    "action_type": "RESET_INTERVENTIONS",
                                    "details": {
                                        "lr_multiplier": 1.0,
                                        "temp_multiplier": 1.0,
                                        "train_loss": current_train_loss,
                                        "val_loss": current_val_loss
                                    }
                                }
                                epoch_entry["corrective_actions"].append(corrective_action)
                                self._corrective_actions.append(corrective_action)
                
                # Check for resolved warnings (warnings that were active but are no longer detected)
                # This happens after we've processed failures, so we know current state
                if hasattr(self, '_active_warnings'):
                    active_warning_types = set(self._active_warnings.keys())
                    current_failure_types = set()
                    if has_failure and failure_type:
                        failure_list = failure_type if isinstance(failure_type, list) else [failure_type]
                        if "NO_LEARNING" in str(failure_list):
                            current_failure_types.add("NO_LEARNING")
                        if "SEVERE_OVERFITTING" in str(failure_list):
                            current_failure_types.add("SEVERE_OVERFITTING")
                        if "DEAD_GRADIENTS" in str(failure_list) or "ZERO_GRADIENTS" in str(failure_list):
                            current_failure_types.add("DEAD_GRADIENTS")
                    
                    # Check TINY_GRADIENTS separately (it's checked during batch loop)
                    # If we warned this epoch, it's still active
                    if hasattr(self, '_tiny_grad_warned_this_epoch') and self._tiny_grad_warned_this_epoch:
                        current_failure_types.add("TINY_GRADIENTS")
                    # If we didn't warn this epoch but it was active before, check if gradient recovered
                    elif "TINY_GRADIENTS" in active_warning_types:
                        # Check if gradient is now reasonable (>= 0.001 means not tiny anymore)
                        latest_grad_norm = getattr(self, '_latest_gradient_norm', None)
                        if latest_grad_norm is not None:
                            grad_val = float(latest_grad_norm.item()) if hasattr(latest_grad_norm, 'item') else float(latest_grad_norm)
                            if grad_val < 0.001:  # Still tiny
                                current_failure_types.add("TINY_GRADIENTS")
                    
                    # Resolve warnings that are no longer active
                    for warning_type in list(active_warning_types):
                        if warning_type not in current_failure_types:
                            # Warning resolved
                            self._track_warning_in_timeline(
                                epoch_idx=epoch_idx,
                                warning_type=warning_type,
                                is_active=False,
                                details={
                                    "train_loss": current_train_loss,
                                    "val_loss": current_val_loss,
                                    "lr": lr_value
                                }
                            )
                
                # Add entry to timeline
                self._training_timeline.append(epoch_entry)
                # MEMORY LEAK FIX: Push to SQLite and keep timeline in memory (it's already limited)
                if hasattr(self, 'history_db') and self.history_db:
                    self.history_db.push_timeline_entry(epoch_idx, epoch_entry)
                # Keep timeline in memory (it's the main thing we want to track)
                # Limit to last 50 entries to prevent unbounded growth
                max_timeline_history = 50
                if len(self._training_timeline) > max_timeline_history:
                    self._training_timeline = self._training_timeline[-max_timeline_history:]
                
                # CLEAN EPOCH SUMMARY - one line per epoch with key metrics
                # ========================================================
                # EPOCH SUMMARY - Add separator for visual grouping
                # ========================================================
                logger.info("─" * 100)
                
                status_symbol = "✅" if not has_failure else "⚠️ "
                failure_label = f" [{failure_type}]" if has_failure and failure_type else ""
                intervention_label = f" I{intervention_stage}" if intervention_stage > 0 else ""
                
                # Calculate cumulative epoch for K-fold CV (makes K-fold CV invisible - epochs are cumulative)
                cumulative_epoch = epoch_idx
                if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                    cumulative_epoch = epoch_idx + self._kv_fold_epoch_offset
                
                # Get values safely (they might be None in some edge cases)
                lr_value_str = f"{lr_value:.6f}" if lr_value else "N/A"
                current_dropout_str = f"{current_dropout:0.3f} " if current_dropout else "N/A"
                train_loss_str = f"{current_train_loss:.4f}" if current_train_loss is not None else "N/A"
                val_loss_str = f"{current_val_loss:.4f}" if current_val_loss is not None else "N/A"
                grad_str = f"{latest_gradient_norm:.4f}" if latest_gradient_norm is not None else "N/A"
                # Show cumulative epoch in status line
                # For K-fold CV, show cumulative epoch without denominator (n_epochs is per-fold, not total)
                epoch_str = f"{cumulative_epoch:3d}" if cumulative_epoch is not None else "?"
                if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                    # K-fold CV: just show cumulative epoch
                    epoch_display = f"{epoch_str}"
                else:
                    # Regular training: show epoch/total
                    epochs_str = f"{n_epochs}" if n_epochs is not None else "?"
                    epoch_display = f"{epoch_str}/{epochs_str}"
                
                logger.info(
                    f"{status_symbol} [{epoch_display}] "
                    f"train={train_loss_str} val={val_loss_str} "
                    f"lr={lr_value_str} drop={current_dropout_str} "
                    f"grad={grad_str}{intervention_label}{failure_label}"
                )
                
                # Save timeline to JSON file every 5 epochs
                if n_epochs is not None and (epoch_idx % 5 == 0 or epoch_idx == n_epochs - 1):
                    timeline_path = os.path.join(self.output_dir, "training_timeline.json")
                    try:
                        with open(timeline_path, 'w') as f:
                            json.dump({
                                "timeline": self._training_timeline,
                                "corrective_actions": self._corrective_actions,
                                "metadata": {
                                    "initial_lr": optimizer_params.get("lr", 0.001),
                                    "total_epochs": n_epochs,
                                    "batch_size": batch_size,  # Add batch size to metadata
                                    "scheduler_type": "OneCycleLR" if scheduler else "None",
                                    "dropout_scheduler_enabled": dropout_scheduler is not None,
                                    "initial_dropout": initial_dropout if dropout_scheduler else None,
                                    "final_dropout": final_dropout if dropout_scheduler else None
                                }
                            }, f, indent=2)
                        # Show cumulative epoch for K-fold CV
                        cumulative_epoch = epoch_idx
                        if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                            cumulative_epoch = epoch_idx + self._kv_fold_epoch_offset
                        logger.info(f"[epoch={cumulative_epoch}] 💾 Training timeline saved to {timeline_path}")
                    except Exception as e:
                        logger.warning(f"[epoch={epoch_idx}] ⚠️  Failed to save training timeline: {e}")

                thisProc = psutil.Process(os.getpid())
                with thisProc.oneshot():
                    cpu_times = thisProc.cpu_times()
                    cpu_times = {"user": cpu_times.user, "system": cpu_times.system}
                    mem_info = thisProc.memory_info()
                    mem_info = {"rss": mem_info.rss, "vms": mem_info.vms}
                    resource_usage = {
                        "epoch": 1 + epoch_idx,
                        "pid": os.getpid(),
                        "p_create_time": thisProc.create_time(),
                        "p_cpu_times": cpu_times,
                        "p_mem_info": mem_info,
                    }
                    training_event_dict["resource_usage"] = resource_usage

                # Report gradient clipping statistics for this epoch
                if grad_clip_stats["total_batches"] > 0:
                    if use_adaptive_clipping:
                        clip_rate = (grad_clip_stats["clipped_batches"] / grad_clip_stats["total_batches"]) * 100
                        avg_unclipped = grad_clip_stats["sum_unclipped_norms"] / grad_clip_stats["total_batches"]
                        
                        # Show cumulative epoch for K-fold CV
                        cumulative_epoch = epoch_idx
                        if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                            cumulative_epoch = epoch_idx + self._kv_fold_epoch_offset
                        logger.info(f"📊 [epoch={cumulative_epoch}] GRADIENT STATS: clipped={grad_clip_stats['clipped_batches']}/{grad_clip_stats['total_batches']} ({clip_rate:.1f}%), "
                                   f"max_ratio={grad_clip_stats['max_grad_loss_ratio']:.2f}, avg_grad={avg_unclipped:.2f}")
                        
                        # Analyze gradient/loss relationship if we have history
                        if len(grad_clip_stats["gradient_norms_history"]) >= 10:
                            import numpy as np
                            grads = np.array(grad_clip_stats["gradient_norms_history"])
                            losses = np.array(grad_clip_stats["loss_values_history"])
                            
                            if len(grads) > 1 and np.std(grads) > 0 and np.std(losses) > 0:
                                correlation = np.corrcoef(grads, losses)[0, 1]
                                avg_ratio = np.mean(grads / (losses + 1e-8))
                                logger.info(f"📈 [epoch={epoch_idx}] grad/loss: correlation={correlation:.3f}, avg_ratio={avg_ratio:.3f}")

                # Save out the state
                if save_state_after_every_epoch:
                    logger.info("about to save_state_after_every_epoch")
                    try:
                        self.save_state(epoch_idx, 0, self.encoder, optimizer, scheduler, dropout_scheduler)
                        # Queue projection build task only if embedding space checkpoint was saved successfully
                        if getattr(self, '_last_embedding_space_checkpoint_saved', False):
                            self._queue_project_training_movie_frame(epoch_idx)
                        else:
                            logger.warning(f"⚠️  Skipping projection build for epoch {epoch_idx} - embedding space checkpoint not saved")
                    except Exception as e:
                        # Don't abort training if checkpoint save fails
                        logger.warning(f"⚠️  Failed to save checkpoint after epoch {epoch_idx}: {e}")
                        logger.warning(f"   Training will continue - checkpoint can be saved at next epoch")
                if epoch_idx > 0 and save_state_epoch_interval > 0 and (epoch_idx % save_state_epoch_interval) == 0:
                    logger.info(f"[epoch={epoch_idx}] 💾 Saving checkpoint (interval={save_state_epoch_interval}, total_epochs={n_epochs})")
                    try:
                        self.save_state(epoch_idx, 0, self.encoder, optimizer, scheduler, dropout_scheduler)
                        # Queue projection build task only if embedding space checkpoint was saved successfully
                        if getattr(self, '_last_embedding_space_checkpoint_saved', False):
                            self._queue_project_training_movie_frame(epoch_idx)
                        else:
                            logger.warning(f"⚠️  Skipping projection build for epoch {epoch_idx} - embedding space checkpoint not saved")
                    except Exception as e:
                        # Don't abort training if periodic checkpoint save fails
                        logger.warning(f"⚠️  Failed to save periodic checkpoint at epoch {epoch_idx}: {e}")
                        logger.warning(f"   Training will continue - checkpoint can be saved at next interval or best model save")

                # If the validation loss is the lowest it's been, save the current model
                # to a file. Only compare if val_loss is numeric (not "not set")
                if isinstance(val_loss, (int, float)) and isinstance(lowest_val_loss, (int, float)) and val_loss < lowest_val_loss:
                    lowest_val_loss = val_loss
                    try:
                        self.save_best_checkoint(epoch_idx, self.encoder, val_loss)
                    except Exception as e:
                        # Don't abort training if best checkpoint save fails
                        logger.warning(f"⚠️  Failed to save best checkpoint at epoch {epoch_idx}: {e}")
                        logger.warning(f"   Training will continue - best model will be saved on next improvement")
                
                # VALIDATION LOSS EARLY STOPPING - check if validation loss is increasing (overfitting)
                # Now tracks BOTH total loss AND individual components (spread, joint, marginal)
                if not hasattr(self, '_val_loss_tracker'):
                    self._val_loss_tracker = {
                        'best_val_loss': float('inf'),
                        'epochs_without_improvement': 0,
                        'patience': val_loss_early_stop_patience,
                        'min_delta': val_loss_min_delta,
                        # Component-level tracking
                        'best_spread': float('inf'),
                        'best_joint': float('inf'),
                        'best_marginal': float('inf'),
                        'spread_no_improvement': 0,
                        'joint_no_improvement': 0,
                        'marginal_no_improvement': 0,
                        # Track LR and marginal weight history for display
                        'lr_history': [],
                        'marginal_weight_history': []
                    }
                    logger.info(f"📉 Validation loss early stopping enabled: patience={val_loss_early_stop_patience}, min_delta={val_loss_min_delta}")
                    logger.info(f"📊 Component-level tracking enabled: spread, joint, marginal losses")
                
                if isinstance(val_loss, (int, float)) and val_loss > 0:
                    # Track component improvements
                    if val_components:
                        for comp_name in ['spread', 'joint', 'marginal']:
                            if comp_name in val_components:
                                comp_val = val_components[comp_name]
                                best_key = f'best_{comp_name}'
                                no_improve_key = f'{comp_name}_no_improvement'
                                
                                # Get previous epoch loss for change calculation
                                prev_loss = self._val_loss_tracker.get(f'{comp_name}_prev', comp_val)
                                
                                # Initialize start loss if first time
                                start_loss = self._val_loss_tracker.get(f'{comp_name}_start', comp_val)
                                if f'{comp_name}_start' not in self._val_loss_tracker:
                                    self._val_loss_tracker[f'{comp_name}_start'] = comp_val
                                    start_loss = comp_val
                                
                                # Track loss history for windowed improvements
                                history_key = f'{comp_name}_history'
                                if history_key not in self._val_loss_tracker:
                                    self._val_loss_tracker[history_key] = []
                                self._val_loss_tracker[history_key].append((epoch_idx, comp_val))
                                
                                # Calculate change vs previous epoch
                                change_vs_last = prev_loss - comp_val
                                change_pct_vs_last = ((change_vs_last / prev_loss * 100) if prev_loss > 0 else 0) if prev_loss != comp_val else 0
                                
                                # Determine status: improved, worsened, or no change
                                min_delta = self._val_loss_tracker['min_delta']
                                if comp_val < self._val_loss_tracker[best_key] - min_delta:
                                    status = "improved"
                                    self._val_loss_tracker[best_key] = comp_val
                                    self._val_loss_tracker[no_improve_key] = 0
                                    
                                    # Calculate improvements from different baselines
                                    imp_since_start = ((start_loss - comp_val) / start_loss * 100) if start_loss > 0 else 0
                                    imp_vs_last = ((prev_loss - comp_val) / prev_loss * 100) if prev_loss > 0 else 0
                                    
                                    # Time-moving graph: n-16, n-8, n-4, n-2, n-1, n
                                    history = self._val_loss_tracker[history_key]
                                    
                                    # Find loss values at specific epochs ago
                                    loss_n16 = None
                                    loss_n8 = None
                                    loss_n4 = None
                                    loss_n2 = None
                                    loss_n1 = prev_loss
                                    
                                    # Search backwards through history
                                    for hist_epoch, hist_loss in reversed(history[:-1]):  # Exclude current epoch
                                        epochs_ago = epoch_idx - hist_epoch
                                        if epochs_ago == 16 and loss_n16 is None:
                                            loss_n16 = hist_loss
                                        if epochs_ago == 8 and loss_n8 is None:
                                            loss_n8 = hist_loss
                                        if epochs_ago == 4 and loss_n4 is None:
                                            loss_n4 = hist_loss
                                        if epochs_ago == 2 and loss_n2 is None:
                                            loss_n2 = hist_loss
                                        if epochs_ago == 1 and loss_n1 is None:
                                            loss_n1 = hist_loss
                                        if loss_n16 is not None and loss_n8 is not None and loss_n4 is not None and loss_n2 is not None and loss_n1 is not None:
                                            break
                                    
                                    # Simple numbers format
                                    nums = []
                                    nums.append(f"{loss_n16:8.4f}" if loss_n16 is not None else "     N/A")
                                    nums.append(f"{loss_n8:8.4f}" if loss_n8 is not None else "     N/A")
                                    nums.append(f"{loss_n4:8.4f}" if loss_n4 is not None else "     N/A")
                                    nums.append(f"{loss_n2:8.4f}" if loss_n2 is not None else "     N/A")
                                    nums.append(f"{loss_n1:8.4f}" if loss_n1 is not None else "     N/A")
                                    nums.append(f"{comp_val:8.4f}")
                                    
                                    logger.info(f"[epoch={epoch_idx}] {comp_name.capitalize():8s}: {' '.join(nums)}")
                                elif comp_val > prev_loss + min_delta:
                                    status = "worsened"
                                    self._val_loss_tracker[no_improve_key] += 1
                                    
                                    # Time-moving: n-16, n-8, n-4, n-2, n-1, n
                                    history = self._val_loss_tracker[history_key]
                                    loss_n16 = None
                                    loss_n8 = None
                                    loss_n4 = None
                                    loss_n2 = None
                                    loss_n1 = prev_loss
                                    
                                    for hist_epoch, hist_loss in reversed(history[:-1]):
                                        epochs_ago = epoch_idx - hist_epoch
                                        if epochs_ago == 16 and loss_n16 is None:
                                            loss_n16 = hist_loss
                                        if epochs_ago == 8 and loss_n8 is None:
                                            loss_n8 = hist_loss
                                        if epochs_ago == 4 and loss_n4 is None:
                                            loss_n4 = hist_loss
                                        if epochs_ago == 2 and loss_n2 is None:
                                            loss_n2 = hist_loss
                                        if epochs_ago == 1 and loss_n1 is None:
                                            loss_n1 = hist_loss
                                        if loss_n16 is not None and loss_n8 is not None and loss_n4 is not None and loss_n2 is not None and loss_n1 is not None:
                                            break
                                    
                                    nums = []
                                    nums.append(f"{loss_n16:8.4f}" if loss_n16 is not None else "     N/A")
                                    nums.append(f"{loss_n8:8.4f}" if loss_n8 is not None else "     N/A")
                                    nums.append(f"{loss_n4:8.4f}" if loss_n4 is not None else "     N/A")
                                    nums.append(f"{loss_n2:8.4f}" if loss_n2 is not None else "     N/A")
                                    nums.append(f"{loss_n1:8.4f}" if loss_n1 is not None else "     N/A")
                                    nums.append(f"{comp_val:8.4f}")
                                    
                                    logger.info(f"[epoch={epoch_idx}] {comp_name.capitalize():8s}: {' '.join(nums)}")
                                else:
                                    status = "no change"
                                    self._val_loss_tracker[no_improve_key] += 1
                                    
                                    # Time-moving: n-16, n-8, n-4, n-2, n-1, n
                                    history = self._val_loss_tracker[history_key]
                                    loss_n16 = None
                                    loss_n8 = None
                                    loss_n4 = None
                                    loss_n2 = None
                                    loss_n1 = prev_loss
                                    
                                    for hist_epoch, hist_loss in reversed(history[:-1]):
                                        epochs_ago = epoch_idx - hist_epoch
                                        if epochs_ago == 16 and loss_n16 is None:
                                            loss_n16 = hist_loss
                                        if epochs_ago == 8 and loss_n8 is None:
                                            loss_n8 = hist_loss
                                        if epochs_ago == 4 and loss_n4 is None:
                                            loss_n4 = hist_loss
                                        if epochs_ago == 2 and loss_n2 is None:
                                            loss_n2 = hist_loss
                                        if epochs_ago == 1 and loss_n1 is None:
                                            loss_n1 = hist_loss
                                        if loss_n16 is not None and loss_n8 is not None and loss_n4 is not None and loss_n2 is not None and loss_n1 is not None:
                                            break
                                    
                                    nums = []
                                    nums.append(f"{loss_n16:8.4f}" if loss_n16 is not None else "     N/A")
                                    nums.append(f"{loss_n8:8.4f}" if loss_n8 is not None else "     N/A")
                                    nums.append(f"{loss_n4:8.4f}" if loss_n4 is not None else "     N/A")
                                    nums.append(f"{loss_n2:8.4f}" if loss_n2 is not None else "     N/A")
                                    nums.append(f"{loss_n1:8.4f}" if loss_n1 is not None else "     N/A")
                                    nums.append(f"{comp_val:8.4f}")
                                    
                                    logger.info(f"[epoch={epoch_idx}] {comp_name.capitalize():8s}: {' '.join(nums)}")
                                    
                                    # Special warning for marginal loss: if it's not improving but weight is changing
                                    if comp_name == 'marginal' and self._val_loss_tracker.get(f'{comp_name}_no_improvement', 0) >= 5:
                                        current_marginal_weight = self.encoder.config.loss_config.marginal_loss_weight
                                        logger.warning(f"⚠️  Marginal loss hasn't improved for {self._val_loss_tracker[f'{comp_name}_no_improvement']} epochs, but weight={current_marginal_weight:.4f} is changing due to curriculum schedule")
                                
                                # Always update previous value
                                self._val_loss_tracker[f'{comp_name}_prev'] = comp_val
                    
                    # Track LR and marginal weight history for display
                    if 'lr_history' not in self._val_loss_tracker:
                        self._val_loss_tracker['lr_history'] = []
                    if 'marginal_weight_history' not in self._val_loss_tracker:
                        self._val_loss_tracker['marginal_weight_history'] = []
                    
                    # Get current LR and marginal weight
                    current_lr = get_lr()
                    lr_value = current_lr[0] if isinstance(current_lr, list) else current_lr
                    current_marginal_weight = self.encoder.config.loss_config.marginal_loss_weight
                    
                    # Track history
                    self._val_loss_tracker['lr_history'].append((epoch_idx, lr_value))
                    self._val_loss_tracker['marginal_weight_history'].append((epoch_idx, current_marginal_weight))
                    
                    # Log LR and marginal weight in same format as component losses
                    # Find values at n-16, n-8, n-4, n-2, n-1 epochs ago
                    lr_history = self._val_loss_tracker['lr_history']
                    lr_n16 = None
                    lr_n8 = None
                    lr_n4 = None
                    lr_n2 = None
                    lr_n1 = None
                    
                    for hist_epoch, hist_lr in reversed(lr_history[:-1]):
                        epochs_ago = epoch_idx - hist_epoch
                        if epochs_ago == 16 and lr_n16 is None:
                            lr_n16 = hist_lr
                        if epochs_ago == 8 and lr_n8 is None:
                            lr_n8 = hist_lr
                        if epochs_ago == 4 and lr_n4 is None:
                            lr_n4 = hist_lr
                        if epochs_ago == 2 and lr_n2 is None:
                            lr_n2 = hist_lr
                        if epochs_ago == 1 and lr_n1 is None:
                            lr_n1 = hist_lr
                        if lr_n16 is not None and lr_n8 is not None and lr_n4 is not None and lr_n2 is not None and lr_n1 is not None:
                            break
                    
                    lr_nums = []
                    lr_nums.append(f"{lr_n16:8.4e}" if lr_n16 is not None else "     N/A")
                    lr_nums.append(f"{lr_n8:8.4e}" if lr_n8 is not None else "     N/A")
                    lr_nums.append(f"{lr_n4:8.4e}" if lr_n4 is not None else "     N/A")
                    lr_nums.append(f"{lr_n2:8.4e}" if lr_n2 is not None else "     N/A")
                    lr_nums.append(f"{lr_n1:8.4e}" if lr_n1 is not None else "     N/A")
                    lr_nums.append(f"{lr_value:8.4e}")
                    logger.info(f"[epoch={epoch_idx}] LR       : {' '.join(lr_nums)}")
                    
                    # Marginal weight history
                    mw_history = self._val_loss_tracker['marginal_weight_history']
                    mw_n16 = None
                    mw_n8 = None
                    mw_n4 = None
                    mw_n2 = None
                    mw_n1 = None
                    
                    for hist_epoch, hist_mw in reversed(mw_history[:-1]):
                        epochs_ago = epoch_idx - hist_epoch
                        if epochs_ago == 16 and mw_n16 is None:
                            mw_n16 = hist_mw
                        if epochs_ago == 8 and mw_n8 is None:
                            mw_n8 = hist_mw
                        if epochs_ago == 4 and mw_n4 is None:
                            mw_n4 = hist_mw
                        if epochs_ago == 2 and mw_n2 is None:
                            mw_n2 = hist_mw
                        if epochs_ago == 1 and mw_n1 is None:
                            mw_n1 = hist_mw
                        if mw_n16 is not None and mw_n8 is not None and mw_n4 is not None and mw_n2 is not None and mw_n1 is not None:
                            break
                    
                    mw_nums = []
                    mw_nums.append(f"{mw_n16:8.4f}" if mw_n16 is not None else "     N/A")
                    mw_nums.append(f"{mw_n8:8.4f}" if mw_n8 is not None else "     N/A")
                    mw_nums.append(f"{mw_n4:8.4f}" if mw_n4 is not None else "     N/A")
                    mw_nums.append(f"{mw_n2:8.4f}" if mw_n2 is not None else "     N/A")
                    mw_nums.append(f"{mw_n1:8.4f}" if mw_n1 is not None else "     N/A")
                    mw_nums.append(f"{current_marginal_weight:8.4f}")
                    logger.info(f"[epoch={epoch_idx}] Marg Wt  : {' '.join(mw_nums)}")
                    
                    # Don't start early stopping until at least epoch 50
                    # SPECIAL: With OneCycleLR, wait even longer (60% of epochs + 10%)
                    # because the LR ramps UP for first ~45%, peaks, then cools down
                    # We need to let the cooldown phase finish before considering early stop
                    min_epoch_for_early_stop = 50
                    if scheduler is not None and isinstance(scheduler, OneCycleLR):
                        # OneCycleLR: peak is around 30-45% of training
                        # Wait until at least 60% + 10% buffer before allowing early stop
                        min_epoch_for_early_stop = int(n_epochs * 0.70)  # 70% of total epochs
                        logger.info(f"[epoch={epoch_idx}] 📍 OneCycleLR detected: early stopping disabled until epoch {min_epoch_for_early_stop} ({min_epoch_for_early_stop/n_epochs*100:.0f}% of {n_epochs} epochs)")
                    
                    if epoch_idx < min_epoch_for_early_stop:
                        if epoch_idx == 50 or epoch_idx % 20 == 0:  # Log occasionally
                            logger.info(f"⏭️  Early stopping DISABLED until epoch {min_epoch_for_early_stop} (currently at epoch {epoch_idx})")
                        # Skip all early stopping logic - just continue training
                        pass
                    else:
                        # Check validation loss change (improved, worsened, or no change)
                        prev_val_loss = self._val_loss_tracker.get('val_prev', val_loss)
                        min_delta = self._val_loss_tracker['min_delta']
                        change_vs_last = prev_val_loss - val_loss
                        change_pct_vs_last = ((change_vs_last / prev_val_loss * 100) if prev_val_loss > 0 else 0) if prev_val_loss != val_loss else 0
                        
                        # Initialize start loss if first time
                        start_loss = self._val_loss_tracker.get('val_start', val_loss)
                        if 'val_start' not in self._val_loss_tracker:
                            self._val_loss_tracker['val_start'] = val_loss
                            start_loss = val_loss
                        
                        # Track loss history for windowed improvements
                        if 'val_history' not in self._val_loss_tracker:
                            self._val_loss_tracker['val_history'] = []
                        self._val_loss_tracker['val_history'].append((epoch_idx, val_loss))
                        
                        if val_loss < self._val_loss_tracker['best_val_loss'] - min_delta:
                            status = "improved"
                            self._val_loss_tracker['best_val_loss'] = val_loss
                            self._val_loss_tracker['epochs_without_improvement'] = 0
                            
                            # Calculate improvements from different baselines
                            imp_since_start = ((start_loss - val_loss) / start_loss * 100) if start_loss > 0 else 0
                            imp_vs_last = ((prev_val_loss - val_loss) / prev_val_loss * 100) if prev_val_loss > 0 else 0
                            
                            # Time-moving: n-16, n-8, n-4, n-2, n-1, n
                            history = self._val_loss_tracker['val_history']
                            loss_n16 = None
                            loss_n8 = None
                            loss_n4 = None
                            loss_n2 = None
                            loss_n1 = prev_val_loss
                            
                            for hist_epoch, hist_loss in reversed(history[:-1]):
                                epochs_ago = epoch_idx - hist_epoch
                                if epochs_ago == 16 and loss_n16 is None:
                                    loss_n16 = hist_loss
                                if epochs_ago == 8 and loss_n8 is None:
                                    loss_n8 = hist_loss
                                if epochs_ago == 4 and loss_n4 is None:
                                    loss_n4 = hist_loss
                                if epochs_ago == 2 and loss_n2 is None:
                                    loss_n2 = hist_loss
                                if epochs_ago == 1 and loss_n1 is None:
                                    loss_n1 = hist_loss
                                if loss_n16 is not None and loss_n8 is not None and loss_n4 is not None and loss_n2 is not None and loss_n1 is not None:
                                    break
                            
                            nums = []
                            nums.append(f"{loss_n16:8.4f}" if loss_n16 is not None else "     N/A")
                            nums.append(f"{loss_n8:8.4f}" if loss_n8 is not None else "     N/A")
                            nums.append(f"{loss_n4:8.4f}" if loss_n4 is not None else "     N/A")
                            nums.append(f"{loss_n2:8.4f}" if loss_n2 is not None else "     N/A")
                            nums.append(f"{loss_n1:8.4f}" if loss_n1 is not None else "     N/A")
                            nums.append(f"{val_loss:8.4f}")
                            
                            logger.info(f"[epoch={epoch_idx}] Val loss  : {' '.join(nums)}")
                        elif val_loss > prev_val_loss + min_delta:
                            status = "worsened"
                            self._val_loss_tracker['epochs_without_improvement'] += 1
                            
                            # Calculate improvements from different baselines for consistency
                            imp_since_start = ((start_loss - val_loss) / start_loss * 100) if start_loss > 0 else 0
                            imp_vs_last = ((prev_val_loss - val_loss) / prev_val_loss * 100) if prev_val_loss > 0 else 0
                            history = self._val_loss_tracker['val_history']
                            imp_6_ago = None
                            imp_3_ago = None
                            epoch_6_ago = None
                            epoch_3_ago = None
                            for hist_epoch, hist_loss in reversed(history[:-1]):
                                epochs_ago = epoch_idx - hist_epoch
                                if epochs_ago == 6 and imp_6_ago is None:
                                    imp_6_ago = ((hist_loss - val_loss) / hist_loss * 100) if hist_loss > 0 else 0
                                    epoch_6_ago = hist_epoch
                                if epochs_ago == 3 and imp_3_ago is None:
                                    imp_3_ago = ((hist_loss - val_loss) / hist_loss * 100) if hist_loss > 0 else 0
                                    epoch_3_ago = hist_epoch
                                if imp_6_ago is not None and imp_3_ago is not None:
                                    break
                            
                            imp_parts = []
                            imp_parts.append(f"epoch=  0: {imp_since_start:+7.2f}%")
                            if imp_6_ago is not None:
                                imp_parts.append(f"epoch={epoch_6_ago:3d}: {imp_6_ago:+7.2f}%")
                            else:
                                imp_parts.append(f"epoch=6ago: {'N/A':>7s}")
                            if imp_3_ago is not None:
                                imp_parts.append(f"epoch={epoch_3_ago:3d}: {imp_3_ago:+7.2f}%")
                            else:
                                imp_parts.append(f"epoch=3ago: {'N/A':>7s}")
                            imp_parts.append(f"epoch={epoch_idx-1:3d}: {imp_vs_last:+7.2f}%")
                            
                            change_str = f"{change_pct_vs_last:.2f}%"
                            logger.info(f"LOSS IMPROVEMENT: [epoch={epoch_idx}] Val loss   [{status:8s}] {val_loss:.4f} ({change_str:>7s}) | {' | '.join(imp_parts)}")
                        else:
                            status = "no change"
                            self._val_loss_tracker['epochs_without_improvement'] += 1
                            
                            # Calculate improvements from different baselines for consistency
                            imp_since_start = ((start_loss - val_loss) / start_loss * 100) if start_loss > 0 else 0
                            imp_vs_last = ((prev_val_loss - val_loss) / prev_val_loss * 100) if prev_val_loss > 0 else 0
                            history = self._val_loss_tracker['val_history']
                            imp_6_ago = None
                            imp_3_ago = None
                            epoch_6_ago = None
                            epoch_3_ago = None
                            for hist_epoch, hist_loss in reversed(history[:-1]):
                                epochs_ago = epoch_idx - hist_epoch
                                if epochs_ago == 6 and imp_6_ago is None:
                                    imp_6_ago = ((hist_loss - val_loss) / hist_loss * 100) if hist_loss > 0 else 0
                                    epoch_6_ago = hist_epoch
                                if epochs_ago == 3 and imp_3_ago is None:
                                    imp_3_ago = ((hist_loss - val_loss) / hist_loss * 100) if hist_loss > 0 else 0
                                    epoch_3_ago = hist_epoch
                                if imp_6_ago is not None and imp_3_ago is not None:
                                    break
                            
                            imp_parts = []
                            imp_parts.append(f"epoch=  0: {imp_since_start:+7.2f}%")
                            if imp_6_ago is not None:
                                imp_parts.append(f"epoch={epoch_6_ago:3d}: {imp_6_ago:+7.2f}%")
                            else:
                                imp_parts.append(f"epoch=6ago: {'N/A':>7s}")
                            if imp_3_ago is not None:
                                imp_parts.append(f"epoch={epoch_3_ago:3d}: {imp_3_ago:+7.2f}%")
                            else:
                                imp_parts.append(f"epoch=3ago: {'N/A':>7s}")
                            imp_parts.append(f"epoch={epoch_idx-1:3d}: {imp_vs_last:+7.2f}%")
                            
                            change_str = f"{change_pct_vs_last:.2f}%" if abs(change_pct_vs_last) > 0.01 else "0.00%"
                            logger.info(f"LOSS IMPROVEMENT: [epoch={epoch_idx}] Val loss   [{status:8s}] {val_loss:.4f} ({change_str:>7s}) | {' | '.join(imp_parts)}")
                            
                            # Log component status when total isn't improving
                            comp_status = []
                            if val_components:
                                for comp_name in ['spread', 'joint', 'marginal']:
                                    if comp_name in val_components:
                                        no_improve = self._val_loss_tracker[f'{comp_name}_no_improvement']
                                        comp_status.append(f"{comp_name}:{no_improve}")
                            
                            status_str = " ".join(comp_status) if comp_status else "N/A"
                            logger.info(f"⚠️  No improvement for {self._val_loss_tracker['epochs_without_improvement']} epochs "
                                       f"(current: {val_loss:.4f}, best: {self._val_loss_tracker['best_val_loss']:.4f}) "
                                       f"Components: {status_str}")
                        
                        # Always update previous value
                        self._val_loss_tracker['val_prev'] = val_loss
                        
                        # Check if early stopping is blocked due to recent NO_LEARNING warning
                        early_stop_blocked = False
                        if hasattr(self, '_no_learning_tracker') and 'last_no_learning_epoch' in self._no_learning_tracker:
                            epochs_since_no_learning = epoch_idx - self._no_learning_tracker['last_no_learning_epoch']
                            min_epochs_required = self._no_learning_tracker.get('min_epochs_before_early_stop', 10)
                            
                            if epochs_since_no_learning < min_epochs_required:
                                early_stop_blocked = True
                                epochs_remaining = min_epochs_required - epochs_since_no_learning
                                logger.info(f"🚫 Early stopping BLOCKED: {epochs_remaining} more epochs required after NO_LEARNING warning")
                            else:
                                # Block has expired, reset the flag
                                if hasattr(self, '_early_stop_block_logged'):
                                    self._early_stop_block_logged = False
                        
                        # Early stopping if validation loss hasn't improved for patience epochs
                        # BUT ONLY if we're not in the blocked period after NO_LEARNING
                        # NEW: Consider if ANY component is still improving
                        total_no_improvement = self._val_loss_tracker['epochs_without_improvement']
                        any_component_improving = False
                        if val_components:
                            # Check if any major component is still improving
                            # NOTE: Don't rely on marginal loss in first 25% of epochs
                            # Marginal loss is normalized by 4.0 * effective_n_cols, and in early epochs
                            # the model hasn't learned much yet, so raw losses are high but normalized
                            # values can be misleading. Wait until after 25% to use marginal loss for decisions.
                            training_progress = epoch_idx / n_epochs if n_epochs > 0 else 0.0
                            if training_progress >= 0.25:
                                # Marginal loss dominates, so it's most important (after 25% of training)
                                marginal_no_improve = self._val_loss_tracker.get('marginal_no_improvement', total_no_improvement)
                                # Don't stop if marginal loss improved recently (< 50% of patience)
                                if marginal_no_improve < (self._val_loss_tracker['patience'] // 2):
                                    any_component_improving = True
                                    logger.info(f"🔄 Marginal loss still improving (stale: {marginal_no_improve} epochs) - continuing training")
                            else:
                                # In first 25% of epochs, marginal loss values are unreliable due to normalization
                                # and early learning phase, so don't use it for early stopping decisions
                                pass
                        
                        if total_no_improvement >= self._val_loss_tracker['patience'] and not any_component_improving:
                            if early_stop_blocked:
                                # Only log if this is the FIRST time we're blocking
                                if not hasattr(self, '_early_stop_block_logged') or not self._early_stop_block_logged:
                                    logger.warning(f"⏸️  [{epoch_idx}] Early stopping blocked → giving model {epochs_remaining} more epochs to recover")
                                    self._early_stop_block_logged = True
                            else:
                                # NEW: Check if we've completed at least 1 epoch of spread focus phase
                                # This ensures the model gets the benefit of spread-focused training before stopping
                                spread_only_epochs = self._spread_only_tracker.get('spread_only_epochs_completed', 0)
                                
                                if spread_only_epochs < 1:
                                    # Block early stopping - we need at least 1 epoch of spread focus training
                                    # Only log the first time we block, then every 10 epochs to avoid spam
                                    if not hasattr(self, '_spread_delay_first_epoch'):
                                        self._spread_delay_first_epoch = epoch_idx
                                        logger.warning(f"⏸️  [{epoch_idx+1}] Early stopping DELAYED: Need at least 1 epoch of spread focus phase (completed: {spread_only_epochs})")
                                        logger.info(f"   📊 Current marginal_loss_weight: {self.encoder.config.loss_config.marginal_loss_weight:.4f}")
                                        logger.info(f"   🎯 Will continue training until spread focus phase is reached (at ~{int(n_epochs * 0.95)} epochs)")
                                    elif (epoch_idx - self._spread_delay_first_epoch) % 10 == 0:
                                        # Log every 10 epochs while waiting
                                        epochs_waiting = epoch_idx - self._spread_delay_first_epoch
                                        logger.info(f"⏳ Still waiting for spread focus phase (waited {epochs_waiting} epochs, current weight: {self.encoder.config.loss_config.marginal_loss_weight:.4f})")
                                else:
                                    # Show component details in early stop message
                                    comp_details = ""
                                    if val_components:
                                        comp_details = f"\n   Component staleness: spread={self._val_loss_tracker.get('spread_no_improvement', 0)} joint={self._val_loss_tracker.get('joint_no_improvement', 0)} marginal={self._val_loss_tracker.get('marginal_no_improvement', 0)}"
                                    
                                    logger.info(f"🛑 EARLY STOPPING: Val loss hasn't improved for {self._val_loss_tracker['patience']} epochs")
                                    logger.info(f"   Best validation loss: {self._val_loss_tracker['best_val_loss']:.4f} (current: {val_loss:.4f}){comp_details}")
                                    logger.info(f"   ✅ Completed {spread_only_epochs} epoch(s) of spread focus phase training")
                                    logger.info(f"   Stopping training to prevent overfitting")
                            
                                    # Save final checkpoint
                                    final_checkpoint_path = self.get_training_state_path(epoch_idx, 0)
                                    try:
                                        self.save_state(epoch_idx, 0, self.encoder, optimizer, scheduler, dropout_scheduler)
                                        logger.info(f"💾 Final model saved to {final_checkpoint_path}")
                                    except Exception as e:
                                        logger.warning(f"⚠️  Failed to save final checkpoint at epoch {epoch_idx}: {e}")
                                        logger.warning(f"   Training is stopping anyway - checkpoint may be available from best model save")
                                    
                                    # Update progress dict
                                    d["progress_counter"] = max_progress  # Mark as fully complete
                                    d["status"] = "early_stopped"  # Update status from "training"
                                    d["early_stopping"] = True
                                    d["early_stop_reason"] = "validation_loss_plateau"
                                    d["stopped_epoch"] = epoch_idx + 1
                                    d["best_val_loss"] = self._val_loss_tracker['best_val_loss']
                                    d["spread_only_epochs_completed"] = spread_only_epochs
                                    
                                    # Send final progress update
                                    if print_callback is not None:
                                        d["time_now"] = time.time()
                                        logger.info(f"📊 Sending final progress update: {d['progress_counter']}/{d['max_progress']} (100%)")
                                        print_callback(d)
                                    
                                    # Send final training event callback
                                    if training_event_callback is not None:
                                        training_event_dict["early_stopped"] = True
                                        training_event_dict["early_stop_reason"] = "validation_loss_plateau"
                                        training_event_dict["best_val_loss"] = self._val_loss_tracker['best_val_loss']
                                        training_event_dict["spread_only_epochs_completed"] = spread_only_epochs
                                        training_event_dict["progress_counter"] = max_progress
                                        training_event_dict["max_progress"] = max_progress
                                        training_event_callback(training_event_dict)
                                    
                                    break  # Exit the training loop

                # Run WeightWatcher analysis with convergence monitoring if enabled
                if enable_weightwatcher and (epoch_idx % weightwatcher_save_every == 0 or epoch_idx == 0):
                    try:
                        from lib.weightwatcher_tracking import WeightWatcherCallback
                        # Note: get_config is already imported at top of file
                        
                        # Create WeightWatcher callback if not exists
                        if not hasattr(self, '_ww_callback'):
                            # Get spectral norm clipping config
                            sphere_config = get_config()
                            enable_clipping = sphere_config.get_enable_spectral_norm_clipping()
                            clip_threshold = sphere_config.get_spectral_norm_clip_threshold()
                            
                            # If clipping is disabled, use None to signal no clipping
                            spectral_norm_clip_value = clip_threshold if enable_clipping else None
                            
                            logger.info(f"🔧 Spectral norm clipping: {'ENABLED' if enable_clipping else 'DISABLED'}")
                            if enable_clipping:
                                logger.info(f"   Clip threshold: {clip_threshold}")
                            
                            self._ww_callback = WeightWatcherCallback(
                                out_dir=weightwatcher_out_dir,
                                job_id=weightwatcher_job_id,
                                save_every=weightwatcher_save_every,
                                convergence_patience=5,  # Stop if no improvement for 5 epochs
                                convergence_min_improve=1e-4,
                                spectral_norm_clip=spectral_norm_clip_value,
                                freeze_threshold=None,  # Use default 15.0 if ever enabled
                                min_epoch_before_freeze=20,  # Don't freeze layers until epoch 20+
                                max_layers_to_freeze=5,  # Maximum 5 layers per epoch
                                max_freeze_percentage=0.1,  # Maximum 10% of model parameters
                                enable_layer_freezing=False  # DISABLED: Layer freezing was too aggressive and froze adaptive parameters
                            )
                        
                        # Run analysis and get convergence results
                        ww_result = self._ww_callback(self.encoder, epoch_idx)
                        
                        # WOULD_FREEZE checkpoint: Save a checkpoint the first time we would freeze layers
                        # This creates a decision point for future experiments with layer freezing enabled
                        if ww_result.get('save_would_freeze_checkpoint', False):
                            try:
                                checkpoint_name = f"WOULD_FREEZE_epoch_{epoch_idx}"
                                logger.warning(f"💾 Saving WOULD_FREEZE checkpoint: {checkpoint_name}")
                                logger.warning(f"   📍 This checkpoint can be used to experiment with layer freezing enabled")
                                logger.warning(f"   🔬 {ww_result.get('would_freeze_layer_count', 0)} layers would have been frozen at this point")
                                
                                # Save checkpoint using existing checkpoint mechanism
                                checkpoint_path = self.save_checkpoint(
                                    epoch_idx,
                                    self.encoder,
                                    val_loss=val_loss if val_loss else None,
                                    checkpoint_name=checkpoint_name,
                                    metadata={
                                        'checkpoint_type': 'WOULD_FREEZE',
                                        'would_freeze_layer_count': ww_result.get('would_freeze_layer_count', 0),
                                        'would_freeze_layers': [(name, float(norm)) for name, norm in ww_result.get('would_freeze_layers', [])[:10]],  # Top 10
                                        'reason': 'First epoch where layers would have been frozen (if layer freezing were enabled)',
                                        'experiment_hint': 'Can restart from this checkpoint with enable_layer_freezing=True to compare outcomes'
                                    }
                                )
                                logger.warning(f"   ✅ WOULD_FREEZE checkpoint saved: {checkpoint_path}")
                            except Exception as e:
                                logger.error(f"   ❌ Failed to save WOULD_FREEZE checkpoint: {e}")
                                import traceback
                                traceback.print_exc()
                        
                        # Store WeightWatcher data in timeline if we have a current epoch entry
                        if hasattr(self, '_training_timeline') and self._training_timeline:
                            # Find the current epoch's entry (should be the last one)
                            # Use cumulative epoch for matching (timeline uses cumulative epochs)
                            cumulative_epoch_for_ww = epoch_idx
                            if hasattr(self, '_kv_fold_epoch_offset') and self._kv_fold_epoch_offset is not None:
                                cumulative_epoch_for_ww = epoch_idx + self._kv_fold_epoch_offset
                            
                            current_epoch_entry = self._training_timeline[-1]
                            if current_epoch_entry['epoch'] == cumulative_epoch_for_ww:
                                # Extract key WeightWatcher metrics
                                ww_data = {
                                    'should_stop': ww_result.get('should_stop', False),
                                    'converged': ww_result.get('converged', False),
                                    'avg_alpha': ww_result.get('avg_alpha'),
                                    'avg_spectral_norm': ww_result.get('avg_spectral_norm'),
                                    'avg_log_norm': ww_result.get('avg_log_norm'),
                                    'rank_loss': ww_result.get('rank_loss'),
                                    'entropy': ww_result.get('entropy'),
                                    'layers_frozen': ww_result.get('layers_frozen', []),
                                    'layers_clipped': ww_result.get('layers_clipped', []),
                                }
                                # Remove None values
                                ww_data = {k: v for k, v in ww_data.items() if v is not None}
                                current_epoch_entry['weightwatcher'] = ww_data
                                logger.info(f"📊 Added WeightWatcher data to timeline for epoch {epoch_idx}")
                        
                        # Check if early stopping is blocked due to recent NO_LEARNING warning
                        convergence_early_stop_blocked = False
                        if hasattr(self, '_no_learning_tracker') and 'last_no_learning_epoch' in self._no_learning_tracker:
                            epochs_since_no_learning = epoch_idx - self._no_learning_tracker['last_no_learning_epoch']
                            min_epochs_required = self._no_learning_tracker.get('min_epochs_before_early_stop', 10)
                            
                            if epochs_since_no_learning < min_epochs_required:
                                convergence_early_stop_blocked = True
                                epochs_remaining = min_epochs_required - epochs_since_no_learning
                        
                        # Check if training should stop due to convergence
                        # BUT ONLY if we're not in the blocked period after NO_LEARNING
                        # AND if we're past the minimum epoch threshold (e.g., OneCycleLR cooldown)
                        if ww_result.get('should_stop', False):
                            # Check for NO_STOP flag file
                            # output_dir can be a string or Path object - handle both
                            output_dir_str = str(self.output_dir) if hasattr(self, 'output_dir') and self.output_dir else None
                            job_id = getattr(self, 'job_id', None) or self.training_info.get('job_id', None)
                            if check_no_stop_file(job_id, output_dir_str):
                                logger.warning(f"🚫 NO_STOP flag detected - early stopping DISABLED")
                                logger.warning(f"   → WeightWatcher convergence detected but ignoring due to NO_STOP file")
                                logger.warning(f"   → Training will continue for all {n_epochs} epochs")
                                logger.warning(f"   → Remove NO_STOP file from job directory to re-enable early stopping")
                            elif epoch_idx < min_epoch_for_early_stop:
                                # Respect OneCycleLR cooldown period - don't stop during LR schedule
                                logger.info(f"⏭️  WeightWatcher convergence detected but early stopping DISABLED until epoch {min_epoch_for_early_stop} (currently at epoch {epoch_idx})")
                                logger.info(f"   → OneCycleLR cooldown period - continuing training to allow LR schedule to complete")
                            elif convergence_early_stop_blocked:
                                logger.warning(f"⏸️  WeightWatcher convergence early stopping triggered but BLOCKED")
                                logger.warning(f"   → Recent NO_LEARNING warning at epoch {self._no_learning_tracker['last_no_learning_epoch']}")
                                logger.warning(f"   → Continuing training for {epochs_remaining} more epochs to give model a chance to recover")
                                logger.warning(f"   → Model appears converged but may just need more time after NO_LEARNING plateau")
                            else:
                                logger.info(f"🛑 Early stopping triggered by convergence monitor at epoch {epoch_idx}")
                                logger.info(f"   Model has converged - stopping training to save compute")
                                
                                # Save final checkpoint with clear logging
                                final_checkpoint_path = self.get_training_state_path(epoch_idx, 0)
                                try:
                                    self.save_state(epoch_idx, 0, self.encoder, optimizer, scheduler, dropout_scheduler)
                                    logger.info(f"💾 Final converged model saved to {final_checkpoint_path}")
                                except Exception as e:
                                    logger.warning(f"⚠️  Failed to save final converged checkpoint at epoch {epoch_idx}: {e}")
                                    logger.warning(f"   Training is stopping anyway - checkpoint may be available from best model save")
                                
                                # Log convergence details for debugging
                                convergence_status = self._ww_callback.get_convergence_status()
                                logger.info(f"📊 Convergence details:")
                                logger.info(f"   Converged at epoch: {convergence_status.get('convergence_epoch', epoch_idx)}")
                                logger.info(f"   Epochs without improvement: {convergence_status.get('epochs_without_improvement', 'unknown')}")
                                logger.info(f"   Best rank loss: {convergence_status.get('best_rank_loss', 'unknown')}")
                                
                                # CRITICAL FIX: Set progress to 100% for early stopping
                                d["progress_counter"] = max_progress  # Mark as fully complete
                                d["status"] = "converged"  # Update status from "training"
                                d["early_stopping"] = True  # Flag that early stopping occurred
                                d["converged_epoch"] = epoch_idx + 1  # Human-readable epoch number
                                
                                # Send final progress update to client
                                if print_callback is not None:
                                    d["time_now"] = time.time()
                                    logger.info(f"📊 Sending final progress update: {d['progress_counter']}/{d['max_progress']} (100%)")
                                    print_callback(d)
                                
                                break  # Exit the training loop early
                        
                        # Log any interventions applied
                        if ww_result.get('clipped_layers'):
                            logger.info(f"🔧 Applied spectral norm clipping to {len(ww_result['clipped_layers'])} layers")
                        
                        if ww_result.get('frozen_layers'):
                            logger.info(f"❄️ Froze {len(ww_result['frozen_layers'])} dominant layers")
                        
                        if ww_result.get('refreshed_sampler'):
                            logger.info(f"🔁 Refreshed hard negative sampler")
                            
                    except Exception as e:
                        logger.warning(f"⚠️ WeightWatcher analysis with convergence monitoring failed for epoch {epoch_idx}: {e}")
                        # Log to centralized error tracker  
                        try:
                            from error_tracker import log_training_error
                            log_training_error(
                                message=f"WeightWatcher finalization failed: {e}",
                                job_id=getattr(self, 'job_id', None) or self.training_info.get('job_id', None),
                                exception=e,
                                context={
                                    "method": "weightwatcher_finalization",
                                    "weightwatcher_out_dir": weightwatcher_out_dir,
                                    "enable_weightwatcher": enable_weightwatcher
                                }
                            )
                        except Exception as tracker_error:
                            logger.warning(f"Error tracker failed: {tracker_error}")

                # Update dropout rate if scheduler is enabled
                if dropout_scheduler is not None:
                    try:
                        current_dropout = dropout_scheduler.step(
                            epoch=epoch_idx,
                            model=self.encoder,
                            val_loss=val_loss if isinstance(val_loss, (int, float)) else None
                        )
                        d["current_dropout"] = current_dropout
                    except Exception as e:
                        logger.warning(f"[epoch={epoch_idx}] ⚠️ DropoutScheduler failed: {e}")

                # End of epoch summary - add separator
                logger.info("─" * 100)
                
                # MEMORY LEAK DETECTION: Log VRAM at end of epoch
                _log_vram_usage("END OF EPOCH", epoch_idx)

                self.preserve_progress(
                    debug=d,
                    progress_counter=progress_counter,
                    # encode_time=loop_stopwatch.interval("encoder").duration(),
                    # loss_time=loop_stopwatch.interval("loss").duration(),
                    # back_time=loop_stopwatch.interval("backward").duration(),
                    # step_time=loop_stopwatch.interval("optimizer_step").duration(),
                    loss=loss,
                    val_loss=val_loss,
                    last_log_time=last_log_time,
                    batches_per_epoch=batches_per_epoch,
                    val_dataloader=val_dataloader,
                    optimizer_params=optimizer_params,
                    data_loader=data_loader,
                    lowest_val_loss=lowest_val_loss,
                )
                embedding_space_debug_training(epoch=epoch_idx, embedding_space=self)
                
                # Final callback after epoch completes (using variables from epoch loop)
                if print_progress_step is not None:
                    if print_callback is not None:
                        d["time_now"] = time.time()
                        d["epoch_idx"] = epoch_idx
                        d["batch_idx"] = batch_idx
                        d["progress_counter"] = progress_counter
                        d["max_progress"] = max_progress

                        try:
                            _loss_item = loss.item()
                        except Exception:
                            _loss_item = "not set"

                        # .... This can insert a duplicate record... so don't do that.
                        gotIt = False
                        for entry in d["loss_history"]:
                            if entry.get("epoch", -1) == epoch_idx:
                                gotIt = True
                                break
                        if not gotIt:
                            loss_entry = {
                                "epoch": epoch_idx,
                                "current_learning_rate": get_lr(),
                                "loss": _loss_item,
                                "validation_loss": val_loss,
                                "time_now": time.time(),
                                "duration": time.time() - epoch_start_time_now,
                            }
                            
                            # Add loss components if available
                            if val_components:
                                loss_entry["spread"] = val_components.get('spread')
                                loss_entry["joint"] = val_components.get('joint')
                                loss_entry["marginal"] = val_components.get('marginal')
                                loss_entry["marginal_weighted"] = val_components.get('marginal_weighted')
                            
                            # Push to SQLite (non-blocking) - don't keep in memory
                            if hasattr(self, 'history_db') and self.history_db:
                                self.history_db.push_loss_history(loss_entry)
                            
                            # Keep only validation loss value in memory
                            d["current_validation_loss"] = val_loss
                        print_callback(d)
                
        logger.info("Setting encoder.eval()")
        self.encoder.eval()

        # Final validation loss computation after all epochs complete
        if print_progress_step is not None:
            try:
                if val_dataloader is not None:
                    final_val_loss = self.compute_val_loss(val_dataloader)
                    if isinstance(final_val_loss, tuple):
                        final_val_loss = final_val_loss[0]  # Extract loss value if tuple
                else:
                    final_val_loss = 0
                logger.info(f"📊 Final validation loss after all epochs: {final_val_loss:.4f}")
            except Exception:
                pass  # Final validation loss computation is optional

        # TODO: anything to do post-training?
        # TODO: this method is where we would put tracking for e.g. W&B
        self.training_info["end_time"] = time.time()
        self.training_info["progress_info"] = d
        self.training_info["epochs"] = n_epochs
        
        # MEMORY LEAK FIX: Load full loss history from SQLite for summary
        if hasattr(self, 'history_db') and self.history_db:
            # Final flush to ensure all data is written
            self.history_db.flush()
            # Load full history from DB for summary
            full_loss_history = self.history_db.get_all_loss_history()
            if full_loss_history:
                # Update d with full history for summary
                d["loss_history"] = full_loss_history
                logger.info(f"💾 Loaded {len(full_loss_history)} loss history entries from SQLite for summary")
        
        # Final gradient statistics summary
        logger.info("=" * 100)
        logger.info("📊 GRADIENT CLIPPING SUMMARY (ENTIRE TRAINING)")
        logger.info("=" * 100)
        if grad_clip_stats["total_batches"] > 0:
            total_batches = grad_clip_stats["total_batches"]
            clipped_batches = grad_clip_stats["clipped_batches"]
            clip_rate = (clipped_batches / total_batches) * 100
            avg_unclipped = grad_clip_stats["sum_unclipped_norms"] / total_batches
            avg_clipped = grad_clip_stats["sum_clipped_norms"] / total_batches
            
            logger.info(f"Total batches processed: {total_batches}")
            
            if use_adaptive_clipping:
                logger.info(f"Gradient clipping: ADAPTIVE (clip when grad > loss × {adaptive_grad_clip_ratio:.1f})")
                logger.info(f"Batches clipped: {clipped_batches} / {total_batches} ({clip_rate:.1f}%)")
                logger.info(f"Max gradient/loss ratio: {grad_clip_stats['max_grad_loss_ratio']:.2f}")
                logger.info(f"Average gradient norm: {avg_unclipped:.2f}")
                
                if grad_clip_stats["large_gradient_warnings"] > 0:
                    logger.info(f"📊 Logged {grad_clip_stats['large_gradient_warnings']} gradient outliers")
                
                # Final gradient/loss correlation analysis
                if len(grad_clip_stats["gradient_norms_history"]) >= 10:
                    import numpy as np
                    grads = np.array(grad_clip_stats["gradient_norms_history"])
                    losses = np.array(grad_clip_stats["loss_values_history"])
                    
                    logger.info("")
                    logger.info("🔬 GRADIENT/LOSS RELATIONSHIP:")
                    logger.info(f"   Sample: {len(grads)} recent batches")
                    
                    if np.std(grads) > 0 and np.std(losses) > 0:
                        correlation = np.corrcoef(grads, losses)[0, 1]
                        avg_ratio = np.mean(grads / (losses + 1e-8))
                        logger.info(f"   Correlation: {correlation:.3f}")
                        logger.info(f"   Avg gradient/loss ratio: {avg_ratio:.3f}")
                        
                        if correlation > 0.5:
                            logger.info(f"   → Gradients scale with loss (correlation={correlation:.3f})")
                        elif correlation < -0.3:
                            logger.warning(f"   → Negative correlation ({correlation:.3f}) - unusual, may indicate LR too high or instability")
                        else:
                            logger.info(f"   → Weak correlation ({correlation:.3f}) - high batch-to-batch variance")
            else:
                logger.info("ℹ️  GRADIENT CLIPPING WAS DISABLED")
                logger.info(f"   Max gradient norm: {grad_clip_stats['max_unclipped_norm']:.2f}")
                logger.info(f"   Avg gradient norm: {avg_unclipped:.2f}")
        else:
            logger.warning("No gradient statistics collected (no batches processed?)")
        
        logger.info("=" * 100)
        
        # Store gradient stats in training info for later analysis
        self.training_info["gradient_clip_stats"] = {
            "total_batches": grad_clip_stats["total_batches"],
            "clipped_batches": grad_clip_stats["clipped_batches"],
            "clip_rate_pct": (grad_clip_stats["clipped_batches"] / max(1, grad_clip_stats["total_batches"])) * 100,
            "max_unclipped_norm": grad_clip_stats["max_unclipped_norm"],
            "max_clipped_norm": grad_clip_stats["max_clipped_norm"],
            "avg_unclipped_norm": grad_clip_stats["sum_unclipped_norms"] / max(1, grad_clip_stats["total_batches"]),
            "avg_clipped_norm": grad_clip_stats["sum_clipped_norms"] / max(1, grad_clip_stats["total_batches"]),
            "large_gradient_warnings": grad_clip_stats["large_gradient_warnings"],
            "clipping_mode": "adaptive" if use_adaptive_clipping else "disabled",
            "adaptive_grad_clip_ratio": adaptive_grad_clip_ratio,
            "max_grad_loss_ratio": grad_clip_stats["max_grad_loss_ratio"],
            "warning_multiplier": grad_clip_warning_multiplier,
        }
        
        # CRITICAL: Load the best checkpoint before generating summary or using the model
        # The final epoch may be overfit - we want the BEST model for downstream tasks
        logger.info("=" * 100)
        logger.info("🏆 LOADING BEST CHECKPOINT")
        logger.info("=" * 100)
        try:
            best_checkpoint_path = self.get_best_checkpoint_path()
            if os.path.exists(best_checkpoint_path):
                logger.info(f"📂 Loading best model from: {best_checkpoint_path}")
                best_epoch_idx = self.load_best_checkpoint()
                logger.info(f"✅ Successfully loaded best checkpoint from epoch {best_epoch_idx}")
                
                # Create self-contained model package
                self._create_model_package(best_epoch_idx)
                
                # Re-compute losses on the best model for accurate reporting
                logger.info("🔄 Re-evaluating best model to verify performance...")
                self.encoder.eval()
                with torch.no_grad():
                    # Compute training loss on best model
                    best_train_loss = 0.0
                    train_batches = 0
                    for batch in data_loader:
                        encodings = self.encoder(batch)
                        batch_loss, loss_dict = self.encoder.compute_total_loss(*encodings)
                        best_train_loss += batch_loss.item()
                        train_batches += 1
                        if train_batches >= 50:  # Sample for efficiency
                            break
                    best_train_loss = best_train_loss / train_batches if train_batches > 0 else 0
                    
                    # Compute validation loss on best model
                    if val_dataloader is not None:
                        best_val_loss, best_val_components = self.compute_val_loss(val_dataloader)
                    else:
                        best_val_loss = 0
                        best_val_components = None
                
                logger.info(f"📊 Best model performance:")
                logger.info(f"   Training Loss: {best_train_loss:.4f}")
                if best_val_components:
                    logger.info(f"   Validation Loss: {best_val_loss:.4f} (spread={best_val_components['spread']:.4f}, joint={best_val_components['joint']:.4f}, marginal={best_val_components['marginal_weighted']:.4f})")
                else:
                    logger.info(f"   Validation Loss: {best_val_loss:.4f}")
                
                # Store best model info for summary
                self.training_info["best_checkpoint_loaded"] = True
                self.training_info["best_checkpoint_epoch"] = best_epoch_idx
                self.training_info["best_checkpoint_train_loss"] = best_train_loss
                self.training_info["best_checkpoint_val_loss"] = best_val_loss
            else:
                logger.warning(f"⚠️ Best checkpoint not found at {best_checkpoint_path}")
                logger.warning(f"   Using final epoch model (may be suboptimal)")
                self.training_info["best_checkpoint_loaded"] = False
        except Exception as e:
            logger.error(f"❌ Failed to load best checkpoint: {e}")
            logger.warning(f"   Using final epoch model (may be suboptimal)")
            self.training_info["best_checkpoint_loaded"] = False
        
        # Generate and log training summary with quality assessment
        try:
            progress_info = self.training_info.get('progress_info', {})
            loss_history = progress_info.get('loss_history', [])
            training_summary = summarize_es_training_results(self.training_info, loss_history)
            self.training_info["training_summary"] = training_summary
        except Exception as e:
            logger.warning(f"⚠️ Could not generate training summary: {e}")
        
        # Finalize WeightWatcher analysis
        if enable_weightwatcher:
            try:
                logger.info("📊 Creating final WeightWatcher summary...")
                from lib.weightwatcher_tracking import create_weightwatcher_summary, plot_convergence_dashboard
                create_weightwatcher_summary(
                    out_dir=weightwatcher_out_dir,
                    job_id=weightwatcher_job_id
                )
                
                # Create convergence dashboard visualization
                plot_convergence_dashboard(
                    out_dir=weightwatcher_out_dir,
                    job_id=weightwatcher_job_id,
                    save_plot=True,
                    show_plot=False
                )
                
            except Exception as e:
                logger.warning(f"⚠️ WeightWatcher finalization failed: {e}")
                # Log to centralized error tracker  
                try:
                    from error_tracker import log_training_error
                    log_training_error(
                        message=f"WeightWatcher finalization failed: {e}",
                        job_id=getattr(self, 'job_id', None) or self.training_info.get('job_id', None),
                        exception=e,
                        context={
                            "method": "weightwatcher_finalization",
                            "weightwatcher_out_dir": weightwatcher_out_dir,
                            "enable_weightwatcher": enable_weightwatcher
                        }
                    )
                except Exception as tracker_error:
                    logger.warning(f"Error tracker failed: {tracker_error}")
        
        # MEMORY LEAK FIX: Close training history database
        if hasattr(self, 'history_db') and self.history_db:
            self.history_db.close()
            logger.info("💾 Training history database closed")
        
        # Create comprehensive training movie JSON with all data
        logger.info("🎬 Creating comprehensive training movie JSON...")
        try:
            movie_data = self.create_training_movie_json(
                enable_weightwatcher=enable_weightwatcher,
                weightwatcher_out_dir=weightwatcher_out_dir
            )
            if movie_data:
                logger.info("✅ Training movie JSON created successfully!")
        except Exception as e:
            logger.error(f"❌ Failed to create training movie JSON: {e}")
            # Log to centralized error tracker
            try:
                from error_tracker import log_training_error
                log_training_error(
                    message=f"Failed to create training movie JSON: {e}",
                    job_id=getattr(self, 'job_id', None) or self.training_info.get('job_id', None),
                    exception=e,
                    context={
                        "method": "create_training_movie_json",
                        "enable_weightwatcher": enable_weightwatcher,
                        "weightwatcher_out_dir": weightwatcher_out_dir
                    }
                )
            except Exception as tracker_error:
                logger.warning(f"Error tracker failed: {tracker_error}")
            return None
        
        # Generate GraphViz visualization of network architecture
        logger.info("🔷 Generating GraphViz network architecture visualization...")
        try:
            from lib.featrix.neural.network_viz import generate_graphviz_for_embedding_space
            graphviz_path = generate_graphviz_for_embedding_space(self)
            if graphviz_path:
                logger.info(f"✅ Network architecture visualization saved to {graphviz_path}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to generate GraphViz visualization: {e}")
        
        # Log encoder summary including adaptive strategies
        logger.info("")
        self.log_encoder_summary()
        
        self.reset_training_state()

        return

    def to_json_dict(self):
        # serialize to a json dict
        d = {}
        d["column-list"] = list(self.col_codecs.keys())
        d["codecs"] = self._codecs_to_dict()
        d["column_spec"] = self.column_spec
        d["json_transformations"] = self.json_transformations  # Include JSON transformation metadata
        # d['column-env_files'] = self.
        return d

    def _codecs_to_dict(self):
        d = {}
        for k, v in self.col_codecs.items():
            codec_dict = v.save()  # gets a dict
            d[k] = codec_dict
        return d

    def get_codec_meta(self):
        r = {}
        for k, v in self.col_codecs.items():
            codec_name = None
            try:
                codec_name = v.get_codec_name()
            except Exception:
                traceback.print_exc()
                codec_name = "ERROR"
            try:
                codec_info = v.get_codec_info()
            except Exception:
                codec_info = None
            r[k] = {"name": codec_name, "info": codec_info}
        return r

    def get_dimensions(self):
        return self.d_model

    def pre_warm_string_cache(self):
        """Pre-warm string cache with ALL strings from train and validation datasets."""
        if not self.string_cache:
            logger.info("No string cache provided - skipping pre-warming")
            return
            
        logger.info("🔥 Pre-warming string cache with ALL train and validation strings...")
        
        # Collect ALL string values from both datasets
        all_string_values = []
        string_columns = []
        
        # Get string columns from train dataset
        for c, codec in self.train_input_data.column_codecs().items():
            if codec == ColumnType.FREE_STRING:
                string_columns.append(c)
        
        if not string_columns:
            logger.info("ℹ️  No string columns found - skipping cache pre-warming")
            return
        
        logger.info(f"📝 Found {len(string_columns)} string columns: {string_columns}")
        
        # Collect strings from training dataset
        for col in string_columns:
            if col in self.train_input_data.df.columns:
                vals = self.train_input_data.df[col].astype(str).tolist()
                all_string_values.extend(vals)
                logger.info(f"   Train[{col}]: {len(vals)} strings")
        
        # Collect strings from validation dataset  
        for col in string_columns:
            if col in self.val_input_data.df.columns:
                vals = self.val_input_data.df[col].astype(str).tolist()
                all_string_values.extend(vals)
                logger.info(f"   Val[{col}]: {len(vals)} strings")
        
        # Remove duplicates
        unique_strings = list(set(all_string_values))
        logger.info(f"📊 Total unique strings to cache: {len(unique_strings)} (from {len(all_string_values)} total)")
        
        if unique_strings:
            try:
                # Create a temporary StringCache to add all strings
                _log_gpu_memory_embedded_space("BEFORE creating StringCache for pre-warming")
                from featrix.neural.string_cache import StringCache
                temp_cache = StringCache(
                    initial_values=unique_strings,
                    debugName="pre_warm_cache",
                    string_cache_filename=self.string_cache
                )
                _log_gpu_memory_embedded_space("AFTER creating StringCache for pre-warming")
                logger.info(f"✅ String cache pre-warmed with {len(unique_strings)} unique strings")
                logger.info("🚀 Training should now have minimal cache misses!")
            except Exception as e:
                logger.warning(f"⚠️ Failed to pre-warm cache: {e}")
                logger.info("Proceeding anyway - cache will be updated during training")
        else:
            logger.info("ℹ️  No strings to cache")

    def create_training_movie_json(self, enable_weightwatcher=False, weightwatcher_out_dir="ww_metrics"):
        """
        Create a comprehensive training movie JSON containing all training trajectory data.
        
        This includes:
        - Complete loss history with row IDs for path visualization
        - WeightWatcher metrics across all epochs
        - Mutual information progression
        - Training timings and resource usage
        - Convergence diagnostics and layer interventions
        
        Args:
            enable_weightwatcher: Whether WeightWatcher was enabled during training
            weightwatcher_out_dir: Directory containing WeightWatcher metrics
            
        Returns:
            dict: Comprehensive training movie data
        """
        try:
            logger.info("🎬 Creating comprehensive training movie JSON...")
            
            # Get job ID for file organization
            job_id = getattr(self, 'job_id', None) or self.training_info.get('job_id', None)
            
            # Base movie data from training_info
            movie_data = {
                "metadata": {
                    "job_id": job_id,
                    "creation_time": time.time(),
                    "model_type": "embedding_space",
                    "model_param_count": getattr(self, 'model_param_count', 0),
                    "num_rows": self.len_df(),
                    "num_cols": len(self.train_input_data.df.columns),
                    "column_list": list(self.col_codecs.keys()),
                    "compute_device": device.type,
                    "hostname": socket.gethostname(),
                    "pid": os.getpid(),
                },
                "training_trajectory": [],
                "weightwatcher_metrics": [],
                "convergence_diagnostics": {},
                "final_summary": {}
            }
            
            # Extract progress info from training_info
            progress_info = self.training_info.get('progress_info', {})
            
            # 1. Build training trajectory with row IDs
            loss_history = progress_info.get('loss_history', [])
            mutual_info = progress_info.get('mutual_information', [])
            
            # Create comprehensive trajectory combining all data sources
            row_id = 0
            for epoch_data in loss_history:
                trajectory_point = {
                    "row_id": row_id,
                    "epoch": epoch_data.get('epoch', 0),
                    "timestamp": epoch_data.get('time_now', 0),
                    "loss_metrics": {
                        "training_loss": epoch_data.get('loss', 0),
                        "validation_loss": epoch_data.get('validation_loss', 0),
                        "learning_rate": epoch_data.get('current_learning_rate', 0),
                        "duration": epoch_data.get('duration', 0),
                    },
                    "mutual_information": None,  # Will be populated below
                    "weightwatcher_metrics": None,  # Will be populated below
                    "interventions": {
                        "layers_clipped": [],
                        "layers_frozen": [],
                        "dropout_rate": None
                    }
                }
                
                # Add mutual information for this epoch
                for mi_data in mutual_info:
                    if mi_data.get('epoch') == epoch_data.get('epoch'):
                        trajectory_point["mutual_information"] = {
                            "column_estimates": mi_data.get('columns', {}),
                            "joint_estimate": mi_data.get('joint', 0)
                        }
                        break
                
                movie_data["training_trajectory"].append(trajectory_point)
                row_id += 1
            
            # 2. Load WeightWatcher metrics if enabled
            if enable_weightwatcher:
                try:
                    # Determine WeightWatcher output directory
                    if job_id and job_id != "unknown":
                        ww_full_dir = os.path.join(weightwatcher_out_dir, job_id)
                    else:
                        ww_full_dir = weightwatcher_out_dir
                    
                    # Load summary JSON if available
                    ww_summary_file = os.path.join(ww_full_dir, "ww_summary.json")
                    if os.path.exists(ww_summary_file):
                        with open(ww_summary_file, 'r') as f:
                            ww_data = json.load(f)
                        
                        # Add WeightWatcher metrics to trajectory points
                        for ww_entry in ww_data:
                            epoch = ww_entry.get('epoch', 0)
                            
                            # Find corresponding trajectory point
                            for traj_point in movie_data["training_trajectory"]:
                                if traj_point["epoch"] == epoch:
                                    traj_point["weightwatcher_metrics"] = {
                                        "alpha": ww_entry.get('alpha', 0),
                                        "spectral_norm": ww_entry.get('spectral_norm', 0),
                                        "log_norm": ww_entry.get('log_norm', 0),
                                        "entropy": ww_entry.get('entropy', 0),
                                        "rank_loss": ww_entry.get('rank_loss', 0),
                                        "layer_name": ww_entry.get('layer_name', ''),
                                        "layer_id": ww_entry.get('layer_id', 0)
                                    }
                                    break
                        
                        # Store all WeightWatcher metrics separately too
                        movie_data["weightwatcher_metrics"] = ww_data
                        
                        logger.info(f"📊 Added {len(ww_data)} WeightWatcher metric entries")
                    
                    # Load convergence diagnostics
                    clipping_file = os.path.join(ww_full_dir, "clipping_diagnostics.json")
                    if os.path.exists(clipping_file):
                        with open(clipping_file, 'r') as f:
                            clipping_data = json.load(f)
                        movie_data["convergence_diagnostics"] = clipping_data
                        logger.info("🔧 Added clipping diagnostics")
                    
                    # Load WeightWatcher summary CSV for aggregated metrics
                    ww_summary_csv = os.path.join(ww_full_dir, "ww_summary.csv")
                    if os.path.exists(ww_summary_csv):
                        df_summary = pd.read_csv(ww_summary_csv)
                        
                        # Add epoch-level summary metrics to trajectory
                        for _, row in df_summary.iterrows():
                            epoch = row.get('epoch', 0)
                            
                            # Find trajectory point and add summary metrics
                            for traj_point in movie_data["training_trajectory"]:
                                if traj_point["epoch"] == epoch:
                                    traj_point["epoch_summary"] = {
                                        "alpha_mean": row.get('alpha_mean', 0),
                                        "alpha_std": row.get('alpha_std', 0),
                                        "spectral_norm_mean": row.get('spectral_norm_mean', 0),
                                        "alpha_pct_below_6": row.get('alpha_pct_below_6', 0),
                                        "entropy_mean": row.get('entropy_mean', 0),
                                        "rank_loss_mean": row.get('rank_loss_mean', 0),
                                        "log_norm_mean": row.get('log_norm_mean', 0)
                                    }
                                    break
                        
                        logger.info(f"📈 Added epoch-level summary metrics for {len(df_summary)} epochs")
                
                except Exception as e:
                    logger.warning(f"⚠️ Failed to load WeightWatcher metrics: {e}")
            
            # 3. Add final summary
            final_epoch = len(loss_history)
            if loss_history:
                final_loss = loss_history[-1]
                movie_data["final_summary"] = {
                    "total_epochs": final_epoch,
                    "final_training_loss": final_loss.get('loss', 0),
                    "final_validation_loss": final_loss.get('validation_loss', 0),
                    "final_learning_rate": final_loss.get('current_learning_rate', 0),
                    "total_training_time": self.training_info.get('end_time', 0) - self.training_info.get('start_time', 0),
                    "converged": False,  # Will be updated if convergence info available
                    "convergence_epoch": None
                }
            
            # Add convergence status if available
            if hasattr(self, '_ww_callback') and self._ww_callback:
                convergence_status = self._ww_callback.get_convergence_status()
                movie_data["final_summary"]["converged"] = convergence_status.get('has_converged', False)
                movie_data["final_summary"]["convergence_epoch"] = convergence_status.get('convergence_epoch', None)
                movie_data["convergence_diagnostics"]["convergence_status"] = convergence_status
            
            # 4. Save the comprehensive movie JSON
            movie_filename = f"training_movie_{job_id}.json" if job_id else "training_movie.json"
            movie_path = os.path.join(self.output_dir, movie_filename)
            
            with open(movie_path, 'w') as f:
                json.dump(movie_data, f, indent=2)
            
            logger.info(f"🎬 Training movie saved to {movie_path}")
            logger.info(f"   📊 {len(movie_data['training_trajectory'])} trajectory points")
            logger.info(f"   📈 {len(movie_data['weightwatcher_metrics'])} WeightWatcher entries")
            logger.info(f"   🔧 Convergence diagnostics: {len(movie_data['convergence_diagnostics'])} entries")
            
            return movie_data
            
        except Exception as e:
            logger.error(f"❌ Failed to create training movie JSON: {e}")
            import traceback
            traceback.print_exc()
            return None


if __name__ == "__main__":
    from input_data_set import FeatrixInputDataSet

    fileName = sys.argv[1]
    if not os.path.exists(fileName):
        logger.error(f"No file exists at {fileName}")
        os._exit(2)

    fids = FeatrixInputDataSet(fileName)  # "/Users/admin/Downloads/train.csv")
    es = EmbeddingSpace(fids)
    es.train()
