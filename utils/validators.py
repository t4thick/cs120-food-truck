"""
Input validation utilities for forms and user input.
"""
import re
from datetime import datetime
from typing import Optional, Tuple
from decimal import Decimal, InvalidOperation

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email format.
    Returns (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "Email is required"
    
    email = email.strip().lower()
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Please provide a valid email address (e.g., user@example.com)"
    
    if len(email) > 254:  # RFC 5321 limit
        return False, "Email address is too long (maximum 254 characters)"
    
    return True, None

def validate_password(password: str, min_length: int = 6) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength.
    Returns (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters long"
    
    if len(password) > 128:
        return False, "Password is too long (maximum 128 characters)"
    
    return True, None

def validate_price(price_str: str, min_value: float = 0.01, max_value: float = 9999.99) -> Tuple[bool, Optional[float], Optional[str]]:
    """
    Validate price input.
    Returns (is_valid, price_value, error_message)
    """
    if not price_str:
        return False, None, "Price is required"
    
    try:
        price = float(price_str)
        if price < min_value:
            return False, None, f"Price must be at least ${min_value:.2f}"
        if price > max_value:
            return False, None, f"Price cannot exceed ${max_value:.2f}"
        return True, price, None
    except (ValueError, TypeError):
        return False, None, "Price must be a valid number"

def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> Tuple[bool, Optional[datetime], Optional[str]]:
    """
    Validate date format.
    Returns (is_valid, date_object, error_message)
    """
    if not date_str:
        return False, None, "Date is required"
    
    try:
        date_obj = datetime.strptime(date_str.strip(), date_format)
        return True, date_obj, None
    except ValueError:
        return False, None, f"Date must be in format {date_format} (e.g., 2025-12-30)"

def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """
    Validate phone number format (basic validation).
    Returns (is_valid, error_message)
    """
    if not phone:
        return True, None  # Phone is optional
    
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    
    # Check if it's all digits
    if not cleaned.isdigit():
        return False, "Phone number must contain only digits and formatting characters"
    
    # Check length (10-15 digits is reasonable)
    if len(cleaned) < 10 or len(cleaned) > 15:
        return False, "Phone number must be between 10 and 15 digits"
    
    return True, None

def validate_name(name: str, field_name: str = "Name") -> Tuple[bool, Optional[str]]:
    """
    Validate name fields (first name, last name, etc.).
    Returns (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, f"{field_name} is required"
    
    name = name.strip()
    
    if len(name) < 1:
        return False, f"{field_name} cannot be empty"
    
    if len(name) > 100:
        return False, f"{field_name} is too long (maximum 100 characters)"
    
    # Check for potentially malicious content
    if re.search(r'[<>"\']', name):
        return False, f"{field_name} contains invalid characters"
    
    return True, None

def validate_quantity(qty_str: str, min_value: int = 1, max_value: int = 99) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Validate quantity input.
    Returns (is_valid, quantity_value, error_message)
    """
    if not qty_str:
        return False, None, "Quantity is required"
    
    try:
        qty = int(qty_str)
        if qty < min_value:
            return False, None, f"Quantity must be at least {min_value}"
        if qty > max_value:
            return False, None, f"Quantity cannot exceed {max_value}"
        return True, qty, None
    except (ValueError, TypeError):
        return False, None, "Quantity must be a valid whole number"

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file uploads.
    Removes dangerous characters and limits length.
    """
    if not filename:
        return "file"
    
    # Remove path components and dangerous characters
    filename = os.path.basename(filename)
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext
    
    return filename

def validate_image_upload(file, max_size_mb: int = 5) -> Tuple[bool, Optional[str]]:
    """
    Validate uploaded image file.
    Returns (is_valid, error_message)
    """
    if not file or not file.filename:
        return True, None  # File upload is optional
    
    # Check file extension
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        return False, f"File size exceeds {max_size_mb}MB limit"
    
    if file_size == 0:
        return False, "File is empty"
    
    return True, None

import os

