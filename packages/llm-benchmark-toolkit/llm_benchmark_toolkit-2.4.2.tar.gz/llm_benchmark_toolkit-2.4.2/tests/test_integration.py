"""
Quick test to verify full benchmarks integration works correctly
"""

from llm_evaluator.benchmarks import (
    DATASETS_AVAILABLE,
    BenchmarkRunner,
    load_hellaswag_dataset,
    load_mmlu_dataset,
    load_truthfulqa_dataset,
)


def test_datasets_available() -> None:
    """Verify datasets library is installed"""
    print("✓ Testing datasets library availability...")
    assert DATASETS_AVAILABLE, "datasets library not installed"
    print("  ✅ datasets library is available")


def test_demo_mode() -> None:
    """Test that demo mode works (no actual LLM calls)"""
    print("\n✓ Testing demo mode initialization...")
    from unittest.mock import Mock

    from llm_evaluator.providers import GenerationResult, LLMProvider

    # Mock provider
    provider = Mock(spec=LLMProvider)
    provider.model = "test-model"
    provider.generate.return_value = GenerationResult(
        text="Test response", response_time=0.1, tokens_used=5, model="test-model", metadata={}
    )

    # Test demo mode
    runner = BenchmarkRunner(provider, use_full_datasets=False)
    assert runner.use_full_datasets is False
    print("  ✅ Demo mode works")


def test_full_mode_initialization() -> None:
    """Test that full mode can be initialized"""
    print("\n✓ Testing full mode initialization...")
    from unittest.mock import Mock

    from llm_evaluator.providers import LLMProvider

    provider = Mock(spec=LLMProvider)
    provider.model = "test-model"

    runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=10)
    assert runner.use_full_datasets is True
    assert runner.sample_size == 10
    print("  ✅ Full mode initialization works")


def test_dataset_loading() -> None:
    """Test that datasets can be loaded (may take a moment)"""
    print("\n✓ Testing dataset loading from HuggingFace...")

    print("  Loading MMLU...")
    mmlu = load_mmlu_dataset()
    assert mmlu is not None
    mmlu_test = mmlu["test"]  # type: ignore[index]
    print(f"    ✅ MMLU loaded ({len(mmlu_test)} questions)")  # type: ignore[arg-type]

    print("  Loading TruthfulQA...")
    truthfulqa = load_truthfulqa_dataset()
    assert truthfulqa is not None
    truthfulqa_val = truthfulqa["validation"]  # type: ignore[index]
    print(f"    ✅ TruthfulQA loaded ({len(truthfulqa_val)} questions)")  # type: ignore[arg-type]

    print("  Loading HellaSwag...")
    hellaswag = load_hellaswag_dataset()
    assert hellaswag is not None
    hellaswag_val = hellaswag["validation"]  # type: ignore[index]
    print(f"    ✅ HellaSwag loaded ({len(hellaswag_val)} scenarios)")  # type: ignore[arg-type]


if __name__ == "__main__":
    print("=" * 60)
    print("FULL BENCHMARKS INTEGRATION TEST")
    print("=" * 60)

    try:
        test_datasets_available()
        test_demo_mode()
        test_full_mode_initialization()
        test_dataset_loading()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\n🎉 Full benchmark integration is working correctly!")
        print("\nNext steps:")
        print("1. Run demo: python demo_full_benchmarks.py")
        print("2. Read docs: FULL_BENCHMARKS.md")
        print("3. Run tests: python -m pytest tests/test_full_benchmarks.py -v")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
