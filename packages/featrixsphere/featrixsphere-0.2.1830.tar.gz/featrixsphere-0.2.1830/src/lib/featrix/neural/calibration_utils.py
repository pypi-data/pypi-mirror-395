#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
"""
Calibration utilities for single predictor probability calibration.

Provides temperature scaling and other calibration methods to improve
the reliability of predicted probabilities.
"""
import logging
import numpy as np
import torch
import torch.nn.functional as F
from typing import Dict, Tuple, Optional, List
from scipy.optimize import minimize_scalar
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)


def compute_ece(predicted_probs: np.ndarray, true_labels: np.ndarray, n_bins: int = 10) -> float:
    """
    Compute Expected Calibration Error (ECE).
    
    ECE measures how well-calibrated the probabilities are by binning predictions
    and comparing the average predicted probability in each bin to the actual
    fraction of positive examples in that bin.
    
    Args:
        predicted_probs: Array of predicted probabilities (shape: [n_samples] for binary, [n_samples, n_classes] for multi-class)
        true_labels: Array of true labels (shape: [n_samples])
        n_bins: Number of bins for calibration error calculation (default: 10)
    
    Returns:
        ECE value (lower is better, 0 is perfect calibration)
    """
    if len(predicted_probs.shape) == 2:
        # Multi-class: use max probability for each sample
        predicted_probs = np.max(predicted_probs, axis=1)
    
    # Ensure probabilities are in [0, 1]
    predicted_probs = np.clip(predicted_probs, 0.0, 1.0)
    
    # Bin the predictions
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]
    
    ece = 0.0
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        # Find samples in this bin
        in_bin = (predicted_probs > bin_lower) & (predicted_probs <= bin_upper)
        prop_in_bin = in_bin.mean()
        
        if prop_in_bin > 0:
            # Average predicted probability in this bin
            accuracy_in_bin = true_labels[in_bin].mean()
            avg_confidence_in_bin = predicted_probs[in_bin].mean()
            
            # Add to ECE
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin
    
    return float(ece)


def compute_brier_score(predicted_probs: np.ndarray, true_labels: np.ndarray) -> float:
    """
    Compute Brier Score (mean squared error between predicted probabilities and true labels).
    
    Lower is better. Perfect calibration would have Brier score of 0.
    
    Args:
        predicted_probs: Array of predicted probabilities (shape: [n_samples] for binary, [n_samples, n_classes] for multi-class)
        true_labels: Array of true labels (shape: [n_samples])
    
    Returns:
        Brier score (lower is better)
    """
    if len(predicted_probs.shape) == 2:
        # Multi-class: convert to one-hot and compute Brier score
        n_classes = predicted_probs.shape[1]
        true_one_hot = np.eye(n_classes)[true_labels.astype(int)]
        return float(np.mean(np.sum((predicted_probs - true_one_hot) ** 2, axis=1)))
    else:
        # Binary classification
        return float(np.mean((predicted_probs - true_labels) ** 2))


def fit_temperature_scaling(
    logits: torch.Tensor,
    labels: torch.Tensor,
    initial_temp: float = 1.0,
    method: str = 'nll'
) -> Tuple[float, Dict[str, float]]:
    """
    Fit temperature scaling parameter to calibrate probabilities.
    
    Temperature scaling applies a single temperature parameter T to logits:
    calibrated_logits = logits / T
    
    The optimal T minimizes negative log-likelihood (NLL) on the calibration set.
    
    Args:
        logits: Raw model logits (shape: [n_samples, n_classes])
        labels: True class labels (shape: [n_samples])
        initial_temp: Initial temperature value for optimization (default: 1.0)
        method: Optimization method - 'nll' (negative log-likelihood) or 'ece' (expected calibration error)
    
    Returns:
        Tuple of (optimal_temperature, metrics_dict)
        metrics_dict contains:
            - 'temperature': Optimal temperature value
            - 'ece_before': ECE before calibration
            - 'ece_after': ECE after calibration
            - 'brier_before': Brier score before calibration
            - 'brier_after': Brier score after calibration
            - 'nll_before': Negative log-likelihood before calibration
            - 'nll_after': Negative log-likelihood after calibration
    """
    # Ensure tensors are on CPU and converted to numpy for scipy optimization
    if isinstance(logits, torch.Tensor):
        logits_np = logits.detach().cpu().numpy()
    else:
        logits_np = np.array(logits)
    
    if isinstance(labels, torch.Tensor):
        labels_np = labels.detach().cpu().numpy()
    else:
        labels_np = np.array(labels)
    
    # Compute baseline metrics (before calibration)
    probs_before = F.softmax(torch.from_numpy(logits_np), dim=1).numpy()
    ece_before = compute_ece(probs_before, labels_np)
    brier_before = compute_brier_score(probs_before, labels_np)
    
    # Compute NLL before calibration
    log_probs_before = F.log_softmax(torch.from_numpy(logits_np), dim=1).numpy()
    nll_before = -np.mean([log_probs_before[i, int(labels_np[i])] for i in range(len(labels_np))])
    
    # Define objective function for optimization
    def objective(temp):
        """Objective function: negative log-likelihood with temperature scaling."""
        if temp <= 0:
            return 1e10  # Penalize invalid temperatures
        
        # Apply temperature scaling
        scaled_logits = logits_np / temp
        
        # Compute log probabilities
        log_probs = F.log_softmax(torch.from_numpy(scaled_logits), dim=1).numpy()
        
        # Compute negative log-likelihood
        nll = -np.mean([log_probs[i, int(labels_np[i])] for i in range(len(labels_np))])
        
        return float(nll)
    
    # Optimize temperature
    try:
        result = minimize_scalar(
            objective,
            bounds=(0.01, 10.0),  # Reasonable temperature range
            method='bounded',
            options={'xatol': 1e-6}
        )
        
        if result.success:
            optimal_temp = float(result.x)
            logger.info(f"✅ Temperature scaling fitted: T = {optimal_temp:.4f} (NLL: {result.fun:.4f})")
        else:
            logger.warning(f"⚠️  Temperature optimization did not converge, using initial temp: {initial_temp}")
            optimal_temp = initial_temp
    except Exception as e:
        logger.warning(f"⚠️  Temperature optimization failed: {e}, using initial temp: {initial_temp}")
        optimal_temp = initial_temp
    
    # Compute metrics after calibration
    scaled_logits = logits_np / optimal_temp
    probs_after = F.softmax(torch.from_numpy(scaled_logits), dim=1).numpy()
    ece_after = compute_ece(probs_after, labels_np)
    brier_after = compute_brier_score(probs_after, labels_np)
    
    # Compute NLL after calibration
    log_probs_after = F.log_softmax(torch.from_numpy(scaled_logits), dim=1).numpy()
    nll_after = -np.mean([log_probs_after[i, int(labels_np[i])] for i in range(len(labels_np))])
    
    metrics = {
        'temperature': optimal_temp,
        'ece_before': ece_before,
        'ece_after': ece_after,
        'brier_before': brier_before,
        'brier_after': brier_after,
        'nll_before': nll_before,
        'nll_after': nll_after,
        'ece_improvement': ece_before - ece_after,
        'brier_improvement': brier_before - brier_after,
        'nll_improvement': nll_before - nll_after,
    }
    
    logger.info(f"📊 Calibration metrics:")
    logger.info(f"   ECE: {ece_before:.4f} → {ece_after:.4f} (improvement: {metrics['ece_improvement']:.4f})")
    logger.info(f"   Brier: {brier_before:.4f} → {brier_after:.4f} (improvement: {metrics['brier_improvement']:.4f})")
    logger.info(f"   NLL: {nll_before:.4f} → {nll_after:.4f} (improvement: {metrics['nll_improvement']:.4f})")
    
    return optimal_temp, metrics


def apply_temperature_scaling(logits: torch.Tensor, temperature: float) -> torch.Tensor:
    """
    Apply temperature scaling to logits.
    
    Args:
        logits: Raw model logits (shape: [batch_size, n_classes] or [n_classes])
        temperature: Temperature parameter (T > 0)
    
    Returns:
        Scaled logits (logits / temperature)
    """
    if temperature <= 0:
        logger.warning(f"⚠️  Invalid temperature {temperature}, using 1.0")
        temperature = 1.0
    
    return logits / temperature


def get_calibrated_probs(
    logits: torch.Tensor,
    temperature: Optional[float] = None
) -> torch.Tensor:
    """
    Get calibrated probabilities from logits.
    
    If temperature is provided, applies temperature scaling before softmax.
    Otherwise, applies standard softmax.
    
    Args:
        logits: Raw model logits (shape: [batch_size, n_classes] or [n_classes])
        temperature: Optional temperature parameter for calibration (None = no calibration)
    
    Returns:
        Calibrated probabilities (shape: same as logits)
    """
    if temperature is not None and temperature != 1.0:
        scaled_logits = apply_temperature_scaling(logits, temperature)
        return F.softmax(scaled_logits, dim=-1)
    else:
        return F.softmax(logits, dim=-1)


def compute_calibration_metrics(
    predicted_probs: np.ndarray,
    true_labels: np.ndarray,
    n_bins: int = 10
) -> Dict[str, float]:
    """
    Compute comprehensive calibration metrics.
    
    Args:
        predicted_probs: Predicted probabilities (shape: [n_samples] for binary, [n_samples, n_classes] for multi-class)
        true_labels: True labels (shape: [n_samples])
        n_bins: Number of bins for ECE calculation
    
    Returns:
        Dictionary of calibration metrics:
            - 'ece': Expected Calibration Error
            - 'brier_score': Brier Score
            - 'max_calibration_error': Maximum calibration error across bins
            - 'reliability': Average reliability (lower is better)
    """
    ece = compute_ece(predicted_probs, true_labels, n_bins=n_bins)
    brier = compute_brier_score(predicted_probs, true_labels)
    
    # Compute maximum calibration error
    if len(predicted_probs.shape) == 2:
        predicted_probs_flat = np.max(predicted_probs, axis=1)
    else:
        predicted_probs_flat = predicted_probs
    
    predicted_probs_flat = np.clip(predicted_probs_flat, 0.0, 1.0)
    
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]
    
    max_error = 0.0
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        in_bin = (predicted_probs_flat > bin_lower) & (predicted_probs_flat <= bin_upper)
        if in_bin.sum() > 0:
            accuracy_in_bin = true_labels[in_bin].mean()
            avg_confidence_in_bin = predicted_probs_flat[in_bin].mean()
            error = np.abs(avg_confidence_in_bin - accuracy_in_bin)
            max_error = max(max_error, error)
    
    return {
        'ece': ece,
        'brier_score': brier,
        'max_calibration_error': float(max_error),
        'reliability': ece  # Same as ECE for now
    }


def fit_platt_scaling(
    logits: torch.Tensor,
    labels: torch.Tensor
) -> Tuple[LogisticRegression, Dict[str, float]]:
    """
    Fit Platt scaling (logistic regression on logits) for binary classification.
    
    Platt scaling fits a logistic regression model to the logits to produce
    calibrated probabilities. Works best for binary classification.
    
    Args:
        logits: Raw model logits (shape: [n_samples, n_classes])
        labels: True class labels (shape: [n_samples])
    
    Returns:
        Tuple of (fitted_logistic_model, metrics_dict)
    """
    # Ensure tensors are on CPU and converted to numpy
    if isinstance(logits, torch.Tensor):
        logits_np = logits.detach().cpu().numpy()
    else:
        logits_np = np.array(logits)
    
    if isinstance(labels, torch.Tensor):
        labels_np = labels.detach().cpu().numpy()
    else:
        labels_np = np.array(labels)
    
    # For multi-class, use max logit or convert to binary
    if logits_np.shape[1] > 2:
        # Multi-class: use difference between max and second-max logit
        sorted_logits = np.sort(logits_np, axis=1)
        logit_diff = sorted_logits[:, -1] - sorted_logits[:, -2]
        logits_for_platt = logit_diff.reshape(-1, 1)
        # Use binary labels: 1 if predicted class matches true class
        predicted_classes = np.argmax(logits_np, axis=1)
        binary_labels = (predicted_classes == labels_np).astype(float)
    else:
        # Binary classification: use logit difference
        logits_for_platt = (logits_np[:, 1] - logits_np[:, 0]).reshape(-1, 1)
        binary_labels = (labels_np == 1).astype(float) if logits_np.shape[1] == 2 else labels_np.astype(float)
    
    # Compute baseline metrics
    probs_before = F.softmax(torch.from_numpy(logits_np), dim=1).numpy()
    ece_before = compute_ece(probs_before, labels_np)
    brier_before = compute_brier_score(probs_before, labels_np)
    
    # Fit logistic regression (Platt scaling)
    try:
        platt_model = LogisticRegression()
        platt_model.fit(logits_for_platt, binary_labels)
        
        # Get calibrated probabilities
        calibrated_binary_probs = platt_model.predict_proba(logits_for_platt)[:, 1]
        
        # For multi-class, we need to map back to class probabilities
        if logits_np.shape[1] > 2:
            # Use calibrated probability for predicted class, distribute remainder
            predicted_classes = np.argmax(logits_np, axis=1)
            probs_after = probs_before.copy()
            for i in range(len(predicted_classes)):
                pred_class = predicted_classes[i]
                probs_after[i, pred_class] = calibrated_binary_probs[i]
                # Redistribute remaining probability
                remaining = 1.0 - calibrated_binary_probs[i]
                other_probs = probs_before[i].copy()
                other_probs[pred_class] = 0
                other_sum = other_probs.sum()
                if other_sum > 0:
                    probs_after[i] = np.where(probs_after[i] == probs_after[i, pred_class], 
                                             probs_after[i, pred_class],
                                             other_probs * (remaining / other_sum))
        else:
            # Binary: convert back to 2-class probabilities
            probs_after = np.zeros_like(probs_before)
            probs_after[:, 1] = calibrated_binary_probs
            probs_after[:, 0] = 1.0 - calibrated_binary_probs
        
        ece_after = compute_ece(probs_after, labels_np)
        brier_after = compute_brier_score(probs_after, labels_np)
        
        metrics = {
            'ece_before': ece_before,
            'ece_after': ece_after,
            'brier_before': brier_before,
            'brier_after': brier_after,
            'ece_improvement': ece_before - ece_after,
            'brier_improvement': brier_before - brier_after,
        }
        
        logger.info(f"✅ Platt scaling fitted (ECE: {ece_before:.4f} → {ece_after:.4f})")
        
    except Exception as e:
        logger.warning(f"⚠️  Platt scaling failed: {e}, returning None")
        return None, {}
    
    return platt_model, metrics


def apply_platt_scaling(logits: torch.Tensor, platt_model: LogisticRegression) -> np.ndarray:
    """
    Apply Platt scaling to logits using a fitted model.
    
    Args:
        logits: Raw model logits (shape: [batch_size, n_classes] or [n_classes])
        platt_model: Fitted LogisticRegression model
    
    Returns:
        Calibrated probabilities (numpy array)
    """
    if isinstance(logits, torch.Tensor):
        logits_np = logits.detach().cpu().numpy()
    else:
        logits_np = np.array(logits)
    
    # Handle single sample
    if len(logits_np.shape) == 1:
        logits_np = logits_np.reshape(1, -1)
    
    n_classes = logits_np.shape[1]
    
    if n_classes > 2:
        # Multi-class: use logit difference
        sorted_logits = np.sort(logits_np, axis=1)
        logit_diff = sorted_logits[:, -1] - sorted_logits[:, -2]
        logits_for_platt = logit_diff.reshape(-1, 1)
        predicted_classes = np.argmax(logits_np, axis=1)
    else:
        # Binary: use logit difference
        logits_for_platt = (logits_np[:, 1] - logits_np[:, 0]).reshape(-1, 1)
        predicted_classes = np.argmax(logits_np, axis=1)
    
    # Get calibrated binary probabilities
    calibrated_binary = platt_model.predict_proba(logits_for_platt)[:, 1]
    
    # Convert back to multi-class probabilities
    probs_before = F.softmax(torch.from_numpy(logits_np), dim=1).numpy()
    probs_after = probs_before.copy()
    
    for i in range(len(predicted_classes)):
        pred_class = predicted_classes[i]
        probs_after[i, pred_class] = calibrated_binary[i]
        # Redistribute remaining probability
        remaining = 1.0 - calibrated_binary[i]
        other_probs = probs_before[i].copy()
        other_probs[pred_class] = 0
        other_sum = other_probs.sum()
        if other_sum > 0:
            probs_after[i] = np.where(np.arange(n_classes) == pred_class,
                                     probs_after[i, pred_class],
                                     other_probs * (remaining / other_sum))
    
    return probs_after


def fit_isotonic_regression(
    logits: torch.Tensor,
    labels: torch.Tensor
) -> Tuple[IsotonicRegression, Dict[str, float]]:
    """
    Fit isotonic regression for probability calibration.
    
    Isotonic regression is a non-parametric method that fits a piecewise
    constant, non-decreasing function. Works well for both binary and multi-class.
    
    Args:
        logits: Raw model logits (shape: [n_samples, n_classes])
        labels: True class labels (shape: [n_samples])
    
    Returns:
        Tuple of (fitted_isotonic_model, metrics_dict)
    """
    # Ensure tensors are on CPU and converted to numpy
    if isinstance(logits, torch.Tensor):
        logits_np = logits.detach().cpu().numpy()
    else:
        logits_np = np.array(logits)
    
    if isinstance(labels, torch.Tensor):
        labels_np = labels.detach().cpu().numpy()
    else:
        labels_np = np.array(labels)
    
    # Compute baseline metrics
    probs_before = F.softmax(torch.from_numpy(logits_np), dim=1).numpy()
    ece_before = compute_ece(probs_before, labels_np)
    brier_before = compute_brier_score(probs_before, labels_np)
    
    # For multi-class, fit isotonic regression per class or use max probability
    n_classes = logits_np.shape[1]
    
    try:
        if n_classes == 2:
            # Binary: fit on positive class probability
            pos_probs = probs_before[:, 1]
            isotonic_model = IsotonicRegression(out_of_bounds='clip')
            isotonic_model.fit(pos_probs, (labels_np == 1).astype(float))
            
            # Apply calibration
            calibrated_pos = isotonic_model.predict(pos_probs)
            probs_after = np.zeros_like(probs_before)
            probs_after[:, 1] = calibrated_pos
            probs_after[:, 0] = 1.0 - calibrated_pos
        else:
            # Multi-class: fit on max probability
            max_probs = np.max(probs_before, axis=1)
            predicted_classes = np.argmax(probs_before, axis=1)
            # Use binary labels: 1 if predicted class matches true class
            binary_labels = (predicted_classes == labels_np).astype(float)
            
            isotonic_model = IsotonicRegression(out_of_bounds='clip')
            isotonic_model.fit(max_probs, binary_labels)
            
            # Apply calibration to max probabilities
            calibrated_max = isotonic_model.predict(max_probs)
            
            # Redistribute probabilities
            probs_after = probs_before.copy()
            for i in range(len(predicted_classes)):
                pred_class = predicted_classes[i]
                probs_after[i, pred_class] = calibrated_max[i]
                # Redistribute remaining probability
                remaining = 1.0 - calibrated_max[i]
                other_probs = probs_before[i].copy()
                other_probs[pred_class] = 0
                other_sum = other_probs.sum()
                if other_sum > 0:
                    probs_after[i] = np.where(np.arange(n_classes) == pred_class,
                                             probs_after[i, pred_class],
                                             other_probs * (remaining / other_sum))
        
        ece_after = compute_ece(probs_after, labels_np)
        brier_after = compute_brier_score(probs_after, labels_np)
        
        metrics = {
            'ece_before': ece_before,
            'ece_after': ece_after,
            'brier_before': brier_before,
            'brier_after': brier_after,
            'ece_improvement': ece_before - ece_after,
            'brier_improvement': brier_before - brier_after,
        }
        
        logger.info(f"✅ Isotonic regression fitted (ECE: {ece_before:.4f} → {ece_after:.4f})")
        
    except Exception as e:
        logger.warning(f"⚠️  Isotonic regression failed: {e}, returning None")
        return None, {}
    
    return isotonic_model, metrics


def apply_isotonic_regression(logits: torch.Tensor, isotonic_model: IsotonicRegression) -> np.ndarray:
    """
    Apply isotonic regression calibration to logits.
    
    Args:
        logits: Raw model logits (shape: [batch_size, n_classes] or [n_classes])
        isotonic_model: Fitted IsotonicRegression model
    
    Returns:
        Calibrated probabilities (numpy array)
    """
    if isinstance(logits, torch.Tensor):
        logits_np = logits.detach().cpu().numpy()
    else:
        logits_np = np.array(logits)
    
    # Handle single sample
    if len(logits_np.shape) == 1:
        logits_np = logits_np.reshape(1, -1)
    
    n_classes = logits_np.shape[1]
    probs_before = F.softmax(torch.from_numpy(logits_np), dim=1).numpy()
    
    if n_classes == 2:
        # Binary: calibrate positive class probability
        pos_probs = probs_before[:, 1]
        calibrated_pos = isotonic_model.predict(pos_probs)
        probs_after = np.zeros_like(probs_before)
        probs_after[:, 1] = calibrated_pos
        probs_after[:, 0] = 1.0 - calibrated_pos
    else:
        # Multi-class: calibrate max probability
        max_probs = np.max(probs_before, axis=1)
        predicted_classes = np.argmax(probs_before, axis=1)
        calibrated_max = isotonic_model.predict(max_probs)
        
        # Redistribute probabilities
        probs_after = probs_before.copy()
        for i in range(len(predicted_classes)):
            pred_class = predicted_classes[i]
            probs_after[i, pred_class] = calibrated_max[i]
            # Redistribute remaining probability
            remaining = 1.0 - calibrated_max[i]
            other_probs = probs_before[i].copy()
            other_probs[pred_class] = 0
            other_sum = other_probs.sum()
            if other_sum > 0:
                probs_after[i] = np.where(np.arange(n_classes) == pred_class,
                                         probs_after[i, pred_class],
                                         other_probs * (remaining / other_sum))
    
    return probs_after


def auto_fit_calibration(
    logits: torch.Tensor,
    labels: torch.Tensor,
    validation_split: float = 0.2
) -> Tuple[str, Optional[float], Optional[LogisticRegression], Optional[IsotonicRegression], Dict[str, float]]:
    """
    Automatically fit the best calibration method by trying all three and selecting the one
    with the lowest ECE (Expected Calibration Error).
    
    Args:
        logits: Raw model logits (shape: [n_samples, n_classes])
        labels: True class labels (shape: [n_samples])
        validation_split: Fraction of data to use for validation (default: 0.2)
    
    Returns:
        Tuple of:
            - best_method: 'temperature', 'platt', 'isotonic', or 'none'
            - temperature: Optimal temperature (if method is 'temperature')
            - platt_model: Fitted Platt model (if method is 'platt')
            - isotonic_model: Fitted isotonic model (if method is 'isotonic')
            - metrics: Dictionary with calibration metrics for all methods
    """
    # Ensure tensors are on CPU
    if isinstance(logits, torch.Tensor):
        logits_np = logits.detach().cpu()
    else:
        logits_np = torch.from_numpy(np.array(logits))
    
    if isinstance(labels, torch.Tensor):
        labels_np = labels.detach().cpu().numpy()
    else:
        labels_np = np.array(labels)
    
    n_samples = len(labels_np)
    
    # Split into calibration and validation sets
    if validation_split > 0 and n_samples > 10:
        n_cal = int(n_samples * (1 - validation_split))
        indices = np.random.permutation(n_samples)
        cal_indices = indices[:n_cal]
        val_indices = indices[n_cal:]
        
        cal_logits = logits_np[cal_indices]
        cal_labels = labels_np[cal_indices]
        val_logits = logits_np[val_indices]
        val_labels = labels_np[val_indices]
    else:
        # Use all data for both calibration and validation (small dataset)
        cal_logits = logits_np
        cal_labels = labels_np
        val_logits = logits_np
        val_labels = labels_np
    
    logger.info(f"🔍 Auto-fitting calibration: {len(cal_labels)} calibration samples, {len(val_labels)} validation samples")
    
    # Try all three methods
    methods = {}
    metrics = {}
    candidate_scores = {}
    
    # Compute baseline NLL for comparison
    baseline_probs = F.softmax(val_logits, dim=1).numpy()
    baseline_log_probs = F.log_softmax(val_logits, dim=1).numpy()
    baseline_nll = -np.mean([baseline_log_probs[i, int(val_labels[i])] for i in range(len(val_labels))])
    candidate_scores['none'] = {'nll': float(baseline_nll)}
    
    # 1. Temperature Scaling
    try:
        temp, temp_metrics = fit_temperature_scaling(cal_logits, cal_labels)
        # Evaluate on validation set
        val_probs_temp = get_calibrated_probs(val_logits, temp).numpy()
        val_ece_temp = compute_ece(val_probs_temp, val_labels)
        val_log_probs_temp = F.log_softmax(apply_temperature_scaling(val_logits, temp), dim=1).numpy()
        val_nll_temp = -np.mean([val_log_probs_temp[i, int(val_labels[i])] for i in range(len(val_labels))])
        methods['temperature'] = {
            'model': temp,
            'val_ece': val_ece_temp,
            'val_nll': val_nll_temp,
            'metrics': temp_metrics
        }
        metrics['temperature'] = {
            **temp_metrics,
            'val_ece': val_ece_temp,
            'val_nll': val_nll_temp
        }
        candidate_scores['ts'] = {'nll': float(val_nll_temp)}
        logger.info(f"   Temperature Scaling: val ECE = {val_ece_temp:.4f}, val NLL = {val_nll_temp:.4f}")
    except Exception as e:
        logger.warning(f"   Temperature Scaling failed: {e}")
        methods['temperature'] = None
    
    # 2. Platt Scaling
    try:
        platt_model, platt_metrics = fit_platt_scaling(cal_logits, cal_labels)
        if platt_model is not None:
            # Evaluate on validation set
            val_probs_platt = apply_platt_scaling(val_logits, platt_model)
            val_ece_platt = compute_ece(val_probs_platt, val_labels)
            # Compute NLL for Platt (approximate using calibrated probs)
            val_log_probs_platt = np.log(np.clip(val_probs_platt, 1e-10, 1.0))
            val_nll_platt = -np.mean([val_log_probs_platt[i, int(val_labels[i])] for i in range(len(val_labels))])
            methods['platt'] = {
                'model': platt_model,
                'val_ece': val_ece_platt,
                'val_nll': val_nll_platt,
                'metrics': platt_metrics
            }
            metrics['platt'] = {
                **platt_metrics,
                'val_ece': val_ece_platt,
                'val_nll': val_nll_platt
            }
            candidate_scores['platt'] = {'nll': float(val_nll_platt)}
            logger.info(f"   Platt Scaling: val ECE = {val_ece_platt:.4f}, val NLL = {val_nll_platt:.4f}")
        else:
            methods['platt'] = None
    except Exception as e:
        logger.warning(f"   Platt Scaling failed: {e}")
        methods['platt'] = None
    
    # 3. Isotonic Regression
    try:
        isotonic_model, isotonic_metrics = fit_isotonic_regression(cal_logits, cal_labels)
        if isotonic_model is not None:
            # Evaluate on validation set
            val_probs_isotonic = apply_isotonic_regression(val_logits, isotonic_model)
            val_ece_isotonic = compute_ece(val_probs_isotonic, val_labels)
            # Compute NLL for Isotonic (approximate using calibrated probs)
            val_log_probs_isotonic = np.log(np.clip(val_probs_isotonic, 1e-10, 1.0))
            val_nll_isotonic = -np.mean([val_log_probs_isotonic[i, int(val_labels[i])] for i in range(len(val_labels))])
            methods['isotonic'] = {
                'model': isotonic_model,
                'val_ece': val_ece_isotonic,
                'val_nll': val_nll_isotonic,
                'metrics': isotonic_metrics
            }
            metrics['isotonic'] = {
                **isotonic_metrics,
                'val_ece': val_ece_isotonic,
                'val_nll': val_nll_isotonic
            }
            candidate_scores['iso'] = {'nll': float(val_nll_isotonic)}
            logger.info(f"   Isotonic Regression: val ECE = {val_ece_isotonic:.4f}, val NLL = {val_nll_isotonic:.4f}")
        else:
            methods['isotonic'] = None
    except Exception as e:
        logger.warning(f"   Isotonic Regression failed: {e}")
        methods['isotonic'] = None
    
    # Find best method (lowest validation ECE)
    best_method = 'none'
    best_ece = float('inf')
    best_temperature = None
    best_platt = None
    best_isotonic = None
    
    for method_name, method_data in methods.items():
        if method_data is not None and 'val_ece' in method_data:
            if method_data['val_ece'] < best_ece:
                best_ece = method_data['val_ece']
                best_method = method_name
                if method_name == 'temperature':
                    best_temperature = method_data['model']
                elif method_name == 'platt':
                    best_platt = method_data['model']
                elif method_name == 'isotonic':
                    best_isotonic = method_data['model']
    
    # Compare to baseline (no calibration)
    baseline_ece = compute_ece(baseline_probs, val_labels)
    
    if best_ece < baseline_ece:
        logger.info(f"✅ Best calibration method: {best_method} (val ECE: {baseline_ece:.4f} → {best_ece:.4f})")
    else:
        logger.info(f"ℹ️  No calibration improves over baseline (baseline ECE: {baseline_ece:.4f}, best: {best_ece:.4f})")
        best_method = 'none'
        best_temperature = None
        best_platt = None
        best_isotonic = None
    
    # Add baseline to metrics
    metrics['baseline'] = {
        'ece': baseline_ece,
        'brier_score': compute_brier_score(baseline_probs, val_labels),
        'nll': baseline_nll
    }
    metrics['best_method'] = best_method
    metrics['best_val_ece'] = best_ece
    metrics['candidate_scores'] = candidate_scores
    
    return best_method, best_temperature, best_platt, best_isotonic, metrics

