"""Basic login template for Streamlit applications."""
import streamlit as st
import bcrypt
from typing import Optional, Dict, Any
from .session_manager import SessionManager


class BasicAuthenticator:
    """Basic authentication handler with username/password.

    This class provides simple authentication functionality
    with password hashing using bcrypt.
    """

    def __init__(self) -> None:
        """Initialize the BasicAuthenticator."""
        self.session_manager = SessionManager()
        self._initialize_users()

    def _initialize_users(self) -> None:
        """Initialize default users (for demo purposes).

        In production, this should connect to a database.
        """
        if "users_db" not in st.session_state:
            # Demo users with hashed passwords
            st.session_state.users_db = {
                "admin": {
                    "password": self._hash_password("admin123"),
                    "role": "admin",
                    "email": "admin@example.com",
                },
                "user": {
                    "password": self._hash_password("user123"),
                    "role": "user",
                    "email": "user@example.com",
                },
            }

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash.

        Args:
            password: Plain text password
            hashed: Hashed password

        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user with username and password.

        Args:
            username: Username
            password: Password

        Returns:
            True if authentication successful, False otherwise
        """
        users_db = st.session_state.get("users_db", {})

        if username not in users_db:
            return False

        user_data = users_db[username]

        if self._verify_password(password, user_data["password"]):
            self.session_manager.login(username, user_data)
            return True

        return False

    def register(
        self, username: str, password: str, email: str, role: str = "user"
    ) -> bool:
        """Register a new user.

        Args:
            username: Username
            password: Password
            email: Email address
            role: User role (default: user)

        Returns:
            True if registration successful, False otherwise
        """
        users_db = st.session_state.get("users_db", {})

        if username in users_db:
            return False

        users_db[username] = {
            "password": self._hash_password(password),
            "role": role,
            "email": email,
        }

        st.session_state.users_db = users_db
        return True


def login_page() -> None:
    """Render the basic login page."""
    st.title("🔐 Login")

    authenticator = BasicAuthenticator()

    # Create tabs for login and registration
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
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
        with st.expander("Demo Credentials"):
            st.info(
                """
                **Admin Account:**
                - Username: `admin`
                - Password: `admin123`

                **User Account:**
                - Username: `user`
                - Password: `user123`
                """
            )

    with tab2:
        st.subheader("Create Account")

        with st.form("register_form"):
            new_username = st.text_input("Username", key="reg_username")
            new_email = st.text_input("Email", key="reg_email")
            new_password = st.text_input(
                "Password", type="password", key="reg_password"
            )
            confirm_password = st.text_input(
                "Confirm Password", type="password", key="reg_confirm"
            )
            register_submit = st.form_submit_button("Register")

            if register_submit:
                if not all([new_username, new_email, new_password, confirm_password]):
                    st.error("❌ Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif len(new_password) < 8:
                    st.error("❌ Password must be at least 8 characters")
                elif authenticator.register(new_username, new_password, new_email):
                    st.success("✅ Account created successfully! Please login.")
                else:
                    st.error("❌ Username already exists")
