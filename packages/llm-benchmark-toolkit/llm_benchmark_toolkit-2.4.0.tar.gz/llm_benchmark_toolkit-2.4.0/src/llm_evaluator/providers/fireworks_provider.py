"""
Fireworks AI Provider for fast and affordable inference

Fireworks provides optimized inference for open models.
Uses OpenAI-compatible API.

Requires: pip install openai
Set FIREWORKS_API_KEY environment variable.

Supported models (selection):
- accounts/fireworks/models/llama-v3p3-70b-instruct
- accounts/fireworks/models/llama-v3p1-8b-instruct
- accounts/fireworks/models/mixtral-8x7b-instruct
- accounts/fireworks/models/qwen2p5-72b-instruct
"""

import logging
import os
import time
from typing import Dict, List, Optional, Union

try:
    from openai import APIError, APITimeoutError, OpenAI
    from openai import RateLimitError as OpenAIRateLimitError
    from openai.types.chat import ChatCompletionMessageParam
except ImportError:
    raise ImportError(
        "Fireworks provider requires 'openai' package. Install with: pip install openai"
    )

from .base import (
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


class FireworksProvider(LLMProvider):
    """
    Fireworks AI provider for optimized open model inference

    Fast inference with competitive pricing on popular open models.

    Requires FIREWORKS_API_KEY environment variable or api_key parameter.

    Example:
        >>> import os
        >>> os.environ["FIREWORKS_API_KEY"] = "..."
        >>> provider = FireworksProvider(model="accounts/fireworks/models/llama-v3p1-8b-instruct")
        >>> result = provider.generate("Hello!")
        >>> print(result.text)
    """

    FIREWORKS_BASE_URL = "https://api.fireworks.ai/inference/v1"

    SUPPORTED_MODELS = [
        # Llama 3
        "accounts/fireworks/models/llama-v3p3-70b-instruct",
        "accounts/fireworks/models/llama-v3p2-3b-instruct",
        "accounts/fireworks/models/llama-v3p1-8b-instruct",
        "accounts/fireworks/models/llama-v3p1-70b-instruct",
        "accounts/fireworks/models/llama-v3p1-405b-instruct",
        # Mixtral
        "accounts/fireworks/models/mixtral-8x7b-instruct",
        "accounts/fireworks/models/mixtral-8x22b-instruct",
        # Qwen
        "accounts/fireworks/models/qwen2p5-72b-instruct",
        "accounts/fireworks/models/qwen2p5-coder-32b-instruct",
        # DeepSeek
        "accounts/fireworks/models/deepseek-v3",
        "accounts/fireworks/models/deepseek-r1",
        # Others
        "accounts/fireworks/models/gemma2-9b-it",
        "accounts/fireworks/models/phi-3-vision-128k-instruct",
    ]

    # Pricing per 1M tokens
    PRICING = {
        "accounts/fireworks/models/llama-v3p3-70b-instruct": {"input": 0.90, "output": 0.90},
        "accounts/fireworks/models/llama-v3p2-3b-instruct": {"input": 0.10, "output": 0.10},
        "accounts/fireworks/models/llama-v3p1-8b-instruct": {"input": 0.20, "output": 0.20},
        "accounts/fireworks/models/llama-v3p1-70b-instruct": {"input": 0.90, "output": 0.90},
        "accounts/fireworks/models/llama-v3p1-405b-instruct": {"input": 3.00, "output": 3.00},
        "accounts/fireworks/models/mixtral-8x7b-instruct": {"input": 0.50, "output": 0.50},
        "accounts/fireworks/models/qwen2p5-72b-instruct": {"input": 0.90, "output": 0.90},
        "accounts/fireworks/models/deepseek-v3": {"input": 0.90, "output": 0.90},
    }

    def __init__(
        self,
        model: str = "accounts/fireworks/models/llama-v3p1-8b-instruct",
        api_key: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ):
        """
        Initialize Fireworks provider

        Args:
            model: Model name (full path like "accounts/fireworks/models/...")
            api_key: Fireworks API key (or set FIREWORKS_API_KEY env var)
            config: Generation configuration
        """
        super().__init__(model, config)

        self.api_key = api_key or os.environ.get("FIREWORKS_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Fireworks API key required. Set FIREWORKS_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.FIREWORKS_BASE_URL,
        )

        logger.info(f"Initialized Fireworks provider with model: {model}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> GenerationResult:
        """Generate text using Fireworks API"""
        cfg = config or self.config

        messages: List[ChatCompletionMessageParam] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        last_error: Optional[Exception] = None
        for attempt in range(cfg.retry_attempts):
            try:
                start_time = time.time()

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=cfg.temperature,
                    max_tokens=cfg.max_tokens,
                    top_p=cfg.top_p,
                    timeout=cfg.timeout_seconds,
                )

                elapsed = time.time() - start_time

                choice = response.choices[0]
                text = choice.message.content or ""

                usage = response.usage
                prompt_tokens = usage.prompt_tokens if usage else 0
                completion_tokens = usage.completion_tokens if usage else 0
                total_tokens = usage.total_tokens if usage else 0

                pricing = self.PRICING.get(self.model, {"input": 0.0, "output": 0.0})
                cost = (prompt_tokens / 1_000_000) * pricing["input"] + (
                    completion_tokens / 1_000_000
                ) * pricing["output"]

                logger.debug(
                    f"Fireworks generation successful: {total_tokens} tokens in {elapsed:.2f}s"
                )

                return GenerationResult(
                    text=text,
                    response_time=elapsed,
                    tokens_used=total_tokens,
                    model=self.model,
                    provider="fireworks",
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    cost_usd=cost,
                    finish_reason=choice.finish_reason or "unknown",
                )

            except OpenAIRateLimitError as e:
                last_error = e
                if attempt < cfg.retry_attempts - 1:
                    wait_time = 2**attempt
                    logger.warning(f"Rate limited, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise RateLimitError(
                        message=f"Rate limit exceeded after {cfg.retry_attempts} attempts",
                        original_error=e,
                        retry_after=60,
                    )

            except APITimeoutError as e:
                last_error = e
                if attempt < cfg.retry_attempts - 1:
                    wait_time = 2**attempt
                    logger.warning(f"Timeout, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise TimeoutError(
                        message=f"Request timed out after {cfg.retry_attempts} attempts",
                        original_error=e,
                    )

            except APIError as e:
                if "model" in str(e).lower() and "not found" in str(e).lower():
                    raise ModelNotFoundError(
                        message=f"Model '{self.model}' not found on Fireworks",
                        original_error=e,
                    )
                else:
                    raise ProviderError(
                        message=f"Fireworks API error: {str(e)}",
                        original_error=e,
                    )

            except Exception as e:
                raise ProviderError(
                    message=f"Unexpected error: {str(e)}",
                    original_error=e,
                )

        raise ProviderError(
            message=f"Failed after {cfg.retry_attempts} attempts",
            original_error=last_error,
        )

    def generate_batch(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> List[GenerationResult]:
        """Generate responses for multiple prompts"""
        results = []

        for i, prompt in enumerate(prompts):
            try:
                result = self.generate(prompt, system_prompt, config)
                results.append(result)

                if i < len(prompts) - 1:
                    time.sleep(0.15)

            except ProviderError as e:
                logger.error(f"Failed to generate for prompt {i}: {e.message}")
                results.append(
                    GenerationResult(
                        text="",
                        response_time=0.0,
                        tokens_used=0,
                        model=self.model,
                        provider="fireworks",
                        error=str(e),
                    )
                )

        return results

    def is_available(self) -> bool:
        """Check if Fireworks API is accessible"""
        try:
            self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"Fireworks API not available: {e}")
            return False

    def get_model_info(self) -> Dict[str, Union[str, int, float, List[str]]]:
        """Get information about the current model"""
        return {
            "model_id": self.model,
            "provider": "fireworks",
            "supported_models": self.SUPPORTED_MODELS,
            "base_url": self.FIREWORKS_BASE_URL,
        }

    def _get_provider_type(self) -> ProviderType:
        """Return provider type"""
        return ProviderType.FIREWORKS
