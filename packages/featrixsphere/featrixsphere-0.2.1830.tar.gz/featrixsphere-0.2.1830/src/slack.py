import json
import os
import logging
import requests
import socket
import time
import hashlib
from collections import defaultdict

from config import config

# Set up proper logging for Slack functionality  
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Global throttling state
_slack_message_cache = {}  # message_hash -> (last_sent_time, count)
_slack_throttle_window = 300  # 5 minutes in seconds
_slack_max_duplicates = 3  # Max times to send duplicate message in window


def get_hostname():
    """Get the current hostname for identifying which machine is posting to Slack."""
    try:
        hostname = socket.gethostname()
        # If hostname is fully qualified, just get the short name
        if '.' in hostname:
            hostname = hostname.split('.')[0]
        return hostname
    except Exception:
        return "unknown-host"


# def run_command(command):
#     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#     stdout, stderr = process.communicate()
    
#     if process.returncode == 0:
#         return stdout.decode('utf-8')
#     else:
#         return stderr.decode('utf-8')


def get_webhook_url():
    """Get Slack webhook URL from environment variable or /etc/.hook file."""
    # First try environment variable
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if webhook_url:
        return webhook_url
    
    # Fall back to /etc/.hook file (legacy method)
    if config.slack_hook_file.is_file():
        try:
            webhook_url = config.slack_hook_file.read_text().strip()
            if webhook_url:
                return webhook_url
        except Exception as e:
            logger.warning(f"Failed to read Slack hook file {config.slack_hook_file}: {e}")
    
    # Try config.slack_hook_url as final fallback
    if config.slack_hook_url:
        return config.slack_hook_url
    
    logger.debug("No Slack webhook URL found (checked SLACK_WEBHOOK_URL env var, /etc/.hook file, and config)")
    return None


def _get_message_hash(message):
    """Generate a hash for deduplication. Normalize to ignore minor variations."""
    # Remove timestamps and session IDs for better deduplication
    import re
    normalized = message
    # Remove timestamps like "2024-11-14 09:03:45"
    normalized = re.sub(r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', '', normalized)
    # Remove specific session IDs (keep session= prefix for grouping)
    normalized = re.sub(r'session=\d{8}-\d{6}_[a-f0-9]+', 'session=SESSION_ID', normalized)
    # Remove job IDs
    normalized = re.sub(r'job_\d{8}-\d{6}_[a-f0-9]+', 'job_ID', normalized)
    # Generate hash
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()


def _should_throttle_message(message):
    """Check if message should be throttled based on recent history."""
    global _slack_message_cache
    
    message_hash = _get_message_hash(message)
    current_time = time.time()
    
    # Clean up old entries (older than throttle window)
    expired_hashes = [
        h for h, (last_time, _) in _slack_message_cache.items()
        if current_time - last_time > _slack_throttle_window
    ]
    for h in expired_hashes:
        del _slack_message_cache[h]
    
    # Check if this message was sent recently
    if message_hash in _slack_message_cache:
        last_sent_time, count = _slack_message_cache[message_hash]
        time_since_last = current_time - last_sent_time
        
        # If within throttle window and already sent max times
        if time_since_last < _slack_throttle_window:
            if count >= _slack_max_duplicates:
                logger.debug(f"Throttling Slack message (sent {count} times in last {time_since_last:.0f}s)")
                return True
            else:
                # Increment count
                _slack_message_cache[message_hash] = (current_time, count + 1)
                return False
        else:
            # Outside window, reset
            _slack_message_cache[message_hash] = (current_time, 1)
            return False
    else:
        # First time seeing this message
        _slack_message_cache[message_hash] = (current_time, 1)
        return False


def send_slack_message(message, throttle=True, skip_hostname_prefix=False):
    """
    Send a message to Slack with hostname prefix for identification.
    
    Args:
        message: Message to send
        throttle: If True, apply deduplication and rate limiting (default: True)
                 Set to False for critical messages that should always be sent
        skip_hostname_prefix: If True, don't add the [hostname] prefix (useful when
                             message already includes hostname in formatted content)
    
    Returns:
        bool: True if message was sent, False otherwise
    """
    
    # Apply throttling if enabled
    if throttle and _should_throttle_message(message):
        return False
    
    webhook_url = get_webhook_url()
    if not webhook_url:
        logger.debug("No webhook URL found, skipping Slack notification")
        return False

    # Prefix message with hostname to identify which machine is posting
    if skip_hostname_prefix:
        prefixed_message = message
    else:
        hostname = get_hostname()
        prefixed_message = f"[{hostname}] {message}"

    payload = {
        'text': prefixed_message
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            logger.debug(f"Slack message sent successfully: {prefixed_message[:100]}")
            return True
        else:
            logger.warning(f"Failed to send Slack message: HTTP {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Slack message due to network error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending Slack message: {e}")
        return False
