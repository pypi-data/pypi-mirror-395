#!/usr/bin/env python3
"""
Intelligent Adaptive Training Test

Instead of testing focal vs cross-entropy everywhere, this script:
1. Analyzes each class ratio scenario
2. Uses the Model Advisor's recommendation automatically
3. Applies recommended training configuration
4. Reports only the recommended metrics
5. Assesses model health

This demonstrates the advisor working as an intelligent, automatic system.
"""
import sys
import os
import json
import asyncio
from pathlib import Path
from datetime import datetime

# Paths
test_dir = Path(__file__).parent
neural_dir = test_dir.parent
featrix_dir = neural_dir.parent
lib_dir = featrix_dir.parent
src_dir = lib_dir.parent

sys.path.insert(0, str(lib_dir))
sys.path.insert(0, str(src_dir))

from featrix.neural.input_data_file import FeatrixInputDataFile
from featrix.neural.embedded_space import EmbeddingSpace
from featrix.neural.input_data_set import FeatrixInputDataSet
from featrix.neural.single_predictor import FeatrixSinglePredictor
from featrix.neural.simple_mlp import SimpleMLP
from featrix.neural.model_config import SimpleMLPConfig
from featrix.neural.device import set_device_cpu
import pandas as pd
import numpy as np

# Import the intelligent advisor
from model_advisor import ModelAdvisor

set_device_cpu()

print("=" * 100)
print("🤖 INTELLIGENT ADAPTIVE TRAINING TEST")
print("=" * 100)
print(f"Started: {datetime.now()}")
print()
print("This test demonstrates the Model Advisor working automatically:")
print("  ✓ Analyzes class distribution")
print("  ✓ Recommends optimal loss function")
print("  ✓ Selects appropriate metrics")
print("  ✓ Configures training parameters")
print("  ✓ Assesses model health")
print()

# Load data
data_file = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "qa_data" / "credit_g_31.csv"
input_file = FeatrixInputDataFile(str(data_file))
df = input_file.df

print("=" * 100)
print("DATASET INFORMATION")
print("=" * 100)
print(f"Total rows: {len(df)}")
print(f"\nNatural class distribution:")
target_counts = df["target"].value_counts()
total = len(df)
for label in sorted(target_counts.index):
    count = target_counts[label]
    pct = count / total * 100
    print(f"  {label:6s}: {count:4d} samples ({pct:5.1f}%)")

if len(target_counts) == 2:
    labels = sorted(target_counts.index)
    majority = max(target_counts[labels[0]], target_counts[labels[1]])
    minority = min(target_counts[labels[0]], target_counts[labels[1]])
    ratio = majority / minority
    print(f"\nClass balance ratio: {ratio:.2f}:1")
print("=" * 100)
print()

# Create datasets function
def create_dataset(df, pos_count, neg_count):
    """Sample specific counts WITHOUT replacement"""
    pos = df[df["target"] == "good"].sample(n=pos_count, random_state=42, replace=False)
    neg = df[df["target"] == "bad"].sample(n=neg_count, random_state=42, replace=False)
    return pd.concat([pos, neg]).sample(frac=1, random_state=42).reset_index(drop=True)

# Initialize advisor
advisor = ModelAdvisor()

# Scenarios to test
scenarios = [
    (None, None, "Natural Distribution (70/30)"),
    (300, 300, "Balanced (50/50)"),
    (225, 75, "Mild Imbalance (75/25)"),
    (270, 30, "Severe Imbalance (90/10)"),
    (285, 15, "Extreme Imbalance (95/5)"),
]

results = []

# Train ES once
print("Training Embedding Space (100 epochs)...")
dataset = FeatrixInputDataSet(df=df, ignore_cols=[], limit_rows=None, encoder_overrides=None)
train_data, val_data = dataset.split(fraction=0.2)
es = EmbeddingSpace(train_data, val_data, n_epochs=100, d_model=128, output_debug_label="adaptive_test")
es.train(batch_size=128, n_epochs=100)
print("✓ Embedding Space trained\n")

test_num = 0
total_tests = len(scenarios)

for pos_count, neg_count, scenario_name in scenarios:
    test_num += 1
    
    print("=" * 100)
    print(f"SCENARIO {test_num}/{total_tests}: {scenario_name}")
    print("=" * 100)
    
    # Prepare dataset
    if pos_count is None and neg_count is None:
        test_df = df.copy()
        actual_counts = test_df["target"].value_counts()
        pos_actual = actual_counts.get("good", 0)
        neg_actual = actual_counts.get("bad", 0)
    else:
        test_df = create_dataset(df, pos_count, neg_count)
        pos_actual = pos_count
        neg_actual = neg_count
    
    print(f"Dataset: {pos_actual} positive / {neg_actual} negative")
    print()
    
    # 🤖 STEP 1: Analyze Distribution
    y_for_scenario = test_df["target"].values
    distribution = advisor.analyze_class_distribution(y_for_scenario)
    
    print("🔍 STEP 1: Class Distribution Analysis")
    print(f"   Imbalance Ratio: {distribution.imbalance_ratio:.2f}:1")
    print(f"   Severity: {distribution.severity.value.upper()}")
    print(f"   Majority Class: {distribution.majority_class} ({distribution.majority_ratio:.1%})")
    print(f"   Minority Class: {distribution.minority_class} ({distribution.minority_ratio:.1%})")
    print()
    
    # 🤖 STEP 2: Get Loss Recommendation
    loss_rec = advisor.recommend_loss_function(distribution, task_priority="balanced")
    
    print("💡 STEP 2: Loss Function Recommendation")
    print(f"   Recommended: {loss_rec.loss_type}")
    print(f"   Confidence: {loss_rec.confidence:.0%}")
    print(f"   Reason: {loss_rec.reason}")
    if loss_rec.parameters:
        print(f"   Parameters: {loss_rec.parameters}")
    if loss_rec.alternatives:
        print(f"   Alternatives considered:")
        for alt_loss, reason in loss_rec.alternatives[:2]:  # Show top 2
            print(f"      • {alt_loss}: {reason}")
    print()
    
    # 🤖 STEP 3: Get Metrics Recommendation
    metrics_rec = advisor.recommend_metrics(distribution)
    
    print("📊 STEP 3: Metrics Selection")
    print(f"   Primary Metrics: {', '.join(metrics_rec.primary_metrics)}")
    print(f"   Secondary Metrics: {', '.join(metrics_rec.secondary_metrics[:3])}...")
    if metrics_rec.avoid_metrics:
        print(f"   ⚠️  Avoid (misleading): {', '.join(metrics_rec.avoid_metrics)}")
    print()
    
    # 🤖 STEP 4: Get Training Configuration
    config = advisor.generate_training_config(
        distribution, 
        n_samples=len(test_df),
        n_features=len(df.columns) - 1
    )
    
    print("⚙️  STEP 4: Training Configuration")
    print(f"   Batch Size: {config['batch_size']}")
    print(f"   Learning Rate: {config['learning_rate']}")
    print(f"   Epochs: {config['epochs']}")
    print(f"   Dropout: {config['dropout']}")
    print(f"   Weight Decay: {config['weight_decay']}")
    print(f"   Early Stop Patience: {config['early_stopping_patience']}")
    print()
    
    # 🚀 STEP 5: Train with Recommended Configuration
    print(f"🚀 STEP 5: Training with {loss_rec.loss_type}...")
    
    try:
        mlp_config = SimpleMLPConfig(
            d_in=128, 
            d_out=2, 
            d_hidden=256, 
            n_hidden_layers=2, 
            dropout=config['dropout'],
            normalize=False, 
            residual=True, 
            use_batch_norm=True
        )
        predictor = SimpleMLP(mlp_config)
        fsp = FeatrixSinglePredictor(es, predictor)
        
        # Map loss recommendation to actual loss type
        # (In production, you'd map all loss types the advisor can recommend)
        actual_loss_type = loss_rec.loss_type
        if actual_loss_type == "class_balanced_focal":
            actual_loss_type = "focal"  # Fallback if not implemented
        elif actual_loss_type not in ["focal", "cross_entropy"]:
            print(f"   ⚠️  Loss '{actual_loss_type}' not implemented, using focal as fallback")
            actual_loss_type = "focal"
        
        fsp.prep_for_training(
            train_df=test_df, 
            target_col_name="target", 
            target_col_type="set", 
            use_class_weights=False, 
            loss_type=actual_loss_type
        )
        
        # Callback for progress
        training_history = {
            "epochs": [],
            "train_losses": [],
            "val_losses": [],
            "metrics": []
        }
        
        def collect_progress(progress):
            epoch = progress.get("epoch", 0)
            train_loss = progress.get("training_loss", 0)
            val_loss = progress.get("validation_loss", 0)
            metrics = progress.get("metrics", {})
            
            training_history["epochs"].append(epoch)
            training_history["train_losses"].append(train_loss)
            training_history["val_losses"].append(val_loss)
            training_history["metrics"].append(metrics)
            
            if epoch % 20 == 0:
                f1 = metrics.get("f1", 0) if metrics else 0
                print(f"   Epoch {epoch}/{config['epochs']}: train_loss={train_loss:.3f}, val_loss={val_loss:.3f}, F1={f1:.3f}")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        viz_id = f"{scenario_name.replace('/', '_').replace(' ', '_')}_{actual_loss_type}"
        
        training_results = loop.run_until_complete(fsp.train(
            n_epochs=config['epochs'],
            batch_size=config['batch_size'],
            fine_tune=False,
            val_pos_label="good",
            print_callback=collect_progress,
            print_progress_step=20,
            network_viz_identifier=viz_id
        ))
        loop.close()
        
        if training_results and len(training_results) > 0:
            final = training_results[-1]
            final_metrics = final.get("metrics", {})
            
            # Find best epoch
            val_losses = [r.get("validation_loss", float('inf')) for r in training_results]
            best_epoch = val_losses.index(min(val_losses))
            best_val_loss = val_losses[best_epoch]
            
            print(f"   ✓ Training complete!")
            print(f"   Best epoch: {best_epoch}")
            print(f"   Best validation loss: {best_val_loss:.4f}")
            print()
            
            # 🔍 STEP 6: Assess Model Health
            print("🏥 STEP 6: Model Health Assessment")
            
            health = advisor.assess_model_health(
                train_losses=training_history["train_losses"],
                val_losses=training_history["val_losses"],
                train_metrics={},
                val_metrics={},
                best_epoch=best_epoch
            )
            
            print(f"   Overall Health: {'✅ HEALTHY' if health.is_healthy else '⚠️  NEEDS ATTENTION'}")
            print(f"   Stability Score: {health.stability_score:.2f}")
            print(f"   Learning Score: {health.learning_score:.2f}")
            print(f"   Generalization Score: {health.generalization_score:.2f}")
            
            if health.issues:
                print(f"   🚨 Issues:")
                for issue in health.issues:
                    print(f"      • {issue}")
            
            if health.warnings:
                print(f"   ⚠️  Warnings:")
                for warning in health.warnings:
                    print(f"      • {warning}")
            
            if health.recommendations:
                print(f"   💡 Recommendations:")
                for rec in health.recommendations[:2]:  # Top 2
                    print(f"      • {rec}")
            print()
            
            # 📊 STEP 7: Report Primary Metrics Only
            print("📊 STEP 7: Final Metrics (Primary Only)")
            
            all_metrics = {
                "accuracy": final_metrics.get("accuracy", 0),
                "f1": final_metrics.get("f1", 0),
                "precision": final_metrics.get("precision", 0),
                "recall": final_metrics.get("recall", 0),
                "auc": final_metrics.get("auc", 0),
                "balanced_accuracy": final_metrics.get("balanced_accuracy", 0),
                "mcc": final_metrics.get("mcc", 0),
            }
            
            # Report only primary metrics
            for metric in metrics_rec.primary_metrics:
                value = all_metrics.get(metric, 0)
                # Check if this metric is in avoid list
                if metric in metrics_rec.avoid_metrics:
                    print(f"   {metric:20s}: {value:.4f} ⚠️  (not reliable for this ratio)")
                else:
                    print(f"   {metric:20s}: {value:.4f}")
            
            print()
            print(f"   Note: Avoiding {', '.join(metrics_rec.avoid_metrics)} as they're misleading for this imbalance level")
            print()
            
            # Store result
            result_entry = {
                "scenario": scenario_name,
                "pos_count": pos_actual,
                "neg_count": neg_actual,
                "imbalance_ratio": distribution.imbalance_ratio,
                "severity": distribution.severity.value,
                
                # Advisor decisions
                "recommended_loss": loss_rec.loss_type,
                "used_loss": actual_loss_type,
                "confidence": loss_rec.confidence,
                "recommended_metrics": metrics_rec.primary_metrics,
                "avoid_metrics": metrics_rec.avoid_metrics,
                
                # Training config used
                "batch_size": config['batch_size'],
                "learning_rate": config['learning_rate'],
                "epochs": config['epochs'],
                
                # Results
                "best_epoch": best_epoch,
                "validation_loss": best_val_loss,
                "final_metrics": all_metrics,
                
                # Health
                "is_healthy": health.is_healthy,
                "stability_score": health.stability_score,
                "learning_score": health.learning_score,
                "generalization_score": health.generalization_score,
                "health_issues": health.issues,
                "health_warnings": health.warnings,
                "health_recommendations": health.recommendations,
                
                # Loss history
                "loss_history": {
                    "epochs": training_history["epochs"],
                    "train_loss": training_history["train_losses"],
                    "val_loss": training_history["val_losses"],
                }
            }
            
            results.append(result_entry)
            
            print("✅ Scenario complete!")
        else:
            print("❌ No training results")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print()

# Save results
output_file = test_dir / "adaptive_training_results.json"
with open(output_file, "w") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "description": "Intelligent adaptive training using Model Advisor recommendations",
        "results": results
    }, f, indent=2)

print("=" * 100)
print("SUMMARY - ADVISOR DECISIONS")
print("=" * 100)
print()
print(f"{'Scenario':<30} | {'Ratio':<10} | {'Severity':<10} | {'Loss Used':<20} | {'Confidence':<10}")
print("-" * 100)

for r in results:
    scenario = r['scenario'][:28]
    ratio = f"{r['imbalance_ratio']:.1f}:1"
    severity = r['severity']
    loss = r['used_loss']
    conf = f"{r['confidence']:.0%}"
    print(f"{scenario:<30} | {ratio:<10} | {severity:<10} | {loss:<20} | {conf:<10}")

print()
print("=" * 100)
print("KEY METRICS (Primary Only)")
print("=" * 100)
print()

for r in results:
    print(f"\n{r['scenario']}:")
    print(f"  Used: {r['used_loss']} (recommended: {r['recommended_loss']})")
    print(f"  Primary Metrics: {', '.join(r['recommended_metrics'])}")
    
    metrics_to_show = r['recommended_metrics']
    for metric in metrics_to_show:
        value = r['final_metrics'].get(metric, 0)
        avoided = "⚠️ " if metric in r['avoid_metrics'] else ""
        print(f"    {metric:20s}: {value:.4f} {avoided}")
    
    # Health summary
    health_emoji = "✅" if r['is_healthy'] else "⚠️"
    print(f"  Health: {health_emoji} (stability: {r['stability_score']:.2f}, learning: {r['learning_score']:.2f}, generalization: {r['generalization_score']:.2f})")

print()
print("=" * 100)
print(f"✅ Complete! Results saved to: {output_file}")
print("=" * 100)
print()
print("Next steps:")
print("  1. Generate HTML report: python3 generate_focal_report.py adaptive_training_results.json")
print("  2. Quick view: python3 show_results.py adaptive_training_results.json")
print()

