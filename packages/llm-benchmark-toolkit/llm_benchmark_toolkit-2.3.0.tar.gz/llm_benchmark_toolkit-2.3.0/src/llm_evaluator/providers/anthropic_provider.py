"""
Anthropic Provider for Claude models

Implements the LLMProvider interface for Anthropic's Claude API.
Requires: pip install anthropic
"""

import logging
import time
from typing import Dict, List, Optional, Union

try:
    from anthropic import Anthropic, APIError, APITimeoutError
    from anthropic import RateLimitError as AnthropicRateLimitError
except ImportError:
    raise ImportError(
        "Anthropic provider requires 'anthropic' package. Install with: pip install anthropic"
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


class AnthropicProvider(LLMProvider):
    """
    Anthropic provider for Claude models

    Supports:
    - Claude 3 Opus (claude-3-opus-20240229)
    - Claude 3 Sonnet (claude-3-sonnet-20240229)
    - Claude 3 Haiku (claude-3-haiku-20240307)
    - Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)

    Requires ANTHROPIC_API_KEY environment variable or api_key parameter.

    Example:
        >>> import os
        >>> os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."
        >>> provider = AnthropicProvider(model="claude-3-5-sonnet-20241022")
        >>> result = provider.generate("Hello, world!")
        >>> print(result.text)
    """

    SUPPORTED_MODELS = [
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
        "claude-3-5-sonnet-20241022",
        "claude-3-5-sonnet-20240620",
    ]

    def __init__(
        self,
        model: str = "claude-3-5-sonnet-20241022",
        api_key: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
        base_url: Optional[str] = None,
    ):
        """
        Initialize Anthropic provider

        Args:
            model: Model name (e.g., "claude-3-5-sonnet-20241022")
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
            config: Generation configuration
            base_url: Custom API base URL (for proxies)
        """
        super().__init__(model, config)

        self.api_key = api_key
        self.base_url = base_url

        # Initialize Anthropic client
        if api_key and base_url:
            self.client = Anthropic(api_key=api_key, base_url=base_url)
        elif api_key:
            self.client = Anthropic(api_key=api_key)
        elif base_url:
            self.client = Anthropic(base_url=base_url)
        else:
            self.client = Anthropic()

        logger.info(f"Initialized Anthropic provider with model: {model}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> GenerationResult:
        """
        Generate text using Anthropic API

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

        # Retry logic with exponential backoff
        last_error: Optional[Exception] = None
        for attempt in range(cfg.retry_attempts):
            try:
                start_time = time.time()

                if system_prompt:
                    response = self.client.messages.create(
                        model=self.model,
                        max_tokens=cfg.max_tokens,
                        temperature=cfg.temperature,
                        top_p=cfg.top_p,
                        messages=[{"role": "user", "content": prompt}],
                        timeout=float(cfg.timeout_seconds),
                        system=system_prompt,
                    )
                else:
                    response = self.client.messages.create(
                        model=self.model,
                        max_tokens=cfg.max_tokens,
                        temperature=cfg.temperature,
                        top_p=cfg.top_p,
                        messages=[{"role": "user", "content": prompt}],
                        timeout=float(cfg.timeout_seconds),
                    )

                elapsed = time.time() - start_time

                # Extract response text
                text = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        text += block.text

                # Token counts
                usage = response.usage
                input_tokens = usage.input_tokens if usage else 0
                output_tokens = usage.output_tokens if usage else 0
                total_tokens = input_tokens + output_tokens

                logger.debug(
                    f"Anthropic generation successful: {total_tokens} tokens in {elapsed:.2f}s"
                )

                return GenerationResult(
                    text=text,
                    response_time=elapsed,
                    tokens_used=total_tokens,
                    model=self.model,
                    metadata={
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "total_tokens": total_tokens,
                        "stop_reason": response.stop_reason or "unknown",
                        "provider": "anthropic",
                    },
                )

            except AnthropicRateLimitError as e:
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
                error_str = str(e).lower()
                if "model" in error_str and ("not found" in error_str or "invalid" in error_str):
                    raise ModelNotFoundError(
                        message=f"Model '{self.model}' not found",
                        original_error=e,
                    )
                else:
                    raise ProviderError(
                        message=f"Anthropic API error: {str(e)}",
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

        Note: Anthropic doesn't have native batch API for messages,
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
                        metadata={"error": str(e), "provider": "anthropic"},
                    )
                )

        return results

    def is_available(self) -> bool:
        """
        Check if Anthropic API is accessible

        Returns:
            True if API key is valid and service is reachable
        """
        try:
            # Try a minimal message to verify API access
            self.client.messages.create(
                model=self.model,
                max_tokens=1,
                messages=[{"role": "user", "content": "test"}],
            )
            return True
        except Exception as e:
            logger.error(f"Anthropic API not available: {e}")
            return False

    def get_model_info(self) -> Dict[str, Union[str, int, float, List[str]]]:
        """
        Get information about the current model

        Returns:
            Dictionary with model metadata
        """
        # Anthropic doesn't have a models.retrieve endpoint
        # Return basic info
        model_family = "unknown"
        if "opus" in self.model:
            model_family = "claude-3-opus"
        elif "sonnet" in self.model:
            if "3-5" in self.model:
                model_family = "claude-3.5-sonnet"
            else:
                model_family = "claude-3-sonnet"
        elif "haiku" in self.model:
            model_family = "claude-3-haiku"

        return {
            "model_id": self.model,
            "model_family": model_family,
            "provider": "anthropic",
            "context_window": 200000,  # Claude 3 has 200k context
        }

    def _get_provider_type(self) -> ProviderType:
        """Return provider type"""
        return ProviderType.ANTHROPIC
