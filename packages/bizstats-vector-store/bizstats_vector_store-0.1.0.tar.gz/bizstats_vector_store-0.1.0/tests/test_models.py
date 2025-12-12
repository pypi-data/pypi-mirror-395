"""
Tests for vector store models.
"""

import pytest
from bizstats_vector_store.models.enums import (
    CollectionType,
    EmbeddingProvider,
    IndexType,
    MetricType,
    DocumentType,
    FilterOperator,
)
from bizstats_vector_store.models.schemas import (
    DocumentChunk,
    EmbeddingRequest,
    EmbeddingResponse,
    BatchEmbeddingRequest,
    BatchEmbeddingResponse,
    KnowledgeEmbeddingRequest,
    SearchRequest,
    SearchResult,
    SearchResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResult,
    CollectionInfo,
    EmbeddingResult,
)


class TestEnums:
    """Tests for enumeration types."""

    def test_collection_type_values(self):
        """Test CollectionType enum values."""
        assert CollectionType.CHAT_MESSAGES.value == "chat_messages"
        assert CollectionType.KNOWLEDGE_BASE.value == "knowledge_base"

    def test_embedding_provider_values(self):
        """Test EmbeddingProvider enum values."""
        assert EmbeddingProvider.OLLAMA.value == "ollama"
        assert EmbeddingProvider.OPENAI.value == "openai"
        assert EmbeddingProvider.HTTPX.value == "httpx"

    def test_index_type_values(self):
        """Test IndexType enum values."""
        assert IndexType.FLAT.value == "FLAT"
        assert IndexType.IVF_FLAT.value == "IVF_FLAT"
        assert IndexType.HNSW.value == "HNSW"

    def test_metric_type_values(self):
        """Test MetricType enum values."""
        assert MetricType.COSINE.value == "COSINE"
        assert MetricType.L2.value == "L2"
        assert MetricType.IP.value == "IP"

    def test_document_type_values(self):
        """Test DocumentType enum values."""
        assert DocumentType.TEXT.value == "text"
        assert DocumentType.FILE.value == "file"
        assert DocumentType.URL.value == "url"
        assert DocumentType.PDF.value == "pdf"

    def test_filter_operator_values(self):
        """Test FilterOperator enum values."""
        assert FilterOperator.EQUALS.value == "=="
        assert FilterOperator.IN.value == "in"
        assert FilterOperator.LIKE.value == "like"


class TestDocumentChunk:
    """Tests for DocumentChunk schema."""

    def test_document_chunk_creation(self):
        """Test creating a document chunk."""
        chunk = DocumentChunk(
            document_id="doc-123",
            project_id="proj-456",
            title="Test Document",
            content="This is test content.",
            chunk_index=0,
            total_chunks=1,
            metadata={"source": "test"},
        )

        assert chunk.document_id == "doc-123"
        assert chunk.project_id == "proj-456"
        assert chunk.title == "Test Document"
        assert chunk.chunk_index == 0
        assert chunk.metadata["source"] == "test"

    def test_document_chunk_default_metadata(self):
        """Test DocumentChunk with default metadata."""
        chunk = DocumentChunk(
            document_id="doc-1",
            project_id="proj-1",
            title="Doc",
            content="Content",
            chunk_index=0,
            total_chunks=1,
        )

        assert chunk.metadata == {}


class TestEmbeddingRequest:
    """Tests for EmbeddingRequest schema."""

    def test_embedding_request_creation(self):
        """Test creating an embedding request."""
        request = EmbeddingRequest(
            message_id=1,
            content="Hello, world!",
            conversation_id="conv-123",
            role="user",
            created_at=1234567890,
        )

        assert request.message_id == 1
        assert request.content == "Hello, world!"
        assert request.role == "user"
        assert request.should_embed is None

    def test_embedding_request_with_optional_fields(self):
        """Test EmbeddingRequest with all optional fields."""
        request = EmbeddingRequest(
            message_id=2,
            content="Test",
            conversation_id="conv-456",
            agent_id="agent-123",
            user_id="user-789",
            role="assistant",
            created_at=1234567890,
            should_embed=True,
        )

        assert request.agent_id == "agent-123"
        assert request.user_id == "user-789"
        assert request.should_embed is True


class TestEmbeddingResponse:
    """Tests for EmbeddingResponse schema."""

    def test_embedding_response_success(self):
        """Test successful embedding response."""
        response = EmbeddingResponse(
            message_id=1,
            embedded=True,
            reason="content worth embedding",
            processing_time_ms=45.5,
        )

        assert response.embedded is True
        assert response.processing_time_ms == 45.5

    def test_embedding_response_failure(self):
        """Test failed embedding response."""
        response = EmbeddingResponse(
            message_id=2,
            embedded=False,
            reason="content too short",
        )

        assert response.embedded is False
        assert response.reason == "content too short"


class TestBatchEmbedding:
    """Tests for batch embedding schemas."""

    def test_batch_embedding_request(self):
        """Test batch embedding request."""
        messages = [
            EmbeddingRequest(
                message_id=i,
                content=f"Message {i}",
                conversation_id="conv-1",
                role="user",
                created_at=1234567890,
            )
            for i in range(3)
        ]

        request = BatchEmbeddingRequest(messages=messages)
        assert len(request.messages) == 3

    def test_batch_embedding_response(self):
        """Test batch embedding response."""
        results = [
            EmbeddingResponse(message_id=i, embedded=True)
            for i in range(3)
        ]

        response = BatchEmbeddingResponse(
            results=results,
            total_processed=3,
            total_embedded=3,
            total_time_ms=150.0,
        )

        assert response.total_processed == 3
        assert response.total_embedded == 3


class TestKnowledgeEmbeddingRequest:
    """Tests for knowledge embedding request."""

    def test_knowledge_embedding_request(self):
        """Test knowledge embedding request creation."""
        request = KnowledgeEmbeddingRequest(
            project_id="proj-1",
            document_id="doc-1",
            title="Test Doc",
            content="Document content here.",
            document_type="text",
            metadata={"author": "test"},
        )

        assert request.project_id == "proj-1"
        assert request.document_type == "text"
        assert request.metadata["author"] == "test"


class TestSearchSchemas:
    """Tests for search-related schemas."""

    def test_search_request_defaults(self):
        """Test SearchRequest with defaults."""
        request = SearchRequest(query="test query")

        assert request.query == "test query"
        assert request.limit == 10
        assert request.score_threshold == 0.7

    def test_search_request_with_filters(self):
        """Test SearchRequest with filters."""
        request = SearchRequest(
            query="test",
            limit=5,
            conversation_id="conv-123",
            agent_id="agent-456",
            role_filter="user",
            score_threshold=0.8,
        )

        assert request.limit == 5
        assert request.conversation_id == "conv-123"
        assert request.role_filter == "user"

    def test_search_result(self):
        """Test SearchResult creation."""
        result = SearchResult(
            message_id=1,
            score=0.95,
            conversation_id="conv-1",
            role="user",
            created_at=1234567890,
            content_preview="Test content...",
        )

        assert result.score == 0.95
        assert result.content_preview == "Test content..."

    def test_search_response(self):
        """Test SearchResponse creation."""
        response = SearchResponse(
            query="test",
            results=[],
            total_found=0,
            processing_time_ms=25.0,
        )

        assert response.query == "test"
        assert response.total_found == 0


class TestKnowledgeSearchSchemas:
    """Tests for knowledge search schemas."""

    def test_knowledge_search_request(self):
        """Test KnowledgeSearchRequest creation."""
        request = KnowledgeSearchRequest(
            query="What is AI?",
            project_id="proj-1",
            limit=5,
            score_threshold=0.6,
            hybrid_search=True,
        )

        assert request.project_id == "proj-1"
        assert request.hybrid_search is True

    def test_knowledge_search_result(self):
        """Test KnowledgeSearchResult creation."""
        result = KnowledgeSearchResult(
            document_id="doc-1",
            chunk_id="0",
            score=0.85,
            project_id="proj-1",
            title="AI Introduction",
            document_type="text",
            chunk_content="Artificial intelligence is...",
            metadata={"chunk_index": 0},
            created_at=1234567890,
        )

        assert result.document_id == "doc-1"
        assert result.score == 0.85


class TestCollectionInfo:
    """Tests for CollectionInfo schema."""

    def test_collection_info(self):
        """Test CollectionInfo creation."""
        info = CollectionInfo(
            name="test_collection",
            collection_type="knowledge_base",
            num_entities=1000,
            is_loaded=True,
        )

        assert info.name == "test_collection"
        assert info.num_entities == 1000

    def test_collection_info_with_error(self):
        """Test CollectionInfo with error."""
        info = CollectionInfo(
            name="broken_collection",
            collection_type="unknown",
            error="Collection not found",
        )

        assert info.error == "Collection not found"


class TestEmbeddingResult:
    """Tests for EmbeddingResult schema."""

    def test_embedding_result(self):
        """Test EmbeddingResult creation."""
        result = EmbeddingResult(
            embedding=[0.1, 0.2, 0.3],
            model="mxbai-embed-large",
            processing_time_ms=50.0,
        )

        assert len(result.embedding) == 3
        assert result.model == "mxbai-embed-large"
