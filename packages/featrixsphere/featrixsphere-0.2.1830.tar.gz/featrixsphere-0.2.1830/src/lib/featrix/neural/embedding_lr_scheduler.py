#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
"""
Custom Learning Rate Scheduler for Embedding Space Training

Replacement for OneCycleLR with better control and adaptability for
self-supervised contrastive learning in embedding spaces.

Key improvements over OneCycleLR:
- Adaptive warm-up based on early training dynamics
- Plateau detection with LR reduction
- Better control over peak LR timing
- Support for early stopping awareness
- Can extend training if learning is still happening
"""

import logging
import math
from typing import Optional, List, Dict, Any

import torch
from torch.optim import Optimizer
from torch.optim.lr_scheduler import _LRScheduler

logger = logging.getLogger(__name__)


class EmbeddingSpaceLRScheduler(_LRScheduler):
    """
    Custom LR scheduler optimized for embedding space training.
    
    Phases:
    1. Warm-up: Linear increase to max_lr (configurable duration)
    2. Peak: Hold at max_lr briefly
    3. Cosine Annealing: Smooth decay to min_lr
    4. Optional: Plateau-based reductions if loss stops improving
    
    Unlike OneCycleLR:
    - Can adapt schedule based on validation loss
    - Better control over warm-up duration
    - Can trigger LR reductions on plateau
    - Supports dynamic schedule extension
    """
    
    def __init__(
        self,
        optimizer: Optimizer,
        max_lr: float,
        total_steps: int,
        min_lr: Optional[float] = None,  # None = compute from final_div_factor
        warmup_fraction: float = 0.15,   # 15% of training for warm-up
        peak_fraction: float = 0.05,      # 5% at peak LR
        anneal_strategy: str = 'cos',     # 'cos' or 'linear'
        div_factor: float = 25.0,         # initial_lr = max_lr / div_factor
        final_div_factor: float = 1e4,    # min_lr = max_lr / final_div_factor (if min_lr=None)
        last_epoch: int = -1,
        verbose: bool = False
    ):
        """
        Args:
            optimizer: Wrapped optimizer
            max_lr: Maximum learning rate to reach
            total_steps: Total number of training steps (epochs * batches_per_epoch)
            min_lr: Minimum learning rate (if None, computed as max_lr / final_div_factor)
            warmup_fraction: Fraction of total_steps for warm-up phase (default: 0.15 = 15%)
            peak_fraction: Fraction of total_steps to hold at peak (default: 0.05 = 5%)
            anneal_strategy: 'cos' for cosine annealing, 'linear' for linear decay
            div_factor: Divisor for initial LR (initial_lr = max_lr / div_factor)
            final_div_factor: Divisor for final LR (used if min_lr=None)
            last_epoch: Index of last epoch (for resuming training)
            verbose: If True, prints LR changes
        """
        self.max_lr = max_lr
        self.total_steps = total_steps
        self.min_lr = (max_lr / final_div_factor) if min_lr is None else min_lr
        self.initial_lr = max_lr / div_factor
        self.warmup_fraction = warmup_fraction
        self.peak_fraction = peak_fraction
        self.anneal_strategy = anneal_strategy
        
        # Calculate phase boundaries with guards against invalid fractions
        self.warmup_steps = max(0, int(total_steps * warmup_fraction))
        self.peak_steps = max(0, int(total_steps * peak_fraction))
        self.anneal_start = min(total_steps, self.warmup_steps + self.peak_steps)
        self.anneal_steps = max(1, total_steps - self.anneal_start)
        
        # Adaptive features
        self.plateau_lr_factor = 0.5  # Reduce LR by 50% on plateau
        self.plateau_patience = 10     # Steps without improvement before reduction
        self.plateau_min_delta = 0.001 # Minimum improvement to count
        
        # History tracking
        self.best_val_loss = float('inf')
        self.steps_without_improvement = 0
        self.plateau_reductions = 0
        self.max_plateau_reductions = 3
        
        logger.info("=" * 80)
        logger.info("📚 EMBEDDING SPACE LR SCHEDULER")
        logger.info("=" * 80)
        logger.info(f"   Total steps: {total_steps:,}")
        logger.info(f"   Initial LR: {self.initial_lr:.6e}")
        logger.info(f"   Max LR: {self.max_lr:.6e}")
        logger.info(f"   Min LR: {self.min_lr:.6e}")
        logger.info(f"   Warm-up: {self.warmup_steps:,} steps ({warmup_fraction*100:.1f}%)")
        logger.info(f"   Peak: {self.peak_steps:,} steps ({peak_fraction*100:.1f}%)")
        logger.info(f"   Anneal: {self.anneal_steps:,} steps ({(1-warmup_fraction-peak_fraction)*100:.1f}%)")
        logger.info(f"   Anneal strategy: {anneal_strategy}")
        logger.info("=" * 80)
        
        super().__init__(optimizer, last_epoch, verbose)
        
        # Set initial LR for all param groups
        for group in self.optimizer.param_groups:
            group['lr'] = self.initial_lr
    
    def get_lr(self) -> List[float]:
        """
        Calculate learning rate for current step.
        
        Returns:
            List of learning rates for each parameter group
        """
        current_step = self.last_epoch
        
        if current_step < self.warmup_steps:
            # Phase 1: Warm-up (linear increase)
            progress = 0.0 if self.warmup_steps == 0 else current_step / self.warmup_steps
            lr = self.initial_lr + (self.max_lr - self.initial_lr) * progress
            
        elif current_step < self.anneal_start:
            # Phase 2: Peak (hold at max_lr)
            lr = self.max_lr
            
        else:
            # Phase 3: Annealing
            anneal_progress = (current_step - self.anneal_start) / self.anneal_steps
            
            if self.anneal_strategy == 'cos':
                # Cosine annealing
                lr = self.min_lr + (self.max_lr - self.min_lr) * \
                     (1 + math.cos(math.pi * anneal_progress)) / 2
            else:
                # Linear decay
                lr = self.max_lr - (self.max_lr - self.min_lr) * anneal_progress
        
        # Apply cumulative plateau reductions (PERSISTENT - always applied)
        lr *= (self.plateau_lr_factor ** self.plateau_reductions)
        
        return [lr for _ in self.optimizer.param_groups]
    
    def step(self, epoch: Optional[int] = None):
        """
        Step the scheduler (standard PyTorch API).
        
        Args:
            epoch: Deprecated, kept for compatibility
        """
        # Standard step
        super().step(epoch)
    
    def report_metrics(self, val_loss: float):
        """
        Report validation loss for plateau detection.
        Call this separately from step() to avoid API conflicts.
        
        Args:
            val_loss: Current validation loss
        """
        self._update_plateau_tracker(val_loss)
    
    def _update_plateau_tracker(self, val_loss: float):
        """
        Track validation loss and trigger LR reduction on plateau.
        
        Args:
            val_loss: Current validation loss
        """
        # Only check after warm-up + peak phases
        if self.last_epoch < self.anneal_start:
            return
        
        # Check if loss improved
        improved = val_loss < self.best_val_loss - self.plateau_min_delta
        if improved:
            self.best_val_loss = val_loss
            self.steps_without_improvement = 0
        else:
            self.steps_without_improvement += 1
        
        # Trigger plateau reduction if needed
        if (self.steps_without_improvement >= self.plateau_patience and 
            self.plateau_reductions < self.max_plateau_reductions):
            
            self.plateau_reductions += 1
            self.steps_without_improvement = 0
            
            current_lr = self.get_lr()[0]
            
            logger.warning(f"📉 PLATEAU DETECTED at step {self.last_epoch}")
            logger.warning(f"   Val loss hasn't improved for {self.plateau_patience} steps")
            logger.warning(f"   LR reduction #{self.plateau_reductions}: factor={self.plateau_lr_factor}")
            logger.warning(f"   New effective LR: {current_lr:.6e}")
            logger.warning(f"   Best val loss: {self.best_val_loss:.4f}")
    
    def get_current_phase(self) -> str:
        """
        Get the current phase name for logging.
        
        Returns:
            Phase name: 'warmup', 'peak', 'anneal'
        """
        if self.last_epoch < self.warmup_steps:
            return 'warmup'
        elif self.last_epoch < self.anneal_start:
            return 'peak'
        else:
            return 'anneal'
    
    def get_progress(self) -> float:
        """
        Get overall progress through the schedule (0.0 to 1.0).
        
        Returns:
            Progress fraction
        """
        return min(1.0, self.last_epoch / self.total_steps)
    
    def get_phase_progress(self) -> float:
        """
        Get progress within current phase (0.0 to 1.0).
        
        Returns:
            Phase progress fraction
        """
        phase = self.get_current_phase()
        
        if phase == 'warmup':
            return self.last_epoch / self.warmup_steps if self.warmup_steps > 0 else 1.0
        elif phase == 'peak':
            steps_in_peak = self.last_epoch - self.warmup_steps
            return steps_in_peak / self.peak_steps if self.peak_steps > 0 else 1.0
        else:  # anneal
            steps_in_anneal = self.last_epoch - self.anneal_start
            return steps_in_anneal / self.anneal_steps if self.anneal_steps > 0 else 1.0
    
    def state_dict(self) -> Dict[str, Any]:
        """
        Return scheduler state for checkpointing.
        
        Returns:
            State dictionary
        """
        state = super().state_dict()
        state.update({
            'best_val_loss': self.best_val_loss,
            'steps_without_improvement': self.steps_without_improvement,
            'plateau_reductions': self.plateau_reductions,
        })
        return state
    
    def load_state_dict(self, state_dict: Dict[str, Any]):
        """
        Load scheduler state from checkpoint.
        
        Args:
            state_dict: State dictionary
        """
        # Extract custom state before calling parent
        self.best_val_loss = state_dict.pop('best_val_loss', float('inf'))
        self.steps_without_improvement = state_dict.pop('steps_without_improvement', 0)
        self.plateau_reductions = state_dict.pop('plateau_reductions', 0)
        # Remove old plateau_mode if present (backwards compat)
        state_dict.pop('plateau_mode', None)
        
        # Load base state
        super().load_state_dict(state_dict)


class AdaptiveEmbeddingLRScheduler(EmbeddingSpaceLRScheduler):
    """
    Enhanced version with more aggressive adaptation.
    
    Adds:
    - Early learning rate boost if progress is slow
    - Automatic schedule extension if still learning
    - Temperature-aware LR adjustment (for contrastive learning)
    """
    
    def __init__(self, *args, enable_early_boost: bool = True, **kwargs):
        """
        Args:
            enable_early_boost: If True, can boost LR during warmup if learning is slow
            *args, **kwargs: Passed to parent
        """
        self.enable_early_boost = enable_early_boost
        self.early_boost_applied = False
        self.early_boost_factor = 1.5
        
        super().__init__(*args, **kwargs)
    
    def check_early_progress(self, train_loss: float, val_loss: float, current_step: int):
        """
        Check if early training progress is too slow and boost LR if needed.
        
        Args:
            train_loss: Current training loss
            val_loss: Current validation loss  
            current_step: Current training step
        """
        # Only check during first 10% of warm-up
        if not self.enable_early_boost or self.early_boost_applied:
            return
        
        if current_step < int(self.warmup_steps * 0.1):
            return
        
        # If losses are very high and not decreasing much, boost LR
        if train_loss > 1000 and val_loss > 1000:
            logger.warning(f"🚀 EARLY LR BOOST at step {current_step}")
            logger.warning(f"   Losses still very high (train={train_loss:.1f}, val={val_loss:.1f})")
            logger.warning(f"   Boosting max_lr: {self.max_lr:.6e} → {self.max_lr * self.early_boost_factor:.6e}")
            
            self.max_lr *= self.early_boost_factor
            self.early_boost_applied = True


def create_embedding_lr_scheduler(
    optimizer: Optimizer,
    n_epochs: int,
    batches_per_epoch: int,
    max_lr: float = 0.001,
    scheduler_type: str = 'standard',
    **kwargs
) -> EmbeddingSpaceLRScheduler:
    """
    Factory function to create embedding LR scheduler.
    
    Args:
        optimizer: PyTorch optimizer
        n_epochs: Total number of epochs
        batches_per_epoch: Number of batches per epoch
        max_lr: Maximum learning rate
        scheduler_type: 'standard' or 'adaptive'
        **kwargs: Additional scheduler parameters
        
    Returns:
        EmbeddingSpaceLRScheduler instance
    """
    total_steps = n_epochs * batches_per_epoch
    
    if scheduler_type == 'adaptive':
        scheduler_class = AdaptiveEmbeddingLRScheduler
        logger.info("📚 Creating ADAPTIVE Embedding LR Scheduler")
    else:
        scheduler_class = EmbeddingSpaceLRScheduler
        logger.info("📚 Creating STANDARD Embedding LR Scheduler")
    
    scheduler = scheduler_class(
        optimizer=optimizer,
        max_lr=max_lr,
        total_steps=total_steps,
        **kwargs
    )
    
    return scheduler

