"""Minimal login template for Streamlit applications."""
import streamlit as st
from .session_manager import SessionManager
from .user_repository import UserRepository


class MinimalAuthenticator:
    """Minimal authentication handler with SQLite persistence."""

    def __init__(self) -> None:
        """Initialize the MinimalAuthenticator."""
        self.session_manager = SessionManager()
        self.user_repository = UserRepository()

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user against the database.

        Args:
            username: Username
            password: Plain text password

        Returns:
            True if authentication successful, False otherwise
        """
        user_data = self.user_repository.authenticate(username, password)

        if user_data:
            self.session_manager.login(username, user_data)
            return True

        return False


def login_page() -> None:
    """Render the minimal login page."""
    # Minimal CSS
    st.markdown(
        """
        <style>
        .minimal-login {
            max-width: 350px;
            margin: 5rem auto;
        }
        .minimal-title {
            font-size: 1.5rem;
            font-weight: 400;
            margin-bottom: 2rem;
            text-align: center;
            color: #333;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Spacer
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Center column
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        st.markdown('<h1 class="minimal-title">Sign In</h1>', unsafe_allow_html=True)

        authenticator = MinimalAuthenticator()

        username = st.text_input("Username", key="minimal_user")
        password = st.text_input("Password", type="password", key="minimal_pass")

        if st.button("Enter", use_container_width=True):
            if not username or not password:
                st.error("Fill all fields")
            elif authenticator.authenticate(username, password):
                st.success("Success")
                st.rerun()
            else:
                st.error("Invalid credentials")

        # Minimal demo info
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("Demo"):
            st.text("admin / admin123")
            st.text("user / user123")
