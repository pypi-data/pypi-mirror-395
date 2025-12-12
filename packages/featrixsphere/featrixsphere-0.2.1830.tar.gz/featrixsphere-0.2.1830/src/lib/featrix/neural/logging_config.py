import logging
import os
import sys
import socket
import warnings
from datetime import datetime
from contextvars import ContextVar

# Get hostname once at module load
HOSTNAME = socket.gethostname()

# Flag to ensure logging is only configured once
_logging_configured = False

# Context variable to track current epoch across all threads/coroutines
current_epoch_ctx: ContextVar[int] = ContextVar('current_epoch', default=None)


class EpochFormatter(logging.Formatter):
    """Custom formatter that ensures epoch_str exists before formatting."""
    def format(self, record):
        # Always ensure epoch_str exists before formatting
        if not hasattr(record, 'epoch_str'):
            epoch = current_epoch_ctx.get(None)
            if epoch is not None:
                record.epoch_str = f"[E{epoch}] "
            else:
                record.epoch_str = ""
        return super().format(record)


class EpochFilter(logging.Filter):
    """Add current epoch to log records."""
    def filter(self, record):
        # Always ensure epoch_str exists (even if not set by context)
        if not hasattr(record, 'epoch_str'):
            epoch = current_epoch_ctx.get(None)
            if epoch is not None:
                record.epoch_str = f"[E{epoch}] "
            else:
                record.epoch_str = ""
        return True

def configure_logging():
    """
    Configure logging with timestamps and hostname for all Featrix modules.
    This should be called early in the process before any other modules
    that might call logging.basicConfig().
    """
    global _logging_configured
    
    if _logging_configured:
        return
    
    # Get root logger once
    root_logger = logging.getLogger()
    
    # Force reconfiguration by clearing existing handlers
    root_logger.handlers = []
    
    # Set up comprehensive logging configuration with timestamps, hostname, thread ID, and PID
    # Format: timestamp [HOSTNAME] [LEVEL] [PID] [THREAD] [EPOCH] message
    # Removed %(name)-45s to save space (was taking 45 chars per line!)
    # %(levelname)-8s provides fixed-width severity (padded to 8 chars, left-aligned)
    # %(process)d shows the process ID to distinguish main vs workers
    # %(epoch_str)s will be populated by EpochFilter/EpochFormatter with [E5] or empty string
    log_format = f'%(asctime)s [{HOSTNAME}] [%(levelname)-8s] [PID:%(process)d] [%(threadName)s] %(epoch_str)s%(message)s'
    formatter = EpochFormatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
    
    # Create handler with our custom formatter (formatter ensures epoch_str exists)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    
    # Add epoch filter to root logger as backup (formatter already handles it, but filter is extra safety)
    epoch_filter = EpochFilter()
    root_logger.addFilter(epoch_filter)
    
    # Also add filter to all existing handlers to ensure it's applied
    for handler in root_logger.handlers:
        if epoch_filter not in handler.filters:
            handler.addFilter(epoch_filter)
    
    # Also add to any child loggers that might have been created before this
    # This ensures all loggers get the epoch_str field
    for logger_name in logging.Logger.manager.loggerDict:
        logger_obj = logging.getLogger(logger_name)
        if epoch_filter not in logger_obj.filters:
            logger_obj.addFilter(epoch_filter)
    
    _logging_configured = True
    
    # Suppress Pydantic protected namespace warnings (we've configured all models with protected_namespaces=())
    warnings.filterwarnings('ignore', message='.*Field.*has conflict with protected namespace.*model_.*', category=UserWarning)
    
    # Log that logging was configured (but use DEBUG level to avoid spam in INFO logs)
    # Workers spawn constantly and each one imports this module, causing log spam
    # 
    # CRITICAL: The PYTORCH_DATALOADER_WORKER env var is set in worker_init_fn, which runs
    # AFTER module imports. So we can't reliably detect workers at import time.
    # 
    # SOLUTION: Use DEBUG level for the configuration message so it doesn't spam INFO logs.
    # If you need to see it, set log level to DEBUG. This prevents spam from workers
    # that are constantly being spawned/recreated.
    logger = logging.getLogger(__name__)
    is_worker = os.environ.get('PYTORCH_DATALOADER_WORKER') == '1'
    
    # Use DEBUG level to avoid spam - workers spawn constantly and cause INFO log spam
    # Only use INFO level if we're definitely NOT a worker (env var check)
    if not is_worker:
        logger.debug(f"🕐 Featrix logging configured on {HOSTNAME} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Workers: completely silent (DEBUG level) - no logging to avoid massive spam from constant respawning

# Auto-configure logging when this module is imported
configure_logging() 