import sqlite3
import pandas as pd
import faiss
import numpy as np
import pickle
import os
import sys
import logging
import json
import ast
import re
import requests
import time
import shutil
import traceback
from collections import defaultdict
from typing import Dict, List, Set, Any
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import uuid4

from pathlib import Path

print("structureddata.py")
print(sys.path)

# Set up Python path for featrix imports
try:
    from featrix.neural.logging_config import configure_logging
except (ModuleNotFoundError, ImportError):
    # Add current directory to path for featrix imports
    p = Path(__file__).parent
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
    
    try:
        from featrix.neural.logging_config import configure_logging
    except (ModuleNotFoundError, ImportError):
        # Fallback to basic logging if module not found
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s'
        )
        def configure_logging():
            pass

configure_logging()
logger = logging.getLogger(__name__)

from featrix.neural.device import device

from featrix.neural.featrix_csv import featrix_wrap_pd_read_csv
from featrix.neural.featrix_json import try_jsonl_file, featrix_wrap_read_json_file
from featrix.neural.input_data_file import FeatrixInputDataFile
from featrix.neural.input_data_set import FeatrixInputDataSet

class CSVtoDB:
    def __init__(self, column_overrides=None, json_analysis_config=None):
        db_path: str = "data.db"

        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.index = None
        
        self.json_transformations = {}  # Store JSON transformation metadata
        self.column_overrides = column_overrides or {}  # Store column overrides
        self.json_parseable_columns = []  # Track columns containing JSON-parseable dicts or lists of dicts
        
        # JSON analysis configuration - NO MORE HARDCODED VALUES!
        default_config = {
            'sample_size': 100,                    # Number of rows to sample per column  
            'stable_key_threshold': 0.1,           # Frequency threshold for expanding keys (10% - much more useful!)
            'min_objects_for_analysis': 2,         # Minimum JSON objects needed for analysis
            'max_example_values': 5,               # Max example values to store per key
            'example_value_max_length': 100,       # Max length of example values
            'max_nesting_depth': 0,                # DISABLED: No nested expansion at all
            'max_columns_per_nested_object': 1,    # AGGRESSIVE: Convert anything with >1 nested key to list format
            'nested_list_format': True,            # Enable key=value list format for large nested objects
        }
        
        if json_analysis_config:
            default_config.update(json_analysis_config)
        
        self.json_config = default_config

    def _safe_parse_dict_like(self, value: str) -> Dict:
        """
        Safely parse dict-like strings including:
        - Valid JSON: {"key": "value"}
        - Python dict literals: {'key': 'value', 'num': 123}
        - Malformed JSON: {key: 'value'} (unquoted keys)
        - Mixed quotes and other common issues
        
        Uses ast.literal_eval() which is safe (no code execution).
        
        Args:
            value: String that might contain a dict-like structure
            
        Returns:
            Parsed dictionary or None if parsing fails
        """
        if not isinstance(value, str):
            return None
            
        value = value.strip()
        if not (value.startswith('{') and value.endswith('}')):
            return None
        
        # Strategy 1: Try standard JSON parsing first
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                logger.debug(f"✅ FUZZY PARSE: Standard JSON succeeded")
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
        
        # Strategy 2: Try fixing common JSON issues and parse again
        try:
            # Fix common issues:
            # 1. Single quotes to double quotes (but be careful with strings containing single quotes)
            # 2. Unquoted keys
            fixed_value = self._preprocess_malformed_json(value)
            
            parsed = json.loads(fixed_value)
            if isinstance(parsed, dict):
                logger.debug(f"✅ FUZZY PARSE: Fixed JSON succeeded: {value[:50]}...")
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
            
        # Strategy 3: Try ast.literal_eval for Python dict literals (SAFE - no code execution)
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, dict):
                logger.debug(f"✅ FUZZY PARSE: Python dict literal succeeded: {value[:50]}...")
                return parsed
        except (ValueError, SyntaxError):
            pass
        
        # Strategy 4: Try more aggressive preprocessing + ast.literal_eval
        try:
            # Handle cases like: {key: 'value'} -> {'key': 'value'}
            preprocessed = self._aggressive_dict_preprocessing(value)
            parsed = ast.literal_eval(preprocessed)
            if isinstance(parsed, dict):
                logger.debug(f"✅ FUZZY PARSE: Aggressive preprocessing succeeded: {value[:50]}...")
                return parsed
        except (ValueError, SyntaxError):
            pass
        
        logger.debug(f"❌ FUZZY PARSE: All parsing strategies failed for: {value[:50]}...")
        return None
    
    def _safe_parse_list_of_dicts(self, value: str) -> List[Dict]:
        """
        Safely parse list-of-dicts-like strings including:
        - Valid JSON: [{"key": "value"}, {"key2": "value2"}]
        - Python list literals: [{'key': 'value'}, {'key2': 'value2'}]
        - Malformed JSON with common issues
        
        Uses ast.literal_eval() which is safe (no code execution).
        
        Args:
            value: String that might contain a list-of-dicts structure
            
        Returns:
            Parsed list of dictionaries or None if parsing fails or doesn't contain dicts
        """
        if not isinstance(value, str):
            return None
            
        value = value.strip()
        if not (value.startswith('[') and value.endswith(']')):
            return None
        
        # Strategy 1: Try standard JSON parsing first
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list) and len(parsed) > 0:
                # Check if all elements are dicts
                if all(isinstance(item, dict) for item in parsed):
                    logger.debug(f"✅ LIST-OF-DICTS PARSE: Standard JSON succeeded")
                    return parsed
        except (json.JSONDecodeError, TypeError):
            pass
        
        # Strategy 2: Try fixing common JSON issues and parse again
        try:
            fixed_value = self._preprocess_malformed_json(value)
            parsed = json.loads(fixed_value)
            if isinstance(parsed, list) and len(parsed) > 0:
                if all(isinstance(item, dict) for item in parsed):
                    logger.debug(f"✅ LIST-OF-DICTS PARSE: Fixed JSON succeeded: {value[:50]}...")
                    return parsed
        except (json.JSONDecodeError, TypeError):
            pass
        
        # Strategy 3: Try ast.literal_eval for Python list literals (SAFE - no code execution)
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list) and len(parsed) > 0:
                if all(isinstance(item, dict) for item in parsed):
                    logger.debug(f"✅ LIST-OF-DICTS PARSE: Python list literal succeeded: {value[:50]}...")
                    return parsed
        except (ValueError, SyntaxError):
            pass
        
        # Strategy 4: Try more aggressive preprocessing + ast.literal_eval
        try:
            preprocessed = self._aggressive_dict_preprocessing(value)
            parsed = ast.literal_eval(preprocessed)
            if isinstance(parsed, list) and len(parsed) > 0:
                if all(isinstance(item, dict) for item in parsed):
                    logger.debug(f"✅ LIST-OF-DICTS PARSE: Aggressive preprocessing succeeded: {value[:50]}...")
                    return parsed
        except (ValueError, SyntaxError):
            pass
        
        logger.debug(f"❌ LIST-OF-DICTS PARSE: All parsing strategies failed for: {value[:50]}...")
        return None
    
    def _preprocess_malformed_json(self, value: str) -> str:
        """
        Fix common JSON formatting issues.
        """
        # Replace single quotes with double quotes, but be careful about embedded quotes
        # This is a simple approach - could be made more sophisticated
        
        # Method 1: Simple replacement (works for many cases)
        fixed = value.replace("'", '"')
        
        # Method 2: Try to quote unquoted keys  
        # Pattern to find unquoted keys: {word: or ,word:
        fixed = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', fixed)
        
        return fixed
    
    def _aggressive_dict_preprocessing(self, value: str) -> str:
        """
        More aggressive preprocessing for badly formatted dict-like strings.
        """
        # Remove any extra whitespace
        cleaned = re.sub(r'\s+', ' ', value.strip())
        
        # Quote unquoted keys more aggressively
        # Handle patterns like: {key: 'value'} -> {'key': 'value'}
        cleaned = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r"\1'\2':", cleaned)
        
        # Handle mixed quotes by standardizing to single quotes for Python literals
        # This is tricky, but we'll try a simple approach
        
        return cleaned

    def _count_total_columns_from_nested_analysis(self, analysis: Dict) -> int:
        """
        Count the total number of columns that would be created from a nested analysis.
        
        Args:
            analysis: Result from _analyze_json_keys
            
        Returns:
            Total number of columns including all nested expansions
        """
        if not analysis:
            return 0
            
        total_columns = len(analysis.get('keys_to_expand', []))
        
        # Add nested columns recursively
        for key_info in analysis.get('keys_to_expand', []):
            nested_analysis = key_info.get('nested_analysis')
            if nested_analysis:
                total_columns += self._count_total_columns_from_nested_analysis(nested_analysis)
        
        return total_columns

    def _analyze_json_keys(self, json_objects: List[Dict], depth: int = 0, parent_path: str = "") -> Dict[str, Any]:
        """
        Analyze the keys in JSON objects to determine which ones to expand.
        Now with nested JSON support and NO MORE VARIABLE KEY BULLSHIT!
        
        Args:
            json_objects: List of parsed JSON dictionaries
            depth: Current nesting depth (for recursive analysis)
            parent_path: Path prefix for nested keys
            
        Returns:
            Analysis results with keys to expand
        """
        try:
            prefix = "  " * depth  # Indentation for nested logging
            logger.info(f"{prefix}🔍 KEY ANALYSIS: Analyzing {len(json_objects)} JSON objects at depth {depth}")
            if parent_path:
                logger.info(f"{prefix}   Parent path: {parent_path}")
            
            # Collect all keys and their frequency + values
            key_frequency = defaultdict(int)
            key_examples = defaultdict(set)
            key_nested_values = defaultdict(list)  # Store actual values for nested analysis
            
            # Log first few objects to see what we're working with
            for i, obj in enumerate(json_objects[:3]):
                logger.info(f"{prefix}   Sample object {i+1}: {obj}")
            
            # Check for empty dictionaries
            empty_dicts = sum(1 for obj in json_objects if len(obj) == 0)
            if empty_dicts > 0:
                logger.warning(f"{prefix}   ⚠️  Found {empty_dicts}/{len(json_objects)} empty dictionaries")
            
            for obj in json_objects:
                logger.debug(f"{prefix}   Processing object with {len(obj)} keys: {list(obj.keys())}")
                for key, value in obj.items():
                    key_frequency[key] += 1
                    
                    # Store example values
                    max_examples = self.json_config['max_example_values']
                    max_length = self.json_config['example_value_max_length']
                    if len(key_examples[key]) < max_examples:
                        key_examples[key].add(str(value)[:max_length])
                    
                    # Store actual values for potential nested analysis
                    key_nested_values[key].append(value)
            
            total_objects = len(json_objects)
            threshold = self.json_config['stable_key_threshold']
            max_depth = self.json_config['max_nesting_depth']
            
            logger.info(f"{prefix}🔍 KEY ANALYSIS: Found {len(key_frequency)} unique keys across {total_objects} objects")
            logger.info(f"{prefix}   Using {threshold:.0%} threshold for key expansion")
            
            # Log all keys with their frequencies  
            keys_to_expand = []
            keys_skipped = []
            
            for key, frequency in sorted(key_frequency.items(), key=lambda x: x[1], reverse=True):
                frequency_ratio = frequency / total_objects
                logger.info(f"{prefix}   Key '{key}': appears {frequency}/{total_objects} times ({frequency_ratio:.1%})")
                logger.info(f"{prefix}      Example values: {list(key_examples[key])[:3]}")
                
                if frequency_ratio >= threshold:
                    # Check if this key's values are nested JSON objects
                    nested_json_analysis = None
                    convert_to_list = False
                    
                    if depth < max_depth:
                        nested_objects = []
                        for value in key_nested_values[key]:
                            if isinstance(value, str):
                                nested_dict = self._safe_parse_dict_like(value)
                                if nested_dict is not None:
                                    nested_objects.append(nested_dict)
                            elif isinstance(value, dict):
                                nested_objects.append(value)
                        
                        # If we found nested JSON objects, analyze them too
                        if len(nested_objects) >= self.json_config['min_objects_for_analysis']:
                            nested_path = f"{parent_path}.dict.{key}" if parent_path else key
                            logger.info(f"{prefix}   🔍 Found {len(nested_objects)} nested JSON objects in key '{key}' - analyzing recursively")
                            nested_json_analysis = self._analyze_json_keys(nested_objects, depth + 1, nested_path)
                            
                            # Check if the nested expansion would create too many columns
                            max_columns_per_nested = self.json_config['max_columns_per_nested_object']
                            use_list_format = self.json_config['nested_list_format']
                            
                            if use_list_format and nested_json_analysis:
                                total_nested_columns = self._count_total_columns_from_nested_analysis(nested_json_analysis)
                                if total_nested_columns > max_columns_per_nested:
                                    logger.warning(f"{prefix}   🚨 COLUMN EXPLOSION DETECTED: Key '{key}' would create {total_nested_columns} columns (> {max_columns_per_nested} limit)")
                                    logger.warning(f"{prefix}   🔄 Converting to list format: key=value pairs instead of individual columns")
                                    convert_to_list = True
                                    nested_json_analysis = None  # Don't expand nested - convert to list instead
                    
                    keys_to_expand.append({
                        'key': key,
                        'frequency': frequency,
                        'frequency_ratio': frequency_ratio,
                        'example_values': list(key_examples[key]),
                        'nested_analysis': nested_json_analysis,  # Include nested analysis if present
                        'convert_to_list': convert_to_list  # NEW: Flag for list conversion
                    })
                    logger.info(f"{prefix}   ✅ EXPAND KEY: '{key}' ({frequency_ratio:.1%} frequency)")
                else:
                    keys_skipped.append({
                        'key': key,
                        'frequency': frequency,
                        'frequency_ratio': frequency_ratio,
                        'example_values': list(key_examples[key])
                    })
                    logger.info(f"{prefix}   ⏭️  SKIP KEY: '{key}' ({frequency_ratio:.1%} frequency - below {threshold:.0%} threshold)")
            
            logger.info(f"{prefix}🔍 KEY ANALYSIS SUMMARY:")
            logger.info(f"{prefix}   Keys to expand (≥{threshold:.0%} frequency): {len(keys_to_expand)}")
            logger.info(f"{prefix}   Keys skipped (<{threshold:.0%} frequency): {len(keys_skipped)}")
            
            # Include nested keys in the count
            total_expanded_keys = len(keys_to_expand)
            for key_info in keys_to_expand:
                if key_info.get('nested_analysis'):
                    nested_keys = len(key_info['nested_analysis'].get('keys_to_expand', []))
                    total_expanded_keys += nested_keys
            
            if total_expanded_keys > len(keys_to_expand):
                logger.info(f"{prefix}   Total keys to expand (including nested): {total_expanded_keys}")
            
            return {
                'keys_to_expand': sorted(keys_to_expand, key=lambda x: x['frequency_ratio'], reverse=True),
                'keys_skipped': sorted(keys_skipped, key=lambda x: x['frequency_ratio'], reverse=True),
                'total_unique_keys': len(key_frequency),
                'avg_keys_per_object': sum(len(obj) for obj in json_objects) / len(json_objects),
                'depth': depth,
                'parent_path': parent_path
            }
        except Exception as e:
            logger.error(f"{prefix}❌ ERROR in _analyze_json_keys: {e}")
            logger.error(f"{prefix}   Traceback: {traceback.format_exc()}")
            # Return empty analysis if there's an error
            return {
                'keys_to_expand': [],
                'keys_skipped': [],
                'total_unique_keys': 0,
                'avg_keys_per_object': 0,
                'depth': depth,
                'parent_path': parent_path
            }

    def analyze_json_columns(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Analyze DataFrame columns to find JSON/dict data and analyze their key patterns.
        Now with frequency-based expansion (no more variable key bullshit!)
        """
        json_analysis = {}
        sample_size = self.json_config['sample_size']
        min_objects = self.json_config['min_objects_for_analysis']
        
        for col in df.columns:
            # CRITICAL: Skip ALL __featrix* columns - these are internal and must NEVER be expanded
            # - __featrix_meta_*: Metadata columns (should stay as-is, not be expanded)
            # - __featrix_train_predictor: Training filter column
            # - __featrix_*: Any other internal columns
            if col.startswith('__featrix'):
                logger.info(f"🔒 Skipping internal column (will not expand JSON): {col}")
                continue
                
            if df[col].dtype != 'object':  # Skip non-string columns
                continue
                
            # Get sample of non-null values
            non_null_values = df[col].dropna()
            if len(non_null_values) == 0:
                continue
                
            # Sample for JSON detection
            detection_sample = non_null_values.sample(min(sample_size, len(non_null_values)), random_state=42)
            
            # Try to parse as JSON
            json_objects = []
            parse_failures = 0
            found_dicts = False
            found_list_of_dicts = False
            
            for value in detection_sample:
                if not isinstance(value, str):
                    continue
                    
                value_stripped = value.strip()
                
                # Check for dictionaries
                if value_stripped.startswith('{') and value_stripped.endswith('}'):
                    parsed = self._safe_parse_dict_like(value)
                    if parsed is not None:
                        logger.debug(f"   ✅ PARSED DICT SUCCESSFULLY: {parsed}")
                        json_objects.append(parsed)
                        found_dicts = True
                        continue
                
                # Check for lists of dictionaries
                if value_stripped.startswith('[') and value_stripped.endswith(']'):
                    parsed_list = self._safe_parse_list_of_dicts(value)
                    if parsed_list is not None:
                        logger.debug(f"   ✅ PARSED LIST-OF-DICTS SUCCESSFULLY: {len(parsed_list)} dicts")
                        # Add all dicts from the list to json_objects for analysis
                        json_objects.extend(parsed_list)
                        found_list_of_dicts = True
                        continue
                
                # If we get here, parsing failed
                logger.debug(f"   ❌ PARSE FAILED: {value[:100]}...")
                parse_failures += 1
            
            # Track columns that contain JSON-parseable dicts or lists of dicts
            if found_dicts or found_list_of_dicts:
                column_info = {
                    'column': col,
                    'has_dicts': found_dicts,
                    'has_list_of_dicts': found_list_of_dicts
                }
                if col not in [c['column'] for c in self.json_parseable_columns]:
                    self.json_parseable_columns.append(column_info)
                    logger.info(f"📝 Tracked JSON-parseable column: {col} (dicts: {found_dicts}, list-of-dicts: {found_list_of_dicts})")
                    # Mark as JSON type in column overrides (use JsonCodec, don't expand)
                    if col not in self.column_overrides:
                        self.column_overrides[col] = 'json'
                        logger.info(f"🔧 Auto-marked '{col}' as JSON type (will use JsonCodec, not expand)")
            
            # If we found enough JSON objects, analyze them
            if len(json_objects) >= min_objects:
                logger.info(f"🔍 ANALYZING JSON COLUMN: {col}")
                logger.info(f"   Parsed {len(json_objects)} JSON objects, {parse_failures} parse failures")
                logger.info(f"   Total non-null values: {len(non_null_values)}")
                
                # Analyze the key patterns (now including nested analysis)
                key_analysis = self._analyze_json_keys(json_objects)
                
                # Store results
                json_analysis[col] = {
                    'key_analysis': key_analysis,
                    'total_objects': len(json_objects),
                    'sample_size': len(detection_sample),
                    'total_non_null': len(non_null_values),
                    'parse_failures': parse_failures
                }
                
                # Log summary
                keys_to_expand = key_analysis.get('keys_to_expand', [])
                keys_skipped = key_analysis.get('keys_skipped', [])
                
                logger.info(f"📋 JSON ANALYSIS SUMMARY for '{col}':")
                logger.info(f"   • Keys to expand: {len(keys_to_expand)}")
                logger.info(f"   • Keys skipped: {len(keys_skipped)}")
                
                # Include nested analysis summary
                total_nested_keys = 0
                for key_info in keys_to_expand:
                    if key_info.get('nested_analysis'):
                        nested_keys = len(key_info['nested_analysis'].get('keys_to_expand', []))
                        total_nested_keys += nested_keys
                
                if total_nested_keys > 0:
                    logger.info(f"   • Nested keys to expand: {total_nested_keys}")
        
        if not json_analysis:
            logger.info("No JSON columns detected")
        
        return json_analysis

    def _transform_inspection_counts_by_date(self, df: pd.DataFrame, added_columns_stats: List[Dict]) -> pd.DataFrame:
        """
        Hard-coded transformation for inspection_counts_by_date column.
        
        Transforms from:
            {"2022-06-04": {"17197": 1}, "2025-01-07": {"48449": 1}}
        
        To columns:
            inspection_counts_by_date_2022_17 = 1
            inspection_counts_by_date_2025_48 = 1
        """
        logger.info(f"🚚 Applying hard-coded transformation for inspection_counts_by_date column")
        
        col_name = 'inspection_counts_by_date'
        year_location_counts = {}  # Will store aggregated counts
        transformation_count = 0
        
        # Process each row
        for idx, value in df[col_name].items():
            if pd.isna(value) or value == '':
                continue
                
            try:
                # Parse the JSON/dict string
                if isinstance(value, str):
                    parsed_data = ast.literal_eval(value)
                elif isinstance(value, dict):
                    parsed_data = value
                elif isinstance(value, list):
                    # If it's a list, skip this row (not the expected format)
                    logger.debug(f"Skipping row {idx}: inspection_counts_by_date is a list, expected dict")
                    continue
                else:
                    continue
                
                # Ensure parsed_data is a dict before processing
                if not isinstance(parsed_data, dict):
                    logger.debug(f"Skipping row {idx}: parsed_data is {type(parsed_data)}, expected dict")
                    continue
                
                transformation_count += 1
                
                # Process each date and its location counts
                for date_str, locations in parsed_data.items():
                    if not isinstance(locations, dict):
                        continue
                        
                    year = date_str[:4]  # Extract YYYY from YYYY-MM-DD
                    
                    for location_code, count in locations.items():
                        if len(str(location_code)) >= 2:
                            location_prefix = str(location_code)[:2]  # First 2 digits
                            col_key = f"inspection_counts_by_date_{year}_{location_prefix}"
                            
                            # Initialize the column data if not exists
                            if col_key not in year_location_counts:
                                year_location_counts[col_key] = [0] * len(df)
                            
                            # Add the count to this row's total for this year-location
                            year_location_counts[col_key][idx] += int(count)
                
            except (ValueError, SyntaxError, TypeError) as e:
                logger.debug(f"Could not parse inspection_counts_by_date value at row {idx}: {e}")
                continue
        
        # Add the new columns to the dataframe
        new_columns = []
        for col_key, values in year_location_counts.items():
            # Convert 0s to None for cleaner data
            cleaned_values = [val if val > 0 else None for val in values]
            df[col_key] = cleaned_values
            new_columns.append(col_key)
            
            # Calculate stats for reporting
            non_null_count = sum(1 for v in cleaned_values if v is not None)
            population_pct = (non_null_count / len(df)) * 100 if len(df) > 0 else 0
            sample_values = [str(v) for v in cleaned_values if v is not None][:3]
            
            added_columns_stats.append({
                'column_name': col_key,
                'source_column': col_name,
                'total_rows': len(df),
                'populated_rows': non_null_count,
                'population_percentage': population_pct,
                'sample_values': sample_values
            })
        
        # Drop the original column
        df = df.drop(columns=[col_name])
        
        logger.info(f"✅ Transformed inspection_counts_by_date into {len(new_columns)} year-location columns")
        logger.info(f"   • Processed {transformation_count}/{len(df)} non-null rows")
        logger.info(f"   • Sample columns: {new_columns[:5]}{'...' if len(new_columns) > 5 else ''}")
        
        return df

    def _chi2_feature_selection(self, df: pd.DataFrame, target_column: str, p_threshold: float = 0.2) -> pd.DataFrame:
        """
        Hard-coded chi-squared feature selection against a target column.
        
        Tests association between each column and target_column using chi-squared test.
        Only keeps columns with p-value < p_threshold.
        
        Args:
            df: DataFrame to filter
            target_column: Column to test associations against (e.g., 'fuel_card')
            p_threshold: P-value threshold for keeping columns (default: 0.2)
        """
        from scipy.stats import chi2_contingency
        
        logger.info(f"🔬 Running chi-squared feature selection against '{target_column}' (p < {p_threshold})")
        logger.info(f"   • Input dataframe: {len(df)} rows × {len(df.columns)} columns")
        
        # Enable debug logging for detailed chi-squared output
        logger.setLevel(logging.DEBUG)
        
        # Skip if target column is missing or has no valid data
        if target_column not in df.columns:
            logger.warning(f"Target column '{target_column}' not found - skipping chi-squared selection")
            return df
            
        target_data = df[target_column].dropna()
        logger.info(f"   • Target column '{target_column}' has {len(target_data)} non-null values")
        if len(target_data) == 0:
            logger.warning(f"Target column '{target_column}' has no valid data - skipping chi-squared selection")
            return df
        
        columns_to_keep = [target_column]  # Always keep the target column
        columns_to_drop = []
        chi2_results = []
        
        initial_columns = len(df.columns)
        
        for col in df.columns:
            if col == target_column:
                continue
                
            logger.debug(f"   🔍 Testing column: {col}")
            try:
                # KILL THE NULLS: Get non-null data for both columns
                mask = df[col].notna() & df[target_column].notna()
                col_data = df.loc[mask, col]
                target_subset = df.loc[mask, target_column]
                
                logger.debug(f"     📊 {col}: {len(col_data)} non-null pairs (from {len(df)} total rows)")
                
                if len(col_data) < 5:  # Reduced threshold since we're filtering nulls
                    columns_to_drop.append(col)
                    chi2_results.append({'column': col, 'p_value': 1.0, 'reason': 'insufficient_data'})
                    logger.debug(f"     ❌ {col}: insufficient data ({len(col_data)} non-null pairs)")
                    continue
                
                # BUCKET THE SCALARS: Convert continuous variables to categorical if needed
                unique_vals = col_data.nunique()
                logger.debug(f"     📈 {col}: {unique_vals} unique values")
                
                if pd.api.types.is_numeric_dtype(col_data):
                    # For numeric data, create bins if it has many unique values
                    if unique_vals > 5:  # Bin if more than 5 unique values
                        # Create bins for continuous data
                        try:
                            # Use quantile-based binning for better distribution
                            col_data_binned = pd.qcut(col_data, q=5, duplicates='drop', precision=2)
                            col_data = col_data_binned.astype(str)
                            logger.debug(f"     🪣 {col}: binned into quantiles -> {col_data.nunique()} bins")
                        except Exception as e:
                            # Fallback to equal-width bins
                            try:
                                col_data_binned = pd.cut(col_data, bins=5, duplicates='drop')
                                col_data = col_data_binned.astype(str)
                                logger.debug(f"     🪣 {col}: binned into equal-width -> {col_data.nunique()} bins")
                            except Exception:
                                # If all binning fails, skip this column
                                columns_to_drop.append(col)
                                chi2_results.append({'column': col, 'p_value': 1.0, 'reason': 'binning_failed'})
                                logger.debug(f"     ❌ {col}: binning failed completely")
                                continue
                    else:
                        # Convert to string for categorical treatment
                        col_data = col_data.astype(str)
                        logger.debug(f"     📝 {col}: treated as categorical ({unique_vals} categories)")
                else:
                    # Already categorical, convert to string
                    col_data = col_data.astype(str)
                    logger.debug(f"     📝 {col}: already categorical ({unique_vals} categories)")
                
                # Convert target to string for categorical treatment
                target_subset = target_subset.astype(str)
                
                # Create contingency table
                contingency_table = pd.crosstab(col_data, target_subset)
                logger.debug(f"     🔢 {col}: contingency table {contingency_table.shape} -> min={contingency_table.min().min()}")
                
                # KILL THE ZEROS: Remove zero rows and columns
                original_shape = contingency_table.shape
                contingency_table = contingency_table.loc[(contingency_table != 0).any(axis=1), (contingency_table != 0).any(axis=0)]
                
                logger.debug(f"     🗑️ {col}: after killing zeros {original_shape} -> {contingency_table.shape}")
                
                # Check if contingency table is still valid after killing zeros
                if contingency_table.size == 0 or contingency_table.shape[0] < 2 or contingency_table.shape[1] < 2:
                    columns_to_drop.append(col)
                    chi2_results.append({'column': col, 'p_value': 1.0, 'reason': 'no_variation_after_zero_removal'})
                    logger.debug(f"     ❌ {col}: no variation after removing zeros")
                    continue
                
                # Choose test based on table size and expected frequencies
                table_size = contingency_table.shape[0] * contingency_table.shape[1]
                
                # For small tables or low expected frequencies, use Fisher's exact test
                if table_size <= 4:  # 2x2 tables
                    try:
                        from scipy.stats import fisher_exact
                        if contingency_table.shape == (2, 2):
                            # Fisher's exact test for 2x2 tables
                            odds_ratio, p_value = fisher_exact(contingency_table)
                            test_used = "fisher_exact"
                            chi2_stat = None
                            dof = 1
                            expected = None
                            low_expected = False
                            logger.debug(f"     🎣 {col}: Fisher's exact test p={p_value:.6f}")
                        else:
                            # Fall back to chi-squared for non-2x2 small tables
                            chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)
                            test_used = "chi2_small"
                            low_expected = (expected < 5).any()
                            logger.debug(f"     📊 {col}: Chi-squared (small table) p={p_value:.6f}")
                    except ImportError:
                        # If Fisher's exact test not available, use chi-squared
                        chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)
                        test_used = "chi2_fallback"
                        low_expected = (expected < 5).any()
                        logger.debug(f"     📊 {col}: Chi-squared (Fisher's unavailable) p={p_value:.6f}")
                else:
                    # Perform chi-squared test for larger tables
                    chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)
                    test_used = "chi2"
                    # Check if expected frequencies are sufficient (rule of thumb: all >= 5)
                    low_expected = (expected < 5).any()
                    if low_expected:
                        logger.debug(f"     ⚠️ {col}: Chi-squared with low expected frequencies p={p_value:.6f}")
                    else:
                        logger.debug(f"     📊 {col}: Chi-squared p={p_value:.6f}")
                
                chi2_results.append({
                    'column': col, 
                    'p_value': p_value, 
                    'chi2_stat': chi2_stat,
                    'dof': dof,
                    'test_used': test_used,
                    'low_expected': low_expected,
                    'reason': 'tested'
                })
                
                # Keep column if p-value is below threshold
                if p_value < p_threshold:
                    columns_to_keep.append(col)
                    logger.debug(f"     ✅ {col}: KEPT (p={p_value:.6f} < {p_threshold}) [{test_used}]{' [low expected]' if low_expected else ''}")
                else:
                    columns_to_drop.append(col)
                    logger.debug(f"     ❌ {col}: dropped (p={p_value:.6f} >= {p_threshold}) [{test_used}]{' [low expected]' if low_expected else ''}")
                    
            except Exception as e:
                logger.debug(f"Chi-squared test failed for column '{col}': {e}")
                columns_to_drop.append(col)
                chi2_results.append({'column': col, 'p_value': 1.0, 'reason': f'error: {str(e)[:50]}'})
        
        # Filter the dataframe
        df_filtered = df[columns_to_keep].copy()
        
        # Log results
        kept_count = len(columns_to_keep) - 1  # Subtract 1 for target column
        dropped_count = len(columns_to_drop)
        
        logger.info(f"✅ Chi-squared feature selection complete:")
        logger.info(f"   • Initial columns: {initial_columns}")
        logger.info(f"   • Columns kept: {kept_count} (+ target)")
        logger.info(f"   • Columns dropped: {dropped_count}")
        logger.info(f"   • Retention rate: {kept_count/max(initial_columns-1, 1)*100:.1f}%")
        
        # Log ALL columns with p-values sorted from biggest to smallest
        tested_results = [r for r in chi2_results if r['reason'] == 'tested']
        logger.info(f"   • Total chi2_results: {len(chi2_results)}")
        logger.info(f"   • Results with reason='tested': {len(tested_results)}")
        if tested_results:
            # Sort by p-value (biggest to smallest as requested)
            sorted_results = sorted(tested_results, key=lambda x: x['p_value'], reverse=True)
            
            logger.info(f"   • ALL TESTED COLUMNS WITH P-VALUES (biggest to smallest):")
            for i, result in enumerate(sorted_results):
                test_info = f"[{result.get('test_used', 'unknown')}]"
                low_exp_info = " [low exp]" if result.get('low_expected', False) else ""
                logger.info(f"     {i+1:3d}. {result['column']:<50} (p={result['p_value']:.6f}) {test_info}{low_exp_info}")
            
            # Show p-value distribution summary
            p_values = [r['p_value'] for r in tested_results]
            logger.info(f"   • P-value distribution: min={min(p_values):.6f}, "
                       f"median={np.median(p_values):.6f}, max={max(p_values):.6f}")
            logger.info(f"   • Columns with p < 0.1: {sum(1 for p in p_values if p < 0.1)}")
            logger.info(f"   • Columns with p < 0.2: {sum(1 for p in p_values if p < 0.2)}")
            logger.info(f"   • Columns with p < 0.5: {sum(1 for p in p_values if p < 0.5)}")
            logger.info(f"   • Total tested columns: {len(tested_results)}")
        
        # Log sample of dropped columns
        if dropped_count > 0:
            sample_dropped = columns_to_drop[:5]
            logger.info(f"   • Sample dropped columns: {sample_dropped}{'...' if dropped_count > 5 else ''}")
        
        # Log reasons for dropping columns
        reason_counts = {}
        for result in chi2_results:
            reason = result['reason']
            if reason not in reason_counts:
                reason_counts[reason] = 0
            reason_counts[reason] += 1
        
        logger.info(f"   • Drop reasons: {reason_counts}")
        
        # Log test types used for successfully tested columns
        test_counts = {}
        for result in chi2_results:
            if result['reason'] == 'tested':
                test_type = result.get('test_used', 'unknown')
                if test_type not in test_counts:
                    test_counts[test_type] = 0
                test_counts[test_type] += 1
        
        if test_counts:
            logger.info(f"   • Statistical tests used: {test_counts}")
        
        # Also show if we have no tested results
        if not tested_results:
            logger.info(f"   • ⚠️  NO COLUMNS WERE TESTED - all columns failed preliminary checks")
            logger.info(f"   • This means no p-values were calculated")
        
        return df_filtered

    def _detect_and_report_column_types(self, df: pd.DataFrame) -> None:
        """
        Re-detect column types after JSON expansion and print a summary table.
        """
        from featrix.neural.detect import DetectorList
        
        logger.info(f"🔍 Re-detecting column types after JSON expansion...")
        logger.info(f"   • Analyzing {len(df.columns)} columns in {len(df)} rows")
        
        # Analyze each column
        column_info = []
        auto_detected_overrides = {}  # NEW: Store auto-detected encoders for JSON-expanded columns
        
        for col_name in df.columns:
            col_data = df[col_name]
            
            # Calculate basic stats
            total_rows = len(col_data)
            non_null_count = col_data.notna().sum()
            non_null_pct = (non_null_count / total_rows) * 100 if total_rows > 0 else 0
            unique_count = col_data.nunique()
            unique_pct = (unique_count / non_null_count) * 100 if non_null_count > 0 else 0
            
            # Run detection
            best_detector = None
            best_confidence = 0
            best_type = "unknown"
            
            for detector_class in DetectorList:
                try:
                    detector = detector_class(
                        colSample=col_data,
                        debugColName=col_name,
                        numUniques=unique_count,
                        numNotNulls=non_null_count,
                    )
                    
                    confidence = detector.confidence()
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_detector = detector
                        best_type = detector.get_type_name()
                        
                except Exception as e:
                    # Skip detectors that fail
                    continue
                        
            # Store column info for reporting
            column_info.append({
                'column': col_name,
                'type': best_type,
                'confidence': best_confidence,
                'non_null_pct': non_null_pct,
                'unique_pct': unique_pct,
                'unique_count': unique_count,
                'non_null_count': non_null_count,
                'total_rows': total_rows
            })
        
        # NEW: Add auto-detected overrides to the main column_overrides
        if auto_detected_overrides:
            logger.info(f"🔧 Adding {len(auto_detected_overrides)} auto-detected encoders to column overrides:")
            for col_name, encoder_type in auto_detected_overrides.items():
                self.column_overrides[col_name] = encoder_type
                logger.info(f"   • {col_name} → {encoder_type}")
        
        # Sort by confidence for better readability
        column_info.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Print summary table
        logger.info(f"\n📊 COLUMN TYPE DETECTION RESULTS:")
        logger.info(f"{'Column':<40} {'Type':<15} {'Confidence':<12} {'Population':<12} {'Uniqueness'}")
        logger.info(f"{'-' * 40} {'-' * 15} {'-' * 12} {'-' * 12} {'-' * 10}")
        
        for info in column_info:
            col_name = info['column']
            display_name = col_name if len(col_name) <= 39 else col_name[:36] + "..."
            
            type_name = info['type']
            confidence = info['confidence']
            non_null_pct = info['non_null_pct']
            unique_pct = info['unique_pct']
            
            # Color-code confidence levels
            conf_str = f"{confidence:.2f}"
            if confidence >= 0.8:
                conf_indicator = "🟢"  # High confidence
            elif confidence >= 0.5:
                conf_indicator = "🟡"  # Medium confidence
            elif confidence > 0:
                conf_indicator = "🔴"  # Low confidence
            else:
                conf_indicator = "❌"  # No detection
            
            logger.info(f"{display_name:<40} {type_name:<15} {conf_indicator} {conf_str:<9} {non_null_pct:>5.1f}% {non_null_pct:>4.0f}/{info['total_rows']:<4} {unique_pct:>5.1f}%")
        
        # Summary statistics
        high_confidence = sum(1 for info in column_info if info['confidence'] >= 0.8)
        medium_confidence = sum(1 for info in column_info if 0.5 <= info['confidence'] < 0.8)
        low_confidence = sum(1 for info in column_info if 0 < info['confidence'] < 0.5)
        no_detection = sum(1 for info in column_info if info['confidence'] == 0)
        
        logger.info(f"\n📈 DETECTION SUMMARY:")
        logger.info(f"   🟢 High confidence (≥0.8): {high_confidence}/{len(column_info)} columns")
        logger.info(f"   🟡 Medium confidence (0.5-0.8): {medium_confidence}/{len(column_info)} columns")
        logger.info(f"   🔴 Low confidence (<0.5): {low_confidence}/{len(column_info)} columns")
        logger.info(f"   ❌ No detection: {no_detection}/{len(column_info)} columns")
        
        if auto_detected_overrides:
            logger.info(f"   🔧 Auto-added encoders: {len(auto_detected_overrides)} JSON-expanded columns")

    def _expand_json_columns(self, df: pd.DataFrame, json_analysis: Dict[str, Dict]) -> pd.DataFrame:
        """
        Expand JSON columns into separate columns.
        Now supports nested JSON expansion up to configurable depth!
        """
        df_expanded = df.copy()
        
        # Track all transformations for metadata storage
        transformations = {}
        
        # Track all added columns and their population stats
        added_columns_stats = []
        
        # 🚚 HARD-CODED TRANSFORMATION: inspection_counts_by_date
        if 'inspection_counts_by_date' in df_expanded.columns:
            df_expanded = self._transform_inspection_counts_by_date(df_expanded, added_columns_stats)
            
            # Remove this column from JSON analysis since we handled it specially
            if 'inspection_counts_by_date' in json_analysis:
                del json_analysis['inspection_counts_by_date']
        
        for col_name, analysis in json_analysis.items():
            keys_to_expand = analysis.get('key_analysis', {}).get('keys_to_expand', [])
            keys_skipped = analysis.get('key_analysis', {}).get('keys_skipped', [])
            
            logger.info(f"🔍 Processing JSON column: {col_name}")
            logger.info(f"   • {len(keys_to_expand)} keys to expand (≥10% frequency)")
            logger.info(f"   • {len(keys_skipped)} keys skipped (<10% frequency)")
            
            # Log skipped keys for transparency
            if keys_skipped:
                skipped_names = [k['key'] for k in keys_skipped]
                logger.info(f"⏭️  Skipped keys in '{col_name}': {skipped_names}")
            
            # Store transformation metadata
            transformation_info = {
                'original_column': col_name,
                'keys_to_expand': [k['key'] for k in keys_to_expand],
                'keys_skipped': [k['key'] for k in keys_skipped],
                'expanded_columns': [],  # Will populate below
                'transformation_type': 'json_dict_expansion'
            }
            
            # DISABLED: Don't expand JSON keys - use JsonCodec instead
            # Mark column as JSON type so it uses JsonCodec
            if col_name not in self.column_overrides:
                self.column_overrides[col_name] = 'json'
                logger.info(f"🔧 Marked '{col_name}' as JSON type (will use JsonCodec, expansion disabled)")
            
            # Skip expansion - return empty list
            expanded_columns = []
            if keys_to_expand:
                # OLD CODE: expanded_columns = self._expand_keys_recursively(df_expanded, col_name, keys_to_expand, transformation_info)
                
                # No expanded columns to process - using JsonCodec instead
                logger.info(f"✅ Column '{col_name}' will use JsonCodec (no expansion)")
                
                # Keep original JSON column - we'll use JsonCodec to encode it
                # Don't drop it - JsonCodec needs the original JSON string
                
                # Store transformation metadata
                transformations[col_name] = transformation_info
            
            else:
                logger.info(f"ℹ️  Column '{col_name}' contains JSON but no keys meet the frequency threshold")
        
        # Store transformations for later retrieval
        self.json_transformations = transformations
        
        # Store column stats for reporting
        self.added_columns_stats = added_columns_stats
        
        # 🔍 RE-DETECT COLUMN TYPES: Analyze all columns after JSON expansion
        if len(df_expanded.columns) > 1:  # More than just target column
            self._detect_and_report_column_types(df_expanded)
        
        # 📅 AGGREGATE DATE COLUMNS: Collapse YYYY-MM-DD to YYYY with sums
        if added_columns_stats:
            df_expanded = self._aggregate_date_columns(df_expanded)
        
        # 🔬 CHI-SQUARED FEATURE SELECTION: Filter columns based on association with fuel_card
        # TEMPORARILY DISABLED TO DEBUG ROW LOSS ISSUE
        # if 'fuel_card' in df_expanded.columns:
        #     logger.info(f"🔬 About to run chi-squared selection on {len(df_expanded.columns)} columns")
        #     df_expanded = self._chi2_feature_selection(df_expanded, target_column='fuel_card', p_threshold=0.5)
        #     logger.info(f"🔬 After chi-squared selection: {len(df_expanded.columns)} columns remain")
        
        # 🛡️ DATA QUALITY & FEATURE SCALING: Prevent numerical instability
        # TODO: Implement proper data quality checks if needed
        # df_expanded = self._apply_data_quality_checks(df_expanded)
        
        # Report on added columns
        if added_columns_stats:
            self._report_added_columns(added_columns_stats)
        
        return df_expanded
    
    def _convert_nested_dict_to_list(self, nested_dict: Dict, prefix: str = "") -> List[str]:
        """
        Convert a nested dictionary to a list of key=value strings.
        
        Args:
            nested_dict: The nested dictionary to convert
            prefix: Prefix for nested keys (e.g., "2025." for year-based nesting)
            
        Returns:
            List of "key=value" strings
        """
        key_value_pairs = []
        
        for key, value in nested_dict.items():
            full_key = f"{prefix}{key}" if prefix else key
            
            if isinstance(value, dict):
                # Recursively handle nested dicts
                nested_pairs = self._convert_nested_dict_to_list(value, f"{full_key}.")
                key_value_pairs.extend(nested_pairs)
            elif isinstance(value, (list, tuple)):
                # Convert lists to comma-separated strings
                list_str = ",".join(str(item) for item in value)
                key_value_pairs.append(f"{full_key}={list_str}")
            elif value is not None:
                # Convert primitive values
                key_value_pairs.append(f"{full_key}={value}")
        
        return key_value_pairs

    # def _expand_keys_recursively(self, df: pd.DataFrame, base_col_name: str, keys_to_expand: List[Dict], 
    #                             transformation_info: Dict, parent_path: str = "") -> List[str]:
    #     """
    #     Recursively expand JSON keys, including nested JSON objects.
        
    #     Returns:
    #         List of all expanded column names
    #     """
    #     # DISABLED: JSON dict expansion - return empty list to prevent column blowout
    #     logger.info(f"🚫 JSON dict expansion DISABLED for '{base_col_name}' (would have expanded {len(keys_to_expand)} keys)")
    #     return []
        
    #     expanded_columns = []
        
    #     for key_info in keys_to_expand:
    #         key = key_info['key']
    #         frequency_ratio = key_info['frequency_ratio']
    #         nested_analysis = key_info.get('nested_analysis')
    #         convert_to_list = key_info.get('convert_to_list', False)
            
    #         # Create column name for this level
    #         if parent_path:
    #             new_col_name = f"{parent_path}.dict.{key}"
    #         else:
    #             new_col_name = f"{base_col_name}.dict.{key}"
            
    #         if convert_to_list:
    #             # Convert nested object to list format instead of expanding columns
    #             logger.info(f"   • {new_col_name}.list (converting nested dict to key=value list format)")
    #             list_col_name = f"{new_col_name}.list"
                
    #             # Extract and convert nested values to list format
    #             list_values = []
    #             for idx, value in df[base_col_name].items():
    #                 if pd.isna(value):
    #                     list_values.append(None)
    #                     continue
                        
    #                 # Parse the main JSON object
    #                 parsed = self._safe_parse_dict_like(value)
    #                 if parsed is not None:
    #                     nested_value = parsed.get(key, None)
                        
    #                     if nested_value is None:
    #                         list_values.append(None)
    #                     elif isinstance(nested_value, dict):
    #                         # Convert nested dict to key=value list
    #                         key_value_pairs = self._convert_nested_dict_to_list(nested_value)
    #                         # Join with | delimiter for set-like processing
    #                         list_values.append("|".join(key_value_pairs) if key_value_pairs else None)
    #                     elif isinstance(nested_value, str):
    #                         # Try to parse as nested JSON
    #                         nested_dict = self._safe_parse_dict_like(nested_value)
    #                         if nested_dict is not None:
    #                             key_value_pairs = self._convert_nested_dict_to_list(nested_dict)
    #                             list_values.append("|".join(key_value_pairs) if key_value_pairs else None)
    #                         else:
    #                             list_values.append(str(nested_value))
    #                     else:
    #                         list_values.append(str(nested_value))
    #                 else:
    #                     list_values.append(None)
                
    #             # Add the list column
    #             df[list_col_name] = list_values
    #             expanded_columns.append(list_col_name)
    #             transformation_info['expanded_columns'].append(list_col_name)
                
    #             # Update transformation info to indicate list conversion
    #             transformation_info['transformation_type'] = 'json_dict_to_list_expansion'
                
    #             logger.info(f"     Converted to list format to avoid {self._count_total_columns_from_nested_analysis({'keys_to_expand': [key_info]})} column explosion")
                
    #         else:
    #             # Normal column expansion
    #             logger.info(f"   • {new_col_name} (appears in {frequency_ratio:.1%} of objects)")
                
    #             # Extract values for this key
    #             extracted_values = []
    #             for idx, value in df[base_col_name].items():
    #                 if pd.isna(value):
    #                     extracted_values.append(None)
    #                     continue
                        
    #                 # Use fuzzy parsing to handle various dict-like formats
    #                 parsed = self._safe_parse_dict_like(value)
    #                 if parsed is not None:
    #                     extracted_value = parsed.get(key, None)
                        
    #                     # CRITICAL FIX: Always convert to SQLite-compatible types
    #                     if extracted_value is None:
    #                         extracted_values.append(None)
    #                     elif isinstance(extracted_value, (dict, list)):
    #                         # Convert complex objects to JSON strings for SQLite compatibility
    #                         # If we have nested analysis, we'll parse these strings again later
    #                         try:
    #                             extracted_values.append(json.dumps(extracted_value))
    #                         except (TypeError, ValueError):
    #                             # If JSON serialization fails, convert to string
    #                             extracted_values.append(str(extracted_value))
    #                     elif isinstance(extracted_value, (str, int, float, bool)):
    #                         # Keep primitive types as-is
    #                         extracted_values.append(extracted_value)
    #                     else:
    #                         # Convert anything else to string
    #                         extracted_values.append(str(extracted_value))
    #                 else:
    #                     extracted_values.append(None)
                
    #             # Add the new column
    #             df[new_col_name] = extracted_values
    #             expanded_columns.append(new_col_name)
                
    #             # Track this expanded column
    #             transformation_info['expanded_columns'].append(new_col_name)
                
    #             # If this key has nested JSON analysis, expand those too
    #             if nested_analysis and nested_analysis.get('keys_to_expand'):
    #                 logger.info(f"   🔍 Expanding nested keys for {new_col_name}...")
                    
    #                 nested_keys = nested_analysis['keys_to_expand']
    #                 nested_expanded = self._expand_keys_recursively(
    #                     df, new_col_name, nested_keys, transformation_info, new_col_name
    #                 )
    #                 expanded_columns.extend(nested_expanded)
                    
    #                 # Drop the intermediate JSON column after expanding its nested keys
    #                 if nested_expanded:  # Only drop if we actually expanded something
    #                     df.drop(columns=[new_col_name], inplace=True)
    #                     expanded_columns.remove(new_col_name)  # Remove from list since we dropped it
    #                     transformation_info['expanded_columns'].remove(new_col_name)
    #                     logger.info(f"   Dropped intermediate column '{new_col_name}' after nested expansion")
        
    #     return expanded_columns

    def _aggregate_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate date-based columns from YYYY-MM-DD format to YYYY format.
        Sums numeric values for each year group.
        """
        logger.info("📅 AGGREGATING DATE COLUMNS: Collapsing YYYY-MM-DD to YYYY...")
        
        # Find columns with YYYY-MM-DD patterns - handle both with and without suffixes
        date_columns = {}  # {base_pattern: [matching_columns]}
        
        # Pattern 1: columns ending with date (e.g., "inspection_counts_by_date.dict.2025-01-06")
        date_pattern_1 = re.compile(r'(.+\.dict\.)(\d{4}-\d{2}-\d{2})$')
        
        # Pattern 2: columns with content after date (e.g., "col.dict.2025-01-06.dict.something")
        date_pattern_2 = re.compile(r'(.+\.dict\.)(\d{4}-\d{2}-\d{2})(\.dict\..+)')
        
        for col in df.columns:
            match = date_pattern_1.match(col) or date_pattern_2.match(col)
            if match:
                groups = match.groups()
                prefix = groups[0]
                date_str = groups[1]
                suffix = groups[2] if len(groups) > 2 else ""
                
                year = date_str[:4]  # Extract YYYY
                base_pattern = f"{prefix}YEAR{suffix}" if suffix else f"{prefix}YEAR"
                
                if base_pattern not in date_columns:
                    date_columns[base_pattern] = {}
                if year not in date_columns[base_pattern]:
                    date_columns[base_pattern][year] = []
                    
                date_columns[base_pattern][year].append(col)
        
        if not date_columns:
            logger.info("   No date columns found to aggregate")
            return df
        
        logger.info(f"   Found {len(date_columns)} date column patterns to aggregate")
        
        aggregated_columns = []
        columns_to_drop = []
        
        # Aggregate each pattern
        for base_pattern, year_groups in date_columns.items():
            for year, columns in year_groups.items():
                # Create new aggregated column name
                new_col_name = base_pattern.replace('YEAR', year)
                
                if len(columns) == 1:
                    # Single column - just rename it to year format
                    logger.info(f"   📅 Renaming single column to {new_col_name}")
                    df[new_col_name] = df[columns[0]]
                    aggregated_columns.append(new_col_name)
                    columns_to_drop.extend(columns)
                    
                    # Log stats
                    non_null_count = df[new_col_name].notna().sum()
                    logger.info(f"      ✅ {new_col_name}: {non_null_count}/{len(df)} populated ({non_null_count/len(df)*100:.1f}%)")
                    
                else:
                    # Multiple columns - aggregate by summing
                    logger.info(f"   📅 Aggregating {len(columns)} columns into {new_col_name}")
                    logger.debug(f"      Columns: {columns[:3]}{'...' if len(columns) > 3 else ''}")
                    
                    # Sum numeric values across all date columns for this year
                    aggregated_values = []
                    for idx in df.index:
                        total = 0
                        has_data = False
                        
                        for col in columns:
                            value = df.loc[idx, col]
                            if pd.notna(value) and value != '':
                                try:
                                    numeric_val = float(value)
                                    total += numeric_val
                                    has_data = True
                                except (ValueError, TypeError):
                                    # Non-numeric value, skip
                                    pass
                        
                        aggregated_values.append(total if has_data else None)
                    
                    # Add the new aggregated column
                    df[new_col_name] = aggregated_values
                    aggregated_columns.append(new_col_name)
                    
                    # Mark original columns for removal
                    columns_to_drop.extend(columns)
                    
                    # Log aggregation stats
                    non_null_count = pd.Series(aggregated_values).notna().sum()
                    logger.info(f"      ✅ {new_col_name}: {non_null_count}/{len(df)} populated ({non_null_count/len(df)*100:.1f}%)")
        
        # Remove original date columns
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)
            logger.info(f"   🗑️  Dropped {len(columns_to_drop)} original date columns")
        
        logger.info(f"📅 DATE AGGREGATION COMPLETE: Added {len(aggregated_columns)} year-based columns")
        
        return df

    def _report_added_columns(self, stats: List[Dict]):
        """Report on the columns that were added during JSON expansion"""
        if not stats:
            return
            
        logger.info(f"\n📊 JSON EXPANSION SUMMARY REPORT:")
        logger.info(f"   Added {len(stats)} new columns from JSON expansion")
        logger.info(f"   {'Column Name':<50} {'Population':<12} {'Sample Values'}")
        logger.info(f"   {'-' * 50} {'-' * 12} {'-' * 30}")
        
        # Sort by population percentage (highest first)
        sorted_stats = sorted(stats, key=lambda x: x['population_percentage'], reverse=True)
        
        for stat in sorted_stats:
            col_name = stat['column_name']
            pop_pct = stat['population_percentage']
            pop_count = stat['populated_rows']
            total = stat['total_rows']
            sample_vals = stat['sample_values']
            
            # Truncate column name if too long
            display_name = col_name if len(col_name) <= 49 else col_name[:46] + "..."
            
            # Format sample values
            sample_str = str(sample_vals[:2]).replace("'", '"') if sample_vals else "[]"
            if len(sample_str) > 28:
                sample_str = sample_str[:25] + "..."
                
            logger.info(f"   {display_name:<50} {pop_count:>4}/{total:<4} ({pop_pct:>5.1f}%) {sample_str}")
        
        # Summary statistics
        avg_population = sum(s['population_percentage'] for s in stats) / len(stats)
        fully_populated = sum(1 for s in stats if s['population_percentage'] >= 95.0)
        sparsely_populated = sum(1 for s in stats if s['population_percentage'] < 25.0)
        
        logger.info(f"\n📈 POPULATION STATISTICS:")
        logger.info(f"   Average population: {avg_population:.1f}%")
        logger.info(f"   Well populated (≥95%): {fully_populated}/{len(stats)} columns")
        logger.info(f"   Sparsely populated (<25%): {sparsely_populated}/{len(stats)} columns")

    def csv_to_sqlite(self, csv_path: str, table_name: str = "data"):
        # Check if file is JSONL or JSON format
        csv_path_obj = Path(csv_path)
        abs_path = csv_path_obj.resolve()
        file_extension = csv_path_obj.suffix.lower()
        logger.info(f"📄 Processing input file:")
        logger.info(f"   Raw path: {csv_path}")
        logger.info(f"   Absolute path: {abs_path}")
        logger.info(f"   File extension: {file_extension}")
        logger.info(f"   File exists: {csv_path_obj.exists()}")
        if csv_path_obj.exists():
            file_size = csv_path_obj.stat().st_size
            logger.info(f"   File size: {file_size / 1024 / 1024:.2f} MB ({file_size:,} bytes)")
        else:
            logger.error(f"   ❌ File does not exist at: {abs_path}")
        
        if file_extension in ['.jsonl', '.json']:
            # Trust the extension - parse as JSON/JSONL only
            if file_extension == '.jsonl':
                logger.info(f"📋 Detected JSONL file - parsing as JSON Lines (one JSON object per line)...")
            else:
                logger.info(f"📋 Detected JSON file - parsing as JSON...")
            
            read_start_time = time.time()
            try:
                df = featrix_wrap_read_json_file(csv_path)
                if df is None:
                    raise ValueError(f"JSON parsing returned None for {csv_path}")
            except Exception as e:
                logger.error(f"❌ Failed to parse {file_extension} file: {e}")
                raise ValueError(f"Failed to parse {file_extension} file {csv_path}: {e}")
            
            read_elapsed = time.time() - read_start_time
            logger.info(f"✅ JSON/JSONL file parsed in {read_elapsed:.1f} seconds")
        elif file_extension == '.parquet':
            # Parquet file
            logger.info(f"📦 Detected Parquet file - reading with pandas...")
            read_start_time = time.time()
            try:
                df = pd.read_parquet(csv_path)
            except Exception as e:
                logger.error(f"❌ Failed to read Parquet file: {e}")
                raise ValueError(f"Failed to parse Parquet file {csv_path}: {e}")
            read_elapsed = time.time() - read_start_time
            logger.info(f"✅ Parquet file read in {read_elapsed:.1f} seconds")
        elif file_extension in ['.csv', '.gz']:
            # Regular CSV file (or gzipped CSV) - trust the extension, no JSON parsing
            logger.info(f"📄 Detected CSV file - reading with pandas...")
            read_start_time = time.time()
            try:
                df = featrix_wrap_pd_read_csv(csv_path)
            except Exception as e:
                logger.error(f"❌ Failed to read CSV file: {e}")
                raise ValueError(f"Failed to parse CSV file {csv_path}: {e}")
            read_elapsed = time.time() - read_start_time
            logger.info(f"✅ CSV file read in {read_elapsed:.1f} seconds")
        else:
            # Unknown file extension - fail
            raise ValueError(f"Unsupported file extension '{file_extension}' for file {csv_path}. Supported formats: .csv, .gz, .parquet, .json, .jsonl")
        
        logger.info(f"🧹 Cleaning column names and string values...")
        df.columns = df.columns.str.strip()  # Strips spaces around column names
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)  # Strips spaces in string values
        logger.info(f"✅ Data cleaning complete")
        
        initial_column_count = df.shape[1]
        logger.info(f"📊 Initial data shape: {df.shape[0]} rows × {initial_column_count} columns")
        
        # Log columns found after CSV reading for debugging
        logger.info(f"📋 Columns found in CSV ({len(df.columns)} total): {list(df.columns)[:50]}{'...' if len(df.columns) > 50 else ''}")
        if len(df.columns) > 50:
            logger.info(f"   ... and {len(df.columns) - 50} more columns")
        
        # 🔍 JSON DETECTION AND EXPANSION
        logger.info("🔍 Analyzing columns for JSON content...")
        json_analysis = self.analyze_json_columns(df)
        
        if json_analysis:
            logger.info(f"📋 Found {len(json_analysis)} columns containing JSON data")
            
            # Expand JSON columns with keys that meet frequency threshold
            df = self._expand_json_columns(df, json_analysis)
            
            new_column_count = df.shape[1]
            added_columns = new_column_count - initial_column_count
            logger.info(f"📊 After JSON expansion: {df.shape[0]} rows × {new_column_count} columns")
            logger.info(f"   Added {added_columns} new columns from JSON expansion")
        else:
            logger.info("ℹ️  No JSON columns detected in dataset")
        
        # df = pd.read_csv(csv_path)
        
        # 🛡️ DEFENSIVE CHECK: Convert any remaining dict/list objects to JSON strings for SQLite compatibility
        logger.info("🛡️ Performing final SQLite compatibility check...")
        for col in df.columns:
            # Check if any values in this column are dict/list objects
            dict_count = 0
            for idx, value in df[col].items():
                if isinstance(value, (dict, list)):
                    try:
                        df.at[idx, col] = json.dumps(value)
                        dict_count += 1
                    except (TypeError, ValueError):
                        df.at[idx, col] = str(value)
                        dict_count += 1
            
            if dict_count > 0:
                logger.warning(f"🔧 Converted {dict_count} dict/list objects to strings in column '{col}'")
        
        logger.info("✅ SQLite compatibility check complete")
        
        logger.info(f"💾 Writing data to SQLite table '{table_name}'...")
        sqlite_start_time = time.time()
        
        # Ensure we have a fresh connection before writing
        # Close existing connection if it exists
        try:
            if self.conn:
                self.conn.close()
        except Exception:
            pass
        
        # Create a fresh connection to ensure it's valid
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        try:
            # CRITICAL: Rename existing table instead of dropping it for safety
            # This preserves the old data as a backup in case something goes wrong
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            table_exists = self.cursor.fetchone() is not None
            
            if table_exists:
                # Generate backup table name with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_table_name = f"{table_name}_backup_{timestamp}"
                
                logger.info(f"💾 Renaming existing table '{table_name}' to '{backup_table_name}' for safety...")
                self.cursor.execute(f"ALTER TABLE {table_name} RENAME TO {backup_table_name}")
                self.conn.commit()
                logger.info(f"✅ Table '{table_name}' renamed to '{backup_table_name}'")
                
                # Clean up old backup tables (keep only the 3 most recent)
                # This prevents the database from growing indefinitely with backup tables
                self.cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name LIKE ?
                    ORDER BY name DESC
                """, (f"{table_name}_backup_%",))
                backup_tables = [row[0] for row in self.cursor.fetchall()]
                
                if len(backup_tables) > 3:
                    # Drop the oldest backups, keeping only the 3 most recent
                    tables_to_drop = backup_tables[3:]  # Skip first 3 (most recent)
                    for old_backup in tables_to_drop:
                        logger.info(f"🗑️  Cleaning up old backup table '{old_backup}' (keeping 3 most recent)")
                        self.cursor.execute(f"DROP TABLE IF EXISTS {old_backup}")
                    self.conn.commit()
                    logger.info(f"✅ Cleaned up {len(tables_to_drop)} old backup tables")
            else:
                logger.info(f"ℹ️  Table '{table_name}' does not exist - will create new table")
            
            # Verify table doesn't exist before creating (safety check)
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            table_still_exists = self.cursor.fetchone() is not None
            
            if table_still_exists:
                logger.warning(f"⚠️  Table '{table_name}' still exists after rename attempt - using 'replace' mode as fallback")
                # Use 'replace' as fallback - this will drop and recreate, but we tried to preserve it
                if_exists_mode = 'replace'
            else:
                # Table doesn't exist (either never existed or was successfully renamed)
                if_exists_mode = 'fail'  # Will create new table, fail if somehow exists
            
            # Log DataFrame columns for debugging
            logger.info(f"📋 DataFrame columns ({len(df.columns)}): {list(df.columns)[:20]}{'...' if len(df.columns) > 20 else ''}")
            
            # Now create the table fresh with the current DataFrame schema
            df.to_sql(table_name, self.conn, if_exists=if_exists_mode, index=False)
            self.conn.commit()
            
            # Verify the table was created and has data
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = self.cursor.fetchone()[0]
            if row_count == 0:
                raise ValueError(f"Table '{table_name}' was created but contains 0 rows. DataFrame had {len(df)} rows.")
            
            # Verify the database file is not empty
            db_file = Path(self.db_path)
            if db_file.exists():
                db_size = db_file.stat().st_size
                if db_size == 0:
                    raise ValueError(f"Database file {self.db_path} is 0 bytes after write operation")
                logger.info(f"   Database file size: {db_size / 1024 / 1024:.2f} MB")
            
            sqlite_elapsed = time.time() - sqlite_start_time
            logger.info(f"✅ Data written to SQLite in {sqlite_elapsed:.1f} seconds ({row_count:,} rows)")
        except Exception as e:
            sqlite_elapsed = time.time() - sqlite_start_time
            logger.error(f"❌ FAILED to write data to SQLite after {sqlite_elapsed:.1f} seconds")
            logger.error(f"   Error type: {type(e).__name__}")
            logger.error(f"   Error message: {str(e)}")
            logger.error(f"   DataFrame shape: {df.shape}")
            logger.error(f"   DataFrame columns ({len(df.columns)}): {list(df.columns)}")
            logger.error(f"   Database path: {self.db_path}")
            
            # Check what columns exist in the table (if it exists)
            try:
                self.cursor.execute(f"PRAGMA table_info({table_name})")
                existing_columns = [row[1] for row in self.cursor.fetchall()]
                if existing_columns:
                    logger.error(f"   Existing table columns: {existing_columns}")
                else:
                    logger.error(f"   Table '{table_name}' does not exist or has no columns")
            except Exception as pragma_error:
                logger.error(f"   Could not check existing table schema: {pragma_error}")
            # Check disk space
            try:
                import shutil
                stat = shutil.disk_usage(Path(self.db_path).parent)
                free_gb = stat.free / (1024**3)
                logger.error(f"   Disk space: {free_gb:.2f} GB free")
            except Exception:
                pass
            # Close connection on error
            try:
                if self.conn:
                    self.conn.close()
            except Exception:
                pass
            # Re-raise so the job fails properly
            raise

        # OK now that we have the data
        # 1. create validation set / training set
        # 2. detect columns
        # 3. pre-run string_cache on unique values

        # Verify database file exists and is not empty before reading
        db_file = Path(self.db_path)
        if not db_file.exists():
            raise FileNotFoundError(f"Database file {self.db_path} does not exist after write operation")
        
        db_size = db_file.stat().st_size
        if db_size == 0:
            raise ValueError(f"Database file {self.db_path} is 0 bytes - write operation may have failed")
        
        logger.info(f"📂 Loading data from SQLite for string cache creation...")
        logger.info(f"   Database file size: {db_size / 1024 / 1024:.2f} MB")
        
        # Verify table exists before trying to read
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not self.cursor.fetchone():
            raise ValueError(f"Table '{table_name}' does not exist in database {self.db_path}")
        
        input_data_file = FeatrixInputDataFile(self.db_path)
        df = input_data_file.df
        logger.info(f"✅ Loaded {len(df)} rows from SQLite")
        
        # Build string cache with FULL dataset to avoid cache misses in downstream jobs
        logger.info(f"🔧 Creating FeatrixInputDataSet for string cache...")
        logger.info(f"   Rows: {len(df)}")
        logger.info(f"   Columns: {len(df.columns)}")
        logger.info(f"   Column overrides: {len(self.column_overrides) if self.column_overrides else 0} columns")
        
        dataset_start_time = time.time()
        full_data_set = FeatrixInputDataSet(
            df=df,
            ignore_cols=[],                         
            limit_rows=None,                        # Use full dataset for comprehensive string cache
            encoder_overrides=self.column_overrides,  # Use column overrides from job spec
            project_row_meta_data=None,
        )
        dataset_elapsed = time.time() - dataset_start_time
        logger.info(f"✅ FeatrixInputDataSet created in {dataset_elapsed:.1f} seconds")

        # Create string caches with ALL strings in the dataset
        # CRITICAL: We MUST build the string cache here, even in Celery workers
        # Celery workers CAN load the sentence model - they're not PyTorch DataLoader workers
        # Only PyTorch DataLoader workers (PYTORCH_DATALOADER_WORKER=1) should skip model loading
        is_pytorch_dataloader_worker = os.environ.get('PYTORCH_DATALOADER_WORKER') == '1'
        
        if is_pytorch_dataloader_worker:
            logger.warning(f"⚠️  Skipping string cache creation in PyTorch DataLoader worker (cannot load sentence model)")
            logger.warning(f"   String cache should already be pre-populated by main process")
            # Create empty cache file so get_output_files() doesn't fail
            cache_path = Path("strings.sqlite3")
            if not cache_path.exists():
                cache_path.touch()
        else:
            logger.info(f"🔥 Building comprehensive string cache from {len(df)} rows...")
            logger.info(f"🔍 STRUCTUREDDATA DEBUG: current working directory = {os.getcwd()}")
            logger.info(f"🔍 STRUCTUREDDATA DEBUG: cache will be created at: {os.path.abspath('strings.sqlite3')}")
            
            cache_start_time = time.time()
            full_data_set.create_string_caches("strings.sqlite3")
            cache_elapsed = time.time() - cache_start_time
            logger.info(f"✅ String cache creation completed in {cache_elapsed:.1f} seconds")

        # Verify the cache was actually created
        cache_path = Path("strings.sqlite3")
        if cache_path.exists():
            cache_size = cache_path.stat().st_size
            logger.info(f"✅ STRUCTUREDDATA DEBUG: Cache file created successfully")
            logger.info(f"   Path: {cache_path.resolve()}")
            logger.info(f"   Size: {cache_size / 1024:.1f} KB")
        else:
            # This is expected if there are no string columns in the data
            logger.info(f"ℹ️  STRUCTUREDDATA DEBUG: Cache file was NOT created (no string columns in data)")
            logger.debug(f"   Expected path: {cache_path.resolve() if cache_path.is_absolute() else 'relative to cwd'}")

    def get_output_files(self):
        # Make sure we return the absolute path for the cache
        # Use absolute path construction to avoid getcwd() failures
        try:
            cwd = os.getcwd()
            cache_path = Path(cwd) / "strings.sqlite3"
        except FileNotFoundError:
            # Current working directory doesn't exist - use the db_path's directory as fallback
            logger.warning(f"⚠️  Current working directory doesn't exist, using db_path directory as fallback")
            cache_path = Path(self.db_path).parent / "strings.sqlite3"
        
        # CRITICAL: Ensure path is absolute and resolve any symlinks
        cache_path = cache_path.resolve()
        logger.info(f"🔍 STRUCTUREDDATA DEBUG: get_output_files() returning cache path: {cache_path}")
        logger.info(f"   Absolute path: {cache_path}")
        logger.info(f"   File exists: {cache_path.exists()}")
        
        return dict(
            sqlite_db=self.db_path, 
            strings_cache=str(cache_path),  # Return absolute resolved path
            json_transformations=self.json_transformations,  # Include transformation metadata
            added_columns_stats=getattr(self, 'added_columns_stats', []),  # Include column population stats
            json_parseable_columns=getattr(self, 'json_parseable_columns', [])  # Include JSON-parseable columns tracking
        )
    
    def close(self):
        self.conn.close()