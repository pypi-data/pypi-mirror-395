"""Application configuration management."""
from typing import Any, Dict, Optional
import streamlit as st


class AppConfig:
    """Application configuration manager.

    Reads configuration from Streamlit secrets and provides
    easy access to configuration values.
    """

    def __init__(self) -> None:
        """Initialize the configuration manager."""
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from Streamlit secrets."""
        try:
            if hasattr(st, "secrets"):
                # Load database config
                if "database" in st.secrets:
                    self._config["database"] = dict(st.secrets["database"])

                # Load auth config
                if "auth" in st.secrets:
                    self._config["auth"] = dict(st.secrets["auth"])

                # Load app config
                if "app" in st.secrets:
                    self._config["app"] = dict(st.secrets["app"])
        except Exception as e:
            st.warning(f"Could not load configuration: {e}")

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            section: Configuration section (database, auth, app)
            key: Configuration key
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        return self._config.get(section, {}).get(key, default)

    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration.

        Returns:
            Database configuration dictionary
        """
        return self._config.get("database", {})

    def get_auth_config(self) -> Dict[str, Any]:
        """Get authentication configuration.

        Returns:
            Authentication configuration dictionary
        """
        return self._config.get("auth", {})

    def get_app_config(self) -> Dict[str, Any]:
        """Get application configuration.

        Returns:
            Application configuration dictionary
        """
        return self._config.get("app", {})
