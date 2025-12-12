#!/usr/bin/env python3
"""
Complete example: Using Model Advisor to automatically configure and evaluate a model.

This demonstrates the full workflow:
1. Analyze class distribution
2. Get recommendations for loss function and metrics
3. Configure training parameters
4. Assess model health after training
5. Generate comprehensive report
"""

import sys
import json
from pathlib import Path
import numpy as np

# Add paths
qa_dir = Path(__file__).parent
sys.path.insert(0, str(qa_dir.parent.parent.parent.parent))
sys.path.insert(0, str(qa_dir.parent.parent.parent))

from model_advisor import ModelAdvisor
from featrix.neural.input_data_file import FeatrixInputDataFile

print("=" * 100)
print("COMPLETE MODEL EVALUATION WORKFLOW")
print("=" * 100)
print()

# Initialize advisor
advisor = ModelAdvisor()

# Load data
data_file = qa_dir.parent.parent.parent.parent.parent / "qa_data" / "credit_g_31.csv"
if not data_file.exists():
    print(f"❌ Data file not found: {data_file}")
    print("Please ensure credit_g_31.csv is in the qa_data directory")
    sys.exit(1)

input_file = FeatrixInputDataFile(str(data_file))
df = input_file.df

print(f"📊 Dataset: {data_file.name}")
print(f"   Samples: {len(df)}")
print(f"   Features: {len(df.columns)}")
print()

# Extract target column
target_col = "target"  # Adjust if needed
y = df[target_col].values
n_features = len(df.columns) - 1

print("=" * 100)
print("STEP 1: ANALYZE CLASS DISTRIBUTION")
print("=" * 100)
print()

distribution = advisor.analyze_class_distribution(y)

print(f"Total Samples: {distribution.total}")
print(f"Classes: {distribution.classes}")
print(f"Majority Class: {distribution.majority_class} ({distribution.majority_ratio:.1%})")
print(f"Minority Class: {distribution.minority_class} ({distribution.minority_ratio:.1%})")
print(f"Imbalance Ratio: {distribution.imbalance_ratio:.1f}:1")
print(f"Severity: {distribution.severity.value.upper()}")
print()

print("=" * 100)
print("STEP 2: GET LOSS FUNCTION RECOMMENDATION")
print("=" * 100)
print()

loss_rec = advisor.recommend_loss_function(distribution, task_priority="balanced")

print(f"✅ Recommended Loss: {loss_rec.loss_type}")
print(f"   Confidence: {loss_rec.confidence:.0%}")
print(f"   Reason: {loss_rec.reason}")
if loss_rec.parameters:
    print(f"   Suggested Parameters: {loss_rec.parameters}")
print()

if loss_rec.alternatives:
    print("Alternative Options:")
    for alt_loss, alt_reason in loss_rec.alternatives:
        print(f"  • {alt_loss}: {alt_reason}")
print()

print("=" * 100)
print("STEP 3: GET METRICS RECOMMENDATION")
print("=" * 100)
print()

metrics_rec = advisor.recommend_metrics(distribution)

print("📊 Primary Metrics (report these):")
for metric in metrics_rec.primary_metrics:
    reason = metrics_rec.rationale.get(metric, "")
    print(f"  ✓ {metric:20s} - {reason}")
print()

print("📈 Secondary Metrics (additional insight):")
for metric in metrics_rec.secondary_metrics:
    reason = metrics_rec.rationale.get(metric, "")
    print(f"  • {metric:20s} - {reason}")
print()

if metrics_rec.avoid_metrics:
    print("⚠️  Metrics to AVOID (misleading for this data):")
    for metric in metrics_rec.avoid_metrics:
        reason = metrics_rec.rationale.get(metric, "")
        print(f"  ✗ {metric:20s} - {reason}")
print()

print("=" * 100)
print("STEP 4: GET TRAINING CONFIGURATION")
print("=" * 100)
print()

config = advisor.generate_training_config(distribution, len(df), n_features)

print("🎯 Recommended Training Configuration:")
for key, value in config.items():
    print(f"  {key:30s} = {value}")
print()

print("=" * 100)
print("STEP 5: EXAMPLE MODEL HEALTH ASSESSMENT")
print("=" * 100)
print()

# Simulate some training history (replace with actual training results)
print("Simulating training history...")
print("(In real usage, this would come from actual model training)")
print()

# Simulate improving then overfitting scenario
train_losses = [1.0, 0.8, 0.65, 0.55, 0.48, 0.42, 0.38, 0.35, 0.32, 0.30]
val_losses = [0.95, 0.78, 0.68, 0.62, 0.60, 0.61, 0.63, 0.65, 0.67, 0.70]

train_metrics = {
    "accuracy": [0.5, 0.6, 0.65, 0.7, 0.75, 0.78, 0.82, 0.85, 0.87, 0.89],
    "f1": [0.4, 0.55, 0.6, 0.65, 0.7, 0.73, 0.76, 0.78, 0.8, 0.82]
}

val_metrics = {
    "accuracy": [0.52, 0.58, 0.63, 0.68, 0.70, 0.69, 0.68, 0.67, 0.66, 0.65],
    "f1": [0.42, 0.53, 0.58, 0.63, 0.67, 0.66, 0.65, 0.64, 0.63, 0.62]
}

best_epoch = 4

health_report = advisor.assess_model_health(
    train_losses=train_losses,
    val_losses=val_losses,
    train_metrics=train_metrics,
    val_metrics=val_metrics,
    best_epoch=best_epoch
)

print(f"Overall Health: {'✅ HEALTHY' if health_report.is_healthy else '⚠️  NEEDS ATTENTION'}")
print()

print(f"Health Scores:")
print(f"  Stability:       {health_report.stability_score:.2f} / 1.00")
print(f"  Learning:        {health_report.learning_score:.2f} / 1.00")
print(f"  Generalization:  {health_report.generalization_score:.2f} / 1.00")
print()

if health_report.issues:
    print("🚨 ISSUES DETECTED:")
    for issue in health_report.issues:
        print(f"  ✗ {issue}")
    print()

if health_report.warnings:
    print("⚠️  WARNINGS:")
    for warning in health_report.warnings:
        print(f"  • {warning}")
    print()

if health_report.recommendations:
    print("💡 RECOMMENDATIONS:")
    for rec in health_report.recommendations:
        print(f"  → {rec}")
print()

print("=" * 100)
print("STEP 6: GENERATE COMPREHENSIVE REPORT")
print("=" * 100)
print()

print("To generate a full HTML report with visualizations:")
print()
print("1. Run your test with the recommended configuration:")
print(f"   python3 test_focal_comparison.py")
print()
print("2. Generate the report:")
print(f"   python3 generate_focal_report.py")
print()
print("3. Or use the shortcut:")
print(f"   ./report")
print()

print("=" * 100)
print("SUMMARY")
print("=" * 100)
print()

print(f"Dataset: {distribution.total} samples, {distribution.imbalance_ratio:.1f}:1 imbalance ({distribution.severity.value})")
print(f"Loss: Use {loss_rec.loss_type} ({loss_rec.confidence:.0%} confidence)")
print(f"Primary Metrics: {', '.join(metrics_rec.primary_metrics)}")
print(f"Batch Size: {config['batch_size']}, Epochs: {config['epochs']}, LR: {config['learning_rate']}")
print()

print("✅ System will automatically:")
print("  • Select appropriate loss function based on class distribution")
print("  • Report relevant metrics (avoiding misleading ones)")
print("  • Detect overfitting, underfitting, and instability")
print("  • Provide actionable recommendations")
print()

print("Next Steps:")
print("  1. Use recommended configuration for training")
print("  2. Monitor primary metrics during training")
print("  3. Check model health after training")
print("  4. Generate HTML report for stakeholders")
print()

