"""
Pydantic schemas for vector store operations.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    """Represents a chunk of a document."""

    document_id: str
    project_id: str
    title: str
    content: str
    chunk_index: int
    total_chunks: int
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EmbeddingRequest(BaseModel):
    """Request model for chat message embedding."""

    message_id: int
    content: str
    conversation_id: str
    agent_id: Optional[str] = None
    user_id: Optional[str] = None
    role: str = "user"
    created_at: int
    should_embed: Optional[bool] = None  # Override smart filtering


class EmbeddingResponse(BaseModel):
    """Response model for embedding operations."""

    message_id: int
    embedded: bool
    reason: Optional[str] = None
    processing_time_ms: Optional[float] = None


class BatchEmbeddingRequest(BaseModel):
    """Request model for batch embedding."""

    messages: List[EmbeddingRequest]


class BatchEmbeddingResponse(BaseModel):
    """Response model for batch embedding."""

    results: List[EmbeddingResponse]
    total_processed: int
    total_embedded: int
    total_time_ms: float


class KnowledgeEmbeddingRequest(BaseModel):
    """Request model for knowledge base document embedding."""

    project_id: str
    document_id: str
    title: str
    content: str
    document_type: str = "text"
    metadata: Optional[Dict[str, Any]] = None


class KnowledgeEmbeddingResponse(BaseModel):
    """Response model for knowledge base embedding."""

    document_id: str
    embedded: bool
    chunks_embedded: int = 0
    processing_time_ms: float
    reason: Optional[str] = None


class SearchRequest(BaseModel):
    """Request model for chat message search."""

    query: str
    limit: int = Field(default=10, ge=1, le=100)
    conversation_id: Optional[str] = None
    agent_id: Optional[str] = None
    user_id: Optional[str] = None
    role_filter: Optional[str] = None
    score_threshold: float = Field(default=0.7, ge=0.0, le=1.0)


class SearchResult(BaseModel):
    """Individual search result."""

    message_id: int
    score: float
    conversation_id: str
    agent_id: Optional[str] = None
    user_id: Optional[str] = None
    role: str
    created_at: int
    content_preview: str


class SearchResponse(BaseModel):
    """Response model for search operations."""

    query: str
    results: List[SearchResult]
    total_found: int
    processing_time_ms: float


class KnowledgeSearchRequest(BaseModel):
    """Request model for knowledge base search."""

    query: str
    project_id: str
    limit: int = Field(default=10, ge=1, le=100)
    document_type_filter: Optional[str] = None
    score_threshold: float = Field(default=0.6, ge=0.0, le=1.0)
    hybrid_search: bool = True


class KnowledgeSearchResult(BaseModel):
    """Knowledge search result."""

    document_id: str
    chunk_id: str
    score: float
    project_id: str
    title: str
    document_type: str
    chunk_content: str
    metadata: Dict[str, Any]
    created_at: int


class KnowledgeSearchResponse(BaseModel):
    """Response model for knowledge base search."""

    query: str
    results: List[KnowledgeSearchResult]
    total_found: int
    processing_time_ms: float
    hybrid_search_used: bool = False


class CollectionInfo(BaseModel):
    """Information about a Milvus collection."""

    name: str
    collection_type: str
    num_entities: int = 0
    is_loaded: bool = False
    error: Optional[str] = None


class CollectionCreateRequest(BaseModel):
    """Request model for creating collections."""

    collection_type: str
    project_id: Optional[str] = None


class EmbeddingResult(BaseModel):
    """Result of an embedding operation."""

    embedding: List[float]
    model: str
    processing_time_ms: float
