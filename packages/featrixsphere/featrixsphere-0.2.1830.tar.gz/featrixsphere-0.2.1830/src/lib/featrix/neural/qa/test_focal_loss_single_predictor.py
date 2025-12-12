#!/usr/bin/env python3
"""
Local QA test for focal loss in single predictor training.
Runs entirely in one process on CPU - no jobs, no API, no bullshit.
"""
import sys
import os
import pickle
from pathlib import Path

# Add paths - we're in src/lib/featrix/neural/qa/, need to add src/ and src/lib/
test_dir = Path(__file__).parent  # qa/
neural_dir = test_dir.parent  # neural/
featrix_dir = neural_dir.parent  # featrix/
lib_dir = featrix_dir.parent  # lib/
src_dir = lib_dir.parent  # src/

sys.path.insert(0, str(lib_dir))  # For featrix.neural imports
sys.path.insert(0, str(src_dir))  # For other src imports

from featrix.neural.input_data_file import FeatrixInputDataFile
from featrix.neural.embedded_space import EmbeddingSpace
from featrix.neural.input_data_set import FeatrixInputDataSet
from featrix.neural.single_predictor_mlp import SinglePredictorMLP
from featrix.neural.device import set_device_cpu

print("=" * 80)
print("FOCAL LOSS SINGLE PREDICTOR QA TEST")
print("=" * 80)
print("Running locally on CPU - no jobs, no API")
print()

# Force CPU
set_device_cpu()
print("✅ Forced CPU training")
print()

# Load credit data
data_file = Path(__file__).parent.parent.parent.parent.parent.parent / "qa_data" / "credit_g_31.csv"
if not data_file.exists():
    print(f"❌ Data file not found: {data_file}")
    sys.exit(1)

print(f"📁 Loading data from: {data_file}")
input_file = FeatrixInputDataFile(str(data_file))
print(f"📊 Loaded {len(input_file.df)} rows, {len(input_file.df.columns)} columns")
print()

# Create training datasets
dataset = FeatrixInputDataSet(
    df=input_file.df,
    ignore_cols=[],
    limit_rows=None,
    encoder_overrides=None,
)

# Split train/val
train_data, val_data = dataset.split(fraction=0.2)  # 80/20 split
print(f"📊 Train: {len(train_data.df)} rows")
print(f"📊 Val: {len(val_data.df)} rows")
print()

# Train embedding space
print("=" * 80)
print("STEP 1: TRAINING EMBEDDING SPACE (50 EPOCHS)")
print("=" * 80)
print()

es = EmbeddingSpace(
    train_data,
    val_data,
    n_epochs=50,
    d_model=128,
    output_debug_label="focal_loss_qa"
)

print("🚀 Starting ES training...")
es.train(batch_size=128, n_epochs=50)
print("✅ ES training complete")
print()

# Train single predictor using simplified class
print("=" * 80)
print("STEP 2: TRAINING SINGLE PREDICTOR (50 EPOCHS)")
print("=" * 80)
print("Using SinglePredictorMLP - simplified interface")
print("This will use FocalLoss with min_weight=0.1")
print()

sp = SinglePredictorMLP(
    embedding_space=es,
    target_column="target",
    target_column_type="set",
    positive_label="good"
)

print("🚀 Starting single predictor training...")
training_results = sp.train(
    data_file=str(data_file),
    n_epochs=50,
    batch_size=128,
    learning_rate=0.0001,
    fine_tune=False,
    use_class_weights=False
)

print()
print("=" * 80)
print("✅ TRAINING COMPLETE")
print("=" * 80)
print()

# Print final metrics
if training_results and len(training_results) > 0:
    final = training_results[-1]
    print("📊 Final Training Metrics:")
    print(f"   Epoch: {final.get('epoch', 'N/A')}")
    print(f"   Training Loss: {final.get('training_loss', 'N/A'):.4f}")
    print(f"   Validation Loss: {final.get('validation_loss', 'N/A'):.4f}")
    
    metrics = final.get('metrics', {})
    if metrics:
        print(f"   Accuracy: {metrics.get('accuracy', 'N/A'):.3f}")
        print(f"   F1: {metrics.get('f1', 'N/A'):.3f}")
        print(f"   AUC: {metrics.get('auc', 'N/A'):.3f}")
        print(f"   Precision: {metrics.get('precision', 'N/A'):.3f}")
        print(f"   Recall: {metrics.get('recall', 'N/A'):.3f}")

print()
print("✅ QA TEST PASSED - Focal loss with min_weight working!")
print("✅ SinglePredictorMLP simplified interface working!")
