"""
DeepSeek Provider for DeepSeek models

Implements the LLMProvider interface for DeepSeek's API.
Uses OpenAI-compatible API format.
Requires: pip install openai
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
        "DeepSeek provider requires 'openai' package. Install with: pip install openai"
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


class DeepSeekProvider(LLMProvider):
    """
    DeepSeek provider for DeepSeek models

    Supports:
    - deepseek-chat (DeepSeek-V3, default)
    - deepseek-reasoner (DeepSeek-R1)
    - deepseek-coder

    Requires DEEPSEEK_API_KEY environment variable or api_key parameter.

    Example:
        >>> import os
        >>> os.environ["DEEPSEEK_API_KEY"] = "sk-..."
        >>> provider = DeepSeekProvider(model="deepseek-chat")
        >>> result = provider.generate("Hello, world!")
        >>> print(result.text)
    """

    SUPPORTED_MODELS = [
        "deepseek-chat",
        "deepseek-reasoner",
        "deepseek-coder",
    ]

    # Pricing per 1M tokens (approximate, check DeepSeek docs)
    PRICING = {
        "deepseek-chat": {"input": 0.14, "output": 0.28},
        "deepseek-reasoner": {"input": 0.55, "output": 2.19},
        "deepseek-coder": {"input": 0.14, "output": 0.28},
    }

    BASE_URL = "https://api.deepseek.com"

    def __init__(
        self,
        model: str = "deepseek-chat",
        api_key: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
        base_url: Optional[str] = None,
    ):
        """
        Initialize DeepSeek provider

        Args:
            model: Model name (e.g., "deepseek-chat", "deepseek-reasoner")
            api_key: DeepSeek API key (or set DEEPSEEK_API_KEY env var)
            config: Generation configuration
            base_url: Custom API base URL (default: https://api.deepseek.com)
        """
        super().__init__(model, config)

        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        self.base_url = base_url or self.BASE_URL

        if not self.api_key:
            raise ProviderError(
                "DeepSeek API key not found. Set DEEPSEEK_API_KEY environment variable "
                "or pass api_key parameter."
            )

        # Initialize OpenAI client with DeepSeek endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        logger.info(f"Initialized DeepSeek provider with model: {model}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> GenerationResult:
        """
        Generate text using DeepSeek API

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            config: Optional generation config (overrides default)

        Returns:
            GenerationResult with response text and metadata
        """
        cfg = config or self.config
        start_time = time.time()

        messages: List[ChatCompletionMessageParam] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        for attempt in range(cfg.retry_attempts):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=cfg.temperature,
                    max_tokens=cfg.max_tokens,
                    top_p=cfg.top_p,
                    timeout=cfg.timeout_seconds,
                )

                response_time = time.time() - start_time
                choice = response.choices[0]
                text = choice.message.content or ""

                # Calculate cost
                prompt_tokens = response.usage.prompt_tokens if response.usage else 0
                completion_tokens = response.usage.completion_tokens if response.usage else 0

                pricing = self.PRICING.get(self.model, {"input": 0.14, "output": 0.28})
                cost = (prompt_tokens / 1_000_000) * pricing["input"] + (
                    completion_tokens / 1_000_000
                ) * pricing["output"]

                return GenerationResult(
                    text=text,
                    response_time=response_time,
                    tokens_used=prompt_tokens + completion_tokens,
                    model=self.model,
                    provider="deepseek",
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                    cost_usd=cost,
                    finish_reason=choice.finish_reason or "",
                )

            except OpenAIRateLimitError as e:
                if attempt < cfg.retry_attempts - 1:
                    wait_time = 2**attempt
                    logger.warning(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise RateLimitError(
                        f"DeepSeek rate limit exceeded: {e}",
                        original_error=e,
                    )

            except APITimeoutError as e:
                if attempt < cfg.retry_attempts - 1:
                    logger.warning(f"Timeout, retrying (attempt {attempt + 2})...")
                else:
                    raise TimeoutError(
                        f"DeepSeek request timed out: {e}",
                        original_error=e,
                    )

            except APIError as e:
                if "model_not_found" in str(e).lower():
                    raise ModelNotFoundError(
                        f"DeepSeek model '{self.model}' not found. "
                        f"Available: {', '.join(self.SUPPORTED_MODELS)}",
                        original_error=e,
                    )
                raise ProviderError(
                    f"DeepSeek API error: {e}",
                    original_error=e,
                )

        # Should not reach here
        raise ProviderError("Max retries exceeded")

    def generate_batch(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> List[GenerationResult]:
        """Generate responses for multiple prompts"""
        return [self.generate(prompt, system_prompt, config) for prompt in prompts]

    def is_available(self) -> bool:
        """Check if DeepSeek API is accessible"""
        try:
            # Simple test call
            self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5,
                timeout=10,
            )
            return True
        except Exception as e:
            logger.warning(f"DeepSeek availability check failed: {e}")
            return False

    def get_model_info(self) -> Dict[str, Union[str, int, float, List[str]]]:
        """Get model metadata"""
        pricing = self.PRICING.get(self.model, {"input": 0.14, "output": 0.28})
        return {
            "model": self.model,
            "provider": "deepseek",
            "context_window": 64000,  # DeepSeek-V3 supports 64K
            "max_output_tokens": 8192,
            "supported_models": self.SUPPORTED_MODELS,
            "cost_per_1m_input": pricing["input"],
            "cost_per_1m_output": pricing["output"],
            "capabilities": ["chat", "code", "reasoning"],
        }

    def count_tokens(self, text: str) -> int:
        """Approximate token count (DeepSeek uses similar tokenization to GPT)"""
        # Rough approximation: 1 token ≈ 4 characters for English
        return len(text) // 4

    @property
    def provider_type(self) -> ProviderType:
        """Get provider type identifier"""
        return ProviderType.DEEPSEEK

    def _get_provider_type(self) -> ProviderType:
        """Return the provider type enum"""
        return ProviderType.DEEPSEEK
