# -*- coding: utf-8 -*-
"""
Webhook helpers for Featrix Sphere training callbacks.
"""

import json
import logging
import requests
from pathlib import Path
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


def call_s3_backup_webhook(
    webhook_url: str,
    model_id: str,
    org_id: str,
    file_name: str,
    content_type: str = "application/octet-stream",
    webhook_secret: str = None
) -> Optional[Dict[str, Any]]:
    """
    Call the s3_backup_url webhook to get an upload URL for model assets.
    
    Args:
        webhook_url: The webhook URL to call
        model_id: The model ID (e.g., "dot_model_20251118_383")
        org_id: The organization ID (used as webhook_secret if not provided)
        file_name: Name of the file to upload
        content_type: MIME type of the file
        webhook_secret: Secret for webhook authentication (defaults to org_id)
        
    Returns:
        Dict with "upload_url", "storage_path", "expires_in" if successful, None otherwise
    """
    if not webhook_url:
        logger.warning("No s3_backup_url provided, skipping webhook call")
        return None
    
    if not webhook_secret:
        webhook_secret = org_id
    
    payload = {
        "model_id": model_id,
        "org_id": org_id,
        "file_name": file_name,
        "content_type": content_type,
        "webhook_secret": webhook_secret
    }
    
    try:
        logger.info(f"📤 Calling s3_backup webhook: {webhook_url}")
        logger.debug(f"   Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 401:
            logger.error(f"❌ Webhook authentication failed (401): Invalid webhook_secret")
            return None
        
        response.raise_for_status()
        result = response.json()
        
        logger.info(f"✅ S3 backup webhook successful: {result.get('storage_path', 'unknown path')}")
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to call s3_backup webhook: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"   Response status: {e.response.status_code}")
            logger.error(f"   Response body: {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"❌ Unexpected error calling s3_backup webhook: {e}")
        return None


def upload_file_to_s3_url(file_path: Path, upload_url: str, content_type: str = "application/octet-stream") -> bool:
    """
    Upload a file to the signed S3 URL returned by the webhook.
    
    Args:
        file_path: Path to the file to upload
        upload_url: Signed URL from the webhook response
        content_type: MIME type of the file
        
    Returns:
        True if successful, False otherwise
    """
    if not file_path.exists():
        logger.error(f"❌ File not found: {file_path}")
        return False
    
    try:
        logger.info(f"📤 Uploading {file_path.name} to S3...")
        
        with open(file_path, 'rb') as f:
            response = requests.put(
                upload_url,
                data=f,
                headers={"Content-Type": content_type},
                timeout=300  # 5 minute timeout for large files
            )
        
        response.raise_for_status()
        logger.info(f"✅ Successfully uploaded {file_path.name} to S3")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to upload {file_path.name} to S3: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"   Response status: {e.response.status_code}")
            logger.error(f"   Response body: {e.response.text}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error uploading {file_path.name}: {e}")
        return False


def call_model_id_update_webhook(
    webhook_url: str,
    model_id: str,
    org_id: str,
    featrix_model_id: str,
    featrix_session_id: str,
    featrix_es_id: Optional[str],
    status: str,
    metrics: Dict[str, Any],
    webhook_secret: str = None
) -> bool:
    """
    Call the model_id_update_url webhook when training completes.
    
    Args:
        webhook_url: The webhook URL to call
        model_id: The model ID (e.g., "dot_model_20251118_383")
        org_id: The organization ID (used as webhook_secret if not provided)
        featrix_model_id: The Featrix predictor ID
        featrix_session_id: The Featrix session ID
        featrix_es_id: The Featrix embedding space ID (optional)
        status: Training status ("succeeded" or "failed")
        metrics: Training metrics dict (e.g., {"auc": 0.95, "f1": 0.92})
        webhook_secret: Secret for webhook authentication (defaults to org_id)
        
    Returns:
        True if successful, False otherwise
    """
    if not webhook_url:
        logger.warning("No model_id_update_url provided, skipping webhook call")
        return False
    
    if not webhook_secret:
        webhook_secret = org_id
    
    payload = {
        "model_id": model_id,
        "org_id": org_id,
        "webhook_secret": webhook_secret,
        "featrix_model_id": featrix_model_id,
        "featrix_session_id": featrix_session_id,
        "featrix_es_id": featrix_es_id,
        "status": status,
        "metrics": metrics
    }
    
    try:
        logger.info(f"📤 Calling model_id_update webhook: {webhook_url}")
        logger.debug(f"   Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 401:
            logger.error(f"❌ Webhook authentication failed (401): Invalid webhook_secret")
            return False
        
        if response.status_code == 403:
            logger.error(f"❌ Webhook authorization failed (403): org_id mismatch")
            return False
        
        response.raise_for_status()
        result = response.json()
        
        logger.info(f"✅ Model ID update webhook successful: {result.get('message', 'unknown')}")
        
        # Log webhook event
        try:
            from event_log import log_webhook_event
            log_webhook_event(
                session_id=featrix_session_id,
                event_name="webhook_sent",
                webhook_url=webhook_url,
                additional_info={
                    "model_id": model_id,
                    "status": status,
                    "response_message": result.get('message'),
                    "status_code": response.status_code
                }
            )
        except Exception as e:
            logger.debug(f"Failed to log webhook event: {e}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to call model_id_update webhook: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"   Response status: {e.response.status_code}")
            logger.error(f"   Response body: {e.response.text}")
        
        # Log webhook failure event
        try:
            from event_log import log_webhook_event
            log_webhook_event(
                session_id=featrix_session_id,
                event_name="webhook_failed",
                webhook_url=webhook_url,
                additional_info={
                    "model_id": model_id,
                    "status": status,
                    "error": str(e),
                    "status_code": e.response.status_code if hasattr(e, 'response') and e.response is not None else None
                }
            )
        except Exception as log_error:
            logger.debug(f"Failed to log webhook failure event: {log_error}")
        
        # Log for retry
        try:
            from lib.api_event_retry import get_retry_manager, EventType
            retry_manager = get_retry_manager()
            error_msg = f"{e.response.status_code if hasattr(e, 'response') and e.response else 'unknown'}: {str(e)}"
            retry_manager.log_failed_event(
                event_type=EventType.WEBHOOK,
                url=webhook_url,
                method="POST",
                payload=payload,
                timeout=30,
                error=error_msg,
                metadata={
                    "model_id": model_id,
                    "featrix_session_id": featrix_session_id,
                    "status": status
                }
            )
        except Exception as retry_err:
            logger.debug(f"Failed to log webhook for retry: {retry_err}")
        
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error calling model_id_update webhook: {e}")
        return False

