"""
Extended tests for ModelEvaluator - focus on initialization, chat, and core methods
"""

from unittest.mock import Mock, patch

import pytest


class TestEvaluationResultsDataclass:
    """Test EvaluationResults dataclass"""

    def test_evaluation_results_creation(self):
        """Test creating EvaluationResults"""
        from llm_evaluator.evaluator import DetailedMetrics, EvaluationResults

        results = EvaluationResults(
            model_name="test-model",
            accuracy=0.85,
            avg_response_time=1.5,
            token_efficiency=0.9,
            hallucination_rate=0.1,
            coherence_score=0.8,
            overall_score=0.75,
            detailed_metrics=DetailedMetrics(),
        )

        assert results.model_name == "test-model"
        assert results.accuracy == 0.85
        assert results.avg_response_time == 1.5

    def test_detailed_metrics_defaults(self):
        """Test DetailedMetrics default values"""
        from llm_evaluator.evaluator import DetailedMetrics

        metrics = DetailedMetrics()
        assert metrics.performance == {}
        assert metrics.quality == {}
        assert metrics.benchmarks == {}
        assert metrics.errors == []


class TestAcademicEvaluationResults:
    """Test AcademicEvaluationResults dataclass"""

    def test_academic_results_creation(self):
        """Test creating AcademicEvaluationResults"""
        from llm_evaluator.evaluator import AcademicEvaluationResults

        results = AcademicEvaluationResults(
            model_name="test-model",
            mmlu_accuracy=0.5,
            mmlu_ci=(0.4, 0.6),
            mmlu_se=0.05,
            mmlu_n=100,
            truthfulqa_accuracy=0.6,
            truthfulqa_ci=(0.5, 0.7),
            truthfulqa_se=0.04,
            truthfulqa_n=50,
            hellaswag_accuracy=0.7,
            hellaswag_ci=(0.6, 0.8),
            hellaswag_se=0.03,
            hellaswag_n=200,
            average_accuracy=0.6,
            baseline_comparison={},
            reproducibility_manifest={},
            elapsed_time=120.5,
            timestamp="2024-01-01T00:00:00",
        )

        assert results.model_name == "test-model"
        assert results.mmlu_accuracy == 0.5

    def test_academic_results_to_dict(self):
        """Test to_dict method"""
        from llm_evaluator.evaluator import AcademicEvaluationResults

        results = AcademicEvaluationResults(
            model_name="test-model",
            mmlu_accuracy=0.5,
            mmlu_ci=(0.4, 0.6),
            mmlu_se=0.05,
            mmlu_n=100,
            truthfulqa_accuracy=0.6,
            truthfulqa_ci=(0.5, 0.7),
            truthfulqa_se=0.04,
            truthfulqa_n=50,
            hellaswag_accuracy=0.7,
            hellaswag_ci=(0.6, 0.8),
            hellaswag_se=0.03,
            hellaswag_n=200,
            average_accuracy=0.6,
            baseline_comparison={},
            reproducibility_manifest={},
            elapsed_time=120.5,
            timestamp="2024-01-01T00:00:00",
        )

        d = results.to_dict()

        assert "model_name" in d
        assert "mmlu" in d
        assert d["mmlu"]["accuracy"] == 0.5
        assert d["mmlu"]["confidence_interval_95"] == (0.4, 0.6)


class TestModelEvaluatorInit:
    """Test ModelEvaluator initialization"""

    @pytest.fixture
    def mock_provider(self):
        """Create mock provider"""
        from llm_evaluator.providers.base import GenerationConfig, GenerationResult

        provider = Mock()
        provider.model = "test-model"
        provider.config = GenerationConfig()
        provider.generate.return_value = GenerationResult(
            text="Test response", response_time=0.1, tokens_used=10, model="test-model", metadata={}
        )
        return provider

    def test_init_with_provider(self, mock_provider):
        """Test initialization with custom provider"""
        from llm_evaluator.evaluator import ModelEvaluator

        evaluator = ModelEvaluator(provider=mock_provider)

        assert evaluator.provider is mock_provider

    def test_init_creates_benchmark_runner(self, mock_provider):
        """Test initialization creates benchmark runner"""
        from llm_evaluator.benchmarks import BenchmarkRunner
        from llm_evaluator.evaluator import ModelEvaluator

        evaluator = ModelEvaluator(provider=mock_provider)

        assert isinstance(evaluator.benchmark_runner, BenchmarkRunner)

    def test_init_creates_metrics(self, mock_provider):
        """Test initialization creates metrics instances"""
        from llm_evaluator.evaluator import ModelEvaluator
        from llm_evaluator.metrics import PerformanceMetrics, QualityMetrics

        evaluator = ModelEvaluator(provider=mock_provider)

        assert isinstance(evaluator.performance_metrics, PerformanceMetrics)
        assert isinstance(evaluator.quality_metrics, QualityMetrics)


class TestModelEvaluatorChat:
    """Test ModelEvaluator chat method"""

    @pytest.fixture
    def mock_provider(self):
        """Create mock provider"""
        from llm_evaluator.providers.base import GenerationConfig, GenerationResult

        provider = Mock()
        provider.model = "test-model"
        provider.config = GenerationConfig()
        provider.generate.return_value = GenerationResult(
            text="Hello, I am an AI assistant.",
            response_time=0.5,
            tokens_used=10,
            model="test-model",
            metadata={},
        )
        return provider

    def test_chat_returns_response_and_time(self, mock_provider):
        """Test chat returns response text and time"""
        from llm_evaluator.evaluator import ModelEvaluator

        evaluator = ModelEvaluator(provider=mock_provider)

        text, time = evaluator.chat("Hello")

        assert text == "Hello, I am an AI assistant."
        assert time == 0.5

    def test_chat_calls_provider_generate(self, mock_provider):
        """Test chat calls provider.generate"""
        from llm_evaluator.evaluator import ModelEvaluator

        evaluator = ModelEvaluator(provider=mock_provider)
        evaluator.chat("Test prompt")

        mock_provider.generate.assert_called_once()

    def test_chat_raises_provider_error(self, mock_provider):
        """Test chat propagates ProviderError"""
        from llm_evaluator.evaluator import ModelEvaluator
        from llm_evaluator.providers.base import ProviderError

        mock_provider.generate.side_effect = ProviderError("Generation failed")
        evaluator = ModelEvaluator(provider=mock_provider)

        with pytest.raises(ProviderError):
            evaluator.chat("Test prompt")


class TestModelEvaluatorEvaluation:
    """Test ModelEvaluator evaluation methods"""

    @pytest.fixture
    def mock_provider(self):
        """Create mock provider"""
        from llm_evaluator.providers.base import GenerationConfig, GenerationResult

        provider = Mock()
        provider.model = "test-model"
        provider.config = GenerationConfig()
        provider.generate.return_value = GenerationResult(
            text="Test response with some content here.",
            response_time=0.5,
            tokens_used=10,
            model="test-model",
            metadata={},
        )
        provider.generate_batch.return_value = [
            GenerationResult(
                text="Response", response_time=0.5, tokens_used=10, model="test-model", metadata={}
            )
            for _ in range(10)
        ]
        return provider

    def test_evaluate_performance(self, mock_provider):
        """Test evaluate_performance returns dict"""
        from llm_evaluator.evaluator import ModelEvaluator

        evaluator = ModelEvaluator(provider=mock_provider)

        result = evaluator.evaluate_performance(num_samples=2)

        assert isinstance(result, dict)

    def test_evaluate_quality(self, mock_provider):
        """Test evaluate_quality returns dict"""
        from llm_evaluator.evaluator import ModelEvaluator

        evaluator = ModelEvaluator(provider=mock_provider)

        result = evaluator.evaluate_quality()

        assert isinstance(result, dict)


class TestDetailedMetricsDataclass:
    """Test DetailedMetrics dataclass edge cases"""

    def test_detailed_metrics_with_values(self):
        """Test DetailedMetrics with custom values"""
        from llm_evaluator.evaluator import DetailedMetrics

        metrics = DetailedMetrics(
            performance={"speed": 0.9},
            quality={"coherence": 0.8},
            benchmarks={"mmlu": 0.7},
            errors=["Error 1"],
        )

        assert metrics.performance["speed"] == 0.9
        assert "Error 1" in metrics.errors


class TestEvaluatorWithDefaultProvider:
    """Test evaluator without explicit provider"""

    @patch("llm_evaluator.evaluator.OllamaProvider")
    def test_default_provider_created(self, mock_ollama_class):
        """Test default OllamaProvider is created if no provider given"""
        from llm_evaluator.evaluator import ModelEvaluator

        mock_instance = Mock()
        mock_ollama_class.return_value = mock_instance

        ModelEvaluator()

        mock_ollama_class.assert_called()
