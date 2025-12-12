#!/usr/bin/env python3
"""
Quick test to verify training monitor integration.
Tests that training data is posted to monitor.featrix.com after training.
"""
import sys
import os
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
from featrix.neural.device import set_device_cpu
import pandas as pd

set_device_cpu()

print("=" * 80)
print("TESTING TRAINING MONITOR INTEGRATION")
print("=" * 80)

# Load data
data_file = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "qa_data" / "credit_g_31.csv"
if not data_file.exists():
    print(f"❌ Data file not found: {data_file}")
    sys.exit(1)

input_file = FeatrixInputDataFile(str(data_file))
df = input_file.df

# Use a small subset for quick test
df = df.head(200)  # Just 200 rows for quick test
print(f"Dataset: {len(df)} rows (subset for quick test)")

# Create train/val splits
train_df = df.sample(frac=0.8, random_state=42).reset_index(drop=True)
val_df = df.drop(train_df.index).reset_index(drop=True)

train_data = FeatrixInputDataSet(df=train_df, ignore_cols=[], limit_rows=None)
val_data = FeatrixInputDataSet(df=val_df, ignore_cols=[], limit_rows=None)

# Train embedding space for just 3 epochs
print(f"\nTraining ES for 3 epochs (quick test)...")
print(f"Output dir: {test_dir}")

training_start_time = datetime.now()

es = EmbeddingSpace(
    train_input_data=train_data,
    val_input_data=val_data,
    d_model=64,  # Smaller model for quick test
    n_epochs=3,
    output_dir=str(test_dir),
)

es.train(
    batch_size=32,
    n_epochs=3,
    print_progress_step=1,
)

training_end_time = datetime.now()

print("\n✅ Training complete")
print()

# Now test the monitor integration
print("=" * 80)
print("TESTING MONITOR INTEGRATION")
print("=" * 80)

try:
    from training_monitor import collect_es_training_data, post_training_data
    
    print("📊 Collecting training data for monitor...")
    training_data = collect_es_training_data(
        embedding_space=es,
        train_df=train_df,
        val_df=val_df,
        training_start_time=training_start_time,
        training_end_time=training_end_time,
        epochs=3,
        batch_size=32,
        learning_rate=0.001,
    )
    
    print(f"✅ Collected training data:")
    print(f"   - Training type: {training_data.get('training_type')}")
    print(f"   - Epochs: {training_data.get('epochs')}")
    print(f"   - Columns: {len(training_data.get('columns', []))}")
    print(f"   - Training loss entries: {len(training_data.get('training_loss', []))}")
    print(f"   - Validation loss entries: {len(training_data.get('validation_loss', []))}")
    print()
    
    # Check column stats
    if training_data.get('columns'):
        col = training_data['columns'][0]
        print(f"📊 Sample column stats (first column):")
        print(f"   - Name: {col.get('column_name')}")
        print(f"   - Detector type: {col.get('detector_type', 'N/A')}")
        print(f"   - Fill rate: {col.get('fill_rate', 0):.2%}")
        if 'string_length_mean' in col:
            print(f"   - String length mean: {col.get('string_length_mean'):.1f}")
        if 'mean' in col:
            print(f"   - Numeric mean: {col.get('mean'):.2f}")
        print()
    
    print("📤 Posting to monitor.featrix.com...")
    success = post_training_data(training_data)
    
    if success:
        print("✅ Successfully posted training data to monitor!")
    else:
        print("⚠️  Failed to post to monitor (check logs above for details)")
        print("   This is OK for testing - monitor endpoint may not be available")
    
except Exception as e:
    print(f"❌ Error testing monitor integration: {e}")
    import traceback
    traceback.print_exc()

print("=" * 80)

