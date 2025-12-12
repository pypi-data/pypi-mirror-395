#!/usr/bin/env python3
"""
Generate comprehensive HTML report from focal loss comparison test results.

Usage:
    python3 generate_focal_report.py [results.json] [output.html]
    
If no arguments provided, uses default paths:
    - focal_comparison_results.json (or focal_comparison_enhanced_results.json)
    - focal_comparison_report.html
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import base64
from io import BytesIO

# Try to import plotting libraries
try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_PLOTTING = True
except ImportError:
    HAS_PLOTTING = False
    print("Warning: matplotlib not available, report will not include graphs")


def load_results(json_path):
    """Load test results from JSON file."""
    with open(json_path, 'r') as f:
        return json.load(f)


def fig_to_base64(fig):
    """Convert matplotlib figure to base64 encoded PNG."""
    if not HAS_PLOTTING:
        return ""
    
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{img_base64}"


def create_loss_comparison_chart(results):
    """Create bar chart comparing validation losses."""
    if not HAS_PLOTTING:
        return ""
    
    # Group by ratio
    ratios = {}
    for r in results:
        ratio = r['ratio']
        if ratio not in ratios:
            ratios[ratio] = {'focal': None, 'cross_entropy': None}
        ratios[ratio][r['loss_type']] = r['validation_loss']
    
    # Create grouped bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ratio_names = list(ratios.keys())
    focal_losses = [ratios[r]['focal'] for r in ratio_names]
    ce_losses = [ratios[r]['cross_entropy'] for r in ratio_names]
    
    x = np.arange(len(ratio_names))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, focal_losses, width, label='Focal Loss', color='#2E86AB')
    bars2 = ax.bar(x + width/2, ce_losses, width, label='Cross-Entropy', color='#A23B72')
    
    ax.set_xlabel('Class Ratio', fontsize=12, fontweight='bold')
    ax.set_ylabel('Validation Loss', fontsize=12, fontweight='bold')
    ax.set_title('Validation Loss Comparison: Focal vs Cross-Entropy', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(ratio_names, rotation=15, ha='right')
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}',
                   ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    return fig_to_base64(fig)


def create_loss_curves(results):
    """Create validation loss curves for each ratio."""
    if not HAS_PLOTTING:
        return ""
    
    # Group by ratio
    ratios = {}
    for r in results:
        ratio = r['ratio']
        if ratio not in ratios:
            ratios[ratio] = {}
        
        if 'loss_history' in r and r['loss_history']:
            ratios[ratio][r['loss_type']] = r['loss_history']
    
    # Filter out ratios without history data
    ratios = {k: v for k, v in ratios.items() if v}
    
    if not ratios:
        return ""
    
    n_ratios = len(ratios)
    n_cols = min(3, n_ratios)
    n_rows = (n_ratios + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 5*n_rows))
    if n_ratios == 1:
        axes = np.array([axes])
    axes = axes.flatten() if n_ratios > 1 else axes
    
    for idx, (ratio_name, loss_types) in enumerate(ratios.items()):
        ax = axes[idx] if n_ratios > 1 else axes[0]
        
        for loss_type, history in loss_types.items():
            epochs = history.get('epochs', [])
            val_loss = history.get('val_loss', [])
            train_loss = history.get('train_loss', [])
            
            # Filter out None values
            valid_data = [(e, v, t) for e, v, t in zip(epochs, val_loss, train_loss) 
                         if v is not None and t is not None]
            
            if valid_data:
                epochs, val_loss, train_loss = zip(*valid_data)
                
                color = '#2E86AB' if loss_type == 'focal' else '#A23B72'
                label = 'Focal' if loss_type == 'focal' else 'Cross-Entropy'
                
                # Plot validation loss (solid line)
                ax.plot(epochs, val_loss, '-o', color=color, linewidth=2, 
                       label=f'{label} (val)', markersize=3, alpha=0.8)
                
                # Plot training loss (dashed line, lighter)
                ax.plot(epochs, train_loss, '--', color=color, linewidth=1, 
                       alpha=0.4, label=f'{label} (train)')
        
        ax.set_xlabel('Epoch', fontsize=11, fontweight='bold')
        ax.set_ylabel('Loss', fontsize=11, fontweight='bold')
        ax.set_title(f'{ratio_name}', fontsize=12, fontweight='bold')
        ax.legend(fontsize=9, loc='best')
        ax.grid(True, alpha=0.3)
    
    # Hide unused subplots
    for idx in range(n_ratios, len(axes)):
        fig.delaxes(axes[idx])
    
    plt.suptitle('Training & Validation Loss Curves', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig_to_base64(fig)


def create_metrics_comparison_chart(results):
    """Create grouped bar chart for all metrics."""
    if not HAS_PLOTTING:
        return ""
    
    metrics = ['f1', 'accuracy', 'precision', 'recall', 'auc']
    metric_labels = ['F1 Score', 'Accuracy', 'Precision', 'Recall', 'AUC']
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    
    # Group by ratio
    ratios = {}
    for r in results:
        ratio = r['ratio']
        if ratio not in ratios:
            ratios[ratio] = {'focal': {}, 'cross_entropy': {}}
        for metric in metrics:
            ratios[ratio][r['loss_type']][metric] = r.get(metric, 0)
    
    ratio_names = list(ratios.keys())
    x = np.arange(len(ratio_names))
    width = 0.35
    
    for idx, (metric, label) in enumerate(zip(metrics, metric_labels)):
        ax = axes[idx]
        
        focal_values = [ratios[r]['focal'].get(metric, 0) for r in ratio_names]
        ce_values = [ratios[r]['cross_entropy'].get(metric, 0) for r in ratio_names]
        
        bars1 = ax.bar(x - width/2, focal_values, width, label='Focal', color='#2E86AB')
        bars2 = ax.bar(x + width/2, ce_values, width, label='Cross-Entropy', color='#A23B72')
        
        ax.set_ylabel(label, fontsize=11, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(ratio_names, rotation=15, ha='right', fontsize=9)
        ax.legend(fontsize=9)
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim([0, 1.1])
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=7)
    
    # Remove extra subplot
    fig.delaxes(axes[5])
    
    plt.suptitle('Classification Metrics Comparison', fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    return fig_to_base64(fig)


def create_radar_chart(results, ratio_name):
    """Create radar chart for a specific ratio comparing both loss types."""
    if not HAS_PLOTTING:
        return ""
    
    # Find results for this ratio
    focal_result = next((r for r in results if r['ratio'] == ratio_name and r['loss_type'] == 'focal'), None)
    ce_result = next((r for r in results if r['ratio'] == ratio_name and r['loss_type'] == 'cross_entropy'), None)
    
    if not focal_result or not ce_result:
        return ""
    
    categories = ['F1', 'Accuracy', 'Precision', 'Recall', 'AUC']
    
    focal_values = [
        focal_result.get('f1', 0),
        focal_result.get('accuracy', 0),
        focal_result.get('precision', 0),
        focal_result.get('recall', 0),
        focal_result.get('auc', 0)
    ]
    
    ce_values = [
        ce_result.get('f1', 0),
        ce_result.get('accuracy', 0),
        ce_result.get('precision', 0),
        ce_result.get('recall', 0),
        ce_result.get('auc', 0)
    ]
    
    # Number of variables
    N = len(categories)
    
    # Compute angle for each axis
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    focal_values += focal_values[:1]
    ce_values += ce_values[:1]
    angles += angles[:1]
    
    # Create plot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    ax.plot(angles, focal_values, 'o-', linewidth=2, label='Focal Loss', color='#2E86AB')
    ax.fill(angles, focal_values, alpha=0.25, color='#2E86AB')
    
    ax.plot(angles, ce_values, 'o-', linewidth=2, label='Cross-Entropy', color='#A23B72')
    ax.fill(angles, ce_values, alpha=0.25, color='#A23B72')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylim(0, 1)
    ax.set_title(f'Metrics Comparison: {ratio_name}', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
    ax.grid(True)
    
    plt.tight_layout()
    return fig_to_base64(fig)


def create_winner_table(results):
    """Determine which loss function wins for each metric and ratio."""
    comparisons = []
    
    # Group by ratio
    ratios = {}
    for r in results:
        ratio = r['ratio']
        if ratio not in ratios:
            ratios[ratio] = {'focal': {}, 'cross_entropy': {}}
        ratios[ratio][r['loss_type']] = r
    
    for ratio_name, loss_types in ratios.items():
        focal = loss_types['focal']
        ce = loss_types['cross_entropy']
        
        comparison = {
            'ratio': ratio_name,
            'val_loss': '✓ Focal' if focal['validation_loss'] < ce['validation_loss'] else '✓ Cross-Entropy',
            'f1': '✓ Focal' if focal.get('f1', 0) > ce.get('f1', 0) else '✓ Cross-Entropy',
            'accuracy': '✓ Focal' if focal.get('accuracy', 0) > ce.get('accuracy', 0) else '✓ Cross-Entropy',
            'precision': '✓ Focal' if focal.get('precision', 0) > ce.get('precision', 0) else '✓ Cross-Entropy',
            'recall': '✓ Focal' if focal.get('recall', 0) > ce.get('recall', 0) else '✓ Cross-Entropy',
            'auc': '✓ Focal' if focal.get('auc', 0) > ce.get('auc', 0) else '✓ Cross-Entropy',
        }
        comparisons.append(comparison)
    
    return comparisons


def generate_html_report(results_path, output_path):
    """Generate comprehensive HTML report."""
    
    # Load results
    data = load_results(results_path)
    results = data.get('results', data if isinstance(data, list) else [])
    timestamp = data.get('timestamp', 'Unknown') if isinstance(data, dict) else datetime.now().isoformat()
    
    # Generate visualizations
    print("Generating visualizations...")
    loss_chart = create_loss_comparison_chart(results)
    loss_curves = create_loss_curves(results)
    metrics_chart = create_metrics_comparison_chart(results)
    
    # Create radar charts for each ratio
    ratios = list(set(r['ratio'] for r in results))
    radar_charts = {ratio: create_radar_chart(results, ratio) for ratio in ratios}
    
    # Create winner comparison
    winner_table = create_winner_table(results)
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Focal Loss Comparison Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #2E86AB 0%, #1B4965 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #2E86AB;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #2E86AB;
        }}
        
        .subsection-title {{
            font-size: 1.4em;
            color: #1B4965;
            margin: 30px 0 15px 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        thead {{
            background: linear-gradient(135deg, #2E86AB 0%, #1B4965 100%);
            color: white;
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        
        tbody tr:hover {{
            background-color: #f5f9ff;
            transition: background-color 0.3s;
        }}
        
        tbody tr:last-child td {{
            border-bottom: none;
        }}
        
        .focal-row {{
            background-color: #e3f2fd;
        }}
        
        .ce-row {{
            background-color: #fce4ec;
        }}
        
        .metric-good {{
            color: #2e7d32;
            font-weight: bold;
        }}
        
        .metric-bad {{
            color: #c62828;
            font-weight: bold;
        }}
        
        .metric-neutral {{
            color: #666;
        }}
        
        .chart-container {{
            margin: 30px 0;
            text-align: center;
            background: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .stat-card h3 {{
            font-size: 2.5em;
            margin-bottom: 5px;
        }}
        
        .stat-card p {{
            font-size: 0.9em;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .winner-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .winner-focal {{
            background: #2E86AB;
            color: white;
        }}
        
        .winner-ce {{
            background: #A23B72;
            color: white;
        }}
        
        .summary-box {{
            background: #f0f7ff;
            border-left: 4px solid #2E86AB;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        
        .summary-box h3 {{
            color: #2E86AB;
            margin-bottom: 10px;
        }}
        
        .summary-box ul {{
            margin-left: 20px;
        }}
        
        .summary-box li {{
            margin: 8px 0;
        }}
        
        footer {{
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        .radar-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin: 30px 0;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 Focal Loss vs Cross-Entropy</h1>
            <h2>Comprehensive Comparison Report</h2>
            <p>Generated: {timestamp}</p>
        </header>
        
        <div class="content">
            <!-- Executive Summary -->
            <div class="section">
                <h2 class="section-title">📊 Executive Summary</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>{len(results)}</h3>
                        <p>Total Tests</p>
                    </div>
                    <div class="stat-card">
                        <h3>{len(ratios)}</h3>
                        <p>Class Ratios</p>
                    </div>
                    <div class="stat-card">
                        <h3>2</h3>
                        <p>Loss Functions</p>
                    </div>
                    <div class="stat-card">
                        <h3>{max(r.get('epochs', 0) for r in results)}</h3>
                        <p>Max Epochs</p>
                    </div>
                </div>
            </div>
            
            <!-- Winner Comparison -->
            <div class="section">
                <h2 class="section-title">🏆 Winner by Metric</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Ratio</th>
                            <th>Val Loss<br><span style="font-weight:normal;font-size:0.8em">(lower better)</span></th>
                            <th>F1 Score</th>
                            <th>Accuracy</th>
                            <th>Precision</th>
                            <th>Recall</th>
                            <th>AUC</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    
    # Add winner rows
    for comp in winner_table:
        html += f"""                        <tr>
                            <td><strong>{comp['ratio']}</strong></td>
                            <td><span class="winner-badge winner-{'focal' if 'Focal' in comp['val_loss'] else 'ce'}">{comp['val_loss']}</span></td>
                            <td><span class="winner-badge winner-{'focal' if 'Focal' in comp['f1'] else 'ce'}">{comp['f1']}</span></td>
                            <td><span class="winner-badge winner-{'focal' if 'Focal' in comp['accuracy'] else 'ce'}">{comp['accuracy']}</span></td>
                            <td><span class="winner-badge winner-{'focal' if 'Focal' in comp['precision'] else 'ce'}">{comp['precision']}</span></td>
                            <td><span class="winner-badge winner-{'focal' if 'Focal' in comp['recall'] else 'ce'}">{comp['recall']}</span></td>
                            <td><span class="winner-badge winner-{'focal' if 'Focal' in comp['auc'] else 'ce'}">{comp['auc']}</span></td>
                        </tr>
"""
    
    html += """                    </tbody>
                </table>
            </div>
            
            <!-- Detailed Results -->
            <div class="section">
                <h2 class="section-title">📈 Detailed Results</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Ratio</th>
                            <th>Loss Type</th>
                            <th>Val Loss</th>
                            <th>F1</th>
                            <th>Accuracy</th>
                            <th>Precision</th>
                            <th>Recall</th>
                            <th>AUC</th>
                            <th>Epochs</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    
    # Add detailed result rows
    for r in results:
        row_class = "focal-row" if r['loss_type'] == 'focal' else "ce-row"
        html += f"""                        <tr class="{row_class}">
                            <td><strong>{r['ratio']}</strong></td>
                            <td><strong>{r['loss_type'].replace('_', ' ').title()}</strong></td>
                            <td>{r['validation_loss']:.4f}</td>
                            <td>{r.get('f1', 0):.3f}</td>
                            <td>{r.get('accuracy', 0):.3f}</td>
                            <td>{r.get('precision', 0):.3f}</td>
                            <td>{r.get('recall', 0):.3f}</td>
                            <td>{r.get('auc', 0):.3f}</td>
                            <td>{r.get('epochs', 'N/A')}</td>
                        </tr>
"""
    
    html += """                    </tbody>
                </table>
            </div>
"""
    
    # Add charts
    if HAS_PLOTTING and loss_curves:
        html += f"""
            <!-- Loss Curves -->
            <div class="section">
                <h2 class="section-title">📈 Training & Validation Loss Curves</h2>
                <div class="chart-container">
                    <img src="{loss_curves}" alt="Loss Curves Over Time">
                </div>
                <p style="text-align: center; color: #666; font-style: italic; margin-top: 10px;">
                    Solid lines = Validation Loss (what matters for model selection)<br>
                    Dashed lines = Training Loss (lighter, for reference)<br>
                    Lower is better. Watch for divergence (overfitting indicator).
                </p>
            </div>
"""
    
    if HAS_PLOTTING and loss_chart:
        html += f"""
            <!-- Loss Comparison Chart -->
            <div class="section">
                <h2 class="section-title">📉 Final Validation Loss Comparison</h2>
                <div class="chart-container">
                    <img src="{loss_chart}" alt="Loss Comparison">
                </div>
            </div>
"""
    
    if HAS_PLOTTING and metrics_chart:
        html += f"""
            <!-- Metrics Comparison Chart -->
            <div class="section">
                <h2 class="section-title">📊 All Metrics Comparison</h2>
                <div class="chart-container">
                    <img src="{metrics_chart}" alt="Metrics Comparison">
                </div>
            </div>
"""
    
    # Add radar charts
    if HAS_PLOTTING and any(radar_charts.values()):
        html += """
            <!-- Radar Charts -->
            <div class="section">
                <h2 class="section-title">🎯 Radar Chart Analysis</h2>
                <div class="radar-grid">
"""
        for ratio, chart in radar_charts.items():
            if chart:
                html += f"""                    <div class="chart-container">
                        <img src="{chart}" alt="Radar Chart for {ratio}">
                    </div>
"""
        html += """                </div>
            </div>
"""
    
    # Key Findings
    html += """
            <!-- Key Findings -->
            <div class="section">
                <h2 class="section-title">🔍 Key Findings</h2>
                <div class="summary-box">
                    <h3>Performance Highlights:</h3>
                    <ul>
"""
    
    # Calculate focal wins
    focal_wins = sum(1 for comp in winner_table for metric in ['val_loss', 'f1', 'accuracy', 'precision', 'recall', 'auc'] if 'Focal' in comp[metric])
    total_comparisons = len(winner_table) * 6
    focal_win_pct = (focal_wins / total_comparisons) * 100
    
    html += f"""                        <li><strong>Focal Loss won {focal_wins} out of {total_comparisons} metric comparisons ({focal_win_pct:.1f}%)</strong></li>
"""
    
    # Find best performers
    best_f1 = max(results, key=lambda x: x.get('f1', 0))
    worst_loss = min(results, key=lambda x: x['validation_loss'])
    best_auc = max(results, key=lambda x: x.get('auc', 0))
    
    html += f"""                        <li>Best F1 Score: <strong>{best_f1.get('f1', 0):.3f}</strong> ({best_f1['loss_type']} on {best_f1['ratio']})</li>
                        <li>Lowest Validation Loss: <strong>{worst_loss['validation_loss']:.4f}</strong> ({worst_loss['loss_type']} on {worst_loss['ratio']})</li>
                        <li>Best AUC: <strong>{best_auc.get('auc', 0):.3f}</strong> ({best_auc['loss_type']} on {best_auc['ratio']})</li>
"""
    
    html += """                    </ul>
                </div>
                
                <div class="summary-box">
                    <h3>Observations by Class Imbalance:</h3>
                    <ul>
"""
    
    # Analyze by ratio
    for ratio in ratios:
        ratio_results = [r for r in results if r['ratio'] == ratio]
        focal = next(r for r in ratio_results if r['loss_type'] == 'focal')
        ce = next(r for r in ratio_results if r['loss_type'] == 'cross_entropy')
        
        loss_diff_pct = ((ce['validation_loss'] - focal['validation_loss']) / ce['validation_loss']) * 100
        f1_diff = focal.get('f1', 0) - ce.get('f1', 0)
        
        html += f"""                        <li><strong>{ratio}:</strong> Focal loss is {abs(loss_diff_pct):.1f}% {'lower' if loss_diff_pct > 0 else 'higher'} than cross-entropy (Val Loss). F1 score {'improved' if f1_diff > 0 else 'decreased'} by {abs(f1_diff):.3f}.</li>
"""
    
    html += """                    </ul>
                </div>
                
                <div class="summary-box">
                    <h3>Recommendations:</h3>
                    <ul>
"""
    
    if focal_win_pct > 60:
        html += """                        <li>✅ <strong>Focal Loss is recommended</strong> - Shows consistent improvements across most metrics and class ratios</li>
"""
    elif focal_win_pct > 40:
        html += """                        <li>⚠️ <strong>Results are mixed</strong> - Consider the specific metric priorities for your use case</li>
"""
    else:
        html += """                        <li>⚠️ <strong>Cross-Entropy performed better</strong> - Focal loss may not provide benefits for this dataset</li>
"""
    
    # Check for extreme imbalance handling
    extreme_ratios = [r for r in ratios if '90/10' in r or '10/90' in r]
    if extreme_ratios:
        for ratio in extreme_ratios:
            ratio_focal = next(r for r in results if r['ratio'] == ratio and r['loss_type'] == 'focal')
            ratio_ce = next(r for r in results if r['ratio'] == ratio and r['loss_type'] == 'cross_entropy')
            
            if ratio_focal['validation_loss'] < ratio_ce['validation_loss']:
                html += f"""                        <li>✅ Focal loss shows particular strength on extreme imbalance ({ratio})</li>
"""
            break
    
    html += """                        <li>📊 Always validate on held-out test data before production deployment</li>
                        <li>🔍 Consider ensemble methods combining both loss functions for robust performance</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <footer>
            <p>Report generated by Featrix Sphere QA System</p>
            <p>For questions or issues, please contact the ML engineering team</p>
        </footer>
    </div>
</body>
</html>
"""
    
    # Write report
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"\n✅ Report generated successfully: {output_path}")
    print(f"📊 Analyzed {len(results)} test results across {len(ratios)} class ratios")
    print(f"🏆 Focal Loss win rate: {focal_win_pct:.1f}%")


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
            print("Error: No results file found. Please provide path as argument.")
            print("Usage: python3 generate_focal_report.py [results.json] [output.html]")
            sys.exit(1)
    
    # Determine output file
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])
    else:
        output_path = script_dir / "focal_comparison_report.html"
    
    print(f"📖 Reading results from: {results_path}")
    print(f"📝 Writing report to: {output_path}")
    
    if not results_path.exists():
        print(f"Error: Results file not found: {results_path}")
        sys.exit(1)
    
    generate_html_report(results_path, output_path)
    
    print(f"\n🌐 Open in browser: file://{output_path.absolute()}")


if __name__ == "__main__":
    main()

