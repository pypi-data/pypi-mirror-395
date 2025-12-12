"""
Unit tests for benchmarks module

Refactored for Clean Architecture with provider mocking
"""

import pytest

from llm_evaluator.benchmarks import BenchmarkRunner
from llm_evaluator.providers import ProviderError
from tests.mocks import MockProvider, create_mock_responses


class TestBenchmarkRunner:
    """Test suite for BenchmarkRunner class with dependency injection"""

    def test_init(self):
        """Test BenchmarkRunner initialization with provider"""
        provider = MockProvider(model="test-model")
        runner = BenchmarkRunner(provider=provider)

        assert runner.provider.model == "test-model"

    def test_run_mmlu_sample(self):
        """Test MMLU benchmark execution"""
        provider = MockProvider(model="test-model", responses=create_mock_responses())
        runner = BenchmarkRunner(provider=provider, use_full_datasets=False)

        results = runner.run_mmlu_sample()

        assert "mmlu_accuracy" in results
        assert "questions_tested" in results
        assert "correct" in results
        assert results["questions_tested"] == 3  # Demo has 3 questions
        assert 0.0 <= results["mmlu_accuracy"] <= 1.0

    def test_run_truthfulqa_sample(self):
        """Test TruthfulQA benchmark execution"""
        provider = MockProvider(model="test-model", responses=create_mock_responses())
        runner = BenchmarkRunner(provider=provider, use_full_datasets=False)

        results = runner.run_truthfulqa_sample()

        assert "truthfulness_score" in results
        assert "questions_tested" in results
        assert "correct" in results
        assert results["questions_tested"] == 3  # Demo has 3 questions
        assert 0.0 <= results["truthfulness_score"] <= 1.0

    def test_run_hellaswag_sample(self):
        """Test HellaSwag benchmark execution"""
        provider = MockProvider(
            model="test-model",
            responses={
                # Correct choice is A for both scenarios
                scenario: "A"
                for scenario in [
                    "A man is sitting in a chair. He picks up a book.\n\nWhich is more likely:\nA) He begins reading the book.\nB) He throws the book into the ocean.\n\nAnswer with A or B:",
                    "A woman walks into a kitchen. She opens the refrigerator.\n\nWhich is more likely:\nA) She takes out some food.\nB) She starts flying around the room.\n\nAnswer with A or B:",
                ]
            },
        )
        runner = BenchmarkRunner(provider=provider, use_full_datasets=False)

        results = runner.run_hellaswag_sample()

        assert "hellaswag_accuracy" in results
        assert "questions_tested" in results
        assert "correct" in results
        assert results["questions_tested"] == 2  # Demo has 2 scenarios
        assert 0.0 <= results["hellaswag_accuracy"] <= 1.0

    def test_run_all_benchmarks(self):
        """Test running all benchmarks"""
        provider = MockProvider(model="test-model", responses=create_mock_responses())
        runner = BenchmarkRunner(provider=provider, use_full_datasets=False)

        results = runner.run_all_benchmarks()

        assert "mmlu" in results
        assert "truthfulqa" in results
        assert "hellaswag" in results
        assert "aggregate_benchmark_score" in results
        agg = results["aggregate_benchmark_score"]
        score = agg["score"] if isinstance(agg, dict) else agg
        assert 0.0 <= score <= 1.0

    def test_benchmark_error_handling(self):
        """Test benchmark handles provider errors"""
        from tests.mocks import create_failing_provider

        provider = create_failing_provider()
        runner = BenchmarkRunner(provider=provider, use_full_datasets=False)

        with pytest.raises(ProviderError):
            runner.run_mmlu_sample()
