"""
Dataset loaders for LLM benchmarks.

Provides cached loading of benchmark datasets from HuggingFace.
Each loader is cached to avoid redundant downloads.
"""

import logging
from functools import lru_cache
from typing import Any

logger = logging.getLogger(__name__)

# Check datasets availability
try:
    from datasets import load_dataset

    DATASETS_AVAILABLE = True
except ImportError:
    DATASETS_AVAILABLE = False
    logger.warning("datasets library not available. Install with: pip install datasets")


# ==================== KNOWLEDGE BENCHMARKS ====================


@lru_cache(maxsize=1)
def load_mmlu_dataset() -> Any:
    """Load and cache MMLU dataset (14,042 questions)"""
    if not DATASETS_AVAILABLE:
        raise ImportError("datasets library required. Install with: pip install datasets")
    logger.info("Loading MMLU dataset from HuggingFace...")
    return load_dataset("cais/mmlu", "all")


@lru_cache(maxsize=1)
def load_truthfulqa_dataset() -> Any:
    """Load and cache TruthfulQA dataset (817 questions) - multiple choice format"""
    if not DATASETS_AVAILABLE:
        raise ImportError("datasets library required. Install with: pip install datasets")
    logger.info("Loading TruthfulQA dataset from HuggingFace (multiple_choice config)...")
    return load_dataset("truthful_qa", "multiple_choice")


@lru_cache(maxsize=1)
def load_hellaswag_dataset() -> Any:
    """Load and cache HellaSwag dataset (10,042 scenarios)"""
    if not DATASETS_AVAILABLE:
        raise ImportError("datasets library required. Install with: pip install datasets")
    logger.info("Loading HellaSwag dataset from HuggingFace...")
    return load_dataset("Rowan/hellaswag")


@lru_cache(maxsize=1)
def load_arc_dataset() -> Any:
    """Load and cache ARC-Challenge dataset (2,590 science questions)"""
    if not DATASETS_AVAILABLE:
        raise ImportError("datasets library required. Install with: pip install datasets")
    logger.info("Loading ARC-Challenge dataset from HuggingFace...")
    return load_dataset("allenai/ai2_arc", "ARC-Challenge")


@lru_cache(maxsize=1)
def load_winogrande_dataset() -> Any:
    """Load and cache WinoGrande dataset (44,000 pronoun resolution questions)"""
    if not DATASETS_AVAILABLE:
        raise ImportError("datasets library required. Install with: pip install datasets")
    logger.info("Loading WinoGrande dataset from HuggingFace...")
    return load_dataset("winogrande", "winogrande_xl")


@lru_cache(maxsize=1)
def load_commonsenseqa_dataset() -> Any:
    """Load and cache CommonsenseQA dataset (12,247 commonsense questions)"""
    if not DATASETS_AVAILABLE:
        raise ImportError("datasets library required. Install with: pip install datasets")
    logger.info("Loading CommonsenseQA dataset from HuggingFace...")
    return load_dataset("commonsense_qa")


@lru_cache(maxsize=1)
def load_boolq_dataset() -> Any:
    """Load and cache BoolQ dataset (15,942 yes/no questions)"""
    if not DATASETS_AVAILABLE:
        raise ImportError("datasets library required. Install with: pip install datasets")
    logger.info("Loading BoolQ dataset from HuggingFace...")
    return load_dataset("boolq")


# ==================== SECURITY BENCHMARKS ====================


@lru_cache(maxsize=1)
def load_safetybench_dataset() -> Any:
    """
    Load and cache SafetyBench dataset (dev split with answers, 35 questions)

    Note: Using 'dev' config because 'test' config answers are not publicly available.
    Dev config has 'en' and 'zh' splits with 5 examples per safety category (35 total).
    """
    if not DATASETS_AVAILABLE:
        raise ImportError("datasets library required. Install with: pip install datasets")
    logger.info("Loading SafetyBench dataset (dev config) from HuggingFace...")
    # The 'dev' config has splits: 'en' (English) and 'zh' (Chinese)
    dataset = load_dataset("thu-coai/SafetyBench", "dev")
    return dataset


@lru_cache(maxsize=1)
def load_donotanswer_dataset() -> Any:
    """Load and cache Do-Not-Answer dataset (939 harmful prompts)"""
    if not DATASETS_AVAILABLE:
        raise ImportError("datasets library required. Install with: pip install datasets")
    logger.info("Loading Do-Not-Answer dataset from HuggingFace...")
    dataset = load_dataset("LibrAI/do-not-answer")
    return dataset


# ==================== MATH REASONING BENCHMARKS ====================


@lru_cache(maxsize=1)
def load_gsm8k_dataset() -> Any:
    """Load and cache GSM8K dataset (8,500 grade school math problems)"""
    if not DATASETS_AVAILABLE:
        raise ImportError("datasets library required. Install with: pip install datasets")
    logger.info("Loading GSM8K dataset from HuggingFace...")
    return load_dataset("gsm8k", "main")


# ==================== CODE GENERATION BENCHMARKS ====================


@lru_cache(maxsize=1)
def load_humaneval_dataset() -> Any:
    """Load and cache HumanEval dataset (164 Python programming problems)"""
    if not DATASETS_AVAILABLE:
        raise ImportError("datasets library required. Install with: pip install datasets")
    logger.info("Loading HumanEval dataset from HuggingFace...")
    return load_dataset("openai_humaneval")
