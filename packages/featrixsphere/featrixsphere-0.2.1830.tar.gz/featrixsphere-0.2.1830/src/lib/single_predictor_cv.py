#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
"""
Proper K-fold cross-validation for single predictor training.

This module implements true cross-validation where:
1. 5 independent predictors are trained (one per fold)
2. Each predictor trains only on its fold's training data
3. Each predictor is evaluated on its fold's validation data
4. The best predictor is selected based on validation performance
5. Only the best predictor is returned and saved

This is different from the sequential/incremental approach where
one predictor is trained across all folds sequentially.
"""
import asyncio
import logging
import os
from typing import Optional, Dict, Any, List, Tuple

import pandas as pd
from sklearn.model_selection import KFold

from featrix.neural.embedded_space import EmbeddingSpace
from featrix.neural.single_predictor import FeatrixSinglePredictor

logger = logging.getLogger(__name__)


def train_with_proper_cv(
    embedding_space: EmbeddingSpace,
    train_df: pd.DataFrame,
    args: Any,  # LightSinglePredictorArgs
    epochs: int,
    batch_size: int,
    predictor_base: Any,  # The predictor architecture (SimpleMLP)
    predictor_name: str,
    progress_callback: Optional[callable] = None,
) -> FeatrixSinglePredictor:
    """
    Train 5 independent predictors using proper K-fold cross-validation.
    
    Each fold trains a completely independent predictor, then the best one
    is selected based on validation performance.
    
    Args:
        embedding_space: Pre-trained embedding space (shared across all folds)
        train_df: Full training dataset (will be split into folds)
        args: Training arguments (LightSinglePredictorArgs)
        epochs: Total epochs (will be divided across folds)
        batch_size: Batch size for training
        predictor_base: The predictor architecture to use (will be cloned per fold)
        predictor_name: Name for the predictor
        progress_callback: Optional callback for training progress
        
    Returns:
        The best predictor based on validation performance
    """
    n_folds = 5
    
    logger.info("="*100)
    logger.info("🔀 PROPER K-FOLD CROSS-VALIDATION: Training 5 independent predictors")
    logger.info(f"   Epochs specified: {epochs}")
    logger.info("   Each fold trains an independent predictor from scratch")
    logger.info("   Best predictor will be selected based on validation performance")
    logger.info("="*100)
    
    # Each fold gets the FULL epoch count (not divided)
    epochs_per_fold = epochs
    logger.info(f"📊 Training plan: {epochs_per_fold} epochs per fold × {n_folds} folds = {epochs_per_fold * n_folds} total epochs")
    
    # K-Fold splitter (shuffle for randomness, fixed seed for reproducibility)
    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
    
    # Store predictors and metrics for each fold
    fold_predictors: List[FeatrixSinglePredictor] = []
    fold_metrics: List[Dict[str, Any]] = []
    fold_val_losses: List[float] = []
    
    # Train each fold independently
    for fold_idx, (train_idx, val_idx) in enumerate(kf.split(train_df)):
        logger.info("="*80)
        logger.info(f"🔀 FOLD {fold_idx + 1}/{n_folds}: Training independent predictor")
        logger.info(f"   Training on {len(train_idx)} rows, validating on {len(val_idx)} rows")
        logger.info("="*80)
        
        # Create fold-specific train/val data
        fold_train_df = train_df.iloc[train_idx].copy().reset_index(drop=True)
        fold_val_df = train_df.iloc[val_idx].copy().reset_index(drop=True)
        
        # Create a NEW predictor instance for this fold
        # Clone the predictor architecture (same structure, fresh weights)
        import copy
        fold_predictor_base = copy.deepcopy(predictor_base)
        
        fold_predictor_name = f"{predictor_name}_fold_{fold_idx + 1}"
        logger.info(f"   Creating new predictor instance: {fold_predictor_name}")
        
        fold_fsp = FeatrixSinglePredictor(
            embedding_space=embedding_space,
            predictor=fold_predictor_base,
            name=fold_predictor_name,
            user_metadata=args.user_metadata
        )
        
        # Prep for training with fold-specific data
        logger.info(f"   Preparing predictor for fold {fold_idx + 1}...")
        fold_fsp.prep_for_training(
            train_df=fold_train_df,
            target_col_name=args.target_column,
            target_col_type=args.target_column_type,
            use_class_weights=args.use_class_weights,
            class_imbalance=args.class_imbalance,
            cost_false_positive=args.cost_false_positive,
            cost_false_negative=args.cost_false_negative
        )
        
        # Train this fold's predictor independently
        logger.info(f"🏋️  Training fold {fold_idx + 1} predictor for {epochs_per_fold} epochs...")
        
        asyncio.run(fold_fsp.train(
            n_epochs=epochs_per_fold,
            batch_size=batch_size,
            fine_tune=args.fine_tune,
            val_df=fold_val_df,  # Use fold-specific validation set
            optimizer_params={"lr": args.learning_rate},
            val_pos_label=args.positive_label,
            print_callback=progress_callback,
            print_progress_step=10,
            job_id=args.job_id,
        ))
        
        # Store predictor and metrics
        fold_predictors.append(fold_fsp)
        
        # Extract metrics
        metrics = fold_fsp.training_metrics if hasattr(fold_fsp, 'training_metrics') and fold_fsp.training_metrics else {}
        fold_metrics.append(metrics)
        
        # Extract validation loss (for regression or as fallback)
        val_loss = metrics.get('validation_loss', float('inf'))
        if val_loss is None:
            val_loss = float('inf')
        fold_val_losses.append(val_loss)
        
        logger.info(f"✅ Fold {fold_idx + 1} completed")
        logger.info(f"   Validation loss: {val_loss:.6f}")
        if metrics:
            auc = metrics.get('auc', None)
            if auc is not None:
                logger.info(f"   AUC: {auc:.4f}")
            accuracy = metrics.get('accuracy', None)
            if accuracy is not None:
                logger.info(f"   Accuracy: {accuracy:.4f}")
    
    # Select the best predictor
    logger.info("="*80)
    logger.info("🏆 SELECTING BEST PREDICTOR")
    logger.info("="*80)
    
    best_idx = _select_best_fold(
        fold_metrics=fold_metrics,
        fold_val_losses=fold_val_losses,
        target_column_type=args.target_column_type
    )
    
    best_fsp = fold_predictors[best_idx]
    best_metrics = fold_metrics[best_idx]
    
    logger.info(f"✅ Selected fold {best_idx + 1} as best predictor")
    logger.info(f"   Validation loss: {fold_val_losses[best_idx]:.6f}")
    if best_metrics:
        auc = best_metrics.get('auc', None)
        if auc is not None:
            logger.info(f"   AUC: {auc:.4f}")
        accuracy = best_metrics.get('accuracy', None)
        if accuracy is not None:
            logger.info(f"   Accuracy: {accuracy:.4f}")
    
    # Update the best predictor's name to remove fold suffix
    best_fsp.name = predictor_name
    logger.info(f"   Renamed predictor to: {predictor_name}")
    
    logger.info("="*80)
    logger.info(f"✅ PROPER K-FOLD CROSS-VALIDATION COMPLETE")
    logger.info(f"   Trained {n_folds} independent predictors")
    logger.info(f"   Selected best predictor from fold {best_idx + 1}")
    logger.info("="*80)
    
    return best_fsp


def _select_best_fold(
    fold_metrics: List[Dict[str, Any]],
    fold_val_losses: List[float],
    target_column_type: str,
) -> int:
    """
    Select the best fold based on validation performance.
    
    For binary classification: Prefer highest AUC (or PR-AUC if imbalanced)
    For regression/scalar: Prefer lowest validation loss
    
    Args:
        fold_metrics: List of metrics dicts, one per fold
        fold_val_losses: List of validation losses, one per fold
        target_column_type: "set" (classification) or "scalar" (regression)
        
    Returns:
        Index of the best fold (0-based)
    """
    if target_column_type == "scalar":
        # Regression: lowest validation loss wins
        best_idx = min(range(len(fold_val_losses)), key=lambda i: fold_val_losses[i])
        logger.info(f"📊 Regression mode: Selected fold {best_idx + 1} with lowest validation loss ({fold_val_losses[best_idx]:.6f})")
        return best_idx
    
    # Classification: prefer AUC
    # Check if we have AUC metrics
    fold_aucs = []
    fold_pr_aucs = []
    
    for metrics in fold_metrics:
        auc = metrics.get('auc', None)
        pr_auc = metrics.get('pr_auc', None)  # Precision-Recall AUC (better for imbalanced)
        
        fold_aucs.append(auc if auc is not None else -1.0)
        fold_pr_aucs.append(pr_auc if pr_auc is not None and pr_auc >= 0 else -1.0)
    
    # Check if dataset is imbalanced (use PR-AUC if available and imbalanced)
    # For now, prefer PR-AUC if available, otherwise ROC-AUC
    has_pr_auc = any(pr_auc >= 0 for pr_auc in fold_pr_aucs)
    
    if has_pr_auc:
        # Use PR-AUC (better for imbalanced datasets)
        best_idx = max(range(len(fold_pr_aucs)), key=lambda i: fold_pr_aucs[i])
        best_score = fold_pr_aucs[best_idx]
        logger.info(f"📊 Classification mode (imbalanced): Selected fold {best_idx + 1} with highest PR-AUC ({best_score:.4f})")
        return best_idx
    else:
        # Use ROC-AUC
        best_idx = max(range(len(fold_aucs)), key=lambda i: fold_aucs[i])
        best_score = fold_aucs[best_idx]
        if best_score < 0:
            # Fallback to validation loss if no valid AUC
            logger.warning(f"⚠️  No valid AUC metrics found, falling back to validation loss")
            best_idx = min(range(len(fold_val_losses)), key=lambda i: fold_val_losses[i])
            logger.info(f"📊 Classification mode (fallback): Selected fold {best_idx + 1} with lowest validation loss ({fold_val_losses[best_idx]:.6f})")
        else:
            logger.info(f"📊 Classification mode: Selected fold {best_idx + 1} with highest AUC ({best_score:.4f})")
        return best_idx




