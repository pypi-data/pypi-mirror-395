import math
from dataclasses import dataclass
import logging

import torch
import torch.nn as nn
import torch.nn.functional as F

from featrix.neural.featrix_module_dict import FeatrixModuleDict
from featrix.neural.model_config import JointEncoderConfig
from featrix.neural.simple_mlp import SimpleMLP

logger = logging.getLogger(__name__)


class AddCLSToken(nn.Module):
    def __init__(self, d_model):
        super().__init__()

        self.d_model = d_model

        # Initialize the [CLS] token as a learnable parameter
        self.cls_token = nn.Parameter(
            torch.randn(self.d_model) / math.sqrt(self.d_model)
        )

    def forward(self, x):
        # x has shape (B, S, F)

        # Replicate the [CLS] token for all sequences in the batch
        # self.cls_token has shape (F,)
        cls_tokens = self.cls_token.repeat(x.size(0), 1, 1)  # Shape: (B, 1, F)

        # Concatenate the [CLS] token with sequences
        x = torch.cat([cls_tokens, x], dim=1)  # Shape: (B, S+1, F)

        return x


class ColumnEncoding(nn.Module):
    def __init__(self, d_model, seq_len):
        super().__init__()

        #  we add an encoding for the cls token, which always gets prepended as the 0th element
        n_encodings = seq_len

        # Initialize a tensor for positional encodings and set it as a learnable parameter
        # NOTE: this assumes the input comes in the form (sequence, feature)
        self.pos_embedding = nn.Parameter(
            torch.randn(n_encodings, d_model) / math.sqrt(d_model)
        )

        # NOTE: this could be accomplished with an Embedding module, but that would get more
        # cumbersome. Going with a simple single parameter as above is much better.

    def forward(self, x):
        # assume x is in the format (batch, seq, feat)
        # the positional embedding_space gets broadcast across the batch dimension

        return x + self.pos_embedding


# def apply_network_to_tensor(data, network):
#     N, M, K = data.shape

#     # Reshape data to (N*M, K) for batch processing
#     data_reshaped = data.view(N * M, K)

#     # Apply network
#     output = network(data_reshaped)

#     # Reshape output back to (N, M, output_dim)
#     # Assuming output dimension is the same as input K for simplicity
#     output_dim = output.shape[-1]
#     output_reshaped = output.view(N, M, output_dim)

#     return output_reshaped


class JointEncoder(nn.Module):
    def __init__(self, d_embed, col_names_in_order, config: JointEncoderConfig):
        super().__init__()

        self.d_embed = d_embed
        self.config = config

        self.col_names_in_order = col_names_in_order
        self.in_converters = FeatrixModuleDict(
            {
                col_name: SimpleMLP(config.in_converter_configs[col_name])
                for col_name in col_names_in_order
            }
        )

        self.out_converter = SimpleMLP(config=config.out_converter_config)
        self.batch_norm_out = nn.BatchNorm1d(d_embed)

        # Trainable Positional Encoding
        if config.use_col_encoding:
            self.col_encoder = ColumnEncoding(self.config.d_model, self.config.n_cols)

        # simple module to add the cls token to create the joint encoding for the whole sequence
        self.add_cls_token = AddCLSToken(self.config.d_model)

        # Transformer Encoder with batch_first=True for better performance
        encoder_layer = nn.TransformerEncoderLayer(
            self.config.d_model,
            self.config.n_heads,
            dim_feedforward=self.config.d_model * self.config.dim_feedforward_factor,
            dropout=self.config.dropout,
            batch_first=True,  # Enable nested tensor optimization
        )
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer, num_layers=self.config.n_layers
        )
        
        # Storage for attention weights (for diagnostics)
        self._attention_weights = None
        self._enable_attention_capture = False

    def enable_attention_capture(self):
        """Enable capturing attention weights for diagnostic analysis."""
        self._enable_attention_capture = True
    
    def disable_attention_capture(self):
        """Disable capturing attention weights (default, saves memory)."""
        self._enable_attention_capture = False
    
    def get_attention_weights(self):
        """Return captured attention weights. Returns None if capture is disabled."""
        return self._attention_weights

    def forward(self, x):
        # NOTE: we're using a typical transformer encoder here, where all columns get their
        # own encoding. Then we throw away all encodings except the one for the [CLS] token.
        # A more efficient implementation would apply attention directly to inputs and produce
        # only one encoding.

        # FIXME: should the converter be the same for all variables, or should we use different converters for
        # different input variables?
        # ANSWER: using one encoder is fine, at least on smaller datasets.
        # On larger datasets we may want to revisit.

        col_x = []
        for i, col_name in enumerate(self.col_names_in_order):
            converter = self.in_converters[col_name]
            col_x.append(converter(x[:, i, :]))

        x = torch.stack(col_x, dim=1)

        # Add column encodings first, then cls token
        # this means the cls token does not get a positional encoding, but
        # that's OK because only one token gets placed in that position anyway.
        # This simplifies things because this way the positional encoder does
        # not need to worry about adding a positional encoding for the cls token.
        if self.config.use_col_encoding:
            x = self.col_encoder(x)

        x = self.add_cls_token(x)

        # Pass through the transformer encoder (now using batch_first=True)
        x = self.transformer_encoder(x)

        # Use the output of the first token as the encoding of the whole sequence
        # This corresponds to the encoding of the [CLS] token. We throw out the encodings
        # for all other positions. With batch_first=True, CLS token is at position [:, 0, :]
        joint = x[:, 0, :]
        # marginal = x[1:]  # marginal encodings - we don's use these

        # convert from trnsformer dim to embedding_space dim, and normalize
        joint = self.out_converter(joint)

        # CONDITIONAL NORMALIZATION based on config
        # This config check is for safety/future flexibility
        # In practice, this should almost always be True
        if self.config.normalize_output:
            short_vec = nn.functional.normalize(joint[:, 0:3], dim=1)
            full_vec = nn.functional.normalize(joint, dim=1)
        else:
            # This path should rarely/never be used
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("⚠️  Joint encoder normalization is disabled! Embeddings may not be unit norm.")
            short_vec = joint[:, 0:3]
            full_vec = joint

        return short_vec, full_vec
    
    def analyze_attention_head_redundancy(self, batch_data, top_k=5):
        """
        Analyze if attention heads are learning redundant patterns.
        
        This diagnostic helps determine if you need more attention heads:
        - High redundancy (>0.8 similarity) → heads are learning the same thing → need more heads
        - Low redundancy (<0.5 similarity) → heads are diverse → current head count is good
        
        Args:
            batch_data: Input tensor (batch_size, n_cols, d_model) 
            top_k: Number of top attention positions to consider per head
        
        Returns:
            dict with:
                - 'head_similarities': (n_heads, n_heads) pairwise cosine similarities
                - 'avg_similarity': Average pairwise similarity across all heads
                - 'max_similarity': Maximum pairwise similarity (most redundant pair)
                - 'redundant_pairs': List of (head_i, head_j, similarity) where sim > 0.7
                - 'diversity_score': 1 - avg_similarity (higher = more diverse)
                - 'recommendation': String suggesting if more heads are needed
        """
        if not self._enable_attention_capture:
            logger.warning("⚠️  Attention capture is disabled. Call enable_attention_capture() first.")
            return None
        
        # Run forward pass to populate attention weights
        self.eval()  # Set to eval mode to get consistent attention
        with torch.no_grad():
            _ = self.forward(batch_data)
        
        # NOTE: PyTorch's TransformerEncoder doesn't expose attention weights by default
        # We need to monkey-patch or use a custom implementation
        # For now, we'll extract attention from the encoder layers
        
        attention_patterns = []
        n_layers = self.config.n_layers
        n_heads = self.config.n_heads
        
        # Extract attention weights from each layer
        for layer_idx, layer in enumerate(self.transformer_encoder.layers):
            # Access the self-attention module
            self_attn = layer.self_attn
            
            # Need to hook into attention computation
            # This requires modifying the forward pass or using hooks
            # For now, we'll compute attention patterns manually
            pass
        
        # TODO: This requires deeper integration with PyTorch's attention mechanism
        # For now, return a placeholder
        logger.warning("⚠️  Full attention analysis requires attention weight extraction hooks.")
        logger.info("   Analyzing attention patterns via weight similarity instead...")
        
        # Alternative: Analyze attention weight matrices for similarity
        head_patterns = self._analyze_attention_weight_similarity()
        
        return head_patterns
    
    def _analyze_attention_weight_similarity(self):
        """
        Analyze similarity between attention heads by comparing their learned weight matrices.
        
        This is an approximation: instead of comparing attention patterns on specific inputs,
        we compare the learned Q, K, V projection matrices for each head.
        """
        n_heads = self.config.n_heads
        d_model = self.config.d_model
        
        # Collect Q, K, V weight matrices from first transformer layer
        first_layer = self.transformer_encoder.layers[0]
        
        # PyTorch's MultiheadAttention stores weights as (d_model, d_model)
        # Then splits into n_heads during forward pass
        q_weights = first_layer.self_attn.in_proj_weight[:d_model, :]  # Query weights
        k_weights = first_layer.self_attn.in_proj_weight[d_model:2*d_model, :]  # Key weights
        v_weights = first_layer.self_attn.in_proj_weight[2*d_model:, :]  # Value weights
        
        head_dim = d_model // n_heads
        
        # Split into per-head matrices
        q_heads = q_weights.reshape(n_heads, head_dim, d_model)
        k_heads = k_weights.reshape(n_heads, head_dim, d_model)
        v_heads = v_weights.reshape(n_heads, head_dim, d_model)
        
        # Compute pairwise similarities between heads
        # We'll use cosine similarity of flattened QK^T patterns
        head_similarities = torch.zeros(n_heads, n_heads)
        
        for i in range(n_heads):
            for j in range(i, n_heads):
                # Compute attention pattern similarity: compare QK^T for each head
                # QK^T shape would be (head_dim, head_dim) but we want to compare overall behavior
                # Simplified: compare Q and K weights directly
                
                q_i_flat = q_heads[i].flatten()
                q_j_flat = q_heads[j].flatten()
                k_i_flat = k_heads[i].flatten()
                k_j_flat = k_heads[j].flatten()
                
                # Cosine similarity of Q weights
                q_sim = F.cosine_similarity(q_i_flat.unsqueeze(0), q_j_flat.unsqueeze(0))
                
                # Cosine similarity of K weights  
                k_sim = F.cosine_similarity(k_i_flat.unsqueeze(0), k_j_flat.unsqueeze(0))
                
                # Average Q and K similarity
                sim = (q_sim + k_sim) / 2.0
                
                head_similarities[i, j] = sim.item()
                head_similarities[j, i] = sim.item()
        
        # Compute statistics
        # Exclude diagonal (self-similarity = 1.0)
        mask = ~torch.eye(n_heads, dtype=torch.bool)
        off_diagonal = head_similarities[mask]
        
        avg_similarity = off_diagonal.mean().item()
        max_similarity = off_diagonal.max().item()
        min_similarity = off_diagonal.min().item()
        
        # Find redundant pairs (similarity > 0.7)
        redundant_pairs = []
        for i in range(n_heads):
            for j in range(i+1, n_heads):
                sim = head_similarities[i, j].item()
                if sim > 0.7:
                    redundant_pairs.append((i, j, sim))
        
        # Sort by similarity (most redundant first)
        redundant_pairs.sort(key=lambda x: x[2], reverse=True)
        
        # Diversity score (higher = more diverse)
        diversity_score = 1.0 - avg_similarity
        
        # Generate recommendation
        if avg_similarity > 0.8:
            recommendation = "HIGH REDUNDANCY: Heads are learning very similar patterns. Consider increasing n_heads."
            status = "❌ REDUNDANT"
        elif avg_similarity > 0.6:
            recommendation = "MODERATE REDUNDANCY: Some overlap between heads. Current head count is okay, but could benefit from more."
            status = "⚠️  MODERATE"
        else:
            recommendation = "GOOD DIVERSITY: Heads are learning distinct patterns. Current head count is appropriate."
            status = "✅ DIVERSE"
        
        result = {
            'head_similarities': head_similarities.cpu().numpy(),
            'avg_similarity': avg_similarity,
            'max_similarity': max_similarity,
            'min_similarity': min_similarity,
            'redundant_pairs': redundant_pairs,
            'diversity_score': diversity_score,
            'recommendation': recommendation,
            'status': status,
            'n_heads': n_heads,
            'n_redundant_pairs': len(redundant_pairs),
        }
        
        return result
    
    def log_attention_analysis(self, batch_data=None):
        """
        Log attention head diversity analysis.
        
        Args:
            batch_data: Optional input batch. If None, only analyzes weight similarity.
        """
        logger.info("🔍 ATTENTION HEAD DIVERSITY ANALYSIS")
        logger.info(f"   Number of heads: {self.config.n_heads}")
        logger.info(f"   Number of layers: {self.config.n_layers}")
        logger.info(f"   Model dimension: {self.config.d_model}")
        logger.info(f"   Head dimension: {self.config.d_model // self.config.n_heads}")
        
        # Analyze weight similarity
        analysis = self._analyze_attention_weight_similarity()
        
        logger.info(f"\n{analysis['status']} Attention Head Diversity:")
        logger.info(f"   Average head similarity: {analysis['avg_similarity']:.3f}")
        logger.info(f"   Diversity score: {analysis['diversity_score']:.3f} (higher is better)")
        logger.info(f"   Min similarity: {analysis['min_similarity']:.3f}")
        logger.info(f"   Max similarity: {analysis['max_similarity']:.3f}")
        
        if analysis['redundant_pairs']:
            logger.info(f"\n⚠️  Found {len(analysis['redundant_pairs'])} redundant head pairs (>0.7 similarity):")
            for i, j, sim in analysis['redundant_pairs'][:5]:  # Show top 5
                logger.info(f"      Head {i} ↔ Head {j}: {sim:.3f}")
        else:
            logger.info("\n✅ No redundant head pairs found (all < 0.7 similarity)")
        
        logger.info(f"\n💡 {analysis['recommendation']}")
        
        return analysis
