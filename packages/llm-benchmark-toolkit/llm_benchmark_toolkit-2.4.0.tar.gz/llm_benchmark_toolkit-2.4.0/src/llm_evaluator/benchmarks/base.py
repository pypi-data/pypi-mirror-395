"""
Base classes for benchmarks with common functionality.
"""

import logging
import random
import re
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from tqdm import tqdm

from ..providers import GenerationResult, LLMProvider, ProviderError

logger = logging.getLogger(__name__)


class Benchmark(ABC):
    """
    Abstract base class for all benchmarks.

    Provides common functionality:
    - Dataset loading and sampling
    - Progress bars with ETA
    - Result formatting
    - Mode handling (demo/full/sample)
    """

    def __init__(
        self,
        provider: LLMProvider,
        mode: str = "demo",
        sample_size: Optional[int] = None,
    ):
        """
        Initialize benchmark.

        Args:
            provider: LLM provider for generation
            mode: "demo" (few examples), "full" (complete dataset), or custom
            sample_size: If specified, randomly sample this many questions
        """
        self.provider = provider
        self.mode = mode
        self.sample_size = sample_size

    @property
    @abstractmethod
    def name(self) -> str:
        """Benchmark name (e.g., 'MMLU', 'TruthfulQA')"""
        pass

    @property
    @abstractmethod
    def emoji(self) -> str:
        """Emoji for progress bar (e.g., '📚', '🧠')"""
        pass

    @abstractmethod
    def load_dataset(self) -> Any:
        """Load the dataset. Return format depends on benchmark."""
        pass

    @abstractmethod
    def get_demo_data(self) -> List[Dict[str, Any]]:
        """Get demo mode data (2-5 examples)"""
        pass

    @abstractmethod
    def format_prompt(self, item: Any) -> str:
        """Format a single item into a prompt string"""
        pass

    @abstractmethod
    def evaluate_response(
        self, item: Any, response: GenerationResult
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Evaluate model response for a single item.

        Args:
            item: Dataset item
            response: Model's generation result

        Returns:
            (is_correct, scenario_data) tuple
        """
        pass

    def _generate(self, prompt: str) -> GenerationResult:
        """Generate response from provider"""
        return self.provider.generate(prompt)

    def _sample_dataset(self, dataset: Any, total_size: int) -> Tuple[List[Any], str]:
        """
        Sample dataset if requested.

        Returns:
            (sampled_data, log_message) tuple
        """
        if self.sample_size:
            sample_size = min(self.sample_size, total_size)
            indices = random.sample(range(total_size), sample_size)
            sampled = [dataset[i] for i in indices]
            msg = f"Sampling {len(sampled)} from {total_size} total"
            return sampled, msg
        else:
            msg = f"Testing all {total_size} questions"
            return list(dataset), msg

    def run(self) -> Dict[str, Any]:
        """
        Run the benchmark.

        Returns:
            Dictionary with results including accuracy, scenarios, metadata
        """
        try:
            # Select data based on mode
            if self.mode == "demo":
                data_to_test = self.get_demo_data()
                logger.info(f"Running {self.name} DEMO mode ({len(data_to_test)} examples)")
            else:
                dataset = self.load_dataset()
                total_size = len(dataset)
                data_to_test, sample_msg = self._sample_dataset(dataset, total_size)
                logger.info(f"Running {self.name} FULL mode - {sample_msg}")

            # Run evaluation with progress bar
            correct = 0
            scenarios = []
            start_time = time.time()

            pbar = tqdm(
                data_to_test,
                desc=f"{self.emoji} {self.name} Progress",
                unit="q",
                ncols=100,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}",
            )

            for i, item in enumerate(pbar):
                # Generate prompt and get response
                prompt = self.format_prompt(item)
                response = self._generate(prompt)

                # Evaluate
                is_correct, scenario = self.evaluate_response(item, response)
                scenario["id"] = i

                if is_correct:
                    correct += 1

                scenarios.append(scenario)

                # Update progress
                current_acc = (correct / (i + 1)) * 100
                pbar.set_postfix_str(f"{current_acc:.1f}%")

            pbar.close()

            # Calculate final metrics
            accuracy = correct / len(data_to_test) if data_to_test else 0
            elapsed_time = time.time() - start_time

            logger.info(
                f"{self.name}: {correct}/{len(data_to_test)} correct ({accuracy:.1%}) in {elapsed_time:.1f}s"
            )

            # Return standardized results
            result = {
                f"{self.name.lower()}_accuracy": accuracy,
                "questions_tested": len(data_to_test),
                "correct": correct,
                "elapsed_time": elapsed_time,
                "mode": (
                    self.mode
                    if self.mode == "demo"
                    else f"sample_{self.sample_size}" if self.sample_size else "full"
                ),
                "scenarios": scenarios,
            }

            # Add total_available for full mode
            if self.mode != "demo":
                dataset = self.load_dataset()
                result["total_available"] = len(dataset)

            return result

        except ProviderError as e:
            logger.error(f"{self.name} benchmark failed: {e}")
            raise
        except Exception as e:
            logger.error(f"{self.name} benchmark failed: {e}")
            raise


class MultipleChoiceBenchmark(Benchmark):
    """
    Base class for multiple choice benchmarks.

    Adds common MCQ functionality:
    - Letter extraction
    - Exact text matching
    - Anti-echo detection
    """

    def _extract_letter_from_response(
        self, response: str, valid_letters: List[str]
    ) -> Optional[str]:
        """
        Extract which letter the model chose from its response.

        Returns the extracted letter (A, B, C, etc.) or None if no valid letter found.

        Args:
            response: Model's response text
            valid_letters: List of valid letter choices (e.g., ['A', 'B', 'C', 'D'])

        Returns:
            The extracted letter or None
        """
        response = response.strip().upper()

        # Strategy 1: Exact match (just the letter)
        if response in valid_letters:
            return response

        # Strategy 2: Letter with punctuation at start (A., A), A:, etc.)
        for letter in valid_letters:
            if re.match(rf"^{letter}[\.\)\:\,\-\s]", response):
                return letter

        # Strategy 3: "The answer is X" or "Choose X" patterns
        for letter in valid_letters:
            if re.search(
                rf"\b(answer|choice|select|choose)\s+(is\s+)?{letter}\b", response, re.IGNORECASE
            ):
                return letter

        # Strategy 4: Letter at start of response (must be isolated)
        if response and response[0] in valid_letters:
            # Check it's not part of a longer word
            if len(response) == 1 or not response[1].isalpha():
                return response[0]

        # Strategy 5: Letter in parentheses or brackets
        for letter in valid_letters:
            if re.search(rf"[\(\[]{letter}[\)\]]", response):
                return letter

        # No valid letter found
        return None

    def _extract_mcq_answer(self, response: str, correct_letter: str, num_choices: int = 4) -> bool:
        """
        Extract answer from response and check if correct.

        This method first extracts which letter the model chose, then compares it
        to the correct letter. This prevents false positives where the model's
        response happens to contain the correct letter but chose a different one.

        Args:
            response: Model's response text
            correct_letter: The correct answer letter (A, B, C, D, etc.)
            num_choices: Number of choices (default 4 for A-D)

        Returns:
            True if the extracted answer matches the correct letter
        """
        # Get valid letters based on number of choices
        valid_letters = [chr(65 + i) for i in range(num_choices)]

        # Extract which letter the model chose
        model_letter = self._extract_letter_from_response(response, valid_letters)

        # Compare with correct answer
        if model_letter is None:
            return False  # Model didn't provide a valid letter

        return model_letter.upper() == correct_letter.upper()

    def _check_exact_match(
        self, response: str, correct_text: str, all_choices: List[str]
    ) -> Tuple[bool, bool]:
        """
        Check if correct text appears in response via exact matching.
        Also detects if model is echoing all options.

        Args:
            response: Model's response
            correct_text: The correct answer text
            all_choices: All available choices

        Returns:
            (is_correct_found, is_echoing) tuple
        """
        response_lower = response.lower()
        correct_lower = correct_text.lower()

        # Check for echo: does response contain most/all options?
        num_options_in_response = sum(
            1 for choice in all_choices if choice.lower() in response_lower and len(choice) > 10
        )
        is_echoing = num_options_in_response >= len(all_choices) - 1

        # Check if correct answer appears (but only if not echoing)
        is_correct = False
        if not is_echoing:
            # Use word boundary regex for exact matching
            is_correct = bool(re.search(r"\b" + re.escape(correct_lower), response_lower))

        return is_correct, is_echoing
