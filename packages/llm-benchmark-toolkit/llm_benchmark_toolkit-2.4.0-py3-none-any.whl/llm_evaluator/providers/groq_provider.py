"""
Groq Provider for ultra-fast LLM inference

Groq provides extremely fast inference using custom LPU hardware.
Uses OpenAI-compatible API.

Requires: pip install openai
Set GROQ_API_KEY environment variable.

Supported models:
- llama-3.3-70b-versatile
- llama-3.1-8b-instant
- llama-3.2-3b-preview
- llama-3.2-1b-preview
- mixtral-8x7b-32768
- gemma2-9b-it
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
    raise ImportError("Groq provider requires 'openai' package. Install with: pip install openai")

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


class GroqProvider(LLMProvider):
    """
    Groq provider for ultra-fast LLM inference

    Uses OpenAI-compatible API with Groq's custom LPU hardware.
    Extremely fast inference (100+ tokens/second).

    Requires GROQ_API_KEY environment variable or api_key parameter.

    Example:
        >>> import os
        >>> os.environ["GROQ_API_KEY"] = "gsk_..."
        >>> provider = GroqProvider(model="llama-3.1-8b-instant")
        >>> result = provider.generate("Hello!")
        >>> print(result.text)
    """

    GROQ_BASE_URL = "https://api.groq.com/openai/v1"

    SUPPORTED_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-3.2-3b-preview",
        "llama-3.2-1b-preview",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ]

    # Pricing per 1M tokens (Groq is very affordable)
    PRICING = {
        "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
        "llama-3.1-70b-versatile": {"input": 0.59, "output": 0.79},
        "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
        "llama-3.2-3b-preview": {"input": 0.06, "output": 0.06},
        "llama-3.2-1b-preview": {"input": 0.04, "output": 0.04},
        "llama3-70b-8192": {"input": 0.59, "output": 0.79},
        "llama3-8b-8192": {"input": 0.05, "output": 0.08},
        "mixtral-8x7b-32768": {"input": 0.24, "output": 0.24},
        "gemma2-9b-it": {"input": 0.20, "output": 0.20},
    }

    def __init__(
        self,
        model: str = "llama-3.1-8b-instant",
        api_key: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ):
        """
        Initialize Groq provider

        Args:
            model: Model name (e.g., "llama-3.1-8b-instant")
            api_key: Groq API key (or set GROQ_API_KEY env var)
            config: Generation configuration
        """
        super().__init__(model, config)

        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Groq API key required. Set GROQ_API_KEY environment variable "
                "or pass api_key parameter."
            )

        # Initialize OpenAI client with Groq base URL
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.GROQ_BASE_URL,
        )

        logger.info(f"Initialized Groq provider with model: {model}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> GenerationResult:
        """
        Generate text using Groq API

        Args:
            prompt: User prompt
            system_prompt: Optional system message
            config: Override generation config

        Returns:
            GenerationResult with response
        """
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

                logger.debug(f"Groq generation successful: {total_tokens} tokens in {elapsed:.2f}s")

                return GenerationResult(
                    text=text,
                    response_time=elapsed,
                    tokens_used=total_tokens,
                    model=self.model,
                    provider="groq",
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
                        message=f"Model '{self.model}' not found on Groq",
                        original_error=e,
                    )
                else:
                    raise ProviderError(
                        message=f"Groq API error: {str(e)}",
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

                # Groq is fast but has rate limits
                if i < len(prompts) - 1:
                    time.sleep(0.1)

            except ProviderError as e:
                logger.error(f"Failed to generate for prompt {i}: {e.message}")
                results.append(
                    GenerationResult(
                        text="",
                        response_time=0.0,
                        tokens_used=0,
                        model=self.model,
                        provider="groq",
                        error=str(e),
                    )
                )

        return results

    def is_available(self) -> bool:
        """Check if Groq API is accessible"""
        try:
            self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"Groq API not available: {e}")
            return False

    def get_model_info(self) -> Dict[str, Union[str, int, float, List[str]]]:
        """Get information about the current model"""
        return {
            "model_id": self.model,
            "provider": "groq",
            "supported_models": self.SUPPORTED_MODELS,
            "base_url": self.GROQ_BASE_URL,
        }

    def _get_provider_type(self) -> ProviderType:
        """Return provider type"""
        return ProviderType.GROQ
