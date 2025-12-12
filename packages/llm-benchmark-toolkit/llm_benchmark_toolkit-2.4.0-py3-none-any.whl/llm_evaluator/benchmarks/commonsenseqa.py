"""
CommonsenseQA benchmark - commonsense reasoning questions.

Tests model ability to answer questions requiring commonsense knowledge.
Dataset: Validation split with 5-choice questions.
"""

import logging
from typing import Any, Dict, List, Tuple

from ..dataset_loaders import load_commonsenseqa_dataset
from ..providers import GenerationResult
from .base import MultipleChoiceBenchmark

logger = logging.getLogger(__name__)


class CommonsenseQABenchmark(MultipleChoiceBenchmark):
    """CommonsenseQA reasoning benchmark"""

    @property
    def name(self) -> str:
        return "CommonsenseQA"

    @property
    def emoji(self) -> str:
        return "💡"

    def load_dataset(self) -> Any:
        """Load CommonsenseQA validation split"""
        dataset = load_commonsenseqa_dataset()
        return dataset["validation"]

    def get_demo_data(self) -> List[Dict[str, Any]]:
        """Get 3 demo commonsense questions"""
        return [
            {
                "question": "Where would you put uncooked food that you want to eat soon?",
                "choices": {
                    "label": ["A", "B", "C", "D", "E"],
                    "text": [
                        "pantry",
                        "refrigerator",
                        "supermarket",
                        "container",
                        "kitchen",
                    ],
                },
                "answerKey": "B",
            },
            {
                "question": "What do people typically do when they are bored?",
                "choices": {
                    "label": ["A", "B", "C", "D", "E"],
                    "text": [
                        "sleep",
                        "watch television",
                        "play games",
                        "talk to friends",
                        "all of the above",
                    ],
                },
                "answerKey": "E",
            },
            {
                "question": "What is the opposite of day?",
                "choices": {
                    "label": ["A", "B", "C", "D", "E"],
                    "text": ["light", "night", "morning", "afternoon", "evening"],
                },
                "answerKey": "B",
            },
        ]

    def format_prompt(self, item: Any) -> str:
        """Format CommonsenseQA question with 5 choices"""
        question = item["question"]
        choices_data = item["choices"]

        # Extract choices and labels
        labels = choices_data["label"]
        texts = choices_data["text"]

        # Format choices with letters
        choices_str = "\n".join([f"{label}) {text}" for label, text in zip(labels, texts)])

        # Simple prompt
        prompt = f"{question}\n\n{choices_str}\n\nAnswer with only the letter:"

        return prompt

    def evaluate_response(
        self, item: Any, response: GenerationResult
    ) -> Tuple[bool, Dict[str, Any]]:
        """Evaluate CommonsenseQA response with exact matching + letter extraction"""
        question = item["question"]
        choices_data = item["choices"]
        correct_letter = item["answerKey"]

        # Extract choices
        labels = choices_data["label"]
        texts = choices_data["text"]

        # Find correct answer text
        correct_idx = labels.index(correct_letter)
        correct_text = texts[correct_idx]

        response_text = response.text.strip()

        # Strategy 1: Letter extraction first (most reliable for MCQ)
        is_correct = self._extract_mcq_answer(response_text, correct_letter, len(texts))

        # Strategy 2: Text matching fallback (but only if no echoing)
        if not is_correct:
            # Check for echoing - if model repeats all options, it's invalid
            response_lower = response_text.lower()
            num_options_in_response = sum(
                1 for text in texts if text.lower() in response_lower and len(text) > 5
            )
            is_echoing = num_options_in_response >= len(texts) - 1

            # Only use text matching if not echoing
            if not is_echoing:
                correct_lower = correct_text.lower()
                # Check correct answer appears
                if correct_lower in response_lower:
                    # But also check that NO incorrect answers appear
                    incorrect_in_response = any(
                        text.lower() in response_lower
                        for i, text in enumerate(texts)
                        if i != correct_idx and len(text) > 5
                    )
                    if not incorrect_in_response:
                        is_correct = True

        scenario = {
            "question": question,
            "choices": texts,
            "correct_answer": correct_text,
            "correct_letter": correct_letter,
            "model_response": response_text,
            "is_correct": is_correct,
        }

        return is_correct, scenario
