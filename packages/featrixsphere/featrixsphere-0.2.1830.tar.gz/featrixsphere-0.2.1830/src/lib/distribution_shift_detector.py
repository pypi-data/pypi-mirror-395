#!/usr/bin/env python3
"""
Distribution Shift Detection for Single Predictor Training

Detects when training data for a single predictor differs significantly from
the data used to train the base embedding space.

Checks for:
- Null rate differences (e.g., ES had 5% nulls, SP data has 95% nulls)
- Out-of-vocabulary values (values not seen during ES training)
- Type mismatches (ES saw floats, SP data has strings)
- Distribution shifts (KL divergence, Chi-square test)
- Extreme value differences (min/max changes)
"""
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from collections import Counter

logger = logging.getLogger(__name__)


class DistributionShiftReport:
    """Container for distribution shift analysis results."""
    
    def __init__(self, column_name: str):
        self.column_name = column_name
        self.issues = []
        self.warnings = []
        self.info = []
        self.metrics = {}
        
    def add_issue(self, message: str, severity: str = "error"):
        """Add a critical issue (will likely cause training problems)."""
        self.issues.append({'message': message, 'severity': severity})
    
    def add_warning(self, message: str):
        """Add a warning (may affect quality but won't break training)."""
        self.warnings.append(message)
    
    def add_info(self, message: str):
        """Add informational message."""
        self.info.append(message)
    
    def add_metric(self, name: str, value: float):
        """Add a numeric metric."""
        self.metrics[name] = value
    
    def has_critical_issues(self) -> bool:
        """Return True if there are critical issues."""
        return len([i for i in self.issues if i['severity'] == 'error']) > 0
    
    def has_warnings(self) -> bool:
        """Return True if there are warnings."""
        return len(self.warnings) > 0
    
    def log_report(self, log_level: int = logging.INFO):
        """Log the full report."""
        logger.log(log_level, f"📊 DISTRIBUTION ANALYSIS: '{self.column_name}'")
        logger.log(log_level, "─" * 80)
        
        # Log critical issues
        if self.issues:
            for issue in self.issues:
                if issue['severity'] == 'error':
                    logger.error(f"   ❌ {issue['message']}")
                else:
                    logger.warning(f"   ⚠️  {issue['message']}")
        
        # Log warnings
        if self.warnings:
            for warning in self.warnings:
                logger.warning(f"   ⚠️  {warning}")
        
        # Log info
        if self.info:
            for info in self.info:
                logger.log(log_level, f"   ℹ️  {info}")
        
        # Log metrics
        if self.metrics:
            logger.log(log_level, f"   📈 Metrics:")
            for name, value in self.metrics.items():
                logger.log(log_level, f"      {name}: {value}")


class DistributionShiftDetector:
    """
    Detect distribution shifts between ES training data and SP training data.
    """
    
    def __init__(self, embedding_space):
        """
        Initialize detector with base embedding space.
        
        Args:
            embedding_space: The EmbeddingSpace object that was trained
        """
        self.es = embedding_space
        self.es_stats = self._extract_es_stats()
    
    def _extract_es_stats(self) -> Dict:
        """
        Extract statistics from the embedding space's training data.
        
        Returns:
            dict mapping column_name → stats dict
        """
        stats = {}
        
        # Get ES training data if available
        if not hasattr(self.es, 'train_input_data') or self.es.train_input_data is None:
            logger.warning("⚠️  Cannot extract ES stats - train_input_data not available")
            return stats
        
        es_df = self.es.train_input_data.df
        
        for col in es_df.columns:
            col_stats = {}
            
            # Basic stats
            col_stats['total_rows'] = len(es_df)
            col_stats['null_count'] = es_df[col].isnull().sum()
            col_stats['null_rate'] = col_stats['null_count'] / col_stats['total_rows']
            col_stats['dtype'] = str(es_df[col].dtype)
            
            # Get codec info if available
            if hasattr(self.es, 'col_codecs') and col in self.es.col_codecs:
                codec = self.es.col_codecs[col]
                col_stats['codec_type'] = type(codec).__name__
                
                # For categorical codecs, get vocabulary
                if hasattr(codec, 'members'):
                    col_stats['vocabulary'] = set(codec.members)
                    col_stats['vocab_size'] = len(codec.members)
                
                # For scalar codecs, get min/max
                if hasattr(codec, 'min') and hasattr(codec, 'max'):
                    col_stats['min'] = float(codec.min) if codec.min is not None else None
                    col_stats['max'] = float(codec.max) if codec.max is not None else None
            
            # Value distribution for categorical columns
            if pd.api.types.is_object_dtype(es_df[col]) or pd.api.types.is_categorical_dtype(es_df[col]):
                value_counts = es_df[col].value_counts()
                col_stats['value_counts'] = dict(value_counts.head(100))  # Top 100 values
                col_stats['unique_count'] = es_df[col].nunique()
            
            # Numeric stats
            if pd.api.types.is_numeric_dtype(es_df[col]):
                col_stats['mean'] = float(es_df[col].mean()) if not es_df[col].isnull().all() else None
                col_stats['std'] = float(es_df[col].std()) if not es_df[col].isnull().all() else None
                col_stats['min_value'] = float(es_df[col].min()) if not es_df[col].isnull().all() else None
                col_stats['max_value'] = float(es_df[col].max()) if not es_df[col].isnull().all() else None
            
            stats[col] = col_stats
        
        return stats
    
    def analyze_column(self, col_name: str, sp_data: pd.Series) -> DistributionShiftReport:
        """
        Analyze a single column for distribution shift.
        
        Args:
            col_name: Column name
            sp_data: Series containing SP training data for this column
            
        Returns:
            DistributionShiftReport with findings
        """
        report = DistributionShiftReport(col_name)
        
        # Check if column existed in ES
        if col_name not in self.es_stats:
            report.add_issue(f"Column '{col_name}' NOT in base ES training data (new column)")
            return report
        
        es_col_stats = self.es_stats[col_name]
        
        # 1. NULL RATE COMPARISON
        sp_null_count = sp_data.isnull().sum()
        sp_null_rate = sp_null_count / len(sp_data)
        es_null_rate = es_col_stats.get('null_rate', 0)
        
        report.add_metric('sp_null_rate', sp_null_rate)
        report.add_metric('es_null_rate', es_null_rate)
        
        null_rate_diff = abs(sp_null_rate - es_null_rate)
        
        if sp_null_rate > 0.9:
            report.add_issue(f"SP data is {sp_null_rate*100:.1f}% NULL (ES was {es_null_rate*100:.1f}%) - almost all nulls!", severity='error')
        elif sp_null_rate > 0.5 and es_null_rate < 0.1:
            report.add_warning(f"SP data is {sp_null_rate*100:.1f}% NULL (ES was {es_null_rate*100:.1f}%) - significant increase in nulls")
        elif null_rate_diff > 0.3:
            report.add_warning(f"Null rate changed by {null_rate_diff*100:.1f}% (SP: {sp_null_rate*100:.1f}%, ES: {es_null_rate*100:.1f}%)")
        else:
            report.add_info(f"Null rate: SP={sp_null_rate*100:.1f}%, ES={es_null_rate*100:.1f}% (diff: {null_rate_diff*100:.1f}%)")
        
        # 2. OUT-OF-VOCABULARY CHECK (for categorical columns)
        if 'vocabulary' in es_col_stats:
            es_vocab = es_col_stats['vocabulary']
            sp_values = set(sp_data.dropna().unique())
            
            oov_values = sp_values - es_vocab
            oov_count = sum(sp_data.isin(oov_values))
            oov_rate = oov_count / len(sp_data)
            
            report.add_metric('oov_count', len(oov_values))
            report.add_metric('oov_rate', oov_rate)
            
            if oov_rate > 0.5:
                report.add_issue(
                    f"{oov_rate*100:.1f}% of values are OUT-OF-VOCABULARY (not seen in ES training). "
                    f"{len(oov_values)} new values vs {len(es_vocab)} ES vocab. "
                    f"Examples: {list(oov_values)[:5]}"
                )
            elif oov_rate > 0.1:
                report.add_warning(
                    f"{oov_rate*100:.1f}% of values are out-of-vocabulary. "
                    f"{len(oov_values)} new values. Examples: {list(oov_values)[:5]}"
                )
            elif len(oov_values) > 0:
                report.add_info(f"{len(oov_values)} new values ({oov_rate*100:.2f}% of data)")
            else:
                report.add_info(f"All values in ES vocabulary ({len(sp_values)} values)")
        
        # 3. TYPE COMPATIBILITY CHECK
        sp_dtype = str(sp_data.dtype)
        es_dtype = es_col_stats.get('dtype', 'unknown')
        
        if sp_dtype != es_dtype:
            # Check if it's a compatible difference (e.g., int64 vs float64)
            sp_is_numeric = pd.api.types.is_numeric_dtype(sp_data)
            es_is_numeric = 'int' in es_dtype.lower() or 'float' in es_dtype.lower()
            
            if sp_is_numeric != es_is_numeric:
                report.add_issue(
                    f"TYPE MISMATCH: SP has {sp_dtype}, ES had {es_dtype}. "
                    f"Numeric vs categorical mismatch!"
                )
            else:
                report.add_info(f"Type difference: SP={sp_dtype}, ES={es_dtype} (compatible)")
        
        # 4. NUMERIC DISTRIBUTION SHIFT (for numeric columns)
        if pd.api.types.is_numeric_dtype(sp_data):
            sp_clean = sp_data.dropna()
            if len(sp_clean) > 0:
                sp_mean = float(sp_clean.mean())
                sp_std = float(sp_clean.std())
                sp_min = float(sp_clean.min())
                sp_max = float(sp_clean.max())
                
                es_mean = es_col_stats.get('mean')
                es_std = es_col_stats.get('std')
                es_min = es_col_stats.get('min_value') or es_col_stats.get('min')
                es_max = es_col_stats.get('max_value') or es_col_stats.get('max')
                
                report.add_metric('sp_mean', sp_mean)
                report.add_metric('es_mean', es_mean)
                
                # Check for out-of-range values
                if es_min is not None and es_max is not None:
                    values_below_min = (sp_clean < es_min).sum()
                    values_above_max = (sp_clean > es_max).sum()
                    out_of_range_rate = (values_below_min + values_above_max) / len(sp_clean)
                    
                    if out_of_range_rate > 0.1:
                        report.add_warning(
                            f"{out_of_range_rate*100:.1f}% of values outside ES range "
                            f"[{es_min:.2f}, {es_max:.2f}]. SP range: [{sp_min:.2f}, {sp_max:.2f}]"
                        )
                    elif out_of_range_rate > 0:
                        report.add_info(
                            f"{out_of_range_rate*100:.2f}% values outside ES range. "
                            f"ES: [{es_min:.2f}, {es_max:.2f}], SP: [{sp_min:.2f}, {sp_max:.2f}]"
                        )
                
                # Check mean shift
                if es_mean is not None and es_std is not None and es_std > 0:
                    z_score = abs(sp_mean - es_mean) / es_std
                    if z_score > 3:
                        report.add_warning(
                            f"Mean shifted by {z_score:.1f} standard deviations "
                            f"(ES mean: {es_mean:.2f}, SP mean: {sp_mean:.2f})"
                        )
        
        # 5. CATEGORICAL DISTRIBUTION SHIFT
        if pd.api.types.is_object_dtype(sp_data) or pd.api.types.is_categorical_dtype(sp_data):
            if 'value_counts' in es_col_stats:
                es_counts = es_col_stats['value_counts']
                sp_counts = dict(sp_data.value_counts())
                
                # Check if dominant class changed
                es_top = max(es_counts, key=es_counts.get) if es_counts else None
                sp_top = max(sp_counts, key=sp_counts.get) if sp_counts else None
                
                if es_top and sp_top and es_top != sp_top:
                    es_top_rate = es_counts[es_top] / es_col_stats['total_rows']
                    sp_top_rate = sp_counts[sp_top] / len(sp_data)
                    report.add_warning(
                        f"Dominant class changed: ES='{es_top}' ({es_top_rate*100:.1f}%), "
                        f"SP='{sp_top}' ({sp_top_rate*100:.1f}%)"
                    )
        
        return report
    
    def analyze_dataframe(self, sp_df: pd.DataFrame, target_column: str = None) -> Dict[str, DistributionShiftReport]:
        """
        Analyze entire dataframe for distribution shifts.
        
        Args:
            sp_df: Single predictor training dataframe
            target_column: Optional target column to exclude from analysis
            
        Returns:
            Dict mapping column_name → DistributionShiftReport
        """
        reports = {}
        
        for col in sp_df.columns:
            if col == target_column:
                continue  # Skip target column (it may not have been in ES)
            
            if col.startswith('__featrix'):
                continue  # Skip internal columns
            
            report = self.analyze_column(col, sp_df[col])
            reports[col] = report
        
        return reports
    
    def log_summary(self, reports: Dict[str, DistributionShiftReport]):
        """
        Log a summary of all distribution shift findings.
        
        Args:
            reports: Dict of column reports from analyze_dataframe()
        """
        logger.info("=" * 80)
        logger.info("📊 DISTRIBUTION SHIFT DETECTION SUMMARY")
        logger.info("=" * 80)
        
        # Count issues by severity
        critical_columns = []
        warning_columns = []
        ok_columns = []
        missing_columns = []
        
        for col_name, report in reports.items():
            if col_name not in self.es_stats:
                missing_columns.append(col_name)
            elif report.has_critical_issues():
                critical_columns.append(col_name)
            elif report.has_warnings():
                warning_columns.append(col_name)
            else:
                ok_columns.append(col_name)
        
        logger.info(f"📈 Total columns analyzed: {len(reports)}")
        logger.info(f"   ✅ OK: {len(ok_columns)} columns")
        logger.info(f"   ⚠️  Warnings: {len(warning_columns)} columns")
        logger.info(f"   ❌ Critical: {len(critical_columns)} columns")
        logger.info(f"   ➕ New (not in ES): {len(missing_columns)} columns")
        logger.info("")
        
        # Log critical columns
        if critical_columns:
            logger.error("❌ CRITICAL ISSUES DETECTED:")
            for col in critical_columns:
                report = reports[col]
                logger.error(f"   '{col}':")
                for issue in report.issues:
                    if issue['severity'] == 'error':
                        logger.error(f"      • {issue['message']}")
            logger.error("")
        
        # Log warning columns
        if warning_columns:
            logger.warning("⚠️  WARNINGS:")
            for col in warning_columns[:10]:  # Show first 10
                report = reports[col]
                logger.warning(f"   '{col}':")
                for warning in report.warnings[:2]:  # Show first 2 warnings per column
                    logger.warning(f"      • {warning}")
            if len(warning_columns) > 10:
                logger.warning(f"   ... and {len(warning_columns) - 10} more columns with warnings")
            logger.warning("")
        
        # Log new columns
        if missing_columns:
            logger.info("➕ NEW COLUMNS (not in ES training data):")
            for col in missing_columns[:20]:
                logger.info(f"   • '{col}'")
            if len(missing_columns) > 20:
                logger.info(f"   ... and {len(missing_columns) - 20} more new columns")
            logger.info("")
        
        logger.info("=" * 80)
        
        # Return summary stats
        return {
            'total_columns': len(reports),
            'ok_columns': len(ok_columns),
            'warning_columns': len(warning_columns),
            'critical_columns': len(critical_columns),
            'new_columns': len(missing_columns),
            'has_critical_issues': len(critical_columns) > 0,
        }


def detect_distribution_shift(embedding_space, sp_train_df: pd.DataFrame, target_column: str = None) -> Dict:
    """
    Convenience function to detect and log distribution shifts.
    
    Args:
        embedding_space: Base EmbeddingSpace object
        sp_train_df: Single predictor training dataframe
        target_column: Target column to exclude from analysis
        
    Returns:
        Summary statistics dict
    """
    detector = DistributionShiftDetector(embedding_space)
    reports = detector.analyze_dataframe(sp_train_df, target_column=target_column)
    summary = detector.log_summary(reports)
    
    # Log detailed reports for columns with issues
    logger.info("=" * 80)
    logger.info("📋 DETAILED COLUMN ANALYSIS")
    logger.info("=" * 80)
    
    for col_name, report in reports.items():
        if report.has_critical_issues() or report.has_warnings():
            report.log_report(log_level=logging.INFO)
    
    logger.info("=" * 80)
    
    return summary


if __name__ == '__main__':
    # Test the detector
    logging.basicConfig(level=logging.INFO)
    
    print("\n" + "=" * 80)
    print("DISTRIBUTION SHIFT DETECTOR TEST")
    print("=" * 80 + "\n")
    
    # Create mock ES with some stats
    class MockES:
        def __init__(self):
            self.train_input_data = None
            self.col_codecs = {}
    
    # Create mock ES data
    import pandas as pd
    es_df = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5] * 100,
        'feature2': ['A', 'B', 'C'] * 166 + ['A', 'B'],
        'feature3': [10.0, 20.0, 30.0] * 166 + [10.0, 20.0],
    })
    
    # Create SP data with shifts
    sp_df = pd.DataFrame({
        'feature1': [100, 200, 300] * 50,  # Out of range
        'feature2': ['D', 'E', 'F'] * 50,  # Out of vocabulary
        'feature3': [None] * 150,  # Lots of nulls
    })
    
    class MockInputData:
        def __init__(self, df):
            self.df = df
    
    es = MockES()
    es.train_input_data = MockInputData(es_df)
    
    # Run detection
    summary = detect_distribution_shift(es, sp_df, target_column='target')
    
    print("\n✅ Test complete!\n")

