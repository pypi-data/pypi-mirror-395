import os
import re
import logging
import traceback
from pathlib import Path

import resend
import resend.exceptions
from email_validator import EmailNotValidError, validate_email

from config import config
from lib.session_manager import load_session
from slack import send_slack_message

# Set up proper logging for email functionality
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def validate_and_normalize_email(email: str) -> str | None:
    """Validate and normalize email address."""
    # Basic email validation regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Strip whitespace and convert to lowercase
    normalized_email = email.strip().lower()
    
    if re.match(email_pattern, normalized_email):
        return normalized_email
    else:
        logger.warning(f"Invalid email address format: {email}")
        return None


def send_email(to_address: str, session_id: str, attach_preview: bool = True):
    """Send email notification about session completion."""
    
    logger.info(f"Attempting to send email to {to_address} for session {session_id}")
    
    validated_address = validate_and_normalize_email(to_address)
    if validated_address is None:
        logger.error(f"Address {to_address} is invalid.")
        return False

    resend_api_key = os.getenv("RESEND_API_KEY")
    if not resend_api_key:
        logger.error("No Resend API key found in environment variables.")
        return False

    resend.api_key = resend_api_key

    # Email content
    subject = f"Your Featrix Session {session_id} is Complete"
    html_content = f"""
    <html>
    <body>
        <h2>Your Featrix session is ready!</h2>
        <p>Session ID: <strong>{session_id}</strong></p>
        <p>Your data analysis is complete. You can view the results at:</p>
        <p><a href="https://sphere-api.featrix.com/info/{session_id}">View Results</a></p>
        <hr>
        <p>Thank you for using Featrix!</p>
    </body>
    </html>
    """

    params = {
        "from": "notifications@featrix.ai",
        "to": [validated_address],
        "subject": subject,
        "html": html_content,
    }

    # Attach preview if requested and available
    if attach_preview:
        preview_path = f"preview_{session_id}.png"  # Adjust path as needed
        if Path(preview_path).exists():
            logger.info(f"Attaching preview file: {preview_path}")
            # Add attachment logic here if supported by resend
        else:
            logger.warning(f"Preview file not found: {preview_path}")

    try:
        # Send the email
        response = resend.Emails.send(params)
        
        if response:
            logger.info(f"Email sent successfully to {validated_address} for session {session_id}")
            return True
        else:
            logger.error(f"Failed to send email to {validated_address}: No response from service")
            return False
            
    except Exception as e:
        logger.error(f"Failed to send email to {validated_address}: {e}")
        traceback.print_exc()
        return False
