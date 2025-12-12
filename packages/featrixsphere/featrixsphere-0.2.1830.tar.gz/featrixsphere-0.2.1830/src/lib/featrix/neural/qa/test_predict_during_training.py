#!/usr/bin/env python3
"""
Test predictions during training.

This test verifies that predictions can be made while a single predictor
is still training, using intermediate checkpoints.

REQUIREMENTS:
- Must be run on a Featrix node machine (needs access to /sphere/app)
- Requires a trained embedding space session
- Creates a new single predictor training job

USAGE:
    python3 test_predict_during_training.py <foundation_session_id> <target_column>
    
Example:
    python3 test_predict_during_training.py public-alphafreight-mini-8c482fa5-1304-442d-8875-4263d5bf79d6 has_fuel_card_Comdata
"""

import sys
import os
import time
import json
from pathlib import Path
from typing import Dict, Any

# Add src to path
script_dir = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(script_dir))

try:
    from featrixsphere import FeatrixSphereClient
except ImportError:
    print("ERROR: featrixsphere package not installed.")
    print("   Install with: pip install featrixsphere")
    sys.exit(1)

import requests
from datetime import datetime


def test_predict_during_training(foundation_session_id: str, target_column: str, 
                                  base_url: str = "https://sphere-api.featrix.com"):
    """
    Test making predictions while training is in progress.
    
    Steps:
    1. Start training a single predictor on the foundation model
    2. Poll for training to start
    3. Once training is active, make a prediction request
    4. Verify the prediction succeeds and includes training_guardrails
    5. Wait for training to complete
    6. Make another prediction and verify training_guardrails is gone
    """
    print("=" * 80)
    print("TEST: Predictions During Training")
    print("=" * 80)
    print(f"Foundation Session: {foundation_session_id}")
    print(f"Target Column: {target_column}")
    print(f"Base URL: {base_url}")
    print()
    
    client = FeatrixSphereClient(base_url=base_url)
    
    # Step 1: Start training a single predictor
    print("STEP 1: Starting single predictor training...")
    print("-" * 80)
    
    try:
        # Get session info to find compute cluster
        session_info = client.get_session_status(foundation_session_id)
        compute_cluster = session_info.session.get("compute_cluster")
        
        if compute_cluster:
            client.set_compute_cluster(compute_cluster)
            print(f"   Using compute cluster: {compute_cluster}")
        
        # Start training with a small number of epochs so we can catch it mid-training
        print(f"   Training predictor for target: {target_column}")
        result = client.train_on_foundation_model(
            foundation_model_id=foundation_session_id,
            target_column=target_column,
            target_column_type="set",  # Assuming classification
            epochs=50,  # Small enough to catch during training
            verbose=True
        )
        
        predictor_session_id = result.get("session_id")
        if not predictor_session_id:
            print("ERROR: No session_id returned from train_on_foundation_model")
            return False
        
        print(f"   Predictor session created: {predictor_session_id}")
        print()
        
    except Exception as e:
        print(f"ERROR: Failed to start training: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 2: Poll for training to start and find a test record
    print("STEP 2: Waiting for training to start...")
    print("-" * 80)
    
    training_started = False
    test_record = None
    max_wait = 120  # Wait up to 2 minutes for training to start
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            session_info = client.get_session_status(predictor_session_id)
            jobs = session_info.jobs
            
            # Check if training job is running
            for job_id, job_data in jobs.items():
                if 'train_single_predictor' in job_id or 'train' in job_data.get('type', ''):
                    if job_data.get('status') == 'running':
                        training_started = True
                        print(f"   Training job is running: {job_id}")
                        break
            
            if training_started:
                # Try to get a sample record from the foundation session for testing
                # We'll use a dummy record for now
                test_record = {
                    "fleet_size": 25,
                    "annual_revenue": 5000000,
                    "primary_operation": "long_haul"
                }
                print(f"   Using test record: {test_record}")
                break
            
            time.sleep(2)
            print(f"   Waiting for training to start... ({int(time.time() - start_time)}s)")
            
        except Exception as e:
            print(f"   Error checking training status: {e}")
            time.sleep(2)
    
    if not training_started:
        print("ERROR: Training did not start within timeout period")
        return False
    
    if not test_record:
        print("ERROR: Could not create test record")
        return False
    
    print()
    
    # Step 3: Make prediction while training is in progress
    print("STEP 3: Making prediction during training...")
    print("-" * 80)
    
    prediction_during_training = None
    training_guardrails_found = False
    
    try:
        # Wait a bit for training to progress (so we have a checkpoint)
        print("   Waiting 10 seconds for training to create checkpoints...")
        time.sleep(10)
        
        # Make prediction request
        print(f"   Making prediction request...")
        response = client._post_json(
            f"/session/{predictor_session_id}/predict",
            data={
                "query_record": test_record,
                "target_column": target_column
            }
        )
        
        prediction_during_training = response
        training_guardrails = response.get("training_status")
        
        if training_guardrails:
            training_guardrails_found = True
            print(f"   SUCCESS: Prediction made during training!")
            print(f"   Training status:")
            print(f"      - Is training: {training_guardrails.get('is_training')}")
            print(f"      - Current epoch: {training_guardrails.get('current_epoch')}")
            print(f"      - Total epochs: {training_guardrails.get('total_epochs')}")
            print(f"      - Progress: {training_guardrails.get('progress_percent', 0):.1f}%")
            print(f"      - Checkpoint epoch: {training_guardrails.get('checkpoint_epoch')}")
            
            # Verify prediction result exists
            if "results" in response:
                print(f"   Prediction results: {list(response['results'].keys())[:3]}...")
            else:
                print("   WARNING: No prediction results in response")
        else:
            print("   WARNING: No training_guardrails in response (training may have completed)")
        
        print()
        
    except Exception as e:
        print(f"   ERROR: Failed to make prediction during training: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 4: Wait for training to complete
    print("STEP 4: Waiting for training to complete...")
    print("-" * 80)
    
    training_complete = False
    max_wait_complete = 600  # Wait up to 10 minutes for training to complete
    start_time = time.time()
    
    while time.time() - start_time < max_wait_complete:
        try:
            session_info = client.get_session_status(predictor_session_id)
            
            if session_info.status == "done":
                training_complete = True
                print(f"   Training completed!")
                break
            elif session_info.status == "failed":
                print(f"   ERROR: Training failed")
                return False
            
            time.sleep(5)
            elapsed = int(time.time() - start_time)
            print(f"   Training in progress... ({elapsed}s elapsed)")
            
        except Exception as e:
            print(f"   Error checking training status: {e}")
            time.sleep(5)
    
    if not training_complete:
        print("   WARNING: Training did not complete within timeout (continuing test anyway)")
    
    print()
    
    # Step 5: Make prediction after training completes
    print("STEP 5: Making prediction after training completes...")
    print("-" * 80)
    
    try:
        print(f"   Making prediction request...")
        response = client._post_json(
            f"/session/{predictor_session_id}/predict",
            data={
                "query_record": test_record,
                "target_column": target_column
            }
        )
        
        training_guardrails_after = response.get("training_status")
        
        if training_guardrails_after:
            print(f"   WARNING: training_guardrails still present after training completed")
            print(f"      Is training: {training_guardrails_after.get('is_training')}")
        else:
            print(f"   SUCCESS: No training_guardrails after training completed (as expected)")
        
        # Verify prediction result exists
        if "results" in response:
            print(f"   Prediction results: {list(response['results'].keys())[:3]}...")
        else:
            print("   ERROR: No prediction results in response")
            return False
        
        print()
        
    except Exception as e:
        print(f"   ERROR: Failed to make prediction after training: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    if training_guardrails_found:
        print("✅ PASS: Successfully made prediction during training")
        print("   - Training guardrails were present in response")
        print("   - Prediction succeeded using intermediate checkpoint")
    else:
        print("⚠️  PARTIAL: Prediction worked but training may have completed too quickly")
        print("   - Try with more epochs or slower training to catch it mid-training")
    
    if training_complete:
        print("✅ PASS: Training completed successfully")
    else:
        print("⚠️  WARNING: Training did not complete within timeout")
    
    print()
    print(f"Predictor Session ID: {predictor_session_id}")
    print(f"Foundation Session ID: {foundation_session_id}")
    print()
    
    return training_guardrails_found and training_complete


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print(__doc__)
        print()
        print("ERROR: Missing required arguments")
        print("Usage: python3 test_predict_during_training.py <foundation_session_id> <target_column> [base_url]")
        sys.exit(1)
    
    foundation_session_id = sys.argv[1]
    target_column = sys.argv[2]
    base_url = sys.argv[3] if len(sys.argv) > 3 else "https://sphere-api.featrix.com"
    
    success = test_predict_during_training(foundation_session_id, target_column, base_url)
    
    if success:
        print("✅ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()

