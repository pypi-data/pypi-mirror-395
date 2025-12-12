"""Tests for validation utilities."""
import pytest
from streamlit_app_generator.utils.validators import (
    validate_email,
    validate_username,
    validate_password,
    validate_database_name,
)


class TestValidators:
    """Test cases for validation functions."""

    def test_validate_email_valid(self):
        """Test email validation with valid emails."""
        assert validate_email("user@example.com") is True
        assert validate_email("test.user@domain.co.uk") is True
        assert validate_email("admin+tag@company.com") is True

    def test_validate_email_invalid(self):
        """Test email validation with invalid emails."""
        assert validate_email("invalid") is False
        assert validate_email("@example.com") is False
        assert validate_email("user@") is False
        assert validate_email("") is False

    def test_validate_username_valid(self):
        """Test username validation with valid usernames."""
        is_valid, error = validate_username("john_doe")
        assert is_valid is True
        assert error is None

        is_valid, error = validate_username("user123")
        assert is_valid is True

    def test_validate_username_invalid(self):
        """Test username validation with invalid usernames."""
        is_valid, error = validate_username("ab")  # Too short
        assert is_valid is False
        assert "at least" in error

        is_valid, error = validate_username("user-name")  # Invalid character
        assert is_valid is False
        assert "letters, numbers, and underscores" in error

    def test_validate_password_valid(self):
        """Test password validation with valid passwords."""
        is_valid, error = validate_password("Password123")
        assert is_valid is True
        assert error is None

    def test_validate_password_invalid(self):
        """Test password validation with invalid passwords."""
        is_valid, error = validate_password("short")  # Too short
        assert is_valid is False
        assert "at least" in error

        is_valid, error = validate_password("nouppercase123")  # No uppercase
        assert is_valid is False
        assert "uppercase" in error

        is_valid, error = validate_password("NoNumbers")  # No numbers
        assert is_valid is False
        assert "number" in error

    def test_validate_database_name_valid(self):
        """Test database name validation with valid names."""
        is_valid, error = validate_database_name("myapp_db")
        assert is_valid is True
        assert error is None

    def test_validate_database_name_invalid(self):
        """Test database name validation with invalid names."""
        is_valid, error = validate_database_name("123invalid")  # Starts with number
        assert is_valid is False

        is_valid, error = validate_database_name("my-database")  # Invalid character
        assert is_valid is False
