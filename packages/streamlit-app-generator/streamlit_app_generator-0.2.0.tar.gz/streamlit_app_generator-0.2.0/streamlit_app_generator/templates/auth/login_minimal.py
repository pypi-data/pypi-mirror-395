"""Minimal login template for Streamlit applications."""
import streamlit as st
import bcrypt
from .session_manager import SessionManager


class MinimalAuthenticator:
    """Minimal authentication handler with clean design."""

    def __init__(self) -> None:
        """Initialize the MinimalAuthenticator."""
        self.session_manager = SessionManager()
        self._initialize_users()

    def _initialize_users(self) -> None:
        """Initialize default users."""
        if "users_db" not in st.session_state:
            st.session_state.users_db = {
                "admin": {
                    "password": self._hash_password("admin123"),
                    "role": "admin",
                },
                "user": {
                    "password": self._hash_password("user123"),
                    "role": "user",
                },
            }

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        users_db = st.session_state.get("users_db", {})

        if username not in users_db:
            return False

        user_data = users_db[username]

        if self._verify_password(password, user_data["password"]):
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
