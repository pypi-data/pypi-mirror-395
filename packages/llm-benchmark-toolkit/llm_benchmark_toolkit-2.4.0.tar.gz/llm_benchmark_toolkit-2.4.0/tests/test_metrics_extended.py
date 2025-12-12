"""
Extended tests for metrics module.
"""

import pytest


class TestPerformanceMetricsStatic:
    """Test PerformanceMetrics static methods"""

    def test_calculate_avg_response_time_valid(self):
        """Test average response time calculation"""
        from llm_evaluator.metrics import PerformanceMetrics

        result = PerformanceMetrics.calculate_avg_response_time([1.0, 2.0, 3.0])

        assert result == 2.0

    def test_calculate_avg_response_time_empty(self):
        """Test with empty list raises error"""
        from llm_evaluator.metrics import PerformanceMetrics

        with pytest.raises(ValueError):
            PerformanceMetrics.calculate_avg_response_time([])

    def test_calculate_tokens_per_second_valid(self):
        """Test tokens per second calculation"""
        from llm_evaluator.metrics import PerformanceMetrics

        result = PerformanceMetrics.calculate_tokens_per_second(100, 2.0)

        assert result == 50.0

    def test_calculate_tokens_per_second_zero_time(self):
        """Test with zero time raises error"""
        from llm_evaluator.metrics import PerformanceMetrics

        with pytest.raises(ValueError):
            PerformanceMetrics.calculate_tokens_per_second(100, 0)

    def test_calculate_throughput_valid(self):
        """Test throughput calculation"""
        from llm_evaluator.metrics import PerformanceMetrics

        result = PerformanceMetrics.calculate_throughput(10, 2.0)

        assert result == 5.0

    def test_calculate_throughput_zero_time(self):
        """Test throughput calculation with zero time raises error"""
        from llm_evaluator.metrics import PerformanceMetrics

        with pytest.raises(ValueError, match="Time must be greater than 0"):
            PerformanceMetrics.calculate_throughput(10, 0)

    def test_calculate_latency_percentile_p95(self):
        """Test P95 latency calculation"""
        from llm_evaluator.metrics import PerformanceMetrics

        latencies = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        result = PerformanceMetrics.calculate_latency_percentile(latencies, 95)

        assert result >= 0.9


class TestQualityMetricsStatic:
    """Test QualityMetrics static methods"""

    def test_calculate_accuracy_valid(self):
        """Test accuracy calculation"""
        from llm_evaluator.metrics import QualityMetrics

        result = QualityMetrics.calculate_accuracy(8, 10)

        assert result == 0.8

    def test_calculate_accuracy_zero_total(self):
        """Test with zero total raises error"""
        from llm_evaluator.metrics import QualityMetrics

        with pytest.raises(ValueError):
            QualityMetrics.calculate_accuracy(5, 0)

    def test_calculate_coherence_score_valid(self):
        """Test coherence score calculation"""
        from llm_evaluator.metrics import QualityMetrics

        responses = [
            "This is a well-structured sentence with good content.",
            "Another sentence that makes sense and flows well.",
        ]

        result = QualityMetrics.calculate_coherence_score(responses)

        assert 0 <= result <= 1

    def test_calculate_coherence_score_empty(self):
        """Test with empty list returns 0"""
        from llm_evaluator.metrics import QualityMetrics

        result = QualityMetrics.calculate_coherence_score([])

        assert result == 0.0

    def test_calculate_hallucination_rate_valid(self):
        """Test hallucination rate calculation"""
        from llm_evaluator.metrics import QualityMetrics

        result = QualityMetrics.calculate_hallucination_rate(2, 10)

        assert result == 0.2

    def test_calculate_hallucination_rate_zero_total(self):
        """Test with zero total returns 0"""
        from llm_evaluator.metrics import QualityMetrics

        result = QualityMetrics.calculate_hallucination_rate(0, 0)

        assert result == 0.0

    def test_calculate_precision_recall_f1_valid(self):
        """Test precision/recall/F1 calculation"""
        from llm_evaluator.metrics import QualityMetrics

        result = QualityMetrics.calculate_precision_recall_f1(80, 10, 10)

        assert "precision" in result
        assert "recall" in result
        assert "f1_score" in result
        assert result["precision"] == 0.8888888888888888

    def test_calculate_precision_recall_f1_all_zero(self):
        """Test with all zeros"""
        from llm_evaluator.metrics import QualityMetrics

        result = QualityMetrics.calculate_precision_recall_f1(0, 0, 0)

        assert result["precision"] == 0
        assert result["recall"] == 0
        assert result["f1_score"] == 0

    def test_calculate_bleu_score_valid(self):
        """Test BLEU score calculation"""
        from llm_evaluator.metrics import QualityMetrics

        reference = "the cat sat on the mat"
        candidate = "the cat is on the mat"

        result = QualityMetrics.calculate_bleu_score(reference, candidate)

        assert 0 <= result <= 1

    def test_calculate_bleu_score_empty_candidate(self):
        """Test with empty candidate returns 0"""
        from llm_evaluator.metrics import QualityMetrics

        result = QualityMetrics.calculate_bleu_score("reference", "")

        assert result == 0.0


class TestMetricsDataclasses:
    """Test metrics dataclasses can be instantiated"""

    def test_performance_metrics_instantiation(self):
        """Test PerformanceMetrics can be instantiated"""
        from llm_evaluator.metrics import PerformanceMetrics

        metrics = PerformanceMetrics()

        assert metrics is not None

    def test_quality_metrics_instantiation(self):
        """Test QualityMetrics can be instantiated"""
        from llm_evaluator.metrics import QualityMetrics

        metrics = QualityMetrics()

        assert metrics is not None
