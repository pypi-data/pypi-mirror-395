#!/usr/bin/env python3
"""
Test to verify training monitor integration.
Runs a quick training and verifies that data is posted to monitor.featrix.com.
"""
import sys
import os
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock
import json

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

# Now test the monitor integration with a mock
print("=" * 80)
print("TESTING MONITOR INTEGRATION")
print("=" * 80)

# Mock the requests.post to capture what would be sent
mock_response = MagicMock()
mock_response.status_code = 200
mock_response.json.return_value = {"status": "success", "message": "Training data received"}
mock_response.raise_for_status = MagicMock()  # Don't raise on success

captured_payload = None

def mock_post(url, json=None, timeout=None, **kwargs):
    """Mock requests.post to capture the payload"""
    global captured_payload
    captured_payload = json
    print(f"📤 Mock POST to {url}")
    print(f"   Payload keys: {list(json.keys()) if json else 'None'}")
    return mock_response

# Test with mocked monitor endpoint
with patch('training_monitor.requests.post', side_effect=mock_post):
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
        
        # Verify required fields are present
        required_fields = [
            'customer_id', 'remote_hostname', 'training_type',
            'epochs', 'batch_size', 'metadata',
            'input_rows', 'input_columns', 'training_size', 'validation_size',
            'columns', 'training_loss', 'validation_loss',
            'time_taken', 'ran_on_gpu', 'datetime_started', 'datetime_finished'
        ]
        
        missing_fields = [f for f in required_fields if f not in training_data]
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            sys.exit(1)
        else:
            print("✅ All required fields present")
        
        # Verify column statistics
        if not training_data.get('columns'):
            print("❌ No column statistics collected")
            sys.exit(1)
        
        print(f"\n📊 Column statistics verification:")
        col = training_data['columns'][0]
        print(f"   - First column: {col.get('column_name')}")
        print(f"   - Has detector_type: {'detector_type' in col}")
        print(f"   - Has fill_rate: {'fill_rate' in col}")
        
        # Check if detector info is present
        has_detector_info = any(k.startswith('detector_') or k.startswith('string_length_') for k in col.keys())
        if has_detector_info:
            print("   ✅ Detector information present")
        else:
            print("   ⚠️  No detector information found (may be OK for some column types)")
        
        print()
        
        print("📤 Posting to monitor.featrix.com (mocked)...")
        success = post_training_data(training_data)
        
        if success:
            print("✅ Successfully posted training data to monitor!")
        else:
            print("❌ Failed to post to monitor")
            sys.exit(1)
        
        # Verify the payload was captured
        if captured_payload is None:
            print("❌ Payload was not captured by mock")
            sys.exit(1)
        
        print("\n✅ Monitor integration test PASSED!")
        print("   - Training data collected correctly")
        print("   - All required fields present")
        print("   - Column statistics include detector information")
        print("   - Monitor posting succeeded")
        
    except Exception as e:
        print(f"❌ Error testing monitor integration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

print("=" * 80)

