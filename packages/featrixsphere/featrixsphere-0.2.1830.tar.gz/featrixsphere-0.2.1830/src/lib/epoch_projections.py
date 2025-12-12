#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

import json
import logging
import os
import time
import traceback
from datetime import datetime
from pathlib import Path

import pandas as pd
import torch
import numpy as np

logger = logging.getLogger(__name__)

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

def generate_epoch_projections(embedding_space, df, epoch_idx, max_samples=500, output_dir="epoch_projections", consistent_sample_indices=None):
    """
    Generate lightweight 3D projections for a specific epoch during training.
    
    This is optimized for speed and called during training:
    - Only uses short (3D) embeddings 
    - No expensive clustering
    - Uses CONSISTENT sampling across epochs for point tracking
    - Saves to numbered files for movie creation
    
    Args:
        embedding_space: Trained EmbeddingSpace object
        df: DataFrame with training data (must include __featrix_row_id)
        epoch_idx: Current epoch number
        max_samples: Maximum number of samples to project (default: 500)
        output_dir: Directory to save projection files
        consistent_sample_indices: Pre-selected row indices to use (for consistency across epochs)
        
    Returns:
        str: Path to the saved projection file
    """
    
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Use consistent sampling - same points for every epoch!
        if consistent_sample_indices is not None:
            # Use pre-selected indices for consistency across epochs
            df_sample = df.iloc[consistent_sample_indices].copy()
            logger.info(f"Epoch {epoch_idx}: Using consistent sample of {len(df_sample)} points")
        elif len(df) > max_samples:
            # First time - create consistent sample and save indices
            df_sample = df.sample(max_samples, random_state=42).reset_index(drop=True)
            logger.info(f"Epoch {epoch_idx}: Created consistent sample {len(df)} → {max_samples} records")
        else:
            df_sample = df.copy()
            
        # Generate 3D coordinates using short embeddings only
        coords_3d = []
        rowids = []
        row_offsets = []
        set_columns_matrix = []
        scalar_columns_matrix = []
        string_columns_matrix = []
        
        # Get column info from embedding space
        set_columns_names_and_values = embedding_space.get_set_columns()
        scalar_columns_names_and_codecs = embedding_space.get_scalar_columns()  
        string_columns_names = embedding_space.get_string_column_names()
        
        start_time = datetime.utcnow()
        
        # Encode records using short embeddings only (much faster!)
        for idx, row in df_sample.iterrows():
            try:
                rowids.append(row['__featrix_row_id'])
                row_offsets.append(idx)
                
                # Only get short embedding (3D) - this is the key optimization!
                embedding_short = embedding_space.encode_record(row, short=True, output_device=torch.device("cpu"))
                
                # Convert to 3D coordinates
                coords_3d.append([
                    embedding_short[0].item(), 
                    embedding_short[1].item(), 
                    embedding_short[2].item()
                ])
                
                # Extract column data for metadata (same as original)
                orig_set_data = {}
                orig_scalar_data = {}
                orig_string_data = {}
                
                for k, v in row.items():
                    if k in set_columns_names_and_values:
                        orig_set_data[k] = v
                    elif k in scalar_columns_names_and_codecs:
                        orig_scalar_data[k] = v
                    elif k in string_columns_names:
                        orig_string_data[k] = v
                        
                set_columns_matrix.append(orig_set_data)
                scalar_columns_matrix.append(orig_scalar_data)
                string_columns_matrix.append(orig_string_data)
                
            except Exception as e:
                logger.warning(f"Failed to encode record {idx} in epoch {epoch_idx}: {e}")
                continue
                
        duration = (datetime.utcnow() - start_time).total_seconds()
        logger.info(f"Epoch {epoch_idx}: Encoded {len(coords_3d)} records in {duration:.2f}s")
        
        # Create DataFrame with projection data
        projection_df = pd.DataFrame(coords_3d, columns=['0', '1', '2'])
        projection_df['__featrix_row_id'] = rowids
        projection_df['__featrix_row_offset'] = row_offsets
        projection_df['set_columns'] = set_columns_matrix
        projection_df['scalar_columns'] = scalar_columns_matrix
        projection_df['string_columns'] = string_columns_matrix
        
        # Add dummy cluster info (no clustering for speed)
        projection_df['cluster_pre'] = 0  # Single cluster for all points
        
        # Rename columns for consistency with full projections
        projection_df = projection_df.rename(columns={"0": "x", "1": "y", "2": "z"})
        
        # Create projection data structure
        projection_data = {
            'coords': json.loads(projection_df.to_json(orient='records')),
            'epoch': epoch_idx,
            'timestamp': datetime.utcnow().isoformat(),
            'sample_size': len(coords_3d),
            'total_records': len(df),
            'encoding_duration_seconds': duration,
            'cluster_messages': {},  # No clustering messages for epoch projections
            'is_epoch_projection': True,  # Flag to distinguish from full projections
            'entire_cluster_results': {},  # No clustering results
            'consistent_sampling': consistent_sample_indices is not None,  # Track if using consistent sampling
            'row_ids_for_tracking': rowids  # Explicit list of row IDs for movie tracking
        }
        
        # Save to numbered file for movie creation
        output_file = Path(output_dir) / f"projections_epoch_{epoch_idx:03d}.json"
        
        with open(output_file, "w") as fp:
            json.dump(projection_data, fp, cls=NumpyEncoder, indent=2)
            
        logger.info(f"Epoch {epoch_idx}: Saved projections to {output_file}")
        return str(output_file)
        
    except Exception as e:
        logger.error(f"Failed to generate epoch projections for epoch {epoch_idx}: {e}")
        traceback.print_exc()
        return None

class EpochProjectionCallback:
    """
    Callback class to generate projections at the end of each epoch during training.
    Uses CONSISTENT sampling across epochs for proper point tracking in movies.
    
    ⚠️  IMPORTANT: important_columns parameter is ONLY for visualization sampling
    and has NO EFFECT on model training - only affects which rows are prioritized
    in epoch projection visualizations.
    """
    
    def __init__(self, df, output_dir="epoch_projections", max_samples=500, save_every=1, important_columns=None, original_df=None):
        """
        Initialize epoch projection callback with consistent sampling.
        
        Args:
            df: Training DataFrame (encoded/enriched - must include __featrix_row_id)
            output_dir: Directory to save projection files
            max_samples: Maximum samples to project per epoch (default: 500)
            save_every: Save projections every N epochs (default: 1 = every epoch)
            important_columns: VISUALIZATION ONLY - List of column names to prefer (rows with 
                              non-null values in these columns are prioritized for sampling)
                              ⚠️  Has NO EFFECT on model training, only affects visualization
            original_df: ORIGINAL DataFrame with original column names (before encoding) for 
                        matching important_columns. If not provided, will try to match against df.
        """
        self.df = df
        self.output_dir = output_dir
        self.max_samples = max_samples
        self.save_every = save_every
        self.last_epoch_saved = -1
        self.important_columns = important_columns or []
        self.original_df = original_df
        
        # 🔍 DEBUGGING: Log what we received
        logger.info(f"🔍 EpochProjectionCallback INITIALIZATION DEBUG:")
        logger.info(f"   Encoded DataFrame shape: {df.shape}")
        logger.info(f"   Encoded DataFrame columns ({len(df.columns)} total): {list(df.columns)[:20]}{'...' if len(df.columns) > 20 else ''}")
        if original_df is not None:
            logger.info(f"   Original DataFrame shape: {original_df.shape}")
            logger.info(f"   Original DataFrame columns ({len(original_df.columns)} total): {list(original_df.columns)[:20]}{'...' if len(original_df.columns) > 20 else ''}")
        else:
            logger.warning(f"   ⚠️  NO ORIGINAL DATAFRAME PROVIDED - will try to match important columns against encoded dataframe")
        logger.info(f"   Important columns requested ({len(self.important_columns)} total): {self.important_columns[:10]}{'...' if len(self.important_columns) > 10 else ''}")
        
        # CRITICAL: Create consistent sample indices for all epochs
        if len(df) > max_samples:
            # Smart sampling: prefer rows with non-null values in important columns
            if self.important_columns:
                logger.info(f"🔍 CHECKING COLUMN MATCHING:")
                
                # Use original_df if provided, otherwise fall back to encoded df
                lookup_df = original_df if original_df is not None else df
                logger.info(f"   Using {'ORIGINAL' if original_df is not None else 'ENCODED'} dataframe for column matching")
                
                # Filter to columns that actually exist in the lookup dataframe
                existing_important_cols = [col for col in self.important_columns if col in lookup_df.columns]
                missing_important_cols = [col for col in self.important_columns if col not in lookup_df.columns]
                
                logger.info(f"   ✅ FOUND {len(existing_important_cols)} matching columns: {existing_important_cols[:10]}{'...' if len(existing_important_cols) > 10 else ''}")
                if missing_important_cols:
                    logger.warning(f"   ❌ MISSING {len(missing_important_cols)} columns from dataframe: {missing_important_cols[:10]}{'...' if len(missing_important_cols) > 10 else ''}")
                
                if existing_important_cols:
                    logger.info(f"⚠️  VISUALIZATION ONLY: Preferring rows with non-null values in {len(existing_important_cols)} columns")
                    logger.info(f"   Important columns: {', '.join(existing_important_cols[:5])}{'...' if len(existing_important_cols) > 5 else ''}")
                    
                    # Score rows by how many important columns have non-null values
                    lookup_df_copy = lookup_df.copy()
                    lookup_df_copy['_importance_score'] = lookup_df_copy[existing_important_cols].notna().sum(axis=1)
                    
                    logger.info(f"📊 IMPORTANCE SCORE DISTRIBUTION:")
                    logger.info(f"   Min score: {lookup_df_copy['_importance_score'].min()}")
                    logger.info(f"   Max score: {lookup_df_copy['_importance_score'].max()}")
                    logger.info(f"   Mean score: {lookup_df_copy['_importance_score'].mean():.2f}")
                    logger.info(f"   Rows with score > 0: {(lookup_df_copy['_importance_score'] > 0).sum()} / {len(lookup_df_copy)}")
                    
                    # Sample preferentially from rows with more non-null important columns
                    # Use a weighted sample based on importance score
                    # Add 1 to avoid zero weights
                    weights = lookup_df_copy['_importance_score'] + 1
                    sample_df = lookup_df_copy.sample(max_samples, random_state=42, weights=weights)
                    
                    # Get the indices from the sample
                    self.consistent_sample_indices = sample_df.index.tolist()
                    
                    logger.info(f"✅ Created smart sample of {max_samples} points from {len(df)} total")
                    logger.info(f"   Average importance score in sample: {sample_df['_importance_score'].mean():.2f}/{len(existing_important_cols)}")
                    logger.info(f"   Rows in sample with ALL important columns: {(sample_df['_importance_score'] == len(existing_important_cols)).sum()}")
                    logger.info(f"   Rows in sample with NO important columns: {(sample_df['_importance_score'] == 0).sum()}")
                else:
                    logger.warning(f"⚠️  None of the {len(self.important_columns)} important columns exist in dataframe - using random sampling")
                    logger.warning(f"🔍 COLUMN MISMATCH DEBUG:")
                    logger.warning(f"   Requested columns: {self.important_columns[:5]}...")
                    logger.warning(f"   Available columns in lookup df: {list(lookup_df.columns)[:10]}...")
                    sample_df = df.sample(max_samples, random_state=42)
                    self.consistent_sample_indices = sample_df.index.tolist()
            else:
                # No important columns specified - use random sampling
                logger.info(f"ℹ️  No important columns specified - using random sampling")
                sample_df = df.sample(max_samples, random_state=42)
                self.consistent_sample_indices = sample_df.index.tolist()
                logger.info(f"EpochProjectionCallback: Created consistent sample of {max_samples} points from {len(df)} total")
            
            logger.info(f"  Sample row IDs: {sample_df['__featrix_row_id'].tolist()[:10]}..." if len(sample_df) > 10 else f"  Sample row IDs: {sample_df['__featrix_row_id'].tolist()}")
        else:
            # Use all data if under the limit
            self.consistent_sample_indices = None
            logger.info(f"EpochProjectionCallback: Using all {len(df)} points (under {max_samples} limit)")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"🎬 EpochProjectionCallback initialized: saving every {save_every} epoch(s) to {output_dir}")
        
    def __call__(self, training_event_dict):
        """
        Called during training with progress information.
        Detects epoch completion and generates projections using consistent sampling.
        """
        try:
            # Extract epoch info from training event
            epoch_idx = training_event_dict.get('epoch_idx', -1)
            progress_counter = training_event_dict.get('progress_counter', 0)
            max_progress = training_event_dict.get('max_progress', 1)
            
            # Improved epoch completion detection
            # We check if this is a new epoch we haven't processed yet
            # and if we have access to the embedding space
            if (epoch_idx > self.last_epoch_saved and 
                epoch_idx % self.save_every == 0 and
                epoch_idx >= 0 and  # Valid epoch number
                'embedding_space' in training_event_dict):
                
                logger.info(f"🎬 Generating consistent projections for epoch {epoch_idx}...")
                
                embedding_space = training_event_dict['embedding_space']
                output_file = generate_epoch_projections(
                    embedding_space=embedding_space,
                    df=self.df,
                    epoch_idx=epoch_idx,
                    max_samples=self.max_samples,
                    output_dir=self.output_dir,
                    consistent_sample_indices=self.consistent_sample_indices  # PASS CONSISTENT INDICES
                )
                
                if output_file:
                    self.last_epoch_saved = epoch_idx
                    logger.info(f"✅ Epoch {epoch_idx} consistent projections saved to {output_file}")
                else:
                    logger.warning(f"❌ Failed to save projections for epoch {epoch_idx}")
                    
        except Exception as e:
            logger.error(f"Error in EpochProjectionCallback: {e}")
            traceback.print_exc()

def create_projection_movie_metadata(output_dir="epoch_projections"):
    """
    Create metadata file listing all epoch projection files for movie creation.
    
    Args:
        output_dir: Directory containing epoch projection files
        
    Returns:
        dict: Metadata about available projection files
    """
    
    projection_files = []
    output_path = Path(output_dir)
    
    if output_path.exists():
        # Find all epoch projection files
        for file_path in sorted(output_path.glob("projections_epoch_*.json")):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                projection_files.append({
                    'file': str(file_path),
                    'epoch': data.get('epoch', -1),
                    'timestamp': data.get('timestamp'),
                    'sample_size': data.get('sample_size', 0),
                    'duration': data.get('encoding_duration_seconds', 0)
                })
            except Exception as e:
                logger.warning(f"Could not read projection file {file_path}: {e}")
                
    metadata = {
        'total_epochs': len(projection_files),
        'output_directory': str(output_path),
        'projection_files': projection_files,
        'created_at': datetime.utcnow().isoformat(),
        'movie_ready': len(projection_files) > 1
    }
    
    # Ensure output directory exists before writing metadata
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save metadata file
    metadata_file = output_path / "movie_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
        
    logger.info(f"Created movie metadata with {len(projection_files)} epoch files: {metadata_file}")
    return metadata 