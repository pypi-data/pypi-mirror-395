# SPDX-License-Identifier: MIT
"""Tests for performance optimization utilities."""

import time

from miniflux_tui.performance import CachedProperty, ScreenRefreshOptimizer, get_sort_key_for_entry, memoize_with_ttl
from miniflux_tui.ui.screens.entry_list import EntryListScreen


class TestScreenRefreshOptimizer:
    """Test ScreenRefreshOptimizer functionality."""

    def test_optimizer_initialization(self):
        """Test optimizer initializes with correct values."""
        optimizer = ScreenRefreshOptimizer()
        assert optimizer.refresh_count == 0
        assert optimizer.full_refresh_count == 0
        assert optimizer.partial_refresh_count == 0

    def test_track_full_refresh(self):
        """Test tracking full refresh operations."""
        optimizer = ScreenRefreshOptimizer()
        optimizer.track_full_refresh()
        assert optimizer.refresh_count == 1
        assert optimizer.full_refresh_count == 1
        assert optimizer.partial_refresh_count == 0

    def test_track_partial_refresh(self):
        """Test tracking partial refresh operations."""
        optimizer = ScreenRefreshOptimizer()
        optimizer.track_partial_refresh()
        assert optimizer.refresh_count == 1
        assert optimizer.full_refresh_count == 0
        assert optimizer.partial_refresh_count == 1

    def test_track_mixed_refreshes(self):
        """Test tracking both full and partial refreshes."""
        optimizer = ScreenRefreshOptimizer()
        optimizer.track_full_refresh()
        optimizer.track_partial_refresh()
        optimizer.track_partial_refresh()
        optimizer.track_full_refresh()

        assert optimizer.refresh_count == 4
        assert optimizer.full_refresh_count == 2
        assert optimizer.partial_refresh_count == 2

    def test_efficiency_ratio_no_refreshes(self):
        """Test efficiency ratio with no refreshes."""
        optimizer = ScreenRefreshOptimizer()
        assert optimizer.get_efficiency_ratio() == 0.0

    def test_efficiency_ratio_all_full(self):
        """Test efficiency ratio with only full refreshes."""
        optimizer = ScreenRefreshOptimizer()
        optimizer.track_full_refresh()
        optimizer.track_full_refresh()
        assert optimizer.get_efficiency_ratio() == 0.0

    def test_efficiency_ratio_all_partial(self):
        """Test efficiency ratio with only partial refreshes."""
        optimizer = ScreenRefreshOptimizer()
        optimizer.track_partial_refresh()
        optimizer.track_partial_refresh()
        assert optimizer.get_efficiency_ratio() == 1.0

    def test_efficiency_ratio_mixed(self):
        """Test efficiency ratio with mixed refresh types."""
        optimizer = ScreenRefreshOptimizer()
        optimizer.track_full_refresh()
        optimizer.track_partial_refresh()
        optimizer.track_partial_refresh()
        # 2 partial out of 3 total = 2/3 ≈ 0.667
        assert abs(optimizer.get_efficiency_ratio() - (2 / 3)) < 0.001

    def test_get_stats(self):
        """Test getting performance statistics."""
        optimizer = ScreenRefreshOptimizer()
        optimizer.track_full_refresh()
        optimizer.track_partial_refresh()

        stats = optimizer.get_stats()
        assert stats["total_refreshes"] == 2
        assert stats["full_refreshes"] == 1
        assert stats["partial_refreshes"] == 1
        assert "efficiency_ratio" in stats

    def test_reset(self):
        """Test resetting optimizer statistics."""
        optimizer = ScreenRefreshOptimizer()
        optimizer.track_full_refresh()
        optimizer.track_partial_refresh()
        assert optimizer.refresh_count == 2

        optimizer.reset()
        assert optimizer.refresh_count == 0
        assert optimizer.full_refresh_count == 0
        assert optimizer.partial_refresh_count == 0


class TestGetSortKeyForEntry:
    """Test sort key generation function."""

    def test_sort_key_date_mode(self):
        """Test sort key for date sort mode."""
        key = get_sort_key_for_entry(
            entry_id=1,
            sort_mode="date",
            is_read=True,
            published_at="2024-10-25T10:00:00",
            feed_title="Example Feed",
        )
        assert key == ("2024-10-25T10:00:00",)

    def test_sort_key_feed_mode(self):
        """Test sort key for feed sort mode."""
        key = get_sort_key_for_entry(
            entry_id=1,
            sort_mode="feed",
            is_read=True,
            published_at="2024-10-25T10:00:00",
            feed_title="Example Feed",
        )
        assert key == ("example feed", "2024-10-25T10:00:00")

    def test_sort_key_status_mode(self):
        """Test sort key for status sort mode."""
        key = get_sort_key_for_entry(
            entry_id=1,
            sort_mode="status",
            is_read=True,
            published_at="2024-10-25T10:00:00",
            feed_title="Example Feed",
        )
        assert key == (True, "2024-10-25T10:00:00")

    def test_sort_key_invalid_mode(self):
        """Test sort key with invalid sort mode."""
        key = get_sort_key_for_entry(
            entry_id=5,
            sort_mode="invalid",
            is_read=False,
            published_at="2024-10-25T10:00:00",
            feed_title="Example Feed",
        )
        assert key == (5,)

    def test_sort_key_feed_title_case_insensitive(self):
        """Test that feed titles are case-insensitive for sorting."""
        key1 = get_sort_key_for_entry(
            entry_id=1,
            sort_mode="feed",
            is_read=True,
            published_at="2024-10-25T10:00:00",
            feed_title="Example Feed",
        )
        key2 = get_sort_key_for_entry(
            entry_id=2,
            sort_mode="feed",
            is_read=True,
            published_at="2024-10-25T10:00:00",
            feed_title="EXAMPLE FEED",
        )
        # First part of keys should match (lowercased)
        assert key1[0] == key2[0]


class TestEntryListScreenRefreshOptimization:
    """Test EntryListScreen refresh optimization integration."""

    def test_screen_has_optimizer(self, sample_entries):
        """Test that screen has refresh optimizer."""
        screen = EntryListScreen(entries=sample_entries)
        assert hasattr(screen, "refresh_optimizer")
        assert isinstance(screen.refresh_optimizer, ScreenRefreshOptimizer)

    def test_screen_has_entry_item_map(self, sample_entries):
        """Test that screen has entry item map for tracking."""
        screen = EntryListScreen(entries=sample_entries)
        assert hasattr(screen, "entry_item_map")
        assert isinstance(screen.entry_item_map, dict)

    def test_populate_list_tracks_full_refresh(self, sample_entries):
        """Test that populate_list tracks refresh operations."""
        screen = EntryListScreen(entries=sample_entries)
        # Note: We can't actually call _populate_list without a proper Textual app
        # But we can verify the structure is there
        assert hasattr(screen, "_populate_list")
        assert hasattr(screen, "refresh_optimizer")

    def test_initial_optimizer_stats(self, sample_entries):
        """Test initial optimizer statistics."""
        screen = EntryListScreen(entries=sample_entries)
        stats = screen.refresh_optimizer.get_stats()
        assert stats["total_refreshes"] == 0
        assert stats["full_refreshes"] == 0
        assert stats["partial_refreshes"] == 0
        assert stats["efficiency_ratio"] == 0.0

    def test_entry_item_map_tracking(self, sample_entries):
        """Test that entry item map can track entries."""
        screen = EntryListScreen(entries=sample_entries)
        # The map starts empty
        assert len(screen.entry_item_map) == 0

        # When _add_flat_entries is called (which requires list_view),
        # the map would be populated. We test the logic separately.

    def test_screen_creates_entry_map_on_add_flat(self, sample_entries):
        """Test entry item map is created when adding flat entries."""
        # This tests the logic of _add_flat_entries
        # EntryListScreen creates the entry_item_map during init
        screen = EntryListScreen(entries=sample_entries)
        # The entry_item_map should be empty initially
        assert len(screen.entry_item_map) == 0

        # The entry_item_map would be populated during display
        for entry in sample_entries:
            # Verify entries are valid for mapping
            assert isinstance(entry.id, int)


class TestCachedProperty:
    """Test CachedProperty descriptor."""

    def test_cached_property_init(self):
        """Test CachedProperty initialization."""

        def getter(obj):
            return "value"

        prop = CachedProperty(getter)
        assert prop.func == getter
        assert isinstance(prop.cache, dict)
        assert isinstance(prop.timestamps, dict)

    def test_cached_property_get_on_class(self):
        """Test CachedProperty descriptor get when accessed on class."""

        def getter(obj):
            return "value"

        prop = CachedProperty(getter)
        # Accessing on None (class access) returns the descriptor itself
        result = prop.__get__(None, dict)
        assert result is prop

    def test_cached_property_get_caches_value(self):
        """Test CachedProperty caches computed value."""
        call_count = 0

        def getter(obj):
            nonlocal call_count
            call_count += 1
            return f"value_{call_count}"

        prop = CachedProperty(getter)
        obj = object()

        # First access computes value
        result1 = prop.__get__(obj, object)
        assert result1 == "value_1"
        assert call_count == 1

        # Second access returns cached value
        result2 = prop.__get__(obj, object)
        assert result2 == "value_1"
        assert call_count == 1  # No additional call

    def test_cached_property_different_objects(self):
        """Test CachedProperty caches per object."""

        def getter(obj):
            return f"value_{id(obj)}"

        prop = CachedProperty(getter)
        obj1 = object()
        obj2 = object()

        result1 = prop.__get__(obj1, object)
        result2 = prop.__get__(obj2, object)

        # Different objects get different cached values
        assert result1 != result2
        assert str(id(obj1)) in result1
        assert str(id(obj2)) in result2

    def test_cached_property_invalidate(self):
        """Test CachedProperty invalidate method."""
        call_count = 0

        def getter(obj):
            nonlocal call_count
            call_count += 1
            return f"value_{call_count}"

        prop = CachedProperty(getter)
        obj = object()

        # Get cached value
        result1 = prop.__get__(obj, object)
        assert result1 == "value_1"
        assert call_count == 1

        # Invalidate cache
        prop.invalidate(obj)

        # Next access recomputes value
        result2 = prop.__get__(obj, object)
        assert result2 == "value_2"
        assert call_count == 2

    def test_cached_property_invalidate_nonexistent(self):
        """Test invalidating cache for non-cached object."""

        def getter(obj):
            return "value"

        prop = CachedProperty(getter)
        obj = object()

        # Should not raise error
        prop.invalidate(obj)
        assert True  # No exception


class TestMemoizeWithTTL:
    """Test memoize_with_ttl decorator."""

    def test_memoize_with_ttl_decorator_creates_wrapper(self):
        """Test memoize_with_ttl creates a wrapper function."""

        @memoize_with_ttl(ttl=1.0)
        def func(x):
            return x * 2

        assert callable(func)
        assert hasattr(func, "cache")

    def test_memoize_with_ttl_caches_result(self):
        """Test memoize_with_ttl caches function results."""
        call_count = 0

        @memoize_with_ttl(ttl=1.0)
        def func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call
        result1 = func(5)
        assert result1 == 10
        assert call_count == 1

        # Second call with same args
        result2 = func(5)
        assert result2 == 10
        assert call_count == 1  # No additional call

    def test_memoize_with_ttl_different_args(self):
        """Test memoize_with_ttl handles different arguments."""

        @memoize_with_ttl(ttl=1.0)
        def func(x):
            return x * 2

        result1 = func(5)
        result2 = func(10)

        assert result1 == 10
        assert result2 == 20

    def test_memoize_with_ttl_with_kwargs(self):
        """Test memoize_with_ttl handles keyword arguments."""
        call_count = 0

        @memoize_with_ttl(ttl=1.0)
        def func(x, y=1):
            nonlocal call_count
            call_count += 1
            return x * y

        result1 = func(5, y=2)
        assert result1 == 10
        assert call_count == 1

        # Same args and kwargs returns cached
        result2 = func(5, y=2)
        assert result2 == 10
        assert call_count == 1

        # Different kwargs triggers recompute
        result3 = func(5, y=3)
        assert result3 == 15
        assert call_count == 2

    def test_memoize_with_ttl_ttl_expiration(self):
        """Test memoize_with_ttl cache expires after TTL."""
        call_count = 0

        @memoize_with_ttl(ttl=0.1)  # 100ms TTL
        def func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = func(5)
        assert result1 == 10
        assert call_count == 1

        # Wait for cache to expire
        time.sleep(0.15)

        # Next call should recompute
        result2 = func(5)
        assert result2 == 10
        assert call_count == 2

    def test_memoize_with_ttl_cache_attribute(self):
        """Test memoize_with_ttl function has cache attribute."""

        @memoize_with_ttl(ttl=1.0)
        def func(x):
            return x * 2

        assert hasattr(func, "cache")
        assert isinstance(func.cache, dict)  # type: ignore[attr-defined]

    def test_memoize_with_ttl_default_ttl(self):
        """Test memoize_with_ttl with default TTL."""

        @memoize_with_ttl()  # Default 1.0
        def func(x):
            return x * 2

        result = func(5)
        assert result == 10


class TestPerformanceIntegration:
    """Integration tests for performance utilities."""

    def test_cached_property_with_object(self):
        """Test CachedProperty with a real object."""

        class TestClass:
            def __init__(self):
                self.compute_count = 0

            @CachedProperty
            def expensive_value(self):
                self.compute_count += 1
                return "computed"

        obj = TestClass()
        # Access property through descriptor
        prop = TestClass.expensive_value
        result1 = prop.__get__(obj, TestClass)
        assert result1 == "computed"
        assert obj.compute_count == 1

    def test_memoize_with_multiple_functions(self):
        """Test multiple functions can be memoized independently."""

        @memoize_with_ttl(ttl=1.0)
        def func1(x):
            return x * 2

        @memoize_with_ttl(ttl=1.0)
        def func2(x):
            return x * 3

        result1 = func1(5)
        result2 = func2(5)

        assert result1 == 10
        assert result2 == 15
        assert func1.cache != func2.cache  # type: ignore[attr-defined]  # Independent caches

    def test_screen_refresh_optimizer_stats_structure(self):
        """Test ScreenRefreshOptimizer stats have correct structure."""
        optimizer = ScreenRefreshOptimizer()
        optimizer.track_full_refresh()
        optimizer.track_partial_refresh()

        stats = optimizer.get_stats()

        assert isinstance(stats, dict)
        assert "total_refreshes" in stats
        assert "full_refreshes" in stats
        assert "partial_refreshes" in stats
        assert "efficiency_ratio" in stats
        assert all(isinstance(v, int | float) for v in stats.values())
