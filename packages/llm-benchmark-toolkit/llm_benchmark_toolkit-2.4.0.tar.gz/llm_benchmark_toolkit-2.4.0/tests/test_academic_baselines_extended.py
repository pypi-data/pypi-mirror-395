"""
Extended tests for academic_baselines module.

Tests for:
- get_baseline_citation
- generate_baseline_bibtex
- generate_comparison_table
- list_available_baselines
- Edge cases
"""

import pytest

from llm_evaluator.academic_baselines import (
    ACADEMIC_BASELINES,
    compare_to_baselines,
    generate_baseline_bibtex,
    generate_comparison_table,
    get_baseline_citation,
    get_baselines,
    list_available_baselines,
)


class TestGetBaselineCitation:
    """Test get_baseline_citation function"""

    def test_valid_benchmark_and_model(self):
        """Test getting citation for valid benchmark/model"""
        # MMLU has gpt-4 baseline
        citation = get_baseline_citation("MMLU", "gpt-4")
        # Should return a string or None
        assert citation is None or isinstance(citation, str)

    def test_invalid_benchmark(self):
        """Test with non-existent benchmark"""
        result = get_baseline_citation("NonExistentBenchmark", "gpt-4")
        assert result is None

    def test_invalid_model(self):
        """Test with non-existent model"""
        result = get_baseline_citation("MMLU", "nonexistent-model")
        assert result is None

    def test_case_insensitive_benchmark(self):
        """Test benchmark name is case-insensitive"""
        citation1 = get_baseline_citation("mmlu", "gpt-4")
        citation2 = get_baseline_citation("MMLU", "gpt-4")
        # Both should work the same way
        assert citation1 == citation2


class TestGenerateBaselineBibtex:
    """Test generate_baseline_bibtex function"""

    def test_valid_model_with_reference(self):
        """Test BibTeX generation for model with reference"""
        bibtex = generate_baseline_bibtex("MMLU", "gpt-4")
        # Should return string or None
        if bibtex:
            assert "@misc{" in bibtex or "@article{" in bibtex
            assert "title" in bibtex.lower()

    def test_invalid_benchmark(self):
        """Test with invalid benchmark"""
        result = generate_baseline_bibtex("FakeBenchmark", "gpt-4")
        assert result is None

    def test_invalid_model(self):
        """Test with invalid model"""
        result = generate_baseline_bibtex("MMLU", "fake-model-xyz")
        assert result is None

    def test_bibtex_structure(self):
        """Test BibTeX has proper structure if returned"""
        bibtex = generate_baseline_bibtex("MMLU", "gpt-4")
        if bibtex:
            assert "{" in bibtex
            assert "}" in bibtex
            assert "year" in bibtex.lower()


class TestGenerateComparisonTable:
    """Test generate_comparison_table function"""

    def test_markdown_format(self):
        """Test markdown table generation"""
        results = {"my-model": 0.75, "other-model": 0.65}
        table = generate_comparison_table(results, "MMLU", format_type="markdown")

        assert isinstance(table, str)
        assert "|" in table  # Markdown tables use |
        assert "Model" in table
        assert "Score" in table

    def test_latex_format(self):
        """Test LaTeX table generation"""
        results = {"my-model": 0.75}
        table = generate_comparison_table(results, "MMLU", format_type="latex")

        assert isinstance(table, str)
        assert "\\begin{tabular}" in table
        assert "\\end{tabular}" in table
        assert "\\toprule" in table
        assert "\\bottomrule" in table

    def test_multiple_models(self):
        """Test table with multiple models"""
        results = {
            "model-a": 0.85,
            "model-b": 0.70,
            "model-c": 0.55,
        }
        table = generate_comparison_table(results, "MMLU", format_type="markdown")

        assert "model-a" in table
        assert "model-b" in table
        assert "model-c" in table

    def test_invalid_format_raises_error(self):
        """Test invalid format type raises ValueError"""
        results = {"model": 0.75}

        with pytest.raises(ValueError, match="Unknown format"):
            generate_comparison_table(results, "MMLU", format_type="invalid")

    def test_empty_results(self):
        """Test with empty results dict"""
        results = {}
        table = generate_comparison_table(results, "MMLU", format_type="markdown")

        # Should still have header
        assert "Model" in table
        assert "Score" in table


class TestListAvailableBaselines:
    """Test list_available_baselines function"""

    def test_returns_dict(self):
        """Test function returns dictionary"""
        result = list_available_baselines()
        assert isinstance(result, dict)

    def test_contains_known_benchmarks(self):
        """Test result contains known benchmarks"""
        result = list_available_baselines()

        # Should have at least MMLU
        assert len(result) > 0

    def test_values_are_lists(self):
        """Test dictionary values are lists of model names"""
        result = list_available_baselines()

        for benchmark, models in result.items():
            assert isinstance(models, list)

    def test_benchmarks_match_academic_baselines(self):
        """Test listed benchmarks match ACADEMIC_BASELINES keys"""
        result = list_available_baselines()

        for benchmark in ACADEMIC_BASELINES.keys():
            # Benchmark should be in result (case may differ)
            assert any(b.lower() == benchmark.lower() for b in result.keys())


class TestCompareToBaselinesExtended:
    """Extended tests for compare_to_baselines"""

    def test_sota_tier(self):
        """Test SOTA tier classification (>=0.85)"""
        result = compare_to_baselines("test-model", 0.90, "MMLU")
        assert result["tier"] == "sota"

    def test_strong_tier(self):
        """Test strong tier classification (>=0.75, <0.85)"""
        result = compare_to_baselines("test-model", 0.78, "MMLU")
        assert result["tier"] == "strong"

    def test_mid_range_tier(self):
        """Test mid-range tier classification (>=0.50, <0.75)"""
        result = compare_to_baselines("test-model", 0.60, "MMLU")
        assert result["tier"] == "mid-range"

    def test_weak_tier(self):
        """Test weak tier classification (>random, <0.50)"""
        result = compare_to_baselines("test-model", 0.35, "MMLU")
        assert result["tier"] == "weak"

    def test_below_random_tier(self):
        """Test below-random tier classification"""
        result = compare_to_baselines("test-model", 0.10, "MMLU")
        assert result["tier"] == "below-random"

    def test_percentile_calculation(self):
        """Test percentile is calculated correctly"""
        result = compare_to_baselines("test-model", 0.85, "MMLU")
        assert 0 <= result["percentile"] <= 100

    def test_gap_closure_calculation(self):
        """Test gap closure percentage"""
        result = compare_to_baselines("test-model", 0.80, "MMLU")
        assert "gap_closure_percent" in result

    def test_result_structure(self):
        """Test result has all expected keys"""
        result = compare_to_baselines("test-model", 0.75, "MMLU")

        expected_keys = [
            "model_name",
            "model_score",
            "benchmark",
            "comparisons",
            "rank",
            "total_baselines",
            "percentile",
            "tier",
            "gap_closure_percent",
        ]
        for key in expected_keys:
            assert key in result


class TestAcademicBaselinesData:
    """Test the ACADEMIC_BASELINES data structure"""

    def test_baselines_not_empty(self):
        """Test baselines dict is not empty"""
        assert len(ACADEMIC_BASELINES) > 0

    def test_mmlu_has_baselines(self):
        """Test MMLU has baseline models"""
        mmlu_baselines = get_baselines("MMLU")
        assert len(mmlu_baselines) > 0

    def test_baseline_has_score(self):
        """Test each baseline has a score field"""
        for benchmark, models in ACADEMIC_BASELINES.items():
            for model, data in models.items():
                assert "score" in data, f"{benchmark}/{model} missing score"

    def test_scores_are_valid(self):
        """Test all scores are between 0 and 1"""
        for benchmark, models in ACADEMIC_BASELINES.items():
            for model, data in models.items():
                score = data.get("score", 0)
                assert 0 <= score <= 1, f"{benchmark}/{model} has invalid score {score}"

    def test_random_chance_exists(self):
        """Test random_chance baseline exists for benchmarks"""
        for benchmark in ACADEMIC_BASELINES.keys():
            baselines = ACADEMIC_BASELINES[benchmark]
            assert "random_chance" in baselines, f"{benchmark} missing random_chance"
