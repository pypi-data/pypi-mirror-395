"""
Extended tests for config module - focus on singletons and edge cases
"""


class TestEvaluatorConfigValues:
    """Test EvaluatorConfig default values and validation"""

    def test_default_model_value(self):
        """Test default model is llama3.2:1b"""
        from llm_evaluator.config import EvaluatorConfig

        config = EvaluatorConfig()
        assert config.default_model == "llama3.2:1b"

    def test_default_provider_value(self):
        """Test default provider is ollama"""
        from llm_evaluator.config import EvaluatorConfig

        config = EvaluatorConfig()
        assert config.default_provider == "ollama"

    def test_default_temperature_value(self):
        """Test default temperature is 0.7"""
        from llm_evaluator.config import EvaluatorConfig

        config = EvaluatorConfig()
        assert config.default_temperature == 0.7

    def test_default_max_tokens_value(self):
        """Test default max tokens is 500"""
        from llm_evaluator.config import EvaluatorConfig

        config = EvaluatorConfig()
        assert config.default_max_tokens == 500


class TestOllamaConfigValues:
    """Test OllamaConfig default values"""

    def test_default_base_url(self):
        """Test default Ollama base URL"""
        from llm_evaluator.config import OllamaConfig

        config = OllamaConfig()
        assert config.base_url == "http://localhost:11434"

    def test_pull_missing_models_default(self):
        """Test pull_missing_models default is False"""
        from llm_evaluator.config import OllamaConfig

        config = OllamaConfig()
        assert config.pull_missing_models is False

    def test_keep_alive_default(self):
        """Test keep_alive default is None"""
        from llm_evaluator.config import OllamaConfig

        config = OllamaConfig()
        assert config.keep_alive is None


class TestBenchmarkConfigValues:
    """Test BenchmarkConfig default values"""

    def test_use_demo_benchmarks_default(self):
        """Test use_demo_benchmarks default is True"""
        from llm_evaluator.config import BenchmarkConfig

        config = BenchmarkConfig()
        assert config.use_demo_benchmarks is True

    def test_mmlu_subset_default(self):
        """Test mmlu_subset default is None"""
        from llm_evaluator.config import BenchmarkConfig

        config = BenchmarkConfig()
        assert config.mmlu_subset is None

    def test_cache_dir_default(self):
        """Test cache_dir default is in home directory"""
        from llm_evaluator.config import BenchmarkConfig

        config = BenchmarkConfig()
        assert config.cache_dir is not None
        assert "llm_evaluator" in str(config.cache_dir)


class TestConfigSingletons:
    """Test singleton behavior of config functions"""

    def setup_method(self):
        """Reset config before each test"""
        from llm_evaluator import config

        config.reset_config()

    def test_get_evaluator_config_singleton(self):
        """Test evaluator config returns same instance"""
        from llm_evaluator.config import get_evaluator_config

        config1 = get_evaluator_config()
        config2 = get_evaluator_config()
        assert config1 is config2

    def test_get_ollama_config_singleton(self):
        """Test Ollama config returns same instance"""
        from llm_evaluator.config import get_ollama_config

        config1 = get_ollama_config()
        config2 = get_ollama_config()
        assert config1 is config2

    def test_get_benchmark_config_singleton(self):
        """Test benchmark config returns same instance"""
        from llm_evaluator.config import get_benchmark_config

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

        # Create instances
        eval1 = get_evaluator_config()
        ollama1 = get_ollama_config()
        bench1 = get_benchmark_config()

        # Reset
        reset_config()

        # New instances should be different
        eval2 = get_evaluator_config()
        ollama2 = get_ollama_config()
        bench2 = get_benchmark_config()

        assert eval1 is not eval2
        assert ollama1 is not ollama2
        assert bench1 is not bench2


class TestPydanticVersionHandling:
    """Test PYDANTIC_V2 flag handling"""

    def test_pydantic_version_defined(self):
        """Test PYDANTIC_V2 constant is defined"""
        from llm_evaluator.config import PYDANTIC_V2

        assert isinstance(PYDANTIC_V2, bool)


class TestConfigInstantiation:
    """Test config can be instantiated with custom values"""

    def test_evaluator_config_custom_model(self):
        """Test EvaluatorConfig with custom model"""
        from llm_evaluator.config import EvaluatorConfig

        config = EvaluatorConfig(default_model="gpt-4")
        assert config.default_model == "gpt-4"

    def test_evaluator_config_custom_provider(self):
        """Test EvaluatorConfig with custom provider"""
        from llm_evaluator.config import EvaluatorConfig

        config = EvaluatorConfig(default_provider="openai")
        assert config.default_provider == "openai"

    def test_ollama_config_custom_url(self):
        """Test OllamaConfig with custom URL"""
        from llm_evaluator.config import OllamaConfig

        config = OllamaConfig(base_url="http://remote:11434")
        assert config.base_url == "http://remote:11434"

    def test_benchmark_config_custom_subset(self):
        """Test BenchmarkConfig with custom MMLU subset"""
        from llm_evaluator.config import BenchmarkConfig

        config = BenchmarkConfig(mmlu_subset="abstract_algebra")
        assert config.mmlu_subset == "abstract_algebra"
