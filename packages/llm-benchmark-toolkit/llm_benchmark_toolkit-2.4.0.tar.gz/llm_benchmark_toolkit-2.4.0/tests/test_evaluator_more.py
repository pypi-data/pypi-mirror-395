"""
More extended tests for ModelEvaluator - focus on uncovered methods
"""

from unittest.mock import Mock, patch

import pytest

from llm_evaluator.providers.base import GenerationConfig, GenerationResult, ProviderError


class TestEvaluatePerformance:
    """Test evaluate_performance method"""

    @pytest.fixture
    def mock_provider(self):
        """Create mock provider with batch support"""
        provider = Mock()
        provider.model = "test-model"
        provider.config = GenerationConfig()

        # Create batch response
        provider.generate_batch.return_value = [
            GenerationResult(
                text="Response text here with some content.",
                response_time=0.5,
                tokens_used=20,
                model="test-model",
                metadata={},
            )
            for _ in range(5)
        ]

        return provider

    def test_evaluate_performance_basic(self, mock_provider):
        """Test basic performance evaluation"""
        from llm_evaluator.evaluator import ModelEvaluator

        evaluator = ModelEvaluator(provider=mock_provider)
        result = evaluator.evaluate_performance(num_samples=5)

        assert "avg_response_time" in result
        assert "min_response_time" in result
        assert "max_response_time" in result
        assert "avg_tokens_per_response" in result

    def test_evaluate_performance_calculates_tokens_per_second(self, mock_provider):
        """Test tokens per second calculation"""
        from llm_evaluator.evaluator import ModelEvaluator

        evaluator = ModelEvaluator(provider=mock_provider)
        result = evaluator.evaluate_performance(num_samples=5)

        assert result["tokens_per_second"] > 0


class TestEvaluateQuality:
    """Test evaluate_quality method"""

    @pytest.fixture
    def mock_provider(self):
        """Create mock provider"""
        provider = Mock()
        provider.model = "test-model"
        provider.config = GenerationConfig()

        # Generate returns correct answers
        provider.generate.return_value = GenerationResult(
            text="The answer is 8. This is correct.",
            response_time=0.5,
            tokens_used=10,
            model="test-model",
            metadata={},
        )

        return provider

    def test_evaluate_quality_basic(self, mock_provider):
        """Test basic quality evaluation"""
        from llm_evaluator.evaluator import ModelEvaluator

        evaluator = ModelEvaluator(provider=mock_provider)
        result = evaluator.evaluate_quality()

        assert "accuracy" in result
        assert "coherence_score" in result
        assert "hallucination_rate" in result

    def test_evaluate_quality_with_custom_test_set(self, mock_provider):
        """Test quality evaluation with custom test set"""
        from llm_evaluator.evaluator import ModelEvaluator

        evaluator = ModelEvaluator(provider=mock_provider)

        test_set = [{"prompt": "What is 1+1?", "expected": "2"}]

        result = evaluator.evaluate_quality(test_set=test_set)

        assert isinstance(result, dict)


class TestEvaluateAll:
    """Test evaluate_all method"""

    @pytest.fixture
    def mock_provider(self):
        """Create mock provider"""
        provider = Mock()
        provider.model = "test-model"
        provider.config = GenerationConfig()

        provider.generate.return_value = GenerationResult(
            text="Test response with good content.",
            response_time=0.5,
            tokens_used=15,
            model="test-model",
            metadata={},
        )

        provider.generate_batch.return_value = [
            GenerationResult(
                text="Response", response_time=0.5, tokens_used=10, model="test-model", metadata={}
            )
            for _ in range(5)
        ]

        return provider

    @patch("llm_evaluator.system_info.collect_system_info")
    def test_evaluate_all_returns_results(self, mock_collect, mock_provider):
        """Test evaluate_all returns EvaluationResults"""
        from llm_evaluator.evaluator import EvaluationResults, ModelEvaluator
        from llm_evaluator.system_info import SystemInfo

        mock_collect.return_value = SystemInfo(
            cpu_model="Test CPU",
            cpu_cores=4,
            cpu_threads=8,
            ram_total_gb=16.0,
            gpu_info=None,
            gpu_vram_gb=None,
            os_name="Windows",
            os_version="11",
            python_version="3.11",
            ollama_version=None,
            timestamp="2024-01-01",
        )

        evaluator = ModelEvaluator(provider=mock_provider)

        # Suppress print output
        with patch("builtins.print"):
            result = evaluator.evaluate_all()

        assert isinstance(result, EvaluationResults)
        assert result.model_name == "test-model"


class TestEvaluatorErrorHandling:
    """Test error handling in evaluator"""

    @pytest.fixture
    def failing_provider(self):
        """Create provider that raises errors"""
        provider = Mock()
        provider.model = "failing-model"
        provider.config = GenerationConfig()
        provider.generate.side_effect = ProviderError("Generation failed")
        provider.generate_batch.side_effect = ProviderError("Batch failed")

        return provider

    def test_evaluate_performance_error(self, failing_provider):
        """Test performance evaluation handles errors"""
        from llm_evaluator.evaluator import ModelEvaluator

        evaluator = ModelEvaluator(provider=failing_provider)

        with pytest.raises(ProviderError):
            evaluator.evaluate_performance()

    def test_evaluate_quality_error(self, failing_provider):
        """Test quality evaluation handles errors"""
        from llm_evaluator.evaluator import ModelEvaluator

        evaluator = ModelEvaluator(provider=failing_provider)

        with pytest.raises(ProviderError):
            evaluator.evaluate_quality()


class TestEvaluatorWithConfig:
    """Test evaluator with custom config"""

    def test_evaluator_uses_provided_config(self):
        """Test evaluator uses provided GenerationConfig"""
        from llm_evaluator.evaluator import ModelEvaluator
        from llm_evaluator.providers.base import GenerationConfig

        config = GenerationConfig(temperature=0.5, max_tokens=100)

        provider = Mock()
        provider.model = "test"
        provider.config = config

        evaluator = ModelEvaluator(provider=provider, config=config)

        assert evaluator.config.temperature == 0.5
        assert evaluator.config.max_tokens == 100


class TestAcademicEvaluationResultsMethods:
    """Test AcademicEvaluationResults methods"""

    def test_to_dict_complete(self):
        """Test to_dict returns complete structure"""
        from llm_evaluator.evaluator import AcademicEvaluationResults

        results = AcademicEvaluationResults(
            model_name="test",
            mmlu_accuracy=0.75,
            mmlu_ci=(0.70, 0.80),
            mmlu_se=0.025,
            mmlu_n=100,
            truthfulqa_accuracy=0.65,
            truthfulqa_ci=(0.60, 0.70),
            truthfulqa_se=0.025,
            truthfulqa_n=50,
            hellaswag_accuracy=0.70,
            hellaswag_ci=(0.65, 0.75),
            hellaswag_se=0.025,
            hellaswag_n=200,
            average_accuracy=0.70,
            baseline_comparison={"gpt4": 0.86},
            reproducibility_manifest={"seed": 42},
            elapsed_time=120.0,
            timestamp="2024-01-01",
        )

        d = results.to_dict()

        assert d["model_name"] == "test"
        assert d["mmlu"]["accuracy"] == 0.75
        assert d["truthfulqa"]["n_samples"] == 50
        assert d["hellaswag"]["standard_error"] == 0.025
        assert d["average_accuracy"] == 0.70
