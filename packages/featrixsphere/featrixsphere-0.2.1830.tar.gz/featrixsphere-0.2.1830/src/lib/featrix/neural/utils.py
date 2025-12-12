import math
import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def filter_internal_columns(columns: List[str]) -> List[str]:
    """
    Filter out internal Featrix columns from a column list before showing to users.
    
    Internal columns that should be filtered:
    - __featrix_train_predictor: Training filter column
    - __featrix_meta_*: Metadata columns that should never be expanded or shown
    
    Args:
        columns: List of column names
        
    Returns:
        Filtered list with internal columns removed
    """
    return [col for col in columns if not col.startswith('__featrix')]


def ideal_batch_size(n_rows: int) -> int:
    """
    Compute a reasonable batch size for small-to-medium datasets.

    Logic:
    - Aim for roughly 20–200 steps per epoch (enough for learning dynamics).
    - Scale based on GPU memory (bigger GPUs can handle larger batches)
    - Use powers of two for GPU efficiency.
    - MINIMUM 128 for embedding space training (InfoNCE contrastive loss needs large batches)
    """
    import math
    import torch

    if n_rows < 128:
        return max(4, 2 ** int(math.log2(max(1, n_rows // 4))))
    elif n_rows < 1000:
        # roughly 32–64 steps/epoch
        target_steps = 40
        bs = max(4, min(n_rows // target_steps, 64))
    elif n_rows < 10000:
        # moderate size → batch ~128–512 (increased from 256)
        # Scale based on GPU memory
        target_steps = 50  # Reduced from 100 for larger batches
        bs = min(512, max(128, n_rows // target_steps))
    else:
        # large data → scale aggressively with GPU memory
        target_steps = 100  # Reduced from 200 for larger batches
        bs = min(2048, max(128, n_rows // target_steps))
    
    # round to nearest power of two for GPU friendliness
    bs = 2 ** int(round(math.log2(bs)))
    
    # CRITICAL: InfoNCE contrastive loss needs minimum batch size of 128
    # With smaller batches, the model has too few negatives and can't learn
    # Note: We use drop_last=True in DataLoader to avoid partial batches
    bs = max(128, bs)
    
    # MEMORY OPTIMIZATION: Cap batch size for large datasets to prevent OOM
    # For datasets with many columns (100+), reduce batch size to prevent VRAM exhaustion
    # Estimate columns from n_rows if not available (conservative estimate)
    # Rule: batch_size × num_columns should not exceed ~200k elements per batch
    # This prevents OOM on 50k×100 datasets
    max_batch_for_large_datasets = 1024  # Cap at 1024 for very large datasets
    if n_rows >= 20000:  # Large dataset - be more conservative
        bs = min(bs, max_batch_for_large_datasets)
        logger.info(f"📊 Large dataset ({n_rows} rows) - capping batch size at {bs} to prevent OOM")
    
    # Scale up based on GPU VRAM if available AND not forcing CPU mode
    import os
    force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
    
    if torch.cuda.is_available() and not force_cpu:
        try:
            gpu_mem_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
            # MEMORY OPTIMIZATION: More conservative scaling for large datasets
            if n_rows >= 20000:
                # For large datasets, be more conservative with batch size scaling
                if gpu_mem_gb >= 70:  # H100 (80GB)
                    bs = min(1024, bs * 2)  # Reduced from 4x to 2x, cap at 1024
                elif gpu_mem_gb >= 40:  # A100 (40GB)
                    bs = min(512, int(bs * 1.5))  # Reduced from 2x to 1.5x, cap at 512
                elif gpu_mem_gb >= 20:  # RTX 4090 (24GB)
                    bs = min(512, int(bs * 1.2))  # Reduced from 1.5x to 1.2x, cap at 512
            else:
                # For smaller datasets, use original aggressive scaling
                if gpu_mem_gb >= 70:  # H100 (80GB) - can handle 4x larger batches
                    bs = min(2048, bs * 4)
                elif gpu_mem_gb >= 40:  # A100 (40GB) - can handle 2x larger batches  
                    bs = min(1024, bs * 2)
                elif gpu_mem_gb >= 20:  # RTX 4090 (24GB) - can handle 1.5x larger batches
                    bs = min(512, int(bs * 1.5))
            # Round to power of 2 after scaling
            bs = 2 ** int(round(math.log2(bs)))
            logger.info(f"🚀 GPU-scaled batch size: {bs} (GPU VRAM: {gpu_mem_gb:.1f} GB, dataset: {n_rows} rows)")
        except:
            pass
    elif force_cpu:
        logger.info(f"💻 CPU mode: Using batch size {bs} (GPU scaling disabled)")
    
    return int(bs)




def ideal_epochs(n_rows: int, batch_size: int, mode: str) -> int:
    """
    Compute a recommended number of training epochs given dataset size, batch size, and mode.

    Modes:
      - 'predictor'        : training only the classifier/regressor head
      - 'embedding_space'  : fine-tuning the encoder / embedding space

    Heuristic:
      - 'predictor'       → ~800 optimizer updates
      - 'embedding_space' → ~1800 optimizer updates

    Note:
      Gradient accumulation is fixed at 1 — meaning we perform one optimizer
      update per batch (no simulated larger "effective batch" sizes).
      This keeps epoch counts directly tied to dataset size and step count.
    """
    mode = mode.lower()
    if mode not in {"predictor", "embedding_space"}:
        raise ValueError("mode must be 'predictor' or 'embedding_space'")

    target_updates = 7200 if mode == "predictor" else 36_000

    steps_per_epoch = max(1, math.ceil(n_rows / max(1, batch_size)))
    updates_per_epoch = steps_per_epoch  # grad_accum = 1

    epochs = math.ceil(target_updates / updates_per_epoch)
    return int(max(5, min(epochs, 300)))


def ideal_epochs_predictor(n_rows: int, batch_size: int, imbalance_ratio: float = 1.0) -> int:
    """
    Wrapper for training only the predictor head.
    
    Args:
        n_rows: Number of training samples
        batch_size: Batch size for training
        imbalance_ratio: Ratio of majority class to minority class (e.g., 35 for 97:3 split)
                        Higher values = more imbalanced = more epochs needed
    
    Returns:
        Number of epochs, adjusted for class imbalance
    """
    base_epochs = ideal_epochs(n_rows, batch_size, mode="predictor")
    
    # Adjust epochs based on imbalance ratio
    # For severe imbalance (ratio > 10), multiply epochs by sqrt of ratio
    # This gives more training time without making it excessive
    if imbalance_ratio > 10:
        adjustment_factor = min(math.sqrt(imbalance_ratio / 10), 3.0)  # Cap at 3x
        adjusted_epochs = int(base_epochs * adjustment_factor)
        return int(max(base_epochs, min(adjusted_epochs, 300)))
    
    return base_epochs


def ideal_epochs_embedding_space(n_rows: int, batch_size: int) -> int:
    """Wrapper for fine-tuning the embedding space."""
    return ideal_epochs(n_rows, batch_size, mode="embedding_space")


def analyze_dataset_complexity(
    train_df: pd.DataFrame,
    target_column: str,
    target_column_type: str
) -> Dict[str, Any]:
    """
    Analyze dataset complexity to inform neural network architecture decisions.
    
    This function examines:
    1. Feature-target relationships (correlation, mutual information, chi-square)
    2. Class imbalance (for classification)
    3. Nonlinearity indicators
    4. Data quality metrics
    
    Args:
        train_df: Training dataframe
        target_column: Name of target column
        target_column_type: "set" (classification) or "scalar" (regression)
    
    Returns:
        Dictionary with complexity metrics and architecture recommendations
    """
    import time
    start_time = time.time()
    
    logger.info("=" * 80)
    logger.info("📊 DATASET COMPLEXITY ANALYSIS")
    logger.info("=" * 80)
    
    n_rows = len(train_df)
    n_cols = len(train_df.columns) - 1  # Exclude target
    
    result = {
        'n_rows': n_rows,
        'n_cols': n_cols,
        'target_column': target_column,
        'target_column_type': target_column_type,
        'max_correlation': 0.0,
        'max_mutual_info': 0.0,
        'class_imbalance_ratio': 1.0,
        'nonlinearity_score': 0.0,
        'complexity_level': 'medium',  # low, medium, high
        'recommendations': []
    }
    
    # Separate features from target
    feature_cols = [col for col in train_df.columns if col != target_column]
    X = train_df[feature_cols]
    y = train_df[target_column]
    
    # Handle missing values by dropping them for analysis
    valid_mask = ~y.isna()
    X_clean = X[valid_mask]
    y_clean = y[valid_mask]
    
    if len(y_clean) < 10:
        logger.warning("⚠️  Too few valid samples for complexity analysis")
        result['complexity_level'] = 'low'
        return result
    
    # === ANALYSIS 1: Class Imbalance (for classification) ===
    if target_column_type == "set":
        value_counts = y_clean.value_counts()
        if len(value_counts) >= 2:
            majority_count = value_counts.iloc[0]
            minority_count = value_counts.iloc[-1]
            imbalance_ratio = majority_count / max(minority_count, 1)
            result['class_imbalance_ratio'] = imbalance_ratio
            result['majority_class'] = value_counts.index[0]
            result['minority_class'] = value_counts.index[-1]
            result['n_classes'] = len(value_counts)
            
            logger.info(f"\n📈 Class Distribution:")
            logger.info(f"   • Number of classes: {len(value_counts)}")
            for class_label, count in value_counts.items():
                pct = (count / len(y_clean)) * 100
                logger.info(f"   • '{class_label}': {count:,} ({pct:.1f}%)")
            
            if imbalance_ratio > 10:
                logger.info(f"\n⚠️  SEVERE CLASS IMBALANCE: {imbalance_ratio:.1f}:1 ratio")
                result['recommendations'].append(
                    f"Severe imbalance ({imbalance_ratio:.1f}:1) detected - using class weights is critical"
                )
            elif imbalance_ratio > 3:
                logger.info(f"\n⚖️  Moderate class imbalance: {imbalance_ratio:.1f}:1 ratio")
                result['recommendations'].append(
                    f"Moderate imbalance ({imbalance_ratio:.1f}:1) - class weights recommended"
                )
    
    # === ANALYSIS 2: Feature-Target Correlations ===
    logger.info(f"\n🔍 Feature-Target Relationship Analysis:")
    
    try:
        # Try mutual information (works for both classification and regression)
        from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
        
        # Convert to numeric for sklearn
        X_numeric = pd.DataFrame()
        for col in X_clean.columns:
            if X_clean[col].dtype in ['object', 'category', 'string']:
                # Convert categorical to numeric codes
                X_numeric[col] = pd.Categorical(X_clean[col]).codes
            else:
                X_numeric[col] = pd.to_numeric(X_clean[col], errors='coerce')
        
        # Fill NaN with column medians
        X_numeric = X_numeric.fillna(X_numeric.median())
        
        # Compute mutual information
        if target_column_type == "set":
            # Classification
            y_numeric = pd.Categorical(y_clean).codes
            mi_scores = mutual_info_classif(X_numeric, y_numeric, random_state=42)
        else:
            # Regression
            y_numeric = pd.to_numeric(y_clean, errors='coerce')
            mi_scores = mutual_info_regression(X_numeric, y_numeric, random_state=42)
        
        max_mi = np.max(mi_scores) if len(mi_scores) > 0 else 0.0
        mean_mi = np.mean(mi_scores) if len(mi_scores) > 0 else 0.0
        result['max_mutual_info'] = float(max_mi)
        result['mean_mutual_info'] = float(mean_mi)
        
        # Find top features
        top_n = min(5, len(mi_scores))
        top_indices = np.argsort(mi_scores)[-top_n:][::-1]
        
        logger.info(f"   • Mutual Information (higher = stronger relationship):")
        logger.info(f"     - Maximum MI: {max_mi:.4f}")
        logger.info(f"     - Mean MI: {mean_mi:.4f}")
        logger.info(f"     - Top {top_n} features:")
        for idx in top_indices:
            logger.info(f"       {X_numeric.columns[idx]}: {mi_scores[idx]:.4f}")
        
        # Interpret MI scores
        if max_mi < 0.05:
            logger.info(f"\n🔴 VERY WEAK relationships detected (max MI < 0.05)")
            logger.info(f"   → Likely requires DEEP network to capture complex patterns")
            result['complexity_level'] = 'high'
            result['recommendations'].append(
                "Very weak feature-target relationships suggest complex nonlinear patterns - deeper network recommended"
            )
        elif max_mi < 0.15:
            logger.info(f"\n🟡 WEAK relationships detected (max MI < 0.15)")
            logger.info(f"   → May require deeper network for nonlinear patterns")
            result['complexity_level'] = 'medium-high'
            result['recommendations'].append(
                "Weak feature correlations suggest nonlinear relationships - consider 3+ layers"
            )
        elif max_mi > 0.4:
            logger.info(f"\n🟢 STRONG relationships detected (max MI > 0.4)")
            logger.info(f"   → Shallower network may suffice")
            result['complexity_level'] = 'low-medium'
            result['recommendations'].append(
                "Strong feature-target relationships - shallower network (2-3 layers) may be sufficient"
            )
        
    except Exception as e:
        logger.warning(f"⚠️  Could not compute mutual information: {e}")
        result['recommendations'].append("Mutual information analysis failed - using conservative architecture")
    
    # === ANALYSIS 3: Chi-Square Test (for categorical target) ===
    if target_column_type == "set":
        try:
            from scipy.stats import chi2_contingency
            
            chi2_scores = []
            chi2_pvalues = []
            
            for col in feature_cols[:20]:  # Test first 20 features for speed
                try:
                    # Create contingency table
                    contingency = pd.crosstab(X_clean[col], y_clean)
                    chi2, pvalue, dof, expected = chi2_contingency(contingency)
                    chi2_scores.append(chi2)
                    chi2_pvalues.append(pvalue)
                except:
                    continue
            
            if chi2_pvalues:
                min_pvalue = np.min(chi2_pvalues)
                result['min_chi2_pvalue'] = float(min_pvalue)
                
                significant_features = sum(1 for p in chi2_pvalues if p < 0.05)
                logger.info(f"\n   • Chi-Square Test Results:")
                logger.info(f"     - Features tested: {len(chi2_pvalues)}")
                logger.info(f"     - Significant features (p < 0.05): {significant_features}")
                logger.info(f"     - Minimum p-value: {min_pvalue:.4f}")
                
                if min_pvalue > 0.2:
                    logger.info(f"     → No strong associations found - complex problem")
        except Exception as e:
            logger.warning(f"⚠️  Could not compute chi-square tests: {e}")
    
    # === ANALYSIS 4: Quick Nonlinearity Test ===
    if n_rows >= 200 and n_rows <= 10000:  # Only for reasonable sizes
        try:
            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LogisticRegression, Ridge
            from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
            from sklearn.metrics import accuracy_score, r2_score
            
            # Quick train/test split
            X_train, X_test, y_train, y_test = train_test_split(
                X_numeric, y_clean, test_size=0.25, random_state=42, stratify=y_clean if target_column_type == "set" else None
            )
            
            if target_column_type == "set":
                # Classification
                y_train_numeric = pd.Categorical(y_train).codes
                y_test_numeric = pd.Categorical(y_test).codes
                
                # Quick linear model
                lr = LogisticRegression(max_iter=100, random_state=42, solver='lbfgs')
                lr.fit(X_train, y_train_numeric)
                linear_score = accuracy_score(y_test_numeric, lr.predict(X_test))
                
                # Quick nonlinear model (shallow RF for speed)
                rf = RandomForestClassifier(n_estimators=20, max_depth=5, random_state=42, n_jobs=-1)
                rf.fit(X_train, y_train_numeric)
                nonlinear_score = accuracy_score(y_test_numeric, rf.predict(X_test))
            else:
                # Regression
                y_train_numeric = pd.to_numeric(y_train, errors='coerce')
                y_test_numeric = pd.to_numeric(y_test, errors='coerce')
                
                # Quick linear model
                lr = Ridge(alpha=1.0, random_state=42)
                lr.fit(X_train, y_train_numeric)
                linear_score = r2_score(y_test_numeric, lr.predict(X_test))
                
                # Quick nonlinear model
                rf = RandomForestRegressor(n_estimators=20, max_depth=5, random_state=42, n_jobs=-1)
                rf.fit(X_train, y_train_numeric)
                nonlinear_score = r2_score(y_test_numeric, rf.predict(X_test))
            
            nonlinearity_gain = nonlinear_score - linear_score
            result['nonlinearity_score'] = float(nonlinearity_gain)
            result['linear_baseline_score'] = float(linear_score)
            result['nonlinear_baseline_score'] = float(nonlinear_score)
            
            logger.info(f"\n   • Nonlinearity Test (Linear vs Random Forest):")
            logger.info(f"     - Linear model score: {linear_score:.4f}")
            logger.info(f"     - Nonlinear model score: {nonlinear_score:.4f}")
            logger.info(f"     - Nonlinearity gain: {nonlinearity_gain:+.4f}")
            
            if nonlinearity_gain > 0.15:
                logger.info(f"     🔴 STRONG nonlinearity detected (gain > 0.15)")
                logger.info(f"     → Deep network strongly recommended")
                result['complexity_level'] = 'high'
                result['recommendations'].append(
                    f"Strong nonlinearity detected (RF gain: {nonlinearity_gain:.3f}) - deep network (3-4 layers) recommended"
                )
            elif nonlinearity_gain > 0.05:
                logger.info(f"     🟡 MODERATE nonlinearity detected (gain > 0.05)")
                logger.info(f"     → Moderate depth beneficial")
                if result['complexity_level'] == 'low-medium':
                    result['complexity_level'] = 'medium'
            elif nonlinearity_gain < 0:
                logger.info(f"     🟢 Linear model performs well")
                logger.info(f"     → Shallower network may be sufficient")
        
        except Exception as e:
            logger.warning(f"⚠️  Could not run nonlinearity test: {e}")
    
    # === Final Complexity Assessment ===
    logger.info(f"\n" + "=" * 80)
    logger.info(f"🎯 COMPLEXITY ASSESSMENT: {result['complexity_level'].upper()}")
    logger.info(f"=" * 80)
    
    if result['recommendations']:
        logger.info(f"\n💡 Key Recommendations:")
        for i, rec in enumerate(result['recommendations'], 1):
            logger.info(f"   {i}. {rec}")
    
    elapsed_time = time.time() - start_time
    logger.info(f"\n⏱️  Analysis completed in {elapsed_time:.2f} seconds")
    logger.info("=" * 80)
    
    return result


def ideal_single_predictor_config(
    n_rows: int,
    d_model: int = 128,
    n_cols: int = None,
    fine_tune: bool = True,
    complexity_analysis: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Compute optimal configuration for single predictor MLP based on dataset size.
    
    Args:
        n_rows: Number of training samples
        d_model: Embedding space dimensionality (default 128)
        n_cols: Number of input columns (optional, for complexity analysis)
        fine_tune: Whether the embedding space will be fine-tuned during training
        complexity_analysis: Optional output from analyze_dataset_complexity()
    
    Returns:
        Dictionary with configuration:
        - d_hidden: Hidden layer dimension (None = use linear head)
        - n_hidden_layers: Number of hidden layers (0 = linear head)
        - dropout: Dropout rate
        - use_batch_norm: Whether to use batch normalization
        - residual: Whether to use residual connections
    """
    if n_rows < 500:
        return {
            "d_hidden": None,          # linear head
            "n_hidden_layers": 0,
            "dropout": 0.0,
            "use_batch_norm": False,
            "residual": False,
        }
    elif n_rows < 2000:
        return {
            "d_hidden": min(64, 2 * d_model),
            "n_hidden_layers": 1,
            "dropout": 0.1,
            "use_batch_norm": False,
            "residual": False,
        }
    else:
        # For larger datasets, use complexity analysis if available
        d_hidden = 256  # Default
        n_hidden_layers = 2  # Default baseline
        dropout = 0.3
        use_batch_norm = True
        residual = True
        
        # Apply complexity analysis if available
        if complexity_analysis is not None:
            max_mi = complexity_analysis.get('max_mutual_info', 0.0)
            nonlinearity = complexity_analysis.get('nonlinearity_score', 0.0)
            
            # Adjust layers based on complexity
            if n_rows >= 5000:
                n_hidden_layers += 1  # 3 layers for 5k+ rows
            if n_rows >= 10000:
                n_hidden_layers += 1  # 4 layers for 10k+ rows
            
            # Very weak correlations suggest complex nonlinear patterns
            if max_mi < 0.05 and n_rows >= 2000:
                n_hidden_layers = max(n_hidden_layers, 3)
                if n_rows >= 5000:
                    n_hidden_layers = max(n_hidden_layers, 4)
            elif max_mi < 0.15 and n_rows >= 3000:
                n_hidden_layers = max(n_hidden_layers, 3)
            
            # Strong nonlinearity detected
            if nonlinearity > 0.15 and n_rows >= 2000:
                n_hidden_layers = max(n_hidden_layers, 3)
                if n_rows >= 5000:
                    n_hidden_layers = max(n_hidden_layers, 4)
            elif nonlinearity > 0.05 and n_rows >= 3000:
                n_hidden_layers = max(n_hidden_layers, 3)
            
            # Strong correlations = simpler problem
            if max_mi > 0.4 and nonlinearity < 0.05:
                n_hidden_layers = min(n_hidden_layers, 3)
        
        # Cap at 4 layers
        n_hidden_layers = min(n_hidden_layers, 4)
        
        return {
            "d_hidden": d_hidden,
            "n_hidden_layers": n_hidden_layers,
            "dropout": dropout,
            "use_batch_norm": use_batch_norm,
            "residual": residual,
        }


def ideal_single_predictor_hidden_layers(
    n_rows: int, 
    n_cols: int, 
    d_model: int = 128,
    fine_tune: bool = True,
    complexity_analysis: Optional[Dict[str, Any]] = None
) -> int:
    """
    Compute a reasonable number of hidden layers for the single predictor MLP.
    
    Args:
        n_rows: Number of training samples
        n_cols: Number of input columns (features)
        d_model: Embedding space dimensionality (default 128)
        fine_tune: Whether the embedding space will be fine-tuned during training
        complexity_analysis: Optional output from analyze_dataset_complexity()
    
    Returns:
        Number of hidden layers (2-4)
    
    Logic:
        - Start with baseline of 2 layers (proven default)
        - Increase for complex datasets (many columns, sufficient rows)
        - Increase if fine-tuning (more capacity available)
        - Increase if complexity analysis shows nonlinearity or weak correlations
        - Adjust for extreme class imbalance
        - Cap at 4 layers to prevent overfitting on typical dataset sizes
    
    Examples:
        - Small dataset (< 1000 rows, < 50 cols):         2 layers
        - Medium dataset (2500 rows, 100 cols):           2-3 layers
        - Large complex (10k rows, 300 cols, finetune):   3-4 layers
        - Weak correlations + nonlinearity:               3-4 layers
    """
    # Baseline: 2 layers is solid for most cases
    layers = 2
    reasons = []
    
    # Factor 1: Dataset size
    # Need sufficient data to support more parameters
    if n_rows >= 5000:
        layers += 1  # 3 layers for 5k+ rows
        reasons.append(f"Dataset size ({n_rows:,} rows) supports deeper network")
    if n_rows >= 10000:
        layers += 1  # 4 layers for 10k+ rows
        reasons.append(f"Large dataset ({n_rows:,} rows) can leverage maximum depth")
    
    # Factor 2: Data complexity (number of columns)
    # More columns = more complex relationships to learn
    if n_cols >= 150 and n_rows >= 2500:
        layers = max(layers, 3)  # At least 3 layers for very wide data
        reasons.append(f"Wide dataset ({n_cols} columns) benefits from deeper network")
    
    # Factor 3: Fine-tuning capability
    # Fine-tuning means more total parameters can adapt, supporting deeper predictor
    if fine_tune and n_rows >= 3000 and n_cols >= 100:
        layers = max(layers, 3)  # At least 3 layers when fine-tuning complex data
        reasons.append("Fine-tuning enabled - can leverage deeper predictor")
    
    # Factor 4: Complexity analysis (NEW)
    if complexity_analysis is not None:
        max_mi = complexity_analysis.get('max_mutual_info', 0.0)
        nonlinearity = complexity_analysis.get('nonlinearity_score', 0.0)
        imbalance_ratio = complexity_analysis.get('class_imbalance_ratio', 1.0)
        complexity_level = complexity_analysis.get('complexity_level', 'medium')
        
        # Very weak correlations suggest complex nonlinear patterns
        if max_mi < 0.05 and n_rows >= 2000:
            layers = max(layers, 3)
            reasons.append(f"Very weak feature correlations (MI={max_mi:.3f}) suggest nonlinear patterns")
            if n_rows >= 5000:
                layers = max(layers, 4)
                reasons.append("Large dataset + weak correlations = deep network recommended")
        elif max_mi < 0.15 and n_rows >= 3000:
            layers = max(layers, 3)
            reasons.append(f"Weak feature correlations (MI={max_mi:.3f}) indicate nonlinearity")
        
        # Strong nonlinearity detected
        if nonlinearity > 0.15 and n_rows >= 2000:
            layers = max(layers, 3)
            reasons.append(f"Strong nonlinearity detected (gain={nonlinearity:.3f})")
            if n_rows >= 5000:
                layers = max(layers, 4)
        elif nonlinearity > 0.05 and n_rows >= 3000:
            layers = max(layers, 3)
            reasons.append(f"Moderate nonlinearity detected (gain={nonlinearity:.3f})")
        
        # Strong correlations = simpler problem
        if max_mi > 0.4 and nonlinearity < 0.05:
            layers = min(layers, 3)
            reasons.append(f"Strong linear relationships (MI={max_mi:.3f}) - shallower network sufficient")
        
        # Extreme class imbalance may benefit from extra capacity
        if imbalance_ratio > 100 and n_rows >= 3000:
            layers = max(layers, 3)
            reasons.append(f"Extreme class imbalance ({imbalance_ratio:.1f}:1) - extra capacity for minority class")
    
    # Factor 5: Very small datasets - use simple linear layer
    if n_rows < 1000:
        if layers > 0:
            reasons.append(f"Very small dataset ({n_rows} rows) - using simple linear layer (no hidden layers) to prevent overfitting")
        layers = 0  # Use simple Linear(d_model, d_out) for very small datasets
    elif n_rows < 2000:
        if layers > 2:
            reasons.append(f"Small dataset ({n_rows} rows) - capping at 2 layers to prevent overfitting")
        layers = min(layers, 2)  # Cap at 2 layers for small datasets
    
    # Final cap: Never exceed 4 layers
    # Diminishing returns and overfitting risk beyond this
    if layers > 4:
        reasons.append("Capping at 4 layers (proven maximum for typical dataset sizes)")
        layers = 4
    
    layers = min(layers, 4)
    
    # Log the decision
    logger.info(f"\n🏗️  NEURAL NETWORK ARCHITECTURE DECISION")
    logger.info(f"   → Selected {layers} hidden layers")
    if reasons:
        logger.info(f"   → Reasoning:")
        for reason in reasons:
            logger.info(f"     • {reason}")
    
    return int(layers)


