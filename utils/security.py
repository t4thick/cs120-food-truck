"""
Security utilities: rate limiting, CSRF protection, etc.
"""
import time
from collections import defaultdict
from functools import wraps
from flask import request, session, abort, jsonify
from typing import Dict, Tuple
import secrets

# Rate limiting storage (in production, use Redis or similar)
_rate_limit_storage: Dict[str, Dict[str, float]] = defaultdict(dict)

def rate_limit(max_attempts: int = 5, window_seconds: int = 300, key_func=None):
    """
    Decorator for rate limiting.
    
    Args:
        max_attempts: Maximum number of attempts allowed
        window_seconds: Time window in seconds
        key_func: Function to generate rate limit key (defaults to IP address)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if key_func:
                key = key_func()
            else:
                key = request.remote_addr or 'unknown'
            
            now = time.time()
            attempts = _rate_limit_storage[key]
            
            # Clean old attempts outside the window
            attempts = {k: v for k, v in attempts.items() if now - v < window_seconds}
            _rate_limit_storage[key] = attempts
            
            # Check if limit exceeded
            if len(attempts) >= max_attempts:
                return jsonify({
                    "error": f"Too many attempts. Please try again in {window_seconds // 60} minutes."
                }), 429
            
            # Record this attempt
            attempts[str(time.time())] = now
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def generate_csrf_token() -> str:
    """Generate a CSRF token"""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

def validate_csrf_token(token: str) -> bool:
    """Validate CSRF token"""
    if 'csrf_token' not in session:
        return False
    if not token:
        return False
    return secrets.compare_digest(session['csrf_token'], token)

def csrf_protect(f):
    """Decorator to protect routes with CSRF validation"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
            if not token or not validate_csrf_token(token):
                abort(403)
        return f(*args, **kwargs)
    return decorated_function

def clear_rate_limit(key: str = None):
    """Clear rate limit for a key or all keys"""
    if key:
        _rate_limit_storage.pop(key, None)
    else:
        _rate_limit_storage.clear()

