"""
BoolQ benchmark - yes/no question answering.

Tests model ability to answer boolean questions from passages.
Dataset: Validation split with passage + question pairs.
"""

import logging
from typing import Any, Dict, List, Tuple

from ..dataset_loaders import load_boolq_dataset
from ..providers import GenerationResult
from .base import Benchmark

logger = logging.getLogger(__name__)


class BoolQBenchmark(Benchmark):
    """BoolQ boolean question answering benchmark"""

    @property
    def name(self) -> str:
        return "BoolQ"

    @property
    def emoji(self) -> str:
        return "❓"

    def load_dataset(self) -> Any:
        """Load BoolQ validation split"""
        dataset = load_boolq_dataset()
        return dataset["validation"]

    def get_demo_data(self) -> List[Dict[str, Any]]:
        """Get 3 demo boolean questions"""
        return [
            {
                "passage": "The sky is blue because of Rayleigh scattering.",
                "question": "Is the sky blue?",
                "answer": True,
            },
            {
                "passage": "Humans cannot breathe underwater without assistance.",
                "question": "Can humans breathe underwater naturally?",
                "answer": False,
            },
            {
                "passage": "The Earth orbits around the Sun, not the other way around.",
                "question": "Does the Sun orbit the Earth?",
                "answer": False,
            },
        ]

    def format_prompt(self, item: Any) -> str:
        """Format BoolQ question with passage"""
        passage = item["passage"]
        question = item["question"]

        prompt = (
            f"Passage: {passage}\n\n"
            f"Question: {question}\n\n"
            f"Answer with ONLY 'yes' or 'no', nothing else:"
        )

        return prompt

    def evaluate_response(
        self, item: Any, response: GenerationResult
    ) -> Tuple[bool, Dict[str, Any]]:
        """Evaluate BoolQ response (yes/no matching)"""
        passage = item["passage"]
        question = item["question"]
        correct_answer = item["answer"]

        response_text = response.text.strip().lower()

        # Check for yes/no in response
        has_yes = "yes" in response_text
        has_no = "no" in response_text

        # Determine correctness
        if correct_answer:
            # Correct answer is True/yes
            is_correct = has_yes and not (
                has_no and response_text.index("no") < response_text.index("yes")
            )
        else:
            # Correct answer is False/no
            is_correct = has_no and not (
                has_yes and response_text.index("yes") < response_text.index("no")
            )

        scenario = {
            "passage": passage[:200] + "..." if len(passage) > 200 else passage,
            "question": question,
            "correct_answer": "yes" if correct_answer else "no",
            "model_response": response_text,
            "is_correct": is_correct,
        }

        return is_correct, scenario
