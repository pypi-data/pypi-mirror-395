"""
HellaSwag benchmark - commonsense natural language inference.

Tests model ability to complete scenarios with the most plausible continuation.
Dataset: 10,042 validation scenarios with 4 ending options each.
Special handling: WikiHow markers cleanup.
"""

import logging
import re
from typing import Any, Dict, List, Tuple

from ..dataset_loaders import load_hellaswag_dataset
from ..providers import GenerationResult
from .base import MultipleChoiceBenchmark

logger = logging.getLogger(__name__)


def clean_hellaswag_text(text: str) -> str:
    """Remove WikiHow-specific markers from text"""
    # Remove [header], [title], [step] markers
    text = re.sub(r"\[header\]|\[title\]|\[step\]", "", text, flags=re.IGNORECASE)
    # Clean up extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


class HellaSwagBenchmark(MultipleChoiceBenchmark):
    """HellaSwag commonsense inference benchmark"""

    @property
    def name(self) -> str:
        return "HellaSwag"

    @property
    def emoji(self) -> str:
        return "🤔"

    def load_dataset(self) -> Any:
        """Load HellaSwag validation split (10,042 scenarios)"""
        dataset = load_hellaswag_dataset()
        return dataset["validation"]

    def get_demo_data(self) -> List[Dict[str, Any]]:
        """Get 2 demo scenarios"""
        return [
            {
                "ctx": "A man is sitting on a roof. He",
                "endings": [
                    "is using wrap to wrap a pair of skis.",
                    "starts pulling up roofing on a roof.",
                    "is ripping level tiles off.",
                    "is holding a rubik's cube.",
                ],
                "label": "1",
            },
            {
                "ctx": "A woman is in a kitchen. She",
                "endings": [
                    "puts a cake in the oven.",
                    "starts dancing on the counter.",
                    "throws dishes at the wall.",
                    "climbs into the refrigerator.",
                ],
                "label": "0",
            },
        ]

    def format_prompt(self, item: Any) -> str:
        """Format HellaSwag scenario with continuations"""
        context = clean_hellaswag_text(item["ctx"])
        endings = item["endings"]

        # Clean endings
        cleaned_endings = [clean_hellaswag_text(e) for e in endings]

        # Format choices with letters
        choices_str = "\n".join(
            [f"{chr(65+j)}) {ending}" for j, ending in enumerate(cleaned_endings)]
        )

        prompt = f"{context}\n\n{choices_str}\n\nAnswer with only the letter:"

        return prompt

    def evaluate_response(
        self, item: Any, response: GenerationResult
    ) -> Tuple[bool, Dict[str, Any]]:
        """Evaluate HellaSwag response with exact matching + letter extraction"""
        context = clean_hellaswag_text(item["ctx"])
        endings = item["endings"]
        cleaned_endings = [clean_hellaswag_text(e) for e in endings]

        correct_idx = int(item["label"])
        correct_ending = cleaned_endings[correct_idx]
        correct_letter = chr(65 + correct_idx)

        response_text = response.text.strip()

        # Strategy 1: Letter extraction first (most reliable for MCQ)
        is_correct = self._extract_mcq_answer(response_text, correct_letter, len(endings))

        # Strategy 2: Text matching fallback (but only if no echoing)
        if not is_correct:
            # Check for echoing - if model repeats all options, it's invalid
            response_lower = response_text.lower()
            num_options_in_response = sum(
                1
                for ending in cleaned_endings
                if ending.lower() in response_lower and len(ending) > 10
            )
            is_echoing = num_options_in_response >= len(cleaned_endings) - 1

            # Only use text matching if not echoing
            if not is_echoing:
                correct_lower = correct_ending.lower()
                # Check correct answer appears
                if correct_lower in response_lower:
                    # But also check that NO incorrect endings appear
                    incorrect_in_response = any(
                        ending.lower() in response_lower
                        for i, ending in enumerate(cleaned_endings)
                        if i != correct_idx and len(ending) > 10
                    )
                    if not incorrect_in_response:
                        is_correct = True

        scenario = {
            "context": context,
            "endings": cleaned_endings,
            "correct_ending": correct_ending,
            "correct_letter": correct_letter,
            "model_response": response_text,
            "is_correct": is_correct,
        }

        return is_correct, scenario
