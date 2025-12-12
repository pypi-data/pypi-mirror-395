"""
Common validation utilities for email, phone, etc.

These validators can be used in Pydantic models or standalone.
"""

import re
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_email("test@example.com")
        True
        >>> validate_email("invalid-email")
        False
    """
    if not email:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str, country_code: str = None) -> bool:
    """
    Validate phone number format.

    Args:
        phone: Phone number to validate
        country_code: Optional country code (e.g., 'CM' for Cameroon)

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_phone("+237612345678")
        True
        >>> validate_phone("612345678", "CM")
        True
    """
    if not phone:
        return False

    # Remove spaces and dashes
    phone = phone.replace(' ', '').replace('-', '')

    # Check for Cameroon format (237 or +237)
    if country_code == 'CM':
        pattern = r'^(\+?237)?[26]\d{8}$'
        return bool(re.match(pattern, phone))

    # General international format
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone))


def validate_url(url: str) -> bool:
    """
    Validate URL format.

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    if not url:
        return False

    pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    return bool(re.match(pattern, url))


def validate_uuid(uuid_string: str) -> bool:
    """
    Validate UUID format.

    Args:
        uuid_string: UUID string to validate

    Returns:
        True if valid UUID format, False otherwise
    """
    if not uuid_string:
        return False

    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(pattern, uuid_string.lower()))


def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize string input by removing extra whitespace and optionally truncating.

    Args:
        value: String to sanitize
        max_length: Optional maximum length

    Returns:
        Sanitized string

    Example:
        >>> sanitize_string("  Hello   World  ")
        'Hello World'
        >>> sanitize_string("Long text...", max_length=10)
        'Long text.'
    """
    if not value:
        return ""

    # Strip and normalize whitespace
    sanitized = ' '.join(value.split())

    # Truncate if needed
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip()

    return sanitized


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.

    Requirements:
    - At least 8 characters
    - Contains uppercase and lowercase letters
    - Contains at least one digit
    - Contains at least one special character

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> valid, error = validate_password_strength("SecureP@ss123")
        >>> print(valid)
        True
        >>> valid, error = validate_password_strength("weak")
        >>> print(error)
        'Password must be at least 8 characters'
    """
    if not password:
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"

    return True, None
