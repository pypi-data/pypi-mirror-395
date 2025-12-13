# SPDX-License-Identifier: MIT
"""Performance optimization utilities for screen refresh and caching."""

import time
from collections.abc import Callable
from functools import lru_cache
from typing import Any, TypeVar, overload

T = TypeVar("T")


class CachedProperty:
    """Decorator for cached properties that expire on data changes."""

    def __init__(self, func: Callable[[Any], Any]) -> None:
        """Initialize cached property.

        Args:
            func: The property getter function
        """
        self.func: Callable[[Any], Any] = func
        self.cache: dict[int, Any] = {}
        self.timestamps: dict[int, int] = {}

    @overload
    def __get__(self, obj: None, objtype: Any = None) -> "CachedProperty": ...

    @overload
    def __get__(self, obj: Any, objtype: Any = None) -> Any: ...

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        """Get cached property value, computing if needed."""
        if obj is None:
            return self

        obj_id = id(obj)
        # Check if we have a cached value for this object
        if obj_id in self.cache:
            return self.cache[obj_id]

        # Compute and cache the value
        value = self.func(obj)
        self.cache[obj_id] = value
        return value

    def invalidate(self, obj: Any) -> None:
        """Invalidate cache for a specific object.

        Args:
            obj: Object instance to clear cache for
        """
        obj_id = id(obj)
        self.cache.pop(obj_id, None)
        self.timestamps.pop(obj_id, None)


def memoize_with_ttl(ttl: float = 1.0) -> Callable:
    """Decorator to memoize function results with time-to-live.

    Args:
        ttl: Time-to-live in seconds for cached results

    Returns:
        Decorator function
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        """Decorate function to add TTL-based memoization."""
        cache: dict[tuple, tuple[T, float]] = {}

        def wrapper(*args: Any, **kwargs: Any) -> T:
            """Wrapper function with memoization logic."""
            # Create cache key from args and kwargs
            key = (args, tuple(sorted(kwargs.items())))

            # Check if cached value exists and is still valid
            if key in cache:
                result, timestamp = cache[key]
                if time.time() - timestamp < ttl:
                    return result

            # Compute and cache result
            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result

        wrapper.cache = cache  # type: ignore
        return wrapper

    return decorator


@lru_cache(maxsize=128)
def get_sort_key_for_entry(
    entry_id: int,
    sort_mode: str,
    is_read: bool,
    published_at: str,
    feed_title: str,
) -> tuple:
    """Get the sort key for an entry (cached).

    Args:
        entry_id: Entry ID
        sort_mode: Sort mode (date, feed, status)
        is_read: Whether entry is read
        published_at: Publication timestamp
        feed_title: Feed title for feed sort

    Returns:
        Tuple representing sort key
    """
    if sort_mode == "date":
        # Sort by date (newest first)
        return (published_at,)
    if sort_mode == "feed":
        # Sort by feed name then date
        return (feed_title.lower(), published_at)
    if sort_mode == "status":
        # Sort by read status then date
        return (is_read, published_at)
    return (entry_id,)


class ScreenRefreshOptimizer:
    """Optimizer for screen refresh operations.

    Tracks refresh patterns and provides recommendations for optimization.
    """

    def __init__(self):
        """Initialize refresh optimizer."""
        self.refresh_count = 0
        self.full_refresh_count = 0
        self.partial_refresh_count = 0
        self.last_operation = None

    def track_full_refresh(self) -> None:
        """Track a full screen refresh operation."""
        self.refresh_count += 1
        self.full_refresh_count += 1

    def track_partial_refresh(self) -> None:
        """Track a partial (incremental) screen refresh operation."""
        self.refresh_count += 1
        self.partial_refresh_count += 1

    def get_efficiency_ratio(self) -> float:
        """Get ratio of partial refreshes to total refreshes.

        Returns:
            Ratio from 0.0 to 1.0 (higher is better)
        """
        if self.refresh_count == 0:
            return 0.0
        return self.partial_refresh_count / self.refresh_count

    def get_stats(self) -> dict[str, Any]:
        """Get performance statistics.

        Returns:
            Dictionary with refresh statistics
        """
        return {
            "total_refreshes": self.refresh_count,
            "full_refreshes": self.full_refresh_count,
            "partial_refreshes": self.partial_refresh_count,
            "efficiency_ratio": self.get_efficiency_ratio(),
        }

    def reset(self) -> None:
        """Reset all statistics."""
        self.refresh_count = 0
        self.full_refresh_count = 0
        self.partial_refresh_count = 0
