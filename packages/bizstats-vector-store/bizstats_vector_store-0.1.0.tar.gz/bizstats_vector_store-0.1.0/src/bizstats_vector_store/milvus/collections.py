"""
Milvus collection management.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import logging
from typing import Optional, Dict, Any, List

from bizstats_vector_store.config import get_config, VectorStoreConfig
from bizstats_vector_store.models.enums import CollectionType, IndexType
from bizstats_vector_store.milvus.client import MilvusClient, get_client

logger = logging.getLogger(__name__)


class CollectionManagerError(Exception):
    """Error during collection management."""

    pass


class CollectionManager:
    """
    Manages Milvus collections for different use cases.

    Supports:
    - Chat message embeddings (backward compatible)
    - Knowledge base document embeddings (per-project)
    """

    def __init__(
        self,
        client: Optional[MilvusClient] = None,
        config: Optional[VectorStoreConfig] = None,
    ):
        """
        Initialize collection manager.

        Args:
            client: Milvus client instance (uses global client if not provided)
            config: Vector store configuration (uses global config if not provided)
        """
        self.client = client or get_client()
        self.config = config or get_config()
        self._collection_cache: Dict[str, Any] = {}

    def get_collection_name(
        self,
        collection_type: CollectionType,
        project_id: Optional[str] = None,
    ) -> str:
        """
        Generate collection name for a given type and project.

        Args:
            collection_type: Type of collection
            project_id: Project ID (required for knowledge base)

        Returns:
            Collection name string
        """
        if collection_type == CollectionType.CHAT_MESSAGES:
            return self.config.default_chat_collection
        elif collection_type == CollectionType.KNOWLEDGE_BASE:
            if project_id is None:
                raise ValueError("project_id is required for knowledge base collections")
            # Sanitize project_id for Milvus (replace hyphens with underscores)
            sanitized = project_id.replace("-", "_")
            return f"{self.config.knowledge_collection_prefix}{sanitized}"
        else:
            raise ValueError(f"Unknown collection type: {collection_type}")

    async def ensure_collection(
        self,
        collection_type: CollectionType,
        project_id: Optional[str] = None,
    ) -> Any:
        """
        Ensure a collection exists, creating if necessary.

        Args:
            collection_type: Type of collection
            project_id: Project ID (for knowledge base)

        Returns:
            Milvus Collection instance
        """
        collection_name = self.get_collection_name(collection_type, project_id)
        return await self.ensure_collection_by_name(collection_name, collection_type)

    async def ensure_collection_by_name(
        self,
        collection_name: str,
        collection_type: CollectionType,
    ) -> Any:
        """
        Ensure collection exists by name.

        Args:
            collection_name: Name of the collection
            collection_type: Type of collection

        Returns:
            Milvus Collection instance
        """
        from pymilvus import Collection, utility

        self.client.ensure_connected()

        # Check cache first
        if collection_name in self._collection_cache:
            return self._collection_cache[collection_name]

        # Check if collection exists
        if utility.has_collection(collection_name):
            collection = Collection(name=collection_name)
            collection.load()
            self._collection_cache[collection_name] = collection
            logger.info(f"Loaded existing collection: {collection_name}")
            return collection
        else:
            # Create new collection
            collection = await self.create_collection(collection_name, collection_type)
            collection.load()
            self._collection_cache[collection_name] = collection
            logger.info(f"Created new collection: {collection_name}")
            return collection

    async def create_collection(
        self,
        collection_name: str,
        collection_type: CollectionType,
    ) -> Any:
        """
        Create a new collection.

        Args:
            collection_name: Name of the collection
            collection_type: Type of collection

        Returns:
            Milvus Collection instance
        """
        if collection_type == CollectionType.CHAT_MESSAGES:
            return await self._create_chat_collection(collection_name)
        elif collection_type == CollectionType.KNOWLEDGE_BASE:
            return await self._create_knowledge_collection(collection_name)
        else:
            raise CollectionManagerError(f"Unknown collection type: {collection_type}")

    async def _create_chat_collection(self, collection_name: str) -> Any:
        """Create chat messages collection."""
        from pymilvus import Collection, CollectionSchema, FieldSchema, DataType

        self.client.ensure_connected()

        fields = [
            FieldSchema(
                name="pk",
                dtype=DataType.INT64,
                is_primary=True,
                auto_id=False,
                description="Primary key mapping to messages.id",
            ),
            FieldSchema(
                name="embedding",
                dtype=DataType.FLOAT_VECTOR,
                dim=self.config.embedding_dimension,
                description="Message content embedding vector",
            ),
            FieldSchema(
                name="conversation_id",
                dtype=DataType.VARCHAR,
                max_length=36,
                description="UUID of the conversation",
            ),
            FieldSchema(
                name="agent_id",
                dtype=DataType.VARCHAR,
                max_length=36,
                description="UUID of the agent",
            ),
            FieldSchema(
                name="user_id",
                dtype=DataType.VARCHAR,
                max_length=36,
                description="UUID of the user",
            ),
            FieldSchema(
                name="created_at",
                dtype=DataType.INT64,
                description="Message creation timestamp",
            ),
            FieldSchema(
                name="role",
                dtype=DataType.VARCHAR,
                max_length=20,
                description="Message role",
            ),
            FieldSchema(
                name="content_preview",
                dtype=DataType.VARCHAR,
                max_length=500,
                description="First 500 chars of content",
            ),
        ]

        schema = CollectionSchema(
            fields=fields,
            description="Chat message embeddings for semantic search",
        )
        collection = Collection(name=collection_name, schema=schema)

        # Create indexes
        index_params = {
            "index_type": "IVF_PQ",
            "metric_type": "COSINE",
            "params": {"nlist": 4096, "m": 8, "nbits": 8},
        }
        collection.create_index(field_name="embedding", index_params=index_params)

        # Filter indexes
        collection.create_index(field_name="conversation_id")
        collection.create_index(field_name="agent_id")
        collection.create_index(field_name="user_id")
        collection.create_index(field_name="created_at")
        collection.create_index(field_name="role")

        logger.info(f"Created chat collection: {collection_name}")
        return collection

    async def _create_knowledge_collection(self, collection_name: str) -> Any:
        """Create knowledge base collection."""
        from pymilvus import Collection, CollectionSchema, FieldSchema, DataType

        self.client.ensure_connected()

        fields = [
            FieldSchema(
                name="pk",
                dtype=DataType.INT64,
                is_primary=True,
                auto_id=True,
                description="Auto-generated primary key",
            ),
            FieldSchema(
                name="embedding",
                dtype=DataType.FLOAT_VECTOR,
                dim=self.config.embedding_dimension,
                description="Document content embedding vector",
            ),
            FieldSchema(
                name="document_id",
                dtype=DataType.VARCHAR,
                max_length=255,
                description="ID of the source document",
            ),
            FieldSchema(
                name="project_id",
                dtype=DataType.VARCHAR,
                max_length=255,
                description="ID of the project",
            ),
            FieldSchema(
                name="chunk_index",
                dtype=DataType.INT32,
                description="Chunk index within document",
            ),
            FieldSchema(
                name="document_title",
                dtype=DataType.VARCHAR,
                max_length=255,
                description="Title of the document",
            ),
            FieldSchema(
                name="document_type",
                dtype=DataType.VARCHAR,
                max_length=50,
                description="Type of document",
            ),
            FieldSchema(
                name="content_preview",
                dtype=DataType.VARCHAR,
                max_length=1000,
                description="First 1000 chars of chunk",
            ),
            FieldSchema(
                name="metadata_json",
                dtype=DataType.VARCHAR,
                max_length=2000,
                description="JSON-encoded metadata",
            ),
            FieldSchema(
                name="created_at",
                dtype=DataType.INT64,
                description="Embedding creation timestamp",
            ),
        ]

        schema = CollectionSchema(
            fields=fields,
            description="Knowledge base document embeddings",
        )
        collection = Collection(name=collection_name, schema=schema)

        # Create indexes
        index_params = {
            "index_type": self.config.index_type,
            "metric_type": "COSINE",
            "params": {"nlist": self.config.index_nlist},
        }
        collection.create_index(field_name="embedding", index_params=index_params)

        # Filter indexes
        collection.create_index(field_name="document_id")
        collection.create_index(field_name="project_id")
        collection.create_index(field_name="document_type")
        collection.create_index(field_name="created_at")

        logger.info(f"Created knowledge collection: {collection_name}")
        return collection

    async def list_collections(self) -> List[Dict[str, Any]]:
        """
        List all collections with their information.

        Returns:
            List of collection info dictionaries
        """
        from pymilvus import Collection, utility

        self.client.ensure_connected()

        collection_names = utility.list_collections()
        collections_info = []

        for name in collection_names:
            try:
                collection = Collection(name)
                collections_info.append({
                    "name": name,
                    "num_entities": collection.num_entities,
                    "is_loaded": collection.is_loaded,
                    "type": self._guess_collection_type(name),
                })
            except Exception as e:
                collections_info.append({
                    "name": name,
                    "error": str(e),
                    "type": "unknown",
                })

        return collections_info

    def _guess_collection_type(self, collection_name: str) -> str:
        """Guess collection type from name."""
        if "knowledge" in collection_name:
            return CollectionType.KNOWLEDGE_BASE.value
        elif "chat" in collection_name:
            return CollectionType.CHAT_MESSAGES.value
        return "unknown"

    def clear_cache(self) -> None:
        """Clear the collection cache."""
        self._collection_cache.clear()


# Module-level convenience functions

_manager: Optional[CollectionManager] = None


def get_collection_manager() -> CollectionManager:
    """Get the default collection manager."""
    global _manager
    if _manager is None:
        _manager = CollectionManager()
    return _manager
