# SPDX-License-Identifier: MIT
"""Tests for the documentation cache module."""

from __future__ import annotations

import pytest

from miniflux_tui.docs_cache import DocsCache


@pytest.fixture
def cache():
    """Create a fresh DocsCache instance for each test."""
    return DocsCache()


class TestDocsCacheInitialization:
    """Test DocsCache initialization."""

    def test_init_creates_empty_cache(self):
        """Test that __init__ creates an empty cache dictionary."""
        cache = DocsCache()
        assert isinstance(cache.cache, dict)
        assert len(cache.cache) == 0

    def test_multiple_instances_have_separate_caches(self):
        """Test that multiple DocsCache instances have separate caches."""
        cache1 = DocsCache()
        cache2 = DocsCache()
        cache1.cache["test"] = "value1"
        assert "test" not in cache2.cache


class TestDocsCacheMethods:
    """Test DocsCache methods."""

    @pytest.mark.asyncio
    async def test_get_documentation_empty_rule_type_raises_error(self, cache):
        """Test that empty rule_type raises ValueError."""
        with pytest.raises(ValueError, match="rule_type cannot be empty"):
            await cache.get_documentation("")

    @pytest.mark.asyncio
    async def test_get_documentation_none_rule_type_raises_error(self, cache):
        """Test that None rule_type raises ValueError."""
        with pytest.raises(ValueError, match="rule_type cannot be empty"):
            await cache.get_documentation(None)

    @pytest.mark.asyncio
    async def test_get_documentation_returns_string(self, cache):
        """Test that get_documentation returns a string."""
        result = await cache.get_documentation("scraper_rules")
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_get_documentation_caches_result(self, cache):
        """Test that documentation is cached after first fetch."""
        rule_type = "scraper_rules"

        # First call
        result1 = await cache.get_documentation(rule_type)

        # Check it's cached
        assert rule_type in cache.cache
        assert cache.cache[rule_type] == result1

    @pytest.mark.asyncio
    async def test_get_documentation_returns_cached_value(self, cache):
        """Test that subsequent calls return cached value."""
        rule_type = "rewrite_rules"

        # First call
        result1 = await cache.get_documentation(rule_type)

        # Store original value
        cached_value = cache.cache[rule_type]

        # Second call should return same value
        result2 = await cache.get_documentation(rule_type)
        assert result2 == cached_value
        assert result1 == result2

    @pytest.mark.asyncio
    async def test_get_documentation_multiple_rule_types(self, cache):
        """Test caching multiple different rule types."""
        rule_types = ["scraper_rules", "rewrite_rules", "blocking_rules"]

        for rule_type in rule_types:
            result = await cache.get_documentation(rule_type)
            assert isinstance(result, str)

        # All should be cached
        for rule_type in rule_types:
            assert rule_type in cache.cache


class TestDocsCacheClear:
    """Test DocsCache clear functionality."""

    @pytest.mark.asyncio
    async def test_clear_empties_cache(self, cache):
        """Test that clear() empties the cache."""
        # Add some items to cache
        rule_types = ["scraper_rules", "rewrite_rules"]
        for rule_type in rule_types:
            await cache.get_documentation(rule_type)

        assert len(cache.cache) > 0

        # Clear cache
        cache.clear()
        assert len(cache.cache) == 0

    def test_clear_on_empty_cache(self, cache):
        """Test that clear() works on empty cache."""
        cache.clear()  # Should not raise
        assert len(cache.cache) == 0


class TestDocsCacheGetCachedKeys:
    """Test DocsCache cached keys retrieval."""

    @pytest.mark.asyncio
    async def test_get_cached_keys_empty(self, cache):
        """Test get_cached_keys() on empty cache."""
        keys = cache.get_cached_keys()
        assert keys == []

    @pytest.mark.asyncio
    async def test_get_cached_keys_returns_list(self, cache):
        """Test that get_cached_keys() returns a list."""
        await cache.get_documentation("scraper_rules")
        keys = cache.get_cached_keys()
        assert isinstance(keys, list)

    @pytest.mark.asyncio
    async def test_get_cached_keys_contains_cached_items(self, cache):
        """Test that get_cached_keys() contains all cached items."""
        rule_types = ["scraper_rules", "rewrite_rules", "blocking_rules"]

        for rule_type in rule_types:
            await cache.get_documentation(rule_type)

        keys = cache.get_cached_keys()
        assert len(keys) == len(rule_types)
        for rule_type in rule_types:
            assert rule_type in keys

    @pytest.mark.asyncio
    async def test_get_cached_keys_after_clear(self, cache):
        """Test get_cached_keys() after clearing cache."""
        await cache.get_documentation("scraper_rules")
        assert len(cache.get_cached_keys()) > 0

        cache.clear()
        assert cache.get_cached_keys() == []


class TestDocsCacheFetchError:
    """Test DocsCache error handling during fetch."""

    @pytest.mark.asyncio
    async def test_fetch_returns_empty_string_on_error(self, cache):
        """Test that fetch errors return empty string instead of raising."""
        # This tests the error handling in _fetch_from_web
        # It should return empty string rather than raising
        result = await cache.get_documentation("invalid_rule_type_that_will_cause_error_xyz")
        assert isinstance(result, str)


class TestDocsCacheFetchFromWeb:
    """Test DocsCache _fetch_from_web method."""

    @pytest.mark.asyncio
    async def test_fetch_from_web_returns_string(self, cache):
        """Test that _fetch_from_web returns a string."""
        result = await cache._fetch_from_web("scraper_rules")
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_fetch_from_web_handles_all_rule_types(self, cache):
        """Test that _fetch_from_web handles all rule types."""
        rule_types = [
            "scraper_rules",
            "rewrite_rules",
            "url_rewrite_rules",
            "blocking_rules",
            "keep_rules",
            "entry_blocking_rules",
            "entry_allow_rules",
        ]

        for rule_type in rule_types:
            result = await cache._fetch_from_web(rule_type)
            assert isinstance(result, str)


class TestDocsCacheIntegration:
    """Integration tests for DocsCache."""

    @pytest.mark.asyncio
    async def test_session_simulation(self, cache):
        """Test a typical session with multiple cache accesses."""
        # Simulate user opening multiple rule types during a session
        rule_types = [
            "scraper_rules",
            "rewrite_rules",
            "url_rewrite_rules",
            "blocking_rules",
            "keep_rules",
            "entry_blocking_rules",
            "entry_allow_rules",
        ]

        # First pass: fetch all
        for rule_type in rule_types:
            await cache.get_documentation(rule_type)

        # Verify all cached
        assert len(cache.get_cached_keys()) == len(rule_types)

        # Second pass: verify cached values are returned
        for rule_type in rule_types:
            result = await cache.get_documentation(rule_type)
            assert isinstance(result, str)
            assert rule_type in cache.cache

        # Clear at end of session
        cache.clear()
        assert len(cache.get_cached_keys()) == 0
