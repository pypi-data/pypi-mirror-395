#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
"""
Adaptive string column analysis for intelligent encoding strategy selection.

This module analyzes string columns to detect:
1. Random/meaningless strings (UUIDs, IDs, hashes) → EXCLUDE
2. Sequential/monotonic IDs → CONVERT TO NUMERIC
3. Cyclic patterns → KEEP AS STRING
4. Delimiters → PREPROCESS
5. Information density → ADAPTIVE ARCHITECTURE
"""

import logging
import math
import re
from collections import Counter
from typing import Dict, List, Any

import numpy as np
import torch

logger = logging.getLogger(__name__)

# Common delimiters to detect in multi-valued fields
# Note: '-' and '_' are NOT included because they're too common in natural language
# (e.g., "quick-brown", "user_name"). Delimiter detection has heuristics to be conservative.
DELIMITERS = [',', ';', '|', '/', '::', '//', ' / ', ' | ', '\t']

# Pattern matching for common ID formats
ID_PATTERNS = {
    "uuid": r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    "hex_hash": r'^[0-9a-f]{32,64}$',
    "prefixed_hex": r'^[A-Z]+[_-][0-9a-f]{8,}$',
    "sequential_id": r'^(ORD|TXN|SESS|ID|USER)[_-]?\d{4,}',
}

# Seed null values - we'll compute embeddings and use semantic similarity
NULL_SEED_STRINGS = [
    # Standard programming nulls
    'none', 'null', 'nil', 'n/a', 'na', 'nan',
    # Punctuation nulls
    '-', '--', '_', '...', 
    # Natural language nulls
    'nothing', 'empty', 'blank', 'unknown', 'missing',
    'not available', 'not applicable',
    'no data', 'no value',
    # Fun nulls
    'nada', 'zilch', 'void',
]

# Global cache for null embeddings (computed once)
_null_embeddings = None
_null_similarity_threshold = 0.85  # If similarity > 0.85, treat as null


def get_null_embeddings(sentence_model):
    """
    Get or compute embeddings for null seed strings.
    Uses global cache to avoid recomputing.
    """
    global _null_embeddings
    
    if _null_embeddings is not None:
        return _null_embeddings
    
    if sentence_model is None:
        return None
    
    logger.info(f"📦 Computing embeddings for {len(NULL_SEED_STRINGS)} null seed strings...")
    
    try:
        embeddings = sentence_model.encode(
            NULL_SEED_STRINGS,
            convert_to_tensor=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        # CRITICAL: Detach tensor for multiprocessing compatibility
        # Without this, DataLoader workers can't pickle the tensor across process boundaries
        _null_embeddings = embeddings.detach()
        logger.info(f"✅ Null embeddings cached (detached for multiprocessing)")
        return _null_embeddings
    except Exception as e:
        logger.warning(f"⚠️ Failed to compute null embeddings: {e}")
        return None


def is_null_natural_language(value: str, value_embedding=None, sentence_model=None) -> bool:
    """
    Check if a string is semantically similar to null values.
    Uses BERT embeddings and cosine similarity instead of hardcoded list.
    
    This catches:
    - Typos: "nonne", "nul"
    - Variants: "not specified", "no answer", "skip"
    - Different languages: "ninguno", "aucun"
    - Domain-specific: "TBD", "pending", "awaiting"
    
    Examples:
        "N/A" → True (exact match to seed)
        "n/aa" → True (typo, but similar embedding)
        "not specified" → True (semantic similarity)
        "Hello" → False (not similar to nulls)
    
    Args:
        value: String to check
        value_embedding: Pre-computed BERT embedding (optional, for efficiency)
        sentence_model: BERT model (optional, needed if value_embedding not provided)
    
    Returns:
        True if string is semantically null-like
    """
    if not isinstance(value, str):
        return False
    
    # Quick check: empty or whitespace
    if not value.strip():
        return True
    
    # Get null embeddings
    if sentence_model is None:
        # Fallback to simple hardcoded check if no BERT model
        normalized = value.lower().strip()
        return normalized in {'none', 'null', 'nil', 'n/a', 'na', 'nan', '-', '_'}
    
    null_embeddings = get_null_embeddings(sentence_model)
    if null_embeddings is None:
        # Fallback if embedding failed
        normalized = value.lower().strip()
        return normalized in {'none', 'null', 'nil', 'n/a', 'na', 'nan', '-', '_'}
    
    # Get value embedding if not provided
    if value_embedding is None:
        try:
            value_embedding = sentence_model.encode(
                value,
                convert_to_tensor=True,
                normalize_embeddings=True,
                show_progress_bar=False
            )
            # Detach for multiprocessing compatibility
            value_embedding = value_embedding.detach()
        except Exception as e:
            logger.warning(f"⚠️ Failed to encode value for null check: {e}")
            return False
    
    # Compute cosine similarity to all null embeddings
    similarities = torch.nn.functional.cosine_similarity(
        value_embedding.unsqueeze(0),
        null_embeddings,
        dim=1
    )
    
    max_similarity = similarities.max().item()
    
    # If very similar to any null string, treat as null
    return max_similarity > _null_similarity_threshold


def precompute_string_properties(column_values, column_name, sentence_model=None):
    """
    Pre-compute ALL expensive operations ONCE per unique string.
    This is the performance bottleneck - do it once, use results everywhere.
    
    Args:
        column_values: Raw column values from dataframe
        column_name: Name of the column (for logging)
        sentence_model: BERT model for batch encoding (optional, will skip BERT if None)
    
    Returns:
        Dict with:
            - value_properties: {string_value: {props}} for dict lookups
            - column_stats: aggregated statistics
            - column_name: name of column
    """
    # Clean values
    values = [str(v) for v in column_values if v is not None and str(v) != 'nan']
    
    if len(values) == 0:
        logger.warning(f"Column '{column_name}' has no valid string values")
        return {
            "value_properties": {},
            "column_stats": {"total_count": 0, "unique_count": 0},
            "column_name": column_name,
        }
    
    value_counts = Counter(values)
    unique_strings = list(value_counts.keys())
    
    logger.info(f"🔄 Pre-computing properties for {len(unique_strings):,} unique strings in '{column_name}'...")
    
    # ============================================
    # PHASE 1: Per-string properties (fast operations)
    # ============================================
    value_properties = {}
    
    for s in unique_strings:
        # Basic properties
        length = len(s)
        
        # Extract ALL numeric parts at once
        numeric_matches = re.findall(r'\d+', s)
        numeric_parts = [int(m) for m in numeric_matches] if numeric_matches else []
        
        # Count delimiters (all at once)
        delimiter_counts = {delim: s.count(delim) for delim in DELIMITERS if delim in s}
        
        # Pattern matching (all patterns at once)
        pattern_matches = {
            name: bool(re.match(pattern, s.lower()))
            for name, pattern in ID_PATTERNS.items()
        }
        
        # Character distribution (for entropy calculation)
        s_lower = s.lower()
        # Remove common separators for char analysis
        s_clean = s_lower
        for sep in ['-', '_', ' ', '.', ',', ';', '|', '/']:
            s_clean = s_clean.replace(sep, '')
        
        char_counts = Counter(s_clean) if s_clean else {}
        
        value_properties[s] = {
            "length": length,
            "numeric_parts": numeric_parts,
            "max_numeric": max(numeric_parts) if numeric_parts else None,
            "delimiter_counts": delimiter_counts,
            "pattern_matches": pattern_matches,
            "char_counts": char_counts,
            "frequency": value_counts[s],
            "bert_embedding": None,
        }
    
    # ============================================
    # PHASE 2: Batch BERT encoding (MUCH FASTER than one-by-one)
    # ============================================
    if sentence_model is not None and len(unique_strings) > 0:
        logger.info(f"   📦 Batch encoding {len(unique_strings):,} unique strings with BERT...")
        
        try:
            # Batch encode - 100x faster than one-by-one!
            embeddings = sentence_model.encode(
                unique_strings,
                batch_size=64,  # GPU efficiency
                show_progress_bar=False,
                convert_to_tensor=True,
                normalize_embeddings=True
            )
            
            # Store embeddings (detached for multiprocessing compatibility)
            for s, emb in zip(unique_strings, embeddings):
                value_properties[s]["bert_embedding"] = emb.detach()
        except Exception as e:
            logger.warning(f"   ⚠️ Failed to batch encode strings: {e}")
    
    # ============================================
    # PHASE 3: Column-level aggregated stats
    # ============================================
    logger.info(f"   📊 Computing column-level statistics...")
    
    total_count = len(values)
    unique_count = len(unique_strings)
    unique_ratio = unique_count / total_count if total_count > 0 else 0
    
    # Shannon entropy
    probabilities = [count / total_count for count in value_counts.values()]
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    max_entropy = math.log2(unique_count) if unique_count > 1 else 1
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
    
    # Average length (weighted by frequency)
    avg_length = sum(value_properties[s]["length"] * value_properties[s]["frequency"] 
                     for s in unique_strings) / total_count
    
    # Most common delimiter (if any)
    all_delimiter_counts = Counter()
    for s in unique_strings:
        for delim, count in value_properties[s]["delimiter_counts"].items():
            all_delimiter_counts[delim] += count * value_properties[s]["frequency"]
    
    dominant_delimiter = all_delimiter_counts.most_common(1)[0] if all_delimiter_counts else None
    
    # Pattern prevalence (what % match each pattern)
    pattern_frequencies = {}
    for pattern_name in ID_PATTERNS.keys():
        matching_count = sum(
            value_properties[s]["frequency"] 
            for s in unique_strings 
            if value_properties[s]["pattern_matches"].get(pattern_name, False)
        )
        pattern_frequencies[pattern_name] = matching_count / total_count
    
    # Numeric analysis (for monotonic detection)
    numeric_sequence = []
    for v in values:  # Use original order
        props = value_properties[v]
        if props["max_numeric"] is not None:
            numeric_sequence.append(props["max_numeric"])
    
    is_monotonic_increasing = False
    is_monotonic_decreasing = False
    numeric_sequence_coverage = len(numeric_sequence) / total_count if total_count > 0 else 0
    
    if len(numeric_sequence) > 10 and numeric_sequence_coverage > 0.8:
        is_monotonic_increasing = all(
            numeric_sequence[i] <= numeric_sequence[i+1] 
            for i in range(len(numeric_sequence)-1)
        )
        is_monotonic_decreasing = all(
            numeric_sequence[i] >= numeric_sequence[i+1] 
            for i in range(len(numeric_sequence)-1)
        )
    
    # Semantic similarity (from BERT embeddings)
    avg_semantic_similarity = None
    if sentence_model is not None and len(unique_strings) >= 10:
        try:
            # Sample for efficiency
            sample_size = min(50, len(unique_strings))
            sample_indices = np.random.choice(len(unique_strings), sample_size, replace=False)
            sample_strings = [unique_strings[i] for i in sample_indices]
            sample_embeddings = [value_properties[s]["bert_embedding"] for s in sample_strings]
            
            # Filter out None embeddings
            sample_embeddings = [e for e in sample_embeddings if e is not None]
            
            if len(sample_embeddings) >= 10:
                # Compute pairwise similarities
                similarities = []
                for i in range(len(sample_embeddings)):
                    for j in range(i+1, min(i+10, len(sample_embeddings))):
                        sim = torch.nn.functional.cosine_similarity(
                            sample_embeddings[i].unsqueeze(0),
                            sample_embeddings[j].unsqueeze(0)
                        ).item()
                        similarities.append(sim)
                
                avg_semantic_similarity = np.mean(similarities) if similarities else None
        except Exception as e:
            logger.warning(f"   ⚠️ Failed to compute semantic similarity: {e}")
    
    column_stats = {
        "total_count": total_count,
        "unique_count": unique_count,
        "unique_ratio": unique_ratio,
        "entropy": entropy,
        "normalized_entropy": normalized_entropy,
        "avg_length": avg_length,
        "dominant_delimiter": dominant_delimiter,
        "pattern_frequencies": pattern_frequencies,
        "is_monotonic_increasing": is_monotonic_increasing,
        "is_monotonic_decreasing": is_monotonic_decreasing,
        "numeric_sequence_coverage": numeric_sequence_coverage,
        "avg_semantic_similarity": avg_semantic_similarity,
    }
    
    logger.info(f"   ✅ Pre-computation complete!")
    
    return {
        "value_properties": value_properties,
        "column_stats": column_stats,
        "column_name": column_name,
    }


def detect_monotonic_sequence(precomputed: Dict) -> Dict[str, Any]:
    """
    Detect if column contains monotonic sequence (sequential IDs, timestamps).
    If true, should convert to numeric temporal feature instead of string.
    
    Fast - just dict lookup from precomputed stats.
    """
    stats = precomputed["column_stats"]
    
    if stats["is_monotonic_increasing"]:
        return {
            "is_monotonic": True,
            "direction": "increasing",
            "reason": f"Monotonic increasing sequence detected ({stats['numeric_sequence_coverage']:.1%} coverage)",
            "recommendation": "CONVERT_TO_NUMERIC_TEMPORAL"
        }
    elif stats["is_monotonic_decreasing"]:
        return {
            "is_monotonic": True,
            "direction": "decreasing",
            "reason": f"Monotonic decreasing sequence detected ({stats['numeric_sequence_coverage']:.1%} coverage)",
            "recommendation": "CONVERT_TO_NUMERIC_TEMPORAL"
        }
    
    return {
        "is_monotonic": False,
        "recommendation": "KEEP_AS_STRING"
    }


def detect_random_strings(precomputed: Dict) -> Dict[str, Any]:
    """
    Detect if column contains random/meaningless strings (UUIDs, hashes, transaction IDs).
    These have high entropy but ZERO semantic meaning - should be EXCLUDED.
    
    Fast - just dict lookup from precomputed stats.
    """
    stats = precomputed["column_stats"]
    col_name = precomputed["column_name"]
    
    signals = []
    randomness_score = 0.0
    
    # SIGNAL 1: Very high unique ratio (almost every value is unique)
    if stats["unique_ratio"] > 0.95:
        signals.append(f"Very high unique ratio: {stats['unique_ratio']:.2%}")
        randomness_score += 0.3
    
    # SIGNAL 2: Low semantic similarity (random strings have uncorrelated embeddings)
    if stats["avg_semantic_similarity"] is not None:
        if stats["avg_semantic_similarity"] < 0.3:
            signals.append(f"Low semantic similarity: {stats['avg_semantic_similarity']:.3f}")
            randomness_score += 0.4
    
    # SIGNAL 3: Pattern matches (UUID, hash, etc.)
    for pattern_name, frequency in stats["pattern_frequencies"].items():
        if frequency > 0.8:
            signals.append(f"Matches {pattern_name} pattern: {frequency:.0%}")
            randomness_score += 0.5
            break
    
    # SIGNAL 4: Low repetition (most repeated value is < 1% of total)
    if len(precomputed["value_properties"]) > 0:
        max_freq = max(props["frequency"] for props in precomputed["value_properties"].values())
        repetition_ratio = max_freq / stats["total_count"]
        if repetition_ratio < 0.01:
            signals.append(f"Very low repetition: max {repetition_ratio:.2%}")
            randomness_score += 0.2
    
    # SIGNAL 5: Column name hints
    random_keywords = ['id', 'uuid', 'guid', 'hash', 'token', 'session', 'transaction', 'txn', 'key']
    col_lower = col_name.lower()
    if any(kw in col_lower for kw in random_keywords):
        # Only add score if other signals present (name alone isn't enough)
        if randomness_score > 0.3:
            signals.append(f"Column name suggests ID: '{col_name}'")
            randomness_score += 0.1
    
    is_random = randomness_score > 0.7
    
    return {
        "is_random": is_random,
        "confidence": randomness_score,
        "signals": signals,
        "recommendation": "EXCLUDE_ZERO_CONTRIBUTION" if is_random else "KEEP_AS_STRING"
    }


def detect_delimiter(precomputed: Dict) -> Dict[str, Any]:
    """
    Detect if column contains delimited multi-valued fields.
    These should be preprocessed: "a,b,c" → "a\nb\nc" before BERT encoding.
    
    Fast - just dict lookup from precomputed stats.
    """
    stats = precomputed["column_stats"]
    
    if stats["dominant_delimiter"]:
        delim, count = stats["dominant_delimiter"]
        frequency = count / stats["total_count"]
        
        # Need at least 30% of values to have delimiter
        if frequency > 0.3:
            return {
                "has_delimiter": True,
                "delimiter": delim,
                "frequency": frequency,
                "recommendation": "PREPROCESS_WITH_NEWLINES"
            }
    
    return {
        "has_delimiter": False,
        "recommendation": "NO_PREPROCESSING_NEEDED"
    }


def compute_info_density(precomputed: Dict) -> float:
    """
    Compute information density score (0-1) based on:
    - Entropy (how diverse are values)
    - Average length (how much content per value)
    - Unique ratio (how many distinct values)
    
    Fast - just dict lookup from precomputed stats.
    """
    stats = precomputed["column_stats"]
    
    entropy = stats["normalized_entropy"]
    avg_length = min(stats["avg_length"] / 100, 1.0)  # Normalize to 0-1
    unique_ratio = stats["unique_ratio"]
    
    # Weighted combination
    info_density = (entropy * 0.4) + (avg_length * 0.3) + (unique_ratio * 0.3)
    
    return info_density


def select_architecture_from_info_density(info_density: float, d_model: int) -> Dict[str, Any]:
    """
    Select encoding architecture based on information density.
    
    Low density (categories) → Aggressive compression
    Medium density (names) → Standard
    High density (descriptions) → Preserve/expand
    """
    # LOW INFORMATION DENSITY (< 0.3)
    # Categories, status fields, simple codes
    if info_density < 0.3:
        return {
            "d_out": d_model // 2,  # Aggressive compression
            "n_hidden_layers": 0,   # Simple linear
            "d_hidden": 256,
            "strategy": "LOW_INFO_AGGRESSIVE_COMPRESS",
            "reason": f"Low info density ({info_density:.2f}) - categorical-like data"
        }
    
    # MODERATE INFORMATION DENSITY (0.3 - 0.6)
    # Names, cities, product codes, short descriptions
    elif info_density < 0.6:
        return {
            "d_out": d_model,       # Standard: match d_model
            "n_hidden_layers": 1,
            "d_hidden": 384,        # Match BERT for feature interaction
            "strategy": "MODERATE_INFO_STANDARD",
            "reason": f"Moderate info density ({info_density:.2f}) - standard encoding"
        }
    
    # HIGH INFORMATION DENSITY (0.6 - 0.8)
    # Rich descriptions, reviews, emails
    elif info_density < 0.8:
        return {
            "d_out": d_model * 2,   # Expand: preserve BERT semantics
            "n_hidden_layers": 1,
            "d_hidden": 512,        # Wide for expressiveness
            "strategy": "HIGH_INFO_PRESERVE",
            "reason": f"High info density ({info_density:.2f}) - rich semantic content"
        }
    
    # VERY HIGH INFORMATION DENSITY (> 0.8)
    # Complex documents, long-form text, highly diverse content
    else:
        return {
            "d_out": d_model * 3,   # Maximum preservation
            "n_hidden_layers": 2,
            "d_hidden": 512,        # Deep + wide
            "strategy": "VERY_HIGH_INFO_MAXIMUM_PRESERVE",
            "reason": f"Very high info density ({info_density:.2f}) - maximum capacity needed"
        }


def preprocess_delimited_string(value: str, delimiter: str) -> str:
    """
    Convert delimited string to newline-separated for better BERT encoding.
    
    Example:
        "apple,banana,orange" → "apple\nbanana\norange"
    
    This makes BERT treat it as a list/multiple items instead of one long string.
    """
    if not isinstance(value, str):
        return str(value)
    
    # Split and clean
    parts = [part.strip() for part in value.split(delimiter)]
    
    # Remove empty parts
    parts = [p for p in parts if p]
    
    # Join with newlines
    return '\n'.join(parts)


def compute_string_features(value: str, column_freq_stats: Dict[str, Any] = None) -> torch.Tensor:
    """
    Compute 27 structured features from a string value.
    
    Features:
    - Structure/shape (16): is_delimited (1), delimiter_type (5), list_len (1), uniq_list_items (1),
                          length (1), token_count (1), char_entropy (1), shape_pattern (5)
    - Numeric-ish (4): can_parse_numeric, parsed_numeric_value, is_zeroish, is_small_nonzero
    - Missing/NA-ish (2): is_empty_whitespace, is_naish
    - Frequency/target-driven (2): frequency_encoding, rarity
    - Length (3): raw_length, trimmed_length, has_trimmed_value
    
    Args:
        value: String value to analyze
        column_freq_stats: Dict with 'value_counts' (Counter) and 'total_count' (int)
                          for frequency encoding. If None, frequency features are 0.
    
    Returns:
        torch.Tensor of shape [27] with all features normalized to [0, 1] or [-1, 1]
    """
    import math
    from collections import Counter
    
    if not isinstance(value, str):
        value = str(value)
    
    features = []
    
    # ============================================
    # STRUCTURE/SHAPE FEATURES (8 features)
    # ============================================
    
    # 1. is_delimited: bool (0/1)
    delimiters = [',', ';', '|', '/', '\t']
    is_delimited = 1.0 if any(d in value for d in delimiters) else 0.0
    features.append(is_delimited)
    
    # 2. delimiter_type: one-hot (comma=1, semicolon=2, pipe=3, slash=4, tab=5, none=0)
    delimiter_type = [0.0] * 5
    if ',' in value:
        delimiter_type[0] = 1.0  # comma
    elif ';' in value:
        delimiter_type[1] = 1.0  # semicolon
    elif '|' in value:
        delimiter_type[2] = 1.0  # pipe
    elif '/' in value:
        delimiter_type[3] = 1.0  # slash
    elif '\t' in value:
        delimiter_type[4] = 1.0  # tab
    features.extend(delimiter_type)
    
    # 3. list_len: normalized count of delimited items
    if is_delimited:
        # Find which delimiter was used
        delimiter = None
        for d in delimiters:
            if d in value:
                delimiter = d
                break
        if delimiter:
            parts = [p.strip() for p in value.split(delimiter) if p.strip()]
            list_len = min(len(parts) / 100.0, 1.0)  # Normalize to [0, 1], cap at 100 items
        else:
            list_len = 0.0
    else:
        list_len = 0.0
    features.append(list_len)
    
    # 4. uniq_list_items: ratio of unique items
    if is_delimited and delimiter:
        parts = [p.strip() for p in value.split(delimiter) if p.strip()]
        if len(parts) > 0:
            uniq_ratio = len(set(parts)) / len(parts)
        else:
            uniq_ratio = 0.0
    else:
        uniq_ratio = 0.0
    features.append(uniq_ratio)
    
    # 5. length: normalized string length
    length = min(len(value) / 1000.0, 1.0)  # Normalize to [0, 1], cap at 1000 chars
    features.append(length)
    
    # 6. token_count: normalized word count
    words = value.split()
    token_count = min(len(words) / 100.0, 1.0)  # Normalize to [0, 1], cap at 100 words
    features.append(token_count)
    
    # 7. char_entropy: character diversity (Shannon entropy)
    if len(value) > 0:
        char_counts = Counter(value)
        total_chars = len(value)
        entropy = 0.0
        for count in char_counts.values():
            p = count / total_chars
            if p > 0:
                entropy -= p * math.log2(p)
        # Normalize: max entropy for uniform distribution is log2(alphabet_size)
        # Assume max alphabet size of 100 for normalization
        char_entropy = min(entropy / 7.0, 1.0)  # log2(100) ≈ 6.64, normalize to [0, 1]
    else:
        char_entropy = 0.0
    features.append(char_entropy)
    
    # 8. shape_pattern: one-hot (LLL-DDD, LLLL, DDDD, MIXED, OTHER)
    # LLL = letters, DDD = digits, MIXED = both, OTHER = neither
    shape_pattern = [0.0] * 5
    if len(value) == 0:
        shape_pattern[4] = 1.0  # OTHER
    else:
        has_letters = any(c.isalpha() for c in value)
        has_digits = any(c.isdigit() for c in value)
        if has_letters and has_digits:
            # Check for common patterns like "LLL-DDD" or "DDDD-LLL"
            if '-' in value or '_' in value:
                shape_pattern[0] = 1.0  # LLL-DDD pattern
            else:
                shape_pattern[3] = 1.0  # MIXED
        elif has_letters:
            shape_pattern[1] = 1.0  # LLLL (letters only)
        elif has_digits:
            shape_pattern[2] = 1.0  # DDDD (digits only)
        else:
            shape_pattern[4] = 1.0  # OTHER (punctuation/symbols)
    features.extend(shape_pattern)
    
    # ============================================
    # NUMERIC-ISH FEATURES (4 features)
    # ============================================
    
    # 9. can_parse_numeric: bool (0/1)
    can_parse = 0.0
    parsed_value = 0.0
    try:
        # Try to parse as float
        parsed = float(value.replace(',', '').replace('$', '').replace('%', '').strip())
        can_parse = 1.0
        parsed_value = parsed
    except (ValueError, AttributeError):
        pass
    
    features.append(can_parse)
    
    # 10. parsed_numeric_value: normalized numeric value (if parseable)
    if can_parse:
        # Normalize to [-1, 1] using tanh
        normalized_value = math.tanh(parsed_value / 1000.0)  # Scale by 1000
    else:
        normalized_value = 0.0
    features.append(normalized_value)
    
    # 11. is_zeroish: bool (0/1) - close to zero
    if can_parse:
        is_zeroish = 1.0 if abs(parsed_value) < 0.001 else 0.0
    else:
        is_zeroish = 0.0
    features.append(is_zeroish)
    
    # 12. is_small_nonzero: bool (0/1) - small but not zero
    if can_parse and not is_zeroish:
        is_small_nonzero = 1.0 if 0.001 <= abs(parsed_value) < 10.0 else 0.0
    else:
        is_small_nonzero = 0.0
    features.append(is_small_nonzero)
    
    # ============================================
    # MISSING/NA-ISH FEATURES (2 features)
    # ============================================
    
    # 13. is_empty_whitespace: bool (0/1)
    is_empty = 1.0 if not value.strip() else 0.0
    features.append(is_empty)
    
    # 14. is_naish: bool (0/1) - semantic null detection
    # Use simple heuristic (full semantic check happens in tokenize)
    naish_keywords = ['none', 'null', 'nil', 'n/a', 'na', 'nan', '-', '_', 'empty', 'blank', 'missing']
    is_naish = 1.0 if value.lower().strip() in naish_keywords else 0.0
    features.append(is_naish)
    
    # ============================================
    # FREQUENCY/TARGET-DRIVEN FEATURES (2 features)
    # ============================================
    
    # 15. frequency_encoding: normalized frequency in column
    if column_freq_stats and 'value_counts' in column_freq_stats and 'total_count' in column_freq_stats:
        value_counts = column_freq_stats['value_counts']
        total_count = column_freq_stats['total_count']
        if total_count > 0 and value in value_counts:
            frequency = value_counts[value] / total_count
        else:
            frequency = 0.0
    else:
        frequency = 0.0
    features.append(frequency)
    
    # 16. rarity: is_common (0) vs is_rare (1)
    # Common = appears in top 10% of values, rare = appears in bottom 50%
    if column_freq_stats and 'value_counts' in column_freq_stats and 'total_count' in column_freq_stats:
        value_counts = column_freq_stats['value_counts']
        total_count = column_freq_stats['total_count']
        if total_count > 0 and value in value_counts:
            count = value_counts[value]
            # Compute percentile: how many values appear more frequently?
            more_frequent = sum(1 for v, c in value_counts.items() if c > count)
            percentile = more_frequent / len(value_counts) if len(value_counts) > 0 else 0.0
            # Rare = bottom 50%, common = top 10%
            if percentile > 0.5:
                rarity = 1.0  # Rare
            elif percentile < 0.1:
                rarity = 0.0  # Common
            else:
                rarity = 0.5  # Medium
        else:
            rarity = 1.0  # Not seen = rare
    else:
        rarity = 0.0  # Default to common if no stats
    features.append(rarity)
    
    # ============================================
    # LENGTH FEATURES (3 features)
    # ============================================
    
    # 17. raw_length: raw string length (normalized)
    raw_length = min(len(value) / 1000.0, 1.0)  # Normalize to [0, 1], cap at 1000 chars
    features.append(raw_length)
    
    # 18. trimmed_length: length after stripping whitespace (normalized)
    trimmed_value = value.strip()
    trimmed_length = min(len(trimmed_value) / 1000.0, 1.0)  # Normalize to [0, 1], cap at 1000 chars
    features.append(trimmed_length)
    
    # 19. has_trimmed_value: 1 if len(trim()) > 0, else 0
    has_trimmed_value = 1.0 if len(trimmed_value) > 0 else 0.0
    features.append(has_trimmed_value)
    
    # Convert to tensor
    feature_tensor = torch.tensor(features, dtype=torch.float32)
    
    # Ensure we have exactly 27 features (was 24, added 3 length features)
    assert len(features) == 27, f"Expected 27 features, got {len(features)}"
    
    return feature_tensor

