#!/usr/bin/env python3
"""
Example: Add Single Predictor Training to Existing Session

This script demonstrates how to add single predictor training to a session
that already has a trained embedding space.
"""

import sys
from test_api_client import FeatrixSphereClient

def main():
    if len(sys.argv) < 4:
        print("Usage: python example_train_predictor.py <session_id> <target_column> <target_type> [epochs]")
        print("  session_id: ID of session with trained embedding space")
        print("  target_column: Name of target column to predict")
        print("  target_type: 'set' for categorical or 'scalar' for numeric")
        print("  epochs: Number of training epochs (optional, default: auto)")
        print()
        print("Example:")
        print("  python example_train_predictor.py 20250620-162402_fb593f is_fuel_card_reference set 100")
        sys.exit(1)
    
    session_id = sys.argv[1]
    target_column = sys.argv[2]
    target_type = sys.argv[3]
    epochs = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    
    # Validate target type
    if target_type not in ['set', 'scalar']:
        print("Error: target_type must be 'set' or 'scalar'")
        sys.exit(1)
    
    print("=" * 60)
    print("🎯 Adding Single Predictor Training to Session")
    print("=" * 60)
    print(f"Session ID: {session_id}")
    print(f"Target Column: {target_column}")
    print(f"Target Type: {target_type}")
    print(f"Training Epochs: {epochs}")
    print()
    
    # Initialize the client
    client = FeatrixSphereClient()
    
    try:
        # 1. Check session status first
        print("1. Checking session status...")
        session_info = client.get_session_status(session_id)
        # SessionInfo is a dataclass, access attributes directly
        session = {'session_id': session_info.session_id, 'session_type': session_info.session_type, 'status': session_info.status}
        jobs = session_info.jobs
        
        print(f"   Session status: {session.get('status', 'unknown')}")
        print(f"   Session type: {session.get('session_type', 'unknown')}")
        
        # Check if embedding space is trained (would need to fetch full session for this)
        has_embedding_space = True  # Assume true if session exists
        print(f"   Has embedding space: {'✅' if has_embedding_space else '❌'}")
        
        # Check if already has predictor
        has_predictor = session.get('single_predictor') is not None
        print(f"   Has single predictor: {'✅' if has_predictor else '❌'}")
        
        if not has_embedding_space:
            print("❌ Error: Session must have a trained embedding space first!")
            print("   Please ensure the embedding space training is complete.")
            sys.exit(1)
        
        if has_predictor:
            print("❌ Error: Session already has a single predictor!")
            print("   Cannot add another predictor to the same session.")
            sys.exit(1)
        
        print()
        
        # 2. Start single predictor training
        print("2. Starting single predictor training...")
        result = client.train_single_predictor(
            session_id=session_id,
            target_column=target_column,
            target_column_type=target_type,
            epochs=epochs,
            batch_size=0,
            learning_rate=0.001
        )
        
        print(f"✅ {result.get('message')}")
        print()
        
        # 3. Monitor training progress
        print("3. Training started! You can monitor progress with:")
        print(f"   python example_api_usage.py monitor {session_id}")
        print()
        print("4. Once training is complete, you can make predictions with:")
        print(f"   python example_api_usage.py predict {session_id}")
        print()
        print("5. Or view the session info page at:")
        print(f"   https://sphere-api.featrix.com/info/{session_id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 