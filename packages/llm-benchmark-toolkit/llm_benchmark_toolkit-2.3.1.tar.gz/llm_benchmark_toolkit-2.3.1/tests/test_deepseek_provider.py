"""
Tests for DeepSeek provider
"""

import os
from unittest.mock import MagicMock, patch

import pytest

# Skip if openai not installed
pytest.importorskip("openai")

from llm_evaluator.providers import ProviderError
from llm_evaluator.providers.deepseek_provider import DeepSeekProvider


class TestDeepSeekProvider:
    """Test DeepSeek provider functionality"""

    @pytest.fixture
    def mock_api_key(self):
        """Mock API key in environment"""
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-key-123"}):
            yield

    @pytest.fixture
    def provider(self, mock_api_key):
        """Create provider with mocked client"""
        with patch("llm_evaluator.providers.deepseek_provider.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            provider = DeepSeekProvider(model="deepseek-chat")
            provider.client = mock_client
            return provider

    def test_init_with_api_key_env(self, mock_api_key):
        """Test initialization with API key from environment"""
        with patch("llm_evaluator.providers.deepseek_provider.OpenAI"):
            provider = DeepSeekProvider(model="deepseek-chat")
            assert provider.model == "deepseek-chat"
            assert provider.api_key == "test-key-123"

    def test_init_with_api_key_param(self):
        """Test initialization with API key parameter"""
        with patch("llm_evaluator.providers.deepseek_provider.OpenAI"):
            provider = DeepSeekProvider(model="deepseek-chat", api_key="explicit-key-456")
            assert provider.api_key == "explicit-key-456"

    def test_init_without_api_key_raises(self):
        """Test that initialization without API key raises error"""
        with patch.dict(os.environ, {}, clear=True):
            # Clear DEEPSEEK_API_KEY if set
            os.environ.pop("DEEPSEEK_API_KEY", None)
            with pytest.raises(ProviderError, match="API key not found"):
                DeepSeekProvider(model="deepseek-chat")

    def test_supported_models(self):
        """Test supported models list"""
        assert "deepseek-chat" in DeepSeekProvider.SUPPORTED_MODELS
        assert "deepseek-reasoner" in DeepSeekProvider.SUPPORTED_MODELS
        assert "deepseek-coder" in DeepSeekProvider.SUPPORTED_MODELS

    def test_base_url(self, mock_api_key):
        """Test default base URL"""
        with patch("llm_evaluator.providers.deepseek_provider.OpenAI"):
            provider = DeepSeekProvider(model="deepseek-chat")
            assert provider.base_url == "https://api.deepseek.com"

    def test_custom_base_url(self, mock_api_key):
        """Test custom base URL"""
        with patch("llm_evaluator.providers.deepseek_provider.OpenAI"):
            provider = DeepSeekProvider(model="deepseek-chat", base_url="https://custom.api.com")
            assert provider.base_url == "https://custom.api.com"

    def test_generate_success(self, provider):
        """Test successful text generation"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello! How can I help?"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5

        provider.client.chat.completions.create.return_value = mock_response

        result = provider.generate("Hi there!")

        assert result.text == "Hello! How can I help?"
        assert result.provider == "deepseek"
        assert result.model == "deepseek-chat"
        assert result.prompt_tokens == 10
        assert result.completion_tokens == 5

    def test_generate_batch(self, provider):
        """Test batch generation"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Response"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.usage.prompt_tokens = 5
        mock_response.usage.completion_tokens = 3

        provider.client.chat.completions.create.return_value = mock_response

        results = provider.generate_batch(["Prompt 1", "Prompt 2"])

        assert len(results) == 2
        assert all(r.text == "Response" for r in results)

    def test_get_model_info(self, provider):
        """Test getting model information"""
        info = provider.get_model_info()

        assert info["model"] == "deepseek-chat"
        assert info["provider"] == "deepseek"
        assert "context_window" in info
        assert "cost_per_1m_input" in info
        assert "cost_per_1m_output" in info

    def test_count_tokens(self, provider):
        """Test token counting approximation"""
        text = "Hello world! This is a test."
        tokens = provider.count_tokens(text)

        # Approximate: 1 token ≈ 4 characters
        assert tokens > 0
        assert tokens == len(text) // 4

    def test_provider_type(self, provider):
        """Test provider type property"""
        from llm_evaluator.providers import ProviderType

        assert provider.provider_type == ProviderType.DEEPSEEK

    def test_pricing(self):
        """Test pricing information exists"""
        assert "deepseek-chat" in DeepSeekProvider.PRICING
        assert "input" in DeepSeekProvider.PRICING["deepseek-chat"]
        assert "output" in DeepSeekProvider.PRICING["deepseek-chat"]

    def test_is_available_success(self, provider):
        """Test availability check when API is working"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hi"

        provider.client.chat.completions.create.return_value = mock_response

        assert provider.is_available() is True

    def test_is_available_failure(self, provider):
        """Test availability check when API fails"""
        provider.client.chat.completions.create.side_effect = Exception("API Error")

        assert provider.is_available() is False
