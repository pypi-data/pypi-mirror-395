#!/usr/bin/env python3
"""
Enhanced focal loss comparison test with comprehensive metrics.

Tracks:
- All standard metrics (F1, Acc, Prec, Rec, AUC)
- Best epoch information
- Confusion matrix details (TP, FP, TN, FN)
- Specificity, MCC, Balanced Accuracy
- PR-AUC (Precision-Recall curve)
- Optimal threshold
- Training loss at best epoch
- Brier score (calibration)
"""
import sys
import os
import json
import asyncio
import time
from pathlib import Path
from datetime import datetime
import numpy as np

# Paths
test_dir = Path(__file__).parent
neural_dir = test_dir.parent
featrix_dir = neural_dir.parent
lib_dir = featrix_dir.parent
src_dir = lib_dir.parent

sys.path.insert(0, str(lib_dir))
sys.path.insert(0, str(src_dir))

from featrix.neural.input_data_file import FeatrixInputDataFile
from featrix.neural.embedded_space import EmbeddingSpace
from featrix.neural.input_data_set import FeatrixInputDataSet
from featrix.neural.single_predictor import FeatrixSinglePredictor
from featrix.neural.simple_mlp import SimpleMLP
from featrix.neural.model_config import SimpleMLPConfig
from featrix.neural.device import set_device_cpu
import pandas as pd

set_device_cpu()

print("=" * 80)
print("ENHANCED FOCAL LOSS COMPARISON TEST")
print("=" * 80)
print(f"Started: {datetime.now()}")
print()

# Load data
data_file = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "qa_data" / "credit_g_31.csv"
input_file = FeatrixInputDataFile(str(data_file))
df = input_file.df

# Create datasets
def create_dataset(df, pos_count, neg_count, pos_label="good"):
    """
    Sample specific counts WITHOUT replacement.
    
    Args:
        df: Source dataframe
        pos_count: Number of positive class samples
        neg_count: Number of negative class samples
        pos_label: Which label to treat as positive ("good" or "bad")
    """
    neg_label = "bad" if pos_label == "good" else "good"
    pos = df[df["target"] == pos_label].sample(n=pos_count, random_state=42, replace=False)
    neg = df[df["target"] == neg_label].sample(n=neg_count, random_state=42, replace=False)
    return pd.concat([pos, neg]).sample(frac=1, random_state=42).reset_index(drop=True)

def compute_enhanced_metrics(y_true, y_pred, y_prob, pos_label="good"):
    """
    Compute comprehensive metrics beyond what's in the training loop.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        y_prob: Predicted probabilities for positive class
        pos_label: Label for positive class
    
    Returns:
        Dict of additional metrics
    """
    from sklearn.metrics import (
        confusion_matrix, matthews_corrcoef, 
        balanced_accuracy_score, average_precision_score,
        brier_score_loss, roc_curve
    )
    
    # Convert to binary
    y_true_binary = [1 if y == pos_label else 0 for y in y_true]
    y_pred_binary = [1 if y == pos_label else 0 for y in y_pred]
    
    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(y_true_binary, y_pred_binary).ravel()
    
    # Specificity (True Negative Rate)
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    # Matthews Correlation Coefficient (good for imbalanced data)
    mcc = matthews_corrcoef(y_true_binary, y_pred_binary)
    
    # Balanced Accuracy
    balanced_acc = balanced_accuracy_score(y_true_binary, y_pred_binary)
    
    # Precision-Recall AUC (often better than ROC-AUC for imbalanced)
    pr_auc = average_precision_score(y_true_binary, y_prob)
    
    # Brier Score (calibration quality - lower is better)
    brier = brier_score_loss(y_true_binary, y_prob)
    
    # Find optimal threshold using Youden's J statistic
    fpr, tpr, thresholds = roc_curve(y_true_binary, y_prob)
    j_scores = tpr - fpr
    optimal_idx = np.argmax(j_scores)
    optimal_threshold = thresholds[optimal_idx]
    
    return {
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn),
        "specificity": float(specificity),
        "mcc": float(mcc),
        "balanced_accuracy": float(balanced_acc),
        "pr_auc": float(pr_auc),
        "brier_score": float(brier),
        "optimal_threshold": float(optimal_threshold),
        "sensitivity": float(tp / (tp + fn)) if (tp + fn) > 0 else 0,  # same as recall
    }

# Configurations: (pos_count, neg_count, name, pos_label)
# pos_label indicates which class is treated as "positive" for metrics
configs = [
    (300, 300, "50/50 Balanced", "good"),
    (225, 75, "75/25 (good pos)", "good"),
    (270, 30, "90/10 Extreme (good pos)", "good"),
    (75, 225, "25/75 (bad pos)", "bad"),  # Inverted: bad is minority
    (30, 270, "10/90 Extreme (bad pos)", "bad"),  # Inverted: bad is minority
]

loss_types = ["focal", "cross_entropy"]
results = []

# Train ES once
print("Training ES (100 epochs)...")
dataset = FeatrixInputDataSet(df=df, ignore_cols=[], limit_rows=None, encoder_overrides=None)
train_data, val_data = dataset.split(fraction=0.2)
es = EmbeddingSpace(train_data, val_data, n_epochs=100, d_model=128, output_debug_label="focal_comp_enh")
es.train(batch_size=128, n_epochs=100)
print("ES complete\n")

test_num = 0
total_tests = len(configs) * len(loss_types)

for pos_count, neg_count, ratio_name, pos_label in configs:
    print("=" * 80)
    print(f"RATIO: {ratio_name} ({pos_count} {pos_label} / {neg_count} {'bad' if pos_label == 'good' else 'good'})")
    print("=" * 80)
    
    balanced_df = create_dataset(df, pos_count, neg_count, pos_label=pos_label)
    
    for loss_type in loss_types:
        test_num += 1
        print(f"  [{test_num}/{total_tests}] {loss_type} (75 epochs)...", end=" ", flush=True)
        
        # Track timing and best metrics across all epochs - use a dict so we can modify in callback
        training_state = {
            "training_start_time": time.time(),
            "best_val_loss": float('inf'),
            "best_epoch": 0,
            "best_metrics": None,
            "best_train_loss": None,
            "best_epoch_time": None,
            "epoch_history": [],
            "epoch_times": [],
            "last_epoch_completed": 0,
            "stopped_early": False,
            "early_stop_epoch": None,
        }
        
        # Callback to track progress
        def track_progress(progress):
            epoch = progress.get("epoch", 0)
            total_epochs = progress.get("total_epochs", 75)
            train_loss = progress.get("training_loss", 0)
            val_loss = progress.get("validation_loss", 0)
            metrics = progress.get("metrics", {})
            
            # Track epoch timing
            epoch_start = training_state["epoch_times"][-1] if training_state["epoch_times"] else training_state["training_start_time"]
            current_time = time.time()
            epoch_duration = current_time - epoch_start
            training_state["epoch_times"].append(current_time)
            
            # Track this epoch
            training_state["epoch_history"].append({
                "epoch": epoch,
                "train_loss": train_loss,
                "val_loss": val_loss,
                "metrics": metrics.copy() if metrics else {},
                "epoch_duration": epoch_duration,
                "elapsed_time": current_time - training_state["training_start_time"]
            })
            
            # Check if this is the best epoch
            if val_loss < training_state["best_val_loss"]:
                training_state["best_val_loss"] = val_loss
                training_state["best_epoch"] = epoch
                training_state["best_metrics"] = metrics.copy() if metrics else {}
                training_state["best_train_loss"] = train_loss
                training_state["best_epoch_time"] = current_time - training_state["training_start_time"]
            
            training_state["last_epoch_completed"] = epoch
            
            if epoch % 10 == 0:
                f1 = metrics.get("f1", 0) if metrics else 0
                avg_epoch_time = np.mean([e["epoch_duration"] for e in training_state["epoch_history"][-10:]])
                print(f"\n    Epoch {epoch}/{total_epochs}: train_loss={train_loss:.3f}, val_loss={val_loss:.3f}, F1={f1:.3f} [best={training_state['best_epoch']}, {avg_epoch_time:.1f}s/ep]", end="", flush=True)
        
        try:
            config = SimpleMLPConfig(d_in=128, d_out=2, d_hidden=256, n_hidden_layers=2, dropout=0.1, normalize=False, residual=True, use_batch_norm=True)
            predictor = SimpleMLP(config)
            fsp = FeatrixSinglePredictor(es, predictor)
            
            fsp.prep_for_training(train_df=balanced_df, target_col_name="target", target_col_type="set", use_class_weights=False, loss_type=loss_type)
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            training_results = loop.run_until_complete(fsp.train(
                n_epochs=75, 
                batch_size=128, 
                fine_tune=False, 
                val_pos_label=pos_label,
                print_callback=track_progress,
                print_progress_step=10
            ))
            loop.close()
            
            training_end_time = time.time()
            total_training_time = training_end_time - training_state["training_start_time"]
            
            # Check if training stopped early
            if training_state["last_epoch_completed"] < 74:  # 74 because epochs are 0-indexed
                training_state["stopped_early"] = True
                training_state["early_stop_epoch"] = training_state["last_epoch_completed"]
            
            if training_results and len(training_results) > 0:
                # Get predictions for enhanced metrics
                # We'll use the final model (which should be the best due to checkpointing)
                val_data_df = balanced_df.sample(frac=0.2, random_state=42)
                val_queries = [row.to_dict() for _, row in val_data_df.iterrows()]
                val_ground_truth = val_data_df["target"].tolist()
                
                # Get predictions and probabilities
                predictions = []
                probabilities = []
                for q in val_queries:
                    q_copy = q.copy()
                    q_copy.pop("target", None)
                    pred = fsp.predict(q_copy, ignore_unknown=True)
                    if isinstance(pred, dict):
                        predictions.append(max(pred, key=pred.get))
                        probabilities.append(pred.get(pos_label, 0))
                
                # Compute enhanced metrics
                enhanced = compute_enhanced_metrics(
                    val_ground_truth, 
                    predictions, 
                    probabilities,
                    pos_label=pos_label
                )
                
                # Compute train/val gap
                train_val_gap = abs(training_state["best_train_loss"] - training_state["best_val_loss"]) if training_state["best_train_loss"] is not None else None
                
                # Compute timing statistics
                avg_epoch_time = np.mean([e["epoch_duration"] for e in training_state["epoch_history"]]) if training_state["epoch_history"] else None
                median_epoch_time = np.median([e["epoch_duration"] for e in training_state["epoch_history"]]) if training_state["epoch_history"] else None
                
                # Extract loss history for curves
                loss_history = {
                    "epochs": [r.get("epoch", i) for i, r in enumerate(training_results)],
                    "train_loss": [r.get("training_loss") for r in training_results],
                    "val_loss": [r.get("validation_loss") for r in training_results],
                }
                
                result_entry = {
                    # Basic info
                    "ratio": ratio_name,
                    "pos_count": pos_count,
                    "neg_count": neg_count,
                    "pos_label": pos_label,
                    "loss_type": loss_type,
                    "total_epochs": 75,
                    
                    # Timing info
                    "total_training_time_secs": round(total_training_time, 2),
                    "avg_epoch_time_secs": round(avg_epoch_time, 2) if avg_epoch_time else None,
                    "median_epoch_time_secs": round(median_epoch_time, 2) if median_epoch_time else None,
                    "time_to_best_epoch_secs": round(training_state["best_epoch_time"], 2) if training_state["best_epoch_time"] else None,
                    "stopped_early": training_state["stopped_early"],
                    "early_stop_epoch": training_state["early_stop_epoch"],
                    "epochs_completed": training_state["last_epoch_completed"] + 1,  # +1 because 0-indexed
                    
                    # Best epoch info
                    "best_epoch": training_state["best_epoch"],
                    "best_train_loss": training_state["best_train_loss"],
                    "best_val_loss": training_state["best_val_loss"],
                    "train_val_gap": train_val_gap,
                    
                    # Standard metrics from best epoch
                    "accuracy": training_state["best_metrics"].get("accuracy") if training_state["best_metrics"] else None,
                    "f1": training_state["best_metrics"].get("f1") if training_state["best_metrics"] else None,
                    "precision": training_state["best_metrics"].get("precision") if training_state["best_metrics"] else None,
                    "recall": training_state["best_metrics"].get("recall") if training_state["best_metrics"] else None,
                    "auc": training_state["best_metrics"].get("auc") if training_state["best_metrics"] else None,
                    
                    # Enhanced metrics
                    "tp": enhanced["tp"],
                    "fp": enhanced["fp"],
                    "tn": enhanced["tn"],
                    "fn": enhanced["fn"],
                    "specificity": enhanced["specificity"],
                    "sensitivity": enhanced["sensitivity"],
                    "mcc": enhanced["mcc"],
                    "balanced_accuracy": enhanced["balanced_accuracy"],
                    "pr_auc": enhanced["pr_auc"],
                    "brier_score": enhanced["brier_score"],
                    "optimal_threshold": enhanced["optimal_threshold"],
                    
                    # Loss history for curves
                    "loss_history": loss_history,
                }
                
                results.append(result_entry)
                
                # Print summary
                early_stop_msg = f" (STOPPED EARLY at epoch {training_state['early_stop_epoch']})" if training_state["stopped_early"] else ""
                print(f" ✓ Best: Epoch {training_state['best_epoch']}/{training_state['last_epoch_completed']}, Val Loss={training_state['best_val_loss']:.3f}, F1={result_entry['f1']:.3f}, MCC={result_entry['mcc']:.3f}")
                print(f"    Time: {total_training_time:.1f}s total ({avg_epoch_time:.1f}s/epoch avg, {training_state['best_epoch_time']:.1f}s to best){early_stop_msg}")
            else:
                print("NO RESULTS")
                
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print()

# Save
output_file = test_dir / "focal_comparison_enhanced_results.json"
with open(output_file, "w") as f:
    json.dump({"timestamp": datetime.now().isoformat(), "results": results}, f, indent=2)

print("=" * 80)
print("ENHANCED RESULTS")
print("=" * 80)
print()

# Print table with key metrics
print("Core Metrics:")
print(f"{'Ratio':<22} | {'Loss':<13} | {'BestEp':<7} | {'ValLoss':<7} | {'F1':<6} | {'Acc':<6} | {'Prec':<6} | {'Rec':<6} | {'AUC':<6}")
print("-" * 120)
for r in results:
    print(f"{r['ratio']:<22} | {r['loss_type']:<13} | {r['best_epoch']:<7} | {r['best_val_loss']:<7.3f} | {r['f1']:<6.3f} | {r['accuracy']:<6.3f} | {r['precision']:<6.3f} | {r['recall']:<6.3f} | {r['auc']:<6.3f}")

print()
print("Timing Metrics:")
print(f"{'Ratio':<22} | {'Loss':<13} | {'Total(s)':<8} | {'Avg/Ep(s)':<9} | {'ToBest(s)':<10} | {'EpDone':<7} | {'Early?':<7}")
print("-" * 110)
for r in results:
    early_mark = "YES" if r['stopped_early'] else "NO"
    print(f"{r['ratio']:<22} | {r['loss_type']:<13} | {r['total_training_time_secs']:<8.1f} | {r['avg_epoch_time_secs']:<9.2f} | {r['time_to_best_epoch_secs']:<10.1f} | {r['epochs_completed']:<7} | {early_mark:<7}")

print()
print("Enhanced Metrics:")
print(f"{'Ratio':<22} | {'Loss':<13} | {'MCC':<6} | {'BalAcc':<6} | {'Spec':<6} | {'PR-AUC':<7} | {'Brier':<6} | {'Thresh':<6}")
print("-" * 110)
for r in results:
    print(f"{r['ratio']:<22} | {r['loss_type']:<13} | {r['mcc']:<6.3f} | {r['balanced_accuracy']:<6.3f} | {r['specificity']:<6.3f} | {r['pr_auc']:<7.3f} | {r['brier_score']:<6.3f} | {r['optimal_threshold']:<6.3f}")

print()
print("Confusion Matrix:")
print(f"{'Ratio':<22} | {'Loss':<13} | {'TP':<5} | {'FP':<5} | {'TN':<5} | {'FN':<5}")
print("-" * 80)
for r in results:
    print(f"{r['ratio']:<22} | {r['loss_type']:<13} | {r['tp']:<5} | {r['fp']:<5} | {r['tn']:<5} | {r['fn']:<5}")

print()
print(f"Saved: {output_file}")
print(f"Done: {datetime.now()}")

