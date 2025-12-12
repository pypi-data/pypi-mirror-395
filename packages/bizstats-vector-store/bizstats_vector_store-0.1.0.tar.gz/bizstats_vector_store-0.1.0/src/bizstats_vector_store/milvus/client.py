"""
Milvus client wrapper for vector database operations.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import logging
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

from bizstats_vector_store.config import get_config, VectorStoreConfig

logger = logging.getLogger(__name__)


class MilvusClientError(Exception):
    """Error during Milvus operations."""

    pass


class MilvusClient:
    """
    Milvus client wrapper for vector database operations.

    Provides connection management and utility methods for
    interacting with Milvus vector database.
    """

    def __init__(
        self,
        config: Optional[VectorStoreConfig] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        alias: str = "default",
    ):
        """
        Initialize Milvus client.

        Args:
            config: Vector store configuration (uses global config if not provided)
            host: Override Milvus host from config
            port: Override Milvus port from config
            alias: Connection alias
        """
        self.config = config or get_config()
        self.host = host or self.config.milvus_host
        self.port = port or self.config.milvus_port
        self.alias = alias or self.config.milvus_alias
        self._connected = False

    def connect(self) -> None:
        """
        Establish connection to Milvus.

        Raises:
            MilvusClientError: If connection fails
        """
        try:
            from pymilvus import connections

            logger.info(f"Connecting to Milvus at {self.host}:{self.port}")
            connections.connect(alias=self.alias, host=self.host, port=self.port)
            self._connected = True
            logger.info("Successfully connected to Milvus")
        except Exception as e:
            logger.error(f"Failed to connect to Milvus: {e}")
            raise MilvusClientError(f"Connection failed: {e}")

    def disconnect(self) -> None:
        """Disconnect from Milvus."""
        try:
            from pymilvus import connections

            connections.disconnect(self.alias)
            self._connected = False
            logger.info("Disconnected from Milvus")
        except Exception as e:
            logger.warning(f"Error disconnecting from Milvus: {e}")

    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        return self._connected

    def ensure_connected(self) -> None:
        """Ensure client is connected, connecting if necessary."""
        if not self._connected:
            self.connect()

    @contextmanager
    def connection(self):
        """Context manager for Milvus connection."""
        self.connect()
        try:
            yield self
        finally:
            self.disconnect()

    def list_collections(self) -> List[str]:
        """
        List all available collections.

        Returns:
            List of collection names
        """
        self.ensure_connected()
        from pymilvus import utility

        return utility.list_collections()

    def has_collection(self, collection_name: str) -> bool:
        """
        Check if a collection exists.

        Args:
            collection_name: Name of the collection

        Returns:
            True if collection exists
        """
        self.ensure_connected()
        from pymilvus import utility

        return utility.has_collection(collection_name)

    def drop_collection(self, collection_name: str) -> bool:
        """
        Drop a collection.

        Args:
            collection_name: Name of the collection to drop

        Returns:
            True if collection was dropped
        """
        self.ensure_connected()
        from pymilvus import utility

        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
            logger.info(f"Dropped collection: {collection_name}")
            return True
        return False

    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """
        Get statistics for a collection.

        Args:
            collection_name: Name of the collection

        Returns:
            Dictionary with collection statistics
        """
        self.ensure_connected()
        from pymilvus import Collection

        try:
            collection = Collection(name=collection_name)
            return {
                "name": collection_name,
                "num_entities": collection.num_entities,
                "is_loaded": collection.is_loaded,
            }
        except Exception as e:
            logger.error(f"Failed to get stats for {collection_name}: {e}")
            return {"name": collection_name, "error": str(e)}

    def load_collection(self, collection_name: str) -> None:
        """
        Load a collection into memory.

        Args:
            collection_name: Name of the collection to load
        """
        self.ensure_connected()
        from pymilvus import Collection

        collection = Collection(name=collection_name)
        collection.load()
        logger.info(f"Loaded collection: {collection_name}")

    def release_collection(self, collection_name: str) -> None:
        """
        Release a collection from memory.

        Args:
            collection_name: Name of the collection to release
        """
        self.ensure_connected()
        from pymilvus import Collection

        collection = Collection(name=collection_name)
        collection.release()
        logger.info(f"Released collection: {collection_name}")

    def flush_collection(self, collection_name: str) -> None:
        """
        Flush a collection to ensure data persistence.

        Args:
            collection_name: Name of the collection to flush
        """
        self.ensure_connected()
        from pymilvus import Collection

        collection = Collection(name=collection_name)
        collection.flush()
        logger.debug(f"Flushed collection: {collection_name}")

    def compact_collection(self, collection_name: str) -> None:
        """
        Compact a collection to optimize storage.

        Args:
            collection_name: Name of the collection to compact
        """
        self.ensure_connected()
        from pymilvus import Collection

        collection = Collection(name=collection_name)
        collection.compact()
        logger.info(f"Compacted collection: {collection_name}")


# Module-level client instance
_client: Optional[MilvusClient] = None


def get_client() -> MilvusClient:
    """Get or create the default Milvus client."""
    global _client
    if _client is None:
        _client = MilvusClient()
    return _client


def connect() -> MilvusClient:
    """Connect using the default client."""
    client = get_client()
    client.connect()
    return client


def disconnect() -> None:
    """Disconnect the default client."""
    global _client
    if _client is not None:
        _client.disconnect()
        _client = None
