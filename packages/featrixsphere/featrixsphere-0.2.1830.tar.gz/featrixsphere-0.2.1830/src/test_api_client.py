#!/usr/bin/env python3
"""
Featrix Sphere API Client

A simple Python client for testing the Featrix Sphere API endpoints,
with a focus on the new single predictor functionality.
"""

import json
import time
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class SessionInfo:
    """Container for session information."""
    session_id: str
    session_type: str
    status: str
    jobs: Dict[str, Any]
    job_queue_positions: Dict[str, Any]


class FeatrixSphereClient:
    """Client for interacting with the Featrix Sphere API."""
    
    def __init__(self, base_url: str = "https://sphere-api.featrix.com"):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        # Set a reasonable timeout
        self.session.timeout = 30
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an HTTP request with error handling."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {method} {url}")
            print(f"Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response body: {e.response.text[:500]}")
            raise
    
    def _get_json(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a GET request and return JSON response."""
        response = self._make_request("GET", endpoint, **kwargs)
        return response.json()
    
    def _post_json(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Make a POST request with JSON data and return JSON response."""
        if data is not None:
            kwargs['json'] = data
        response = self._make_request("POST", endpoint, **kwargs)
        return response.json()

    # =========================================================================
    # Session Management
    # =========================================================================
    
    def create_session(self, session_type: str = "sphere") -> SessionInfo:
        """
        Create a new session.
        
        Args:
            session_type: Type of session to create ('sphere', 'predictor', etc.)
            
        Returns:
            SessionInfo object with session details
        """
        print(f"Creating {session_type} session...")
        
        # Send empty JSON object to ensure proper content-type
        response_data = self._post_json("/compute/session", {})
        
        session_id = response_data.get('session_id')
        print(f"Created session: {session_id}")
        
        return SessionInfo(
            session_id=session_id,
            session_type=response_data.get('session_type', 'sphere'),
            status=response_data.get('status', 'unknown'),
            jobs={},
            job_queue_positions={}
        )
    
    def get_session_status(self, session_id: str) -> SessionInfo:
        """
        Get detailed session status.
        
        Args:
            session_id: ID of the session
            
        Returns:
            SessionInfo object with current session details
        """
        response_data = self._get_json(f"/compute/session/{session_id}")
        
        session = response_data.get('session', {})
        jobs = response_data.get('jobs', {})
        positions = response_data.get('job_queue_positions', {})
        detailed_queue_info = response_data.get('detailed_queue_info', {})
        
        # Store enhanced queue info for display
        session_info = SessionInfo(
            session_id=session.get('session_id', session_id),
            session_type=session.get('session_type', 'unknown'),
            status=session.get('status', 'unknown'),
            jobs=jobs,
            job_queue_positions=positions
        )
        
        # Add detailed queue info as additional attribute
        session_info.detailed_queue_info = detailed_queue_info
        
        return session_info
    
    def get_session_models(self, session_id: str) -> Dict[str, Any]:
        """
        Get available models and embedding spaces for a session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            Dictionary containing available models, their metadata, and summary information
        """
        print(f"Getting available models for session {session_id}")
        
        response_data = self._get_json(f"/compute/session/{session_id}/models")
        
        models = response_data.get('models', {})
        summary = response_data.get('summary', {})
        
        print(f"Available models: {summary.get('available_model_types', [])}")
        print(f"Training complete: {'✅' if summary.get('training_complete') else '❌'}")
        print(f"Prediction ready: {'✅' if summary.get('prediction_ready') else '❌'}")
        print(f"Similarity search ready: {'✅' if summary.get('similarity_search_ready') else '❌'}")
        print(f"Visualization ready: {'✅' if summary.get('visualization_ready') else '❌'}")
        
        return response_data
    
    def wait_for_session_completion(self, session_id: str, max_wait_time: int = 3600, 
                                   check_interval: int = 10) -> SessionInfo:
        """
        Wait for a session to complete, polling for status updates.
        
        Args:
            session_id: ID of the session to monitor
            max_wait_time: Maximum time to wait in seconds
            check_interval: How often to check status in seconds
            
        Returns:
            Final SessionInfo when session completes or times out
        """
        print(f"Waiting for session {session_id} to complete...")
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            session_info = self.get_session_status(session_id)
            
            print(f"Session status: {session_info.status}")
            
            # Print job progress with enhanced queue information
            for job_id, job in session_info.jobs.items():
                job_status = job.get('status', 'unknown')
                progress = job.get('progress')
                job_type = job.get('type', job_id.split('_')[0])
                
                # Get detailed queue info for this job
                detailed_info = getattr(session_info, 'detailed_queue_info', {}).get(job_id, {})
                
                # Build status line with enhanced information
                status_line = f"  {job_type}: {job_status}"
                
                # Add queue-specific information
                if detailed_info:
                    wait_message = detailed_info.get('estimated_wait_message')
                    if wait_message and wait_message != f"Currently running":
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
                            
                elif detailed_info and detailed_info.get('queue_status') == 'running':
                    progress_pct = detailed_info.get('progress_percent', 0)
                    if progress_pct > 0:
                        print(f"    📊 Training progress: {progress_pct}%")
            
            # Check if session is complete
            if session_info.status in ['done', 'failed', 'cancelled']:
                print(f"Session completed with status: {session_info.status}")
                return session_info
            
            # Check if all jobs are in terminal states (done or failed)
            if session_info.jobs:
                terminal_states = {'done', 'failed', 'cancelled'}
                all_jobs_terminal = all(
                    job.get('status') in terminal_states 
                    for job in session_info.jobs.values()
                )
                
                if all_jobs_terminal:
                    # Analyze job completion status
                    job_summary = self._analyze_job_completion(session_info.jobs)
                    print(f"All jobs completed. {job_summary}")
                    return session_info
            
            time.sleep(check_interval)
        
        print(f"Timeout waiting for session completion after {max_wait_time} seconds")
        return self.get_session_status(session_id)
    
    def _analyze_job_completion(self, jobs: Dict[str, Any]) -> str:
        """
        Analyze job completion status and provide detailed summary.
        
        Args:
            jobs: Dictionary of job information
            
        Returns:
            Formatted string describing job completion status
        """
        done_jobs = []
        failed_jobs = []
        cancelled_jobs = []
        
        for job_id, job in jobs.items():
            status = job.get('status', 'unknown')
            job_type = job.get('type', 'unknown')
            
            if status == 'done':
                done_jobs.append(f"{job_type} ({job_id})")
            elif status == 'failed':
                error_info = ""
                # Look for error information in various possible fields
                if 'error' in job:
                    error_info = f" - Error: {job['error']}"
                elif 'message' in job:
                    error_info = f" - Message: {job['message']}"
                failed_jobs.append(f"{job_type} ({job_id}){error_info}")
            elif status == 'cancelled':
                cancelled_jobs.append(f"{job_type} ({job_id})")
        
        # Build summary message
        summary_parts = []
        if done_jobs:
            summary_parts.append(f"✅ {len(done_jobs)} succeeded: {', '.join(done_jobs)}")
        if failed_jobs:
            summary_parts.append(f"❌ {len(failed_jobs)} failed: {', '.join(failed_jobs)}")
        if cancelled_jobs:
            summary_parts.append(f"🚫 {len(cancelled_jobs)} cancelled: {', '.join(cancelled_jobs)}")
        
        return " | ".join(summary_parts) if summary_parts else "No jobs found"

    # =========================================================================
    # File Upload
    # =========================================================================
    
    def upload_file_and_create_session(self, file_path: Path) -> SessionInfo:
        """
        Upload a CSV file and create a new session.
        
        Args:
            file_path: Path to the CSV file to upload
            
        Returns:
            SessionInfo for the newly created session
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"Uploading file: {file_path}")
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, 'text/csv')}
            response = self._make_request("POST", "/compute/upload_with_new_session/", files=files)
        
        response_data = response.json()
        session_id = response_data.get('session_id')
        
        print(f"File uploaded, session created: {session_id}")
        
        # Check for and display warnings
        warnings = response_data.get('warnings', [])
        if warnings:
            print("\n" + "="*60)
            print("⚠️  UPLOAD WARNINGS")
            print("="*60)
            for warning in warnings:
                print(warning)
            print("="*60 + "\n")
        
        return SessionInfo(
            session_id=session_id,
            session_type=response_data.get('session_type', 'sphere'),
            status=response_data.get('status', 'ready'),
            jobs={},
            job_queue_positions={}
        )
    
    def upload_df_and_create_session(self, df, filename: str = "data.csv", 
                                     name: str = None, session_name_prefix: str = None,
                                     epochs: int = None, **kwargs) -> SessionInfo:
        """
        Upload a pandas DataFrame and create a new session.
        
        Args:
            df: pandas DataFrame to upload
            filename: Name for the uploaded file
            name: Optional name for the embedding space
            session_name_prefix: Optional prefix for session ID
            epochs: Optional number of epochs for ES training
            **kwargs: Additional form data to pass (e.g., column_overrides, etc.)
            
        Returns:
            SessionInfo for the newly created session
        """
        import tempfile
        import pandas as pd
        
        print(f"Uploading DataFrame ({len(df)} rows, {len(df.columns)} columns)")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
            df.to_csv(tmp.name, index=False)
            tmp_path = Path(tmp.name)
        
        try:
            # Prepare form data
            data = {}
            if name:
                data['name'] = name
            if session_name_prefix:
                data['session_name_prefix'] = session_name_prefix
            if epochs is not None:
                data['epochs'] = str(epochs)
            
            # Add any additional kwargs as form data
            for key, value in kwargs.items():
                if value is not None:
                    if isinstance(value, (dict, list)):
                        import json
                        data[key] = json.dumps(value)
                    else:
                        data[key] = str(value)
            
            # Upload the file
            with open(tmp_path, 'rb') as f:
                files = {'file': (filename, f, 'text/csv')}
                response = self._make_request("POST", "/compute/upload_with_new_session/", 
                                            files=files, data=data)
            
            response_data = response.json()
            session_id = response_data.get('session_id')
            
            print(f"DataFrame uploaded, session created: {session_id}")
            
            # Check for and display warnings
            warnings = response_data.get('warnings', [])
            if warnings:
                print("\n" + "="*60)
                print("⚠️  UPLOAD WARNINGS")
                print("="*60)
                for warning in warnings:
                    print(warning)
                print("="*60 + "\n")
            
            return SessionInfo(
                session_id=session_id,
                session_type=response_data.get('session_type', 'sphere'),
                status=response_data.get('status', 'ready'),
                jobs={},
                job_queue_positions={}
            )
        finally:
            # Clean up temporary file
            try:
                tmp_path.unlink()
            except Exception:
                pass

    # =========================================================================
    # Single Predictor Functionality
    # =========================================================================
    
    def make_prediction(self, session_id: str, query_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a prediction using a trained single predictor.
        
        Args:
            session_id: ID of session with trained predictor
            query_record: Record to make prediction for
            
        Returns:
            Prediction results
        """
        print(f"Making prediction for session {session_id}")
        print(f"Query record: {query_record}")
        
        data = {"query_record": query_record}
        response_data = self._post_json(f"/compute/session/{session_id}/predict", data)
        
        prediction = response_data.get('prediction')
        print(f"Prediction result: {prediction}")
        
        return response_data
    
    def get_training_metrics(self, session_id: str) -> Dict[str, Any]:
        """
        Get training metrics for a session's single predictor.
        
        Args:
            session_id: ID of session with trained single predictor
            
        Returns:
            Training metrics including loss history, validation metrics, etc.
        """
        print(f"Getting training metrics for session {session_id}")
        
        response_data = self._get_json(f"/compute/session/{session_id}/training_metrics")
        
        metrics = response_data.get('training_metrics', {})
        print(f"Retrieved metrics for {len(metrics.get('loss_history', []))} training epochs")
        
        return response_data

    def train_single_predictor(self, session_id: str, target_column: str, target_column_type: str, 
                              epochs: int = 50, batch_size: int = 256, learning_rate: float = 0.001,
                              positive_label: str = None) -> Dict[str, Any]:
        """
        Add single predictor training to an existing session that has a trained embedding space.
        
        Args:
            session_id: ID of session with trained embedding space
            target_column: Name of the target column to predict
            target_column_type: Type of target column ("set" or "scalar")
            epochs: Number of training epochs (default: 50)
            batch_size: Training batch size (default: 256)
            learning_rate: Learning rate for training (default: 0.001)
            positive_label: Positive label for binary classification (default: None)
            
        Returns:
            Response with training start confirmation
        """
        print(f"Starting single predictor training on session {session_id}")
        print(f"Target: {target_column} (type: {target_column_type})")
        print(f"Training config: epochs={epochs}, batch_size={batch_size}, lr={learning_rate}")
        if positive_label:
            print(f"Positive label: {positive_label}")
        
        data = {
            "target_column": target_column,
            "target_column_type": target_column_type,
            "epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "positive_label": positive_label
        }
        
        response_data = self._post_json(f"/compute/session/{session_id}/train_predictor", data)
        
        print(f"✅ Single predictor training started: {response_data.get('message')}")
        
        return response_data

    # =========================================================================
    # JSON Tables Batch Prediction
    # =========================================================================
    
    def predict_records(self, session_id: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Make batch predictions on a list of records.
        
        Args:
            session_id: ID of session with trained predictor
            records: List of record dictionaries
            
        Returns:
            Batch prediction results
        """
        # Convert to JSON Tables format
        from jsontables import JSONTablesEncoder
        table_data = JSONTablesEncoder.from_records(records)
        
        return self.predict_table(session_id, table_data)
    
    def predict_table(self, session_id: str, table_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make batch predictions using JSON Tables format.
        
        Args:
            session_id: ID of session with trained predictor
            table_data: Data in JSON Tables format, or list of records, or dict with 'table'/'records'
            
        Returns:
            Batch prediction results in JSON Tables format
        """
        response_data = self._post_json(f"/compute/session/{session_id}/predict_table", table_data)
        return response_data
    
    def predict_csv_file(self, session_id: str, file_path: Path) -> Dict[str, Any]:
        """
        Make batch predictions on a CSV file.
        
        Args:
            session_id: ID of session with trained predictor
            file_path: Path to CSV file
            
        Returns:
            Batch prediction results
        """
        import pandas as pd
        from jsontables import JSONTablesEncoder
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"Loading CSV file: {file_path}")
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        
        # Convert to JSON Tables format
        table_data = JSONTablesEncoder.from_dataframe(df)
        
        return self.predict_table(session_id, table_data)

    def test_predictions(self, session_id: str, records: List[Dict[str, Any]], 
                        actual_values: List[str] = None, target_column: str = None) -> Dict[str, Any]:
        """
        Test predictions on all provided records with optional accuracy calculation.
        
        Args:
            session_id: ID of session with trained predictor
            records: List of record dictionaries (without target column)
            actual_values: Optional list of actual target values for accuracy calculation
            target_column: Name of target column (for display purposes)
            
        Returns:
            Dictionary with prediction results, accuracy metrics, and detailed analysis
        """
        # Try batch predictions
        try:
            batch_results = self.predict_records(session_id, records)
            predictions = batch_results['predictions']
            
            analysis = {
                'total_records': len(records),
                'successful_predictions': len([p for p in predictions if p['prediction']]),
                'failed_predictions': len([p for p in predictions if not p['prediction']]),
                'predictions': [],
                'accuracy_metrics': None
            }
            
            # Process predictions
            correct_predictions = 0
            total_valid_predictions = 0
            confidence_scores = []
            
            for i, pred in enumerate(predictions):
                if pred['prediction']:
                    record_idx = pred['row_index']
                    prediction = pred['prediction']
                    
                    # Get predicted class and confidence
                    predicted_class = max(prediction, key=prediction.get)
                    confidence = prediction[predicted_class]
                    confidence_scores.append(confidence)
                    
                    prediction_info = {
                        'record_index': record_idx,
                        'record': records[record_idx] if record_idx < len(records) else None,
                        'prediction': prediction,
                        'predicted_class': predicted_class,
                        'confidence': confidence,
                        'actual_value': None,
                        'correct': None
                    }
                    
                    # Compare with actual if available
                    if actual_values and record_idx < len(actual_values):
                        actual = str(actual_values[record_idx])
                        prediction_info['actual_value'] = actual
                        prediction_info['correct'] = (predicted_class == actual)
                        
                        if predicted_class == actual:
                            correct_predictions += 1
                        total_valid_predictions += 1
                    
                    analysis['predictions'].append(prediction_info)
            
            # Calculate accuracy metrics if we have ground truth
            if actual_values and total_valid_predictions > 0:
                accuracy = correct_predictions / total_valid_predictions
                avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
                
                analysis['accuracy_metrics'] = {
                    'accuracy': accuracy,
                    'correct_predictions': correct_predictions,
                    'total_predictions': total_valid_predictions,
                    'average_confidence': avg_confidence,
                    'target_column': target_column
                }
            
            return analysis
            
        except Exception as e:
            print(f"Error in prediction testing: {e}")
            raise

    def test_csv_predictions(self, session_id: str, csv_file: str, target_column: str = None,
                           sample_size: int = None, remove_target: bool = True) -> Dict[str, Any]:
        """
        Test predictions on a CSV file with automatic accuracy calculation.
        
        Args:
            session_id: ID of session with trained predictor
            csv_file: Path to CSV file
            target_column: Name of target column (if present in CSV)
            sample_size: Number of records to test (default: None = process ALL records)
            remove_target: Whether to remove target column from prediction input
            
        Returns:
            Dictionary with prediction results and accuracy metrics
        """
        import pandas as pd
        
        # Load CSV
        df = pd.read_csv(csv_file)
        
        # Handle target column
        actual_values = None
        if target_column and target_column in df.columns:
            actual_values = df[target_column].tolist()
            if remove_target:
                prediction_df = df.drop(target_column, axis=1)
            else:
                prediction_df = df
        else:
            prediction_df = df
        
        # Take sample ONLY if explicitly requested
        if sample_size and sample_size < len(prediction_df):
            sample_df = prediction_df.head(sample_size)
            if actual_values:
                actual_values = actual_values[:sample_size]
        else:
            sample_df = prediction_df
        
        # Convert to records
        records = sample_df.to_dict('records')
        
        # Run predictions with accuracy testing
        return self.test_predictions(
            session_id=session_id,
            records=records,
            actual_values=actual_values,
            target_column=target_column
        )

    def run_comprehensive_test(self, session_id: str, test_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run a comprehensive test of the single predictor including individual and batch predictions.
        
        Args:
            session_id: ID of session with trained predictor
            test_data: Optional dict with 'csv_file', 'target_column', 'sample_size', 'test_records'
            
        Returns:
            Comprehensive test results
        """
        print("🧪 " + "="*60)
        print("🧪 COMPREHENSIVE SINGLE PREDICTOR TEST")
        print("🧪 " + "="*60)
        
        results = {
            'session_id': session_id,
            'individual_tests': [],
            'batch_test': None,
            'training_metrics': None,
            'session_models': None
        }
        
        # 1. Check session models
        print("\n1. 📦 Checking available models...")
        try:
            models_info = self.get_session_models(session_id)
            results['session_models'] = models_info
        except Exception as e:
            print(f"Error checking models: {e}")
        
        # 2. Get training metrics
        print("\n2. 📊 Getting training metrics...")
        try:
            metrics = self.get_training_metrics(session_id)
            results['training_metrics'] = metrics
            
            training_metrics = metrics['training_metrics']
            print(f"Target column: {training_metrics.get('target_column')}")
            print(f"Target type: {training_metrics.get('target_column_type')}")
            print(f"Training epochs: {len(training_metrics.get('training_info', []))}")
        except Exception as e:
            print(f"Error getting training metrics: {e}")
        
        # 3. Individual prediction tests
        print("\n3. 🎯 Testing individual predictions...")
        
        # Default test records if none provided
        default_test_records = [
            {"domain": "shell.com", "snippet": "fuel card rewards program", "keyword": "fuel card"},
            {"domain": "exxon.com", "snippet": "gas station locator and fuel cards", "keyword": "gas station"},
            {"domain": "amazon.com", "snippet": "buy books online", "keyword": "books"},
            {"domain": "bp.com", "snippet": "fleet fuel cards for business", "keyword": "fleet cards"},
        ]
        
        test_records = test_data.get('test_records', default_test_records) if test_data else default_test_records
        
        for i, record in enumerate(test_records):
            try:
                result = self.make_prediction(session_id, record)
                prediction = result['prediction']
                
                # Get predicted class and confidence
                predicted_class = max(prediction, key=prediction.get)
                confidence = prediction[predicted_class]
                
                test_result = {
                    'record': record,
                    'prediction': prediction,
                    'predicted_class': predicted_class,
                    'confidence': confidence,
                    'success': True
                }
                
                results['individual_tests'].append(test_result)
                print(f"✅ Record {i+1}: {predicted_class} ({confidence*100:.1f}% confidence)")
                
            except Exception as e:
                test_result = {
                    'record': record,
                    'error': str(e),
                    'success': False
                }
                results['individual_tests'].append(test_result)
                print(f"❌ Record {i+1}: Error - {e}")
        
        # 4. Batch prediction test
        print("\n4. 📊 Testing batch predictions...")
        
        if test_data and test_data.get('csv_file'):
            try:
                batch_results = self.test_csv_predictions(
                    session_id=session_id,
                    csv_file=test_data['csv_file'],
                    target_column=test_data.get('target_column'),
                    sample_size=test_data.get('sample_size', 100)
                )
                results['batch_test'] = batch_results
                
                # Summary
                if batch_results.get('accuracy_metrics'):
                    acc = batch_results['accuracy_metrics']
                    print(f"✅ Batch test completed: {acc['accuracy']*100:.2f}% accuracy")
                else:
                    print(f"✅ Batch test completed: {batch_results['successful_predictions']} predictions")
                    
            except Exception as e:
                print(f"❌ Batch test failed: {e}")
                results['batch_test'] = {'error': str(e)}
        else:
            print("📝 No CSV file provided for batch testing")
        
        # 5. Summary
        print("\n" + "="*60)
        print("📋 TEST SUMMARY")
        print("="*60)
        
        individual_success = sum(1 for t in results['individual_tests'] if t['success'])
        print(f"Individual predictions: {individual_success}/{len(results['individual_tests'])} successful")
        
        if results['batch_test'] and 'accuracy_metrics' in results['batch_test']:
            acc = results['batch_test']['accuracy_metrics']
            print(f"Batch prediction accuracy: {acc['accuracy']*100:.2f}%")
            print(f"Average confidence: {acc['average_confidence']*100:.2f}%")
        
        if results['training_metrics']:
            tm = results['training_metrics']['training_metrics']
            print(f"Model trained on: {tm.get('target_column')} ({tm.get('target_column_type')})")
        
        print("\n🎉 Comprehensive test completed!")
        
        return results

    # =========================================================================
    # Other API Endpoints
    # =========================================================================
    
    def encode_records(self, session_id: str, query_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encode records using the embedding space.
        
        Args:
            session_id: ID of session with trained embedding space
            query_record: Record to encode
            
        Returns:
            Encoded vector representation
        """
        print(f"Encoding record for session {session_id}")
        
        data = {"query_record": query_record}
        response_data = self._post_json(f"/compute/session/{session_id}/encode_records", data)
        
        embedding = response_data.get('embedding')
        print(f"Embedding dimension: {len(embedding) if embedding else 'None'}")
        
        return response_data
    
    def similarity_search(self, session_id: str, query_record: Dict[str, Any], k: int = 5) -> Dict[str, Any]:
        """
        Find similar records using vector similarity search.
        
        Args:
            session_id: ID of session with trained embedding space and vector DB
            query_record: Record to find similarities for
            k: Number of similar records to return
            
        Returns:
            List of similar records with distances
        """
        print(f"Performing similarity search for session {session_id} (k={k})")
        
        data = {"query_record": query_record}
        response_data = self._post_json(f"/compute/session/{session_id}/similarity_search", data)
        
        results = response_data.get('results', [])
        print(f"Found {len(results)} similar records")
        
        return response_data
    
    def add_records(self, session_id: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add new records to an existing vector database for similarity search.
        
        Args:
            session_id: ID of session with trained embedding space and vector DB
            records: List of dictionaries containing the new records to add
            
        Returns:
            Statistics about the append operation
        """
        print(f"Adding {len(records)} records to vector database for session {session_id}")
        
        data = {"records": records}
        response_data = self._post_json(f"/compute/session/{session_id}/add_records", data)
        
        records_added = response_data.get('records_added', 0)
        records_failed = response_data.get('records_failed', 0)
        new_total = response_data.get('new_total', 0)
        
        print(f"✅ Added {records_added} records (failed: {records_failed})")
        print(f"📊 New total records in vector DB: {new_total}")
        
        return response_data
    
    def get_projections(self, session_id: str) -> Dict[str, Any]:
        """
        Get 2D projections for visualization.
        
        Args:
            session_id: ID of session with generated projections
            
        Returns:
            Projection data for visualization
        """
        print(f"Getting projections for session {session_id}")
        
        response_data = self._get_json(f"/compute/session/{session_id}/projections")
        
        projections = response_data.get('projections')
        print(f"Retrieved projections data")
        
        return response_data

    def run_predictions(self, session_id: str, data, target_column: str = None, 
                       remove_target: bool = True, show_details: bool = True,
                       batch_size: int = 1000) -> Dict[str, Any]:
        """
        Run predictions on flexible input data (DataFrame or list of dicts).
        Automatically chunks large datasets for progress monitoring.
        
        Args:
            session_id: ID of session with trained predictor
            data: Either pandas DataFrame or list of dictionaries
            target_column: Name of target column (if present) for accuracy calculation
            remove_target: Whether to remove target column from prediction input
            show_details: Whether to show detailed prediction results
            batch_size: Size of batches for large datasets (default: 1000)
            
        Returns:
            Dictionary with prediction results, accuracy metrics, and detailed analysis
        """
        import pandas as pd
        
        # Convert input to standardized format
        if isinstance(data, pd.DataFrame):
            df = data.copy()
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            raise ValueError(f"Unsupported data type: {type(data)}. Use pandas DataFrame or list of dicts.")
        
        # Handle target column for accuracy calculation
        actual_values = None
        if target_column and target_column in df.columns:
            actual_values = df[target_column].tolist()
            if remove_target:
                prediction_df = df.drop(target_column, axis=1)
            else:
                prediction_df = df
        else:
            prediction_df = df
        
        total_records = len(prediction_df)
        
        # Convert to records for prediction
        records = prediction_df.to_dict('records')
        
        # Determine if we need chunking for large datasets
        if total_records > batch_size:
            return self._run_chunked_predictions(
                session_id=session_id,
                records=records,
                actual_values=actual_values,
                target_column=target_column,
                show_details=show_details,
                batch_size=batch_size
            )
        else:
            return self.test_predictions(
                session_id=session_id,
                records=records,
                actual_values=actual_values,
                target_column=target_column
            )
    
    def _run_chunked_predictions(self, session_id: str, records: List[Dict[str, Any]], 
                               actual_values: List[str] = None, target_column: str = None,
                               show_details: bool = True, batch_size: int = 1000) -> Dict[str, Any]:
        """
        Run predictions in chunks for large datasets with progress monitoring.
        
        Args:
            session_id: ID of session with trained predictor
            records: List of record dictionaries
            actual_values: Optional list of actual target values
            target_column: Name of target column
            show_details: Whether to show detailed prediction results
            batch_size: Size of each chunk
            
        Returns:
            Combined prediction results from all chunks
        """
        import math
        
        total_records = len(records)
        num_chunks = math.ceil(total_records / batch_size)
        
        # Initialize combined results
        all_predictions = []
        total_correct = 0
        total_successful = 0
        total_failed = 0
        all_confidence_scores = []
        
        # Process each chunk
        for chunk_idx in range(num_chunks):
            start_idx = chunk_idx * batch_size
            end_idx = min(start_idx + batch_size, total_records)
            
            chunk_records = records[start_idx:end_idx]
            chunk_actual = actual_values[start_idx:end_idx] if actual_values else None
            chunk_size = len(chunk_records)
            
            try:
                # Try batch prediction for this chunk - NO FALLBACK
                chunk_results = self.test_predictions(
                    session_id=session_id,
                    records=chunk_records,
                    actual_values=chunk_actual,
                    target_column=target_column
                )
                
                # Accumulate results
                chunk_predictions = chunk_results.get('predictions', [])
                
                # Adjust record indices for global indexing
                for pred in chunk_predictions:
                    if 'record_index' in pred:
                        pred['record_index'] += start_idx
                
                all_predictions.extend(chunk_predictions)
                total_successful += chunk_results.get('successful_predictions', 0)
                total_failed += chunk_results.get('failed_predictions', 0)
                
                # Accumulate accuracy metrics
                if chunk_results.get('accuracy_metrics'):
                    chunk_acc = chunk_results['accuracy_metrics']
                    total_correct += chunk_acc.get('correct_predictions', 0)
                    
                    # Collect confidence scores
                    for pred in chunk_predictions:
                        if pred.get('success') and pred.get('confidence'):
                            all_confidence_scores.append(pred['confidence'])
                
            except Exception as e:
                # Continue with next chunk
                continue
        
        # Combine final results
        analysis = {
            'total_records': total_records,
            'successful_predictions': total_successful,
            'failed_predictions': total_failed,
            'predictions': all_predictions,
            'accuracy_metrics': None,
            'chunked_processing': True,
            'num_chunks': num_chunks,
            'batch_size': batch_size
        }
        
        # Calculate overall accuracy metrics
        if actual_values and total_correct > 0:
            total_valid = total_successful if target_column else len([p for p in all_predictions if p.get('success')])
            accuracy = total_correct / total_valid if total_valid > 0 else 0
            avg_confidence = sum(all_confidence_scores) / len(all_confidence_scores) if all_confidence_scores else 0
            
            analysis['accuracy_metrics'] = {
                'accuracy': accuracy,
                'correct_predictions': total_correct,
                'total_predictions': total_valid,
                'average_confidence': avg_confidence,
                'target_column': target_column
            }
        
        return analysis

    def _run_individual_predictions(self, session_id: str, records: List[Dict[str, Any]], 
                                  actual_values: List[str] = None, target_column: str = None,
                                  show_details: bool = True) -> Dict[str, Any]:
        """
        Run individual predictions when batch predictions are not available.
        
        Args:
            session_id: ID of session with trained predictor
            records: List of record dictionaries
            actual_values: Optional list of actual target values
            target_column: Name of target column
            show_details: Whether to show detailed prediction results
            
        Returns:
            Dictionary with prediction results and accuracy metrics
        """
        print(f"🎯 Running {len(records)} individual predictions...")
        
        predictions = []
        correct_predictions = 0
        total_valid_predictions = 0
        confidence_scores = []
        
        for i, record in enumerate(records):
            try:
                # Make individual prediction
                result = self.make_prediction(session_id, record)
                prediction = result.get('prediction', {})
                
                if prediction:
                    # Get predicted class and confidence
                    predicted_class = max(prediction, key=prediction.get)
                    confidence = prediction[predicted_class]
                    confidence_scores.append(confidence)
                    
                    # Build prediction info
                    prediction_info = {
                        'record_index': i,
                        'record': record,
                        'prediction': prediction,
                        'predicted_class': predicted_class,
                        'confidence': confidence,
                        'actual_value': None,
                        'correct': None,
                        'success': True
                    }
                    
                    # Compare with actual if available
                    if actual_values and i < len(actual_values):
                        actual = str(actual_values[i])
                        prediction_info['actual_value'] = actual
                        prediction_info['correct'] = (str(predicted_class) == actual)
                        
                        if str(predicted_class) == actual:
                            correct_predictions += 1
                        total_valid_predictions += 1
                        
                        correct_symbol = "✅" if predicted_class == actual else "❌"
                        print(f"{i+1:3d}. {correct_symbol} Predicted: {predicted_class} ({confidence*100:.1f}% confidence) | Actual: {actual}")
                    else:
                        print(f"{i+1:3d}. ✅ Predicted: {predicted_class} ({confidence*100:.1f}% confidence)")
                    
                    predictions.append(prediction_info)
                    
                else:
                    prediction_info = {
                        'record_index': i,
                        'record': record,
                        'error': 'No prediction returned',
                        'success': False
                    }
                    predictions.append(prediction_info)
                    if show_details:
                        print(f"{i+1:3d}. ❌ No prediction returned")
                
            except Exception as e:
                prediction_info = {
                    'record_index': i,
                    'record': record,
                    'error': str(e),
                    'success': False
                }
                predictions.append(prediction_info)
                if show_details:
                    print(f"{i+1:3d}. ❌ Error: {e}")
        
        # Calculate metrics
        successful_predictions = sum(1 for p in predictions if p['success'])
        failed_predictions = len(predictions) - successful_predictions
        
        analysis = {
            'total_records': len(records),
            'successful_predictions': successful_predictions,
            'failed_predictions': failed_predictions,
            'predictions': predictions,
            'accuracy_metrics': None
        }
        
        # Calculate accuracy metrics if we have ground truth
        if actual_values and total_valid_predictions > 0:
            accuracy = correct_predictions / total_valid_predictions
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
            
            analysis['accuracy_metrics'] = {
                'accuracy': accuracy,
                'correct_predictions': correct_predictions,
                'total_predictions': total_valid_predictions,
                'average_confidence': avg_confidence,
                'target_column': target_column
            }
            
            print(f"\n🎯 PREDICTION RESULTS:")
            print(f"Total records: {len(records)}")
            print(f"Successful predictions: {successful_predictions}")
            print(f"Failed predictions: {failed_predictions}")
            print(f"Accuracy: {accuracy*100:.2f}% ({correct_predictions}/{total_valid_predictions})")
            print(f"Average confidence: {avg_confidence*100:.2f}%")
            if target_column:
                print(f"Target column: {target_column}")
        else:
            print(f"\n📊 PREDICTION SUMMARY:")
            print(f"Total records: {len(records)}")
            print(f"Successful predictions: {successful_predictions}")
            print(f"Failed predictions: {failed_predictions}")
            if confidence_scores:
                avg_confidence = sum(confidence_scores) / len(confidence_scores)
                print(f"Average confidence: {avg_confidence*100:.2f}%")
        
        return analysis


def main():
    """Example usage of the API client."""
    
    # Initialize client
    client = FeatrixSphereClient("https://sphere-api.featrix.com")
    
    print("=== Featrix Sphere API Client Test ===\n")
    
    try:
        # Example 1: Create a session and check status
        print("1. Creating a new session...")
        session_info = client.create_session("sphere")
        print(f"Session created: {session_info.session_id}\n")
        
        # Example 2: Check session status
        print("2. Checking session status...")
        current_status = client.get_session_status(session_info.session_id)
        print(f"Current status: {current_status.status}\n")
        
        # Example 3: Upload a file (if test data exists)
        test_file = Path("featrix_data/test.csv")
        if test_file.exists():
            print("3. Uploading test file...")
            upload_session = client.upload_file_and_create_session(test_file)
            print(f"Upload session: {upload_session.session_id}\n")
        else:
            print("3. Skipping file upload (test.csv not found)\n")
        
        print("API client test completed successfully!")
        
    except Exception as e:
        print(f"Error during API client test: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 