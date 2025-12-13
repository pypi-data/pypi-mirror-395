"""PostgreSQL database connector."""
from typing import Any, Dict, List, Optional
import streamlit as st

try:
    import psycopg2
    from psycopg2 import pool
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

from .base_connector import BaseConnector


class PostgreSQLConnector(BaseConnector):
    """PostgreSQL database connector with connection pooling."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize PostgreSQL connector.

        Args:
            config: Database configuration
        """
        if not PSYCOPG2_AVAILABLE:
            raise ImportError(
                "psycopg2 is not installed. Install it with: pip install psycopg2-binary"
            )

        if config is None:
            # Load from Streamlit secrets
            try:
                config = dict(st.secrets.get("database", {}))
            except Exception:
                raise ValueError("Database configuration not found")

        super().__init__(config)
        self.pool = None

    def connect(self) -> None:
        """Establish a connection pool to PostgreSQL."""
        try:
            self.pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=self.config.get("host", "localhost"),
                port=self.config.get("port", 5432),
                database=self.config.get("database"),
                user=self.config.get("username"),
                password=self.config.get("password"),
            )
            self.logger.info("Connected to PostgreSQL database")
        except psycopg2.Error as e:
            self.logger.error(f"Error connecting to PostgreSQL: {e}")
            raise

    def disconnect(self) -> None:
        """Close all connections in the pool."""
        if self.pool:
            self.pool.closeall()
            self.pool = None
            self.logger.info("Disconnected from PostgreSQL database")

    def _get_connection(self) -> Any:
        """Get a connection from the pool."""
        if not self.pool:
            self.connect()
        return self.pool.getconn()

    def _put_connection(self, connection: Any) -> None:
        """Return a connection to the pool."""
        if self.pool:
            self.pool.putconn(connection)

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
        connection = self._get_connection()

        try:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                results = [dict(row) for row in cursor.fetchall()]
                return results

        except psycopg2.Error as e:
            self.logger.error(f"Error executing query: {e}")
            raise

        finally:
            self._put_connection(connection)

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an UPDATE/INSERT/DELETE query.

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            Number of affected rows
        """
        connection = self._get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                return cursor.rowcount

        except psycopg2.Error as e:
            connection.rollback()
            self.logger.error(f"Error executing update: {e}")
            raise

        finally:
            self._put_connection(connection)

    def is_connected(self) -> bool:
        """Check if the database connection pool is active.

        Returns:
            True if connected, False otherwise
        """
        if not self.pool:
            return False

        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self._put_connection(connection)
            return True
        except Exception:
            return False


@st.cache_resource
def get_postgresql_connection() -> PostgreSQLConnector:
    """Get a cached PostgreSQL connection.

    Returns:
        PostgreSQLConnector instance
    """
    connector = PostgreSQLConnector()
    connector.connect()
    return connector
