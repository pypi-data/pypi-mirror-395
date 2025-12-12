"""
Vector store configuration settings.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings


class VectorStoreConfig(BaseSettings):
    """Configuration for vector store operations."""

    # Milvus settings
    milvus_host: str = Field(default="localhost", description="Milvus server host")
    milvus_port: int = Field(default=19530, description="Milvus server port")
    milvus_alias: str = Field(default="default", description="Milvus connection alias")

    # Embedding settings
    embedding_provider: str = Field(
        default="ollama", description="Embedding provider: ollama, openai, httpx"
    )
    embedding_model: str = Field(
        default="mxbai-embed-large:latest", description="Embedding model name"
    )
    embedding_dimension: int = Field(default=1024, description="Embedding vector dimension")

    # Ollama settings
    ollama_base_url: str = Field(
        default="http://localhost:11434", description="Ollama server base URL"
    )
    ollama_api_key: Optional[str] = Field(default=None, description="Ollama API key (optional)")

    # OpenAI settings
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="text-embedding-3-small", description="OpenAI embedding model")

    # Redis caching
    redis_url: Optional[str] = Field(default=None, description="Redis URL for embedding cache")
    cache_ttl_seconds: int = Field(default=3600, description="Cache TTL in seconds")
    enable_cache: bool = Field(default=True, description="Enable Redis caching")

    # Chunking settings
    chunk_max_tokens: int = Field(default=500, description="Maximum tokens per chunk")
    chunk_overlap_tokens: int = Field(default=50, description="Overlap tokens between chunks")

    # Search settings
    default_search_limit: int = Field(default=10, description="Default search result limit")
    default_score_threshold: float = Field(
        default=0.7, description="Default similarity score threshold"
    )
    enable_hybrid_search: bool = Field(default=True, description="Enable hybrid search by default")

    # Smart filtering
    min_content_length: int = Field(default=10, description="Minimum content length for embedding")
    max_content_length: int = Field(default=8000, description="Maximum content length for embedding")
    embeddable_roles: List[str] = Field(
        default=["user", "assistant"], description="Roles that can be embedded"
    )

    # Collection defaults
    default_chat_collection: str = Field(
        default="chat_message_embeddings", description="Default chat messages collection"
    )
    knowledge_collection_prefix: str = Field(
        default="knowledge_project_", description="Prefix for knowledge base collections"
    )

    # Index settings
    index_type: str = Field(default="IVF_FLAT", description="Milvus index type")
    index_nlist: int = Field(default=2048, description="Number of cluster units for IVF indexes")
    search_nprobe: int = Field(default=32, description="Number of units to query during search")

    model_config = {
        "env_prefix": "VECTOR_STORE_",
        "case_sensitive": False,
        "extra": "ignore",
    }


# Global configuration instance
_config: Optional[VectorStoreConfig] = None


def get_config() -> VectorStoreConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = VectorStoreConfig()
    return _config


def configure(**kwargs) -> VectorStoreConfig:
    """
    Configure the global vector store settings.

    Args:
        **kwargs: Configuration options to override

    Returns:
        Updated configuration instance
    """
    global _config
    _config = VectorStoreConfig(**kwargs)
    return _config


def reset_config() -> None:
    """Reset configuration to defaults (useful for testing)."""
    global _config
    _config = None
