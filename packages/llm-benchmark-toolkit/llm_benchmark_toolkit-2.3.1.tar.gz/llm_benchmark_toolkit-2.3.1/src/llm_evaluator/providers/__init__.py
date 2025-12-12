"""
LLM Provider abstraction layer.

Supports multiple backends: Ollama (local), OpenAI, Anthropic, HuggingFace.
"""

from typing import Any

from .base import (
    AuthenticationError,
    GenerationConfig,
    GenerationResult,
    LLMProvider,
    ModelNotFoundError,
    ProviderError,
    ProviderType,
    RateLimitError,
    TimeoutError,
)
from .cached_provider import CachedProvider
from .ollama_provider import OllamaProvider

# Conditional imports for optional providers
_has_openai = False
OpenAIProvider: Any = None
try:
    from .openai_provider import OpenAIProvider as _OpenAIProvider

    OpenAIProvider = _OpenAIProvider
    _has_openai = True
except ImportError:
    pass

_has_anthropic = False
AnthropicProvider: Any = None
try:
    from .anthropic_provider import AnthropicProvider as _AnthropicProvider

    AnthropicProvider = _AnthropicProvider
    _has_anthropic = True
except ImportError:
    pass

_has_huggingface = False
HuggingFaceProvider: Any = None
try:
    from .huggingface_provider import HuggingFaceProvider as _HuggingFaceProvider

    HuggingFaceProvider = _HuggingFaceProvider
    _has_huggingface = True
except ImportError:
    pass

_has_deepseek = False
DeepSeekProvider: Any = None
try:
    from .deepseek_provider import DeepSeekProvider as _DeepSeekProvider

    DeepSeekProvider = _DeepSeekProvider
    _has_deepseek = True
except ImportError:
    pass

# New providers (all use OpenAI-compatible API)
_has_groq = False
GroqProvider: Any = None
try:
    from .groq_provider import GroqProvider as _GroqProvider

    GroqProvider = _GroqProvider
    _has_groq = True
except ImportError:
    pass

_has_together = False
TogetherProvider: Any = None
try:
    from .together_provider import TogetherProvider as _TogetherProvider

    TogetherProvider = _TogetherProvider
    _has_together = True
except ImportError:
    pass

_has_fireworks = False
FireworksProvider: Any = None
try:
    from .fireworks_provider import FireworksProvider as _FireworksProvider

    FireworksProvider = _FireworksProvider
    _has_fireworks = True
except ImportError:
    pass

__all__ = [
    # Types
    "ProviderType",
    "GenerationConfig",
    "GenerationResult",
    # Base class
    "LLMProvider",
    # Errors
    "ProviderError",
    "RateLimitError",
    "AuthenticationError",
    "ModelNotFoundError",
    "TimeoutError",
    # Providers
    "OllamaProvider",
    "CachedProvider",
    "OpenAIProvider",
    "AnthropicProvider",
    "HuggingFaceProvider",
    "DeepSeekProvider",
    "GroqProvider",
    "TogetherProvider",
    "FireworksProvider",
]
