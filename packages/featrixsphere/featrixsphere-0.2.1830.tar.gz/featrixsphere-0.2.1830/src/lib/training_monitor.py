#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.

"""
Training Monitor Integration

Posts training data to monitor.featrix.com for analysis and hyperparameter prediction.
Collects comprehensive column statistics, training metrics, and hyperparameters.
"""

import logging
import os
import socket
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, List
import requests
import pandas as pd

# Import clean_numpy_values from utils
from utils import clean_numpy_values

logger = logging.getLogger(__name__)


def get_column_statistics(
    df: pd.DataFrame,
    codecs: Dict[str, Any],
    input_data_set: Optional[Any] = None
) -> List[Dict[str, Any]]:
    """
    Collect comprehensive statistics for each column using detectors from FeatrixInputDataSet.
    
    Args:
        df: DataFrame with the data
        codecs: Dictionary mapping column names to codec objects
        input_data_set: Optional FeatrixInputDataSet object to get detectors from
        
    Returns:
        List of column statistics dictionaries
    """
    column_stats = []
    
    # Get detectors from input_data_set if provided
    detectors = {}
    if input_data_set is not None:
        if hasattr(input_data_set, '_detectors'):
            detectors = input_data_set._detectors
        elif hasattr(input_data_set, 'get_detector_for_col_name'):
            # Build detectors dict by calling get_detector_for_col_name for each column
            for col_name in df.columns:
                detector = input_data_set.get_detector_for_col_name(col_name)
                if detector:
                    detectors[col_name] = detector
    
    for col_name in df.columns:
        col_data = df[col_name]
        total_rows = len(col_data)
        non_null_count = col_data.notna().sum()
        null_count = col_data.isnull().sum()
        fill_rate = non_null_count / total_rows if total_rows > 0 else 0.0
        unique_count = col_data.nunique()
        
        col_info = {
            "column_name": col_name,
            "dtype": str(col_data.dtype),
            "total_rows": total_rows,
            "non_null_count": int(non_null_count),
            "null_count": int(null_count),
            "fill_rate": float(fill_rate),
            "unique_count": int(unique_count),
            "unique_ratio": float(unique_count / non_null_count) if non_null_count > 0 else 0.0,
        }
        
        # Get detector information first - detectors have the richest information
        detector = detectors.get(col_name)
        if detector:
            # Get detector type and confidence
            if hasattr(detector, 'get_codec_name'):
                col_info["detector_type"] = detector.get_codec_name()
            if hasattr(detector, 'confidence'):
                col_info["detector_confidence"] = float(detector.confidence())
            if hasattr(detector, 'get_meta_description'):
                meta_desc = detector.get_meta_description()
                if meta_desc:
                    col_info["detector_meta"] = meta_desc
            
            # Get comprehensive debug info from detector
            if hasattr(detector, 'get_debug_info'):
                debug_info = detector.get_debug_info()
                if debug_info:
                    # String complexity metrics from detector (most accurate)
                    if 'min_str_len' in debug_info:
                        col_info["string_length_min"] = int(debug_info.get('min_str_len', 0))
                    if 'max_str_len' in debug_info:
                        col_info["string_length_max"] = int(debug_info.get('max_str_len', 0))
                    if 'mean_str_len' in debug_info:
                        col_info["string_length_mean"] = float(debug_info.get('mean_str_len', 0))
                    if 'median_str_len' in debug_info:
                        col_info["string_length_median"] = float(debug_info.get('median_str_len', 0))
                    if 'quantile75_str_len' in debug_info:
                        col_info["string_length_q75"] = float(debug_info.get('quantile75_str_len', 0))
                    if 'std_str_len' in debug_info:
                        col_info["string_length_std"] = float(debug_info.get('std_str_len', 0))
                    if 'bertMaxLength' in debug_info:
                        col_info["bert_max_length"] = int(debug_info.get('bertMaxLength', 0))
                    
                    # String length distribution
                    if 'str_len_value_counts' in debug_info:
                        str_len_counts = debug_info['str_len_value_counts']
                        if str_len_counts:
                            # Convert to a more usable format
                            col_info["string_length_distribution"] = {str(k): int(v) for k, v in str_len_counts.items()}
                    
                    # Value counts from detector
                    if 'value_counts_10_largest' in debug_info:
                        col_info["top_10_values"] = {str(k): int(v) for k, v in debug_info['value_counts_10_largest'].items()}
                    if 'value_counts_10_weight' in debug_info:
                        col_info["top_10_values_total"] = int(debug_info['value_counts_10_weight'])
                    
                    # Detector-specific stats
                    if 'numUniques' in debug_info:
                        col_info["detector_num_uniques"] = int(debug_info['numUniques'])
                    if 'numNotNulls' in debug_info:
                        col_info["detector_num_not_nulls"] = int(debug_info['numNotNulls'])
                    if 'numNulls' in debug_info:
                        col_info["detector_num_nulls"] = int(debug_info['numNulls'])
            
            # Get detector-specific attributes
            # For string list detectors
            if hasattr(detector, 'delimiter'):
                col_info["delimiter"] = detector.delimiter
            if hasattr(detector, 'list_format'):
                col_info["list_format"] = detector.list_format
            if hasattr(detector, 'string_elements'):
                if detector.string_elements:
                    col_info["unique_string_elements"] = len(detector.string_elements)
                    if len(detector.string_elements) <= 100:
                        col_info["string_elements"] = list(detector.string_elements)
            
            # For set detectors
            if hasattr(detector, 'set_delimiter'):
                col_info["set_delimiter"] = detector.set_delimiter
        
        # Get codec information (supplement detector info)
        codec = codecs.get(col_name)
        if codec:
            codec_type = type(codec).__name__
            col_info["encoder_type"] = codec_type
            
            # Numeric columns (ScalarCodec)
            if hasattr(codec, 'mean') and hasattr(codec, 'stdev'):
                col_info["mean"] = float(codec.mean) if codec.mean is not None else None
                col_info["std"] = float(codec.stdev) if codec.stdev is not None else None
                
                # Try to get min/max from actual data (if not already from detector)
                if 'min' not in col_info:
                    numeric_data = pd.to_numeric(col_data, errors='coerce').dropna()
                    if len(numeric_data) > 0:
                        col_info["min"] = float(numeric_data.min())
                        col_info["max"] = float(numeric_data.max())
                        col_info["median"] = float(numeric_data.median())
                        col_info["q25"] = float(numeric_data.quantile(0.25))
                        col_info["q75"] = float(numeric_data.quantile(0.75))
            
            # Categorical/Set columns
            if hasattr(codec, 'vocabulary'):
                vocab = codec.vocabulary
                if vocab:
                    col_info["vocabulary_size"] = len(vocab)
                    col_info["cardinality"] = len(vocab)
                    # Store top values for distribution analysis
                    if len(vocab) <= 100:
                        col_info["vocabulary"] = list(vocab)
                    else:
                        col_info["top_values"] = list(vocab)[:50]
            
            # String columns - get string cache info
            if hasattr(codec, 'string_cache') and codec.string_cache:
                cache_dict = codec.string_cache.cache_dict if hasattr(codec.string_cache, 'cache_dict') else {}
                col_info["string_cache_size"] = len(cache_dict)
                if 'vocabulary_size' not in col_info:
                    col_info["vocabulary_size"] = len(cache_dict)
            
            # Set delimiter for set columns (if not from detector)
            if 'set_delimiter' not in col_info and hasattr(codec, 'set_delimiter'):
                col_info["set_delimiter"] = codec.set_delimiter
            
            # Vector columns
            if hasattr(codec, 'vector_dim'):
                col_info["vector_dimension"] = codec.vector_dim
        
        # Value distribution for categorical columns (if not already from detector)
        if 'top_10_values' not in col_info and col_info.get("unique_count", 0) < 100 and col_info.get("unique_count", 0) > 0:
            value_counts = col_data.value_counts().head(20).to_dict()
            # Convert keys to strings for JSON serialization
            col_info["value_distribution"] = {str(k): int(v) for k, v in value_counts.items()}
        
        column_stats.append(col_info)
    
    return column_stats


def collect_es_training_data(
    embedding_space,
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    training_start_time: datetime,
    training_end_time: datetime,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    customer_id: Optional[str] = None,
    remote_hostname: Optional[str] = None,
    s3_path: Optional[str] = None,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Collect training data for Embedding Space training.
    
    Args:
        embedding_space: Trained EmbeddingSpace object
        train_df: Training dataframe
        val_df: Validation dataframe
        training_start_time: When training started
        training_end_time: When training finished
        epochs: Number of epochs trained
        batch_size: Batch size used
        learning_rate: Learning rate used
        customer_id: Optional customer ID
        remote_hostname: Optional hostname
        s3_path: Optional S3 path to saved model
        
    Returns:
        Dictionary ready to post to monitor API
    """
    # Get hostname if not provided
    if remote_hostname is None:
        try:
            remote_hostname = socket.gethostname()
        except:
            remote_hostname = "unknown"
    
    # Get customer ID from environment if not provided
    if customer_id is None:
        customer_id = os.getenv("FEATRIX_CUSTOMER_ID", "default")
    
    # Collect column statistics
    codecs = embedding_space.col_codecs if hasattr(embedding_space, 'col_codecs') else {}
    
    # Get input_data_set from embedding_space (prefer train_input_data)
    input_data_set = None
    if hasattr(embedding_space, 'train_input_data'):
        input_data_set = embedding_space.train_input_data
    elif hasattr(embedding_space, 'val_input_data'):
        input_data_set = embedding_space.val_input_data
    
    # Use combined dataframe for column stats
    combined_df = pd.concat([train_df, val_df], ignore_index=True)
    column_stats = get_column_statistics(combined_df, codecs, input_data_set)
    
    # Extract training losses from timeline
    training_loss = []
    validation_loss = []
    
    if hasattr(embedding_space, '_training_timeline') and embedding_space._training_timeline:
        for entry in embedding_space._training_timeline:
            if entry.get('train_loss') is not None:
                training_loss.append(float(entry['train_loss']))
            if entry.get('validation_loss') is not None:
                validation_loss.append(float(entry['validation_loss']))
    
    # Fallback to training_info if timeline not available
    if not training_loss and hasattr(embedding_space, 'training_info'):
        progress_info = embedding_space.training_info.get('progress_info', {})
        loss_history = progress_info.get('loss_history', [])
        for entry in loss_history:
            if isinstance(entry, dict):
                if entry.get('loss') is not None:
                    training_loss.append(float(entry['loss']))
                if entry.get('validation_loss') is not None:
                    validation_loss.append(float(entry['validation_loss']))
    
    # Get hyperparameters from training_info
    training_info = getattr(embedding_space, 'training_info', {})
    
    # Extract metadata/hyperparameters
    metadata = {
        "learning_rate": learning_rate,
        "optimizer": "adam",  # Default for ES training
        "d_model": getattr(embedding_space, 'd_model', None),
        "n_columns": len(train_df.columns),
        "n_epochs": epochs,
        "batch_size": batch_size,
        "compute_hostname": remote_hostname,  # Include hostname in metadata for tracking
    }
    
    # Add dropout info if available
    if hasattr(embedding_space, '_training_timeline') and embedding_space._training_timeline:
        first_epoch = embedding_space._training_timeline[0] if embedding_space._training_timeline else {}
        last_epoch = embedding_space._training_timeline[-1] if embedding_space._training_timeline else {}
        if 'dropout_rate' in first_epoch:
            metadata["initial_dropout"] = first_epoch.get('dropout_rate')
        if 'dropout_rate' in last_epoch:
            metadata["final_dropout"] = last_epoch.get('dropout_rate')
    
    # Calculate time taken
    time_taken = (training_end_time - training_start_time).total_seconds()
    
    # Check if GPU was used
    ran_on_gpu = False
    try:
        import torch
        ran_on_gpu = torch.cuda.is_available()
    except:
        pass
    
    # Build the training data payload
    training_data = {
        "customer_id": customer_id,
        "remote_hostname": remote_hostname,
        "training_type": "embedding_space",
        
        # Core hyperparameters
        "epochs": epochs,
        "batch_size": batch_size,
        
        # Additional hyperparameters in metadata
        "metadata": metadata,
        
        # Dataset info
        "input_rows": len(combined_df),
        "input_columns": len(train_df.columns),
        "training_size": len(train_df),
        "validation_size": len(val_df),
        
        # Column statistics
        "columns": column_stats,
        
        # Results - Loss curves
        "training_loss": training_loss,
        "validation_loss": validation_loss,
        
        # Execution details
        "time_taken": time_taken,
        "ran_on_gpu": ran_on_gpu,
        "datetime_started": training_start_time.isoformat() + "Z",
        "datetime_finished": training_end_time.isoformat() + "Z",
        
        # ES training doesn't have classification metrics - use empty metrics object
        "metrics": {},
        
        "s3_path": s3_path if s3_path else None,
    }
    
    # Add session_id if provided (optional field per API docs)
    if session_id:
        training_data["session_id"] = session_id
    
    return training_data


def collect_sp_training_data(
    single_predictor,
    embedding_space,
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    target_column: str,
    target_column_type: str,
    training_start_time: datetime,
    training_end_time: datetime,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    customer_id: Optional[str] = None,
    remote_hostname: Optional[str] = None,
    s3_path: Optional[str] = None,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Collect training data for Single Predictor training.
    
    Args:
        single_predictor: Trained FeatrixSinglePredictor object
        embedding_space: The EmbeddingSpace used
        train_df: Training dataframe
        val_df: Validation dataframe
        target_column: Name of target column
        target_column_type: Type of target ("set" or "scalar")
        training_start_time: When training started
        training_end_time: When training finished
        epochs: Number of epochs trained
        batch_size: Batch size used
        learning_rate: Learning rate used
        customer_id: Optional customer ID
        remote_hostname: Optional hostname
        s3_path: Optional S3 path to saved model
        
    Returns:
        Dictionary ready to post to monitor API
    """
    # Get hostname if not provided
    if remote_hostname is None:
        try:
            remote_hostname = socket.gethostname()
        except:
            remote_hostname = "unknown"
    
    # Get customer ID from environment if not provided
    if customer_id is None:
        customer_id = os.getenv("FEATRIX_CUSTOMER_ID", "default")
    
    # Collect column statistics (excluding target column for input columns)
    input_df = train_df.drop(columns=[target_column], errors='ignore')
    codecs = embedding_space.col_codecs if hasattr(embedding_space, 'col_codecs') else {}
    
    # Get input_data_set from embedding_space (prefer train_input_data)
    input_data_set = None
    if hasattr(embedding_space, 'train_input_data'):
        input_data_set = embedding_space.train_input_data
    elif hasattr(embedding_space, 'val_input_data'):
        input_data_set = embedding_space.val_input_data
    
    # Use combined dataframe for column stats
    combined_input_df = pd.concat([
        train_df.drop(columns=[target_column], errors='ignore'),
        val_df.drop(columns=[target_column], errors='ignore')
    ], ignore_index=True)
    
    column_stats = get_column_statistics(combined_input_df, codecs, input_data_set)
    
    # Extract training losses from timeline
    training_loss = []
    validation_loss = []
    
    if hasattr(single_predictor, '_training_timeline') and single_predictor._training_timeline:
        for entry in single_predictor._training_timeline:
            if entry.get('current_loss') is not None:
                training_loss.append(float(entry['current_loss']))
            if entry.get('validation_loss') is not None:
                validation_loss.append(float(entry['validation_loss']))
    
    # Fallback to training_info if timeline not available
    if not training_loss and hasattr(single_predictor, 'training_info') and single_predictor.training_info:
        for entry in single_predictor.training_info:
            if isinstance(entry, dict):
                if entry.get('loss') is not None:
                    training_loss.append(float(entry['loss']))
                if entry.get('validation_loss') is not None:
                    validation_loss.append(float(entry['validation_loss']))
    
    # Get final metrics
    metrics = {}
    if hasattr(single_predictor, 'training_metrics') and single_predictor.training_metrics:
        metrics = single_predictor.training_metrics
    
    # Get hyperparameters
    metadata = {
        "learning_rate": learning_rate,
        "optimizer": "adam",  # Default for SP training
        "target_column": target_column,
        "target_column_type": target_column_type,
        "d_model": getattr(embedding_space, 'd_model', None),
        "n_input_columns": len(input_df.columns),
        "n_epochs": epochs,
        "batch_size": batch_size,
        "compute_hostname": remote_hostname,  # Include hostname in metadata for tracking
    }
    
    # Add model architecture info
    if hasattr(single_predictor, 'predictor'):
        try:
            param_count = sum(p.numel() for p in single_predictor.predictor.parameters())
            metadata["parameter_count"] = param_count
        except:
            pass
    
    # Calculate time taken
    time_taken = (training_end_time - training_start_time).total_seconds()
    
    # Check if GPU was used
    ran_on_gpu = False
    try:
        import torch
        ran_on_gpu = torch.cuda.is_available()
    except:
        pass
    
    # Build the training data payload
    training_data = {
        "customer_id": customer_id,
        "remote_hostname": remote_hostname,
        "training_type": "classification" if target_column_type == "set" else "regression",
        
        # Core hyperparameters
        "epochs": epochs,
        "batch_size": batch_size,
        
        # Additional hyperparameters in metadata
        "metadata": metadata,
        
        # Dataset info
        "input_rows": len(train_df) + len(val_df),
        "input_columns": len(input_df.columns),
        "training_size": len(train_df),
        "validation_size": len(val_df),
        
        # Column statistics
        "columns": column_stats,
        
        # Results - Loss curves
        "training_loss": training_loss,
        "validation_loss": validation_loss,
        
        # Results - Metrics (nested object format)
        "metrics": {},
        
        # Execution details
        "time_taken": time_taken,
        "ran_on_gpu": ran_on_gpu,
        "datetime_started": training_start_time.isoformat() + "Z",
        "datetime_finished": training_end_time.isoformat() + "Z",
    }
    
    # Populate metrics object with available metrics
    if metrics:
        # Convert all metrics to float and add to metrics object
        for key, value in metrics.items():
            try:
                training_data["metrics"][key] = float(value)
            except (ValueError, TypeError):
                # Skip non-numeric metrics
                continue
    
    # Always include s3_path (API requires it, use null if not available)
    training_data["s3_path"] = s3_path
    
    # Add session_id if provided (optional field per API docs)
    if session_id:
        training_data["session_id"] = session_id
    
    return training_data


def post_training_progress(
    session_id: str,
    customer_id: Optional[str] = None,
    remote_hostname: Optional[str] = None,
    training_type: str = "embedding_space",
    current_epoch: int = 0,
    total_epochs: int = 0,
    current_training_loss: Optional[float] = None,
    current_validation_loss: Optional[float] = None,
    estimated_time_remaining: Optional[str] = None,
    ran_on_gpu: bool = False,
    monitor_url: str = "https://monitor.featrix.com/training/progress"
) -> bool:
    """
    Post in-progress training updates to the monitor API.
    
    Args:
        session_id: Session/job ID for this training
        customer_id: Optional customer ID
        remote_hostname: Optional hostname
        training_type: Type of training ("embedding_space" or "classification"/"regression")
        current_epoch: Current epoch number
        total_epochs: Total epochs planned
        current_training_loss: Current training loss
        current_validation_loss: Current validation loss
        estimated_time_remaining: Estimated time remaining (e.g., "10m")
        ran_on_gpu: Whether running on GPU
        monitor_url: URL of the monitor progress endpoint
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get hostname if not provided
        if remote_hostname is None:
            try:
                remote_hostname = socket.gethostname()
            except:
                remote_hostname = "unknown"
        
        # Get customer ID from environment if not provided
        if customer_id is None:
            customer_id = os.getenv("FEATRIX_CUSTOMER_ID", "default")
        
        progress_data = {
            "session_id": session_id,
            "customer_id": customer_id,
            "remote_hostname": remote_hostname,
            "training_type": training_type,
            "current_epoch": current_epoch,
            "total_epochs": total_epochs,
            "ran_on_gpu": ran_on_gpu,
        }
        
        if current_training_loss is not None:
            progress_data["current_training_loss"] = float(current_training_loss)
        if current_validation_loss is not None:
            progress_data["current_validation_loss"] = float(current_validation_loss)
        if estimated_time_remaining:
            progress_data["estimated_time_remaining"] = estimated_time_remaining
        
        response = requests.post(
            monitor_url,
            json=progress_data,
            timeout=10  # Shorter timeout for progress updates
        )
        
        response.raise_for_status()
        return True
        
    except requests.exceptions.HTTPError as e:
        # Log failed progress updates for retry
        try:
            from lib.api_event_retry import get_retry_manager, EventType
            retry_manager = get_retry_manager()
            retry_manager.log_failed_event(
                event_type=EventType.TRAINING_PROGRESS,
                url=monitor_url,
                method="POST",
                payload=progress_data,
                timeout=10,
                error=f"HTTP {e.response.status_code if hasattr(e, 'response') and e.response else 'unknown'}: {str(e)}",
                metadata={"session_id": session_id, "training_type": training_type}
            )
        except Exception as retry_err:
            logger.debug(f"Failed to log progress update for retry: {retry_err}")
        return False
    except requests.exceptions.RequestException as e:
        # Log failed progress updates for retry
        try:
            from lib.api_event_retry import get_retry_manager, EventType
            retry_manager = get_retry_manager()
            retry_manager.log_failed_event(
                event_type=EventType.TRAINING_PROGRESS,
                url=monitor_url,
                method="POST",
                payload=progress_data,
                timeout=10,
                error=str(e),
                metadata={"session_id": session_id, "training_type": training_type}
            )
        except Exception as retry_err:
            logger.debug(f"Failed to log progress update for retry: {retry_err}")
        return False
    except Exception as e:
        # Log failed progress updates for retry
        try:
            from lib.api_event_retry import get_retry_manager, EventType
            retry_manager = get_retry_manager()
            retry_manager.log_failed_event(
                event_type=EventType.TRAINING_PROGRESS,
                url=monitor_url,
                method="POST",
                payload=progress_data,
                timeout=10,
                error=str(e),
                metadata={"session_id": session_id, "training_type": training_type}
            )
        except Exception as retry_err:
            logger.debug(f"Failed to log progress update for retry: {retry_err}")
        return False


def post_training_data(training_data: Dict[str, Any], monitor_url: str = "https://monitor.featrix.com/training") -> bool:
    """
    Post training data to the monitor API.
    
    Args:
        training_data: Dictionary with training data
        monitor_url: URL of the monitor API endpoint
        
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"📊 Posting training data to {monitor_url}...")
        logger.info(f"   Training type: {training_data.get('training_type')}")
        logger.info(f"   Epochs: {training_data.get('epochs')}")
        logger.info(f"   Columns: {training_data.get('input_columns')}")
        logger.info(f"   Rows: {training_data.get('input_rows')}")
        
        # Sanitize the data to remove NaN/Inf values before JSON serialization
        # Use the existing clean_numpy_values function from featrix_queue
        sanitized_data = clean_numpy_values(training_data)
        
        response = requests.post(
            monitor_url,
            json=sanitized_data,
            timeout=30  # 30 second timeout
        )
        
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"✅ Successfully posted training data to monitor")
        logger.debug(f"   Response: {result}")
        
        return True
        
    except requests.exceptions.HTTPError as e:
        # Log the actual error response from the server
        error_detail = ""
        try:
            if hasattr(e.response, 'text'):
                error_detail = f" - {e.response.text[:500]}"
            elif hasattr(e.response, 'json'):
                error_json = e.response.json()
                error_detail = f" - {error_json}"
        except:
            pass
        
        error_msg = f"HTTP {e.response.status_code if hasattr(e, 'response') and e.response else 'unknown'}: {str(e)}{error_detail}"
        logger.warning(f"⚠️  Failed to post training data to monitor: {e}{error_detail}")
        logger.debug(f"   Full traceback: {traceback.format_exc()}")
        
        # Log for retry
        try:
            from lib.api_event_retry import get_retry_manager, EventType
            retry_manager = get_retry_manager()
            retry_manager.log_failed_event(
                event_type=EventType.TRAINING_DATA,
                url=monitor_url,
                method="POST",
                payload=sanitized_data,
                timeout=30,
                error=error_msg,
                metadata={"training_type": training_data.get('training_type')}
            )
        except Exception as retry_err:
            logger.debug(f"Failed to log training data for retry: {retry_err}")
        
        return False
    except requests.exceptions.RequestException as e:
        logger.warning(f"⚠️  Failed to post training data to monitor: {e}")
        logger.debug(f"   Full traceback: {traceback.format_exc()}")
        
        # Log for retry
        try:
            from lib.api_event_retry import get_retry_manager, EventType
            retry_manager = get_retry_manager()
            retry_manager.log_failed_event(
                event_type=EventType.TRAINING_DATA,
                url=monitor_url,
                method="POST",
                payload=sanitized_data,
                timeout=30,
                error=str(e),
                metadata={"training_type": training_data.get('training_type')}
            )
        except Exception as retry_err:
            logger.debug(f"Failed to log training data for retry: {retry_err}")
        
        return False
    except Exception as e:
        logger.warning(f"⚠️  Unexpected error posting training data: {e}")
        logger.debug(f"   Full traceback: {traceback.format_exc()}")
        
        # Log for retry
        try:
            from lib.api_event_retry import get_retry_manager, EventType
            retry_manager = get_retry_manager()
            retry_manager.log_failed_event(
                event_type=EventType.TRAINING_DATA,
                url=monitor_url,
                method="POST",
                payload=sanitized_data,
                timeout=30,
                error=str(e),
                metadata={"training_type": training_data.get('training_type')}
            )
        except Exception as retry_err:
            logger.debug(f"Failed to log training data for retry: {retry_err}")
        
        return False

