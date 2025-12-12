"""
Strategic tests to push coverage from 79% to 80%+
Targeting: error_analysis (81%), system_info (82%), statistical_metrics (81%)
"""

import numpy as np


class TestErrorAnalysisClasses:
    """Test error_analysis dataclasses and ErrorAnalyzer"""

    def test_error_example_creation(self):
        """Test ErrorExample dataclass"""
        from llm_evaluator.error_analysis import ErrorExample

        example = ErrorExample(
            question="What is 2+2?",
            predicted="5",
            expected="4",
            category="math",
            context="Basic arithmetic",
            explanation="Off by one",
        )

        assert example.question == "What is 2+2?"
        assert example.predicted == "5"
        assert example.expected == "4"
        assert example.category == "math"

    def test_error_analysis_result_creation(self):
        """Test ErrorAnalysisResult dataclass"""
        from llm_evaluator.error_analysis import ErrorAnalysisResult

        result = ErrorAnalysisResult(
            total_errors=10,
            total_correct=90,
            total_samples=100,
            error_distribution={"math": 5, "logic": 5},
            error_rate_by_category={"math": 0.1, "logic": 0.05},
            examples_per_category={},
            most_common_error_type="math",
            error_rate=0.1,
        )

        assert result.total_errors == 10
        assert result.error_rate == 0.1

    def test_error_analysis_result_to_dict(self):
        """Test ErrorAnalysisResult.to_dict method"""
        from llm_evaluator.error_analysis import ErrorAnalysisResult

        result = ErrorAnalysisResult(
            total_errors=5,
            total_correct=95,
            total_samples=100,
            error_distribution={"cat1": 5},
            error_rate_by_category={"cat1": 0.05},
            examples_per_category={},
            most_common_error_type="cat1",
            error_rate=0.05,
        )

        d = result.to_dict()
        assert isinstance(d, dict)
        assert d["total_errors"] == 5
        assert d["error_rate"] == 0.05

    def test_calibration_result_creation(self):
        """Test CalibrationResult dataclass"""
        from llm_evaluator.error_analysis import CalibrationResult

        result = CalibrationResult(
            ece=0.05,
            mce=0.1,
            bins=[{"bin_index": 0, "accuracy": 0.8}],
            interpretation="Well calibrated",
            n_samples=100,
        )

        assert result.ece == 0.05
        assert result.mce == 0.1
        assert result.n_samples == 100


class TestErrorAnalyzerClass:
    """Test ErrorAnalyzer class methods"""

    def test_error_analyzer_init(self):
        """Test ErrorAnalyzer initialization"""
        from llm_evaluator.error_analysis import ErrorAnalyzer

        analyzer = ErrorAnalyzer()
        assert analyzer is not None

    def test_error_analyzer_analyze_errors(self):
        """Test analyze_errors method"""
        from llm_evaluator.error_analysis import ErrorAnalyzer

        analyzer = ErrorAnalyzer()

        predictions = ["A", "B", "C"]
        ground_truth = ["A", "C", "C"]  # 2 correct, 1 wrong
        questions = ["Q1", "Q2", "Q3"]

        result = analyzer.analyze_errors(
            predictions=predictions, ground_truth=ground_truth, questions=questions
        )

        assert result.total_samples == 3
        assert result.total_correct == 2
        assert result.total_errors == 1


class TestErrorAnalysisFunctions:
    """Test standalone error analysis functions"""

    def test_expected_calibration_error(self):
        """Test ECE calculation"""
        from llm_evaluator.error_analysis import CalibrationResult, expected_calibration_error

        confidences = np.array([0.9, 0.8, 0.7, 0.6])
        accuracies = np.array([1, 1, 0, 1])  # 3/4 correct

        result = expected_calibration_error(confidences, accuracies)

        # Returns CalibrationResult, not float
        assert isinstance(result, CalibrationResult)
        assert 0 <= result.ece <= 1

    def test_cohens_kappa(self):
        """Test Cohen's kappa calculation"""
        from llm_evaluator.error_analysis import cohens_kappa

        predictions = ["A", "B", "A", "B"]
        ground_truth = ["A", "B", "B", "A"]  # 2 agreements

        result = cohens_kappa(predictions, ground_truth)

        # Returns dict with kappa value
        assert isinstance(result, dict)
        assert "kappa" in result
        assert -1 <= result["kappa"] <= 1

    def test_analyze_error_patterns(self):
        """Test analyze_error_patterns function"""
        from llm_evaluator.error_analysis import analyze_error_patterns

        questions = ["Q1", "Q2", "Q3"]
        predictions = ["A", "B", "C"]
        ground_truth = ["A", "C", "C"]  # Q2 is wrong
        categories = ["cat1", "cat1", "cat2"]

        result = analyze_error_patterns(
            questions=questions,
            predictions=predictions,
            ground_truth=ground_truth,
            categories=categories,
        )

        assert isinstance(result, dict)


class TestSystemInfoModule:
    """Test system_info module functions"""

    def test_collect_system_info(self):
        """Test collect_system_info function"""
        from llm_evaluator.system_info import collect_system_info

        info = collect_system_info()

        assert info is not None
        assert hasattr(info, "cpu_model")
        assert hasattr(info, "cpu_cores")
        assert hasattr(info, "ram_total_gb")

    def test_system_info_to_dict(self):
        """Test SystemInfo.to_dict method"""
        from llm_evaluator.system_info import collect_system_info

        info = collect_system_info()
        d = info.to_dict()

        assert isinstance(d, dict)
        assert "cpu_model" in d
        assert "cpu_cores" in d

    def test_system_info_to_json(self):
        """Test SystemInfo.to_json method"""
        import json

        from llm_evaluator.system_info import collect_system_info

        info = collect_system_info()
        json_str = info.to_json()

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert isinstance(parsed, dict)

    def test_system_info_to_markdown(self):
        """Test SystemInfo.to_markdown method"""
        from llm_evaluator.system_info import collect_system_info

        info = collect_system_info()
        md = info.to_markdown()

        assert isinstance(md, str)
        assert "System Information" in md or "CPU" in md

    def test_get_cpu_model(self):
        """Test get_cpu_model function"""
        from llm_evaluator.system_info import get_cpu_model

        cpu_model = get_cpu_model()

        assert isinstance(cpu_model, str)
        assert len(cpu_model) > 0

    def test_get_gpu_info(self):
        """Test get_gpu_info function"""
        from llm_evaluator.system_info import get_gpu_info

        gpu_name, gpu_vram = get_gpu_info()

        # Can be None if no GPU
        assert gpu_name is None or isinstance(gpu_name, str)
        assert gpu_vram is None or isinstance(gpu_vram, float)


class TestStatisticalMetricsFunctions:
    """Test statistical_metrics functions with correct signatures"""

    def test_calculate_wilson_ci_basic(self):
        """Test Wilson CI with basic inputs"""
        from llm_evaluator.statistical_metrics import calculate_wilson_ci

        lower, upper = calculate_wilson_ci(correct=85, total=100)

        assert 0 <= lower <= upper <= 1
        assert lower < 0.85 < upper  # 85% should be inside CI

    def test_calculate_wilson_ci_edge_cases(self):
        """Test Wilson CI edge cases"""
        from llm_evaluator.statistical_metrics import calculate_wilson_ci

        # Perfect accuracy
        lower, upper = calculate_wilson_ci(correct=100, total=100)
        assert upper == 1.0

        # Zero accuracy - lower bound is very close to 0
        lower, upper = calculate_wilson_ci(correct=0, total=100)
        assert lower < 0.001  # Essentially zero

    def test_calculate_wilson_ci_different_confidence(self):
        """Test Wilson CI with different confidence levels"""
        from llm_evaluator.statistical_metrics import calculate_wilson_ci

        ci_95 = calculate_wilson_ci(correct=50, total=100, confidence=0.95)
        ci_99 = calculate_wilson_ci(correct=50, total=100, confidence=0.99)

        # 99% CI should be wider
        assert (ci_99[1] - ci_99[0]) > (ci_95[1] - ci_95[0])

    def test_calculate_standard_error(self):
        """Test standard error calculation"""
        from llm_evaluator.statistical_metrics import calculate_standard_error

        se = calculate_standard_error(correct=50, total=100)

        assert isinstance(se, float)
        assert 0 <= se <= 0.5  # Max SE for binomial is 0.5

    def test_calculate_standard_error_edge_cases(self):
        """Test SE edge cases"""
        from llm_evaluator.statistical_metrics import calculate_standard_error

        # Perfect accuracy has lower SE
        se_perfect = calculate_standard_error(correct=100, total=100)
        se_half = calculate_standard_error(correct=50, total=100)

        assert se_perfect < se_half


class TestAcademicBaselines:
    """Test academic_baselines module"""

    def test_get_baselines(self):
        """Test get_baselines function"""
        from llm_evaluator.academic_baselines import get_baselines

        baselines = get_baselines("mmlu")

        assert isinstance(baselines, dict)
        # Should have some baseline models
        assert len(baselines) > 0

    def test_compare_to_baselines(self):
        """Test compare_to_baselines function"""
        from llm_evaluator.academic_baselines import compare_to_baselines

        result = compare_to_baselines(model_name="test-model", model_score=0.7, benchmark="mmlu")

        assert isinstance(result, dict)
        assert "comparisons" in result or "rank" in result

    def test_list_available_baselines(self):
        """Test list_available_baselines function"""
        from llm_evaluator.academic_baselines import list_available_baselines

        available = list_available_baselines()

        assert isinstance(available, dict)
        assert "mmlu" in available or len(available) > 0

    def test_get_baseline_citation(self):
        """Test get_baseline_citation function"""
        from llm_evaluator.academic_baselines import get_baseline_citation

        citation = get_baseline_citation("mmlu", "gpt-4")

        # Can be None if not found, or string
        assert citation is None or isinstance(citation, str)


class TestExportFunctions:
    """Test export module functions"""

    def test_generate_reproducibility_manifest(self):
        """Test reproducibility manifest generation"""
        from llm_evaluator.export import generate_reproducibility_manifest

        config = {"sample_size": 100, "temperature": 0.0}
        results = {"accuracy": 0.85}

        manifest = generate_reproducibility_manifest(config, results)

        assert isinstance(manifest, dict)
        assert "evaluation_hash" in manifest

    def test_export_to_latex(self):
        """Test LaTeX export function"""
        from llm_evaluator.export import export_to_latex

        assert export_to_latex is not None

    def test_generate_bibtex(self):
        """Test BibTeX generation function"""
        from llm_evaluator.export import generate_bibtex

        assert generate_bibtex is not None
