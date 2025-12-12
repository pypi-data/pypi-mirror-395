"""Login module - imports the appropriate login style."""
try:
    from .login_basic import login_page
except ImportError:
    # Fallback for generated apps
    import streamlit as st

    def login_page() -> None:
        """Fallback login page."""
        st.title("🔐 Login")
        st.warning("Login template not configured properly")
