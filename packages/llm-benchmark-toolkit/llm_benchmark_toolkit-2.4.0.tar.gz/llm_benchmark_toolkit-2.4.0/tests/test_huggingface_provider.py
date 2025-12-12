"""
Tests for HuggingFace Provider

Mocks HuggingFace Hub Inference API calls.
"""

from unittest.mock import MagicMock, patch

import pytest

# Skip all tests if huggingface-hub not installed
pytest.importorskip("huggingface_hub", reason="huggingface-hub not installed")

from llm_evaluator.providers import GenerationConfig, ProviderType
from llm_evaluator.providers.huggingface_provider import HuggingFaceProvider


class TestHuggingFaceProvider:
    """Test HuggingFace provider functionality"""

    @pytest.fixture
    def mock_client(self):
        """Create mocked InferenceClient"""
        with patch("llm_evaluator.providers.huggingface_provider.InferenceClient") as mock:
            mock_instance = MagicMock()
            mock.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def provider(self, mock_client):
        """Create provider with mocked client"""
        with patch("llm_evaluator.providers.huggingface_provider.InferenceClient") as mock:
            mock.return_value = mock_client
            provider = HuggingFaceProvider(model="meta-llama/Meta-Llama-3-8B-Instruct")
            return provider

    def test_init_default_model(self, mock_client):
        """Test initialization with default model"""
        with patch("llm_evaluator.providers.huggingface_provider.InferenceClient"):
            provider = HuggingFaceProvider()
            assert provider.model == "meta-llama/Meta-Llama-3-8B-Instruct"

    def test_init_custom_model(self, mock_client):
        """Test initialization with custom model"""
        with patch("llm_evaluator.providers.huggingface_provider.InferenceClient"):
            provider = HuggingFaceProvider(model="mistralai/Mistral-7B-Instruct-v0.2")
            assert provider.model == "mistralai/Mistral-7B-Instruct-v0.2"

    def test_init_with_token(self, mock_client):
        """Test initialization with explicit token"""
        with patch("llm_evaluator.providers.huggingface_provider.InferenceClient"):
            provider = HuggingFaceProvider(
                model="meta-llama/Meta-Llama-3-8B-Instruct", token="hf_test_token_123"
            )
            assert provider.token == "hf_test_token_123"

    def test_init_with_config(self, mock_client):
        """Test initialization with custom config"""
        with patch("llm_evaluator.providers.huggingface_provider.InferenceClient"):
            config = GenerationConfig(temperature=0.9, max_tokens=500)
            provider = HuggingFaceProvider(
                model="meta-llama/Meta-Llama-3-8B-Instruct", config=config
            )
            assert provider.config.temperature == 0.9
            assert provider.config.max_tokens == 500

    def test_generate_success(self, provider):
        """Test successful text generation"""
        provider.client.text_generation.return_value = "Hello from HuggingFace!"

        result = provider.generate("Test prompt")

        assert result.text == "Hello from HuggingFace!"
        assert result.model == "meta-llama/Meta-Llama-3-8B-Instruct"
        provider.client.text_generation.assert_called_once()

    def test_generate_with_system_prompt(self, provider):
        """Test generation with system prompt prepended"""
        provider.client.text_generation.return_value = "I can help!"

        provider.generate("Help me", system_prompt="You are an assistant")

        # Verify system prompt was prepended
        call_args = provider.client.text_generation.call_args
        prompt_used = call_args.kwargs.get("prompt", "")
        assert "You are an assistant" in prompt_used
        assert "Help me" in prompt_used

    def test_generate_with_config_override(self, provider):
        """Test generation with config override"""
        provider.client.text_generation.return_value = "Response"

        custom_config = GenerationConfig(temperature=0.1, max_tokens=100)
        provider.generate("Test", config=custom_config)

        call_args = provider.client.text_generation.call_args
        assert call_args.kwargs["max_new_tokens"] == 100
        assert call_args.kwargs["temperature"] == 0.1

    def test_generate_response_time(self, provider):
        """Test that response time is tracked"""
        provider.client.text_generation.return_value = "Response"

        result = provider.generate("Test")

        assert result.response_time >= 0
        assert isinstance(result.response_time, float)

    def test_generate_tokens_estimated(self, provider):
        """Test that token count is estimated"""
        # Response of 100 chars should estimate ~25 tokens
        provider.client.text_generation.return_value = "x" * 100

        result = provider.generate("Test")

        assert result.tokens_used == 25  # 100 / 4

    def test_generate_batch(self, provider):
        """Test batch generation"""
        provider.client.text_generation.return_value = "Response"

        results = provider.generate_batch(["Prompt 1", "Prompt 2", "Prompt 3"])

        assert len(results) == 3
        assert all(r.text == "Response" for r in results)
        assert provider.client.text_generation.call_count == 3

    def test_provider_type(self, provider):
        """Test provider type is correct"""
        assert provider.provider_type == ProviderType.HUGGINGFACE

    def test_is_available_success(self, provider):
        """Test availability check when API works"""
        provider.client.text_generation.return_value = "test"

        result = provider.is_available()

        assert result is True

    def test_is_available_failure(self, provider):
        """Test availability check when API fails"""
        provider.client.text_generation.side_effect = Exception("API Error")

        result = provider.is_available()

        assert result is False

    def test_get_model_info(self, provider):
        """Test getting model information"""
        info = provider.get_model_info()

        assert "model" in info or "provider" in info
        assert "huggingface" in str(info).lower() or "meta-llama" in str(info).lower()


class TestHuggingFaceProviderConfig:
    """Test HuggingFace provider configuration"""

    def test_default_config(self):
        """Test default configuration values"""
        with patch("llm_evaluator.providers.huggingface_provider.InferenceClient"):
            provider = HuggingFaceProvider()

            assert provider.config.temperature == 0.7
            assert provider.config.max_tokens == 512  # Actual default

    def test_custom_temperature(self):
        """Test custom temperature setting"""
        with patch("llm_evaluator.providers.huggingface_provider.InferenceClient"):
            config = GenerationConfig(temperature=0.0)
            provider = HuggingFaceProvider(config=config)

            assert provider.config.temperature == 0.0

    def test_custom_max_tokens(self):
        """Test custom max_tokens setting"""
        with patch("llm_evaluator.providers.huggingface_provider.InferenceClient"):
            config = GenerationConfig(max_tokens=2000)
            provider = HuggingFaceProvider(config=config)

            assert provider.config.max_tokens == 2000


class TestHuggingFaceProviderErrors:
    """Test HuggingFace provider error handling"""

    @pytest.fixture
    def provider(self):
        """Create provider with mocked client"""
        with patch("llm_evaluator.providers.huggingface_provider.InferenceClient") as mock:
            mock_client = MagicMock()
            mock.return_value = mock_client
            provider = HuggingFaceProvider(model="meta-llama/Meta-Llama-3-8B-Instruct")
            return provider

    def test_generate_exception_handling(self, provider):
        """Test that exceptions are properly handled"""
        provider.client.text_generation.side_effect = Exception("Network error")

        with pytest.raises(Exception):
            provider.generate("Test")
