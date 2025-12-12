"""MongoDB database connector."""
from typing import Any, Dict, List, Optional
import streamlit as st

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

from .base_connector import BaseConnector


class MongoDBConnector(BaseConnector):
    """MongoDB database connector."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize MongoDB connector.

        Args:
            config: Database configuration
        """
        if not PYMONGO_AVAILABLE:
            raise ImportError(
                "pymongo is not installed. Install it with: pip install pymongo"
            )

        if config is None:
            try:
                config = dict(st.secrets.get("database", {}))
            except Exception:
                raise ValueError("Database configuration not found")

        super().__init__(config)
        self.client = None
        self.db = None

    def connect(self) -> None:
        """Establish a connection to MongoDB."""
        try:
            host = self.config.get("host", "localhost")
            port = self.config.get("port", 27017)
            username = self.config.get("username")
            password = self.config.get("password")
            database = self.config.get("database")

            if username and password:
                connection_string = f"mongodb://{username}:{password}@{host}:{port}/"
            else:
                connection_string = f"mongodb://{host}:{port}/"

            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            self.db = self.client[database]

            # Test connection
            self.client.admin.command("ping")
            self.logger.info(f"Connected to MongoDB database: {database}")

        except ConnectionFailure as e:
            self.logger.error(f"Error connecting to MongoDB: {e}")
            raise

    def disconnect(self) -> None:
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            self.logger.info("Disconnected from MongoDB database")

    def execute_query(
        self, query: str, params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """Execute a query (not typically used for MongoDB).

        For MongoDB, use find_documents() instead.

        Args:
            query: Not used for MongoDB
            params: Not used for MongoDB

        Returns:
            Empty list
        """
        self.logger.warning("execute_query() is not typical for MongoDB. Use find_documents() instead.")
        return []

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an update (not typically used for MongoDB).

        For MongoDB, use update_documents() instead.

        Args:
            query: Not used for MongoDB
            params: Not used for MongoDB

        Returns:
            0
        """
        self.logger.warning("execute_update() is not typical for MongoDB. Use update_documents() instead.")
        return 0

    def is_connected(self) -> bool:
        """Check if the MongoDB connection is active.

        Returns:
            True if connected, False otherwise
        """
        if not self.client:
            return False

        try:
            self.client.admin.command("ping")
            return True
        except Exception:
            return False

    # MongoDB-specific methods

    def find_documents(
        self, collection: str, filter_query: Optional[Dict[str, Any]] = None, limit: int = 0
    ) -> List[Dict[str, Any]]:
        """Find documents in a collection.

        Args:
            collection: Collection name
            filter_query: Query filter
            limit: Maximum number of documents to return (0 = no limit)

        Returns:
            List of documents
        """
        if not self.db:
            self.connect()

        try:
            coll = self.db[collection]
            filter_query = filter_query or {}

            if limit > 0:
                cursor = coll.find(filter_query).limit(limit)
            else:
                cursor = coll.find(filter_query)

            # Convert ObjectId to string
            results = []
            for doc in cursor:
                if "_id" in doc:
                    doc["_id"] = str(doc["_id"])
                results.append(doc)

            return results

        except Exception as e:
            self.logger.error(f"Error finding documents: {e}")
            raise

    def insert_document(self, collection: str, document: Dict[str, Any]) -> str:
        """Insert a document into a collection.

        Args:
            collection: Collection name
            document: Document to insert

        Returns:
            Inserted document ID
        """
        if not self.db:
            self.connect()

        try:
            coll = self.db[collection]
            result = coll.insert_one(document)
            return str(result.inserted_id)

        except Exception as e:
            self.logger.error(f"Error inserting document: {e}")
            raise

    def update_documents(
        self, collection: str, filter_query: Dict[str, Any], update: Dict[str, Any]
    ) -> int:
        """Update documents in a collection.

        Args:
            collection: Collection name
            filter_query: Query filter
            update: Update operations

        Returns:
            Number of modified documents
        """
        if not self.db:
            self.connect()

        try:
            coll = self.db[collection]
            result = coll.update_many(filter_query, {"$set": update})
            return result.modified_count

        except Exception as e:
            self.logger.error(f"Error updating documents: {e}")
            raise

    def delete_documents(self, collection: str, filter_query: Dict[str, Any]) -> int:
        """Delete documents from a collection.

        Args:
            collection: Collection name
            filter_query: Query filter

        Returns:
            Number of deleted documents
        """
        if not self.db:
            self.connect()

        try:
            coll = self.db[collection]
            result = coll.delete_many(filter_query)
            return result.deleted_count

        except Exception as e:
            self.logger.error(f"Error deleting documents: {e}")
            raise


@st.cache_resource
def get_mongodb_connection() -> MongoDBConnector:
    """Get a cached MongoDB connection.

    Returns:
        MongoDBConnector instance
    """
    connector = MongoDBConnector()
    connector.connect()
    return connector
