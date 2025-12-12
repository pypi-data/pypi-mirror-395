"""
Document chunking utilities for large documents.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from bizstats_vector_store.config import get_config


@dataclass
class ChunkResult:
    """Result of document chunking."""

    document_id: str
    project_id: str
    title: str
    content: str
    chunk_index: int
    total_chunks: int
    metadata: Dict[str, Any]


class DocumentChunker:
    """
    Document chunking utility for large documents.

    Splits documents into smaller chunks suitable for embedding
    while maintaining context through overlapping segments.
    """

    def __init__(
        self,
        max_tokens: Optional[int] = None,
        overlap_tokens: Optional[int] = None,
        max_chunk_chars: int = 800,
        overlap_chars: int = 100,
    ):
        """
        Initialize the document chunker.

        Args:
            max_tokens: Maximum tokens per chunk (uses config default if not provided)
            overlap_tokens: Overlap tokens between chunks (uses config default if not provided)
            max_chunk_chars: Maximum characters per chunk (for character-based chunking)
            overlap_chars: Overlap characters between chunks
        """
        config = get_config()
        self.max_tokens = max_tokens or config.chunk_max_tokens
        self.overlap_tokens = overlap_tokens or config.chunk_overlap_tokens
        self.max_chunk_chars = max_chunk_chars
        self.overlap_chars = overlap_chars

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        Uses a rough approximation of ~4 characters per token.

        Args:
            text: Input text

        Returns:
            Estimated token count
        """
        return len(text) // 4

    def chunk_document(
        self,
        content: str,
        document_id: str,
        project_id: str,
        document_title: str,
        document_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[ChunkResult]:
        """
        Chunk a document into smaller pieces for embedding.

        Args:
            content: Document content
            document_id: Unique document identifier
            project_id: Project identifier
            document_title: Title of the document
            document_type: Type of document (text, file, url)
            metadata: Additional metadata

        Returns:
            List of document chunks
        """
        if metadata is None:
            metadata = {}

        chunks = []
        estimated_tokens = self.estimate_tokens(content)

        if estimated_tokens <= self.max_tokens:
            # Document is small enough, don't chunk
            # Ensure content is under safe limit for Milvus
            safe_content = content[:950] if len(content) > 950 else content
            chunk_metadata = {
                **metadata,
                "chunk_index": 0,
                "total_chunks": 1,
                "document_type": document_type,
            }
            chunks.append(
                ChunkResult(
                    document_id=document_id,
                    project_id=project_id,
                    title=document_title,
                    content=safe_content,
                    chunk_index=0,
                    total_chunks=1,
                    metadata=chunk_metadata,
                )
            )
        else:
            # Split into chunks using character-based approach
            chunks = self._chunk_by_characters(
                content=content,
                document_id=document_id,
                project_id=project_id,
                document_title=document_title,
                document_type=document_type,
                metadata=metadata,
            )

        return chunks

    def _chunk_by_characters(
        self,
        content: str,
        document_id: str,
        project_id: str,
        document_title: str,
        document_type: str,
        metadata: Dict[str, Any],
    ) -> List[ChunkResult]:
        """
        Chunk content by character count with overlap.

        Args:
            content: Document content
            document_id: Document identifier
            project_id: Project identifier
            document_title: Document title
            document_type: Document type
            metadata: Additional metadata

        Returns:
            List of chunks
        """
        chunks = []
        chunk_index = 0
        start = 0

        while start < len(content):
            # Calculate end position
            end = min(start + self.max_chunk_chars, len(content))

            # If not at the end, try to break at word boundary
            if end < len(content):
                last_space = content.rfind(" ", start, end)
                if last_space > start + self.max_chunk_chars - 200:
                    end = last_space

            chunk_content = content[start:end].strip()

            if chunk_content:
                chunk_metadata = {
                    **metadata,
                    "chunk_index": chunk_index,
                    "total_chunks": -1,  # Will be updated after processing
                    "chunk_start_char": start,
                    "chunk_end_char": end,
                    "document_type": document_type,
                }

                chunks.append(
                    ChunkResult(
                        document_id=document_id,
                        project_id=project_id,
                        title=document_title,
                        content=chunk_content,
                        chunk_index=chunk_index,
                        total_chunks=-1,
                        metadata=chunk_metadata,
                    )
                )
                chunk_index += 1

            # Move start position with overlap
            start = max(start + self.max_chunk_chars - self.overlap_chars, end)

        # Update total_chunks count
        total = len(chunks)
        for chunk in chunks:
            chunk.total_chunks = total
            chunk.metadata["total_chunks"] = total

        return chunks

    def chunk_by_sentences(
        self,
        content: str,
        document_id: str,
        project_id: str,
        document_title: str,
        document_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
        max_sentences_per_chunk: int = 5,
    ) -> List[ChunkResult]:
        """
        Chunk document by sentences.

        Args:
            content: Document content
            document_id: Document identifier
            project_id: Project identifier
            document_title: Document title
            document_type: Document type
            metadata: Additional metadata
            max_sentences_per_chunk: Maximum sentences per chunk

        Returns:
            List of chunks
        """
        import re

        if metadata is None:
            metadata = {}

        # Simple sentence splitting (handles . ! ? followed by space or end)
        sentences = re.split(r"(?<=[.!?])\s+", content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= max_sentences_per_chunk:
            # Small enough, return as single chunk
            chunk_metadata = {
                **metadata,
                "chunk_index": 0,
                "total_chunks": 1,
                "document_type": document_type,
            }
            return [
                ChunkResult(
                    document_id=document_id,
                    project_id=project_id,
                    title=document_title,
                    content=content[:950],
                    chunk_index=0,
                    total_chunks=1,
                    metadata=chunk_metadata,
                )
            ]

        chunks = []
        chunk_index = 0
        overlap_sentences = max(1, max_sentences_per_chunk // 5)

        i = 0
        while i < len(sentences):
            chunk_sentences = sentences[i : i + max_sentences_per_chunk]
            chunk_content = " ".join(chunk_sentences)

            # Ensure safe content length
            if len(chunk_content) > 950:
                chunk_content = chunk_content[:950]

            chunk_metadata = {
                **metadata,
                "chunk_index": chunk_index,
                "total_chunks": -1,
                "sentence_start": i,
                "sentence_end": min(i + max_sentences_per_chunk, len(sentences)),
                "document_type": document_type,
            }

            chunks.append(
                ChunkResult(
                    document_id=document_id,
                    project_id=project_id,
                    title=document_title,
                    content=chunk_content,
                    chunk_index=chunk_index,
                    total_chunks=-1,
                    metadata=chunk_metadata,
                )
            )
            chunk_index += 1
            i += max_sentences_per_chunk - overlap_sentences

        # Update total_chunks
        total = len(chunks)
        for chunk in chunks:
            chunk.total_chunks = total
            chunk.metadata["total_chunks"] = total

        return chunks


# Module-level convenience functions

_chunker: Optional[DocumentChunker] = None


def _get_chunker() -> DocumentChunker:
    """Get the default chunker instance."""
    global _chunker
    if _chunker is None:
        _chunker = DocumentChunker()
    return _chunker


def chunk_document(
    content: str,
    document_id: str,
    project_id: str,
    document_title: str,
    document_type: str = "text",
    metadata: Optional[Dict[str, Any]] = None,
) -> List[ChunkResult]:
    """
    Chunk a document using the default chunker.

    Args:
        content: Document content
        document_id: Document identifier
        project_id: Project identifier
        document_title: Document title
        document_type: Document type
        metadata: Additional metadata

    Returns:
        List of document chunks
    """
    return _get_chunker().chunk_document(
        content=content,
        document_id=document_id,
        project_id=project_id,
        document_title=document_title,
        document_type=document_type,
        metadata=metadata,
    )
