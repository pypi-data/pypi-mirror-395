"""
Comprehensive tests for config module - covering uncovered code paths
"""


class TestEvaluatorConfig:
    """Test EvaluatorConfig class"""

    def test_default_values(self):
        """Test EvaluatorConfig default values"""
        from llm_evaluator.config import EvaluatorConfig

        config = EvaluatorConfig()

        assert config.default_model == "llama3.2:1b"
        assert config.default_provider == "ollama"
        assert config.default_temperature == 0.7
        assert config.default_max_tokens == 500
        assert config.default_timeout == 30
        assert config.default_retry_attempts == 3
        assert config.log_level == "INFO"

    def test_custom_values(self):
        """Test EvaluatorConfig with custom values"""
        from llm_evaluator.config import EvaluatorConfig

        config = EvaluatorConfig(
            default_model="gpt-4",
            default_provider="openai",
            default_temperature=0.5,
            default_max_tokens=1000,
            log_level="DEBUG",
        )

        assert config.default_model == "gpt-4"
        assert config.default_provider == "openai"
        assert config.default_temperature == 0.5
        assert config.default_max_tokens == 1000
        assert config.log_level == "DEBUG"


class TestOllamaConfig:
    """Test OllamaConfig class"""

    def test_default_values(self):
        """Test OllamaConfig default values"""
        from llm_evaluator.config import OllamaConfig

        config = OllamaConfig()

        assert config.base_url == "http://localhost:11434"
        assert config.pull_missing_models is False
        assert config.keep_alive is None

    def test_custom_values(self):
        """Test OllamaConfig with custom values"""
        from llm_evaluator.config import OllamaConfig

        config = OllamaConfig(
            base_url="http://custom:11434", pull_missing_models=True, keep_alive="10m"
        )

        assert config.base_url == "http://custom:11434"
        assert config.pull_missing_models is True
        assert config.keep_alive == "10m"


class TestBenchmarkConfig:
    """Test BenchmarkConfig class"""

    def test_default_values(self):
        """Test BenchmarkConfig default values"""
        from llm_evaluator.config import BenchmarkConfig

        config = BenchmarkConfig()

        assert config.use_demo_benchmarks is True
        assert config.mmlu_subset is None

    def test_custom_values(self):
        """Test BenchmarkConfig with custom values"""
        from llm_evaluator.config import BenchmarkConfig

        config = BenchmarkConfig(use_demo_benchmarks=False, mmlu_subset="abstract_algebra")

        assert config.use_demo_benchmarks is False
        assert config.mmlu_subset == "abstract_algebra"


class TestConfigSingletons:
    """Test configuration singleton functions"""

    def test_get_evaluator_config_singleton(self):
        """Test get_evaluator_config returns singleton"""
        from llm_evaluator.config import get_evaluator_config, reset_config

        reset_config()  # Reset first

        config1 = get_evaluator_config()
        config2 = get_evaluator_config()

        assert config1 is config2

    def test_get_ollama_config_singleton(self):
        """Test get_ollama_config returns singleton"""
        from llm_evaluator.config import get_ollama_config, reset_config

        reset_config()

        config1 = get_ollama_config()
        config2 = get_ollama_config()

        assert config1 is config2

    def test_get_benchmark_config_singleton(self):
        """Test get_benchmark_config returns singleton"""
        from llm_evaluator.config import get_benchmark_config, reset_config

        reset_config()

        config1 = get_benchmark_config()
        config2 = get_benchmark_config()

        assert config1 is config2

    def test_reset_config_clears_singletons(self):
        """Test reset_config clears all singletons"""
        from llm_evaluator.config import (
            get_benchmark_config,
            get_evaluator_config,
            get_ollama_config,
            reset_config,
        )

        # Create singletons
        config1 = get_evaluator_config()
        get_ollama_config()
        get_benchmark_config()

        # Reset
        reset_config()

        # New instances should be different
        config2 = get_evaluator_config()
        assert config1 is not config2


class TestConfigValidation:
    """Test config validation"""

    def test_temperature_bounds(self):
        """Test temperature must be between 0 and 2"""
        from llm_evaluator.config import EvaluatorConfig

        # Valid values should work
        config = EvaluatorConfig(default_temperature=0.0)
        assert config.default_temperature == 0.0

        config = EvaluatorConfig(default_temperature=2.0)
        assert config.default_temperature == 2.0

    def test_max_tokens_positive(self):
        """Test max_tokens must be positive"""
        from llm_evaluator.config import EvaluatorConfig

        config = EvaluatorConfig(default_max_tokens=1)
        assert config.default_max_tokens == 1

    def test_retry_attempts_bounds(self):
        """Test retry_attempts must be between 1 and 10"""
        from llm_evaluator.config import EvaluatorConfig

        config = EvaluatorConfig(default_retry_attempts=1)
        assert config.default_retry_attempts == 1

        config = EvaluatorConfig(default_retry_attempts=10)
        assert config.default_retry_attempts == 10


class TestConfigEnvironment:
    """Test config environment settings"""

    def test_environment_values(self):
        """Test valid environment values"""
        from llm_evaluator.config import EvaluatorConfig

        for env in ["dev", "test", "prod"]:
            config = EvaluatorConfig(environment=env)
            assert config.environment == env

    def test_log_level_values(self):
        """Test valid log level values"""
        from llm_evaluator.config import EvaluatorConfig

        for level in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            config = EvaluatorConfig(log_level=level)
            assert config.log_level == level


class TestPydanticVersion:
    """Test pydantic version detection"""

    def test_pydantic_v2_flag_exists(self):
        """Test PYDANTIC_V2 flag exists"""
        from llm_evaluator.config import PYDANTIC_V2

        assert isinstance(PYDANTIC_V2, bool)
