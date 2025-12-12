#!/usr/bin/env python3
"""
Quick summary of focal loss comparison results in terminal.

Usage:
    python3 show_results.py [results.json]
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def format_metric(value, metric_type='float'):
    """Format metric for display."""
    if value is None:
        return "N/A"
    if metric_type == 'float':
        return f"{value:.4f}"
    elif metric_type == 'percent':
        return f"{value:.1f}%"
    return str(value)


def print_colored(text, color_code):
    """Print colored text in terminal."""
    print(f"\033[{color_code}m{text}\033[0m")


def show_summary(results_path):
    """Display results summary in terminal."""
    
    # Load results
    with open(results_path, 'r') as f:
        data = json.load(f)
    
    results = data.get('results', data if isinstance(data, list) else [])
    timestamp = data.get('timestamp', 'Unknown')
    
    # Header
    print()
    print_colored("=" * 100, "1;36")  # Cyan bold
    print_colored("  FOCAL LOSS vs CROSS-ENTROPY COMPARISON RESULTS", "1;36")
    print_colored("=" * 100, "1;36")
    print()
    print(f"📅 Generated: {timestamp}")
    print(f"📊 Total Tests: {len(results)}")
    print()
    
    # Group by ratio
    ratios = {}
    for r in results:
        ratio = r['ratio']
        if ratio not in ratios:
            ratios[ratio] = {}
        ratios[ratio][r['loss_type']] = r
    
    # Display each ratio
    for ratio_name, loss_types in ratios.items():
        print_colored(f"\n{'─' * 100}", "1;34")  # Blue
        print_colored(f"  {ratio_name}", "1;34")
        print_colored(f"{'─' * 100}", "1;34")
        
        focal = loss_types.get('focal', {})
        ce = loss_types.get('cross_entropy', {})
        
        # Table header
        print(f"\n{'Metric':<25} {'Focal Loss':<20} {'Cross-Entropy':<20} {'Winner':<15}")
        print("─" * 80)
        
        # Define metrics to compare
        metrics = [
            ('validation_loss', 'Validation Loss', 'float', 'lower'),
            ('f1', 'F1 Score', 'float', 'higher'),
            ('accuracy', 'Accuracy', 'float', 'higher'),
            ('precision', 'Precision', 'float', 'higher'),
            ('recall', 'Recall', 'float', 'higher'),
            ('auc', 'AUC', 'float', 'higher'),
        ]
        
        for key, label, fmt, better in metrics:
            focal_val = focal.get(key)
            ce_val = ce.get(key)
            
            if focal_val is not None and ce_val is not None:
                # Determine winner
                if better == 'lower':
                    focal_wins = focal_val < ce_val
                else:
                    focal_wins = focal_val > ce_val
                
                winner = "✓ Focal" if focal_wins else "✓ Cross-Entropy"
                winner_color = "32" if focal_wins else "35"  # Green or Magenta
                
                focal_str = format_metric(focal_val, fmt)
                ce_str = format_metric(ce_val, fmt)
                
                print(f"{label:<25} {focal_str:<20} {ce_str:<20}", end="")
                print_colored(f"{winner:<15}", winner_color)
            else:
                print(f"{label:<25} {'N/A':<20} {'N/A':<20} {'N/A':<15}")
        
        # Show additional info
        if focal.get('epochs'):
            print(f"\n  ℹ️  Training epochs: {focal.get('epochs', 'N/A')}")
    
    # Overall statistics
    print_colored(f"\n\n{'═' * 100}", "1;36")
    print_colored("  OVERALL STATISTICS", "1;36")
    print_colored(f"{'═' * 100}", "1;36")
    print()
    
    # Count wins
    focal_wins = 0
    ce_wins = 0
    total_comparisons = 0
    
    for ratio_name, loss_types in ratios.items():
        focal = loss_types.get('focal', {})
        ce = loss_types.get('cross_entropy', {})
        
        metrics_to_check = [
            ('validation_loss', 'lower'),
            ('f1', 'higher'),
            ('accuracy', 'higher'),
            ('precision', 'higher'),
            ('recall', 'higher'),
            ('auc', 'higher'),
        ]
        
        for key, better in metrics_to_check:
            focal_val = focal.get(key)
            ce_val = ce.get(key)
            
            if focal_val is not None and ce_val is not None:
                total_comparisons += 1
                if better == 'lower':
                    if focal_val < ce_val:
                        focal_wins += 1
                    else:
                        ce_wins += 1
                else:
                    if focal_val > ce_val:
                        focal_wins += 1
                    else:
                        ce_wins += 1
    
    focal_pct = (focal_wins / total_comparisons * 100) if total_comparisons > 0 else 0
    ce_pct = (ce_wins / total_comparisons * 100) if total_comparisons > 0 else 0
    
    print(f"🏆 Focal Loss Wins:       {focal_wins}/{total_comparisons} ({focal_pct:.1f}%)")
    print(f"🏆 Cross-Entropy Wins:    {ce_wins}/{total_comparisons} ({ce_pct:.1f}%)")
    print()
    
    # Recommendation
    if focal_pct > 60:
        print_colored("✅ RECOMMENDATION: Use Focal Loss - Shows consistent improvements", "1;32")
    elif focal_pct > 40:
        print_colored("⚠️  RECOMMENDATION: Mixed results - Consider metric priorities", "1;33")
    else:
        print_colored("⚠️  RECOMMENDATION: Cross-Entropy performed better overall", "1;33")
    
    print()
    
    # Best performers
    print_colored("\n📈 BEST PERFORMERS:", "1;36")
    print()
    
    best_f1 = max(results, key=lambda x: x.get('f1', 0))
    print(f"  Highest F1 Score:      {best_f1.get('f1', 0):.4f} ({best_f1['loss_type']} on {best_f1['ratio']})")
    
    lowest_loss = min(results, key=lambda x: x.get('validation_loss', float('inf')))
    print(f"  Lowest Val Loss:       {lowest_loss.get('validation_loss', 0):.4f} ({lowest_loss['loss_type']} on {lowest_loss['ratio']})")
    
    best_auc = max(results, key=lambda x: x.get('auc', 0))
    print(f"  Highest AUC:           {best_auc.get('auc', 0):.4f} ({best_auc['loss_type']} on {best_auc['ratio']})")
    
    print()
    print_colored("=" * 100, "1;36")
    print()
    print(f"💡 Tip: Generate full HTML report with graphs using:")
    print(f"    python3 generate_focal_report.py")
    print()


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    
    # Determine input file
    if len(sys.argv) > 1:
        results_path = Path(sys.argv[1])
    else:
        # Try to find results file
        enhanced_path = script_dir / "focal_comparison_enhanced_results.json"
        basic_path = script_dir / "focal_comparison_results.json"
        
        if enhanced_path.exists():
            results_path = enhanced_path
        elif basic_path.exists():
            results_path = basic_path
        else:
            print("Error: No results file found.")
            print("Usage: python3 show_results.py [results.json]")
            sys.exit(1)
    
    if not results_path.exists():
        print(f"Error: Results file not found: {results_path}")
        sys.exit(1)
    
    show_summary(results_path)


if __name__ == "__main__":
    main()

