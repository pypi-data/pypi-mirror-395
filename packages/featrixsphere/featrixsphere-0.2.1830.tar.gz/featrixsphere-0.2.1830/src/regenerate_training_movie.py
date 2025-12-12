#!/usr/bin/env python3
"""
Regenerate Training Movie Tool

Regenerates epoch projection files and training movie metadata after training has completed.
Useful for creating movies with different visualization preferences without re-training.

Usage:
    python regenerate_training_movie.py --job-dir /path/to/train_es_job --important-columns customer_name revenue
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
import pickle
import shutil

# Add lib paths for imports
lib_path = Path(__file__).parent / "lib"
if str(lib_path) not in sys.path:
    sys.path.insert(0, str(lib_path))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def load_embedding_space(job_dir):
    """Load the trained embedding space from job directory."""
    es_pickle = Path(job_dir) / "embedded_space.pickle"
    
    if not es_pickle.exists():
        raise FileNotFoundError(f"Embedding space not found: {es_pickle}")
    
    logger.info(f"📦 Loading embedding space from {es_pickle}")
    with open(es_pickle, 'rb') as f:
        es = pickle.load(f)
    
    logger.info(f"✅ Embedding space loaded")
    return es


def load_training_data(job_dir):
    """Load the training data (SQLite DB or CSV)."""
    # First try SQLite database (preferred)
    sqlite_db = Path(job_dir) / "final_data.db"
    if sqlite_db.exists():
        logger.info(f"📊 Loading training data from SQLite: {sqlite_db}")
        import pandas as pd
        import sqlite3
        
        conn = sqlite3.connect(sqlite_db)
        df = pd.read_sql_query("SELECT * FROM data", conn)
        conn.close()
        logger.info(f"✅ Loaded {len(df)} rows from SQLite")
        return df
    
    # Fall back to CSV
    csv_files = list(Path(job_dir).glob("*.csv"))
    if csv_files:
        csv_file = csv_files[0]
        logger.info(f"📊 Loading training data from CSV: {csv_file}")
        import pandas as pd
        df = pd.read_csv(csv_file)
        logger.info(f"✅ Loaded {len(df)} rows from CSV")
        return df
    
    raise FileNotFoundError(f"No training data found in {job_dir}")


def regenerate_projections(es, df, output_dir, max_samples=500, important_columns=None, save_every=1):
    """
    Regenerate epoch projection files using the trained model.
    
    Since we don't have checkpoints for every epoch, we'll generate projections
    using the final trained model. This shows where the data ended up after training.
    
    Args:
        es: Trained EmbeddingSpace
        df: Training DataFrame
        output_dir: Directory to save projections
        max_samples: Max samples to project
        important_columns: Columns to prioritize for sampling
        save_every: Generate projection for every N epochs (simulated)
    """
    from epoch_projections import EpochProjectionCallback, generate_epoch_projections
    
    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"🎬 Regenerating epoch projections")
    logger.info(f"   Output directory: {output_dir}")
    logger.info(f"   Max samples: {max_samples}")
    logger.info(f"   Important columns: {important_columns or 'None'}")
    logger.info(f"   Save every: {save_every} epoch(s)")
    
    # Add row IDs if missing
    if '__featrix_row_id' not in df.columns:
        df['__featrix_row_id'] = df.index
    
    # Initialize callback for consistent sampling
    callback = EpochProjectionCallback(
        df=df,
        output_dir=str(output_dir),
        max_samples=max_samples,
        save_every=save_every,
        important_columns=important_columns
    )
    
    # Get total epochs from training info
    total_epochs = es.training_info.get('n_epochs', 100)
    logger.info(f"📊 Model was trained for {total_epochs} epochs")
    
    # Generate projections for epochs that should have been saved
    epochs_to_generate = range(save_every, total_epochs + 1, save_every)
    logger.info(f"🎬 Generating {len(list(epochs_to_generate))} projection files")
    
    for epoch_idx in epochs_to_generate:
        logger.info(f"📸 Generating projections for epoch {epoch_idx}/{total_epochs}")
        
        output_file = generate_epoch_projections(
            embedding_space=es,
            df=df,
            epoch_idx=epoch_idx,
            max_samples=max_samples,
            output_dir=str(output_dir),
            consistent_sample_indices=callback.consistent_sample_indices
        )
        
        if output_file:
            logger.info(f"✅ Saved: {output_file}")
        else:
            logger.warning(f"❌ Failed to generate epoch {epoch_idx}")
    
    logger.info(f"🎉 Regeneration complete!")
    return output_dir


def create_movie_metadata(output_dir):
    """Create training movie metadata JSON."""
    from epoch_projections import create_projection_movie_metadata
    
    logger.info(f"🎬 Creating movie metadata")
    metadata_file = create_projection_movie_metadata(output_dir=str(output_dir))
    
    if metadata_file:
        logger.info(f"✅ Movie metadata created: {metadata_file}")
    else:
        logger.warning(f"❌ Failed to create movie metadata")
    
    return metadata_file


def main():
    parser = argparse.ArgumentParser(
        description="Regenerate training movie projections with different visualization preferences"
    )
    parser.add_argument(
        "--job-dir",
        required=True,
        help="Path to training job directory (contains embedded_space.pickle)"
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for projections (default: job_dir/epoch_projections_regenerated)"
    )
    parser.add_argument(
        "--important-columns",
        nargs="+",
        default=None,
        help="Column names to prioritize in visualization (space-separated)"
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=500,
        help="Maximum number of samples to project (default: 500)"
    )
    parser.add_argument(
        "--save-every",
        type=int,
        default=1,
        help="Generate projection for every N epochs (default: 1 = every epoch)"
    )
    parser.add_argument(
        "--backup-original",
        action="store_true",
        help="Backup original epoch_projections directory before regenerating"
    )
    
    args = parser.parse_args()
    
    # Validate job directory
    job_dir = Path(args.job_dir)
    if not job_dir.exists():
        logger.error(f"❌ Job directory not found: {job_dir}")
        return 1
    
    # Set output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = job_dir / "epoch_projections_regenerated"
    
    # Backup original if requested
    if args.backup_original:
        original_dir = job_dir / "epoch_projections"
        if original_dir.exists():
            backup_dir = job_dir / "epoch_projections_backup"
            logger.info(f"💾 Backing up original projections to {backup_dir}")
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            shutil.copytree(original_dir, backup_dir)
            logger.info(f"✅ Backup complete")
    
    try:
        # Load embedding space
        es = load_embedding_space(job_dir)
        
        # Load training data
        df = load_training_data(job_dir)
        
        # Regenerate projections
        regenerate_projections(
            es=es,
            df=df,
            output_dir=output_dir,
            max_samples=args.max_samples,
            important_columns=args.important_columns,
            save_every=args.save_every
        )
        
        # Create movie metadata
        create_movie_metadata(output_dir)
        
        logger.info(f"")
        logger.info(f"{'='*80}")
        logger.info(f"✅ SUCCESS: Training movie regenerated!")
        logger.info(f"{'='*80}")
        logger.info(f"📁 Output directory: {output_dir}")
        logger.info(f"🎬 Movie metadata: {output_dir}/movie_metadata.json")
        logger.info(f"")
        logger.info(f"Next steps:")
        logger.info(f"  1. View projections in output directory")
        logger.info(f"  2. Use movie_metadata.json to create visualization")
        logger.info(f"  3. Compare with original projections if needed")
        logger.info(f"{'='*80}")
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())

