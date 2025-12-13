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
        cloud_optimized: bool = False,
    ) -> None:
        """Initialize the AppGenerator.

        Args:
            name: Name of the application
            database: Database type
            auth_style: Authentication style
            pages: List of page names
            theme: Application theme
            output_dir: Output directory
            cloud_optimized: Optimize for Streamlit Community Cloud deployment
        """
        self.name = name
        self.database = database
        self.auth_style = auth_style
        self.pages = pages or ["home", "dashboard", "settings"]
        self.theme = theme
        self.output_dir = output_dir or Path(".")
        self.app_path = self.output_dir / name
        self.cloud_optimized = cloud_optimized

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

        # Cloud optimization files
        if self.cloud_optimized:
            self._create_runtime_txt()
            self._create_packages_txt()
            self._create_deploy_md()
            self._add_cloud_warning()

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
            # Copy session_manager.py, session.py, and user_repository.py
            for filename in ["session_manager.py", "session.py", "user_repository.py"]:
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
            "overview": "📄",
            "metrics": "📄",
            "charts": "📄",
            "data": "📄",
            "users": "👥",
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

        # Always create User Management page (Admin Panel) as the last page
        self._create_user_management_page(len(self.pages) + 1)

    def _create_user_management_page(self, page_number: int) -> None:
        """Create User Management page (Admin Panel) for user CRUD operations with SQLite persistence."""
        content = '''"""
User Management page - Admin Panel for managing users.

⚠️ IMPORTANT: Only administrators can access this page.
✅ Users are persisted in SQLite database (users.db)
"""
import streamlit as st
from auth.session import check_authentication
from auth.user_repository import UserRepository


def check_admin_role() -> bool:
    """Check if current user is an admin."""
    if "user_role" not in st.session_state:
        return False
    return st.session_state.user_role == "admin"


def main() -> None:
    """Main function for User Management page."""
    # Check authentication
    if not check_authentication():
        st.warning("Please login to access this page.")
        st.stop()

    # Check admin role
    if not check_admin_role():
        st.error("🚫 Access Denied: This page is only accessible to administrators.")
        st.info("Please contact your system administrator if you need access.")
        st.stop()

    st.title("👥 User Management")
    st.markdown("**Admin Panel** - Manage user accounts and permissions")
    st.markdown("💾 **Database:** users.db (SQLite)")

    # Initialize repository
    repo = UserRepository()

    # Tabs for different operations
    tab1, tab2, tab3 = st.tabs(["📋 View Users", "➕ Create User", "✏️ Edit/Delete User"])

    with tab1:
        st.subheader("Current Users")

        users = repo.get_all_users()

        if not users:
            st.info("No users found in the system.")
        else:
            st.markdown(f"**Total users:** {len(users)}")
            st.markdown("---")

            # Display users in a table
            for user in users:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                    with col1:
                        st.markdown(f"**👤 {user['username']}**")
                    with col2:
                        role = user.get("role", "user")
                        role_emoji = "🔐" if role == "admin" else "👤"
                        st.markdown(f"{role_emoji} Role: **{role}**")
                    with col3:
                        email = user.get("email", "N/A")
                        st.text(email)
                    with col4:
                        # Show creation date
                        created = user.get("created_at", "")[:10] if user.get("created_at") else "N/A"
                        st.text(created)
                    st.markdown("---")

    with tab2:
        st.subheader("Create New User")

        with st.form("create_user_form"):
            new_username = st.text_input("Username*", help="Unique username for the new user")
            new_email = st.text_input("Email*", help="User email address")
            new_password = st.text_input("Password*", type="password", help="Minimum 8 characters")
            new_role = st.selectbox(
                "Role*",
                options=["user", "admin"],
                help="user = read-only access | admin = full access"
            )
            new_full_name = st.text_input("Full Name (optional)", help="User's full name")

            submit_create = st.form_submit_button("Create User", use_container_width=True)

            if submit_create:
                # Validation
                if not all([new_username, new_email, new_password]):
                    st.error("❌ Please fill in all required fields (*)")
                elif len(new_password) < 8:
                    st.error("❌ Password must be at least 8 characters long")
                elif repo.user_exists(new_username):
                    st.error(f"❌ Username '{new_username}' already exists")
                else:
                    # Create new user in database
                    success = repo.create_user(
                        username=new_username,
                        password=new_password,
                        email=new_email,
                        role=new_role,
                        full_name=new_full_name if new_full_name else new_username
                    )

                    if success:
                        st.success(f"✅ User '{new_username}' created successfully!")
                        st.info(f"**Login credentials:**\\nUsername: `{new_username}`\\nPassword: `{new_password}`")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to create user. Please try again.")

    with tab3:
        st.subheader("Edit or Delete User")

        users = repo.get_all_users()

        if not users:
            st.info("No users available to edit.")
        else:
            usernames = [user['username'] for user in users]
            selected_user = st.selectbox(
                "Select User",
                options=usernames,
                help="Choose a user to edit or delete"
            )

            if selected_user:
                user_data = repo.get_user(selected_user)

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### Edit User")
                    with st.form(f"edit_user_{selected_user}"):
                        edit_email = st.text_input("Email", value=user_data.get("email", ""))
                        edit_role = st.selectbox(
                            "Role",
                            options=["user", "admin"],
                            index=0 if user_data.get("role") == "user" else 1
                        )
                        edit_password = st.text_input(
                            "New Password (leave empty to keep current)",
                            type="password"
                        )
                        edit_full_name = st.text_input(
                            "Full Name",
                            value=user_data.get("full_name", "")
                        )

                        submit_edit = st.form_submit_button("💾 Save Changes")

                        if submit_edit:
                            # Prepare update data
                            update_data = {
                                "email": edit_email,
                                "role": edit_role,
                                "full_name": edit_full_name
                            }

                            if edit_password:
                                if len(edit_password) < 8:
                                    st.error("❌ Password must be at least 8 characters")
                                else:
                                    update_data["password"] = edit_password

                            # Update user in database
                            success = repo.update_user(selected_user, **update_data)

                            if success:
                                st.success(f"✅ User '{selected_user}' updated successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to update user.")

                with col2:
                    st.markdown("### Delete User")
                    st.warning(f"⚠️ You are about to delete user: **{selected_user}**")
                    st.markdown("This action cannot be undone!")

                    # Prevent deleting yourself
                    current_user = st.session_state.get("user", "")
                    if selected_user == current_user:
                        st.error("❌ You cannot delete your own account")
                    else:
                        if st.button("🗑️ Delete User", type="secondary", use_container_width=True):
                            success = repo.delete_user(selected_user)

                            if success:
                                st.success(f"✅ User '{selected_user}' deleted successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete user.")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.9rem;'>
            <p>🔒 <strong>Security Best Practices</strong></p>
            <ul style='list-style: none; padding: 0;'>
                <li>✓ Change default admin credentials immediately</li>
                <li>✓ Use strong passwords (min 8 characters)</li>
                <li>✓ Grant admin access only when necessary</li>
                <li>✓ Regularly review user accounts</li>
                <li>✓ Backup users.db file regularly</li>
            </ul>
            <p style='margin-top: 1rem;'>
                <strong>💾 Database Location:</strong> users.db (SQLite)
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
'''
        filename = f"{page_number}_👥_User_Management.py"
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

        # Copy about_section.py for donation and credits
        templates_dir = Path(__file__).parent / "templates"
        about_file = templates_dir / "about_section.py"
        if about_file.exists():
            shutil.copy(about_file, self.app_path / "utils" / "about_section.py")

    def _create_requirements(self) -> None:
        """Create requirements.txt file."""
        base_requirements = [
            "streamlit>=1.28.0",
            "python-dotenv>=1.0.2",
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
        # Determine pages list (include User Management)
        all_pages = self.pages + ["User Management (Admin)"]
        pages_str = ", ".join(all_pages)

        # Add Streamlit badge if cloud-optimized
        badge = ""
        if self.cloud_optimized:
            app_name_slug = self.name.lower().replace(" ", "-").replace("_", "-")
            badge = f"\n\n[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)\n\n> **Ready for Streamlit Community Cloud!** See [DEPLOY.md](DEPLOY.md) for deployment instructions."

        content = f'''# {self.name}{badge}

🚀 **Production-ready Streamlit application** with authentication, database integration, and admin panel.

Generated with [Streamlit App Generator](https://github.com/leandrodalcortivo/streamlit-app-generator) 💜

---

## 🎯 Features

- 🔐 **Authentication**: {self.auth_style} style with secure password hashing (bcrypt)
- 🗄️ **Database**: {self.database} integration ready
- 🎨 **Theme**: {self.theme} theme pre-configured
- 📄 **Pages**: {pages_str}
- 👥 **Admin Panel**: Full user management system (CRUD operations)
- 🔒 **Security**: Role-based access control (admin/user roles)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database (Optional)

Edit `.streamlit/secrets.toml` with your database credentials.

For SQLite (default), no configuration needed!

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🔑 Default Credentials

**⚠️ IMPORTANT: Change these credentials immediately in production!**

### Admin Account (Full Access)
```
Username: admin
Password: admin123
```

### User Account (Read-Only)
```
Username: user
Password: user123
```

**Admin capabilities:**
- ✅ Create new users
- ✅ Edit existing users (email, role, password)
- ✅ Delete users
- ✅ Full access to all pages

**User capabilities:**
- ✅ View all pages (except User Management)
- ❌ Cannot manage users
- ❌ Cannot access admin panel

---

## 📁 Project Structure

```
{self.name}/
├── .streamlit/
│   ├── config.toml           # Theme and server configuration
│   └── secrets.toml          # Database credentials (DO NOT commit!)
├── auth/
│   ├── login.py              # {self.auth_style.capitalize()} login page
│   ├── session.py            # Session state checker
│   └── session_manager.py    # Session management
├── database/
│   ├── connection.py         # Database connector
│   └── {self.database}.py    # {self.database.capitalize()} implementation
├── pages/
│   ├── 1_📄_*.py            # Your application pages
│   └── *_👥_User_Management.py  # Admin panel (admin only)
├── utils/
│   └── helpers.py            # Utility functions
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

---

## 👥 User Management

### Accessing the Admin Panel

1. Login with admin credentials
2. Navigate to "User Management" in the sidebar
3. Use the tabs to:
   - **View Users**: See all registered users and their roles
   - **Create User**: Add new users with custom credentials
   - **Edit/Delete**: Modify or remove existing users

### Creating a New User

1. Go to "User Management" → "Create User" tab
2. Fill in the form:
   - **Username**: Unique identifier (required)
   - **Email**: User email address (required)
   - **Password**: Minimum 8 characters (required)
   - **Role**: Choose `admin` or `user` (required)
   - **Full Name**: Display name (optional)
3. Click "Create User"
4. Share the credentials securely with the new user

### Security Best Practices

🔒 **Password Security:**
- Minimum 8 characters required
- Passwords are hashed using bcrypt
- Never store plain-text passwords

🔒 **Access Control:**
- Grant `admin` role only to trusted users
- Regular users have read-only access
- Admins cannot delete their own accounts

🔒 **Production Deployment:**
- Change default credentials immediately
- Use environment variables for sensitive data
- Enable HTTPS in production
- Regular security audits

---

## 🗄️ Database Configuration

### Current Database: {self.database}

Configuration file: `.streamlit/secrets.toml`

**Important Notes:**
- This file contains sensitive information
- **NEVER commit `secrets.toml` to version control**
- Use `.env.example` as a template
- In production, use environment variables or secret managers

### Database Options Available

The generator supports multiple databases:
- 📁 **SQLite**: Lightweight, zero-config (default)
- 🐘 **PostgreSQL**: Production-grade relational DB
- 🐬 **MySQL**: Popular relational database
- 🍃 **MongoDB**: NoSQL document database
- 🔴 **Redis**: In-memory data store
- 🏛️ **Oracle**: Enterprise database

### ⚠️ Important: User Authentication Database

**For SQLite users (default):**
✅ **Fully automatic!** The authentication system uses SQLite with zero configuration:
- Database file `users.db` is created automatically on first run
- Default admin and user accounts are created automatically
- All user management operations work out of the box
- No manual setup required!

**For other databases (PostgreSQL, MySQL, MongoDB, Redis, Oracle):**
⚠️ **Manual configuration required!** The authentication system currently only supports SQLite out of the box.

If you selected a different database, you have two options:

**Option 1: Use SQLite for authentication (Recommended)**
- Keep `users.db` for user authentication (works automatically)
- Use your selected database for application data
- This is the easiest approach and works perfectly for most use cases

**Option 2: Implement custom authentication repository**
1. Create your own database and tables for user authentication
2. Configure connection in `.env` or `secrets.toml`
3. Implement a custom user repository in `auth/user_repository.py` following the existing interface:
   - `create_user()`, `get_user()`, `get_all_users()`
   - `update_user()`, `delete_user()`, `authenticate()`
   - `user_exists()`, `count_users()`
4. Update `auth/login.py` and `pages/*_User_Management.py` to use your custom repository

**Example structure for custom repository:**
```python
class CustomUserRepository:
    def __init__(self):
        # Your database connection here
        pass

    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        # Your authentication logic here
        pass

    # Implement other methods...
```

**Note:** The `.env.example` file and `database/` folder are provided for your application data, not for authentication. Authentication uses SQLite by default.

---

## 🎨 Customization

### Adding New Pages

Create a new file in `pages/` directory:

```python
# pages/6_📈_Analytics.py
import streamlit as st
from auth.session import check_authentication

def main():
    # Check authentication
    if not check_authentication():
        st.warning("Please login to access this page.")
        st.stop()

    st.title("📈 Analytics")
    st.write("Your custom analytics here!")

    # Your code here...

if __name__ == "__main__":
    main()
```

### Changing Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"      # Accent color
backgroundColor = "#FFFFFF"    # Background
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

---

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets in the Streamlit Cloud dashboard
5. Deploy!

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### Other Platforms

- Heroku
- AWS (EC2, ECS, Lambda)
- Google Cloud Platform
- Azure App Service

---

## 📚 Learn More

### Streamlit Documentation
- [Official Docs](https://docs.streamlit.io)
- [API Reference](https://docs.streamlit.io/library/api-reference)
- [Gallery](https://streamlit.io/gallery)

### Generator Documentation
- [GitHub Repository](https://github.com/leandrodalcortivo/streamlit-app-generator)
- [PyPI Package](https://pypi.org/project/streamlit-app-generator/)
- [Report Issues](https://github.com/leandrodalcortivo/streamlit-app-generator/issues)

---

## 💖 Support the Project

If you find **Streamlit App Generator** useful, please consider supporting its development!

### 🇧🇷 PIX (Brazil)
```
lmdcorti@gmail.com
```

### 🌍 Cryptocurrency (International)

**Bitcoin (BTC)**
```
bc1qqkhzmz0fmlgt8m0sn2d3hf9qpz56mpsrmkz4k9
```

**Ethereum (ETH)**
```
0x4533957C8a21043ce3843bD3ACB2e09ca59541F8
```

**BNB (Binance Smart Chain)**
```
0x4533957C8a21043ce3843bD3ACB2e09ca59541F8
```

**USDT (ERC20)**
```
0x4533957C8a21043ce3843bD3ACB2e09ca59541F8
```

---

## 📄 License

MIT License - Copyright (c) 2024 Leandro Meyer Dal Cortivo

---

## ⭐ Credits

**Created by:** [Leandro Meyer Dal Cortivo](https://github.com/leandrodalcortivo)

**Generated with:** [Streamlit App Generator](https://github.com/leandrodalcortivo/streamlit-app-generator)

If you enjoy using this application, please:
- ⭐ Star the [generator repository](https://github.com/leandrodalcortivo/streamlit-app-generator)
- 📢 Share with others
- 💖 [Support the project](#-support-the-project)

---

**Happy coding!** 🎉
'''
        (self.app_path / "README.md").write_text(content, encoding="utf-8")

    def _create_runtime_txt(self) -> None:
        """Create runtime.txt for Streamlit Community Cloud.

        Specifies Python version for cloud deployment.
        """
        content = '''python-3.11
'''
        (self.app_path / "runtime.txt").write_text(content, encoding="utf-8")

    def _create_packages_txt(self) -> None:
        """Create packages.txt for system dependencies.

        Only needed for PostgreSQL and MySQL which require system libraries.
        """
        if self.database in ["postgresql", "mysql"]:
            content = '''# System dependencies for database connectivity
libpq-dev
'''
            (self.app_path / "packages.txt").write_text(content, encoding="utf-8")

    def _create_deploy_md(self) -> None:
        """Create DEPLOY.md with comprehensive deployment guide."""
        sqlite_warning = ""
        if self.database == "sqlite":
            sqlite_warning = '''

### ⚠️ CRITICAL: SQLite Limitation on Cloud

**SQLite WILL NOT work on Streamlit Community Cloud!**

The Community Cloud has **ephemeral file storage**, meaning:
- Files are temporary and reset on every deploy
- Your `users.db` will be recreated and users lost
- Authentication data won't persist between sessions

**Solutions:**
1. **Recommended:** Use a cloud database (Supabase PostgreSQL, PlanetScale MySQL, MongoDB Atlas)
2. **Alternative:** Keep SQLite for local development, use cloud DB for production
3. **Quick fix:** Use `st.secrets` with hardcoded credentials (not scalable)

To migrate from SQLite:
```bash
# Option 1: Use Supabase (Free tier available)
1. Create account at https://supabase.com
2. Create new project
3. Copy database connection string
4. Update .streamlit/secrets.toml with new credentials
5. Implement PostgreSQL UserRepository (see docs)

# Option 2: Use PlanetScale MySQL
1. Create account at https://planetscale.com
2. Create database
3. Get connection URL
4. Update secrets and implement MySQL UserRepository
```
'''

        content = f'''# 🚀 Deployment Guide - Streamlit Community Cloud

Complete guide for deploying **{self.name}** to Streamlit Community Cloud.

---

## 📋 Table of Contents

1. [Prerequisites](#-prerequisites)
2. [Pre-Deployment Checklist](#-pre-deployment-checklist)
3. [Cloud Limitations](#-cloud-limitations)
4. [Step-by-Step Deployment](#-step-by-step-deployment)
5. [Configuring Secrets](#-configuring-secrets)
6. [Troubleshooting](#-troubleshooting)
7. [Performance Optimization](#-performance-optimization)

---

## ✅ Prerequisites

Before deploying, ensure you have:

- ✅ GitHub account (public or private repository)
- ✅ Streamlit Community Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- ✅ Database hosted externally (if not using SQLite)
  - Recommended: [Supabase](https://supabase.com) (PostgreSQL)
  - Alternative: [PlanetScale](https://planetscale.com) (MySQL)
  - Alternative: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

---

## 📝 Pre-Deployment Checklist

Complete these steps before deploying:

### 1. Database Setup

**Current Database:** {self.database}
{sqlite_warning}

### 2. Repository Preparation

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit - {self.name}"

# Create GitHub repository and push
git remote add origin https://github.com/your-username/{self.name}.git
git branch -M main
git push -u origin main
```

### 3. Files Verification

Ensure these files exist:
- ✅ `requirements.txt` - Python dependencies
- ✅ `runtime.txt` - Python version (3.11)
- ✅ `.streamlit/config.toml` - App configuration
- ✅ `.streamlit/secrets.toml.example` - Secrets template
- ✅ `.gitignore` - Excludes sensitive files (secrets.toml)
{f'- ✅ `packages.txt` - System dependencies' if self.database in ["postgresql", "mysql"] else ''}

**⚠️ CRITICAL:** Never commit `.streamlit/secrets.toml` with real credentials!

---

## 🔴 Cloud Limitations

Streamlit Community Cloud has resource constraints:

| Resource | Limit | Impact |
|----------|-------|--------|
| **RAM** | ~1 GB | Use caching extensively |
| **CPU** | Limited | Optimize heavy operations |
| **Storage** | Ephemeral | Use external database |
| **Execution Time** | Timeouts after prolonged processing | Break into smaller tasks |
| **Concurrent Users** | Limited | Performance degrades with traffic |

**Optimizations applied in this app:**
- ✅ Minimal requirements.txt (only essentials)
- ✅ Connection pooling for database
- ✅ Session state management
- ✅ Appropriate file exclusions (.gitignore)

---

## 🚀 Step-by-Step Deployment

### Step 1: Access Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in with GitHub"
3. Authorize Streamlit access to your repositories

### Step 2: Deploy New App

1. Click "New app" button
2. Select your repository: `your-username/{self.name}`
3. Choose branch: `main`
4. Set main file path: `app.py`
5. Click "Advanced settings..."

### Step 3: Configure Secrets

In the "Secrets" section, paste your secrets from `.streamlit/secrets.toml.example`:

```toml
# Example secrets configuration
[database]
host = "your-database-host.com"
port = "5432"
database = "your_db_name"
user = "your_username"
password = "your_secure_password"

[auth]
cookie_name = "{self.name}_auth"
cookie_key = "your_random_secret_key_here"
cookie_expiry_days = 30
```

**🔑 Generate secure cookie_key:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

### Step 4: Launch

1. Click "Deploy!"
2. Wait 2-3 minutes for build
3. Your app will be live at: `https://your-username-{self.name}-xxxxx.streamlit.app`

---

## 🔐 Configuring Secrets

### Database Secrets

**For PostgreSQL (Supabase):**
```toml
[database]
host = "db.xxxxxxxxxxxx.supabase.co"
port = "5432"
database = "postgres"
user = "postgres"
password = "your-supabase-password"
```

**For MySQL (PlanetScale):**
```toml
[database]
host = "aws.connect.psdb.cloud"
port = "3306"
database = "your-database"
user = "your-username"
password = "pscale_pw_xxxxx"
```

**For MongoDB Atlas:**
```toml
[database]
connection_string = "mongodb+srv://user:password@cluster.mongodb.net/"
database = "your_db_name"
```

### Authentication Secrets

```toml
[auth]
cookie_name = "{self.name}_auth"
cookie_key = "YOUR_RANDOM_SECRET_KEY_MINIMUM_32_CHARS"
cookie_expiry_days = 30
```

---

## 🐛 Troubleshooting

### Error: "Module not found: X"

**Cause:** Missing dependency in requirements.txt

**Solution:**
```bash
# Add to requirements.txt
echo "missing-package>=1.0.2" >> requirements.txt
git add requirements.txt
git commit -m "Add missing dependency"
git push
```

### Error: "Database connection failed"

**Cause:** Incorrect secrets or database not accessible

**Solutions:**
1. Verify secrets in Streamlit Cloud dashboard
2. Check database is publicly accessible (whitelist Streamlit Cloud IP)
3. Test connection locally with same credentials
4. Ensure database service is running

### Error: "App crashed" or "Out of memory"

**Cause:** Exceeded 1GB RAM limit

**Solutions:**
1. Add `@st.cache_data` to expensive functions
2. Add `@st.cache_resource` to database connections
3. Reduce data loaded at once
4. Clear session state when not needed

### App is very slow

**Solutions:**
1. Enable caching for queries: `@st.cache_data(ttl=3600)`
2. Use connection pooling (already configured)
3. Lazy load large resources
4. Optimize database queries
5. Consider pagination for large datasets

### Error 403: Forbidden

**Cause:** Repository permissions

**Solution:**
1. Go to GitHub repository settings
2. Ensure it's public OR Streamlit Cloud has access
3. Re-authorize Streamlit Cloud app

---

## ⚡ Performance Optimization

### 1. Database Connection Caching

Already implemented in `database/connection.py`:
```python
@st.cache_resource
def get_engine():
    """Cached database engine (singleton)"""
    return create_engine(...)
```

### 2. Query Result Caching

Add to your queries:
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_users():
    return db.query(User).all()
```

### 3. Session State Management

Use session state efficiently:
```python
# Initialize once
if 'data' not in st.session_state:
    st.session_state.data = load_data()
```

### 4. Lazy Loading

Load resources only when needed:
```python
if st.button("Load Heavy Resource"):
    data = expensive_operation()
```

---

## 📊 Monitoring & Logs

View logs in Streamlit Cloud:
1. Go to your app dashboard
2. Click "Manage app"
3. View "Logs" tab
4. Check for errors and performance issues

---

## 🔄 Updating Your App

After making changes:
```bash
git add .
git commit -m "Update: your changes"
git push
```

Streamlit Cloud automatically redeploys on push to main branch.

---

## 🆘 Support

**Streamlit Docs:** https://docs.streamlit.io/deploy/streamlit-community-cloud

**Community Forum:** https://discuss.streamlit.io

**Generator Docs:** https://github.com/leandrodalcortivo/streamlit-app-generator

**Issues:** https://github.com/leandrodalcortivo/streamlit-app-generator/issues

---

## 📝 Post-Deployment Tasks

After successful deployment:

- [ ] Test all features in production
- [ ] Verify database connectivity
- [ ] Test authentication flow
- [ ] Check all pages load correctly
- [ ] Test user creation/management
- [ ] Monitor performance
- [ ] Set up error notifications (if needed)
- [ ] Add custom domain (optional, requires paid plan)

---

## 🎉 Success!

Your app is now live! Share it with:
- 📧 Email: Send app URL
- 💬 Social media: Tweet your achievement
- 📱 Embed: Use iframe in your website

**App URL:** `https://your-username-{self.name}-xxxxx.streamlit.app`

---

**Generated with:** [Streamlit App Generator](https://github.com/leandrodalcortivo/streamlit-app-generator)

**Happy deploying!** 🚀
'''
        (self.app_path / "DEPLOY.md").write_text(content, encoding="utf-8")

    def _add_cloud_warning(self) -> None:
        """Print cloud optimization warnings to console."""
        print("\n" + "=" * 70)
        print("☁️  CLOUD-OPTIMIZED MODE ENABLED")
        print("=" * 70)

        print("\n📄 Additional files created:")
        print("  ✅ runtime.txt - Python 3.11 specified")
        if self.database in ["postgresql", "mysql"]:
            print("  ✅ packages.txt - System dependencies included")
        print("  ✅ DEPLOY.md - Complete deployment guide")

        if self.database == "sqlite":
            print("\n⚠️  CRITICAL WARNING - SQLite on Cloud:")
            print("  🔴 SQLite WILL NOT work on Streamlit Community Cloud!")
            print("  🔴 File storage is ephemeral - users.db will reset on deploy")
            print("  🔴 You MUST use an external database (PostgreSQL/MySQL/MongoDB)")
            print("\n  📖 Read DEPLOY.md for migration instructions")
            print("  💡 Recommended: Supabase (free PostgreSQL hosting)")

        print("\n🚀 Next steps:")
        print("  1. Read DEPLOY.md for complete deployment guide")
        print("  2. Push code to GitHub")
        print("  3. Deploy at https://share.streamlit.io")
        print("  4. Configure secrets in Streamlit Cloud dashboard")

        print("\n" + "=" * 70 + "\n")
