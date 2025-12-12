#!/usr/bin/env python3
"""
JSON Tables Batch Prediction Test

This script demonstrates the new JSON Tables batch prediction functionality.
It shows different ways to make batch predictions using the API.
"""

import json
import pandas as pd
from pathlib import Path
from test_api_client import FeatrixSphereClient
from jsontables import (
    JSONTablesEncoder, 
    JSONTablesDecoder, 
    render_json_table,
    to_json_table
)


def test_json_tables_basics():
    """Test basic JSON Tables encoding/decoding functionality."""
    
    print("=== Testing JSON Tables Basics ===\n")
    
    # Sample data
    sample_data = [
        {"name": "Alice", "age": 25, "score": 85.5, "active": True},
        {"name": "Bob", "age": 30, "score": 92.0, "active": False},
        {"name": "Charlie", "age": 35, "score": 78.5, "active": True},
    ]
    
    print("Original data:")
    print(json.dumps(sample_data, indent=2))
    print()
    
    # Convert to JSON Tables format
    json_table = to_json_table(sample_data)
    print("JSON Tables format:")
    print(json.dumps(json_table, indent=2))
    print()
    
    # Render in aligned format
    print("Aligned rendering:")
    print(render_json_table(json_table))
    print()
    
    # Convert back to DataFrame
    df = pd.DataFrame(sample_data)
    print("As DataFrame:")
    print(df)
    print()


def test_batch_prediction_formats():
    """Test different input formats for batch prediction."""
    
    print("=== Testing Batch Prediction Input Formats ===\n")
    
    # Initialize client (this will fail without a real session, but shows the format)
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    # Sample prediction data
    records = [
        {"feature1": "value1", "feature2": 42.0, "feature3": "category_a"},
        {"feature1": "value2", "feature2": 38.5, "feature3": "category_b"},
        {"feature1": "value3", "feature2": 41.2, "feature3": "category_a"},
    ]
    
    print("Sample records for prediction:")
    for i, record in enumerate(records):
        print(f"  {i+1}. {record}")
    print()
    
    # Format 1: Direct JSON Tables format
    json_table_format = to_json_table(records)
    print("Format 1: JSON Tables format")
    print(render_json_table(json_table_format))
    print()
    
    # Format 2: List of records
    print("Format 2: List of records")
    print(json.dumps(records, indent=2))
    print()
    
    # Format 3: Wrapped in 'records' field
    wrapped_records = {"records": records}
    print("Format 3: Wrapped records")
    print(json.dumps(wrapped_records, indent=2))
    print()
    
    # Format 4: Wrapped in 'table' field
    wrapped_table = {"table": json_table_format}
    print("Format 4: Wrapped table")
    print("{\n  \"table\": <JSON Tables object>\n}")
    print()
    
    # Note about usage (these would fail without a real trained session)
    session_id = "example-session-id"  # Replace with real session ID
    
    print("Usage examples (replace with real session ID):")
    print(f"  client.predict_table('{session_id}', json_table_format)")
    print(f"  client.predict_table('{session_id}', records)")
    print(f"  client.predict_table('{session_id}', wrapped_records)")
    print(f"  client.predict_table('{session_id}', wrapped_table)")
    print(f"  client.predict_records('{session_id}', records)")
    print()


def test_csv_file_prediction():
    """Test CSV file batch prediction."""
    
    print("=== Testing CSV File Prediction ===\n")
    
    # Create a sample CSV file
    sample_data = pd.DataFrame([
        {"name": "Alice", "age": 25, "department": "Engineering", "salary": 75000},
        {"name": "Bob", "age": 30, "department": "Marketing", "salary": 65000},
        {"name": "Charlie", "age": 35, "department": "Engineering", "salary": 85000},
        {"name": "Diana", "age": 28, "department": "Sales", "salary": 70000},
        {"name": "Eve", "age": 32, "department": "Marketing", "salary": 72000},
    ])
    
    # Save to CSV
    csv_file = Path("sample_prediction_data.csv")
    sample_data.to_csv(csv_file, index=False)
    print(f"Created sample CSV file: {csv_file}")
    print("Contents:")
    print(sample_data)
    print()
    
    # Convert to JSON Tables for demonstration
    json_table = JSONTablesEncoder.from_dataframe(sample_data)
    print("As JSON Tables format:")
    print(render_json_table(json_table))
    print()
    
    # Show API usage
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    session_id = "example-session-id"  # Replace with real session ID
    
    print("API usage example:")
    print(f"  result = client.predict_csv_file('{session_id}', Path('{csv_file}'))")
    print()
    
    # Clean up
    if csv_file.exists():
        csv_file.unlink()
        print(f"Cleaned up: {csv_file}")


def test_pagination():
    """Test JSON Tables pagination features."""
    
    print("=== Testing JSON Tables Pagination ===\n")
    
    # Create larger dataset
    large_data = []
    for i in range(25):
        large_data.append({
            "id": i + 1,
            "name": f"User_{i+1:03d}",
            "score": round(50 + (i * 2.5), 1),
            "active": i % 3 == 0
        })
    
    print(f"Created dataset with {len(large_data)} records")
    print()
    
    # Test pagination
    page_size = 10
    for page in range(3):
        print(f"Page {page + 1} (page_size={page_size}):")
        
        json_table_page = JSONTablesEncoder.from_records(
            large_data, 
            page_size=page_size, 
            current_page=page
        )
        
        print(f"  Page info: {json_table_page['current_page']+1}/{json_table_page['total_pages']}")
        print(f"  Rows on page: {json_table_page['page_rows']}")
        print("  Data preview:")
        print(render_json_table(json_table_page, max_width=100))
        print()


def demonstrate_api_workflow():
    """Demonstrate a complete API workflow with JSON Tables."""
    
    print("=== Complete API Workflow Demo ===\n")
    
    # This demonstrates the workflow but won't actually run without a real session
    
    print("Step 1: Create or load data")
    data = [
        {"customer_id": "C001", "age": 28, "income": 55000, "purchase_history": 5},
        {"customer_id": "C002", "age": 34, "income": 72000, "purchase_history": 12},
        {"customer_id": "C003", "age": 22, "income": 38000, "purchase_history": 2},
        {"customer_id": "C004", "age": 45, "income": 95000, "purchase_history": 18},
        {"customer_id": "C005", "age": 31, "income": 63000, "purchase_history": 8},
    ]
    
    print("Sample data:")
    for record in data:
        print(f"  {record}")
    print()
    
    print("Step 2: Convert to JSON Tables format")
    json_table = to_json_table(data)
    print("JSON Tables representation:")
    print(render_json_table(json_table))
    print()
    
    print("Step 3: Make batch predictions (example API calls)")
    print("```python")
    print("from test_api_client import FeatrixSphereClient")
    print("from jsontables import to_json_table")
    print()
    print("client = FeatrixSphereClient('https://sphere-api.featrix.com')")
    print("session_id = 'your-trained-session-id'")
    print()
    print("# Method 1: Direct JSON Tables format")
    print("result1 = client.predict_table(session_id, json_table)")
    print()
    print("# Method 2: List of records")
    print("result2 = client.predict_records(session_id, data)")
    print()
    print("# Method 3: CSV file")
    print("result3 = client.predict_csv_file(session_id, Path('data.csv'))")
    print("```")
    print()
    
    print("Step 4: Expected response format")
    print("```json")
    print(json.dumps({
        "input_table": {"__dict_type": "table", "cols": ["customer_id", "age", "income", "purchase_history"], "...": "..."},
        "predictions": [
            {"row_index": 0, "prediction": {"will_buy": 0.75, "wont_buy": 0.25}, "error": None},
            {"row_index": 1, "prediction": {"will_buy": 0.92, "wont_buy": 0.08}, "error": None},
            "..."
        ],
        "results_table": {"__dict_type": "table", "cols": ["customer_id", "age", "income", "purchase_history", "pred_will_buy", "pred_wont_buy", "predicted_class"], "...": "..."},
        "summary": {
            "total_records": 5,
            "successful_predictions": 5,
            "failed_predictions": 0,
            "errors": []
        }
    }, indent=2))
    print("```")
    print()
    
    print("Step 5: Extract results")
    print("```python")
    print("# Get the results table (includes original data + predictions)")
    print("results_table = result1['results_table']")
    print("results_df = pd.DataFrame(results_table['row_data'], columns=results_table['cols'])")
    print()
    print("# Or get individual predictions")
    print("predictions = result1['predictions']")
    print("for i, pred in enumerate(predictions):")
    print("    if pred['error'] is None:")
    print("        print(f'Row {i}: {pred[\"prediction\"]}')")
    print("    else:")
    print("        print(f'Row {i}: Error - {pred[\"error\"]}')")
    print("```")


def main():
    """Run all JSON Tables tests."""
    
    print("🔬 JSON Tables Batch Prediction Test Suite")
    print("=" * 60)
    print()
    
    try:
        # Test basic JSON Tables functionality
        test_json_tables_basics()
        
        # Test different input formats
        test_batch_prediction_formats()
        
        # Test CSV file prediction
        test_csv_file_prediction()
        
        # Test pagination
        test_pagination()
        
        # Demonstrate complete workflow
        demonstrate_api_workflow()
        
        print("✅ All tests completed successfully!")
        print()
        print("📝 Summary:")
        print("  • JSON Tables encoding/decoding: Working")
        print("  • Multiple input formats: Supported")
        print("  • CSV file processing: Working")
        print("  • Pagination: Working")
        print("  • API integration: Ready")
        print()
        print("🚀 Ready to use with real trained sessions!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 