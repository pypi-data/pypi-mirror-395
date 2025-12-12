"""
ARC (AI2 Reasoning Challenge) benchmark - science questions.

Tests scientific reasoning across grade school level questions.
Dataset: 2,590 Challenge set questions (harder subset).
"""

import logging
from typing import Any, Dict, List, Tuple

from ..dataset_loaders import load_arc_dataset
from ..providers import GenerationResult
from .base import MultipleChoiceBenchmark

logger = logging.getLogger(__name__)


class ARCBenchmark(MultipleChoiceBenchmark):
    """ARC science reasoning benchmark"""

    @property
    def name(self) -> str:
        return "ARC"

    @property
    def emoji(self) -> str:
        return "🔬"

    def load_dataset(self) -> Any:
        """Load ARC-Challenge test split (2,590 questions)"""
        dataset = load_arc_dataset()
        return dataset["test"]

    def get_demo_data(self) -> List[Dict[str, Any]]:
        """Get 3 demo science questions"""
        return [
            {
                "question": "Which of these is a renewable resource?",
                "choices": {
                    "text": ["Coal", "Oil", "Solar energy", "Natural gas"],
                    "label": ["A", "B", "C", "D"],
                },
                "answerKey": "C",
            },
            {
                "question": "What is the primary function of roots in plants?",
                "choices": {
                    "text": [
                        "Photosynthesis",
                        "Absorbing water and nutrients",
                        "Producing flowers",
                        "Storing glucose",
                    ],
                    "label": ["A", "B", "C", "D"],
                },
                "answerKey": "B",
            },
            {
                "question": "Which phase of matter has a definite volume but no definite shape?",
                "choices": {
                    "text": ["Solid", "Liquid", "Gas", "Plasma"],
                    "label": ["A", "B", "C", "D"],
                },
                "answerKey": "B",
            },
        ]

    def format_prompt(self, item: Any) -> str:
        """Format ARC question with choices"""
        question = item["question"]
        choices_data = item["choices"]

        # Extract choices and labels
        if isinstance(choices_data, dict):
            texts = choices_data["text"]
            labels = choices_data["label"]
        else:
            # Fallback for different format
            texts = [c["text"] for c in choices_data]
            labels = [c["label"] for c in choices_data]

        # Format choices with letters
        choices_str = "\n".join([f"{label}) {text}" for label, text in zip(labels, texts)])

        # Simple prompt without verbose instructions
        prompt = f"{question}\n\n{choices_str}\n\nAnswer with only the letter:"

        return prompt

    def evaluate_response(
        self, item: Any, response: GenerationResult
    ) -> Tuple[bool, Dict[str, Any]]:
        """Evaluate ARC response with exact matching + letter extraction"""
        question = item["question"]
        choices_data = item["choices"]
        correct_letter = item["answerKey"]

        # Extract choices
        if isinstance(choices_data, dict):
            texts = choices_data["text"]
            labels = choices_data["label"]
        else:
            texts = [c["text"] for c in choices_data]
            labels = [c["label"] for c in choices_data]

        # Find correct answer text
        correct_idx = labels.index(correct_letter)
        correct_text = texts[correct_idx]

        response_text = response.text.strip()

        # Strategy 1: Letter extraction first (most reliable for MCQ)
        is_correct = self._extract_mcq_answer(response_text, correct_letter, len(texts))

        # Strategy 2: Text matching fallback (strict - no incorrect options)
        if not is_correct:
            response_lower = response_text.lower()

            # Check for echoing
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
