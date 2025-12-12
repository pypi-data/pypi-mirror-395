#!/usr/bin/env python3
"""
Intelligent model configuration advisor.

Analyzes data characteristics and recommends:
- Best loss function for the class distribution
- Appropriate metrics for evaluation
- Training configuration parameters
- Detects model health issues
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ImbalanceSeverity(Enum):
    """Class imbalance severity levels."""
    BALANCED = "balanced"           # ~50/50 (40-60%)
    MILD = "mild"                   # 60-75% or 25-40%
    MODERATE = "moderate"           # 75-90% or 10-25%
    SEVERE = "severe"               # 90-95% or 5-10%
    EXTREME = "extreme"             # >95% or <5%


@dataclass
class ClassDistribution:
    """Class distribution analysis."""
    classes: Dict[str, int]
    total: int
    majority_class: str
    minority_class: str
    majority_ratio: float
    minority_ratio: float
    imbalance_ratio: float  # majority/minority
    severity: ImbalanceSeverity


@dataclass
class LossRecommendation:
    """Loss function recommendation."""
    loss_type: str
    confidence: float  # 0-1
    reason: str
    alternatives: List[Tuple[str, str]]  # [(loss_type, reason), ...]
    parameters: Dict[str, Any]  # Suggested hyperparameters


@dataclass
class MetricsRecommendation:
    """Metrics recommendation for evaluation."""
    primary_metrics: List[str]  # Most important for this scenario
    secondary_metrics: List[str]  # Additional useful metrics
    avoid_metrics: List[str]  # Misleading for this scenario
    rationale: Dict[str, str]  # Why each metric is included/excluded


@dataclass
class ModelHealthReport:
    """Model health assessment."""
    is_healthy: bool
    issues: List[str]
    warnings: List[str]
    recommendations: List[str]
    stability_score: float  # 0-1 (1 is most stable)
    learning_score: float   # 0-1 (1 is learning well)
    generalization_score: float  # 0-1 (1 is generalizing well)


class ModelAdvisor:
    """
    Intelligent advisor for model configuration and evaluation.
    """
    
    def analyze_class_distribution(
        self, 
        y: np.ndarray,
        pos_label: Optional[str] = None
    ) -> ClassDistribution:
        """
        Analyze class distribution in target variable.
        
        Args:
            y: Target variable (labels)
            pos_label: Optional positive label (for binary)
            
        Returns:
            ClassDistribution object with detailed analysis
        """
        unique, counts = np.unique(y, return_counts=True)
        total = len(y)
        
        classes = dict(zip(unique, counts))
        
        # Find majority/minority
        majority_idx = np.argmax(counts)
        minority_idx = np.argmin(counts)
        
        majority_class = unique[majority_idx]
        minority_class = unique[minority_idx]
        
        majority_ratio = counts[majority_idx] / total
        minority_ratio = counts[minority_idx] / total
        
        imbalance_ratio = counts[majority_idx] / counts[minority_idx]
        
        # Determine severity
        if minority_ratio >= 0.40:
            severity = ImbalanceSeverity.BALANCED
        elif minority_ratio >= 0.25:
            severity = ImbalanceSeverity.MILD
        elif minority_ratio >= 0.10:
            severity = ImbalanceSeverity.MODERATE
        elif minority_ratio >= 0.05:
            severity = ImbalanceSeverity.SEVERE
        else:
            severity = ImbalanceSeverity.EXTREME
        
        return ClassDistribution(
            classes=classes,
            total=total,
            majority_class=str(majority_class),
            minority_class=str(minority_class),
            majority_ratio=majority_ratio,
            minority_ratio=minority_ratio,
            imbalance_ratio=imbalance_ratio,
            severity=severity
        )
    
    def recommend_loss_function(
        self,
        distribution: ClassDistribution,
        task_priority: str = "balanced"  # "balanced", "recall", "precision"
    ) -> LossRecommendation:
        """
        Recommend best loss function based on class distribution.
        
        Args:
            distribution: Class distribution analysis
            task_priority: What matters most for the task
            
        Returns:
            LossRecommendation with suggested loss and parameters
        """
        severity = distribution.severity
        ratio = distribution.imbalance_ratio
        
        # Decision logic based on imbalance severity and task requirements
        if severity == ImbalanceSeverity.BALANCED:
            return LossRecommendation(
                loss_type="cross_entropy",
                confidence=0.9,
                reason="Classes are well balanced; standard cross-entropy is optimal",
                alternatives=[
                    ("focal", "Can still help focus on hard examples if accuracy plateaus"),
                ],
                parameters={}
            )
        
        elif severity == ImbalanceSeverity.MILD:
            if task_priority == "recall":
                return LossRecommendation(
                    loss_type="focal",
                    confidence=0.7,
                    reason="Mild imbalance with recall priority; focal loss helps minority class",
                    alternatives=[
                        ("cross_entropy", "May work with class weights"),
                        ("weighted_cross_entropy", "Good alternative with explicit weights"),
                    ],
                    parameters={"gamma": 1.0, "alpha": 0.75}
                )
            else:
                return LossRecommendation(
                    loss_type="cross_entropy",
                    confidence=0.75,
                    reason="Mild imbalance; cross-entropy with monitoring is reasonable",
                    alternatives=[
                        ("focal", "Consider if minority class performance is poor"),
                        ("weighted_cross_entropy", "Good for explicit control"),
                    ],
                    parameters={"class_weights": {
                        distribution.majority_class: 1.0,
                        distribution.minority_class: ratio * 0.5
                    }}
                )
        
        elif severity == ImbalanceSeverity.MODERATE:
            return LossRecommendation(
                loss_type="focal",
                confidence=0.85,
                reason=f"Moderate imbalance ({ratio:.1f}:1); focal loss handles this well",
                alternatives=[
                    ("weighted_cross_entropy", "Explicit weight control may work"),
                    ("asymmetric", "If false negatives are much worse than false positives"),
                ],
                parameters={"gamma": 2.0, "alpha": 0.75}
            )
        
        elif severity == ImbalanceSeverity.SEVERE:
            return LossRecommendation(
                loss_type="focal",
                confidence=0.95,
                reason=f"Severe imbalance ({ratio:.1f}:1); focal loss is strongly recommended",
                alternatives=[
                    ("class_balanced_focal", "Even better handling of extreme imbalance"),
                    ("dice_loss", "Good for very rare positive class"),
                ],
                parameters={"gamma": 2.5, "alpha": 0.8}
            )
        
        else:  # EXTREME
            return LossRecommendation(
                loss_type="class_balanced_focal",
                confidence=0.98,
                reason=f"Extreme imbalance ({ratio:.1f}:1); specialized loss required",
                alternatives=[
                    ("focal", "Good but may need higher gamma"),
                    ("dice_loss", "Excellent for extremely rare positives"),
                    ("tversky_loss", "Flexible control of FP/FN balance"),
                ],
                parameters={"gamma": 3.0, "alpha": 0.9, "beta": 0.999}
            )
    
    def recommend_metrics(
        self,
        distribution: ClassDistribution,
        task_type: str = "classification"
    ) -> MetricsRecommendation:
        """
        Recommend appropriate metrics based on class distribution.
        
        Args:
            distribution: Class distribution analysis
            task_type: Type of task (classification, etc.)
            
        Returns:
            MetricsRecommendation with prioritized metrics
        """
        severity = distribution.severity
        
        if severity == ImbalanceSeverity.BALANCED:
            return MetricsRecommendation(
                primary_metrics=["accuracy", "f1", "auc"],
                secondary_metrics=["precision", "recall", "confusion_matrix"],
                avoid_metrics=[],
                rationale={
                    "accuracy": "Classes balanced; accuracy is meaningful",
                    "f1": "Good overall measure of precision/recall balance",
                    "auc": "Threshold-independent performance measure",
                    "precision": "Useful for understanding false positive rate",
                    "recall": "Useful for understanding false negative rate",
                }
            )
        
        elif severity == ImbalanceSeverity.MILD:
            return MetricsRecommendation(
                primary_metrics=["f1", "auc", "balanced_accuracy"],
                secondary_metrics=["precision", "recall", "mcc", "pr_auc"],
                avoid_metrics=["accuracy"],
                rationale={
                    "f1": "Better than accuracy for slight imbalance",
                    "auc": "Threshold-independent, good for imbalanced data",
                    "balanced_accuracy": "Accounts for class imbalance",
                    "accuracy": "Can be misleading; majority class bias possible",
                    "mcc": "Good single metric for imbalanced data",
                    "pr_auc": "Better than ROC-AUC for imbalanced data",
                }
            )
        
        elif severity in [ImbalanceSeverity.MODERATE, ImbalanceSeverity.SEVERE]:
            return MetricsRecommendation(
                primary_metrics=["mcc", "balanced_accuracy", "pr_auc", "f1"],
                secondary_metrics=["precision", "recall", "specificity", "g_mean"],
                avoid_metrics=["accuracy", "auc"],
                rationale={
                    "mcc": "Best single metric for imbalanced classification",
                    "balanced_accuracy": "Equal weight to both classes",
                    "pr_auc": "Much better than ROC-AUC for imbalanced data",
                    "f1": "Harmonic mean focuses on minority class",
                    "accuracy": "Very misleading; can be high by predicting majority",
                    "auc": "ROC-AUC can be optimistic with severe imbalance",
                    "precision": "Critical for understanding false positives",
                    "recall": "Critical for catching minority class",
                    "specificity": "Ensure not over-predicting minority",
                    "g_mean": "Geometric mean of sensitivity/specificity",
                }
            )
        
        else:  # EXTREME
            return MetricsRecommendation(
                primary_metrics=["mcc", "pr_auc", "recall", "precision"],
                secondary_metrics=["f1", "balanced_accuracy", "brier_score"],
                avoid_metrics=["accuracy", "auc"],
                rationale={
                    "mcc": "Only reliable single metric at extreme imbalance",
                    "pr_auc": "Essential - ROC-AUC is meaningless here",
                    "recall": "Must know if we're catching minority class at all",
                    "precision": "Must know false positive rate",
                    "accuracy": "Completely misleading at extreme imbalance",
                    "auc": "ROC-AUC is very misleading with extreme imbalance",
                    "f1": "Useful but can mask low precision or recall",
                    "brier_score": "Calibration is critical with rare events",
                }
            )
    
    def assess_model_health(
        self,
        train_losses: List[float],
        val_losses: List[float],
        train_metrics: Dict[str, List[float]],
        val_metrics: Dict[str, List[float]],
        best_epoch: int
    ) -> ModelHealthReport:
        """
        Assess overall model health and detect issues.
        
        Args:
            train_losses: Training loss history
            val_losses: Validation loss history
            train_metrics: Training metrics history
            val_metrics: Validation metrics history
            best_epoch: Epoch with best validation loss
            
        Returns:
            ModelHealthReport with issues and recommendations
        """
        issues = []
        warnings = []
        recommendations = []
        
        train_losses_arr = np.array(train_losses)
        val_losses_arr = np.array(val_losses)
        
        # Check if training is happening at all
        if len(train_losses) < 3:
            issues.append("Insufficient training epochs to assess model health")
            return ModelHealthReport(
                is_healthy=False,
                issues=issues,
                warnings=warnings,
                recommendations=["Train for at least 10 epochs"],
                stability_score=0.0,
                learning_score=0.0,
                generalization_score=0.0
            )
        
        # 1. Check if model is learning
        train_improvement = (train_losses_arr[0] - train_losses_arr[-1]) / train_losses_arr[0]
        
        if train_improvement < 0.01:
            issues.append(f"Model not learning: training loss only improved {train_improvement*100:.1f}%")
            recommendations.append("Try increasing learning rate or model capacity")
            learning_score = 0.2
        elif train_improvement < 0.05:
            warnings.append(f"Slow learning: training loss improved only {train_improvement*100:.1f}%")
            recommendations.append("Consider increasing learning rate")
            learning_score = 0.5
        else:
            learning_score = min(1.0, train_improvement * 2)
        
        # 2. Check for overfitting
        if len(val_losses) >= 3:
            val_trend = np.polyfit(range(len(val_losses)), val_losses, 1)[0]
            train_val_gap = abs(train_losses_arr[-1] - val_losses_arr[-1])
            relative_gap = train_val_gap / train_losses_arr[-1] if train_losses_arr[-1] > 0 else 0
            
            if val_trend > 0.01 and relative_gap > 0.5:
                issues.append(f"Severe overfitting: val loss increasing while train loss decreases (gap: {relative_gap:.2f}x)")
                recommendations.append("Add regularization: increase dropout, weight decay, or reduce model capacity")
                generalization_score = 0.2
            elif val_trend > 0.005 or relative_gap > 0.3:
                warnings.append(f"Overfitting detected: train/val gap is {relative_gap:.2f}x")
                recommendations.append("Consider early stopping or more regularization")
                generalization_score = 0.5
            else:
                generalization_score = max(0.5, 1.0 - relative_gap)
        else:
            generalization_score = 0.5
        
        # 3. Check for instability
        if len(train_losses) >= 5:
            # Calculate variance of loss changes
            train_changes = np.diff(train_losses_arr)
            train_volatility = np.std(train_changes) / (np.mean(np.abs(train_changes)) + 1e-8)
            
            val_changes = np.diff(val_losses_arr)
            val_volatility = np.std(val_changes) / (np.mean(np.abs(val_changes)) + 1e-8)
            
            if train_volatility > 2.0 or val_volatility > 2.0:
                issues.append(f"Training unstable: high loss variance (train: {train_volatility:.2f}, val: {val_volatility:.2f})")
                recommendations.append("Reduce learning rate or use learning rate scheduling")
                stability_score = 0.3
            elif train_volatility > 1.0 or val_volatility > 1.0:
                warnings.append(f"Some training instability detected (train: {train_volatility:.2f}, val: {val_volatility:.2f})")
                recommendations.append("Consider learning rate reduction or gradient clipping")
                stability_score = 0.6
            else:
                stability_score = 1.0 - min(0.5, (train_volatility + val_volatility) / 4)
        else:
            stability_score = 0.5
        
        # 4. Check if best epoch is at the end (might need more training)
        if best_epoch >= len(val_losses) - 2:
            warnings.append("Best model found at end of training; may benefit from more epochs")
            recommendations.append("Train for more epochs to ensure convergence")
        
        # 5. Check if best epoch is very early (might be issues)
        if best_epoch <= 2:
            warnings.append("Best model found very early; model may not be learning effectively")
            recommendations.append("Check learning rate and model capacity")
        
        # 6. Check for degenerate solutions (if metrics available)
        if "accuracy" in val_metrics and val_metrics["accuracy"]:
            final_acc = val_metrics["accuracy"][-1]
            if final_acc > 0.95 or final_acc < 0.55:
                warnings.append(f"Unusual accuracy {final_acc:.3f}; check for class imbalance or degenerate predictions")
                recommendations.append("Verify model isn't predicting single class; check confusion matrix")
        
        # Overall health
        avg_score = (stability_score + learning_score + generalization_score) / 3
        is_healthy = len(issues) == 0 and avg_score > 0.6
        
        if not recommendations:
            recommendations.append("Model appears healthy; continue monitoring on test data")
        
        return ModelHealthReport(
            is_healthy=is_healthy,
            issues=issues,
            warnings=warnings,
            recommendations=recommendations,
            stability_score=stability_score,
            learning_score=learning_score,
            generalization_score=generalization_score
        )
    
    def generate_training_config(
        self,
        distribution: ClassDistribution,
        n_samples: int,
        n_features: int
    ) -> Dict[str, Any]:
        """
        Generate recommended training configuration.
        
        Args:
            distribution: Class distribution analysis
            n_samples: Number of training samples
            n_features: Number of features
            
        Returns:
            Dictionary with recommended training parameters
        """
        config = {}
        
        # Batch size based on sample count
        if n_samples < 500:
            config["batch_size"] = 32
        elif n_samples < 5000:
            config["batch_size"] = 64
        elif n_samples < 50000:
            config["batch_size"] = 128
        else:
            config["batch_size"] = 256
        
        # Learning rate based on imbalance and sample size
        if distribution.severity in [ImbalanceSeverity.SEVERE, ImbalanceSeverity.EXTREME]:
            config["learning_rate"] = 0.0001  # Lower LR for difficult cases
        elif n_samples < 1000:
            config["learning_rate"] = 0.0005
        else:
            config["learning_rate"] = 0.001
        
        # Epochs based on sample size
        if n_samples < 1000:
            config["epochs"] = 150
        elif n_samples < 10000:
            config["epochs"] = 100
        else:
            config["epochs"] = 75
        
        # Early stopping patience
        config["early_stopping_patience"] = max(10, config["epochs"] // 10)
        
        # Regularization based on sample size and features
        samples_per_feature = n_samples / max(1, n_features)
        if samples_per_feature < 10:
            config["dropout"] = 0.5
            config["weight_decay"] = 0.01
        elif samples_per_feature < 50:
            config["dropout"] = 0.3
            config["weight_decay"] = 0.001
        else:
            config["dropout"] = 0.2
            config["weight_decay"] = 0.0001
        
        return config


if __name__ == "__main__":
    # Example usage
    advisor = ModelAdvisor()
    
    # Simulate different imbalance scenarios
    scenarios = [
        ("Balanced", np.array([0]*500 + [1]*500)),
        ("Mild Imbalance", np.array([0]*700 + [1]*300)),
        ("Moderate Imbalance", np.array([0]*850 + [1]*150)),
        ("Severe Imbalance", np.array([0]*950 + [1]*50)),
        ("Extreme Imbalance", np.array([0]*990 + [1]*10)),
    ]
    
    print("=" * 100)
    print("MODEL ADVISOR - Loss Function Recommendations")
    print("=" * 100)
    
    for name, y in scenarios:
        print(f"\n{name}")
        print("-" * 100)
        
        dist = advisor.analyze_class_distribution(y)
        loss_rec = advisor.recommend_loss_function(dist)
        metrics_rec = advisor.recommend_metrics(dist)
        
        print(f"  Class Distribution: {dist.imbalance_ratio:.1f}:1 ({dist.severity.value})")
        print(f"  Recommended Loss: {loss_rec.loss_type} (confidence: {loss_rec.confidence:.0%})")
        print(f"  Reason: {loss_rec.reason}")
        print(f"  Primary Metrics: {', '.join(metrics_rec.primary_metrics)}")
        print(f"  Avoid: {', '.join(metrics_rec.avoid_metrics) if metrics_rec.avoid_metrics else 'None'}")

