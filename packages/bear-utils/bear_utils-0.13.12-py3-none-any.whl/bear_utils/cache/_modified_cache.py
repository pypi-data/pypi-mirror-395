"""Modified Cache Module."""

from __future__ import annotations

from functools import cache
from typing import TYPE_CHECKING, Any

from diskcache import Cache
from funcy_bear.sentinels import NOTSET, NotSetType

if TYPE_CHECKING:
    from collections.abc import Callable


@cache
def match(key: Any, query: Any) -> bool:
    """Check if the query matches the key."""
    if not isinstance(query, str):
        query = str(query)

    return (isinstance(key, (tuple | list)) and any(query in str(part) for part in key)) or query in str(key)


class ModifiedCache(Cache):
    """A modified cache class with additional functionality."""

    def __init__(self, expiry: float | NotSetType = NOTSET, *args, **kwargs) -> None:
        """Initialize the cache with custom parameters.

        Args:
            expiry: Default expiry time for cache entries in seconds, allows one to
            set the default expiry for all memoized functions in this cache instance.
            Uses a sentinel value NOTSET to indicate no default expiry if not provided.
        """
        self.expiry: float | NotSetType = expiry
        super().__init__(*args, **kwargs)

    def find(self, query: Any) -> list[Any]:
        """Find cache entries matching the query.

        Args:
            query: The query string to match against cache keys.

        Returns:
            A list of matching cache keys.
        """
        return [key for key in self if match(key, query)]

    def deletes(self, *keys: Any) -> bool:
        """Delete multiple cache entries by their keys.

        Args:
            *keys: The keys of the cache entries to delete.

        Returns:
            True if all deletions were successful, False otherwise.
        """
        return all(self.delete(key) for key in keys)

    def find_and_delete(self, query: Any) -> bool:
        """Find and delete cache entries matching the query.

        Args:
            query: The query string to match against cache keys.
        """
        find: list[Any] = self.find(query)
        if find:
            return self.deletes(*find)
        return False

    def memoize(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        name: str | None = None,
        typed: bool = False,
        expire: float | NotSetType = NOTSET,
        **kwargs,
    ) -> Callable:
        return super().memoize(
            name=name,
            typed=typed,
            expire=expire if expire is not NOTSET else self.expiry if self.expiry is not NOTSET else None,
            **kwargs,
        )
