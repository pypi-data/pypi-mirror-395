#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import logging
import traceback
from typing import Optional

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from featrix.neural.device import device
from featrix.neural.featrix_token import Token, TokenStatus
from featrix.neural.model_config import ColumnType, SimpleMLPConfig
from featrix.neural.simple_mlp import SimpleMLP
from featrix.neural.string_cache import StringCache
from featrix.neural.url_parser import parse_url, URLComponents
from featrix.neural.hubspot_free_domains_list_may_2025 import is_free_email_domain
from featrix.neural.domain_codec import DomainEncoder

logger = logging.getLogger(__name__)


class URLEncoderConfig:
    """Configuration for URL encoder."""
    def __init__(self, d_model: int, n_hidden_layers: int = 2, d_hidden: int = None):
        self.d_model = d_model
        self.n_hidden_layers = n_hidden_layers
        self.d_hidden = d_hidden or d_model * 2


class URLEncoder(nn.Module):
    """
    URL encoder that combines multiple components via MLP:
    - Protocol (categorical embedding)
    - Subdomain (string embedding)
    - Domain main part (string embedding for semantics)
    - TLD (categorical embedding)
    - TLD type (categorical: generic/country/new)
    - Is free domain (binary flag)
    - Path (string embedding)
    - Endpoint (string embedding)
    - Query params (string embedding)
    """
    
    def __init__(self, config: URLEncoderConfig, string_cache: StringCache):
        super().__init__()
        self.config = config
        self.string_cache = string_cache
        self.d_model = config.d_model
        
        # Protocol vocabulary (common protocols)
        self.protocols = ['http', 'https', 'ftp', 'ftps', 'ws', 'wss', 'file', 'other']
        self.protocol_to_idx = {p: i for i, p in enumerate(self.protocols)}
        self.protocol_embedding = nn.Embedding(len(self.protocols), 32)
        nn.init.xavier_uniform_(self.protocol_embedding.weight)
        
        # Create DomainEncoder to reuse domain encoding logic
        # DomainEncoder outputs d_model, but we'll project it down to a smaller size
        # to combine with URL-specific features
        domain_embed_dim = 128  # Intermediate size for domain embedding
        domain_config = DomainEncoder.get_default_config(domain_embed_dim, dropout=0.3)
        self.domain_encoder = DomainEncoder(domain_config, string_cache)
        
        # String embeddings come from string_cache (384 dim)
        string_embed_dim = string_cache.embedding_dim if string_cache else 384
        
        # Project string embeddings for URL-specific parts
        self.path_proj = nn.Linear(string_embed_dim, 64, bias=False)
        self.endpoint_proj = nn.Linear(string_embed_dim, 64, bias=False)
        self.params_proj = nn.Linear(string_embed_dim, 32, bias=False)
        
        nn.init.xavier_uniform_(self.path_proj.weight, gain=0.5)
        nn.init.xavier_uniform_(self.endpoint_proj.weight, gain=0.5)
        nn.init.xavier_uniform_(self.params_proj.weight, gain=0.5)
        
        # Total input dimension to MLP:
        # protocol(32) + domain_embedding(128) + path(64) + endpoint(64) + params(32) = 320
        total_dim = 32 + domain_embed_dim + 64 + 64 + 32
        
        # MLP to combine all components
        mlp_config = SimpleMLPConfig(
            d_in=total_dim,
            d_out=config.d_model,
            d_model=None,
            normalize=False,
            n_hidden_layers=config.n_hidden_layers,
            d_hidden=config.d_hidden
        )
        self.combiner_mlp = SimpleMLP(mlp_config)
        
        # Initialize MLP weights
        for name, param in self.combiner_mlp.named_parameters():
            if 'weight' in name and param.ndim >= 2:
                nn.init.xavier_uniform_(param, gain=1.0)
            elif 'bias' in name:
                nn.init.zeros_(param)
        
        # Replacement embedding for invalid/missing URLs
        self._replacement_embedding = nn.Parameter(torch.zeros(config.d_model))
        nn.init.normal_(self._replacement_embedding, mean=0.0, std=0.01)
        
        logger.info(f"🌐 URLEncoder initialized: d_model={config.d_model}, total_input_dim={total_dim}")
    
    def _get_protocol_idx(self, protocol: str) -> int:
        """Get protocol index, defaulting to 'other' for unknown protocols."""
        protocol_clean = protocol.lower() if protocol else 'https'
        return self.protocol_to_idx.get(protocol_clean, self.protocol_to_idx['other'])
    
    def _url_components_to_domain_dict(self, url_comp: URLComponents) -> dict:
        """Convert URLComponents to domain component dict for DomainEncoder."""
        return {
            'subdomain': url_comp.subdomain,
            'domain_main': url_comp.domain_main,
            'tld': url_comp.tld,
            'tld_type': url_comp.tld_type,
            'is_free_email_domain': url_comp.is_free_domain,
            'ip_addresses': [],  # URLs don't do DNS lookup (too slow), domain codec handles it
            'has_ipv6': False
        }
    
    def _get_string_embedding(self, text: str) -> torch.Tensor:
        """Get string embedding from cache, or zeros if not available."""
        if not text:
            # Keep on CPU for DataLoader workers
            return torch.zeros(self.string_cache.embedding_dim)
        
        try:
            emb = self.string_cache.get_embedding(text)
            if emb is not None:
                # Keep on CPU for DataLoader workers
                return torch.tensor(emb, dtype=torch.float32)
        except Exception as e:
            logger.debug(f"Failed to get string embedding for '{text}': {e}")
        
        # Keep on CPU for DataLoader workers
        return torch.zeros(self.string_cache.embedding_dim)
    
    def forward(self, url_components_list):
        """
        Encode a batch of URL components.
        
        Args:
            url_components_list: List of URLComponents objects
        
        Returns:
            Tensor of shape (batch_size, d_model)
        """
        batch_size = len(url_components_list)
        embeddings = []
        
        for url_comp in url_components_list:
            # Handle invalid URLs
            if not url_comp.is_valid:
                embeddings.append(self._replacement_embedding.unsqueeze(0))
                continue
            
            # 1. Protocol embedding (32)
            proto_idx = self._get_protocol_idx(url_comp.protocol)
            # Keep on CPU for DataLoader workers
            proto_emb = self.protocol_embedding(torch.tensor(proto_idx))
            
            # 2. Domain embedding using DomainEncoder (128)
            # Convert URLComponents to domain dict format
            domain_comp = self._url_components_to_domain_dict(url_comp)
            domain_emb = self.domain_encoder.encode_domain_components(domain_comp)
            
            # 3. Path string embedding → projected (64)
            path_str_emb = self._get_string_embedding(url_comp.path if url_comp.path != '/' else '')
            path_emb = self.path_proj(path_str_emb)
            
            # 4. Endpoint string embedding → projected (64)
            endpoint_str_emb = self._get_string_embedding(url_comp.endpoint)
            endpoint_emb = self.endpoint_proj(endpoint_str_emb)
            
            # 5. Query params string embedding → projected (32)
            params_str_emb = self._get_string_embedding(url_comp.query_params)
            params_emb = self.params_proj(params_str_emb)
            
            # Concatenate all components
            combined = torch.cat([
                proto_emb,
                domain_emb,
                path_emb,
                endpoint_emb,
                params_emb
            ], dim=-1)
            
            # Pass through MLP
            final_emb = self.combiner_mlp(combined.unsqueeze(0))
            embeddings.append(final_emb)
        
        # Stack all embeddings
        result = torch.cat(embeddings, dim=0)
        return result


class URLCodec:
    """
    Codec for URL/domain columns.
    Parses URLs into components and encodes them via URLEncoder.
    """
    
    def __init__(self, embed_dim: int, string_cache: StringCache, debugName: str = "url_col"):
        self.embed_dim = embed_dim
        self.string_cache = string_cache
        self.debugName = debugName
        self.name = debugName
        self.column_type = ColumnType.URL
        
        # Create encoder config
        config = URLEncoderConfig(d_model=embed_dim, n_hidden_layers=2)
        
        # Create encoder
        self.encoder = URLEncoder(config, string_cache).to(device)
        
        logger.info(f"🌐 URLCodec created for column '{debugName}': d_model={embed_dim}")
    
    def tokenize(self, value):
        """
        Tokenize a URL value into a Token.
        
        Args:
            value: URL string or list of URL strings
        
        Returns:
            Token or list of Tokens
        """
        if isinstance(value, (list, tuple)):
            return [self.tokenize(v) for v in value]
        
        # Parse URL
        url_comp = parse_url(str(value), check_free_domain_fn=is_free_email_domain)
        
        # Create token
        status = TokenStatus.OK if url_comp.is_valid else TokenStatus.UNPARSEABLE
        
        return Token(
            embedding=None,  # Will be computed by encoder
            status=status,
            metadata={'url_components': url_comp, 'original': value}
        )
    
    def detokenize(self, token):
        """
        Detokenize a Token back to URL string (best-effort reconstruction).
        
        Args:
            token: Token object
        
        Returns:
            Reconstructed URL string
        """
        if hasattr(token, 'metadata') and 'url_components' in token.metadata:
            url_comp = token.metadata['url_components']
            
            if not url_comp.is_valid:
                return url_comp.original
            
            # Reconstruct URL from components
            parts = []
            if url_comp.protocol:
                parts.append(f"{url_comp.protocol}://")
            
            if url_comp.subdomain:
                parts.append(f"{url_comp.subdomain}.")
            
            if url_comp.domain_main:
                parts.append(url_comp.domain_main)
            
            if url_comp.tld:
                parts.append(f".{url_comp.tld}")
            
            if url_comp.path and url_comp.path != '/':
                parts.append(url_comp.path)
            
            if url_comp.query_params:
                parts.append(f"?{url_comp.query_params}")
            
            return ''.join(parts)
        
        # Fallback
        if hasattr(token, 'metadata') and 'original' in token.metadata:
            return token.metadata['original']
        
        return "<unknown_url>"
    
    def encode(self, tokens):
        """
        Encode tokens using the URLEncoder.
        
        Args:
            tokens: List of Token objects
        
        Returns:
            Tensor of shape (batch_size, embed_dim)
        """
        # Extract URL components from tokens
        url_components_list = []
        for token in tokens:
            if hasattr(token, 'metadata') and 'url_components' in token.metadata:
                url_components_list.append(token.metadata['url_components'])
            else:
                # Create invalid component for unparseable tokens
                url_components_list.append(URLComponents(is_valid=False, original=''))
        
        # Encode using URLEncoder
        with torch.set_grad_enabled(self.encoder.training):
            embeddings = self.encoder(url_components_list)
        
        return embeddings
    
    def decode(self, embeddings):
        """
        Decode embeddings back to tokens (approximate, for reconstruction loss).
        
        Note: This is a lossy operation. We can't perfectly reconstruct URLs from embeddings.
        Returns placeholder tokens.
        """
        batch_size = embeddings.shape[0]
        tokens = []
        
        for i in range(batch_size):
            token = Token(
                embedding=embeddings[i].detach().cpu().numpy(),
                status=TokenStatus.OK,
                metadata={'reconstructed': True}
            )
            tokens.append(token)
        
        return tokens
    
    def get_codec_name(self):
        """Return codec name for logging/debugging."""
        return "url"
    
    def get_not_present_token(self):
        """Return a token representing a not-present value."""
        return Token(
            value=None,
            status=TokenStatus.NOT_PRESENT,
            metadata={'url_components': None, 'original': ''}
        )
    
    def get_marginal_token(self):
        """Return a token representing a masked/marginal value for reconstruction testing."""
        return Token(
            value=None,
            status=TokenStatus.MARGINAL,
            metadata={'url_components': None, 'original': ''}
        )

