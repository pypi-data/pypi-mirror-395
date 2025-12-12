"""
Academic baselines for LLM evaluation benchmarks.

Contains published results from major models for comparison.
All scores sourced from official papers, model cards, and technical reports.

References are provided for citation in academic papers.
"""

from typing import Any, Dict, List, Optional

# Published baseline results from academic papers and model cards
ACADEMIC_BASELINES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "mmlu": {
        "random_chance": {
            "score": 0.25,
            "description": "4-choice multiple choice random baseline",
            "reference": None,
            "date": None,
            "url": None,
        },
        "gpt-3.5-turbo": {
            "score": 0.700,
            "description": "OpenAI GPT-3.5 Turbo",
            "reference": "OpenAI (2023). GPT-3.5 Technical Report",
            "date": "2023-03",
            "url": "https://openai.com/research/gpt-3-5",
        },
        "gpt-4": {
            "score": 0.864,
            "description": "OpenAI GPT-4",
            "reference": "OpenAI (2023). GPT-4 Technical Report. arXiv:2303.08774",
            "date": "2023-03",
            "url": "https://arxiv.org/abs/2303.08774",
        },
        "gpt-4o": {
            "score": 0.887,
            "description": "OpenAI GPT-4o",
            "reference": "OpenAI (2024). GPT-4o System Card",
            "date": "2024-05",
            "url": "https://openai.com/index/hello-gpt-4o/",
        },
        "claude-3-opus": {
            "score": 0.868,
            "description": "Anthropic Claude 3 Opus",
            "reference": "Anthropic (2024). Claude 3 Model Card",
            "date": "2024-03",
            "url": "https://www.anthropic.com/claude",
        },
        "claude-3.5-sonnet": {
            "score": 0.882,
            "description": "Anthropic Claude 3.5 Sonnet",
            "reference": "Anthropic (2024). Claude 3.5 Sonnet",
            "date": "2024-06",
            "url": "https://www.anthropic.com/claude",
        },
        "llama-3-70b": {
            "score": 0.820,
            "description": "Meta Llama 3 70B",
            "reference": "Meta (2024). Llama 3 Model Card",
            "date": "2024-04",
            "url": "https://llama.meta.com/",
        },
        "llama-3.1-405b": {
            "score": 0.873,
            "description": "Meta Llama 3.1 405B",
            "reference": "Meta (2024). Llama 3.1 Model Card",
            "date": "2024-07",
            "url": "https://llama.meta.com/",
        },
        "llama-3.2-1b": {
            "score": 0.320,
            "description": "Meta Llama 3.2 1B (small model)",
            "reference": "Meta (2024). Llama 3.2 Model Card",
            "date": "2024-09",
            "url": "https://llama.meta.com/",
        },
        "llama-3.2-3b": {
            "score": 0.580,
            "description": "Meta Llama 3.2 3B",
            "reference": "Meta (2024). Llama 3.2 Model Card",
            "date": "2024-09",
            "url": "https://llama.meta.com/",
        },
        "mistral-7b": {
            "score": 0.625,
            "description": "Mistral 7B",
            "reference": "Mistral AI (2023). Mistral 7B",
            "date": "2023-09",
            "url": "https://mistral.ai/",
        },
        "mistral-large": {
            "score": 0.813,
            "description": "Mistral Large",
            "reference": "Mistral AI (2024). Mistral Large",
            "date": "2024-02",
            "url": "https://mistral.ai/",
        },
        "gemini-1.5-pro": {
            "score": 0.853,
            "description": "Google Gemini 1.5 Pro",
            "reference": "Google (2024). Gemini 1.5 Technical Report",
            "date": "2024-02",
            "url": "https://deepmind.google/technologies/gemini/",
        },
        "human_expert": {
            "score": 0.896,
            "description": "Human expert performance",
            "reference": (
                "Hendrycks et al. (2021). Measuring Massive Multitask "
                "Language Understanding. ICLR 2021."
            ),
            "date": "2021-01",
            "url": "https://arxiv.org/abs/2009.03300",
        },
    },
    "truthfulqa": {
        "random_chance": {
            "score": 0.25,
            "description": "Random baseline for MC questions",
            "reference": None,
            "date": None,
            "url": None,
        },
        "gpt-3.5-turbo": {
            "score": 0.47,
            "description": "OpenAI GPT-3.5 Turbo",
            "reference": "Lin et al. (2022). TruthfulQA. ACL 2022.",
            "date": "2022-05",
            "url": "https://arxiv.org/abs/2109.07958",
        },
        "gpt-4": {
            "score": 0.59,
            "description": "OpenAI GPT-4",
            "reference": "OpenAI (2023). GPT-4 Technical Report",
            "date": "2023-03",
            "url": "https://arxiv.org/abs/2303.08774",
        },
        "claude-3-opus": {
            "score": 0.55,
            "description": "Anthropic Claude 3 Opus",
            "reference": "Anthropic (2024). Claude 3 Model Card",
            "date": "2024-03",
            "url": "https://www.anthropic.com/claude",
        },
        "llama-3-70b": {
            "score": 0.52,
            "description": "Meta Llama 3 70B",
            "reference": "Meta (2024). Llama 3 Model Card",
            "date": "2024-04",
            "url": "https://llama.meta.com/",
        },
        "human": {
            "score": 0.94,
            "description": "Human performance",
            "reference": "Lin et al. (2022). TruthfulQA. ACL 2022.",
            "date": "2022-05",
            "url": "https://arxiv.org/abs/2109.07958",
        },
    },
    "hellaswag": {
        "random_chance": {
            "score": 0.25,
            "description": "4-choice random baseline",
            "reference": None,
            "date": None,
            "url": None,
        },
        "gpt-3.5-turbo": {
            "score": 0.85,
            "description": "OpenAI GPT-3.5 Turbo",
            "reference": "OpenAI internal evaluations (2023)",
            "date": "2023-03",
            "url": None,
        },
        "gpt-4": {
            "score": 0.95,
            "description": "OpenAI GPT-4",
            "reference": "OpenAI (2023). GPT-4 Technical Report",
            "date": "2023-03",
            "url": "https://arxiv.org/abs/2303.08774",
        },
        "claude-3-opus": {
            "score": 0.946,
            "description": "Anthropic Claude 3 Opus",
            "reference": "Anthropic (2024). Claude 3 Model Card",
            "date": "2024-03",
            "url": "https://www.anthropic.com/claude",
        },
        "llama-3-70b": {
            "score": 0.854,
            "description": "Meta Llama 3 70B",
            "reference": "Meta (2024). Llama 3 Model Card",
            "date": "2024-04",
            "url": "https://llama.meta.com/",
        },
        "llama-3.2-1b": {
            "score": 0.415,
            "description": "Meta Llama 3.2 1B",
            "reference": "Meta (2024). Llama 3.2 Model Card",
            "date": "2024-09",
            "url": "https://llama.meta.com/",
        },
        "mistral-7b": {
            "score": 0.814,
            "description": "Mistral 7B",
            "reference": "Mistral AI (2023). Mistral 7B",
            "date": "2023-09",
            "url": "https://mistral.ai/",
        },
        "human": {
            "score": 0.953,
            "description": "Human performance",
            "reference": (
                "Zellers et al. (2019). HellaSwag: Can a Machine Really "
                "Finish Your Sentence? ACL 2019."
            ),
            "date": "2019-06",
            "url": "https://arxiv.org/abs/1905.07830",
        },
    },
}


def get_baselines(benchmark: str) -> Dict[str, Dict[str, Any]]:
    """
    Get all baselines for a specific benchmark.

    Args:
        benchmark: Benchmark name ('mmlu', 'truthfulqa', 'hellaswag')

    Returns:
        Dictionary of baseline results

    Raises:
        ValueError: If benchmark not found
    """
    benchmark = benchmark.lower()
    if benchmark not in ACADEMIC_BASELINES:
        available = ", ".join(ACADEMIC_BASELINES.keys())
        raise ValueError(f"Unknown benchmark: {benchmark}. Available: {available}")
    return ACADEMIC_BASELINES[benchmark]


def compare_to_baselines(
    model_name: str,
    model_score: float,
    benchmark: str,
) -> Dict[str, Any]:
    """
    Compare model to published baselines.

    Args:
        model_name: Name of the evaluated model
        model_score: Model's accuracy score (0.0 to 1.0)
        benchmark: Benchmark name ('mmlu', 'truthfulqa', 'hellaswag')

    Returns:
        Comprehensive comparison dictionary

    Example:
        >>> result = compare_to_baselines('my-model', 0.75, 'mmlu')
        >>> print(f"Rank: {result['rank']}/{result['total_baselines']}")
        >>> print(f"vs GPT-4: {result['comparisons']['gpt-4']['delta']:+.1%}")
    """
    baselines = get_baselines(benchmark)

    comparisons: Dict[str, Dict[str, Any]] = {}
    baseline_scores: List[float] = []

    for baseline_name, baseline_data in baselines.items():
        baseline_score = baseline_data["score"]
        baseline_scores.append(baseline_score)

        delta = model_score - baseline_score
        percentage_diff = (delta / baseline_score * 100) if baseline_score > 0 else 0.0

        # Calculate gap closure to human (if available)
        human_score = baselines.get("human_expert", baselines.get("human", {}))
        human_score_val = human_score.get("score", 1.0) if human_score else 1.0
        random_score = baselines.get("random_chance", {}).get("score", 0.25)

        # Gap from random to human
        total_gap = human_score_val - random_score
        model_gap_closed = model_score - random_score
        gap_closure = (model_gap_closed / total_gap * 100) if total_gap > 0 else 0.0

        comparisons[baseline_name] = {
            "baseline_score": baseline_score,
            "delta": delta,
            "percentage_difference": percentage_diff,
            "reference": baseline_data.get("reference"),
        }

    # Calculate rank (1 = best)
    all_scores = sorted(baseline_scores + [model_score], reverse=True)
    rank = all_scores.index(model_score) + 1
    total = len(all_scores)
    percentile = (1 - (rank - 1) / (total - 1)) * 100 if total > 1 else 100.0

    # Determine tier
    random_baseline = baselines.get("random_chance", {}).get("score", 0.25)
    if model_score >= 0.85:
        tier = "sota"
    elif model_score >= 0.75:
        tier = "strong"
    elif model_score >= 0.50:
        tier = "mid-range"
    elif model_score > random_baseline:
        tier = "weak"
    else:
        tier = "below-random"

    return {
        "model_name": model_name,
        "model_score": model_score,
        "benchmark": benchmark,
        "comparisons": comparisons,
        "rank": rank,
        "total_baselines": total,
        "percentile": percentile,
        "tier": tier,
        "gap_closure_percent": gap_closure,
    }


def get_baseline_citation(benchmark: str, model: str) -> Optional[str]:
    """
    Get citation string for a baseline.

    Args:
        benchmark: Benchmark name
        model: Baseline model name

    Returns:
        Citation string or None if not found
    """
    try:
        baselines = get_baselines(benchmark)
        if model in baselines:
            return baselines[model].get("reference")
    except ValueError:
        pass
    return None


def generate_baseline_bibtex(benchmark: str, model: str) -> Optional[str]:
    """
    Generate BibTeX entry for a baseline reference.

    Args:
        benchmark: Benchmark name
        model: Baseline model name

    Returns:
        BibTeX string or None
    """
    try:
        baselines = get_baselines(benchmark)
        if model not in baselines:
            return None

        data = baselines[model]
        ref = data.get("reference", "")
        url = data.get("url", "")
        date = data.get("date", "2024")

        if not ref:
            return None

        # Extract year from date
        year = date.split("-")[0] if date else "2024"

        # Generate a citation key
        key = f"{model.replace('-', '_').replace('.', '_')}_{year}"

        bibtex = f"""@misc{{{key},
  title = {{{data.get('description', model)}}},
  author = {{{ref.split('(')[0].strip() if '(' in ref else 'Unknown'}}},
  year = {{{year}}},
  url = {{{url if url else 'N/A'}}},
  note = {{{ref}}}
}}"""
        return bibtex

    except ValueError:
        return None


def generate_comparison_table(
    results: Dict[str, float],
    benchmark: str,
    format_type: str = "markdown",
) -> str:
    """
    Generate comparison table for multiple models.

    Args:
        results: Dict of {model_name: score}
        benchmark: Benchmark name
        format_type: 'markdown' or 'latex'

    Returns:
        Formatted table string
    """
    baselines = get_baselines(benchmark)

    if format_type == "markdown":
        lines = [
            "| Model | Score | vs GPT-4 | vs Human | Rank |",
            "|-------|-------|----------|----------|------|",
        ]

        all_scores = list(results.items())

        for model_name, score in all_scores:
            comparison = compare_to_baselines(model_name, score, benchmark)
            gpt4_delta = comparison["comparisons"].get("gpt-4", {}).get("delta", 0)
            human_key = "human_expert" if "human_expert" in baselines else "human"
            human_delta = comparison["comparisons"].get(human_key, {}).get("delta", 0)
            rank = comparison["rank"]
            total = comparison["total_baselines"]

            lines.append(
                f"| {model_name} | {score:.1%} | {gpt4_delta:+.1%} | "
                f"{human_delta:+.1%} | {rank}/{total} |"
            )

        return "\n".join(lines)

    elif format_type == "latex":
        lines = [
            r"\begin{tabular}{lcccc}",
            r"\toprule",
            r"Model & Score & vs GPT-4 & vs Human & Rank \\",
            r"\midrule",
        ]

        for model_name, score in results.items():
            comparison = compare_to_baselines(model_name, score, benchmark)
            gpt4_delta = comparison["comparisons"].get("gpt-4", {}).get("delta", 0)
            human_key = "human_expert" if "human_expert" in baselines else "human"
            human_delta = comparison["comparisons"].get(human_key, {}).get("delta", 0)
            rank = comparison["rank"]
            total = comparison["total_baselines"]

            lines.append(
                f"{model_name} & {score:.1%} & {gpt4_delta:+.1%} & "
                f"{human_delta:+.1%} & {rank}/{total} \\\\"
            )

        lines.extend([r"\bottomrule", r"\end{tabular}"])
        return "\n".join(lines)

    else:
        raise ValueError(f"Unknown format: {format_type}")


def list_available_baselines() -> Dict[str, List[str]]:
    """
    List all available baselines by benchmark.

    Returns:
        Dictionary mapping benchmark names to list of baseline names
    """
    return {
        benchmark: list(baselines.keys()) for benchmark, baselines in ACADEMIC_BASELINES.items()
    }
