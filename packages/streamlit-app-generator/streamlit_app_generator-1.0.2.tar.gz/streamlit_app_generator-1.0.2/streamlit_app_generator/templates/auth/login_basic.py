"""Basic login template for Streamlit applications."""
import streamlit as st
from typing import Optional, Dict, Any
from .session_manager import SessionManager
from .user_repository import UserRepository


class BasicAuthenticator:
    """Basic authentication handler with SQLite persistence.

    This class provides simple authentication functionality
    with database-backed user management.
    """

    def __init__(self) -> None:
        """Initialize the BasicAuthenticator."""
        self.session_manager = SessionManager()
        self.user_repository = UserRepository()

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user with username and password.

        Args:
            username: Username
            password: Password

        Returns:
            True if authentication successful, False otherwise
        """
        user_data = self.user_repository.authenticate(username, password)

        if user_data:
            self.session_manager.login(username, user_data)
            return True

        return False



def login_page() -> None:
    """Render the basic login page."""
    st.title("🔐 Login")

    authenticator = BasicAuthenticator()

    st.subheader("Sign In")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if not username or not password:
                st.error("❌ Please enter both username and password")
            elif authenticator.authenticate(username, password):
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    # Demo credentials info
    with st.expander("🔑 Demo Credentials"):
        st.info(
            """
            **Admin Account:**
            - Username: `admin`
            - Password: `admin123`

            **User Account:**
            - Username: `user`
            - Password: `user123`

            ⚠️ **Security Notice:**
            Change these default credentials in production!
            Only administrators can create new users via the Admin Panel.
            """
        )
