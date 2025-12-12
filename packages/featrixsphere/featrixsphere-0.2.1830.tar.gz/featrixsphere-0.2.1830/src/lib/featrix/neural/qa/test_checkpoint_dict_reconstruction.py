#!/usr/bin/env python3
"""
Local QA test for checkpoint dict reconstruction in load_embedded_space.
Tests the code path where embedded_space.pickle contains a dict (checkpoint) instead of a full EmbeddingSpace.
Runs entirely locally on CPU - no jobs, no API, no bullshit.
"""
import sys
import os
import pickle
import tempfile
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
from featrix.neural.device import set_device_cpu
from featrix.neural.io_utils import load_embedded_space
from lib.session_manager import save_session, load_session
from lib.session_manager import create_session
from config import config

print("=" * 80)
print("CHECKPOINT DICT RECONSTRUCTION QA TEST")
print("=" * 80)
print("Testing load_embedded_space with checkpoint dict (not full EmbeddingSpace)")
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

# Train embedding space (just a few epochs for speed)
print("=" * 80)
print("STEP 1: TRAINING EMBEDDING SPACE (5 EPOCHS - JUST FOR TESTING)")
print("=" * 80)
print()

with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)
    es_output_dir = tmp_path / "test_es"
    es_output_dir.mkdir()
    
    es = EmbeddingSpace(
        train_data,
        val_data,
        n_epochs=5,
        d_model=64,  # Small for speed
        output_debug_label="checkpoint_reconstruction_qa",
        output_dir=str(es_output_dir)
    )
    
    print("🚀 Starting ES training...")
    es.train(batch_size=128, n_epochs=5)
    print("✅ ES training complete")
    print()
    
    # Find the embedded_space.pickle file
    embedded_space_files = list(es_output_dir.rglob("embedded_space.pickle"))
    if not embedded_space_files:
        print(f"❌ No embedded_space.pickle found in {es_output_dir}")
        sys.exit(1)
    
    embedded_space_path = embedded_space_files[0]
    print(f"📁 Found embedded_space.pickle at: {embedded_space_path}")
    print()
    
    # Create a session for reconstruction
    session_id = "test-checkpoint-reconstruction-qa"
    print(f"📋 Creating test session: {session_id}")
    
    # Create session with all necessary info
    session = {
        'session_id': session_id,
        'status': 'RUNNING',
        'input_data': str(data_file),
        'sqlite_db': None,  # We'll use input_data instead
        'n_epochs': 5,
        'd_model': 64,
        'column_overrides': {},
        'strings_cache': None,
        'json_transformations': {},
        'version_info': None,
        'name': 'test-checkpoint-reconstruction',
        'required_child_es_mapping': {},
        'user_metadata': None,
    }
    
    # Save session
    save_session(session_id, session, exist_ok=True)
    print(f"✅ Session saved")
    print()
    
    # Now create a checkpoint dict version of the pickle
    print("=" * 80)
    print("STEP 2: CREATING CHECKPOINT DICT VERSION")
    print("=" * 80)
    print()
    
    # Load the actual EmbeddingSpace
    with open(embedded_space_path, 'rb') as f:
        actual_es = pickle.load(f)
    
    print(f"✅ Loaded actual EmbeddingSpace from {embedded_space_path}")
    print(f"   Type: {type(actual_es)}")
    print()
    
    # Create a checkpoint dict (simulating what happens when we save just the model)
    checkpoint_dict = {
        'model': actual_es.encoder,  # Just the encoder
        'epoch_idx': 5,
        'other_data': 'test'
    }
    
    # Save checkpoint dict to a new file
    checkpoint_path = embedded_space_path.parent / "embedded_space_checkpoint.pickle"
    with open(checkpoint_path, 'wb') as f:
        pickle.dump(checkpoint_dict, f)
    
    print(f"✅ Created checkpoint dict at: {checkpoint_path}")
    print(f"   Dict keys: {list(checkpoint_dict.keys())}")
    print()
    
    # Update session to point to the checkpoint path structure
    # The path needs to match the pattern: .../featrix_output/{session_id}/train_es/.../embedded_space.pickle
    # So we need to create that structure
    featrix_output = Path(config.output_dir) if hasattr(config, 'output_dir') else Path("/tmp/featrix_output")
    featrix_output.mkdir(parents=True, exist_ok=True)
    
    session_output_dir = featrix_output / session_id / "train_es" / "test-job-id"
    session_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy checkpoint to the session structure
    checkpoint_in_session = session_output_dir / "embedded_space.pickle"
    import shutil
    shutil.copy(checkpoint_path, checkpoint_in_session)
    
    print(f"✅ Copied checkpoint to session structure: {checkpoint_in_session}")
    print()
    
    # Now test load_embedded_space with the checkpoint dict
    print("=" * 80)
    print("STEP 3: TESTING load_embedded_space WITH CHECKPOINT DICT")
    print("=" * 80)
    print()
    
    try:
        print(f"🔍 Calling load_embedded_space({checkpoint_in_session})...")
        reconstructed_es = load_embedded_space(str(checkpoint_in_session))
        print(f"✅ load_embedded_space returned: {type(reconstructed_es)}")
        
        # Verify it's an EmbeddingSpace
        if not isinstance(reconstructed_es, EmbeddingSpace):
            print(f"❌ FAILED: Expected EmbeddingSpace, got {type(reconstructed_es)}")
            sys.exit(1)
        
        print(f"✅ Successfully reconstructed EmbeddingSpace from checkpoint dict!")
        print(f"   Has encoder: {hasattr(reconstructed_es, 'encoder') and reconstructed_es.encoder is not None}")
        print(f"   Encoder type: {type(reconstructed_es.encoder) if hasattr(reconstructed_es, 'encoder') else 'N/A'}")
        
        if hasattr(reconstructed_es, 'training_info') and reconstructed_es.training_info:
            print(f"   Training info: {reconstructed_es.training_info}")
        
        print()
        print("=" * 80)
        print("✅ QA TEST PASSED - Checkpoint dict reconstruction working!")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ FAILED: Exception during load_embedded_space")
        print(f"   Exception type: {type(e).__name__}")
        print(f"   Exception message: {e}")
        import traceback
        print(f"   Full traceback:\n{traceback.format_exc()}")
        sys.exit(1)

