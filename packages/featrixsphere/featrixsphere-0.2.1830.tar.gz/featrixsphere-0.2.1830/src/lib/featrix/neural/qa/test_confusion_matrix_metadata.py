#!/usr/bin/env python3
"""
Quick test to verify confusion matrix metrics are computed and returned.
"""
import sys
import os
from pathlib import Path

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
import asyncio

set_device_cpu()

print("=" * 80)
print("Testing Confusion Matrix Metrics in Single Predictor")
print("=" * 80)

# Load data
data_file = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "qa_data" / "credit_g_31.csv"
input_file = FeatrixInputDataFile(str(data_file))
df = input_file.df

# Sample a small balanced dataset for quick test
pos = df[df["target"] == "good"].sample(n=150, random_state=42, replace=False)
neg = df[df["target"] == "bad"].sample(n=150, random_state=42, replace=False)
test_df = pd.concat([pos, neg]).sample(frac=1, random_state=42).reset_index(drop=True)

print(f"\nDataset: {len(test_df)} records (150 good, 150 bad)")

# Train ES quickly
print("\nTraining ES (10 epochs)...")
dataset = FeatrixInputDataSet(df=test_df, ignore_cols=[], limit_rows=None, encoder_overrides=None)
train_data, val_data = dataset.split(fraction=0.3)  # 30% validation to ensure enough samples
es = EmbeddingSpace(train_data, val_data, n_epochs=10, d_model=64, output_debug_label="confusion_test")
es.train(batch_size=64, n_epochs=10)
print("ES complete")

# Train predictor
print("\nTraining predictor (10 epochs)...")
config = SimpleMLPConfig(d_in=64, d_out=2, d_hidden=128, n_hidden_layers=1, dropout=0.1, normalize=False, residual=True, use_batch_norm=True)
predictor = SimpleMLP(config)
fsp = FeatrixSinglePredictor(es, predictor)

fsp.prep_for_training(train_df=test_df, target_col_name="target", target_col_type="set", use_class_weights=False, loss_type="focal")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
training_results = loop.run_until_complete(fsp.train(
    n_epochs=10,
    batch_size=64,
    fine_tune=False,
    val_pos_label="good"
))
loop.close()

print("\n" + "=" * 80)
print("CHECKING METRICS FROM FINAL EPOCH")
print("=" * 80)

if training_results and len(training_results) > 0:
    final_metrics = training_results[-1].get("metrics", {})
    
    print("\n✅ Standard Metrics:")
    print(f"  - Accuracy: {final_metrics.get('accuracy', 'N/A')}")
    print(f"  - F1: {final_metrics.get('f1', 'N/A')}")
    print(f"  - Precision: {final_metrics.get('precision', 'N/A')}")
    print(f"  - Recall: {final_metrics.get('recall', 'N/A')}")
    print(f"  - AUC: {final_metrics.get('auc', 'N/A')}")
    
    print("\n✅ Confusion Matrix Metrics:")
    has_confusion = all(k in final_metrics for k in ['tp', 'fp', 'tn', 'fn'])
    
    if has_confusion:
        tp = final_metrics.get('tp')
        fp = final_metrics.get('fp')
        tn = final_metrics.get('tn')
        fn = final_metrics.get('fn')
        spec = final_metrics.get('specificity')
        
        print(f"  - TP (True Positives): {tp}")
        print(f"  - FP (False Positives): {fp}")
        print(f"  - TN (True Negatives): {tn}")
        print(f"  - FN (False Negatives): {fn}")
        print(f"  - Specificity: {spec}")
        
        print("\n✅ Confusion Matrix Visualization:")
        print(f"                   Predicted")
        print(f"                Positive  Negative")
        print(f"  Actual Positive   {tp:4d}      {fn:4d}")
        print(f"         Negative   {fp:4d}      {tn:4d}")
        
        # Verify calculations
        total = tp + fp + tn + fn
        accuracy_from_cm = (tp + tn) / total if total > 0 else 0
        precision_from_cm = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall_from_cm = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity_from_cm = tn / (tn + fp) if (tn + fp) > 0 else 0
        
        print(f"\n✅ Verification:")
        print(f"  - Total samples: {total}")
        print(f"  - Accuracy from CM: {accuracy_from_cm:.3f} (vs {final_metrics.get('accuracy'):.3f})")
        print(f"  - Precision from CM: {precision_from_cm:.3f} (vs {final_metrics.get('precision'):.3f})")
        print(f"  - Recall from CM: {recall_from_cm:.3f} (vs {final_metrics.get('recall'):.3f})")
        print(f"  - Specificity from CM: {specificity_from_cm:.3f} (vs {spec:.3f})")
        
        print("\n" + "=" * 80)
        print("✅ SUCCESS: Confusion matrix metrics are present in model metadata!")
        print("=" * 80)
    else:
        print("  ❌ ERROR: Confusion matrix metrics NOT found in metadata!")
        print(f"  Available keys: {list(final_metrics.keys())}")
        print("\n" + "=" * 80)
        print("❌ FAILURE: Confusion matrix metrics missing!")
        print("=" * 80)
else:
    print("❌ ERROR: No training results available!")

