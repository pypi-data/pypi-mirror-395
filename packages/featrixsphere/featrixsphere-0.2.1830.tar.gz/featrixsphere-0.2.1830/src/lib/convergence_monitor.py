#!/usr/bin/env python3
"""
Convergence monitoring for neural network training using WeightWatcher metrics.
"""

import logging
import torch
import torch.nn
import numpy as np
from typing import Optional, Dict, Any, List, Tuple
import math

logger = logging.getLogger(__name__)


class ConvergenceMonitor:
    """
    Monitor training convergence using WeightWatcher metrics.
    
    Tracks rank_loss, alpha_mean, and entropy_mean over a sliding window
    to detect when the model has converged and training should stop.
    """
    
    def __init__(self, patience: int = 5, min_improve: float = 1e-4):
        self.patience = patience
        self.min_improve = min_improve
        
        # Sliding windows for metrics
        self.rank_loss_window = []
        self.alpha_window = []
        self.entropy_window = []
        self.alpha_lt6_window = []  # Track α<6% proportion for meaningful directions
        
        # Convergence tracking
        self.epochs_without_improvement = 0
        self.best_rank_loss = float('inf')
        
        logger.info(f"🔍 ConvergenceMonitor initialized: patience={patience}, min_improve={min_improve}")
        logger.info(f"   Enhanced with α<6% tracking and dynamic thresholds")
    
    def update(self, epoch: int, ww_metrics: Dict[str, Any], no_freeze_candidates: bool = False) -> bool:
        """
        Update convergence monitor with WeightWatcher metrics.
        
        Args:
            epoch: Current training epoch
            ww_metrics: Dictionary containing WeightWatcher analysis results
            no_freeze_candidates: True if no layers remain available for freezing
            
        Returns:
            bool: True if training should stop (converged), False otherwise
        """
        
        # Extract key metrics
        rank_loss = ww_metrics.get('rank_loss_mean', 0.0)
        alpha_mean = ww_metrics.get('alpha_mean', 0.0)
        entropy_mean = ww_metrics.get('entropy_mean', 0.0)
        alpha_lt6_pct = ww_metrics.get('alpha_pct_below_6', 0.0)  # Proportion of meaningful directions
        
        # Handle None values gracefully
        rank_loss = rank_loss if rank_loss is not None else 0.0
        alpha_mean = alpha_mean if alpha_mean is not None else 0.0
        entropy_mean = entropy_mean if entropy_mean is not None else 0.0
        alpha_lt6_pct = alpha_lt6_pct if alpha_lt6_pct is not None else 0.0
        
        # Add to sliding windows
        self.rank_loss_window.append(rank_loss)
        self.alpha_window.append(alpha_mean)
        self.entropy_window.append(entropy_mean)
        self.alpha_lt6_window.append(alpha_lt6_pct)
        
        # Maintain window size
        if len(self.rank_loss_window) > self.patience:
            self.rank_loss_window.pop(0)
            self.alpha_window.pop(0)
            self.entropy_window.pop(0)
            self.alpha_lt6_window.pop(0)
        
        # Check for improvement in rank_loss (primary metric)
        if rank_loss < self.best_rank_loss - self.min_improve:
            self.best_rank_loss = rank_loss
            self.epochs_without_improvement = 0
            logger.debug(f"📈 Epoch {epoch}: New best rank_loss: {rank_loss:.6f}")
        else:
            self.epochs_without_improvement += 1
        
        # Check convergence conditions only if we have enough history
        if len(self.rank_loss_window) >= self.patience:
            converged = self._check_convergence(epoch, no_freeze_candidates)
            if converged:
                logger.info(f"🛑 CONVERGENCE DETECTED at epoch {epoch}")
                logger.info(f"   Rank loss range: {min(self.rank_loss_window):.6f} - {max(self.rank_loss_window):.6f}")
                logger.info(f"   Alpha range: {min(self.alpha_window):.4f} - {max(self.alpha_window):.4f}")
                logger.info(f"   α<6% range: {min(self.alpha_lt6_window):.1%} - {max(self.alpha_lt6_window):.1%}")
                logger.info(f"   Entropy range: {min(self.entropy_window):.6f} - {max(self.entropy_window):.6f}")
                logger.info(f"   Epochs without improvement: {self.epochs_without_improvement}")
                if no_freeze_candidates:
                    logger.info(f"   🧊 No more layers available for freezing")
                return True
        
        return False
    
    def _check_convergence(self, epoch: int, no_freeze_candidates: bool) -> bool:
        """Check if all metrics have plateaued with enhanced convergence detection."""
        
        # Calculate metric ranges over the window
        rank_range = max(self.rank_loss_window) - min(self.rank_loss_window)
        alpha_range = max(self.alpha_window) - min(self.alpha_window)
        entropy_range = max(self.entropy_window) - min(self.entropy_window)
        alpha_lt6_range = max(self.alpha_lt6_window) - min(self.alpha_lt6_window)
        
        # Dynamic alpha threshold - more forgiving late in training
        if epoch > 60:
            alpha_threshold = 0.07  # Most forgiving
        elif epoch > 40:
            alpha_threshold = 0.05  # Standard threshold
        else:
            alpha_threshold = 0.03  # Strict early training
        
        # Define convergence thresholds (enhanced based on feedback)
        rank_flat = rank_range < self.min_improve  # Primary metric - keep strict
        alpha_flat = alpha_range < alpha_threshold  # Dynamic threshold
        entropy_flat = entropy_range < 0.01  # Loosened - but weight it less
        alpha_lt6_flat = alpha_lt6_range < 0.01  # α<6% proportion stable (1% change)
        
        # Log current state with enhanced metrics
        logger.debug(f"Enhanced convergence check epoch {epoch}:")
        logger.debug(f"  Rank loss range: {rank_range:.6f} (flat: {rank_flat})")
        logger.debug(f"  Alpha range: {alpha_range:.4f} vs {alpha_threshold:.2f} (flat: {alpha_flat})")
        logger.debug(f"  α<6% range: {alpha_lt6_range:.3f} (flat: {alpha_lt6_flat})")
        logger.debug(f"  Entropy range: {entropy_range:.6f} (flat: {entropy_flat})")
        logger.debug(f"  Epochs without improvement: {self.epochs_without_improvement}")
        logger.debug(f"  No freeze candidates: {no_freeze_candidates}")
        
        # Primary convergence: rank_loss and alpha must both be flat
        primary_converged = rank_flat and alpha_flat and self.epochs_without_improvement >= self.patience
        
        # Enhanced signal: α<6% proportion has plateaued (meaningful directions stable)
        alpha_lt6_converged = alpha_lt6_flat and primary_converged
        
        # Enhanced signal: no more layers to freeze + model plateaued
        no_freeze_converged = no_freeze_candidates and primary_converged
        
        # Full convergence: all signals aligned
        fully_converged = primary_converged and entropy_flat and alpha_lt6_flat
        
        # Decision logic with enhanced signals
        if fully_converged:
            logger.debug("  → Fully converged (all metrics flat including α<6%)")
            return True
        elif no_freeze_converged:
            logger.debug("  → No-freeze convergence (no layers to freeze + plateaued)")
            return True
        elif alpha_lt6_converged:
            logger.debug("  → α<6% convergence (meaningful directions stable)")
            return True
        elif primary_converged:
            logger.debug("  → Primary convergence detected (rank_loss + alpha flat)")
            return True
        else:
            logger.debug("  → Not converged yet")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current convergence monitor status."""
        return {
            'epochs_without_improvement': self.epochs_without_improvement,
            'best_rank_loss': self.best_rank_loss,
            'window_size': len(self.rank_loss_window),
            'recent_rank_loss': self.rank_loss_window[-1] if self.rank_loss_window else None,
            'recent_alpha': self.alpha_window[-1] if self.alpha_window else None,
            'recent_entropy': self.entropy_window[-1] if self.entropy_window else None,
            'recent_alpha_lt6': self.alpha_lt6_window[-1] if self.alpha_lt6_window else None,
            'alpha_lt6_range': (max(self.alpha_lt6_window) - min(self.alpha_lt6_window)) if len(self.alpha_lt6_window) >= 2 else 0.0,
        }


def clip_top_spectral_norm_layers(model: torch.nn.Module, max_norm: float = 10.0):
    """
    Clip spectral norms of layers that exceed the threshold with robust SVD failure handling.

    Args:
        model: PyTorch model
        max_norm: Maximum allowed spectral norm
        
    Returns:
        List[Tuple[str, float, float]]: List of (layer_name, old_norm, new_norm) for clipped layers
    """
    clipped_layers = []
    svd_failed_layers = []

    for name, module in model.named_modules():
        if hasattr(module, "weight") and module.weight is not None and module.weight.ndim >= 2:
            W = module.weight.data
            
            # First try SVD computation
            try:
                # Compute spectral norm (largest singular value)
                _, S, _ = torch.linalg.svd(W, full_matrices=False)
                top_s = S[0]

                if top_s > max_norm:
                    scale = torch.tensor(max_norm / top_s, device=W.device, dtype=W.dtype)
                    with torch.no_grad():
                        module.weight.mul_(scale)
                    clipped_layers.append((name, top_s.item(), max_norm))

            except Exception as e:
                # SVD failed - matrix is likely ill-conditioned
                logger.error(f"🚨 SVD FAILED for {name}: {e}")
                svd_failed_layers.append(name)
                
                # EMERGENCY STABILIZATION: Use alternative methods
                try:
                    # Method 1: Check for NaN/Inf values
                    if torch.isnan(W).any() or torch.isinf(W).any():
                        logger.error(f"   → Matrix contains NaN/Inf - reinitializing")
                        with torch.no_grad():
                            # Reinitialize with Xavier normal
                            torch.nn.init.xavier_normal_(module.weight)
                        clipped_layers.append((name, float('inf'), "reinitialized"))
                        continue
                    
                    # Method 2: Use Frobenius norm as proxy
                    frobenius_norm = torch.norm(W, p='fro')
                    approx_spectral = frobenius_norm / math.sqrt(min(W.shape))  # Conservative approximation
                    
                    if approx_spectral > max_norm * 2:  # More aggressive threshold for failed SVD
                        logger.warning(f"   → Using Frobenius norm proxy: {approx_spectral:.2f}")
                        scale = torch.tensor(max_norm / approx_spectral, device=W.device, dtype=W.dtype)
                        with torch.no_grad():
                            module.weight.mul_(scale)
                        clipped_layers.append((name, approx_spectral.item(), max_norm))
                        continue
                    
                    # Method 3: Check condition number using eigenvalues (for square matrices)
                    if W.shape[0] == W.shape[1]:
                        try:
                            eigenvals = torch.linalg.eigvals(W)
                            max_eigval = torch.max(torch.real(eigenvals))
                            min_eigval = torch.min(torch.real(eigenvals))
                            
                            if min_eigval > 0:
                                condition_number = max_eigval / min_eigval
                                if condition_number > 1e6:  # Very ill-conditioned
                                    logger.warning(f"   → Ill-conditioned matrix (cond={condition_number:.2e}) - stabilizing")
                                    # Add regularization to diagonal
                                    with torch.no_grad():
                                        regularization = 1e-6 * torch.eye(W.shape[0], device=W.device, dtype=W.dtype)
                                        module.weight.add_(regularization)
                                    clipped_layers.append((name, condition_number, "regularized"))
                        except:
                            pass  # Eigenvalue computation also failed
                    
                    # Method 4: Last resort - check magnitude and clip if extreme
                    max_weight = torch.max(torch.abs(W))
                    if max_weight > max_norm * 10:  # Extremely large weights
                        logger.warning(f"   → Extreme weights detected ({max_weight:.2f}) - aggressive clipping")
                        scale = torch.tensor(max_norm / max_weight, device=W.device, dtype=W.dtype)
                        with torch.no_grad():
                            module.weight.mul_(scale)
                        clipped_layers.append((name, max_weight.item(), max_norm))
                
                except Exception as stabilization_error:
                    logger.error(f"   → All stabilization methods failed for {name}: {stabilization_error}")
                    # Final fallback - reinitialize the layer
                    try:
                        with torch.no_grad():
                            torch.nn.init.xavier_normal_(module.weight)
                        logger.error(f"   → Layer {name} reinitialized as last resort")
                        clipped_layers.append((name, float('inf'), "emergency_reinit"))
                    except:
                        logger.error(f"   → Could not stabilize layer {name} - training may fail")

    # Report results
    if clipped_layers:
        logger.info(f"🔧 Clipped {len(clipped_layers)} layers:")
        for name, old, new in clipped_layers:
            if isinstance(new, str):
                logger.info(f"   {name}: {old} → {new}")
            else:
                logger.info(f"   {name}: {old:.2f} → {new:.2f}")
    
    if svd_failed_layers:
        logger.error(f"🚨 SVD FAILURES detected in {len(svd_failed_layers)} layers:")
        for layer_name in svd_failed_layers:
            logger.error(f"   {layer_name}")
        logger.error("   This indicates severe training instability - consider:")
        logger.error("   • Reducing learning rate by 10x")
        logger.error("   • Increasing regularization")
        logger.error("   • Using gradient clipping")
        logger.error("   • Restarting from earlier checkpoint")

    return clipped_layers


def _has_adaptive_parameters(module: torch.nn.Module) -> bool:
    """
    Check if a module contains adaptive/learnable mixture parameters that should never be frozen.
    
    These are typically single-parameter logits that control strategy mixing and are critical
    for the model's ability to adapt during training.
    
    Returns:
        True if module has adaptive parameters (should NOT be frozen)
    """
    # Check for known adaptive parameter names
    adaptive_param_names = {
        'mixture_logit',      # SetEncoder: learned vs semantic mixture
        'strategy_logits',    # AdaptiveScalarEncoder: 20-strategy mixture weights
        'mixture_weights',    # AdaptiveStringEncoder: BERT vs trained mixture
        'temperature',        # Temperature-scaled attention
        'alpha',              # Learnable alpha parameters
        'beta',               # Learnable beta parameters
    }
    
    for param_name, param in module.named_parameters(recurse=False):
        # Check if this is an adaptive parameter
        if any(adaptive_name in param_name for adaptive_name in adaptive_param_names):
            return True
    
    return False


def freeze_dominant_layers(model: torch.nn.Module, norm_threshold: float = 10.0, 
                          max_layers_to_freeze: int = 5, max_param_percentage: float = 0.1):
    """
    Freeze layers with spectral norms above threshold, with safeguards to prevent over-freezing and robust SVD handling.
    
    CRITICAL: Never freezes modules with adaptive parameters (mixture_logit, strategy_logits, etc.)
    These tiny learnable weights are essential for strategy adaptation during training.

    Args:
        model: PyTorch model
        norm_threshold: Threshold for freezing layers
        max_layers_to_freeze: Maximum number of layers to freeze per call (default: 5)
        max_param_percentage: Maximum percentage of model parameters to freeze (default: 0.1 = 10%)

    Returns:
        List[Tuple[str, float]]: List of (layer_name, spectral_norm) for frozen layers
    """
    # Collect all layers with their spectral norms
    layer_candidates = []
    total_params = 0
    currently_frozen_params = 0
    svd_failed_layers = []
    skipped_adaptive_modules = []
    
    for name, module in model.named_modules():
        if hasattr(module, "weight") and module.weight is not None and module.weight.ndim >= 2:
            # CRITICAL: Skip modules with adaptive parameters - these MUST stay trainable
            if _has_adaptive_parameters(module):
                skipped_adaptive_modules.append(name)
                continue
            
            # Count parameters
            module_params = sum(p.numel() for p in module.parameters() if p is not None)
            total_params += module_params
            
            # Count already frozen parameters - check ALL parameters, not just weight
            # A module is considered frozen if ALL its parameters have requires_grad=False
            module_params_list = list(module.parameters())
            if module_params_list:
                all_frozen = all(not p.requires_grad for p in module_params_list if p is not None)
                if all_frozen:
                    currently_frozen_params += module_params
                    continue  # Skip already frozen layers
            
            # Try to compute spectral norm with robust handling
            try:
                W = module.weight
                s = torch.linalg.svdvals(W)
                top_s = s[0]

                if top_s > norm_threshold:
                    layer_candidates.append((name, top_s.item(), module_params, module))

            except Exception as e:
                # SVD failed - try alternative methods to estimate norm
                logger.warning(f"SVD failed for layer {name} during freezing analysis: {e}")
                svd_failed_layers.append(name)
                
                try:
                    W = module.weight.data
                    
                    # Check for NaN/Inf - these layers definitely need attention
                    if torch.isnan(W).any() or torch.isinf(W).any():
                        logger.error(f"   → Layer {name} contains NaN/Inf - marking for freeze")
                        layer_candidates.append((name, float('inf'), module_params, module))
                        continue
                    
                    # Use Frobenius norm as conservative proxy
                    frobenius_norm = torch.norm(W, p='fro')
                    approx_spectral = frobenius_norm / math.sqrt(min(W.shape))
                    
                    # Be more aggressive with SVD-failed layers
                    conservative_threshold = norm_threshold * 0.5  # Lower threshold for failed SVD
                    if approx_spectral > conservative_threshold:
                        logger.warning(f"   → Using Frobenius proxy for {name}: {approx_spectral:.2f} (threshold: {conservative_threshold:.2f})")
                        layer_candidates.append((name, approx_spectral.item(), module_params, module))
                    
                except Exception as fallback_error:
                    logger.error(f"   → All norm estimation methods failed for {name}: {fallback_error}")
                    # If we can't compute any norm, assume it's problematic and freeze it
                    logger.error(f"   → Marking {name} for freeze due to instability")
                    layer_candidates.append((name, float('inf'), module_params, module))
    
    # Sort by spectral norm (highest first) - freeze worst offenders first
    layer_candidates.sort(key=lambda x: x[1], reverse=True)
    
    # Apply safeguards
    current_frozen_percentage = currently_frozen_params / total_params if total_params > 0 else 0
    logger.info(f"🔍 Layer freezing analysis:")
    logger.info(f"   Total model parameters: {total_params:,}")
    logger.info(f"   Already frozen: {currently_frozen_params:,} ({current_frozen_percentage:.1%})")
    logger.info(f"   Candidates for freezing: {len(layer_candidates)}")
    
    if skipped_adaptive_modules:
        logger.info(f"   🔓 Skipped {len(skipped_adaptive_modules)} modules with adaptive parameters (never freeze these)")
        if len(skipped_adaptive_modules) <= 10:
            for module_name in skipped_adaptive_modules:
                logger.info(f"      • {module_name}")
    
    if svd_failed_layers:
        logger.warning(f"   ⚠️  {len(svd_failed_layers)} layers had SVD failures during analysis")
    
    if current_frozen_percentage >= max_param_percentage:
        logger.warning(f"⚠️  Already at {current_frozen_percentage:.1%} frozen parameters - skipping further freezing")
        return []
    
    # Determine how many layers we can safely freeze
    frozen_layers = []
    additional_frozen_params = 0
    
    for name, spectral_norm, module_params, module in layer_candidates:
        # Check if we've hit our limits
        if len(frozen_layers) >= max_layers_to_freeze:
            logger.info(f"⚠️  Hit max layers limit ({max_layers_to_freeze}) - stopping")
            break
            
        # Check if freezing this layer would exceed parameter percentage limit
        new_frozen_percentage = (currently_frozen_params + additional_frozen_params + module_params) / total_params
        if new_frozen_percentage > max_param_percentage:
            logger.info(f"⚠️  Freezing layer '{name}' would exceed {max_param_percentage:.1%} parameter limit - stopping")
            break
        
        # Freeze ALL parameters in this module
        trainable_params = [param for param in module.parameters() if param.requires_grad]
        
        if trainable_params:  # Only freeze if we actually have trainable parameters
            with torch.no_grad():
                for param in trainable_params:
                    param.requires_grad = False
            frozen_layers.append((name, spectral_norm))
            additional_frozen_params += module_params
            logger.debug(f"   Froze layer '{name}' with {module_params:,} params (spectral norm: {spectral_norm:.2f})")

    if frozen_layers:
        final_frozen_percentage = (currently_frozen_params + additional_frozen_params) / total_params
        logger.warning(f"❄️ Frozen {len(frozen_layers)} dominant layers ({additional_frozen_params:,} params, {final_frozen_percentage:.1%} total):")
        for name, norm in frozen_layers:
            if norm == float('inf'):
                logger.warning(f"   {name}: UNSTABLE (NaN/Inf or SVD failed)")
            else:
                logger.warning(f"   {name}: spectral norm {norm:.2f}")
        
        # Show what we didn't freeze
        skipped_count = len(layer_candidates) - len(frozen_layers)
        if skipped_count > 0:
            logger.info(f"⏭️  Skipped {skipped_count} additional high-norm layers due to safeguards")
    
    return frozen_layers


def detect_training_instability(model: torch.nn.Module, epoch: int, current_loss: float = None, 
                               prev_losses: List[float] = None) -> Dict[str, Any]:
    """
    Detect early signs of training instability before SVD failures occur.
    
    Args:
        model: PyTorch model to analyze
        epoch: Current training epoch
        current_loss: Current training loss value
        prev_losses: List of previous loss values for trend analysis
        
    Returns:
        Dict containing instability analysis and recommendations
    """
    instability_report = {
        'is_unstable': False,
        'severity': 'stable',
        'issues': [],
        'recommendations': [],
        'emergency_actions': []
    }
    
    issue_count = 0
    severe_issues = 0
    
    # 1. Check for NaN/Inf weights
    nan_layers = []
    inf_layers = []
    extreme_weight_layers = []
    
    for name, module in model.named_modules():
        if hasattr(module, "weight") and module.weight is not None:
            W = module.weight.data
            
            if torch.isnan(W).any():
                nan_layers.append(name)
                severe_issues += 1
            
            if torch.isinf(W).any():
                inf_layers.append(name)
                severe_issues += 1
            
            # Check for extremely large weights (potential overflow precursors)
            max_weight = torch.max(torch.abs(W))
            if max_weight > 100:  # Threshold for concerning weight magnitude
                extreme_weight_layers.append((name, max_weight.item()))
                issue_count += 1
    
    # 2. Check loss trends for instability
    loss_unstable = False
    if current_loss is not None:
        if math.isnan(current_loss) or math.isinf(current_loss):
            instability_report['issues'].append(f"Loss is NaN/Inf: {current_loss}")
            severe_issues += 1
            loss_unstable = True
        elif current_loss > 1000:  # Extremely high loss
            instability_report['issues'].append(f"Extremely high loss: {current_loss:.2f}")
            issue_count += 1
            loss_unstable = True
    
    if prev_losses and len(prev_losses) >= 3:
        # Check for loss explosion
        recent_losses = prev_losses[-3:]
        if all(loss > recent_losses[0] * 2 for loss in recent_losses[1:]):
            instability_report['issues'].append("Loss explosion detected - losses doubling")
            severe_issues += 1
            loss_unstable = True
        
        # Check for oscillating loss
        if len(prev_losses) >= 5:
            recent_5 = prev_losses[-5:]
            if max(recent_5) / min(recent_5) > 10:
                instability_report['issues'].append("Severe loss oscillations detected")
                issue_count += 1
    
    # 3. Try to compute spectral norms and detect problematic layers
    high_norm_layers = []
    svd_failing_layers = []
    
    for name, module in model.named_modules():
        if hasattr(module, "weight") and module.weight is not None and module.weight.ndim >= 2:
            try:
                W = module.weight.data
                s = torch.linalg.svdvals(W)
                top_s = s[0]
                
                if top_s > 50:  # Very high spectral norm
                    high_norm_layers.append((name, top_s.item()))
                    issue_count += 1
                elif top_s > 100:  # Extremely high
                    severe_issues += 1
                    
            except Exception:
                svd_failing_layers.append(name)
                severe_issues += 1
    
    # 4. Report findings
    if nan_layers:
        instability_report['issues'].append(f"NaN weights in {len(nan_layers)} layers: {nan_layers[:3]}{'...' if len(nan_layers) > 3 else ''}")
        instability_report['emergency_actions'].append("Reinitialize layers with NaN weights")
    
    if inf_layers:
        instability_report['issues'].append(f"Inf weights in {len(inf_layers)} layers: {inf_layers[:3]}{'...' if len(inf_layers) > 3 else ''}")
        instability_report['emergency_actions'].append("Reinitialize layers with Inf weights")
    
    if extreme_weight_layers:
        worst_layers = sorted(extreme_weight_layers, key=lambda x: x[1], reverse=True)[:3]
        instability_report['issues'].append(f"Extreme weights detected: {worst_layers}")
        instability_report['recommendations'].append("Apply aggressive spectral norm clipping")
    
    if svd_failing_layers:
        instability_report['issues'].append(f"SVD computation failing in {len(svd_failing_layers)} layers")
        instability_report['emergency_actions'].append("Emergency layer stabilization required")
    
    if high_norm_layers:
        worst_norms = sorted(high_norm_layers, key=lambda x: x[1], reverse=True)[:3]
        instability_report['issues'].append(f"High spectral norms: {worst_norms}")
        instability_report['recommendations'].append("Reduce learning rate and apply spectral norm clipping")
    
    # 5. Generate severity assessment and recommendations
    if severe_issues > 0:
        instability_report['is_unstable'] = True
        instability_report['severity'] = 'critical'
        instability_report['recommendations'].extend([
            "STOP TRAINING IMMEDIATELY",
            "Reduce learning rate by 100x",
            "Restore from earlier checkpoint",
            "Add gradient clipping (max_norm=1.0)",
            "Increase weight decay regularization"
        ])
    elif issue_count > 5 or loss_unstable:
        instability_report['is_unstable'] = True
        instability_report['severity'] = 'high'
        instability_report['recommendations'].extend([
            "Reduce learning rate by 10x",
            "Apply spectral norm clipping (max_norm=5.0)",
            "Add gradient clipping",
            "Monitor closely"
        ])
    elif issue_count > 2:
        instability_report['is_unstable'] = True
        instability_report['severity'] = 'moderate'
        instability_report['recommendations'].extend([
            "Reduce learning rate by 3x",
            "Apply spectral norm clipping",
            "Monitor weight norms"
        ])
    
    # 6. Add epoch-specific advice
    if epoch < 5 and instability_report['is_unstable']:
        instability_report['recommendations'].append("Early instability suggests learning rate too high")
    elif epoch > 50 and instability_report['severity'] == 'critical':
        instability_report['recommendations'].append("Late-stage instability suggests model degradation")
    
    return instability_report


def refresh_hard_negative_sampler():
    """
    Refresh hard negative sampling strategy.
    
    This is a placeholder for implementing more sophisticated 
    negative sampling when rank loss gets too low.
    """
    logger.info("🔁 Refreshing hard negative sampler")
    # TODO: Implement hard negative sampling refresh logic
    # This could involve:
    # - Resampling validation set
    # - Adjusting contrastive loss parameters
    # - Modifying data augmentation strategy
    pass 