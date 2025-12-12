#!/usr/bin/env python3
"""
Visualize ES Training Timeline

This script reads the training_timeline.json file and creates visualizations
to help understand what's happening during training.

Usage:
    python visualize_training_timeline.py [path_to_training_timeline.json]
"""
import json
import sys
import os
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  Warning: matplotlib not available, will only print text summary")


def load_timeline(path):
    """Load the training timeline JSON file"""
    with open(path, 'r') as f:
        return json.load(f)


def print_summary(data):
    """Print a text summary of the training timeline"""
    timeline = data['timeline']
    corrective_actions = data.get('corrective_actions', [])
    metadata = data.get('metadata', {})
    
    print("=" * 80)
    print("ES TRAINING TIMELINE SUMMARY")
    print("=" * 80)
    print()
    
    # Metadata
    print("📋 Training Configuration:")
    print(f"  Initial LR: {metadata.get('initial_lr', 'unknown')}")
    print(f"  Total Epochs: {metadata.get('total_epochs', 'unknown')}")
    print(f"  Batch Size: {metadata.get('batch_size', 'unknown')}")
    print(f"  Scheduler: {metadata.get('scheduler_type', 'unknown')}")
    print(f"  Dropout Scheduler: {'Enabled' if metadata.get('dropout_scheduler_enabled') else 'Disabled'}")
    if metadata.get('dropout_scheduler_enabled'):
        print(f"    Initial: {metadata.get('initial_dropout')} → Final: {metadata.get('final_dropout')}")
    print()
    
    # Failure summary
    failure_counts = {}
    for entry in timeline:
        for failure in entry.get('failures_detected', []):
            failure_counts[failure] = failure_counts.get(failure, 0) + 1
    
    if failure_counts:
        print("🚨 Failures Detected:")
        for failure, count in sorted(failure_counts.items()):
            print(f"  {failure}: {count} epochs")
        print()
    
    # Corrective actions summary
    if corrective_actions:
        print("🔧 Corrective Actions Taken:")
        for action in corrective_actions:
            details = action.get('details', {})
            lr_mult = details.get('lr_multiplier', 1.0)
            temp_mult = details.get('temp_multiplier', 1.0)
            
            # Build action description
            action_desc = []
            if lr_mult > 1.0:
                action_desc.append(f"LR×{lr_mult}")
            if temp_mult > 1.0:
                action_desc.append(f"Temp×{temp_mult}")
            action_str = ", ".join(action_desc) if action_desc else action['action_type']
            
            print(f"  Epoch {action['epoch']}: {action_str}")
            print(f"    Trigger: {action['trigger']}")
            if details:
                for key, value in details.items():
                    if key not in ['lr_multiplier', 'temp_multiplier']:  # Already shown above
                        print(f"    {key}: {value}")
        print()
    
    # Detect temperature changes by scanning timeline
    print("🌡️  Temperature Changes Detected:")
    temp_changes_found = False
    for i in range(1, len(timeline)):
        prev_temp = timeline[i-1].get('spread_temperature')
        curr_temp = timeline[i].get('spread_temperature')
        prev_batch = timeline[i-1].get('batch_size')
        curr_batch = timeline[i].get('batch_size')
        
        if prev_temp is not None and curr_temp is not None:
            if abs(curr_temp - prev_temp) / prev_temp > 0.1:  # >10% change
                change_pct = ((curr_temp - prev_temp) / prev_temp) * 100
                epoch = timeline[i]['epoch']
                # Check if this was a logged corrective action
                was_logged = any(a['epoch'] == epoch for a in corrective_actions)
                status = "✓ logged" if was_logged else "⚠️  unlogged"
                
                # Show batch size change if available
                batch_info = ""
                if prev_batch is not None and curr_batch is not None and prev_batch != curr_batch:
                    batch_change = ((curr_batch - prev_batch) / prev_batch) * 100
                    batch_info = f" [batch: {prev_batch}→{curr_batch} ({batch_change:+.0f}%)]"
                
                print(f"  Epoch {epoch}: {prev_temp:.4f} → {curr_temp:.4f} ({change_pct:+.1f}%) [{status}]{batch_info}")
                temp_changes_found = True
    if not temp_changes_found:
        print("  (none detected)")
    print()
    
    # Detect validation set rotations
    print("🔄 Validation Set Rotations:")
    rotation_epochs = [e['epoch'] for e in timeline if e.get('val_set_resampled', False)]
    if rotation_epochs:
        for epoch in rotation_epochs:
            print(f"  Epoch {epoch}: Train/val split resampled")
        print(f"  Total: {len(rotation_epochs)} rotations")
    else:
        print("  (none detected)")
    print()
    
    # Epoch-by-epoch details
    print("📊 Epoch-by-Epoch Timeline:")
    print(f"{'Epoch':>6} {'LR':>12} {'Train Loss':>12} {'Val Loss':>12} {'Dropout':>9} {'Spread Loss':>12} {'Temp':>8} {'Grad(uncl)':>12} {'Grad(clip)':>12} {'WW Alpha':>10} {'Failures':>20} {'Actions':>10}")
    print("-" * 160)
    
    for entry in timeline:
        epoch = entry['epoch']
        lr = entry.get('learning_rate', 0)
        train_loss = entry.get('train_loss')
        val_loss = entry.get('validation_loss')
        dropout = entry.get('dropout_rate')
        spread_loss = entry.get('spread_loss')
        spread_temp = entry.get('spread_temperature')
        
        # Get gradient info (new detailed format or legacy)
        gradients = entry.get('gradients', {})
        grad_unclipped = gradients.get('unclipped_norm') if gradients else entry.get('gradient_norm')
        grad_clipped = gradients.get('clipped_norm')
        
        # Get WeightWatcher data
        ww_data = entry.get('weightwatcher')
        ww_alpha = ww_data.get('avg_alpha') if ww_data else None
        
        failures = ', '.join(entry.get('failures_detected', []))
        actions = '✓' if entry.get('corrective_actions') else ''
        
        # Format values
        lr_str = f"{lr:.6f}" if lr is not None else "N/A"
        train_loss_str = f"{train_loss:.4f}" if train_loss is not None else "N/A"
        val_loss_str = f"{val_loss:.4f}" if val_loss is not None else "N/A"
        dropout_str = f"{dropout:.3f}" if dropout is not None else "N/A"
        spread_loss_str = f"{spread_loss:.4f}" if spread_loss is not None else "N/A"
        spread_temp_str = f"{spread_temp:.4f}" if spread_temp is not None else "N/A"
        grad_uncl_str = f"{grad_unclipped:.4f}" if grad_unclipped is not None else "N/A"
        grad_clip_str = f"{grad_clipped:.4f}" if grad_clipped is not None else "N/A"
        ww_alpha_str = f"{ww_alpha:.3f}" if ww_alpha is not None else "N/A"
        
        # Highlight problematic epochs
        marker = ""
        if 'NO_LEARNING' in failures:
            marker = "🚨"
        elif entry.get('early_stop_blocked'):
            marker = "🚫"
        elif failures:
            marker = "⚠️ "
        
        print(f"{marker}{epoch:>5} {lr_str:>12} {train_loss_str:>12} {val_loss_str:>12} {dropout_str:>9} {spread_loss_str:>12} {spread_temp_str:>8} {grad_uncl_str:>12} {grad_clip_str:>12} {ww_alpha_str:>10} {failures:>20} {actions:>10}")
    
    print("=" * 80)


def plot_timeline(data, output_path=None):
    """Create visualization plots of the training timeline"""
    if not HAS_MATPLOTLIB:
        print("⚠️  Cannot create plots without matplotlib")
        return
    
    timeline = data['timeline']
    
    # Extract data for plotting
    epochs = [e['epoch'] for e in timeline]
    lrs = [e.get('learning_rate', 0) for e in timeline]
    train_losses = [e.get('train_loss') for e in timeline]
    val_losses = [e.get('validation_loss') for e in timeline]
    dropouts = [e.get('dropout_rate') for e in timeline]
    spread_losses = [e.get('spread_loss') for e in timeline]
    spread_temps = [e.get('spread_temperature') for e in timeline]
    
    # Extract gradient data (handle both new and legacy formats)
    grad_unclipped = []
    grad_clipped = []
    grad_ratios = []
    for e in timeline:
        gradients = e.get('gradients', {})
        if gradients:
            grad_unclipped.append(gradients.get('unclipped_norm'))
            grad_clipped.append(gradients.get('clipped_norm'))
            grad_ratios.append(gradients.get('clip_ratio'))
        else:
            grad_unclipped.append(e.get('gradient_norm'))
            grad_clipped.append(None)
            grad_ratios.append(None)
    
    # Extract WeightWatcher alpha values
    ww_alphas = []
    for e in timeline:
        ww_data = e.get('weightwatcher')
        ww_alphas.append(ww_data.get('avg_alpha') if ww_data else None)
    
    # Find epochs with failures
    no_learning_epochs = [e['epoch'] for e in timeline if 'NO_LEARNING' in e.get('failures_detected', [])]
    other_failure_epochs = [e['epoch'] for e in timeline if e.get('failures_detected') and 'NO_LEARNING' not in e.get('failures_detected', [])]
    blocked_epochs = [e['epoch'] for e in timeline if e.get('early_stop_blocked')]
    
    # Extract corrective actions with their types
    corrective_actions_data = data.get('corrective_actions', [])
    lr_boost_epochs = []
    temp_boost_epochs = []
    other_action_epochs = []
    
    for action in corrective_actions_data:
        epoch = action.get('epoch')
        action_type = action.get('action_type', '')
        details = action.get('details', {})
        
        # Determine if it's an LR boost or temp boost based on details
        lr_mult = details.get('lr_multiplier', 1.0)
        temp_mult = details.get('temp_multiplier', 1.0)
        
        if lr_mult > 1.0 and temp_mult == 1.0:
            lr_boost_epochs.append(epoch)
        elif temp_mult > 1.0 and lr_mult == 1.0:
            temp_boost_epochs.append(epoch)
        elif lr_mult > 1.0 and temp_mult > 1.0:
            # Both changed - mark as both
            lr_boost_epochs.append(epoch)
            temp_boost_epochs.append(epoch)
        else:
            other_action_epochs.append(epoch)
    
    # Extract validation set rotation epochs
    val_rotation_epochs = [e['epoch'] for e in timeline if e.get('val_set_resampled', False)]
    
    # Also detect temperature changes by comparing consecutive epochs
    detected_temp_changes = []
    for i in range(1, len(timeline)):
        prev_temp = timeline[i-1].get('spread_temperature')
        curr_temp = timeline[i].get('spread_temperature')
        
        if prev_temp is not None and curr_temp is not None:
            # Detect significant temp changes (>10% change)
            if abs(curr_temp - prev_temp) / prev_temp > 0.1:
                detected_temp_changes.append(timeline[i]['epoch'])
    
    # Create figure with subplots (3x2 grid now for more charts)
    fig, axes = plt.subplots(3, 2, figsize=(16, 15))
    fig.suptitle('ES Training Timeline', fontsize=16, fontweight='bold')
    
    # Plot 1: Learning Rate
    ax1 = axes[0, 0]
    ax1.plot(epochs, lrs, 'b-', linewidth=2, label='Learning Rate')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Learning Rate')
    ax1.set_title('Learning Rate Schedule')
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')  # Log scale for LR
    
    # Mark NO_LEARNING epochs
    for epoch in no_learning_epochs:
        ax1.axvline(x=epoch, color='red', alpha=0.3, linestyle='--')
    
    # Plot 2: Training and Validation Loss WITH INTERVENTION MARKERS
    ax2 = axes[0, 1]
    # Filter out None values
    train_epochs = [e for e, l in zip(epochs, train_losses) if l is not None]
    train_losses_clean = [l for l in train_losses if l is not None]
    val_epochs = [e for e, l in zip(epochs, val_losses) if l is not None]
    val_losses_clean = [l for l in val_losses if l is not None]
    
    if train_losses_clean:
        ax2.plot(train_epochs, train_losses_clean, 'g-', linewidth=2, label='Train Loss', alpha=0.7)
    if val_losses_clean:
        ax2.plot(val_epochs, val_losses_clean, 'orange', linewidth=2, label='Validation Loss')
    
    # Mark interventions with different symbols and colors
    y_min, y_max = ax2.get_ylim() if val_losses_clean or train_losses_clean else (0, 1)
    
    # LR boost interventions (green upward triangles)
    for epoch in lr_boost_epochs:
        ax2.axvline(x=epoch, color='green', alpha=0.5, linestyle='--', linewidth=2)
        # Find the validation loss at this epoch for marker placement
        if epoch < len(val_losses_clean):
            y_pos = val_losses_clean[min(epoch, len(val_losses_clean)-1)]
        else:
            y_pos = (y_min + y_max) / 2
        ax2.plot(epoch, y_pos, marker='^', color='green', markersize=12, 
                markeredgecolor='darkgreen', markeredgewidth=2, zorder=5)
    
    # Temperature boost interventions (red circles)
    for epoch in temp_boost_epochs:
        ax2.axvline(x=epoch, color='red', alpha=0.5, linestyle=':', linewidth=2)
        if epoch < len(val_losses_clean):
            y_pos = val_losses_clean[min(epoch, len(val_losses_clean)-1)]
        else:
            y_pos = (y_min + y_max) / 2
        ax2.plot(epoch, y_pos, marker='o', color='red', markersize=10, 
                markeredgecolor='darkred', markeredgewidth=2, zorder=5)
    
    # Detected temperature changes (yellow diamonds) - catches unlogged interventions
    for epoch in detected_temp_changes:
        if epoch not in temp_boost_epochs:  # Only show if not already marked
            if epoch < len(val_losses_clean):
                y_pos = val_losses_clean[min(epoch, len(val_losses_clean)-1)]
            else:
                y_pos = (y_min + y_max) / 2
            ax2.plot(epoch, y_pos, marker='D', color='gold', markersize=10, 
                    markeredgecolor='darkorange', markeredgewidth=2, zorder=5)
    
    # NO_LEARNING detections (light red vertical bands)
    for epoch in no_learning_epochs:
        ax2.axvline(x=epoch, color='red', alpha=0.2, linestyle='-', linewidth=4)
    
    # Validation set rotations (light blue vertical lines)
    for epoch in val_rotation_epochs:
        ax2.axvline(x=epoch, color='blue', alpha=0.3, linestyle=':', linewidth=2)
    
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.set_title('Validation Loss with Interventions')
    ax2.grid(True, alpha=0.3)
    
    # Create custom legend with intervention explanations
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='orange', linewidth=2, label='Validation Loss'),
    ]
    if train_losses_clean:
        legend_elements.append(Line2D([0], [0], color='g', linewidth=2, alpha=0.7, label='Train Loss'))
    if lr_boost_epochs:
        legend_elements.append(Line2D([0], [0], marker='^', color='green', linewidth=0, 
                                    markersize=10, markeredgecolor='darkgreen', markeredgewidth=2,
                                    label=f'LR Boost ({len(lr_boost_epochs)}x)'))
    if temp_boost_epochs:
        legend_elements.append(Line2D([0], [0], marker='o', color='red', linewidth=0,
                                    markersize=8, markeredgecolor='darkred', markeredgewidth=2,
                                    label=f'Temp Boost ({len(temp_boost_epochs)}x)'))
    if detected_temp_changes:
        unlogged_changes = [e for e in detected_temp_changes if e not in temp_boost_epochs]
        if unlogged_changes:
            legend_elements.append(Line2D([0], [0], marker='D', color='gold', linewidth=0,
                                        markersize=8, markeredgecolor='darkorange', markeredgewidth=2,
                                        label=f'Temp Change (unlogged, {len(unlogged_changes)}x)'))
    if no_learning_epochs:
        legend_elements.append(Line2D([0], [0], color='red', alpha=0.3, linewidth=4,
                                    label=f'NO_LEARNING ({len(no_learning_epochs)}x)'))
    if val_rotation_epochs:
        legend_elements.append(Line2D([0], [0], color='blue', alpha=0.3, linestyle=':', linewidth=2,
                                    label=f'Val Set Rotated ({len(val_rotation_epochs)}x)'))
    
    ax2.legend(handles=legend_elements, loc='best', fontsize=9)
    
    # Plot 3: Dropout Rate
    ax3 = axes[1, 0]
    dropout_epochs = [e for e, d in zip(epochs, dropouts) if d is not None]
    dropouts_clean = [d for d in dropouts if d is not None]
    
    if dropouts_clean:
        ax3.plot(dropout_epochs, dropouts_clean, 'purple', linewidth=2, label='Dropout Rate')
        ax3.set_xlabel('Epoch')
        ax3.set_ylabel('Dropout Rate')
        ax3.set_title('Dropout Schedule')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Mark NO_LEARNING epochs
        for epoch in no_learning_epochs:
            ax3.axvline(x=epoch, color='red', alpha=0.3, linestyle='--')
    
    # Plot 4: Gradient Norms (unclipped vs clipped)
    ax4 = axes[1, 1]
    grad_uncl_epochs = [e for e, g in zip(epochs, grad_unclipped) if g is not None]
    grad_uncl_clean = [g for g in grad_unclipped if g is not None]
    grad_clip_epochs = [e for e, g in zip(epochs, grad_clipped) if g is not None]
    grad_clip_clean = [g for g in grad_clipped if g is not None]
    
    if grad_uncl_clean:
        ax4.plot(grad_uncl_epochs, grad_uncl_clean, 'brown', linewidth=2, label='Unclipped Gradient Norm', alpha=0.7)
    if grad_clip_clean:
        ax4.plot(grad_clip_epochs, grad_clip_clean, 'darkred', linewidth=2, label='Clipped Gradient Norm', linestyle='--')
    
    ax4.set_xlabel('Epoch')
    ax4.set_ylabel('Gradient Norm')
    ax4.set_title('Gradient Norms (Unclipped vs Clipped)')
    if grad_uncl_clean or grad_clip_clean:
        ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # Mark NO_LEARNING epochs
    for epoch in no_learning_epochs:
        ax4.axvline(x=epoch, color='red', alpha=0.3, linestyle='--')
    
    # Plot 5: Spread Loss
    ax5 = axes[2, 0]
    spread_loss_epochs = [e for e, s in zip(epochs, spread_losses) if s is not None]
    spread_losses_clean = [s for s in spread_losses if s is not None]
    
    if spread_losses_clean:
        ax5.plot(spread_loss_epochs, spread_losses_clean, 'teal', linewidth=2, label='Spread Loss')
        ax5.set_xlabel('Epoch')
        ax5.set_ylabel('Spread Loss')
        ax5.set_title('Spread Loss (Contrastive Learning)')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # Mark NO_LEARNING epochs
        for epoch in no_learning_epochs:
            ax5.axvline(x=epoch, color='red', alpha=0.3, linestyle='--')
    
    # Plot 6: Adaptive Temperature
    ax6 = axes[2, 1]
    spread_temp_epochs = [e for e, t in zip(epochs, spread_temps) if t is not None]
    spread_temps_clean = [t for t in spread_temps if t is not None]
    
    if spread_temps_clean:
        ax6.plot(spread_temp_epochs, spread_temps_clean, 'magenta', linewidth=2, label='Adaptive Temperature')
        ax6.set_xlabel('Epoch')
        ax6.set_ylabel('Temperature')
        ax6.set_title('Spread Loss Temperature (Adaptive)')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        
        # Mark NO_LEARNING epochs
        for epoch in no_learning_epochs:
            ax6.axvline(x=epoch, color='red', alpha=0.3, linestyle='--')
    
    # Add legend for failure markers
    if no_learning_epochs or other_failure_epochs or blocked_epochs:
        legend_elements = []
        if no_learning_epochs:
            legend_elements.append(mpatches.Patch(color='red', alpha=0.3, label='NO_LEARNING detected'))
        if other_failure_epochs:
            legend_elements.append(mpatches.Patch(color='orange', alpha=0.3, label='Other failures'))
        if blocked_epochs:
            legend_elements.append(mpatches.Patch(color='blue', alpha=0.3, label='Early stop blocked'))
        
        fig.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.99, 0.99))
    
    plt.tight_layout()
    
    # Save or show
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"📊 Plot saved to {output_path}")
    else:
        plt.show()


def main():
    """Main entry point"""
    # Find timeline file
    if len(sys.argv) > 1:
        timeline_path = sys.argv[1]
    else:
        # Look in current directory
        timeline_path = "training_timeline.json"
        if not os.path.exists(timeline_path):
            # Look in qa directory
            timeline_path = os.path.join(os.path.dirname(__file__), "training_timeline.json")
    
    if not os.path.exists(timeline_path):
        print(f"❌ Could not find training_timeline.json")
        print(f"   Looked in: {timeline_path}")
        print()
        print("Usage: python visualize_training_timeline.py [path_to_training_timeline.json]")
        sys.exit(1)
    
    print(f"📂 Loading timeline from: {timeline_path}")
    data = load_timeline(timeline_path)
    
    # Print text summary
    print_summary(data)
    
    # Create plots if matplotlib is available
    if HAS_MATPLOTLIB:
        print()
        output_path = timeline_path.replace('.json', '_plot.png')
        plot_timeline(data, output_path)
    else:
        print()
        print("💡 Install matplotlib to generate visualization plots:")
        print("   pip install matplotlib")


if __name__ == '__main__':
    main()

