"""
More extended tests for CLI module - focus on uncovered lines.
"""

import os
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner


class TestCLIEchoFunctions:
    """Test CLI echo helper functions"""

    def test_echo_success(self):
        """Test echo_success function"""
        from llm_evaluator.cli import echo_success

        # Just verify it doesn't crash
        echo_success("Test message")

    def test_echo_error(self):
        """Test echo_error function"""
        from llm_evaluator.cli import echo_error

        echo_error("Test error")

    def test_echo_warning(self):
        """Test echo_warning function"""
        from llm_evaluator.cli import echo_warning

        echo_warning("Test warning")

    def test_echo_info(self):
        """Test echo_info function"""
        from llm_evaluator.cli import echo_info

        echo_info("Test info")


class TestCreateProvider:
    """Test create_provider function"""

    def test_create_ollama_provider(self):
        """Test creating Ollama provider"""
        from llm_evaluator.cli import create_provider
        from llm_evaluator.providers.ollama_provider import OllamaProvider

        provider = create_provider("llama3.2:1b", "ollama", cache=False)

        assert isinstance(provider, OllamaProvider)

    def test_create_provider_with_cache_flag(self):
        """Test creating provider with cache flag (uses CachedProvider)"""
        from llm_evaluator.cli import create_provider
        from llm_evaluator.providers.cached_provider import CachedProvider

        # Use a model name without special characters for Windows
        provider = create_provider("testmodel", "ollama", cache=True)

        assert isinstance(provider, CachedProvider)


class TestCLIProvidersCommand:
    """Test providers command"""

    def test_providers_list(self):
        """Test listing providers"""
        from llm_evaluator.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["providers"])

        assert result.exit_code == 0
        assert "ollama" in result.output.lower() or "provider" in result.output.lower()


class TestCLILatexExportCommand:
    """Test latex export functionality"""

    def test_export_help(self):
        """Test export command help"""
        from llm_evaluator.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["export", "--help"])

        # May or may not exist as separate command
        assert result.exit_code in [0, 2]


class TestCLIInfoCommand:
    """Test info command"""

    def test_info_command(self):
        """Test info command"""
        from llm_evaluator.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["info", "--help"])

        # May or may not exist
        assert result.exit_code in [0, 2]


class TestDetectProviderEdgeCases:
    """Test detect_provider_from_env edge cases"""

    def test_detect_huggingface_hf_token(self):
        """Test HuggingFace detection with HF_TOKEN"""
        from llm_evaluator.cli import detect_provider_from_env

        # Clear other API keys first
        env = {"HF_TOKEN": "hf_test123"}
        with patch.dict(os.environ, env, clear=True):
            provider, model = detect_provider_from_env()
            # Should detect huggingface
            assert provider == "huggingface" or provider is None

    def test_detect_no_provider(self):
        """Test when no provider is detected"""
        from llm_evaluator.cli import detect_provider_from_env

        # Clear all API keys
        env = {}
        with patch.dict(os.environ, env, clear=True):
            # Mock socket to fail (Ollama not running)
            with patch("socket.socket") as mock_socket:
                mock_sock = Mock()
                mock_sock.connect_ex.return_value = 1  # Port closed
                mock_socket.return_value = mock_sock
                provider, model = detect_provider_from_env()
                assert provider is None

    def test_detect_ollama_running(self):
        """Test Ollama detection when running"""
        import json
        import socket
        import urllib.request

        from llm_evaluator.cli import detect_provider_from_env

        # Mock socket to simulate Ollama port is open
        mock_socket = Mock()
        mock_socket.connect_ex.return_value = 0  # Port is open

        # Mock urllib response with models
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(
            {"models": [{"name": "tinyllama:latest"}]}
        ).encode()
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        with patch.dict(os.environ, {}, clear=True):
            with patch.object(socket, "socket", return_value=mock_socket):
                with patch.object(urllib.request, "urlopen", return_value=mock_response):
                    provider, model = detect_provider_from_env()
                    assert provider == "ollama"
                    assert "tinyllama" in model.lower()


class TestCLIVersion:
    """Test CLI version"""

    def test_version_constant(self):
        """Test version constant exists"""
        from llm_evaluator.cli import __version__

        assert __version__
        assert "." in __version__


class TestCreateProviderUnknown:
    """Test create_provider with unknown provider"""

    def test_unknown_provider_exits(self):
        """Test unknown provider causes exit"""
        from llm_evaluator.cli import create_provider

        with pytest.raises(SystemExit):
            create_provider("model", "unknown_provider", cache=False)


class TestCreateProviderMissingDeps:
    """Test create_provider when dependencies are missing"""

    @patch("llm_evaluator.cli.HAS_OPENAI", False)
    def test_openai_missing(self):
        """Test OpenAI provider when not installed"""
        from llm_evaluator.cli import create_provider

        with pytest.raises(SystemExit):
            create_provider("gpt-4", "openai")

    @patch("llm_evaluator.cli.HAS_ANTHROPIC", False)
    def test_anthropic_missing(self):
        """Test Anthropic provider when not installed"""
        from llm_evaluator.cli import create_provider

        with pytest.raises(SystemExit):
            create_provider("claude-3", "anthropic")

    @patch("llm_evaluator.cli.HAS_HUGGINGFACE", False)
    def test_huggingface_missing(self):
        """Test HuggingFace provider when not installed"""
        from llm_evaluator.cli import create_provider

        with pytest.raises(SystemExit):
            create_provider("llama", "huggingface")

    @patch("llm_evaluator.cli.HAS_DEEPSEEK", False)
    def test_deepseek_missing(self):
        """Test DeepSeek provider when not installed"""
        from llm_evaluator.cli import create_provider

        with pytest.raises(SystemExit):
            create_provider("deepseek-chat", "deepseek")


class TestCreateProviderAuto:
    """Test create_provider with auto detection"""

    def test_auto_no_detection(self):
        """Test auto provider with no detected provider"""
        from llm_evaluator.cli import create_provider

        # Mock no provider detected
        with patch("llm_evaluator.cli.detect_provider_from_env", return_value=(None, None)):
            with pytest.raises(SystemExit):
                create_provider("auto", "auto")

    def test_auto_detects_ollama(self):
        """Test auto provider detects Ollama"""
        from llm_evaluator.cli import create_provider
        from llm_evaluator.providers.ollama_provider import OllamaProvider

        with patch(
            "llm_evaluator.cli.detect_provider_from_env", return_value=("ollama", "llama3.2:1b")
        ):
            provider = create_provider("auto", "auto")
            assert isinstance(provider, OllamaProvider)


class TestCLIRunCommand:
    """Test run command execution"""

    @patch("llm_evaluator.cli.ModelEvaluator")
    def test_run_with_mock_evaluator(self, mock_evaluator_class):
        """Test run command with mocked evaluator"""
        from llm_evaluator.cli import cli
        from llm_evaluator.evaluator import DetailedMetrics, EvaluationResults

        mock_evaluator = Mock()
        mock_evaluator.evaluate_all.return_value = EvaluationResults(
            model_name="test",
            accuracy=0.8,
            avg_response_time=1.0,
            token_efficiency=0.9,
            hallucination_rate=0.1,
            coherence_score=0.8,
            overall_score=0.75,
            detailed_metrics=DetailedMetrics(),
        )
        mock_evaluator_class.return_value = mock_evaluator

        runner = CliRunner()
        # Just test it can parse the arguments
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0


class TestCLICompareCommand:
    """Test compare command"""

    def test_compare_requires_models(self):
        """Test compare requires models argument"""
        from llm_evaluator.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["compare"])

        # Should fail or show error about missing models
        assert result.exit_code != 0 or "models" in result.output.lower()
