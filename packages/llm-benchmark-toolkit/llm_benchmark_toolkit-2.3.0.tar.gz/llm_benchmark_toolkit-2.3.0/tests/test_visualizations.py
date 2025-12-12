"""Tests for visualization module"""

import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend for testing

import pytest

from llm_evaluator.visualizations import EvaluationVisualizer, quick_comparison


@pytest.fixture
def sample_results():
    """Sample evaluation results for testing"""
    return {
        "model1": {"mmlu": 0.65, "truthful_qa": 0.70, "accuracy": 0.75, "coherence": 0.80},
        "model2": {"mmlu": 0.70, "truthful_qa": 0.75, "accuracy": 0.80, "coherence": 0.85},
    }


@pytest.fixture
def visualizer():
    """Create visualizer instance"""
    return EvaluationVisualizer()


@pytest.fixture
def temp_output_dir():
    """Create temporary directory for test outputs"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestEvaluationVisualizer:
    """Test cases for EvaluationVisualizer class"""

    def test_visualizer_initialization(self):
        """Test that visualizer initializes correctly"""
        viz = EvaluationVisualizer()
        assert viz.style == "seaborn-v0_8-darkgrid"

    def test_benchmark_comparison_static(self, visualizer, sample_results, temp_output_dir):
        """Test static benchmark comparison chart generation"""
        output_path = temp_output_dir / "benchmark.png"

        visualizer.plot_benchmark_comparison(
            sample_results, output_path=output_path, interactive=False
        )

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_benchmark_comparison_interactive(self, visualizer, sample_results, temp_output_dir):
        """Test interactive benchmark comparison chart generation"""
        output_path = temp_output_dir / "benchmark.html"

        fig = visualizer.plot_benchmark_comparison(
            sample_results, output_path=output_path, interactive=True
        )

        assert fig is not None
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_radar_chart(self, visualizer, sample_results, temp_output_dir):
        """Test radar chart generation"""
        output_path = temp_output_dir / "radar.html"

        fig = visualizer.plot_radar_chart(sample_results, output_path=output_path)

        assert fig is not None
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_performance_trends(self, visualizer, temp_output_dir):
        """Test performance trends chart generation"""
        time_series = {
            "model1": [(i, i * 0.1) for i in range(10)],
            "model2": [(i, i * 0.15) for i in range(10)],
        }
        output_path = temp_output_dir / "trends.png"

        visualizer.plot_performance_trends(
            time_series, metric_name="Response Time", output_path=output_path
        )

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_model_heatmap(self, visualizer, sample_results, temp_output_dir):
        """Test model heatmap generation"""
        output_path = temp_output_dir / "heatmap.png"

        visualizer.plot_model_heatmap(sample_results, output_path=output_path)

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_score_distribution(self, visualizer, temp_output_dir):
        """Test score distribution chart generation"""
        scores = {"model1": [0.6, 0.7, 0.65, 0.75, 0.70], "model2": [0.7, 0.8, 0.75, 0.85, 0.80]}
        output_path = temp_output_dir / "distribution.png"

        visualizer.plot_score_distribution(scores, output_path=output_path)

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_dashboard_creation(self, visualizer, sample_results, temp_output_dir):
        """Test comprehensive dashboard creation"""
        output_path = temp_output_dir / "dashboard.html"

        visualizer.create_dashboard(sample_results, output_path=output_path)

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_empty_results(self, visualizer, temp_output_dir):
        """Test handling of empty results"""
        empty_results = {}
        output_path = temp_output_dir / "empty.png"

        # Should not crash with empty data
        try:
            visualizer.plot_model_heatmap(empty_results, output_path=output_path)
        except Exception as e:
            # Expected to handle gracefully or raise meaningful error
            assert isinstance(e, (ValueError, KeyError))

    def test_single_model_results(self, visualizer, temp_output_dir):
        """Test visualization with single model"""
        single_model = {"model1": {"mmlu": 0.65, "accuracy": 0.75}}
        output_path = temp_output_dir / "single.png"

        visualizer.plot_model_heatmap(single_model, output_path=output_path)

        assert output_path.exists()


class TestQuickComparison:
    """Test cases for quick_comparison utility function"""

    def test_quick_comparison(self, sample_results, temp_output_dir):
        """Test quick comparison generates all expected files"""
        quick_comparison(sample_results, output_dir=temp_output_dir)

        # Check that expected files were created
        expected_files = ["benchmarks.png", "radar.html", "heatmap.png", "dashboard.html"]

        for filename in expected_files:
            file_path = temp_output_dir / filename
            assert file_path.exists(), f"Expected file {filename} was not created"
            assert file_path.stat().st_size > 0, f"File {filename} is empty"

    def test_quick_comparison_creates_directory(self, sample_results):
        """Test that quick_comparison creates output directory if it doesn't exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "new_dir" / "visualizations"

            quick_comparison(sample_results, output_dir=output_dir)

            assert output_dir.exists()
            assert output_dir.is_dir()


class TestVisualizationDataValidation:
    """Test cases for data validation in visualizations"""

    def test_invalid_score_range(self, visualizer, temp_output_dir):
        """Test handling of scores outside 0-1 range"""
        invalid_results = {
            "model1": {"metric1": 1.5, "metric2": -0.2}  # Invalid: > 1  # Invalid: < 0
        }
        output_path = temp_output_dir / "invalid.png"

        # Should handle gracefully (values may be clipped or shown as-is)
        visualizer.plot_model_heatmap(invalid_results, output_path=output_path)

        assert output_path.exists()

    def test_missing_metrics(self, visualizer, temp_output_dir):
        """Test handling of models with different sets of metrics"""
        results = {
            "model1": {"mmlu": 0.65, "accuracy": 0.75},
            "model2": {"mmlu": 0.70, "coherence": 0.80},  # Different metric
        }
        output_path = temp_output_dir / "missing.html"

        # Should handle NaN/missing values appropriately
        fig = visualizer.plot_radar_chart(results, output_path=output_path)

        assert fig is not None
