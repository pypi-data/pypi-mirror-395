"""
HuggingFace Provider for Inference API

Implements the LLMProvider interface for HuggingFace's Inference API.
Requires: pip install huggingface-hub
"""

import logging
import time
from typing import Dict, List, Optional, Union

try:
    from huggingface_hub import InferenceClient
    from huggingface_hub.utils import HfHubHTTPError  # type: ignore[attr-defined]
except ImportError:
    raise ImportError(
        "HuggingFace provider requires 'huggingface-hub' package. "
        "Install with: pip install huggingface-hub"
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


class HuggingFaceProvider(LLMProvider):
    """
    HuggingFace Inference API provider

    Supports any text-generation model on HuggingFace Hub.

    Popular models:
    - meta-llama/Meta-Llama-3-8B-Instruct
    - mistralai/Mistral-7B-Instruct-v0.2
    - google/gemma-7b-it
    - microsoft/phi-2

    Requires HF_TOKEN environment variable or token parameter.

    Example:
        >>> import os
        >>> os.environ["HF_TOKEN"] = "hf_..."
        >>> provider = HuggingFaceProvider(model="meta-llama/Meta-Llama-3-8B-Instruct")
        >>> result = provider.generate("Hello, world!")
        >>> print(result.text)
    """

    def __init__(
        self,
        model: str = "meta-llama/Meta-Llama-3-8B-Instruct",
        token: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
        base_url: Optional[str] = None,
    ):
        """
        Initialize HuggingFace provider

        Args:
            model: Model ID on HuggingFace Hub
            token: HuggingFace API token (or set HF_TOKEN env var)
            config: Generation configuration
            base_url: Custom inference endpoint URL
        """
        super().__init__(model, config)

        self.token = token
        self.base_url = base_url

        # Initialize HuggingFace client
        self.client = InferenceClient(
            model=model,
            token=token,
        )

        logger.info(f"Initialized HuggingFace provider with model: {model}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> GenerationResult:
        """
        Generate text using HuggingFace Inference API

        Args:
            prompt: User prompt
            system_prompt: Optional system message (prepended to prompt)
            config: Override generation config

        Returns:
            GenerationResult with response

        Raises:
            ProviderError: On API errors
            RateLimitError: On rate limit
            TimeoutError: On timeout
        """
        cfg = config or self.config

        # Combine system and user prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        # Retry logic with exponential backoff
        last_error = None
        for attempt in range(cfg.retry_attempts):
            try:
                start_time = time.time()

                # Use text_generation endpoint with keyword arguments
                response = self.client.text_generation(
                    prompt=full_prompt,
                    max_new_tokens=cfg.max_tokens,
                    temperature=cfg.temperature,
                    top_p=cfg.top_p,
                    top_k=cfg.top_k if hasattr(cfg, "top_k") else None,
                    do_sample=cfg.temperature > 0,
                    return_full_text=False,
                )

                elapsed = time.time() - start_time

                # Extract response text
                text = response if isinstance(response, str) else response.generated_text

                # Estimate token count (HF doesn't always provide this)
                # Rough estimate: ~4 chars per token
                estimated_tokens = len(text) // 4

                logger.debug(
                    f"HuggingFace generation successful: ~{estimated_tokens} tokens in {elapsed:.2f}s"
                )

                return GenerationResult(
                    text=text,
                    response_time=elapsed,
                    tokens_used=estimated_tokens,
                    model=self.model,
                    metadata={
                        "estimated_tokens": estimated_tokens,
                        "provider": "huggingface",
                        "prompt_length": len(full_prompt),
                    },
                )

            except HfHubHTTPError as e:
                last_error = e

                # Check error type
                if e.response.status_code == 429:
                    # Rate limit
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

                elif e.response.status_code == 404:
                    raise ModelNotFoundError(
                        message=f"Model '{self.model}' not found on HuggingFace Hub",
                        original_error=e,
                    )

                elif e.response.status_code == 503:
                    # Model loading or temporarily unavailable
                    if attempt < cfg.retry_attempts - 1:
                        wait_time = 5 * (attempt + 1)  # 5s, 10s, 15s
                        logger.warning(f"Model loading, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise ProviderError(
                            message=f"Model unavailable after {cfg.retry_attempts} attempts",
                            original_error=e,
                        )
                else:
                    raise ProviderError(
                        message=f"HuggingFace API error: {str(e)}",
                        original_error=e,
                    )

            except TimeoutError as e:
                last_error = e  # type: ignore[assignment]
                if attempt < cfg.retry_attempts - 1:
                    wait_time = 2**attempt
                    logger.warning(f"Timeout, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise TimeoutError(
                        message=f"Request timed out after {cfg.retry_attempts} attempts",
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
                    time.sleep(1.0)  # HF free tier needs more delay

            except ProviderError as e:
                logger.error(f"Failed to generate for prompt {i}: {e.message}")
                # Add error result
                results.append(
                    GenerationResult(
                        text="",
                        response_time=0.0,
                        tokens_used=0,
                        model=self.model,
                        metadata={"error": str(e), "provider": "huggingface"},
                    )
                )

        return results

    def is_available(self) -> bool:
        """
        Check if HuggingFace Inference API is accessible

        Returns:
            True if model is accessible
        """
        try:
            # Try a minimal generation to verify access
            self.client.text_generation(
                prompt="test",
                max_new_tokens=1,
            )
            return True
        except Exception as e:
            logger.error(f"HuggingFace API not available: {e}")
            return False

    def get_model_info(self) -> Dict[str, Union[str, int, float, List[str]]]:
        """
        Get information about the current model

        Returns:
            Dictionary with model metadata
        """
        try:
            # Try to get model info from HF Hub
            from huggingface_hub import model_info

            info = model_info(self.model, token=self.token)

            downloads = info.downloads if hasattr(info, "downloads") and info.downloads else 0
            likes = info.likes if hasattr(info, "likes") and info.likes else 0

            return {
                "model_id": self.model,
                "model_type": info.pipeline_tag or "text-generation",
                "provider": "huggingface",
                "downloads": downloads,
                "likes": likes,
            }
        except Exception as e:
            logger.warning(f"Could not retrieve model info: {e}")
            return {
                "model_id": self.model,
                "provider": "huggingface",
                "error": str(e),
            }

    def _get_provider_type(self) -> ProviderType:
        """Return provider type"""
        return ProviderType.HUGGINGFACE
