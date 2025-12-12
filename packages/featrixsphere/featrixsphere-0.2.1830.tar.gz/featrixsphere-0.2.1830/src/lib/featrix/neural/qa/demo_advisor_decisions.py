#!/usr/bin/env python3
"""
Quick Demo: Show what the Model Advisor recommends for different scenarios.

This is a fast preview (no training) that shows how the advisor makes decisions.
"""
import sys
from pathlib import Path
import numpy as np

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from model_advisor import ModelAdvisor
import pandas as pd

print("=" * 100)
print("🤖 MODEL ADVISOR - DECISION PREVIEW")
print("=" * 100)
print()
print("This shows what the advisor recommends for different class imbalance scenarios.")
print("(No training - just recommendations)")
print()

# Simulate credit data for quick demo
print("Creating simulated credit dataset (1000 samples, 70/30 distribution)...")
np.random.seed(42)
df = pd.DataFrame({
    'target': (['good'] * 700) + (['bad'] * 300)
})
print()

advisor = ModelAdvisor()

# Define scenarios
def create_scenario(df, pos_count, neg_count):
    """Create a scenario dataset"""
    if pos_count is None:
        return df.copy()
    return pd.DataFrame({
        'target': (['good'] * pos_count) + (['bad'] * neg_count)
    })

scenarios = [
    (None, None, "Natural Distribution"),
    (300, 300, "Balanced (50/50)"),
    (225, 75, "Mild Imbalance (75/25)"),
    (270, 30, "Severe Imbalance (90/10)"),
    (285, 15, "Extreme Imbalance (95/5)"),
]

print("=" * 100)
print("ADVISOR RECOMMENDATIONS FOR EACH SCENARIO")
print("=" * 100)
print()

for pos_count, neg_count, scenario_name in scenarios:
    # Create dataset
    if pos_count is None:
        test_df = df.copy()
    else:
        test_df = create_scenario(df, pos_count, neg_count)
    
    y = test_df["target"].values
    
    # Analyze
    distribution = advisor.analyze_class_distribution(y)
    loss_rec = advisor.recommend_loss_function(distribution)
    metrics_rec = advisor.recommend_metrics(distribution)
    config = advisor.generate_training_config(distribution, len(test_df), 20)  # Assuming 20 features
    
    print(f"{'─' * 100}")
    print(f"📊 {scenario_name}")
    print(f"{'─' * 100}")
    print()
    
    print(f"  Dataset:")
    print(f"    Samples: {distribution.total}")
    print(f"    Majority: {distribution.majority_class} ({distribution.majority_ratio:.1%})")
    print(f"    Minority: {distribution.minority_class} ({distribution.minority_ratio:.1%})")
    print(f"    Ratio: {distribution.imbalance_ratio:.2f}:1")
    print(f"    Severity: {distribution.severity.value.upper()}")
    print()
    
    print(f"  💡 Loss Function:")
    print(f"    Use: {loss_rec.loss_type}")
    print(f"    Confidence: {loss_rec.confidence:.0%}")
    print(f"    Reason: {loss_rec.reason}")
    if loss_rec.parameters:
        print(f"    Parameters: {loss_rec.parameters}")
    if loss_rec.alternatives:
        print(f"    Alternatives:")
        for alt, reason in loss_rec.alternatives[:2]:
            print(f"      • {alt}: {reason}")
    print()
    
    print(f"  📊 Metrics:")
    print(f"    PRIMARY (report these): {', '.join(metrics_rec.primary_metrics)}")
    print(f"    Secondary: {', '.join(metrics_rec.secondary_metrics[:3])}...")
    if metrics_rec.avoid_metrics:
        print(f"    ⚠️  AVOID (misleading): {', '.join(metrics_rec.avoid_metrics)}")
    print()
    
    print(f"  ⚙️  Training Config:")
    print(f"    Batch Size: {config['batch_size']}")
    print(f"    Learning Rate: {config['learning_rate']}")
    print(f"    Epochs: {config['epochs']}")
    print(f"    Dropout: {config['dropout']}")
    print(f"    Weight Decay: {config['weight_decay']}")
    print()

print("=" * 100)
print("DECISION SUMMARY TABLE")
print("=" * 100)
print()
print(f"{'Scenario':<30} | {'Ratio':<8} | {'Severity':<10} | {'Loss':<20} | {'Key Metric':<15} | {'Avoid':<20}")
print("─" * 120)

for pos_count, neg_count, scenario_name in scenarios:
    if pos_count is None:
        test_df = df.copy()
    else:
        test_df = create_scenario(df, pos_count, neg_count)
    
    y = test_df["target"].values
    distribution = advisor.analyze_class_distribution(y)
    loss_rec = advisor.recommend_loss_function(distribution)
    metrics_rec = advisor.recommend_metrics(distribution)
    
    ratio = f"{distribution.imbalance_ratio:.1f}:1"
    severity = distribution.severity.value
    loss = loss_rec.loss_type
    key_metric = metrics_rec.primary_metrics[0]
    avoid = metrics_rec.avoid_metrics[0] if metrics_rec.avoid_metrics else "none"
    
    print(f"{scenario_name:<30} | {ratio:<8} | {severity:<10} | {loss:<20} | {key_metric:<15} | {avoid:<20}")

print()
print("=" * 100)
print("KEY INSIGHTS")
print("=" * 100)
print()
print("✅ Balanced data (50/50):")
print("   → Use standard cross-entropy")
print("   → Report accuracy, F1, AUC")
print()
print("⚠️  Mild imbalance (70/30):")
print("   → Use cross-entropy with class weights")
print("   → Report F1, AUC, balanced_accuracy")
print("   → AVOID accuracy (can be misleading)")
print()
print("🚨 Severe imbalance (90/10):")
print("   → Use focal loss")
print("   → Report MCC, PR-AUC, F1")
print("   → AVOID accuracy and ROC-AUC (very misleading)")
print()
print("💥 Extreme imbalance (95/5):")
print("   → Use class-balanced focal loss")
print("   → Report MCC, PR-AUC, recall, precision")
print("   → AVOID accuracy and ROC-AUC (completely misleading)")
print()
print("=" * 100)
print()
print("💡 To see these recommendations in action with real training:")
print("   python3 test_adaptive_training.py")
print()
print("   (This will train models using the recommended configuration for each scenario)")
print()

