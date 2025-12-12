#!/usr/bin/env python3
"""
WeightWatcher integration for monitoring model weights during training.

This module provides functionality to track weight statistics using the 
weightwatcher package during embedding space training.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any

import weightwatcher as ww
import pandas as pd
import json
import torch

from lib.convergence_monitor import ConvergenceMonitor, clip_top_spectral_norm_layers, freeze_dominant_layers, refresh_hard_negative_sampler, detect_training_instability

logger = logging.getLogger(__name__)


def _check_model_for_none_weights(model):
    """
    Check model for None weights that would cause WeightWatcher to fail.
    
    Args:
        model: PyTorch model to check
        
    Returns:
        List of layer names with None weights
    """
    none_weight_layers = []
    
    for name, module in model.named_modules():
        if hasattr(module, 'weight') and module.weight is None:
            none_weight_layers.append(name)
        if hasattr(module, 'bias') and module.bias is None:
            # This is normal for many layers, so we don't report it
            pass
    
    return none_weight_layers


def save_weightwatcher_metrics(model, epoch: int, out_dir: str = "ww_metrics", job_id: Optional[str] = None):
    """
    Save WeightWatcher metrics for the given model and epoch.
    
    Args:
        model: PyTorch model to analyze (FeatrixTableEncoder or component)
        epoch: Current training epoch number
        out_dir: Output directory for metrics files
        job_id: Optional job ID to include in file paths
    """
    import pandas as pd

    try:
        # Create output directory - use job_id if available, otherwise save directly to out_dir
        if job_id and job_id != "unknown":
            full_out_dir = os.path.join(out_dir, job_id)
        else:
            # If job_id is missing/unknown, save directly to out_dir to avoid nested unknown dirs
            full_out_dir = out_dir
            if job_id == "unknown":
                logger.warning("⚠️ WeightWatcher received job_id='unknown' - saving to base directory")
        
        os.makedirs(full_out_dir, exist_ok=True)

        # Pick component to analyze
        if hasattr(model, 'joint_encoder'):
            analyze_model = model.joint_encoder
            model_name = "joint_encoder"
            logger.info(f"🔍 Running WeightWatcher analysis on joint_encoder for epoch {epoch}...")
        else:
            analyze_model = model
            model_name = "full_model"
            logger.info(f"🔍 Running WeightWatcher analysis for epoch {epoch}...")

        watcher = ww.WeightWatcher(model=analyze_model)

        try:
            df = watcher.analyze()
        except (AttributeError, TypeError, ValueError) as e:
            if "'NoneType' object has no attribute 'data'" in str(e) or "'NoneType' object has no attribute 'shape'" in str(e):
                logger.debug(f"🔍 WW skipping incompatible layer (has None weights): {e}")
                return False
            raise

        df["epoch"] = epoch
        df["job_id"] = job_id if job_id else "unknown"
        df["model_component"] = model_name

        # Save full JSON metrics
        output_file = os.path.join(full_out_dir, f"ww_epoch_{epoch:03d}.json")
        df.to_json(output_file, orient="records", indent=2)
        logger.info(f"✅ WW metrics saved to {output_file}")

        if df.empty:
            logger.warning("⚠️ WW DataFrame is empty.")
            return False

        # --- Extended summary statistics ---
        summary = {
            "epoch": epoch,
            "job_id": job_id,
            "model_component": model_name,
            "alpha_mean": df.get("alpha", pd.Series(dtype=float)).mean(),
            "alpha_std": df.get("alpha", pd.Series(dtype=float)).std(),
            "log_norm_mean": df.get("log_norm", pd.Series(dtype=float)).mean(),
            "spectral_norm_mean": df.get("spectral_norm", pd.Series(dtype=float)).mean(),
            "spectral_norm_top5": df.get("spectral_norm", pd.Series(dtype=float)).nlargest(5).tolist(),
            "alpha_pct_below_6": (df.get("alpha", pd.Series(dtype=float)) < 6).mean(),
            "entropy_mean": df.get("entropy", pd.Series(dtype=float)).mean(),
            "rank_loss_mean": df.get("rank_loss", pd.Series(dtype=float)).mean(),
        }

        # Log with helpful explanations
        logger.info(f"📊 WeightWatcher Analysis (Epoch {epoch}):")
        logger.info(f"   Avg α = {summary['alpha_mean']:.4f} (power-law exponent: 2-5 is good, >6 means noise-dominated)")
        logger.info(f"   σ = {summary['alpha_std']:.4f} (spectral spread: lower is more stable)")
        logger.info(f"   log∥W∥ = {summary['log_norm_mean']:.4f} (weight magnitude: gives sense of layer 'energy')")
        logger.info(f"   SN = {summary['spectral_norm_mean']:.4f} (stable rank: 2-4 typical, higher = more redundancy)")
        logger.info(f"   α < 6 = {summary['alpha_pct_below_6']:.2%} (well-behaved layers: aim for 80-90%)")
        
        # Add interpretation based on values
        if summary['alpha_pct_below_6'] < 0.6:
            logger.warning(f"   ⚠️ Only {summary['alpha_pct_below_6']:.0%} of layers are learning well - consider reducing LR or adding regularization")
        elif summary['alpha_pct_below_6'] < 0.7:
            logger.info(f"   💡 {summary['alpha_pct_below_6']:.0%} of layers learning - room for improvement")
        elif summary['alpha_pct_below_6'] < 0.85:
            logger.info(f"   ✅ {summary['alpha_pct_below_6']:.0%} of layers learning well - good progress")
        else:
            logger.info(f"   🎉 {summary['alpha_pct_below_6']:.0%} of layers learning well - excellent convergence")
        
        if summary['alpha_mean'] > 6:
            logger.info(f"   💡 High avg α ({summary['alpha_mean']:.2f}) suggests many layers in noise regime")

        # Save summary CSV
        summary_csv = os.path.join(full_out_dir, "ww_summary.csv")
        df_summary = pd.DataFrame([summary])
        if os.path.exists(summary_csv):
            df_summary.to_csv(summary_csv, mode="a", header=False, index=False)
        else:
            df_summary.to_csv(summary_csv, index=False)

        return True

    except Exception as e:
        logger.error(f"❌ WW analysis failed for epoch {epoch}: {e}")
        logger.error(f"   Model type: {type(model)}")
        logger.error(f"   Output dir: {out_dir}")
        return False


def create_weightwatcher_summary(out_dir: str = "ww_metrics", job_id: Optional[str] = None):
    """
    Create a summary of all WeightWatcher metrics across epochs.
    
    Args:
        out_dir: Directory containing metric files
        job_id: Optional job ID for file paths
    """

    
    try:
        # Find all metric files
        if job_id:
            full_out_dir = os.path.join(out_dir, job_id)
        else:
            full_out_dir = out_dir
            
        metric_files = list(Path(full_out_dir).glob("ww_epoch_*.json"))
        
        if not metric_files:
            logger.warning(f"No WeightWatcher metric files found in {full_out_dir}")
            return None
        
        # Load and combine all metrics
        all_metrics = []
        for file_path in sorted(metric_files):
            try:
                df = pd.read_json(file_path)
                all_metrics.append(df)
            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {e}")
        
        if not all_metrics:
            return None
            
        # Combine into single DataFrame
        combined_df = pd.concat(all_metrics, ignore_index=True)
        
        # Save summary
        summary_file = os.path.join(full_out_dir, "ww_summary.json")
        combined_df.to_json(summary_file, orient="records", indent=2)
        
        logger.info(f"📊 WeightWatcher summary saved to {summary_file}")
        logger.info(f"   Combined {len(all_metrics)} epoch files with {len(combined_df)} total layer measurements")
        
        return combined_df
        
    except Exception as e:
        logger.error(f"❌ Failed to create WeightWatcher summary: {e}")
        return None


class WeightWatcherCallback:
    """
    Callback class for integrating WeightWatcher into training loops with convergence monitoring.
    """
    
    def __init__(self, out_dir: str = "ww_metrics", job_id: Optional[str] = None, save_every: int = 1, 
                 convergence_patience: int = 5, convergence_min_improve: float = 1e-4,
                 spectral_norm_clip: Optional[float] = 12.0, freeze_threshold: Optional[float] = None,
                 min_epoch_before_freeze: int = 20, max_layers_to_freeze: int = 5,
                 max_freeze_percentage: float = 0.1, enable_layer_freezing: bool = False):
        """
        Initialize WeightWatcher callback with convergence monitoring.
        
        Args:
            out_dir: Output directory for metrics
            job_id: Job ID for file organization
            save_every: Save metrics every N epochs (default: every epoch)
            convergence_patience: Epochs to wait for improvement before stopping
            convergence_min_improve: Minimum improvement threshold
            spectral_norm_clip: Maximum spectral norm before clipping (None to disable clipping)
            freeze_threshold: Spectral norm threshold for freezing layers (None = use default 15.0)
            min_epoch_before_freeze: Minimum epoch before allowing layer freezing (default: 20)
            max_layers_to_freeze: Maximum number of layers to freeze per epoch (default: 5)
            max_freeze_percentage: Maximum percentage of model parameters to freeze (default: 0.1 = 10%)
            enable_layer_freezing: Enable automatic layer freezing (default: False - DISABLED)
                                  Layer freezing can cause issues by freezing adaptive parameters
                                  and has been found to be overly aggressive in embedding space training.
        """
        self.out_dir = out_dir
        self.job_id = job_id
        self.save_every = save_every
        self.epoch_count = 0
        self.spectral_norm_clip = spectral_norm_clip
        self.freeze_threshold = freeze_threshold if freeze_threshold is not None else 15.0
        self.min_epoch_before_freeze = min_epoch_before_freeze
        self.max_layers_to_freeze = max_layers_to_freeze
        self.max_freeze_percentage = max_freeze_percentage
        self.enable_layer_freezing = enable_layer_freezing
        
        # Track if we've saved the "would freeze" checkpoint
        self._would_freeze_checkpoint_saved = False
        
        # Diagnostic tracking for repeated clipping
        self.layer_clip_counts = {}  # layer_name -> count of times clipped
        self.layer_clip_history = {}  # layer_name -> list of epochs when clipped
        self.total_epochs_processed = 0
        
        # Initialize convergence monitor
        self.convergence_monitor = ConvergenceMonitor(
            patience=convergence_patience,
            min_improve=convergence_min_improve
        )
        
        self.has_converged = False
        self.convergence_epoch = None
        
        logger.info(f"🔍 WeightWatcher callback initialized:")
        logger.info(f"   Saving every {save_every} epochs to {out_dir}")
        logger.info(f"   Convergence patience: {convergence_patience}")
        if spectral_norm_clip is not None:
            logger.info(f"   Spectral norm clip: {spectral_norm_clip}")
        else:
            logger.info(f"   Spectral norm clip: DISABLED")
        logger.info(f"   Freeze threshold: {freeze_threshold}")
        logger.info(f"   Min epoch before freeze: {min_epoch_before_freeze}")
        logger.info(f"   Max layers to freeze per epoch: {max_layers_to_freeze}")
        logger.info(f"   Max freeze percentage: {max_freeze_percentage:.1%}")
        logger.info(f"   🔧 Diagnostic: Tracking repeated layer clipping")
    
    def __call__(self, model, epoch: int):
        """
        Call the callback with model and epoch, including convergence monitoring and instability detection.
        
        Args:
            model: PyTorch model to analyze
            epoch: Current epoch number
            
        Returns:
            dict: Contains convergence status and any interventions applied
        """
        result = {
            'should_stop': False,
            'converged': False,
            'clipped_layers': [],
            'frozen_layers': [],
            'refreshed_sampler': False,
            'instability_detected': False,
            'emergency_actions_taken': []
        }
        
        # FIRST: Check for training instability before doing anything else
        try:
            instability_report = detect_training_instability(model, epoch)
            
            if instability_report['is_unstable']:
                result['instability_detected'] = True
                
                logger.error(f"🚨 TRAINING INSTABILITY DETECTED at epoch {epoch}")
                logger.error(f"   Severity: {instability_report['severity']}")
                logger.error(f"   Issues found: {len(instability_report['issues'])}")
                
                for issue in instability_report['issues']:
                    logger.error(f"   • {issue}")
                
                # Take emergency actions for critical instability
                if instability_report['severity'] == 'critical':
                    logger.error("🆘 CRITICAL INSTABILITY - TAKING EMERGENCY ACTIONS")
                    
                    # Emergency stabilization
                    emergency_clipped = clip_top_spectral_norm_layers(model, max_norm=1.0)  # Very aggressive clipping
                    result['clipped_layers'] = emergency_clipped
                    result['emergency_actions_taken'].append(f"Emergency clipping: {len(emergency_clipped)} layers")
                    
                    # Try to freeze problematic layers immediately
                    emergency_frozen = freeze_dominant_layers(model, norm_threshold=2.0, max_layers_to_freeze=10, max_param_percentage=0.3)
                    result['frozen_layers'] = emergency_frozen
                    result['emergency_actions_taken'].append(f"Emergency freezing: {len(emergency_frozen)} layers")
                    
                    # Recommend stopping training
                    result['should_stop'] = True
                    logger.error("🛑 RECOMMENDING IMMEDIATE TRAINING STOP")
                    logger.error("   Model state is critically unstable")
                    
                    for action in instability_report['emergency_actions']:
                        logger.error(f"   REQUIRED: {action}")
                    
                    for rec in instability_report['recommendations']:
                        logger.error(f"   RECOMMEND: {rec}")
                    
                    return result  # Return early for critical cases
                    
                elif instability_report['severity'] == 'high':
                    logger.warning("⚠️ HIGH INSTABILITY - APPLYING INTERVENTIONS")
                    
                    # More aggressive than normal clipping
                    aggressive_clipped = clip_top_spectral_norm_layers(model, max_norm=3.0)
                    result['clipped_layers'] = aggressive_clipped
                    result['emergency_actions_taken'].append(f"Aggressive clipping: {len(aggressive_clipped)} layers")
                    
                    # Log recommendations
                    for rec in instability_report['recommendations']:
                        logger.warning(f"   RECOMMEND: {rec}")
                        
                elif instability_report['severity'] == 'moderate':
                    logger.info("⚠️ MODERATE INSTABILITY - MONITORING CLOSELY")
                    for rec in instability_report['recommendations']:
                        logger.info(f"   SUGGEST: {rec}")
                    
        except Exception as e:
            logger.error(f"Failed to detect instability: {e}")
        
        # Apply standard spectral norm clipping (if not already done in emergency mode and if enabled)
        if not result['emergency_actions_taken']:
            if self.spectral_norm_clip is not None:
                clipped_layers = clip_top_spectral_norm_layers(model, max_norm=self.spectral_norm_clip)
                result['clipped_layers'] = clipped_layers
            else:
                # Clipping is disabled
                result['clipped_layers'] = []
        
        # Track clipped layers for diagnostic purposes
        self.total_epochs_processed += 1
        for layer_name, old_norm, new_norm in result['clipped_layers']:
            # Update clip counts
            self.layer_clip_counts[layer_name] = self.layer_clip_counts.get(layer_name, 0) + 1
            
            # Update clip history
            if layer_name not in self.layer_clip_history:
                self.layer_clip_history[layer_name] = []
            self.layer_clip_history[layer_name].append(epoch)
        
        # Diagnostic reporting for problematic layers
        if epoch > 0 and epoch % 20 == 0:  # Report every 20 epochs
            self._report_clipping_diagnostics(epoch)
        
        # Check if we should save WeightWatcher metrics this epoch
        should_analyze = (epoch % self.save_every) == 0 or epoch == 0
        
        if should_analyze:
            # Run WeightWatcher analysis
            success = save_weightwatcher_metrics(
                model=model,
                epoch=epoch,
                out_dir=self.out_dir,
                job_id=self.job_id
            )
            
            if success:
                # Load the metrics we just saved for convergence monitoring
                metrics = self._load_latest_metrics()
                
                if metrics:
                    # Check convergence with enhanced signals
                    
                    # Determine if no layers are available for freezing (key convergence signal)
                    no_freeze_candidates = False
                    if epoch >= self.min_epoch_before_freeze:
                        # Check if any layers exceed freeze threshold
                        layers_above_threshold = []
                        all_spectral_norms = []  # Collect all spectral norms for distribution
                        for name, module in model.named_modules():
                            if hasattr(module, "weight") and module.weight is not None and module.weight.ndim >= 2:
                                if not module.weight.requires_grad:
                                    continue  # Skip already frozen layers
                                try:
                                    W = module.weight
                                    s = torch.linalg.svdvals(W)
                                    top_s = s[0].item()  # Convert to Python float
                                    all_spectral_norms.append((name, top_s))
                                    if top_s > self.freeze_threshold:
                                        layers_above_threshold.append(name)
                                except:
                                    pass
                        
                        no_freeze_candidates = len(layers_above_threshold) == 0
                        if no_freeze_candidates:
                            # Print distribution of spectral norms
                            if all_spectral_norms:
                                # Sort by spectral norm descending
                                all_spectral_norms.sort(key=lambda x: x[1], reverse=True)
                                spectral_values = [norm for _, norm in all_spectral_norms]
                                
                                # Calculate statistics
                                max_norm = max(spectral_values)
                                min_norm = min(spectral_values)
                                mean_norm = sum(spectral_values) / len(spectral_values)
                                
                                # Show top 10 layers and distribution
                                logger.info(f"🧊 No layers exceed freeze threshold ({self.freeze_threshold}) - freeze candidates exhausted")
                                logger.info(f"   Spectral norm distribution: max={max_norm:.2f}, min={min_norm:.2f}, mean={mean_norm:.2f}, count={len(spectral_values)}")
                                logger.info(f"   Top 10 spectral norms:")
                                for i, (name, norm) in enumerate(all_spectral_norms[:10], 1):
                                    logger.info(f"      {i:2d}. {name[:60]:60s} = {norm:.2f}")
                                
                                # Show distribution buckets
                                buckets = [0, 5, 10, 12, 15, 20, 30, float('inf')]
                                bucket_counts = [0] * (len(buckets) - 1)
                                for norm in spectral_values:
                                    for i in range(len(buckets) - 1):
                                        if buckets[i] <= norm < buckets[i + 1]:
                                            bucket_counts[i] += 1
                                            break
                                
                                logger.info(f"   Distribution by range:")
                                for i in range(len(buckets) - 1):
                                    if buckets[i + 1] == float('inf'):
                                        range_str = f">={buckets[i]:.0f}"
                                    else:
                                        range_str = f"{buckets[i]:.0f}-{buckets[i+1]:.0f}"
                                    logger.info(f"      {range_str:>8s}: {bucket_counts[i]:3d} layers")
                            else:
                                logger.info(f"🧊 No layers exceed freeze threshold ({self.freeze_threshold}) - no valid layers found")
                    
                    converged = self.convergence_monitor.update(epoch, metrics, no_freeze_candidates)
                    result['converged'] = converged
                    
                    # Don't stop on convergence if we have instability
                    if converged and not result['instability_detected']:
                        result['should_stop'] = True
                    elif converged and result['instability_detected']:
                        logger.warning("⚠️ Convergence detected but instability present - continuing training")
                        result['should_stop'] = False
                    
                    if converged and not self.has_converged:
                        self.has_converged = True
                        self.convergence_epoch = epoch
                        logger.info(f"🎯 Training converged at epoch {epoch} - early stopping recommended")
                    
                    # Apply additional interventions based on metrics
                    rank_loss = metrics.get('rank_loss_mean', 1.0)
                    
                    # Refresh hard negative sampling if rank loss is very low
                    if rank_loss < 0.001 and epoch > 20:
                        print(f"@@@@ NOT IMPLEMENTED: Refreshing hard negative sampler: rank_loss = {rank_loss}")
                        # refresh_hard_negative_sampler()
                        result['refreshed_sampler'] = True
                    
                    # LAYER FREEZING: Only if explicitly enabled (disabled by default)
                    # Layer freezing was found to be too aggressive and froze adaptive parameters
                    if self.enable_layer_freezing and epoch >= self.min_epoch_before_freeze and not result['emergency_actions_taken']:
                        frozen_layers = freeze_dominant_layers(model, norm_threshold=self.freeze_threshold,
                                                               max_layers_to_freeze=self.max_layers_to_freeze,
                                                               max_param_percentage=self.max_freeze_percentage)
                        if not result['frozen_layers']:  # Only if we didn't already freeze in emergency mode
                            result['frozen_layers'] = frozen_layers
                        
                        # Track layer changes for convergence detection
                        if frozen_layers:
                            logger.info(f"🏗️  Model structure still adapting - {len(frozen_layers)} layers frozen")
                            # If layers are still being frozen, the model is still adapting
                            # We should be more conservative about calling it "converged"
                            self.convergence_monitor.epochs_without_improvement = max(0, 
                                self.convergence_monitor.epochs_without_improvement - 1)
                    elif not self.enable_layer_freezing and epoch >= self.min_epoch_before_freeze:
                        # Layer freezing is disabled, but check if we WOULD freeze layers
                        # Save a checkpoint the first time we would have frozen something
                        if not self._would_freeze_checkpoint_saved and epoch >= self.min_epoch_before_freeze:
                            # Check if any layers exceed the threshold (simulate freeze_dominant_layers)
                            layers_that_would_freeze = []
                            for name, module in model.named_modules():
                                if hasattr(module, "weight") and module.weight is not None and module.weight.ndim >= 2:
                                    try:
                                        # Skip adaptive parameter modules
                                        from lib.convergence_monitor import _has_adaptive_parameters
                                        if _has_adaptive_parameters(module):
                                            continue
                                        
                                        # Check if already frozen
                                        module_params_list = list(module.parameters())
                                        if module_params_list:
                                            all_frozen = all(not p.requires_grad for p in module_params_list if p is not None)
                                            if all_frozen:
                                                continue
                                        
                                        # Compute spectral norm
                                        W = module.weight
                                        s = torch.linalg.svdvals(W)
                                        top_s = s[0].item()
                                        
                                        if top_s > self.freeze_threshold:
                                            layers_that_would_freeze.append((name, top_s))
                                    except:
                                        pass
                            
                            if layers_that_would_freeze:
                                # We WOULD freeze layers at this point - save a checkpoint!
                                logger.warning(f"📸 WOULD_FREEZE checkpoint opportunity at epoch {epoch}!")
                                logger.warning(f"   🧊 {len(layers_that_would_freeze)} layers exceed freeze threshold ({self.freeze_threshold})")
                                logger.warning(f"   ⚡ Saving checkpoint to enable future 'what-if' experiments with freezing")
                                
                                # Show top layers that would be frozen
                                layers_that_would_freeze.sort(key=lambda x: x[1], reverse=True)
                                for i, (name, norm) in enumerate(layers_that_would_freeze[:5], 1):
                                    logger.info(f"      {i}. {name[:60]:60s} = {norm:.2f}")
                                if len(layers_that_would_freeze) > 5:
                                    logger.info(f"      ... and {len(layers_that_would_freeze) - 5} more")
                                
                                # Signal to save checkpoint
                                result['save_would_freeze_checkpoint'] = True
                                result['would_freeze_layer_count'] = len(layers_that_would_freeze)
                                result['would_freeze_layers'] = layers_that_would_freeze
                                self._would_freeze_checkpoint_saved = True
                        
                        # Log once that layer freezing is disabled (at first opportunity)
                        if epoch == self.min_epoch_before_freeze:
                            logger.info(f"🔓 Layer freezing DISABLED - adaptive parameters will continue learning throughout training")
                        
                        if not result['frozen_layers']:
                            result['frozen_layers'] = []
                    else:
                        # Not freezing layers this epoch
                        if not result['frozen_layers']:
                            result['frozen_layers'] = []
                
                # Add layer change counts to metrics for convergence tracking
                enhanced_metrics = metrics.copy() if metrics else {}
                enhanced_metrics['num_layers_clipped'] = len(result['clipped_layers'])
                enhanced_metrics['num_layers_frozen'] = len(result.get('frozen_layers', []))
                enhanced_metrics['layers_still_adapting'] = len(result['clipped_layers']) > 0 or len(result.get('frozen_layers', [])) > 0
                enhanced_metrics['no_freeze_candidates'] = locals().get('no_freeze_candidates', False)
                enhanced_metrics['instability_detected'] = result['instability_detected']
                
                # Re-check convergence with enhanced metrics - instability overrides convergence
                if enhanced_metrics.get('instability_detected', False):
                    logger.debug(f"🚨 Instability detected - ignoring convergence signals")
                    result['should_stop'] = result.get('instability_detected', False) and instability_report.get('severity') == 'critical'
                elif enhanced_metrics.get('layers_still_adapting', False):
                    logger.debug(f"🏗️  Layers still adapting (clipped: {enhanced_metrics['num_layers_clipped']}, frozen: {enhanced_metrics['num_layers_frozen']}) - delaying convergence")
                    result['should_stop'] = False  # Don't stop if architecture is still changing
        
        return result
    
    def _report_clipping_diagnostics(self, epoch: int):
        """Report diagnostic information about layers that are being clipped repeatedly."""
        if not self.layer_clip_counts:
            return
        
        # Find layers that have been clipped multiple times
        frequently_clipped = {name: count for name, count in self.layer_clip_counts.items() if count >= 5}
        
        if frequently_clipped:
            logger.warning(f"🔧 CLIPPING DIAGNOSTICS at epoch {epoch}:")
            logger.warning(f"   Total epochs processed: {self.total_epochs_processed}")
            logger.warning(f"   Layers clipped ≥5 times: {len(frequently_clipped)}")
            
            # Sort by clip frequency
            sorted_clipped = sorted(frequently_clipped.items(), key=lambda x: x[1], reverse=True)
            
            for layer_name, clip_count in sorted_clipped[:5]:  # Show top 5
                clip_rate = clip_count / self.total_epochs_processed
                recent_clips = [e for e in self.layer_clip_history.get(layer_name, []) if e >= epoch - 10]
                logger.warning(f"   • {layer_name}: {clip_count} clips ({clip_rate:.1%} rate), recent: {len(recent_clips)}/10 epochs")
            
            # Alert for chronic instability
            chronic_layers = [name for name, count in frequently_clipped.items() if count > self.total_epochs_processed * 0.5]
            if chronic_layers:
                logger.error(f"🚨 CHRONIC INSTABILITY: {len(chronic_layers)} layers clipped >50% of epochs")
                logger.error(f"   Affected layers: {chronic_layers[:3]}{'...' if len(chronic_layers) > 3 else ''}")
                logger.error(f"   Consider: Reduce learning rate by 10x, add weight decay, or reinitialize model")
    
    def _load_latest_metrics(self) -> Optional[Dict[str, Any]]:
        """Load the most recently saved metrics for convergence monitoring."""
        try:
            # Determine the correct directory
            if self.job_id and self.job_id != "unknown":
                full_out_dir = os.path.join(self.out_dir, self.job_id)
            else:
                full_out_dir = self.out_dir
            
            # Find the most recent summary CSV
            summary_csv = os.path.join(full_out_dir, "ww_summary.csv")
            
            if os.path.exists(summary_csv):
                df = pd.read_csv(summary_csv)
                if not df.empty:
                    # Return the most recent row as a dict
                    return df.iloc[-1].to_dict()
        
        except Exception as e:
            logger.warning(f"Failed to load latest metrics for convergence monitoring: {e}")
        
        return None
    
    def get_convergence_status(self) -> Dict[str, Any]:
        """Get current convergence status."""
        status = self.convergence_monitor.get_status()
        status.update({
            'has_converged': self.has_converged,
            'convergence_epoch': self.convergence_epoch,
            'spectral_norm_clip': self.spectral_norm_clip,
            'freeze_threshold': self.freeze_threshold
        })
        return status
    
    def finalize(self):
        """
        Create final summary after training completion.
        """
        logger.info("📊 Creating final WeightWatcher summary...")
        
        # Generate clipping diagnostics summary
        clipping_summary = self.get_clipping_summary()
        if clipping_summary:
            logger.info("🔧 Final Clipping Diagnostics Summary:")
            logger.info(f"   Total epochs processed: {clipping_summary['total_epochs_processed']}")
            logger.info(f"   Layers that required clipping: {clipping_summary['layers_clipped_count']}")
            
            if clipping_summary['problematic_layers']:
                logger.warning(f"⚠️  Problematic layers (clipped >50% of time):")
                for layer_name in clipping_summary['problematic_layers'][:5]:
                    freq = clipping_summary['layer_frequencies'][layer_name]
                    count = clipping_summary['layer_clip_counts'][layer_name]
                    logger.warning(f"     {layer_name}: {count} times ({freq:.1%}) - consider structural changes")
            
            if clipping_summary['most_clipped_layer']:
                most_clipped_name, most_clipped_count = clipping_summary['most_clipped_layer']
                freq = clipping_summary['layer_frequencies'][most_clipped_name]
                logger.info(f"   Most clipped layer: {most_clipped_name} ({most_clipped_count} times, {freq:.1%})")
            
            # Save clipping diagnostics to file
            try:
                if self.job_id and self.job_id != "unknown":
                    full_out_dir = os.path.join(self.out_dir, self.job_id)
                else:
                    full_out_dir = self.out_dir
                
                os.makedirs(full_out_dir, exist_ok=True)
                clipping_file = os.path.join(full_out_dir, "clipping_diagnostics.json")
                with open(clipping_file, 'w') as f:
                    json.dump(clipping_summary, f, indent=2)
                logger.info(f"🔧 Clipping diagnostics saved to {clipping_file}")
            except Exception as e:
                logger.warning(f"Failed to save clipping diagnostics: {e}")
        
        return create_weightwatcher_summary(
            out_dir=self.out_dir,
            job_id=self.job_id
        )

    def get_clipping_summary(self) -> Dict[str, Any]:
        """Get a summary of layer clipping patterns for final reporting."""
        if not self.layer_clip_counts:
            return {}
        
        # Calculate frequencies
        layer_frequencies = {
            name: count / self.total_epochs_processed 
            for name, count in self.layer_clip_counts.items()
        }
        
        # Find problematic layers
        problematic = [
            name for name, freq in layer_frequencies.items() 
            if freq > 0.5
        ]
        
        return {
            'total_epochs_processed': self.total_epochs_processed,
            'layers_clipped_count': len(self.layer_clip_counts),
            'layer_clip_counts': dict(self.layer_clip_counts),
            'layer_frequencies': layer_frequencies,
            'problematic_layers': problematic,
            'most_clipped_layer': max(self.layer_clip_counts.items(), key=lambda x: x[1]) if self.layer_clip_counts else None
        }


def plot_convergence_dashboard(out_dir: str = "ww_metrics", job_id: Optional[str] = None, 
                              save_plot: bool = True, show_plot: bool = False):
    """
    Create a convergence dashboard visualization from WeightWatcher logs.
    
    Designed for headless server environments - uses Agg backend and saves to file.
    
    Args:
        out_dir: Directory containing WW metrics
        job_id: Job ID for file organization
        save_plot: Whether to save the plot to file (default: True)
        show_plot: Whether to display the plot (default: False for server compatibility)
        
    Returns:
        matplotlib figure object or None
    """
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use headless backend for server environments without X11
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Find metrics directory
        if job_id and job_id != "unknown":
            full_out_dir = os.path.join(out_dir, job_id)
        else:
            full_out_dir = out_dir
            
        # Load summary CSV
        summary_csv = os.path.join(full_out_dir, "ww_summary.csv")
        if not os.path.exists(summary_csv):
            logger.warning(f"No summary CSV found at {summary_csv}")
            return None
            
        df = pd.read_csv(summary_csv)
        if df.empty:
            logger.warning("Summary CSV is empty")
            return None
        
        # Create dashboard with subplots
        fig, axes = plt.subplots(2, 3, figsize=(20, 10))
        fig.suptitle(f'Convergence Dashboard - {job_id or "Training Session"}', fontsize=16)
        
        # Plot 1: Rank Loss over time
        axes[0, 0].plot(df['epoch'], df['rank_loss_mean'], 'b-', linewidth=2, label='Rank Loss')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Rank Loss Mean')
        axes[0, 0].set_title('Rank Loss Convergence')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].legend()
        
        # Plot 2: Alpha Mean over time
        axes[0, 1].plot(df['epoch'], df['alpha_mean'], 'g-', linewidth=2, label='Alpha Mean')
        axes[0, 1].axhline(y=6, color='r', linestyle='--', alpha=0.5, label='Alpha=6 threshold')
        
        # Add α<6% proportion if available
        if 'alpha_pct_below_6' in df.columns:
            ax2_alpha = axes[0, 1].twinx()
            ax2_alpha.plot(df['epoch'], df['alpha_pct_below_6'] * 100, 'b--', linewidth=1.5, alpha=0.7, label='α<6% (%)')
            ax2_alpha.set_ylabel('α<6% Percentage', color='b')
            ax2_alpha.legend(loc='lower right')
        
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Alpha Mean')
        axes[0, 1].set_title('Alpha Parameter & Meaningful Directions')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend(loc='upper left')
        
        # Plot 3: Spectral Norm and layer changes
        axes[0, 2].plot(df['epoch'], df['spectral_norm_mean'], 'purple', linewidth=2, label='Spectral Norm Mean')
        if 'num_layers_clipped' in df.columns:
            ax2 = axes[0, 2].twinx()
            ax2.bar(df['epoch'], df['num_layers_clipped'], alpha=0.3, color='orange', label='Layers Clipped')
            ax2.set_ylabel('Layers Clipped')
            ax2.legend(loc='upper right')
        axes[0, 2].set_xlabel('Epoch')
        axes[0, 2].set_ylabel('Spectral Norm Mean')
        axes[0, 2].set_title('Spectral Norms & Layer Changes')
        axes[0, 2].grid(True, alpha=0.3)
        axes[0, 2].legend(loc='upper left')
        
        # Plot 4: Entropy and convergence indicators
        axes[1, 0].plot(df['epoch'], df['entropy_mean'], 'orange', linewidth=2, label='Entropy Mean')
        if 'num_layers_frozen' in df.columns and df['num_layers_frozen'].sum() > 0:
            frozen_epochs = df[df['num_layers_frozen'] > 0]['epoch']
            frozen_counts = df[df['num_layers_frozen'] > 0]['num_layers_frozen']
            axes[1, 0].scatter(frozen_epochs, [axes[1, 0].get_ylim()[1] * 0.9] * len(frozen_epochs), 
                              c='red', s=frozen_counts*20, alpha=0.6, label='Layers Frozen')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Entropy Mean')
        axes[1, 0].set_title('Entropy & Layer Freezing')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend()
        
        # Plot 5: Layer Clipping Frequency Histogram
        try:
            clipping_file = os.path.join(full_out_dir, "clipping_diagnostics.json")
            if os.path.exists(clipping_file):
                with open(clipping_file, 'r') as f:
                    clipping_data = json.load(f)
                
                if clipping_data.get('layer_frequencies'):
                    frequencies = list(clipping_data['layer_frequencies'].values())
                    layer_names = list(clipping_data['layer_frequencies'].keys())
                    
                    # Create histogram of clipping frequencies
                    axes[1, 1].hist(frequencies, bins=20, alpha=0.7, color='coral', edgecolor='black')
                    axes[1, 1].axvline(x=0.5, color='red', linestyle='--', alpha=0.7, label='50% threshold')
                    axes[1, 1].set_xlabel('Clipping Frequency')
                    axes[1, 1].set_ylabel('Number of Layers')
                    axes[1, 1].set_title('Layer Clipping Frequency Distribution')
                    axes[1, 1].grid(True, alpha=0.3)
                    axes[1, 1].legend()
                    
                    # Annotate problematic layers
                    problematic_count = len([f for f in frequencies if f > 0.5])
                    if problematic_count > 0:
                        axes[1, 1].text(0.6, max(axes[1, 1].get_ylim()) * 0.8, 
                                        f'{problematic_count} layers\n>50% clipped', 
                                        bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
                else:
                    axes[1, 1].text(0.5, 0.5, 'No clipping data\navailable', 
                                   transform=axes[1, 1].transAxes, ha='center', va='center')
                    axes[1, 1].set_title('Layer Clipping Frequency')
            else:
                axes[1, 1].text(0.5, 0.5, 'Clipping diagnostics\nnot found', 
                               transform=axes[1, 1].transAxes, ha='center', va='center')
                axes[1, 1].set_title('Layer Clipping Frequency')
        except Exception as e:
            axes[1, 1].text(0.5, 0.5, f'Error loading\nclipping data:\n{str(e)[:30]}...', 
                           transform=axes[1, 1].transAxes, ha='center', va='center')
            axes[1, 1].set_title('Layer Clipping Frequency')
        
        # Plot 6: Training Progress Summary
        axes[1, 2].text(0.1, 0.9, f"Training Summary", transform=axes[1, 2].transAxes, 
                        fontsize=14, fontweight='bold')
        
        summary_text = f"Training Summary:\n"
        summary_text += f"Total Epochs: {df['epoch'].max()}\n"
        summary_text += f"Final Rank Loss: {df['rank_loss_mean'].iloc[-1]:.6f}\n"
        summary_text += f"Final Alpha: {df['alpha_mean'].iloc[-1]:.2f}\n"
        if 'alpha_pct_below_6' in df.columns:
            summary_text += f"Final α<6%: {df['alpha_pct_below_6'].iloc[-1]:.1%}\n"
        summary_text += f"Avg Spectral Norm: {df['spectral_norm_mean'].mean():.2f}\n"
        
        # Add convergence threshold info
        final_epoch = df['epoch'].max()
        if final_epoch > 60:
            alpha_threshold = 0.07
        elif final_epoch > 40:
            alpha_threshold = 0.05
        else:
            alpha_threshold = 0.03
        summary_text += f"\nConvergence Info:\n"
        summary_text += f"Dynamic α threshold: {alpha_threshold:.2f}\n"
        
        try:
            clipping_file = os.path.join(full_out_dir, "clipping_diagnostics.json")
            if os.path.exists(clipping_file):
                with open(clipping_file, 'r') as f:
                    clipping_data = json.load(f)
                summary_text += f"\nClipping Stats:\n"
                summary_text += f"Layers clipped: {clipping_data.get('layers_clipped_count', 0)}\n"
                if clipping_data.get('problematic_layers'):
                    summary_text += f"Problematic layers: {len(clipping_data['problematic_layers'])}\n"
                if clipping_data.get('most_clipped_layer'):
                    name, count = clipping_data['most_clipped_layer']
                    freq = clipping_data['layer_frequencies'][name]
                    summary_text += f"Most clipped: {freq:.1%}\n"
        except:
            pass
        
        axes[1, 2].text(0.1, 0.7, summary_text, transform=axes[1, 2].transAxes, 
                        fontsize=10, verticalalignment='top', fontfamily='monospace')
        axes[1, 2].set_xlim(0, 1)
        axes[1, 2].set_ylim(0, 1)
        axes[1, 2].axis('off')
        axes[1, 2].set_title('Summary Statistics')
        
        plt.tight_layout()
        
        # Save plot if requested
        if save_plot:
            plot_path = os.path.join(full_out_dir, "convergence_dashboard.png")
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            logger.info(f"📈 Convergence dashboard saved to {plot_path}")
        
        # Show plot if requested (not recommended for server environments)
        if show_plot:
            try:
                plt.show()
            except Exception as e:
                logger.warning(f"Failed to display plot (running on server without display?): {e}")
        
        # Close figure to free memory if we saved it
        if save_plot and not show_plot:
            plt.close(fig)
            return None  # Figure is closed, don't return it
        
        return fig
        
    except ImportError:
        logger.warning("matplotlib not available - cannot create convergence dashboard")
        return None
    except Exception as e:
        logger.error(f"Failed to create convergence dashboard: {e}")
        return None 