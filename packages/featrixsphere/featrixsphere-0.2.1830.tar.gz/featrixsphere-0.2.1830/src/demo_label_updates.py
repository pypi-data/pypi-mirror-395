#!/usr/bin/env python3
"""
Demo: How to Update Prediction Labels via API

This script shows how to:
1. Make predictions and get prediction UUIDs
2. Update labels when predictions are wrong
3. View prediction history and corrections
4. Create retraining batches

🚀 QUICK API REFERENCE:

# Make predictions (automatically stores with UUID)
result = client.predict(session_id, record)
prediction_id = result['prediction_id']

# Correct wrong predictions
client.update_prediction_label(prediction_id, "correct_label")

# View prediction history
all_preds = client.get_session_predictions(session_id)
corrections = client.get_session_predictions(session_id, corrected_only=True)

# Create retraining batch
batch = client.create_retraining_batch(session_id)
"""

import sys
from pathlib import Path

# Add the parent directory to access featrixsphere package
sys.path.append(str(Path(__file__).parent.parent))

from featrixsphere.client import FeatrixSphereClient

def demo_label_updates():
    """Demonstrate how to update prediction labels via API."""
    
    print("🏷️  " + "="*60)
    print("🏷️  PREDICTION LABEL UPDATE DEMO")
    print("🏷️  " + "="*60)
    
    # Initialize client
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    # Use your session with trained predictor
    session_id = "20250623-124806_4591e7"  # Update this to your session
    
    print(f"\n1. 🎯 Making predictions to get UUIDs...")
    
    # Test records for fuel card detection
    test_records = [
        {"domain": "shell.com", "snippet": "fuel card rewards program for drivers", "keyword": "fuel card"},
        {"domain": "walmart.com", "snippet": "grocery shopping and retail store", "keyword": "shopping"},
        {"domain": "bp.com", "snippet": "fleet fuel cards for business vehicles", "keyword": "fleet cards"},
        {"domain": "amazon.com", "snippet": "buy electronics and gadgets online", "keyword": "electronics"},
        {"domain": "exxon.com", "snippet": "gas station locator and fuel services", "keyword": "gas station"},
    ]
    
    prediction_ids = []
    predictions_made = []
    
    for i, record in enumerate(test_records):
        try:
            # Make prediction - this automatically stores it with a UUID
            result = client.predict(session_id, record)
            prediction_id = result.get('prediction_id')
            prediction = result.get('prediction', {})
            
            if prediction_id:
                prediction_ids.append(prediction_id)
                
                # Show what was predicted
                predicted_class = max(prediction, key=prediction.get)
                confidence = prediction[predicted_class]
                
                predictions_made.append({
                    'record': record,
                    'predicted_class': predicted_class,
                    'confidence': confidence,
                    'prediction_id': prediction_id
                })
                
                print(f"  ✅ Record {i+1}: {predicted_class} ({confidence*100:.1f}% confidence)")
                print(f"     UUID: {prediction_id}")
                print(f"     Input: {record['domain']} - {record['snippet'][:50]}...")
                print()
                
        except Exception as e:
            print(f"  ❌ Error with record {i+1}: {e}")
    
    print(f"\n2. 🏷️  Updating prediction labels...")
    
    # Simulate user corrections based on domain knowledge
    corrections = [
        ("True", "Shell is a fuel company - this should be True"),
        ("False", "Walmart is retail, not fuel cards - this should be False"), 
        ("True", "BP fleet cards are definitely fuel cards - this should be True"),
        ("False", "Amazon electronics has nothing to do with fuel - this should be False"),
        ("True", "Exxon gas stations typically have fuel cards - this should be True")
    ]
    
    for i, (prediction_id, (correct_label, reason)) in enumerate(zip(prediction_ids, corrections)):
        if i >= len(predictions_made):
            break
            
        try:
            prediction_info = predictions_made[i]
            original_prediction = prediction_info['predicted_class']
            
            print(f"  🔄 Updating prediction {i+1}...")
            print(f"     UUID: {prediction_id}")
            print(f"     Original: {original_prediction} ({prediction_info['confidence']*100:.1f}%)")
            print(f"     Correcting to: {correct_label}")
            print(f"     Reason: {reason}")
            
            # Update the label via API
            result = client.update_prediction_label(prediction_id, correct_label)
            print(f"     ✅ {result.get('message')}")
            
            # Show if this was actually a correction
            if original_prediction != correct_label:
                print(f"     🎯 CORRECTION: {original_prediction} → {correct_label}")
            else:
                print(f"     ✓ Confirmed: Prediction was already correct")
            print()
            
        except Exception as e:
            print(f"     ❌ Error updating: {e}")
    
    print(f"\n3. 📊 Viewing prediction history...")
    
    try:
        # Get all predictions for this session
        all_predictions = client.get_session_predictions(session_id, corrected_only=False, limit=20)
        total_count = all_predictions.get('total_count', 0)
        print(f"  📈 Total predictions: {total_count}")
        
        # Get only corrected predictions
        corrected_predictions = client.get_session_predictions(session_id, corrected_only=True, limit=10)
        corrected_count = corrected_predictions.get('total_count', 0)
        print(f"  🏷️  Corrected predictions: {corrected_count}")
        
        # Calculate correction rate
        if total_count > 0:
            correction_rate = (corrected_count / total_count) * 100
            print(f"  📊 Correction rate: {correction_rate:.1f}%")
        
        # Show recent corrections
        print(f"\n  📋 Recent corrections:")
        for pred in corrected_predictions.get('predictions', [])[:5]:
            original_pred = pred.get('predicted_class', 'Unknown')
            user_label = pred.get('user_label', 'Unknown')
            confidence = pred.get('confidence', 0) * 100
            created_at = pred.get('created_at', '')
            
            # Determine if this was actually a correction
            was_wrong = original_pred != user_label
            status_icon = "❌→✅" if was_wrong else "✅✓"
            
            print(f"     {status_icon} ID: {pred['prediction_id'][:8]}...")
            print(f"        Original: {original_pred} ({confidence:.1f}%) → Corrected: {user_label}")
            print(f"        Created: {created_at}")
            if was_wrong:
                print(f"        📝 Model was WRONG - learned from this correction")
            else:
                print(f"        ✓ Model was right - user confirmed")
            print()
            
    except Exception as e:
        print(f"  ❌ Error retrieving history: {e}")
    
    print(f"\n4. 🔄 Creating retraining batch...")
    
    try:
        # Create a retraining batch from corrected predictions
        batch_result = client.create_retraining_batch(session_id)
        
        print(f"  ✅ Retraining batch created!")
        print(f"     Batch ID: {batch_result.get('batch_id')}")
        print(f"     Total predictions: {batch_result.get('total_predictions')}")
        print(f"     Corrected predictions: {batch_result.get('corrected_predictions')}")
        print(f"     Status: {batch_result.get('status')}")
        
        # Give recommendations
        corrected = batch_result.get('corrected_predictions', 0)
        if corrected >= 10:
            print(f"  💡 Great! {corrected} corrections is enough for meaningful retraining")
        elif corrected >= 5:
            print(f"  💡 {corrected} corrections is a good start - collect more for better results")
        else:
            print(f"  💡 Only {corrected} corrections - try to collect 10+ for effective retraining")
        
    except Exception as e:
        print(f"  ❌ Error creating batch: {e}")
    
    print(f"\n" + "="*60)
    print(f"🎉 PREDICTION FEEDBACK DEMO COMPLETED")
    print(f"="*60)
    print(f"📝 What you learned:")
    print(f"   1. Every prediction gets a UUID automatically")
    print(f"   2. Use client.update_prediction_label(uuid, label) to correct")
    print(f"   3. Use client.get_session_predictions() to view history") 
    print(f"   4. Use client.create_retraining_batch() to prepare for retraining")
    print()
    print(f"🔗 Key API Endpoints:")
    print(f"   POST /compute/prediction/{{uuid}}/update_label")
    print(f"   GET  /compute/session/{{session_id}}/predictions")
    print(f"   POST /compute/session/{{session_id}}/create_retraining_batch")
    print()
    print(f"💡 Production Tips:")
    print(f"   • Store prediction UUIDs for all production predictions")
    print(f"   • Collect user feedback systematically")
    print(f"   • Monitor correction rates to detect model drift")
    print(f"   • Retrain when you have 20+ meaningful corrections")
    print(f"   • Use batch predictions for better performance")

def show_api_examples():
    """Show quick API usage examples."""
    
    print("\n" + "="*60)
    print("🚀 QUICK API EXAMPLES")
    print("="*60)
    
    print("""
# 1. Initialize client
from featrixsphere.client import FeatrixSphereClient
client = FeatrixSphereClient("https://sphere-api.featrix.com")

# 2. Make prediction (gets UUID automatically)
result = client.predict(session_id, {"domain": "shell.com", "snippet": "fuel cards"})
prediction_id = result['prediction_id']
prediction = result['prediction']

# 3. Correct wrong prediction
client.update_prediction_label(prediction_id, "True")

# 4. View prediction history
all_predictions = client.get_session_predictions(session_id)
corrections_only = client.get_session_predictions(session_id, corrected_only=True)

# 5. Create retraining batch
batch = client.create_retraining_batch(session_id)

# 6. Batch predictions (more efficient)
records = [{"domain": "bp.com"}, {"domain": "amazon.com"}]
results = client.predict_records(session_id, records)

# 7. Test model accuracy
results = client.run_csv_predictions(
    session_id, "test_data.csv", target_column="actual_label"
)
accuracy = results['accuracy_metrics']['accuracy']
print(f"Model accuracy: {accuracy*100:.2f}%")
""")

if __name__ == "__main__":
    demo_label_updates()
    show_api_examples() 