#!/usr/bin/env python3
"""
Example API Usage

Simple examples of how to use the Featrix Sphere API client
for common tasks and workflows.
"""

from pathlib import Path
from test_api_client import FeatrixSphereClient


def example_1_basic_session():
    """Example 1: Create a session and check its status."""
    
    print("=== Example 1: Basic Session Management ===")
    
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    try:
        # Create a new session
        session = client.create_session("sphere")
        print(f"Created session: {session.session_id}")
        
        # Check session status
        status = client.get_session_status(session.session_id)
        print(f"Session status: {status.status}")
        print(f"Session type: {status.session_type}")
        print(f"Jobs: {len(status.jobs)}")
    except Exception as e:
        print(f"Server error - {e}")


def example_2_file_upload():
    """Example 2: Upload a file and create a session."""
    
    print("\n=== Example 2: File Upload ===")
    
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    # Upload a file (modify path as needed)
    test_file = Path("featrix_data/test.csv")
    
    if test_file.exists():
        try:
            session = client.upload_file_and_create_session(test_file)
            print(f"File uploaded, session created: {session.session_id}")
            
            # Monitor progress briefly
            status = client.get_session_status(session.session_id)
            print(f"Initial status: {status.status}")
        except Exception as e:
            print(f"Upload error - this would upload: {test_file}")
    else:
        print(f"Test file not found: {test_file}")
        print("This would upload a CSV file and create a session")


def example_3_make_prediction():
    """Example 3: Make a prediction (requires trained predictor)."""
    
    print("\n=== Example 3: Making Predictions ===")
    
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    # You would replace this with a real session ID that has a trained predictor
    session_id = "your-session-id-here"
    
    # Example query record
    query_record = {
        "column1": "some_value",
        "column2": 42.0,
        "column3": "another_value"
    }
    
    try:
        # This will fail unless you have a real session with a trained predictor
        prediction = client.make_prediction(session_id, query_record)
        print(f"Prediction: {prediction}")
    except Exception as e:
        print(f"Prediction failed (expected if no real session): {e}")


def example_4_encoding_and_search():
    """Example 4: Encode records and perform similarity search."""
    
    print("\n=== Example 4: Encoding and Similarity Search ===")
    
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    # You would replace this with a real session ID
    session_id = "your-session-id-here"
    
    query_record = {
        "feature1": "example",
        "feature2": 123.45
    }
    
    try:
        # Encode a record
        encoding = client.encode_records(session_id, query_record)
        print(f"Encoding dimension: {len(encoding.get('embedding', []))}")
        
        # Find similar records
        similar = client.similarity_search(session_id, query_record, k=5)
        print(f"Found {len(similar.get('results', []))} similar records")
        
    except Exception as e:
        print(f"Encoding/search failed (expected if no real session): {e}")


def example_5_monitor_training():
    """Example 5: Monitor training progress."""
    
    print("\n=== Example 5: Training Monitoring ===")
    
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    # You would replace this with a real session ID
    session_id = "your-session-id-here"
    
    try:
        # Check current status
        status = client.get_session_status(session_id)
        print(f"Session status: {status.status}")
        
        # Print job details
        for job_id, job in status.jobs.items():
            job_type = job.get('type', 'unknown')
            job_status = job.get('status', 'unknown')
            progress = job.get('progress')
            
            if progress is not None:
                print(f"  {job_type}: {job_status} ({progress*100:.1f}%)")
            else:
                print(f"  {job_type}: {job_status}")
        
        # If training is complete, get metrics
        if status.status == 'done':
            try:
                metrics = client.get_training_metrics(session_id)
                print("Training metrics retrieved successfully")
            except Exception as e:
                print(f"No training metrics available: {e}")
    
    except Exception as e:
        print(f"Status check failed (expected if no real session): {e}")


def example_6_complete_workflow():
    """Example 6: Complete workflow simulation."""
    
    print("\n=== Example 6: Complete Workflow (Simulation) ===")
    
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    print("This example shows the complete workflow:")
    print("1. Upload data → Create session")
    print("2. Wait for training completion")
    print("3. Make predictions")
    print("4. Get training metrics")
    print("5. Perform similarity search")
    
    print("\nTo run this for real:")
    print("1. Use the remote API server: https://sphere-api.featrix.com")
    print("2. Create a predictor session via CLI:")
    print("   python cli.py create-predictor-session --target-column 'your_target' --target-column-type 'set'")
    print("3. Run the test_single_predictor_api.py script")


def main():
    """Run all examples."""
    
    print("Featrix Sphere API Client Examples")
    print("=" * 40)
    
    # Run examples that don't require a real session
    example_1_basic_session()
    example_2_file_upload()
    
    # Show examples that would work with real sessions
    example_3_make_prediction()
    example_4_encoding_and_search()
    example_5_monitor_training()
    example_6_complete_workflow()
    
    print("\n" + "=" * 40)
    print("Examples completed!")
    print("\nTo test with real data:")
    print("1. Start the API server")
    print("2. Use test_single_predictor_api.py for end-to-end testing")


if __name__ == "__main__":
    main() 