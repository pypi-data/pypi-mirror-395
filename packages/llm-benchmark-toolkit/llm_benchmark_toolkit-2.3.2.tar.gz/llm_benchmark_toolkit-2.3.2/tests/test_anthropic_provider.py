"""
Tests for Anthropic Provider

Mocks Anthropic API calls to test provider logic.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

# Skip all tests if anthropic not installed
pytest.importorskip("anthropic", reason="anthropic not installed")

from llm_evaluator.providers.anthropic_provider import AnthropicProvider


class TestAnthropicProvider:
    """Test Anthropic provider functionality"""

    @pytest.fixture
    def mock_api_key(self):
        """Mock API key in environment"""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key-123"}):
            yield

    @pytest.fixture
    def provider(self, mock_api_key):
        """Create provider with mocked client"""
        with patch("llm_evaluator.providers.anthropic_provider.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            provider = AnthropicProvider(model="claude-3-haiku-20240307")
            provider.client = mock_client
            return provider

    @pytest.fixture
    def mock_response(self):
        """Mock Anthropic API response"""
        mock_resp = MagicMock()
        mock_resp.content = [MagicMock()]
        mock_resp.content[0].text = "Hello from Claude!"
        mock_resp.stop_reason = "end_turn"
        mock_resp.usage = MagicMock()
        mock_resp.usage.input_tokens = 10
        mock_resp.usage.output_tokens = 5
        return mock_resp

    def test_init_with_api_key_env(self, mock_api_key):
        """Test initialization with API key from environment"""
        with patch("llm_evaluator.providers.anthropic_provider.Anthropic"):
            provider = AnthropicProvider(model="claude-3-haiku-20240307")
            assert provider.model == "claude-3-haiku-20240307"

    def test_init_with_api_key_param(self):
        """Test initialization with API key parameter"""
        with patch("llm_evaluator.providers.anthropic_provider.Anthropic"):
            provider = AnthropicProvider(model="claude-3-haiku-20240307", api_key="explicit-key")
            assert provider.api_key == "explicit-key"

    def test_supported_models(self):
        """Test supported models list"""
        assert "claude-3-haiku-20240307" in AnthropicProvider.SUPPORTED_MODELS
        assert "claude-3-sonnet-20240229" in AnthropicProvider.SUPPORTED_MODELS
        assert "claude-3-opus-20240229" in AnthropicProvider.SUPPORTED_MODELS

    def test_generate_success(self, provider, mock_response):
        """Test successful text generation"""
        provider.client.messages.create.return_value = mock_response

        result = provider.generate("Test prompt")

        assert result.text == "Hello from Claude!"
        # Check metadata contains provider info
        assert result.metadata.get("provider") == "anthropic"
        assert result.tokens_used == 15  # 10 input + 5 output

    def test_generate_with_system_prompt(self, provider, mock_response):
        """Test generation with system prompt"""
        provider.client.messages.create.return_value = mock_response

        provider.generate("Test", system_prompt="You are helpful")

        call_args = provider.client.messages.create.call_args
        assert "system" in call_args.kwargs or any("system" in str(arg) for arg in call_args.args)

    def test_generate_batch(self, provider, mock_response):
        """Test batch generation"""
        provider.client.messages.create.return_value = mock_response

        results = provider.generate_batch(["Prompt 1", "Prompt 2"])

        assert len(results) == 2
        assert all(r.text == "Hello from Claude!" for r in results)

    def test_get_model_info(self, provider):
        """Test getting model information"""
        info = provider.get_model_info()

        assert info["model_id"] == "claude-3-haiku-20240307"
        assert info["provider"] == "anthropic"
        assert "context_window" in info

    def test_is_available_success(self, provider, mock_response):
        """Test availability check when API works"""
        provider.client.messages.create.return_value = mock_response

        assert provider.is_available() is True

    def test_is_available_failure(self, provider):
        """Test availability check when API fails"""
        provider.client.messages.create.side_effect = Exception("API Error")

        assert provider.is_available() is False
