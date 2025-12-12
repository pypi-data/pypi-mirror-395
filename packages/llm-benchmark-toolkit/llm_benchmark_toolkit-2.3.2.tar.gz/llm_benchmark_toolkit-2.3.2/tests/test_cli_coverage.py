"""
Additional CLI tests to improve coverage

Tests for command execution, provider creation, error handling, and CLI commands.
"""

import os
from unittest.mock import Mock, patch

import click.testing
import pytest

from llm_evaluator.cli import (
    cli,
    create_provider,
    detect_provider_from_env,
    echo_error,
    echo_info,
    echo_success,
    echo_warning,
)


@pytest.fixture
def runner():
    """Create CLI test runner"""
    return click.testing.CliRunner()


@pytest.fixture
def mock_ollama_provider():
    """Mock Ollama provider"""
    provider = Mock()
    provider.model = "llama3.2:1b"
    provider.generate.return_value = Mock(text="Test response")
    provider.is_available.return_value = True
    return provider


class TestDetectProviderFromEnv:
    """Test provider auto-detection from environment"""

    def test_detect_gemini(self):
        """Test Gemini detection from GEMINI_API_KEY"""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=True):
            provider, model = detect_provider_from_env()
            assert provider == "gemini"
            assert model == "gemini-2.5-flash"

    def test_detect_gemini_google_key(self):
        """Test Gemini detection from GOOGLE_API_KEY"""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}, clear=True):
            provider, model = detect_provider_from_env()
            assert provider == "gemini"
            assert model == "gemini-2.5-flash"

    def test_priority_gemini_over_openai(self):
        """Test that Gemini has priority over OpenAI"""
        with patch.dict(
            os.environ, {"GEMINI_API_KEY": "gemini-key", "OPENAI_API_KEY": "openai-key"}, clear=True
        ):
            provider, model = detect_provider_from_env()
            assert provider == "gemini"


class TestCreateProvider:
    """Test provider creation"""

    def test_create_gemini_provider(self):
        """Test Gemini provider creation"""
        with (
            patch("llm_evaluator.cli.HAS_GEMINI", True),
            patch("llm_evaluator.cli.GeminiProvider") as mock_provider,
        ):
            create_provider("gemini-2.5-flash", "gemini", api_key="test-key")
            mock_provider.assert_called_once_with(model="gemini-2.5-flash", api_key="test-key")

    def test_create_groq_provider(self):
        """Test Groq provider creation"""
        with (
            patch("llm_evaluator.cli.HAS_GROQ", True),
            patch("llm_evaluator.cli.GroqProvider") as mock_provider,
        ):
            create_provider("llama-3.3-70b-versatile", "groq", api_key="test-key")
            mock_provider.assert_called_once()

    def test_create_together_provider(self):
        """Test Together provider creation"""
        with (
            patch("llm_evaluator.cli.HAS_TOGETHER", True),
            patch("llm_evaluator.cli.TogetherProvider") as mock_provider,
        ):
            create_provider("meta-llama/model", "together", api_key="test-key")
            mock_provider.assert_called_once()

    def test_create_fireworks_provider(self):
        """Test Fireworks provider creation"""
        with (
            patch("llm_evaluator.cli.HAS_FIREWORKS", True),
            patch("llm_evaluator.cli.FireworksProvider") as mock_provider,
        ):
            create_provider("llama-v3-8b", "fireworks", api_key="test-key")
            mock_provider.assert_called_once()

    def test_create_provider_with_base_url(self):
        """Test provider creation with custom base URL"""
        with patch("llm_evaluator.cli.OllamaProvider") as mock_provider:
            create_provider("llama3.2", "ollama", base_url="http://custom:11434")
            mock_provider.assert_called_once_with(model="llama3.2", base_url="http://custom:11434")

    def test_create_auto_provider_success(self):
        """Test auto provider creation with detection"""
        with (
            patch("llm_evaluator.cli.detect_provider_from_env") as mock_detect,
            patch("llm_evaluator.cli.create_provider") as mock_create,
        ):
            mock_detect.return_value = ("gemini", "gemini-2.5-flash")
            mock_create.return_value = Mock()

            create_provider("auto", "auto")
            mock_detect.assert_called_once()

    def test_create_auto_provider_no_detection(self):
        """Test auto provider fails when nothing detected"""
        with patch("llm_evaluator.cli.detect_provider_from_env") as mock_detect:
            mock_detect.return_value = (None, None)

            with pytest.raises(SystemExit):
                create_provider("auto", "auto")

    def test_create_gemini_not_installed(self):
        """Test error when Gemini not installed"""
        with patch("llm_evaluator.cli.HAS_GEMINI", False):
            with pytest.raises(SystemExit):
                create_provider("gemini-2.5-flash", "gemini")

    def test_create_groq_not_installed(self):
        """Test error when Groq not installed"""
        with patch("llm_evaluator.cli.HAS_GROQ", False):
            with pytest.raises(SystemExit):
                create_provider("llama-3.3-70b-versatile", "groq")

    def test_create_together_not_installed(self):
        """Test error when Together not installed"""
        with patch("llm_evaluator.cli.HAS_TOGETHER", False):
            with pytest.raises(SystemExit):
                create_provider("model", "together")

    def test_create_fireworks_not_installed(self):
        """Test error when Fireworks not installed"""
        with patch("llm_evaluator.cli.HAS_FIREWORKS", False):
            with pytest.raises(SystemExit):
                create_provider("model", "fireworks")

    def test_create_unknown_provider(self):
        """Test error with unknown provider"""
        with pytest.raises(SystemExit):
            create_provider("model", "unknown_provider")


class TestQuickCommand:
    """Test quick evaluation command"""

    def test_quick_no_provider_detected(self, runner):
        """Test quick command when no provider detected"""
        with patch("llm_evaluator.cli.detect_provider_from_env") as mock_detect:
            mock_detect.return_value = (None, None)

            result = runner.invoke(cli, ["quick"])
            assert result.exit_code != 0
            assert "No provider detected" in result.output

    def test_quick_with_gemini_detected(self, runner):
        """Test quick command with Gemini auto-detected"""
        with (
            patch("llm_evaluator.cli.detect_provider_from_env") as mock_detect,
            patch("llm_evaluator.cli.create_provider") as mock_create,
            patch("llm_evaluator.cli.BenchmarkRunner") as mock_runner,
        ):
            mock_detect.return_value = ("gemini", "gemini-2.5-flash")
            mock_provider = Mock()
            mock_create.return_value = mock_provider

            mock_benchmark = Mock()
            mock_benchmark.run_mmlu.return_value = {"accuracy": 0.75}
            mock_benchmark.run_truthfulqa.return_value = {"accuracy": 0.65}
            mock_benchmark.run_hellaswag.return_value = {"accuracy": 0.80}
            mock_runner.return_value = mock_benchmark

            runner.invoke(cli, ["quick", "-s", "5"])
            assert mock_detect.called

    def test_quick_with_custom_model(self, runner):
        """Test quick command with custom model specified"""
        with (
            patch("llm_evaluator.cli.detect_provider_from_env") as mock_detect,
            patch("llm_evaluator.cli.create_provider") as mock_create,
            patch("llm_evaluator.cli.BenchmarkRunner") as mock_runner,
        ):
            mock_detect.return_value = ("gemini", "gemini-2.5-flash")
            mock_provider = Mock()
            mock_create.return_value = mock_provider

            mock_benchmark = Mock()
            mock_benchmark.run_mmlu.return_value = {"accuracy": 0.75}
            mock_benchmark.run_truthfulqa.return_value = {"accuracy": 0.65}
            mock_benchmark.run_hellaswag.return_value = {"accuracy": 0.80}
            mock_runner.return_value = mock_benchmark

            runner.invoke(cli, ["quick", "--model", "custom-model"])
            mock_create.assert_called()


class TestBenchmarkCommand:
    """Test benchmark command"""

    def test_benchmark_help(self, runner):
        """Test benchmark command help"""
        result = runner.invoke(cli, ["benchmark", "--help"])
        assert result.exit_code == 0
        assert "benchmark" in result.output.lower()


class TestCompareCommand:
    """Test compare command"""

    def test_compare_help(self, runner):
        """Test compare command help"""
        result = runner.invoke(cli, ["compare", "--help"])
        assert result.exit_code == 0


class TestRunCommand:
    """Test run command"""

    def test_run_help(self, runner):
        """Test run command help"""
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0


class TestAcademicCommand:
    """Test academic evaluation command"""

    def test_academic_help(self, runner):
        """Test academic command help"""
        result = runner.invoke(cli, ["academic", "--help"])
        assert result.exit_code == 0


class TestPowerCommand:
    """Test power analysis command"""

    def test_power_command_exists(self, runner):
        """Test power command is accessible"""
        result = runner.invoke(cli, ["power", "--help"])
        assert result.exit_code == 0
        assert "power" in result.output.lower() or "sample" in result.output.lower()


class TestInfoCommand:
    """Test info command"""

    def test_info_command_exists(self, runner):
        """Test info command is accessible"""
        result = runner.invoke(cli, ["info", "--help"])
        assert "info" in result.output.lower() or "system" in result.output.lower()


class TestVersionCommand:
    """Test version command"""

    def test_version_displays_correctly(self, runner):
        """Test version command shows version"""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.output.lower()


class TestEchoFunctions:
    """Test CLI echo functions"""

    def test_echo_functions_callable(self):
        """Test all echo functions are callable"""
        # These should not raise errors
        echo_success("Success message")
        echo_error("Error message")
        echo_warning("Warning message")
        echo_info("Info message")
