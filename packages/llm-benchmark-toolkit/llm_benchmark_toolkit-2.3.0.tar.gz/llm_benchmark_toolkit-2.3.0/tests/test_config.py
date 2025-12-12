"""
Tests for configuration module

Tests EvaluatorConfig, BenchmarkConfig, and OllamaConfig classes.
"""

from pathlib import Path

from llm_evaluator.config import BenchmarkConfig, EvaluatorConfig, OllamaConfig


class TestEvaluatorConfig:
    """Test EvaluatorConfig class"""

    def test_default_values(self):
        """Test that default values are set correctly"""
        config = EvaluatorConfig()

        assert config.default_model == "llama3.2:1b"
        assert config.default_provider == "ollama"
        assert config.default_temperature == 0.7
        assert config.default_max_tokens == 500
        assert config.default_timeout == 30
        assert config.default_retry_attempts == 3

    def test_custom_model(self):
        """Test setting custom model"""
        config = EvaluatorConfig(default_model="gpt-4")
        assert config.default_model == "gpt-4"

    def test_custom_provider(self):
        """Test setting custom provider"""
        config = EvaluatorConfig(default_provider="openai")
        assert config.default_provider == "openai"

    def test_temperature_bounds(self):
        """Test temperature validation"""
        # Valid temperatures
        config = EvaluatorConfig(default_temperature=0.0)
        assert config.default_temperature == 0.0

        config = EvaluatorConfig(default_temperature=2.0)
        assert config.default_temperature == 2.0

    def test_max_tokens_positive(self):
        """Test max_tokens must be positive"""
        config = EvaluatorConfig(default_max_tokens=100)
        assert config.default_max_tokens == 100

    def test_timeout_positive(self):
        """Test timeout must be positive"""
        config = EvaluatorConfig(default_timeout=60)
        assert config.default_timeout == 60

    def test_retry_attempts_bounds(self):
        """Test retry_attempts within bounds"""
        config = EvaluatorConfig(default_retry_attempts=5)
        assert config.default_retry_attempts == 5

    def test_performance_samples(self):
        """Test performance_samples setting"""
        config = EvaluatorConfig(performance_samples=50)
        assert config.performance_samples == 50

    def test_log_level(self):
        """Test log level setting"""
        config = EvaluatorConfig(log_level="DEBUG")
        assert config.log_level == "DEBUG"

        config = EvaluatorConfig(log_level="ERROR")
        assert config.log_level == "ERROR"

    def test_output_dir_path(self):
        """Test output_dir is Path object"""
        config = EvaluatorConfig()
        assert isinstance(config.output_dir, Path)

    def test_environment_settings(self):
        """Test environment setting"""
        config = EvaluatorConfig(environment="prod")
        assert config.environment == "prod"


class TestBenchmarkConfig:
    """Test BenchmarkConfig class"""

    def test_default_values(self):
        """Test default benchmark config values"""
        config = BenchmarkConfig()

        assert config.use_demo_benchmarks is True
        assert config.mmlu_subset is None
        assert config.cache_dir is not None

    def test_use_demo_benchmarks(self):
        """Test use_demo_benchmarks toggle"""
        config = BenchmarkConfig(use_demo_benchmarks=False)
        assert config.use_demo_benchmarks is False

    def test_mmlu_subset(self):
        """Test MMLU subset setting"""
        config = BenchmarkConfig(mmlu_subset="abstract_algebra")
        assert config.mmlu_subset == "abstract_algebra"

    def test_cache_dir_is_path(self):
        """Test cache_dir is a Path"""
        config = BenchmarkConfig()
        assert config.cache_dir is None or isinstance(config.cache_dir, Path)


class TestOllamaConfig:
    """Test OllamaConfig class"""

    def test_default_values(self):
        """Test default Ollama config values"""
        config = OllamaConfig()

        assert config.base_url == "http://localhost:11434"
        assert config.pull_missing_models is False
        assert config.keep_alive is None

    def test_custom_base_url(self):
        """Test custom base URL"""
        config = OllamaConfig(base_url="http://192.168.1.100:11434")
        assert config.base_url == "http://192.168.1.100:11434"

    def test_pull_missing_models(self):
        """Test pull_missing_models toggle"""
        config = OllamaConfig(pull_missing_models=True)
        assert config.pull_missing_models is True

    def test_keep_alive(self):
        """Test keep_alive setting"""
        config = OllamaConfig(keep_alive="5m")
        assert config.keep_alive == "5m"


class TestConfigIntegration:
    """Integration tests for config classes"""

    def test_evaluator_config_serialization(self):
        """Test config can be serialized to dict"""
        config = EvaluatorConfig()

        # Should be able to dump to dict
        if hasattr(config, "model_dump"):
            data = config.model_dump()
        else:
            data = config.dict()

        assert isinstance(data, dict)
        assert "default_model" in data
        assert "default_provider" in data

    def test_benchmark_config_serialization(self):
        """Test benchmark config serialization"""
        config = BenchmarkConfig()

        if hasattr(config, "model_dump"):
            data = config.model_dump()
        else:
            data = config.dict()

        assert isinstance(data, dict)
        assert "use_demo_benchmarks" in data

    def test_ollama_config_serialization(self):
        """Test Ollama config serialization"""
        config = OllamaConfig()

        if hasattr(config, "model_dump"):
            data = config.model_dump()
        else:
            data = config.dict()

        assert isinstance(data, dict)
        assert "base_url" in data

    def test_configs_are_independent(self):
        """Test that config instances are independent"""
        config1 = EvaluatorConfig(default_model="model1")
        config2 = EvaluatorConfig(default_model="model2")

        assert config1.default_model != config2.default_model
        assert config1.default_model == "model1"
        assert config2.default_model == "model2"
