"""
Embedding generation service with multiple provider support.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import time
import hashlib
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import httpx

from bizstats_vector_store.config import get_config, VectorStoreConfig
from bizstats_vector_store.models.enums import EmbeddingProvider

logger = logging.getLogger(__name__)


@dataclass
class EmbeddingResult:
    """Result of an embedding operation."""

    embedding: List[float]
    model: str
    processing_time_ms: float


class EmbeddingGeneratorError(Exception):
    """Error during embedding generation."""

    pass


class EmbeddingGenerator:
    """
    Embedding generation service supporting multiple providers.

    Supports:
    - Ollama (local or remote)
    - OpenAI
    - Custom HTTP endpoints
    """

    def __init__(
        self,
        config: Optional[VectorStoreConfig] = None,
        provider: Optional[str] = None,
    ):
        """
        Initialize the embedding generator.

        Args:
            config: Vector store configuration (uses global config if not provided)
            provider: Override the default provider from config
        """
        self.config = config or get_config()
        self.provider = EmbeddingProvider(provider or self.config.embedding_provider)
        self.model = self.config.embedding_model
        self.dimension = self.config.embedding_dimension

        # Ollama client (initialized lazily)
        self._ollama_client = None

        # OpenAI client (initialized lazily)
        self._openai_client = None

        # HTTP client for generic endpoints
        self._http_client: Optional[httpx.AsyncClient] = None

        # Redis cache (initialized lazily)
        self._redis_client = None
        self._cache_enabled = self.config.enable_cache and self.config.redis_url

    @property
    def ollama_client(self):
        """Lazily initialize Ollama client."""
        if self._ollama_client is None:
            try:
                from ollama import Client

                client_kwargs = {"host": self.config.ollama_base_url}
                if self.config.ollama_api_key:
                    client_kwargs["headers"] = {
                        "Authorization": f"Bearer {self.config.ollama_api_key}"
                    }
                self._ollama_client = Client(**client_kwargs)
            except ImportError:
                raise EmbeddingGeneratorError(
                    "ollama package not installed. Install with: pip install bizstats-vector-store[ollama]"
                )
        return self._ollama_client

    @property
    def openai_client(self):
        """Lazily initialize OpenAI client."""
        if self._openai_client is None:
            try:
                from openai import OpenAI

                if not self.config.openai_api_key:
                    raise EmbeddingGeneratorError(
                        "OpenAI API key not configured. Set VECTOR_STORE_OPENAI_API_KEY"
                    )
                self._openai_client = OpenAI(api_key=self.config.openai_api_key)
            except ImportError:
                raise EmbeddingGeneratorError(
                    "openai package not installed. Install with: pip install bizstats-vector-store[openai]"
                )
        return self._openai_client

    async def _get_http_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(timeout=30.0)
        return self._http_client

    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text."""
        text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
        return f"embed:{self.provider.value}:{self.model}:{text_hash}"

    async def _get_from_cache(self, text: str) -> Optional[List[float]]:
        """Get embedding from cache if available."""
        if not self._cache_enabled:
            return None

        try:
            if self._redis_client is None:
                import redis.asyncio as redis

                self._redis_client = redis.from_url(self.config.redis_url)

            key = self._get_cache_key(text)
            cached = await self._redis_client.get(key)
            if cached:
                import json

                return json.loads(cached)
        except Exception as e:
            logger.warning(f"Cache read error: {e}")
        return None

    async def _set_cache(self, text: str, embedding: List[float]) -> None:
        """Store embedding in cache."""
        if not self._cache_enabled:
            return

        try:
            if self._redis_client is None:
                import redis.asyncio as redis

                self._redis_client = redis.from_url(self.config.redis_url)

            import json

            key = self._get_cache_key(text)
            await self._redis_client.setex(
                key, self.config.cache_ttl_seconds, json.dumps(embedding)
            )
        except Exception as e:
            logger.warning(f"Cache write error: {e}")

    async def generate(self, text: str) -> EmbeddingResult:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            EmbeddingResult with embedding vector
        """
        start_time = time.time()

        # Check cache first
        cached = await self._get_from_cache(text)
        if cached:
            return EmbeddingResult(
                embedding=cached,
                model=self.model,
                processing_time_ms=(time.time() - start_time) * 1000,
            )

        # Generate embedding based on provider
        if self.provider == EmbeddingProvider.OLLAMA:
            embedding = await self._generate_ollama(text)
        elif self.provider == EmbeddingProvider.OPENAI:
            embedding = await self._generate_openai(text)
        elif self.provider == EmbeddingProvider.HTTPX:
            embedding = await self._generate_httpx(text)
        else:
            raise EmbeddingGeneratorError(f"Unknown provider: {self.provider}")

        # Cache the result
        await self._set_cache(text, embedding)

        return EmbeddingResult(
            embedding=embedding,
            model=self.model,
            processing_time_ms=(time.time() - start_time) * 1000,
        )

    async def generate_batch(self, texts: List[str]) -> List[EmbeddingResult]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of EmbeddingResult objects
        """
        results = []
        for text in texts:
            result = await self.generate(text)
            results.append(result)
        return results

    async def _generate_ollama(self, text: str) -> List[float]:
        """Generate embedding using Ollama."""
        try:
            response = self.ollama_client.embeddings(model=self.model, prompt=text)
            return response["embedding"]
        except Exception as e:
            logger.error(f"Ollama embedding error: {e}")
            # Return zero vector as fallback
            return [0.0] * self.dimension

    async def _generate_openai(self, text: str) -> List[float]:
        """Generate embedding using OpenAI."""
        try:
            model = self.config.openai_model or "text-embedding-3-small"
            response = self.openai_client.embeddings.create(model=model, input=text)
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"OpenAI embedding error: {e}")
            raise EmbeddingGeneratorError(f"OpenAI embedding failed: {e}")

    async def _generate_httpx(self, text: str) -> List[float]:
        """Generate embedding using generic HTTP endpoint."""
        try:
            client = await self._get_http_client()

            # Assume Ollama-compatible API
            response = await client.post(
                f"{self.config.ollama_base_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
            )
            response.raise_for_status()
            data = response.json()
            return data.get("embedding", [0.0] * self.dimension)
        except Exception as e:
            logger.error(f"HTTP embedding error: {e}")
            return [0.0] * self.dimension

    async def close(self) -> None:
        """Close resources."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None
        if self._redis_client:
            await self._redis_client.close()
            self._redis_client = None


# Module-level convenience functions

_generator: Optional[EmbeddingGenerator] = None


def _get_generator() -> EmbeddingGenerator:
    """Get the default embedding generator instance."""
    global _generator
    if _generator is None:
        _generator = EmbeddingGenerator()
    return _generator


async def generate_embedding(text: str) -> EmbeddingResult:
    """
    Generate embedding using the default generator.

    Args:
        text: Text to embed

    Returns:
        EmbeddingResult with embedding vector
    """
    return await _get_generator().generate(text)


async def generate_embeddings(texts: List[str]) -> List[EmbeddingResult]:
    """
    Generate embeddings for multiple texts.

    Args:
        texts: List of texts to embed

    Returns:
        List of EmbeddingResult objects
    """
    return await _get_generator().generate_batch(texts)
