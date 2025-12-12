"""
Tests for full benchmark datasets integration
"""

from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pytest

from llm_evaluator.benchmarks import (
    DATASETS_AVAILABLE,
    BenchmarkRunner,
    load_hellaswag_dataset,
    load_mmlu_dataset,
    load_truthfulqa_dataset,
)
from llm_evaluator.providers import GenerationResult, LLMProvider


class TestFullBenchmarkIntegration:
    """Test full benchmark dataset integration"""

    def test_datasets_library_available(self):
        """Test that datasets library is available"""
        assert DATASETS_AVAILABLE, "datasets library should be installed"

    @pytest.mark.skipif(not DATASETS_AVAILABLE, reason="datasets library not available")
    def test_mmlu_dataset_loads(self):
        """Test MMLU dataset can be loaded"""
        dataset = load_mmlu_dataset()
        assert dataset is not None
        assert "test" in dataset or "validation" in dataset

    @pytest.mark.skipif(not DATASETS_AVAILABLE, reason="datasets library not available")
    def test_truthfulqa_dataset_loads(self):
        """Test TruthfulQA dataset can be loaded"""
        dataset = load_truthfulqa_dataset()
        assert dataset is not None
        assert "validation" in dataset

    @pytest.mark.skipif(not DATASETS_AVAILABLE, reason="datasets library not available")
    def test_hellaswag_dataset_loads(self):
        """Test HellaSwag dataset can be loaded"""
        dataset = load_hellaswag_dataset()
        assert dataset is not None
        assert "validation" in dataset or "test" in dataset


class TestBenchmarkRunnerModes:
    """Test different modes of BenchmarkRunner"""

    @pytest.fixture
    def mock_provider(self) -> Mock:  # type: ignore[misc]
        """Create mock provider"""
        provider = Mock(spec=LLMProvider)
        provider.model = "test-model"
        provider.generate.return_value = GenerationResult(
            text="A) Mitochondria",
            response_time=0.5,
            tokens_used=10,
            model="test-model",
            metadata={"tokens": 10},
        )
        return provider

    def test_runner_initialization_demo_mode(self, mock_provider: Any) -> None:  # type: ignore[misc]
        """Test runner initializes in demo mode"""
        runner = BenchmarkRunner(mock_provider, use_full_datasets=False)
        assert runner.use_full_datasets is False
        # In demo mode, sample_size defaults to None (uses demo questions)
        assert runner.sample_size is None

    def test_runner_initialization_full_mode(self, mock_provider: Any) -> None:  # type: ignore[misc]
        """Test runner initializes in full mode"""
        if not DATASETS_AVAILABLE:
            with pytest.raises(ImportError):
                BenchmarkRunner(mock_provider, use_full_datasets=True)
        else:
            runner = BenchmarkRunner(mock_provider, use_full_datasets=True)
            assert runner.use_full_datasets is True

    def test_runner_initialization_with_sampling(self, mock_provider: Any) -> None:  # type: ignore[misc]
        """Test runner initializes with sampling"""
        if not DATASETS_AVAILABLE:
            with pytest.raises(ImportError):
                BenchmarkRunner(mock_provider, use_full_datasets=True, sample_size=50)
        else:
            runner = BenchmarkRunner(mock_provider, use_full_datasets=True, sample_size=50)
            assert runner.sample_size == 50

    def test_demo_mode_mmlu(self, mock_provider: Any) -> None:  # type: ignore[misc]
        """Test MMLU runs in demo mode"""
        runner = BenchmarkRunner(mock_provider, use_full_datasets=False)
        result = runner.run_mmlu_sample()

        assert "mmlu_accuracy" in result
        assert "questions_tested" in result
        assert result["questions_tested"] == 3  # Demo has 3 questions
        assert result["mode"] == "demo"

    def test_demo_mode_truthfulqa(self, mock_provider: Any) -> None:  # type: ignore[misc]
        """Test TruthfulQA runs in demo mode"""
        runner = BenchmarkRunner(mock_provider, use_full_datasets=False)
        result = runner.run_truthfulqa_sample()

        assert "truthfulness_score" in result
        assert "questions_tested" in result
        assert result["questions_tested"] == 3  # Demo has 3 questions
        assert result["mode"] == "demo"

    def test_demo_mode_hellaswag(self, mock_provider: Any) -> None:  # type: ignore[misc]
        """Test HellaSwag runs in demo mode"""
        runner = BenchmarkRunner(mock_provider, use_full_datasets=False)
        result = runner.run_hellaswag_sample()

        assert "hellaswag_accuracy" in result
        assert "questions_tested" in result
        assert result["questions_tested"] == 2  # Demo has 2 scenarios
        assert result["mode"] == "demo"


class TestFullBenchmarkExecution:
    """Test full benchmark execution (with mocked datasets to avoid long runtime)"""

    @pytest.fixture
    def mock_provider(self) -> Mock:  # type: ignore[misc]
        """Create mock provider"""
        provider = Mock(spec=LLMProvider)
        provider.model = "test-model"
        provider.generate.return_value = GenerationResult(
            text="A",
            response_time=0.5,
            tokens_used=5,
            model="test-model",
            metadata={"tokens": 5},
        )
        return provider

    @pytest.fixture
    def mock_mmlu_dataset(self) -> Dict[str, List[Dict[str, Any]]]:
        """Create mock MMLU dataset"""
        mock_data: List[Dict[str, Any]] = []
        for i in range(10):
            mock_data.append(
                {
                    "question": f"Question {i}",
                    "choices": ["A", "B", "C", "D"],
                    "answer": 0,  # Always A
                    "subject": "test",
                }
            )

        mock_dataset: Dict[str, List[Dict[str, Any]]] = {"test": mock_data}
        return mock_dataset

    @pytest.mark.skipif(not DATASETS_AVAILABLE, reason="datasets library not available")
    @patch("llm_evaluator.benchmarks.load_mmlu_dataset")
    def test_full_mmlu_with_sampling(self, mock_load: Any, mock_provider: Any, mock_mmlu_dataset: Any) -> None:  # type: ignore[misc]
        """Test MMLU full mode with sampling"""
        mock_load.return_value = mock_mmlu_dataset

        runner = BenchmarkRunner(mock_provider, use_full_datasets=True, sample_size=5)
        result = runner.run_mmlu_sample()

        assert "mmlu_accuracy" in result
        assert result["questions_tested"] == 5
        assert result["total_available"] == 10
        assert "sample_5" in str(result["mode"])  # type: ignore[arg-type]

    @pytest.mark.skipif(not DATASETS_AVAILABLE, reason="datasets library not available")
    @patch("llm_evaluator.benchmarks.load_mmlu_dataset")
    def test_full_mmlu_without_sampling(self, mock_load: Any, mock_provider: Any, mock_mmlu_dataset: Any) -> None:  # type: ignore[misc]
        """Test MMLU full mode without sampling (all questions)"""
        mock_load.return_value = mock_mmlu_dataset

        runner = BenchmarkRunner(mock_provider, use_full_datasets=True, sample_size=None)
        result = runner.run_mmlu_sample()

        assert result["questions_tested"] == 10  # All questions
        assert result["mode"] == "full"


class TestBackwardCompatibility:
    """Test that old code still works (backward compatibility)"""

    @pytest.fixture
    def mock_provider(self) -> Mock:  # type: ignore[misc]
        provider = Mock(spec=LLMProvider)
        provider.model = "test-model"
        provider.generate.return_value = GenerationResult(
            text="Mitochondria",
            response_time=0.5,
            tokens_used=10,
            model="test-model",
            metadata={"tokens": 10},
        )
        return provider

    def test_old_initialization_still_works(self, mock_provider: Any) -> None:  # type: ignore[misc]
        """Test that old way of initializing runner still works"""
        # Old way: just provider, no parameters
        # Note: New default is use_full_datasets=True, sample_size=100
        runner = BenchmarkRunner(mock_provider, use_full_datasets=False)

        # Should be in demo mode when explicitly set
        assert runner.use_full_datasets is False

        # Should still work
        result = runner.run_mmlu_sample()
        assert "mmlu_accuracy" in result

    def test_old_run_all_benchmarks_still_works(self, mock_provider: Any) -> None:  # type: ignore[misc]
        """Test that run_all_benchmarks still works"""
        runner = BenchmarkRunner(mock_provider, use_full_datasets=False)
        results = runner.run_all_benchmarks()

        assert "mmlu" in results
        assert "truthfulqa" in results
        assert "hellaswag" in results
        assert "aggregate_benchmark_score" in results
