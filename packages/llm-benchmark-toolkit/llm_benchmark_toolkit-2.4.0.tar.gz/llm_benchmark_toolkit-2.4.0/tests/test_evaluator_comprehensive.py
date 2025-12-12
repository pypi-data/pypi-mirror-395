"""
Comprehensive tests for ModelEvaluator - covering uncovered code paths
"""

import os
import tempfile
from unittest.mock import Mock, patch


class TestEvaluatorEvaluateAllWithErrors:
    """Test evaluate_all method with various error conditions"""

    def test_evaluate_all_with_performance_error(self):
        """Test evaluate_all handles performance evaluation errors"""
        from llm_evaluator.evaluator import ModelEvaluator
        from llm_evaluator.providers.base import GenerationConfig, ProviderError

        mock_provider = Mock()
        mock_provider.model = "test-model"
        mock_provider.config = GenerationConfig()

        evaluator = ModelEvaluator(mock_provider)

        # Mock evaluate_performance to raise error
        with patch.object(
            evaluator, "evaluate_performance", side_effect=ProviderError("API Error")
        ):
            with patch.object(
                evaluator,
                "evaluate_quality",
                return_value={"accuracy": 0.8, "coherence_score": 0.9, "hallucination_rate": 0.1},
            ):
                result = evaluator.evaluate_all()

                # Should still return results with default perf values
                assert result.avg_response_time == 0.0
                assert "Performance: API Error" in result.detailed_metrics.errors

    def test_evaluate_all_with_quality_error(self):
        """Test evaluate_all handles quality evaluation errors"""
        from llm_evaluator.evaluator import ModelEvaluator
        from llm_evaluator.providers.base import GenerationConfig, ProviderError

        mock_provider = Mock()
        mock_provider.model = "test-model"
        mock_provider.config = GenerationConfig()

        evaluator = ModelEvaluator(mock_provider)

        # Mock evaluate_quality to raise error
        with patch.object(
            evaluator,
            "evaluate_performance",
            return_value={"avg_response_time": 0.5, "tokens_per_second": 100},
        ):
            with patch.object(
                evaluator, "evaluate_quality", side_effect=ProviderError("Quality Error")
            ):
                result = evaluator.evaluate_all()

                # Should return results with default quality values
                assert result.accuracy == 0.0
                assert result.hallucination_rate == 1.0
                assert "Quality: Quality Error" in result.detailed_metrics.errors


class TestEvaluatorGenerateReport:
    """Test report generation"""

    def test_generate_report_creates_file(self):
        """Test generate_report creates markdown file"""
        from llm_evaluator.evaluator import DetailedMetrics, EvaluationResults, ModelEvaluator
        from llm_evaluator.providers.base import GenerationConfig

        mock_provider = Mock()
        mock_provider.model = "test-model"
        mock_provider.config = GenerationConfig()

        evaluator = ModelEvaluator(mock_provider)

        results = EvaluationResults(
            model_name="test-model",
            accuracy=0.9,
            avg_response_time=0.5,
            token_efficiency=100,
            hallucination_rate=0.1,
            coherence_score=0.85,
            overall_score=0.8,
            detailed_metrics=DetailedMetrics(
                performance={"avg_response_time": 0.5},
                quality={"accuracy": 0.9},
                benchmarks={},
                errors=[],
            ),
            system_info={},
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "report.md")
            evaluator.generate_report(results, output_path)

            assert os.path.exists(output_path)
            with open(output_path, "r") as f:
                content = f.read()
            assert "test-model" in content
            assert "0.9" in content or "90" in content

    def test_generate_report_with_errors(self):
        """Test generate_report includes error section"""
        from llm_evaluator.evaluator import DetailedMetrics, EvaluationResults, ModelEvaluator
        from llm_evaluator.providers.base import GenerationConfig

        mock_provider = Mock()
        mock_provider.model = "test-model"
        mock_provider.config = GenerationConfig()

        evaluator = ModelEvaluator(mock_provider)

        results = EvaluationResults(
            model_name="test-model",
            accuracy=0.9,
            avg_response_time=0.5,
            token_efficiency=100,
            hallucination_rate=0.1,
            coherence_score=0.85,
            overall_score=0.8,
            detailed_metrics=DetailedMetrics(
                performance={}, quality={}, benchmarks={}, errors=["Error 1", "Error 2"]
            ),
            system_info={},
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "report.md")
            evaluator.generate_report(results, output_path)

            with open(output_path, "r") as f:
                content = f.read()
            assert "Error" in content or "error" in content


class TestEvaluatorScoreCalculations:
    """Test score calculation logic"""

    def test_overall_score_formula(self):
        """Test overall score calculation formula"""
        from llm_evaluator.evaluator import ModelEvaluator
        from llm_evaluator.providers.base import GenerationConfig

        mock_provider = Mock()
        mock_provider.model = "test-model"
        mock_provider.config = GenerationConfig()

        evaluator = ModelEvaluator(mock_provider)

        with patch.object(
            evaluator,
            "evaluate_performance",
            return_value={"avg_response_time": 0.5, "tokens_per_second": 100},  # Fast = good score
        ):
            with patch.object(
                evaluator,
                "evaluate_quality",
                return_value={
                    "accuracy": 1.0,
                    "coherence_score": 1.0,
                    "hallucination_rate": 0.0,  # No hallucinations = good
                },
            ):
                result = evaluator.evaluate_all()

                # With perfect metrics, overall score should be high
                assert result.overall_score > 0.8

    def test_speed_score_normalization(self):
        """Test speed score normalizes correctly"""
        from llm_evaluator.evaluator import ModelEvaluator
        from llm_evaluator.providers.base import GenerationConfig

        mock_provider = Mock()
        mock_provider.model = "test-model"
        mock_provider.config = GenerationConfig()

        evaluator = ModelEvaluator(mock_provider)

        # Very slow response time
        with patch.object(
            evaluator,
            "evaluate_performance",
            return_value={"avg_response_time": 10.0, "tokens_per_second": 10},  # Very slow
        ):
            with patch.object(
                evaluator,
                "evaluate_quality",
                return_value={"accuracy": 0.5, "coherence_score": 0.5, "hallucination_rate": 0.5},
            ):
                result = evaluator.evaluate_all()

                # Score should still be calculated
                assert 0 <= result.overall_score <= 1


class TestEvaluatorEvaluatePerformance:
    """Test performance evaluation methods"""

    def test_evaluate_performance_returns_dict(self):
        """Test evaluate_performance returns proper dict"""
        from llm_evaluator.evaluator import ModelEvaluator
        from llm_evaluator.providers.base import GenerationConfig, GenerationResult

        mock_provider = Mock()
        mock_provider.model = "test-model"
        mock_provider.config = GenerationConfig()

        # Mock generate to return proper result
        gen_result = GenerationResult(
            text="Test response", response_time=0.5, tokens_used=50, model="test-model", metadata={}
        )
        mock_provider.generate.return_value = gen_result

        # Mock generate_batch to return list
        mock_provider.generate_batch.return_value = [gen_result, gen_result, gen_result]

        evaluator = ModelEvaluator(mock_provider)
        result = evaluator.evaluate_performance()

        assert isinstance(result, dict)
        assert "avg_response_time" in result


class TestEvaluatorEvaluateQuality:
    """Test quality evaluation methods"""

    def test_evaluate_quality_returns_dict(self):
        """Test evaluate_quality returns proper dict"""
        from llm_evaluator.evaluator import ModelEvaluator
        from llm_evaluator.providers.base import GenerationConfig, GenerationResult

        mock_provider = Mock()
        mock_provider.model = "test-model"
        mock_provider.config = GenerationConfig()
        mock_provider.generate.return_value = GenerationResult(
            text="Paris is the capital of France.",
            response_time=0.5,
            tokens_used=10,
            model="test-model",
            metadata={},
        )

        evaluator = ModelEvaluator(mock_provider)
        result = evaluator.evaluate_quality()

        assert isinstance(result, dict)
        assert "accuracy" in result
        assert "coherence_score" in result
        assert "hallucination_rate" in result


class TestDetailedMetrics:
    """Test DetailedMetrics dataclass"""

    def test_detailed_metrics_creation(self):
        """Test creating DetailedMetrics"""
        from llm_evaluator.evaluator import DetailedMetrics

        dm = DetailedMetrics(
            performance={"key": "value"},
            quality={"key2": "value2"},
            benchmarks={"bench": 0.5},
            errors=["error1"],
        )

        assert dm.performance == {"key": "value"}
        assert dm.quality == {"key2": "value2"}
        assert dm.benchmarks == {"bench": 0.5}
        assert "error1" in dm.errors

    def test_detailed_metrics_empty(self):
        """Test creating empty DetailedMetrics"""
        from llm_evaluator.evaluator import DetailedMetrics

        dm = DetailedMetrics(performance={}, quality={}, benchmarks={}, errors=[])

        assert dm.performance == {}
        assert len(dm.errors) == 0


class TestEvaluationResults:
    """Test EvaluationResults dataclass"""

    def test_evaluation_results_creation(self):
        """Test creating EvaluationResults"""
        from llm_evaluator.evaluator import DetailedMetrics, EvaluationResults

        results = EvaluationResults(
            model_name="model",
            accuracy=0.9,
            avg_response_time=0.5,
            token_efficiency=100,
            hallucination_rate=0.1,
            coherence_score=0.85,
            overall_score=0.8,
            detailed_metrics=DetailedMetrics({}, {}, {}, []),
            system_info={},
        )

        assert results.model_name == "model"
        assert results.accuracy == 0.9
        assert results.overall_score == 0.8


class TestAcademicEvaluationResults:
    """Test AcademicEvaluationResults dataclass"""

    def test_academic_results_creation(self):
        """Test creating AcademicEvaluationResults"""
        from llm_evaluator.evaluator import AcademicEvaluationResults

        results = AcademicEvaluationResults(
            model_name="model",
            mmlu_accuracy=0.7,
            mmlu_ci=(0.65, 0.75),
            mmlu_se=0.02,
            mmlu_n=100,
            truthfulqa_accuracy=0.6,
            truthfulqa_ci=(0.55, 0.65),
            truthfulqa_se=0.02,
            truthfulqa_n=100,
            hellaswag_accuracy=0.8,
            hellaswag_ci=(0.75, 0.85),
            hellaswag_se=0.02,
            hellaswag_n=100,
            average_accuracy=0.7,
            baseline_comparison={},
            reproducibility_manifest={},
            elapsed_time=10.0,
            timestamp="",
        )

        assert results.model_name == "model"
        assert results.mmlu_accuracy == 0.7
        assert results.average_accuracy == 0.7

    def test_academic_results_to_dict(self):
        """Test AcademicEvaluationResults.to_dict method"""
        from llm_evaluator.evaluator import AcademicEvaluationResults

        results = AcademicEvaluationResults(
            model_name="test-model",
            mmlu_accuracy=0.7,
            mmlu_ci=(0.65, 0.75),
            mmlu_se=0.02,
            mmlu_n=100,
            truthfulqa_accuracy=0.6,
            truthfulqa_ci=(0.55, 0.65),
            truthfulqa_se=0.02,
            truthfulqa_n=100,
            hellaswag_accuracy=0.8,
            hellaswag_ci=(0.75, 0.85),
            hellaswag_se=0.02,
            hellaswag_n=100,
            average_accuracy=0.7,
            baseline_comparison={},
            reproducibility_manifest={},
            elapsed_time=10.0,
            timestamp="2024-01-01",
        )

        d = results.to_dict()

        assert d["model_name"] == "test-model"
        assert d["mmlu"]["accuracy"] == 0.7
        assert d["truthfulqa"]["accuracy"] == 0.6
        assert d["hellaswag"]["accuracy"] == 0.8
        assert d["average_accuracy"] == 0.7
