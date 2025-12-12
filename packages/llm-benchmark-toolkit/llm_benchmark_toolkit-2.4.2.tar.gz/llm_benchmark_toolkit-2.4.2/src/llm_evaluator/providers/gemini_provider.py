"""
Google Gemini Provider

Implements the LLMProvider interface for Google's Gemini API.
Requires: pip install google-genai
"""

import logging
import time
from typing import Dict, List, Optional

try:
    from google import genai
    from google.genai import types
except ImportError:
    raise ImportError(
        "Gemini provider requires 'google-genai' package. " "Install with: pip install google-genai"
    )

from . import (
    GenerationConfig,
    GenerationResult,
    LLMProvider,
    ModelNotFoundError,
    ProviderError,
    ProviderType,
    RateLimitError,
    TimeoutError,
)

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """
    Google Gemini provider

    Supports:
    - Gemini 2.5 Flash (recommended)
    - Gemini 2.5 Pro
    - Gemini 2.0 Flash

    Requires GEMINI_API_KEY environment variable or api_key parameter.

    Example:
        >>> import os
        >>> os.environ["GEMINI_API_KEY"] = "..."
        >>> provider = GeminiProvider(model="gemini-2.5-flash")
        >>> result = provider.generate("Hello, world!")
        >>> print(result.text)
    """

    SUPPORTED_MODELS = {
        "gemini-2.5-flash": {
            "name": "Gemini 2.5 Flash",
            "context_window": 1_000_000,
            "input_cost_per_1m": 0.075,
            "output_cost_per_1m": 0.30,
            "description": "Fast and intelligent, best for price-performance",
        },
        "gemini-2.5-pro": {
            "name": "Gemini 2.5 Pro",
            "context_window": 2_000_000,
            "input_cost_per_1m": 3.50,
            "output_cost_per_1m": 10.50,
            "description": "Advanced thinking model for complex reasoning",
        },
        "gemini-2.0-flash": {
            "name": "Gemini 2.0 Flash",
            "context_window": 1_000_000,
            "input_cost_per_1m": 0.10,
            "output_cost_per_1m": 0.40,
            "description": "Second generation workhorse model",
        },
    }

    def __init__(
        self,
        model: str = "gemini-2.5-flash",
        api_key: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
        **kwargs,
    ):
        """
        Initialize Gemini provider

        Args:
            model: Model name (default: "gemini-2.5-flash")
            api_key: Google API key (or set GEMINI_API_KEY environment variable)
            config: Generation configuration
        """
        super().__init__(model=model, config=config)

        if model not in self.SUPPORTED_MODELS:
            raise ModelNotFoundError(
                f"Model '{model}' not found. Available: {list(self.SUPPORTED_MODELS.keys())}"
            )

        # Initialize client (auto-picks GEMINI_API_KEY from environment)
        self.client = genai.Client(api_key=api_key) if api_key else genai.Client()
        self._model_name = model

        logger.info(f"Initialized Gemini provider with model: {model}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> GenerationResult:
        """Generate text from a prompt with automatic retry on rate limits"""
        gen_config = config or self.config

        last_error: Optional[Exception] = None
        for attempt in range(gen_config.retry_attempts):
            start_time = time.time()

            try:
                # Build generation config
                cfg = types.GenerateContentConfig(
                    max_output_tokens=gen_config.max_tokens,
                    temperature=gen_config.temperature,
                    top_p=gen_config.top_p,
                )

                if system_prompt:
                    cfg.system_instruction = system_prompt

                # Generate response
                response = self.client.models.generate_content(
                    model=self._model_name,
                    contents=prompt,
                    config=cfg,
                )

                text = response.text if response.text else ""
                latency = time.time() - start_time

                # Get token usage
                usage = response.usage_metadata if hasattr(response, "usage_metadata") else None
                prompt_tokens = getattr(usage, "prompt_token_count", 0) if usage else 0
                completion_tokens = getattr(usage, "candidates_token_count", 0) if usage else 0

                # Ensure we have valid integers
                prompt_tokens = prompt_tokens if prompt_tokens is not None else 0
                completion_tokens = completion_tokens if completion_tokens is not None else 0

                return GenerationResult(
                    text=text,
                    response_time=latency,
                    model=self._model_name,
                    provider=ProviderType.GEMINI.value,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                )

            except Exception as e:
                error_msg = str(e)
                last_error = e

                if (
                    "429" in error_msg
                    or "quota" in error_msg.lower()
                    or "RESOURCE_EXHAUSTED" in error_msg
                ):
                    if attempt < gen_config.retry_attempts - 1:
                        # Extract retry delay from error message if available
                        wait_time = 2**attempt  # Exponential backoff: 1s, 2s, 4s
                        if "retry" in error_msg.lower() and "s" in error_msg:
                            # Try to extract the retry delay from error message
                            try:
                                import re

                                match = re.search(
                                    r"retry.*?(\d+\.?\d*)\s*s", error_msg, re.IGNORECASE
                                )
                                if match:
                                    suggested_wait = float(match.group(1))
                                    wait_time = max(wait_time, suggested_wait + 0.5)  # Add buffer
                            except Exception:
                                pass

                        logger.warning(
                            f"Gemini rate limited (attempt {attempt + 1}/{gen_config.retry_attempts}), retrying in {wait_time:.1f}s..."
                        )
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RateLimitError(
                            f"Gemini rate limit exceeded after {gen_config.retry_attempts} attempts: {e}"
                        )
                elif "timeout" in error_msg.lower():
                    if attempt < gen_config.retry_attempts - 1:
                        wait_time = 2**attempt
                        logger.warning(
                            f"Gemini timeout (attempt {attempt + 1}/{gen_config.retry_attempts}), retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
                        continue
                    else:
                        raise TimeoutError(
                            f"Gemini timeout after {gen_config.retry_attempts} attempts: {e}"
                        )
                else:
                    raise ProviderError(f"Gemini error: {e}")

        # Should never reach here, but just in case
        raise ProviderError(f"Failed after {gen_config.retry_attempts} attempts: {last_error}")

    def generate_batch(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> List[GenerationResult]:
        """Generate text for multiple prompts"""
        results = []
        for prompt in prompts:
            try:
                result = self.generate(prompt, system_prompt, config)
                results.append(result)
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                logger.error(f"Error generating: {e}")
                results.append(
                    GenerationResult(
                        text="",
                        response_time=0,
                        model=self._model_name,
                        provider=ProviderType.GEMINI.value,
                        error=str(e),
                    )
                )
        return results

    def list_models(self) -> List[str]:
        """List available models"""
        return list(self.SUPPORTED_MODELS.keys())

    def get_model_info(self, model: Optional[str] = None) -> Dict:
        """Get model information"""
        model_name = model or self._model_name
        if model_name not in self.SUPPORTED_MODELS:
            raise ModelNotFoundError(f"Model '{model_name}' not found")
        return self.SUPPORTED_MODELS[model_name]

    @classmethod
    def is_available(cls) -> bool:
        """Check if Gemini provider is available"""
        try:
            import google.genai  # noqa: F401

            return True
        except ImportError:
            return False

    @classmethod
    def _get_provider_type(cls) -> ProviderType:
        """Get provider type"""
        return ProviderType.GEMINI
