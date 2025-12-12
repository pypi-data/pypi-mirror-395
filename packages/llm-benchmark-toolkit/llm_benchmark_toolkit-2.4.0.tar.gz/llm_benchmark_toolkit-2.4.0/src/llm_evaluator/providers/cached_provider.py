"""
Cached Provider Wrapper

Wraps any LLMProvider with intelligent caching to avoid redundant API calls.
Provides 10x+ speedup for repeated evaluations.

Features:
- In-memory caching
- Optional disk persistence
- Configurable cache size
- TTL (time-to-live) support
"""

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Union

from .base import GenerationConfig, GenerationResult, LLMProvider, ProviderType

logger = logging.getLogger(__name__)


class CachedProvider(LLMProvider):
    """
    Wrapper that adds caching to any LLMProvider

    Caches generation results in memory and optionally on disk.
    Significantly speeds up benchmark re-runs and testing.

    Example:
        >>> from llm_evaluator.providers.ollama_provider import OllamaProvider
        >>> base_provider = OllamaProvider(model="llama3.2:1b")
        >>> cached = CachedProvider(base_provider, cache_dir="cache/")
        >>>
        >>> # First call: hits API
        >>> result1 = cached.generate("What is Python?")  # ~2 seconds
        >>>
        >>> # Second call: from cache
        >>> result2 = cached.generate("What is Python?")  # ~0.001 seconds
        >>> assert result1.text == result2.text
    """

    def __init__(
        self,
        provider: LLMProvider,
        cache_dir: Optional[str] = None,
        max_cache_size: int = 10000,
        ttl_seconds: Optional[int] = None,
        enable_disk_cache: bool = True,
    ):
        """
        Initialize cached provider wrapper

        Args:
            provider: Base LLM provider to wrap
            cache_dir: Directory for disk cache (default: .cache/llm_eval/)
            max_cache_size: Maximum number of entries in memory cache
            ttl_seconds: Time-to-live for cache entries (None = no expiry)
            enable_disk_cache: Whether to use disk caching
        """
        # Don't call super().__init__ as we're wrapping, not inheriting
        self.provider = provider
        self.model = provider.model
        self.config = provider.config

        # In-memory cache: {cache_key: (result, timestamp)}
        self._memory_cache: Dict[str, tuple[GenerationResult, float]] = {}
        self.max_cache_size = max_cache_size
        self.ttl_seconds = ttl_seconds

        # Disk cache - sanitize model name for filesystem
        self.enable_disk_cache = enable_disk_cache
        safe_model_name = self.model.replace("/", "_").replace(":", "_").replace("\\", "_")
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path.home() / ".cache" / "llm_eval" / safe_model_name

        if self.enable_disk_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Disk cache enabled: {self.cache_dir}")

        # Statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "disk_hits": 0,
            "evictions": 0,
        }

        logger.info(f"Initialized cached provider wrapping {provider.__class__.__name__}")

    def _generate_cache_key(
        self, prompt: str, system_prompt: Optional[str], config: Optional[GenerationConfig]
    ) -> str:
        """
        Generate unique cache key for a request

        Uses SHA256 hash of prompt + config parameters.

        Args:
            prompt: User prompt
            system_prompt: System prompt
            config: Generation config

        Returns:
            Cache key string
        """
        cfg = config or self.config

        # Build key components
        key_data = {
            "model": self.model,
            "prompt": prompt,
            "system_prompt": system_prompt,
            "temperature": cfg.temperature,
            "max_tokens": cfg.max_tokens,
            "top_p": cfg.top_p,
            "top_k": cfg.top_k,
        }

        # Hash to fixed-length key
        key_string = json.dumps(key_data, sort_keys=True)
        cache_key = hashlib.sha256(key_string.encode()).hexdigest()

        return cache_key

    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cached entry is still valid based on TTL"""
        if self.ttl_seconds is None:
            return True
        return (time.time() - timestamp) < self.ttl_seconds

    def _get_from_memory_cache(self, cache_key: str) -> Optional[GenerationResult]:
        """Get result from in-memory cache"""
        if cache_key in self._memory_cache:
            result, timestamp = self._memory_cache[cache_key]
            if self._is_cache_valid(timestamp):
                self.stats["hits"] += 1
                logger.debug(f"Memory cache HIT: {cache_key[:16]}...")
                return result
            else:
                # Expired, remove
                del self._memory_cache[cache_key]
                logger.debug(f"Cache entry expired: {cache_key[:16]}...")
        return None

    def _get_from_disk_cache(self, cache_key: str) -> Optional[GenerationResult]:
        """Get result from disk cache"""
        if not self.enable_disk_cache:
            return None

        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text())

                # Check TTL
                if not self._is_cache_valid(data["timestamp"]):
                    cache_file.unlink()  # Delete expired
                    return None

                # Reconstruct GenerationResult
                result = GenerationResult(
                    text=data["text"],
                    response_time=data["response_time"],
                    tokens_used=data.get("tokens_used", data.get("token_count", 0)),
                    model=data.get("model", data.get("model_name", "")),
                    metadata=data["metadata"],
                )

                # Add to memory cache for faster future access
                self._memory_cache[cache_key] = (result, data["timestamp"])

                self.stats["disk_hits"] += 1
                logger.debug(f"Disk cache HIT: {cache_key[:16]}...")
                return result

            except Exception as e:
                logger.warning(f"Failed to read disk cache: {e}")
                return None
        return None

    def _save_to_cache(self, cache_key: str, result: GenerationResult) -> None:
        """Save result to both memory and disk cache"""
        timestamp = time.time()

        # Memory cache
        if len(self._memory_cache) >= self.max_cache_size:
            # Evict oldest entry (simple FIFO)
            oldest_key = next(iter(self._memory_cache))
            del self._memory_cache[oldest_key]
            self.stats["evictions"] += 1
            logger.debug(f"Evicted cache entry: {oldest_key[:16]}...")

        self._memory_cache[cache_key] = (result, timestamp)

        # Disk cache
        if self.enable_disk_cache:
            try:
                cache_file = self.cache_dir / f"{cache_key}.json"
                data = {
                    "text": result.text,
                    "response_time": result.response_time,
                    "tokens_used": result.tokens_used,
                    "model": result.model,
                    "metadata": result.metadata,
                    "timestamp": timestamp,
                }
                cache_file.write_text(json.dumps(data, indent=2))
            except Exception as e:
                logger.warning(f"Failed to write disk cache: {e}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> GenerationResult:
        """
        Generate with caching

        Checks cache first, falls back to provider if miss.
        """
        cache_key = self._generate_cache_key(prompt, system_prompt, config)

        # Try memory cache
        cached = self._get_from_memory_cache(cache_key)
        if cached:
            return cached

        # Try disk cache
        cached = self._get_from_disk_cache(cache_key)
        if cached:
            return cached

        # Cache miss - call provider
        self.stats["misses"] += 1
        logger.debug(f"Cache MISS: {cache_key[:16]}... (calling provider)")

        result = self.provider.generate(prompt, system_prompt, config)

        # Save to cache
        self._save_to_cache(cache_key, result)

        return result

    def generate_batch(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
    ) -> List[GenerationResult]:
        """Generate batch with per-prompt caching"""
        return [self.generate(p, system_prompt, config) for p in prompts]

    def clear_cache(self, disk_only: bool = False) -> None:
        """
        Clear cache

        Args:
            disk_only: If True, only clear disk cache (keep memory)
        """
        if not disk_only:
            self._memory_cache.clear()
            logger.info("Memory cache cleared")

        if self.enable_disk_cache:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            logger.info(f"Disk cache cleared: {self.cache_dir}")

    def get_cache_stats(self) -> Dict[str, Union[int, float]]:
        """
        Get cache performance statistics

        Returns:
            Dictionary with hits, misses, hit rate, etc.
        """
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0

        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "disk_hits": self.stats["disk_hits"],
            "evictions": self.stats["evictions"],
            "total_requests": total_requests,
            "hit_rate_percent": round(hit_rate, 2),
            "memory_cache_size": len(self._memory_cache),
        }

    def is_available(self) -> bool:
        """Check if underlying provider is available"""
        return self.provider.is_available()

    def get_model_info(self) -> Dict[str, Union[str, int, float, List[str]]]:
        """Get model info from underlying provider"""
        info = self.provider.get_model_info()
        info["cached"] = True
        return info

    def _get_provider_type(self) -> ProviderType:
        """Return underlying provider type"""
        return self.provider._get_provider_type()
