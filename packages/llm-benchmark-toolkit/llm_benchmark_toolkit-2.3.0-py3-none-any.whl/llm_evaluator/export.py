"""
Export utilities for academic papers.

Provides LaTeX table generation, BibTeX citations, and reproducibility manifests
for publishing LLM evaluation results.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def export_to_latex(
    results: Dict[str, Dict[str, Any]],
    include_ci: bool = True,
    caption: str = "Benchmark Results Comparison",
    label: str = "tab:results",
    benchmarks: Optional[List[str]] = None,
) -> str:
    """
    Generate LaTeX table ready for paper inclusion.

    Uses booktabs package for professional formatting.

    Args:
        results: {model_name: {mmlu: 0.75, mmlu_ci: (0.72, 0.78), ...}}
        include_ci: Whether to show confidence intervals
        caption: Table caption
        label: LaTeX label for referencing
        benchmarks: List of benchmarks to include (default: mmlu, truthfulqa, hellaswag)

    Returns:
        LaTeX code string with booktabs formatting

    Example:
        >>> results = {'llama': {'mmlu': 0.68, 'mmlu_ci': (0.65, 0.71)}}
        >>> latex = export_to_latex(results)
        >>> print(latex)  # Ready for paper
    """
    if benchmarks is None:
        benchmarks = ["mmlu", "truthfulqa", "hellaswag"]

    # Build header
    header_cols = ["Model"] + [b.upper() for b in benchmarks] + ["Avg"]
    n_cols = len(header_cols)

    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        r"\begin{tabular}{l" + "c" * (n_cols - 1) + "}",
        r"\toprule",
        " & ".join(header_cols) + r" \\",
        r"\midrule",
    ]

    # Add model rows
    for model_name, scores in results.items():
        row_parts = [_escape_latex(model_name)]
        sum_scores = 0.0
        count = 0

        for benchmark in benchmarks:
            score = scores.get(benchmark, scores.get(f"{benchmark}_accuracy"))
            ci = scores.get(f"{benchmark}_ci")

            if score is not None:
                sum_scores += score
                count += 1

                if include_ci and ci is not None:
                    ci_width = (ci[1] - ci[0]) / 2 * 100
                    row_parts.append(f"{score*100:.1f}$\\pm${ci_width:.1f}")
                else:
                    row_parts.append(f"{score*100:.1f}")
            else:
                row_parts.append("--")

        # Average
        if count > 0:
            avg = sum_scores / count
            row_parts.append(f"{avg*100:.1f}")
        else:
            row_parts.append("--")

        lines.append(" & ".join(row_parts) + r" \\")

    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
        ]
    )

    return "\n".join(lines)


def export_comparison_to_latex(
    model_results: Dict[str, float],
    baselines: Dict[str, float],
    benchmark: str,
    highlight_best: bool = True,
    caption: str = "Model Comparison with Published Baselines",
    label: str = "tab:comparison",
) -> str:
    """
    Generate comparison table with baselines.

    Highlights best model in bold, shows deltas from key baselines.

    Args:
        model_results: {model_name: score}
        baselines: {baseline_name: score}
        benchmark: Benchmark name for labeling
        highlight_best: Whether to bold the best score
        caption: Table caption
        label: LaTeX label

    Returns:
        LaTeX table string
    """
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        r"\begin{tabular}{lccc}",
        r"\toprule",
        r"Model & Score & vs GPT-4 & vs Human \\",
        r"\midrule",
    ]

    # Combine all scores to find best
    all_models = {**model_results, **baselines}
    best_score = max(all_models.values()) if all_models else 0

    gpt4_score = baselines.get("gpt-4", baselines.get("gpt_4", 0.864))
    human_score = baselines.get("human", baselines.get("human_expert", 0.95))

    # Add evaluated models first
    for model, score in model_results.items():
        delta_gpt4 = (score - gpt4_score) * 100
        delta_human = (score - human_score) * 100

        score_str = f"{score*100:.1f}"
        if highlight_best and score == best_score:
            score_str = f"\\textbf{{{score_str}}}"

        lines.append(
            f"{_escape_latex(model)} & {score_str} & "
            f"{delta_gpt4:+.1f} & {delta_human:+.1f} \\\\"
        )

    lines.append(r"\midrule")

    # Add baselines
    for baseline, score in baselines.items():
        if baseline in ("gpt-4", "gpt_4"):
            lines.append(f"GPT-4 (baseline) & {score*100:.1f} & -- & -- \\\\")
        elif baseline in ("human", "human_expert"):
            lines.append(f"Human (baseline) & {score*100:.1f} & -- & -- \\\\")

    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
        ]
    )

    return "\n".join(lines)


def generate_bibtex(
    evaluation_metadata: Dict[str, Any],
    entry_type: str = "software",
) -> str:
    """
    Generate BibTeX entry for citing this evaluation.

    Args:
        evaluation_metadata: {
            'version': '1.0.0',
            'date': '2024-12-01',
            'author': 'Name',
            'models_evaluated': ['llama3.2:1b'],
            'n_samples': 1000,
            'github_url': 'https://github.com/...'
        }
        entry_type: BibTeX entry type (software, misc, techreport)

    Returns:
        BibTeX citation string
    """
    version = evaluation_metadata.get("version", "1.0.0")
    date = evaluation_metadata.get("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    author = evaluation_metadata.get("author", "Anonymous")
    n_samples = evaluation_metadata.get("n_samples", "N/A")
    github_url = evaluation_metadata.get("github_url", "")
    models = evaluation_metadata.get("models_evaluated", [])

    year = date.split("-")[0] if "-" in date else date[:4]
    models_str = ", ".join(models[:3]) if models else "various models"

    citation_key = f"llm_evaluation_{year}"

    bibtex = f"""@{entry_type}{{{citation_key},
  title = {{LLM Evaluation Suite: Reproducible Benchmark Framework}},
  author = {{{author}}},
  year = {{{year}}},
  version = {{{version}}},
  url = {{{github_url}}},
  note = {{Evaluated {models_str} on {date} with {n_samples} samples per benchmark}}
}}"""

    return bibtex


def generate_methods_section(
    benchmark_config: Dict[str, Any],
    include_citations: bool = True,
) -> str:
    """
    Generate LaTeX methods section text.

    Returns ready-to-paste paragraph describing evaluation methodology.

    Args:
        benchmark_config: Configuration used for evaluation
        include_citations: Whether to include citation commands

    Returns:
        LaTeX-formatted methods paragraph
    """
    n_samples = benchmark_config.get("n_samples", 1000)
    confidence = benchmark_config.get("confidence_level", 0.95)
    temperature = benchmark_config.get("temperature", 0.0)
    seed = benchmark_config.get("random_seed", 42)

    confidence_pct = int(confidence * 100)

    if include_citations:
        mmlu_cite = r"\citep{hendrycks2021measuring}"
        truthful_cite = r"\citep{lin2022truthfulqa}"
        hellaswag_cite = r"\citep{zellers2019hellaswag}"
        wilson_cite = r"\citep{wilson1927probable}"
        mcnemar_cite = r"\citep{mcnemar1947note}"
    else:
        mmlu_cite = "(Hendrycks et al., 2021)"
        truthful_cite = "(Lin et al., 2022)"
        hellaswag_cite = "(Zellers et al., 2019)"
        wilson_cite = "(Wilson, 1927)"
        mcnemar_cite = "(McNemar, 1947)"

    methods = f"""We evaluated models on three standard benchmarks: MMLU {mmlu_cite},
TruthfulQA {truthful_cite}, and HellaSwag {hellaswag_cite}. For each benchmark,
we sampled {n_samples} questions uniformly at random and computed accuracy with
{confidence_pct}\\% confidence intervals using the Wilson score method {wilson_cite}.
Statistical significance was assessed using McNemar's test {mcnemar_cite} with
$\\alpha = 0.05$. All evaluations used temperature $T = {temperature}$ and
random seed {seed} for reproducibility."""

    return methods


def generate_reproducibility_manifest(
    config: Dict[str, Any],
    results: Dict[str, Any],
    system_info: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Generate complete reproducibility manifest.

    Creates a hashable record of evaluation for verification.

    Args:
        config: Evaluation configuration
        results: Evaluation results
        system_info: Optional system information

    Returns:
        Complete manifest dictionary with SHA256 hash

    Example:
        >>> manifest = generate_reproducibility_manifest(
        ...     config={'temperature': 0.0, 'seed': 42},
        ...     results={'mmlu_accuracy': 0.685}
        ... )
        >>> print(manifest['evaluation_hash'][:16])
    """
    timestamp = datetime.now(timezone.utc).isoformat()

    manifest: Dict[str, Any] = {
        "timestamp": timestamp,
        "framework_version": config.get("version", "2.0.0"),
        "config": {
            "temperature": config.get("temperature", 0.0),
            "top_p": config.get("top_p", 1.0),
            "random_seed": config.get("random_seed", 42),
            "sample_size": config.get("sample_size", 1000),
            "confidence_level": config.get("confidence_level", 0.95),
        },
        "datasets": {
            "mmlu": {
                "version": "cais/mmlu",
                "split": "test",
            },
            "truthfulqa": {
                "version": "truthful_qa",
                "split": "validation",
            },
            "hellaswag": {
                "version": "Rowan/hellaswag",
                "split": "validation",
            },
        },
        "results": _sanitize_results(results),
    }

    if system_info:
        manifest["system_info"] = system_info

    # Compute hash for verification (excluding the hash itself)
    manifest_for_hash = {k: v for k, v in manifest.items() if k != "evaluation_hash"}
    manifest_str = json.dumps(manifest_for_hash, sort_keys=True, default=str)
    evaluation_hash = hashlib.sha256(manifest_str.encode()).hexdigest()

    manifest["evaluation_hash"] = f"sha256:{evaluation_hash}"

    return manifest


def export_results_json(
    results: Dict[str, Any],
    output_path: Optional[str] = None,
    include_manifest: bool = True,
) -> str:
    """
    Export results to JSON format.

    Args:
        results: Evaluation results
        output_path: Optional file path to write
        include_manifest: Whether to include reproducibility manifest

    Returns:
        JSON string
    """
    export_data = {
        "results": results,
        "exported_at": datetime.now(timezone.utc).isoformat(),
    }

    if include_manifest:
        export_data["manifest"] = generate_reproducibility_manifest(
            config=results.get("config", {}),
            results=results,
        )

    json_str = json.dumps(export_data, indent=2, default=str)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_str)

    return json_str


def generate_references_bibtex() -> str:
    """
    Generate BibTeX entries for standard benchmark references.

    Returns:
        BibTeX string with all standard citations
    """
    return r"""@inproceedings{hendrycks2021measuring,
  title={Measuring Massive Multitask Language Understanding},
  author={Hendrycks, Dan and Burns, Collin and Basart, Steven and Zou, Andy and Mazeika, Mantas and Song, Dawn and Steinhardt, Jacob},
  booktitle={International Conference on Learning Representations},
  year={2021}
}

@inproceedings{lin2022truthfulqa,
  title={TruthfulQA: Measuring How Models Mimic Human Falsehoods},
  author={Lin, Stephanie and Hilton, Jacob and Evans, Owain},
  booktitle={Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics},
  year={2022}
}

@inproceedings{zellers2019hellaswag,
  title={HellaSwag: Can a Machine Really Finish Your Sentence?},
  author={Zellers, Rowan and Holtzman, Ari and Bisk, Yonatan and Farhadi, Ali and Choi, Yejin},
  booktitle={Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics},
  year={2019}
}

@article{wilson1927probable,
  title={Probable inference, the law of succession, and statistical inference},
  author={Wilson, Edwin B},
  journal={Journal of the American Statistical Association},
  volume={22},
  number={158},
  pages={209--212},
  year={1927}
}

@article{mcnemar1947note,
  title={Note on the sampling error of the difference between correlated proportions or percentages},
  author={McNemar, Quinn},
  journal={Psychometrika},
  volume={12},
  number={2},
  pages={153--157},
  year={1947}
}

@inproceedings{guo2017calibration,
  title={On Calibration of Modern Neural Networks},
  author={Guo, Chuan and Pleiss, Geoff and Sun, Yu and Weinberger, Kilian Q},
  booktitle={International Conference on Machine Learning},
  year={2017}
}
"""


def _escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


def _sanitize_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize results for JSON serialization."""
    sanitized: Dict[str, Any] = {}
    for key, value in results.items():
        if isinstance(value, (int, float, str, bool, type(None))):
            sanitized[key] = value
        elif isinstance(value, (list, tuple)):
            sanitized[key] = [
                v if isinstance(v, (int, float, str, bool, type(None))) else str(v) for v in value
            ]
        elif isinstance(value, dict):
            sanitized[key] = _sanitize_results(value)
        else:
            sanitized[key] = str(value)
    return sanitized
