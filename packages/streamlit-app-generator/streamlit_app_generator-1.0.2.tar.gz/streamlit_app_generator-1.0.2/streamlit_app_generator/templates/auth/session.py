"""Session utilities - compatibility wrapper for session_manager."""
from .session_manager import (
    check_authentication,
    require_authentication,
    require_role,
    SessionManager,
)

__all__ = [
    "check_authentication",
    "require_authentication",
    "require_role",
    "SessionManager",
]
