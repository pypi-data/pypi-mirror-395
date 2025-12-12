"""
WinoGrande benchmark - commonsense reasoning via pronoun resolution.

Tests model ability to resolve ambiguous pronouns using commonsense.
Dataset: ~1,767 validation scenarios with 2 options each.
"""

import logging
import re
from typing import Any, Dict, List, Tuple

from ..dataset_loaders import load_winogrande_dataset
from ..providers import GenerationResult
from .base import MultipleChoiceBenchmark

logger = logging.getLogger(__name__)


class WinoGrandeBenchmark(MultipleChoiceBenchmark):
    """WinoGrande pronoun resolution benchmark"""

    @property
    def name(self) -> str:
        return "WinoGrande"

    @property
    def emoji(self) -> str:
        return "🧩"

    def load_dataset(self) -> Any:
        """Load WinoGrande validation split (~1,767 scenarios)"""
        dataset = load_winogrande_dataset()
        return dataset["validation"]

    def get_demo_data(self) -> List[Dict[str, Any]]:
        """Get 3 demo pronoun resolution scenarios"""
        return [
            {
                "sentence": "The trophy doesn't fit in the suitcase because _ is too big.",
                "option1": "the trophy",
                "option2": "the suitcase",
                "answer": "1",
            },
            {
                "sentence": "The man couldn't lift the box because _ was too heavy.",
                "option1": "the man",
                "option2": "the box",
                "answer": "2",
            },
            {
                "sentence": "Sarah gave her sister a gift because _ was generous.",
                "option1": "Sarah",
                "option2": "her sister",
                "answer": "1",
            },
        ]

    def format_prompt(self, item: Any) -> str:
        """Format WinoGrande scenario with options"""
        sentence = item["sentence"]
        option1 = item["option1"]
        option2 = item["option2"]

        prompt = f"{sentence}\n\nA) {option1}\nB) {option2}\n\nAnswer with only the letter:"

        return prompt

    def evaluate_response(
        self, item: Any, response: GenerationResult
    ) -> Tuple[bool, Dict[str, Any]]:
        """Evaluate WinoGrande response with exact matching + letter extraction"""
        sentence = item["sentence"]
        option1 = item["option1"]
        option2 = item["option2"]
        correct_idx = int(item["answer"])

        # Determine correct option
        correct_option = option1 if correct_idx == 1 else option2
        correct_letter = "A" if correct_idx == 1 else "B"

        response_text = response.text.strip()

        # First, try letter extraction (more reliable for MCQ format)
        is_correct = self._extract_mcq_answer(response_text, correct_letter, 2)

        # Fallback: Exact text matching if no letter found
        # (but only if the response doesn't contain an invalid letter)
        if not is_correct:
            # Check if response starts with an invalid letter (C, D, etc.)
            response_upper = response_text.upper().strip()
            has_invalid_letter = False
            for invalid_letter in ["C", "D", "E", "F", "G", "H"]:
                if re.match(rf"^{invalid_letter}[\.\)\:\,\-\s]", response_upper):
                    has_invalid_letter = True
                    break

            # Only use text matching if no invalid letter prefix
            if not has_invalid_letter:
                options = [option1, option2]
                is_correct, is_echoing = self._check_exact_match(
                    response_text, correct_option, options
                )

        scenario = {
            "sentence": sentence,
            "option1": option1,
            "option2": option2,
            "correct_option": correct_option,
            "correct_letter": correct_letter,
            "model_response": response_text,
            "is_correct": is_correct,
        }

        return is_correct, scenario
