#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

import os
import pickle
import shutil
import tempfile
import traceback
import time
import threading
from pathlib import Path


def write_embedding_space_pickle(embedding_space, local_path: str, filename: str = "embedding_space.pickle", show_progress: bool = True):
    """
    Save an embedding space as a pickle file.
    
    This function handles cleanup of unpicklable objects (like DataLoader iterators)
    before saving. The EmbeddingSpace class has a __getstate__ method that should
    handle most cleanup, but we add extra safety here.
    
    Args:
        embedding_space: The EmbeddingSpace object to save
        local_path: Directory where to save the pickle file
        filename: Name of the pickle file (default: embedding_space.pickle)
        show_progress: If True, estimate size and show progress/ETA during pickling.
                      Set to False for hourly pickles to avoid duplicate work.
    
    Returns:
        str: Path to the saved pickle file
    """
    assert os.path.exists(local_path), f"Directory does not exist: {local_path}"
    pickle_path = os.path.join(local_path, filename)
    
    # Check disk space before attempting to save (need at least 2GB free for large pickle files)
    try:
        stat = shutil.disk_usage(local_path)
        free_gb = stat.free / (1024**3)
        if free_gb < 2.0:
            error_msg = f"Insufficient disk space to save embedding space: {free_gb:.2f}GB free (need at least 2GB). Path: {pickle_path}"
            raise OSError(28, error_msg)  # Errno 28 = No space left on device
    except OSError:
        # Re-raise OSError (including our disk space error)
        raise
    except Exception as e:
        # Log warning but continue if we can't check disk space
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"⚠️  Could not check disk space before saving pickle: {e}")
    
    # Clean up any DataLoader references that might cause pickling issues
    # The EmbeddingSpace.__getstate__ should handle this, but we add extra safety
    # by temporarily removing any DataLoader attributes
    original_attrs = {}
    attrs_to_remove = []
    
    try:
        # Find and temporarily remove DataLoader-related attributes
        for attr_name in dir(embedding_space):
            if attr_name.startswith('_'):
                continue
            try:
                attr_value = getattr(embedding_space, attr_name, None)
                if attr_value is not None:
                    # Check if it's a DataLoader or contains DataLoader iterators
                    attr_type_name = type(attr_value).__name__
                    if 'DataLoader' in attr_type_name or 'DataLoaderIter' in attr_type_name:
                        original_attrs[attr_name] = attr_value
                        attrs_to_remove.append(attr_name)
                        # Temporarily set to None
                        setattr(embedding_space, attr_name, None)
            except (AttributeError, TypeError):
                # Skip attributes we can't access
                continue
        
        # Use tempfile to ensure atomic write
        # CRITICAL: Create tempfile in the same directory/filesystem as destination
        # This ensures os.rename() works atomically (same filesystem) and avoids
        # cross-filesystem move issues that could cause disk space errors.
        # We explicitly use dir=local_path to avoid creating tempfile on root filesystem (/tmp)
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"💾 Creating tempfile in destination directory (not /tmp): {local_path}")
        
        try:
            # Create tempfile first to get the filename
            tmp_file = tempfile.NamedTemporaryFile(mode="wb", delete=False, dir=local_path)
            tmp_filename = tmp_file.name
            logger.info(f"   Tempfile created at: {tmp_filename}")
            
            # Verify tempfile is on same filesystem as destination
            tmp_stat = os.stat(tmp_filename)
            dest_stat = os.stat(local_path)
            if tmp_stat.st_dev != dest_stat.st_dev:
                tmp_file.close()
                os.unlink(tmp_filename)
                raise OSError(f"Tempfile created on different filesystem! Temp: {tmp_filename}, Dest: {local_path}")
            
            # Create a progress-tracking wrapper for pickle.dump
            start_time = time.time()
            
            class ProgressTrackingFile:
                """Wrapper to track progress during pickle dump."""
                def __init__(self, file_obj, estimated_size=0, show_progress=True):
                    self.file_obj = file_obj
                    self.bytes_written = 0
                    self.start_time = time.time()
                    self.last_log_time = self.start_time
                    self.log_interval = 5.0  # Log every 5 seconds
                    self.estimated_size = estimated_size
                    self.show_progress = show_progress
                    self.recent_rates = []  # Track recent rates for better ETA
                    self.max_rate_history = 10  # Keep last 10 rates
                
                def write(self, data):
                    """Write data and log progress periodically."""
                    written = self.file_obj.write(data)
                    self.bytes_written += written
                    
                    # Skip progress logging if show_progress is False
                    if not self.show_progress:
                        return written
                    
                    current_time = time.time()
                    if current_time - self.last_log_time >= self.log_interval:
                        elapsed = current_time - self.start_time
                        size_mb = self.bytes_written / (1024 * 1024)
                        size_gb = size_mb / 1024
                        rate_mb_per_sec = size_mb / elapsed if elapsed > 0 else 0
                        
                        # Track recent rates for better ETA
                        self.recent_rates.append(rate_mb_per_sec)
                        if len(self.recent_rates) > self.max_rate_history:
                            self.recent_rates.pop(0)
                        
                        # Calculate ETA if we have an estimate
                        eta_str = ""
                        if self.estimated_size > 0 and rate_mb_per_sec > 0:
                            remaining_bytes = max(0, self.estimated_size - self.bytes_written)
                            remaining_mb = remaining_bytes / (1024 * 1024)
                            # Use average of recent rates for better ETA
                            avg_rate = sum(self.recent_rates) / len(self.recent_rates) if self.recent_rates else rate_mb_per_sec
                            eta_seconds = remaining_mb / avg_rate if avg_rate > 0 else 0
                            
                            if eta_seconds > 0:
                                if eta_seconds < 60:
                                    eta_str = f", ~{eta_seconds:.0f}s remaining"
                                elif eta_seconds < 3600:
                                    eta_minutes = eta_seconds / 60
                                    eta_str = f", ~{eta_minutes:.1f} min remaining"
                                else:
                                    eta_hours = eta_seconds / 3600
                                    eta_str = f", ~{eta_hours:.1f} hours remaining"
                                
                                # Add percentage if we have estimate
                                percent = (self.bytes_written / self.estimated_size * 100) if self.estimated_size > 0 else 0
                                eta_str = f" ({percent:.1f}% complete{eta_str})"
                        
                        if size_gb >= 1.0:
                            logger.info(f"💾 Pickling progress: {size_gb:.2f} GB written ({rate_mb_per_sec:.1f} MB/s, {elapsed:.0f}s elapsed{eta_str})")
                        else:
                            logger.info(f"💾 Pickling progress: {size_mb:.1f} MB written ({rate_mb_per_sec:.1f} MB/s, {elapsed:.0f}s elapsed{eta_str})")
                        self.last_log_time = current_time
                    
                    return written
                
                def flush(self):
                    return self.file_obj.flush()
                
                def close(self):
                    return self.file_obj.close()
            
            # Try to estimate total size first by doing a quick test pickle to memory
            # Skip this for hourly pickles to avoid duplicate work (they already pickle the full object)
            # For very large objects (>10GB), size estimation can take 20+ minutes, so we use a timeout
            estimated_size_bytes = 0
            if show_progress:
                logger.info(f"💾 Estimating pickle size (30s timeout)...")
                import io
                
                # Use threading-based timeout to prevent spending 20+ minutes on size estimation
                estimation_result = {'size': 0, 'error': None, 'done': False}
                
                def estimate_size():
                    try:
                        # Get the state dict to estimate size
                        state = embedding_space.__getstate__()
                        # Estimate size by pickling state to memory (this might be large but gives us an estimate)
                        # For very large objects, this can take 20+ minutes, so we use a timeout
                        test_pickle = pickle.dumps(state, protocol=pickle.HIGHEST_PROTOCOL)
                        estimation_result['size'] = len(test_pickle)
                        estimation_result['done'] = True
                    except Exception as e:
                        estimation_result['error'] = str(e)
                        estimation_result['done'] = True
                
                # Run estimation in a thread with timeout
                est_thread = threading.Thread(target=estimate_size, daemon=True)
                est_thread.start()
                est_thread.join(timeout=30)  # 30 second timeout
                
                if est_thread.is_alive():
                    # Estimation is taking too long - skip it
                    logger.warning(f"⚠️  Size estimation timed out after 30s - skipping estimate (object is very large, will show progress during actual pickle)")
                    estimated_size_bytes = 0
                elif estimation_result['error']:
                    logger.warning(f"⚠️  Could not estimate pickle size: {estimation_result['error']}")
                    estimated_size_bytes = 0
                else:
                    estimated_size_bytes = estimation_result['size']
                    estimated_size_mb = estimated_size_bytes / (1024 * 1024)
                    estimated_size_gb = estimated_size_mb / 1024
                    if estimated_size_gb >= 1.0:
                        logger.info(f"📊 Estimated pickle size: ~{estimated_size_gb:.2f} GB")
                    else:
                        logger.info(f"📊 Estimated pickle size: ~{estimated_size_mb:.1f} MB")
            
            logger.info(f"💾 Starting pickle dump...")
            progress_file = ProgressTrackingFile(tmp_file, estimated_size=estimated_size_bytes, show_progress=show_progress)
            
            try:
                # The EmbeddingSpace.__getstate__ method will handle most cleanup,
                # but we've also removed DataLoader attributes as extra safety
                pickle.dump(embedding_space, progress_file)
                
                # Flush before final log
                progress_file.flush()
                
                # Final progress log
                total_time = time.time() - start_time
                total_size_mb = progress_file.bytes_written / (1024 * 1024)
                total_size_gb = total_size_mb / 1024
                avg_rate = total_size_mb / total_time if total_time > 0 else 0
                if total_size_gb >= 1.0:
                    logger.info(f"✅ Pickle dump complete: {total_size_gb:.2f} GB in {total_time:.1f}s ({avg_rate:.1f} MB/s)")
                else:
                    logger.info(f"✅ Pickle dump complete: {total_size_mb:.1f} MB in {total_time:.1f}s ({avg_rate:.1f} MB/s)")
            finally:
                # Make sure we close properly
                progress_file.close()
            
            # Use os.rename() for atomic move - safe because tempfile is on same filesystem
            logger.info(f"   Moving tempfile to final location: {pickle_path}")
            os.rename(tmp_filename, pickle_path)
            
            # CRITICAL: Fix file permissions so other processes (like train_knn) can read it
            # Set to 644 (rw-r--r--) so owner can write, everyone can read
            os.chmod(pickle_path, 0o644)
            logger.info(f"   ✅ Set pickle file permissions to 644 (world-readable)")
        except OSError as e:
            # Check if it's a disk space error
            traceback.print_exc()
            if e.errno == 28 or "No space left on device" in str(e):
                error_msg = f"Failed to save embedding space pickle: No space left on device. Path: {pickle_path}"
                raise OSError(28, error_msg) from e
            raise
        
    finally:
        # Restore original attributes
        for attr_name in attrs_to_remove:
            if attr_name in original_attrs:
                try:
                    setattr(embedding_space, attr_name, original_attrs[attr_name])
                except (AttributeError, TypeError):
                    # If we can't restore, that's okay - it was probably temporary anyway
                    pass
    
    return pickle_path

