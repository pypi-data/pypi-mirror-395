"""
Together.ai Provider for inference on many open models

Together.ai provides access to 100+ open models with fast inference.
Uses OpenAI-compatible API.

Requires: pip install openai
Set TOGETHER_API_KEY environment variable.

Supported models (selection):
- meta-llama/Llama-3.3-70B-Instruct-Turbo
- meta-llama/Llama-3.2-3B-Instruct-Turbo
- mistralai/Mixtral-8x7B-Instruct-v0.1
- Qwen/Qwen2.5-72B-Instruct-Turbo
- deepseek-ai/DeepSeek-V3
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
        "Together provider requires 'openai' package. Install with: pip install openai"
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


class TogetherProvider(LLMProvider):
    """
    Together.ai provider for open model inference

    Access to 100+ open models including Llama, Mistral, Qwen, DeepSeek, etc.

    Requires TOGETHER_API_KEY environment variable or api_key parameter.

    Example:
        >>> import os
        >>> os.environ["TOGETHER_API_KEY"] = "..."
        >>> provider = TogetherProvider(model="meta-llama/Llama-3.2-3B-Instruct-Turbo")
        >>> result = provider.generate("Hello!")
        >>> print(result.text)
    """

    TOGETHER_BASE_URL = "https://api.together.xyz/v1"

    SUPPORTED_MODELS = [
        # Llama 3
        "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "meta-llama/Llama-3.2-3B-Instruct-Turbo",
        "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
        "meta-llama/Llama-3.1-8B-Instruct-Turbo",
        "meta-llama/Llama-3.1-70B-Instruct-Turbo",
        "meta-llama/Llama-3.1-405B-Instruct-Turbo",
        # Mistral
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "mistralai/Mistral-7B-Instruct-v0.3",
        # Qwen
        "Qwen/Qwen2.5-72B-Instruct-Turbo",
        "Qwen/Qwen2.5-7B-Instruct-Turbo",
        # DeepSeek
        "deepseek-ai/DeepSeek-V3",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        # Others
        "google/gemma-2-27b-it",
        "databricks/dbrx-instruct",
    ]

    # Pricing per 1M tokens (Together has competitive pricing)
    PRICING = {
        "meta-llama/Llama-3.3-70B-Instruct-Turbo": {"input": 0.88, "output": 0.88},
        "meta-llama/Llama-3.2-3B-Instruct-Turbo": {"input": 0.06, "output": 0.06},
        "meta-llama/Llama-3.1-8B-Instruct-Turbo": {"input": 0.18, "output": 0.18},
        "meta-llama/Llama-3.1-70B-Instruct-Turbo": {"input": 0.88, "output": 0.88},
        "meta-llama/Llama-3.1-405B-Instruct-Turbo": {"input": 3.50, "output": 3.50},
        "mistralai/Mixtral-8x7B-Instruct-v0.1": {"input": 0.60, "output": 0.60},
        "Qwen/Qwen2.5-72B-Instruct-Turbo": {"input": 1.20, "output": 1.20},
        "deepseek-ai/DeepSeek-V3": {"input": 0.90, "output": 0.90},
    }

    def __init__(
        self,
        model: str = "meta-llama/Llama-3.2-3B-Instruct-Turbo",
        api_key: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ):
        """
        Initialize Together provider

        Args:
            model: Model name (full path like "meta-llama/Llama-3.2-3B-Instruct-Turbo")
            api_key: Together API key (or set TOGETHER_API_KEY env var)
            config: Generation configuration
        """
        super().__init__(model, config)

        self.api_key = api_key or os.environ.get("TOGETHER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Together API key required. Set TOGETHER_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.TOGETHER_BASE_URL,
        )

        logger.info(f"Initialized Together provider with model: {model}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> GenerationResult:
        """Generate text using Together API"""
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
                    f"Together generation successful: {total_tokens} tokens in {elapsed:.2f}s"
                )

                return GenerationResult(
                    text=text,
                    response_time=elapsed,
                    tokens_used=total_tokens,
                    model=self.model,
                    provider="together",
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
                        message=f"Model '{self.model}' not found on Together",
                        original_error=e,
                    )
                else:
                    raise ProviderError(
                        message=f"Together API error: {str(e)}",
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
                    time.sleep(0.2)

            except ProviderError as e:
                logger.error(f"Failed to generate for prompt {i}: {e.message}")
                results.append(
                    GenerationResult(
                        text="",
                        response_time=0.0,
                        tokens_used=0,
                        model=self.model,
                        provider="together",
                        error=str(e),
                    )
                )

        return results

    def is_available(self) -> bool:
        """Check if Together API is accessible"""
        try:
            self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"Together API not available: {e}")
            return False

    def get_model_info(self) -> Dict[str, Union[str, int, float, List[str]]]:
        """Get information about the current model"""
        return {
            "model_id": self.model,
            "provider": "together",
            "supported_models": self.SUPPORTED_MODELS,
            "base_url": self.TOGETHER_BASE_URL,
        }

    def _get_provider_type(self) -> ProviderType:
        """Return provider type"""
        return ProviderType.TOGETHER
