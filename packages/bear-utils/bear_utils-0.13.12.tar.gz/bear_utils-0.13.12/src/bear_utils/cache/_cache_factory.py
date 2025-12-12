"""Cache factory for configurable diskcache instances."""

from __future__ import annotations

from pathlib import Path  # noqa: TC003
from typing import TYPE_CHECKING, ClassVar, Literal, Protocol

from funcy_bear.constants import Megabytes

from bear_epoch_time import SECONDS_IN_MINUTE as MINUTES

from ._modified_cache import ModifiedCache

if TYPE_CHECKING:
    from _typeshed import StrPath


class ConfigProtocol(Protocol):
    """Protocol for cache configuration."""

    base_directory: StrPath
    default_size_limit: int
    eviction_policy: str
    default_expiry: int


EvictionPolicies = Literal["least-recently-used", "least-frequently-used", "none"]


class BaseCacheFactory:
    """Factory for creating configured cache instances."""

    _default_size_limit: ClassVar[int] = Megabytes(100)
    _default_eviction_policy: ClassVar[EvictionPolicies] = "least-recently-used"
    _default_expiry: ClassVar[int] = 5 * MINUTES

    def __init__(self, base_dir: Path, config: ConfigProtocol | None = None) -> None:
        """Initialize the cache factory."""
        self.base_dir: Path = base_dir
        self.config: ConfigProtocol | None = config

    def get_size_limit(self, override: int | None = None) -> int:
        """Get the default size limit for caches."""
        return override or getattr(self.config, "default_size_limit", None) or self._default_size_limit

    def get_eviction_policy(self, override: EvictionPolicies | None = None) -> EvictionPolicies:
        """Get the default eviction policy for caches."""
        if override is not None:
            return override
        if not hasattr(self.config, "eviction_policy"):
            return self._default_eviction_policy
        return getattr(self.config, "eviction_policy", "none")

    def get_expiry(self, override: int | None = None) -> int:
        """Get the default expiry time for caches."""
        if override is not None:
            return override
        if not hasattr(self.config, "default_expiry"):
            return self._default_expiry
        return getattr(self.config, "default_expiry", 0)

    def get_cache(self, cache_type: str, **kwargs) -> ModifiedCache:
        """Get a cache instance for the specified type.

        Args:
            cache_type: name of the cache type (used as subdirectory)
            **kwargs: Optional overrides for size_limit, eviction_policy, expiry

        Returns:
            Configured Cache instance
        """
        return ModifiedCache(
            directory=str(self.base_dir / cache_type),
            size_limit=self.get_size_limit(kwargs.get("size_limit")),
            eviction_policy=self.get_eviction_policy(kwargs.get("eviction_policy")),
            ignore_exceptions=kwargs.get("ignore_exceptions", True),
            expiry=self.get_expiry(kwargs.get("expiry")),
        )


__all__ = ["BaseCacheFactory", "ModifiedCache"]
