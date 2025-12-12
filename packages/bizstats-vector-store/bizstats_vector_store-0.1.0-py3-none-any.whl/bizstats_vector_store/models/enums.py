"""
Enumerations for vector store operations.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from enum import Enum


class CollectionType(str, Enum):
    """Types of Milvus collections."""

    CHAT_MESSAGES = "chat_messages"
    KNOWLEDGE_BASE = "knowledge_base"


class EmbeddingProvider(str, Enum):
    """Supported embedding providers."""

    OLLAMA = "ollama"
    OPENAI = "openai"
    HTTPX = "httpx"  # Generic HTTP-based provider


class IndexType(str, Enum):
    """Milvus index types for vector search."""

    FLAT = "FLAT"  # Brute-force search, 100% accuracy
    IVF_FLAT = "IVF_FLAT"  # Inverted file with flat quantization
    IVF_SQ8 = "IVF_SQ8"  # IVF with scalar quantization
    IVF_PQ = "IVF_PQ"  # IVF with product quantization
    HNSW = "HNSW"  # Hierarchical Navigable Small World graphs
    AUTOINDEX = "AUTOINDEX"  # Automatic index selection


class MetricType(str, Enum):
    """Distance metrics for similarity search."""

    COSINE = "COSINE"  # Cosine similarity (normalized)
    L2 = "L2"  # Euclidean distance
    IP = "IP"  # Inner product


class DocumentType(str, Enum):
    """Types of documents for knowledge base."""

    TEXT = "text"
    FILE = "file"
    URL = "url"
    PDF = "pdf"
    HTML = "html"


class FilterOperator(str, Enum):
    """Operators for search filters."""

    EQUALS = "=="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    IN = "in"
    NOT_IN = "not in"
    LIKE = "like"
