"""
Tests for CachedProvider

Tests the caching layer for LLM providers.
"""

from unittest.mock import Mock

import pytest

from llm_evaluator.providers import GenerationConfig, GenerationResult
from llm_evaluator.providers.cached_provider import CachedProvider


class TestCachedProvider:
    """Test CachedProvider functionality"""

    @pytest.fixture
    def mock_base_provider(self):
        """Create a mock base provider"""
        provider = Mock()
        provider.model = "test-model"
        provider.config = GenerationConfig()
        provider.generate.return_value = GenerationResult(
            text="Test response",
            response_time=0.5,
            tokens_used=10,
            model="test-model",
            provider="mock",
        )
        provider.is_available.return_value = True
        provider.get_model_info.return_value = {"model": "test-model"}
        provider._get_provider_type.return_value = "mock"
        return provider

    @pytest.fixture
    def cached_provider(self, mock_base_provider, tmp_path):
        """Create a CachedProvider with temporary cache directory"""
        return CachedProvider(mock_base_provider, cache_dir=str(tmp_path))

    def test_init(self, mock_base_provider, tmp_path):
        """Test CachedProvider initialization"""
        cached = CachedProvider(mock_base_provider, cache_dir=str(tmp_path))
        assert cached.provider == mock_base_provider
        assert cached.model == mock_base_provider.model

    def test_generate_cache_miss(self, cached_provider, mock_base_provider):
        """Test generation on cache miss"""
        result = cached_provider.generate("Test prompt")

        # Should call the base provider
        mock_base_provider.generate.assert_called_once()
        assert result.text == "Test response"

    def test_generate_cache_hit(self, cached_provider, mock_base_provider):
        """Test generation on cache hit"""
        # First call - cache miss
        result1 = cached_provider.generate("Test prompt")
        assert mock_base_provider.generate.call_count == 1

        # Second call - should be cache hit
        result2 = cached_provider.generate("Test prompt")

        # Should still be 1 call (cached)
        assert mock_base_provider.generate.call_count == 1
        assert result2.text == result1.text

    def test_cache_stats_initial(self, cached_provider):
        """Test initial cache stats"""
        stats = cached_provider.get_cache_stats()

        assert stats["hits"] == 0
        assert stats["misses"] == 0

    def test_cache_stats_after_operations(self, cached_provider, mock_base_provider):
        """Test cache stats after operations"""
        # Generate once (miss)
        cached_provider.generate("Prompt 1")

        # Generate same prompt again (hit)
        cached_provider.generate("Prompt 1")

        # Generate different prompt (miss)
        cached_provider.generate("Prompt 2")

        stats = cached_provider.get_cache_stats()

        assert stats["hits"] == 1
        assert stats["misses"] == 2

    def test_is_available(self, cached_provider, mock_base_provider):
        """Test is_available delegates to base provider"""
        assert cached_provider.is_available() is True
        mock_base_provider.is_available.assert_called()

    def test_get_model_info(self, cached_provider, mock_base_provider):
        """Test get_model_info delegates to base provider"""
        info = cached_provider.get_model_info()

        assert info["model"] == "test-model"
        mock_base_provider.get_model_info.assert_called()

    def test_different_prompts_not_cached(self, cached_provider, mock_base_provider):
        """Test that different prompts don't share cache"""
        cached_provider.generate("Prompt A")
        cached_provider.generate("Prompt B")

        # Both should be cache misses
        assert mock_base_provider.generate.call_count == 2

    def test_generate_batch(self, cached_provider, mock_base_provider):
        """Test batch generation with caching"""
        mock_base_provider.generate_batch.return_value = [
            GenerationResult(text="Response 1", response_time=0.5, tokens_used=10, model="test"),
            GenerationResult(text="Response 2", response_time=0.5, tokens_used=10, model="test"),
        ]

        results = cached_provider.generate_batch(["Prompt 1", "Prompt 2"])

        assert len(results) == 2

    def test_cache_key_generation(self, cached_provider):
        """Test cache key is consistent"""
        key1 = cached_provider._generate_cache_key("prompt", "system", None)
        key2 = cached_provider._generate_cache_key("prompt", "system", None)

        assert key1 == key2

    def test_cache_key_different_for_different_inputs(self, cached_provider):
        """Test cache keys differ for different inputs"""
        key1 = cached_provider._generate_cache_key("prompt1", None, None)
        key2 = cached_provider._generate_cache_key("prompt2", None, None)

        assert key1 != key2

    def test_custom_cache_dir(self, mock_base_provider, tmp_path):
        """Test using custom cache directory"""
        custom_dir = tmp_path / "custom_cache"
        cached = CachedProvider(mock_base_provider, cache_dir=str(custom_dir))

        # Generate to create cache entry
        cached.generate("Test")

        # Check cache was created in custom directory
        assert custom_dir.exists()


class TestCacheKeyGeneration:
    """Test cache key generation edge cases"""

    @pytest.fixture
    def cached_provider(self, tmp_path):
        mock_provider = Mock()
        mock_provider.model = "test"
        mock_provider.config = GenerationConfig()
        mock_provider.generate.return_value = GenerationResult(
            text="Test", response_time=0.1, tokens_used=5, model="test"
        )
        return CachedProvider(mock_provider, cache_dir=str(tmp_path))

    def test_empty_prompt(self, cached_provider):
        """Test cache key for empty prompt"""
        key = cached_provider._generate_cache_key("", None, None)
        assert key is not None
        assert len(key) > 0

    def test_unicode_prompt(self, cached_provider):
        """Test cache key for unicode prompt"""
        key = cached_provider._generate_cache_key("你好世界 🎉", None, None)
        assert key is not None

    def test_very_long_prompt(self, cached_provider):
        """Test cache key for very long prompt"""
        long_prompt = "x" * 100000
        key = cached_provider._generate_cache_key(long_prompt, None, None)

        # Key should be fixed length (hash)
        assert len(key) < 100

    def test_config_affects_key(self, cached_provider):
        """Test that config affects cache key"""
        config1 = GenerationConfig(temperature=0.5)
        config2 = GenerationConfig(temperature=0.9)

        key1 = cached_provider._generate_cache_key("prompt", None, config1)
        key2 = cached_provider._generate_cache_key("prompt", None, config2)

        assert key1 != key2
