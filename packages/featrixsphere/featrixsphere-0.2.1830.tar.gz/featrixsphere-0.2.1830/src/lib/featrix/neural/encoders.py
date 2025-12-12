#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import logging
import math
import os
import random
from typing import Dict

import pandas as pd
import torch
import torch.nn.functional as F
from pydantic import BaseModel
from torch import nn

from featrix.neural.device import device
from featrix.neural.featrix_token import TokenStatus
from featrix.neural.featrix_module_dict import FeatrixModuleDict
from featrix.neural.model_config import ColumnEncoderConfigType
from featrix.neural.model_config import ColumnType
from featrix.neural.model_config import FeatrixTableEncoderConfig
from featrix.neural.model_config import JointEncoderConfig
from featrix.neural.model_config import SimpleMLPConfig
from featrix.neural.scalar_codec import ScalarCodec
from featrix.neural.scalar_codec import ScalarEncoder
from featrix.neural.set_codec import SetCodec
from featrix.neural.set_codec import SetEncoder
from featrix.neural.setlist_codec import ListOfASetEncoder
from featrix.neural.setlist_codec import ListsOfASetCodec
from featrix.neural.simple_mlp import SimpleMLP
# from featrix.neural.stopwatch import StopWatch
from featrix.neural.string_codec import StringCodec
from featrix.neural.string_codec import StringEncoder
from featrix.neural.transformer_encoder import JointEncoder
from featrix.neural.vector_codec import VectorCodec
from featrix.neural.vector_codec import VectorEncoder

logger = logging.getLogger(__name__)


# FIXME: I think these functions can all go away by standardizing the Codec
# FIXME: constructor to (df_col, detector) and let the codec ask the detector
# FIXME: for whatever it needs--uniques, metadata will have been calculated by
# FIXME: the detector. [MH 27 Sep 2023]
def create_set_codec(df_col, embed_dim, loss_type="cross_entropy", detector=None, string_cache=None, vocabulary_override=None):
    """
    Create a SetCodec for a column.
    
    Args:
        df_col: DataFrame column to extract vocabulary from
        embed_dim: Embedding dimension
        loss_type: Loss type for training
        detector: Column detector (for sparsity info)
        string_cache: String cache path for semantic initialization
        vocabulary_override: Optional set of vocabulary members to use instead of extracting from df_col.
                            This is used when reconstructing from checkpoint to ensure vocabulary matches.
    """
    # If vocabulary override is provided, use it directly (for checkpoint reconstruction)
    if vocabulary_override is not None:
        uniques = set(vocabulary_override)
        logger.debug(f"   Using vocabulary override: {len(uniques)} members")
    else:
        # Convert all values in the column to strings.
        # TODO: how will this affect encoding values from other dataframes
        # that have the same column? We will need to make sure the same pre-processing
        # is applied to both.
        df_col = df_col.astype(str)
        
        # CRITICAL: Normalize numeric strings to prevent "1" vs "1.0" from being different classes
        # This ensures that 1, 1.0, "1", "1.0" all become "1"
        def normalize_numeric_string(val):
            if pd.isna(val) or val in ['nan', 'NaN', 'None', '', ' ']:
                return val
            try:
                # Try to convert to float, then back to int if it's a whole number
                float_val = float(val)
                if float_val.is_integer():
                    return str(int(float_val))
                return str(float_val)
            except (ValueError, TypeError):
                # Not numeric, return as-is
                return str(val)
        
        df_col_normalized = df_col.apply(normalize_numeric_string)
        uniques = set(df_col_normalized.unique())
    
    # Calculate sparsity ratio from detector (if available) or from data
    sparsity_ratio = 0.0
    if detector is not None and hasattr(detector, '_numNulls'):
        # Use pre-calculated null counts from detector
        total_count = detector._numNulls + detector._numNotNulls
        if total_count > 0:
            sparsity_ratio = float(detector._numNulls) / float(total_count)
    else:
        # Fallback: calculate from data (for backward compatibility)
        null_values = {"nan", "NaN", "Nan", "NAN", "None", "none", "NONE", "", " "}
        null_count = df_col.isin(null_values).sum()
        total_count = len(df_col)
        sparsity_ratio = float(null_count / total_count) if total_count > 0 else 0.0
    
    # print("@@@@@@@ uniques = ", uniques)
    return SetCodec(uniques, embed_dim, loss_type=loss_type, sparsity_ratio=sparsity_ratio, string_cache=string_cache)


def create_scalar_codec(df_col, embed_dim):
    # Convert scalar columns to floats.
    # This converts nan values to float("nan").
    df_col = df_col.astype(float, errors="ignore")
    
    # Compute rich statistics for adaptive encoding
    df_clean = df_col.dropna()
    
    if len(df_clean) == 0:
        # All NaN column - use dummy stats
        stats = {
            'mean': 0.0,
            'std': 1.0,
            'median': 0.0,
            'q10': 0.0,
            'q90': 1.0,
            'q25': 0.0,
            'q75': 1.0,
            'min': 0.0,
            'max': 1.0,
        }
    else:
        stats = {
            'mean': float(df_clean.mean()),
            'std': float(df_clean.std()) if len(df_clean) > 1 else 1.0,
            'median': float(df_clean.median()),
            'q10': float(df_clean.quantile(0.10)),
            'q90': float(df_clean.quantile(0.90)),
            'q25': float(df_clean.quantile(0.25)),
            'q75': float(df_clean.quantile(0.75)),
            'min': float(df_clean.min()),
            'max': float(df_clean.max()),
        }
    
    return ScalarCodec(stats, embed_dim)


def create_timestamp_codec(df_col, embed_dim):
    """
    Create a TimestampCodec for timestamp columns.
    
    Args:
        df_col: DataFrame column with datetime values
        embed_dim: Embedding dimension
        
    Returns:
        TimestampCodec instance
    """
    from featrix.neural.timestamp_codec import TimestampCodec
    return TimestampCodec(enc_dim=embed_dim)


# def create_lists_of_a_set_codec(df_col, detector, embed_dim):
#     df_col = df_col.astype(str)
#     uniques = set(df_col.unique())
#     return ListsOfASetCodec(uniques, detector.get_delimiter(), embed_dim)


def create_string_codec(df_col, detector, embed_dim, string_cache, sentence_model=None, validation_df_col=None):
    """
    Create StringCodec with adaptive string analysis.
    
    Analyzes the column to detect:
    - Random strings (UUIDs, hashes) → mark as random
    - Delimited fields ("a,b,c") → preprocess with newlines
    - Null variants ("N/A", "none") → handled by semantic similarity
    
    Args:
        df_col: DataFrame column from training data
        detector: Column detector
        embed_dim: Embedding dimension
        string_cache: Path to string cache
        sentence_model: BERT model for analysis (optional)
        validation_df_col: Optional DataFrame column from validation data (to ensure all values are cached)
    """
    from featrix.neural.string_analysis import (
        precompute_string_properties,
        detect_random_strings,
        detect_delimiter
    )
    
    col_name = detector._debugColName
    
    # Precompute all expensive operations once
    logger.info(f"🔍 Analyzing string column: '{col_name}'")
    precomputed = precompute_string_properties(df_col, col_name, sentence_model)
    
    # Check if random (UUIDs, hashes, transaction IDs)
    random_result = detect_random_strings(precomputed)
    is_random = random_result["is_random"]
    
    if is_random:
        logger.warning(f"   🚫 RANDOM STRING DETECTED (confidence: {random_result['confidence']:.2f})")
        logger.warning(f"      Signals: {', '.join(random_result['signals'][:3])}")
        logger.warning(f"      → Creating codec with ZERO contribution")
    
    # Check for delimiters - controlled by config.json
    from featrix.neural.sphere_config import get_config
    if get_config().use_delimiter_preprocessing():
        delimiter_result = detect_delimiter(precomputed)
        delimiter = delimiter_result["delimiter"] if delimiter_result["has_delimiter"] else None
        
        if delimiter:
            logger.info(f"   🔧 DELIMITER DETECTED: '{delimiter}' → will preprocess strings before BERT encoding")
    else:
        delimiter = None
        logger.debug(f"   Delimiter preprocessing disabled (config.json: use_delimiter_preprocessing=false)")
    
    # Collect unique values from BOTH training and validation data
    # This ensures all values encountered during training are cached
    train_unique_values = df_col.dropna().astype(str).unique().tolist()
    
    # Also collect from validation data if provided
    if validation_df_col is not None:
        val_unique_values = validation_df_col.dropna().astype(str).unique().tolist()
        # Combine and deduplicate
        all_unique_values = list(set(train_unique_values + val_unique_values))
        train_count = len(train_unique_values)
        val_count = len(val_unique_values)
        logger.info(f"   📊 Collected {train_count} unique values from training, {val_count} from validation")
        logger.info(f"   📊 Total unique values: {len(all_unique_values)} (after deduplication)")
    else:
        all_unique_values = train_unique_values
        logger.info(f"   📊 Collected {len(all_unique_values)} unique values from training data")
    
    # Apply delimiter preprocessing to cache keys (must match tokenize() behavior)
    if delimiter:
        from featrix.neural.string_analysis import preprocess_delimited_string
        preprocessed_values = [preprocess_delimited_string(v, delimiter) for v in all_unique_values]
        logger.info(f"   📊 Caching {len(preprocessed_values)} unique values (delimiter-preprocessed)")
    else:
        preprocessed_values = all_unique_values
        logger.info(f"   📊 Caching {len(preprocessed_values)} unique values (no delimiter preprocessing)")
    
    # Create codec with preprocessed initial values for cache
    codec = StringCodec(
        enc_dim=embed_dim,
        debugName=col_name,
        initial_values=preprocessed_values,  # Preprocessed to match tokenize() lookup keys
        string_cache=string_cache,
        delimiter=delimiter,  # Codec will apply same preprocessing during tokenize()
        is_random_column=is_random
    )
    
    # Store adaptive analysis for encoder config selection
    codec._adaptive_analysis = {
        "precomputed": precomputed,
        "is_random": is_random,
        "delimiter": delimiter,
    }
    
    return codec


def create_vector_codec(df_col, detector, embed_dim):
    in_dim_len = detector.get_input_embedding_length()
    return VectorCodec(
        in_dim=in_dim_len,
        enc_dim=embed_dim,
        # bert_encoding_length=bl,
        debugName=detector._debugColName,
    )


def create_url_codec(df_col, detector, embed_dim, string_cache):
    """
    Create URLCodec for URL/domain columns.
    
    Args:
        df_col: DataFrame column containing URLs
        detector: Column detector
        embed_dim: Embedding dimension
        string_cache: StringCache for encoding domain/path components
    """
    from featrix.neural.url_codec import URLCodec
    
    col_name = detector._debugColName
    logger.info(f"🌐 Creating URL codec for column: '{col_name}'")
    
    codec = URLCodec(
        embed_dim=embed_dim,
        string_cache=string_cache,
        debugName=col_name
    )
    
    return codec


def create_domain_codec(df_col, detector, embed_dim, string_cache):
    """
    Create DomainCodec for domain name columns.
    
    Args:
        df_col: DataFrame column containing domain names
        detector: Column detector
        embed_dim: Embedding dimension
        string_cache: StringCache for encoding domain components
    """
    from featrix.neural.domain_codec import DomainCodec
    
    col_name = detector._debugColName
    logger.info(f"🌐 Creating domain codec for column: '{col_name}'")
    
    # DomainCodec needs a StringCache instance, not just a filename
    # If string_cache is a string (filename), we need to create a StringCache
    if isinstance(string_cache, str):
        from featrix.neural.string_cache import StringCache
        cache_instance = StringCache(string_cache_filename=string_cache, readonly=False)
    else:
        cache_instance = string_cache
    
    codec = DomainCodec(
        enc_dim=embed_dim,
        string_cache=cache_instance,
        debugName=col_name
    )
    
    return codec


def create_json_codec(df_col, detector, embed_dim, json_cache_filename=None, child_es_session_id: str = None):
    """
    Create JsonCodec with ES lookup for JSON columns.
    
    Extracts schema fields from JSON values, queries API for matching ES,
    and creates JsonCodec with the ES if found.
    
    Args:
        df_col: DataFrame column with JSON values
        detector: Column detector
        embed_dim: Embedding dimension
        json_cache_filename: Path to JSON cache file
        child_es_session_id: Session ID of child ES to use for encoding (via API)
        
    Returns:
        JsonCodec instance
    """
    from featrix.neural.json_codec import JsonCodec
    import json
    import ast
    from collections import Counter
    
    col_name = detector._debugColName if hasattr(detector, '_debugColName') else "json_col"
    
    # Extract schema fields from JSON values
    schema_fields = set()
    sample_values = df_col.dropna().head(100)  # Sample first 100 non-null values
    
    for value in sample_values:
        try:
            # Parse JSON value
            if isinstance(value, str):
                value = value.strip()
                if value.startswith('{'):
                    try:
                        parsed = json.loads(value)
                    except:
                        try:
                            parsed = ast.literal_eval(value)
                        except:
                            continue
                elif value.startswith('['):
                    try:
                        parsed = json.loads(value)
                        if isinstance(parsed, list) and len(parsed) > 0:
                            parsed = parsed[0]  # Use first dict
                    except:
                        try:
                            parsed = ast.literal_eval(value)
                            if isinstance(parsed, list) and len(parsed) > 0:
                                parsed = parsed[0]
                        except:
                            continue
                else:
                    continue
            elif isinstance(value, dict):
                parsed = value
            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                parsed = value[0]
            else:
                continue
            
            # Extract keys from dict
            if isinstance(parsed, dict):
                schema_fields.update(parsed.keys())
        except Exception:
            continue
    
    schema_fields = sorted(list(schema_fields))
    logger.info(f"🔍 JsonCodec '{col_name}': Extracted {len(schema_fields)} schema fields: {schema_fields[:10]}{'...' if len(schema_fields) > 10 else ''}")
    
    # Query API for matching ES
    embedding_space = None
    if schema_fields:
        try:
            import requests
            from config import config as app_config
            
            # Build API URL
            api_base = getattr(app_config, 'api_base_url', 'http://localhost:8000')
            if not api_base.startswith('http'):
                api_base = f"http://{api_base}"
            
            # Query endpoint
            schema_fields_str = ','.join(schema_fields)
            url = f"{api_base}/api-sphere/json-encoders"
            params = {"schema_fields": schema_fields_str}
            
            logger.info(f"🔍 Querying JSON encoder API: {url} with fields: {schema_fields_str}")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                matched_es = result.get("matched_es")
                
                if matched_es:
                    es_path = matched_es.get("embedding_space_path")
                    logger.info(f"✅ Found matching ES: {matched_es.get('name')} at {es_path}")
                    
                    # Load embedding space
                    try:
                        import pickle
                        with open(es_path, 'rb') as f:
                            embedding_space = pickle.load(f)
                        logger.info(f"✅ Loaded embedding space for JsonCodec '{col_name}'")
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to load ES from {es_path}: {e}")
                else:
                    logger.info(f"ℹ️ No matching ES found for schema: {schema_fields}")
            else:
                logger.warning(f"⚠️ API query failed with status {response.status_code}: {response.text}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to query JSON encoder API: {e}")
            import traceback
            logger.debug(traceback.format_exc())
    
    # Get initial values for caching
    initial_values = df_col.dropna().tolist()[:1000]  # Limit to first 1000 for caching
    
    # Create JsonCodec
    # Prefer child_es_session_id over embedding_space (for API calls)
    codec = JsonCodec(
        enc_dim=embed_dim,
        debugName=col_name,
        initial_values=initial_values,
        json_cache_filename=json_cache_filename,
        embedding_space=embedding_space if not child_es_session_id else None,  # Only use local ES if no child ES session
        schema_fields=schema_fields,
        child_es_session_id=child_es_session_id
    )
    
    return codec


class LayerEncoder(nn.Module):
    def __init__(self, segments):
        super().__init__()

        modules, input_lengths = list(zip(*segments))
        self.layer_modules = nn.ModuleList(modules)
        self.input_lengths = input_lengths

        self.total_length = sum(self.input_lengths)

    def forward(self, input):
        assert input.shape[1] == self.total_length, (
            "input.shape = %s; total_length = %s; input_lengths = %s"
            % (
                input.shape,
                self.total_length,
                self.input_lengths,
            )
        )

        segments = torch.split(input, self.input_lengths, dim=1)
        encodings = [
            module(segment) for module, segment in zip(self.layer_modules, segments)
        ]

        return torch.cat(encodings, dim=1)


class ColumnEncoders(nn.Module):
    # This is the first layer that takes in a dictionary-like batch, and
    # returns a completely vectorized batch.

    # NOTE: col_order can contain duplicates, e.g. when the same columns is
    # fed into multiple encoders.

    def __init__(self, col_configs, col_order, col_types, col_codecs):
        super().__init__()

        self.col_order = col_order

        self.encoders = FeatrixModuleDict()
        for col_name, col_type in col_types.items():
            col_config = col_configs[col_name]
            if col_type == ColumnType.SET:
                # Pass column_name for semantic initialization
                codec = col_codecs.get(col_name)
                member_names = codec.member_names if hasattr(codec, 'member_names') else None
                # ALWAYS get string cache for semantic initialization (make all SetEncoders adaptive)
                from featrix.neural.string_codec import get_global_string_cache
                # Try to get string cache from codec, or use default global cache
                cache_filename = None
                if hasattr(codec, 'string_cache') and codec.string_cache:
                    cache_filename = codec.string_cache
                # Always get the global string cache object (will use default if filename is None)
                string_cache_obj = get_global_string_cache(
                    cache_filename=cache_filename,
                    initial_values=None,  # Values already cached during codec creation
                    debug_name=col_name
                )
                encoder = SetEncoder(col_config, string_cache=string_cache_obj, column_name=col_name, member_names=member_names)
            elif col_type == ColumnType.SCALAR:
                # Use AdaptiveScalarEncoder with stats from codec
                codec = col_codecs[col_name]
                from featrix.neural.scalar_codec import AdaptiveScalarEncoder
                encoder = AdaptiveScalarEncoder(codec.stats, col_config.d_out, column_name=col_name)
            elif col_type == ColumnType.TIMESTAMP:
                # Use TimestampEncoder
                from featrix.neural.timestamp_codec import TimestampEncoder
                encoder = TimestampEncoder(col_config, column_name=col_name)
            elif col_type == ColumnType.FREE_STRING:
                encoder = StringEncoder(col_config, column_name=col_name)
            elif col_type == ColumnType.LIST_OF_A_SET:
                encoder = ListOfASetEncoder(col_config)
            elif col_type == ColumnType.VECTOR:
                encoder = VectorEncoder(col_config)
            elif col_type == ColumnType.URL:
                # URL codec handles its own encoding, just pass through
                codec = col_codecs[col_name]
                encoder = codec.encoder
            elif col_type == ColumnType.JSON:
                # JSON codec handles its own encoding via embedding space
                # The codec's tokenize() already produces the final embedding
                # We just need a pass-through encoder
                from featrix.neural.json_codec import JsonEncoder
                codec = col_codecs[col_name]
                encoder = JsonEncoder(col_config, codec)

            self.encoders[col_name] = encoder

    def forward(self, batch_data):
        short_encoding_list = []
        full_encoding_list = []
        
        # DEBUG: Log column order and batch data to diagnose empty tensor list
        import logging
        logger = logging.getLogger(__name__)
        if len(self.col_order) == 0:
            logger.error(f"💥 CRITICAL: col_order is EMPTY! No columns to encode!")
            logger.error(f"   Available encoders: {list(self.encoders.keys())}")
            logger.error(f"   Batch data columns: {list(batch_data.keys())}")
            
        for col_name in self.col_order:
            col_data = batch_data[col_name]
            encoder = self.encoders[col_name]
            short_col_encoding, full_col_encoding = encoder(col_data)
            short_encoding_list.append(short_col_encoding)
            full_encoding_list.append(full_col_encoding)

        # create a tensor with all the token statuses
        # this is effectively a mask with multiple possible values
        status_list = [batch_data[col_name].status for col_name in self.col_order]

        # return torch.stack(encoding_list, dim=1), torch.stack(status_list, dim=1)
        return short_encoding_list, full_encoding_list, status_list


class NormalizedPoolJointEncoder(nn.Module):
    """Simplest possible joint encoder."""

    def forward(self, batch):
        # Batch is a tensor of dimensions (b, n, d)
        # use keepdim=True to retain the fact that the output is a sequence of length 1
        return nn.functional.normalize(torch.sum(batch, dim=1, keepdim=True), dim=-1)


class PassThroughJointEncoder(nn.Module):
    def forward(self, batch):
        return batch


# def sample_marginal_masks(batch_mask):
#     new_mask_A = batch_mask.clone()  # Clone the original mask to create a new mask
#     new_mask_B = batch_mask.clone()

#     for i in range(batch_mask.size(0)):  # Iterate over rows
#         # Find indices where mask is not NOT_PRESENT
#         # The output looks something like
#         # This gives the indices in the row that are NOT equal to NOT_PRESENT
#         # This means that these are the indices that CAN be masked out
#         # For a row equal to [TokenStatus.NOT_PRESENT, TokenStatus.OK, TokenStatus.OK, TokenStatus.NOT_PRESENT],
#         # present will be torch.tensor([1, 2])
#         present = torch.nonzero(
#             batch_mask[i] != TokenStatus.NOT_PRESENT, as_tuple=True
#         )[0]

#         # If there is only one present token (or zero), leave the mask row as-is.
#         if len(present) > 1:
#             # Make sure at least one present token is left unmasked
#             max_selected = len(present) - 1
#             # Randomly choose number of elements to select for masking in one of the returned masks.
#             # we want to select at least one token to mask because otherwise the second mask will have no unmasked tokens.
#             min_selected = 1
#             num_to_select = random.randint(min_selected, max_selected)

#             # Randomly select indices
#             # Make sure that masks A and B are complimentary - i.e. a token that is masked in one is not masked in the other.
#             permutation = torch.randperm(len(present))
#             selected_indices_A = present[permutation[:num_to_select]]
#             selected_indices_B = present[permutation[num_to_select:]]

#             # Set the status for the selected token to MARGINAL
#             new_mask_A[i, selected_indices_A] = TokenStatus.MARGINAL
#             new_mask_B[i, selected_indices_B] = TokenStatus.MARGINAL

#     return new_mask_A, new_mask_B

# Feature flag: Set to True to use ratio-limited masking strategy
# Old strategy: Random split anywhere from 1 to n-1 columns
# New strategy: Limit masking to 10-30% of columns (better for large datasets)
TRY_NEW_MASKING = True

def sample_marginal_masks(batch_mask):
    # Move the batch mask to the cpu, so we can iterate over rows on the cpu,
    # which eliminates the need to shuffle data back and forth.
    # We move all masks back to the GPU at the end of this function.
    batch_mask = batch_mask.to(torch.device("cpu"))

    # Clone the original mask to create new masks
    new_mask_A = batch_mask.clone()
    new_mask_B = batch_mask.clone()
    
    # Find indices where each row has tokens present
    # present_indices is a tensor, where each row corresponds to an INDIVIDUAL ENTRY
    # in batch_mask that does NOT correspond to a NOT_PRESENT token, and has two elements
    # that represent the index of that element in batch_mask.
    present_indices = (batch_mask != TokenStatus.NOT_PRESENT).nonzero(as_tuple=False)
    rows, cols = present_indices[:, 0], present_indices[:, 1]
    
    # Group by row index and perform vectorized selection of tokens to mask
    unique_rows = torch.unique(rows)
    
    for row in unique_rows:
        # Get the column indices where tokens are present in the current row
        present = cols[rows == row]
        
        if len(present) > 1:
            # Ensure at least one token is left unmasked in one of the masks
            max_selected = len(present) - 1
            
            if TRY_NEW_MASKING:
                # NEW STRATEGY: Limit masking ratio to reasonable range (10-30%)
                # This prevents extreme cases like masking 190/200 columns
                # Inspired by BERT's 15% masking ratio
                min_mask_ratio = 0.10  # At least 10%
                max_mask_ratio = 0.30  # At most 30%
                
                min_to_mask = max(1, int(len(present) * min_mask_ratio))
                max_to_mask = min(max_selected, int(len(present) * max_mask_ratio))
                
                # Ensure valid range
                if min_to_mask > max_to_mask:
                    # Fallback for very small column counts
                    num_to_select = random.randint(1, max_selected)
                else:
                    num_to_select = random.randint(min_to_mask, max_to_mask)
            else:
                # OLD STRATEGY: Random split anywhere from 1 to n-1
                # Can result in very imbalanced masks (e.g., 1:199 or 100:100)
                num_to_select = random.randint(1, max_selected)
            
            # Shuffle the present indices and split them into two groups for masks A and B
            # permutation = torch.randperm(len(present), device=batch_mask.device)
            permutation = torch.randperm(len(present))
            selected_indices_A = present[permutation[:num_to_select]]
            selected_indices_B = present[permutation[num_to_select:]]
            
            # Assign MARGINAL to selected indices in each mask
            new_mask_A[row, selected_indices_A] = TokenStatus.MARGINAL
            new_mask_B[row, selected_indices_B] = TokenStatus.MARGINAL

    # Move everything back to the GPU (or CPU if forced)
    force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
    target_device = torch.device('cpu') if force_cpu else device
    batch_mask = batch_mask.to(target_device)
    new_mask_A = new_mask_A.to(target_device)
    new_mask_B = new_mask_B.to(target_device)

    return new_mask_A, new_mask_B


def apply_replacement_mask(base_tensor, replacement_tensor, replacement_mask):
    # Replaces the entires in base tensor with the corresponding entries in replacement tensor.
    # Which entries are replaced is controlled by the replacement_mask tensor.

    # replacement vectors must be a (B, N, D) tensor
    # that carries replacement vectors for each column in the batch.

    batch_size, n_elements, d_features = base_tensor.shape

    assert replacement_tensor.shape == (batch_size, n_elements, d_features)
    assert replacement_mask.shape == (batch_size, n_elements, 1)

    remain_mask = replacement_mask.logical_not()

    remain = base_tensor * remain_mask
    replace = replacement_tensor * replacement_mask

    return remain + replace


class ColumnPredictor(nn.Module):
    def __init__(self, cols_in_order, col_configs):
        super().__init__()

        self.cols_in_order = cols_in_order
        self.col_predictors = FeatrixModuleDict()
        for col_name, col_config in col_configs.items():
            self.col_predictors[col_name] = SimpleMLP(col_config)

    def forward(self, joint_embeddings):
        predictions = []
        for col_name in self.cols_in_order:
            prediction = self.col_predictors[col_name](joint_embeddings)
            predictions.append(prediction)

        return predictions


class ShortColumnPredictor(nn.Module):
    """Same as ColumnPredictor, but shares a single config across all columns."""

    def __init__(self, cols_in_order, config):
        super().__init__()

        self.cols_in_order = cols_in_order
        self.col_predictors = FeatrixModuleDict()
        for col_name in cols_in_order:
            # This is just for UI and display, so we hard-code the same
            # parameters for all column.
            self.col_predictors[col_name] = SimpleMLP(config)

    def forward(self, joint_embeddings):
        predictions = []
        for col_name in self.cols_in_order:
            prediction = self.col_predictors[col_name](joint_embeddings)
            predictions.append(prediction)

        return predictions


# Should there be different objects for data-space batches (which are per-column, whether tokens or actual data),
# and encoding batches, which are just tensors?
# each tensor batch, as opposed to a column batch, would have values and status_masks, which would be 2D tensors, not
# dictionaries of elements.
# The "collate" function in DataLoader could handle much of the complexity of constructing the batch.


def get_infoNCE_targets(batch_size, shuffle_n=0):
    force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
    target_device = torch.device('cpu') if force_cpu else device
    
    N = batch_size

    tensor = torch.arange(N).to(target_device)  # Tensor: [1, 2, 3, ..., N]

    if shuffle_n < 1:
        return tensor

    # # Set K, the number of elements to shuffle
    K = shuffle_n

    # # Ensure K is not greater than N
    K = min(K, N)

    # # Indices of the last K elements
    last_k_indices = torch.arange(N - K, N).to(target_device)

    # # Generate a random permutation of these indices
    shuffled_indices = last_k_indices[torch.randperm(K)]

    # # Shuffle the last K elements
    tensor[N - K :] = tensor[shuffled_indices]

    return tensor


class FeatrixTableEncoder(nn.Module):
    def __init__(self, col_codecs, config: FeatrixTableEncoderConfig):
        super().__init__()

        self.config = config
        self.d_model = config.d_model

        self.column_encoder = ColumnEncoders(
            config.column_encoders_config, config.cols_in_order, config.col_types, col_codecs
        )

        self.column_predictor = ColumnPredictor(
            cols_in_order=config.cols_in_order,
            col_configs=config.column_predictors_config,
        )
        self.short_column_predictor = ShortColumnPredictor(
            cols_in_order=config.cols_in_order,
            config=config.column_predictors_short_config,
        )

        self.joint_encoder = JointEncoder(
            d_embed=self.d_model,
            col_names_in_order=config.cols_in_order,
            config=config.joint_encoder_config,
        )

        self.joint_predictor = SimpleMLP(config.joint_predictor_config)
        # This is just for UI and display, so we hard-code the parameters here.
        self.joint_predictor_short = SimpleMLP(config.joint_predictor_short_config)

        self.idx_to_col_name = {
            i: col_name for i, col_name in enumerate(config.cols_in_order)
        }
        self.col_mi_estimates = {col_name: None for col_name in config.cols_in_order}
        self.joint_mi_estimate = None

        # TODO: create "column encoders" and "column predictors" as separate models here.
        # That's pretty much the only place they are needed I think.
        # TODO: look into what's being done in SinglePredictor - I think they use the encoders
        self.n_codecs = config.n_cols
        self.column_order = config.cols_in_order
        self.col_codecs_in_order = [
            col_codecs[col_name] for col_name in self.column_order
        ]

        # defines how much noise is applied to the sample embeddings for CPC
        # self.latent_noise = 0.01
        self.latent_noise = 0
        # We do not reduce the loss so that we can mask out loss associated with fields
        # that are NOT_PRESENT (or not in schema).
        self.ce_loss = nn.CrossEntropyLoss(reduction="none")

        # We use separate stopwatches for the encoder and loss computation becase we don't want
        # to have to synchronize the start/stop of stopwatches between encoder and loss
        # computation to retain the flexibility to use them independently, e.g. in testing.
        self.encoder_stopwatch = None #StopWatch()
        self.loss_stopwatch = None #StopWatch()

    def __setstate__(self, state):
        """Force CPU during unpickling to prevent GPU allocation."""
        logger = logging.getLogger(__name__)
        
        # Log GPU memory before unpickling
        if torch.cuda.is_available():
            allocated_before = torch.cuda.memory_allocated() / (1024**3)
            logger.info(f"📊 FeatrixTableEncoder.__setstate__: GPU memory BEFORE: Allocated={allocated_before:.3f} GB")
        
        # Restore state
        self.__dict__.update(state)
        
        # Log GPU memory after unpickling
        if torch.cuda.is_available():
            allocated_after = torch.cuda.memory_allocated() / (1024**3)
            logger.info(f"📊 FeatrixTableEncoder.__setstate__: GPU memory AFTER dict.update: Allocated={allocated_after:.3f} GB")
        
        # CRITICAL: Move everything to CPU if in CPU mode
        force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
        if force_cpu:
            logger.info(f"📊 FeatrixTableEncoder.__setstate__: Moving all components to CPU")
            self.cpu()
            
            # AGGRESSIVE GPU MEMORY CLEANUP
            if torch.cuda.is_available():
                logger.info(f"📊 FeatrixTableEncoder.__setstate__: Aggressively freeing GPU memory...")
                
                # Force garbage collection to free Python references
                import gc
                gc.collect()
                
                # Clear CUDA cache multiple times
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
                
                allocated_after_first_clear = torch.cuda.memory_allocated() / (1024**3)
                logger.info(f"📊 FeatrixTableEncoder.__setstate__: GPU memory after first cache clear: Allocated={allocated_after_first_clear:.3f} GB")
                
                # GC again
                gc.collect()
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
                
                allocated_after_second_clear = torch.cuda.memory_allocated() / (1024**3)
                logger.info(f"📊 FeatrixTableEncoder.__setstate__: GPU memory after second cache clear: Allocated={allocated_after_second_clear:.3f} GB")
                
                # One more time for good measure
                gc.collect()
                torch.cuda.empty_cache()
                
                allocated_final = torch.cuda.memory_allocated() / (1024**3)
                reserved_final = torch.cuda.memory_reserved() / (1024**3)
                logger.info(f"📊 FeatrixTableEncoder.__setstate__: GPU memory FINAL: Allocated={allocated_final:.3f} GB, Reserved={reserved_final:.3f} GB")

    def count_model_parameters(self):
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)

        # Column and joint encoders are the parts of the model involved in inference.
        # "predictors" and encoders for "short" embeddings are not counted because they're
        # not used in inference in production.
        column_encoders_params = sum(
            p.numel() for p in self.column_encoder.parameters()
        )
        column_encoders_trainable_params = sum(
            p.numel() for p in self.column_encoder.parameters() if p.requires_grad
        )

        joint_encoder_params = sum(
            p.numel() for p in self.joint_encoder.parameters() if p.requires_grad
        )
        joint_encoder_trainable_params = sum(
            p.numel() for p in self.joint_encoder.parameters() if p.requires_grad
        )

        return {
            "total_params": total_params,
            "total_trainable_params": trainable_params,
            "column_encoders_params": column_encoders_params,
            "column_encoders_trainable_params": column_encoders_trainable_params,
            "joint_encoder_params": joint_encoder_params,
            "joint_encoder_trainable_params": joint_encoder_trainable_params,
        }

    def get_marginal_tensor(self, batch_size):
        # Create columns of marginal embeddings, one for each codec.
        column_marginal_embeddings_list = [
            # codec.marginal_embedding.repeat(batch_size, 1)
            self.column_encoder.encoders[col_name].marginal_embedding.repeat(
                batch_size, 1
            )
            # for codec in self.col_codecs_in_order
            for col_name in self.column_order
        ]

        # Combine the columns of embeddings into a single tensor.
        # The columns are stacked side-by-side, i.e. along the first dimension.
        column_marginal_embeddings = torch.stack(column_marginal_embeddings_list, dim=1)

        return column_marginal_embeddings

    def apply_marginal_mask(self, tensor, marginal_tensor, mask):
        # We want to replace the vectors that correspond to the MARGINAL tokens in
        # the batch_mask. The batch mask is 2D (batch_size, n_cols) so we add
        # a third dimension to explicity broadcast the mask to the same shape as the
        # tensors whose values need to be replaced.
        replacement_mask = (mask == TokenStatus.MARGINAL).unsqueeze(dim=-1)

        return apply_replacement_mask(
            tensor,
            marginal_tensor,
            replacement_mask,
        )

    def infoNCE_loss(
        self,
        context_enc,
        sample_enc,
        mask=None,
        unknown_targets=False,
        random_fraction=0,
    ):
        sample_enc = sample_enc + torch.randn_like(sample_enc) * self.latent_noise
        sample_enc = nn.functional.normalize(sample_enc, dim=1)

        logits = context_enc @ sample_enc.T

        batch_size = context_enc.shape[0]
        shuffle_n = int(batch_size * random_fraction)
        targets = get_infoNCE_targets(batch_size, shuffle_n=shuffle_n)

        # If the mask indicatest that the token is not present, set
        # the corresponding logit to -inf so it does not affect the loss.
        # The columns in the logits tensor correspond to individual tokens
        # in the column for which we're computing the loss
        if mask is not None:
            # do NOT mask MARGINAL tokens becasuse marginal encodings are not
            # at all related to MARGINAL tokens because these are only
            # created for the joint encoder.

            # select all rows, but only the columns where we did not
            logits[:, mask == TokenStatus.NOT_PRESENT] = float("-inf")

        # NOTE: for columns where ALL the elements are NOT_PRESENT, e.g.
        # because the particular column does not exist in the segment
        # that the batch came from, all the entries in the `logits`
        # tensor will be float("-inf"), and therefore the loss
        # below will be torch.tensor([nan, ..., nan]) where there will
        # be as many `nan`s as there are rows in the batch.

        loss = self.ce_loss(logits, targets)

        return loss

    def compute_spread_loss(
        self, unmasked_encoding, joint_encoding_1, joint_encoding_2, temp=None, temp_multiplier=1.0
    ):
        """
        Compute spread loss with adaptive temperature.
        
        Temperature controls the sharpness of the contrastive learning objective:
        - Lower temp (e.g., 0.01) = sharper, more aggressive separation
        - Higher temp (e.g., 0.1) = softer, more forgiving of nearby embeddings
        
        Args:
            temp: Temperature value. If None, computed adaptively based on batch size and n_columns
            temp_multiplier: Multiplier applied to temperature during NO_LEARNING recovery (default 1.0)
        """
        force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
        target_device = torch.device('cpu') if force_cpu else device
        
        batch_size = unmasked_encoding.shape[0]
        targets = torch.arange(batch_size).to(target_device)
        
        # Compute adaptive temperature if not provided
        if temp is None:
            # Get number of columns from the encoder config
            n_columns = len(self.col_codecs_in_order)
            
            # Adaptive temperature formula:
            # - Scales with batch size: larger batches can handle sharper temp
            # - Scales with data richness: more columns = more discriminative power
            # Base temp of 0.2 (increased from 0.05 to make task harder)
            base_temp = 0.2
            
            # Batch size factor: normalize to batch_size=128
            # Larger batches → lower temp (sharper)
            batch_factor = max(0.5, min(2.0, batch_size / 128.0))
            
            # Column factor: normalize to 20 columns
            # More columns → lower temp (sharper) because embeddings are more discriminative
            column_factor = max(0.5, min(1.5, n_columns / 20.0))
            
            # Compute adaptive temp
            temp = base_temp / (batch_factor * column_factor)
        
        # Apply temp multiplier for NO_LEARNING recovery
        temp = temp * temp_multiplier
        
        # Clamp to reasonable range
        temp = max(0.01, min(0.4, temp))  # Increased max to 0.4 for multiplier support
        
        # Store temperature for logging (convert to float for JSON serialization)
        self._last_spread_temp = float(temp)

        logits_joint = unmasked_encoding @ unmasked_encoding.T / temp
        spread_loss_joint = F.cross_entropy(logits_joint, targets)

        logits_1 = joint_encoding_1 @ joint_encoding_1.T / temp
        spread_loss_1 = F.cross_entropy(logits_1, targets)

        logits_2 = joint_encoding_2 @ joint_encoding_2.T / temp
        spread_loss_2 = F.cross_entropy(logits_2, targets)

        loss_config = self.config.loss_config.spread_loss_config

        total = (
            loss_config.joint_weight * spread_loss_joint
            + loss_config.marginal_weight * spread_loss_1
            + loss_config.marginal_weight * spread_loss_2
        )

        dict = {
            "joint": spread_loss_joint.item(),
            "mask_1": spread_loss_1.item(),
            "mask_2": spread_loss_2.item(),
            "temperature": self._last_spread_temp,
        }

        return total, dict

    def update_col_mi(self, col_name, update_value):
        ema_coeff = 0.99

        old_value = self.col_mi_estimates[col_name]
        if old_value is None:
            new_value = update_value
        else:
            new_value = (1 - ema_coeff) * update_value + ema_coeff * old_value

        self.col_mi_estimates[col_name] = new_value

    def update_joint_mi(self, update_value):
        ema_coeff = 0.99

        if self.joint_mi_estimate is None:
            self.joint_mi_estimate = update_value
        else:
            self.joint_mi_estimate = (
                1 - ema_coeff
            ) * update_value + ema_coeff * self.joint_mi_estimate

    def compute_marginal_infoNCE_loss(
        self,
        batch_size,
        column_predictions,
        column_encodings,
        status_mask,
        update_mi=False,
    ):
        # def compute_marginal_infoNCE_loss(self, marginal_encodings, column_encodings, status_mask):
        """
        column_encodings: a 3D tensor (batch_size, n_cols, d_model)
        column_predictions: list of tensors, each tensor is of shape (batch_size, d_model)
                            There's one tensor per column in the dataset.
        """
        # We ONLY want to focus on predicting marginals that have been replaced in the
        # status mask.
        prediction_mask = status_mask == TokenStatus.MARGINAL

        # Compute the infoNCE loss for each marginal distribution.
        # This requries matching predictions and encodings for each column.
        mean_loss_per_column = []

        # We iterate over the codecs, extrac the relevant predictions and column encodigns, and
        # compute the average loss over the MARGINAL tokens, which signify the predictions we
        # actually need to make
        # for i, codec in enumerate(self.col_codecs_in_order):
        col_losses_dict = dict()
        for i, col_prediction in enumerate(column_predictions):
            # the shape of column_encodings is (batch_size, n_cols, model_dim)
            col_target = column_encodings[:, i, :]
            # mask shape is (batch_size, n_col). The third dimension is not present because
            # the mask is a boolean
            col_status_mask = status_mask[:, i]

            # col_losses is a 1D tensor of losses for each row
            col_losses = self.infoNCE_loss(
                col_prediction, col_target, col_status_mask, unknown_targets=False
            )

            # pick out the losses corresponding to the MARGINAL tokens
            col_prediction_mask = prediction_mask[:, i]
            col_prediction_losses = col_losses[col_prediction_mask]

            col_name = self.idx_to_col_name[i]

            if len(col_prediction_losses) == 0:
                # Make this a tensor for consistency - using a bare float causes issues
                # if we e.g. want to call .item() on it.
                col_loss_avg = torch.tensor(0.0)

                # If there are no predictions, which can happen e.g. for columns that are
                # not present in a particular data segment (for multi-segment datasets),
                # we do not update MI because col_loss_avg=0 is just a neural component
                # when it comes to computing gradients, but it does NOT fit in with the
                # formula used to compute mutual information.
            else:
                # This is where we average the loss across all the MARGINAL tokens,
                # i.e. across all the valid predictions.
                col_loss_avg = torch.mean(col_prediction_losses)

                # This is where we compute the mutual information between column i and the rest of the columns.
                # This is computed twice: once for each of the two "marginal" masks.
                # It can be averaged out between the two masks, so we get just one value per column.
                # if update_mi:
                log_n = math.log(batch_size)
                col_mi = log_n - col_loss_avg.detach().item()
                if update_mi:
                    self.update_col_mi(
                        col_name, col_mi / math.log(2)
                    )  # convert from nats to bits

            col_losses_dict[col_name] = col_loss_avg.detach().item()
            mean_loss_per_column.append(col_loss_avg)

        total = sum(mean_loss_per_column)
        # sum the loss over all columns
        return total, col_losses_dict

    def compute_joint_infoNCE_loss(
        self, joint_encoding, unmasked_encoding, short=False
    ):
        if short:
            prediction = self.joint_predictor_short(joint_encoding)
        else:
            prediction = self.joint_predictor(joint_encoding)
        return self.infoNCE_loss(prediction, unmasked_encoding).mean()

    def compute_total_loss(
        self,
        batch_size,
        #
        full_joint_encodings_unmasked,
        full_joint_encodings_1,
        full_joint_encodings_2,
        #
        full_column_encodings,
        short_column_encodings,
        #
        short_joint_encodings_unmasked,
        short_joint_encodings_1,
        short_joint_encodings_2,
        #
        mask_1,
        mask_2,
        #
        full_column_predictions_1,
        full_column_predictions_2,
        full_column_predictions_unmasked,
        #
        short_column_predictions_1,
        short_column_predictions_2,
        short_column_predictions_unmasked,
        #
        temp_multiplier=1.0
    ):
        # MARGINAL LOSS
        (
            marginal_cpc_loss_1_total,
            marginal_cpc_loss_1_col_dict,
        ) = self.compute_marginal_infoNCE_loss(
            batch_size,
            full_column_predictions_1,
            full_column_encodings,
            mask_1,
            update_mi=True,
        )
        (
            marginal_cpc_loss_2_total,
            marginal_cpc_loss_2_col_dict,
        ) = self.compute_marginal_infoNCE_loss(
            batch_size,
            full_column_predictions_2,
            full_column_encodings,
            mask_2,
            update_mi=True,
        )
        # marginal_cpc_loss_unmasked = self.compute_marginal_infoNCE_loss(
        #     batch_size, full_column_predictions_unmasked, full_column_encodings, torch.ones_like(mask_2) * TokenStatus.OK,
        # )
        (
            short_marginal_cpc_loss_1_total,
            short_marginal_cpc_loss_1_col_dict,
        ) = self.compute_marginal_infoNCE_loss(
            batch_size, short_column_predictions_1, short_column_encodings, mask_1
        )
        (
            short_marginal_cpc_loss_2_total,
            short_marginal_cpc_loss_2_col_dict,
        ) = self.compute_marginal_infoNCE_loss(
            batch_size, short_column_predictions_2, short_column_encodings, mask_2
        )
        # short_marginal_cpc_loss_unmasked = self.compute_marginal_infoNCE_loss(
        #     batch_size, short_column_predictions_unmasked, short_column_encodings, torch.ones_like(mask_2) * TokenStatus.OK,
        # )


        # --- NEW: normalize over 4 views * number of active columns ---
        # each *_total is a SUM over columns of per-column mean InfoNCE.
        # we want an average over views and columns so the magnitude
        # is ~log(batch_size) instead of ~4 * n_cols * log(batch_size)
        # Count active columns in this batch (columns with at least one OK token)
        # This is more precise than using total n_cols when some columns are completely masked out
        n_cols_total = len(self.idx_to_col_name) if hasattr(self, "idx_to_col_name") else full_column_encodings.shape[1]
        
        # Count columns that have at least one OK token in any of the masks
        # mask_1 and mask_2 have shape (batch_size, n_cols)
        # A column is "active" if it has at least one OK token across all rows
        effective_n_cols = n_cols_total
        try:
            if mask_1 is not None and mask_2 is not None:
                # Check mask_1: columns with at least one OK token
                has_ok_mask1 = (mask_1 == TokenStatus.OK).any(dim=0)  # (n_cols,)
                # Check mask_2: columns with at least one OK token
                has_ok_mask2 = (mask_2 == TokenStatus.OK).any(dim=0)  # (n_cols,)
                # A column is active if it has OK tokens in either mask
                active_cols = (has_ok_mask1 | has_ok_mask2)
                effective_n_cols = active_cols.sum().item()
                # Ensure at least 1 column (safety check)
                if effective_n_cols == 0:
                    effective_n_cols = n_cols_total
        except Exception:
            # If counting fails for any reason, fall back to total columns
            effective_n_cols = n_cols_total
        
        # Ensure normalizer is at least 4.0 (for 1 column)
        normalizer = 4.0 * max(1, effective_n_cols)

        marginal_loss_raw = (
            marginal_cpc_loss_1_total
            + marginal_cpc_loss_2_total
            + short_marginal_cpc_loss_1_total
            + short_marginal_cpc_loss_2_total
        )

        marginal_loss = marginal_loss_raw / normalizer

        # marginal_loss = (
        #     marginal_cpc_loss_1_total
        #     + marginal_cpc_loss_2_total
        #     # + marginal_cpc_loss_unmasked
        #     + short_marginal_cpc_loss_1_total
        #     + short_marginal_cpc_loss_2_total
        #     # + short_marginal_cpc_loss_unmasked
        # )

        # COMPUTRE JOINT LOSS
        # The mask for joint embedding_space loss is not necessary because there's
        # no NOT_PRESENT tokens to worry about because all tokens are guaranteed present
        # because we created the joint encodings ourselves.
        joint_loss_1 = self.compute_joint_infoNCE_loss(
            full_joint_encodings_1, full_joint_encodings_unmasked
        )
        joint_loss_2 = self.compute_joint_infoNCE_loss(
            full_joint_encodings_2, full_joint_encodings_unmasked
        )
        short_joint_loss_1 = self.compute_joint_infoNCE_loss(
            short_joint_encodings_1,
            short_joint_encodings_unmasked,
            short=True,
        )
        short_joint_loss_2 = self.compute_joint_infoNCE_loss(
            short_joint_encodings_2,
            short_joint_encodings_unmasked,
            short=True,
        )
        joint_loss = (
            joint_loss_1 + joint_loss_2 + short_joint_loss_1 + short_joint_loss_2
        )

        # COMPUTE SPREAD LOSS
        spread_loss_full_total, spread_loss_full_dict = self.compute_spread_loss(
            full_joint_encodings_unmasked,
            full_joint_encodings_1,
            full_joint_encodings_2,
            temp_multiplier=temp_multiplier
        )
        spread_loss_short_total, spread_loss_short_dict = self.compute_spread_loss(
            short_joint_encodings_unmasked,
            short_joint_encodings_1,
            short_joint_encodings_2,
            temp_multiplier=temp_multiplier
        )

        spread_loss = spread_loss_full_total + spread_loss_short_total

        # NOTE to Mitch: this is where we compute the mutual information between the joint
        # encodings for the two "masks". The average of these two valuese gives us
        # log_n = torch.log(torch.tensor(batch_size))
        log_n = math.log(batch_size)
        mi_1 = log_n - joint_loss_1.detach().item()
        mi_2 = log_n - joint_loss_2.detach().item()
        self.update_joint_mi(mi_1 / math.log(2))  # convert from nats to bits
        self.update_joint_mi(mi_2 / math.log(2))  # convert from nats to bits

        # Collect entropy regularization losses from adaptive encoders
        # This encourages sharper strategy selection (one strategy dominates)
        entropy_regularization_loss = None
        if self.training:
            entropy_losses = []
            for col_name, encoder in self.column_encoder.encoders.items():
                if hasattr(encoder, '_current_entropy_loss'):
                    entropy_loss = encoder._current_entropy_loss
                    if entropy_loss is not None and entropy_loss.requires_grad:
                        entropy_losses.append(entropy_loss)
            
            if entropy_losses:
                # Sum all entropy losses from adaptive encoders
                entropy_regularization_loss = sum(entropy_losses)
            else:
                # No entropy losses - create zero tensor on correct device
                entropy_regularization_loss = torch.tensor(0.0, device=joint_loss.device, requires_grad=False)
        else:
            # Not training - no entropy regularization
            entropy_regularization_loss = torch.tensor(0.0, device=joint_loss.device, requires_grad=False)

        loss_config = self.config.loss_config
        # Apply scaling coefficient to marginal loss value (not weight) to make it comparable to spread/joint
        # This way the weight can be simple (0.3-1.0) without needing to remember the scaling
        marginal_loss_scaled = marginal_loss
        if hasattr(loss_config, 'marginal_loss_scaling_coefficient') and loss_config.marginal_loss_scaling_coefficient is not None:
            marginal_loss_scaled = marginal_loss * loss_config.marginal_loss_scaling_coefficient
        
        # Add entropy regularization to encourage sharper strategy selection
        # Weight it relatively low (0.01) so it guides but doesn't dominate
        entropy_weight = 0.01
        total = (
            loss_config.joint_loss_weight * joint_loss
            + loss_config.marginal_loss_weight * marginal_loss_scaled
            + loss_config.spread_loss_weight * spread_loss
            + entropy_weight * entropy_regularization_loss
        )

        loss_dict = {
            "total": total.item(),
            "batch_size": batch_size,
            "entropy_regularization": {
                "total": entropy_regularization_loss.item() if hasattr(entropy_regularization_loss, 'item') else 0.0,
            },
            "spread_loss": {
                "total": spread_loss.item(),
                "full": {
                    "total": spread_loss_full_total.item(),
                    **spread_loss_full_dict,
                },
                "short": {
                    "total": spread_loss_short_total.item(),
                    **spread_loss_short_dict,
                },
            },
            "joint_loss": {
                "total": joint_loss.item(),
                "joint_loss_full_1": joint_loss_1.item(),
                "joint_loss_full_2": joint_loss_2.item(),
                "joint_loss_short_1": short_joint_loss_1.item(),
                "joint_loss_short_2": short_joint_loss_2.item(),
            },
            "marginal_loss": {
                "total": marginal_loss.item(),
                "marginal_loss_full_1": {
                    "total": marginal_cpc_loss_1_total.item(),
                    "cols": marginal_cpc_loss_1_col_dict,
                },
                "marginal_loss_full_2": {
                    "total": marginal_cpc_loss_2_total.item(),
                    "cols": marginal_cpc_loss_2_col_dict,
                },
                "marginal_loss_short_1": {
                    "total": short_marginal_cpc_loss_1_total.item(),
                    "cols": short_marginal_cpc_loss_1_col_dict,
                },
                "marginal_loss_short_2": {
                    "total": short_marginal_cpc_loss_2_total.item(),
                    "cols": short_marginal_cpc_loss_2_col_dict,
                },
            },
        }

        return total, loss_dict

    def encode(self, column_batches, apply_noise=False):
        """This is the method that should be called at query time."""
        
        # Get logger from the current module
        import logging
        logger = logging.getLogger(__name__)
        
        # CRITICAL: Force CPU mode for single predictor training
        force_cpu_env = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR')
        if force_cpu_env == '1':
            # Ensure encoder and all submodules are on CPU
            if list(self.parameters()):
                encoder_device = next(self.parameters()).device
                if encoder_device.type != 'cpu':
                    self.cpu()
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
            
            # CRITICAL: Move all input TokenBatch objects to CPU
            cpu_device = torch.device('cpu')
            for col_name, token_batch in column_batches.items():
                if hasattr(token_batch, 'to'):
                    token_batch.to(cpu_device)
        
        # Debug counter for tracking problematic batches
        # debug_count = getattr(self, '_encode_debug_count', 0)
        # should_debug = debug_count < 3  # Debug first 3 batches
        
        # if should_debug:
        #     logger.info(f"🔍 ENCODER DEBUG #{debug_count}: Starting encoder.encode")
        #     logger.info(f"   Input columns: {list(column_batches.keys())}")
        #     logger.info(f"   Apply noise: {apply_noise}")
        
        (
            short_column_encoding_list,
            full_column_encoding_list,
            token_status_list,
        ) = self.column_encoder(column_batches)
        
        # if should_debug:
        #     logger.info(f"   Column encoder output - lists length: {len(short_column_encoding_list)}")
        #     for i, (short_enc, full_enc) in enumerate(zip(short_column_encoding_list, full_column_encoding_list)):
        #         if torch.isnan(short_enc).any() or torch.isnan(full_enc).any():
        #             col_name = list(column_batches.keys())[i] if i < len(column_batches) else f"col_{i}"
        #             logger.error(f"🚨 COLUMN ENCODER OUTPUT HAS NaN: {col_name}")
        #             if torch.isnan(short_enc).any():
        #                 logger.error(f"   Short encoding NaN count: {torch.isnan(short_enc).sum()}/{short_enc.numel()}")
        #             if torch.isnan(full_enc).any():
        #                 logger.error(f"   Full encoding NaN count: {torch.isnan(full_enc).sum()}/{full_enc.numel()}")
        
        column_encodings, token_status_mask = (
            torch.stack(full_column_encoding_list, dim=1),
            torch.stack(token_status_list, dim=1),
        )

        # if should_debug:
        #     if torch.isnan(column_encodings).any():
        #         logger.error(f"🚨 STACKED COLUMN ENCODINGS HAVE NaN: {torch.isnan(column_encodings).sum()}/{column_encodings.numel()}")
        #     logger.info(f"   Stacked encodings shape: {column_encodings.shape}")

        self.column_encodings = column_encodings
        self.token_status_mask = token_status_mask

        if apply_noise is True:
            batch_size = column_encodings.shape[0]
            column_marginal_embeddings = self.get_marginal_tensor(batch_size)
            column_encodings = self.apply_marginal_mask(
                column_encodings, column_marginal_embeddings, token_status_mask
            )
            
            # if should_debug:
            #     if torch.isnan(column_encodings).any():
            #         logger.error(f"🚨 AFTER MARGINAL MASK ENCODINGS HAVE NaN: {torch.isnan(column_encodings).sum()}/{column_encodings.numel()}")

        # ROOT CAUSE DEBUGGING: Check for zero vectors before joint encoder
        # if should_debug:
        #     # Check for zero vectors that could cause NaN during normalization
        #     zero_tensor = torch.zeros_like(column_encodings)
        #     zero_vectors = torch.allclose(column_encodings, zero_tensor, atol=1e-8)
        #     if zero_vectors:
        #         logger.error(f"🚨 ZERO VECTORS DETECTED before joint encoder!")
        #         logger.error(f"   column_encodings contains all zeros: {column_encodings}")
            
        #     # Check for individual zero rows/columns
        #     for i in range(column_encodings.shape[0]):  # batch dimension
        #         for j in range(column_encodings.shape[1]):  # column dimension
        #             vec = column_encodings[i, j, :]
        #             zero_vec = torch.zeros_like(vec)
        #             if torch.allclose(vec, zero_vec, atol=1e-8):
        #                 col_name = list(column_batches.keys())[j] if j < len(column_batches) else f"col_{j}"
        #                 logger.error(f"🚨 Zero vector for batch {i}, column '{col_name}': {vec}")

        short_joint_encodings, full_joint_encodings = self.joint_encoder(
            column_encodings
        )

        # if should_debug:
        #     if torch.isnan(short_joint_encodings).any():
        #         logger.error(f"🚨 JOINT ENCODER SHORT OUTPUT HAS NaN: {torch.isnan(short_joint_encodings).sum()}/{short_joint_encodings.numel()}")
        #     if torch.isnan(full_joint_encodings).any():
        #         logger.error(f"🚨 JOINT ENCODER FULL OUTPUT HAS NaN: {torch.isnan(full_joint_encodings).sum()}/{full_joint_encodings.numel()}")
        #     logger.info(f"   Joint encoder output shapes: short={short_joint_encodings.shape}, full={full_joint_encodings.shape}")
        #     self._encode_debug_count = debug_count + 1

        return short_joint_encodings, full_joint_encodings

    def forward(self, column_batches):

        # Encode the columns invidividually
        (
            short_column_encoding_list,
            full_column_encoding_list,
            token_status_list,
        ) = self.column_encoder(column_batches)

        # Combine the individual column encodings and masks into tensors for easier handling
        # the resulting tensors have shapes (batch_size, n_cols, d_model) and (batch_size, n_cols), respectively
        # The ease of handling is mostly related to masking - it's much easier to carry out the masking procedure
        # on a single tensor object that contains the embeddings for all the columns because that makes
        # the coordination of how many columns to mask out much easier.
        
        # DEBUG: Check for empty encoding lists before stacking
        import logging
        logger = logging.getLogger(__name__)
        if len(short_column_encoding_list) == 0:
            logger.error(f"💥 CRITICAL: short_column_encoding_list is EMPTY!")
            logger.error(f"   This causes 'stack expects a non-empty TensorList' error")
            logger.error(f"   Column encoder returned no encodings")
            raise RuntimeError("No columns were encoded - check column setup and codec creation")
            
        short_column_encodings, full_column_encodings, token_status_mask = (
            torch.stack(short_column_encoding_list, dim=1),
            torch.stack(full_column_encoding_list, dim=1),
            torch.stack(token_status_list, dim=1),
        )

        batch_size = full_column_encodings.shape[0]

        # with stopwatch.interval("sample_marginal_masks"):
        # Each row is randomly split into two non-overlapping parts. We do that so we
        # can embed each part separately and then use it to predict the other part.
        # We take in the batch status mask, and return two mask that are complimentary.
        mask_1, mask_2 = sample_marginal_masks(token_status_mask)

        # with stopwatch.interval("get_marginal_tensor"):
        full_column_marginal_embeddings = self.get_marginal_tensor(batch_size)

        # with stopwatch.interval("apply_marginal_masks"):
        masked_column_encodings_1 = self.apply_marginal_mask(
            full_column_encodings, full_column_marginal_embeddings, mask_1
        )
        masked_column_encodings_2 = self.apply_marginal_mask(
            full_column_encodings, full_column_marginal_embeddings, mask_2
        )

        # with stopwatch.interval("joint_encoding"):
        short_joint_encodings_1, full_joint_encodings_1 = self.joint_encoder(
            masked_column_encodings_1
        )
        short_joint_encodings_2, full_joint_encodings_2 = self.joint_encoder(
            masked_column_encodings_2
        )
        (
            short_joint_encodings_unmasked,
            full_joint_encodings_unmasked,
        ) = self.joint_encoder(full_column_encodings)

        # Column predictions are a list of torch.tensors. Each element of the list
        # corresponds to the predictions made for the corresponding column.
        # The list elements are ordered by config.cols_in_order.
        # The list elements all have shape (batch_size, model_dim)
        # with stopwatch.interval("column_predictors"):
        full_column_predictions_unmasked = self.column_predictor(
            full_joint_encodings_unmasked
        )
        full_column_predictions_1 = self.column_predictor(full_joint_encodings_1)
        full_column_predictions_2 = self.column_predictor(full_joint_encodings_2)

        # with stopwatch.interval("column_predictors_short"):
        short_column_predictions_1 = self.short_column_predictor(
            short_joint_encodings_1
        )
        short_column_predictions_2 = self.short_column_predictor(
            short_joint_encodings_2
        )
        short_column_predictions_unmasked = self.short_column_predictor(
            short_joint_encodings_unmasked
            )

        # stopwatch.stop()

        return (
            batch_size,
            #
            full_joint_encodings_unmasked,
            full_joint_encodings_1,
            full_joint_encodings_2,
            #
            full_column_encodings,
            short_column_encodings,
            #
            short_joint_encodings_unmasked,
            short_joint_encodings_1,
            short_joint_encodings_2,
            #
            mask_1,
            mask_2,
            #
            full_column_predictions_1,
            full_column_predictions_2,
            full_column_predictions_unmasked,
            #
            short_column_predictions_1,
            short_column_predictions_2,
            short_column_predictions_unmasked,
        )
