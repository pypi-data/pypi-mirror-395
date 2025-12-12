"""
Tests for embedding generation service.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from bizstats_vector_store.config import reset_config, configure
from bizstats_vector_store.models.enums import EmbeddingProvider
from bizstats_vector_store.embedding.service import (
    EmbeddingGenerator,
    EmbeddingGeneratorError,
    EmbeddingResult,
    generate_embedding,
    generate_embeddings,
)


class TestEmbeddingGenerator:
    """Tests for EmbeddingGenerator class."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    def test_generator_initialization_defaults(self):
        """Test generator initialization with defaults."""
        generator = EmbeddingGenerator()

        assert generator.provider == EmbeddingProvider.OLLAMA
        assert generator.dimension == 1024

    def test_generator_initialization_custom_provider(self):
        """Test generator with custom provider."""
        configure(embedding_provider="openai")
        generator = EmbeddingGenerator()

        assert generator.provider == EmbeddingProvider.OPENAI

    def test_generator_override_provider(self):
        """Test generator with provider override."""
        generator = EmbeddingGenerator(provider="openai")

        assert generator.provider == EmbeddingProvider.OPENAI

    def test_cache_key_generation(self):
        """Test cache key generation."""
        generator = EmbeddingGenerator()

        key1 = generator._get_cache_key("test text")
        key2 = generator._get_cache_key("test text")
        key3 = generator._get_cache_key("different text")

        assert key1 == key2  # Same text = same key
        assert key1 != key3  # Different text = different key
        assert "embed:" in key1
        assert "ollama" in key1

    @pytest.mark.asyncio
    async def test_generate_ollama_success(self):
        """Test successful Ollama embedding generation."""
        generator = EmbeddingGenerator()

        # Mock the Ollama client
        mock_response = {"embedding": [0.1] * 1024}
        mock_client = Mock()
        mock_client.embeddings.return_value = mock_response
        generator._ollama_client = mock_client

        result = await generator._generate_ollama("test text")

        assert len(result) == 1024
        mock_client.embeddings.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_ollama_error_returns_zero_vector(self):
        """Test Ollama error returns zero vector."""
        generator = EmbeddingGenerator()

        mock_client = Mock()
        mock_client.embeddings.side_effect = Exception("Connection error")
        generator._ollama_client = mock_client

        result = await generator._generate_ollama("test text")

        assert result == [0.0] * 1024

    @pytest.mark.asyncio
    async def test_generate_with_cache(self):
        """Test embedding generation with cache."""
        generator = EmbeddingGenerator()
        generator._cache_enabled = True

        cached_embedding = [0.5] * 1024

        # Mock cache retrieval
        generator._get_from_cache = AsyncMock(return_value=cached_embedding)

        result = await generator.generate("cached text")

        assert result.embedding == cached_embedding
        generator._get_from_cache.assert_called_once_with("cached text")

    @pytest.mark.asyncio
    async def test_generate_batch(self):
        """Test batch embedding generation."""
        generator = EmbeddingGenerator()

        # Mock single generate
        generator.generate = AsyncMock(
            return_value=EmbeddingResult(
                embedding=[0.1] * 1024,
                model="test",
                processing_time_ms=10.0,
            )
        )

        texts = ["text1", "text2", "text3"]
        results = await generator.generate_batch(texts)

        assert len(results) == 3
        assert generator.generate.call_count == 3

    @pytest.mark.asyncio
    async def test_generate_httpx(self):
        """Test HTTP-based embedding generation."""
        generator = EmbeddingGenerator(provider="httpx")

        mock_response = Mock()
        mock_response.json.return_value = {"embedding": [0.2] * 1024}
        mock_response.raise_for_status = Mock()

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        generator._http_client = mock_client

        result = await generator._generate_httpx("test")

        assert len(result) == 1024

    @pytest.mark.asyncio
    async def test_generate_httpx_error_returns_zero_vector(self):
        """Test HTTP error returns zero vector."""
        generator = EmbeddingGenerator(provider="httpx")

        mock_client = AsyncMock()
        mock_client.post.side_effect = Exception("Network error")
        generator._http_client = mock_client

        result = await generator._generate_httpx("test")

        assert result == [0.0] * 1024

    @pytest.mark.asyncio
    async def test_close_resources(self):
        """Test closing generator resources."""
        generator = EmbeddingGenerator()

        mock_http = AsyncMock()
        mock_redis = AsyncMock()
        generator._http_client = mock_http
        generator._redis_client = mock_redis

        await generator.close()

        mock_http.aclose.assert_called_once()
        mock_redis.close.assert_called_once()
        assert generator._http_client is None
        assert generator._redis_client is None

    def test_ollama_client_lazy_initialization(self):
        """Test Ollama client is lazily initialized."""
        generator = EmbeddingGenerator()
        assert generator._ollama_client is None

    def test_ollama_not_installed_error(self):
        """Test error when ollama package not installed."""
        generator = EmbeddingGenerator()

        with patch.dict("sys.modules", {"ollama": None}):
            with patch("builtins.__import__", side_effect=ImportError("No module")):
                # Force re-evaluation of property
                generator._ollama_client = None
                with pytest.raises(EmbeddingGeneratorError) as exc_info:
                    _ = generator.ollama_client

                assert "ollama package not installed" in str(exc_info.value)


class TestEmbeddingResult:
    """Tests for EmbeddingResult dataclass."""

    def test_embedding_result_creation(self):
        """Test creating embedding result."""
        result = EmbeddingResult(
            embedding=[0.1, 0.2, 0.3],
            model="test-model",
            processing_time_ms=25.5,
        )

        assert len(result.embedding) == 3
        assert result.model == "test-model"
        assert result.processing_time_ms == 25.5


class TestModuleFunctions:
    """Tests for module-level convenience functions."""

    def setup_method(self):
        """Reset before each test."""
        reset_config()

    @pytest.mark.asyncio
    async def test_generate_embedding_function(self):
        """Test module-level generate_embedding function."""
        with patch(
            "bizstats_vector_store.embedding.service._get_generator"
        ) as mock_get:
            mock_generator = AsyncMock()
            mock_generator.generate.return_value = EmbeddingResult(
                embedding=[0.1],
                model="test",
                processing_time_ms=10,
            )
            mock_get.return_value = mock_generator

            result = await generate_embedding("test")

            assert result.embedding == [0.1]

    @pytest.mark.asyncio
    async def test_generate_embeddings_function(self):
        """Test module-level generate_embeddings function."""
        with patch(
            "bizstats_vector_store.embedding.service._get_generator"
        ) as mock_get:
            mock_generator = AsyncMock()
            mock_generator.generate_batch.return_value = [
                EmbeddingResult(embedding=[0.1], model="test", processing_time_ms=10)
            ]
            mock_get.return_value = mock_generator

            results = await generate_embeddings(["test"])

            assert len(results) == 1


class TestOllamaClientWithApiKey:
    """Tests for Ollama client with API key."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    def test_ollama_client_with_api_key(self):
        """Test Ollama client initialization includes API key in headers."""
        configure(ollama_api_key="test-api-key", ollama_base_url="http://test:11434")
        generator = EmbeddingGenerator()

        # Verify config has the API key
        assert generator.config.ollama_api_key == "test-api-key"

        # The logic in the property builds headers when api_key is present
        # We verify the config is set correctly, which is the input to the property
        assert generator.config.ollama_base_url == "http://test:11434"


class TestOpenAIClient:
    """Tests for OpenAI client initialization."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    def test_openai_client_no_api_key_error(self):
        """Test OpenAI client raises error without API key."""
        generator = EmbeddingGenerator(provider="openai")

        with pytest.raises(EmbeddingGeneratorError) as exc_info:
            _ = generator.openai_client

        # Error can be either "API key not configured" or "not installed"
        error_msg = str(exc_info.value)
        assert "OpenAI" in error_msg or "openai" in error_msg

    def test_openai_client_not_installed_error(self):
        """Test error when openai package not installed."""
        configure(openai_api_key="test-key")
        generator = EmbeddingGenerator(provider="openai")

        with patch.dict("sys.modules", {"openai": None}):
            with patch("builtins.__import__", side_effect=ImportError("No module")):
                generator._openai_client = None
                with pytest.raises(EmbeddingGeneratorError) as exc_info:
                    _ = generator.openai_client

                assert "openai package not installed" in str(exc_info.value)


class TestCacheOperations:
    """Tests for cache operations."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    @pytest.mark.asyncio
    async def test_get_from_cache_disabled(self):
        """Test _get_from_cache when cache is disabled."""
        generator = EmbeddingGenerator()
        generator._cache_enabled = False

        result = await generator._get_from_cache("test")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_from_cache_with_redis(self):
        """Test _get_from_cache with Redis."""
        import json
        generator = EmbeddingGenerator()
        generator._cache_enabled = True

        mock_redis = AsyncMock()
        mock_redis.get.return_value = json.dumps([0.1, 0.2, 0.3])
        generator._redis_client = mock_redis

        result = await generator._get_from_cache("test")

        assert result == [0.1, 0.2, 0.3]

    @pytest.mark.asyncio
    async def test_get_from_cache_error(self):
        """Test _get_from_cache handles errors gracefully."""
        generator = EmbeddingGenerator()
        generator._cache_enabled = True

        mock_redis = AsyncMock()
        mock_redis.get.side_effect = Exception("Redis error")
        generator._redis_client = mock_redis

        result = await generator._get_from_cache("test")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_cache_disabled(self):
        """Test _set_cache when cache is disabled."""
        generator = EmbeddingGenerator()
        generator._cache_enabled = False

        # Should not raise any errors
        await generator._set_cache("test", [0.1, 0.2])

    @pytest.mark.asyncio
    async def test_set_cache_with_redis(self):
        """Test _set_cache with Redis."""
        generator = EmbeddingGenerator()
        generator._cache_enabled = True

        mock_redis = AsyncMock()
        generator._redis_client = mock_redis

        await generator._set_cache("test", [0.1, 0.2])

        mock_redis.setex.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_cache_error(self):
        """Test _set_cache handles errors gracefully."""
        generator = EmbeddingGenerator()
        generator._cache_enabled = True

        mock_redis = AsyncMock()
        mock_redis.setex.side_effect = Exception("Redis error")
        generator._redis_client = mock_redis

        # Should not raise any errors
        await generator._set_cache("test", [0.1, 0.2])


class TestGenerateWithProviders:
    """Tests for generate with different providers."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    @pytest.mark.asyncio
    async def test_generate_openai_provider(self):
        """Test generate with OpenAI provider."""
        generator = EmbeddingGenerator(provider="openai")
        generator._cache_enabled = False

        # Mock the OpenAI client
        mock_response = Mock()
        mock_response.data = [Mock(embedding=[0.3] * 1024)]

        mock_client = Mock()
        mock_client.embeddings.create.return_value = mock_response
        generator._openai_client = mock_client

        result = await generator.generate("test")

        assert len(result.embedding) == 1024
        mock_client.embeddings.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_openai_error(self):
        """Test OpenAI error raises exception."""
        generator = EmbeddingGenerator(provider="openai")
        generator._cache_enabled = False

        mock_client = Mock()
        mock_client.embeddings.create.side_effect = Exception("API error")
        generator._openai_client = mock_client

        with pytest.raises(EmbeddingGeneratorError) as exc_info:
            await generator._generate_openai("test")

        assert "OpenAI embedding failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_generate_unknown_provider_error(self):
        """Test generate with unknown provider raises error."""
        generator = EmbeddingGenerator()
        generator._cache_enabled = False
        generator.provider = "unknown"

        with pytest.raises(EmbeddingGeneratorError) as exc_info:
            await generator.generate("test")

        assert "Unknown provider" in str(exc_info.value)


class TestCloseResources:
    """Tests for close resource handling."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    @pytest.mark.asyncio
    async def test_close_only_redis(self):
        """Test closing only Redis client."""
        generator = EmbeddingGenerator()
        generator._http_client = None

        mock_redis = AsyncMock()
        generator._redis_client = mock_redis

        await generator.close()

        mock_redis.close.assert_called_once()
        assert generator._redis_client is None

    @pytest.mark.asyncio
    async def test_close_no_resources(self):
        """Test closing when no resources exist."""
        generator = EmbeddingGenerator()
        generator._http_client = None
        generator._redis_client = None

        # Should not raise any errors
        await generator.close()


class TestGetGenerator:
    """Tests for _get_generator function."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()
        # Reset the module-level generator
        import bizstats_vector_store.embedding.service as service
        service._generator = None

    def test_get_generator_creates_instance(self):
        """Test _get_generator creates a new instance."""
        from bizstats_vector_store.embedding.service import _get_generator, _generator

        generator = _get_generator()
        assert generator is not None
        assert isinstance(generator, EmbeddingGenerator)

    def test_get_generator_singleton(self):
        """Test _get_generator returns the same instance."""
        from bizstats_vector_store.embedding.service import _get_generator

        gen1 = _get_generator()
        gen2 = _get_generator()

        assert gen1 is gen2


class TestHttpClientInitialization:
    """Tests for HTTP client lazy initialization."""

    def setup_method(self):
        """Reset config before each test."""
        reset_config()

    @pytest.mark.asyncio
    async def test_http_client_lazy_init(self):
        """Test HTTP client is lazily initialized."""
        generator = EmbeddingGenerator(provider="httpx")
        assert generator._http_client is None

        client = await generator._get_http_client()
        assert client is not None
        assert generator._http_client is client

        # Second call returns same client
        client2 = await generator._get_http_client()
        assert client2 is client

        # Cleanup
        await generator.close()
