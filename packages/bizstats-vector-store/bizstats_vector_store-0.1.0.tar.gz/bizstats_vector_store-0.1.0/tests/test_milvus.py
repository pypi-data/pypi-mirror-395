"""
Tests for Milvus client and collection management.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from bizstats_vector_store.config import reset_config, configure
from bizstats_vector_store.models.enums import CollectionType
from bizstats_vector_store.milvus.client import (
    MilvusClient,
    MilvusClientError,
    get_client,
)
from bizstats_vector_store.milvus.collections import (
    CollectionManager,
    CollectionManagerError,
    get_collection_manager,
)


class TestMilvusClient:
    """Tests for MilvusClient class."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    def test_client_initialization_defaults(self):
        """Test client initialization with defaults."""
        client = MilvusClient()

        assert client.host == "localhost"
        assert client.port == 19530
        assert client.alias == "default"
        assert client._connected is False

    def test_client_initialization_custom(self):
        """Test client with custom connection params."""
        client = MilvusClient(
            host="milvus.example.com",
            port=19531,
            alias="custom",
        )

        assert client.host == "milvus.example.com"
        assert client.port == 19531
        assert client.alias == "custom"

    def test_client_from_config(self):
        """Test client reads from config."""
        configure(
            milvus_host="config-host",
            milvus_port=19532,
        )
        client = MilvusClient()

        assert client.host == "config-host"
        assert client.port == 19532

    @patch("pymilvus.connections")
    def test_connect_success(self, mock_connections):
        """Test successful connection."""
        client = MilvusClient()
        client.connect()

        mock_connections.connect.assert_called_once_with(
            alias="default",
            host="localhost",
            port=19530,
        )
        assert client._connected is True

    @patch("pymilvus.connections")
    def test_connect_failure(self, mock_connections):
        """Test connection failure."""
        mock_connections.connect.side_effect = Exception("Connection refused")

        client = MilvusClient()

        with pytest.raises(MilvusClientError) as exc_info:
            client.connect()

        assert "Connection failed" in str(exc_info.value)

    @patch("pymilvus.connections")
    def test_disconnect(self, mock_connections):
        """Test disconnection."""
        client = MilvusClient()
        client._connected = True

        client.disconnect()

        mock_connections.disconnect.assert_called_once_with("default")
        assert client._connected is False

    def test_is_connected_property(self):
        """Test is_connected property."""
        client = MilvusClient()

        assert client.is_connected is False

        client._connected = True
        assert client.is_connected is True

    @patch("pymilvus.connections")
    def test_ensure_connected(self, mock_connections):
        """Test ensure_connected connects if needed."""
        client = MilvusClient()

        client.ensure_connected()

        mock_connections.connect.assert_called_once()
        assert client._connected is True

    @patch("pymilvus.connections")
    def test_ensure_connected_already_connected(self, mock_connections):
        """Test ensure_connected skips if already connected."""
        client = MilvusClient()
        client._connected = True

        client.ensure_connected()

        mock_connections.connect.assert_not_called()

    @patch("pymilvus.connections")
    @patch("pymilvus.utility")
    def test_list_collections(self, mock_utility, mock_connections):
        """Test listing collections."""
        mock_utility.list_collections.return_value = ["col1", "col2"]

        client = MilvusClient()
        client._connected = True

        collections = client.list_collections()

        assert collections == ["col1", "col2"]

    @patch("pymilvus.connections")
    @patch("pymilvus.utility")
    def test_has_collection(self, mock_utility, mock_connections):
        """Test checking collection existence."""
        mock_utility.has_collection.return_value = True

        client = MilvusClient()
        client._connected = True

        assert client.has_collection("test_collection") is True
        mock_utility.has_collection.assert_called_once_with("test_collection")

    @patch("pymilvus.connections")
    @patch("pymilvus.utility")
    def test_drop_collection(self, mock_utility, mock_connections):
        """Test dropping a collection."""
        mock_utility.has_collection.return_value = True

        client = MilvusClient()
        client._connected = True

        result = client.drop_collection("old_collection")

        assert result is True
        mock_utility.drop_collection.assert_called_once_with("old_collection")

    @patch("pymilvus.connections")
    @patch("pymilvus.utility")
    def test_drop_nonexistent_collection(self, mock_utility, mock_connections):
        """Test dropping non-existent collection."""
        mock_utility.has_collection.return_value = False

        client = MilvusClient()
        client._connected = True

        result = client.drop_collection("nonexistent")

        assert result is False
        mock_utility.drop_collection.assert_not_called()

    @patch("pymilvus.connections")
    @patch("pymilvus.Collection")
    def test_get_collection_stats(self, MockCollection, mock_connections):
        """Test getting collection statistics."""
        mock_collection = Mock()
        mock_collection.num_entities = 1000
        mock_collection.is_loaded = True
        MockCollection.return_value = mock_collection

        client = MilvusClient()
        client._connected = True

        stats = client.get_collection_stats("test_collection")

        assert stats["name"] == "test_collection"
        assert stats["num_entities"] == 1000
        assert stats["is_loaded"] is True

    @patch("pymilvus.connections")
    def test_connection_context_manager(self, mock_connections):
        """Test connection context manager."""
        client = MilvusClient()

        with client.connection():
            assert client._connected is True

        mock_connections.disconnect.assert_called_once()


class TestCollectionManager:
    """Tests for CollectionManager class."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    def test_manager_initialization(self):
        """Test manager initialization."""
        mock_client = Mock()
        manager = CollectionManager(client=mock_client)

        assert manager.client is mock_client
        assert manager._collection_cache == {}

    def test_get_collection_name_chat(self):
        """Test getting chat collection name."""
        manager = CollectionManager(client=Mock())

        name = manager.get_collection_name(CollectionType.CHAT_MESSAGES)

        assert name == "chat_message_embeddings"

    def test_get_collection_name_knowledge(self):
        """Test getting knowledge collection name."""
        manager = CollectionManager(client=Mock())

        name = manager.get_collection_name(
            CollectionType.KNOWLEDGE_BASE,
            project_id="proj-123",
        )

        assert name == "knowledge_project_proj_123"

    def test_get_collection_name_knowledge_sanitizes(self):
        """Test knowledge collection name sanitizes hyphens."""
        manager = CollectionManager(client=Mock())

        name = manager.get_collection_name(
            CollectionType.KNOWLEDGE_BASE,
            project_id="proj-with-hyphens",
        )

        assert name == "knowledge_project_proj_with_hyphens"
        assert "-" not in name.split("knowledge_project_")[1]

    def test_get_collection_name_knowledge_requires_project(self):
        """Test knowledge collection requires project_id."""
        manager = CollectionManager(client=Mock())

        with pytest.raises(ValueError) as exc_info:
            manager.get_collection_name(CollectionType.KNOWLEDGE_BASE)

        assert "project_id is required" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_ensure_collection_cached(self):
        """Test ensure_collection returns cached collection."""
        manager = CollectionManager(client=Mock())

        mock_collection = Mock()
        manager._collection_cache["chat_message_embeddings"] = mock_collection

        result = await manager.ensure_collection(CollectionType.CHAT_MESSAGES)

        assert result is mock_collection

    @pytest.mark.asyncio
    @patch("pymilvus.utility")
    @patch("pymilvus.Collection")
    async def test_ensure_collection_existing(self, MockCollection, mock_utility):
        """Test ensure_collection loads existing collection."""
        mock_client = Mock()
        mock_client.ensure_connected = Mock()

        manager = CollectionManager(client=mock_client)

        mock_collection = Mock()
        mock_collection.load = Mock()
        mock_utility.has_collection.return_value = True
        MockCollection.return_value = mock_collection

        result = await manager.ensure_collection(CollectionType.CHAT_MESSAGES)

        assert result is mock_collection
        mock_collection.load.assert_called_once()

    @pytest.mark.asyncio
    @patch("pymilvus.Collection")
    @patch("pymilvus.CollectionSchema")
    @patch("pymilvus.FieldSchema")
    @patch("pymilvus.DataType")
    async def test_create_chat_collection(
        self, MockDataType, MockFieldSchema, MockCollectionSchema, MockCollection
    ):
        """Test creating chat messages collection."""
        mock_client = Mock()
        mock_client.ensure_connected = Mock()

        manager = CollectionManager(client=mock_client)

        mock_collection = Mock()
        mock_collection.create_index = Mock()
        MockCollection.return_value = mock_collection

        result = await manager._create_chat_collection("test_chat")

        assert result is mock_collection
        # Should create indexes
        assert mock_collection.create_index.call_count >= 6

    @pytest.mark.asyncio
    @patch("pymilvus.Collection")
    @patch("pymilvus.CollectionSchema")
    @patch("pymilvus.FieldSchema")
    @patch("pymilvus.DataType")
    async def test_create_knowledge_collection(
        self, MockDataType, MockFieldSchema, MockCollectionSchema, MockCollection
    ):
        """Test creating knowledge base collection."""
        mock_client = Mock()
        mock_client.ensure_connected = Mock()

        manager = CollectionManager(client=mock_client)

        mock_collection = Mock()
        mock_collection.create_index = Mock()
        MockCollection.return_value = mock_collection

        result = await manager._create_knowledge_collection("test_kb")

        assert result is mock_collection
        # Should create indexes
        assert mock_collection.create_index.call_count >= 5

    @pytest.mark.asyncio
    @patch("pymilvus.utility")
    @patch("pymilvus.Collection")
    async def test_list_collections(self, MockCollection, mock_utility):
        """Test listing collections."""
        mock_client = Mock()
        mock_client.ensure_connected = Mock()

        manager = CollectionManager(client=mock_client)

        mock_utility.list_collections.return_value = ["chat_col", "knowledge_col"]

        mock_col1 = Mock()
        mock_col1.num_entities = 100
        mock_col1.is_loaded = True

        mock_col2 = Mock()
        mock_col2.num_entities = 200
        mock_col2.is_loaded = False

        MockCollection.side_effect = [mock_col1, mock_col2]

        result = await manager.list_collections()

        assert len(result) == 2

    def test_guess_collection_type_knowledge(self):
        """Test guessing knowledge collection type."""
        manager = CollectionManager(client=Mock())

        result = manager._guess_collection_type("knowledge_project_123")
        assert result == "knowledge_base"

    def test_guess_collection_type_chat(self):
        """Test guessing chat collection type."""
        manager = CollectionManager(client=Mock())

        result = manager._guess_collection_type("chat_message_embeddings")
        assert result == "chat_messages"

    def test_guess_collection_type_unknown(self):
        """Test guessing unknown collection type."""
        manager = CollectionManager(client=Mock())

        result = manager._guess_collection_type("random_collection")
        assert result == "unknown"

    def test_clear_cache(self):
        """Test clearing collection cache."""
        manager = CollectionManager(client=Mock())
        manager._collection_cache = {"col1": Mock(), "col2": Mock()}

        manager.clear_cache()

        assert manager._collection_cache == {}


class TestMilvusClientAdditional:
    """Additional tests for MilvusClient coverage."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    @patch("pymilvus.connections")
    def test_disconnect_error_handling(self, mock_connections):
        """Test disconnect handles errors gracefully."""
        mock_connections.disconnect.side_effect = Exception("Disconnect error")

        client = MilvusClient()
        client._connected = True

        # Should not raise error
        client.disconnect()

        # Note: When disconnect fails, _connected is not updated
        # as the exception is caught before the state change
        # This tests that the error is logged but not raised
        mock_connections.disconnect.assert_called_once()

    @patch("pymilvus.connections")
    @patch("pymilvus.Collection")
    def test_get_collection_stats_error(self, MockCollection, mock_connections):
        """Test get_collection_stats error handling."""
        MockCollection.side_effect = Exception("Collection not found")

        client = MilvusClient()
        client._connected = True

        stats = client.get_collection_stats("bad_collection")

        assert stats["name"] == "bad_collection"
        assert "error" in stats

    @patch("pymilvus.connections")
    @patch("pymilvus.Collection")
    def test_load_collection(self, MockCollection, mock_connections):
        """Test load_collection."""
        mock_collection = Mock()
        mock_collection.load = Mock()
        MockCollection.return_value = mock_collection

        client = MilvusClient()
        client._connected = True

        client.load_collection("test_collection")

        mock_collection.load.assert_called_once()

    @patch("pymilvus.connections")
    @patch("pymilvus.Collection")
    def test_release_collection(self, MockCollection, mock_connections):
        """Test release_collection."""
        mock_collection = Mock()
        mock_collection.release = Mock()
        MockCollection.return_value = mock_collection

        client = MilvusClient()
        client._connected = True

        client.release_collection("test_collection")

        mock_collection.release.assert_called_once()

    @patch("pymilvus.connections")
    @patch("pymilvus.Collection")
    def test_flush_collection(self, MockCollection, mock_connections):
        """Test flush_collection."""
        mock_collection = Mock()
        mock_collection.flush = Mock()
        MockCollection.return_value = mock_collection

        client = MilvusClient()
        client._connected = True

        client.flush_collection("test_collection")

        mock_collection.flush.assert_called_once()

    @patch("pymilvus.connections")
    @patch("pymilvus.Collection")
    def test_compact_collection(self, MockCollection, mock_connections):
        """Test compact_collection."""
        mock_collection = Mock()
        mock_collection.compact = Mock()
        MockCollection.return_value = mock_collection

        client = MilvusClient()
        client._connected = True

        client.compact_collection("test_collection")

        mock_collection.compact.assert_called_once()


class TestModuleFunctions:
    """Tests for module-level functions."""

    def setup_method(self):
        """Reset before each test."""
        reset_config()

    def test_get_client_singleton(self):
        """Test get_client returns singleton."""
        # Reset the global
        import bizstats_vector_store.milvus.client as client_module
        client_module._client = None

        client1 = get_client()
        client2 = get_client()

        assert client1 is client2

    @patch("pymilvus.connections")
    def test_connect_function(self, mock_connections):
        """Test module-level connect function."""
        from bizstats_vector_store.milvus.client import connect
        import bizstats_vector_store.milvus.client as client_module
        client_module._client = None

        client = connect()

        assert client is not None
        mock_connections.connect.assert_called()

    @patch("pymilvus.connections")
    def test_disconnect_function(self, mock_connections):
        """Test module-level disconnect function."""
        from bizstats_vector_store.milvus.client import connect, disconnect
        import bizstats_vector_store.milvus.client as client_module
        client_module._client = None

        connect()
        disconnect()

        mock_connections.disconnect.assert_called()
        assert client_module._client is None

    def test_disconnect_function_no_client(self):
        """Test disconnect when no client exists."""
        from bizstats_vector_store.milvus.client import disconnect
        import bizstats_vector_store.milvus.client as client_module
        client_module._client = None

        # Should not raise error
        disconnect()
        assert client_module._client is None
