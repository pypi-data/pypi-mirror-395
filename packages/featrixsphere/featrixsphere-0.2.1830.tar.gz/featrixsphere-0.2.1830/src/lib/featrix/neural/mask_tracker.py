#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import json
import time
from collections import Counter
from pathlib import Path
import logging

import torch
import numpy as np

from .featrix_token import TokenStatus

logger = logging.getLogger(__name__)


class MaskDistributionTracker:
    """
    Tracks the distribution of mask patterns used during embedding space training.
    
    This tracker records every mask pattern used, verifies complementarity,
    and provides analysis of the mask distribution to ensure proper randomness.
    """
    
    def __init__(self, output_dir, save_full_sequence=False, column_names=None):
        """
        Initialize the mask tracker.
        
        Args:
            output_dir: Directory to save mask statistics
            save_full_sequence: If True, saves every single mask used (larger files)
            column_names: List of column names in order (maps positions to names)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.save_full_sequence = save_full_sequence
        self.column_names = column_names  # List like ['age', 'income', 'city', ...]
        
        # Counters for distribution analysis
        self.mask_a_counter = Counter()
        self.mask_b_counter = Counter()
        self.pair_counter = Counter()
        self.coverage_counter = Counter()  # (n_masked_a, n_masked_b) tuples
        
        # Per-column statistics - now using column NAMES not positions
        self.column_mask_a_count = Counter()  # How often each column NAME is masked in A
        self.column_mask_b_count = Counter()  # How often each column NAME is masked in B
        self.total_samples = 0
        
        # Optional: full sequence streaming
        self.sequence_file = None
        if save_full_sequence:
            self.sequence_file = open(self.output_dir / "mask_sequence.jsonl", 'w')
        
        self.start_time = time.time()
        self.last_save_time = self.start_time
        
        # Counter for mask size mismatch logging (log once, then every 1000)
        self._mask_mismatch_count = 0
        self._mask_mismatch_logged_once = False
        
        # Save column name mapping
        if self.column_names:
            mapping_file = self.output_dir / "column_mapping.json"
            with open(mapping_file, 'w') as f:
                json.dump({
                    'column_names': self.column_names,
                    'num_columns': len(self.column_names),
                    'mapping': {i: name for i, name in enumerate(self.column_names)}
                }, f, indent=2)
            logger.info(f"📋 Saved column mapping: {len(self.column_names)} columns")
        
    def masks_to_string(self, mask_a_row, mask_b_row, present_mask_row):
        """
        Convert BOTH mask tensor rows to a combined string that ALWAYS has the same length.
        
        Position i in the string ALWAYS corresponds to df.columns[i], so masks
        can be directly compared across rows/batches/epochs.
        
        Each position is encoded as 2 characters showing both masks, separated by dashes:
        - 'Ab' = mask_a MARGINAL (masked), mask_b OK (available)
        - 'aB' = mask_a OK (available), mask_b MARGINAL (masked)  
        - 'XX' = NOT_PRESENT in both (column doesn't exist)
        
        Due to complementarity, you should only see 'Ab', 'aB', or 'XX'.
        
        Args:
            mask_a_row: Single row from mask_a tensor
            mask_b_row: Single row from mask_b tensor
            present_mask_row: Single row from original status mask
            
        Returns:
            String like "Ab-aB-XX-Ab-aB" where pairs map to df columns (with dashes)
        """
        # Use minimum length to avoid index errors if masks have different sizes
        min_len = min(len(mask_a_row), len(mask_b_row), len(present_mask_row))
        
        # Silently handle size mismatches (can happen with variable batch column counts)
        # Only log at debug level if there's a significant mismatch
        if len(mask_a_row) != len(mask_b_row) or len(mask_a_row) != len(present_mask_row):
            import logging
            logger = logging.getLogger(__name__)
            # Only warn if mismatch is significant (more than 10% difference)
            max_len = max(len(mask_a_row), len(mask_b_row), len(present_mask_row))
            if min_len < max_len * 0.9:
                self._mask_mismatch_count += 1
                # Log once initially, then every 1000 occurrences
                if not self._mask_mismatch_logged_once:
                    logger.debug(
                        f"Mask size mismatch: mask_a={len(mask_a_row)}, mask_b={len(mask_b_row)}, "
                        f"present_mask={len(present_mask_row)}. Using min_len={min_len}"
                    )
                    self._mask_mismatch_logged_once = True
                elif self._mask_mismatch_count % 1000 == 0:
                    logger.debug(
                        f"Mask size mismatch (occurred {self._mask_mismatch_count} times): "
                        f"mask_a={len(mask_a_row)}, mask_b={len(mask_b_row)}, "
                        f"present_mask={len(present_mask_row)}. Using min_len={min_len}"
                    )
        
        result = []
        for i in range(min_len):
            if present_mask_row[i] == TokenStatus.NOT_PRESENT:
                result.append('XX')
            else:
                # Mask A: uppercase if MARGINAL, lowercase if OK
                a_char = 'A' if mask_a_row[i] == TokenStatus.MARGINAL else 'a'
                # Mask B: uppercase if MARGINAL, lowercase if OK
                b_char = 'B' if mask_b_row[i] == TokenStatus.MARGINAL else 'b'
                result.append(a_char + b_char)
        
        return '-'.join(result)  # Join with dashes for readability
    
    def record_batch(self, epoch, batch_idx, mask_a, mask_b, original_mask):
        """
        Record mask patterns for an entire batch.
        
        Args:
            epoch: Current epoch number
            batch_idx: Current batch index
            mask_a: First mask tensor (batch_size, n_cols)
            mask_b: Second mask tensor (batch_size, n_cols)
            original_mask: Original status mask (batch_size, n_cols)
        """
        # CRITICAL: Detach from computation graph and move to CPU to avoid triggering
        # DataLoader workers or keeping references that prevent garbage collection.
        # This prevents OOM kills when system RAM is low.
        if mask_a.is_cuda:
            mask_a = mask_a.detach().cpu()
        else:
            mask_a = mask_a.detach()
        
        if mask_b.is_cuda:
            mask_b = mask_b.detach().cpu()
        else:
            mask_b = mask_b.detach()
        
        if original_mask.is_cuda:
            original_mask = original_mask.detach().cpu()
        else:
            original_mask = original_mask.detach()
        
        # Convert to numpy to completely disconnect from PyTorch memory management
        # This ensures no references to DataLoader workers or computation graphs
        mask_a_np = mask_a.numpy()
        mask_b_np = mask_b.numpy()
        original_mask_np = original_mask.numpy()
        
        batch_size = mask_a_np.shape[0]
        
        for i in range(batch_size):
            # Convert to combined string (each position shows both masks)
            # Use numpy arrays to avoid any tensor operations that might trigger DataLoader workers
            combined_str = self.masks_to_string(mask_a_np[i], mask_b_np[i], original_mask_np[i])
            
            # Split by dashes to get individual pairs
            pairs = combined_str.split('-')
            
            # Also extract individual mask patterns for separate analysis
            a_only_str = '-'.join(['1' if p == 'Ab' else ('0' if p == 'ab' else 'X') for p in pairs])
            b_only_str = '-'.join(['1' if p == 'aB' else ('0' if p == 'ab' else 'X') for p in pairs])
            
            # Update counters
            self.pair_counter[combined_str] += 1  # Combined pattern
            self.mask_a_counter[a_only_str] += 1  # Mask A alone
            self.mask_b_counter[b_only_str] += 1  # Mask B alone
            
            # Track per-column masking frequency
            for col_idx, pair in enumerate(pairs):
                if pair == 'XX':
                    continue  # Skip NOT_PRESENT columns
                
                # Use column name if available, otherwise use position
                col_key = self.column_names[col_idx] if self.column_names else col_idx
                
                if 'A' in pair:  # Mask A has this column masked
                    self.column_mask_a_count[col_key] += 1
                if 'B' in pair:  # Mask B has this column masked
                    self.column_mask_b_count[col_key] += 1
            
            # Track how many columns were masked in each mask
            n_masked_a = combined_str.count('A')
            n_masked_b = combined_str.count('B')
            self.coverage_counter[(n_masked_a, n_masked_b)] += 1
            
            self.total_samples += 1
            
            # Optionally stream to disk
            if self.save_full_sequence:
                record = {
                    'epoch': epoch,
                    'batch': batch_idx,
                    'row': i,
                    'masks': combined_str,  # Single combined string like "Ab-aB-XX"
                    'mask_a': a_only_str,   # Individual patterns for analysis
                    'mask_b': b_only_str,
                }
                self.sequence_file.write(json.dumps(record) + '\n')
        
        # Save distribution periodically (every 100 batches)
        if batch_idx % 100 == 0:
            self.save_distribution()
            if self.save_full_sequence:
                self.sequence_file.flush()
    
    def verify_complementarity(self):
        """
        Verify that all mask pairs are truly complementary.
        
        With the Ab-aB-XX encoding, valid patterns at each position are:
        - 'Ab' (mask_a masked, mask_b available)
        - 'aB' (mask_a available, mask_b masked)
        - 'XX' (NOT_PRESENT)
        
        Invalid patterns (violations):
        - 'AB' (both masked - overlap!)
        - 'ab' (neither masked - uncovered!)
        
        Returns:
            List of violations: [(combined_string, count, violation_type), ...]
            Empty list means all masks are valid.
        """
        violations = []
        for combined_str, count in self.pair_counter.items():
            # Split by dashes to check each pair
            pairs = combined_str.split('-')
            
            for col_idx, pair in enumerate(pairs):
                if pair == 'AB':
                    violations.append((combined_str, count, f"OVERLAP at column {col_idx}"))
                    break
                elif pair == 'ab':
                    violations.append((combined_str, count, f"UNCOVERED at column {col_idx}"))
                    break
                elif pair not in ('Ab', 'aB', 'XX'):
                    violations.append((combined_str, count, f"INVALID pattern '{pair}' at column {col_idx}"))
                    break
        
        return violations
    
    def get_summary(self):
        """
        Get human-readable summary of mask distribution.
        
        Returns:
            Dictionary with statistics
        """
        # Convert tuple keys to strings for JSON serialization
        coverage_dist = {f"{k[0]},{k[1]}": v for k, v in sorted(self.coverage_counter.items())}
        
        # Convert most_common results to JSON-safe format (list of [key, count])
        # Keys might be complex objects that aren't JSON serializable
        def safe_most_common(counter, n=10):
            return [[str(k), v] for k, v in counter.most_common(n)]
        
        return {
            'total_samples': self.total_samples,
            'unique_mask_a_patterns': len(self.mask_a_counter),
            'unique_mask_b_patterns': len(self.mask_b_counter),
            'unique_pairs': len(self.pair_counter),
            'most_common_mask_a': safe_most_common(self.mask_a_counter),
            'most_common_mask_b': safe_most_common(self.mask_b_counter),
            'most_common_pairs': safe_most_common(self.pair_counter),
            'coverage_distribution': coverage_dist,
            'elapsed_time_seconds': time.time() - self.start_time,
        }
    
    def analyze_uniformity(self):
        """
        Analyze how uniform the mask distribution is.
        
        Returns:
            Dictionary with uniformity metrics
        """
        if self.total_samples == 0:
            return {}
        
        # Calculate entropy (higher = more uniform)
        def entropy(counter):
            total = sum(counter.values())
            if total == 0:
                return 0.0
            probs = [count / total for count in counter.values()]
            return -sum(p * np.log2(p) for p in probs if p > 0)
        
        # Calculate coefficient of variation (lower = more uniform)
        def cv(counter):
            counts = list(counter.values())
            if len(counts) == 0 or np.mean(counts) == 0:
                return 0.0
            return np.std(counts) / np.mean(counts)
        
        # Per-column uniformity (should be ~0.5 for each column)
        # Handle both numeric and string column keys
        column_frequencies = {}
        all_column_keys = set(self.column_mask_a_count.keys()) | set(self.column_mask_b_count.keys())
        
        for col_key in sorted(all_column_keys, key=lambda x: (isinstance(x, str), x)):
            freq_a = self.column_mask_a_count.get(col_key, 0) / self.total_samples
            freq_b = self.column_mask_b_count.get(col_key, 0) / self.total_samples
            # Convert col_key to string for JSON serialization
            col_key_str = str(col_key)
            column_frequencies[col_key_str] = {
                'mask_a_frequency': freq_a,
                'mask_b_frequency': freq_b,
                'combined_frequency': freq_a + freq_b,  # Should be ~1.0
            }
        
        return {
            'mask_a_entropy_bits': entropy(self.mask_a_counter),
            'mask_b_entropy_bits': entropy(self.mask_b_counter),
            'pair_entropy_bits': entropy(self.pair_counter),
            'mask_a_coefficient_of_variation': cv(self.mask_a_counter),
            'mask_b_coefficient_of_variation': cv(self.mask_b_counter),
            'max_theoretical_entropy_bits': np.log2(len(self.pair_counter)) if len(self.pair_counter) > 0 else 0,
            'column_frequencies': column_frequencies,
        }
    
    def save_distribution(self):
        """Save current distribution to disk."""
        try:
            distribution_data = {
                'summary': self.get_summary(),
                'uniformity': self.analyze_uniformity(),
                'last_updated': time.time(),
            }
            
            output_file = self.output_dir / "mask_distribution.json"
            with open(output_file, 'w') as f:
                json.dump(distribution_data, f, indent=2)
            
            self.last_save_time = time.time()
        except Exception as e:
            logger.error(f"Failed to save mask distribution: {e}")
    
    def save_final_report(self):
        """
        Generate and save final comprehensive report at end of training.
        """
        # Verify complementarity
        violations = self.verify_complementarity()
        
        report = {
            'training_complete': True,
            'timestamp': time.time(),
            'total_training_time_seconds': time.time() - self.start_time,
            'summary': self.get_summary(),
            'uniformity_analysis': self.analyze_uniformity(),
            'complementarity_check': {
                'violations_found': len(violations),
                'all_masks_valid': len(violations) == 0,
                'violations': violations[:100] if violations else [],  # Limit to first 100
            },
        }
        
        output_file = self.output_dir / "mask_final_report.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Log summary
        logger.info("=" * 80)
        logger.info("MASK DISTRIBUTION FINAL REPORT")
        logger.info("=" * 80)
        logger.info(f"Total samples: {self.total_samples:,}")
        logger.info(f"Unique mask A patterns: {len(self.mask_a_counter):,}")
        logger.info(f"Unique mask B patterns: {len(self.mask_b_counter):,}")
        logger.info(f"Unique pairs: {len(self.pair_counter):,}")
        
        uniformity = self.analyze_uniformity()
        logger.info(f"Mask A entropy: {uniformity.get('mask_a_entropy_bits', 0):.2f} bits")
        logger.info(f"Mask B entropy: {uniformity.get('mask_b_entropy_bits', 0):.2f} bits")
        
        if violations:
            logger.error(f"❌ COMPLEMENTARITY VIOLATIONS: {len(violations)} found!")
            for combined_str, count, violation_type in violations[:10]:
                logger.error(f"   {combined_str}: {count} occurrences - {violation_type}")
        else:
            logger.info("✅ Complementarity verified: All masks valid!")
        
        logger.info(f"Report saved to: {output_file}")
        logger.info("=" * 80)
        
        return report
    
    def close(self):
        """Close any open files and save final state."""
        logger.info("=" * 80)
        logger.info("📊 Finalizing mask tracking...")
        
        if self.sequence_file:
            self.sequence_file.close()
        
        self.save_distribution()
        self.save_final_report()
        
        logger.info("📊 Mask tracking complete!")
        logger.info("=" * 80)
    
    def __del__(self):
        """Ensure cleanup happens even if close() not called explicitly."""
        try:
            if hasattr(self, 'sequence_file') and self.sequence_file and not self.sequence_file.closed:
                self.close()
        except:
            pass  # Don't raise exceptions in __del__

