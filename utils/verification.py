"""
Email verification code management.
Stores and validates 4-digit verification codes.
"""
import secrets
import time
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# In-memory storage for verification codes
# In production, use Redis or a database
_verification_codes: Dict[str, dict] = {}

# Code expiration time (10 minutes)
CODE_EXPIRY_MINUTES = 10

def generate_verification_code() -> str:
    """Generate a random 4-digit verification code"""
    return f"{secrets.randbelow(10000):04d}"

def store_verification_code(email: str, code: str) -> None:
    """
    Store a verification code for an email.
    Codes expire after CODE_EXPIRY_MINUTES.
    """
    expires_at = datetime.now() + timedelta(minutes=CODE_EXPIRY_MINUTES)
    _verification_codes[email.lower()] = {
        "code": code,
        "expires_at": expires_at,
        "attempts": 0,
        "max_attempts": 5
    }
    logger.info(f"Verification code stored for {email}, expires at {expires_at}")

def verify_code(email: str, code: str) -> Tuple[bool, Optional[str]]:
    """
    Verify a code for an email.
    
    Returns:
        (is_valid: bool, error_message: Optional[str])
    """
    email = email.lower()
    
    if email not in _verification_codes:
        return False, "No verification code found. Please request a new code."
    
    code_data = _verification_codes[email]
    
    # Check if code expired
    if datetime.now() > code_data["expires_at"]:
        del _verification_codes[email]
        return False, "Verification code has expired. Please request a new code."
    
    # Check attempts
    if code_data["attempts"] >= code_data["max_attempts"]:
        del _verification_codes[email]
        return False, "Too many failed attempts. Please request a new code."
    
    # Verify code
    if code_data["code"] == code:
        # Code is valid, remove it
        del _verification_codes[email]
        return True, None
    else:
        # Increment attempts
        code_data["attempts"] += 1
        remaining = code_data["max_attempts"] - code_data["attempts"]
        if remaining > 0:
            return False, f"Invalid code. {remaining} attempt(s) remaining."
        else:
            del _verification_codes[email]
            return False, "Too many failed attempts. Please request a new code."

def get_code_info(email: str) -> Optional[dict]:
    """Get information about a stored verification code"""
    email = email.lower()
    if email not in _verification_codes:
        return None
    
    code_data = _verification_codes[email]
    if datetime.now() > code_data["expires_at"]:
        del _verification_codes[email]
        return None
    
    return {
        "expires_at": code_data["expires_at"],
        "attempts": code_data["attempts"],
        "max_attempts": code_data["max_attempts"]
    }

def clear_code(email: str) -> None:
    """Clear a verification code (e.g., after successful verification)"""
    email = email.lower()
    _verification_codes.pop(email, None)

def clear_expired_codes() -> None:
    """Clean up expired codes (call periodically)"""
    now = datetime.now()
    expired = [email for email, data in _verification_codes.items() 
               if now > data["expires_at"]]
    for email in expired:
        del _verification_codes[email]

