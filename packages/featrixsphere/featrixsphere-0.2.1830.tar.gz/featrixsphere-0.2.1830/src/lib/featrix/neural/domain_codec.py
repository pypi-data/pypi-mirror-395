#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
"""
Domain Codec and Encoder

Encodes domain names by combining:
- Subdomain (string embedding)
- Domain main part (string embedding)
- TLD (categorical embedding)
- TLD type (categorical: generic/country/new)
- Is free email domain (binary flag)
"""
import logging
import ipaddress
import torch
import torch.nn as nn
import torch.nn.functional as F

from typing import Optional, List, Tuple

from featrix.neural.device import device
from featrix.neural.featrix_token import Token, TokenStatus
from featrix.neural.model_config import ColumnType, SimpleMLPConfig
from featrix.neural.simple_mlp import SimpleMLP
from featrix.neural.string_cache import StringCache
from featrix.neural.url_parser import parse_domain_parts, classify_tld
from featrix.neural.hubspot_free_domains_list_may_2025 import is_free_email_domain
from featrix.neural.world_data import get_or_lookup_dns

logger = logging.getLogger(__name__)


class DomainEncoder(nn.Module):
    """
    Encodes domain features using an MLP.
    
    Combines:
    - Subdomain (string embedding, projected)
    - Domain main part (string embedding, projected)
    - TLD (categorical embedding)
    - TLD type (categorical: generic/country/new)
    - Is free email domain (binary flag)
    """
    
    def __init__(self, config: SimpleMLPConfig, string_cache: StringCache, column_name: Optional[str] = None):
        super().__init__()
        self.config = config
        self.string_cache = string_cache
        self.column_name = column_name
        self.d_model = config.d_out
        
        # String embeddings come from string_cache (384 dim)
        string_embed_dim = string_cache.embedding_dim if string_cache else 384
        
        # Project string embeddings to smaller dimensions
        self.subdomain_proj = nn.Linear(string_embed_dim, 64, bias=False)
        self.domain_proj = nn.Linear(string_embed_dim, 128, bias=False)  # Main domain gets more capacity
        
        nn.init.xavier_uniform_(self.subdomain_proj.weight, gain=0.5)
        nn.init.xavier_uniform_(self.domain_proj.weight, gain=1.0)
        
        # TLD vocabulary (top TLDs + other)
        self.tlds = [
            'com', 'net', 'org', 'edu', 'gov', 'mil',
            'uk', 'de', 'fr', 'ca', 'au', 'jp', 'cn', 'ru',
            'io', 'ai', 'app', 'dev', 'tech', 'online',
            'other'
        ]
        self.tld_to_idx = {t: i for i, t in enumerate(self.tlds)}
        self.tld_embedding = nn.Embedding(len(self.tlds), 32)
        nn.init.xavier_uniform_(self.tld_embedding.weight)
        
        # TLD type vocabulary
        self.tld_types = ['generic', 'country', 'new']
        self.tld_type_to_idx = {t: i for i, t in enumerate(self.tld_types)}
        self.tld_type_embedding = nn.Embedding(len(self.tld_types), 16)
        nn.init.xavier_uniform_(self.tld_type_embedding.weight)
        
        # Binary flag for free email domain (learned scalar)
        self.free_domain_weight = nn.Parameter(torch.randn(1, 8))
        
        # IP address encoding: up to 4 IPs, each IPv4=4 octets, IPv6=8 segments
        # We'll encode as: 4 IPs × 4 features each = 16 features (IPv4) or 4 IPs × 8 features = 32 features (IPv6)
        # For simplicity, use max size: 4 IPs × 8 features = 32, plus 2 metadata (count, has_ipv6) = 34
        self.max_ips = 4
        self.ip_features_per_ip = 8  # Support both IPv4 (4 octets) and IPv6 (8 segments)
        self.ip_embedding_dim = (self.max_ips * self.ip_features_per_ip) + 2  # 34 total
        
        # Total input dimension to MLP:
        # subdomain(64) + domain(128) + tld(32) + tld_type(16) + free_domain(8) + ip_features(34) = 282
        mlp_input_dim = 64 + 128 + 32 + 16 + 8 + self.ip_embedding_dim
        
        # Create MLP encoder
        self.mlp_encoder = SimpleMLP(
            SimpleMLPConfig(
                d_in=mlp_input_dim,
                d_out=config.d_out,
                d_hidden=config.d_hidden if hasattr(config, 'd_hidden') else 256,
                n_hidden_layers=config.n_hidden_layers if hasattr(config, 'n_hidden_layers') else 2,
                dropout=config.dropout if hasattr(config, 'dropout') else 0.3,
                normalize=config.normalize if hasattr(config, 'normalize') else True,
                residual=config.residual if hasattr(config, 'residual') else True,
                use_batch_norm=config.use_batch_norm if hasattr(config, 'use_batch_norm') else True,
            )
        )
        
        # Replacement embedding for unknown/not present tokens
        self._replacement_embedding = nn.Parameter(torch.randn(config.d_out))
    
    def _get_string_embedding(self, text: str) -> torch.Tensor:
        """Get string embedding from string cache."""
        if not text or not self.string_cache:
            # Keep on CPU for DataLoader workers
            return torch.zeros(self.string_cache.embedding_dim)
        
        try:
            embedding = self.string_cache.get_embedding(text)
            if embedding is not None:
                return embedding.to(device)
        except Exception as e:
            logger.debug(f"Failed to get string embedding for '{text}': {e}")
        
        # Keep on CPU for DataLoader workers
        return torch.zeros(self.string_cache.embedding_dim)
    
    def _get_tld_idx(self, tld: str) -> int:
        """Get TLD index, defaulting to 'other' if not found."""
        tld_clean = tld.lower().lstrip('.') if tld else ''
        return self.tld_to_idx.get(tld_clean, len(self.tlds) - 1)  # 'other' is last
    
    def _get_tld_type_idx(self, tld: str) -> int:
        """Get TLD type index."""
        tld_type = classify_tld(tld) if tld else 'generic'
        return self.tld_type_to_idx.get(tld_type, 0)  # Default to 'generic'
    
    def encode_domain_components(self, domain_comp: dict) -> torch.Tensor:
        """
        Encode domain components directly (without TokenBatch).
        Useful for composition in other encoders like URLEncoder.
        
        Args:
            domain_comp: Dictionary with domain components (subdomain, domain_main, tld, etc.)
            
        Returns:
            Domain embedding tensor of shape [d_model]
        """
        # 1. Subdomain string embedding → projected (64)
        subdomain_str_emb = self._get_string_embedding(domain_comp.get('subdomain', ''))
        subdomain_emb = self.subdomain_proj(subdomain_str_emb)
        
        # 2. Domain main string embedding → projected (128)
        domain_str_emb = self._get_string_embedding(domain_comp.get('domain_main', ''))
        domain_emb = self.domain_proj(domain_str_emb)
        
        # 3. TLD embedding (32)
        tld = domain_comp.get('tld', '')
        tld_idx = self._get_tld_idx(tld)
        # Keep on CPU for DataLoader workers
        tld_emb = self.tld_embedding(torch.tensor(tld_idx))
        
        # 4. TLD type embedding (16)
        tld_type_idx = self._get_tld_type_idx(tld)
        # Keep on CPU for DataLoader workers
        tld_type_emb = self.tld_type_embedding(torch.tensor(tld_type_idx))
        
        # 5. Free email domain flag (8)
        is_free = domain_comp.get('is_free_email_domain', False)
        # Keep on CPU for DataLoader workers
        free_domain_flag = torch.tensor([1.0 if is_free else 0.0])
        free_domain_emb = free_domain_flag * self.free_domain_weight.squeeze(0)
        
        # 6. IP address features (34)
        ip_list = domain_comp.get('ip_addresses', [])
        has_ipv6 = domain_comp.get('has_ipv6', False)
        ip_features = self._encode_ips(ip_list, has_ipv6)
        
        # Concatenate all features
        combined = torch.cat([
            subdomain_emb,
            domain_emb,
            tld_emb,
            tld_type_emb,
            free_domain_emb,
            ip_features
        ]).unsqueeze(0)  # Add batch dimension
        
        # Encode through MLP
        out = self.mlp_encoder(combined)
        
        # Return single embedding (remove batch dimension)
        return out.squeeze(0)
    
    def forward(self, token_batch):
        """
        Encode domain token batch into embeddings.
        
        Args:
            token_batch: TokenBatch with value containing domain components metadata
            
        Returns:
            (short_vec, full_vec) tuple of embeddings
        """
        batch_size = token_batch.value.shape[0] if hasattr(token_batch.value, 'shape') else len(token_batch.value)
        
        # Extract domain components from token metadata
        embeddings = []
        for i in range(batch_size):
            if token_batch.status[i] != TokenStatus.OK:
                embeddings.append(self._replacement_embedding.unsqueeze(0))
                continue
            
            # Get domain components from token metadata
            domain_comp = token_batch.value[i] if hasattr(token_batch.value, '__getitem__') else token_batch.value
            
            # 1. Subdomain string embedding → projected (64)
            subdomain_str_emb = self._get_string_embedding(domain_comp.get('subdomain', ''))
            subdomain_emb = self.subdomain_proj(subdomain_str_emb)
            
            # 2. Domain main string embedding → projected (128)
            domain_str_emb = self._get_string_embedding(domain_comp.get('domain_main', ''))
            domain_emb = self.domain_proj(domain_str_emb)
            
            # 3. TLD embedding (32)
            tld = domain_comp.get('tld', '')
            tld_idx = self._get_tld_idx(tld)
            # Keep on CPU for DataLoader workers
            tld_emb = self.tld_embedding(torch.tensor(tld_idx))
            
            # 4. TLD type embedding (16)
            tld_type_idx = self._get_tld_type_idx(tld)
            # Keep on CPU for DataLoader workers
            tld_type_emb = self.tld_type_embedding(torch.tensor(tld_type_idx))
            
            # 5. Free email domain flag (8)
            is_free = domain_comp.get('is_free_email_domain', False)
            # Keep on CPU for DataLoader workers
            free_domain_flag = torch.tensor([1.0 if is_free else 0.0])
            free_domain_emb = free_domain_flag * self.free_domain_weight.squeeze(0)
            
            # 6. IP address features (34)
            ip_list = domain_comp.get('ip_addresses', [])
            has_ipv6 = domain_comp.get('has_ipv6', False)
            ip_features = self._encode_ips(ip_list, has_ipv6)
            
            # Concatenate all features
            combined = torch.cat([
                subdomain_emb,
                domain_emb,
                tld_emb,
                tld_type_emb,
                free_domain_emb,
                ip_features
            ])
            
            embeddings.append(combined.unsqueeze(0))
        
        # Stack into batch tensor
        features = torch.cat(embeddings, dim=0)  # [batch_size, 248]
        
        # Encode through MLP
        out = self.mlp_encoder(features)
        
        # Check for NaN in output
        if torch.isnan(out).any() or torch.isinf(out).any():
            logger.error(f"💥 DomainEncoder output contains NaN/Inf!")
            out = self._replacement_embedding.unsqueeze(0).expand(batch_size, -1)
        
        # Override embeddings for special tokens
        out[token_batch.status == TokenStatus.NOT_PRESENT] = self._replacement_embedding
        out[token_batch.status == TokenStatus.UNKNOWN] = self._replacement_embedding
        out[token_batch.status == TokenStatus.MARGINAL] = self._replacement_embedding
        
        # Normalize if configured
        if self.config.normalize:
            short_vec = F.normalize(out[:, 0:3], dim=1, eps=1e-8)
            full_vec = F.normalize(out, dim=1, eps=1e-8)
        else:
            short_vec = out[:, 0:3]
            full_vec = out
        
        return short_vec, full_vec
    
    @staticmethod
    def get_default_config(d_model: int, dropout: float):
        """Get default config for domain encoder."""
        from featrix.neural.sphere_config import get_config
        normalize_column_encoders = get_config().get_normalize_column_encoders()
        
        return SimpleMLPConfig(
            d_in=282,  # subdomain(64) + domain(128) + tld(32) + tld_type(16) + free_domain(8) + ip_features(34)
            d_out=d_model,
            d_hidden=256,
            n_hidden_layers=2,
            dropout=dropout,
            normalize=normalize_column_encoders,
            residual=True,
            use_batch_norm=True,
        )


class DomainCodec(nn.Module):
    """
    Codec for domain columns.
    
    Parses domain names into components and tokenizes them.
    """
    
    def __init__(self, enc_dim: int, string_cache: StringCache, debugName: str = "domain_col"):
        super().__init__()
        self._is_decodable = False  # Domains are not directly decodable
        self.enc_dim = enc_dim
        self.string_cache = string_cache
        self.debugName = debugName
        
    def get_codec_name(self):
        return ColumnType.DOMAIN
    
    def get_codec_info(self):
        return {
            "enc_dim": self.enc_dim,
            "features": [
                "subdomain", "domain_main", "tld", "tld_type", "is_free_email_domain"
            ]
        }
    
    def get_not_present_token(self):
        """Return token for missing domain values."""
        return Token(
            value={
                'subdomain': '', 
                'domain_main': '', 
                'tld': '', 
                'tld_type': 'generic', 
                'is_free_email_domain': False,
                'ip_addresses': [],
                'has_ipv6': False
            },
            status=TokenStatus.NOT_PRESENT,
        )
    
    def get_marginal_token(self):
        """Return token for masked domain values."""
        return Token(
            value={
                'subdomain': '', 
                'domain_main': '', 
                'tld': '', 
                'tld_type': 'generic', 
                'is_free_email_domain': False,
                'ip_addresses': [],
                'has_ipv6': False
            },
            status=TokenStatus.MARGINAL,
        )
    
    def _parse_domain(self, domain_str: str) -> dict:
        """
        Parse domain string into components and perform DNS lookup using world data cache.
        
        Returns:
            Dictionary with subdomain, domain_main, tld, tld_type, is_free_email_domain,
            ip_addresses, has_ipv6
        """
        if not domain_str or not isinstance(domain_str, str):
            return {
                'subdomain': '',
                'domain_main': '',
                'tld': '',
                'tld_type': 'generic',
                'is_free_email_domain': False,
                'ip_addresses': [],
                'has_ipv6': False
            }
        
        # Remove protocol if present
        domain_str = domain_str.strip()
        if domain_str.startswith('http://'):
            domain_str = domain_str[7:]
        elif domain_str.startswith('https://'):
            domain_str = domain_str[8:]
        
        # Remove leading/trailing slashes
        domain_str = domain_str.strip('/')
        
        # Parse domain parts
        subdomain, domain_main, tld = parse_domain_parts(domain_str)
        
        # Classify TLD
        tld_type = classify_tld(tld) if tld else 'generic'
        
        # Check if free email domain
        is_free = False
        ip_addresses = []
        has_ipv6 = False
        
        if domain_main and tld:
            full_domain = f"{domain_main}.{tld}"
            try:
                is_free = is_free_email_domain(full_domain)
            except Exception as e:
                logger.debug(f"Error checking free email domain for {full_domain}: {e}")
            
            # Perform DNS lookup using world data cache
            try:
                dns_info = get_or_lookup_dns(full_domain, force_refresh=False)
                ip_addresses = dns_info.get('ip_addresses', [])
                has_ipv6 = dns_info.get('has_ipv6', False)
            except Exception as e:
                logger.debug(f"Error performing DNS lookup for {full_domain}: {e}")
        
        return {
            'subdomain': subdomain,
            'domain_main': domain_main,
            'tld': tld,
            'tld_type': tld_type,
            'is_free_email_domain': is_free,
            'ip_addresses': ip_addresses,
            'has_ipv6': has_ipv6
        }
    
    def tokenize(self, value):
        """
        Tokenize a domain value into a Token.
        
        Args:
            value: Domain string
            
        Returns:
            Token with domain components as metadata
        """
        try:
            domain_str = str(value) if value is not None else ''
            
            # Parse domain
            domain_comp = self._parse_domain(domain_str)
            
            # Check if valid
            if not domain_comp['domain_main']:
                return Token(
                    value=domain_comp,
                    status=TokenStatus.UNKNOWN,
                )
            
            return Token(
                value=domain_comp,
                status=TokenStatus.OK,
            )
            
        except Exception as e:
            logger.debug(f"DomainCodec.tokenize failed for value {value}: {e}")
            return Token(
                value={
                    'subdomain': '', 
                    'domain_main': '', 
                    'tld': '', 
                    'tld_type': 'generic', 
                    'is_free_email_domain': False,
                    'ip_addresses': [],
                    'has_ipv6': False
                },
                status=TokenStatus.UNKNOWN,
            )
    
    @property
    def token_dtype(self):
        return dict  # Token value is a dict of domain components

