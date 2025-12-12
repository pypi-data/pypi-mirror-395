#!/usr/bin/env python3
"""
Test Session Models Endpoint

This script demonstrates the new /session/{id}/models endpoint that lists
available embedding spaces and models for a session.
"""

import json
import sys
from pathlib import Path
from test_api_client import FeatrixSphereClient


def format_file_size(size_bytes):
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def format_timestamp(timestamp):
    """Format timestamp in human-readable format."""
    import datetime
    try:
        return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return str(timestamp)


def print_model_details(model_name, model_info):
    """Print detailed information about a model."""
    available = model_info.get("available", False)
    status_icon = "✅" if available else "❌"
    
    print(f"\n{status_icon} {model_name.replace('_', ' ').title()}")
    print(f"   Type: {model_info.get('type', 'unknown')}")
    print(f"   Available: {available}")
    print(f"   Description: {model_info.get('description', 'No description')}")
    
    if available:
        if "file_size" in model_info:
            print(f"   Size: {format_file_size(model_info['file_size'])}")
        if "file_count" in model_info:
            print(f"   Files: {model_info['file_count']}")
        if "created_at" in model_info:
            print(f"   Created: {format_timestamp(model_info['created_at'])}")
        if "modified_at" in model_info:
            print(f"   Modified: {format_timestamp(model_info['modified_at'])}")
        
        endpoints = model_info.get("endpoints", [])
        if endpoints:
            print(f"   Endpoints: {', '.join(endpoints)}")
    else:
        if "error" in model_info:
            print(f"   Error: {model_info['error']}")
    
    if "path" in model_info and model_info["path"]:
        print(f"   Path: {model_info['path']}")


def test_session_models(session_id):
    """Test the session models endpoint for a specific session."""
    
    print(f"🔍 Testing Session Models Endpoint")
    print(f"Session ID: {session_id}")
    print("=" * 60)
    
    # Initialize client
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    try:
        # Get available models
        result = client.get_session_models(session_id)
        
        models = result.get('models', {})
        summary = result.get('summary', {})
        
        print(f"\n📊 Summary")
        print(f"   Total models checked: {summary.get('total_models', 0)}")
        print(f"   Available models: {summary.get('available_models', 0)}")
        print(f"   Training complete: {'✅' if summary.get('training_complete') else '❌'}")
        print(f"   Prediction ready: {'✅' if summary.get('prediction_ready') else '❌'}")
        print(f"   Similarity search ready: {'✅' if summary.get('similarity_search_ready') else '❌'}")
        print(f"   Visualization ready: {'✅' if summary.get('visualization_ready') else '❌'}")
        
        print(f"\n📋 Model Details")
        
        # Print details for each model
        model_order = [
            "embedding_space",
            "single_predictor", 
            "vector_database",
            "projections",
            "training_metrics",
            "data_database"
        ]
        
        for model_name in model_order:
            if model_name in models:
                print_model_details(model_name, models[model_name])
        
        # Print any additional models not in the standard order
        for model_name, model_info in models.items():
            if model_name not in model_order:
                print_model_details(model_name, model_info)
        
        print(f"\n🚀 Next Steps")
        
        if summary.get('training_complete') and not summary.get('prediction_ready'):
            print("   • Training is complete! You can now add a single predictor:")
            print(f"     client.train_single_predictor('{session_id}', 'target_column', 'set')")
        
        if summary.get('prediction_ready'):
            print("   • You can make predictions:")
            print(f"     client.make_prediction('{session_id}', query_record)")
            print(f"     client.predict_records('{session_id}', records_list)")
        
        if summary.get('similarity_search_ready'):
            print("   • You can perform similarity searches:")
            print(f"     client.similarity_search('{session_id}', query_record, k=5)")
        
        if summary.get('visualization_ready'):
            print("   • You can view 2D projections:")
            print(f"     client.get_projections('{session_id}')")
        
        print(f"\n📖 Raw Response (JSON):")
        print(json.dumps(result, indent=2))
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing session models: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function."""
    
    if len(sys.argv) < 2:
        print("Usage: python test_session_models.py <session_id>")
        print()
        print("Examples:")
        print("  python test_session_models.py 20250620-162402_fb593f")
        print("  python test_session_models.py your-session-id")
        return 1
    
    session_id = sys.argv[1]
    
    success = test_session_models(session_id)
    
    if success:
        print(f"\n✅ Session models test completed successfully!")
        return 0
    else:
        print(f"\n❌ Session models test failed!")
        return 1


if __name__ == "__main__":
    exit(main()) 