"""
OpenAI Provider for GPT-3.5/GPT-4 models

Implements the LLMProvider interface for OpenAI's API.
Requires: pip install openai
"""

import logging
import time
from typing import Dict, List, Optional, Union

try:
    from openai import APIError, APITimeoutError, OpenAI
    from openai import RateLimitError as OpenAIRateLimitError
    from openai.types.chat import ChatCompletionMessageParam
except ImportError:
    raise ImportError("OpenAI provider requires 'openai' package. Install with: pip install openai")

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


class OpenAIProvider(LLMProvider):
    """
    OpenAI provider for GPT models

    Supports:
    - GPT-4 (gpt-4, gpt-4-turbo, gpt-4o)
    - GPT-3.5 (gpt-3.5-turbo)

    Requires OPENAI_API_KEY environment variable or api_key parameter.

    Example:
        >>> import os
        >>> os.environ["OPENAI_API_KEY"] = "sk-..."
        >>> provider = OpenAIProvider(model="gpt-3.5-turbo")
        >>> result = provider.generate("Hello, world!")
        >>> print(result.text)
    """

    SUPPORTED_MODELS = [
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4-turbo-preview",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
    ]

    # Pricing per 1M tokens (as of 2024)
    PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-4-turbo-preview": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        "gpt-3.5-turbo-16k": {"input": 1.00, "output": 2.00},
    }

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
        base_url: Optional[str] = None,
        organization: Optional[str] = None,
    ):
        """
        Initialize OpenAI provider

        Args:
            model: Model name (e.g., "gpt-3.5-turbo", "gpt-4")
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            config: Generation configuration
            base_url: Custom API base URL (for proxies)
            organization: OpenAI organization ID
        """
        super().__init__(model, config)

        self.api_key = api_key
        self.base_url = base_url
        self.organization = organization

        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            organization=organization,
        )

        logger.info(f"Initialized OpenAI provider with model: {model}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> GenerationResult:
        """
        Generate text using OpenAI API

        Args:
            prompt: User prompt
            system_prompt: Optional system message
            config: Override generation config

        Returns:
            GenerationResult with response

        Raises:
            ProviderError: On API errors
            RateLimitError: On rate limit
            TimeoutError: On timeout
        """
        cfg = config or self.config

        # Build messages with proper typing
        messages: List[ChatCompletionMessageParam] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Retry logic with exponential backoff
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

                # Extract response
                choice = response.choices[0]
                text = choice.message.content or ""

                # Token counts
                usage = response.usage
                prompt_tokens = usage.prompt_tokens if usage else 0
                completion_tokens = usage.completion_tokens if usage else 0
                total_tokens = usage.total_tokens if usage else 0

                # Calculate cost
                pricing = self.PRICING.get(self.model, {"input": 0.0, "output": 0.0})
                cost = (prompt_tokens / 1_000_000) * pricing["input"] + (
                    completion_tokens / 1_000_000
                ) * pricing["output"]

                logger.debug(
                    f"OpenAI generation successful: {total_tokens} tokens in {elapsed:.2f}s"
                )

                return GenerationResult(
                    text=text,
                    response_time=elapsed,
                    tokens_used=total_tokens,
                    model=self.model,
                    provider="openai",
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
                # Check if it's a model not found error
                if "model" in str(e).lower() and "not found" in str(e).lower():
                    raise ModelNotFoundError(
                        message=f"Model '{self.model}' not found",
                        original_error=e,
                    )
                else:
                    raise ProviderError(
                        message=f"OpenAI API error: {str(e)}",
                        original_error=e,
                    )

            except Exception as e:
                raise ProviderError(
                    message=f"Unexpected error: {str(e)}",
                    original_error=e,
                )

        # Should not reach here
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
        """
        Generate responses for multiple prompts

        Note: OpenAI doesn't have native batch API for chat completions,
        so we process sequentially with rate limiting.

        Args:
            prompts: List of prompts
            system_prompt: Optional system message
            config: Override generation config

        Returns:
            List of GenerationResults
        """
        results = []

        for i, prompt in enumerate(prompts):
            try:
                result = self.generate(prompt, system_prompt, config)
                results.append(result)

                # Rate limiting: small delay between requests
                if i < len(prompts) - 1:
                    time.sleep(0.5)

            except ProviderError as e:
                logger.error(f"Failed to generate for prompt {i}: {e.message}")
                # Add error result
                results.append(
                    GenerationResult(
                        text="",
                        response_time=0.0,
                        tokens_used=0,
                        model=self.model,
                        metadata={"error": str(e), "provider": "openai"},
                    )
                )

        return results

    def is_available(self) -> bool:
        """
        Check if OpenAI API is accessible

        Returns:
            True if API key is valid and service is reachable
        """
        try:
            # Try to list models to verify API access
            self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"OpenAI API not available: {e}")
            return False

    def get_model_info(self) -> Dict[str, Union[str, int, float, List[str]]]:
        """
        Get information about the current model

        Returns:
            Dictionary with model metadata
        """
        try:
            model_info = self.client.models.retrieve(self.model)

            return {
                "model_id": model_info.id,
                "owned_by": model_info.owned_by,
                "provider": "openai",
                "created": model_info.created,
            }
        except Exception as e:
            logger.warning(f"Could not retrieve model info: {e}")
            return {
                "model_id": self.model,
                "provider": "openai",
                "error": str(e),
            }

    def _get_provider_type(self) -> ProviderType:
        """Return provider type"""
        return ProviderType.OPENAI
