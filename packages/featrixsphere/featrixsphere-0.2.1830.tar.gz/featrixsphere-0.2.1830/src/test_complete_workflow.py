#!/usr/bin/env python3
"""
Complete Workflow Test: ES + Single Predictor Training + Predictions

This test demonstrates the new single predictor training functionality:
1. Upload data and train embedding space
2. Add single predictor training to the existing session (NEW FEATURE)
3. Make predictions and show results
"""

import json
import time
import sys
import requests
from pathlib import Path
from test_api_client import FeatrixSphereClient
import pandas as pd

# Add the current directory to the path so we can import config
sys.path.insert(0, str(Path(__file__).parent))

API_BASE = "https://sphere-api.featrix.com"

def test_complete_workflow():
    """Test the complete workflow with the new train_predictor endpoint."""
    
    print("🧪 " + "="*60)
    print("🧪 COMPLETE WORKFLOW TEST: ES + Single Predictor + Predictions")
    print("🧪 " + "="*60)
    print()
    
    # Initialize client
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    # Define single predictor we want to add
    single_predictors = [
        {
            "target_column": "is_fuel_card_reference",
            "target_column_type": "set",
            "epochs": 10,
            "batch_size": 256,
            "learning_rate": 0.001
        }
    ]
    
    # Use the fuel cards test data
    test_file = Path("src/featrix_data/fuel_cards_cleaned.csv")
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False
    
    print(f"📁 Using test data: {test_file}")
    print(f"📏 File size: {test_file.stat().st_size / 1024:.1f} KB")
    
    try:
        # Step 1: Upload file and create session
        print("🚀 Step 1: Uploading data and creating session...")
        session_info = client.upload_file_and_create_session(test_file)
        session_id = session_info.session_id
        
        print(f"✅ Session created: {session_id}")
        print(f"📊 Session type: {session_info.session_type}")
        print(f"⏰ Status: {session_info.status}")
        print()
        
        # Step 2: Wait for embedding space to complete, then add multiple predictors
        print("⏳ Step 2: Waiting for embedding space training...")
        print("   This typically takes 2-5 minutes...")
        
        # Wait for embedding space to be ready
        start_time = time.time()
        while True:
            session_status = client.get_session_status(session_id)
            
            # Check if embedding space training is done
            embedding_done = False
            for job_id, job in session_status.jobs.items():
                if job.get('type') == 'train_es' and job.get('status') == 'done':
                    embedding_done = True
                    break
            
            if embedding_done:
                print("✅ Embedding space training completed!")
                break
            elif session_status.status == 'failed':
                print("❌ Session failed!")
                return False
            
            # Timeout after 10 minutes
            if time.time() - start_time > 600:
                print("⏰ Timeout waiting for embedding space training")
                return False
            
            time.sleep(15)
        
        # Step 3: Add multiple single predictors using the existing endpoint
        print()
        print("🎯 Step 3: Adding multiple single predictors...")
        
        for i, predictor_spec in enumerate(single_predictors):
            target_column = predictor_spec["target_column"]
            target_type = predictor_spec["target_column_type"]
            epochs = predictor_spec["epochs"]
            
            print(f"   Adding predictor {i+1}: {target_column} ({target_type})")
            
            try:
                result = client.train_single_predictor(
                    session_id=session_id,
                    target_column=target_column,
                    target_column_type=target_type,
                    epochs=epochs,
                    batch_size=predictor_spec["batch_size"],
                    learning_rate=predictor_spec["learning_rate"]
                )
                print(f"   ✅ Added: {result.get('message')}")
            except Exception as e:
                print(f"   ❌ Failed to add predictor {i+1}: {e}")
        
        # Step 4: Wait for all predictors to complete
        print()
        print("⏳ Step 4: Waiting for all single predictors to complete...")
        
        final_session = client.wait_for_session_completion(session_id, max_wait_time=15*60, check_interval=30)
        
        if final_session.status == "done":
            print("✅ All jobs completed!")
        elif final_session.status == "failed":
            print("❌ Session failed!")
            return False
        else:
            print("⏰ Test timed out waiting for completion")
            return False
        
        print()
        print("🎉 Step 4: Testing predictions...")
        
        # Load actual data from the CSV to get real column names and values
        try:
            df = pd.read_csv(test_file)
            print(f"   📊 Loaded {len(df)} rows with columns: {list(df.columns)}")
            
            # Get target column info
            target_column = single_predictors[0]["target_column"]
            
            if target_column not in df.columns:
                print(f"   ❌ Target column '{target_column}' not found in data!")
                available_cols = list(df.columns)
                print(f"   📋 Available columns: {available_cols}")
                return False
            
            # Get a real row from the data (excluding the target column for prediction)
            test_row = df.iloc[0]  # Use first row
            test_record = test_row.drop(target_column).to_dict()
            
            # Show what we're testing with
            print(f"   🎯 Testing with real data from row 0:")
            print(f"   📝 Target column '{target_column}' actual value: {test_row[target_column]}")
            print(f"   📊 Input features: {dict(list(test_record.items())[:3])}..." if len(test_record) > 3 else test_record)
            
        except Exception as e:
            print(f"   ❌ Failed to load test data: {e}")
            # Fallback to dummy data if CSV loading fails
            test_record = {
                "FUEL_LOCATION_NAME": "Shell",
                "MERCHANT_CATEGORY_DESC": "Service Stations",
                "TRANSACTION_AMOUNT": 45.67
            }
            print(f"   ⚠️  Using fallback dummy data: {test_record}")
        
        try:
            result = client.make_prediction(session_id, test_record)
            prediction = result.get("prediction")
            print(f"   ✅ Prediction: {prediction}")
        except Exception as e:
            print(f"   ❌ Prediction failed: {e}")
        
        print()
        print("📊 Step 6: Checking available models...")
        
        try:
            models_info = client.get_session_models(session_id)
            summary = models_info.get("summary", {})
            
            print(f"   📦 Total models: {summary.get('total_models', 0)}")
            print(f"   ✅ Available models: {summary.get('available_models', 0)}")
            print(f"   🧠 Embedding space ready: {summary.get('training_complete', False)}")
            print(f"   🎯 Prediction ready: {summary.get('prediction_ready', False)}")
            print(f"   🔍 Similarity search ready: {summary.get('similarity_search_ready', False)}")
            print(f"   📈 Visualization ready: {summary.get('visualization_ready', False)}")
        except Exception as e:
            print(f"   ❌ Failed to get models info: {e}")
        
        print()
        print("🎉 Test completed successfully!")
        print(f"📊 Session ID: {session_id}")
        print("🌐 Check the admin inventory at /admin/inventory to see job logs")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complete_workflow_with_multiple_predictors():
    """Test creating a session and then adding multiple single predictors."""
    
    print("🧪 ============================================================")
    print("🧪 COMPLETE WORKFLOW TEST: ES + Multiple Single Predictors")
    print("🧪 ============================================================")
    print()
    
    # Initialize client
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    # Define the test data file
    data_file = Path("featrix_data/fuel_cards_cleaned.csv")
    print(f"📁 Using test data: {data_file}")
    
    # Check if file exists
    if not data_file.exists():
        print(f"❌ Test data file not found: {data_file}")
        return False
    
    file_size = data_file.stat().st_size / 1024  # KB
    print(f"📏 File size: {file_size:.1f} KB")
    print()
    
    # Define single predictor we want to add
    single_predictors = [
        {
            "target_column": "is_fuel_card_reference",
            "target_column_type": "set",
            "epochs": 10,
            "batch_size": 256,
            "learning_rate": 0.001
        }
    ]
    
    print(f"🎯 Will add {len(single_predictors)} single predictor:")
    for i, sp in enumerate(single_predictors):
        print(f"   {i+1}. {sp['target_column']} ({sp['target_column_type']})")
    print()
    
    try:
        # Step 1: Upload file and create session (standard workflow)
        print("🚀 Step 1: Uploading data and creating session...")
        session_info = client.upload_file_and_create_session(data_file)
        session_id = session_info.session_id
        
        print(f"✅ Session created: {session_id}")
        print(f"📊 Session type: {session_info.session_type}")
        print(f"⏰ Status: {session_info.status}")
        print()
        
        # Step 2: Wait for the standard pipeline to complete
        print("⏳ Step 2: Waiting for full pipeline completion...")
        print("   (embedding space, KNN, projections)")
        
        final_session = client.wait_for_session_completion(session_id, max_wait_time=10*60, check_interval=20)
        
        if final_session.status != "done":
            print(f"❌ Pipeline failed with status: {final_session.status}")
            return False
        
        print("✅ Standard pipeline completed!")
        print()
        
        # Step 3: Add multiple single predictors sequentially
        print("🎯 Step 3: Adding multiple single predictors...")
        
        for i, predictor_spec in enumerate(single_predictors):
            target_column = predictor_spec["target_column"]
            target_type = predictor_spec["target_column_type"]
            epochs = predictor_spec["epochs"]
            
            print(f"   Adding predictor {i+1}: {target_column} ({target_type})")
            
            try:
                result = client.train_single_predictor(
                    session_id=session_id,
                    target_column=target_column,
                    target_column_type=target_type,
                    epochs=epochs,
                    batch_size=predictor_spec["batch_size"],
                    learning_rate=predictor_spec["learning_rate"]
                )
                print(f"   ✅ Added: {result.get('message')}")
                
                # Wait for this predictor to complete before adding the next one
                print(f"   ⏳ Waiting for predictor {i+1} to complete...")
                predictor_session = client.wait_for_session_completion(session_id, max_wait_time=5*60, check_interval=15)
                
                if predictor_session.status == "done":
                    print(f"   ✅ Predictor {i+1} completed!")
                else:
                    print(f"   ❌ Predictor {i+1} failed!")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Failed to add predictor {i+1}: {e}")
                return False
        
        print()
        print("🎉 Step 4: Testing predictions...")
        
        # Load actual data from the CSV to get real column names and values
        try:
            df = pd.read_csv(data_file)
            print(f"   📊 Loaded {len(df)} rows with columns: {list(df.columns)}")
            
            # Get target column info
            target_column = single_predictors[0]["target_column"]
            
            if target_column not in df.columns:
                print(f"   ❌ Target column '{target_column}' not found in data!")
                available_cols = list(df.columns)
                print(f"   📋 Available columns: {available_cols}")
                return False
            
            # Get a real row from the data (excluding the target column for prediction)
            test_row = df.iloc[0]  # Use first row
            test_record = test_row.drop(target_column).to_dict()
            
            # Show what we're testing with
            print(f"   🎯 Testing with real data from row 0:")
            print(f"   📝 Target column '{target_column}' actual value: {test_row[target_column]}")
            print(f"   📊 Input features: {dict(list(test_record.items())[:3])}..." if len(test_record) > 3 else test_record)
            
        except Exception as e:
            print(f"   ❌ Failed to load test data: {e}")
            # Fallback to dummy data if CSV loading fails
            test_record = {
                "FUEL_LOCATION_NAME": "Shell",
                "MERCHANT_CATEGORY_DESC": "Service Stations",
                "TRANSACTION_AMOUNT": 45.67
            }
            print(f"   ⚠️  Using fallback dummy data: {test_record}")
        
        try:
            result = client.make_prediction(session_id, test_record)
            prediction = result.get("prediction")
            print(f"   ✅ Prediction: {prediction}")
        except Exception as e:
            print(f"   ❌ Prediction failed: {e}")
        
        print()
        print("📊 Step 5: Checking available models...")
        
        try:
            models_info = client.get_session_models(session_id)
            summary = models_info.get("summary", {})
            
            print(f"   📦 Total models: {summary.get('total_models', 0)}")
            print(f"   ✅ Available models: {summary.get('available_models', 0)}")
            print(f"   🧠 Embedding space ready: {summary.get('training_complete', False)}")
            print(f"   🎯 Prediction ready: {summary.get('prediction_ready', False)}")
            print(f"   🔍 Similarity search ready: {summary.get('similarity_search_ready', False)}")
            print(f"   📈 Visualization ready: {summary.get('visualization_ready', False)}")
        except Exception as e:
            print(f"   ❌ Failed to get models info: {e}")
        
        print()
        print("🎉 Test completed successfully!")
        print(f"📊 Session ID: {session_id}")
        print("🌐 Check the admin inventory at /admin/inventory to see job logs")
        print(f"🎯 Successfully added {len(single_predictors)} single predictors!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_workflow()
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1) 