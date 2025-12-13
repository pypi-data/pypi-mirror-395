"""Modern login template with beautiful UI for Streamlit applications."""
import streamlit as st
from .session_manager import SessionManager
from .user_repository import UserRepository


class ModernAuthenticator:
    """Modern authentication handler with enhanced UI and SQLite persistence."""

    def __init__(self) -> None:
        """Initialize the ModernAuthenticator."""
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
    """Render the modern login page with enhanced UI."""
    # Custom CSS for modern look
    st.markdown(
        """
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .login-subtitle {
            color: #666;
            font-size: 1rem;
        }
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .demo-credentials {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Login header
    st.markdown(
        """
        <div class="login-header">
            <h1 class="login-title">Welcome Back! 👋</h1>
            <p class="login-subtitle">Sign in to continue to your account</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    authenticator = ModernAuthenticator()

    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("modern_login_form", clear_on_submit=False):
            st.markdown("### Sign In")

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                label_visibility="collapsed",
                key="modern_username",
            )
            st.markdown('<p style="margin-top: -10px; color: #666;">Username</p>', unsafe_allow_html=True)

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                label_visibility="collapsed",
                key="modern_password",
            )
            st.markdown('<p style="margin-top: -10px; color: #666;">Password</p>', unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                remember = st.checkbox("Remember me")
            with col_b:
                st.markdown(
                    '<p style="text-align: right; color: #667eea; cursor: pointer;">Forgot password?</p>',
                    unsafe_allow_html=True,
                )

            submit = st.form_submit_button("Sign In", use_container_width=True)

            if submit:
                if not username or not password:
                    st.error("❌ Please enter both username and password")
                elif authenticator.authenticate(username, password):
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")

        # Demo credentials
        with st.expander("🔑 Demo Credentials", expanded=False):
            st.markdown(
                """
                <div class="demo-credentials">
                    <p><strong>Admin Account:</strong></p>
                    <ul>
                        <li>Username: <code>admin</code></li>
                        <li>Password: <code>admin123</code></li>
                    </ul>
                    <p><strong>User Account:</strong></p>
                    <ul>
                        <li>Username: <code>user</code></li>
                        <li>Password: <code>user123</code></li>
                    </ul>
                    <hr style="margin: 1rem 0;">
                    <p style="font-size: 0.9rem; color: #666;">
                        <strong>⚠️ Security Notice:</strong><br>
                        Change these credentials in production!<br>
                        Only administrators can create new users via the Admin Panel.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
