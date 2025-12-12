#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
"""
Featrix Classification Metrics Module

Binary + Multiclass (single-label) only.
Multilabel / multi-output can be added later.

This module provides comprehensive metrics computation for classification tasks,
including imbalanced data metrics, calibration metrics, and cost-based optimization.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple, Sequence, List, Union
import logging

import numpy as np
import torch
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    matthews_corrcoef,
    balanced_accuracy_score,
    brier_score_loss,
    log_loss,
    top_k_accuracy_score,
    confusion_matrix,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Tensor conversion helpers
# ---------------------------------------------------------------------------

def _to_tensor(x: Union[np.ndarray, torch.Tensor], device: Optional[torch.device] = None) -> torch.Tensor:
    """Convert numpy array or tensor to torch tensor, optionally moving to device."""
    if isinstance(x, torch.Tensor):
        tensor = x
    else:
        tensor = torch.from_numpy(np.asarray(x))
    
    if device is not None:
        tensor = tensor.to(device)
    
    return tensor


def _to_numpy(x: Union[np.ndarray, torch.Tensor]) -> np.ndarray:
    """Convert tensor to numpy array."""
    if isinstance(x, torch.Tensor):
        return x.detach().cpu().numpy()
    return np.asarray(x)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _is_binary(y: np.ndarray) -> bool:
    """Check if labels represent binary classification."""
    classes = np.unique(y)
    return classes.size == 2


def pr_auc_torch(y_true: torch.Tensor, y_scores: torch.Tensor) -> float:
    """
    Average Precision (PR-AUC) in torch.
    
    y_true: (N,) {0,1}
    y_scores: (N,) float
    """
    device = y_true.device
    y_true = y_true.to(device).long()
    y_scores = y_scores.to(device).float()
    
    N = y_true.numel()
    if N == 0:
        return float('nan')
    
    # Sort by score descending
    scores_sorted, idx = torch.sort(y_scores, descending=True)
    y_sorted = y_true[idx]
    
    # Cumulative TP and FP
    ones = torch.ones_like(y_sorted, dtype=torch.float32)
    cum_tp = torch.cumsum((y_sorted == 1).float(), dim=0)
    cum_fp = torch.cumsum((y_sorted == 0).float(), dim=0)
    k = torch.arange(1, N + 1, device=device, dtype=torch.float32)
    
    total_pos = cum_tp[-1]
    if total_pos == 0:
        return float('nan')
    
    precision = cum_tp / k
    recall = cum_tp / total_pos
    
    # Take values only at positions where y_sorted == 1
    pos_mask = (y_sorted == 1)
    precision_pos = precision[pos_mask]
    recall_pos = recall[pos_mask]
    
    if precision_pos.numel() == 0:
        return float('nan')
    
    # Delta recall
    # recall_pos is already sorted increasing since we sorted by scores
    recall_prev = torch.cat([torch.zeros(1, device=device), recall_pos[:-1]])
    delta_recall = recall_pos - recall_prev
    
    ap = (precision_pos * delta_recall).sum()
    return float(ap.item())


def _ece_binary(
    y_true: Union[np.ndarray, torch.Tensor],
    y_scores: Union[np.ndarray, torch.Tensor],
    n_bins: int = 10
) -> Tuple[float, float, List[Dict[str, Any]]]:
    """
    Expected Calibration Error (ECE) and Maximum Calibration Error (MCE) for binary probabilities.
    Also returns reliability curve data. GPU-accelerated with PyTorch.
    
    Returns:
        (ece, mce, reliability_curve_data)
    """
    # Convert to tensors
    y_true = _to_tensor(y_true)
    y_scores = _to_tensor(y_scores)
    
    device = y_scores.device
    y_true = y_true.to(device).long()
    y_scores = y_scores.to(device).float()
    
    # Create bins
    bins = torch.linspace(0.0, 1.0, n_bins + 1, device=device)
    bin_lowers = bins[:-1]
    bin_uppers = bins[1:]
    
    ece_sum = torch.tensor(0.0, device=device)
    mce_max = torch.tensor(0.0, device=device)
    reliability_data = []
    N = y_true.numel()
    
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        # Find samples in this bin (vectorized)
        in_bin = (y_scores > bin_lower) & (y_scores <= bin_upper)
        prop_in_bin = in_bin.float().mean()
        
        if prop_in_bin > 0:
            # Mean predicted probability in this bin
            mean_pred_prob = y_scores[in_bin].mean()
            
            # Actual event frequency in this bin
            actual_freq = y_true[in_bin].float().mean()
            
            # Calibration error for this bin
            bin_error = torch.abs(mean_pred_prob - actual_freq)
            
            # Weight by proportion of samples in bin
            ece_sum = ece_sum + bin_error * prop_in_bin
            
            # Track maximum error
            mce_max = torch.max(mce_max, bin_error)
            
            # Store reliability curve data
            reliability_data.append({
                'bin_center': float((bin_lower + bin_upper) / 2.0),
                'mean_pred_prob': float(mean_pred_prob.item()),
                'actual_freq': float(actual_freq.item()),
                'prop_in_bin': float(prop_in_bin.item()),
                'bin_error': float(bin_error.item())
            })
        else:
            # Empty bin - still record for completeness
            reliability_data.append({
                'bin_center': float((bin_lower + bin_upper) / 2.0),
                'mean_pred_prob': None,
                'actual_freq': None,
                'prop_in_bin': 0.0,
                'bin_error': None
            })
    
    return float(ece_sum.item()), float(mce_max.item()), reliability_data


def _ece_multiclass(
    y_true: Union[np.ndarray, torch.Tensor],
    proba: Union[np.ndarray, torch.Tensor],
    n_bins: int = 10
) -> Tuple[float, float]:
    """
    ECE and MCE for multiclass using the predicted class probability. GPU-accelerated.
    
    Returns:
        (ece, mce)
    """
    # Convert to tensors
    y_true = _to_tensor(y_true)
    proba = _to_tensor(proba)
    
    device = proba.device
    y_true = y_true.to(device).long()
    proba = proba.to(device).float()
    
    y_pred = torch.argmax(proba, dim=1)
    p_max = proba[torch.arange(len(proba)), y_pred]
    correct = (y_pred == y_true).float()
    
    # Create bins
    bins = torch.linspace(0.0, 1.0, n_bins + 1, device=device)
    bin_lowers = bins[:-1]
    bin_uppers = bins[1:]
    
    ece_sum = torch.tensor(0.0, device=device)
    mce_max = torch.tensor(0.0, device=device)
    
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        mask = (p_max >= bin_lower) & (p_max < bin_upper)
        if not mask.any():
            continue
        
        conf = p_max[mask].mean()
        acc = correct[mask].mean()
        bin_error = torch.abs(conf - acc)
        
        prop_in_bin = mask.float().mean()
        ece_sum = ece_sum + bin_error * prop_in_bin
        
        mce_max = torch.max(mce_max, bin_error)
    
    return float(ece_sum.item()), float(mce_max.item())


def _compute_baseline_cost_binary(
    y_true: Union[np.ndarray, torch.Tensor],
    cost_fp: float,
    cost_fn: float
) -> float:
    """
    Simple baseline: always predict negative (no positives flagged).
    Cost = cost_fn * (#positives). GPU-accelerated.
    """
    y_true = _to_tensor(y_true)
    if isinstance(y_true, torch.Tensor):
        n_pos = int((y_true == 1).sum().item())
    else:
        n_pos = int(np.sum(y_true == 1))
    return float(cost_fn * n_pos)


def cost_optimal_threshold_binary(
    y_true: Union[np.ndarray, torch.Tensor],
    y_scores: Union[np.ndarray, torch.Tensor],
    cost_fp: float,
    cost_fn: float,
    min_pred_pos_frac: float = 0.0,
    max_pred_pos_frac: float = 1.0,
) -> Dict[str, Any]:
    """
    Vectorized cost-optimal threshold selection on GPU.
    
    y_true:   (N,) int {0,1}
    y_scores: (N,) float [0,1]
    
    Returns:
        stats_dict with tp, fp, tn, fn, tau, acc, f1, balanced_acc, mcc, pred_pos_rate, min_cost
    """
    # Convert to tensors and ensure on same device
    if isinstance(y_true, np.ndarray):
        y_true = torch.from_numpy(y_true)
    if isinstance(y_scores, np.ndarray):
        y_scores = torch.from_numpy(y_scores)
    
    device = y_scores.device
    y_true = y_true.to(device).long()
    y_scores = y_scores.to(device).float()
    
    N = y_true.numel()
    if N == 0:
        raise ValueError("Empty y_true")
    
    # Sort scores descending
    scores_sorted, idx = torch.sort(y_scores, descending=True)
    y_sorted = y_true[idx]  # (N,)
    
    # Cumulative positives as we go down the ranking
    ones = torch.ones_like(y_sorted, dtype=torch.long)
    cum_pos = torch.cumsum(y_sorted, dim=0)  # TP_k
    cum_all = torch.cumsum(ones, dim=0)  # k = 1..N
    
    total_pos = cum_pos[-1]
    total_neg = N - total_pos
    
    # For k positives predicted (top k)
    tp = cum_pos  # (N,)
    fp = cum_all - tp
    fn = total_pos - tp
    tn = total_neg - fp
    
    # Predicted positive rate per k
    pred_pos_rate = cum_all.float() / float(N)
    
    # Cost per k
    cost_fp_t = torch.tensor(cost_fp, device=device, dtype=torch.float32)
    cost_fn_t = torch.tensor(cost_fn, device=device, dtype=torch.float32)
    cost = cost_fp_t * fp.float() + cost_fn_t * fn.float()  # (N,)
    
    # Apply pred_pos_rate band
    mask = (pred_pos_rate >= min_pred_pos_frac) & (pred_pos_rate <= max_pred_pos_frac)
    if mask.any():
        masked_cost = torch.where(mask, cost, torch.tensor(float('inf'), device=device))
        k_star = torch.argmin(masked_cost)
    else:
        # No k satisfies band → use unconstrained min
        k_star = torch.argmin(cost)
    
    k_star = int(k_star.item())
    tau = float(scores_sorted[k_star].item())  # threshold at that score
    
    # Metrics at this threshold
    tp_k = int(tp[k_star].item())
    fp_k = int(fp[k_star].item())
    fn_k = int(fn[k_star].item())
    tn_k = int(tn[k_star].item())
    
    # Reconstruct predictions at tau (to avoid off-by-one weirdness)
    y_pred = (y_scores >= tau).long()
    acc = float((y_pred == y_true).float().mean().item())
    
    # F1, balanced accuracy, MCC
    denom_f1 = (2 * tp_k + fp_k + fn_k)
    f1 = 0.0 if denom_f1 == 0 else (2.0 * tp_k) / denom_f1
    
    tpr = tp_k / max(1, tp_k + fn_k)
    tnr = tn_k / max(1, tn_k + fp_k)
    bal_acc = (tpr + tnr) / 2.0
    
    mcc_denom = (tp_k + fp_k) * (tp_k + fn_k) * (tn_k + fp_k) * (tn_k + fn_k)
    if mcc_denom > 0:
        mcc = ((tp_k * tn_k) - (fp_k * fn_k)) / (mcc_denom ** 0.5)
    else:
        mcc = 0.0
    
    stats = {
        "tp": tp_k,
        "fp": fp_k,
        "tn": tn_k,
        "fn": fn_k,
        "tau": tau,
        "acc": acc,
        "f1": f1,
        "balanced_acc": bal_acc,
        "mcc": mcc,
        "pred_pos_rate": float(pred_pos_rate[k_star].item()),
        "min_cost": float(cost[k_star].item()),
    }
    return stats


def _find_cost_opt_threshold_binary(
    y_true: Union[np.ndarray, torch.Tensor],
    y_scores: Union[np.ndarray, torch.Tensor],
    cost_fp: float,
    cost_fn: float,
    min_pred_pos_frac: Optional[float] = None,
    max_pred_pos_frac: Optional[float] = None,
    n_thresholds: int = 201,
) -> Tuple[float, float, Dict[str, Any]]:
    """
    Wrapper for cost_optimal_threshold_binary that returns (tau, cost, stats).
    Maintains backward compatibility.
    """
    min_frac = min_pred_pos_frac if min_pred_pos_frac is not None else 0.0
    max_frac = max_pred_pos_frac if max_pred_pos_frac is not None else 1.0
    
    stats = cost_optimal_threshold_binary(
        y_true, y_scores, cost_fp, cost_fn,
        min_pred_pos_frac=min_frac,
        max_pred_pos_frac=max_frac,
    )
    
    return stats["tau"], stats["min_cost"], stats


def _choose_binary_weights(pos_rate: float) -> Tuple[float, float, float]:
    """
    Decide weights for PR-AUC, cost-savings, ROC-AUC in composite score.
    """
    if pos_rate < 0.05:
        # Very rare positives: PR-AUC primary
        return 0.6, 0.3, 0.1
    elif pos_rate < 0.2:
        return 0.5, 0.3, 0.2
    else:
        # e.g. credit-g at 30%
        return 0.4, 0.3, 0.3


def _normalize_logloss_multiclass(ll: float) -> float:
    """
    Map log loss to [0,1] in a simple, monotonic way.
    0.0 -> 1.0, large loss -> ~0
    """
    return float(1.0 / (1.0 + ll))


def _confusion_entropy_multiclass(y_true: np.ndarray, y_pred: np.ndarray, n_classes: int) -> float:
    """
    Compute confusion entropy for multiclass classification.
    Measures disorder in the confusion matrix.
    """
    try:
        cm = confusion_matrix(y_true, y_pred, labels=np.arange(n_classes))
        
        # Normalize confusion matrix to probabilities
        cm_norm = cm.astype(float) / (cm.sum(axis=1, keepdims=True) + 1e-10)
        
        # Compute entropy for each row (actual class)
        entropy_sum = 0.0
        for i in range(n_classes):
            row = cm_norm[i, :]
            # Remove zeros to avoid log(0)
            row = row[row > 0]
            if len(row) > 0:
                entropy_sum += -np.sum(row * np.log(row + 1e-10))
        
        # Average entropy across classes
        return float(entropy_sum / n_classes) if n_classes > 0 else 0.0
    except Exception as e:
        logger.warning(f"Failed to compute confusion entropy: {e}")
        return 0.0


# ---------------------------------------------------------------------------
# MetricPolicy
# ---------------------------------------------------------------------------

@dataclass
class MetricPolicy:
    """
    MetricPolicy decides how to evaluate and score epochs for checkpoint
    selection, given the problem type and optional cost settings.
    
    Supports:
        - Binary classification
        - Multiclass (single-label)
    
    Multilabel will be added later.
    """
    problem_type: str  # "binary" or "multiclass"
    n_classes: int
    pos_label: Optional[Any] = None  # for binary (can be any type)
    cost_fp: float = 1.0
    cost_fn: Optional[float] = None  # if None, derived from imbalance
    
    @classmethod
    def from_targets(
        cls,
        y_true: Sequence,
        cost_fp: float = 1.0,
        cost_fn: Optional[float] = None,
        pos_label: Optional[Any] = None,
    ) -> "MetricPolicy":
        """
        Infer problem_type and default costs from labels.
        
        For binary:
            - positive class = minority (or pos_label if provided)
            - default cost_fn = (#neg / #pos) if not supplied
        """
        y_arr = np.asarray(y_true)
        classes = np.unique(y_arr)
        n_classes = classes.size
        
        if n_classes <= 1:
            raise ValueError("Need at least 2 distinct labels.")
        
        if n_classes == 2:
            problem_type = "binary"
            
            # Determine positive label
            if pos_label is None:
                # Pick minority as positive
                counts = {c: int(np.sum(y_arr == c)) for c in classes}
                pos_label = min(counts, key=counts.get)
            
            # Derive cost_fn if not provided
            if cost_fn is None:
                pos_mask = (y_arr == pos_label)
                n_pos = int(pos_mask.sum())
                n_neg = int(len(y_arr) - n_pos)
                if n_pos == 0:
                    raise ValueError("No positive examples; cannot define cost_fn.")
                cost_fn = float(n_neg / n_pos)
        else:
            problem_type = "multiclass"
            pos_label = None
            # cost_fp/fn not used for multiclass (yet)
        
        return cls(
            problem_type=problem_type,
            n_classes=n_classes,
            pos_label=pos_label,
            cost_fp=cost_fp,
            cost_fn=cost_fn,
        )
    
    # ---------------------------------------------------------------------
    # Epoch metric computation
    # ---------------------------------------------------------------------
    
    def compute_epoch_metrics(
        self,
        y_true: np.ndarray,
        outputs: np.ndarray,
    ) -> Dict[str, Any]:
        """
        Compute metrics for a single epoch.
        
        Parameters
        ----------
        y_true : np.ndarray
            True labels (shape (N,)), can be any type.
        outputs : np.ndarray
            - Binary: predicted probabilities for positive class (shape (N,))
            - Multiclass: predicted probabilities per class (shape (N, C))
        
        Returns
        -------
        metrics : dict
            Dictionary of metrics appropriate to the problem type.
        """
        y_true = np.asarray(y_true)
        
        if self.problem_type == "binary":
            y_scores = np.asarray(outputs).reshape(-1)
            return self._compute_epoch_metrics_binary(y_true, y_scores)
        else:
            proba = np.asarray(outputs)
            return self._compute_epoch_metrics_multiclass(y_true, proba)
    
    def _compute_epoch_metrics_binary(
        self,
        y_true: np.ndarray,
        y_scores: np.ndarray,
    ) -> Dict[str, Any]:
        """Compute binary classification metrics."""
        # Remap labels to {0,1} if needed
        if self.pos_label is not None:
            y_bin = (y_true == self.pos_label).astype(int)
        else:
            # Assume already 0/1
            y_bin = y_true.astype(int)
        
        pos_rate = float(np.mean(y_bin == 1))
        
        # Ranking metrics
        try:
            roc_auc = roc_auc_score(y_bin, y_scores)
        except Exception:
            roc_auc = np.nan
        
        try:
            pr_auc = average_precision_score(y_bin, y_scores)
        except Exception:
            pr_auc = np.nan
        
        # Cost-aware threshold search (GPU-accelerated)
        cost_fp = float(self.cost_fp)
        cost_fn = float(self.cost_fn) if self.cost_fn is not None else 1.0
        
        # Allow predicted positive rate within [0.5 * pos_rate, 1.5 * pos_rate]
        min_frac = max(0.0, pos_rate * 0.5)
        max_frac = min(1.0, pos_rate * 1.5)
        
        tau_cost, cost_min, stats = _find_cost_opt_threshold_binary(
            y_bin,
            y_scores,
            cost_fp=cost_fp,
            cost_fn=cost_fn,
            min_pred_pos_frac=min_frac,
            max_pred_pos_frac=max_frac,
        )
        
        # Calibration & behavior (GPU-accelerated)
        # Brier score: mean squared error of probabilities
        brier = float(((y_scores - y_bin.float()) ** 2).mean().item())
        
        ece, mce, reliability_curve = _ece_binary(y_bin, y_scores, n_bins=10)
        sharpness = float(y_scores.var().item())
        
        # Imbalanced data metrics (at cost-optimal threshold)
        # TPR = Recall = TP / (TP + FN)
        tpr = stats['tp'] / (stats['tp'] + stats['fn']) if (stats['tp'] + stats['fn']) > 0 else 0.0
        # TNR = Specificity = TN / (TN + FP)
        tnr = stats['tn'] / (stats['tn'] + stats['fp']) if (stats['tn'] + stats['fp']) > 0 else 0.0
        # Balanced Accuracy = (TPR + TNR) / 2
        balanced_acc = (tpr + tnr) / 2.0
        
        baseline_cost = _compute_baseline_cost_binary(y_bin, cost_fp, cost_fn)
        
        metrics = {
            "problem_type": "binary",
            "pos_rate": pos_rate,
            "roc_auc": float(roc_auc),
            "pr_auc": float(pr_auc),
            "cost_min": float(cost_min),
            "baseline_cost": float(baseline_cost),
            "tau_cost": float(tau_cost),
            "tp": stats["tp"],
            "fp": stats["fp"],
            "tn": stats["tn"],
            "fn": stats["fn"],
            "f1_cost": stats["f1"],
            "acc_cost": stats["acc"],
            "balanced_acc_cost": stats["balanced_acc"],
            "mcc_cost": stats["mcc"],
            "pred_pos_rate_cost": stats["pred_pos_rate"],
            "tpr": float(tpr),
            "tnr": float(tnr),
            "balanced_accuracy": float(balanced_acc),
            "brier": float(brier),
            "ece": float(ece),
            "mce": float(mce),
            "sharpness": sharpness,
            "reliability_curve": reliability_curve,
        }
        return metrics
    
    def _compute_epoch_metrics_multiclass(
        self,
        y_true: Union[np.ndarray, torch.Tensor],
        proba: Union[np.ndarray, torch.Tensor],
    ) -> Dict[str, Any]:
        """
        Multiclass (single-label) metrics. GPU-accelerated where possible.
        """
        # Convert to tensors
        y_true = _to_tensor(y_true)
        proba = _to_tensor(proba)
        
        # Ensure on same device
        device = proba.device if isinstance(proba, torch.Tensor) else torch.device('cpu')
        y_true = y_true.to(device) if isinstance(y_true, torch.Tensor) else _to_tensor(y_true, device)
        proba = proba.to(device) if isinstance(proba, torch.Tensor) else _to_tensor(proba, device)
        
        n_samples, n_classes = proba.shape
        if n_classes != self.n_classes:
            raise ValueError(f"Expected proba.shape[1]={self.n_classes}, got {n_classes}")
        
        y_pred = torch.argmax(proba, dim=1)
        
        # Core metrics (GPU-accelerated)
        acc = float((y_pred == y_true).float().mean().item())
        
        # Log loss: -mean(log(p_true_class))
        try:
            y_true_long = y_true.long()
            # Gather probabilities for true classes
            probs_true = proba[torch.arange(n_samples), y_true_long]
            # Avoid log(0)
            probs_true = torch.clamp(probs_true, min=1e-15)
            ll = float(-torch.log(probs_true).mean().item())
        except Exception:
            # Fallback to sklearn
            try:
                ll = log_loss(_to_numpy(y_true), _to_numpy(proba), labels=np.arange(self.n_classes))
            except Exception:
                ll = np.nan
        
        # F1 scores using sklearn (more stable)
        macro_f1 = f1_score(_to_numpy(y_true), _to_numpy(y_pred), average="macro", zero_division=0)
        weighted_f1 = f1_score(_to_numpy(y_true), _to_numpy(y_pred), average="weighted", zero_division=0)
        
        # Top-k: use min(3, n_classes) as example
        k = min(3, self.n_classes)
        try:
            # GPU-accelerated top-k accuracy
            # Get top-k predictions
            topk_probs, topk_preds = torch.topk(proba, k, dim=1)
            # Check if true label is in top-k
            y_true_expanded = y_true.unsqueeze(1).expand(-1, k)
            topk_correct = (topk_preds == y_true_expanded).any(dim=1)
            topk_acc = float(topk_correct.float().mean().item())
        except Exception:
            # Fallback to sklearn
            try:
                topk_acc = top_k_accuracy_score(_to_numpy(y_true), _to_numpy(proba), k=k, labels=np.arange(self.n_classes))
            except Exception:
                topk_acc = np.nan
        
        # Confusion entropy (CPU - uses sklearn)
        confusion_entropy = _confusion_entropy_multiclass(_to_numpy(y_true), _to_numpy(y_pred), self.n_classes)
        
        # Balanced accuracy (CPU - uses sklearn)
        try:
            balanced_acc = balanced_accuracy_score(_to_numpy(y_true), _to_numpy(y_pred))
        except Exception:
            balanced_acc = 0.0
        
        # Calibration (GPU-accelerated)
        # Multiclass Brier: mean over samples of sum_j (p_j - y_j)^2
        y_onehot = torch.zeros_like(proba)
        y_onehot[torch.arange(n_samples), y_true.long()] = 1.0
        brier_multi = float(((proba - y_onehot) ** 2).sum(dim=1).mean().item())
        
        ece, mce = _ece_multiclass(y_true, proba, n_bins=10)
        sharpness = float(proba.var(dim=1).mean().item())  # variance per row
        
        # Entropy of predicted softmax (GPU-accelerated)
        # High entropy = uncertain, low entropy = overconfident
        # Entropy = -sum(p * log(p))
        log_proba = torch.log(proba + 1e-10)
        entropy_per_sample = -(proba * log_proba).sum(dim=1)
        entropy_softmax = float(entropy_per_sample.mean().item())
        
        metrics = {
            "problem_type": "multiclass",
            "acc": acc,
            "log_loss": float(ll),
            "macro_f1": float(macro_f1),
            "weighted_f1": float(weighted_f1),
            "topk_acc": float(topk_acc),
            "balanced_accuracy": float(balanced_acc),
            "confusion_entropy": float(confusion_entropy),
            "brier": float(brier_multi),
            "ece": float(ece),
            "mce": float(mce),
            "sharpness": sharpness,
            "entropy_softmax": float(entropy_softmax),
            "k": k,
            "n_classes": self.n_classes,
        }
        return metrics
    
    # ---------------------------------------------------------------------
    # Scoring for checkpoint selection
    # ---------------------------------------------------------------------
    
    def score_epoch(self, metrics: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        Compute a composite scalar score for checkpoint selection.
        
        For binary:
            Score = α * PR-AUC + β * cost_savings + γ * ROC-AUC
        
        For multiclass:
            Score = 0.5 * f(log_loss) + 0.3 * macro-F1 + 0.2 * top-k accuracy
        """
        if metrics["problem_type"] == "binary":
            return self._score_epoch_binary(metrics)
        else:
            return self._score_epoch_multiclass(metrics)
    
    def _score_epoch_binary(self, m: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        roc_auc = m["roc_auc"]
        pr_auc = m["pr_auc"]
        cost_min = m["cost_min"]
        baseline_cost = m["baseline_cost"]
        pos_rate = m["pos_rate"]
        
        if np.isnan(roc_auc):
            roc_auc = 0.5
        if np.isnan(pr_auc):
            pr_auc = 0.0
        
        if baseline_cost > 0.0:
            cost_savings = (baseline_cost - cost_min) / baseline_cost
        else:
            cost_savings = 0.0
        cost_savings = float(np.clip(cost_savings, 0.0, 1.0))
        
        alpha, beta, gamma = _choose_binary_weights(pos_rate)
        
        score = (alpha * pr_auc) + (beta * cost_savings) + (gamma * roc_auc)
        
        extra = {
            "roc_auc": roc_auc,
            "pr_auc": pr_auc,
            "cost_savings": cost_savings,
            "alpha": alpha,
            "beta": beta,
            "gamma": gamma,
        }
        return float(score), extra
    
    def _score_epoch_multiclass(self, m: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        ll = m["log_loss"]
        macro_f1 = m["macro_f1"]
        topk_acc = m["topk_acc"]
        
        if np.isnan(ll):
            ll = 10.0  # terrible
        if np.isnan(topk_acc):
            topk_acc = 0.0
        
        # Normalize log loss to [0,1], higher is better
        ll_norm = _normalize_logloss_multiclass(ll)
        
        # Simple weights; can be tuned later
        alpha = 0.5  # log loss (via ll_norm)
        beta = 0.3  # macro-F1
        gamma = 0.2  # top-k acc
        
        score = alpha * ll_norm + beta * macro_f1 + gamma * topk_acc
        
        extra = {
            "log_loss": ll,
            "log_loss_norm": ll_norm,
            "macro_f1": macro_f1,
            "topk_acc": topk_acc,
            "alpha": alpha,
            "beta": beta,
            "gamma": gamma,
        }
        return float(score), extra

