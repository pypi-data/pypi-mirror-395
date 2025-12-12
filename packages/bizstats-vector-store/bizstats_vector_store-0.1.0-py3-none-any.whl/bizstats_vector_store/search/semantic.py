"""
Semantic search implementation with hybrid search support.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import time
import json
import logging
from typing import Optional, Dict, Any, List

from bizstats_vector_store.config import get_config, VectorStoreConfig
from bizstats_vector_store.models.enums import CollectionType
from bizstats_vector_store.models.schemas import (
    SearchRequest,
    SearchResult,
    SearchResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResult,
    KnowledgeSearchResponse,
)
from bizstats_vector_store.embedding.service import EmbeddingGenerator
from bizstats_vector_store.milvus.collections import CollectionManager

logger = logging.getLogger(__name__)


class SemanticSearchError(Exception):
    """Error during semantic search."""

    pass


class SemanticSearch:
    """
    Semantic search with hybrid search capability.

    Combines:
    - Vector similarity search
    - Keyword-based filtering
    - Score boosting based on keyword overlap
    """

    def __init__(
        self,
        collection_manager: Optional[CollectionManager] = None,
        embedding_generator: Optional[EmbeddingGenerator] = None,
        config: Optional[VectorStoreConfig] = None,
    ):
        """
        Initialize semantic search.

        Args:
            collection_manager: Collection manager instance
            embedding_generator: Embedding generator instance
            config: Vector store configuration
        """
        self.config = config or get_config()
        self.collection_manager = collection_manager or CollectionManager()
        self.embedding_generator = embedding_generator or EmbeddingGenerator()

    async def search_chat_messages(self, request: SearchRequest) -> SearchResponse:
        """
        Search chat messages using semantic similarity.

        Args:
            request: Search request parameters

        Returns:
            SearchResponse with results
        """
        start_time = time.time()

        try:
            # Generate query embedding
            embedding_result = await self.embedding_generator.generate(request.query)
            query_embedding = embedding_result.embedding

            # Build filter expression
            expressions = []
            if request.conversation_id:
                expressions.append(f'conversation_id == "{request.conversation_id}"')
            if request.agent_id:
                expressions.append(f'agent_id == "{request.agent_id}"')
            if request.user_id:
                expressions.append(f'user_id == "{request.user_id}"')
            if request.role_filter:
                expressions.append(f'role == "{request.role_filter}"')

            search_expr = " && ".join(expressions) if expressions else None

            # Get collection
            collection = await self.collection_manager.ensure_collection(
                CollectionType.CHAT_MESSAGES
            )

            # Search parameters
            search_params = {
                "metric_type": "COSINE",
                "params": {"nprobe": self.config.search_nprobe},
            }

            # Perform search
            results = collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=request.limit,
                expr=search_expr,
                output_fields=[
                    "conversation_id",
                    "agent_id",
                    "user_id",
                    "created_at",
                    "role",
                    "content_preview",
                ],
            )

            # Process results
            search_results = []
            for hit in results[0]:
                if hit.score >= request.score_threshold:
                    search_results.append(
                        SearchResult(
                            message_id=hit.id,
                            score=float(hit.score),
                            conversation_id=hit.entity.get("conversation_id"),
                            agent_id=hit.entity.get("agent_id") or None,
                            user_id=hit.entity.get("user_id") or None,
                            role=hit.entity.get("role"),
                            created_at=hit.entity.get("created_at"),
                            content_preview=hit.entity.get("content_preview"),
                        )
                    )

            processing_time = (time.time() - start_time) * 1000

            return SearchResponse(
                query=request.query,
                results=search_results,
                total_found=len(search_results),
                processing_time_ms=processing_time,
            )

        except Exception as e:
            logger.error(f"Chat message search failed: {e}")
            raise SemanticSearchError(f"Search failed: {e}")

    async def search_knowledge_base(
        self,
        request: KnowledgeSearchRequest,
    ) -> KnowledgeSearchResponse:
        """
        Search knowledge base with hybrid search capability.

        Args:
            request: Knowledge search request parameters

        Returns:
            KnowledgeSearchResponse with results
        """
        start_time = time.time()

        logger.info(
            f"Searching knowledge base for project {request.project_id}: '{request.query}'"
        )

        try:
            # Generate query embedding
            embedding_result = await self.embedding_generator.generate(request.query)
            query_embedding = embedding_result.embedding

            # Build filter expression
            expressions = [f'project_id == "{request.project_id}"']
            if request.document_type_filter:
                expressions.append(f'document_type == "{request.document_type_filter}"')

            search_expr = " && ".join(expressions)

            # Get collection
            collection = await self.collection_manager.ensure_collection(
                CollectionType.KNOWLEDGE_BASE,
                project_id=request.project_id,
            )

            # Ensure collection is loaded
            collection.load()

            # Search parameters
            search_params = {
                "metric_type": "COSINE",
                "params": {"nprobe": self.config.search_nprobe},
            }

            # Perform semantic search (get more for hybrid)
            limit = request.limit * 2 if request.hybrid_search else request.limit
            results = collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=limit,
                expr=search_expr,
                output_fields=[
                    "document_id",
                    "chunk_index",
                    "document_title",
                    "document_type",
                    "content_preview",
                    "metadata_json",
                    "created_at",
                ],
            )

            # Process results
            search_results = []
            for hit in results[0]:
                if hit.score >= request.score_threshold:
                    try:
                        metadata = json.loads(hit.entity.get("metadata_json", "{}"))
                    except (json.JSONDecodeError, TypeError):
                        metadata = {}

                    result = KnowledgeSearchResult(
                        document_id=hit.entity.get("document_id"),
                        chunk_id=str(hit.entity.get("chunk_index", 0)),
                        score=float(hit.score),
                        project_id=request.project_id,
                        title=hit.entity.get("document_title"),
                        document_type=hit.entity.get("document_type"),
                        chunk_content=hit.entity.get("content_preview"),
                        metadata=metadata,
                        created_at=hit.entity.get("created_at"),
                    )
                    search_results.append(result)

            # Apply hybrid search boosting
            if request.hybrid_search and search_results:
                search_results = self._apply_keyword_boost(
                    request.query, search_results
                )

            # Limit final results
            search_results = search_results[: request.limit]

            processing_time = (time.time() - start_time) * 1000

            logger.info(
                f"Knowledge search completed in {processing_time:.2f}ms, "
                f"found {len(search_results)} results"
            )

            return KnowledgeSearchResponse(
                query=request.query,
                results=search_results,
                total_found=len(search_results),
                processing_time_ms=processing_time,
                hybrid_search_used=request.hybrid_search,
            )

        except Exception as e:
            logger.error(f"Knowledge base search failed: {e}")
            raise SemanticSearchError(f"Search failed: {e}")

    def _apply_keyword_boost(
        self,
        query: str,
        results: List[KnowledgeSearchResult],
    ) -> List[KnowledgeSearchResult]:
        """
        Apply keyword-based score boosting to results.

        Args:
            query: Original search query
            results: Search results to boost

        Returns:
            Results with boosted scores, re-sorted
        """
        query_keywords = set(query.lower().split())

        for result in results:
            content_keywords = set(result.chunk_content.lower().split())
            keyword_overlap = len(query_keywords.intersection(content_keywords))

            # Boost score based on keyword overlap
            keyword_boost = min(0.2, keyword_overlap * 0.05)
            result.score = min(1.0, result.score + keyword_boost)

        # Re-sort by boosted scores
        results.sort(key=lambda x: x.score, reverse=True)

        return results


# Module-level convenience functions

_search: Optional[SemanticSearch] = None


def get_semantic_search() -> SemanticSearch:
    """Get the default semantic search instance."""
    global _search
    if _search is None:
        _search = SemanticSearch()
    return _search


async def search_chat(request: SearchRequest) -> SearchResponse:
    """Search chat messages using the default search instance."""
    return await get_semantic_search().search_chat_messages(request)


async def search_knowledge(request: KnowledgeSearchRequest) -> KnowledgeSearchResponse:
    """Search knowledge base using the default search instance."""
    return await get_semantic_search().search_knowledge_base(request)
