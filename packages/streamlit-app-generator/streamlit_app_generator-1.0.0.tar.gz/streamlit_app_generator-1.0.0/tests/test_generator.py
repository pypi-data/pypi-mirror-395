"""Tests for the AppGenerator class."""
import pytest
from pathlib import Path
import tempfile
import shutil
from streamlit_app_generator import AppGenerator


class TestAppGenerator:
    """Test cases for AppGenerator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_generator_initialization(self):
        """Test AppGenerator initialization."""
        generator = AppGenerator(
            name="test_app",
            database="sqlite",
            auth_style="basic",
            output_dir=self.temp_dir,
        )

        assert generator.name == "test_app"
        assert generator.database == "sqlite"
        assert generator.auth_style == "basic"
        assert generator.output_dir == self.temp_dir

    def test_generate_basic_app(self):
        """Test generating a basic app."""
        generator = AppGenerator(
            name="test_app",
            database="sqlite",
            auth_style="basic",
            output_dir=self.temp_dir,
        )

        generator.generate()

        app_path = self.temp_dir / "test_app"

        # Check directory structure
        assert app_path.exists()
        assert (app_path / ".streamlit").exists()
        assert (app_path / "pages").exists()
        assert (app_path / "auth").exists()
        assert (app_path / "database").exists()
        assert (app_path / "utils").exists()

        # Check files exist
        assert (app_path / "app.py").exists()
        assert (app_path / ".streamlit" / "config.toml").exists()
        assert (app_path / ".streamlit" / "secrets.toml").exists()
        assert (app_path / "requirements.txt").exists()
        assert (app_path / "README.md").exists()
        assert (app_path / ".gitignore").exists()

        # Check auth files
        assert (app_path / "auth" / "login.py").exists()
        assert (app_path / "auth" / "session.py").exists()

    def test_generate_with_custom_pages(self):
        """Test generating an app with custom pages."""
        generator = AppGenerator(
            name="test_app",
            pages=["home", "analytics", "reports"],
            output_dir=self.temp_dir,
        )

        generator.generate()

        app_path = self.temp_dir / "test_app"
        pages_dir = app_path / "pages"

        # Should have 3 pages
        page_files = list(pages_dir.glob("*.py"))
        assert len(page_files) == 3

    def test_generate_with_postgresql(self):
        """Test generating an app with PostgreSQL."""
        generator = AppGenerator(
            name="test_app",
            database="postgresql",
            output_dir=self.temp_dir,
        )

        generator.generate()

        app_path = self.temp_dir / "test_app"

        # Check requirements include psycopg2
        requirements = (app_path / "requirements.txt").read_text()
        assert "psycopg2-binary" in requirements

    def test_generate_with_modern_auth(self):
        """Test generating an app with modern auth."""
        generator = AppGenerator(
            name="test_app",
            auth_style="modern",
            output_dir=self.temp_dir,
        )

        generator.generate()

        app_path = self.temp_dir / "test_app"
        login_file = app_path / "auth" / "login.py"

        # Check that login file was created
        assert login_file.exists()

        # Check content contains modern auth
        content = login_file.read_text()
        assert "ModernAuthenticator" in content or "modern" in content.lower()
