"""
Extended tests for statistical_metrics module.
"""

import pytest


class TestWilsonConfidenceInterval:
    """Test Wilson confidence interval calculation"""

    def test_wilson_ci_basic(self):
        """Test basic Wilson CI calculation"""
        from llm_evaluator.statistical_metrics import calculate_wilson_ci

        lower, upper = calculate_wilson_ci(80, 100)

        assert 0.7 <= lower <= 0.75
        assert 0.85 <= upper <= 0.9

    def test_wilson_ci_perfect_score(self):
        """Test with 100% accuracy"""
        from llm_evaluator.statistical_metrics import calculate_wilson_ci

        lower, upper = calculate_wilson_ci(100, 100)

        assert lower > 0.95
        assert upper == 1.0

    def test_wilson_ci_zero_score(self):
        """Test with 0% accuracy"""
        from llm_evaluator.statistical_metrics import calculate_wilson_ci

        lower, upper = calculate_wilson_ci(0, 100)

        assert lower < 0.001  # Very close to 0
        assert upper < 0.05

    def test_wilson_ci_invalid_total(self):
        """Test with invalid total raises error"""
        from llm_evaluator.statistical_metrics import calculate_wilson_ci

        with pytest.raises(ValueError):
            calculate_wilson_ci(50, 0)

    def test_wilson_ci_invalid_correct(self):
        """Test with negative correct raises error"""
        from llm_evaluator.statistical_metrics import calculate_wilson_ci

        with pytest.raises(ValueError):
            calculate_wilson_ci(-1, 100)

    def test_wilson_ci_correct_exceeds_total(self):
        """Test with correct > total raises error"""
        from llm_evaluator.statistical_metrics import calculate_wilson_ci

        with pytest.raises(ValueError):
            calculate_wilson_ci(110, 100)


class TestStandardError:
    """Test standard error calculation"""

    def test_standard_error_basic(self):
        """Test basic SE calculation"""
        from llm_evaluator.statistical_metrics import calculate_standard_error

        se = calculate_standard_error(80, 100)

        assert 0.03 <= se <= 0.05

    def test_standard_error_perfect(self):
        """Test SE with 100% accuracy"""
        from llm_evaluator.statistical_metrics import calculate_standard_error

        se = calculate_standard_error(100, 100)

        assert se == 0.0

    def test_standard_error_invalid_total(self):
        """Test with invalid total raises error"""
        from llm_evaluator.statistical_metrics import calculate_standard_error

        with pytest.raises(ValueError):
            calculate_standard_error(50, 0)


class TestBootstrapCI:
    """Test bootstrap confidence interval"""

    def test_bootstrap_ci_basic(self):
        """Test basic bootstrap CI"""
        from llm_evaluator.statistical_metrics import bootstrap_confidence_interval

        predictions = [True] * 80 + [False] * 20
        lower, upper = bootstrap_confidence_interval(predictions, n_bootstrap=1000)

        assert 0.65 <= lower <= 0.85
        assert 0.85 <= upper <= 0.95

    def test_bootstrap_ci_reproducible(self):
        """Test bootstrap CI is reproducible with seed"""
        from llm_evaluator.statistical_metrics import bootstrap_confidence_interval

        predictions = [True] * 50 + [False] * 50

        ci1 = bootstrap_confidence_interval(predictions, random_seed=42)
        ci2 = bootstrap_confidence_interval(predictions, random_seed=42)

        assert ci1 == ci2


class TestMcNemarTest:
    """Test McNemar's test"""

    def test_mcnemar_basic(self):
        """Test basic McNemar test"""
        from llm_evaluator.statistical_metrics import mcnemar_test

        # Ground truth and model predictions
        ground_truth = [True, True, False, False, True, True, False, True, True, True]
        predictions_a = [True, True, False, False, True, True, False, True, True, True]
        predictions_b = [True, False, True, False, True, True, True, False, True, True]

        result = mcnemar_test(predictions_a, predictions_b, ground_truth)

        assert "statistic" in result or "p_value" in result

    def test_mcnemar_identical(self):
        """Test McNemar with identical predictions"""
        from llm_evaluator.statistical_metrics import mcnemar_test

        ground_truth = [True, True, False, True] * 10
        predictions = [True, True, False, True] * 10

        result = mcnemar_test(predictions, predictions, ground_truth)

        # P-value should be high when models are identical
        assert result.get("p_value", 1.0) >= 0.05


class TestCohenKappa:
    """Test Cohen's Kappa"""

    def test_cohen_kappa_perfect(self):
        """Test Cohen's Kappa with perfect agreement"""
        from llm_evaluator.statistical_metrics import calculate_cohens_kappa

        # Perfect agreement
        predictions_a = [True, True, False, False, True]
        predictions_b = [True, True, False, False, True]

        kappa = calculate_cohens_kappa(predictions_a, predictions_b)

        assert kappa == 1.0

    def test_cohen_kappa_no_agreement(self):
        """Test Cohen's Kappa with no agreement"""
        from llm_evaluator.statistical_metrics import calculate_cohens_kappa

        # Complete disagreement
        predictions_a = [True, True, True, True, True]
        predictions_b = [False, False, False, False, False]

        kappa = calculate_cohens_kappa(predictions_a, predictions_b)

        # Kappa should be negative or very low
        assert kappa < 0.5


class TestEffectSize:
    """Test effect size calculation"""

    def test_effect_size_basic(self):
        """Test basic effect size calculation"""
        from llm_evaluator.statistical_metrics import calculate_effect_size

        # 80% vs 70% accuracy
        effect = calculate_effect_size(0.80, 0.70, 100)

        # Should be a meaningful positive effect
        assert effect > 0

    def test_effect_size_no_difference(self):
        """Test effect size with no difference"""
        from llm_evaluator.statistical_metrics import calculate_effect_size

        effect = calculate_effect_size(0.80, 0.80, 100)

        assert effect == 0.0 or abs(effect) < 0.01


class TestStatisticalPower:
    """Test statistical power calculation"""

    def test_statistical_power_basic(self):
        """Test basic power calculation"""
        from llm_evaluator.statistical_metrics import calculate_required_sample_size

        n = calculate_required_sample_size(effect_size=0.1, power=0.8, alpha=0.05)  # 10% difference

        assert n > 0
        assert n < 10000  # Reasonable sample size


class TestAggregateStats:
    """Test aggregate statistics functions"""

    def test_calculate_aggregate_statistics(self):
        """Test aggregate statistics calculation"""
        from llm_evaluator.statistical_metrics import calculate_aggregate_statistics

        accuracies = [0.75, 0.80, 0.70, 0.85, 0.78]

        stats = calculate_aggregate_statistics(accuracies)

        assert "mean" in stats
        assert "std" in stats
        assert "min" in stats
        assert "max" in stats
