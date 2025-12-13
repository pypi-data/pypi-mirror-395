"""Helper utilities for streamlit-app-generator."""
from pathlib import Path
from typing import Any, Dict, List
import secrets
import string


def generate_secret_key(length: int = 32) -> str:
    """Generate a random secret key.

    Args:
        length: Length of the secret key

    Returns:
        Random secret key string
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def ensure_directory(path: Path) -> None:
    """Ensure a directory exists, creating it if necessary.

    Args:
        path: Path to the directory
    """
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str) -> None:
    """Write content to a file.

    Args:
        path: Path to the file
        content: Content to write
    """
    ensure_directory(path.parent)
    path.write_text(content, encoding="utf-8")


def get_database_dependencies(database: str) -> List[str]:
    """Get required dependencies for a database type.

    Args:
        database: Database type

    Returns:
        List of dependency strings
    """
    dependencies = {
        "postgresql": ["psycopg2-binary>=2.9.0", "sqlalchemy>=2.0.0"],
        "mysql": ["mysql-connector-python>=8.0.0", "sqlalchemy>=2.0.0"],
        "sqlite": [],
        "mongodb": ["pymongo>=4.0.0"],
        "redis": ["redis>=5.0.0"],
        "oracle": ["oracledb>=2.0.0"],
    }
    return dependencies.get(database, [])


def get_page_icon(page_name: str) -> str:
    """Get an appropriate icon for a page name.

    Args:
        page_name: Name of the page

    Returns:
        Emoji icon
    """
    icons = {
        "home": "🏠",
        "dashboard": "📊",
        "settings": "⚙️",
        "analytics": "📈",
        "reports": "📄",
        "profile": "👤",
        "users": "👥",
        "data": "💾",
        "charts": "📉",
        "search": "🔍",
        "notifications": "🔔",
        "messages": "💬",
        "calendar": "📅",
        "tasks": "✅",
        "files": "📁",
        "admin": "🔧",
    }
    return icons.get(page_name.lower(), "📄")


def format_class_name(name: str) -> str:
    """Format a string as a class name (PascalCase).

    Args:
        name: String to format

    Returns:
        Formatted class name
    """
    words = name.replace("_", " ").replace("-", " ").split()
    return "".join(word.capitalize() for word in words)


def format_function_name(name: str) -> str:
    """Format a string as a function name (snake_case).

    Args:
        name: String to format

    Returns:
        Formatted function name
    """
    name = name.replace(" ", "_").replace("-", "_")
    return name.lower()


def get_database_config_template(database: str) -> str:
    """Get configuration template for a database type.

    Args:
        database: Database type

    Returns:
        TOML configuration string
    """
    templates = {
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
username = "system"
password = "changeme"
''',
    }
    return templates.get(database, templates["sqlite"])
