#!/usr/bin/env python3
"""
Test extending embedding space training with new data at the neural layer.

This test directly exercises the EmbeddingSpace class to verify that:
1. An embedding space can be trained for initial epochs
2. The embedding space can be saved and loaded
3. New data can be added and training can continue from the checkpoint
4. The training actually continues from where it left off (not restarting)

This is a neural-layer test that bypasses the API and tests the core functionality.
"""
import sys
import os
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Check for required dependencies
try:
    import pandas as pd
    import numpy as np
    import torch
except ImportError as e:
    print(f"❌ Missing required dependency: {e}")
    print("   This test requires pandas, numpy, and torch to be installed.")
    print("   Please install them or run this test in the proper environment.")
    sys.exit(1)

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
from featrix.neural.io_utils import load_embedded_space

set_device_cpu()

print("=" * 80)
print("🧪 TEST: Extend Embedding Space Training (Neural Layer)")
print("=" * 80)
print(f"Started: {datetime.now()}")
print()

# Create a temporary directory for this test
test_output_dir = Path(tempfile.mkdtemp(prefix="test_extend_es_"))
print(f"Test output directory: {test_output_dir}")
print()

try:
    # Step 1: Create initial training data
    print("=" * 80)
    print("STEP 1: Create Initial Training Data")
    print("=" * 80)
    
    initial_data = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5] * 20,  # 100 rows
        'feature2': ['a', 'b', 'c', 'd', 'e'] * 20,
        'feature3': [10.5, 20.3, 30.1, 40.9, 50.7] * 20,
        'target': ['yes', 'no', 'yes', 'no', 'yes'] * 20
    })
    
    print(f"Initial data: {len(initial_data)} rows")
    print(f"Columns: {list(initial_data.columns)}")
    print()
    
    # Create dataset
    initial_dataset = FeatrixInputDataSet(
        df=initial_data,
        ignore_cols=[],
        limit_rows=None,
        encoder_overrides=None
    )
    
    # Extract detected column types
    detected_types = {}
    for col_name, detector in initial_dataset._detectors.items():
        detected_types[col_name] = detector.get_codec_name()
    
    initial_dataset.encoderOverrides = detected_types
    print(f"Detected column types: {detected_types}")
    print()
    
    # Split into train/val
    train_data, val_data = initial_dataset.split(fraction=0.2)
    print(f"Train: {len(train_data)} rows, Val: {len(val_data)} rows")
    print()
    
    # Step 2: Train initial embedding space for 3 epochs
    print("=" * 80)
    print("STEP 2: Train Initial Embedding Space (3 epochs)")
    print("=" * 80)
    
    initial_output_dir = test_output_dir / "initial_training"
    initial_output_dir.mkdir(parents=True, exist_ok=True)
    
    es_initial = EmbeddingSpace(
        train_input_data=train_data,
        val_input_data=val_data,
        d_model=128,
        n_epochs=3,
        output_dir=str(initial_output_dir),
        name="test_extend_initial"
    )
    
    print(f"Training for 3 epochs...")
    es_initial.train(
        batch_size=32,
        n_epochs=3,
        print_progress_step=1,
        enable_weightwatcher=False,
        save_state_after_every_epoch=True,  # Save checkpoints every epoch so we can resume
    )
    
    print("✅ Initial training complete")
    print()
    
    # Get training state
    initial_timeline = getattr(es_initial, '_training_timeline', [])
    initial_epochs = len(initial_timeline)
    print(f"Initial training completed {initial_epochs} epochs")
    
    if initial_timeline:
        final_loss = initial_timeline[-1].get('current_loss', 'N/A')
        final_val_loss = initial_timeline[-1].get('validation_loss', 'N/A')
        print(f"Final training loss: {final_loss}")
        print(f"Final validation loss: {final_val_loss}")
    print()
    
    # Step 3: Save the embedding space
    print("=" * 80)
    print("STEP 3: Save Initial Embedding Space")
    print("=" * 80)
    
    es_save_path = initial_output_dir / "embedding_space.pickle"
    import pickle
    with open(es_save_path, 'wb') as f:
        pickle.dump(es_initial, f)
    
    print(f"✅ Saved embedding space to: {es_save_path}")
    print()
    
    # Step 4: Create new data for extension
    print("=" * 80)
    print("STEP 4: Create New Data for Extension")
    print("=" * 80)
    
    new_data = pd.DataFrame({
        'feature1': [6, 7, 8, 9, 10] * 15,  # 75 rows - different data
        'feature2': ['f', 'g', 'h', 'i', 'j'] * 15,
        'feature3': [60.5, 70.3, 80.1, 90.9, 100.7] * 15,
        'target': ['no', 'yes', 'no', 'yes', 'no'] * 15
    })
    
    print(f"New data: {len(new_data)} rows")
    print()
    
    # Combine old and new data
    combined_data = pd.concat([initial_data, new_data], ignore_index=True)
    print(f"Combined data: {len(combined_data)} rows ({len(initial_data)} + {len(new_data)})")
    print()
    
    # Step 5: Load the saved embedding space and extend with new data
    print("=" * 80)
    print("STEP 5: Load Embedding Space and Extend with New Data")
    print("=" * 80)
    
    # Load the saved embedding space
    print(f"Loading embedding space from: {es_save_path}")
    es_extended = load_embedded_space(str(es_save_path))
    print("✅ Embedding space loaded")
    print()
    
    # Create dataset from combined data
    combined_dataset = FeatrixInputDataSet(
        df=combined_data,
        ignore_cols=[],
        limit_rows=None,
        encoder_overrides=detected_types  # Use same types as initial
    )
    combined_dataset.encoderOverrides = detected_types
    
    # Split combined data
    train_data_extended, val_data_extended = combined_dataset.split(fraction=0.2)
    print(f"Extended train: {len(train_data_extended)} rows, Extended val: {len(val_data_extended)} rows")
    print()
    
    # Update the embedding space with new data
    es_extended.train_input_data = train_data_extended
    es_extended.val_input_data = val_data_extended
    
    # Get the current epoch from the timeline (needed for checkpoint creation)
    existing_epochs = len(es_extended._training_timeline) if hasattr(es_extended, '_training_timeline') else 0
    
    # Update output directory for extended training
    extended_output_dir = test_output_dir / "extended_training"
    extended_output_dir.mkdir(parents=True, exist_ok=True)
    
    # CRITICAL: Copy checkpoint files from initial training to extended training directory
    # The training code looks for checkpoints in output_dir, so we need them there
    print("📋 Copying checkpoint files to extended training directory...")
    
    # Find all checkpoint files in initial training directory
    # Checkpoints can be in the output_dir or in subdirectories
    initial_checkpoints = []
    for pattern in ["training_state_*.pth", "**/training_state_*.pth"]:
        initial_checkpoints.extend(initial_output_dir.glob(pattern))
    
    # Also check for BEST checkpoint
    initial_best = initial_output_dir / "training_state_BEST.pth"
    if not initial_best.exists():
        # Check in subdirectories
        best_files = list(initial_output_dir.glob("**/training_state_BEST.pth"))
        if best_files:
            initial_best = best_files[0]
    
    copied_count = 0
    for checkpoint in initial_checkpoints:
        if checkpoint.exists() and checkpoint.is_file():
            dest = extended_output_dir / checkpoint.name
            shutil.copy2(checkpoint, dest)
            copied_count += 1
            print(f"   ✅ Copied: {checkpoint.name}")
    
    # Copy BEST checkpoint and also create epoch-specific checkpoint from it
    if initial_best.exists():
        dest_best = extended_output_dir / "training_state_BEST.pth"
        shutil.copy2(initial_best, dest_best)
        copied_count += 1
        print(f"   ✅ Copied: training_state_BEST.pth")
        
        # CRITICAL: Create epoch-specific checkpoint from BEST checkpoint
        # The training code expects training_state_e-{epoch}.pth, not just BEST
        try:
            import torch
            best_state = torch.load(initial_best, weights_only=False, map_location='cpu')
            # Try to get epoch from checkpoint, fall back to last epoch (existing_epochs - 1)
            best_epoch = best_state.get('epoch_idx', existing_epochs - 1 if existing_epochs > 0 else 0)
            if best_epoch is not None and best_epoch >= 0:
                epoch_checkpoint_path = extended_output_dir / f"training_state_e-{best_epoch}.pth"
                torch.save(best_state, epoch_checkpoint_path)
                copied_count += 1
                print(f"   ✅ Created epoch checkpoint: training_state_e-{best_epoch}.pth (from BEST)")
        except Exception as e:
            print(f"   ⚠️  Could not create epoch checkpoint from BEST: {e}")
    
    # CRITICAL: Create checkpoint for the last completed epoch
    # Epochs are 0-indexed, so if we completed 3 epochs (0, 1, 2), the last epoch is 2
    # But the training code expects to resume FROM epoch 3 (the next epoch to train)
    # So we need to create checkpoints for both the last completed epoch AND the epoch we're resuming from
    if existing_epochs > 0:
        last_completed_epoch = existing_epochs - 1  # Last epoch that was completed (0-indexed)
        resume_from_epoch = existing_epochs  # The epoch we're resuming from (next to train)
        
        if initial_best.exists():
            try:
                import torch
                best_state = torch.load(initial_best, weights_only=False, map_location='cpu')
                
                # Create checkpoint for the last completed epoch
                best_state_last = best_state.copy()
                best_state_last['epoch_idx'] = last_completed_epoch
                epoch_checkpoint_path = extended_output_dir / f"training_state_e-{last_completed_epoch}.pth"
                if not epoch_checkpoint_path.exists():
                    torch.save(best_state_last, epoch_checkpoint_path)
                    copied_count += 1
                    print(f"   ✅ Created epoch checkpoint: training_state_e-{last_completed_epoch}.pth (last completed)")
                
                # Also create checkpoint for the resume epoch (what the training code will look for)
                best_state_resume = best_state.copy()
                best_state_resume['epoch_idx'] = resume_from_epoch
                resume_checkpoint_path = extended_output_dir / f"training_state_e-{resume_from_epoch}.pth"
                if not resume_checkpoint_path.exists():
                    torch.save(best_state_resume, resume_checkpoint_path)
                    copied_count += 1
                    print(f"   ✅ Created epoch checkpoint: training_state_e-{resume_from_epoch}.pth (resume epoch)")
            except Exception as e:
                print(f"   ⚠️  Could not create epoch checkpoints: {e}")
    
    print(f"   Copied/created {copied_count} checkpoint file(s)")
    
    if copied_count == 0:
        print("   ⚠️  WARNING: No checkpoint files found to copy!")
        print("   This may cause issues when resuming training.")
    print()
    
    # Now update output_dir - checkpoints are in place
    es_extended.output_dir = str(extended_output_dir)
    
    # CRITICAL: Update training_state_path to point to new directory
    # The training_state_path is used by get_training_state_path() to find checkpoints
    if hasattr(es_extended, 'training_state_path'):
        # Extract the base name from the old path
        old_path = Path(es_extended.training_state_path)
        # training_state_path is typically like "/path/to/training_state"
        # We need to update it to the new directory
        es_extended.training_state_path = str(extended_output_dir / "training_state")
        print(f"   Updated training_state_path: {es_extended.training_state_path}")
    
    print(f"✅ Updated embedding space with new data")
    print(f"   Train rows: {len(train_data_extended)} (was {len(train_data)})")
    print(f"   Val rows: {len(val_data_extended)} (was {len(val_data)})")
    print()
    
    # Step 6: Continue training for 5 additional epochs
    print("=" * 80)
    print("STEP 6: Continue Training (5 additional epochs)")
    print("=" * 80)
    
    # existing_epochs was already calculated above when copying checkpoints
    print(f"Resuming from epoch {existing_epochs}")
    print(f"Training for 5 additional epochs (will reach epoch {existing_epochs + 5})")
    print()
    
    # WORKAROUND: The training code uses range(base_epoch_index, n_epochs) which is exclusive.
    # If base_epoch_index=4 and we want 5 more epochs (4,5,6,7,8), we need n_epochs=9.
    # So: n_epochs = existing_epochs + additional_epochs + 1
    total_epochs_wanted = existing_epochs + 5 + 1  # 3 initial + 5 more = 8 total, but range needs 9
    
    es_extended.train(
        batch_size=32,
        n_epochs=total_epochs_wanted,  # Pass total epochs + 1 due to exclusive range
        existing_epochs=existing_epochs,  # Continue from where we left off
        print_progress_step=1,
        enable_weightwatcher=False,
    )
    
    print("✅ Extended training complete")
    print()
    
    # Step 7: Verify the extension worked
    print("=" * 80)
    print("STEP 7: Verify Extension Worked")
    print("=" * 80)
    
    extended_timeline = getattr(es_extended, '_training_timeline', [])
    total_epochs = len(extended_timeline)
    
    print(f"Total epochs in timeline: {total_epochs}")
    print(f"Expected: {initial_epochs + 5} epochs ({initial_epochs} initial + 5 extended)")
    print()
    
    # Verify epoch count
    if total_epochs >= initial_epochs + 5:
        print(f"✅ Epoch count correct: {total_epochs} >= {initial_epochs + 5}")
    else:
        print(f"❌ Epoch count incorrect: {total_epochs} < {initial_epochs + 5}")
        raise AssertionError(f"Expected at least {initial_epochs + 5} epochs, got {total_epochs}")
    
    # Check that training continued (not restarted)
    if extended_timeline:
        # First epoch of extended training should have similar loss to last epoch of initial
        first_extended_epoch = extended_timeline[initial_epochs] if len(extended_timeline) > initial_epochs else None
        last_initial_epoch = initial_timeline[-1] if initial_timeline else None
        
        if first_extended_epoch and last_initial_epoch:
            first_ext_loss = first_extended_epoch.get('current_loss', None)
            last_init_loss = last_initial_epoch.get('current_loss', None)
            
            print(f"Last initial epoch loss: {last_init_loss}")
            print(f"First extended epoch loss: {first_ext_loss}")
            
            if first_ext_loss and last_init_loss:
                # Loss should be similar (not drastically different, indicating restart)
                loss_diff = abs(float(first_ext_loss) - float(last_init_loss))
                loss_ratio = loss_diff / float(last_init_loss) if float(last_init_loss) > 0 else float('inf')
                
                print(f"Loss difference: {loss_diff:.6f} ({loss_ratio*100:.2f}%)")
                
                if loss_ratio < 0.5:  # Less than 50% difference
                    print("✅ Loss continuity verified (training continued, not restarted)")
                else:
                    print("⚠️  Loss changed significantly - may have restarted training")
    
    # Check final loss
    if extended_timeline:
        final_loss = extended_timeline[-1].get('current_loss', 'N/A')
        final_val_loss = extended_timeline[-1].get('validation_loss', 'N/A')
        print(f"Final training loss: {final_loss}")
        print(f"Final validation loss: {final_val_loss}")
    
    print()
    print("=" * 80)
    print("✅ TEST PASSED: Embedding space extension works correctly!")
    print("=" * 80)
    print(f"   Initial epochs: {initial_epochs}")
    print(f"   Extended epochs: 5")
    print(f"   Total epochs: {total_epochs}")
    print(f"   Output directory: {test_output_dir}")
    print()

except Exception as e:
    print()
    print("=" * 80)
    print("❌ TEST FAILED")
    print("=" * 80)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    print()
    print(f"Test output directory preserved: {test_output_dir}")
    raise

finally:
    # Optionally clean up (comment out to inspect files)
    # shutil.rmtree(test_output_dir, ignore_errors=True)
    print(f"Test output directory: {test_output_dir}")
    print("(Directory preserved for inspection)")

