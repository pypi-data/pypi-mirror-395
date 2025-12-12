"""Base database connector interface."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseConnector(ABC):
    """Abstract base class for database connectors.

    All database connectors should inherit from this class and
    implement the required methods.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the connector with configuration.

        Args:
            config: Database configuration dictionary
        """
        self.config = config
        self.connection = None
        self.logger = logger

    @abstractmethod
    def connect(self) -> None:
        """Establish a connection to the database."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close the database connection."""
        pass

    @abstractmethod
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results.

        Args:
            query: SQL query or command
            params: Query parameters

        Returns:
            List of dictionaries containing query results
        """
        pass

    @abstractmethod
    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an update/insert/delete query.

        Args:
            query: SQL query or command
            params: Query parameters

        Returns:
            Number of affected rows
        """
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if the database connection is active.

        Returns:
            True if connected, False otherwise
        """
        pass

    def __enter__(self) -> "BaseConnector":
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.disconnect()
