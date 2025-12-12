"""
Tests for vector store configuration.
"""

import pytest
from bizstats_vector_store.config import (
    VectorStoreConfig,
    get_config,
    configure,
    reset_config,
)


class TestVectorStoreConfig:
    """Tests for VectorStoreConfig."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    def test_default_values(self):
        """Test default configuration values."""
        config = VectorStoreConfig()

        assert config.milvus_host == "localhost"
        assert config.milvus_port == 19530
        assert config.embedding_provider == "ollama"
        assert config.embedding_model == "mxbai-embed-large:latest"
        assert config.embedding_dimension == 1024
        assert config.chunk_max_tokens == 500
        assert config.chunk_overlap_tokens == 50
        assert config.default_search_limit == 10
        assert config.default_score_threshold == 0.7

    def test_custom_values(self):
        """Test configuration with custom values."""
        config = VectorStoreConfig(
            milvus_host="milvus.example.com",
            milvus_port=19531,
            embedding_provider="openai",
            embedding_dimension=1536,
        )

        assert config.milvus_host == "milvus.example.com"
        assert config.milvus_port == 19531
        assert config.embedding_provider == "openai"
        assert config.embedding_dimension == 1536

    def test_get_config_singleton(self):
        """Test get_config returns singleton instance."""
        config1 = get_config()
        config2 = get_config()
        assert config1 is config2

    def test_configure_updates_global(self):
        """Test configure updates global instance."""
        configure(milvus_host="custom-host")
        config = get_config()
        assert config.milvus_host == "custom-host"

    def test_reset_config(self):
        """Test reset_config clears global instance."""
        configure(milvus_host="custom-host")
        reset_config()
        config = get_config()
        assert config.milvus_host == "localhost"

    def test_redis_settings(self):
        """Test Redis cache settings."""
        config = VectorStoreConfig(
            redis_url="redis://localhost:6379",
            cache_ttl_seconds=7200,
            enable_cache=True,
        )

        assert config.redis_url == "redis://localhost:6379"
        assert config.cache_ttl_seconds == 7200
        assert config.enable_cache is True

    def test_ollama_settings(self):
        """Test Ollama-specific settings."""
        config = VectorStoreConfig(
            ollama_base_url="https://ollama.example.com",
            ollama_api_key="test-api-key",
        )

        assert config.ollama_base_url == "https://ollama.example.com"
        assert config.ollama_api_key == "test-api-key"

    def test_openai_settings(self):
        """Test OpenAI-specific settings."""
        config = VectorStoreConfig(
            openai_api_key="sk-test-key",
            openai_model="text-embedding-ada-002",
        )

        assert config.openai_api_key == "sk-test-key"
        assert config.openai_model == "text-embedding-ada-002"

    def test_index_settings(self):
        """Test index configuration."""
        config = VectorStoreConfig(
            index_type="HNSW",
            index_nlist=4096,
            search_nprobe=64,
        )

        assert config.index_type == "HNSW"
        assert config.index_nlist == 4096
        assert config.search_nprobe == 64

    def test_collection_prefixes(self):
        """Test collection naming settings."""
        config = VectorStoreConfig(
            default_chat_collection="custom_chat",
            knowledge_collection_prefix="kb_",
        )

        assert config.default_chat_collection == "custom_chat"
        assert config.knowledge_collection_prefix == "kb_"

    def test_smart_filtering_settings(self):
        """Test smart filtering configuration."""
        config = VectorStoreConfig(
            min_content_length=20,
            max_content_length=4000,
            embeddable_roles=["user", "assistant", "system"],
        )

        assert config.min_content_length == 20
        assert config.max_content_length == 4000
        assert "system" in config.embeddable_roles

    def test_hybrid_search_default(self):
        """Test hybrid search is enabled by default."""
        config = VectorStoreConfig()
        assert config.enable_hybrid_search is True
