"""SQLite database connector."""
import sqlite3
from typing import Any, Dict, List, Optional
import streamlit as st
from .base_connector import BaseConnector


class SQLiteConnector(BaseConnector):
    """SQLite database connector with connection pooling."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize SQLite connector.

        Args:
            config: Database configuration (optional for SQLite)
        """
        if config is None:
            # Load from Streamlit secrets if available
            try:
                config = dict(st.secrets.get("database", {}))
            except Exception:
                config = {"database": "app.db"}

        super().__init__(config)
        self.db_path = config.get("database", "app.db")

    def connect(self) -> None:
        """Establish a connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self.logger.info(f"Connected to SQLite database: {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Error connecting to SQLite: {e}")
            raise

    def disconnect(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.logger.info("Disconnected from SQLite database")

    def execute_query(
        self, query: str, params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results.

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            List of dictionaries containing query results
        """
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            columns = [description[0] for description in cursor.description] if cursor.description else []
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return results

        except sqlite3.Error as e:
            self.logger.error(f"Error executing query: {e}")
            raise

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an UPDATE/INSERT/DELETE query.

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            Number of affected rows
        """
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            self.connection.commit()
            return cursor.rowcount

        except sqlite3.Error as e:
            self.connection.rollback()
            self.logger.error(f"Error executing update: {e}")
            raise

    def is_connected(self) -> bool:
        """Check if the database connection is active.

        Returns:
            True if connected, False otherwise
        """
        if not self.connection:
            return False

        try:
            self.connection.execute("SELECT 1")
            return True
        except sqlite3.Error:
            return False

    def create_table(self, table_name: str, schema: str) -> None:
        """Create a table with the given schema.

        Args:
            table_name: Name of the table
            schema: Table schema definition
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
        self.execute_update(query)
        self.logger.info(f"Table {table_name} created successfully")


@st.cache_resource
def get_sqlite_connection() -> SQLiteConnector:
    """Get a cached SQLite connection.

    Returns:
        SQLiteConnector instance
    """
    connector = SQLiteConnector()
    connector.connect()
    return connector
