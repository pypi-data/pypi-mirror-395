"""Oracle database connector."""
from typing import Any, Dict, List, Optional
import streamlit as st

try:
    import oracledb
    ORACLEDB_AVAILABLE = True
except ImportError:
    ORACLEDB_AVAILABLE = False

from .base_connector import BaseConnector


class OracleConnector(BaseConnector):
    """Oracle database connector with connection pooling.

    Supports both Oracle Instant Client and Oracle Database.
    Uses python-oracledb (formerly cx_Oracle) for connectivity.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize Oracle connector.

        Args:
            config: Database configuration
        """
        if not ORACLEDB_AVAILABLE:
            raise ImportError(
                "oracledb is not installed. Install it with: pip install oracledb"
            )

        if config is None:
            try:
                config = dict(st.secrets.get("database", {}))
            except Exception:
                raise ValueError("Database configuration not found")

        super().__init__(config)
        self.pool = None

    def connect(self) -> None:
        """Establish a connection pool to Oracle."""
        try:
            # Get connection parameters
            host = self.config.get("host", "localhost")
            port = self.config.get("port", 1521)
            service_name = self.config.get("service_name")
            sid = self.config.get("sid")
            username = self.config.get("username")
            password = self.config.get("password")

            # Build DSN (Data Source Name)
            if service_name:
                dsn = oracledb.makedsn(host, port, service_name=service_name)
            elif sid:
                dsn = oracledb.makedsn(host, port, sid=sid)
            else:
                raise ValueError("Either 'service_name' or 'sid' must be provided")

            # Create connection pool
            self.pool = oracledb.create_pool(
                user=username,
                password=password,
                dsn=dsn,
                min=2,
                max=10,
                increment=1,
                encoding="UTF-8"
            )

            self.logger.info(f"Connected to Oracle database: {host}:{port}")

        except oracledb.Error as e:
            self.logger.error(f"Error connecting to Oracle: {e}")
            raise

    def disconnect(self) -> None:
        """Close all connections in the pool."""
        if self.pool:
            self.pool.close()
            self.pool = None
            self.logger.info("Disconnected from Oracle database")

    def _get_connection(self) -> Any:
        """Get a connection from the pool."""
        if not self.pool:
            self.connect()
        return self.pool.acquire()

    def _put_connection(self, connection: Any) -> None:
        """Return a connection to the pool."""
        if self.pool:
            self.pool.release(connection)

    def execute_query(
        self, query: str, params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results.

        Args:
            query: SQL query
            params: Query parameters (use :param_name format in query)

        Returns:
            List of dictionaries containing query results
        """
        connection = self._get_connection()

        try:
            cursor = connection.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Get column names
            columns = [desc[0] for desc in cursor.description] if cursor.description else []

            # Fetch results
            rows = cursor.fetchall()
            results = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            return results

        except oracledb.Error as e:
            self.logger.error(f"Error executing query: {e}")
            raise

        finally:
            self._put_connection(connection)

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an UPDATE/INSERT/DELETE query.

        Args:
            query: SQL query
            params: Query parameters (use :param_name format in query)

        Returns:
            Number of affected rows
        """
        connection = self._get_connection()

        try:
            cursor = connection.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            connection.commit()
            rowcount = cursor.rowcount
            cursor.close()

            return rowcount

        except oracledb.Error as e:
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
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM DUAL")
            cursor.close()
            self._put_connection(connection)
            return True
        except Exception:
            return False

    def execute_procedure(
        self, proc_name: str, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Execute a stored procedure.

        Args:
            proc_name: Name of the stored procedure
            params: Dictionary of parameter names and values

        Returns:
            Result from the procedure
        """
        connection = self._get_connection()

        try:
            cursor = connection.cursor()

            if params:
                # Call procedure with parameters
                result = cursor.callproc(proc_name, list(params.values()))
            else:
                # Call procedure without parameters
                result = cursor.callproc(proc_name)

            connection.commit()
            cursor.close()

            return result

        except oracledb.Error as e:
            connection.rollback()
            self.logger.error(f"Error executing procedure: {e}")
            raise

        finally:
            self._put_connection(connection)

    def execute_function(
        self, func_name: str, return_type: Any, params: Optional[List[Any]] = None
    ) -> Any:
        """Execute a stored function.

        Args:
            func_name: Name of the stored function
            return_type: Expected return type (e.g., str, int, oracledb.NUMBER)
            params: List of parameters

        Returns:
            Result from the function
        """
        connection = self._get_connection()

        try:
            cursor = connection.cursor()

            if params:
                result = cursor.callfunc(func_name, return_type, params)
            else:
                result = cursor.callfunc(func_name, return_type)

            cursor.close()
            return result

        except oracledb.Error as e:
            self.logger.error(f"Error executing function: {e}")
            raise

        finally:
            self._put_connection(connection)


@st.cache_resource
def get_oracle_connection() -> OracleConnector:
    """Get a cached Oracle connection.

    Returns:
        OracleConnector instance
    """
    connector = OracleConnector()
    connector.connect()
    return connector
