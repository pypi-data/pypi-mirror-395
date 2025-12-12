#!/usr/bin/env python3
"""
Embedding Space Configuration Test - Learning Rate & Batch Size Focus

Tests different ES configurations on credit-g dataset to solve NO_LEARNING issues:
- Learning rates (base LR from OneCycleLR)
- Batch sizes
- Model sizes (d_model)

The goal is to find configurations that avoid NO_LEARNING plateaus.
"""
import sys
import os
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
import shutil

# Paths
test_dir = Path(__file__).parent
neural_dir = test_dir.parent
featrix_dir = neural_dir.parent
lib_dir = featrix_dir.parent
src_dir = lib_dir.parent

# CRITICAL: Clear Python bytecode cache to ensure we're running latest code
# This prevents old .pyc files from being loaded instead of updated source
print("🧹 Clearing Python bytecode cache (AGGRESSIVE MODE)...")
print(f"   Target directory: {lib_dir}")

# Clear __pycache__ directories
pycache_count = 0
for pycache_dir in lib_dir.rglob("__pycache__"):
    try:
        shutil.rmtree(pycache_dir)
        pycache_count += 1
        print(f"   Removed __pycache__: {pycache_dir.relative_to(lib_dir)}")
    except Exception as e:
        print(f"   Warning: Could not remove {pycache_dir}: {e}")

# Clear .pyc files
pyc_count = 0
for pyc_file in lib_dir.rglob("*.pyc"):
    try:
        pyc_file.unlink()
        pyc_count += 1
    except Exception:
        pass

# Clear .pyo files (optimized bytecode)
pyo_count = 0
for pyo_file in lib_dir.rglob("*.pyo"):
    try:
        pyo_file.unlink()
        pyo_count += 1
    except Exception:
        pass

print(f"   Removed {pycache_count} __pycache__ dirs, {pyc_count} .pyc files, {pyo_count} .pyo files")
print("✅ Cache cleared - using fresh source code")
print()

# Force Python to invalidate its import cache
import importlib
importlib.invalidate_caches()
print("✅ Python import cache invalidated")
print()

sys.path.insert(0, str(lib_dir))
sys.path.insert(0, str(src_dir))

from featrix.neural.input_data_file import FeatrixInputDataFile
from featrix.neural.embedded_space import EmbeddingSpace
from featrix.neural.input_data_set import FeatrixInputDataSet
from featrix.neural.device import set_device_cpu

set_device_cpu()

print("=" * 80)
print("🧪 EMBEDDING SPACE CONFIGURATION TEST - CREDIT-G")
print("=" * 80)
print(f"Started: {datetime.now()}")
print()

# Load credit-g dataset
data_file = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "qa_data" / "credit_g_31.csv"
input_file = FeatrixInputDataFile(str(data_file))
df = input_file.df

print(f"Dataset: {len(df)} rows")
print(f"Columns: {list(df.columns)}")
print()

# Test configurations focusing on LEARNING RATE and BATCH SIZE
# Format: (name, d_model, batch_size, lr_scale)
# lr_scale multiplies the base OneCycleLR max_lr (default is 1e-3)
configs = [
    # Baseline: current defaults
    ("baseline", 128, 64, 1.0),
    
    # Try higher learning rates (NO_LEARNING might mean LR is too low)
    ("high_lr_2x", 128, 64, 2.0),
    ("high_lr_3x", 128, 64, 3.0),
    ("high_lr_5x", 128, 64, 5.0),
    
    # Try different batch sizes (affects gradient noise)
    ("batch_32", 128, 32, 1.0),
    ("batch_128", 128, 128, 1.0),
    
    # Combine higher LR with smaller batch
    ("high_lr_small_batch", 128, 32, 3.0),
    
    # Try smaller model (faster convergence)
    ("small_model", 64, 64, 1.0),
    
    # Try larger model with higher LR
    ("large_model_high_lr", 256, 64, 2.0),
]

results = []
n_epochs = 50  # Train each for 50 epochs

print(f"Testing {len(configs)} configurations ({n_epochs} epochs each)")
print()

for config_name, d_model, batch_size, lr_scale in configs:
    print("=" * 80)
    print(f"📊 Configuration: {config_name}")
    print("=" * 80)
    print(f"Config:")
    print(f"  d_model: {d_model}")
    print(f"  batch_size: {batch_size}")
    print(f"  lr_scale: {lr_scale}x (base max_lr=1e-3)")
    print()
    
    # Create fresh train/val splits for each config
    dataset = FeatrixInputDataSet(df=df, ignore_cols=[], limit_rows=None, encoder_overrides=None)
    
    # Extract detected column types
    detected_types = {}
    for col_name, detector in dataset._detectors.items():
        detected_types[col_name] = detector.get_codec_name()
    
    # SET the encoderOverrides on the dataset so split() will pass them along
    dataset.encoderOverrides = detected_types
    
    # Split
    train_data, val_data = dataset.split(fraction=0.2)
    
    print(f"Train: {len(train_data.df)} rows, Val: {len(val_data.df)} rows")
    print()
    
    # Create embedding space with this model size
    es = EmbeddingSpace(
        train_input_data=train_data,
        val_input_data=val_data,
        d_model=d_model,
        n_epochs=n_epochs,
        output_dir=str(test_dir),
    )
    
    # Calculate actual max_lr for OneCycleLR
    base_max_lr = 1e-3
    actual_max_lr = base_max_lr * lr_scale
    
    # Create custom optimizer params with scaled LR
    optimizer_params = {
        'lr': actual_max_lr,  # This becomes max_lr for OneCycleLR
    }
    
    # Train with this batch size and LR
    print(f"Training with max_lr={actual_max_lr:.6f}...")
    es.train(
        batch_size=batch_size,
        n_epochs=n_epochs,
        print_progress_step=10,
        optimizer_params=optimizer_params,
        enable_weightwatcher=False,  # Disable to focus on learning dynamics
    )
    
    # Extract results from training timeline
    timeline_path = test_dir / "training_timeline.json"
    if timeline_path.exists():
        with open(timeline_path, 'r') as f:
            timeline_data = json.load(f)
        
        timeline = timeline_data.get('timeline', [])
        
        if timeline:
            # Get final metrics
            final_epoch = timeline[-1]
            final_val_loss = final_epoch.get('val_loss')
            epochs_completed = len(timeline)
            
            # Calculate loss variance (stability metric)
            val_losses = [e.get('val_loss') for e in timeline if e.get('val_loss') is not None]
            if len(val_losses) > 1:
                loss_variance = np.var(val_losses)
                loss_std = np.std(val_losses)
            else:
                loss_variance = None
                loss_std = None
            
            # Find best val loss
            best_val_loss = min(val_losses) if val_losses else None
            best_epoch = None
            if best_val_loss:
                for i, e in enumerate(timeline):
                    if e.get('val_loss') == best_val_loss:
                        best_epoch = i
                        break
            
            # Get corrective actions count
            corrective_actions = timeline_data.get('corrective_actions', [])
            n_corrective_actions = len(corrective_actions)
            
            # Check for NO_LEARNING events
            no_learning_count = sum(1 for e in timeline if e.get('no_learning_detected', False))
            
            # Check for early stopping
            stopped_early = epochs_completed < n_epochs
            
            result = {
                'config_name': config_name,
                'd_model': d_model,
                'batch_size': batch_size,
                'lr_scale': lr_scale,
                'actual_max_lr': actual_max_lr,
                'epochs_completed': epochs_completed,
                'stopped_early': stopped_early,
                'final_val_loss': final_val_loss,
                'best_val_loss': best_val_loss,
                'best_epoch': best_epoch,
                'loss_variance': loss_variance,
                'loss_std': loss_std,
                'n_corrective_actions': n_corrective_actions,
                'no_learning_count': no_learning_count,
            }
            
            results.append(result)
            
            print()
            print(f"✅ Results:")
            print(f"   Epochs: {epochs_completed}/{n_epochs}" + (" (stopped early)" if stopped_early else ""))
            print(f"   Final Val Loss: {final_val_loss:.4f}" if final_val_loss else "   Final Val Loss: N/A")
            print(f"   Best Val Loss: {best_val_loss:.4f} (epoch {best_epoch})" if best_val_loss else "   Best Val Loss: N/A")
            print(f"   Loss Std Dev: {loss_std:.4f}" if loss_std else "   Loss Std Dev: N/A")
            print(f"   NO_LEARNING events: {no_learning_count}")
            print(f"   Corrective Actions: {n_corrective_actions}")
        else:
            print("❌ No timeline data found")
            results.append({
                'config_name': config_name,
                'd_model': d_model,
                'batch_size': batch_size,
                'lr_scale': lr_scale,
                'error': 'No timeline data'
            })
    else:
        print(f"❌ Timeline file not found: {timeline_path}")
        results.append({
            'config_name': config_name,
            'd_model': d_model,
            'batch_size': batch_size,
            'lr_scale': lr_scale,
            'error': 'Timeline file not found'
        })
    
    print()

# Save results
output_file = test_dir / "embedding_space_config_results.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print()
print("=" * 80)
print("📊 FINAL COMPARISON")
print("=" * 80)
print()

# Sort by best val loss
valid_results = [r for r in results if 'best_val_loss' in r and r['best_val_loss'] is not None]
if valid_results:
    sorted_results = sorted(valid_results, key=lambda x: x['best_val_loss'])
    
    print("Rankings by Best Validation Loss:")
    print()
    print(f"{'Rank':<6} {'Configuration':<30} {'d_model':<10} {'batch':<8} {'LR scale':<10} {'Best Loss':<12} {'NO_LEARN':<10}")
    print("-" * 100)
    
    for i, r in enumerate(sorted_results, 1):
        print(f"{i:<6} {r['config_name']:<30} {r['d_model']:<10} {r['batch_size']:<8} {r['lr_scale']:<10.1f} {r['best_val_loss']:<12.4f} {r['no_learning_count']:<10}")
    
    print()
    print(f"🏆 Winner: {sorted_results[0]['config_name']}")
    print(f"   d_model: {sorted_results[0]['d_model']}")
    print(f"   batch_size: {sorted_results[0]['batch_size']}")
    print(f"   lr_scale: {sorted_results[0]['lr_scale']}x")
    print(f"   Best Val Loss: {sorted_results[0]['best_val_loss']:.4f}")
    print(f"   NO_LEARNING events: {sorted_results[0]['no_learning_count']}")
    print(f"   Achieved at Epoch: {sorted_results[0]['best_epoch']}")
    print()
    
    # Compare to baseline
    baseline = next((r for r in results if r['config_name'] == 'baseline'), None)
    winner = sorted_results[0]
    
    if baseline and baseline.get('best_val_loss') and winner['config_name'] != 'baseline':
        improvement = baseline['best_val_loss'] - winner['best_val_loss']
        pct_improvement = (improvement / baseline['best_val_loss']) * 100
        print(f"📈 Improvement vs Baseline:")
        print(f"   Baseline: {baseline['best_val_loss']:.4f} ({baseline['no_learning_count']} NO_LEARNING events)")
        print(f"   Winner: {winner['best_val_loss']:.4f} ({winner['no_learning_count']} NO_LEARNING events)")
        print(f"   Difference: {improvement:.4f} ({pct_improvement:+.2f}%)")
        print(f"   NO_LEARNING reduction: {baseline['no_learning_count'] - winner['no_learning_count']} events")
    
else:
    print("❌ No valid results to compare")

print()
print(f"Results saved to: {output_file}")
print()
print("=" * 80)
print(f"Completed: {datetime.now()}")
print("=" * 80)

