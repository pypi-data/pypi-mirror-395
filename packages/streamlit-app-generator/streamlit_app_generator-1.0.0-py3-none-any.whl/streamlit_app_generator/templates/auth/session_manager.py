"""Session management for Streamlit applications."""
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import hashlib


class SessionManager:
    """Manage user sessions and authentication state.

    This class handles session creation, validation, and expiration
    for authenticated users.
    """

    def __init__(self, timeout: int = 3600) -> None:
        """Initialize the SessionManager.

        Args:
            timeout: Session timeout in seconds (default: 3600 = 1 hour)
        """
        self.timeout = timeout
        self._initialize_session()

    def _initialize_session(self) -> None:
        """Initialize session state variables if they don't exist."""
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False

        if "user" not in st.session_state:
            st.session_state.user = None

        if "login_time" not in st.session_state:
            st.session_state.login_time = None

        if "user_role" not in st.session_state:
            st.session_state.user_role = "guest"

    def login(
        self, username: str, user_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log in a user and create a session.

        Args:
            username: Username of the authenticated user
            user_data: Optional additional user data
        """
        st.session_state.authenticated = True
        st.session_state.user = username
        st.session_state.login_time = datetime.now()

        if user_data:
            st.session_state.user_role = user_data.get("role", "user")
            st.session_state.user_email = user_data.get("email", "")
            st.session_state.user_data = user_data

    def logout(self) -> None:
        """Log out the current user and clear the session."""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        self._initialize_session()

    def is_authenticated(self) -> bool:
        """Check if the current user is authenticated.

        Returns:
            True if user is authenticated and session is valid, False otherwise
        """
        if not st.session_state.authenticated:
            return False

        # Check if session has expired
        if self._is_session_expired():
            self.logout()
            return False

        return True

    def _is_session_expired(self) -> bool:
        """Check if the current session has expired.

        Returns:
            True if session has expired, False otherwise
        """
        if st.session_state.login_time is None:
            return True

        elapsed = datetime.now() - st.session_state.login_time
        return elapsed.total_seconds() > self.timeout

    def get_user(self) -> Optional[str]:
        """Get the current authenticated user.

        Returns:
            Username if authenticated, None otherwise
        """
        if self.is_authenticated():
            return st.session_state.user
        return None

    def get_user_role(self) -> str:
        """Get the role of the current user.

        Returns:
            User role (admin, user, guest)
        """
        if self.is_authenticated():
            return st.session_state.get("user_role", "guest")
        return "guest"

    def has_role(self, required_role: str) -> bool:
        """Check if the current user has the required role.

        Args:
            required_role: Required role to check

        Returns:
            True if user has the required role, False otherwise
        """
        if not self.is_authenticated():
            return False

        role_hierarchy = {"admin": 3, "user": 2, "guest": 1}

        current_role = self.get_user_role()
        current_level = role_hierarchy.get(current_role, 0)
        required_level = role_hierarchy.get(required_role, 0)

        return current_level >= required_level

    def get_session_info(self) -> Dict[str, Any]:
        """Get information about the current session.

        Returns:
            Dictionary containing session information
        """
        if not self.is_authenticated():
            return {"authenticated": False}

        elapsed = datetime.now() - st.session_state.login_time
        remaining = max(0, self.timeout - elapsed.total_seconds())

        return {
            "authenticated": True,
            "user": st.session_state.user,
            "role": st.session_state.get("user_role", "guest"),
            "login_time": st.session_state.login_time,
            "elapsed_seconds": int(elapsed.total_seconds()),
            "remaining_seconds": int(remaining),
        }


def check_authentication() -> bool:
    """Check if the current user is authenticated.

    This is a convenience function that creates a SessionManager
    and checks authentication status.

    Returns:
        True if authenticated, False otherwise
    """
    session_manager = SessionManager()
    return session_manager.is_authenticated()


def require_authentication() -> None:
    """Require authentication for the current page.

    If user is not authenticated, stop execution and show a warning.
    """
    if not check_authentication():
        st.warning("🔒 Please login to access this page.")
        st.stop()


def require_role(required_role: str) -> None:
    """Require a specific role for the current page.

    Args:
        required_role: Required role (admin, user, guest)
    """
    session_manager = SessionManager()

    if not session_manager.is_authenticated():
        st.warning("🔒 Please login to access this page.")
        st.stop()

    if not session_manager.has_role(required_role):
        st.error(f"❌ Access denied. Required role: {required_role}")
        st.stop()
