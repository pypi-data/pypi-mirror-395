"""
BizStats Vector Store - Milvus vector database wrapper with embedding generation.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

Features:
- Milvus collection management
- Embedding generation (Ollama/OpenAI)
- Document chunking for large texts
- Semantic search with filtering
- Redis caching for embeddings
- Hybrid search (semantic + keyword)
"""

from bizstats_vector_store.config import VectorStoreConfig, get_config, configure
from bizstats_vector_store.models.enums import CollectionType, EmbeddingProvider, IndexType
from bizstats_vector_store.models.schemas import (
    EmbeddingRequest,
    EmbeddingResponse,
    SearchRequest,
    SearchResult,
    SearchResponse,
    DocumentChunk,
    CollectionInfo,
)
from bizstats_vector_store.chunking.document import DocumentChunker
from bizstats_vector_store.embedding.service import EmbeddingGenerator
from bizstats_vector_store.milvus.client import MilvusClient
from bizstats_vector_store.milvus.collections import CollectionManager
from bizstats_vector_store.search.semantic import SemanticSearch

__version__ = "0.1.0"
__all__ = [
    # Config
    "VectorStoreConfig",
    "get_config",
    "configure",
    # Enums
    "CollectionType",
    "EmbeddingProvider",
    "IndexType",
    # Schemas
    "EmbeddingRequest",
    "EmbeddingResponse",
    "SearchRequest",
    "SearchResult",
    "SearchResponse",
    "DocumentChunk",
    "CollectionInfo",
    # Core classes
    "DocumentChunker",
    "EmbeddingGenerator",
    "MilvusClient",
    "CollectionManager",
    "SemanticSearch",
]
