"""
Extended tests for Ollama Provider.

Tests error handling, batch processing, and model info.
"""

from unittest.mock import Mock, patch

import pytest

from llm_evaluator.providers import (
    GenerationConfig,
    ModelNotFoundError,
    ProviderError,
    ProviderType,
)
from llm_evaluator.providers.ollama_provider import OllamaProvider


class TestOllamaProviderGenerate:
    """Extended tests for generate method"""

    def test_generate_with_system_prompt(self):
        """Test generation with system prompt"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.return_value = {
                "message": {"role": "assistant", "content": "Hello!"},
                "eval_count": 10,
                "total_duration": 1000000,
            }
            mock_get_client.return_value = mock_client

            provider.generate("Hi", system_prompt="You are helpful")

            # Verify system prompt was passed
            call_args = mock_client.chat.call_args
            messages = call_args.kwargs.get("messages", call_args[1].get("messages", []))
            assert any(m.get("role") == "system" for m in messages)

    def test_generate_without_system_prompt(self):
        """Test generation without system prompt"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.return_value = {
                "message": {"role": "assistant", "content": "Response"},
                "eval_count": 5,
            }
            mock_get_client.return_value = mock_client

            provider.generate("Test")

            # Verify no system message
            call_args = mock_client.chat.call_args
            messages = call_args.kwargs.get("messages", call_args[1].get("messages", []))
            assert not any(m.get("role") == "system" for m in messages)

    def test_generate_with_config_override(self):
        """Test generation with config override"""
        provider = OllamaProvider(model="llama3.2:1b")
        custom_config = GenerationConfig(temperature=0.1, max_tokens=100)

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.return_value = {
                "message": {"role": "assistant", "content": "Test"},
                "eval_count": 10,
            }
            mock_get_client.return_value = mock_client

            provider.generate("Hello", config=custom_config)

            # Verify config was used
            call_args = mock_client.chat.call_args
            options = call_args.kwargs.get("options", {})
            assert options.get("temperature") == 0.1

    def test_generate_response_metadata(self):
        """Test that metadata is properly extracted"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.return_value = {
                "message": {"role": "assistant", "content": "Test response"},
                "eval_count": 15,
                "total_duration": 2000000000,
                "load_duration": 500000000,
                "prompt_eval_count": 10,
                "eval_duration": 1500000000,
            }
            mock_get_client.return_value = mock_client

            result = provider.generate("Test")

            assert result.metadata["eval_count"] == 15
            assert result.metadata["total_duration"] == 2000000000
            assert result.metadata["prompt_eval_count"] == 10

    def test_generate_response_time_tracked(self):
        """Test that response time is tracked"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.return_value = {
                "message": {"role": "assistant", "content": "Response"},
                "eval_count": 5,
            }
            mock_get_client.return_value = mock_client

            result = provider.generate("Test")

            assert result.response_time >= 0
            assert isinstance(result.response_time, float)


class TestOllamaProviderBatch:
    """Test batch generation"""

    def test_generate_batch_success(self):
        """Test successful batch generation"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.return_value = {
                "message": {"role": "assistant", "content": "Response"},
                "eval_count": 5,
            }
            mock_get_client.return_value = mock_client

            results = provider.generate_batch(["Prompt 1", "Prompt 2", "Prompt 3"])

            assert len(results) == 3
            assert all(r.text == "Response" for r in results)

    def test_generate_batch_partial_failure(self):
        """Test batch with some failures - retries succeed"""
        provider = OllamaProvider(model="llama3.2:1b")

        call_count = [0]

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            # First call for second prompt fails, retry succeeds
            if call_count[0] == 2:
                raise ProviderError(message="Simulated failure")
            return {
                "message": {"role": "assistant", "content": "Success"},
                "eval_count": 5,
            }

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.side_effect = side_effect
            mock_get_client.return_value = mock_client

            results = provider.generate_batch(["P1", "P2", "P3"])

            assert len(results) == 3
            # All should succeed (retry logic handles failure)
            assert all(r.text == "Success" for r in results)

    def test_generate_batch_empty_list(self):
        """Test batch with empty list"""
        provider = OllamaProvider(model="llama3.2:1b")

        results = provider.generate_batch([])

        assert results == []

    def test_generate_batch_with_system_prompt(self):
        """Test batch with system prompt"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.return_value = {
                "message": {"role": "assistant", "content": "Response"},
                "eval_count": 5,
            }
            mock_get_client.return_value = mock_client

            results = provider.generate_batch(["P1", "P2"], system_prompt="Be helpful")

            assert len(results) == 2


class TestOllamaProviderAvailability:
    """Test availability checking"""

    def test_is_available_with_model(self):
        """Test availability when model exists"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_model = Mock()
            mock_model.model = "llama3.2:1b"
            mock_response = Mock()
            mock_response.models = [mock_model]
            mock_client.list.return_value = mock_response
            mock_get_client.return_value = mock_client

            result = provider.is_available()

            assert result is True

    def test_is_available_without_model(self):
        """Test availability when model doesn't exist"""
        provider = OllamaProvider(model="nonexistent-model")

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.models = []
            mock_client.list.return_value = mock_response
            mock_get_client.return_value = mock_client

            result = provider.is_available()

            assert result is False

    def test_is_available_service_down(self):
        """Test availability when Ollama service is down"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_get_client.side_effect = Exception("Connection refused")

            result = provider.is_available()

            assert result is False

    def test_is_available_matches_base_model(self):
        """Test availability matches base model name without tag"""
        provider = OllamaProvider(model="llama3.2")  # Without tag

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_model = Mock()
            mock_model.model = "llama3.2:1b"  # With tag
            mock_response = Mock()
            mock_response.models = [mock_model]
            mock_client.list.return_value = mock_response
            mock_get_client.return_value = mock_client

            result = provider.is_available()

            assert result is True


class TestOllamaProviderModelInfo:
    """Test get_model_info method"""

    def test_get_model_info_success(self):
        """Test getting model info successfully"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.show.return_value = {
                "format": "gguf",
                "details": {
                    "family": "llama",
                    "parameter_size": "1B",
                    "quantization_level": "Q4_K_M",
                },
            }
            mock_get_client.return_value = mock_client

            info = provider.get_model_info()

            assert info["model"] == "llama3.2:1b"
            assert info["family"] == "llama"
            assert info["parameter_size"] == "1B"

    def test_get_model_info_failure(self):
        """Test getting model info when it fails"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.show.side_effect = Exception("Model not found")
            mock_get_client.return_value = mock_client

            info = provider.get_model_info()

            assert info["model"] == "llama3.2:1b"
            assert "error" in info


class TestOllamaProviderType:
    """Test provider type"""

    def test_provider_type(self):
        """Test provider type is correct"""
        provider = OllamaProvider(model="llama3.2:1b")

        assert provider.provider_type == ProviderType.OLLAMA

    def test_get_provider_type_method(self):
        """Test _get_provider_type method"""
        provider = OllamaProvider(model="llama3.2:1b")

        assert provider._get_provider_type() == ProviderType.OLLAMA


class TestOllamaProviderErrorHandling:
    """Test error handling scenarios"""

    def test_model_not_found_error(self):
        """Test ModelNotFoundError is raised"""
        provider = OllamaProvider(model="nonexistent")

        import ollama

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.side_effect = ollama.ResponseError("model 'nonexistent' not found")
            mock_get_client.return_value = mock_client

            with pytest.raises(ModelNotFoundError):
                provider.generate("Test")

    def test_retry_on_failure(self):
        """Test retry logic on transient failures"""
        provider = OllamaProvider(model="llama3.2:1b", config=GenerationConfig(retry_attempts=3))

        call_count = [0]

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] < 3:
                raise Exception("Transient error")
            return {
                "message": {"role": "assistant", "content": "Success"},
                "eval_count": 5,
            }

        with patch.object(provider, "_get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.side_effect = side_effect
            mock_get_client.return_value = mock_client

            with patch("time.sleep"):  # Skip actual sleep
                result = provider.generate("Test")

            assert result.text == "Success"
            assert call_count[0] == 3


class TestOllamaProviderClient:
    """Test client initialization"""

    def test_get_client_default(self):
        """Test default client initialization"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch("llm_evaluator.providers.ollama_provider.ollama"):
            client = provider._get_client()
            assert client is not None

    def test_get_client_custom_url(self):
        """Test client with custom base URL"""
        provider = OllamaProvider(model="llama3.2:1b", base_url="http://192.168.1.100:11434")

        with patch("llm_evaluator.providers.ollama_provider.ollama") as mock_ollama:
            mock_ollama.Client.return_value = Mock()
            provider._get_client()

            mock_ollama.Client.assert_called_once_with(host="http://192.168.1.100:11434")

    def test_get_client_cached(self):
        """Test client is cached after first call"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch("llm_evaluator.providers.ollama_provider.ollama"):
            client1 = provider._get_client()
            client2 = provider._get_client()

            # Should return same client instance
            assert client1 is client2
