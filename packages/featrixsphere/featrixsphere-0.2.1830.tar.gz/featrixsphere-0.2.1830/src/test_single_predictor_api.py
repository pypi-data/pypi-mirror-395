#!/usr/bin/env python3
"""
Single Predictor API Test

Test script for the single predictor functionality using the API client.
This demonstrates the complete workflow from session creation to making predictions.
"""

import json
import time
from pathlib import Path
from test_api_client import FeatrixSphereClient, SessionInfo


def test_single_predictor_workflow():
    """
    Test the complete single predictor workflow:
    1. Create/upload session
    2. Wait for training completion
    3. Make predictions
    4. Get training metrics
    """
    
    # Initialize client
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    print("=== Single Predictor API Test ===\n")
    
    # Test data - you can modify this based on your actual data
    test_file = Path("featrix_data/test.csv")
    
    # Sample query record for prediction (modify based on your data columns)
    sample_query = {
        "col1": "value1",
        "col2": "value2", 
        "col3": 123.45,
        # Add more columns as needed based on your test data
    }
    
    try:
        # Step 1: Upload file and create session
        print("Step 1: Creating session with data...")
        if test_file.exists():
            session_info = client.upload_file_and_create_session(test_file)
        else:
            print(f"Test file {test_file} not found, creating empty session...")
            session_info = client.create_session("sphere")
        
        session_id = session_info.session_id
        print(f"Session ID: {session_id}\n")
        
        # Step 2: Monitor training progress
        print("Step 2: Monitoring training progress...")
        print("(This will take a while - embedding space + predictor training)")
        
        final_session = client.wait_for_session_completion(
            session_id, 
            max_wait_time=3600,  # 1 hour max
            check_interval=30    # Check every 30 seconds
        )
        
        if final_session.status != 'done':
            print(f"Training did not complete successfully. Status: {final_session.status}")
            return False
        
        print("Training completed successfully!\n")
        
        # Step 3: Check if this session has a single predictor
        if 'single_predictor' not in [job.get('type') for job in final_session.jobs.values()]:
            print("This session doesn't have single predictor training.")
            print("To test single predictor, create a 'predictor' session type via CLI:")
            print("python cli.py create-predictor-session --target-column 'your_target' --target-column-type 'set'")
            return True
        
        # Step 4: Make predictions
        print("Step 3: Making predictions...")
        try:
            prediction_result = client.make_prediction(session_id, sample_query)
            print(f"Prediction successful!")
            print(f"Query: {sample_query}")
            print(f"Prediction: {prediction_result.get('prediction')}\n")
        except Exception as e:
            print(f"Prediction failed: {e}\n")
        
        # Step 5: Get training metrics
        print("Step 4: Retrieving training metrics...")
        try:
            metrics_result = client.get_training_metrics(session_id)
            training_metrics = metrics_result.get('training_metrics', {})
            
            print(f"Training metrics retrieved!")
            print(f"Target column: {training_metrics.get('target_column', 'N/A')}")
            print(f"Target type: {training_metrics.get('target_column_type', 'N/A')}")
            print(f"Final metrics: {training_metrics.get('final_metrics', {})}")
            
            # Print training history if available
            training_info = training_metrics.get('training_info', [])
            if training_info:
                print(f"Training epochs: {len(training_info)}")
                if training_info:
                    last_epoch = training_info[-1]
                    print(f"Final epoch loss: {last_epoch.get('loss', 'N/A')}")
                    print(f"Final validation loss: {last_epoch.get('validation_loss', 'N/A')}")
            
        except Exception as e:
            print(f"Failed to get training metrics: {e}")
        
        print("\nStep 5: Testing other endpoints...")
        
        # Step 6: Test embedding encoding
        try:
            encoding_result = client.encode_records(session_id, sample_query)
            embedding = encoding_result.get('embedding')
            if embedding:
                print(f"Record encoded successfully (dimension: {len(embedding)})")
        except Exception as e:
            print(f"Encoding failed: {e}")
        
        # Step 7: Test similarity search (if vector DB exists)
        try:
            similarity_result = client.similarity_search(session_id, sample_query, k=3)
            results = similarity_result.get('results', [])
            print(f"Similarity search found {len(results)} similar records")
        except Exception as e:
            print(f"Similarity search failed: {e}")
        
        print("\n=== Single Predictor Test Completed Successfully! ===")
        return True
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_session_status_only():
    """
    Quick test to just check session status for an existing session.
    Useful for testing against a session you created via CLI.
    """
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    # You can hardcode a session ID here for testing
    session_id = input("Enter session ID to check (or press Enter to skip): ").strip()
    
    if not session_id:
        print("No session ID provided, skipping status check.")
        return
    
    try:
        print(f"Checking status for session: {session_id}")
        session_info = client.get_session_status(session_id)
        
        print(f"Session Type: {session_info.session_type}")
        print(f"Status: {session_info.status}")
        print(f"Jobs: {len(session_info.jobs)}")
        
        for job_id, job in session_info.jobs.items():
            job_type = job.get('type', 'unknown')
            job_status = job.get('status', 'unknown')
            progress = job.get('progress')
            
            # Get detailed queue info for this job
            detailed_info = getattr(session_info, 'detailed_queue_info', {}).get(job_id, {})
            
            # Build status line with enhanced information
            status_line = f"  {job_type}: {job_status}"
            
            # Add queue-specific information
            if detailed_info:
                wait_message = detailed_info.get('estimated_wait_message')
                if wait_message and wait_message != "Currently running":
                    status_line += f" - {wait_message}"
            
            if progress is not None:
                # Fix percentage issue: show 100% when job is done
                progress_pct = 100.0 if job_status == 'done' else (progress * 100)
                status_line += f" ({progress_pct:.1f}%)"
            
            # Add training metrics for ES and Single Predictor jobs
            if job_type in ['train_es', 'train_single_predictor'] and job_status == 'running':
                metrics = []
                current_epoch = job.get('current_epoch')
                current_loss = job.get('current_loss')
                validation_loss = job.get('validation_loss')
                
                if current_epoch is not None:
                    metrics.append(f"Epoch {current_epoch}")
                if current_loss is not None:
                    metrics.append(f"Loss: {current_loss:.4f}")
                if validation_loss is not None:
                    metrics.append(f"Val Loss: {validation_loss:.4f}")
                
                if metrics:
                    status_line += f" - {', '.join(metrics)}"
            
            print(status_line)
            
            # Show additional queue details for waiting jobs
            if detailed_info and detailed_info.get('queue_status') == 'waiting':
                position = detailed_info.get('position_in_queue', 0)
                total_ready = detailed_info.get('total_ready_jobs', 0)
                running_jobs = detailed_info.get('currently_running_jobs', [])
                
                if position is not None:
                    print(f"    📍 Queue position: {position + 1} of {total_ready} waiting jobs")
                    
                    if running_jobs:
                        running_session = running_jobs[0].get('session_id', 'unknown')
                        print(f"    🔄 Worker busy with session: {running_session}")
                    else:
                        print(f"    ⚡ Worker available - should start soon!")
        
        # If session is done and has a predictor, try making a prediction
        if session_info.status == 'done':
            predictor_jobs = [job for job in session_info.jobs.values() 
                            if job.get('type') == 'train_single_predictor']
            if predictor_jobs:
                print("\nFound trained single predictor!")
                
                # Example prediction
                sample_query = {
                    "feature1": "example_value",
                    "feature2": 42.0,
                    # Modify based on your actual data structure
                }
                
                print(f"Making sample prediction...")
                try:
                    result = client.make_prediction(session_id, sample_query)
                    print(f"Prediction result: {result.get('prediction')}")
                except Exception as e:
                    print(f"Prediction failed: {e}")
    
    except Exception as e:
        print(f"Failed to check session status: {e}")


def main():
    """Main test function."""
    
    print("Single Predictor API Test Options:")
    print("1. Run complete workflow test (upload + train + predict)")
    print("2. Check existing session status")
    print("3. Both")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == "1":
        return test_single_predictor_workflow()
    elif choice == "2":
        test_session_status_only()
        return True
    elif choice == "3":
        test_session_status_only()
        print("\n" + "="*50 + "\n")
        return test_single_predictor_workflow()
    else:
        print("Invalid choice. Running status check only.")
        test_session_status_only()
        return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 