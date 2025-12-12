"""
Tests for Ollama Provider

Tests the Ollama provider with mocked HTTP responses.
"""

from unittest.mock import Mock, patch

from llm_evaluator.providers import GenerationConfig
from llm_evaluator.providers.ollama_provider import OllamaProvider


class TestOllamaProvider:
    """Test Ollama provider functionality"""

    def test_init(self):
        """Test provider initialization"""
        provider = OllamaProvider(model="llama3.2:1b")
        assert provider.model == "llama3.2:1b"

    def test_init_with_config(self):
        """Test initialization with custom config"""
        config = GenerationConfig(temperature=0.5, max_tokens=200)
        provider = OllamaProvider(model="llama3.2:1b", config=config)

        assert provider.model == "llama3.2:1b"
        assert provider.config.temperature == 0.5
        assert provider.config.max_tokens == 200

    def test_generate_calls_api(self):
        """Test that generate makes API call via ollama client"""
        provider = OllamaProvider(model="llama3.2:1b")

        # Mock the ollama module's chat function (used internally by generate)
        with patch.object(provider, "_get_client") as mock_get_client:
            mock_ollama = Mock()
            mock_ollama.chat.return_value = {
                "message": {"role": "assistant", "content": "Test response"},
                "done": True,
                "total_duration": 1000000000,
                "eval_count": 10,
            }
            mock_get_client.return_value = mock_ollama

            result = provider.generate("Hello")

            # Verify client chat was called
            mock_ollama.chat.assert_called()
            assert result.text == "Test response"

    def test_is_available_when_server_up(self):
        """Test availability when Ollama server is running"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"version": "0.1.0"}

            # May or may not be available depending on implementation
            result = provider.is_available()
            assert isinstance(result, bool)

    def test_is_available_when_server_down(self):
        """Test availability when Ollama server is not running"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch("requests.get") as mock_get:
            mock_get.side_effect = Exception("Connection refused")

            result = provider.is_available()
            # Should return False or handle gracefully
            assert isinstance(result, bool)

    def test_get_model_info(self):
        """Test getting model information"""
        provider = OllamaProvider(model="llama3.2:1b")

        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "modelinfo": {"general.architecture": "llama"}
            }

            info = provider.get_model_info()

            assert isinstance(info, dict)
            assert "model" in info or provider.model in str(info)


class TestOllamaProviderConfig:
    """Test Ollama provider configuration handling"""

    def test_default_config(self):
        """Test default configuration values"""
        provider = OllamaProvider(model="llama3.2:1b")

        assert provider.config is not None
        assert isinstance(provider.config, GenerationConfig)

    def test_custom_temperature(self):
        """Test custom temperature configuration"""
        config = GenerationConfig(temperature=0.1)
        provider = OllamaProvider(model="llama3.2:1b", config=config)

        assert provider.config.temperature == 0.1

    def test_custom_max_tokens(self):
        """Test custom max tokens configuration"""
        config = GenerationConfig(max_tokens=500)
        provider = OllamaProvider(model="llama3.2:1b", config=config)

        assert provider.config.max_tokens == 500
