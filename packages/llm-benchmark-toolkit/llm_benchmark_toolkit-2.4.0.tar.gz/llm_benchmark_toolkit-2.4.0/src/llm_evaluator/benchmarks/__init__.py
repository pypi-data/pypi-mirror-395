"""
Benchmark module with clean architecture.

This module provides a base class for all benchmarks and specific implementations.
"""

from ..dataset_loaders import (
    DATASETS_AVAILABLE,
    load_arc_dataset,
    load_boolq_dataset,
    load_commonsenseqa_dataset,
    load_donotanswer_dataset,
    load_gsm8k_dataset,
    load_hellaswag_dataset,
    load_humaneval_dataset,
    load_mmlu_dataset,
    load_safetybench_dataset,
    load_truthfulqa_dataset,
    load_winogrande_dataset,
)
from .arc import ARCBenchmark
from .base import Benchmark, MultipleChoiceBenchmark
from .boolq import BoolQBenchmark
from .commonsenseqa import CommonsenseQABenchmark
from .donotanswer import DoNotAnswerBenchmark
from .gsm8k import GSM8KBenchmark
from .hellaswag import HellaSwagBenchmark
from .mmlu import MMLUBenchmark
from .runner import BenchmarkRunner
from .safetybench import SafetyBenchBenchmark
from .truthfulqa import TruthfulQABenchmark
from .winogrande import WinoGrandeBenchmark

__all__ = [
    "DATASETS_AVAILABLE",
    "load_mmlu_dataset",
    "load_truthfulqa_dataset",
    "load_hellaswag_dataset",
    "load_arc_dataset",
    "load_winogrande_dataset",
    "load_commonsenseqa_dataset",
    "load_boolq_dataset",
    "load_safetybench_dataset",
    "load_donotanswer_dataset",
    "load_gsm8k_dataset",
    "load_humaneval_dataset",
    "Benchmark",
    "MultipleChoiceBenchmark",
    "MMLUBenchmark",
    "TruthfulQABenchmark",
    "HellaSwagBenchmark",
    "ARCBenchmark",
    "WinoGrandeBenchmark",
    "CommonsenseQABenchmark",
    "BoolQBenchmark",
    "SafetyBenchBenchmark",
    "DoNotAnswerBenchmark",
    "GSM8KBenchmark",
    "BenchmarkRunner",
]
