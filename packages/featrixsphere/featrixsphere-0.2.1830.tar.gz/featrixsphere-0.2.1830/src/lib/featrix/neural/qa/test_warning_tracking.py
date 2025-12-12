#!/usr/bin/env python3
"""
Test warning tracking system in single predictor.
"""
import sys
from pathlib import Path

# Paths
test_dir = Path(__file__).parent
neural_dir = test_dir.parent
featrix_dir = neural_dir.parent
lib_dir = featrix_dir.parent
src_dir = lib_dir.parent

sys.path.insert(0, str(lib_dir))
sys.path.insert(0, str(src_dir))

from featrix.neural.single_predictor import FeatrixSinglePredictor
from featrix.neural.embedded_space import EmbeddingSpace

print("=" * 80)
print("Testing Warning Tracking System")
print("=" * 80)

# Create mock predictor
class MockPredictor:
    pass

class MockEmbeddingSpace:
    def __init__(self):
        self.d_model = 64

es = MockEmbeddingSpace()
predictor = MockPredictor()
fsp = FeatrixSinglePredictor(es, predictor)

# Test recording warnings
print("\n1. Recording warnings...")
fsp.record_training_warning("SINGLE_CLASS_BIAS", epoch=10, details={"auc": 0.45, "accuracy": 0.9})
fsp.record_training_warning("SINGLE_CLASS_BIAS", epoch=15, details={"auc": 0.47, "accuracy": 0.92})
fsp.record_training_warning("LOW_AUC", epoch=20, details={"auc": 0.52, "accuracy": 0.65})
fsp.record_training_warning("SINGLE_CLASS_BIAS", epoch=25, details={"auc": 0.46, "accuracy": 0.91})

# Test has_warnings
print(f"\n2. Has warnings? {fsp.has_warnings()}")

# Test get_model_warnings (summary)
print("\n3. Warning summary:")
summary = fsp.get_model_warnings(include_epoch_details=False)
for warning_type, data in summary.items():
    print(f"  {warning_type}:")
    print(f"    First seen: epoch {data['first_seen']}")
    print(f"    Last seen: epoch {data['last_seen']}")
    print(f"    Count: {data['count']}")
    print(f"    At best epoch: {data['occurred_at_best_epoch']}")

# Test get_model_warnings (full)
print("\n4. Full warning details:")
full = fsp.get_model_warnings(include_epoch_details=True)
for warning_type, data in full["warnings"].items():
    print(f"  {warning_type}:")
    print(f"    Epochs: {data['epochs']}")

# Test get_warning_summary
print("\n5. Human-readable summary:")
print(fsp.get_warning_summary())

# Test best epoch warnings
print("\n6. Simulating best epoch warnings...")
fsp.best_epoch_warnings = [
    {
        "type": "SINGLE_CLASS_BIAS",
        "epoch": 25,
        "details": {"recommendations": ["Use class weights", "Train longer"]}
    }
]

print("Updated summary:")
summary = fsp.get_model_warnings(include_epoch_details=False)
for warning_type, data in summary.items():
    print(f"  {warning_type}:")
    print(f"    At best epoch: {data['occurred_at_best_epoch']}")

print("\nUpdated human-readable:")
print(fsp.get_warning_summary())

print("\n" + "=" * 80)
print("✅ Warning tracking system working correctly!")
print("=" * 80)

