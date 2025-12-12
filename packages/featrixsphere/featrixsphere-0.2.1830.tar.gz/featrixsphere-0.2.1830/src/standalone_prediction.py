#!/usr/bin/env python3
"""
Standalone prediction script for Celery subprocess approach.
This avoids all fork/CUDA/import issues by running in a clean process.
Uses JSON Tables format for efficient output.
"""

import sys
import json
import logging
import traceback
from pathlib import Path
import redis
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ProgressReporter:
    """Redis-based progress reporter for subprocess prediction jobs."""
    
    def __init__(self, job_id: str, max_messages: int = 30):
        self.job_id = job_id
        self.redis_key = f"prediction_progress:{job_id}"
        self.redis_messages_key = f"prediction_messages:{job_id}"  # New: List of progress messages
        self.max_messages = max_messages  # Keep last N messages
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
            self.redis_available = True
            logger.info(f"✅ Redis connected for progress tracking: {self.redis_key}")
        except Exception as e:
            logger.warning(f"⚠️ Redis not available for progress tracking: {e}")
            self.redis_available = False
    
    def update_progress(self, current: float, total: int, status: str, metadata: dict = None):
        """Update progress in Redis - stores current state AND appends to message history."""
        if not self.redis_available:
            return
        
        try:
            progress_data = {
                'current': current,
                'total': total,
                'percentage': round((current / total) * 100, 2) if total > 0 else 0,
                'status': status,
                'timestamp': time.time(),
                'job_id': self.job_id
            }
            
            if metadata:
                progress_data.update(metadata)
            
            # Store current progress state (overwrites each time)
            self.redis_client.setex(self.redis_key, 3600, json.dumps(progress_data))
            
            # Also append to message history list (keeps last N messages)
            message_entry = {
                'percentage': progress_data['percentage'],
                'status': status,
                'timestamp': progress_data['timestamp'],
                'current': current,
                'total': total
            }
            
            # Push to the right (end) of the list
            self.redis_client.rpush(self.redis_messages_key, json.dumps(message_entry))
            
            # Trim to keep only last max_messages entries
            self.redis_client.ltrim(self.redis_messages_key, -self.max_messages, -1)
            
            # Set expiration on messages list
            self.redis_client.expire(self.redis_messages_key, 3600)
            
            logger.info(f"📊 Progress: {current}/{total} ({progress_data['percentage']}%) - {status}")
            
        except Exception as e:
            logger.warning(f"Failed to update progress in Redis: {e}")
    
    def set_completed(self, success: bool, final_stats: dict):
        """Mark job as completed."""
        if not self.redis_available:
            return
        
        try:
            completion_data = {
                'completed': True,
                'success': success,
                'timestamp': time.time(),
                'job_id': self.job_id,
                **final_stats
            }
            
            # Store completion status with longer expiration
            self.redis_client.setex(self.redis_key, 7200, json.dumps(completion_data))  # 2 hours
            logger.info(f"✅ Job marked as completed: success={success}")
            
        except Exception as e:
            logger.warning(f"Failed to mark completion in Redis: {e}")
    
    def set_error(self, error_message: str):
        """Mark job as failed."""
        if not self.redis_available:
            return
        
        try:
            error_data = {
                'completed': True,
                'success': False,
                'error': error_message,
                'timestamp': time.time(),
                'job_id': self.job_id
            }
            
            self.redis_client.setex(self.redis_key, 7200, json.dumps(error_data))  # 2 hours
            logger.error(f"❌ Job marked as failed: {error_message}")
            
        except Exception as e:
            logger.warning(f"Failed to mark error in Redis: {e}")

def setup_paths():
    """Set up Python paths for imports."""
    current_path = Path(__file__).parent
    lib_path = current_path / "lib"
    
    if str(lib_path.resolve()) not in sys.path:
        sys.path.insert(0, str(lib_path.resolve()))
    if str(current_path.resolve()) not in sys.path:
        sys.path.insert(0, str(current_path.resolve()))
    
    logger.info(f"✅ Paths configured: lib={lib_path}, current={current_path}")

def main():
    """Main prediction function."""
    try:
        # Read command line arguments
        if len(sys.argv) != 4:
            logger.error("Usage: standalone_prediction.py <input_file> <output_file> <job_id>")
            sys.exit(1)
        
        input_file = Path(sys.argv[1])
        output_file = Path(sys.argv[2])
        job_id = sys.argv[3]
        
        # Initialize progress reporter
        progress = ProgressReporter(job_id)
        
        logger.info(f"🚀 Starting prediction: {input_file} -> {output_file}")
        progress.update_progress(0, 100, "Initializing prediction process...")
        
        # Set up paths
        setup_paths()
        progress.update_progress(5, 100, "Python paths configured")
        
        # Read input data
        progress.update_progress(10, 100, "Loading input data...")
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        session_id = data['session_id']
        predictor_path = data['predictor_path']
        records = data['records']
        batch_size = data.get('batch_size', 256)
        
        logger.info(f"📊 Loaded {len(records)} records for session {session_id}")
        logger.info(f"🎯 Predictor: {predictor_path}")
        
        progress.update_progress(15, 100, f"Loaded {len(records)} records", {
            'total_records': len(records),
            'session_id': session_id
        })
        
        # Import required modules in clean process
        progress.update_progress(20, 100, "Importing PyTorch and dependencies...")
        import torch
        import pickle
        
        # Import JSON Tables for efficient output
        try:
            from jsontables import JSONTablesEncoder
            logger.info(f"✅ JSON Tables imported for efficient output")
        except ImportError:
            logger.warning(f"⚠️ JSON Tables not available, falling back to regular JSON")
            JSONTablesEncoder = None
        
        logger.info(f"✅ Torch available: {torch.cuda.is_available()}")
        progress.update_progress(25, 100, f"PyTorch loaded, CUDA: {torch.cuda.is_available()}")
        
        # Load the predictor
        logger.info(f"📦 Loading predictor from {predictor_path}")
        progress.update_progress(30, 100, "Loading ML predictor model...")
        with open(predictor_path, "rb") as f:
            fsp = pickle.load(f)
        
        logger.info(f"✅ Predictor loaded: {getattr(fsp, 'target_col_name', 'Unknown')}")
        
        # Hydrate to GPU
        logger.info(f"🔄 Hydrating to GPU...")
        progress.update_progress(40, 100, "Moving model to GPU...")
        fsp.hydrate_to_gpu_if_needed()
        fsp.embedding_space.hydrate_to_gpu_if_needed()
        
        if torch.cuda.is_available():
            gpu_memory_mb = torch.cuda.memory_allocated() / 1024 / 1024
            logger.info(f"🖥️ GPU Memory: {gpu_memory_mb:.1f}MB")
        
        progress.update_progress(50, 100, "GPU ready, starting predictions...")
        
        # Define progress callback for batch prediction
        def batch_progress_callback(current_batch, total_batches, message):
            """Report progress during batch processing."""
            # Smooth progress from 60.00 to 80.00 with 2 decimal places for fine granularity
            batch_progress = (current_batch / total_batches) if total_batches > 0 else 0
            overall_percent = 60.0 + (batch_progress * 20.0)  # 60.00 to 80.00
            progress.update_progress(round(overall_percent, 2), 100, message)
        
        # Make predictions
        logger.info(f"🔄 Starting batch prediction...")
        progress.update_progress(60, 100, f"Processing {len(records)} records...")
        
        predictions = fsp.predict_batch(
            records, 
            batch_size=batch_size,
            debug_print=False,
            extended_result=True,
            progress_callback=batch_progress_callback
        )
        
        logger.info(f"✅ Completed {len(predictions)} predictions")
        progress.update_progress(80, 100, f"Completed {len(predictions)} predictions")
        
        # Convert predictions to table format for efficient storage
        logger.info(f"🔄 Converting to efficient JSON Tables format...")
        progress.update_progress(85, 100, "Converting to JSON Tables format...")
        
        # Build results table records
        results_records = []
        successful_count = 0
        failed_count = 0
        
        # For large batches, collect guardrails data for summarization instead of including in every record
        large_batch_threshold = 1000
        should_summarize = len(predictions) >= large_batch_threshold
        guardrails_summary = {
            'issues_histogram': {},
            'missing_columns_histogram': {},
            'ignored_columns_histogram': {},
            'total_records_with_issues': 0,
            'total_records_missing_columns': 0,
            'total_records_ignored_columns': 0
        } if should_summarize else None
        
        if should_summarize:
            logger.info(f"📊 Large batch ({len(predictions)} records) - will summarize guardrails instead of per-record details")
        
        for i, prediction_result in enumerate(predictions):
            # Start with original record
            result_record = records[i].copy()
            result_record['row_index'] = i
            
            # Process prediction result
            if isinstance(prediction_result, dict):
                if 'results' in prediction_result and prediction_result['results'] is not None:
                    prediction = prediction_result['results']
                    successful_count += 1
                    
                    # Add prediction columns
                    if isinstance(prediction, dict):
                        # Classification - add probability columns
                        for class_name, prob in prediction.items():
                            result_record[f"pred_{class_name}"] = prob
                        # Add predicted class
                        predicted_class = max(prediction, key=prediction.get)
                        result_record["predicted_class"] = predicted_class
                        result_record["confidence"] = prediction[predicted_class]
                    else:
                        # Regression or other prediction format
                        result_record["prediction"] = prediction
                        result_record["predicted_class"] = None
                        result_record["confidence"] = None
                    
                    # Handle guardrails metadata
                    if 'guardrails' in prediction_result:
                        if should_summarize:
                            # For large batches, aggregate guardrails into summary histograms
                            gr = prediction_result['guardrails']
                            
                            # Track issues
                            if gr.get('issues'):
                                guardrails_summary['total_records_with_issues'] += 1
                                for issue_type in gr['issues']:
                                    guardrails_summary['issues_histogram'][issue_type] = \
                                        guardrails_summary['issues_histogram'].get(issue_type, 0) + 1
                            
                            # Track missing columns
                            if gr.get('missing_columns'):
                                guardrails_summary['total_records_missing_columns'] += 1
                                for col in gr['missing_columns']:
                                    guardrails_summary['missing_columns_histogram'][col] = \
                                        guardrails_summary['missing_columns_histogram'].get(col, 0) + 1
                            
                            # Track ignored columns
                            if gr.get('ignored_columns'):
                                guardrails_summary['total_records_ignored_columns'] += 1
                                for col in gr['ignored_columns']:
                                    guardrails_summary['ignored_columns_histogram'][col] = \
                                        guardrails_summary['ignored_columns_histogram'].get(col, 0) + 1
                        else:
                            # For small batches, include full guardrails per record
                            result_record["guardrails"] = prediction_result['guardrails']
                    
                    result_record["prediction_error"] = None
                else:
                    failed_count += 1
                    result_record["prediction_error"] = "No prediction result"
                    result_record["predicted_class"] = None
                    result_record["confidence"] = None
                    
            elif prediction_result is not None:
                # Simple prediction format
                successful_count += 1
                if isinstance(prediction_result, dict):
                    for class_name, prob in prediction_result.items():
                        result_record[f"pred_{class_name}"] = prob
                    predicted_class = max(prediction_result, key=prediction_result.get)
                    result_record["predicted_class"] = predicted_class
                    result_record["confidence"] = prediction_result[predicted_class]
                else:
                    result_record["prediction"] = prediction_result
                    result_record["predicted_class"] = None
                    result_record["confidence"] = None
                result_record["prediction_error"] = None
            else:
                failed_count += 1
                result_record["prediction_error"] = "Null prediction result"
                result_record["predicted_class"] = None
                result_record["confidence"] = None
            
            results_records.append(result_record)
        
        logger.info(f"📊 Results: {successful_count} successful, {failed_count} failed")
        
        if should_summarize and guardrails_summary:
            logger.info(f"📊 Guardrails summary: {guardrails_summary['total_records_with_issues']} records with issues, "
                       f"{guardrails_summary['total_records_missing_columns']} with missing columns, "
                       f"{guardrails_summary['total_records_ignored_columns']} with ignored columns")
        
        progress.update_progress(90, 100, "Writing results...")
        
        # Convert to JSON Tables format if available
        if JSONTablesEncoder:
            logger.info(f"📊 Using JSON Tables for {len(results_records)} result records")
            progress.update_progress(92, 100, "Encoding to JSON Tables format...")
            results_table = JSONTablesEncoder.from_records(results_records)
            
            progress.update_progress(94, 100, "Preparing output data...")
            output_data = {
                'success': True,
                'format': 'json_tables',
                'results_table': results_table,
                'total_records': len(records),
                'successful_predictions': successful_count,
                'failed_predictions': failed_count,
                'session_id': session_id,
                'target_column': fsp.target_col_name,  # Add target column info
                'target_column_type': fsp.target_col_type  # Add target type info
            }
            
            # Add guardrails summary for large batches
            if should_summarize and guardrails_summary:
                output_data['guardrails_summary'] = guardrails_summary
                
        else:
            # Fallback to regular format
            logger.info(f"📊 Using regular JSON format for {len(predictions)} predictions")
            progress.update_progress(94, 100, "Preparing output data...")
            output_data = {
                'success': True,
                'format': 'legacy',
                'predictions': predictions,
                'total_records': len(records),
                'successful_predictions': successful_count,
                'failed_predictions': failed_count,
                'session_id': session_id,
                'target_column': fsp.target_col_name,  # Add target column info
                'target_column_type': fsp.target_col_type  # Add target type info
            }
            
            # Add guardrails summary for large batches
            if should_summarize and guardrails_summary:
                output_data['guardrails_summary'] = guardrails_summary
        
        progress.update_progress(96, 100, f"Writing {len(records)} records to disk...")
        with open(output_file, 'w') as f:
            json.dump(output_data, f, separators=(',', ':'))  # Compact JSON
        
        progress.update_progress(98, 100, "Cleaning up GPU memory...")
        logger.info(f"✅ Results written to {output_file} in {'JSON Tables' if JSONTablesEncoder else 'legacy'} format")
        
        # Cleanup GPU
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info(f"✅ GPU cache cleared")
        
        # Mark as completed
        final_stats = {
            'total_records': len(records),
            'successful_predictions': successful_count,
            'failed_predictions': failed_count,
            'session_id': session_id,
            'output_format': 'json_tables' if JSONTablesEncoder else 'legacy'
        }
        progress.set_completed(True, final_stats)
        progress.update_progress(100, 100, "Prediction job completed successfully!")
        
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"❌ Prediction failed: {e}")
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        
        # Report error to Redis if possible
        if 'progress' in locals():
            progress.set_error(f"{type(e).__name__}: {str(e)}")
        
        # Write error output
        try:
            output_data = {
                'success': False,
                'format': 'error',
                'error': str(e),
                'traceback': traceback.format_exc(),
                'session_id': data.get('session_id', 'unknown') if 'data' in locals() else 'unknown',
                'total_records': len(data.get('records', [])) if 'data' in locals() else 0,
                'exc_type': type(e).__name__,
                'exc_message': str(e)
            }
            
            with open(output_file, 'w') as f:
                json.dump(output_data, f)
                
        except Exception as write_error:
            logger.error(f"❌ Failed to write error output: {write_error}")
        
        sys.exit(1)

if __name__ == '__main__':
    main() 