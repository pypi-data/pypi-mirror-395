#!/usr/bin/env python3
"""
Test piecewise_constant dropout schedule with different epoch counts.
"""
import sys
from pathlib import Path

# Add the lib directory to path
test_dir = Path(__file__).parent
neural_dir = test_dir.parent
featrix_dir = neural_dir.parent
lib_dir = featrix_dir.parent
sys.path.insert(0, str(lib_dir))

from featrix.neural.dropout_scheduler import DropoutScheduler, DropoutScheduleType

def test_piecewise_schedule(total_epochs, initial=0.5, final=0.25):
    """Test piecewise schedule for different epoch counts."""
    scheduler = DropoutScheduler(
        schedule_type=DropoutScheduleType.PIECEWISE_CONSTANT,
        initial_dropout=initial,
        final_dropout=final,
        total_epochs=total_epochs
    )
    
    print(f"\n{'='*80}")
    print(f"PIECEWISE_CONSTANT: {total_epochs} epochs ({initial} → {final})")
    print(f"{'='*80}")
    
    third = total_epochs / 3.0
    print(f"Phase 1 (epochs 0-{int(third)-1}): Hold at {initial}")
    print(f"Phase 2 (epochs {int(third)}-{int(2*third)-1}): Ramp {initial} → {final}")
    print(f"Phase 3 (epochs {int(2*third)}-{total_epochs-1}): Hold at {final}")
    print()
    
    # Sample key epochs
    key_epochs = [
        0,
        int(third) - 1,      # End of phase 1
        int(third),          # Start of phase 2
        int(2 * third) - 1,  # End of phase 2
        int(2 * third),      # Start of phase 3
        total_epochs - 1     # Last epoch
    ]
    
    print(f"{'Epoch':>6} {'Dropout':>10} {'Phase':>15}")
    print("-" * 35)
    
    for epoch in key_epochs:
        if epoch >= total_epochs:
            continue
        dropout = scheduler.get_dropout_rate(epoch)
        
        if epoch < third:
            phase = "Phase 1 (hold)"
        elif epoch < 2 * third:
            phase = "Phase 2 (ramp)"
        else:
            phase = "Phase 3 (hold)"
        
        print(f"{epoch:>6} {dropout:>10.3f} {phase:>15}")

# Test common epoch counts
print("="*80)
print("TESTING PIECEWISE_CONSTANT DROPOUT SCHEDULE")
print("="*80)

test_piecewise_schedule(30)   # Short training
test_piecewise_schedule(50)   # Standard
test_piecewise_schedule(75)   # Medium
test_piecewise_schedule(100)  # Long training
test_piecewise_schedule(150)  # Very long

print("\n" + "="*80)
print("✅ Piecewise schedule adapts automatically to any epoch count")
print("="*80)

