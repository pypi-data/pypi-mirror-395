#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
"""
Timestamp Codec and Encoder

Extracts temporal features from datetime values and encodes them using an MLP.
Features include: seconds, minutes, hours, day of month, day of week, month of year,
year, day of year, week of year, timezone (if available), year_since_2000, year_since_2020.
"""
import logging
import math
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F

from datetime import datetime
from typing import Optional, Dict, Any

from featrix.neural.featrix_token import Token, TokenStatus
from featrix.neural.model_config import ColumnType, SimpleMLPConfig
from featrix.neural.simple_mlp import SimpleMLP

logger = logging.getLogger(__name__)


class TimestampEncoder(nn.Module):
    """
    Encodes timestamp features using an MLP.
    
    Extracts temporal features from datetime values:
    - seconds (0-59)
    - minutes (0-59)
    - hours (0-23)
    - day of month (1-31)
    - day of week (0-6, Monday=0)
    - month of year (1-12)
    - year
    - day of year (1-366)
    - week of year (1-53)
    - timezone offset in hours (if available, else 0)
    - year_since_2000
    - year_since_2020
    """
    
    def __init__(self, config: SimpleMLPConfig, column_name: Optional[str] = None):
        super().__init__()
        self.config = config
        self.column_name = column_name
        
        # Input dimension: 12 features
        # seconds, minutes, hours, day_of_month, day_of_week, month, year,
        # day_of_year, week_of_year, timezone, year_since_2000, year_since_2020
        self.n_features = 12
        
        # Create MLP encoder
        self.mlp_encoder = SimpleMLP(
            SimpleMLPConfig(
                d_in=self.n_features,
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
        
    def forward(self, token_batch):
        """
        Encode timestamp token batch into embeddings.
        
        Args:
            token_batch: TokenBatch with value as feature tensor [batch_size, n_features]
            
        Returns:
            (short_vec, full_vec) tuple of embeddings
        """
        batch_size = token_batch.value.shape[0]
        
        # token_batch.value should be [batch_size, n_features] tensor
        features = token_batch.value.float()
        
        # Validate input
        if torch.isnan(features).any() or torch.isinf(features).any():
            nan_mask = torch.isnan(features) | torch.isinf(features)
            features = torch.where(nan_mask, torch.zeros_like(features), features)
            if not hasattr(self, '_nan_warning_logged'):
                logger.warning(f"⚠️  TimestampEncoder: Detected and replaced NaN/Inf values in input")
                self._nan_warning_logged = True
        
        # Encode through MLP
        out = self.mlp_encoder(features)
        
        # Check for NaN in output
        if torch.isnan(out).any() or torch.isinf(out).any():
            logger.error(f"💥 TimestampEncoder output contains NaN/Inf!")
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
    
    @property
    def marginal_embedding(self):
        # We return the same vector as NOT_PRESENT token because they are treated the
        # same from a probabilistic point of view by the network, and should be treated
        # the same when the model is queried.
        if self.config.normalize:
            return F.normalize(self._replacement_embedding, dim=-1)
        return self._replacement_embedding
    
    @staticmethod
    def get_default_config(d_model: int, dropout: float):
        """Get default config for timestamp encoder."""
        from featrix.neural.sphere_config import get_config
        normalize_column_encoders = get_config().get_normalize_column_encoders()
        
        return SimpleMLPConfig(
            d_in=12,  # 12 temporal features
            d_out=d_model,
            d_hidden=256,
            n_hidden_layers=2,
            dropout=dropout,
            normalize=normalize_column_encoders,
            residual=True,
            use_batch_norm=True,
        )


class TimestampCodec(nn.Module):
    """
    Codec for timestamp columns.
    
    Extracts temporal features from datetime values and tokenizes them.
    """
    
    def __init__(self, enc_dim: int):
        super().__init__()
        self._is_decodable = True  # Timestamps can be decoded from feature vector
        self.enc_dim = enc_dim
        
    def get_codec_name(self):
        return ColumnType.TIMESTAMP
    
    def get_codec_info(self):
        return {
            "enc_dim": self.enc_dim,
            "n_features": 12,
            "features": [
                "seconds", "minutes", "hours", "day_of_month", "day_of_week",
                "month", "year", "day_of_year", "week_of_year", "timezone",
                "year_since_2000", "year_since_2020"
            ]
        }
    
    def get_not_present_token(self):
        """Return token for missing timestamp values."""
        # Return zero features for not present
        return Token(
            value=torch.zeros(12, dtype=torch.float32),
            status=TokenStatus.NOT_PRESENT,
        )
    
    def get_marginal_token(self):
        """Return token for masked timestamp values."""
        return Token(
            value=torch.zeros(12, dtype=torch.float32),
            status=TokenStatus.MARGINAL,
        )
    
    def _extract_features(self, dt: pd.Timestamp) -> np.ndarray:
        """
        Extract temporal features from a pandas Timestamp.
        
        Returns:
            numpy array of 12 features: [seconds, minutes, hours, day_of_month, 
            day_of_week, month, year, day_of_year, week_of_year, timezone, 
            year_since_2000, year_since_2020]
        """
        # Basic time features
        seconds = float(dt.second)
        minutes = float(dt.minute)
        hours = float(dt.hour)
        day_of_month = float(dt.day)
        day_of_week = float(dt.dayofweek)  # 0=Monday, 6=Sunday
        month = float(dt.month)
        year = float(dt.year)
        day_of_year = float(dt.dayofyear)
        week_of_year = float(dt.isocalendar()[1])  # ISO week number
        
        # Timezone offset in hours (if available)
        if dt.tz is not None:
            try:
                # Get UTC offset in hours
                offset = dt.tz.utcoffset(dt)
                if offset is not None:
                    timezone = offset.total_seconds() / 3600.0
                else:
                    timezone = 0.0
            except Exception:
                timezone = 0.0
        else:
            timezone = 0.0
        
        # Year offsets
        year_since_2000 = float(year - 2000)
        year_since_2020 = float(year - 2020)
        
        features = np.array([
            seconds,
            minutes,
            hours,
            day_of_month,
            day_of_week,
            month,
            year,
            day_of_year,
            week_of_year,
            timezone,
            year_since_2000,
            year_since_2020
        ], dtype=np.float32)
        
        return features
    
    def tokenize(self, value):
        """
        Tokenize a timestamp value into feature vector.
        
        Args:
            value: datetime-like value (pandas Timestamp, datetime, or string)
            
        Returns:
            Token with feature vector as value
        """
        try:
            # Convert to pandas Timestamp if needed
            if isinstance(value, str):
                dt = pd.to_datetime(value, errors='coerce')
            elif isinstance(value, (datetime, pd.Timestamp)):
                dt = pd.Timestamp(value)
            else:
                # Try to convert numeric value (Unix timestamp)
                try:
                    dt = pd.Timestamp.fromtimestamp(float(value))
                except (ValueError, TypeError, OSError):
                    dt = pd.to_datetime(value, errors='coerce')
            
            # Check if conversion succeeded
            if pd.isna(dt):
                return Token(
                    value=torch.zeros(12, dtype=torch.float32),
                    status=TokenStatus.UNKNOWN,
                )
            
            # Extract features
            features = self._extract_features(dt)
            
            # Convert to tensor
            features_tensor = torch.from_numpy(features)
            
            return Token(
                value=features_tensor,
                status=TokenStatus.OK,
            )
            
        except Exception as e:
            logger.debug(f"TimestampCodec.tokenize failed for value {value}: {e}")
            return Token(
                value=torch.zeros(12, dtype=torch.float32),
                status=TokenStatus.UNKNOWN,
            )
    
    def detokenize(self, token: Token):
        """
        Detokenize a timestamp token back to a datetime.
        
        Args:
            token: Token with feature vector as value
            
        Returns:
            pandas Timestamp or datetime object
        """
        if (
            token.status == TokenStatus.NOT_PRESENT
            or token.status == TokenStatus.UNKNOWN
        ):
            raise ValueError(f"Cannot detokenize a token with status {token.status}")
        
        # Extract features from token value
        # token.value should be a tensor of shape [12]
        if isinstance(token.value, torch.Tensor):
            features = token.value.cpu().numpy()
        else:
            features = np.array(token.value)
        
        # Features: [seconds, minutes, hours, day_of_month, day_of_week, month, year,
        #            day_of_year, week_of_year, timezone, year_since_2000, year_since_2020]
        seconds = int(round(features[0]))
        minutes = int(round(features[1]))
        hours = int(round(features[2]))
        day_of_month = int(round(features[3]))
        month = int(round(features[5]))
        year = int(round(features[6]))
        timezone_offset = features[9]  # Hours offset from UTC
        
        # Clamp values to valid ranges
        seconds = max(0, min(59, seconds))
        minutes = max(0, min(59, minutes))
        hours = max(0, min(23, hours))
        day_of_month = max(1, min(31, day_of_month))
        month = max(1, min(12, month))
        year = max(1900, min(2100, year))  # Reasonable year range
        
        # Create datetime from features
        try:
            dt = pd.Timestamp(
                year=year,
                month=month,
                day=day_of_month,
                hour=hours,
                minute=minutes,
                second=seconds
            )
            
            # Apply timezone offset if present
            if timezone_offset != 0:
                from datetime import timedelta
                dt = dt + timedelta(hours=timezone_offset)
            
            return dt
        except Exception as e:
            logger.warning(f"Failed to reconstruct datetime from features: {e}, features: {features}")
            # Fallback: use year, month, day only
            try:
                return pd.Timestamp(year=year, month=month, day=day_of_month)
            except Exception:
                # Last resort: return epoch
                return pd.Timestamp(0)
    
    @property
    def token_dtype(self):
        return torch.float32

