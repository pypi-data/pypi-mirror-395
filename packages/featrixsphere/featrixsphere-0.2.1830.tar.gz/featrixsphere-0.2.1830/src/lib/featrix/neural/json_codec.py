#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import json
import logging
import math
import traceback
import torch
import torch.nn as nn
import numpy as np

from featrix.neural.device import device
from featrix.neural.featrix_token import Token, TokenStatus, set_not_present
from featrix.neural.model_config import ColumnType
from featrix.neural.json_cache import JsonCache

# Import logging configuration
from featrix.neural.logging_config import configure_logging
configure_logging()

logger = logging.getLogger(__name__)

# JSON embeddings will be the same dimension as string embeddings for now
JSON_DIM = 384  # Same as STRING_DIM


class JsonCodec(nn.Module):
    """
    Codec for JSON columns that uses embedding spaces to encode JSON values.
    Similar to StringCodec but uses ES-based encoding via JsonCache.
    """
    
    def __init__(self, enc_dim: int, debugName=None, initial_values=None, 
                 json_cache_filename: str=None, embedding_space=None, 
                 schema_fields: list=None, child_es_session_id: str = None):
        super().__init__()
        assert enc_dim > 0
        assert debugName is not None, "We need debugName for the JSON cache -- pass in the col name"
        
        self._numEncodeCalls = 0
        self.colName = debugName
        self._is_decodable = False
        self.debug_name = "%50s" % str(debugName)
        self.enc_dim = enc_dim
        self.d_json_model = JSON_DIM
        
        # Store cache filename for reconnection after unpickling
        self._json_cache_filename = json_cache_filename
        
        # Store embedding space and schema for cache (legacy support)
        self._embedding_space = embedding_space
        self._schema_fields = schema_fields or []
        self._child_es_session_id = child_es_session_id
        
        logger.info(f"🔗 JsonCodec using JSON cache: {json_cache_filename or 'default'}")
        logger.info(f"🔍 JSONCODEC DEBUG: json_cache_filename = {json_cache_filename}")
        logger.info(f"🔍 JSONCODEC DEBUG: debugName = {debugName}")
        logger.info(f"🔍 JSONCODEC DEBUG: initial_values count = {len(initial_values) if initial_values else 0}")
        logger.info(f"🔍 JSONCODEC DEBUG: schema_fields = {schema_fields}")
        if child_es_session_id:
            logger.info(f"🔍 JSONCODEC DEBUG: child_es_session_id = {child_es_session_id}")
        
        # Create JSON cache
        self.json_cache = JsonCache(
            column_name=debugName,
            json_cache_filename=json_cache_filename,
            embedding_space=embedding_space,  # Legacy support
            schema_fields=schema_fields,
            child_es_session_id=child_es_session_id  # Use child ES via API
        )
        
        # Pre-cache initial values if provided
        if initial_values:
            logger.info(f"🔥 Pre-caching {len(initial_values)} JSON values for column '{debugName}'")
            self.json_cache.run_batch(initial_values)
        
        # Projection layer: [JSON_DIM] → [enc_dim]
        # This allows us to use ES embeddings (which might be different dimension) 
        # and project to the desired encoding dimension
        self.projection = nn.Sequential(
            nn.Linear(JSON_DIM, enc_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
        )
        
        # Initialize weights
        for name, param in self.projection.named_parameters():
            if 'weight' in name and param.ndim >= 2:
                nn.init.xavier_uniform_(param, gain=0.5)
            elif 'bias' in name:
                nn.init.zeros_(param)
        
        logger.info(f"🔧 JsonCodec '{debugName}': JSON_DIM={JSON_DIM} → enc_dim={enc_dim}")
    
    def __getstate__(self):
        """Exclude cache and embedding space from pickle (they'll be reconnected)."""
        state = self.__dict__.copy()
        state.pop("json_cache", None)
        state.pop("_embedding_space", None)
        return state
    
    def __setstate__(self, state):
        """Restore state and reconnect to JSON cache."""
        self.__dict__.update(state)
        
        # Reconnect to JSON cache
        cache_filename = getattr(self, '_json_cache_filename', None)
        debug_name = getattr(self, 'debug_name', getattr(self, 'colName', 'restored_codec'))
        schema_fields = getattr(self, '_schema_fields', [])
        
        logger.info(f"🔄 JsonCodec reconnecting to JSON cache: {cache_filename or 'default'}")
        
        try:
            self.json_cache = JsonCache(
                column_name=debug_name.strip(),
                json_cache_filename=cache_filename,
                embedding_space=None,  # Will be set when ES is available
                schema_fields=schema_fields
            )
            logger.info(f"✅ JsonCodec reconnected to JSON cache successfully")
        except Exception as e:
            logger.warning(f"⚠️ Failed to reconnect to JSON cache: {e}")
            self.json_cache = None
    
    def set_embedding_space(self, embedding_space):
        """Set the embedding space for encoding JSON values."""
        self._embedding_space = embedding_space
        if self.json_cache:
            self.json_cache.embedding_space = embedding_space
            logger.info(f"✅ JsonCodec '{self.colName}': Updated embedding space")
    
    def get_codec_name(self):
        return ColumnType.JSON
    
    def get_not_present_token(self):
        tok = self.tokenize({})
        return set_not_present(tok)
    
    def get_marginal_token(self):
        """Return a token representing a masked/marginal value."""
        tok = self.tokenize({})
        return Token(
            value=tok.value,
            status=TokenStatus.MARGINAL,
        )
    
    @property
    def token_dtype(self):
        return float
    
    def _safe_parse_json(self, value):
        """Safely parse JSON value (dict, list of dicts, or string)."""
        if value is None:
            return {}
        
        # If already a dict or list, return as-is
        if isinstance(value, dict):
            return value
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            return value[0]  # Use first dict for encoding
        
        # If string, try to parse
        if isinstance(value, str):
            value = value.strip()
            if not value or value == "nan":
                return {}
            
            # Try JSON parsing
            try:
                parsed = json.loads(value)
                if isinstance(parsed, dict):
                    return parsed
                if isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], dict):
                    return parsed[0]
            except (json.JSONDecodeError, TypeError):
                pass
            
            # Try ast.literal_eval for Python literals
            try:
                import ast
                parsed = ast.literal_eval(value)
                if isinstance(parsed, dict):
                    return parsed
                if isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], dict):
                    return parsed[0]
            except (ValueError, SyntaxError):
                pass
        
        # Fallback: return empty dict
        return {}
    
    def tokenize(self, value):
        """Tokenize a JSON value by encoding it using the embedding space."""
        try:
            # Handle NaN/None
            isNan = False
            if value is None:
                isNan = True
            elif isinstance(value, (float, int, np.float64, np.float32)):
                if math.isnan(value):
                    isNan = True
            
            if isNan:
                # Keep on CPU for DataLoader workers
                result = Token(
                    value=torch.zeros(JSON_DIM, dtype=torch.float32),
                    status=TokenStatus.NOT_PRESENT,
                )
                return result
            
            # Parse JSON value
            json_dict = self._safe_parse_json(value)
            
            # Get embedding from cache (which uses ES if available)
            if self.json_cache:
                embedding = self.json_cache.get_embedding_from_cache(json_dict, add_if_missing=True)
            else:
                logger.warning(f"JsonCodec '{self.colName}': No JSON cache available, using zero embedding")
                # Keep on CPU for DataLoader workers
                embedding = torch.zeros(JSON_DIM, dtype=torch.float32)
            
            # Ensure embedding is on correct device and has correct shape
            if embedding is None:
                # Keep on CPU for DataLoader workers
                embedding = torch.zeros(JSON_DIM, dtype=torch.float32)
            
            # Ensure shape is [JSON_DIM]
            if len(embedding.shape) > 1:
                embedding = embedding.squeeze(0)
            if embedding.shape[0] != JSON_DIM:
                logger.warning(f"JsonCodec '{self.colName}': Embedding dimension mismatch: {embedding.shape[0]} != {JSON_DIM}")
                # Keep on CPU for DataLoader workers
                embedding = torch.zeros(JSON_DIM, dtype=torch.float32)
            
            # Project to encoding dimension
            projected = self.projection(embedding.unsqueeze(0)).squeeze(0)
            
            result = Token(value=projected, status=TokenStatus.OK)
            assert result.value.dtype == torch.float32, f"Token value is {result.value.dtype}, expected float32"
            return result
            
        except Exception as e:
            logger.error(f"🚨 JSON TOKENIZATION FAILED for value: {repr(value)}")
            logger.error(f"   Error: {e}")
            traceback.print_exc()
            # Keep on CPU for DataLoader workers
            return Token(
                value=torch.zeros(self.enc_dim, dtype=torch.float32),
                status=TokenStatus.UNKNOWN,
            )
    
    def encode(self, token_batch):
        """
        Encode a batch of tokens.
        For JSON, we just extract the values since tokenize() already does the encoding.
        """
        if isinstance(token_batch, dict):
            # Extract values from token batch dict
            values = [token.value for token in token_batch.values()]
            if len(values) == 0:
                # Keep on CPU for DataLoader workers
                return torch.zeros(0, self.enc_dim, dtype=torch.float32)
            return torch.stack(values)
        elif isinstance(token_batch, list):
            # List of tokens
            values = [token.value for token in token_batch]
            if len(values) == 0:
                # Keep on CPU for DataLoader workers
                return torch.zeros(0, self.enc_dim, dtype=torch.float32)
            return torch.stack(values)
        else:
            # Single token
            return token_batch.value.unsqueeze(0)


class JsonEncoder(nn.Module):
    """
    Encoder for JSON columns.
    Since JsonCodec.tokenize() already produces the final embedding,
    this encoder just extracts values from tokens.
    """
    
    def __init__(self, config, codec):
        super().__init__()
        self.config = config
        self.codec = codec
        self.d_model = config.d_out
    
    def forward(self, token_batch):
        """
        Forward pass: extract embeddings from tokens.
        
        Args:
            token_batch: Batch of tokens (dict, list, or single token)
            
        Returns:
            short_vec: 3D embedding for visualization
            full_vec: Full embedding for training
        """
        # Extract embeddings from tokens
        if isinstance(token_batch, dict):
            values = [token.value for token in token_batch.values()]
            if len(values) == 0:
                batch_size = 0
            else:
                batch_size = len(values)
                embeddings = torch.stack(values)
        elif isinstance(token_batch, list):
            values = [token.value for token in token_batch]
            if len(values) == 0:
                batch_size = 0
            else:
                batch_size = len(values)
                embeddings = torch.stack(values)
        else:
            # Single token
            batch_size = 1
            embeddings = token_batch.value.unsqueeze(0)
        
        if batch_size == 0:
            # Keep on CPU for DataLoader workers
            zero_embedding = torch.zeros(0, self.d_model, dtype=torch.float32)
            return zero_embedding[:, 0:3], zero_embedding
        
        # Ensure embeddings are the right shape
        if len(embeddings.shape) == 1:
            embeddings = embeddings.unsqueeze(0)
        
        # Extract short (3D) and full embeddings
        short_vec = embeddings[:, 0:3] if embeddings.shape[1] >= 3 else embeddings
        full_vec = embeddings
        
        return short_vec, full_vec

