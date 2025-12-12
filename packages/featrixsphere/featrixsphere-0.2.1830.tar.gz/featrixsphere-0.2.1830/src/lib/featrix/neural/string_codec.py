#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import base64
import hashlib
import io
import logging
import math
import traceback

import numpy as np
import torch
import torch.nn as nn


# Import logging configuration FIRST to ensure timestamps
from featrix.neural.logging_config import configure_logging
configure_logging()

from featrix.neural.device import device
from featrix.neural.featrix_token import set_not_present
from featrix.neural.featrix_token import Token
from featrix.neural.featrix_token import TokenStatus
from featrix.neural.model_config import ColumnType
from featrix.neural.model_config import SimpleMLPConfig
from featrix.neural.model_config import StringEncoderConfig
from featrix.neural.simple_mlp import SimpleMLP
from featrix.neural.string_cache import StringCache
from featrix.neural.sphere_config import get_config

logger = logging.getLogger(__name__)

torch.set_printoptions(threshold=10_000)
torch.set_printoptions(profile="full")
torch.set_printoptions(linewidth=240)

# from .exceptions import NaNModelCollapseException


import os
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
        
string_server_client = None

# Removed sentence transformer device caching - no longer needed

# Main process PID - set once at module import time, never updated across spawn/fork
# This allows us to detect if we're in a spawned/forked worker process
_main_pid = os.getpid()

# CRITICAL: Workers must use CPU to avoid VRAM waste
# Each worker would allocate ~600MB VRAM for sentence model
# With 8 workers, that's 4.8GB wasted!

def _init_string_server_client():
    """
    Initialize the string server client with automatic fallback.
    
    The client handles its own URL resolution and fallback:
    - Primary: http://taco.local:9000 (direct to string server)
    - Fallback: https://sphere-api.featrix.com/strings/* (proxy endpoints)
    """
    global string_server_client
    
    if string_server_client is not None:
        return string_server_client
    
    try:
        from featrix_string_server_client import StringServerClient
        # Use client defaults - it handles taco.local -> sphere-api fallback automatically
        string_server_client = StringServerClient()
        logger.info("✅ Initialized string server client with automatic fallback (taco.local:9000 -> sphere-api.featrix.com)")
        return string_server_client
    except ImportError:
        logger.warning("⚠️  featrix-string-server-client not installed, falling back to local model")
        return None
    except Exception as e:
        logger.warning(f"⚠️  Failed to initialize string server client: {e}, falling back to local model")
        return None

def _is_worker_process():
    """
    Detect if we're in a PyTorch DataLoader worker process.
    
    CRITICAL: This must ONLY detect PyTorch DataLoader workers, NOT Celery workers or other forked processes.
    Celery workers CAN and MUST load the sentence model to build string caches.
    
    ONLY checks the PYTORCH_DATALOADER_WORKER environment variable.
    This is set by worker_init_fn in dataloader_utils.py when PyTorch DataLoader workers are spawned.
    """
    # ONLY check environment variable - this is the ONLY reliable way
    # Celery workers do NOT have this set, so they will return False
    return os.environ.get('PYTORCH_DATALOADER_WORKER') == '1'

def _log_gpu_memory_string_codec(context: str = ""):
    """Quick GPU memory logging for tracing memory usage in string_codec."""
    try:
        if not torch.cuda.is_available():
            return
        allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
        reserved = torch.cuda.memory_reserved() / (1024**3)  # GB
        max_allocated = torch.cuda.max_memory_allocated() / (1024**3)  # GB
        logger.debug(f"📊 GPU MEMORY [string_codec: {context}]: Allocated={allocated:.3f} GB, Reserved={reserved:.3f} GB, Peak={max_allocated:.3f} GB")
    except Exception as e:
        logger.debug(f"Could not log GPU memory: {e}")

# Removed _get_sentence_device() and _loadModelIfNeeded() - no longer needed
# String server client handles all encoding now

STRING_DIM = 384

class StringEncoder(nn.Module):
    def __init__(self, config: StringEncoderConfig, column_name=None):
        super().__init__()

        self.config = config
        self.column_name = column_name  # Store column name for logging

        # ADAPTIVE MIXTURE: Create multiple MLP paths with different compression levels
        # Similar to AdaptiveScalarEncoder's mixture of transformations
        # We'll create 5 compression strategies including ZERO and DELIMITER handling
        d_model = config.d_model if config.d_model is not None else config.d_out
        
        # Define the compression strategies
        # Note: We don't go > d_model - no need to expand beyond target dimension
        self.compression_levels = [
            ("ZERO", 0),                     # Zero contribution - for random/uninformative strings
            ("DELIMITER", -1),               # Special: BERT-aware pass-through for delimited text
            ("AGGRESSIVE", d_model // 4),   # Heavy compression (1/4 capacity)
            ("MODERATE", d_model // 2),     # Medium compression (1/2 capacity)
            ("STANDARD", d_model),           # Match d_model exactly (full capacity)
        ]
        
        # Create separate MLP encoders for each compression level
        self.mlp_encoders = nn.ModuleList()
        for strategy_name, d_out_strategy in self.compression_levels:
            if d_out_strategy == 0:
                # ZERO strategy: no MLP needed, will output zeros
                self.mlp_encoders.append(None)
            elif d_out_strategy == -1:
                # DELIMITER strategy: special handling in forward(), no MLP needed here
                # We'll split the input embedding and average (happens in forward pass)
                self.mlp_encoders.append(None)
            else:
                # Create a config for this specific compression level
                strategy_config = StringEncoderConfig(
                    d_in=config.d_in,
                    d_out=d_out_strategy,
                    d_model=None,  # Don't project yet - we'll do it after mixing
                    normalize=False,  # Don't normalize yet - we'll do it after mixing
                    n_hidden_layers=config.n_hidden_layers,
                    d_hidden=config.d_hidden,
                )
                mlp = SimpleMLP(strategy_config)
                
                # WARM START: Initialize MLP to better preserve BERT embedding structure
                self._warm_start_mlp_from_bert(mlp, config.d_in)
                
                self.mlp_encoders.append(mlp)
        
        # Learnable weights to select among compression strategies
        # Initialize with small random values (not zeros) to break symmetry
        self.strategy_logits = nn.Parameter(torch.randn(len(self.compression_levels)) * 0.1)
        
        # CRITICAL FIX: Replacement embedding needs to match d_model (output size after mixing)
        self._replacement_embedding = nn.Parameter(torch.zeros(d_model))
        nn.init.normal_(self._replacement_embedding, mean=0.0, std=0.01)
        
        # Final projection: all strategies project to d_model for mixing
        self.strategy_projections = nn.ModuleList()
        for strategy_name, d_out_strategy in self.compression_levels:
            if d_out_strategy == 0:
                # ZERO strategy: no projection needed (outputs zeros directly)
                proj = None
            elif d_out_strategy == -1:
                # DELIMITER strategy: operates on BERT embeddings, project from STRING_DIM to d_model
                proj = nn.Linear(STRING_DIM, d_model, bias=False)
                nn.init.xavier_uniform_(proj.weight, gain=1.0)
            elif d_out_strategy != d_model:
                proj = nn.Linear(d_out_strategy, d_model, bias=False)
                nn.init.xavier_uniform_(proj.weight, gain=1.0)
            else:
                proj = None  # No projection needed
            self.strategy_projections.append(proj)
        
        logger.info(f"🎯 AdaptiveStringEncoder: {len(self.compression_levels)} compression strategies")
        for i, (name, d_out) in enumerate(self.compression_levels):
            if d_out == 0:
                logger.info(f"   Strategy {i}: {name:12s} ZERO (learns to ignore random/uninformative text)")
            elif d_out == -1:
                logger.info(f"   Strategy {i}: {name:12s} DELIMITER (splits & averages for 'A,B,C' or 'X-Y' patterns)")
            else:
                logger.info(f"   Strategy {i}: {name:12s} d_out={d_out:4d} → d_model={d_model}")
        
        self.needs_projection = False  # We handle projection internally now
        self.final_projection = None
        
        # STRATEGY PRUNING: Track training progress for top-K selection
        self.register_buffer('_epoch_counter', torch.tensor(0, dtype=torch.long))
        self.register_buffer('_total_epochs', torch.tensor(100, dtype=torch.long))  # Will be updated
        self.register_buffer('_pruned_mask', torch.ones(len(self.compression_levels), dtype=torch.float32))
        self.register_buffer('_last_logged_epoch', torch.tensor(-1, dtype=torch.long))  # Track last logged epoch to avoid batch spam
        self._pruning_enabled = False
        self._top_k = 2  # Keep top 2 strategies after warmup
    
    def _warm_start_mlp_from_bert(self, mlp, d_in):
        """
        Warm start MLP layers to better preserve BERT embedding structure.
        
        Strategy:
        - First layer: Initialize to approximate identity mapping (preserve BERT structure)
        - Subsequent layers: Use standard initialization
        - This helps the network start closer to the BERT embedding space
        """
        layers = list(mlp.modules())
        first_linear = None
        
        # Find the first Linear layer
        for module in mlp.modules():
            if isinstance(module, nn.Linear):
                first_linear = module
                break
        
        if first_linear is not None:
            # Initialize first layer to preserve more of the input structure
            # Use smaller weights to start closer to identity-like behavior
            with torch.no_grad():
                # Initialize weights with smaller variance (more conservative)
                # This helps preserve BERT embedding structure initially
                nn.init.normal_(first_linear.weight, mean=0.0, std=0.02)  # Smaller std than xavier
                
                # Initialize bias to zero (already done, but be explicit)
                if first_linear.bias is not None:
                    nn.init.zeros_(first_linear.bias)
            
            # Initialize remaining layers with standard xavier
            found_first = False
            for name, param in mlp.named_parameters():
                if 'weight' in name and param.ndim >= 2:
                    if not found_first:
                        found_first = True  # Skip first layer (already initialized)
                        continue
                    nn.init.xavier_uniform_(param, gain=0.5)
                elif 'bias' in name:
                    if not found_first:
                        found_first = True
                        continue
                    nn.init.zeros_(param)
        else:
            # Fallback: standard initialization if no Linear layer found
            for name, param in mlp.named_parameters():
                if 'weight' in name and param.ndim >= 2:
                    nn.init.xavier_uniform_(param, gain=0.5)
                elif 'bias' in name:
                    nn.init.zeros_(param)

    @property
    def unknown_embedding(self):
        # Replacement embedding is already at d_model size
        emb = nn.functional.normalize(self._replacement_embedding, dim=-1)
        return emb

    @property
    def marginal_embedding(self):
        # We return the same vector as NOT_PRESENT token because they are treated the
        # same from a probabilistic point of view by the network, and should be treated
        # the same when the model is queried.
        # However, they must remain distinct tokens because the masking strategy for the loss
        # function is affected by whether a field is NOT_PRESENT, or MARGINAL.
        emb = nn.functional.normalize(self._replacement_embedding, dim=-1)
        return emb

    @property
    def not_present_embedding(self):
        emb = nn.functional.normalize(self._replacement_embedding, dim=-1)
        return emb

    def forward(self, token):
        # token.value can be:
        # - [STRING_DIM] for single token (will be batched by DataLoader)
        # - [batch_size, STRING_DIM] for already-batched tokens
        # After learned projection: BERT [384] + features [32] → [384]
        # Both are valid! Just pass through.
        
        # FORCE conversion to float32 if we get int64
        value = token.value
        if value.dtype == torch.int64:
            value = value.to(dtype=torch.float32)
        
        # CRITICAL: Ensure value is on the same device as module parameters
        # This fixes device mismatch errors where token.value is on CPU but module is on CUDA
        # Respect FEATRIX_FORCE_CPU_SINGLE_PREDICTOR env var - force CPU if set
        force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
        
        # Get device from first available parameter (projection, mlp, or strategy_logits)
        module_device = None
        if not force_cpu:
            # Only detect module device if not forcing CPU
            # Try to get device from a projection layer
            for proj in self.strategy_projections:
                if proj is not None:
                    try:
                        module_device = next(proj.parameters()).device
                        break
                    except (StopIteration, AttributeError):
                        continue
            # If no projection found, try MLP encoders
            if module_device is None:
                for mlp in self.mlp_encoders:
                    if mlp is not None:
                        try:
                            module_device = next(mlp.parameters()).device
                            break
                        except (StopIteration, AttributeError):
                            continue
            # Fallback to strategy_logits
            if module_device is None and self.strategy_logits is not None:
                module_device = self.strategy_logits.device
        
        # Force CPU mode if env var is set
        if force_cpu:
            module_device = torch.device('cpu')
            # Also ensure module is on CPU (defensive - in case it wasn't moved earlier)
            if list(self.parameters()):
                first_param_device = next(self.parameters()).device
                if first_param_device.type != 'cpu':
                    self.cpu()
        # If not forcing CPU and no device detected, try to use CUDA if available
        elif module_device is None and torch.cuda.is_available():
            # Try to detect device from any parameter in the module
            if list(self.parameters()):
                module_device = next(self.parameters()).device
        
        # Move value to module device if there's a mismatch
        if module_device is not None and value.device != module_device:
            original_device = value.device
            value = value.to(device=module_device)
            # Log once per encoder instance to avoid spam
            if not hasattr(self, '_device_move_logged'):
                logger.debug(f"StringEncoder '{self.column_name or 'unknown'}': Moved token.value from {original_device} to {module_device} (force_cpu={force_cpu})")
                self._device_move_logged = True
        
        # Validate it's a tensor with correct dtype
        assert hasattr(value, 'dtype'), f"StringEncoder received non-tensor token.value: {type(value)}"
        assert value.dtype == torch.float32, f"StringEncoder received {value.dtype} token.value, expected float32. Shape: {value.shape}"
        
        # CRITICAL FIX: Validate and clamp input values to prevent NaN propagation
        # Check for NaN/Inf in inputs and replace with zeros
        if torch.isnan(value).any() or torch.isinf(value).any():
            nan_mask = torch.isnan(value) | torch.isinf(value)
            nan_count = nan_mask.sum().item()
            value = torch.where(nan_mask, torch.zeros_like(value), value)
            # Log warning (but not too verbose)
            if not hasattr(self, '_nan_warning_logged'):
                logger.warning(f"⚠️  StringEncoder: Detected and replaced {nan_count} NaN/Inf values in input")
                logger.warning(f"   Input shape: {value.shape}, token status: {token.status[:5] if hasattr(token.status, '__getitem__') else token.status}")
                self._nan_warning_logged = True
        
        # Clamp extreme values to reasonable range to prevent gradient explosion
        value = torch.clamp(value, min=-100.0, max=100.0)
        
        # Create new token with modified value (Token.value is read-only)
        # Always create new token to ensure device consistency
        token = Token(
            value=value,
            status=token.status,
            attention_mask=token.attention_mask if hasattr(token, 'attention_mask') else None
        )
        
        # ADAPTIVE MIXTURE: Encode with all compression strategies and mix
        # Compute softmax weights over compression strategies
        weights = torch.softmax(self.strategy_logits, dim=0)  # [n_strategies]
        
        # LOG ALL STRATEGY WEIGHTS: Show what's being tried
        if self.training and not hasattr(self, '_strategy_weights_logged'):
            logger.info(f"🔍 AdaptiveStringEncoder: Evaluating {len(self.compression_levels)} compression strategies")
            for i, (strategy_name, _) in enumerate(self.compression_levels):
                weight_pct = weights[i].item() * 100
                logit_val = self.strategy_logits[i].item()
                logger.info(f"   Strategy {i:2d}: {strategy_name:12s} weight={weight_pct:5.1f}% logit={logit_val:6.3f}")
            self._strategy_weights_logged = True
        
        # STRATEGY PRUNING: After warmup (epoch > total_epochs/5), keep only top-2 strategies
        if self.training:
            warmup_epochs = max(1, self._total_epochs.item() // 5)
            current_epoch = self._epoch_counter.item()
            
            if current_epoch >= warmup_epochs and not self._pruning_enabled:
                # Activate pruning: find top-K strategies
                top_k_indices = torch.topk(weights.detach(), k=self._top_k, dim=0).indices
                new_mask = torch.zeros_like(self._pruned_mask)
                new_mask[top_k_indices] = 1.0
                self._pruned_mask.copy_(new_mask)
                self._pruning_enabled = True
                
                # Log which strategies survived
                surviving_strategies = [self.compression_levels[i][0] for i in top_k_indices.cpu().tolist()]
                pruned_strategies = [self.compression_levels[i][0] for i in range(len(self.compression_levels)) 
                                    if i not in top_k_indices.cpu().tolist()]
                logger.info(f"🔪 StringEncoder PRUNING activated at epoch {current_epoch}/{self._total_epochs.item()}")
                logger.info(f"   ✅ Keeping top-{self._top_k} strategies: {', '.join(surviving_strategies)}")
                logger.info(f"   ❌ Pruning {len(pruned_strategies)} strategies: {', '.join(pruned_strategies)}")
                logger.info(f"   📊 Final weights: {[f'{weights[i].item():.1%}' for i in top_k_indices.cpu().tolist()]}")
            
            # Apply pruning mask to weights
            if self._pruning_enabled:
                weights = weights * self._pruned_mask
                # Renormalize over surviving strategies
                weights = weights / (weights.sum() + 1e-10)
                
                # Log current active strategy weights periodically during training
                # Only log once per epoch (not on every batch) to avoid spam
                if current_epoch % 10 == 0 and current_epoch != self._last_logged_epoch.item():
                    active_indices = (self._pruned_mask > 0.5).nonzero(as_tuple=True)[0]
                    if len(active_indices) > 0:
                        active_strategies = [self.compression_levels[i][0] for i in active_indices.cpu().tolist()]
                        active_weights = [f'{weights[i].item():.1%}' for i in active_indices.cpu().tolist()]
                        
                        # Format as table with column name
                        col_name_display = self.column_name or "unknown"
                        
                        # Create formatted table
                        logger.info(f"   📈 Epoch {current_epoch} - String Encoder Strategy Weights:")
                        logger.info(f"      {'Column Name':<35s} | {'Strategies':<40s} | {'Weights':<30s}")
                        logger.info(f"      {'-' * 35} | {'-' * 40} | {'-' * 30}")
                        strategies_str = ', '.join(active_strategies)
                        weights_str = ', '.join(active_weights)
                        logger.info(f"      {col_name_display:<35s} | {strategies_str:<40s} | {weights_str:<30s}")
                        
                        # Mark this epoch as logged
                        self._last_logged_epoch.fill_(current_epoch)
        
        # Encode with each strategy and project to d_model
        strategy_outputs = []
        for i, (mlp, projection) in enumerate(zip(self.mlp_encoders, self.strategy_projections)):
            strategy_name = self.compression_levels[i][0]
            
            # SKIP PRUNED STRATEGIES: Don't compute forward pass if weight is ~0
            if self.training and self._pruning_enabled and self._pruned_mask[i].item() < 0.5:
                # Strategy is pruned - use zeros (won't contribute anyway due to zero weight)
                out = torch.zeros(token.value.shape[0], self.config.d_model or self.config.d_out, 
                                 dtype=torch.float32, device=token.value.device)
                strategy_outputs.append(out)
                continue
            
            if mlp is None and strategy_name == "ZERO":
                # ZERO strategy: output zeros (for random/uninformative columns)
                out = torch.zeros(token.value.shape[0], self.config.d_model or self.config.d_out, 
                                 dtype=torch.float32, device=token.value.device)
            elif mlp is None and strategy_name == "DELIMITER":
                # DELIMITER strategy: The input is already projected [384] from learned projection
                # Just project to d_model
                if projection is not None:
                    # CRITICAL: Ensure projection is on the same device as input
                    proj_device = next(projection.parameters()).device
                    if proj_device != token.value.device:
                        # Move projection to match input device
                        projection = projection.to(token.value.device)
                        # Update the ModuleList entry so future calls use the moved projection
                        self.strategy_projections[i] = projection
                    out = projection(token.value)  # [batch_size, d_model]
                else:
                    out = token.value
            else:
                # Regular MLP strategy: encode with this strategy's MLP
                # CRITICAL: Ensure MLP is on the same device as input
                if mlp is None:
                    # This shouldn't happen in the else branch, but handle gracefully
                    logger.error(f"StringEncoder: MLP is None for strategy {i} ({strategy_name}) in else branch")
                    out = torch.zeros(token.value.shape[0], self.config.d_model or self.config.d_out, 
                                     dtype=torch.float32, device=token.value.device)
                else:
                    mlp_device = next(mlp.parameters()).device
                    if mlp_device != token.value.device:
                        # Move MLP to match input device
                        mlp = mlp.to(token.value.device)
                        # Update the ModuleList entry so future calls use the moved MLP
                        self.mlp_encoders[i] = mlp
                    out = mlp(token.value)  # [batch_size, d_out_strategy]
                
                # Check for NaN in strategy output
                if torch.isnan(out).any() or torch.isinf(out).any():
                    logger.error(f"💥 StringEncoder strategy {i} output contains NaN/Inf!")
                    logger.error(f"   Strategy: {strategy_name}")
                    logger.error(f"   Output shape: {out.shape}, NaN count: {torch.isnan(out).sum().item()}")
                    # Replace with zeros to avoid corruption
                    out = torch.zeros_like(out)
                
                # Project to d_model if needed
                if projection is not None:
                    # CRITICAL: Ensure projection is on the same device as input
                    proj_device = next(projection.parameters()).device
                    if proj_device != out.device:
                        # Move projection to match input device
                        projection = projection.to(out.device)
                        # Update the ModuleList entry so future calls use the moved projection
                        self.strategy_projections[i] = projection
                    out = projection(out)  # [batch_size, d_model]
            
            strategy_outputs.append(out)
        
        # Stack all strategy outputs: [n_strategies, batch_size, d_model]
        strategy_stack = torch.stack(strategy_outputs, dim=0)
        
        # Mix strategies using learned weights: [batch_size, d_model]
        # weights: [n_strategies] → [n_strategies, 1, 1] for broadcasting
        weights_expanded = weights.view(-1, 1, 1)
        out = (strategy_stack * weights_expanded).sum(dim=0)  # [batch_size, d_model]
        
        # ENTROPY REGULARIZATION: Encourage sharp strategy selection
        # (Similar to AdaptiveScalarEncoder)
        if self.training:
            entropy = -(weights * torch.log(weights + 1e-10)).sum()
            # Scale entropy loss - higher penalty = sharper strategies
            # Use 0.1 * entropy as penalty (encouraging sharper distributions)
            entropy_loss = 0.1 * entropy
            # Store for logging/debugging
            if not hasattr(self, '_last_entropy'):
                self._last_entropy = entropy.item()
                self._last_entropy_loss = entropy_loss.item()
            else:
                self._last_entropy = 0.9 * self._last_entropy + 0.1 * entropy.item()  # EMA
                self._last_entropy_loss = 0.9 * self._last_entropy_loss + 0.1 * entropy_loss.item()
            # Store entropy loss so it can be collected and added to total loss
            # This encourages sharper strategy selection (one strategy dominates)
            self._current_entropy_loss = entropy_loss
        else:
            # Not training - clear entropy loss
            self._current_entropy_loss = None

        # Override embeddings for unknown and not present tokens
        out[token.status == TokenStatus.NOT_PRESENT] = self._replacement_embedding
        out[token.status == TokenStatus.UNKNOWN] = self._replacement_embedding
        out[token.status == TokenStatus.MARGINAL] = self._replacement_embedding

        # CONDITIONAL NORMALIZATION based on config
        if self.config.normalize:
            # Add epsilon for numerical stability during normalization
            short_vec = nn.functional.normalize(out[:, 0:3], dim=1, eps=1e-8)
            full_vec = nn.functional.normalize(out, dim=1, eps=1e-8)
        else:
            # No normalization at column level - only joint encoder will normalize
            short_vec = out[:, 0:3]
            full_vec = out

        return short_vec, full_vec

    @staticmethod
    def get_default_config(d_in: int, d_out: int, d_model: int = None):
        # Import here to avoid circular import
        from .sphere_config import get_config
        
        # Get normalization setting from global config
        normalize_column_encoders = get_config().get_normalize_column_encoders()
        
        return StringEncoderConfig(
            d_in=d_in,
            d_out=d_out,
            d_model=d_model,  # Target dimension for stacking
            normalize=normalize_column_encoders,  # Config-controlled normalization
        )

# Global cache manager to share StringCache instances across all StringCodec objects
_global_string_caches = {}  # filename -> StringCache instance

# Shared in-memory cache for workers (multiprocessing.Manager dict)
_shared_memory_cache = None  # multiprocessing.Manager().dict() - shared across all processes
_shared_memory_cache_manager = None  # Manager instance
_shared_memory_cache_init_attempted = False  # Track if we've already tried to initialize
_shared_memory_cache_warning_logged = False  # Track if we've already logged the warning

# Memory limit for string cache: AUTO-SCALED based on available system RAM
# Default to 8 GB (much more conservative than old 32 GB)
# Will be dynamically adjusted based on system RAM in _get_string_cache_limit()
STRING_CACHE_MEMORY_LIMIT_BYTES = 8 * 1024 * 1024 * 1024  # 8 GB default (conservative)
# Track memory usage (approximate - bytes used by embeddings + string keys)
_shared_memory_cache_size_bytes = 0
# LRU tracking: list of keys in order of access (most recent last)
_shared_memory_cache_lru = None

def _get_string_cache_limit():
    """Get adaptive string cache memory limit based on available system RAM.
    
    Returns:
        int: Memory limit in bytes
    """
    try:
        import psutil
        # Get total system RAM
        total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        available_ram_gb = psutil.virtual_memory().available / (1024 ** 3)
        
        # Conservative strategy: use at most 20% of total RAM for cache
        # This leaves plenty for OS, main process, DataLoader workers, PyTorch overhead
        # Old limit of 32 GB could exhaust system RAM on machines with < 160 GB
        max_cache_gb = min(
            total_ram_gb * 0.20,  # 20% of total RAM
            available_ram_gb * 0.30,  # 30% of currently available RAM
            16.0  # Absolute cap at 16 GB (was 32 GB - too aggressive)
        )
        
        # Floor at 2 GB minimum
        max_cache_gb = max(2.0, max_cache_gb)
        
        limit_bytes = int(max_cache_gb * 1024 * 1024 * 1024)
        
        logger.info(f"📊 String cache limit: {max_cache_gb:.1f} GB (System RAM: {total_ram_gb:.1f} GB total, {available_ram_gb:.1f} GB available)")
        
        return limit_bytes
        
    except ImportError:
        # psutil not available - use conservative default
        logger.warning("⚠️  psutil not available - using default 8 GB string cache limit")
        return 8 * 1024 * 1024 * 1024  # 8 GB default
    except Exception as e:
        logger.warning(f"⚠️  Failed to detect system RAM: {e} - using default 8 GB string cache limit")
        return 8 * 1024 * 1024 * 1024  # 8 GB default

# Track logged cache misses to avoid spam (only log each unique value once)
_logged_cache_misses = set()  # Set of values we've already logged

def _init_shared_memory_cache():
    """Initialize shared in-memory cache for workers.
    
    NOTE: This should ONLY be called from the main process, not from worker processes.
    Workers are daemonic and cannot create multiprocessing.Manager().
    """
    global _shared_memory_cache, _shared_memory_cache_manager, _shared_memory_cache_init_attempted, _shared_memory_cache_warning_logged
    global _shared_memory_cache_size_bytes, _shared_memory_cache_lru, STRING_CACHE_MEMORY_LIMIT_BYTES
    
    # If we've already attempted initialization, don't try again
    if _shared_memory_cache_init_attempted:
        return
    
    _shared_memory_cache_init_attempted = True
    
    # CRITICAL: Workers should NEVER try to initialize shared memory cache
    # They are daemonic processes and cannot create Managers
    if _is_worker_process():
        # Worker process - can't create Manager, just use SQLite
        _shared_memory_cache = None
        return
    
    # Set adaptive memory limit based on system RAM
    STRING_CACHE_MEMORY_LIMIT_BYTES = _get_string_cache_limit()
    
    # Main process - try to create Manager for sharing with workers
    try:
        import multiprocessing
        _shared_memory_cache_manager = multiprocessing.Manager()
        _shared_memory_cache = _shared_memory_cache_manager.dict()
        _shared_memory_cache_lru = _shared_memory_cache_manager.list()  # LRU tracking
        _shared_memory_cache_size_bytes = 0
        logger.info(f"✅ Initialized shared in-memory cache for workers (limit: {STRING_CACHE_MEMORY_LIMIT_BYTES / (1024**3):.1f} GB)")
    except Exception as e:
        # Only log warning once to avoid spam
        if not _shared_memory_cache_warning_logged:
            logger.warning(f"⚠️  Failed to initialize shared memory cache: {e}. Workers will use SQLite.")
            _shared_memory_cache_warning_logged = True
        _shared_memory_cache = None
        _shared_memory_cache_lru = None

def _check_shared_memory_cache_alive():
    """Check if shared memory cache manager is still alive.
    
    Returns:
        True if alive, False if dead (will reset cache to None)
    """
    global _shared_memory_cache, _shared_memory_cache_manager, _shared_memory_cache_init_attempted
    if _shared_memory_cache is None:
        return False
    try:
        # Try to access the cache to see if manager is alive
        _ = len(_shared_memory_cache)
        return True
    except (BrokenPipeError, ConnectionResetError, OSError):
        # Manager process died - reset
        logger.warning("⚠️  Shared memory cache manager died, resetting cache")
        _shared_memory_cache = None
        _shared_memory_cache_manager = None
        _shared_memory_cache_init_attempted = False
        return False

def _evict_lru_entries(needed_bytes):
    """Evict least recently used entries until we have enough space.
    
    Args:
        needed_bytes: Bytes needed to add new entry
        
    Returns:
        Bytes freed
    """
    global _shared_memory_cache, _shared_memory_cache_lru, _shared_memory_cache_size_bytes
    
    if not _check_shared_memory_cache_alive() or _shared_memory_cache_lru is None:
        return 0
    
    freed_bytes = 0
    evicted_count = 0
    
    try:
        # Evict oldest entries (first in LRU list) until we have enough space
        while (_shared_memory_cache_size_bytes + needed_bytes > STRING_CACHE_MEMORY_LIMIT_BYTES and 
               len(_shared_memory_cache_lru) > 0):
            # Remove oldest entry (first in list)
            oldest_key = _shared_memory_cache_lru.pop(0)
            if oldest_key in _shared_memory_cache:
                embedding_blob = _shared_memory_cache[oldest_key]
                entry_bytes = len(embedding_blob) + len(oldest_key.encode('utf-8'))
                del _shared_memory_cache[oldest_key]
                _shared_memory_cache_size_bytes -= entry_bytes
                freed_bytes += entry_bytes
                evicted_count += 1
    except (BrokenPipeError, ConnectionResetError, OSError):
        # Manager died during eviction - reset and return
        _check_shared_memory_cache_alive()  # This will reset the cache
        return 0
    
    if evicted_count > 0:
        logger.info(f"🧹 Evicted {evicted_count:,} LRU entries ({freed_bytes / (1024**2):.1f} MB) to stay under {STRING_CACHE_MEMORY_LIMIT_BYTES / (1024**3):.1f} GB limit")
    
    return freed_bytes

def _add_to_shared_memory_cache(string_value, embedding_blob):
    """Add a single entry to shared memory cache with memory limit checking.
    
    Args:
        string_value: String key
        embedding_blob: Embedding bytes (BLOB)
        
    Returns:
        True if added, False if skipped due to memory limit
    """
    global _shared_memory_cache, _shared_memory_cache_lru, _shared_memory_cache_size_bytes
    
    if _shared_memory_cache is None:
        return False
    
    # Skip if already in cache
    if string_value in _shared_memory_cache:
        # Update LRU: move to end (most recent)
        if _shared_memory_cache_lru is not None and string_value in _shared_memory_cache_lru:
            try:
                _shared_memory_cache_lru.remove(string_value)
                _shared_memory_cache_lru.append(string_value)
            except (ValueError, AttributeError):
                pass
        return True
    
    entry_bytes = len(embedding_blob) + len(string_value.encode('utf-8'))
    
    # Check if we need to evict to make room
    if _shared_memory_cache_size_bytes + entry_bytes > STRING_CACHE_MEMORY_LIMIT_BYTES:
        _evict_lru_entries(entry_bytes)
    
    # Check again after eviction
    if _shared_memory_cache_size_bytes + entry_bytes <= STRING_CACHE_MEMORY_LIMIT_BYTES:
        _shared_memory_cache[string_value] = embedding_blob
        if _shared_memory_cache_lru is not None:
            _shared_memory_cache_lru.append(string_value)
        _shared_memory_cache_size_bytes += entry_bytes
        return True
    else:
        # Still over limit after eviction - skip this entry
        return False

def _populate_shared_memory_cache(cache_instance):
    """Populate shared in-memory cache from StringCache instance.
    
    Respects STRING_CACHE_MEMORY_LIMIT_BYTES (32 GB) by using LRU eviction.
    """
    global _shared_memory_cache, _shared_memory_cache_size_bytes, _shared_memory_cache_lru
    
    if _shared_memory_cache is None:
        _init_shared_memory_cache()
    
    if _shared_memory_cache is None:
        return  # Failed to initialize
    
    try:
        # Read all embeddings from SQLite cache into shared memory
        cursor = cache_instance.conn.cursor()
        cursor.execute("SELECT string_value, embeddings_blob FROM cache")
        rows = cursor.fetchall()
        
        # Check if cache is alive before accessing
        if not _check_shared_memory_cache_alive():
            return
        
        # Only add entries that aren't already in shared memory
        try:
            existing_count = len(_shared_memory_cache)
        except (BrokenPipeError, ConnectionResetError, OSError):
            _check_shared_memory_cache_alive()
            return
        
        new_count = 0
        skipped_count = 0
        total_bytes = 0
        
        for string_value, embedding_blob in rows:
            # Check if manager is still alive before each operation
            if not _check_shared_memory_cache_alive():
                break
                
            try:
                if string_value not in _shared_memory_cache:
                    entry_bytes = len(embedding_blob) + len(string_value.encode('utf-8'))
                    
                    # Check if we need to evict to make room
                    if _shared_memory_cache_size_bytes + entry_bytes > STRING_CACHE_MEMORY_LIMIT_BYTES:
                        _evict_lru_entries(entry_bytes)
                        # Check if manager died during eviction
                        if not _check_shared_memory_cache_alive():
                            break
                    
                    # Check again after eviction
                    if _shared_memory_cache_size_bytes + entry_bytes <= STRING_CACHE_MEMORY_LIMIT_BYTES:
                        # Store as bytes (numpy arrays can't be directly stored in Manager dict)
                        _shared_memory_cache[string_value] = embedding_blob
                        # Add to end of LRU list (most recent)
                        if _shared_memory_cache_lru is not None:
                            try:
                                _shared_memory_cache_lru.append(string_value)
                            except (BrokenPipeError, ConnectionResetError, OSError):
                                _check_shared_memory_cache_alive()
                                break
                        _shared_memory_cache_size_bytes += entry_bytes
                        new_count += 1
                        total_bytes += entry_bytes
                    else:
                        skipped_count += 1
            except (BrokenPipeError, ConnectionResetError, OSError):
                # Manager died during iteration
                _check_shared_memory_cache_alive()
                break
        
        if new_count > 0:
            current_mb = _shared_memory_cache_size_bytes / (1024 * 1024)
            current_gb = _shared_memory_cache_size_bytes / (1024 ** 3)
            logger.info(f"📦 Added {new_count:,} new entries to shared memory cache (total: {existing_count + new_count:,})")
            logger.info(f"   Memory usage: {current_mb:.1f} MB ({current_gb:.2f} GB / {STRING_CACHE_MEMORY_LIMIT_BYTES / (1024**3):.1f} GB)")
            if skipped_count > 0:
                logger.warning(f"   ⚠️  Skipped {skipped_count:,} entries due to memory limit")
        else:
            logger.debug(f"Shared memory cache already up to date ({existing_count:,} entries)")
        
    except Exception as e:
        logger.warning(f"⚠️  Failed to populate shared memory cache: {e}. Workers will use SQLite.")
        _shared_memory_cache = None

def get_shared_memory_cache():
    """Get the shared in-memory cache (for workers).
    
    Workers should call this to access the cache, but they should NOT try to initialize it.
    The cache must be initialized in the main process before workers start.
    """
    global _shared_memory_cache
    
    # If we're in a worker and cache is None, don't try to initialize (will fail)
    if _shared_memory_cache is None and not _is_worker_process():
        # Only main process should try to initialize
        _init_shared_memory_cache()
    
    # Workers will get None if cache wasn't initialized in main process - that's OK, they'll use SQLite
    return _shared_memory_cache

def get_global_string_cache(cache_filename=None, initial_values=None, debug_name="global_cache"):
    """
    Get or create a global StringCache instance for the given filename.
    This allows multiple StringCodec objects to share the same cache.
    
    Uses file locking to prevent multiple processes from creating the same cache simultaneously.
    """
    try:
        import fcntl
        HAS_FCNTL = True
    except ImportError:
        HAS_FCNTL = False
    
    # Use default filename if none provided
    cache_key = cache_filename or "default_strings.sqlite3"
    debug_name = debug_name.strip() if debug_name else "global_cache"

    # Return existing cache if available (process-local check)
    if cache_key in _global_string_caches:
        # Removed verbose debug log - cache reuse is expected and frequent
        cache = _global_string_caches[cache_key]
        # Populate shared memory cache if not already done
        # Handle case where manager process may have died (BrokenPipeError)
        global _shared_memory_cache, _shared_memory_cache_manager, _shared_memory_cache_init_attempted
        try:
            if _shared_memory_cache is None or len(_shared_memory_cache) == 0:
                _populate_shared_memory_cache(cache)
        except (BrokenPipeError, ConnectionResetError, OSError) as e:
            # Manager process died - reset and recreate
            logger.warning(f"⚠️  Shared memory cache manager died, recreating: {e}")
            _shared_memory_cache = None
            _shared_memory_cache_manager = None
            _shared_memory_cache_init_attempted = False
            _init_shared_memory_cache()
            # Try to populate again after recreation
            if _shared_memory_cache is not None:
                try:
                    _populate_shared_memory_cache(cache)
                except Exception as e2:
                    logger.debug(f"Could not populate shared memory cache after recreation: {e2}")
        return cache
    
    # Resolve absolute path for cache file
    if cache_filename:
        if os.path.isabs(cache_filename):
            cache_abs_path = cache_filename
        else:
            cache_abs_path = os.path.abspath(cache_filename)
    else:
        cache_abs_path = os.path.abspath("default_strings.sqlite3")
    
    # CRITICAL: Check if cache file already exists before trying to create it
    # This prevents race conditions when multiple processes try to create the same cache
    if os.path.exists(cache_abs_path) and os.path.getsize(cache_abs_path) > 0:
        # Cache already exists - just open it (another process created it)
        logger.debug(f"✅ Cache file already exists: {cache_key}")
        cache = StringCache(
            initial_values=initial_values or [],
            debugName=f"global_{debug_name}",
            string_cache_filename=cache_filename
        )
        _global_string_caches[cache_key] = cache
        _populate_shared_memory_cache(cache)
        return cache
    
    # Cache doesn't exist - need to create it with file locking
    lock_file_path = f"{cache_abs_path}.lock"
    lock_file = None
    try:
        if HAS_FCNTL:
            # Use fcntl for proper file locking (Linux/Unix)
            lock_file = open(lock_file_path, 'w')
            
            # Try to acquire exclusive lock (non-blocking first, then blocking)
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                lock_acquired = True
            except BlockingIOError:
                # Another process is creating the cache - wait for it
                logger.info(f"⏳ Another process is creating cache {cache_key}, waiting...")
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)  # Block until lock is available
                lock_acquired = True
        else:
            # Fallback for systems without fcntl (Windows, some macOS)
            # Use simple file existence check with retries
            import time
            max_wait = 30  # Wait up to 30 seconds
            wait_interval = 0.5
            waited = 0
            while os.path.exists(lock_file_path) and waited < max_wait:
                time.sleep(wait_interval)
                waited += wait_interval
            # Create lock file
            lock_file = open(lock_file_path, 'w')
            lock_file.write(str(os.getpid()))
            lock_file.flush()
            os.fsync(lock_file.fileno())
        
        # After acquiring lock, check again if cache file now exists (another process may have created it)
        if os.path.exists(cache_abs_path) and os.path.getsize(cache_abs_path) > 0:
            # Another process created it while we were waiting - just open it
            logger.info(f"✅ Cache file exists (created by another process): {cache_key}")
            cache = StringCache(
                initial_values=initial_values or [],
                debugName=f"global_{debug_name}",
                string_cache_filename=cache_filename
            )
            _global_string_caches[cache_key] = cache
            _populate_shared_memory_cache(cache)
            return cache
        
        # We have the lock and cache doesn't exist - create it
        logger.info(f"🆕 Creating new global string cache: {cache_key}")
        cache = StringCache(
            initial_values=initial_values or [],
            debugName=f"global_{debug_name}",
            string_cache_filename=cache_filename
        )
        _global_string_caches[cache_key] = cache
        
        # Populate shared memory cache after creating SQLite cache
        _populate_shared_memory_cache(cache)
        
        logger.info(f"✅ Global string cache created and cached: {cache_key}")
        return cache
        
    except Exception as e:
        logger.error(f"❌ Failed to create global string cache {cache_key}: {e}")
        raise
    finally:
        # Release lock
        if lock_file:
            try:
                if HAS_FCNTL:
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
                lock_file.close()
                # Remove lock file if it exists (best effort)
                try:
                    if os.path.exists(lock_file_path):
                        os.unlink(lock_file_path)
                except Exception:
                    pass  # Ignore errors removing lock file
            except Exception:
                pass  # Ignore errors releasing lock

def clear_global_string_caches():
    """Clear all global string caches (useful for testing or memory cleanup)."""
    global _global_string_caches, _logged_cache_misses
    count = len(_global_string_caches)
    _global_string_caches.clear()
    _logged_cache_misses.clear()
    logger.info(f"🧹 Clearing {count} global string caches")

def get_global_string_cache_stats():
    """Get statistics about all global string caches."""
    stats = {
        'total_caches': len(_global_string_caches),
        'cache_files': list(_global_string_caches.keys()),
        'cache_details': {}
    }
    
    for filename, cache in _global_string_caches.items():
        try:
            cache_stats = cache.get_gpu_efficiency_stats()
            stats['cache_details'][filename] = {
                'hit_rate': cache_stats.get('cache_hit_rate', 0),
                'cache_hits': cache_stats.get('cache_hits', 0),
                'cache_misses': cache_stats.get('cache_misses', 0),
                'individual_gpu_encodings': cache_stats.get('individual_gpu_encodings', 0),
                'efficiency': cache_stats.get('gpu_efficiency', 'Unknown')
            }
        except Exception as e:
            stats['cache_details'][filename] = {'error': str(e)}
    
    return stats

gStringCachePath = None

def set_string_cache_path(path):
    global gStringCachePath
    gStringCachePath = path

class StringCodec(nn.Module):
    def __init__(self, enc_dim: int, debugName=None, initial_values=None, string_cache: str=None,
                 delimiter: str=None, is_random_column: bool=False):
        super().__init__()
        # String server client is initialized on first use - no local model loading needed
        assert enc_dim > 0
        assert debugName is not None, "We need debugName for the string cache -- pass in the col name"

        self._numEncodeCalls = 0
        self.colName = debugName  # HACK
        self._is_decodable = False  # String decoding not yet implemented (needs final embedding index)
        # Store without padding - padding is only for display, not for lookups
        # The cache key is based on cache_filename, not debug_name
        self.debug_name = str(debugName).strip()
        self.enc_dim = enc_dim
        # NOTE: change this based on the model used
        # After learned projection, output is still [384] (same as before)
        self.d_string_model = STRING_DIM

        # Store only the cache filename for global cache lookup
        # CRITICAL: Resolve to absolute path so workers can find it regardless of working directory
        if string_cache:
            if not os.path.isabs(string_cache):
                # Relative path - resolve to absolute based on current working directory
                self._string_cache_filename = os.path.abspath(string_cache)
            else:
                # Already absolute
                self._string_cache_filename = string_cache
        else:
            self._string_cache_filename = None
        
        # NEW: Adaptive string encoding features
        self.delimiter = delimiter  # If set, preprocess strings before encoding
        self.is_random_column = is_random_column  # If True, return zero embeddings
        
        if delimiter:
            logger.info(f"🔧 StringCodec '{debugName}' will preprocess with delimiter: '{delimiter}'")
        if is_random_column:
            logger.warning(f"🚫 StringCodec '{debugName}' marked as RANDOM - will return zero embeddings")

        # Use global string cache instead of creating individual cache per codec
        logger.info(f"🔗 StringCodec using global string cache: {string_cache or 'default'}")
        logger.info(f"🔍 STRINGCODEC DEBUG: string_cache parameter = {string_cache}")
        logger.info(f"🔍 STRINGCODEC DEBUG: debugName = {debugName}")
        logger.info(f"🔍 STRINGCODEC DEBUG: initial_values count = {len(initial_values) if initial_values else 0}")
        
        # Get or create the global cache for this filename
        self.string_cache = get_global_string_cache(
            cache_filename=string_cache,
            initial_values=initial_values,
            debug_name=debugName
        )
        
        # Compute frequency statistics for frequency encoding
        from collections import Counter
        if initial_values:
            value_counts = Counter(str(v) for v in initial_values if v is not None and str(v) != 'nan')
            total_count = len([v for v in initial_values if v is not None and str(v) != 'nan'])
            self.column_freq_stats = {
                'value_counts': value_counts,
                'total_count': total_count
            }
        else:
            self.column_freq_stats = None
        
        # Separate paths for BERT and features - both contribute equally, features can matter more
        # BERT path: [384] → [384] (preserve semantic info)
        self.bert_projection = nn.Sequential(
            nn.Linear(STRING_DIM, STRING_DIM),  # [384] → [384]
            nn.ReLU(),
            nn.Dropout(0.1),
        )
        
        # Features path: [27] → [384] (give features full capacity to contribute)
        # Features might matter more than BERT for structured data
        self.feature_embedding_mlp = nn.Sequential(
            nn.Linear(27, 256),  # 27 features → 256 hidden (larger capacity)
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(256, STRING_DIM),  # 256 → [384] (same size as BERT)
        )
        
        # Learned merge: combine BERT [384] + features [384] → [384]
        # Learns how much to weight each (features might be more important)
        self.merge_mlp = nn.Sequential(
            nn.Linear(STRING_DIM * 2, STRING_DIM * 2),  # [768] → [768]
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(STRING_DIM * 2, STRING_DIM),  # [768] → [384]
        )
        
        # Initialize weights
        for name, param in self.bert_projection.named_parameters():
            if 'weight' in name and param.ndim >= 2:
                nn.init.xavier_uniform_(param, gain=0.5)
            elif 'bias' in name:
                nn.init.zeros_(param)
        
        for name, param in self.feature_embedding_mlp.named_parameters():
            if 'weight' in name and param.ndim >= 2:
                nn.init.xavier_uniform_(param, gain=0.5)
            elif 'bias' in name:
                nn.init.zeros_(param)
        
        for name, param in self.merge_mlp.named_parameters():
            if 'weight' in name and param.ndim >= 2:
                nn.init.xavier_uniform_(param, gain=0.5)
            elif 'bias' in name:
                nn.init.zeros_(param)
        
        logger.info(f"🔧 StringCodec '{debugName}': Separate BERT + features paths (both [384]), learned merge (features can matter more)")

    def _safe_get_bert_projection(self):
        """Safely get bert_projection if it exists and is valid, otherwise return None."""
        bert_proj = getattr(self, 'bert_projection', None)
        if bert_proj is not None:
            try:
                # Verify it's a valid module with parameters
                _ = next(bert_proj.parameters())
                return bert_proj
            except (AttributeError, StopIteration, TypeError):
                return None
        return None
    
    def _safe_get_feature_embedding_mlp(self):
        """Safely get feature_embedding_mlp if it exists and is valid, otherwise return None."""
        feature_mlp = getattr(self, 'feature_embedding_mlp', None)
        if feature_mlp is not None:
            try:
                # Verify it's a valid module with parameters
                _ = next(feature_mlp.parameters())
                return feature_mlp
            except (AttributeError, StopIteration, TypeError):
                return None
        return None
    
    def _safe_get_merge_mlp(self):
        """Safely get merge_mlp if it exists and is valid, otherwise return None."""
        merge_mlp = getattr(self, 'merge_mlp', None)
        if merge_mlp is not None:
            try:
                # Verify it's a valid module with parameters
                _ = next(merge_mlp.parameters())
                return merge_mlp
            except (AttributeError, StopIteration, TypeError):
                return None
        return None
    
    def has_mlp_layers(self):
        """Check if all MLP layers exist and are valid."""
        return (self._safe_get_bert_projection() is not None and
                self._safe_get_feature_embedding_mlp() is not None and
                self._safe_get_merge_mlp() is not None)

    def __getstate__(self):
        # Simply exclude the cache object - global cache will handle the rest
        state = self.__dict__.copy()
        state.pop("string_cache", None)
        return state

    def __setstate__(self, state):
        # Get debug_name from state dict (it hasn't been set on self yet)
        debug_name = state.get('debug_name', state.get('colName', 'unknown'))
        
        # CRITICAL: Clear GPU cache at the VERY START of __setstate__ to prevent GPU allocation during unpickling
        # This must happen before self.__dict__.update(state) which triggers unpickling of nested objects
        try:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
        except Exception as e:
            logger.debug(f"Could not clear GPU cache in __setstate__: {e}")
        
        # Log GPU memory at the very start of __setstate__
        allocated_start = 0.0
        reserved_start = 0.0
        if torch.cuda.is_available():
            allocated_start = torch.cuda.memory_allocated() / (1024**3)
            reserved_start = torch.cuda.memory_reserved() / (1024**3)
        
        # CRITICAL: Check force_cpu flag BEFORE unpickling to prevent GPU allocation
        force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
        
        # If force_cpu is set, move any GPU tensors in state to CPU BEFORE self.__dict__.update
        if force_cpu:
            logger.info(f"StringCodec.__setstate__ '{debug_name}': force_cpu=True, moving state tensors to CPU before update")
            for key, value in list(state.items()):
                # Check if it's an nn.Module and move to CPU
                if hasattr(value, 'cpu') and hasattr(value, 'parameters'):
                    try:
                        state[key] = value.cpu()
                        logger.debug(f"  Moved {key} to CPU before update")
                    except Exception as e:
                        logger.debug(f"  Could not move {key} to CPU: {e}")
        
        # Restore state and reconnect to global cache
        self.__dict__.update(state)
        

        # Backward compatibility: set defaults for new attributes not in old pickles
        if 'is_random_column' not in state:
            self.is_random_column = False
        if 'delimiter' not in state:
            self.delimiter = None
        if 'column_freq_stats' not in state:
            # Older models don't have column_freq_stats - set to None (will use fallback in tokenize)
            self.column_freq_stats = None
        
        # MLPs should already be on CPU from above, but double-check
        if force_cpu:
            try:
                # Move all MLPs to CPU if they exist and are on GPU
                if hasattr(self, 'bert_projection') and self.bert_projection is not None:
                    if list(self.bert_projection.parameters()):
                            bert_device = next(self.bert_projection.parameters()).device
                            if bert_device.type == 'cuda':
                                self.bert_projection = self.bert_projection.cpu()
                                if torch.cuda.is_available():
                                    torch.cuda.empty_cache()
                
                if hasattr(self, 'feature_embedding_mlp') and self.feature_embedding_mlp is not None:
                    if list(self.feature_embedding_mlp.parameters()):
                        feature_device = next(self.feature_embedding_mlp.parameters()).device
                        if feature_device.type == 'cuda':
                            self.feature_embedding_mlp = self.feature_embedding_mlp.cpu()
                            if torch.cuda.is_available():
                                torch.cuda.empty_cache()
                
                if hasattr(self, 'merge_mlp') and self.merge_mlp is not None:
                    if list(self.merge_mlp.parameters()):
                        merge_device = next(self.merge_mlp.parameters()).device
                        if merge_device.type == 'cuda':
                            self.merge_mlp = self.merge_mlp.cpu()
                            if torch.cuda.is_available():
                                torch.cuda.empty_cache()
                
            except Exception as e:
                logger.error(f"❌ StringCodec.__setstate__ '{debug_name}': Could not check/move MLPs: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # CRITICAL: Workers must NEVER load sentence model on GPU
        # Check multiple indicators - be VERY defensive during unpickling
        is_worker = _is_worker_process()
        
        # Additional check: spawned processes that aren't MainProcess are likely workers
        is_likely_worker = False
        try:
            import multiprocessing
            mp_name = multiprocessing.current_process().name
            if mp_name != 'MainProcess' and os.environ.get('PYTORCH_DATALOADER_WORKER') is None:
                is_likely_worker = True
        except Exception:
            pass
        
        # Only load if we're CERTAIN we're in main process
        if not is_worker and not is_likely_worker:
            allocated_before = 0.0
            reserved_before = 0.0
            if torch.cuda.is_available():
                allocated_before = torch.cuda.memory_allocated() / (1024**3)
                reserved_before = torch.cuda.memory_reserved() / (1024**3)
            # String server client is initialized on first use - no local model loading needed
        
        # Don't reconnect here - use lazy lookup via _get_string_cache() when needed
        # This prevents storing StringCache object (which has sqlite connections) in the codec
        # This is critical for multiprocessing DataLoader workers which need to pickle the codec

    def _get_string_cache(self):
        """Get StringCache from global registry using filename. Don't store the object."""
        if not hasattr(self, '_string_cache_filename') or not self._string_cache_filename:
            # Don't spam logs - this is normal when string cache isn't configured
            return None
        try:
            # In workers, the global cache registry is empty (not shared across processes)
            # So we need to create a new cache instance that reads from the SQLite file
            # The cache will be opened in read-only mode automatically if we're in a worker
            is_worker = _is_worker_process()
            if is_worker:
                # Worker process - create cache instance that reads from existing SQLite file
                # Don't pass initial_values - workers should only read, not populate
                cache = get_global_string_cache(
                    cache_filename=self._string_cache_filename,
                    initial_values=[],  # Workers don't populate - only read
                    debug_name=getattr(self, 'debug_name', getattr(self, 'colName', 'fallback_codec'))
                )
                # Ensure it's marked as readonly
                if cache:
                    cache.is_readonly = True
                return cache
            else:
                # Main process - use global cache registry
                return get_global_string_cache(
                    cache_filename=self._string_cache_filename,
                    initial_values=[],  # Global cache already has the data
                    debug_name=getattr(self, 'debug_name', getattr(self, 'colName', 'fallback_codec'))
                )
        except Exception as e:
            # Log actual errors with more detail
            logger.error(f"❌ Failed to get string cache for '{getattr(self, 'debug_name', getattr(self, 'colName', 'unknown'))}': {e}")
            logger.error(f"   Cache filename: {self._string_cache_filename}")
            logger.error(f"   Absolute path: {os.path.abspath(self._string_cache_filename) if self._string_cache_filename else 'None'}")
            logger.error(f"   File exists: {os.path.exists(self._string_cache_filename) if self._string_cache_filename else 'N/A'}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
    def get_codec_name(self):
        return ColumnType.FREE_STRING

    def get_not_present_token(self):
        tok = self.tokenize("")
        return set_not_present(tok)

    def get_marginal_token(self):
        """Return a token representing a masked/marginal value for reconstruction testing."""
        tok = self.tokenize("")
        return Token(
            value=tok.value,
            status=TokenStatus.MARGINAL,
            attention_mask=tok.attention_mask,
        )

    # def detokenize(self, token: Token, top_k: int = 1, debug: bool = False):
    #     """
    #     Detokenize a string token back to an actual value using nearest neighbor search.
    #     
    #     COMMENTED OUT: String decoding requires indexing final embeddings (d_model dims) in LanceDB,
    #     not BERT embeddings (384 dims). The encoder outputs d_model dimensions, but the cache stores
    #     BERT embeddings. Need to build a separate index of final embeddings for proper decoding.
    #     
    #     Args:
    #         token: Token with embedding as value (from encoder output)
    #         top_k: Number of nearest neighbors to return (default 1, use 3 for debugging)
    #         debug: If True, return top 3 neighbors for debugging
    #         
    #     Returns:
    #         If debug=False: Best matching string value
    #         If debug=True: Tuple of (best_match, top_3_list) where top_3_list is [(string, distance), ...]
    #     """
    #     raise NotImplementedError("String decoding not yet implemented - needs final embedding index")
    
    @property
    def token_dtype(self):
        return float

    def tokenize(self, value):
        """Here we actually do both the tokenize & encode."""
        # String server client is initialized on first use - no local model loading needed
        # Workers should only read from cache
        
        # Handle random columns - return zero embedding (zero contribution)
        # Backward compatibility: old pickled codecs don't have is_random_column
        is_random = getattr(self, 'is_random_column', False)
        if is_random:
            return Token(
                value=torch.zeros(STRING_DIM, dtype=torch.float32),  # [384] after projection
                status=TokenStatus.NOT_PRESENT,
            )
        
        try:
            try:
                isNan = False
                if value is None:
                    isNan = True
                if (
                    type(value) == float
                    or type(value) == int
                    or type(value) == np.float64
                    or type(value) == np.float32
                ):
                    if math.isnan(value):
                        isNan = True

                if isNan:
                    result = Token(
                        value=torch.zeros(STRING_DIM, dtype=torch.float32),  # [384]
                        status=TokenStatus.NOT_PRESENT,
                    )
                    # DEBUG: Check NOT_PRESENT token type
                    assert result.value.dtype == torch.float32, f"NOT_PRESENT token (1) is {result.value.dtype}, expected float32"
                    return result

                if str(value) == "nan":
                    assert False, "what the heck"

            except:
                traceback.print_exc()

            value = str(value)
            if value == "nan":
                result = Token(
                    value=torch.zeros(STRING_DIM, dtype=torch.float32),  # [384]
                    status=TokenStatus.NOT_PRESENT,
                )
                # DEBUG: Check NOT_PRESENT token type
                assert result.value.dtype == torch.float32, f"NOT_PRESENT token (2) is {result.value.dtype}, expected float32"
                return result

            # Check for natural language null strings ("N/A", "none", "-", "nada", etc.)
            # Uses semantic similarity to catch typos and variants
            # Note: is_null_natural_language has fallback when sentence_model is None
            from featrix.neural.string_analysis import is_null_natural_language
            if is_null_natural_language(value, sentence_model=None):
                result = Token(
                    value=torch.zeros(STRING_DIM, dtype=torch.float32),  # [384]
                    status=TokenStatus.NOT_PRESENT,
                )
                return result

            # Save original value for feature computation (before preprocessing)
            original_value = str(value)
            
            # Preprocess delimited strings BEFORE string cache lookup
            # Convert "a,b,c" → "a\nb\nc" for better BERT encoding
            if self.delimiter and isinstance(value, str):
                from featrix.neural.string_analysis import preprocess_delimited_string
                value = preprocess_delimited_string(value, self.delimiter)

            val = None
            cache_status = "unknown"
            
            # Use lazy lookup to avoid storing StringCache (which has SQLite connections) in the codec
            # This is critical for multiprocessing DataLoader workers
            is_worker = _is_worker_process()
            
            # Workers: Try shared memory cache first (fastest)
            if is_worker:
                shared_cache = get_shared_memory_cache()
                if shared_cache:
                    # Check shared memory cache first
                    if value in shared_cache:
                        # Found in shared memory - convert bytes to tensor
                        embedding_blob = shared_cache[value]
                        embedding = np.frombuffer(embedding_blob, dtype=np.float32)
                        val = torch.tensor(embedding, dtype=torch.float32)
                        cache_status = "shared_memory_hit"
                        assert val.dtype == torch.float32, f"Shared cache returned {val.dtype}, expected float32"
                        
                        # Update LRU: move to end (most recent)
                        global _shared_memory_cache_lru
                        if _shared_memory_cache_lru is not None and value in _shared_memory_cache_lru:
                            try:
                                _shared_memory_cache_lru.remove(value)
                                _shared_memory_cache_lru.append(value)
                            except (ValueError, AttributeError):
                                pass  # Ignore if list operations fail (multiprocessing edge case)
                    else:
                        # Not in shared memory - try SQLite cache
                        cache = self._get_string_cache()
                        if cache:
                            cache_status = "cache_available"
                            # Ensure cache is readonly in workers
                            if not getattr(cache, 'is_readonly', False):
                                cache.is_readonly = True
                                logger.debug(f"Worker process - set cache to readonly mode")
                            # Workers should not add missing entries
                            val = cache.get_embedding_from_cache(value, add_if_missing=False)
                            # If found in SQLite but not shared memory, log once
                            if val is not None and value not in _logged_cache_misses:
                                _logged_cache_misses.add(value)
                                logger.debug(f"Worker: Found '{value[:50]}...' in SQLite but not shared memory cache")
                        else:
                            cache_status = "no_cache"
                            val = None
                else:
                    # Shared memory cache not available - fall back to SQLite
                    cache = self._get_string_cache()
                    if cache:
                        cache_status = "cache_available"
                        # Ensure cache is readonly in workers
                        if not getattr(cache, 'is_readonly', False):
                            cache.is_readonly = True
                            logger.debug(f"Worker process - set cache to readonly mode")
                        # Workers should not add missing entries
                        val = cache.get_embedding_from_cache(value, add_if_missing=False)
                    else:
                        cache_status = "no_cache"
                        val = None
            else:
                # Main process: Use SQLite cache
                cache = self._get_string_cache()
                if cache:
                    cache_status = "cache_available"
                    val = cache.get_embedding_from_cache(value)
                else:
                    cache_status = "no_cache"
                    val = None
                # DEBUG: Check string cache return type
                if val is not None:
                    cache_status = "cache_hit"
                    assert hasattr(val, 'dtype'), f"String cache returned non-tensor: {type(val)}"
                    assert val.dtype == torch.float32, f"String cache returned {val.dtype}, expected float32"
                    
                    # Ensure shape is [384] not [1, 384] - tokens are individual, batching happens later
                    if len(val.shape) == 2:
                        val = val.squeeze(0)
                    
                    # Check for NaN in cached value
                    if torch.isnan(val).any():
                        logger.error(f"🚨 STRING CACHE RETURNED NaN: value='{value}' -> {val}")
                        cache_status = "cache_hit_but_nan"
                else:
                    cache_status = "cache_miss"

            if val is None:
                # Check if we're in a worker - workers should NEVER compute embeddings
                is_worker = _is_worker_process()
                if is_worker:
                    # Worker cache miss - CRITICAL: Don't return zero embeddings, crash instead
                    # Zero embeddings will corrupt the embedding space and produce bad models
                    error_msg = (
                        f"❌ CRITICAL: Worker cache miss for '{value[:50]}...' - value not in cache. "
                        f"Cannot return zero embedding as it would corrupt the embedding space. "
                        f"Total unique cache misses: {len(_logged_cache_misses) + 1}. "
                        f"Consider adding all unique training values to initial_values when creating StringCodec."
                    )
                    logger.error(error_msg)
                    raise RuntimeError(
                        f"StringCodec worker cache miss: '{value[:50]}...' not found in cache. "
                        f"This indicates the cache was not properly populated before workers started. "
                        f"Refusing to return zero embedding to prevent corrupting the embedding space."
                    )
                else:
                    # Main process - can compute embeddings and add to cache
                    cache_status = f"{cache_status}_fallback_to_direct"
                    try:
                        # Use string server client (required - no local model fallback)
                        client = _init_string_server_client()
                        if client is None:
                            raise RuntimeError(
                                "String server client not available. "
                                "Set 'string_server_host' in config.json to 'taco', 'taco.local', or 'localhost'. "
                                "Local sentence transformer model is no longer supported."
                            )
                        
                        # Use string server
                        embedding_list = client.encode(value)
                        val = torch.tensor(embedding_list, dtype=torch.float32)
                        cache_status = f"{cache_status}_string_server"
                        
                        assert val.dtype == torch.float32, f"encode returned {val.dtype}, expected float32"
                        
                        # Check for NaN in encoding
                        if torch.isnan(val).any():
                            logger.error(f"🚨 ENCODING RETURNED NaN: value='{value}' -> {val}")
                            cache_status = f"{cache_status}_nan"
                        
                        # Try to add to cache for future use
                        if cache:
                            try:
                                cache.get_embedding_from_cache(value, add_if_missing=True)
                            except Exception as cache_error:
                                logger.debug(f"Could not add to cache: {cache_error}")
                        
                    except Exception as e:
                        cache_status = f"{cache_status}_direct_failed"
                        error_msg = (
                            f"❌ CRITICAL: Failed to encode string '{value[:50]}...': {e}. "
                            f"Cannot return zero embedding as it would corrupt the embedding space."
                        )
                        logger.error(error_msg)
                        raise RuntimeError(
                            f"StringCodec encoding failure: '{value[:50]}...' could not be encoded. "
                            f"Refusing to return zero embedding to prevent corrupting the embedding space. "
                            f"Original error: {e}"
                        )
                    
            # Log cache status for debugging (first few times)
            # debug_count = getattr(self, '_debug_tokenize_count', 0)
            # if debug_count < 10:
            #     logger.info(f"🔍 STRING TOKENIZE DEBUG #{debug_count}: value='{value[:50]}' status={cache_status} result_shape={val.shape if val is not None else 'None'}")
            #     self._debug_tokenize_count = debug_count + 1
            
            # FINAL SHAPE CHECK: Ensure val is [384] not [1, 384] before creating Token
            if len(val.shape) == 2:
                val = val.squeeze(0)
            assert len(val.shape) == 1 and val.shape[0] == STRING_DIM, f"Token value must be [{STRING_DIM}], got {val.shape}"
            
            # Compute structured features and embed them (use original value before preprocessing)
            from featrix.neural.string_analysis import compute_string_features
            # Handle backward compatibility: older models might not have column_freq_stats
            column_freq_stats = getattr(self, 'column_freq_stats', None)
            raw_features = compute_string_features(original_value, column_freq_stats)
            
            # Backward compatibility: Check if this is an older model without MLP layers
            # Use safe accessors to get MLP layers
            bert_proj = self._safe_get_bert_projection()
            feature_mlp = self._safe_get_feature_embedding_mlp()
            merge_mlp = self._safe_get_merge_mlp()
            
            has_mlp_layers = self.has_mlp_layers()
            
            if has_mlp_layers:
                # New model with MLP layers: Separate paths for BERT and features
                # Double-check that we actually have valid modules (safety check)
                if bert_proj is None or feature_mlp is None or merge_mlp is None:
                    # Fallback to older model behavior if modules are missing
                    logger.warning("MLP layers detected but modules are None - using backward compatibility path")
                    result = Token(value=val, status=TokenStatus.OK)
                    assert hasattr(result.value, 'dtype'), f"Token value is non-tensor: {type(result.value)}"
                    assert result.value.dtype == torch.float32, f"Token value is {result.value.dtype}, expected float32"
                    return result
                
                # Ensure MLPs are on same device as input tensors
                device = val.device
                # Move MLPs to device if needed (they might be on CPU initially)
                # Safe access - we know they exist from has_mlp_layers() check, but add try-except for extra safety
                try:
                    if bert_proj is not None:
                        bert_device = next(bert_proj.parameters()).device
                        if bert_device != device:
                            self.bert_projection = bert_proj.to(device)
                            bert_proj = self.bert_projection  # Update local variable
                except (AttributeError, StopIteration, TypeError) as e:
                    logger.warning(f"Failed to check/move bert_projection device: {e}, falling back to older model path")
                    result = Token(value=val, status=TokenStatus.OK)
                    assert hasattr(result.value, 'dtype'), f"Token value is non-tensor: {type(result.value)}"
                    assert result.value.dtype == torch.float32, f"Token value is {result.value.dtype}, expected float32"
                    return result
                
                try:
                    if feature_mlp is not None:
                        feature_device = next(feature_mlp.parameters()).device
                        if feature_device != device:
                            self.feature_embedding_mlp = feature_mlp.to(device)
                            feature_mlp = self.feature_embedding_mlp  # Update local variable
                except (AttributeError, StopIteration, TypeError) as e:
                    logger.warning(f"Failed to check/move feature_embedding_mlp device: {e}, falling back to older model path")
                    result = Token(value=val, status=TokenStatus.OK)
                    assert hasattr(result.value, 'dtype'), f"Token value is non-tensor: {type(result.value)}"
                    assert result.value.dtype == torch.float32, f"Token value is {result.value.dtype}, expected float32"
                    return result
                
                try:
                    if merge_mlp is not None:
                        merge_device = next(merge_mlp.parameters()).device
                        if merge_device != device:
                            self.merge_mlp = merge_mlp.to(device)
                            merge_mlp = self.merge_mlp  # Update local variable
                except (AttributeError, StopIteration, TypeError) as e:
                    logger.warning(f"Failed to check/move merge_mlp device: {e}, falling back to older model path")
                    result = Token(value=val, status=TokenStatus.OK)
                    assert hasattr(result.value, 'dtype'), f"Token value is non-tensor: {type(result.value)}"
                    assert result.value.dtype == torch.float32, f"Token value is {result.value.dtype}, expected float32"
                    return result
                
                # Final safety check before using MLP layers
                if bert_proj is None or feature_mlp is None or merge_mlp is None:
                    logger.warning("MLP layers became None during device check - using backward compatibility path")
                    result = Token(value=val, status=TokenStatus.OK)
                    assert hasattr(result.value, 'dtype'), f"Token value is non-tensor: {type(result.value)}"
                    assert result.value.dtype == torch.float32, f"Token value is {result.value.dtype}, expected float32"
                    return result
                
                # Use MLP layers - safe because we've verified they exist
                # CRITICAL: Clone val if it was created in inference mode to avoid autograd error
                # val comes from string server client encoding
                # Always clone to ensure we have a fresh tensor that can participate in autograd
                val_clone = val.detach().clone().requires_grad_(True)
                bert_projected = bert_proj(val_clone.unsqueeze(0)).squeeze(0)  # [384] → [384]
                feature_embedding = feature_mlp(raw_features.to(device))  # [27] → [384]
                
                # Concatenate both [384] embeddings = [768]
                combined_input = torch.cat([bert_projected, feature_embedding], dim=0)
                
                # Learned merge: [768] → [384] (learns optimal combination, features can dominate)
                combined_embedding = merge_mlp(combined_input.unsqueeze(0)).squeeze(0)
                assert combined_embedding.shape[0] == STRING_DIM, f"Merged embedding must be [{STRING_DIM}], got {combined_embedding.shape}"
                
                result = Token(value=combined_embedding, status=TokenStatus.OK)
            else:
                # Older model: Just use the BERT embedding directly (backward compatibility)
                result = Token(value=val, status=TokenStatus.OK)
            assert hasattr(result.value, 'dtype'), f"Token value is non-tensor: {type(result.value)}"
            assert result.value.dtype == torch.float32, f"Token value is {result.value.dtype}, expected float32"
            return result

        except Exception as e:
            # Log the error but re-raise - we don't want to silently return zero embeddings
            # Worker cache misses should crash the training to prevent corrupting the embedding space
            traceback.print_exc()
            logger.error(f"🚨 STRING TOKENIZATION FAILED for value: {repr(value)}")
            raise  # Re-raise the exception - don't return zero embeddings

    def save(self):
        # we create a json dict.
        buffer = io.BytesIO()
        torch.save(self.state_dict(), buffer)

        buffer_b64 = "base64:" + str(
            base64.standard_b64encode(buffer.getvalue()).decode("utf8")
        )
        checksum = hashlib.md5(buffer.getvalue()).hexdigest()

        d = {
            "type": "StringCodec",
            "embedding": buffer_b64,
            "embedding_checksum": checksum,
            "enc_dim": self.enc_dim,
        }
        return d

    def load(self, j):
        d_type = j.get("type")
        assert d_type == "StringCodec", "wrong load method called for __%s__" % d_type
        self.enc_dim = j.get("enc_dim")
        embed = j.get("embedding")
        embed_checksum = j.get("embedding_checksum")

        if embed.startswith("base64:"):
            embed = embed[6:]

        r64 = base64.standard_b64decode(embed)
        r_checksum64 = hashlib.md5(r64).hexdigest()

        if r_checksum64 != embed_checksum:
            logger.error(f"CHECKSUMS {r_checksum64} and {embed_checksum} DO NOT MATCH - !")
            return

        self.__init__(self.enc_dim)

        buffer = io.BytesIO(r64)
        theDict = torch.load(buffer, weights_only=False)
        self.load_state_dict(theDict)
        return

    def get_gpu_efficiency_report(self):
        """Get a report on GPU efficiency for string processing."""
        cache = self._get_string_cache()
        if cache is None:
            return {"status": "No string cache available"}
        
        stats = cache.get_gpu_efficiency_stats()
        
        # Get string server info
        client = _init_string_server_client()
        server_url = client.base_url if client else None
        
        report = {
            "string_server_url": server_url,
            "string_server_available": client is not None,
            "gpu_available": torch.cuda.is_available(),
            "cache_statistics": stats,
            "recommendations": []
        }
        
        # Add recommendations based on performance
        if stats['cache_hit_rate'] < 0.5:
            report["recommendations"].append("Consider providing more comprehensive initial_values to StringCodec to reduce cache misses")
        
        if stats['individual_gpu_encodings'] > 100:
            report["recommendations"].append(f"High number of individual GPU encodings ({stats['individual_gpu_encodings']}) - consider batch processing")
            
        # Removed sentence transformer device check - string server handles encoding
            
        return report


# def runStringSaveLoadTest():
#
#     data = [
#         "hello world",
#         "foo",
#         "bar",
#     ]
#     print(data)
#
#     codec = StringCodec(50)
#     jj = codec.save()
#
#     tokenBatch = create_token_batch([codec.tokenize(x) for x in data])
#     print("tokenBatch:", tokenBatch)
#
#     preSave_encodedTokens = codec.encode(tokenBatch)
#     print("preSave_encodedTokens = ", preSave_encodedTokens)
#
#     # print(jj)
#
#     jj_enc_dim = jj.get("enc_dim")
#
#     codec = None  # remove from scope
#     tokenBatch = None
#
#     newCodec = StringCodec(jj_enc_dim)
#     newCodec.load(jj)
#     print(newCodec)
#
#     loadTokenBatch = create_token_batch([newCodec.tokenize(x) for x in data])
#     print("loadTokenBatch:", loadTokenBatch)
#
#     postLoad_encodedTokens = newCodec.encode(loadTokenBatch)
#
#     assert torch.equal(postLoad_encodedTokens, preSave_encodedTokens)
#
#     return


if __name__ == "__main__":
    from Token import create_token_batch, set_not_present, set_unknown

    d_embed = 50  # FIXME: somewhere this is defined.

    sc = StringCodec(enc_dim=d_embed)
    # print(sc.mlp_encoder)

    token = sc.tokenize(
        "hello world asdfas asdf a dfa df asd fas df adf asd fa sdf asdf a df adf "
    )
    # print("the real token:", token)
    token_not_present = set_not_present(token)
    token_unknown = set_unknown(token)

    tokens = create_token_batch([token, token_not_present, token_unknown])
    # print("tokens = ", tokens)
    # print("---")
    out = sc.encode(tokens)
    print("out = ", out)
    assert out.shape[0] == 3
    assert out.shape[1] == d_embed
    print(out.shape)

    # runStringSaveLoadTest()
