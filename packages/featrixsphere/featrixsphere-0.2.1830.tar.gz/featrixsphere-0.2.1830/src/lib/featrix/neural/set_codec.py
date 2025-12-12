#
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
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
import os
import pickle
import traceback
import sys
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

from .device import device
from featrix.neural.embedding_utils import NormalizedEmbedding
from featrix.neural.featrix_token import Token
from featrix.neural.featrix_token import TokenStatus
from featrix.neural.model_config import ColumnType
from featrix.neural.model_config import SetEncoderConfig
from featrix.neural.string_codec import STRING_DIM
from featrix.neural.simple_mlp import SimpleMLP
from featrix.neural.simple_mlp import SimpleMLPConfig

logger = logging.getLogger(__name__)


class FocalLoss(nn.Module):
    """
    Focal Loss for addressing class imbalance in classification tasks.
    
    Focal Loss down-weights easy examples and focuses learning on hard examples.
    This is particularly effective for extreme class imbalance where standard
    cross-entropy (even with class weights) fails.
    
    Paper: "Focal Loss for Dense Object Detection" (Lin et al., 2017)
    https://arxiv.org/abs/1708.02002
    
    Args:
        alpha: Class weights tensor (optional). Should be same shape as number of classes.
        gamma: Focusing parameter. Higher values focus more on hard examples.
               gamma=0 reduces to standard cross-entropy.
               gamma=2 is recommended in the paper.
        min_weight: Minimum weight for easy examples (default=0.1).
                   Ensures correct predictions still get some credit.
    
    Example:
        For a 97% vs 3% class imbalance with gamma=2, min_weight=0.1:
        - Easy examples (97% confident) get weight max(0.1, (1-0.97)^2) = 0.1
        - Hard examples (60% confident) get weight (1-0.60)^2 = 0.16
        This gives 1.6x more weight to hard examples while still rewarding easy examples!
    """
    def __init__(self, alpha=None, gamma=2.0, min_weight=0.1):
        super().__init__()
        self.alpha = alpha  # class weights (tensor)
        self.gamma = gamma  # focusing parameter (higher = more focus on hard examples)
        self.min_weight = min_weight  # minimum weight for easy examples
    
    def forward(self, inputs, targets):
        """
        Args:
            inputs: Raw logits from model (batch_size, num_classes)
            targets: Ground truth class indices (batch_size,)
        
        Returns:
            Mean focal loss across the batch
        """
        # CRITICAL: Ensure inputs and targets are on the same device
        # This can happen if string codecs moved tokens to CPU but targets are still on GPU
        # OR if prediction is on CPU but targets are on GPU
        if inputs.device != targets.device:
            # Move targets to match inputs device (prediction's device)
            original_target_device = targets.device
            targets = targets.to(inputs.device)
            # Don't log device moves - too noisy
        
        # Compute cross entropy loss (per sample, not reduced)
        ce_loss = F.cross_entropy(inputs, targets, reduction='none', weight=self.alpha)
        
        # Get probability of the correct class
        # pt is the model's confidence in the correct class
        pt = torch.exp(-ce_loss)
        
        # Focal loss formula: FL = max(min_weight, (1 - pt)^gamma) * CE
        # When pt is high (easy example), clamp to min_weight → still get some credit
        # When pt is low (hard example), (1-pt)^gamma is large → up-weight
        focal_weight = torch.clamp((1 - pt) ** self.gamma, min=self.min_weight)
        focal_loss = focal_weight * ce_loss
        
        # Always use mean - that's the only thing that makes sense
        return focal_loss.mean()


class SetEncoder(nn.Module):
    def __init__(self, config: SetEncoderConfig, string_cache=None, member_names=None, column_name=None):
        super().__init__()
        self.config = config
        self.string_cache = string_cache
        # Store cache filename for reconnection after unpickling
        if string_cache is not None and hasattr(string_cache, 'filename'):
            self._string_cache_filename = string_cache.filename
        else:
            self._string_cache_filename = None
        self.member_names = member_names or []
        self.column_name = column_name  # NEW: column name for semantic initialization
        
        # Build name-to-index mapping for OOV handling
        self.name_to_idx = {str(name): idx for idx, name in enumerate(self.member_names)} if self.member_names else {}

        # CRITICAL FIX: Better parameter initialization to prevent NaN corruption
        # Use Xavier uniform initialization instead of random normal
        self._replacement_embedding = nn.Parameter(torch.zeros(config.d_model))
        nn.init.xavier_uniform_(self._replacement_embedding.unsqueeze(0))
        self._replacement_embedding.data = self._replacement_embedding.data.squeeze(0)
        
        # LEARNED EMBEDDINGS: Standard nn.Embedding (learns from data)
        self.embedding = nn.Embedding(config.n_members, config.d_model)
        nn.init.xavier_uniform_(self.embedding.weight)
        
        # ADAPTIVE MIXTURE: Enable semantic embeddings if available
        # We'll create a learnable mixture between learned embeddings and BERT semantics
        # ALWAYS enable if we have string_cache and member_names (make all SetEncoders adaptive)
        from featrix.neural.sphere_config import get_config
        # Enable semantic mixture if we have the prerequisites (string_cache and member_names)
        # The config flag can disable it, but by default we try to enable it
        config_enabled = get_config().use_semantic_set_initialization()
        self.use_semantic_mixture = (config_enabled and 
                                      string_cache is not None and 
                                      member_names and
                                      len(member_names) > 0)
        
        if self.use_semantic_mixture:
            logger.info(f"🎨 Enabling ADAPTIVE mixture: learned embeddings + BERT semantics")
            
            # Create projection layer for BERT embeddings
            self.bert_projection = nn.Linear(STRING_DIM, config.d_model, bias=False)
            nn.init.xavier_uniform_(self.bert_projection.weight, gain=0.5)
            
            # Pre-compute BERT embeddings for all known members
            self.bert_embeddings = self._precompute_bert_embeddings()
            logger.info(f"   ✅ Pre-computed {len(self.bert_embeddings)}/{len(member_names)} BERT embeddings")
            
            # Learnable mixing weight: decides between learned vs semantic embeddings
            # Initialize with config value or small random value (not zero) to break symmetry
            # Positive logit → prefer learned, negative logit → prefer semantic
            if config.initial_mixture_logit is not None:
                # Use configured initial value
                initial_logit = config.initial_mixture_logit
                logger.info(f"   🎯 Using configured initial mixture logit: {initial_logit:.4f}")
            else:
                # Default: small random value around 0 (near 50/50 mixture)
                initial_logit = torch.randn(1).item() * 0.1
                logger.info(f"   🎯 Using random initial mixture logit: {initial_logit:.4f}")
            
            self.mixture_logit = nn.Parameter(torch.tensor([initial_logit], dtype=torch.float32))
            
            # Epoch tracking for logging (updated by EmbeddingSpace during training)
            self.register_buffer('_epoch_counter', torch.tensor(0, dtype=torch.long))
            self.register_buffer('_total_epochs', torch.tensor(100, dtype=torch.long))  # Will be updated
            self.register_buffer('_last_logged_epoch', torch.tensor(-1, dtype=torch.long))  # Track last logged epoch to avoid batch spam
            
            # WARM START: Try column+value initialization first (better context), fallback to BERT-only
            if column_name:
                initialized = self._init_from_column_and_values(column_name, member_names)
                if initialized > 0:
                    logger.info(f"   🌟 Warm-started {initialized}/{len(member_names)} learned embeddings from column+value context")
                else:
                    # Fallback to BERT-only if column+value fails
                    initialized = self._init_from_bert()
                    logger.info(f"   🌟 Warm-started {initialized}/{len(member_names)} learned embeddings from BERT")
            else:
                # No column name, use BERT-only
                initialized = self._init_from_bert()
                logger.info(f"   🌟 Warm-started {initialized}/{len(member_names)} learned embeddings from BERT")
        else:
            self.bert_projection = None
            self.bert_embeddings = None
            self.mixture_logit = None
            
            # Legacy path: one-time semantic initialization without mixture
            if get_config().use_semantic_set_initialization() and string_cache is not None and member_names:
                logger.info(f"🎨 Legacy: One-time semantic initialization (no adaptive mixture)")
                initialized = self._init_from_string_cache()
                logger.info(f"   ✅ Initialized {initialized}/{len(member_names)} set embeddings semantically")
                
                # Create projection for OOV handling at inference only
                self.bert_projection = nn.Linear(STRING_DIM, config.d_model, bias=False)
                nn.init.xavier_uniform_(self.bert_projection.weight, gain=0.5)
        
        # SPARSITY-AWARE GRADIENT SCALING
        if config.sparsity_ratio > 0.01:
            min_scale = 0.1
            gradient_scale = max(1.0 - config.sparsity_ratio, min_scale)
            
            def _scale_replacement_grad(grad):
                """Scale gradient to compensate for frequency imbalance"""
                return grad * gradient_scale
            
            self._replacement_embedding.register_hook(_scale_replacement_grad)
            
            logger.info(
                f"⚖️  Sparsity-aware gradient scaling ENABLED: "
                f"sparsity={config.sparsity_ratio:.1%}, "
                f"gradient_scale={gradient_scale:.2f}"
            )
    
    def _precompute_bert_embeddings(self):
        """Pre-compute and cache BERT embeddings for all known members"""
        if not self.string_cache or not self.member_names:
            return {}
        
        bert_cache = {}
        for idx, member_name in enumerate(self.member_names):
            bert_emb = self.string_cache.get_embedding_from_cache(str(member_name))
            if bert_emb is not None:
                # Project to d_model and store
                with torch.no_grad():
                    # Use detach().clone() to avoid warning when copying from tensor
                    if isinstance(bert_emb, torch.Tensor):
                        bert_tensor = bert_emb.detach().clone().to(dtype=torch.float32, device=self._replacement_embedding.device)
                    else:
                        bert_tensor = torch.tensor(bert_emb, dtype=torch.float32, device=self._replacement_embedding.device)
                    projected = self.bert_projection(bert_tensor.unsqueeze(0))
                    bert_cache[idx] = projected.squeeze(0)
        
        return bert_cache
    
    def _init_from_bert(self):
        """Warm-start learned embeddings with BERT vectors (for adaptive mixture)"""
        if not self.bert_embeddings:
            return 0
        
        initialized_count = 0
        for idx, bert_embedding in self.bert_embeddings.items():
            with torch.no_grad():
                self.embedding.weight[idx] = bert_embedding.clone()
            initialized_count += 1
        
        return initialized_count
    
    def _init_from_column_and_values(self, column_name, member_names):
        """
        Initialize embeddings using BERT(column_name) + BERT(value).
        
        This gives each embedding TWO pieces of context:
        1. What column it belongs to (e.g., "business_type")
        2. What value it represents (e.g., "Auto Transport")
        
        Result: "yes" in "is_active" is different from "yes" in "approved" 
        because the column context differs.
        """
        if not self.string_cache or not member_names:
            return 0
        
        # Get column name embedding once (reused for all members)
        column_emb = None
        if column_name:
            column_emb = self.string_cache.get_embedding_from_cache(str(column_name))
        
        # Create MLP to project concatenated embeddings → d_model
        string_dim = STRING_DIM
        # Input is column_emb + value_emb (concatenated)
        input_dim = string_dim * 2 if column_emb is not None else string_dim
        hidden_dim = max(64, self.config.d_model // 2)
        
        temp_mlp = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, self.config.d_model)
        )
        
        # Initialize MLP weights
        for layer in temp_mlp:
            if isinstance(layer, nn.Linear):
                nn.init.xavier_uniform_(layer.weight, gain=0.5)
                if hasattr(layer, 'bias') and layer.bias is not None:
                    nn.init.zeros_(layer.bias)
        
        # Move temp_mlp to same device as embedding
        device = self.embedding.weight.device
        temp_mlp = temp_mlp.to(device)
        
        column_tensor = None
        if column_emb is not None:
            # Keep on CPU for DataLoader workers
            column_tensor = torch.tensor(column_emb, dtype=torch.float32)
        
        initialized_count = 0
        for idx, member_name in enumerate(member_names):
            # Get value embedding from cache
            value_emb = self.string_cache.get_embedding_from_cache(str(member_name))
            
            if value_emb is not None:
                # Keep on CPU for DataLoader workers
                value_tensor = torch.tensor(value_emb, dtype=torch.float32)
                
                # Concatenate column + value embeddings
                if column_tensor is not None:
                    combined = torch.cat([column_tensor, value_tensor]).unsqueeze(0)
                else:
                    combined = value_tensor.unsqueeze(0)
                
                # Project through MLP to d_model
                with torch.no_grad():
                    projected = temp_mlp(combined)
                    self.embedding.weight[idx] = projected.squeeze(0)
                
                initialized_count += 1
        
        return initialized_count

    @property
    def unknown_embedding(self):
        # FIXME: what was the rationale for unknown embeddings again?
        return nn.functional.normalize(self._replacement_embedding, dim=-1)

    @property
    def marginal_embedding(self):
        # We return the same vector as NOT_PRESENT token because they are treated the
        # same from a probabilistic point of view by the network, and should be treated
        # the same when the model is queried.
        # However, they must remain distinct tokens because the masking strategy for the loss
        # function is affected by whether a field is NOT_PRESENT, or MARGINAL.
        return nn.functional.normalize(self._replacement_embedding, dim=-1)

    @property
    def not_present_embedding(self):
        return nn.functional.normalize(self._replacement_embedding, dim=-1)

    def forward(self, token):
        # EMERGENCY FIX: Convert float to long for embedding layer
        value = token.value
        if value.dtype == torch.float32:
            value = value.long()
        
        # CRITICAL: Ensure value is on the same device as module parameters
        # Respect FEATRIX_FORCE_CPU_SINGLE_PREDICTOR env var - force CPU if set
        force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
        
        # Get device from embedding layer
        module_device = None
        if not force_cpu:
            try:
                module_device = next(self.embedding.parameters()).device
            except (StopIteration, AttributeError):
                pass
        
        # Force CPU mode if env var is set
        if force_cpu:
            module_device = torch.device('cpu')
            if list(self.parameters()):
                first_param_device = next(self.parameters()).device
                if first_param_device.type != 'cpu':
                    self.cpu()
        
        # Move value to module device if there's a mismatch
        if module_device is not None and value.device != module_device:
            value = value.to(device=module_device)
        
        # Create new token with modified value (Token.value is read-only)
        token = Token(
            value=value,
            status=token.status,
            attention_mask=token.attention_mask if hasattr(token, 'attention_mask') else None
        )
        
        # Get learned embeddings
        learned_embed = self.embedding(token.value)  # [batch_size, d_model]
        
        # ADAPTIVE MIXTURE: Mix learned and semantic embeddings if enabled
        if self.use_semantic_mixture and self.bert_embeddings:
            # Get BERT embeddings for this batch
            batch_size = token.value.shape[0]
            bert_embed = torch.zeros_like(learned_embed)  # [batch_size, d_model]
            
            # Track BERT coverage for logging
            bert_available_count = 0
            for batch_idx in range(batch_size):
                member_idx = token.value[batch_idx].item()
                if member_idx in self.bert_embeddings:
                    bert_embed[batch_idx] = self.bert_embeddings[member_idx]
                    bert_available_count += 1
                else:
                    # If BERT embedding not available, use learned embedding
                    bert_embed[batch_idx] = learned_embed[batch_idx].detach()
            
            # Compute mixture weight: sigmoid(logit) → [0, 1]
            # weight close to 1 → trust learned embeddings
            # weight close to 0 → trust semantic (BERT) embeddings
            mixture_weight = torch.sigmoid(self.mixture_logit)  # scalar [0, 1]
            learned_pct = mixture_weight.item() * 100
            semantic_pct = (1 - mixture_weight.item()) * 100
            
            # LOG MIXTURE ATTEMPTS: Show what's being tried
            if self.training and not hasattr(self, '_mixture_attempts_logged'):
                logger.info(f"🔍 SetEncoder ({self.column_name or 'unknown'}): Trying adaptive mixture")
                logger.info(f"   📊 BERT embeddings available: {bert_available_count}/{batch_size} in this batch")
                logger.info(f"   🎯 Mixture logit: {self.mixture_logit.item():.4f}")
                logger.info(f"   📈 Initial mixture: {learned_pct:.1f}% Learned, {semantic_pct:.1f}% Semantic (BERT)")
                logger.info(f"   💡 Positive logit → prefer Learned, Negative logit → prefer Semantic")
                self._mixture_attempts_logged = True
            
            # Mix embeddings
            embed = mixture_weight * learned_embed + (1 - mixture_weight) * bert_embed
            
            # ENTROPY REGULARIZATION: Encourage decisive mixing (not 50/50)
            # This pushes mixture_weight away from 0.5 toward 0 or 1
            if self.training:
                # Binary entropy: H = -p*log(p) - (1-p)*log(1-p)
                # Maximum at p=0.5, minimum at p=0 or p=1
                p = mixture_weight
                entropy = -(p * torch.log(p + 1e-10) + (1-p) * torch.log(1-p + 1e-10))
                # Penalize high entropy (encourage sharp decisions)
                entropy_loss = 0.1 * entropy
                # Store for logging
                if not hasattr(self, '_last_entropy'):
                    self._last_entropy = entropy.item()
                    self._last_mixture_weight = mixture_weight.item()
                else:
                    self._last_entropy = 0.9 * self._last_entropy + 0.1 * entropy.item()
                    self._last_mixture_weight = 0.9 * self._last_mixture_weight + 0.1 * mixture_weight.item()
                
                # Log mixture evolution once per epoch (like other encoders)
                current_epoch = self._epoch_counter.item()
                if current_epoch != self._last_logged_epoch.item():
                    col_name_display = self.column_name or "unknown"
                    
                    # Track logit changes across epochs
                    if not hasattr(self, '_previous_logit'):
                        self._previous_logit = self.mixture_logit.item()
                        logit_change = 0.0
                    else:
                        logit_change = self.mixture_logit.item() - self._previous_logit
                        self._previous_logit = self.mixture_logit.item()
                    
                    # Check if mixture_logit has gradients (should always have requires_grad=True)
                    has_grad = self.mixture_logit.requires_grad
                    grad_norm = None
                    if has_grad and self.mixture_logit.grad is not None:
                        grad_norm = self.mixture_logit.grad.item()
                    
                    # Log with gradient info
                    log_msg = (f"   🔄 Epoch {current_epoch} - SetEncoder '{col_name_display}': "
                              f"Mixture={learned_pct:.1f}%LRN/{semantic_pct:.1f}%SEM, "
                              f"Logit={self.mixture_logit.item():.4f} (Δ={logit_change:+.4f}), "
                              f"Entropy={entropy.item():.4f}")
                    if grad_norm is not None:
                        log_msg += f", Grad={grad_norm:.6f}"
                    logger.info(log_msg)
                    
                    # Mark this epoch as logged
                    self._last_logged_epoch.fill_(current_epoch)
                
                # Store entropy loss so it can be collected and added to total loss
                # This encourages sharper mixture selection (prefer either LRN or SEM, not 50/50)
                self._current_entropy_loss = entropy_loss
            else:
                # Not training - clear entropy loss
                self._current_entropy_loss = None
        else:
            # No adaptive mixture - use learned embeddings only
            self._current_entropy_loss = None
            if self.training and not hasattr(self, '_no_mixture_logged'):
                logger.info(f"🔍 SetEncoder ({self.column_name or 'unknown'}): Using learned embeddings only (no semantic mixture)")
                logger.info(f"   Reason: use_semantic_mixture={self.use_semantic_mixture}, "
                          f"bert_embeddings={'available' if self.bert_embeddings else 'None'}")
                self._no_mixture_logged = True
            embed = learned_embed
        
        # OOV HANDLING: Use BERT projection for unknown values (legacy path)
        if not self.use_semantic_mixture and self.bert_projection is not None:
            unknown_mask = (token.status == TokenStatus.UNKNOWN)
            
            if unknown_mask.any() and self.string_cache is not None and hasattr(token, 'original_string'):
                for idx in unknown_mask.nonzero(as_tuple=True)[0]:
                    original_value = token.original_string[idx] if hasattr(token, 'original_string') else None
                    if original_value:
                        bert_emb = self.string_cache.get_embedding_from_cache(str(original_value))
                        if bert_emb is not None:
                            with torch.no_grad():
                                # Use detach().clone() to avoid warning when copying from tensor
                                if isinstance(bert_emb, torch.Tensor):
                                    bert_tensor = bert_emb.detach().clone().to(dtype=torch.float32)
                                else:
                                    bert_tensor = torch.tensor(bert_emb, dtype=torch.float32)
                                projected = self.bert_projection(bert_tensor.unsqueeze(0))
                                embed[idx] = projected.squeeze(0)
                            token.status[idx] = TokenStatus.OK
        
        # Override embeddings for unknown and not present tokens
        embed[token.status == TokenStatus.NOT_PRESENT] = self._replacement_embedding
        embed[token.status == TokenStatus.UNKNOWN] = self._replacement_embedding
        embed[token.status == TokenStatus.MARGINAL] = self._replacement_embedding
        
        # CONDITIONAL NORMALIZATION based on config
        if self.config.normalize_output:
            short_vec = nn.functional.normalize(embed[:, 0:3], dim=1)
            full_vec = nn.functional.normalize(embed, dim=1)
        else:
            short_vec = embed[:, 0:3]
            full_vec = embed
        
        return short_vec, full_vec
    
    def __getstate__(self):
        """Exclude string_cache from pickling (contains non-picklable sqlite3.Connection)"""
        state = self.__dict__.copy()
        state.pop("string_cache", None)
        return state
    
    def __setstate__(self, state):
        """Restore state and reconnect to global string cache"""
        self.__dict__.update(state)
        
        # CRITICAL: Move to CPU if in CPU mode (embedding table might be on GPU)
        import os
        force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
        if force_cpu:
            if hasattr(self, 'embedding') and self.embedding is not None:
                if list(self.embedding.parameters()):
                    embedding_device = next(self.embedding.parameters()).device
                    if embedding_device.type == 'cuda':
                        logger.info(f"📊 SetEncoder '{self.column_name}': embedding table on GPU - moving to CPU")
                        self.cpu()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        # Reconnect to the global string cache if we have a filename
        if hasattr(self, '_string_cache_filename') and self._string_cache_filename:
            try:
                from featrix.neural.string_codec import get_global_string_cache
                self.string_cache = get_global_string_cache(
                    cache_filename=self._string_cache_filename,
                    initial_values=[],  # Global cache already has the data
                    debug_name=self.column_name or 'restored_set_encoder'
                )
            except Exception as e:
                logger.warning(f"⚠️ Failed to reconnect SetEncoder to global cache: {e}")
                self.string_cache = None
        else:
            self.string_cache = None

    @staticmethod
    def get_default_config(d_model: int, n_members: int, sparsity_ratio: float = 0.0, initial_mixture_logit: Optional[float] = None):
        """Initialize the encoder with default parameters for the neural network.
        
        Args:
            d_model: Embedding dimension
            n_members: Number of set members
            sparsity_ratio: Ratio of null/missing values (0.0 = dense, 1.0 = all null)
            initial_mixture_logit: Initial value for mixture logit (None = random small value ~0.1)
                                  Positive → prefer learned embeddings
                                  Negative → prefer semantic (BERT) embeddings
                                  0.0 = 50/50 mixture, +1.0 ≈ 73% learned, -1.0 ≈ 27% learned
        """
        # Import here to avoid circular import
        from .sphere_config import get_config
        
        # Get normalization setting from global config
        normalize_column_encoders = get_config().get_normalize_column_encoders()
        
        return SetEncoderConfig(
            d_model=d_model,
            n_members=n_members,
            normalize_output=normalize_column_encoders,  # Config-controlled normalization
            sparsity_ratio=sparsity_ratio,  # Pass sparsity for gradient scaling
            initial_mixture_logit=initial_mixture_logit  # Pass initial mixture logit if provided
        )


class SetCodec(nn.Module):
    def __init__(self, members: set, enc_dim: int, remove_nan=True, class_weights=None, loss_type="cross_entropy", sparsity_ratio=0.0, string_cache=None):
        super().__init__()
        self._is_decodable = True

        self.members = members
        self.sparsity_ratio = sparsity_ratio  # Store sparsity ratio for later use
        self.string_cache = string_cache  # Store string cache path for semantic initialization
        if remove_nan:
            self.members.discard("nan")
            self.members.discard("NaN")
            self.members.discard("Nan")
            self.members.discard("NAN")
            self.members.discard("None")        # null, NULL, nil
            # empty strings - not sure if it's a great idea to include them here
            self.members.discard("")
            self.members.discard(" ")

            for x in self.members:
                try:
                    if str(x).strip() == "":
                        self.members.discard(x)
                except Exception:
                    traceback.print_exc(file=sys.stdout)
                    print("... continuing")

        # Sorting ensures that two encoders created using the same set will
        # have the same mapping from members to tokens.
        uniques = sorted(list(self.members))
        uniques = ["<UNKNOWN>"] + uniques
        # Need to re-compute the set members, after adding <UNKNOWN>
        # TODO: this seems very hacky.
        self.members = set(uniques)
        self.n_members = len(self.members)

        self.enc_dim = enc_dim
        self.members_to_tokens = {member: token for token, member in enumerate(uniques)}
        self.tokens_to_members = {
            token: member for member, token in self.members_to_tokens.items()
        }
        # Store member names (excluding <UNKNOWN>) for semantic initialization
        self.member_names = [m for m in uniques if m != "<UNKNOWN>"]
        
        # DIAGNOSTIC: Log the token mapping for debugging backwards learning
        logger.info(f"🔍 SET CODEC TOKEN MAPPING:")
        for member, token in sorted(self.members_to_tokens.items(), key=lambda x: x[1]):
            logger.info(f"   Token {token} → '{member}'")

        # Create loss function with optional class weighting
        # loss_type can be "focal" or "cross_entropy"
        # FocalLoss: Better for single predictor training with imbalanced classes
        # CrossEntropyLoss: More stable for embedding space training
        if loss_type == "focal":
            # For single predictor, use min_weight=0.1 so correct negatives still get credit
            focal_min_weight = 0.1
            if class_weights is not None:
                self.loss_fn = FocalLoss(alpha=class_weights, gamma=2.0, min_weight=focal_min_weight)
            else:
                self.loss_fn = FocalLoss(alpha=None, gamma=2.0, min_weight=focal_min_weight)
            logger.info(f"🎯 SetCodec using FocalLoss (gamma=2.0, min_weight={focal_min_weight})")
        elif loss_type == "cross_entropy":
            # We have never used the class_weights before...
            # if class_weights is not None:
            #     self.loss_fn = nn.CrossEntropyLoss(weight=class_weights)
            # else:
            self.loss_fn = nn.CrossEntropyLoss()
            logger.info(f"🎯 SetCodec using CrossEntropyLoss")
        else:
            raise ValueError(f"Unknown loss_type '{loss_type}'. Expected 'focal' or 'cross_entropy'.")

    def get_codec_name(self):
        return ColumnType.SET

    def get_codec_info(self):
        d = {"num_uniques": len(self.members), 
             "enc_dim": self.enc_dim}
        if len(self.members) <= 50:
            d['uniques'] = self.members
        return d

    def get_not_present_token(self):
        return Token(
            value=0,
            status=TokenStatus.NOT_PRESENT,  # torch.tensor([TokenStatus.NOT_PRESENT] * 1),
        )
    
    def get_marginal_token(self):
        """Return a token representing a masked/marginal value for reconstruction testing."""
        return Token(
            value=0,  # Value doesn't matter for MARGINAL tokens
            status=TokenStatus.MARGINAL,
        )

    def get_visualization_domain(self, _min=None, _max=None, _steps=40):
        # ignore inputs for now.
        # We could maybe use _steps to reduce a big set somehow?
        #
        the_members = [
            self.detokenize(Token(value=i, status=TokenStatus.OK))
            for i in range(len(self.members))
        ]

        return the_members

    @property
    def token_dtype(self):
        return int

    def tokenize(self, member):
        # TODO: must be able to tokenize an entire batch in a single go, and return
        # a batch token.

        # TODO:
        try:
            member = str(member)
        except Exception:
            return Token(
                value=torch.tensor(0, dtype=torch.float32),
                status=TokenStatus.UNKNOWN,
            )

        if member in self.members_to_tokens:
            return Token(
                value=torch.tensor(self.members_to_tokens[member], dtype=torch.float32),
                status=TokenStatus.OK,
            )
        else:
            # check for a blasted float. -- we need to solve this upstream when we're creating the tokenizer. But we also should probably handle basic mix/matches like uppercase/lowercase...
            # ... and whitespace trimming...
            if member + ".0" in self.members_to_tokens:
                return Token(
                    value=torch.tensor(self.members_to_tokens[member + ".0"], dtype=torch.float32),
                    status=TokenStatus.OK,
                )

            return Token(
                # the member does not matter for UNKNOWN status, but it's got to
                # be something that does not throw an error when passed to the embedding
                # module, because we embed first, and then overwrite with UNKNOWN vector.
                value=torch.tensor(0, dtype=torch.float32),
                status=TokenStatus.UNKNOWN,
            )

    def detokenize(self, token):
        # ToDO: it should really be a batch of tokens that we take in.
        if (
            token.status == TokenStatus.NOT_PRESENT
            or token.status == TokenStatus.UNKNOWN
        ):
            raise ValueError(f"Cannot detokenize a token with status {token.status}.")
        else:
            if token.value in self.tokens_to_members:
                return self.tokens_to_members[token.value]
            else:
                raise ValueError(f"Cannot decode token with value {token.value}.")

    def loss(self, logits, targets):
        return self.loss_fn(logits, targets)

    def loss_single(self, logits, target):
        # Loss function specific to batches of size one, and single targets.

        # We assume that target can be the wrong type, because it's type depends on the
        # types of other target variables it's batched with, and that it's provided as a
        # single value. Therefore, it must be cast to the correct type, and a dimension
        # must be added via `unsqueeze`.
        target = target.long().unsqueeze(dim=0)

        return self.loss(logits, target)

    def save(self):
        # we create a json dict.
        buffer = io.BytesIO()
        torch.save(self.state_dict(), buffer)

        buffer_b64 = "base64:" + str(
            base64.standard_b64encode(buffer.getvalue()).decode("utf8")
        )
        checksum = hashlib.md5(buffer.getvalue()).hexdigest()
        enc_bytes = pickle.dumps(self.members)
        members_b64 = "base64:" + str(
            base64.standard_b64encode(enc_bytes).decode("utf8")
        )

        d = {
            "type": "SetCodec",
            "embedding": buffer_b64,
            "embedding_checksum": checksum,
            "enc_dim": self.enc_dim,
            "members": members_b64,
        }

        return d

    def load(self, j):
        d_type = j.get("type")
        assert d_type == "SetCodec", "wrong load method called for __%s__" % d_type
        self.enc_dim = j.get("enc_dim")

        ########################
        # Set up members/uniques
        ########################
        members = j.get("members")
        assert members.startswith("base64:")
        members = members[6:]

        try:
            # theEncoder is a string 'b'<>'' ... sigh
            # print("members = __%s__" % members)
            e64 = base64.standard_b64decode(members)  # uniques[2:-1])
            unpickledEncoder = pickle.loads(e64)  # pickleBytes.read())
            # print("unpickledEncoder = ", unpickledEncoder)
            self.members = unpickledEncoder  # encoders[key] = unpickledEncoder
        except Exception:
            print(f"PICKLE ERROR for = __{j}__")
            traceback.print_exc()

        # copied from constructor
        uniques = sorted(list(self.members))
        self.members_to_tokens = {member: token for token, member in enumerate(uniques)}
        self.tokens_to_members = {
            token: member for member, token in self.members_to_tokens.items()
        }

        ########################
        # Set up embedding stuff
        ########################
        embed = j.get("embedding")
        embed_checksum = j.get("embedding_checksum")

        if embed.startswith("base64:"):
            embed = embed[6:]

        r64 = base64.standard_b64decode(embed)
        r_checksum64 = hashlib.md5(r64).hexdigest()

        if r_checksum64 != embed_checksum:
            print(f"CHECKSUMS {r_checksum64} and {embed_checksum} DO NOT MATCH - !")
            return

        buffer = io.BytesIO(r64)
        theDict = torch.load(buffer, weights_only=False)
        # print("theDict = ", theDict)

        # Without the below 'initializations', the load_state_dict() fails due to Size mismatches.
        self._unknown_embedding = nn.Parameter(torch.randn(self.enc_dim))
        self.register_buffer("not_present", torch.zeros(self.enc_dim))
        self.embedding = NormalizedEmbedding(len(uniques), self.enc_dim)
        self.load_state_dict(theDict)
        return


def runTest():
    colors = ["blue", "red", "green"]

    # Save what we make.
    codec = SetCodec(set(colors), enc_dim=50)
    jj = codec.save()
    print(jj)

    # Load what we saved.
    newCodec = SetCodec(set([]), enc_dim=50)
    newCodec.load(jj)

    assert newCodec.members == codec.members
    assert newCodec.enc_dim == codec.enc_dim
    assert torch.equal(newCodec.unknown, codec.unknown)
    assert torch.equal(newCodec.embedding.embed.weight, codec.embedding.embed.weight)
    print("PASS!")
    #    print(newCodec.members)
    return


if __name__ == "__main__":
    runTest()
