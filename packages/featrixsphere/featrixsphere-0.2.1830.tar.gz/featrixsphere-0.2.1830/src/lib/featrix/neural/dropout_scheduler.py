#!/usr/bin/env python3
"""
DropoutScheduler for dynamic dropout rate adjustment during training.

Supports multiple scheduling strategies to improve model regularization
and training dynamics.
"""

import math
import logging
from typing import Optional, Union, List
from enum import Enum

import torch
import torch.nn as nn

logger = logging.getLogger(__name__)


class DropoutScheduleType(Enum):
    """Types of dropout scheduling strategies."""
    CONSTANT = "constant"           # Fixed dropout rate
    LINEAR_DECAY = "linear_decay"   # Linear decrease over time
    COSINE_DECAY = "cosine_decay"   # Cosine annealing decrease
    STEP_DECAY = "step_decay"       # Step-wise decrease
    ADAPTIVE = "adaptive"           # Based on validation loss trends
    PIECEWISE_CONSTANT = "piecewise_constant"  # Hold high, ramp down, hold moderate


class DropoutScheduler:
    """
    Dynamic dropout scheduler for neural network training.
    
    Supports multiple scheduling strategies to adapt dropout rates
    during training for improved regularization.
    """
    
    def __init__(
        self,
        schedule_type: Union[str, DropoutScheduleType] = DropoutScheduleType.LINEAR_DECAY,
        initial_dropout: float = 0.5,
        final_dropout: float = 0.1,
        total_epochs: int = 100,
        step_size: Optional[int] = None,
        step_gamma: float = 0.5,
        patience: int = 10,
        threshold: float = 0.01
    ):
        """
        Initialize DropoutScheduler.
        
        Args:
            schedule_type: Type of scheduling strategy
            initial_dropout: Starting dropout rate
            final_dropout: Ending dropout rate (for decay schedules)
            total_epochs: Total training epochs
            step_size: Epochs between steps (for step_decay)
            step_gamma: Multiplicative factor for step decay
            patience: Epochs to wait before reducing (for adaptive)
            threshold: Minimum improvement threshold (for adaptive)
        """
        if isinstance(schedule_type, str):
            schedule_type = DropoutScheduleType(schedule_type)
            
        self.schedule_type = schedule_type
        self.initial_dropout = initial_dropout
        self.final_dropout = final_dropout
        self.total_epochs = total_epochs
        self.step_size = step_size or (total_epochs // 4)
        self.step_gamma = step_gamma
        self.patience = patience
        self.threshold = threshold
        
        # State tracking
        self.current_dropout = initial_dropout
        self.best_val_loss = float('inf')
        self.epochs_without_improvement = 0
        
        logger.info(f"🎯 DropoutScheduler initialized: {schedule_type.value}")
        logger.info(f"   Initial: {initial_dropout:.3f} → Final: {final_dropout:.3f}")
        
    def get_dropout_rate(self, epoch: int, val_loss: Optional[float] = None) -> float:
        """
        Calculate dropout rate for given epoch and validation loss.
        
        Args:
            epoch: Current training epoch (0-indexed)
            val_loss: Current validation loss (for adaptive scheduling)
            
        Returns:
            Dropout rate to use for this epoch
        """
        if self.schedule_type == DropoutScheduleType.CONSTANT:
            return self.initial_dropout
            
        elif self.schedule_type == DropoutScheduleType.LINEAR_DECAY:
            # Linear interpolation from initial to final
            progress = min(epoch / self.total_epochs, 1.0)
            dropout = self.initial_dropout + progress * (self.final_dropout - self.initial_dropout)
            
        elif self.schedule_type == DropoutScheduleType.COSINE_DECAY:
            # Cosine annealing from initial to final
            progress = min(epoch / self.total_epochs, 1.0)
            dropout = self.final_dropout + 0.5 * (self.initial_dropout - self.final_dropout) * (1 + math.cos(math.pi * progress))
            
        elif self.schedule_type == DropoutScheduleType.STEP_DECAY:
            # Step-wise decay
            step_count = epoch // self.step_size
            dropout = self.initial_dropout * (self.step_gamma ** step_count)
            dropout = max(dropout, self.final_dropout)  # Don't go below final
            
        elif self.schedule_type == DropoutScheduleType.ADAPTIVE:
            # Adaptive based on validation loss
            if val_loss is not None:
                if val_loss < self.best_val_loss - self.threshold:
                    self.best_val_loss = val_loss
                    self.epochs_without_improvement = 0
                else:
                    self.epochs_without_improvement += 1
                    
                if self.epochs_without_improvement >= self.patience:
                    # Reduce dropout when plateauing
                    reduction_factor = 0.8
                    self.current_dropout = max(
                        self.current_dropout * reduction_factor,
                        self.final_dropout
                    )
                    self.epochs_without_improvement = 0
                    logger.info(f"📉 Adaptive dropout reduction: {self.current_dropout:.3f}")
            
            dropout = self.current_dropout
        
        elif self.schedule_type == DropoutScheduleType.PIECEWISE_CONSTANT:
            # Piecewise: Hold high (1/3), ramp down (1/3), hold moderate (1/3)
            # Example for 50 epochs: 0.5 for epochs 0-16, ramp 0.5→0.25 for 17-33, 0.25 for 34-49
            third = self.total_epochs / 3.0
            
            if epoch < third:
                # First third: maintain high dropout
                dropout = self.initial_dropout
            elif epoch < 2 * third:
                # Second third: linear ramp from initial to final
                progress_in_middle = (epoch - third) / third
                dropout = self.initial_dropout + progress_in_middle * (self.final_dropout - self.initial_dropout)
            else:
                # Last third: maintain moderate dropout
                dropout = self.final_dropout
            
        else:
            raise ValueError(f"Unknown schedule type: {self.schedule_type}")
            
        # Update current dropout for next iteration
        self.current_dropout = dropout
        return dropout
    
    def update_model_dropout(self, model: nn.Module, dropout_rate: float, epoch: Optional[int] = None):
        """
        Update dropout rates in all dropout layers of a model.
        
        Args:
            model: PyTorch model to update
            dropout_rate: New dropout rate to apply
            epoch: Current epoch (for logging)
        """
        updated_count = 0
        
        def update_dropout_recursive(module):
            nonlocal updated_count
            for name, child in module.named_children():
                if isinstance(child, nn.Dropout):
                    child.p = dropout_rate
                    updated_count += 1
                else:
                    update_dropout_recursive(child)
        
        update_dropout_recursive(model)
        
        if updated_count > 0:
            epoch_prefix = f"[epoch={epoch}] " if epoch is not None else ""
            logger.debug(f"{epoch_prefix}[Dropout] Updated {updated_count} dropout layers to rate {dropout_rate:.3f}")
        
        return updated_count
    
    def step(self, epoch: int, model: nn.Module, val_loss: Optional[float] = None) -> float:
        """
        Perform a scheduler step: calculate new dropout rate and update model.
        
        Args:
            epoch: Current training epoch
            model: Model to update
            val_loss: Current validation loss
            
        Returns:
            New dropout rate
        """
        new_dropout = self.get_dropout_rate(epoch, val_loss)
        self.update_model_dropout(model, new_dropout, epoch)
        
        # Log significant changes
        if abs(new_dropout - getattr(self, '_last_logged_dropout', new_dropout)) > 0.01:
            logger.info(f"[epoch={epoch}] 📊 Dropout rate = {new_dropout:.3f}")
            self._last_logged_dropout = new_dropout
        
        return new_dropout
    
    def get_state_dict(self) -> dict:
        """Get scheduler state for checkpointing."""
        return {
            'current_dropout': self.current_dropout,
            'best_val_loss': self.best_val_loss,
            'epochs_without_improvement': self.epochs_without_improvement
        }
    
    def load_state_dict(self, state_dict: dict):
        """Load scheduler state from checkpoint."""
        self.current_dropout = state_dict.get('current_dropout', self.initial_dropout)
        self.best_val_loss = state_dict.get('best_val_loss', float('inf'))
        self.epochs_without_improvement = state_dict.get('epochs_without_improvement', 0)
        logger.info(f"🔄 DropoutScheduler state restored: dropout={self.current_dropout:.3f}")


def create_dropout_scheduler(
    schedule_type: str = "linear_decay",
    initial_dropout: float = 0.5,
    final_dropout: float = 0.1,
    total_epochs: int = 100,
    **kwargs
) -> DropoutScheduler:
    """
    Factory function to create dropout scheduler with common presets.
    
    Common presets:
    - "aggressive_decay": 0.7 → 0.05 linear decay
    - "gentle_decay": 0.5 → 0.2 linear decay  
    - "cosine_warm": 0.6 → 0.1 cosine decay
    - "adaptive": Adaptive based on validation loss
    """
    presets = {
        "aggressive_decay": {
            "schedule_type": "linear_decay",
            "initial_dropout": 0.7,
            "final_dropout": 0.05
        },
        "gentle_decay": {
            "schedule_type": "linear_decay", 
            "initial_dropout": 0.5,
            "final_dropout": 0.2
        },
        "cosine_warm": {
            "schedule_type": "cosine_decay",
            "initial_dropout": 0.6,
            "final_dropout": 0.1
        },
        "adaptive": {
            "schedule_type": "adaptive",
            "initial_dropout": 0.5,
            "final_dropout": 0.1
        }
    }
    
    if schedule_type in presets:
        preset_params = presets[schedule_type]
        preset_params.update(kwargs)  # Allow override
        return DropoutScheduler(total_epochs=total_epochs, **preset_params)
    else:
        return DropoutScheduler(
            schedule_type=schedule_type,
            initial_dropout=initial_dropout,
            final_dropout=final_dropout,
            total_epochs=total_epochs,
            **kwargs
        ) 