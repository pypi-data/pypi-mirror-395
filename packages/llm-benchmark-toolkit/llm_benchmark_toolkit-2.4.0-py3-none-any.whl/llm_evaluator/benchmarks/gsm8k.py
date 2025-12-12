"""
GSM8K benchmark - grade school math word problems.

Tests mathematical reasoning and problem-solving abilities.
Dataset: 1,319 test problems requiring multi-step arithmetic.
"""

import logging
import re
from typing import Any, Dict, List, Tuple

from ..dataset_loaders import load_gsm8k_dataset
from ..providers import GenerationResult
from .base import Benchmark

logger = logging.getLogger(__name__)


class GSM8KBenchmark(Benchmark):
    """GSM8K grade school math benchmark"""

    @property
    def name(self) -> str:
        return "GSM8K"

    @property
    def emoji(self) -> str:
        return "🔢"

    def load_dataset(self) -> Any:
        """Load GSM8K test split (1,319 problems)"""
        dataset = load_gsm8k_dataset()
        return dataset["test"]

    def get_demo_data(self) -> List[Dict[str, Any]]:
        """Get 3 demo math problems"""
        return [
            {
                "question": "James has 5 apples. He gives 2 to his friend. How many apples does James have left?",
                "answer": "3",
            },
            {
                "question": "A store sells pencils for $2 each. If you buy 4 pencils, how much do you pay in total?",
                "answer": "8",
            },
            {
                "question": "Sarah ran 3 miles on Monday and 5 miles on Tuesday. How many total miles did she run?",
                "answer": "8",
            },
        ]

    def format_prompt(self, item: Any) -> str:
        """Format GSM8K math problem"""
        question = item["question"]

        prompt = f"{question}\n\nAnswer with only the final number:"

        return prompt

    def evaluate_response(
        self, item: Any, response: GenerationResult
    ) -> Tuple[bool, Dict[str, Any]]:
        """Evaluate GSM8K response (extract and compare final number)"""
        question = item["question"]
        correct_answer = item["answer"]

        # Extract numeric answer from correct answer string
        # (dataset format: "#### 42" or just "42")
        if "####" in correct_answer:
            correct_number = correct_answer.split("####")[-1].strip()
        else:
            correct_number = correct_answer.strip()

        # Remove commas and normalize
        correct_number = correct_number.replace(",", "")

        response_text = response.text.strip()

        # Extract numbers from response (find last number as final answer)
        numbers = re.findall(r"-?\d+(?:,\d{3})*(?:\.\d+)?", response_text)

        # Remove commas from extracted numbers
        numbers = [n.replace(",", "") for n in numbers]

        # Check if correct number appears (prefer last number as final answer)
        is_correct = False
        if numbers:
            # Try last number first (most likely final answer)
            if numbers[-1] == correct_number:
                is_correct = True
            # Fallback: check if correct number appears anywhere
            elif correct_number in numbers:
                is_correct = True

        scenario = {
            "question": question,
            "correct_answer": correct_number,
            "model_response": response_text,
            "is_correct": is_correct,
            "extracted_numbers": numbers,
        }

        return is_correct, scenario
