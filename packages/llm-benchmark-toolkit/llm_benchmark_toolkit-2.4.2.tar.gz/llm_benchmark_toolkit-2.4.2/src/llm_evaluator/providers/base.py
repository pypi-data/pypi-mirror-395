"""
Base classes and types for LLM providers.

This module defines the abstract interface and common types.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Union


class ProviderType(Enum):
    """Supported LLM provider types"""

    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    DEEPSEEK = "deepseek"
    GROQ = "groq"
    TOGETHER = "together"
    FIREWORKS = "fireworks"
    GEMINI = "gemini"


@dataclass
class GenerationConfig:
    """Configuration for text generation"""

    temperature: float = 0.7
    max_tokens: int = 512
    top_p: float = 0.9
    top_k: int = 40
    timeout_seconds: int = 30
    retry_attempts: int = 3


@dataclass
class GenerationResult:
    """Result from LLM generation with strict typing (no Any)"""

    text: str
    response_time: float
    tokens_used: int = 0
    model: str = ""
    provider: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    finish_reason: str = ""
    cached: bool = False
    error: Optional[str] = None
    metadata: Optional[Dict[str, Union[str, int, float]]] = None

    def __post_init__(self) -> None:
        """Validate and compute derived fields"""
        if self.total_tokens == 0 and (self.prompt_tokens or self.completion_tokens):
            self.total_tokens = self.prompt_tokens + self.completion_tokens


class ProviderError(Exception):
    """Base exception for provider errors"""

    def __init__(
        self,
        message: str = "",
        original_error: Optional[Exception] = None,
        **kwargs: object,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.original_error = original_error


class RateLimitError(ProviderError):
    """Rate limit exceeded"""

    def __init__(
        self,
        message: str = "",
        original_error: Optional[Exception] = None,
        retry_after: Optional[int] = None,
        **kwargs: object,
    ) -> None:
        super().__init__(message, original_error)
        self.retry_after = retry_after


class AuthenticationError(ProviderError):
    """Authentication failed"""

    pass


class ModelNotFoundError(ProviderError):
    """Model not found or not available"""

    pass


class TimeoutError(ProviderError):  # noqa: A001
    """Request timed out"""

    pass


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    Implements the Template Method pattern for consistent error handling
    and configuration management across different LLM backends.

    All providers must implement:
    - generate(): Generate text from a prompt
    - generate_batch(): Generate text for multiple prompts
    - is_available(): Check if provider is available
    - get_model_info(): Get model metadata
    """

    def __init__(
        self,
        model: str,
        config: Optional[GenerationConfig] = None,
    ) -> None:
        """
        Initialize provider with model and configuration.

        Args:
            model: Model identifier (e.g., "llama3.2:1b", "gpt-4")
            config: Generation configuration, uses defaults if None
        """
        self.model = model
        self.config = config or GenerationConfig()
        self._validate_config()

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> GenerationResult:
        """
        Generate text from a prompt.

        Args:
            prompt: The input prompt
            system_prompt: Optional system message for the model
            config: Optional override for generation config

        Returns:
            GenerationResult with generated text and metadata

        Raises:
            ProviderError: If generation fails
        """
        pass

    @abstractmethod
    def generate_batch(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> List[GenerationResult]:
        """
        Generate text for multiple prompts.

        Args:
            prompts: List of input prompts
            system_prompt: Optional system message for the model
            config: Optional override for generation config

        Returns:
            List of GenerationResult objects

        Raises:
            ProviderError: If generation fails
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider and model are available.

        Returns:
            True if provider can be used, False otherwise
        """
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Union[str, int, float, List[str]]]:
        """
        Get information about the model.

        Returns:
            Dictionary with model metadata (size, context, etc.)
        """
        pass

    def _validate_config(self) -> None:
        """Validate configuration parameters"""
        if not 0 <= self.config.temperature <= 2:
            raise ValueError("Temperature must be between 0 and 2")
        if self.config.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        if not 0 <= self.config.top_p <= 1:
            raise ValueError("top_p must be between 0 and 1")

    @property
    def provider_type(self) -> ProviderType:
        """Get the provider type"""
        return self._get_provider_type()

    @abstractmethod
    def _get_provider_type(self) -> ProviderType:
        """Return the provider type enum"""
        pass
