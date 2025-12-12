#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
"""
GraphViz visualization for Featrix neural network architectures using torchview.
"""
import os
from typing import Optional
import logging
import torch

logger = logging.getLogger(__name__)


def _try_install_torchview():
    """Try to install torchview if not available."""
    try:
        import torchview
        return True
    except ImportError:
        logger.info("torchview not found, attempting to install...")
        try:
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "torchview", "-q"])
            import torchview
            logger.info("✅ torchview installed successfully")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Could not install torchview: {e}")
            return False


def generate_graphviz_for_embedding_space(embedding_space, output_path: Optional[str] = None):
    """
    Generate a GraphViz document describing the Embedding Space neural network architecture.
    
    Args:
        embedding_space: EmbeddingSpace instance
        output_path: Path to save the .dot/.png files. If None, uses 'network_architecture_es'
    
    Returns:
        str: Path to the saved .dot file
    """
    if not _try_install_torchview():
        logger.warning("⚠️ torchview not available, skipping visualization")
        return None
    
    from torchview import draw_graph
    
    if output_path is None:
        output_path = "network_architecture_es"
    
    # Remove extension if provided
    output_path = output_path.replace('.dot', '').replace('.png', '')
    
    try:
        # Get the encoder model
        encoder = embedding_space.encoder
        
        # Create sample input to trace the model
        # We need to create a batch of encoded columns
        sample_batch_size = 2
        sample_inputs = []
        
        for col_name in encoder.config.cols_in_order:
            codec = embedding_space.col_codecs.get(col_name)
            if codec:
                try:
                    # Create a dummy encoded tensor for this column
                    # Most codecs output d_model dimensional vectors
                    sample_tensor = torch.randn(sample_batch_size, embedding_space.d_model)
                    sample_inputs.append(sample_tensor)
                except Exception as e:
                    logger.debug(f"Could not create sample input for {col_name}: {e}")
        
        if not sample_inputs:
            logger.warning("Could not create sample inputs for model visualization")
            return None
        
        # Stack inputs to create proper input format
        # The encoder expects (batch, n_cols, d_model)
        sample_input = torch.stack(sample_inputs, dim=1)
        
        logger.info(f"📊 Generating visualization with input shape: {sample_input.shape}")
        
        # The EmbeddingSpaceModel uses a ColumnEncoder that expects dictionary inputs
        # with column names as keys, not plain tensors. TorchView doesn't support this,
        # so we need to create a wrapper that provides the expected dictionary format.
        logger.warning("⚠️ EmbeddingSpace visualization currently not supported")
        logger.warning("   The model expects dictionary inputs (col_name -> tensor),")
        logger.warning("   but torchview can only pass plain tensors during tracing.")
        logger.info("   Use embedding_space.encoder to inspect the model structure instead.")
        return None
        
        # Generate the visualization with high resolution
        model_graph = draw_graph(
            encoder,
            input_data=sample_input,
            graph_name=f'Embedding Space Architecture',
            save_graph=True,
            filename=output_path,
            directory='.',
            expand_nested=True,
            depth=10,  # Show deep layer structure
            device='cpu',  # Ensure we use CPU for visualization
            graph_dir='TB',  # Top-to-bottom layout for vertical layers (more readable)
            roll=False,  # Don't roll dimensions
        )
        
        dot_path = f"{output_path}.gv"
        png_path = f"{output_path}.gv.png"
        
        logger.info(f"✅ Embedding Space architecture saved to {dot_path}")
        if os.path.exists(png_path):
            logger.info(f"✅ Rendered PNG saved to {png_path}")
        
        # Also save metadata as a text file
        metadata_path = f"{output_path}_metadata.txt"
        with open(metadata_path, 'w') as f:
            f.write(f"Embedding Space Neural Network Architecture\n")
            f.write(f"=" * 60 + "\n\n")
            f.write(f"Model Parameters: {embedding_space.model_param_count:,}\n")
            f.write(f"d_model: {embedding_space.d_model}\n")
            f.write(f"Number of Columns: {len(encoder.config.cols_in_order)}\n\n")
            f.write(f"Columns:\n")
            for col_name in encoder.config.cols_in_order:
                col_type = encoder.config.col_types.get(col_name, "unknown")
                codec = embedding_space.col_codecs.get(col_name)
                codec_name = type(codec).__name__ if codec else "Unknown"
                f.write(f"  - {col_name} ({col_type}): {codec_name}\n")
            f.write(f"\nTransformer Configuration:\n")
            joint_config = encoder.config.joint_encoder_config
            f.write(f"  Layers: {joint_config.n_layers}\n")
            f.write(f"  Attention Heads: {joint_config.n_heads}\n")
            f.write(f"  Feedforward Dim: {joint_config.d_model * joint_config.dim_feedforward_factor}\n")
        
        logger.info(f"✅ Metadata saved to {metadata_path}")
        
        return dot_path
        
    except Exception as e:
        logger.error(f"❌ Failed to generate GraphViz for Embedding Space: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def generate_graphviz_for_single_predictor(single_predictor, output_path: Optional[str] = None):
    """
    Generate a GraphViz document describing the Single Predictor neural network architecture.
    
    Args:
        single_predictor: FeatrixSinglePredictor instance
        output_path: Path to save the .dot/.png files. If None, uses 'network_architecture_sp'
    
    Returns:
        str: Path to the saved .dot file
    """
    if not _try_install_torchview():
        logger.warning("⚠️ torchview not available, skipping visualization")
        return None
    
    from torchview import draw_graph
    
    if output_path is None:
        output_path = "network_architecture_sp"
    
    # Remove extension if provided
    output_path = output_path.replace('.dot', '').replace('.png', '')
    
    try:
        # Get the predictor model
        predictor = single_predictor.predictor
        if predictor is None:
            logger.warning("Predictor model is None, cannot generate visualization")
            return None
        
        # Create sample input (row embedding from embedding space)
        sample_batch_size = 2
        d_model = single_predictor.d_model
        sample_input = torch.randn(sample_batch_size, d_model)
        
        logger.info(f"📊 Generating Single Predictor visualization with input shape: {sample_input.shape}")
        
        target_col = single_predictor.target_col_name or "target"
        
        # Generate the visualization with high resolution
        model_graph = draw_graph(
            predictor,
            input_data=sample_input,
            graph_name=f'Single Predictor Architecture (Target: {target_col})',
            save_graph=True,
            filename=output_path,
            directory='.',
            expand_nested=True,
            depth=10,  # Show deep layer structure
            device='cpu',  # Ensure we use CPU for visualization
            graph_dir='TB',  # Top-to-bottom layout for vertical layers (more readable)
            roll=False,  # Don't roll dimensions
        )
        
        dot_path = f"{output_path}.gv"
        png_path = f"{output_path}.gv.png"
        
        logger.info(f"✅ Single Predictor architecture saved to {dot_path}")
        if os.path.exists(png_path):
            logger.info(f"✅ Rendered PNG saved to {png_path}")
        
        # Also save metadata as a text file
        embedding_space = single_predictor.embedding_space
        encoder_config = embedding_space.encoder.config
        
        # Count layers in the predictor
        layer_count = 0
        try:
            import torch.nn as nn
            for module in predictor.modules():
                if isinstance(module, (nn.Linear, nn.Conv1d, nn.Conv2d, nn.LSTM, nn.GRU, nn.TransformerEncoderLayer)):
                    layer_count += 1
        except:
            layer_count = 0
        
        metadata_path = f"{output_path}_metadata.txt"
        with open(metadata_path, 'w') as f:
            f.write(f"Single Predictor Neural Network Architecture\n")
            f.write(f"=" * 60 + "\n\n")
            f.write(f"Target Column: {single_predictor.target_col_name}\n")
            f.write(f"Target Type: {single_predictor.target_col_type}\n")
            f.write(f"Target Codec: {type(single_predictor.target_codec).__name__}\n\n")
            f.write(f"Architecture:\n")
            f.write(f"  d_model: {d_model}\n")
            f.write(f"  Layers: {layer_count}\n")
            f.write(f"  Input Features: {len([c for c in encoder_config.cols_in_order if c != single_predictor.target_col_name])}\n")
            f.write(f"  Total Columns: {len(encoder_config.cols_in_order)}\n\n")
            
            # Try to count predictor parameters
            try:
                param_count = sum(p.numel() for p in predictor.parameters())
                f.write(f"Predictor Parameters: {param_count:,}\n")
            except:
                pass
            
            f.write(f"\nInput Columns (excluding target):\n")
            for col_name in encoder_config.cols_in_order:
                if col_name != single_predictor.target_col_name:
                    col_type = encoder_config.col_types.get(col_name, "unknown")
                    f.write(f"  - {col_name} ({col_type})\n")
        
        logger.info(f"✅ Metadata saved to {metadata_path}")
        
        return dot_path
        
    except Exception as e:
        logger.error(f"❌ Failed to generate GraphViz for Single Predictor: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

