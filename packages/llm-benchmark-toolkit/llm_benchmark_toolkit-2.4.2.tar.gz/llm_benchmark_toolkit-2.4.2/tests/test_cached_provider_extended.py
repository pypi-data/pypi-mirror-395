"""
Extended tests for CachedProvider - focus on uncovered code paths
"""

import tempfile
from unittest.mock import Mock


class TestCachedProviderInit:
    """Test CachedProvider initialization"""

    def test_init_with_custom_cache_dir(self):
        """Test initialization with custom cache directory"""
        from llm_evaluator.providers.base import GenerationConfig
        from llm_evaluator.providers.cached_provider import CachedProvider

        mock_provider = Mock()
        mock_provider.model = "test-model"
        mock_provider.config = GenerationConfig()

        with tempfile.TemporaryDirectory() as tmpdir:
            cached = CachedProvider(mock_provider, cache_dir=tmpdir)

            assert cached.provider is mock_provider
            assert str(cached.cache_dir) == tmpdir

    def test_init_stores_provider_reference(self):
        """Test init stores reference to base provider"""
        from llm_evaluator.providers.base import GenerationConfig
        from llm_evaluator.providers.cached_provider import CachedProvider

        mock_provider = Mock()
        mock_provider.model = "test"
        mock_provider.config = GenerationConfig()

        with tempfile.TemporaryDirectory() as tmpdir:
            cached = CachedProvider(mock_provider, cache_dir=tmpdir)

            assert cached.provider is mock_provider


class TestCachedProviderGenerate:
    """Test CachedProvider generate method"""

    def test_generate_caches_result(self):
        """Test generate caches the result"""
        from llm_evaluator.providers.base import GenerationConfig, GenerationResult
        from llm_evaluator.providers.cached_provider import CachedProvider

        mock_provider = Mock()
        mock_provider.model = "test"
        mock_provider.config = GenerationConfig()
        mock_provider.generate.return_value = GenerationResult(
            text="Cached response", response_time=0.5, tokens_used=10, model="test", metadata={}
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            cached = CachedProvider(mock_provider, cache_dir=tmpdir)

            # First call - should hit provider
            cached.generate("test prompt")
            assert mock_provider.generate.call_count == 1

            # Second call - should hit cache
            result2 = cached.generate("test prompt")
            # Provider should not be called again
            assert mock_provider.generate.call_count == 1 or result2.cached

    def test_generate_returns_generation_result(self):
        """Test generate returns GenerationResult"""
        from llm_evaluator.providers.base import GenerationConfig, GenerationResult
        from llm_evaluator.providers.cached_provider import CachedProvider

        mock_provider = Mock()
        mock_provider.model = "test"
        mock_provider.config = GenerationConfig()
        mock_provider.generate.return_value = GenerationResult(
            text="Response", response_time=0.5, tokens_used=10, model="test", metadata={}
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            cached = CachedProvider(mock_provider, cache_dir=tmpdir)
            result = cached.generate("prompt")

            assert isinstance(result, GenerationResult)


class TestCachedProviderModel:
    """Test CachedProvider model property"""

    def test_model_delegates_to_provider(self):
        """Test model property returns provider's model"""
        from llm_evaluator.providers.base import GenerationConfig
        from llm_evaluator.providers.cached_provider import CachedProvider

        mock_provider = Mock()
        mock_provider.model = "delegated-model"
        mock_provider.config = GenerationConfig()

        with tempfile.TemporaryDirectory() as tmpdir:
            cached = CachedProvider(mock_provider, cache_dir=tmpdir)

            assert cached.model == "delegated-model"


class TestCachedProviderCacheKey:
    """Test cache key generation"""

    def test_same_prompt_same_key(self):
        """Test same prompt generates same cache key"""
        from llm_evaluator.providers.base import GenerationConfig
        from llm_evaluator.providers.cached_provider import CachedProvider

        mock_provider = Mock()
        mock_provider.model = "test"
        mock_provider.config = GenerationConfig()

        with tempfile.TemporaryDirectory() as tmpdir:
            cached = CachedProvider(mock_provider, cache_dir=tmpdir)

            key1 = cached._generate_cache_key("test prompt", None, None)
            key2 = cached._generate_cache_key("test prompt", None, None)

            assert key1 == key2

    def test_different_prompts_different_keys(self):
        """Test different prompts generate different keys"""
        from llm_evaluator.providers.base import GenerationConfig
        from llm_evaluator.providers.cached_provider import CachedProvider

        mock_provider = Mock()
        mock_provider.model = "test"
        mock_provider.config = GenerationConfig()

        with tempfile.TemporaryDirectory() as tmpdir:
            cached = CachedProvider(mock_provider, cache_dir=tmpdir)

            key1 = cached._generate_cache_key("prompt 1", None, None)
            key2 = cached._generate_cache_key("prompt 2", None, None)

            assert key1 != key2


class TestCachedProviderClearCache:
    """Test cache clearing"""

    def test_clear_cache(self):
        """Test clear_cache method"""
        from llm_evaluator.providers.base import GenerationConfig, GenerationResult
        from llm_evaluator.providers.cached_provider import CachedProvider

        mock_provider = Mock()
        mock_provider.model = "test"
        mock_provider.config = GenerationConfig()
        mock_provider.generate.return_value = GenerationResult(
            text="Response", response_time=0.5, tokens_used=10, model="test", metadata={}
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            cached = CachedProvider(mock_provider, cache_dir=tmpdir)

            # Generate to create cache
            cached.generate("test")

            # Clear cache
            cached.clear_cache()

            # Cache should be empty (generate again calls provider)
            cached.generate("test")
            assert mock_provider.generate.call_count >= 2


class TestCachedProviderStats:
    """Test cache statistics"""

    def test_get_cache_stats(self):
        """Test getting cache statistics"""
        from llm_evaluator.providers.base import GenerationConfig, GenerationResult
        from llm_evaluator.providers.cached_provider import CachedProvider

        mock_provider = Mock()
        mock_provider.model = "test"
        mock_provider.config = GenerationConfig()
        mock_provider.generate.return_value = GenerationResult(
            text="Response", response_time=0.5, tokens_used=10, model="test", metadata={}
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            cached = CachedProvider(mock_provider, cache_dir=tmpdir)

            stats = cached.get_cache_stats()

            assert isinstance(stats, dict)
            assert "hits" in stats or "cache_size" in stats or "entries" in stats
