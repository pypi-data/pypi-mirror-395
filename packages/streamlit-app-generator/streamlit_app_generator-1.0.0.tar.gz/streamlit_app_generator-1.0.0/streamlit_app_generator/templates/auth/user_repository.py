"""User repository for SQLite database.

This module handles user CRUD operations with SQLite persistence.
For other databases (PostgreSQL, MySQL, MongoDB, etc.), users should
implement their own repository following the same interface.
"""
import sqlite3
import bcrypt
from typing import Optional, Dict, List, Any
from pathlib import Path
from datetime import datetime


class UserRepository:
    """SQLite-based user repository.

    Provides CRUD operations for user management with automatic
    database initialization and default user creation.
    """

    def __init__(self, db_path: str = "users.db"):
        """Initialize the user repository.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_database()
        self._create_default_users()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection.

        Returns:
            SQLite connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_database(self) -> None:
        """Initialize the database and create tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                full_name TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT
            )
        """)

        conn.commit()
        conn.close()

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash.

        Args:
            password: Plain text password
            hashed: Hashed password

        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def _create_default_users(self) -> None:
        """Create default admin and user accounts if they don't exist."""
        # Check if any users exist
        if self.count_users() == 0:
            # Create default admin
            self.create_user(
                username="admin",
                password="admin123",
                email="admin@example.com",
                role="admin",
                full_name="Admin User"
            )

            # Create default user
            self.create_user(
                username="user",
                password="user123",
                email="user@example.com",
                role="user",
                full_name="Regular User"
            )

    def create_user(
        self,
        username: str,
        password: str,
        email: str,
        role: str = "user",
        full_name: Optional[str] = None
    ) -> bool:
        """Create a new user.

        Args:
            username: Unique username
            password: Plain text password (will be hashed)
            email: User email
            role: User role (admin or user)
            full_name: Optional full name

        Returns:
            True if user was created, False if username already exists
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            hashed_password = self._hash_password(password)
            created_at = datetime.now().isoformat()

            cursor.execute("""
                INSERT INTO users (username, password, email, role, full_name, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, hashed_password, email, role, full_name, created_at))

            conn.commit()
            conn.close()
            return True

        except sqlite3.IntegrityError:
            # Username already exists
            return False

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get a user by username.

        Args:
            username: Username to search for

        Returns:
            User dictionary or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        conn.close()

        if row:
            return dict(row)
        return None

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users.

        Returns:
            List of user dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]

    def update_user(
        self,
        username: str,
        email: Optional[str] = None,
        role: Optional[str] = None,
        password: Optional[str] = None,
        full_name: Optional[str] = None
    ) -> bool:
        """Update a user's information.

        Args:
            username: Username of user to update
            email: New email (optional)
            role: New role (optional)
            password: New password (optional, will be hashed)
            full_name: New full name (optional)

        Returns:
            True if user was updated, False if user not found
        """
        user = self.get_user(username)
        if not user:
            return False

        conn = self._get_connection()
        cursor = conn.cursor()

        updates = []
        values = []

        if email is not None:
            updates.append("email = ?")
            values.append(email)

        if role is not None:
            updates.append("role = ?")
            values.append(role)

        if password is not None:
            updates.append("password = ?")
            values.append(self._hash_password(password))

        if full_name is not None:
            updates.append("full_name = ?")
            values.append(full_name)

        updates.append("updated_at = ?")
        values.append(datetime.now().isoformat())

        values.append(username)

        query = f"UPDATE users SET {', '.join(updates)} WHERE username = ?"
        cursor.execute(query, values)

        conn.commit()
        conn.close()

        return True

    def delete_user(self, username: str) -> bool:
        """Delete a user.

        Args:
            username: Username of user to delete

        Returns:
            True if user was deleted, False if user not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return deleted

    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user.

        Args:
            username: Username
            password: Plain text password

        Returns:
            User dictionary if authentication successful, None otherwise
        """
        user = self.get_user(username)

        if user and self._verify_password(password, user['password']):
            # Don't return the password hash
            user_data = dict(user)
            del user_data['password']
            return user_data

        return None

    def count_users(self) -> int:
        """Count total number of users.

        Returns:
            Number of users in database
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]

        conn.close()

        return count

    def user_exists(self, username: str) -> bool:
        """Check if a user exists.

        Args:
            username: Username to check

        Returns:
            True if user exists, False otherwise
        """
        return self.get_user(username) is not None
