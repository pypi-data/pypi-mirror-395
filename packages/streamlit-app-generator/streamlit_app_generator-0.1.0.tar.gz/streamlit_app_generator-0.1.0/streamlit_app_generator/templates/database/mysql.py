"""MySQL database connector."""
from typing import Any, Dict, List, Optional
import streamlit as st

try:
    import mysql.connector
    from mysql.connector import pooling
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

from .base_connector import BaseConnector


class MySQLConnector(BaseConnector):
    """MySQL database connector with connection pooling."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize MySQL connector.

        Args:
            config: Database configuration
        """
        if not MYSQL_AVAILABLE:
            raise ImportError(
                "mysql-connector-python is not installed. Install it with: pip install mysql-connector-python"
            )

        if config is None:
            try:
                config = dict(st.secrets.get("database", {}))
            except Exception:
                raise ValueError("Database configuration not found")

        super().__init__(config)
        self.pool = None

    def connect(self) -> None:
        """Establish a connection pool to MySQL."""
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                host=self.config.get("host", "localhost"),
                port=self.config.get("port", 3306),
                database=self.config.get("database"),
                user=self.config.get("username"),
                password=self.config.get("password"),
            )
            self.logger.info("Connected to MySQL database")
        except mysql.connector.Error as e:
            self.logger.error(f"Error connecting to MySQL: {e}")
            raise

    def disconnect(self) -> None:
        """Close the connection pool."""
        self.pool = None
        self.logger.info("Disconnected from MySQL database")

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
        if not self.pool:
            self.connect()

        connection = self.pool.get_connection()

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results

        except mysql.connector.Error as e:
            self.logger.error(f"Error executing query: {e}")
            raise

        finally:
            connection.close()

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an UPDATE/INSERT/DELETE query.

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            Number of affected rows
        """
        if not self.pool:
            self.connect()

        connection = self.pool.get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            rowcount = cursor.rowcount
            cursor.close()
            return rowcount

        except mysql.connector.Error as e:
            connection.rollback()
            self.logger.error(f"Error executing update: {e}")
            raise

        finally:
            connection.close()

    def is_connected(self) -> bool:
        """Check if the database connection pool is active.

        Returns:
            True if connected, False otherwise
        """
        if not self.pool:
            return False

        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            connection.close()
            return True
        except Exception:
            return False


@st.cache_resource
def get_mysql_connection() -> MySQLConnector:
    """Get a cached MySQL connection.

    Returns:
        MySQLConnector instance
    """
    connector = MySQLConnector()
    connector.connect()
    return connector
