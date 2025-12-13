"""Input validation utilities."""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """Validate an email address.

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_username(username: str, min_length: int = 3, max_length: int = 20) -> tuple[bool, Optional[str]]:
    """Validate a username.

    Args:
        username: Username to validate
        min_length: Minimum length
        max_length: Maximum length

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username:
        return False, "Username cannot be empty"

    if len(username) < min_length:
        return False, f"Username must be at least {min_length} characters"

    if len(username) > max_length:
        return False, f"Username must be at most {max_length} characters"

    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores"

    return True, None


def validate_password(
    password: str, min_length: int = 8, require_uppercase: bool = True, require_number: bool = True
) -> tuple[bool, Optional[str]]:
    """Validate a password.

    Args:
        password: Password to validate
        min_length: Minimum length
        require_uppercase: Require at least one uppercase letter
        require_number: Require at least one number

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password cannot be empty"

    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"

    if require_uppercase and not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if require_number and not re.search(r"\d", password):
        return False, "Password must contain at least one number"

    return True, None


def sanitize_input(text: str, max_length: int = 255) -> str:
    """Sanitize user input by removing potentially dangerous characters.

    Args:
        text: Text to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Remove control characters and trim
    sanitized = "".join(char for char in text if ord(char) >= 32)
    sanitized = sanitized.strip()

    # Truncate to max length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized


def validate_database_name(name: str) -> tuple[bool, Optional[str]]:
    """Validate a database name.

    Args:
        name: Database name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Database name cannot be empty"

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", name):
        return False, "Database name must start with a letter and contain only letters, numbers, and underscores"

    if len(name) > 63:
        return False, "Database name must be at most 63 characters"

    return True, None
