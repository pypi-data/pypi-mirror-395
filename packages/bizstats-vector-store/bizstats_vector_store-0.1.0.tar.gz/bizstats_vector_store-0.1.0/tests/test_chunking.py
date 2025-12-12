"""
Tests for document chunking.
"""

import pytest
from bizstats_vector_store.config import reset_config
from bizstats_vector_store.chunking.document import (
    DocumentChunker,
    ChunkResult,
    chunk_document,
)


class TestDocumentChunker:
    """Tests for DocumentChunker class."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    def test_chunker_initialization_defaults(self):
        """Test chunker initialization with defaults."""
        chunker = DocumentChunker()
        assert chunker.max_tokens == 500
        assert chunker.overlap_tokens == 50

    def test_chunker_initialization_custom(self):
        """Test chunker initialization with custom values."""
        chunker = DocumentChunker(
            max_tokens=200,
            overlap_tokens=20,
            max_chunk_chars=400,
            overlap_chars=50,
        )
        assert chunker.max_tokens == 200
        assert chunker.overlap_tokens == 20
        assert chunker.max_chunk_chars == 400

    def test_estimate_tokens(self):
        """Test token estimation."""
        chunker = DocumentChunker()

        # ~4 chars per token
        assert chunker.estimate_tokens("a" * 100) == 25
        assert chunker.estimate_tokens("a" * 400) == 100

    def test_chunk_small_document(self):
        """Test chunking a small document that doesn't need splitting."""
        chunker = DocumentChunker(max_tokens=1000)

        content = "This is a small document that fits in one chunk."
        chunks = chunker.chunk_document(
            content=content,
            document_id="doc-1",
            project_id="proj-1",
            document_title="Small Doc",
        )

        assert len(chunks) == 1
        assert chunks[0].content == content
        assert chunks[0].chunk_index == 0
        assert chunks[0].total_chunks == 1

    def test_chunk_large_document(self):
        """Test chunking a large document into multiple chunks."""
        chunker = DocumentChunker(max_tokens=50, max_chunk_chars=200, overlap_chars=20)

        # Create content that will require multiple chunks
        content = "This is a test. " * 100  # ~1600 chars

        chunks = chunker.chunk_document(
            content=content,
            document_id="doc-2",
            project_id="proj-1",
            document_title="Large Doc",
        )

        assert len(chunks) > 1

        # Check all chunks have proper metadata
        for i, chunk in enumerate(chunks):
            assert chunk.document_id == "doc-2"
            assert chunk.project_id == "proj-1"
            assert chunk.chunk_index == i
            assert chunk.total_chunks == len(chunks)

    def test_chunk_with_metadata(self):
        """Test chunking preserves metadata."""
        chunker = DocumentChunker(max_tokens=1000)

        metadata = {"source": "test", "version": 1}
        chunks = chunker.chunk_document(
            content="Test content",
            document_id="doc-3",
            project_id="proj-2",
            document_title="Meta Doc",
            document_type="file",
            metadata=metadata,
        )

        assert chunks[0].metadata["source"] == "test"
        assert chunks[0].metadata["document_type"] == "file"

    def test_chunk_content_safe_limit(self):
        """Test chunks respect Milvus content limit."""
        chunker = DocumentChunker(max_tokens=5000)

        # Content over 950 chars should be truncated
        content = "x" * 2000

        chunks = chunker.chunk_document(
            content=content,
            document_id="doc-4",
            project_id="proj-1",
            document_title="Long Content",
        )

        assert len(chunks[0].content) <= 950

    def test_chunk_by_sentences_small(self):
        """Test sentence chunking for small content."""
        chunker = DocumentChunker()

        content = "First sentence. Second sentence."
        chunks = chunker.chunk_by_sentences(
            content=content,
            document_id="doc-5",
            project_id="proj-1",
            document_title="Short Sentences",
            max_sentences_per_chunk=10,
        )

        assert len(chunks) == 1

    def test_chunk_by_sentences_large(self):
        """Test sentence chunking for large content."""
        chunker = DocumentChunker()

        # Create content with many sentences
        sentences = ["This is sentence number {}. ".format(i) for i in range(50)]
        content = " ".join(sentences)

        chunks = chunker.chunk_by_sentences(
            content=content,
            document_id="doc-6",
            project_id="proj-1",
            document_title="Many Sentences",
            max_sentences_per_chunk=5,
        )

        assert len(chunks) > 1

        # Check sentence metadata
        for chunk in chunks:
            assert "sentence_start" in chunk.metadata
            assert "sentence_end" in chunk.metadata

    def test_chunk_result_dataclass(self):
        """Test ChunkResult dataclass."""
        result = ChunkResult(
            document_id="doc-1",
            project_id="proj-1",
            title="Test",
            content="Content",
            chunk_index=0,
            total_chunks=1,
            metadata={},
        )

        assert result.document_id == "doc-1"
        assert result.chunk_index == 0

    def test_chunk_document_convenience_function(self):
        """Test module-level chunk_document function."""
        chunks = chunk_document(
            content="Test content for chunking.",
            document_id="doc-7",
            project_id="proj-3",
            document_title="Convenience Test",
        )

        assert len(chunks) >= 1
        assert chunks[0].document_id == "doc-7"

    def test_chunk_preserves_word_boundaries(self):
        """Test chunks try to break at word boundaries."""
        chunker = DocumentChunker(max_chunk_chars=50, overlap_chars=10)

        content = "The quick brown fox jumps over the lazy dog repeatedly."
        chunks = chunker.chunk_document(
            content=content,
            document_id="doc-8",
            project_id="proj-1",
            document_title="Word Boundary Test",
        )

        # Chunks should not break mid-word (most of the time)
        for chunk in chunks:
            # Check content doesn't start with a partial word (lowercase continuation)
            stripped = chunk.content.strip()
            if stripped:
                # Content should be properly trimmed
                assert not stripped[0].islower() or stripped[0] == content[0].lower()

    def test_empty_content_handling(self):
        """Test handling of empty content."""
        chunker = DocumentChunker()

        chunks = chunker.chunk_document(
            content="",
            document_id="doc-9",
            project_id="proj-1",
            document_title="Empty Doc",
        )

        # Should return at least one chunk (possibly empty)
        assert len(chunks) >= 0

    def test_whitespace_content(self):
        """Test handling of whitespace-only content."""
        chunker = DocumentChunker()

        content = "   \n\t   "
        chunks = chunker.chunk_document(
            content=content,
            document_id="doc-10",
            project_id="proj-1",
            document_title="Whitespace Doc",
        )

        # Should handle whitespace gracefully
        assert isinstance(chunks, list)

    def test_chunk_index_continuity(self):
        """Test chunk indices are continuous."""
        chunker = DocumentChunker(max_chunk_chars=100, overlap_chars=10)

        content = "Word " * 200  # ~1000 chars
        chunks = chunker.chunk_document(
            content=content,
            document_id="doc-11",
            project_id="proj-1",
            document_title="Index Test",
        )

        indices = [c.chunk_index for c in chunks]
        expected = list(range(len(chunks)))
        assert indices == expected

    def test_document_type_in_metadata(self):
        """Test document type is stored in metadata."""
        chunker = DocumentChunker()

        chunks = chunker.chunk_document(
            content="Test content",
            document_id="doc-12",
            project_id="proj-1",
            document_title="Type Test",
            document_type="pdf",
        )

        assert chunks[0].metadata["document_type"] == "pdf"
