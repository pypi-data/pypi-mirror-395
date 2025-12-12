#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
from __future__ import annotations

import logging
import math
import os
import pickle
import tempfile
import traceback
from collections import Counter
from datetime import datetime
from pathlib import Path
from pprint import pprint as pprint
from typing import Optional

import numpy as np
import pandas as pd

# Import logging configuration FIRST to ensure timestamps
from featrix.neural.logging_config import configure_logging
configure_logging()

from featrix.neural.detect import DetectorDict
from featrix.neural.detect import DetectorList
from featrix.neural.detect import DetectorStrDict
from featrix.neural.detect import FeatrixFieldScalarDetection
from featrix.neural.enrich import EnrichMap
from featrix.neural.enrich import FeatrixFieldBaseEnrichment
from featrix.neural.model_config import ColumnType
from sklearn.model_selection import train_test_split

from featrix.neural.integrity import FeatrixDataIntegrity
from featrix.neural.string_cache import StringCache

from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import lru_cache


os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'     # required for mps and sentence_transformers...

# If the user doesn't specify a limit, we make it 100k
LIMIT_DATASET_SIZE = 100000  # 100k
# We want to at least get this many rows from each dataset (if it has that many)
MINIMUM_DATASET_SAMPLE = 1000

logger = logging.getLogger(__name__)

# REMOVED: sentence_model = None
# REMOVED: EMBED_MODEL = "all-minilm-l6-v2"
# REMOVED: _loadModelIfNeeded() function
# 
# NOW USING: The global sentence_model from string_codec.py to avoid loading multiple instances
# This saves GPU memory and ensures consistency across the codebase

def _log_gpu_memory_input_data_set(context: str = ""):
    """Quick GPU memory logging for tracing memory usage in input_data_set."""
    try:
        import torch
        if not torch.cuda.is_available():
            return
        allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
        reserved = torch.cuda.memory_reserved() / (1024**3)  # GB
        max_allocated = torch.cuda.max_memory_allocated() / (1024**3)  # GB
        logger.info(f"📊 GPU MEMORY [input_data_set: {context}]: Allocated={allocated:.3f} GB, Reserved={reserved:.3f} GB, Peak={max_allocated:.3f} GB")
    except Exception as e:
        logger.debug(f"Could not log GPU memory: {e}")

# @lru_cache(maxsize=1000)
# def preview_cached_sentence_model_encode(value):
#     # Use the global sentence_model from string_codec instead of creating a separate instance
#     from featrix.neural.string_codec import _loadModelIfNeeded, sentence_model
#     _loadModelIfNeeded()  # This will load the global model if not already loaded
    
#     if sentence_model is None:
#         logger.error("❌ Failed to get sentence transformer model from string_codec")
#         return None
    
#     val = sentence_model.encode(
#         value,
#         show_progress_bar=False,  # DO NOT DELETE.
#     ) # slightly different than string_codec -- be careful.
#     return val


class FeatrixInputDataSet:
    def __init__(
        self,
        df=None,
        detect_only=False,
        debug_detector=None,
        ignore_cols=[],
        limit_rows=None,
        encoder_overrides=None,
        project_row_meta_data=None,
        standup_only=False,
        dataset_title="DATASET"
    ):
        if limit_rows is None or limit_rows <= 0:
            limit_rows = LIMIT_DATASET_SIZE
        self.limit_rows = limit_rows

        self._hh = None

        self.project_row_meta_data_list = project_row_meta_data
        self.df = df
        assert self.df is not None
        
        self.dataset_title = dataset_title

        self._init_ignore_cols(ignore_cols=ignore_cols)
        self._init_limit_rows(limit_rows=limit_rows)

        # This will contain all the enrichment columns we add to self.df
        self.enrichment_columns = []

        # self.limit_rows = limit_rows
        self.casted_df = None
        self.debug_detector = debug_detector
        self.encoderOverrides = encoder_overrides or dict()

        self._colsNonNullsCount = {}
        self._colsUniquesCount = {}
        self._colsTopNValues = {}

        self.detectorDebugInfo = {}
        self._detectors = {}
        self._enrichedDataDetectors = None
        self._enrichedDataFrames = {}  # Maybe don't want this.
        self._detectOutputData = None
        self._colCodecs = None  # Initialize column codecs (was initialized in _enrichAllColumns)
        self._colTree = [[]]  # Initialize column tree (was initialized in _enrichAllColumns)

        logger.info(f"standup_only = {standup_only}")
        if not standup_only:
            self._computeDescStats()
            self._detectColumnTypes()
            # Enrichment disabled - no longer adding enrichment columns
            # self._enrichAllColumns()
            self._dropLowValueColumns()
            self._computeDescStats()  # do it again to catch up
            self._printDetectorResults(dataset_title)

    def _init_limit_rows(self, limit_rows):
        limit_rows = min(limit_rows, len(self.df))
        if limit_rows < len(self.df):
            logger.info(f"Sampling {limit_rows} of {len(self.df)} rows")
            if (
                self.project_row_meta_data_list is None
                or (self.project_row_meta_data_list) == 1
            ):
                self.df = self.df.sample(limit_rows).reset_index(drop=True)
                if self.project_row_meta_data_list:
                    self.project_row_meta_data_list[0].num_rows = limit_rows
            else:
                self.sample_complex_data()

    def create_string_caches(self, sqlite_file):
        # Build comprehensive string cache with ALL string values
        logger.info(f"🔥 Creating string cache: {sqlite_file}")
        logger.info(f"🔍 INPUT_DATA_SET DEBUG: current working directory = {os.getcwd()}")
        logger.info(f"🔍 INPUT_DATA_SET DEBUG: absolute cache path = {os.path.abspath(sqlite_file)}")
        
        # Collect ALL string values from ALL string columns
        all_string_values = []
        string_columns = []
        
        for c, codec in self.column_codecs().items():
            if codec == ColumnType.FREE_STRING:
                string_columns.append(c)
                vals = self.df[c].astype(str).tolist()
                all_string_values.extend(vals)
                logger.info(f"🔍 INPUT_DATA_SET DEBUG: Column '{c}' has {len(vals)} string values")
        
        if string_columns:
            logger.info(f"📝 Found {len(string_columns)} string columns: {string_columns}")
            logger.info(f"📊 Caching {len(all_string_values)} total string values...")
            
            # Create a single comprehensive cache with the specified filename
            _log_gpu_memory_input_data_set("before string cache in inputdataset")
            sc = StringCache(
                initial_values=all_string_values,
                debugName="comprehensive_string_cache",
                string_cache_filename=sqlite_file
            )
            _log_gpu_memory_input_data_set("after string cache in inputdataset")
            
            # CRITICAL: Ensure all transactions are committed and connection is closed
            if hasattr(sc, 'conn') and sc.conn:
                # Final commit to ensure everything is written
                sc.conn.commit()
                # Close the connection to flush to disk
                sc.conn.close()
                logger.info(f"✅ String cache connection closed, file flushed to disk")
            
            # Small delay to ensure file system has synced
            import time
            time.sleep(0.1)
            
            logger.info(f"✅ String cache created at: {sqlite_file}")
            
            # Verify the cache file exists after creation (use absolute path)
            cache_abs_path = os.path.abspath(sqlite_file)
            if os.path.exists(cache_abs_path):
                file_size = os.path.getsize(cache_abs_path)
                logger.info(f"🔍 INPUT_DATA_SET DEBUG: Cache file verified - size: {file_size / 1024:.1f} KB")
                logger.info(f"🔍 INPUT_DATA_SET DEBUG: Cache file absolute path: {cache_abs_path}")
            else:
                logger.error(f"❌ INPUT_DATA_SET DEBUG: Cache file does NOT exist after creation")
                logger.error(f"   Expected path: {cache_abs_path}")
                logger.error(f"   Current working directory: {os.getcwd()}")
                logger.error(f"   Relative path exists: {os.path.exists(sqlite_file)}")
        else:
            logger.info("ℹ️  No string columns found - no cache created")

        return

    def _init_ignore_cols(self, ignore_cols):
        self.ignore_cols = ignore_cols or []
        
        # CRITICAL: Auto-detect ALL __featrix* columns and add to ignore list
        # These are internal columns that must NEVER be trained on:
        # - __featrix_meta_*: Metadata columns (should be stored but not trained)
        # - __featrix_train_predictor: Training filter column (already dropped in training scripts)
        # - __featrix_*: Any other internal columns we might add in the future
        internal_cols = [col for col in self.df.columns if col.startswith('__featrix')]
        if internal_cols:
            logger.debug(f"🔒 Detected {len(internal_cols)} internal __featrix* columns that will be excluded from training:")
            for col in internal_cols:
                logger.debug(f"   - Excluding: {col}")
            self.ignore_cols.extend(internal_cols)
            # Store separately so we know these are internal columns (not just ignored)
            self.internal_cols = internal_cols
        else:
            self.internal_cols = []
        
        if len(self.ignore_cols) > 0:
            # walk and drop columns.
            logger.info(f"IGNORING columns: {self.ignore_cols}")
            logger.info(f"df columns: {self.df.columns}")
            for theCol in self.ignore_cols:
                if theCol in self.df.columns:
                    self.df = self.df.drop(theCol, axis=1)
        logger.info(f"COLUMN LIST: {self.df.columns}")
        return
        

    def split(self, fraction=0.2):
        # CRITICAL FIX: Extract detected types from FULL dataset BEFORE splitting
        # This ensures train and val use IDENTICAL encoder types
        logger.info("🔍 Extracting encoder types from full dataset before split...")
        detected_types = {}
        if hasattr(self, '_detectors') and self._detectors:
            for col, detector in self._detectors.items():
                detected_types[col] = detector.type_name
            logger.info(f"   Extracted {len(detected_types)} encoder types from full dataset")
            
            # Set as encoder overrides to force consistency
            if not self.encoderOverrides:
                self.encoderOverrides = {}
            self.encoderOverrides.update(detected_types)
            logger.info(f"   ✅ Locked encoder types for train/val consistency")
        else:
            logger.warning("   ⚠️  No detectors found - cannot lock encoder types")
        
        # CRITICAL: Drop columns that are all null BEFORE splitting
        # This ensures train and val have identical columns from the start, preventing column mismatch errors
        logger.info("🔍 Checking for all-null columns in full dataset before split...")
        cols_to_drop = []
        for col in self.df.columns:
            if self.df[col].isna().all():
                cols_to_drop.append(col)
        
        if cols_to_drop:
            logger.info(f"🔍 Dropping {len(cols_to_drop)} all-null columns before split: {cols_to_drop}")
            self.df = self.df.drop(columns=cols_to_drop)
            logger.info(f"   ✅ Dropped from full dataset to ensure train/val column consistency")
        else:
            logger.info("   ✅ No all-null columns found in full dataset")
        
        # Validate fraction: if it's an integer, ensure it doesn't exceed dataset size
        dataset_size = len(self.df)
        if isinstance(fraction, (int, float)) and not isinstance(fraction, bool):
            if isinstance(fraction, int) and fraction >= dataset_size:
                # Convert absolute number to fraction if it's too large
                logger.warning(f"⚠️  val_size ({fraction}) >= dataset size ({dataset_size}). Converting to fraction: {fraction/dataset_size:.3f}")
                fraction = fraction / dataset_size
            elif isinstance(fraction, float) and fraction >= 1.0:
                # Fraction >= 1.0 is invalid, cap it
                logger.warning(f"⚠️  val_size fraction ({fraction}) >= 1.0. Capping to 0.5 (50%)")
                fraction = 0.5
        
        train_df, val_df = train_test_split(
            self.df,
            test_size=fraction,
        )

        train_df.reset_index(drop=True, inplace=True)
        val_df.reset_index(drop=True, inplace=True)
        
        # For small datasets (< 1024 samples), duplicate rows until we have >= 1024 total
        MIN_DATASET_SIZE = 1024
        original_train_size = len(train_df)
        original_val_size = len(val_df)
        total_size = original_train_size + original_val_size
        duplication_factor = 1  # Default: no duplication
        
        if total_size < MIN_DATASET_SIZE:
            logger.info(f"📊 Small dataset detected: {total_size} samples < {MIN_DATASET_SIZE}")
            logger.info(f"   Train: {original_train_size}, Val: {original_val_size}")
            
            # Calculate duplication factor needed to reach >= 1024
            duplication_factor = math.ceil(MIN_DATASET_SIZE / total_size)
            logger.info(f"   Duplicating each set {duplication_factor}x to reach >= {MIN_DATASET_SIZE} samples")
            
            # Duplicate train set
            train_duplicates = [train_df] * duplication_factor
            train_df = pd.concat(train_duplicates, ignore_index=True)
            
            # Duplicate val set
            val_duplicates = [val_df] * duplication_factor
            val_df = pd.concat(val_duplicates, ignore_index=True)
            
            new_total = len(train_df) + len(val_df)
            logger.info(f"✅ Dataset augmented: {total_size} → {new_total} samples")
            logger.info(f"   Train: {original_train_size} → {len(train_df)}, Val: {original_val_size} → {len(val_df)}")

        # CRITICAL: Check for columns that are all null in EITHER split and drop from BOTH
        # This prevents _dropLowValueColumns() in __init__ from dropping them from one but not the other
        logger.info("🔍 Checking for all-null columns in train/val splits after split...")
        all_null_in_train = set()
        all_null_in_val = set()
        
        for col in train_df.columns:
            if col not in val_df.columns:
                continue
            if train_df[col].isna().all():
                all_null_in_train.add(col)
            if val_df[col].isna().all():
                all_null_in_val.add(col)
        
        # Drop columns that are all null in EITHER split from BOTH splits
        cols_to_drop = all_null_in_train | all_null_in_val
        if cols_to_drop:
            logger.info(f"🔍 Dropping {len(cols_to_drop)} columns that are all null in at least one split: {cols_to_drop}")
            train_df = train_df.drop(columns=cols_to_drop)
            val_df = val_df.drop(columns=cols_to_drop)
            logger.info(f"   ✅ Dropped from both splits to prevent column mismatch")
        else:
            logger.info("   ✅ No all-null columns found in either split")

        logger.info(f"SPLIT - project_row_meta_data_list = {self.project_row_meta_data_list}")
        logger.info(f"SPLIT: self.encoderOverrides = {self.encoderOverrides}")
#        assert self.project_row_meta_data_list

        # Handle metadata duplication for small datasets
        train_meta_data = None
        val_meta_data = None
        if self.project_row_meta_data_list is not None:
            if total_size < MIN_DATASET_SIZE:
                # Small dataset case: duplicate metadata to match duplicated dataframes
                # The train/val split happened on original data, so we need to duplicate metadata accordingly
                train_meta_size = original_train_size
                val_meta_size = original_val_size
                # Ensure we have enough metadata for the original split
                if len(self.project_row_meta_data_list) >= train_meta_size + val_meta_size:
                    train_meta_data = self.project_row_meta_data_list[:train_meta_size] * duplication_factor
                    val_meta_data = self.project_row_meta_data_list[train_meta_size:train_meta_size + val_meta_size] * duplication_factor
                else:
                    # Metadata list is shorter - use what we have and duplicate
                    logger.warning(f"⚠️  Metadata list ({len(self.project_row_meta_data_list)}) shorter than original dataframes. Duplicating available metadata.")
                    available_meta = self.project_row_meta_data_list
                    # Split available metadata proportionally
                    train_meta_portion = available_meta[:train_meta_size] if len(available_meta) >= train_meta_size else available_meta
                    val_meta_portion = available_meta[train_meta_size:train_meta_size + val_meta_size] if len(available_meta) >= train_meta_size + val_meta_size else available_meta[train_meta_size:] if len(available_meta) > train_meta_size else []
                    train_meta_data = train_meta_portion * duplication_factor
                    val_meta_data = val_meta_portion * duplication_factor
            else:
                # Normal case: split metadata according to train/val split
                train_meta_size = len(train_df)
                val_meta_size = len(val_df)
                # Note: metadata list might not match exactly due to train_test_split randomness
                # Use lengths of dataframes to determine split point
                if len(self.project_row_meta_data_list) >= train_meta_size + val_meta_size:
                    train_meta_data = self.project_row_meta_data_list[:train_meta_size]
                    val_meta_data = self.project_row_meta_data_list[train_meta_size:train_meta_size + val_meta_size]
                else:
                    # Metadata list is shorter - duplicate to match
                    logger.warning(f"⚠️  Metadata list ({len(self.project_row_meta_data_list)}) shorter than dataframes. Using available metadata.")
                    train_meta_data = (self.project_row_meta_data_list * math.ceil(train_meta_size / len(self.project_row_meta_data_list)))[:train_meta_size] if self.project_row_meta_data_list else None
                    val_meta_data = (self.project_row_meta_data_list * math.ceil(val_meta_size / len(self.project_row_meta_data_list)))[:val_meta_size] if self.project_row_meta_data_list else None

        train_ds = FeatrixInputDataSet(df=train_df,
                                       ignore_cols=self.ignore_cols,
                                       encoder_overrides=self.encoderOverrides,
                                       project_row_meta_data=train_meta_data,
                                       dataset_title="TRAINING SET")

        val_ds   = FeatrixInputDataSet(df=val_df,
                                       ignore_cols=self.ignore_cols,
                                       encoder_overrides=self.encoderOverrides,
                                       project_row_meta_data=val_meta_data,
                                       dataset_title="VALIDATION SET")

        # CRITICAL: Validate that train and val have IDENTICAL encoder types
        # Type mismatches are FATAL - the system cannot work if train uses SetCodec and val uses StringCodec
        self._validate_encoder_type_match(train_ds, val_ds)
        
        # Validate that train and val distributions match (detect distribution drift)
        kl_divergences = self._validate_split_distributions(train_df, val_df)
        
        # Store KL divergences as metadata for later access
        train_ds.kl_divergences_vs_val = kl_divergences
        val_ds.kl_divergences_vs_train = kl_divergences

        return train_ds, val_ds
    
    def _validate_encoder_type_match(self, train_ds, val_ds):
        """
        CRITICAL CHECK: Ensure train and val datasets have IDENTICAL encoder types for all columns.
        
        If encoder types differ, the codecs will be incompatible and everything will break silently.
        This is a FATAL error that must stop execution immediately.
        
        Args:
            train_ds: Training dataset
            val_ds: Validation dataset
            
        Raises:
            ValueError: If any column has different encoder types between train and val
        """
        logger.info("=" * 100)
        logger.info("🔍 VALIDATING ENCODER TYPE CONSISTENCY (TRAIN vs VAL)")
        logger.info("=" * 100)
        
        train_encoders = {}
        val_encoders = {}
        
        # Extract encoder types from both datasets
        for col_name, detector in train_ds._detectors.items():
            train_encoders[col_name] = detector.get_codec_name()
            
        for col_name, detector in val_ds._detectors.items():
            val_encoders[col_name] = detector.get_codec_name()
        
        # Check for column mismatches
        train_cols = set(train_encoders.keys())
        val_cols = set(val_encoders.keys())
        
        if train_cols != val_cols:
            missing_in_val = train_cols - val_cols
            missing_in_train = val_cols - train_cols
            error_msg = "❌ FATAL: Column mismatch between train and val\n"
            if missing_in_val:
                error_msg += f"  Columns in train but not val: {missing_in_val}\n"
            if missing_in_train:
                error_msg += f"  Columns in val but not train: {missing_in_train}\n"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Check for encoder type mismatches
        type_mismatches = []
        for col_name in train_cols:
            train_type = train_encoders[col_name]
            val_type = val_encoders[col_name]
            
            if train_type != val_type:
                type_mismatches.append((col_name, train_type, val_type))
                logger.error(f"  ❌ {col_name:30s}: train={train_type}, val={val_type}")
            else:
                logger.info(f"  ✓ {col_name:30s}: {train_type}")
        
        logger.info("=" * 100)
        
        if type_mismatches:
            error_msg = (
                f"\n❌ FATAL ERROR: ENCODER TYPE MISMATCH BETWEEN TRAIN AND VAL\n\n"
                f"The following columns have DIFFERENT encoder types in train vs val:\n\n"
            )
            for col, train_type, val_type in type_mismatches:
                error_msg += f"  • {col}:\n"
                error_msg += f"      Train: {train_type}\n"
                error_msg += f"      Val:   {val_type}\n\n"
            
            error_msg += (
                f"This happens when:\n"
                f"  1. The dataset is split BEFORE encoder_overrides are set\n"
                f"  2. Train and val independently detect types from different samples\n"
                f"  3. Small val set causes different type detection\n\n"
                f"FIX: Extract detected types from full dataset BEFORE splitting:\n\n"
                f"  dataset = FeatrixInputDataSet(df=df, ...)\n"
                f"  detected_types = {{col: det.get_codec_name() for col, det in dataset._detectors.items()}}\n"
                f"  dataset.encoderOverrides = detected_types  # SET BEFORE SPLIT\n"
                f"  train_data, val_data = dataset.split()\n\n"
                f"This ensures train and val use IDENTICAL encoder types from the full dataset.\n"
            )
            
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("✅ All encoder types match between train and val")
        logger.info("=" * 100)
    
    def _validate_split_distributions(self, train_df, val_df, kl_threshold=0.1):
        """
        Validate that train and val splits have similar distributions using KL divergence.
        
        For categorical columns: compute KL divergence on value distributions
        For numerical columns: bin the values and compute KL divergence on bins
        
        Args:
            train_df: Training dataframe
            val_df: Validation dataframe
            kl_threshold: Maximum acceptable KL divergence (0.1 = 10% divergence is acceptable)
            
        Returns:
            dict: KL divergences for all columns {col_name: kl_divergence}
        """
        import numpy as np
        from scipy.special import kl_div
        
        # Quiet startup - don't spam logs before training even starts
        # logger.info("=" * 100)
        # logger.info("🔍 VALIDATING TRAIN/VAL DISTRIBUTION MATCH")
        # logger.info("=" * 100)
        
        issues_found = []
        all_kl_divergences = {}
        
        for col in train_df.columns:
            if col in self.ignore_cols:
                continue
                
            try:
                # Determine if column is numeric or categorical
                is_numeric = pd.api.types.is_numeric_dtype(train_df[col])
                
                if is_numeric:
                    # For numeric columns: bin and compare distributions
                    # Remove NaNs for comparison
                    train_vals = train_df[col].dropna()
                    val_vals = val_df[col].dropna()
                    
                    if len(train_vals) == 0 or len(val_vals) == 0:
                        continue
                    
                    # Create bins based on train data range
                    n_bins = min(20, len(train_vals.unique()))
                    bins = np.linspace(train_vals.min(), train_vals.max(), n_bins + 1)
                    
                    # Compute histograms
                    train_hist, _ = np.histogram(train_vals, bins=bins)
                    val_hist, _ = np.histogram(val_vals, bins=bins)
                    
                    # Normalize to probabilities (add small epsilon to avoid log(0))
                    epsilon = 1e-10
                    train_prob = (train_hist + epsilon) / (train_hist.sum() + epsilon * len(train_hist))
                    val_prob = (val_hist + epsilon) / (val_hist.sum() + epsilon * len(val_hist))
                    
                else:
                    # For categorical/text columns: compare distributions
                    train_unique = len(train_df[col].dropna().unique())
                    val_unique = len(val_df[col].dropna().unique())
                    
                    # Check null/non-null ratio difference
                    train_total = len(train_df[col])
                    train_non_null = train_df[col].notna().sum()
                    train_null_pct = (train_total - train_non_null) / train_total * 100 if train_total > 0 else 0
                    
                    val_total = len(val_df[col])
                    val_non_null = val_df[col].notna().sum()
                    val_null_pct = (val_total - val_non_null) / val_total * 100 if val_total > 0 else 0
                    
                    null_pct_diff = abs(train_null_pct - val_null_pct)
                    
                    # For text columns (many unique values), use string length distribution
                    if train_unique > 100 or val_unique > 100:
                        # Text column: compute KL divergence on string length distributions
                        train_lengths = train_df[col].dropna().astype(str).str.len()
                        val_lengths = val_df[col].dropna().astype(str).str.len()
                        
                        if len(train_lengths) == 0 or len(val_lengths) == 0:
                            continue
                        
                        # Create bins based on train data range
                        n_bins = min(20, len(train_lengths.unique()))
                        bins = np.linspace(train_lengths.min(), train_lengths.max(), n_bins + 1)
                        
                        # Compute histograms
                        train_hist, _ = np.histogram(train_lengths, bins=bins)
                        val_hist, _ = np.histogram(val_lengths, bins=bins)
                        
                        # Normalize to probabilities (add small epsilon to avoid log(0))
                        epsilon = 1e-10
                        train_prob = (train_hist + epsilon) / (train_hist.sum() + epsilon * len(train_hist))
                        val_prob = (val_hist + epsilon) / (val_hist.sum() + epsilon * len(val_hist))
                    else:
                        # Categorical column: compare value distributions
                        train_counts = train_df[col].value_counts(normalize=True, dropna=True)
                        val_counts = val_df[col].value_counts(normalize=True, dropna=True)
                        
                        # Align indices (handle values that might only appear in one split)
                        all_values = sorted(set(train_counts.index) | set(val_counts.index))
                        
                        epsilon = 1e-10
                        train_prob = np.array([train_counts.get(v, 0) + epsilon for v in all_values])
                        val_prob = np.array([val_counts.get(v, 0) + epsilon for v in all_values])
                        
                        # Renormalize after adding epsilon
                        train_prob = train_prob / train_prob.sum()
                        val_prob = val_prob / val_prob.sum()
                
                # Compute KL divergence: KL(train || val)
                # Measures how much information is lost when val distribution is used to approximate train
                kl_divergence = np.sum(kl_div(train_prob, val_prob))
                all_kl_divergences[col] = float(kl_divergence)  # Convert to float for JSON serialization
                
                # Log one line per column with clear explanation
                if is_numeric:
                    # For numeric columns: drift means value ranges/distributions differ
                    train_mean = train_df[col].mean()
                    val_mean = val_df[col].mean()
                    mean_diff_pct = abs((val_mean - train_mean) / train_mean * 100) if train_mean != 0 else 0
                    
                    # Check null ratio difference
                    train_total = len(train_df[col])
                    train_non_null = train_df[col].notna().sum()
                    train_null_pct = (train_total - train_non_null) / train_total * 100 if train_total > 0 else 0
                    
                    val_total = len(val_df[col])
                    val_non_null = val_df[col].notna().sum()
                    val_null_pct = (val_total - val_non_null) / val_total * 100 if val_total > 0 else 0
                    null_pct_diff = abs(train_null_pct - val_null_pct)
                    null_warning = f" | Null diff: {null_pct_diff:.1f}%" if null_pct_diff > 5.0 else ""
                    
                    logger.info(f"📊 {col:40s} | KL={kl_divergence:6.3f} | Drift: {'HIGH' if kl_divergence > 1.0 else 'OK'} | "
                              f"Train/val mean difference: {mean_diff_pct:.1f}%{null_warning} | "
                              f"Means differ significantly between train and validation sets")
                else:
                    # For categorical/text columns: drift means value frequencies differ
                    # train_unique and val_unique already calculated above
                    train_top_val = train_df[col].value_counts().index[0] if len(train_df[col].dropna()) > 0 else "N/A"
                    val_top_val = val_df[col].value_counts().index[0] if len(val_df[col].dropna()) > 0 else "N/A"
                    top_match = "✓" if train_top_val == val_top_val else "✗"
                    
                    # Check null ratio difference (already calculated above)
                    null_warning = ""
                    if null_pct_diff > 5.0:
                        null_warning = f" | Null diff: {train_null_pct:.1f}% vs {val_null_pct:.1f}% ({null_pct_diff:.1f}% diff)"
                    
                    if train_unique > 100 or val_unique > 100:
                        # Text column (many unique values) - KL is based on string length distribution
                        # Calculate std of value frequencies for additional context
                        train_freq_std = train_df[col].value_counts(normalize=True).std()
                        val_freq_std = val_df[col].value_counts(normalize=True).std()
                        std_diff = abs(train_freq_std - val_freq_std)
                        # Use train std as reference to see if difference is > 1 std
                        std_diff_in_stds = std_diff / train_freq_std if train_freq_std > 0 else 0
                        std_warning = ">1σ" if std_diff_in_stds > 1.0 else "≤1σ"
                        
                        logger.info(f"📝 {col:40s} | KL={kl_divergence:6.3f} | Drift: {'HIGH' if kl_divergence > 1.0 else 'OK'} | "
                                  f"Text length dist differs: train has {train_unique} unique values, val has {val_unique} | "
                                  f"Most common values match: {top_match} | "
                                  f"Std diff: {std_diff:.4f} ({std_diff_in_stds:.2f}σ, {std_warning}){null_warning} | "
                                  f"Different string length distributions between train and validation")
                    else:
                        # Categorical column (few unique values)
                        logger.info(f"📋 {col:40s} | KL={kl_divergence:6.3f} | Drift: {'HIGH' if kl_divergence > 1.0 else 'OK'} | "
                                  f"Category frequencies differ: train has {train_unique} categories, val has {val_unique} | "
                                  f"Top category match: {top_match}{null_warning} | "
                                  f"Different category proportions between train and validation")
                
                # Check threshold - only flag if severe (> 1.0)
                if kl_divergence > 1.0:  # Changed from kl_threshold (0.1) to 1.0
                    issues_found.append((col, kl_divergence))
                    
            except Exception as e:
                logger.warning(f"⚠️  {col:40s} | Could not compute drift: {e}")
                continue
        
        # Summary - only show if issues found
        if issues_found:
            logger.warning(f"⚠️  Train/val distribution drift detected in {len(issues_found)} columns (KL > 1.0): {', '.join([f'{col} (KL={kl:.2f})' for col, kl in issues_found[:5]])}{' ...' if len(issues_found) > 5 else ''}")
        
        return all_kl_divergences

    async def work(self, status_func):
        columns = len(self.df.columns)
        self._computeDescStats()
        await status_func(
            incremental_status={
                "status": "Processing",
                "message": f"Detecting column types for {columns} columns..",
            }
        )
        self._detectColumnTypes()
        await status_func(
            incremental_status={
                "status": "Processing",
                "message": f"Working on possible enrichments for {columns} columns...",
            }
        )
        self._enrichAllColumns()
        await status_func(
            incremental_status={
                "status": "Processing",
                "message": "Finishing column processing...",
            }
        )
        self._dropLowValueColumns()
        self._computeDescStats()  # do it again to catch up
        self._printDetectorResults(f"{self.dataset_title} (ENRICHED)")

    @classmethod
    async def create(
        cls,
        # filename=None,
        df=None,
        detect_only=False,
        debug_detector=None,
        ignore_cols=[],
        limit_rows=None,
        encoder_overrides=None,
        project_row_meta_data=None,
        async_status_update_function=None,
    ):
        logger.info("crazy .create() called")
        fids = cls(
            df=df,
            detect_only=detect_only,
            debug_detector=debug_detector,
            ignore_cols=ignore_cols,
            limit_rows=limit_rows,
            encoder_overrides=encoder_overrides,
            project_row_meta_data=project_row_meta_data,
            standup_only=True,
        )
        await fids.work(async_status_update_function)
        return fids

    @property
    def detectOutputData(self):
        return self._detectOutputData

    # def removeProblematicColumn(self, colName):
    #     self._removeColumn(colName)
    #     return

    def _dropLowValueColumns(self):
        # if the entire column is null, kill it.
        # consider other options later.
        for c in self.df.columns:
            nonNullCounts = self._colsNonNullsCount.get(c)
            if nonNullCounts is None:
                # Well this is a bug
                logger.error(f"BUG: missing {c} from non null counts")
                continue
            # endif

            if nonNullCounts == 0:
                logger.info(f"DROPPING ALL NULL COLUMN: {c}")
                # self.df = self.df.drop(c, axis=1)
                self._removeColumn(c)
        # endfor
        return

    def _removeColumn(self, colName):
        logger.info(f"_removeColumn called with {colName}")
        self.df = self.df.drop(colName, axis=1)
        try:
            del self._colsNonNullsCount[colName]
        except:
            pass
        try:
            del self._colsUniquesCount[colName]
        except:
            pass
        try:
            del self._colsTopNValues[colName]
        except:
            pass
        try:
            del self._detectors[colName]
        except:
            pass

        try:
            del self._colCodecs[colName]
        except:
            pass

        try:
            del self._hh[colName]
        except:
            pass

        for idx, entry in enumerate(self._colTree):
            if colName in entry:
                entry.remove(colName)
                self._colTree[idx] = entry
        return

    def countColumns(self):
        return len(self.df.columns)

    def _computeDescStats(self):
        """OK to call multiple times to update for new columns."""
        colNames = list(self.df.columns)
        for c in colNames:
            if self._colsNonNullsCount.get(c) is None:
                # s_replace = self.df[c].replace(['NaN', 'None', '', 'nan'], float('nan'))
                # s_replace = s_replace[s_replace.notnull()]
                notNulls = sum(self.df[c].notna())  # (NUM_ROWS_TO_CHECK)

                # notNulls = sum(self.df[c].notna())        # needs work -- this isn't right.
                try:
                    uniqueCount = len(self.df[c].unique())
                    # ... this can happen if the column fields are a list.
                except TypeError:
                    logger.warn(f"warning -- type error from unique() for column {c}")
                    uniqueCount = len(self.df[c])

                self._colsNonNullsCount[c] = notNulls
                self._colsUniquesCount[c] = uniqueCount

                try:
                    self._colsTopNValues[c] = (
                        self.df[c].value_counts().nlargest(5).to_dict()
                    )
                except:
                    pass

                # if < 75% unique, calc a dist?
        # endfor
        return

    def numUniquesDict(self):
        return self._colsUniquesCount

    def numNotnullsDict(self):
        return self._colsNonNullsCount

    def histogramsDict(self):
        if self._hh is not None:
            return self._hh

        results = {}
        with ProcessPoolExecutor() as executor:
            futures = {}
            for col in self.df.columns:
                futures[executor.submit(self.histogramForColumn, col)] = col
            
            for future in as_completed(futures):
                col = futures[future]
                try:
                    results[col] = future.result()
                except Exception as e:
                    logger.error(f"Error processing column {col}: {e}")
        
        self._hh = results
        print("histogramsDict: self._hh END --> ", self._hh)
        return self._hh

    # def _tsne_one_col(self, c):
    #     from sklearn.manifold import TSNE

    #     bestDetector = self._detectors.get(c)
    #     if bestDetector is not None and bestDetector.type_name == "free_string":
    #         os.environ["TOKENIZERS_PARALLELISM"] = "false"

    #         embeddings = []
    #         num_nans = 0

    #         NUM_SAMPLES = 500

    #         sampled_values = self.df[c].sample(min(len(self.df), NUM_SAMPLES))
    #         for x in sampled_values:
    #             if x != x:
    #                 num_nans += 1
    #                 continue
    #             v = preview_cached_sentence_model_encode(x)
    #             embeddings.append(v)

    #         num_rows = len(self.df)
    #         perplexity_default = min(30, int(num_rows / 5))
    #         try:
    #             tsne_model = TSNE(
    #                 n_components=2, perplexity=perplexity_default, n_iter=1000, random_state=42
    #             )  # , n_jobs=1)
    #             X = np.array(embeddings)
    #             transformed_data = tsne_model.fit_transform(X)
    #             xform_list = transformed_data.tolist()
    #             result = {
    #                 "sample_size": NUM_SAMPLES,
    #                 "embedding_model": "all-MiniLM-L12-v2",  # Using global model from string_codec
    #                 "pts": xform_list,
    #             }
    #             return result
    #         except:
    #             traceback.print_exc()
    #     return {}
    
    # def tsne2dDict(self):
    #     """
    #     This is used to build the 'sparkline' previews that we show in the UI on the data set.

    #     We are just doing this on string columns right now.
    #     """
    #     str_cols = []
    #     for c in list(self.df.columns):
    #         bestDetector = self._detectors.get(c)
    #         if bestDetector is not None and bestDetector.type_name == "free_string":
    #             str_cols.append(c)
        
    #     # OK spin up some processes!
    #     results = {}
    #     # TSNE already jobs multiprocessing, so don't kill the box... limit to 4 workers.
    #     with ProcessPoolExecutor(max_workers=4) as executor:
    #         futures = {}
    #         for col in str_cols:
    #             futures[executor.submit(self._tsne_one_col, col)] = col

    #         for future in as_completed(futures):
    #             col = futures[future]
    #             try:
    #                 results[col] = future.result()
    #             except Exception as e:
    #                 logger.error(f"Error processing column {col}: {e}")

    #     return results

    def possiblePositiveValues(self):
        hh = self.histogramsDict()
        pp = {}
        for c, v in hh.items():
            if len(v.get("buckets", [])) == 2:
                # binary column (which is clean without noise -- but we're just trying to pick a good default.)
                tt = sum(v.get("n", [0]))
                for idx, k in enumerate(v.get("buckets")):
                    t = v.get("n")[idx]
                    if t < (tt / 2):
                        pp[c] = k
        return pp

    def histogramForColumn(self, c):
        print("histogramForColumn: ", c)
        h = {"buckets": [], "n": []}

        col_list = self.df[c].dropna().tolist()
        val_counts = dict(Counter(col_list))

        lists_of_set_h = self.debug_detectors_raw.get(c, {}).get(
            "lists_of_a_set_histogram"
        )
        if lists_of_set_h is not None:
            col_list = list(lists_of_set_h.keys())
            val_counts = lists_of_set_h

        if len(val_counts) < 100:
            h["buckets"] = list(val_counts.keys())
            h["n"] = list(val_counts.values())
        else:
            # Do a numpy histogram for the others.
            try:
                num_samples, bins = np.histogram(col_list, bins=10)
                h["buckets"] = bins.tolist()
                h["n"] = num_samples.tolist()
            except:
                traceback.print_exc()
        print("histogramForColumn: ", c, "-->", h)
        return h

    def _buildDetectorOneColumn(self, c):
        numRows = float(len(self.df))
        bestDetector = self._detectors.get(c)
        conf = bestDetector.confidence()
        non_nulls_count = self._colsNonNullsCount[c]
        try:
            nonNull = float(non_nulls_count) / float(numRows)
        except:
            traceback.print_exc()
            nonNull = None

        if non_nulls_count == 0:
            uniques = 0
        else:
            uniques = float(self._colsUniquesCount[c]) / float(non_nulls_count)

        result = {
            "type": bestDetector.type_name,
            "conf": conf,
            "nonnull": nonNull,
            "unique": uniques,
        }

        if bestDetector.type_name == "set":
            # throw in the first 100 values.
            unique_values = list(self.df[c].unique())
            if len(unique_values) > 100:
                unique_values = unique_values[:100]
            str_unique_values = []
            for uv in unique_values:
                if uv != uv:
                    continue
                str_unique_values.append(str(uv))
            result["unique_values"] = str_unique_values

        elif bestDetector.type_name == "lists_of_a_set":
            # throw in the first 100 values... but we need to split the lists.
            try:
                goodies = bestDetector.partsCountDict
            except:
                traceback.print_exc()

            # goodies is { val: count } dictionary.
            unique_values = list(goodies.keys())
            if len(unique_values) > 100:
                unique_values = unique_values[:100]

            str_unique_values = []
            for uv in unique_values:
                if uv != uv:
                    continue
                str_unique_values.append(str(uv))
            result["unique_values"] = str_unique_values
            result["lists_of_a_set_histogram"] = goodies

        elif (
            bestDetector.type_name != "vector"
        ):  # or bestDetector.type_name == 'free_string':
            if self._colsUniquesCount[c] <= 100:
                # grab them even if they are not a set... b/c sometimes they are.
                unique_values = list(self.df[c].unique())
                str_unique_values = []
                for uv in unique_values:
                    if uv != uv:
                        continue
                    str_unique_values.append(str(uv))
                result["unique_values"] = str_unique_values
        return result

    def _buildDetectorDict(self):
        self.debug_detectors_raw = {}

        results = {}
        with ProcessPoolExecutor() as executor:
            futures = {}
            for col in self.df.columns:
                futures[executor.submit(self._buildDetectorOneColumn, col)] = col

            for future in as_completed(futures):
                col = futures[future]
                try:
                    results[col] = future.result()
                except Exception as e:
                    logger.error(f"Error processing column {col}: {e}")
        self.debug_detectors_raw = results
        return self.debug_detectors_raw

    def _printDetectorResults(self, dataset_title="DATASET"):
        """
        Print column detection results with improved formatting.
        
        Args:
            dataset_title: Title to identify what dataset this is (e.g., "TRAINING SET", "VALIDATION SET")
        """
        d = []

        colNames = list(self.df.columns)
        colNames.sort()

        # Use fixed 80-character width for column names instead of 60
        col_name_width = 80
        
        fmt = "%" + str(col_name_width + 2) + "s" + "   %15s   %5s   %10s   %9s"
        eqLine = (
            ("=" * (col_name_width + 2))
            + "   "
            + ("=" * 15)
            + "   =====   "
            + ("=" * 10)
            + "    "
            + ("=" * 8)
        )

        # Print title header
        total_width = col_name_width + 2 + 3 + 15 + 3 + 5 + 3 + 10 + 4 + 8
        title_line = f"📊 {dataset_title} COLUMN ANALYSIS"
        print()
        print("=" * total_width)
        print(title_line.center(total_width))
        print("=" * total_width)

        print(fmt % ("col name", "type", "conf", "non-null %", "unique %"))
        print(eqLine)

        numRows = float(len(self.df))
        for c in colNames:
            # Truncate column name to fit in 60 characters, show ... if truncated
            display_col_name = c
            if len(c) > col_name_width:
                display_col_name = c[:col_name_width-3] + "..."
            
            bestDetector = self._detectors.get(c)
            if bestDetector is None:
                d.append(
                    {
                        "col_name": c,
                        "type": "????",
                        "conf": "????",
                        "non-null %": "????",
                        "unique %": "????",
                        "top few values": "????",
                    }
                )
                print(fmt % (display_col_name, "????", "????", "????", "????"))
            else:
                # meta = bestDetector.get_meta_description() or ""
                conf = "%1.3f" % bestDetector.confidence()
                non_nulls_count = self._colsNonNullsCount[c]
                nonNull = "%1.1f" % (100 * float(non_nulls_count) / numRows)
                if non_nulls_count == 0:
                    uniques = "--"
                else:
                    uniques = "%1.1f" % (
                        100 * float(self._colsUniquesCount[c]) / float(non_nulls_count)
                    )

                # Enhanced stats display
                stats_info = ""
                if bestDetector.type_name == "scalar":
                    # Show Q1, median, Q3 for scalar columns
                    try:
                        col_data = self.df[c].dropna()
                        if len(col_data) > 0:
                            q1 = col_data.quantile(0.25)
                            median = col_data.quantile(0.50)
                            q3 = col_data.quantile(0.75)
                            stats_info = f"  Q1={q1:.2f}, Q2={median:.2f}, Q3={q3:.2f}"
                    except Exception:
                        pass
                elif bestDetector.type_name == "url":
                    # Show URL statistics: protocol distribution, TLD breakdown, free domain %
                    try:
                        from featrix.neural.url_parser import parse_url
                        from featrix.neural.hubspot_free_domains_list_may_2025 import is_free_email_domain
                        
                        col_data = self.df[c].dropna().astype(str)
                        if len(col_data) > 0:
                            # Sample for efficiency (max 100 URLs)
                            sample_size = min(len(col_data), 100)
                            sample = col_data.sample(n=sample_size, random_state=42)
                            
                            parsed = [parse_url(url, check_free_domain_fn=is_free_email_domain) for url in sample]
                            
                            # Protocol distribution
                            protocols = [p.protocol for p in parsed if p.is_valid]
                            protocol_counts = {}
                            for proto in protocols:
                                protocol_counts[proto] = protocol_counts.get(proto, 0) + 1
                            top_protocol = max(protocol_counts.items(), key=lambda x: x[1])[0] if protocol_counts else "unknown"
                            
                            # TLD breakdown
                            tlds = [p.tld for p in parsed if p.is_valid and p.tld]
                            tld_counts = {}
                            for tld in tlds:
                                tld_counts[tld] = tld_counts.get(tld, 0) + 1
                            top_tlds = sorted(tld_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                            tld_str = ", ".join([f".{tld}" for tld, _ in top_tlds]) if top_tlds else "N/A"
                            
                            # Free domain percentage
                            free_count = sum(1 for p in parsed if p.is_free_domain)
                            free_pct = (free_count / len(parsed)) * 100 if parsed else 0
                            
                            stats_info = f"  protocol={top_protocol}, TLDs=[{tld_str}], free={free_pct:.0f}%"
                    except Exception as e:
                        import logging
                        logging.getLogger(__name__).debug(f"Error computing URL stats: {e}")
                        pass
                elif bestDetector.type_name in ["set", "free_string"]:
                    # Show popular values for categorical columns
                    try:
                        col_data = self.df[c].dropna()
                        if len(col_data) > 0:
                            value_counts = col_data.value_counts().head(3)
                            popular_values = ", ".join([f"'{val}' ({count})" for val, count in value_counts.items()])
                            stats_info = f"  {popular_values}"
                    except Exception:
                        pass
                
                print(fmt % (display_col_name, bestDetector.type_name, conf, nonNull, uniques) + stats_info)

                d.append(
                    {
                        "col_name": c,
                        "type": bestDetector.type_name,
                        "conf": conf,
                        "non-null %": nonNull,
                        "unique %": uniques,
                        "stats": stats_info,
                    }
                )

        # endfor
        print(eqLine)
        print(f"{len(self.df)} rows x {len(colNames)} column{'s' if len(colNames) != 1 else ''}")
        print("=" * total_width)
        print()

        self._detectOutputData = d
        return

    def __len__(self):
        return len(self.df)

    def get_detector_for_col_name(self, colName):
        return self._detectors.get(colName)

    def _addDetectorDebugInfo(self, colName, detectorName, confidence, debugInfo=None):
        existing = self.detectorDebugInfo.get(colName, {})
        # detectorInfo = existing.get(detectorName, {})

        detectorInfo = {"confidence": confidence}

        if debugInfo is not None:
            assert type(debugInfo) == dict
            if len(debugInfo) > 0:
                # OK...
                detectorInfo["debug"] = debugInfo

        existing[detectorName] = detectorInfo
        self.detectorDebugInfo[colName] = existing
        return

    def getDetectorDebugInfo(self):
        return self.detectorDebugInfo

    def printDetectorDebugInfo(self):
        pprint(self.detectorDebugInfo)
        return

    def _createDetectorByName(self, name, colName):
        detectorClass = DetectorStrDict.get(name)
        assert detectorClass is not None
        newDetector = detectorClass(
            colSample=self.df[colName],
            debugColName=colName,
            numUniques=self._colsUniquesCount[colName],
            numNotNulls=self._colsNonNullsCount[colName],
        )
        newDetector._confidence = 2.0
        return newDetector

    def _detectColumnTypesForColName(self, colName, detect_only=False):
        """
        By the time this is called, we've already handled the encoder_overrides.
        """
        c = colName
        bestDetector = None

        for detector in DetectorList:
            newDetector = detector(
                colSample=self.df[c],
                debugColName=c,
                numUniques=self._colsUniquesCount[c],
                numNotNulls=self._colsNonNullsCount[c],
            )

            detectorName = newDetector.get_codec_name()
            if detectorName is None:
                detectorName = str(newDetector)
            debugInfo = {}
            if detectorName == self.debug_detector:
                debugInfo = newDetector.get_debug_info()
            self._addDetectorDebugInfo(
                colName, detectorName, newDetector.confidence(), debugInfo
            )

            if newDetector.confidence() <= 0:
                # not a fit... keep going.
                continue

            if bestDetector is None:
                bestDetector = newDetector
            else:
                # we use >= here with the assumption that if we find a better or equal
                # match in as we grind through the detectors, we prefer the latter.
                # this means the DetectorList order matters.
                if newDetector.confidence() >= bestDetector.confidence():
                    bestDetector = newDetector
        # endfor

        if bestDetector is None:
            logger.error(f"*** We found nothing to use for column {c}")
        else:
            meta = bestDetector.get_meta_description()
            if meta is None:
                meta = ""
            else:
                meta = " (meta: %s)" % meta

            # Now that we've picked the detector, convert values if we need them.
            bestDetector.cast_values(self.df[c])
            # bestDetector.free_memory()
            self._detectors[c] = bestDetector
        # endif

        return bestDetector

    def insert_casted_values(self, colName, castedValues):
        if self.casted_df is None:
            self.casted_df = pd.DataFrame()
        
        self.casted_df[colName] = castedValues
        return

    def _detectColumnTypes(self):
        self._detectors = {}
        for c in list(self.df.columns.values):
            overrideEncoder = self.encoderOverrides.get(c)
            if overrideEncoder is not None:
                logger.error(
                    "overriding auto-detection of column %s to %s"
                    % (c, overrideEncoder)
                )
                res = self._createDetectorByName(overrideEncoder, c)
                if res.has_casted_values:
                    casted_values = res.cast_values(self.df[c])
                    self.insert_casted_values(c, casted_values)
                self._detectors[c] = res
            else:
                # Always detect columns - removed autodetect_columns parameter
                if c in self.ignore_cols:
                    continue
                
                res = self._detectColumnTypesForColName(c)
        return

    def _createColSpecEntry(self, name, detector):
        return {
            name: detector.get_codec_name()
        }  # { "name": name, "codec": detector.get_codec_name() }

    def _enrichAllColumns(self):
        self._enrichedDataFrames = {}
        self._finalEnrichedDataFrames = {}
        self._colTree = [[]]
        self._colCodecs = None
        self._enrichedDataDetectors = None

        enrichedMap = {}

        for colName, detector in self._detectors.items():
            logger.debug(f"Enriching column {colName} - detector {detector}")

            # First lets get the colTree setup with our main columns if there was an encode-able detector
            if detector.is_encodeable():
                assert colName not in self._colTree[0], "Duplicate colName %s" % colName
                self._colTree[0].append(colName)
            else:
                logger.error("<< WARNING << %s does not have an encodeable codec?!" % colName)

            enricherClass = EnrichMap.get(detector.get_type_name())
            logger.debug(f"... {colName} - enricher {enricherClass}")
            assert colName is not None, "what the hell!"

            if enricherClass is None:
                # If there is no enrichment class, we can move on
                continue

            logger.info(f"Enriching using {enricherClass} for {colName}")
            assert issubclass(
                enricherClass, FeatrixFieldBaseEnrichment
            ), f"enrichment object {enricherClass} does not seem to be a FeatrixFieldBaseEnrichment"
            enricher = enricherClass(detector)

            _start = datetime.now()
            new_df = enricher.enrich(self.df[colName])
            logger.info(
                f"Enriched column {colName} in {(datetime.now() - _start).total_seconds()} seconds"
            )

            if new_df is None or len(new_df) == 0:
                continue
            self._enrichedDataFrames[colName] = new_df

            enrichedColNames = enricher.get_enriched_names()

            d = {}
            for name in enrichedColNames:
                looksCool = enricher.looks_interesting(name)
                if looksCool:
                    v = enricher.get_enriched_data(name)
                    d[name] = v
                    self._finalEnrichedDataFrames[name] = v
            # endfor

            enrichedMap[colName] = d
        # endfor

        # Now add the enriched values to the dataframe and run the detectors on them.
        for k, enriched_df in enrichedMap.items():
            newColGroup = []
            for colName, data in enriched_df.items():  # .columns.values:
                if colName.endswith("_featrix_untie_scalar"):
                    # FIXME: HACK: we need a way to return an explicit type
                    self.df[colName] = data
                    bestDetector = FeatrixFieldScalarDetection(
                        colSample=self.df[colName], debugColName=colName
                    )
                    meta = bestDetector.get_meta_description()
                    if meta is None:
                        meta = ""
                    else:
                        meta = " (meta: %s)" % meta
                    logger.info(
                        f">>> [2] We will treat column {colName} as a {bestDetector.type_name} (confidence = {bestDetector.confidence()}) {meta}"
                    )
                    bestDetector.cast_values(self.df[colName])
                    self._detectors[colName] = bestDetector
                    # assert colName not in newColGroup
                    # newColGroup.append(colName)
                else:
                    self.df[colName] = data  # enriched_df[colName]
                    self._computeDescStats()  #
                    bestDetector = self._detectColumnTypesForColName(
                        colName
                    )  # pick the detected type.
                # endif
                self.enrichment_columns.append(colName)

                if bestDetector is not None:
                    assert colName not in newColGroup
                    newColGroup.append(colName)
                # endif
            # endfor

            if len(newColGroup) > 0:
                self._colTree.append(newColGroup)
            # endif
        # endfor

        self._enrichedDataFrames = {}
        self._enrichedDataDetectors = {}
        # get

    def column_tree(self):
        return self._colTree

    def free_memory(self):
        logger.info("----------------------------------------  free_memory called")
        for k, v in self._detectors.items():  # get(colName)
            try:
                v.free_memory()
            except:
                traceback.print_exc()
        return

    def get_casted_values_for_column_name(self, colName):
        detector = self._detectors.get(colName)
        assert detector is not None, "missing a detector for %s" % colName
        return detector.cast_values(self.df[colName])

    def get_columns_with_codec_count(self):
        if self._colCodecs is None:
            self.column_codecs()  # Initialize _colCodecs if not already done
        return len(self._colCodecs)

    def sample_complex_data(self):
        """
        We have multiple data sets in our self.df -- and the sections (as defined by the ProjectRowMetaData objects
        in self.project_row_meta_data_list) each need to be part of the sample.  We define a minimum number of rows
        from each dataset and try to split up the sampling across the sections to get a good mix that matches the
        input weights.  Note that we might end up with a sampling slightly bigger than our max, since we force a
        floor on each dataset (minimum number of rows) but don't try to rework the other sizes.  It's ok, since we
        made up the row limit to begin with :)
        """
        dfs = []
        logger.info(
            f"Dataset too large, sampling data across {len(self.project_row_meta_data_list)} segments..."
        )
        for idx, segment in enumerate(self.project_row_meta_data_list):
            rows = max(
                int(self.limit_rows * segment.overall_percent), MINIMUM_DATASET_SAMPLE
            )
            if segment.num_rows < rows:
                rows = segment.num_rows
            logger.info(
                f"...segment {idx}:{segment.label}: {segment.overall_percent}% of data, "
                f"{rows} out of {segment.num_rows}"
            )
            dfs.append(
                # Take the old df range for this segment and sample it down to ROWS, and be sure to reset the index
                self.df[
                    segment.row_idx_start : segment.row_idx_start + segment.num_rows
                ]
                .sample(n=rows)
                .reset_index(drop=True)
            )
            segment.original_rows = segment.num_rows
            segment.num_rows = rows
        self.df = pd.concat(dfs)
        sz = sum([_.num_rows for _ in self.project_row_meta_data_list])
        logger.info(f"New data set is {len(self.df)} rows, meta says {sz}")
        return
    
    def column_codecs(self):
        # print(">> column_codecs CALLED")
        # returns a list of column groups
        #  [ ... ], [ .. { <...> : "set" }, ]
        # open_dt, closed_dt are separate groups.
        #
        # pass #return { keyName: "set", keyName2: "scalar"}
        if self._colCodecs is None or len(self._colCodecs) == 0:
            colNamesSoFar = []
            self._colCodecs = {}
            # Initialize column tree with first group for main columns
            self._colTree = [[]]
            
            for colName, detector in self._detectors.items():
                if not detector.is_encodeable():
                    continue

                if colName not in colNamesSoFar:
                    colNamesSoFar.append(colName)
                    self._colCodecs[colName] = ColumnType(detector.get_codec_name())
                    # Add to first group in column tree
                    assert colName not in self._colTree[0], "Duplicate colName %s" % colName
                    self._colTree[0].append(colName)

            if self._enrichedDataDetectors is not None:
                for colName, detector in self._enrichedDataDetectors.items():
                    if not detector.is_encodeable():
                        continue

                    if colName not in colNamesSoFar:
                        colNamesSoFar.append(colName)
                        self._colCodecs[colName] = ColumnType(detector.get_codec_name())
                        # Add to first group in column tree
                        if colName not in self._colTree[0]:
                            self._colTree[0].append(colName)

        return self._colCodecs




"""
    def untie_create_delta_times(self):
        # Create all the delta time columns.
        if len(self.maybe_timestamps) == 0:
            return

        all = list(itertools.combinations(self.maybe_timestamps, 2))
        print("ALL DT PAIRS: ", all)

        new_cols = []
        for entry in all:
            print(entry)

            days_name = f"featrix_delta_time_{entry[0]}_{entry[1]}_days"

            lhs = f"featrix_timestamp_{entry[0]}"
            rhs = f"featrix_timestamp_{entry[1]}"
            self.df[days_name] = (self.df[lhs] - self.df[rhs]).dt.days.astype('float')
            #self.df[days_name] = (self.df[entry[0]] - self.df[entry[1]]).dt.days

            new_cols.append(days_name)
        # endfor

        print(f"days_name == {days_name}")
        print(self.df[days_name])
        self.remove_temp_featrix_timestamp_columns()

        return
"""


    # def df_whack_columns_if_needed(
    #     self,
    #     input_file: Optional[str | Path | BinaryIO] = None,
    #     dataframe: Optional[pd.DataFrame] = None,
    # ):
    #     if self.config_split_columns is None:
    #         return input_file or dataframe

    #     cols_to_drop = []
    #     if input_file:
    #         df = featrix_wrap_pd_read_csv(input_file)
    #     else:
    #         df = dataframe
    #     # print(f"df_whack_columns_if_needed... {input_file} ... df = {len(df) if df is not None else 'None'}")
    #     for entry in self.config_split_columns:
    #         col_name = entry.get("col_name")
    #         split_token = entry.get("split_token")
    #         keep_mask = entry.get("keep_mask")
    #         cols_to_drop.append(col_name)

    #         num_sub_columns = None
    #         exploded_cols = {}
    #         the_data = df[col_name]
    #         num_starting_nans = 0
    #         is_first_row = True
    #         for idx, row in enumerate(the_data):
    #             if row != row:  # NaN... and what if NaN is first, ugh.
    #                 if is_first_row:  # we've never had a row before w/o nans
    #                     num_starting_nans += 1
    #                 else:
    #                     for k in exploded_cols.keys():
    #                         exploded_cols[k].append(row)  # append a nan to every column
    #             else:
    #                 parts = row.split(split_token)
    #                 # print(numStartingNans)
    #                 if num_starting_nans > 0:
    #                     # this is our first non-nan row
    #                     # so we need to append a bunch of nans.
    #                     # b/c until we did the first split, we didn't know how many parts.
    #                     for nan_idx in range(num_starting_nans):
    #                         for part_idx, _ in enumerate(parts):
    #                             if keep_mask is not None:
    #                                 if not keep_mask[part_idx]:
    #                                     continue
    #                             if is_first_row:
    #                                 exploded_cols[part_idx] = []

    #                             exploded_cols[idx].append(np.nan)

    #                         is_first_row = False
    #                     num_starting_nans = 0
    #                 # endif

    #                 for part_idx, p in enumerate(parts):
    #                     if keep_mask is not None:
    #                         if not keep_mask[part_idx]:
    #                             continue
    #                     if is_first_row:
    #                         exploded_cols[part_idx] = []

    #                     exploded_cols[part_idx].append(p)
    #                 is_first_row = False

    #         # OK... now we should have columns!
    #         for col_idx, col_data in exploded_cols.items():
    #             if keep_mask is not None:
    #                 if not keep_mask[col_idx]:
    #                     print(
    #                         "skipping split col idx %s from keep_mask = %s"
    #                         % (col_idx, keep_mask)
    #                     )
    #                     continue
    #             new_name = f"{col_name}_{col_idx}"
    #             df[new_name] = col_data
    #     df = df.drop(columns=cols_to_drop)
    #     if input_file:
    #         new_file = input_file + ".whacked"
    #         df.to_csv(new_file)
    #         return new_file
    #     else:
    #         return df

