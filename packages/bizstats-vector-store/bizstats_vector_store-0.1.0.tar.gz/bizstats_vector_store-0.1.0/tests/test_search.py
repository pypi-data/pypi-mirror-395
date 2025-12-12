"""
Tests for semantic search.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from bizstats_vector_store.config import reset_config
from bizstats_vector_store.models.schemas import (
    SearchRequest,
    SearchResult,
    KnowledgeSearchRequest,
    KnowledgeSearchResult,
)
from bizstats_vector_store.embedding.service import EmbeddingResult
from bizstats_vector_store.search.semantic import (
    SemanticSearch,
    SemanticSearchError,
    get_semantic_search,
    search_chat,
    search_knowledge,
)


class TestSemanticSearch:
    """Tests for SemanticSearch class."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    def test_search_initialization(self):
        """Test search initialization."""
        mock_collection_mgr = Mock()
        mock_embedding_gen = Mock()

        search = SemanticSearch(
            collection_manager=mock_collection_mgr,
            embedding_generator=mock_embedding_gen,
        )

        assert search.collection_manager is mock_collection_mgr
        assert search.embedding_generator is mock_embedding_gen

    @pytest.mark.asyncio
    async def test_search_chat_messages_basic(self):
        """Test basic chat message search."""
        mock_collection_mgr = Mock()
        mock_embedding_gen = Mock()

        search = SemanticSearch(
            collection_manager=mock_collection_mgr,
            embedding_generator=mock_embedding_gen,
        )

        # Mock embedding generation
        mock_embedding_gen.generate = AsyncMock(
            return_value=EmbeddingResult(
                embedding=[0.1] * 1024,
                model="test",
                processing_time_ms=10,
            )
        )

        # Mock collection with proper entity.get method
        mock_collection = Mock()

        class MockEntity:
            def __init__(self, data):
                self._data = data

            def get(self, key):
                return self._data.get(key)

        mock_result = Mock()
        mock_result.id = 1
        mock_result.score = 0.9
        mock_result.entity = MockEntity({
            "conversation_id": "conv-1",
            "agent_id": "agent-1",
            "user_id": "user-1",
            "role": "user",
            "created_at": 1234567890,
            "content_preview": "Test content",
        })

        mock_collection.search.return_value = [[mock_result]]
        mock_collection_mgr.ensure_collection = AsyncMock(return_value=mock_collection)

        request = SearchRequest(query="test query", limit=5)
        response = await search.search_chat_messages(request)

        assert response.query == "test query"
        assert len(response.results) == 1
        assert response.results[0].score == 0.9

    @pytest.mark.asyncio
    async def test_search_chat_messages_with_filters(self):
        """Test chat search with filters."""
        mock_collection_mgr = Mock()
        mock_embedding_gen = Mock()

        search = SemanticSearch(
            collection_manager=mock_collection_mgr,
            embedding_generator=mock_embedding_gen,
        )

        mock_embedding_gen.generate = AsyncMock(
            return_value=EmbeddingResult(
                embedding=[0.1] * 1024,
                model="test",
                processing_time_ms=10,
            )
        )

        mock_collection = Mock()
        mock_collection.search.return_value = [[]]
        mock_collection_mgr.ensure_collection = AsyncMock(return_value=mock_collection)

        request = SearchRequest(
            query="test",
            conversation_id="conv-123",
            agent_id="agent-456",
            role_filter="user",
        )
        await search.search_chat_messages(request)

        # Verify search was called with filter expression
        call_args = mock_collection.search.call_args
        assert call_args.kwargs["expr"] is not None

    @pytest.mark.asyncio
    async def test_search_chat_messages_score_threshold(self):
        """Test chat search filters by score threshold."""
        mock_collection_mgr = Mock()
        mock_embedding_gen = Mock()

        search = SemanticSearch(
            collection_manager=mock_collection_mgr,
            embedding_generator=mock_embedding_gen,
        )

        mock_embedding_gen.generate = AsyncMock(
            return_value=EmbeddingResult(
                embedding=[0.1] * 1024,
                model="test",
                processing_time_ms=10,
            )
        )

        # Create results with varying scores
        class MockEntity:
            def __init__(self, data):
                self._data = data

            def get(self, key):
                return self._data.get(key)

        mock_high_score = Mock()
        mock_high_score.id = 1
        mock_high_score.score = 0.9
        mock_high_score.entity = MockEntity({
            "conversation_id": "c1",
            "role": "user",
            "created_at": 123,
            "content_preview": "t"
        })

        mock_low_score = Mock()
        mock_low_score.id = 2
        mock_low_score.score = 0.5  # Below threshold

        mock_collection = Mock()
        mock_collection.search.return_value = [[mock_high_score, mock_low_score]]
        mock_collection_mgr.ensure_collection = AsyncMock(return_value=mock_collection)

        request = SearchRequest(query="test", score_threshold=0.7)
        response = await search.search_chat_messages(request)

        # Only high score result should be included
        assert len(response.results) == 1

    @pytest.mark.asyncio
    async def test_search_knowledge_base_basic(self):
        """Test basic knowledge base search."""
        mock_collection_mgr = Mock()
        mock_embedding_gen = Mock()

        search = SemanticSearch(
            collection_manager=mock_collection_mgr,
            embedding_generator=mock_embedding_gen,
        )

        mock_embedding_gen.generate = AsyncMock(
            return_value=EmbeddingResult(
                embedding=[0.1] * 1024,
                model="test",
                processing_time_ms=10,
            )
        )

        class MockEntity:
            def __init__(self, data):
                self._data = data

            def get(self, key, default=None):
                return self._data.get(key, default)

        mock_result = Mock()
        mock_result.score = 0.85
        mock_result.entity = MockEntity({
            "document_id": "doc-1",
            "chunk_index": 0,
            "document_title": "Test Doc",
            "document_type": "text",
            "content_preview": "Test content",
            "metadata_json": '{"key": "value"}',
            "created_at": 1234567890,
        })

        mock_collection = Mock()
        mock_collection.search.return_value = [[mock_result]]
        mock_collection.load = Mock()
        mock_collection_mgr.ensure_collection = AsyncMock(return_value=mock_collection)

        request = KnowledgeSearchRequest(
            query="test query",
            project_id="proj-1",
            hybrid_search=False,
        )
        response = await search.search_knowledge_base(request)

        assert response.query == "test query"
        assert len(response.results) == 1
        assert response.results[0].document_id == "doc-1"

    @pytest.mark.asyncio
    async def test_search_knowledge_base_hybrid(self):
        """Test knowledge base search with hybrid boosting."""
        mock_collection_mgr = Mock()
        mock_embedding_gen = Mock()

        search = SemanticSearch(
            collection_manager=mock_collection_mgr,
            embedding_generator=mock_embedding_gen,
        )

        mock_embedding_gen.generate = AsyncMock(
            return_value=EmbeddingResult(
                embedding=[0.1] * 1024,
                model="test",
                processing_time_ms=10,
            )
        )

        class MockEntity:
            def __init__(self, data):
                self._data = data

            def get(self, key, default=None):
                return self._data.get(key, default)

        # Create two results, one with keyword overlap
        mock_result1 = Mock()
        mock_result1.score = 0.7
        mock_result1.entity = MockEntity({
            "document_id": "doc-1",
            "chunk_index": 0,
            "document_title": "Doc 1",
            "document_type": "text",
            "content_preview": "This contains test keyword",  # Has "test"
            "metadata_json": "{}",
            "created_at": 123,
        })

        mock_result2 = Mock()
        mock_result2.score = 0.75
        mock_result2.entity = MockEntity({
            "document_id": "doc-2",
            "chunk_index": 0,
            "document_title": "Doc 2",
            "document_type": "text",
            "content_preview": "No matching words here",  # No "test"
            "metadata_json": "{}",
            "created_at": 124,
        })

        mock_collection = Mock()
        mock_collection.search.return_value = [[mock_result2, mock_result1]]
        mock_collection.load = Mock()
        mock_collection_mgr.ensure_collection = AsyncMock(return_value=mock_collection)

        request = KnowledgeSearchRequest(
            query="test",
            project_id="proj-1",
            hybrid_search=True,
        )
        response = await search.search_knowledge_base(request)

        # Result with keyword overlap should be boosted
        assert response.hybrid_search_used is True

    @pytest.mark.asyncio
    async def test_search_error_handling(self):
        """Test search error handling."""
        mock_collection_mgr = Mock()
        mock_embedding_gen = Mock()

        search = SemanticSearch(
            collection_manager=mock_collection_mgr,
            embedding_generator=mock_embedding_gen,
        )

        mock_embedding_gen.generate = AsyncMock(side_effect=Exception("Embedding error"))

        request = SearchRequest(query="test")

        with pytest.raises(SemanticSearchError) as exc_info:
            await search.search_chat_messages(request)

        assert "Search failed" in str(exc_info.value)

    def test_apply_keyword_boost(self):
        """Test keyword boost application."""
        search = SemanticSearch(
            collection_manager=Mock(),
            embedding_generator=Mock(),
        )

        results = [
            KnowledgeSearchResult(
                document_id="doc-1",
                chunk_id="0",
                score=0.7,
                project_id="proj-1",
                title="Doc 1",
                document_type="text",
                chunk_content="machine learning algorithms",
                metadata={},
                created_at=123,
            ),
            KnowledgeSearchResult(
                document_id="doc-2",
                chunk_id="0",
                score=0.75,
                project_id="proj-1",
                title="Doc 2",
                document_type="text",
                chunk_content="different content here",
                metadata={},
                created_at=124,
            ),
        ]

        boosted = search._apply_keyword_boost("machine learning", results)

        # First result should be boosted and potentially reordered
        assert len(boosted) == 2

    def test_apply_keyword_boost_caps_at_one(self):
        """Test keyword boost doesn't exceed 1.0."""
        search = SemanticSearch(
            collection_manager=Mock(),
            embedding_generator=Mock(),
        )

        results = [
            KnowledgeSearchResult(
                document_id="doc-1",
                chunk_id="0",
                score=0.95,  # High initial score
                project_id="proj-1",
                title="Doc 1",
                document_type="text",
                chunk_content="test test test test",  # Multiple keyword matches
                metadata={},
                created_at=123,
            ),
        ]

        boosted = search._apply_keyword_boost("test", results)

        assert boosted[0].score <= 1.0


class TestModuleFunctions:
    """Tests for module-level convenience functions."""

    def setup_method(self):
        """Reset before each test."""
        reset_config()

    def test_get_semantic_search_singleton(self):
        """Test get_semantic_search returns singleton."""
        import bizstats_vector_store.search.semantic as search_module
        search_module._search = None

        search1 = get_semantic_search()
        search2 = get_semantic_search()

        assert search1 is search2

    @pytest.mark.asyncio
    async def test_search_chat_function(self):
        """Test module-level search_chat function."""
        with patch(
            "bizstats_vector_store.search.semantic.get_semantic_search"
        ) as mock_get:
            mock_search = AsyncMock()
            mock_search.search_chat_messages.return_value = Mock()
            mock_get.return_value = mock_search

            request = SearchRequest(query="test")
            await search_chat(request)

            mock_search.search_chat_messages.assert_called_once_with(request)

    @pytest.mark.asyncio
    async def test_search_knowledge_function(self):
        """Test module-level search_knowledge function."""
        with patch(
            "bizstats_vector_store.search.semantic.get_semantic_search"
        ) as mock_get:
            mock_search = AsyncMock()
            mock_search.search_knowledge_base.return_value = Mock()
            mock_get.return_value = mock_search

            request = KnowledgeSearchRequest(query="test", project_id="proj-1")
            await search_knowledge(request)

            mock_search.search_knowledge_base.assert_called_once_with(request)
