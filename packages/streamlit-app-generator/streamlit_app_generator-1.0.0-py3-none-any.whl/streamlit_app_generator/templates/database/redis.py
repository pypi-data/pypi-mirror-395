"""Redis database connector."""
from typing import Any, Dict, List, Optional
import streamlit as st
import json

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from .base_connector import BaseConnector


class RedisConnector(BaseConnector):
    """Redis database connector with connection pooling."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize Redis connector.

        Args:
            config: Database configuration
        """
        if not REDIS_AVAILABLE:
            raise ImportError(
                "redis is not installed. Install it with: pip install redis"
            )

        if config is None:
            try:
                config = dict(st.secrets.get("database", {}))
            except Exception:
                raise ValueError("Database configuration not found")

        super().__init__(config)
        self.pool = None

    def connect(self) -> None:
        """Establish a connection pool to Redis."""
        try:
            self.pool = redis.ConnectionPool(
                host=self.config.get("host", "localhost"),
                port=self.config.get("port", 6379),
                password=self.config.get("password", None),
                db=self.config.get("db", 0),
                decode_responses=True,
            )

            self.connection = redis.Redis(connection_pool=self.pool)

            # Test connection
            self.connection.ping()
            self.logger.info("Connected to Redis database")

        except redis.RedisError as e:
            self.logger.error(f"Error connecting to Redis: {e}")
            raise

    def disconnect(self) -> None:
        """Close the Redis connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

        if self.pool:
            self.pool.disconnect()
            self.pool = None

        self.logger.info("Disconnected from Redis database")

    def execute_query(
        self, query: str, params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """Execute a query (not typical for Redis).

        For Redis, use get/set methods instead.

        Args:
            query: Not used for Redis
            params: Not used for Redis

        Returns:
            Empty list
        """
        self.logger.warning("execute_query() is not typical for Redis. Use get/set methods instead.")
        return []

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an update (not typical for Redis).

        For Redis, use set/delete methods instead.

        Args:
            query: Not used for Redis
            params: Not used for Redis

        Returns:
            0
        """
        self.logger.warning("execute_update() is not typical for Redis. Use set/delete methods instead.")
        return 0

    def is_connected(self) -> bool:
        """Check if the Redis connection is active.

        Returns:
            True if connected, False otherwise
        """
        if not self.connection:
            return False

        try:
            self.connection.ping()
            return True
        except redis.RedisError:
            return False

    # Redis-specific methods

    def get(self, key: str) -> Optional[str]:
        """Get a value by key.

        Args:
            key: Redis key

        Returns:
            Value or None if not found
        """
        if not self.connection:
            self.connect()

        try:
            return self.connection.get(key)
        except redis.RedisError as e:
            self.logger.error(f"Error getting value: {e}")
            raise

    def set(
        self, key: str, value: str, expire: Optional[int] = None
    ) -> bool:
        """Set a key-value pair.

        Args:
            key: Redis key
            value: Value to store
            expire: Optional expiration time in seconds

        Returns:
            True if successful
        """
        if not self.connection:
            self.connect()

        try:
            return self.connection.set(key, value, ex=expire)
        except redis.RedisError as e:
            self.logger.error(f"Error setting value: {e}")
            raise

    def get_json(self, key: str) -> Optional[Dict[str, Any]]:
        """Get a JSON value by key.

        Args:
            key: Redis key

        Returns:
            Parsed JSON dictionary or None
        """
        value = self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                self.logger.error(f"Error decoding JSON: {e}")
                return None
        return None

    def set_json(
        self, key: str, value: Dict[str, Any], expire: Optional[int] = None
    ) -> bool:
        """Set a JSON value.

        Args:
            key: Redis key
            value: Dictionary to store as JSON
            expire: Optional expiration time in seconds

        Returns:
            True if successful
        """
        try:
            json_value = json.dumps(value)
            return self.set(key, json_value, expire)
        except (TypeError, json.JSONEncodeError) as e:
            self.logger.error(f"Error encoding JSON: {e}")
            raise

    def delete(self, *keys: str) -> int:
        """Delete one or more keys.

        Args:
            keys: Keys to delete

        Returns:
            Number of keys deleted
        """
        if not self.connection:
            self.connect()

        try:
            return self.connection.delete(*keys)
        except redis.RedisError as e:
            self.logger.error(f"Error deleting keys: {e}")
            raise

    def exists(self, *keys: str) -> int:
        """Check if keys exist.

        Args:
            keys: Keys to check

        Returns:
            Number of existing keys
        """
        if not self.connection:
            self.connect()

        try:
            return self.connection.exists(*keys)
        except redis.RedisError as e:
            self.logger.error(f"Error checking existence: {e}")
            raise


@st.cache_resource
def get_redis_connection() -> RedisConnector:
    """Get a cached Redis connection.

    Returns:
        RedisConnector instance
    """
    connector = RedisConnector()
    connector.connect()
    return connector
