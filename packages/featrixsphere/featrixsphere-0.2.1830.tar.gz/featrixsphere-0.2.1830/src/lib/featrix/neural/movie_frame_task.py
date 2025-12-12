#!/usr/bin/env python3
"""
Async movie frame generation task - runs on CPU worker queue.

This module generates movie frames (3D projections) asynchronously on CPU
so training never blocks. Frames are generated every epoch.
"""

import json
import logging
import os
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import torch
import numpy as np

logger = logging.getLogger(__name__)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def generate_movie_frame_on_cpu(
    checkpoint_path: str,
    data_snapshot_path: str,
    epoch: int,
    output_dir: str,
    session_id: str
) -> Optional[str]:
    """
    Generate a single movie frame on CPU from a model checkpoint.
    
    Args:
        checkpoint_path: Path to model checkpoint (.pt file)
        data_snapshot_path: Path to saved data sample (.json)
        epoch: Epoch number
        output_dir: Where to save the projection
        session_id: Session ID for logging
    
    Returns:
        Path to saved projection file, or None if failed
    """
    
    start_time = time.time()
    
    try:
        logger.info(f"🎬 [Session {session_id}] Generating movie frame for epoch {epoch} on CPU...")
        
        # Load checkpoint on CPU
        logger.info(f"   Loading checkpoint from {checkpoint_path}")
        checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
        
        # Extract embedding_space from checkpoint
        embedding_space = checkpoint.get("embedding_space")
        
        # If checkpoint has lightweight format (encoder + codecs), reconstruct minimal embedding_space
        if embedding_space is None:
            encoder = checkpoint.get("encoder")
            if encoder is None:
                raise ValueError("Checkpoint must contain 'embedding_space' or 'encoder'")
            
            # Create a minimal embedding_space wrapper for encoding
            # This doesn't include huge dataframes, just what's needed for encode_record()
            from featrix.neural.embedded_space import EmbeddingSpace
            from featrix.neural.input_data_set import FeatrixInputDataSet
            
            # Create dummy input data (empty, we don't need the actual dataframes)
            dummy_train = FeatrixInputDataSet(pd.DataFrame(), {})
            dummy_val = FeatrixInputDataSet(pd.DataFrame(), {})
            
            # Reconstruct embedding_space with saved components
            embedding_space = EmbeddingSpace(
                train_input_data=dummy_train,
                val_input_data=dummy_val,
                encoder_config=checkpoint.get('encoder_config'),
                d_model=checkpoint.get('d_model')
            )
            # Restore the encoder and codecs
            embedding_space.encoder = encoder
            embedding_space.col_codecs = checkpoint.get('col_codecs', {})
            embedding_space.col_order = checkpoint.get('col_order', [])
            embedding_space.column_spec = checkpoint.get('column_spec', {})
            embedding_space.json_transformations = checkpoint.get('json_transformations', {})
            embedding_space.required_child_es_mapping = checkpoint.get('required_child_es_mapping', {})
        
        # Move everything to CPU and eval mode
        embedding_space.encoder.cpu()
        embedding_space.encoder.eval()
        
        logger.info(f"   ✅ Model loaded on CPU")
        
        # Load data snapshot
        logger.info(f"   Loading data snapshot from {data_snapshot_path}")
        with open(data_snapshot_path, 'r') as f:
            data_snapshot = json.load(f)
        
        # Load the DataFrame from snapshot
        df = pd.DataFrame(data_snapshot['records'])
        sample_indices = data_snapshot.get('sample_indices')
        
        logger.info(f"   Processing {len(df)} records on CPU...")
        
        # Generate 3D embeddings on CPU using short embeddings
        coords_3d = []
        rowids = []
        row_offsets = []
        set_columns_matrix = []
        scalar_columns_matrix = []
        string_columns_matrix = []
        
        # Get column info from embedding space
        set_columns_names = embedding_space.get_set_columns() if hasattr(embedding_space, 'get_set_columns') else {}
        scalar_columns_names = embedding_space.get_scalar_columns() if hasattr(embedding_space, 'get_scalar_columns') else {}
        string_columns_names = embedding_space.get_string_column_names() if hasattr(embedding_space, 'get_string_column_names') else []
        
        for idx, row in df.iterrows():
            try:
                rowids.append(row.get('__featrix_row_id', idx))
                row_offsets.append(idx)
                
                # Encode on CPU using short (3D) embedding
                with torch.no_grad():
                    embedding_short = embedding_space.encode_record(row, short=True, output_device=torch.device("cpu"))
                
                # Convert to 3D coordinates
                coords_3d.append([
                    embedding_short[0].item(),
                    embedding_short[1].item(),
                    embedding_short[2].item()
                ])
                
                # Extract column data for metadata
                orig_set_data = {}
                orig_scalar_data = {}
                orig_string_data = {}
                
                for k, v in row.items():
                    if k in set_columns_names:
                        orig_set_data[k] = v
                    elif k in scalar_columns_names:
                        orig_scalar_data[k] = v
                    elif k in string_columns_names:
                        orig_string_data[k] = v
                
                set_columns_matrix.append(orig_set_data)
                scalar_columns_matrix.append(orig_scalar_data)
                string_columns_matrix.append(orig_string_data)
                
            except Exception as e:
                logger.warning(f"Failed to encode record {idx} in epoch {epoch}: {e}")
                continue
        
        # Create projection DataFrame
        projection_df = pd.DataFrame(coords_3d, columns=['0', '1', '2'])
        projection_df['__featrix_row_id'] = rowids
        projection_df['__featrix_row_offset'] = row_offsets
        projection_df['set_columns'] = set_columns_matrix
        projection_df['scalar_columns'] = scalar_columns_matrix
        projection_df['string_columns'] = string_columns_matrix
        projection_df['cluster_pre'] = 0  # No clustering
        projection_df = projection_df.rename(columns={"0": "x", "1": "y", "2": "z"})
        
        # Create projection data
        duration = time.time() - start_time
        projection_data = {
            'coords': json.loads(projection_df.to_json(orient='records')),
            'epoch': epoch,
            'timestamp': datetime.utcnow().isoformat(),
            'sample_size': len(coords_3d),
            'total_records': data_snapshot['total_records'],
            'encoding_duration_seconds': duration,
            'cluster_messages': {},
            'is_epoch_projection': True,
            'entire_cluster_results': {},
            'consistent_sampling': True,
            'row_ids_for_tracking': rowids,
            'generated_on_cpu_worker': True,
            'session_id': session_id
        }
        
        # Save projection
        output_file = Path(output_dir) / "epoch_projections" / f"projections_epoch_{epoch:03d}.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w") as fp:
            json.dump(projection_data, fp, cls=NumpyEncoder, indent=2)
        
        logger.info(f"✅ [Session {session_id}] Saved movie frame for epoch {epoch} to {output_file} ({duration:.1f}s on CPU)")
        
        return str(output_file)
        
    except Exception as e:
        logger.error(f"❌ [Session {session_id}] Failed to generate movie frame for epoch {epoch}: {e}")
        traceback.print_exc()
        return None
        
    finally:
        # Cleanup temp checkpoint
        checkpoint_file = Path(checkpoint_path)
        if checkpoint_file.exists():
            try:
                checkpoint_file.unlink()
                logger.info(f"🗑️  Cleaned up temp checkpoint: {checkpoint_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup checkpoint {checkpoint_path}: {e}")

