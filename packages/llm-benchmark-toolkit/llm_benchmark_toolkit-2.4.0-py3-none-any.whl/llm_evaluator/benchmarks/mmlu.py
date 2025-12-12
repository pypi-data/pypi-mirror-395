"""
MMLU (Massive Multitask Language Understanding) benchmark.

Tests knowledge across 57 subjects including STEM, humanities, social sciences.
Dataset: 14,042 test questions with 4 choices each.
"""

import logging
from typing import Any, Dict, List, Tuple

from ..dataset_loaders import load_mmlu_dataset
from ..providers import GenerationResult
from .base import MultipleChoiceBenchmark

logger = logging.getLogger(__name__)


class MMLUBenchmark(MultipleChoiceBenchmark):
    """MMLU multiple choice knowledge benchmark"""

    @property
    def name(self) -> str:
        return "MMLU"

    @property
    def emoji(self) -> str:
        return "📚"

    def load_dataset(self) -> Any:
        """Load MMLU test split (14,042 questions)"""
        dataset = load_mmlu_dataset()
        return dataset["test"]

    def get_demo_data(self) -> List[Dict[str, Any]]:
        """Get 3 demo questions covering different subjects"""
        return [
            {
                "question": "What is the capital of France?",
                "choices": ["London", "Berlin", "Paris", "Madrid"],
                "answer": 2,  # Index of correct answer
                "subject": "geography",
            },
            {
                "question": "What is the largest planet in our solar system?",
                "choices": ["Earth", "Mars", "Jupiter", "Saturn"],
                "answer": 2,
                "subject": "astronomy",
            },
            {
                "question": "Who wrote 'Romeo and Juliet'?",
                "choices": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                "answer": 1,
                "subject": "literature",
            },
        ]

    def format_prompt(self, item: Any) -> str:
        """Format MMLU question with choices"""
        question = item["question"]
        choices = item["choices"]

        # Format choices with letters
        choices_str = "\n".join([f"{chr(65+j)}) {choice}" for j, choice in enumerate(choices)])

        # Simple prompt without subject context (was confusing small models)
        prompt = f"{question}\n\n{choices_str}\n\n" f"Answer with only the letter (A, B, C, or D):"

        return prompt

    def evaluate_response(
        self, item: Any, response: GenerationResult
    ) -> Tuple[bool, Dict[str, Any]]:
        """Evaluate MMLU response with exact matching + letter extraction"""
        question = item["question"]
        choices = item["choices"]
        correct_answer_idx = item["answer"]
        correct_answer = choices[correct_answer_idx]
        correct_letter = chr(65 + correct_answer_idx)
        subject = item.get("subject", "unknown")

        response_text = response.text.strip()

        # Strategy 1: Letter extraction first (most reliable for MCQ)
        is_correct = self._extract_mcq_answer(response_text, correct_letter, len(choices))

        # Strategy 2: Text matching fallback (strict - no incorrect options)
        if not is_correct:
            response_lower = response_text.lower()

            # Check for echoing
            num_options_in_response = sum(
                1 for choice in choices if choice.lower() in response_lower and len(choice) > 5
            )
            is_echoing = num_options_in_response >= len(choices) - 1

            # Only use text matching if not echoing
            if not is_echoing:
                correct_lower = correct_answer.lower()
                # Check correct answer appears
                if correct_lower in response_lower:
                    # But also check that NO incorrect answers appear
                    incorrect_in_response = any(
                        choice.lower() in response_lower
                        for i, choice in enumerate(choices)
                        if i != correct_answer_idx and len(choice) > 5
                    )
                    if not incorrect_in_response:
                        is_correct = True

        # Build scenario data
        scenario = {
            "question": question,
            "choices": choices,
            "correct_answer": correct_answer,
            "correct_letter": correct_letter,
            "model_response": response_text,
            "is_correct": is_correct,
            "subject": subject,
        }

        return is_correct, scenario
