"""
Extended tests for providers/__init__.py - test provider factory functions
"""

import pytest


class TestProviderImports:
    """Test provider imports and availability flags"""

    def test_base_imports_available(self):
        """Test base imports are always available"""
        from llm_evaluator.providers import (
            GenerationConfig,
            GenerationResult,
            LLMProvider,
            ProviderError,
        )

        assert LLMProvider is not None
        assert GenerationConfig is not None
        assert GenerationResult is not None
        assert ProviderError is not None

    def test_ollama_provider_import(self):
        """Test OllamaProvider can be imported"""
        from llm_evaluator.providers import OllamaProvider

        assert OllamaProvider is not None

    def test_cached_provider_import(self):
        """Test CachedProvider can be imported"""
        from llm_evaluator.providers import CachedProvider

        assert CachedProvider is not None


class TestGenerationConfig:
    """Test GenerationConfig dataclass"""

    def test_default_values(self):
        """Test GenerationConfig default values"""
        from llm_evaluator.providers import GenerationConfig

        config = GenerationConfig()

        assert config.temperature >= 0
        assert config.max_tokens > 0

    def test_custom_values(self):
        """Test GenerationConfig with custom values"""
        from llm_evaluator.providers import GenerationConfig

        config = GenerationConfig(temperature=0.5, max_tokens=100, top_p=0.9)

        assert config.temperature == 0.5
        assert config.max_tokens == 100
        assert config.top_p == 0.9


class TestGenerationResult:
    """Test GenerationResult dataclass"""

    def test_creation(self):
        """Test GenerationResult creation"""
        from llm_evaluator.providers import GenerationResult

        result = GenerationResult(
            text="Hello world", response_time=0.5, tokens_used=10, model="test-model", metadata={}
        )

        assert result.text == "Hello world"
        assert result.response_time == 0.5
        assert result.tokens_used == 10

    def test_optional_fields(self):
        """Test GenerationResult optional fields"""
        from llm_evaluator.providers import GenerationResult

        result = GenerationResult(
            text="Test",
            response_time=1.0,
            tokens_used=5,
            model="model",
            metadata={},
            cached=True,
            error="Some error",
        )

        assert result.cached is True
        assert result.error == "Some error"


class TestProviderError:
    """Test ProviderError exception"""

    def test_provider_error_creation(self):
        """Test ProviderError can be created"""
        from llm_evaluator.providers import ProviderError

        error = ProviderError("Test error")

        assert "Test error" in str(error)

    def test_provider_error_raise(self):
        """Test ProviderError can be raised"""
        from llm_evaluator.providers import ProviderError

        with pytest.raises(ProviderError):
            raise ProviderError("Test")


class TestLLMProviderInterface:
    """Test LLMProvider abstract interface"""

    def test_llm_provider_is_abstract(self):
        """Test LLMProvider cannot be instantiated directly"""
        from llm_evaluator.providers import LLMProvider

        # Should not be able to instantiate abstract class
        with pytest.raises(TypeError):
            LLMProvider()
