#!/usr/bin/env python3
"""
Training-specific exceptions that provide actionable information for retry strategies.

Each exception type corresponds to a specific training failure mode and includes
recommended parameter adjustments for retry attempts.
"""
from typing import Dict, Any, Optional


class TrainingFailureException(Exception):
    """Base exception for all training failures that may be recoverable with parameter adjustments."""
    
    def __init__(self, message: str, epoch: int, recommendations: list, suggested_adjustments: Optional[Dict[str, Any]] = None):
        """
        Args:
            message: Human-readable error message
            epoch: Epoch at which failure was detected
            recommendations: List of diagnostic messages explaining the failure
            suggested_adjustments: Dict of parameter adjustments to try on retry
                e.g., {"learning_rate_multiplier": 3.0, "d_hidden_multiplier": 2.0, "n_hidden_layers_delta": 1}
        """
        super().__init__(message)
        self.epoch = epoch
        self.recommendations = recommendations
        self.suggested_adjustments = suggested_adjustments or {}
    
    def get_adjusted_params(self, current_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply suggested adjustments to current parameters.
        
        Args:
            current_params: Current training parameters
            
        Returns:
            New parameters with adjustments applied
        """
        adjusted = current_params.copy()
        
        for key, adjustment in self.suggested_adjustments.items():
            if key.endswith('_multiplier'):
                param_name = key.replace('_multiplier', '')
                if param_name in adjusted:
                    adjusted[param_name] = adjusted[param_name] * adjustment
            elif key.endswith('_delta'):
                param_name = key.replace('_delta', '')
                if param_name in adjusted:
                    adjusted[param_name] = adjusted[param_name] + adjustment
            elif key.endswith('_absolute'):
                param_name = key.replace('_absolute', '')
                adjusted[param_name] = adjustment
            else:
                # Direct assignment for parameters without suffix
                adjusted[key] = adjustment
        
        return adjusted


class RandomPredictionsError(TrainingFailureException):
    """
    Model is making random predictions (AUC ~0.5) after significant training.
    
    This suggests the model lacks capacity to learn the patterns, or the learning rate
    is too low to escape local minima.
    
    Recommended adjustments:
    - Increase learning rate by 3-5x (to escape local minima faster)
    - Increase d_hidden by 2x (more model capacity)
    - Add 1 more hidden layer (deeper network for complex patterns)
    - Optionally reduce batch size (noisier gradients help exploration)
    """
    
    def __init__(self, message: str, epoch: int, recommendations: list):
        suggested_adjustments = {
            "learning_rate_multiplier": 3.0,    # 3x learning rate
            "d_hidden_multiplier": 2.0,         # 2x hidden dimension
            "n_hidden_layers_delta": 1,         # Add 1 more layer
            "batch_size_multiplier": 0.5,       # Halve batch size for exploration
        }
        super().__init__(message, epoch, recommendations, suggested_adjustments)


class DeadNetworkError(TrainingFailureException):
    """
    Network outputs are frozen (no variation in predictions).
    
    This is a critical failure indicating gradients aren't flowing or learning rate
    is far too low. Requires aggressive intervention.
    
    Recommended adjustments:
    - Increase learning rate by 10x (to unfreeze the network)
    - Ensure fine-tuning is enabled (embedding space may be frozen)
    """
    
    def __init__(self, message: str, epoch: int, recommendations: list):
        suggested_adjustments = {
            "learning_rate_multiplier": 10.0,   # 10x learning rate
            "fine_tune_absolute": True,         # Ensure fine-tuning is enabled
        }
        super().__init__(message, epoch, recommendations, suggested_adjustments)


class ConstantProbabilityError(TrainingFailureException):
    """
    Model produces nearly identical probabilities for all samples.
    
    Similar to dead network but less severe. Network is learning but very slowly
    or stuck in a poor initialization.
    
    Recommended adjustments:
    - Increase learning rate by 5x
    - Train 50% longer to give more time to learn
    """
    
    def __init__(self, message: str, epoch: int, recommendations: list):
        suggested_adjustments = {
            "learning_rate_multiplier": 5.0,    # 5x learning rate
            "n_epochs_multiplier": 1.5,         # Train 50% longer
        }
        super().__init__(message, epoch, recommendations, suggested_adjustments)


class SingleClassBiasError(TrainingFailureException):
    """
    Model always predicts the same class (>95% of predictions).
    
    Often due to class imbalance. This is usually handled by adaptive loss adjustment
    rather than re-training, but can be raised if adjustment fails.
    
    Recommended adjustments:
    - Ensure class weights are enabled
    - Focal loss adjustment happens automatically in single_predictor.py
    """
    
    def __init__(self, message: str, epoch: int, recommendations: list):
        suggested_adjustments = {
            "use_class_weights_absolute": True,  # Ensure class weights enabled
            # Note: Focal loss adjustment happens automatically in single_predictor.py
        }
        super().__init__(message, epoch, recommendations, suggested_adjustments)


class PoorDiscriminationError(TrainingFailureException):
    """
    Model produces varied outputs but poor performance (varied but wrong).
    
    This suggests the model has capacity but is learning spurious patterns
    or the data quality is poor. May need architectural changes or data investigation.
    
    Recommended adjustments:
    - Modest learning rate increase (to explore better solutions)
    - Slightly more regularization via dropout
    """
    
    def __init__(self, message: str, epoch: int, recommendations: list):
        suggested_adjustments = {
            "learning_rate_multiplier": 1.5,    # Modest increase
            "dropout_delta": 0.05,              # Slightly more regularization
        }
        super().__init__(message, epoch, recommendations, suggested_adjustments)


class UnderconfidentError(TrainingFailureException):
    """
    Model predictions clustered near decision boundary (0.4-0.6 range).
    
    Model is very uncertain. May need more training time or indicates the
    problem is genuinely difficult.
    
    Recommended adjustments:
    - Train 50% longer
    - Moderately increase model capacity
    """
    
    def __init__(self, message: str, epoch: int, recommendations: list):
        suggested_adjustments = {
            "n_epochs_multiplier": 1.5,         # Train 50% longer
            "d_hidden_multiplier": 1.5,         # Moderately increase capacity
        }
        super().__init__(message, epoch, recommendations, suggested_adjustments)

