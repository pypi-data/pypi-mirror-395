"""Main generator for creating Streamlit applications."""
import shutil
from pathlib import Path
from typing import List, Optional
import secrets
import string


class AppGenerator:
    """Generator for creating complete Streamlit applications.

    This class handles the creation of a full Streamlit application structure
    including authentication, database connections, and multi-page support.

    Attributes:
        name: Name of the application
        database: Database type (postgresql, mysql, sqlite, mongodb, redis)
        auth_style: Authentication style (basic, modern, minimal)
        pages: List of page names to create
        theme: Application theme (light, dark)
        output_dir: Directory where the app will be created
    """

    def __init__(
        self,
        name: str,
        database: str = "sqlite",
        auth_style: str = "basic",
        pages: Optional[List[str]] = None,
        theme: str = "light",
        output_dir: Optional[Path] = None,
    ) -> None:
        """Initialize the AppGenerator.

        Args:
            name: Name of the application
            database: Database type
            auth_style: Authentication style
            pages: List of page names
            theme: Application theme
            output_dir: Output directory
        """
        self.name = name
        self.database = database
        self.auth_style = auth_style
        self.pages = pages or ["home", "dashboard", "settings"]
        self.theme = theme
        self.output_dir = output_dir or Path(".")
        self.app_path = self.output_dir / name

    def generate(self) -> None:
        """Generate the complete application structure."""
        self._create_directory_structure()
        self._create_main_app()
        self._create_streamlit_config()
        self._create_secrets_template()
        self._copy_auth_templates()
        self._copy_database_templates()
        self._create_pages()
        self._create_utils()
        self._create_requirements()
        self._create_env_example()
        self._create_gitignore()
        self._create_app_readme()

    def _create_directory_structure(self) -> None:
        """Create the directory structure for the application."""
        directories = [
            self.app_path,
            self.app_path / ".streamlit",
            self.app_path / "pages",
            self.app_path / "auth",
            self.app_path / "database",
            self.app_path / "utils",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        # Create __init__.py files
        init_files = [
            self.app_path / "auth" / "__init__.py",
            self.app_path / "database" / "__init__.py",
            self.app_path / "utils" / "__init__.py",
        ]

        for init_file in init_files:
            init_file.touch()

    def _create_main_app(self) -> None:
        """Create the main app.py file."""
        content = f'''"""Main application file for {self.name}."""
import streamlit as st
from auth.login import login_page
from auth.session import check_authentication


def main() -> None:
    """Main application entry point."""
    # Check authentication first
    is_authenticated = check_authentication()

    # Configure page with sidebar state based on authentication
    st.set_page_config(
        page_title="{self.name}",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed" if not is_authenticated else "expanded",
    )

    # Hide sidebar before login
    if not is_authenticated:
        st.markdown(
            """
            <style>
                [data-testid="collapsedControl"] {{
                    display: none
                }}
                [data-testid="stSidebar"] {{
                    display: none
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
        login_page()
        return

    # Main application content
    st.title("Welcome to {self.name}! 🚀")
    st.markdown(
        """
        ### Your application is ready!

        Use the sidebar to navigate between pages.

        **Features:**
        - 🔐 Secure authentication
        - 🗄️ Database integration ({self.database})
        - 📄 Multi-page support
        - 🎨 Customizable theme
        """
    )

    # Sidebar (only visible after login)
    with st.sidebar:
        st.title("Navigation")
        st.markdown("---")

        # User info
        if "user" in st.session_state:
            st.info(f"Logged in as: **{{st.session_state.user}}**")

        if st.button("Logout", type="primary", use_container_width=True):
            st.session_state.clear()
            st.rerun()


if __name__ == "__main__":
    main()
'''
        (self.app_path / "app.py").write_text(content, encoding="utf-8")

    def _create_streamlit_config(self) -> None:
        """Create Streamlit configuration file."""
        theme_config = {
            "light": {
                "primaryColor": "#FF4B4B",
                "backgroundColor": "#FFFFFF",
                "secondaryBackgroundColor": "#F0F2F6",
                "textColor": "#262730",
            },
            "dark": {
                "primaryColor": "#FF4B4B",
                "backgroundColor": "#0E1117",
                "secondaryBackgroundColor": "#262730",
                "textColor": "#FAFAFA",
            },
        }

        selected_theme = theme_config.get(self.theme, theme_config["light"])

        content = f'''[theme]
primaryColor = "{selected_theme["primaryColor"]}"
backgroundColor = "{selected_theme["backgroundColor"]}"
secondaryBackgroundColor = "{selected_theme["secondaryBackgroundColor"]}"
textColor = "{selected_theme["textColor"]}"
font = "sans serif"

[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
'''
        (self.app_path / ".streamlit" / "config.toml").write_text(
            content, encoding="utf-8"
        )

    def _create_secrets_template(self) -> None:
        """Create secrets.toml template and example."""
        from . import templates

        # First, copy the comprehensive secrets.toml.example template
        templates_dir = Path(templates.__file__).parent
        secrets_example_template = templates_dir / "secrets.toml.example"

        if secrets_example_template.exists():
            shutil.copy(
                secrets_example_template,
                self.app_path / "secrets.toml.example"
            )

        # Then create the actual secrets.toml with the selected database
        db_configs = {
            "postgresql": '''[database]
type = "postgresql"
host = "localhost"
port = 5432
database = "myapp_db"
username = "postgres"
password = "changeme"
''',
            "mysql": '''[database]
type = "mysql"
host = "localhost"
port = 3306
database = "myapp_db"
username = "root"
password = "changeme"
''',
            "sqlite": '''[database]
type = "sqlite"
database = "app.db"
''',
            "mongodb": '''[database]
type = "mongodb"
host = "localhost"
port = 27017
database = "myapp_db"
username = "admin"
password = "changeme"
''',
            "redis": '''[database]
type = "redis"
host = "localhost"
port = 6379
password = ""
db = 0
''',
            "oracle": '''[database]
type = "oracle"
host = "localhost"
port = 1521
service_name = "XEPDB1"
# OR use sid instead of service_name:
# sid = "XE"
username = "system"
password = "changeme"
''',
        }

        secret_key = self._generate_secret_key()

        content = f'''{db_configs.get(self.database, db_configs["sqlite"])}
[auth]
secret_key = "{secret_key}"
session_timeout = 3600
allow_registration = true
password_min_length = 8

[app]
title = "{self.name}"
icon = "🚀"
layout = "wide"
theme = "{self.theme}"
'''
        (self.app_path / ".streamlit" / "secrets.toml").write_text(
            content, encoding="utf-8"
        )

    def _generate_secret_key(self, length: int = 32) -> str:
        """Generate a random secret key.

        Args:
            length: Length of the secret key

        Returns:
            Random secret key string
        """
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def _copy_auth_templates(self) -> None:
        """Copy authentication templates."""
        # Import the template content from the templates module
        from . import templates

        templates_dir = Path(templates.__file__).parent / "auth"

        if templates_dir.exists():
            # Copy session_manager.py and session.py
            for filename in ["session_manager.py", "session.py"]:
                source_file = templates_dir / filename
                if source_file.exists():
                    shutil.copy(source_file, self.app_path / "auth")

            # Copy the appropriate login template based on auth_style
            login_template_map = {
                "basic": "login_basic.py",
                "modern": "login_modern.py",
                "minimal": "login_minimal.py",
            }

            login_template = login_template_map.get(self.auth_style, "login_basic.py")
            source_login = templates_dir / login_template

            if source_login.exists():
                # Copy and rename to login.py
                shutil.copy(source_login, self.app_path / "auth" / "login.py")
            else:
                self._create_basic_auth_templates()
        else:
            # Create basic auth templates if template files don't exist
            self._create_basic_auth_templates()

    def _create_basic_auth_templates(self) -> None:
        """Create basic authentication templates as fallback."""
        login_content = '''"""Basic login page."""
import streamlit as st
import bcrypt


def login_page() -> None:
    """Render a basic login page."""
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Basic demo authentication
        if username == "admin" and password == "admin123":
            st.session_state.authenticated = True
            st.session_state.user = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")
'''
        (self.app_path / "auth" / "login.py").write_text(login_content, encoding="utf-8")

        session_content = '''"""Session management."""
import streamlit as st


def check_authentication() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get("authenticated", False)
'''
        (self.app_path / "auth" / "session.py").write_text(session_content, encoding="utf-8")

    def _copy_database_templates(self) -> None:
        """Copy database templates."""
        from . import templates

        templates_dir = Path(templates.__file__).parent / "database"

        if templates_dir.exists():
            # Always copy base_connector
            base_connector = templates_dir / "base_connector.py"
            if base_connector.exists():
                shutil.copy(base_connector, self.app_path / "database")

            # Copy the specific database connector
            db_file_map = {
                "postgresql": "postgresql.py",
                "mysql": "mysql.py",
                "sqlite": "sqlite.py",
                "mongodb": "mongodb.py",
                "redis": "redis.py",
                "oracle": "oracle.py",
            }

            db_file = db_file_map.get(self.database)
            if db_file:
                source_file = templates_dir / db_file
                if source_file.exists():
                    shutil.copy(source_file, self.app_path / "database")
                    # Also create a connection.py that imports the correct connector
                    self._create_connection_wrapper()
        else:
            self._create_basic_database_templates()

    def _create_connection_wrapper(self) -> None:
        """Create connection.py wrapper that imports the correct database connector."""
        connector_map = {
            "postgresql": "from .postgresql import get_postgresql_connection as get_connection",
            "mysql": "from .mysql import get_mysql_connection as get_connection",
            "sqlite": "from .sqlite import get_sqlite_connection as get_connection",
            "mongodb": "from .mongodb import get_mongodb_connection as get_connection",
            "redis": "from .redis import get_redis_connection as get_connection",
            "oracle": "from .oracle import get_oracle_connection as get_connection",
        }

        import_statement = connector_map.get(self.database, "")

        content = f'''"""Database connection module."""
{import_statement}

__all__ = ["get_connection"]
'''
        (self.app_path / "database" / "connection.py").write_text(content, encoding="utf-8")

    def _create_basic_database_templates(self) -> None:
        """Create basic database templates as fallback."""
        (self.app_path / "database" / "connection.py").write_text(
            '"""Database connection - configure based on your database."""\n', encoding="utf-8"
        )

    def _create_pages(self) -> None:
        """Create page files."""
        page_icons = {
            "home": "🏠",
            "dashboard": "📊",
            "settings": "⚙️",
            "analytics": "📈",
            "reports": "📄",
            "profile": "👤",
        }

        for idx, page_name in enumerate(self.pages, start=1):
            icon = page_icons.get(page_name.lower(), "📄")
            title = page_name.capitalize()

            content = f'''"""
{title} page for {self.name}.
"""
import streamlit as st
from auth.session import check_authentication


def main() -> None:
    """Main function for {title} page."""
    # Check authentication
    if not check_authentication():
        st.warning("Please login to access this page.")
        st.stop()

    st.title("{icon} {title}")
    st.write("Welcome to the {title} page!")

    # Add your content here
    st.info("This is a placeholder page. Add your custom content here.")


if __name__ == "__main__":
    main()
'''
            filename = f"{idx}_{icon}_{title}.py"
            (self.app_path / "pages" / filename).write_text(content, encoding="utf-8")

    def _create_utils(self) -> None:
        """Create utility files."""
        helpers_content = '''"""Helper utilities for the application."""
from typing import Any
import streamlit as st


def format_number(number: float, decimals: int = 2) -> str:
    """Format a number with thousand separators.

    Args:
        number: Number to format
        decimals: Number of decimal places

    Returns:
        Formatted number string
    """
    return f"{number:,.{decimals}f}"


def show_success(message: str) -> None:
    """Display a success message.

    Args:
        message: Success message to display
    """
    st.success(f"✅ {message}")


def show_error(message: str) -> None:
    """Display an error message.

    Args:
        message: Error message to display
    """
    st.error(f"❌ {message}")


def show_info(message: str) -> None:
    """Display an info message.

    Args:
        message: Info message to display
    """
    st.info(f"ℹ️ {message}")
'''
        (self.app_path / "utils" / "helpers.py").write_text(
            helpers_content, encoding="utf-8"
        )

    def _create_requirements(self) -> None:
        """Create requirements.txt file."""
        base_requirements = [
            "streamlit>=1.28.0",
            "python-dotenv>=1.0.0",
            "bcrypt>=4.0.0",
        ]

        db_requirements = {
            "postgresql": ["psycopg2-binary>=2.9.0", "sqlalchemy>=2.0.0"],
            "mysql": ["mysql-connector-python>=8.0.0", "sqlalchemy>=2.0.0"],
            "sqlite": [],
            "mongodb": ["pymongo>=4.0.0"],
            "redis": ["redis>=5.0.0"],
            "oracle": ["oracledb>=2.0.0"],
        }

        requirements = base_requirements + db_requirements.get(self.database, [])
        content = "\n".join(requirements) + "\n"

        (self.app_path / "requirements.txt").write_text(content, encoding="utf-8")

    def _create_env_example(self) -> None:
        """Create .env.example file using comprehensive template."""
        from . import templates

        templates_dir = Path(templates.__file__).parent
        env_template = templates_dir / ".env.example"

        if env_template.exists():
            # Copy the comprehensive template
            shutil.copy(env_template, self.app_path / ".env.example")
        else:
            # Fallback to basic template
            content = f'''# {self.name} Environment Variables

# Database Configuration
DB_TYPE={self.database}
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_db
DB_USER=myuser
DB_PASSWORD=changeme

# Authentication
SECRET_KEY=your-secret-key-here
SESSION_TIMEOUT=3600

# Application
APP_ENV=development
DEBUG=True
'''
            (self.app_path / ".env.example").write_text(content, encoding="utf-8")

    def _create_gitignore(self) -> None:
        """Create .gitignore file."""
        content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# Streamlit
.streamlit/secrets.toml

# Environment
.env

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log
'''
        (self.app_path / ".gitignore").write_text(content, encoding="utf-8")

    def _create_app_readme(self) -> None:
        """Create README.md for the generated app."""
        content = f'''# {self.name}

Generated with [Streamlit App Generator](https://github.com/leandrodalcortivo/streamlit-app-generator.git)

## Features

- 🔐 Authentication: {self.auth_style}
- 🗄️ Database: {self.database}
- 🎨 Theme: {self.theme}
- 📄 Pages: {", ".join(self.pages)}

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure secrets:
Edit `.streamlit/secrets.toml` with your database credentials.

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
{self.name}/
├── .streamlit/          # Streamlit configuration
│   ├── config.toml      # App configuration
│   └── secrets.toml     # Secrets and credentials
├── auth/                # Authentication module
├── database/            # Database connections
├── pages/               # Application pages
├── utils/               # Utility functions
├── app.py              # Main application
└── requirements.txt     # Python dependencies
```

## Development

### Adding a New Page

Create a new file in the `pages/` directory:
```python
# pages/4_📊_NewPage.py
import streamlit as st

st.title("New Page")
st.write("Your content here")
```

### Database Connection

Database configuration is in `.streamlit/secrets.toml`.
Connection code is in `database/connection.py`.

## License

MIT License
'''
        (self.app_path / "README.md").write_text(content, encoding="utf-8")
