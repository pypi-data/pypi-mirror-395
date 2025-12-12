#!/usr/bin/env python3
"""
Comprehensive focal loss comparison test.
Tests focal vs cross-entropy on:
- Natural distribution (70/30)
- 90/10 (extreme imbalance)
- 50/50 (balanced)

Expected "best known" metrics for this dataset:
- Accuracy: 0.82
- F1: 0.81
- Precision: 0.84
- Recall: 0.82
- AUC: 0.88
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


def convert_to_json_serializable(obj):
    """Convert numpy types to native Python types for JSON serialization"""
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    return obj


set_device_cpu()

print("=" * 80)
print("🤖 INTELLIGENT MODEL EVALUATION TEST")
print("=" * 80)
print(f"Started: {datetime.now()}")
print()
print("✨ Using Model Advisor to automatically configure tests")
print()

# Load data
data_file = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "qa_data" / "credit_g_31.csv"
input_file = FeatrixInputDataFile(str(data_file))
df = input_file.df

print()
print("=" * 80)
print("DATASET INFORMATION")
print("=" * 80)
print(f"Total rows: {len(df)}")
print(f"\nNatural class distribution (full dataset):")
target_counts = df["target"].value_counts()
total = len(df)
for label in sorted(target_counts.index):
    count = target_counts[label]
    pct = count / total * 100
    print(f"  {label:6s}: {count:4d} samples ({pct:5.1f}%)")

# Calculate ratio
if len(target_counts) == 2:
    labels = sorted(target_counts.index)
    majority = target_counts[labels[0]] if target_counts[labels[0]] > target_counts[labels[1]] else target_counts[labels[1]]
    minority = target_counts[labels[0]] if target_counts[labels[0]] < target_counts[labels[1]] else target_counts[labels[1]]
    ratio = majority / minority
    print(f"\nClass balance ratio: {ratio:.2f}:1 ({majority}:{minority})")
print("=" * 80)
print()

# Create datasets
def create_dataset(df, pos_count, neg_count):
    """Sample specific counts WITHOUT replacement"""
    pos = df[df["target"] == "good"].sample(n=pos_count, random_state=42, replace=False)
    neg = df[df["target"] == "bad"].sample(n=neg_count, random_state=42, replace=False)
    return pd.concat([pos, neg]).sample(frac=1, random_state=42).reset_index(drop=True)

# Configurations: (pos, neg, name) - subsample both sides
# Use None for pos_count/neg_count to indicate "use full dataset"
# Expanded test covering fine gradient from balanced to extreme imbalance
configs = [
    (None, None, "Natural (70/30)"),  # Full dataset with natural distribution
    (300, 300, "50/50"),
    (165, 135, "55/45"),
    (180, 120, "60/40"),
    (195, 105, "65/35"),
    (210, 90, "70/30"),
    (225, 75, "75/25"),
    (240, 60, "80/20"),
    (255, 45, "85/15"),
    (270, 30, "90/10"),
    (285, 15, "95/5"),
    # Reverse imbalance (minority becomes majority)
    (75, 225, "25/75"),
    (60, 240, "20/80"),
    (45, 255, "15/85"),
    (30, 270, "10/90"),
    (15, 285, "5/95"),
]

loss_types = ["focal", "cross_entropy"]
results = []

# Initialize model advisor
advisor = ModelAdvisor()

# Train ES once
print("Training ES (50 epochs)...")
dataset = FeatrixInputDataSet(df=df, ignore_cols=[], limit_rows=None, encoder_overrides=None)

# Extract detected column types and set them as encoder overrides
# This ensures train and val splits use the SAME types as detected on the full dataset
detected_types = {}
for col_name, detector in dataset._detectors.items():
    detected_types[col_name] = detector.get_codec_name()

print(f"\n📋 Detected column types from full dataset (will be used for train/val splits):")
for col, codec in sorted(detected_types.items()):
    print(f"   {col}: {codec}")
print()

# SET the encoderOverrides on the dataset so split() will pass them along
dataset.encoderOverrides = detected_types

# Now split - the detected types will be passed to train_data and val_data
train_data, val_data = dataset.split(fraction=0.2)

es = EmbeddingSpace(train_data, val_data, n_epochs=50, d_model=128, output_debug_label="focal_comp")
es.train(batch_size=128, n_epochs=50)
print("ES complete\n")

test_num = 0
total_tests = len(configs) * len(loss_types)

for pos_count, neg_count, ratio_name in configs:
    print("=" * 80)
    
    # Handle untouched baseline vs resampled
    if pos_count is None and neg_count is None:
        # Use full dataset
        balanced_df = df.copy()
        actual_counts = balanced_df["target"].value_counts()
        pos_actual = actual_counts.get("good", 0)
        neg_actual = actual_counts.get("bad", 0)
        print(f"RATIO: {ratio_name} ({pos_actual} pos / {neg_actual} neg)")
    else:
        # Resampled data
        balanced_df = create_dataset(df, pos_count, neg_count)
        print(f"RATIO: {ratio_name} ({pos_count} pos / {neg_count} neg)")
    
    print("=" * 80)
    
    # 🤖 AUTOMATIC CONFIGURATION
    # Analyze this specific ratio and get recommendations
    y_for_ratio = balanced_df["target"].values
    distribution = advisor.analyze_class_distribution(y_for_ratio)
    loss_rec = advisor.recommend_loss_function(distribution)
    metrics_rec = advisor.recommend_metrics(distribution)
    
    print(f"\n🤖 Model Advisor Analysis:")
    print(f"   Class Balance: {distribution.imbalance_ratio:.1f}:1 ({distribution.severity.value})")
    print(f"   Recommended Loss: {loss_rec.loss_type} (confidence: {loss_rec.confidence:.0%})")
    print(f"   Reason: {loss_rec.reason}")
    print(f"   Primary Metrics: {', '.join(metrics_rec.primary_metrics)}")
    if metrics_rec.avoid_metrics:
        print(f"   ⚠️  Avoid: {', '.join(metrics_rec.avoid_metrics)} (misleading for this ratio)")
    print()
    
    for loss_type in loss_types:
        test_num += 1
        
        # Create run identifier for logging
        run_id = f"[{ratio_name.replace('/', '_').replace(' ', '_')}/{loss_type}]"
        
        print(f"  [{test_num}/{total_tests}] {run_id} {loss_type} (50 epochs)...", end=" ", flush=True)
        
        try:
            config = SimpleMLPConfig(d_in=128, d_out=2, d_hidden=256, n_hidden_layers=2, dropout=0.1, normalize=False, residual=True, use_batch_norm=True)
            predictor = SimpleMLP(config)
            fsp = FeatrixSinglePredictor(es, predictor)
            
            # Set run identifier on the FSP for logging
            fsp.run_identifier = run_id
            
            fsp.prep_for_training(train_df=balanced_df, target_col_name="target", target_col_type="set", use_class_weights=False, loss_type=loss_type)
            
            # Callback to print progress
            def print_progress(progress):
                epoch = progress.get("epoch", 0)
                total_epochs = progress.get("total_epochs", 50)
                train_loss = progress.get("training_loss", 0)
                val_loss = progress.get("validation_loss", 0)
                metrics = progress.get("metrics", {})
                f1 = metrics.get("f1", 0) if metrics else 0
                if epoch % 10 == 0:
                    print(f"\n    Epoch {epoch}/{total_epochs}: train_loss={train_loss:.3f}, val_loss={val_loss:.3f}, F1={f1:.3f}", end="", flush=True)
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Create unique identifier for this test's network viz files and logging
            viz_identifier = f"{ratio_name.replace('/', '_').replace(' ', '_')}_{loss_type}"
            sp_id = f"target_{ratio_name.replace('/', '_')}_{loss_type}"
            
            training_results = loop.run_until_complete(fsp.train(
                n_epochs=50, 
                batch_size=128, 
                fine_tune=True, 
                val_pos_label="good",
                print_callback=print_progress,
                print_progress_step=10,
                network_viz_identifier=viz_identifier,
                sp_identifier=sp_id
            ))
            loop.close()
            
            if training_results and len(training_results) > 0:
                final = training_results[-1]
                metrics = final.get("metrics", {})
                
                # Extract loss history for curves
                loss_history = {
                    "epochs": [r.get("epoch", i) for i, r in enumerate(training_results)],
                    "train_loss": [r.get("training_loss") for r in training_results],
                    "val_loss": [r.get("validation_loss") for r in training_results],
                }
                
                # Get actual counts from the balanced_df
                actual_counts = balanced_df["target"].value_counts()
                pos_actual = actual_counts.get("good", 0)
                neg_actual = actual_counts.get("bad", 0)
                
                result_entry = {
                    "ratio": ratio_name,
                    "pos_count": pos_actual,  # Use actual counts, not config
                    "neg_count": neg_actual,  # Use actual counts, not config
                    "loss_type": loss_type,
                    "epochs": 50,
                    "training_loss": final.get("training_loss"),
                    "validation_loss": final.get("validation_loss"),
                    "accuracy": metrics.get("accuracy"),
                    "f1": metrics.get("f1"),
                    "precision": metrics.get("precision"),
                    "recall": metrics.get("recall"),
                    "auc": metrics.get("auc"),
                    "loss_history": loss_history,
                }
                
                results.append(result_entry)
                print(f"Loss={result_entry['validation_loss']:.3f}, F1={result_entry['f1']:.3f}")
            else:
                print("NO RESULTS")
                
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print()

# Save (convert numpy types to JSON-serializable types)
output_file = test_dir / "focal_comparison_results.json"
output_data = {
    "timestamp": datetime.now().isoformat(), 
    "results": convert_to_json_serializable(results)
}
with open(output_file, "w") as f:
    json.dump(output_data, f, indent=2)

print("=" * 80)
print("RESULTS")
print("=" * 80)
print()
print(f"Ratio              | Samples    | Loss Type     | Val Loss | F1    | Acc   | Prec  | Rec   | AUC")
print("-" * 110)
for r in results:
    pos = r['pos_count']
    neg = r['neg_count']
    total = pos + neg
    pos_pct = (pos / total * 100) if total > 0 else 0
    samples_info = f"{pos}/{neg} ({pos_pct:.0f}%/{100-pos_pct:.0f}%)"
    print(f"{r['ratio']:18} | {samples_info:10} | {r['loss_type']:13} | {r['validation_loss']:8.3f} | {r['f1']:.3f} | {r['accuracy']:.3f} | {r['precision']:.3f} | {r['recall']:.3f} | {r['auc']:.3f}")

print()
print("=" * 80)
print("ANALYSIS BY IMBALANCE SEVERITY")
print("=" * 80)

# Group results by severity and compare loss functions
severity_groups = {
    'Balanced (45-55%)': [],
    'Slight (55-70%)': [],
    'Moderate (70-80%)': [],
    'Severe (80-90%)': [],
    'Extreme (90%+)': []
}

for r in results:
    pos = r['pos_count']
    neg = r['neg_count']
    total = pos + neg
    majority_pct = max(pos, neg) / total * 100
    
    if majority_pct <= 55:
        severity_groups['Balanced (45-55%)'].append(r)
    elif majority_pct <= 70:
        severity_groups['Slight (55-70%)'].append(r)
    elif majority_pct <= 80:
        severity_groups['Moderate (70-80%)'].append(r)
    elif majority_pct <= 90:
        severity_groups['Severe (80-90%)'].append(r)
    else:
        severity_groups['Extreme (90%+)'].append(r)

for severity, group in severity_groups.items():
    if not group:
        continue
    
    print(f"\n{severity}:")
    print(f"  {'Ratio':<18} | {'Loss Type':<13} | {'Val Loss':<8} | {'F1':<6} | {'AUC':<6}")
    print(f"  {'-'*70}")
    
    for r in group:
        print(f"  {r['ratio']:<18} | {r['loss_type']:<13} | {r['validation_loss']:<8.3f} | {r['f1']:<6.3f} | {r['auc']:<6.3f}")
    
    # Find winners
    focal_results = [r for r in group if r['loss_type'] == 'focal']
    ce_results = [r for r in group if r['loss_type'] == 'cross_entropy']
    
    if focal_results and ce_results:
        focal_avg_loss = sum(r['validation_loss'] for r in focal_results) / len(focal_results)
        ce_avg_loss = sum(r['validation_loss'] for r in ce_results) / len(ce_results)
        focal_avg_f1 = sum(r['f1'] for r in focal_results) / len(focal_results)
        ce_avg_f1 = sum(r['f1'] for r in ce_results) / len(ce_results)
        focal_avg_auc = sum(r['auc'] for r in focal_results) / len(focal_results)
        ce_avg_auc = sum(r['auc'] for r in ce_results) / len(ce_results)
        
        print(f"\n  📊 Average Performance:")
        print(f"     Focal:          Loss={focal_avg_loss:.3f}, F1={focal_avg_f1:.3f}, AUC={focal_avg_auc:.3f}")
        print(f"     Cross-Entropy:  Loss={ce_avg_loss:.3f}, F1={ce_avg_f1:.3f}, AUC={ce_avg_auc:.3f}")
        
        # Declare winner
        if focal_avg_loss < ce_avg_loss and focal_avg_f1 > ce_avg_f1:
            print(f"     🏆 Winner: FOCAL (better on both loss and F1)")
        elif ce_avg_loss < focal_avg_loss and ce_avg_f1 > focal_avg_f1:
            print(f"     🏆 Winner: CROSS-ENTROPY (better on both loss and F1)")
        elif focal_avg_loss < ce_avg_loss:
            print(f"     🏆 Winner: FOCAL (lower loss, F1 similar)")
        elif focal_avg_f1 > ce_avg_f1:
            print(f"     🏆 Winner: FOCAL (higher F1, loss similar)")
        else:
            print(f"     🤝 Tie: Both perform similarly")
        
        # Flag failures
        if focal_avg_auc < 0.6 or ce_avg_auc < 0.6:
            print(f"     ⚠️  WARNING: Low AUC detected - models may be failing at this imbalance level")

print()
print(f"Saved: {output_file}")
print(f"Done: {datetime.now()}")
