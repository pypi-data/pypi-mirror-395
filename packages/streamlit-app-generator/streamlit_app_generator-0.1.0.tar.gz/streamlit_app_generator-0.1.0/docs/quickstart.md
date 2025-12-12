# Quick Start Guide

## Create Your First App

### Basic App

Create a simple Streamlit app with default settings:

```bash
streamlit-app-generator create my_app
```

This creates an app with:
- Basic authentication
- SQLite database
- Home, Dashboard, and Settings pages
- Light theme

### Run the App

```bash
cd my_app
pip install -r requirements.txt
streamlit run app.py
```

Default credentials:
- **Admin:** admin / admin123
- **User:** user / user123

## Interactive Mode

Let the CLI guide you through the options:

```bash
streamlit-app-generator create my_app --interactive
```

You'll be prompted for:
- Database type
- Authentication style
- Theme
- Pages to include

## Custom Configuration

Create an app with specific settings:

```bash
streamlit-app-generator create my_app \
    --database postgresql \
    --auth modern \
    --theme dark \
    --pages home,dashboard,analytics,settings
```

## Using Python API

```python
from streamlit_app_generator import AppGenerator

generator = AppGenerator(
    name="my_awesome_app",
    database="postgresql",
    auth_style="modern",
    pages=["home", "dashboard", "analytics"],
    theme="dark",
)

generator.generate()
```

## Project Structure

Your generated app will have this structure:

```
my_app/
├── .streamlit/
│   ├── config.toml       # Streamlit configuration
│   └── secrets.toml      # Database credentials and secrets
├── pages/
│   ├── 1_🏠_Home.py
│   ├── 2_📊_Dashboard.py
│   └── 3_⚙️_Settings.py
├── auth/
│   ├── login.py          # Login page
│   ├── session.py        # Session management
│   └── session_manager.py
├── database/
│   ├── connection.py     # Database connection
│   └── <database>.py     # Database-specific connector
├── utils/
│   └── helpers.py        # Helper functions
├── app.py                # Main application
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Configuration

Edit `.streamlit/secrets.toml` to configure your database:

### PostgreSQL Example

```toml
[database]
type = "postgresql"
host = "localhost"
port = 5432
database = "myapp_db"
username = "postgres"
password = "your_password"

[auth]
secret_key = "your-secret-key"
session_timeout = 3600
```

### SQLite Example (Default)

```toml
[database]
type = "sqlite"
database = "app.db"

[auth]
secret_key = "your-secret-key"
session_timeout = 3600
```

## Next Steps

1. **Customize Pages**: Edit files in `pages/` directory
2. **Add Database Logic**: Implement database operations in `database/connection.py`
3. **Modify Authentication**: Customize `auth/login.py`
4. **Add New Pages**: Create new files in `pages/` following the naming convention
5. **Style Your App**: Edit `.streamlit/config.toml` for themes and styling

## Common Tasks

### Add a New Page

Create a new file in the `pages/` directory:

```python
# pages/4_📈_Analytics.py
import streamlit as st
from auth.session import check_authentication

if not check_authentication():
    st.warning("Please login to access this page.")
    st.stop()

st.title("📈 Analytics")
st.write("Your analytics content here")
```

### Connect to Database

```python
from database.connection import get_connection

db = get_connection()

# For SQL databases
results = db.execute_query("SELECT * FROM users")

# For MongoDB
results = db.find_documents("users", {"active": True})

# For Redis
value = db.get("key")
```

## Troubleshooting

### Import Errors

Make sure you installed the required database dependencies:

```bash
pip install -r requirements.txt
```

### Authentication Not Working

Check that `secrets.toml` has the correct `secret_key` and `session_timeout` values.

### Database Connection Issues

Verify your database credentials in `.streamlit/secrets.toml` and ensure the database server is running.

## Get Help

- Check the [Configuration Guide](configuration.md)
- See the [API Reference](api_reference.md)
- Report issues on [GitHub](https://github.com/leandrodalcortivo/streamlit-app-generator/issues)

## Support the Project

If you find this tool useful, consider supporting its development:

- ⭐ Star the repository on GitHub
- 💖 Support via PIX: **lmdcorti@gmail.com**
- 📖 Read more about [supporting the project](../SUPPORT.md)
