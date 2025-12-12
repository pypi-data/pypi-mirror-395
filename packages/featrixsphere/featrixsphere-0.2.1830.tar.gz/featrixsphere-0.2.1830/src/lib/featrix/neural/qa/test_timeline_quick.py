#!/usr/bin/env python3
"""
Quick test to verify training timeline generation.
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
from featrix.neural.device import set_device_cpu
import pandas as pd

set_device_cpu()

print("=" * 80)
print("CREDIT-G TRAINING TIMELINE - 100 EPOCHS")
print("=" * 80)

# Load data
data_file = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "qa_data" / "credit_g_31.csv"
input_file = FeatrixInputDataFile(str(data_file))
df = input_file.df

# Use full dataset - NO synthetic bullshit
print(f"Dataset: {len(df)} rows (FULL credit-g)")

# Create train/val splits
train_df = df.sample(frac=0.8, random_state=42).reset_index(drop=True)
val_df = df.drop(train_df.index).reset_index(drop=True)

train_data = FeatrixInputDataSet(df=train_df, ignore_cols=[], limit_rows=None)
val_data = FeatrixInputDataSet(df=val_df, ignore_cols=[], limit_rows=None)

# Train embedding space for 100 epochs
print(f"\nTraining ES for 100 epochs on real credit-g data...")
print(f"Output dir: {test_dir}")

es = EmbeddingSpace(
    train_input_data=train_data,
    val_input_data=val_data,
    d_model=128,  # Full model size
    n_epochs=100,
    output_dir=str(test_dir),
)

es.train(
    batch_size=32,
    n_epochs=100,
    print_progress_step=10,
    enable_weightwatcher=True,
    weightwatcher_save_every=10,
)

print("\n✅ Training complete")

# Check if timeline was created
timeline_path = test_dir / "training_timeline.json"
if timeline_path.exists():
    print(f"\n✅ Timeline file created: {timeline_path}")
    import json
    with open(timeline_path, 'r') as f:
        data = json.load(f)
    print(f"   - {len(data['timeline'])} epochs recorded")
    print(f"   - {len(data.get('corrective_actions', []))} corrective actions")
else:
    print(f"\n❌ Timeline file NOT created at: {timeline_path}")
    print(f"   Output dir was: {es.output_dir}")

print("=" * 80)

