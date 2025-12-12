#!/usr/bin/env python3
"""
Label smoothing comparison test via dataset size variation.

Tests CrossEntropyLoss with automatic label smoothing at different dataset sizes:
- < 500 samples → label_smoothing = 0.1 (aggressive)
- 500-1000 samples → label_smoothing = 0.05 (moderate)
- > 1000 samples → label_smoothing = 0.0 (none)

We test each size tier at multiple imbalance levels to see:
1. Does label smoothing help small datasets?
2. Does it hurt large balanced datasets?
3. What's the sweet spot?
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
print("🎛️  LABEL SMOOTHING TEST VIA DATASET SIZE VARIATION")
print("=" * 80)
print(f"Started: {datetime.now()}")
print()
print("Testing automatic label smoothing thresholds:")
print("  • < 500 samples → smoothing=0.1 (aggressive)")
print("  • 500-1000 samples → smoothing=0.05 (moderate)")
print("  • > 1000 samples (balanced) → smoothing=0.0 (none)")
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
print(f"\nNatural class distribution:")
target_counts = df["target"].value_counts()
total = len(df)
for label in sorted(target_counts.index):
    count = target_counts[label]
    pct = count / total * 100
    print(f"  {label:6s}: {count:4d} samples ({pct:5.1f}%)")
print("=" * 80)
print()


def create_dataset(df, total_samples, good_ratio):
    """
    Create dataset with specific size and class ratio.
    
    Args:
        df: Source dataframe
        total_samples: Total number of samples to use
        good_ratio: Ratio of "good" class (e.g., 0.7 for 70/30)
    """
    good_count = int(total_samples * good_ratio)
    bad_count = total_samples - good_count
    
    # Sample without replacement
    good_samples = df[df["target"] == "good"].sample(n=good_count, random_state=42, replace=False)
    bad_samples = df[df["target"] == "bad"].sample(n=bad_count, random_state=42, replace=False)
    
    return pd.concat([good_samples, bad_samples]).sample(frac=1, random_state=42).reset_index(drop=True)


# Test configurations: (total_samples, good_ratio, description)
# We test at 3 dataset sizes × 3 imbalance levels = 9 configurations
configs = [
    # Small dataset (< 500 samples) → should trigger label_smoothing=0.1
    (300, 0.70, "300_samples_70/30_smooth_0.1"),
    (400, 0.70, "400_samples_70/30_smooth_0.1"),
    (300, 0.50, "300_samples_50/50_smooth_0.1"),
    
    # Medium dataset (500-1000 samples) → should trigger label_smoothing=0.05
    (600, 0.70, "600_samples_70/30_smooth_0.05"),
    (800, 0.70, "800_samples_70/30_smooth_0.05"),
    (600, 0.50, "600_samples_50/50_smooth_0.05"),
    
    # Large dataset (> 1000 samples, balanced) → should trigger label_smoothing=0.0
    # Note: Need to test balanced data to avoid imbalance-triggered smoothing
    (None, None, "Full_dataset_70/30_NO_SMOOTH"),  # ~1000 samples, but imbalanced
    (700, 0.50, "700_samples_50/50_smooth_0.0"),  # 700 balanced = no smoothing
    (600, 0.90, "600_samples_90/10_smooth_0.05"),  # Imbalanced → smoothing despite size
]

results = []

# Train ES once on full dataset
print("Training Embedding Space (50 epochs)...")
dataset = FeatrixInputDataSet(df=df, ignore_cols=[], limit_rows=None, encoder_overrides=None)

# Extract detected column types
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

# Train embedding space
es = EmbeddingSpace(
    train_input_data=train_data,
    val_input_data=val_data,
    d_model=128,
    n_epochs=50,
    output_dir=str(test_dir),  # Save timeline to QA directory
)

es.train(
    batch_size=64,
    n_epochs=50,
    print_progress_step=10,
)

print("\n✅ Embedding Space trained")
print()

# Now test each configuration
print("=" * 80)
print("TESTING LABEL SMOOTHING CONFIGURATIONS")
print("=" * 80)
print()

for total_samples, good_ratio, description in configs:
    print()
    print("=" * 80)
    print(f"Configuration: {description}")
    print("=" * 80)
    
    # Create dataset for this configuration
    if total_samples is None and good_ratio is None:
        # Use full natural dataset
        test_df = df
        good_count = len(df[df["target"] == "good"])
        bad_count = len(df[df["target"] == "bad"])
        actual_total = len(df)
        actual_good_ratio = good_count / actual_total
    else:
        test_df = create_dataset(df, total_samples, good_ratio)
        good_count = int(total_samples * good_ratio)
        bad_count = total_samples - good_count
        actual_total = total_samples
        actual_good_ratio = good_ratio
    
    print(f"Dataset size: {actual_total} samples")
    print(f"Class distribution: good={good_count} ({actual_good_ratio*100:.1f}%), bad={bad_count} ({(1-actual_good_ratio)*100:.1f}%)")
    
    # Create predictor
    mlp_config = SimpleMLPConfig(
        d_in=es.d_model,
        d_out=2,  # Binary classification
        d_hidden=256,
        n_hidden_layers=2,
        dropout=0.1
    )
    mlp = SimpleMLP(mlp_config)
    
    predictor = FeatrixSinglePredictor(
        embedding_space=es,
        predictor=mlp
    )
    
    # Prep for training with CrossEntropyLoss (label smoothing will be automatic)
    predictor.prep_for_training(
        train_df=test_df,
        target_col_name="target",
        target_col_type="set",
        use_class_weights=True,
        loss_type="cross_entropy",  # Use cross_entropy to test label smoothing
        class_imbalance=None
    )
    
    # Note: distribution_metadata is only available after train/val split happens during .train()
    # For now, we'll compute basic stats manually
    target_counts = test_df["target"].value_counts()
    majority_count = target_counts.iloc[0]
    minority_count = target_counts.iloc[-1]
    imbalance_score = minority_count / majority_count
    
    print(f"\n📊 Dataset characteristics:")
    print(f"   total_samples: {actual_total}")
    print(f"   imbalance_score: {imbalance_score:.3f}")
    
    # Train predictor
    print(f"\nTraining predictor (100 epochs)...")
    training_results = asyncio.run(predictor.train(
        n_epochs=100,
        batch_size=128,
        fine_tune=False,
    ))
    
    # training_results is a list of training_info entries
    # Extract metrics from the last entry
    if training_results and len(training_results) > 0:
        last_epoch = training_results[-1]
        val_loss = last_epoch.get('validation_loss', None)
        val_f1 = last_epoch.get('val_f1', None)
        val_accuracy = last_epoch.get('val_accuracy', None)
        val_precision = last_epoch.get('val_precision', None)
        val_recall = last_epoch.get('val_recall', None)
        val_auc = last_epoch.get('val_auc', None)
        
        # Find best epoch (lowest validation loss)
        best_epoch = -1
        best_val_loss = float('inf')
        for i, entry in enumerate(training_results):
            vl = entry.get('validation_loss', None)
            if vl is not None and vl < best_val_loss:
                best_val_loss = vl
                best_epoch = i
    else:
        val_loss = None
        val_f1 = None
        val_accuracy = None
        val_precision = None
        val_recall = None
        val_auc = None
        best_epoch = None
    
    result = {
        'configuration': description,
        'total_samples': actual_total,
        'good_ratio': actual_good_ratio,
        'good_count': good_count,
        'bad_count': bad_count,
        'imbalance_score': imbalance_score,
        'val_loss': val_loss,
        'val_f1': val_f1,
        'val_accuracy': val_accuracy,
        'val_precision': val_precision,
        'val_recall': val_recall,
        'val_auc': val_auc,
        'best_epoch': best_epoch,
    }
    
    results.append(result)
    
    print(f"\n✅ Results:")
    print(f"   Val Loss: {val_loss:.4f}" if val_loss else "   Val Loss: N/A")
    print(f"   F1: {val_f1:.4f}" if val_f1 else "   F1: N/A")
    print(f"   Accuracy: {val_accuracy:.4f}" if val_accuracy else "   Accuracy: N/A")
    print(f"   Precision: {val_precision:.4f}" if val_precision else "   Precision: N/A")
    print(f"   Recall: {val_recall:.4f}" if val_recall else "   Recall: N/A")
    print(f"   AUC: {val_auc:.4f}" if val_auc else "   AUC: N/A")
    print(f"   Best Epoch: {best_epoch}" if best_epoch else "   Best Epoch: N/A")

# Save results
output_file = test_dir / "label_smoothing_results.json"
with open(output_file, 'w') as f:
    json.dump(convert_to_json_serializable(results), f, indent=2)

print()
print("=" * 80)
print("FINAL SUMMARY")
print("=" * 80)
print()
print(f"Results saved to: {output_file}")
print()

# Group results by smoothing level
small_datasets = [r for r in results if r['total_samples'] < 500]
medium_datasets = [r for r in results if 500 <= r['total_samples'] < 1000]
large_datasets = [r for r in results if r['total_samples'] >= 1000]

print("📊 Performance by Label Smoothing Level:")
print()

if small_datasets:
    print("Small Datasets (< 500 samples, smoothing=0.1):")
    avg_f1 = np.mean([r['val_f1'] for r in small_datasets if r['val_f1']])
    avg_auc = np.mean([r['val_auc'] for r in small_datasets if r['val_auc']])
    print(f"  Average F1: {avg_f1:.4f}")
    print(f"  Average AUC: {avg_auc:.4f}")
    print()

if medium_datasets:
    print("Medium Datasets (500-1000 samples, smoothing=0.05):")
    avg_f1 = np.mean([r['val_f1'] for r in medium_datasets if r['val_f1']])
    avg_auc = np.mean([r['val_auc'] for r in medium_datasets if r['val_auc']])
    print(f"  Average F1: {avg_f1:.4f}")
    print(f"  Average AUC: {avg_auc:.4f}")
    print()

if large_datasets:
    print("Large Datasets (>= 1000 samples, smoothing=0.0):")
    avg_f1 = np.mean([r['val_f1'] for r in large_datasets if r['val_f1']])
    avg_auc = np.mean([r['val_auc'] for r in large_datasets if r['val_auc']])
    print(f"  Average F1: {avg_f1:.4f}")
    print(f"  Average AUC: {avg_auc:.4f}")
    print()

print("=" * 80)
print(f"Completed: {datetime.now()}")
print("=" * 80)

