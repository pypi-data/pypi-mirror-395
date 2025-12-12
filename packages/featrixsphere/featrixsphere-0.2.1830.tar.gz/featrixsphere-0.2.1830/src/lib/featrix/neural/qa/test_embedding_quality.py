#!/usr/bin/env python3
"""
Embedding Quality Test - Sensitivity Analysis

Tests the quality of trained embeddings by:
1. Taking a row of data
2. Making small controlled changes (one field at a time)
3. Computing embeddings for original and modified rows
4. Measuring distance between embeddings
5. Evaluating if distances are semantically meaningful

Goal: Verify that:
- Similar data → similar embeddings (small distance)
- Different data → different embeddings (large distance)
- Embeddings capture semantic meaning of changes
"""
import sys
import os
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
import torch

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

set_device_cpu()

print("=" * 80)
print("🔍 EMBEDDING QUALITY TEST - SENSITIVITY ANALYSIS")
print("=" * 80)
print(f"Started: {datetime.now()}")
print()

# Load credit-g dataset
data_file = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "qa_data" / "credit_g_31.csv"
input_file = FeatrixInputDataFile(str(data_file))
df = input_file.df

print(f"Dataset: {len(df)} rows")
print()

# Load a trained embedding space
# First, we need to train one if it doesn't exist
print("Checking for existing trained embedding space...")
best_model_path = test_dir / "training_state_BEST.pth"

if not best_model_path.exists():
    print("No trained model found. Training a quick embedding space (20 epochs)...")
    
    # Create dataset
    dataset = FeatrixInputDataSet(df=df, ignore_cols=[], limit_rows=None, encoder_overrides=None)
    
    # Extract detected column types
    detected_types = {}
    for col_name, detector in dataset._detectors.items():
        detected_types[col_name] = detector.get_codec_name()
    
    dataset.encoderOverrides = detected_types
    train_data, val_data = dataset.split(fraction=0.2)
    
    # Train embedding space
    es = EmbeddingSpace(
        train_input_data=train_data,
        val_input_data=val_data,
        d_model=128,
        n_epochs=20,
        output_dir=str(test_dir),
    )
    
    es.train(
        batch_size=64,
        n_epochs=20,
        print_progress_step=10,
        enable_weightwatcher=False,
    )
    
    print("✅ Training complete")
else:
    print(f"✅ Found trained model: {best_model_path}")
    
    # Load the trained model
    dataset = FeatrixInputDataSet(df=df, ignore_cols=[], limit_rows=None, encoder_overrides=None)
    detected_types = {}
    for col_name, detector in dataset._detectors.items():
        detected_types[col_name] = detector.get_codec_name()
    
    dataset.encoderOverrides = detected_types
    train_data, val_data = dataset.split(fraction=0.2)
    
    es = EmbeddingSpace(
        train_input_data=train_data,
        val_input_data=val_data,
        d_model=128,
        n_epochs=20,
        output_dir=str(test_dir),
    )
    
    print("Loading best checkpoint...")
    es.load_best_checkpoint()
    print("✅ Model loaded")

print()
print("=" * 80)
print("TESTING EMBEDDING SENSITIVITY")
print("=" * 80)
print()


def get_embedding(es, row_df):
    """Get embedding for a single row."""
    # Encode the row
    input_dataset = FeatrixInputDataSet(df=row_df, ignore_cols=[], limit_rows=None, encoder_overrides=es.train_input_data.encoderOverrides)
    
    # Get the encoded tensor
    es.encoder.eval()
    with torch.no_grad():
        encodings = es.encoder.encode_entire_dataset(input_dataset)
    
    # Return as numpy array
    return encodings.cpu().numpy()[0]  # First (only) row


def cosine_distance(emb1, emb2):
    """Compute cosine distance (1 - cosine similarity)."""
    dot = np.dot(emb1, emb2)
    norm1 = np.linalg.norm(emb1)
    norm2 = np.linalg.norm(emb2)
    cosine_sim = dot / (norm1 * norm2)
    return 1 - cosine_sim


def euclidean_distance(emb1, emb2):
    """Compute euclidean distance."""
    return np.linalg.norm(emb1 - emb2)


# Select a test row
test_row_idx = 0
original_row = df.iloc[test_row_idx:test_row_idx+1].copy()

print(f"Original row (index {test_row_idx}):")
for col in original_row.columns:
    print(f"  {col}: {original_row[col].values[0]}")
print()

# Get original embedding
original_embedding = get_embedding(es, original_row)
print(f"Original embedding shape: {original_embedding.shape}")
print(f"Original embedding norm: {np.linalg.norm(original_embedding):.4f}")
print()

# Test different types of changes
results = []

print("=" * 80)
print("TEST 1: Change target (good → bad)")
print("=" * 80)
modified_row = original_row.copy()
if modified_row['target'].values[0] == 'good':
    modified_row['target'] = 'bad'
else:
    modified_row['target'] = 'good'

modified_embedding = get_embedding(es, modified_row)
cos_dist = cosine_distance(original_embedding, modified_embedding)
euc_dist = euclidean_distance(original_embedding, modified_embedding)

print(f"Changed: {original_row['target'].values[0]} → {modified_row['target'].values[0]}")
print(f"Cosine distance: {cos_dist:.6f}")
print(f"Euclidean distance: {euc_dist:.6f}")
print()

results.append({
    'change_type': 'target_flip',
    'field': 'target',
    'original_value': str(original_row['target'].values[0]),
    'new_value': str(modified_row['target'].values[0]),
    'cosine_distance': float(cos_dist),
    'euclidean_distance': float(euc_dist),
})

print("=" * 80)
print("TEST 2: Small change in age (+1 year)")
print("=" * 80)
modified_row = original_row.copy()
original_age = modified_row['age'].values[0]
modified_row['age'] = original_age + 1

modified_embedding = get_embedding(es, modified_row)
cos_dist = cosine_distance(original_embedding, modified_embedding)
euc_dist = euclidean_distance(original_embedding, modified_embedding)

print(f"Changed: age {original_age} → {modified_row['age'].values[0]}")
print(f"Cosine distance: {cos_dist:.6f}")
print(f"Euclidean distance: {euc_dist:.6f}")
print()

results.append({
    'change_type': 'age_plus_1',
    'field': 'age',
    'original_value': str(original_age),
    'new_value': str(modified_row['age'].values[0]),
    'cosine_distance': float(cos_dist),
    'euclidean_distance': float(euc_dist),
})

print("=" * 80)
print("TEST 3: Large change in age (+20 years)")
print("=" * 80)
modified_row = original_row.copy()
original_age = modified_row['age'].values[0]
modified_row['age'] = original_age + 20

modified_embedding = get_embedding(es, modified_row)
cos_dist = cosine_distance(original_embedding, modified_embedding)
euc_dist = euclidean_distance(original_embedding, modified_embedding)

print(f"Changed: age {original_age} → {modified_row['age'].values[0]}")
print(f"Cosine distance: {cos_dist:.6f}")
print(f"Euclidean distance: {euc_dist:.6f}")
print()

results.append({
    'change_type': 'age_plus_20',
    'field': 'age',
    'original_value': str(original_age),
    'new_value': str(modified_row['age'].values[0]),
    'cosine_distance': float(cos_dist),
    'euclidean_distance': float(euc_dist),
})

print("=" * 80)
print("TEST 4: Change credit amount (small change)")
print("=" * 80)
modified_row = original_row.copy()
original_amount = modified_row['credit_amount'].values[0]
modified_row['credit_amount'] = original_amount * 1.1  # 10% increase

modified_embedding = get_embedding(es, modified_row)
cos_dist = cosine_distance(original_embedding, modified_embedding)
euc_dist = euclidean_distance(original_embedding, modified_embedding)

print(f"Changed: credit_amount {original_amount} → {modified_row['credit_amount'].values[0]}")
print(f"Cosine distance: {cos_dist:.6f}")
print(f"Euclidean distance: {euc_dist:.6f}")
print()

results.append({
    'change_type': 'credit_amount_10pct',
    'field': 'credit_amount',
    'original_value': str(original_amount),
    'new_value': str(modified_row['credit_amount'].values[0]),
    'cosine_distance': float(cos_dist),
    'euclidean_distance': float(euc_dist),
})

print("=" * 80)
print("TEST 5: Change checking_status")
print("=" * 80)
modified_row = original_row.copy()
original_status = modified_row['checking_status'].values[0]
# Get all possible values
possible_values = df['checking_status'].unique()
# Pick a different value
new_value = [v for v in possible_values if v != original_status][0]
modified_row['checking_status'] = new_value

modified_embedding = get_embedding(es, modified_row)
cos_dist = cosine_distance(original_embedding, modified_embedding)
euc_dist = euclidean_distance(original_embedding, modified_embedding)

print(f"Changed: checking_status '{original_status}' → '{new_value}'")
print(f"Cosine distance: {cos_dist:.6f}")
print(f"Euclidean distance: {euc_dist:.6f}")
print()

results.append({
    'change_type': 'checking_status_change',
    'field': 'checking_status',
    'original_value': str(original_status),
    'new_value': str(new_value),
    'cosine_distance': float(cos_dist),
    'euclidean_distance': float(euc_dist),
})

print("=" * 80)
print("TEST 6: No change (baseline - should be very small distance)")
print("=" * 80)
modified_row = original_row.copy()

modified_embedding = get_embedding(es, modified_row)
cos_dist = cosine_distance(original_embedding, modified_embedding)
euc_dist = euclidean_distance(original_embedding, modified_embedding)

print(f"No changes made")
print(f"Cosine distance: {cos_dist:.6f}")
print(f"Euclidean distance: {euc_dist:.6f}")
print()

results.append({
    'change_type': 'no_change',
    'field': 'none',
    'original_value': 'same',
    'new_value': 'same',
    'cosine_distance': float(cos_dist),
    'euclidean_distance': float(euc_dist),
})

# Save results
output_file = test_dir / "embedding_quality_results.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()

print(f"{'Test':<30} {'Field':<20} {'Cosine Dist':<15} {'Euclidean Dist':<15}")
print("-" * 80)
for r in results:
    print(f"{r['change_type']:<30} {r['field']:<20} {r['cosine_distance']:<15.6f} {r['euclidean_distance']:<15.2f}")

print()
print("Expected behavior:")
print("  - no_change: Should have ~0 distance (identical rows)")
print("  - Small changes (age+1, credit+10%): Small distance")
print("  - Large changes (age+20, target flip): Large distance")
print()
print(f"Results saved to: {output_file}")
print()
print("=" * 80)
print(f"Completed: {datetime.now()}")
print("=" * 80)

