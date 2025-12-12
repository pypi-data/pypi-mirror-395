"""
Extended tests for export module - LaTeX, BibTeX, and manifests
"""

import json


class TestExportToLatex:
    """Test LaTeX export functionality"""

    def test_export_to_latex_basic(self):
        """Test basic LaTeX export"""
        from llm_evaluator.export import export_to_latex

        results = {"llama3": {"mmlu": 0.75, "truthfulqa": 0.65, "hellaswag": 0.70}}

        latex = export_to_latex(results)

        assert r"\begin{table}" in latex
        assert r"\end{table}" in latex
        assert "llama3" in latex

    def test_export_to_latex_with_ci(self):
        """Test LaTeX export with confidence intervals"""
        from llm_evaluator.export import export_to_latex

        results = {
            "model": {"mmlu": 0.75, "mmlu_ci": (0.70, 0.80), "truthfulqa": 0.65, "hellaswag": 0.70}
        }

        latex = export_to_latex(results, include_ci=True)

        assert r"\pm" in latex

    def test_export_to_latex_custom_caption(self):
        """Test LaTeX export with custom caption"""
        from llm_evaluator.export import export_to_latex

        results = {"model": {"mmlu": 0.5, "truthfulqa": 0.5, "hellaswag": 0.5}}

        latex = export_to_latex(results, caption="Custom Caption")

        assert "Custom Caption" in latex

    def test_export_to_latex_custom_label(self):
        """Test LaTeX export with custom label"""
        from llm_evaluator.export import export_to_latex

        results = {"model": {"mmlu": 0.5, "truthfulqa": 0.5, "hellaswag": 0.5}}

        latex = export_to_latex(results, label="tab:custom")

        assert "tab:custom" in latex

    def test_export_to_latex_missing_benchmarks(self):
        """Test LaTeX export handles missing benchmarks"""
        from llm_evaluator.export import export_to_latex

        results = {"model": {"mmlu": 0.5}}  # Missing truthfulqa, hellaswag

        latex = export_to_latex(results)

        assert "--" in latex  # Missing values shown as --

    def test_export_to_latex_multiple_models(self):
        """Test LaTeX export with multiple models"""
        from llm_evaluator.export import export_to_latex

        results = {
            "model1": {"mmlu": 0.75, "truthfulqa": 0.65, "hellaswag": 0.70},
            "model2": {"mmlu": 0.80, "truthfulqa": 0.70, "hellaswag": 0.75},
        }

        latex = export_to_latex(results)

        assert "model1" in latex
        assert "model2" in latex


class TestReproducibilityManifest:
    """Test reproducibility manifest generation"""

    def test_generate_manifest_structure(self):
        """Test manifest has required structure"""
        from llm_evaluator.export import generate_reproducibility_manifest

        manifest = generate_reproducibility_manifest(
            config={"temperature": 0.0, "seed": 42}, results={"mmlu_accuracy": 0.75}
        )

        assert isinstance(manifest, dict)
        assert "timestamp" in manifest
        assert "config" in manifest

    def test_manifest_includes_timestamp(self):
        """Test manifest includes timestamp"""
        from llm_evaluator.export import generate_reproducibility_manifest

        manifest = generate_reproducibility_manifest(
            config={"temperature": 0.0}, results={"accuracy": 0.75}
        )

        assert "timestamp" in manifest

    def test_manifest_includes_hash(self):
        """Test manifest includes evaluation hash"""
        from llm_evaluator.export import generate_reproducibility_manifest

        manifest = generate_reproducibility_manifest(config={}, results={})

        assert "evaluation_hash" in manifest
        assert manifest["evaluation_hash"].startswith("sha256:")


class TestBibTexExport:
    """Test BibTeX citation export"""

    def test_generate_bibtex_structure(self):
        """Test BibTeX export generates valid structure"""
        from llm_evaluator.export import generate_bibtex

        metadata = {"version": "1.0.0", "date": "2024-01-01", "author": "Test Author"}

        bibtex = generate_bibtex(metadata)

        assert "@" in bibtex
        assert "title" in bibtex.lower()

    def test_generate_references_bibtex(self):
        """Test generating reference BibTeX entries"""
        from llm_evaluator.export import generate_references_bibtex

        bibtex = generate_references_bibtex()

        assert "@inproceedings" in bibtex
        assert "hendrycks" in bibtex.lower()


class TestLatexEscaping:
    """Test LaTeX special character escaping"""

    def test_escape_latex_underscore(self):
        """Test underscore is escaped"""
        from llm_evaluator.export import _escape_latex

        result = _escape_latex("model_name")

        assert "\\_" in result or "_" not in result or "model\\_name" == result

    def test_escape_latex_ampersand(self):
        """Test ampersand is escaped"""
        from llm_evaluator.export import _escape_latex

        result = _escape_latex("A & B")

        assert "\\&" in result or "&" not in result


class TestExportWithAccuracy:
    """Test export using _accuracy suffix"""

    def test_export_uses_accuracy_suffix(self):
        """Test export accepts benchmark_accuracy format"""
        from llm_evaluator.export import export_to_latex

        results = {
            "model": {
                "mmlu_accuracy": 0.75,
                "truthfulqa_accuracy": 0.65,
                "hellaswag_accuracy": 0.70,
            }
        }

        latex = export_to_latex(results)

        # Should use these values
        assert "75" in latex  # 0.75 * 100


class TestExportResultsJson:
    """Test JSON export functionality"""

    def test_export_results_json(self):
        """Test exporting results to JSON"""
        from llm_evaluator.export import export_results_json

        results = {"model": "test-model", "accuracy": 0.75}

        json_str = export_results_json(results)

        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert "results" in parsed

    def test_export_results_json_includes_manifest(self):
        """Test JSON export includes manifest by default"""
        from llm_evaluator.export import export_results_json

        results = {"accuracy": 0.75}

        json_str = export_results_json(results, include_manifest=True)
        parsed = json.loads(json_str)

        assert "manifest" in parsed


class TestExportComparisonToLatex:
    """Test comparison table export"""

    def test_export_comparison_basic(self):
        """Test basic comparison table export"""
        from llm_evaluator.export import export_comparison_to_latex

        model_results = {"mymodel": 0.75}
        baselines = {"gpt-4": 0.864, "human": 0.95}

        latex = export_comparison_to_latex(
            model_results=model_results, baselines=baselines, benchmark="mmlu"
        )

        assert r"\begin{table}" in latex
        assert "mymodel" in latex
        assert "GPT-4" in latex


class TestGenerateMethodsSection:
    """Test methods section generation"""

    def test_generate_methods_section(self):
        """Test methods section generation"""
        from llm_evaluator.export import generate_methods_section

        config = {"n_samples": 1000, "temperature": 0.0, "random_seed": 42}

        methods = generate_methods_section(config)

        assert "MMLU" in methods
        assert "TruthfulQA" in methods
        assert "1000" in methods

    def test_generate_methods_without_citations(self):
        """Test methods section without citations"""
        from llm_evaluator.export import generate_methods_section

        config = {}

        methods = generate_methods_section(config, include_citations=False)

        # Should use author-year format instead of citep
        assert "Hendrycks" in methods or "hendrycks" in methods.lower()
