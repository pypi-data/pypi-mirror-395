"""
Error analysis for academic LLM evaluation.

Provides error categorization, calibration metrics, and analysis tools
for understanding model failures.

References:
    - Guo et al. (2017): On Calibration of Modern Neural Networks
    - Cohen (1960): Coefficient of agreement for nominal scales
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass
class ErrorExample:
    """Single error example with context."""

    question: str
    predicted: str
    expected: str
    category: str
    context: Optional[str] = None
    explanation: Optional[str] = None


@dataclass
class ErrorAnalysisResult:
    """Complete error analysis results."""

    total_errors: int
    total_correct: int
    total_samples: int
    error_distribution: Dict[str, int]
    error_rate_by_category: Dict[str, float]
    examples_per_category: Dict[str, List[ErrorExample]]
    most_common_error_type: str
    error_rate: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "total_errors": self.total_errors,
            "total_correct": self.total_correct,
            "total_samples": self.total_samples,
            "error_rate": self.error_rate,
            "error_distribution": self.error_distribution,
            "error_rate_by_category": self.error_rate_by_category,
            "most_common_error_type": self.most_common_error_type,
            "examples_per_category": {
                cat: [
                    {
                        "question": (
                            ex.question[:100] + "..." if len(ex.question) > 100 else ex.question
                        ),
                        "predicted": ex.predicted,
                        "expected": ex.expected,
                    }
                    for ex in examples[:3]  # Limit to 3 examples
                ]
                for cat, examples in self.examples_per_category.items()
            },
        }


@dataclass
class CalibrationResult:
    """Expected Calibration Error results."""

    ece: float  # Expected Calibration Error
    mce: float  # Maximum Calibration Error
    bins: List[Dict[str, Any]]
    interpretation: str
    n_samples: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "ece": self.ece,
            "mce": self.mce,
            "interpretation": self.interpretation,
            "n_samples": self.n_samples,
            "n_bins": len(self.bins),
            "bins": self.bins,
        }


class ErrorAnalyzer:
    """
    Categorize and analyze model errors for academic papers.

    Error categories following academic standards:
    - factual: Wrong information/facts
    - reasoning: Correct info, wrong logic
    - format: Right answer, wrong format
    - hallucination: Generated false information
    - ambiguous: Question has multiple valid answers
    - refusal: Model refused to answer

    Example:
        >>> analyzer = ErrorAnalyzer()
        >>> result = analyzer.analyze_errors(
        ...     predictions=['A', 'B', 'C'],
        ...     ground_truth=['A', 'C', 'C'],
        ...     questions=['Q1', 'Q2', 'Q3']
        ... )
        >>> print(f"Error rate: {result.error_rate:.1%}")
    """

    CATEGORIES = [
        "factual",
        "reasoning",
        "format",
        "hallucination",
        "ambiguous",
        "refusal",
        "unknown",
    ]

    # Keywords for error classification heuristics
    REFUSAL_KEYWORDS = [
        "i cannot",
        "i can't",
        "i'm unable",
        "i am unable",
        "as an ai",
        "i don't have",
        "i do not have",
        "refuse",
        "inappropriate",
    ]

    FORMAT_INDICATORS = [
        "the answer is",
        "option",
        "choice",
        "select",
    ]

    def __init__(self) -> None:
        """Initialize error analyzer."""
        self._error_counts: Dict[str, int] = defaultdict(int)

    def analyze_errors(
        self,
        predictions: List[str],
        ground_truth: List[str],
        questions: List[str],
        contexts: Optional[List[str]] = None,
    ) -> ErrorAnalysisResult:
        """
        Categorize all errors and provide examples.

        Args:
            predictions: Model predictions
            ground_truth: Correct answers
            questions: Original questions
            contexts: Optional additional context per question

        Returns:
            ErrorAnalysisResult with complete breakdown
        """
        if len(predictions) != len(ground_truth) or len(predictions) != len(questions):
            raise ValueError("All input lists must have the same length")

        errors_by_category: Dict[str, List[ErrorExample]] = {cat: [] for cat in self.CATEGORIES}
        error_distribution: Dict[str, int] = {cat: 0 for cat in self.CATEGORIES}
        total_errors = 0
        total_correct = 0

        for i, (pred, truth, question) in enumerate(zip(predictions, ground_truth, questions)):
            context = contexts[i] if contexts else None

            if str(pred).strip().upper() == str(truth).strip().upper():
                total_correct += 1
                continue

            # Error detected
            total_errors += 1
            category = self._classify_error(question, pred, truth, context)
            error_distribution[category] += 1

            error_example = ErrorExample(
                question=question,
                predicted=str(pred),
                expected=str(truth),
                category=category,
                context=context,
            )
            errors_by_category[category].append(error_example)

        # Calculate error rates by category
        error_rates = {}
        for cat in self.CATEGORIES:
            if total_errors > 0:
                error_rates[cat] = error_distribution[cat] / total_errors
            else:
                error_rates[cat] = 0.0

        # Find most common error type
        if total_errors > 0:
            most_common = max(error_distribution.items(), key=lambda x: x[1])
            most_common_type = most_common[0]
        else:
            most_common_type = "none"

        total_samples = len(predictions)
        error_rate = total_errors / total_samples if total_samples > 0 else 0.0

        return ErrorAnalysisResult(
            total_errors=total_errors,
            total_correct=total_correct,
            total_samples=total_samples,
            error_distribution=error_distribution,
            error_rate_by_category=error_rates,
            examples_per_category=errors_by_category,
            most_common_error_type=most_common_type,
            error_rate=error_rate,
        )

    def _classify_error(
        self,
        question: str,
        prediction: str,
        ground_truth: str,
        context: Optional[str] = None,
    ) -> str:
        """
        Classify a single error into category.

        Uses heuristics based on content analysis.
        """
        pred_lower = prediction.lower().strip()

        # Check for refusal
        for keyword in self.REFUSAL_KEYWORDS:
            if keyword in pred_lower:
                return "refusal"

        # Check for format issues (answer present but wrong format)
        # If prediction contains the ground truth but also other content
        if ground_truth.lower() in pred_lower and len(pred_lower) > len(ground_truth) * 3:
            return "format"

        # Check for empty or very short responses
        if len(pred_lower) < 2:
            return "refusal"

        # Check for hallucination indicators
        # Very long responses with confident-sounding but wrong answers
        if len(pred_lower) > 200:
            return "hallucination"

        # Check for reasoning errors
        # Contains logical connectors but wrong answer
        reasoning_words = ["because", "therefore", "since", "thus", "hence"]
        if any(word in pred_lower for word in reasoning_words):
            return "reasoning"

        # Default to factual error
        return "factual"


def expected_calibration_error(
    confidences: List[float],
    correct: List[bool],
    n_bins: int = 10,
) -> CalibrationResult:
    """
    Calculate Expected Calibration Error (ECE).

    Measures how well model's confidence matches actual accuracy.
    A well-calibrated model has ECE close to 0.

    Args:
        confidences: Model confidence scores (0 to 1)
        correct: Whether each prediction was correct
        n_bins: Number of bins for calibration (default: 10)

    Returns:
        CalibrationResult with ECE, MCE, and per-bin data

    References:
        Guo et al. (2017). "On Calibration of Modern Neural Networks"
        ICML 2017.

    Example:
        >>> confs = [0.9, 0.8, 0.7, 0.6, 0.5]
        >>> correct = [True, True, True, False, False]
        >>> result = expected_calibration_error(confs, correct)
        >>> print(f"ECE: {result.ece:.3f}")
    """
    if len(confidences) != len(correct):
        raise ValueError("Confidences and correct lists must have same length")

    if len(confidences) == 0:
        return CalibrationResult(
            ece=0.0,
            mce=0.0,
            bins=[],
            interpretation="No samples provided",
            n_samples=0,
        )

    confidences_arr = np.array(confidences)
    correct_arr = np.array(correct, dtype=float)

    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bins_data: List[Dict[str, Any]] = []
    gaps: List[float] = []

    for i in range(n_bins):
        bin_lower = float(bin_boundaries[i])
        bin_upper = float(bin_boundaries[i + 1])

        # Find samples in this bin
        if i == n_bins - 1:  # Include upper boundary for last bin
            in_bin = (confidences_arr >= bin_lower) & (confidences_arr <= bin_upper)
        else:
            in_bin = (confidences_arr >= bin_lower) & (confidences_arr < bin_upper)

        bin_count = int(np.sum(in_bin))

        if bin_count > 0:
            bin_accuracy = float(np.mean(correct_arr[in_bin]))
            bin_confidence = float(np.mean(confidences_arr[in_bin]))
            calibration_gap = abs(bin_accuracy - bin_confidence)
        else:
            bin_accuracy = 0.0
            bin_confidence = (bin_lower + bin_upper) / 2
            calibration_gap = 0.0

        gaps.append(calibration_gap * bin_count)

        bins_data.append(
            {
                "bin_index": i,
                "confidence_range": (float(bin_lower), float(bin_upper)),
                "avg_confidence": bin_confidence,
                "accuracy": bin_accuracy,
                "count": bin_count,
                "calibration_gap": calibration_gap,
            }
        )

    # Calculate ECE (weighted average of gaps)
    n_samples = len(confidences)
    ece = sum(gaps) / n_samples if n_samples > 0 else 0.0

    # Calculate MCE (maximum calibration error)
    mce_val: float = 0.0
    if bins_data:
        gaps_list = [float(b.get("calibration_gap", 0)) for b in bins_data]
        mce_val = max(gaps_list) if gaps_list else 0.0

    # Interpretation
    if ece < 0.05:
        interpretation = f"Well-calibrated (ECE={ece:.1%})"
    elif ece < 0.10:
        interpretation = f"Slightly miscalibrated (ECE={ece:.1%})"
    elif ece < 0.20:
        interpretation = f"Moderately miscalibrated (ECE={ece:.1%})"
    else:
        interpretation = f"Poorly calibrated (ECE={ece:.1%})"

    # Determine if over/underconfident
    total_conf: float = 0.0
    total_acc: float = 0.0
    for b in bins_data:
        count = int(b.get("count", 0))
        total_conf += float(b.get("avg_confidence", 0)) * count
        total_acc += float(b.get("accuracy", 0)) * count

    if n_samples > 0:
        avg_conf = total_conf / n_samples
        avg_acc = total_acc / n_samples
        if avg_conf > avg_acc + 0.02:
            interpretation += " - overconfident"
        elif avg_acc > avg_conf + 0.02:
            interpretation += " - underconfident"

    return CalibrationResult(
        ece=ece,
        mce=mce_val,
        bins=bins_data,
        interpretation=interpretation,
        n_samples=n_samples,
    )


def cohens_kappa(
    annotations_a: List[str],
    annotations_b: List[str],
) -> Dict[str, Any]:
    """
    Calculate Cohen's Kappa for inter-annotator agreement.

    Measures agreement between two annotators beyond chance.

    Args:
        annotations_a: First annotator's labels
        annotations_b: Second annotator's labels

    Returns:
        Dictionary with kappa score and interpretation

    References:
        Cohen, J. (1960). "A coefficient of agreement for nominal scales".
        Educational and Psychological Measurement, 20(1), 37-46.

    Interpretation:
        - < 0: No agreement
        - 0.0 - 0.20: Slight agreement
        - 0.21 - 0.40: Fair agreement
        - 0.41 - 0.60: Moderate agreement
        - 0.61 - 0.80: Substantial agreement
        - 0.81 - 1.00: Almost perfect agreement
    """
    if len(annotations_a) != len(annotations_b):
        raise ValueError("Annotation lists must have same length")

    if len(annotations_a) == 0:
        return {
            "kappa": 0.0,
            "interpretation": "No samples",
            "agreement_rate": 0.0,
            "n_samples": 0,
        }

    # Calculate observed agreement
    n = len(annotations_a)
    agreements = sum(1 for a, b in zip(annotations_a, annotations_b) if a == b)
    observed_agreement = agreements / n

    # Calculate expected agreement
    labels_a = set(annotations_a) | set(annotations_b)
    expected_agreement = 0.0

    for label in labels_a:
        p_a = sum(1 for x in annotations_a if x == label) / n
        p_b = sum(1 for x in annotations_b if x == label) / n
        expected_agreement += p_a * p_b

    # Calculate kappa
    if expected_agreement == 1.0:
        kappa = 1.0
    else:
        kappa = (observed_agreement - expected_agreement) / (1 - expected_agreement)

    # Interpretation
    if kappa < 0:
        interpretation = "No agreement (worse than chance)"
    elif kappa < 0.20:
        interpretation = "Slight agreement"
    elif kappa < 0.40:
        interpretation = "Fair agreement"
    elif kappa < 0.60:
        interpretation = "Moderate agreement"
    elif kappa < 0.80:
        interpretation = "Substantial agreement"
    else:
        interpretation = "Almost perfect agreement"

    return {
        "kappa": kappa,
        "interpretation": interpretation,
        "agreement_rate": observed_agreement,
        "expected_agreement": expected_agreement,
        "n_samples": n,
    }


def analyze_error_patterns(
    questions: List[str],
    predictions: List[str],
    ground_truth: List[str],
    categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Analyze patterns in model errors across categories.

    Args:
        questions: Original questions
        predictions: Model predictions
        ground_truth: Correct answers
        categories: Optional category labels for questions

    Returns:
        Analysis of error patterns by category
    """
    if categories is None:
        categories = ["general"] * len(questions)

    category_errors: Dict[str, Dict[str, int]] = defaultdict(lambda: {"correct": 0, "incorrect": 0})

    for q, pred, truth, cat in zip(questions, predictions, ground_truth, categories):
        is_correct = str(pred).strip().upper() == str(truth).strip().upper()
        if is_correct:
            category_errors[cat]["correct"] += 1
        else:
            category_errors[cat]["incorrect"] += 1

    results = {}
    for cat, counts in category_errors.items():
        total = counts["correct"] + counts["incorrect"]
        accuracy = counts["correct"] / total if total > 0 else 0.0
        results[cat] = {
            "correct": counts["correct"],
            "incorrect": counts["incorrect"],
            "total": total,
            "accuracy": accuracy,
            "error_rate": 1 - accuracy,
        }

    # Sort by error rate
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1]["error_rate"], reverse=True))

    return {
        "by_category": sorted_results,
        "worst_category": list(sorted_results.keys())[0] if sorted_results else None,
        "best_category": list(sorted_results.keys())[-1] if sorted_results else None,
    }
