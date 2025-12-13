# SPDX-License-Identifier: MIT
"""Tests for key bindings and UI behavior."""

from datetime import UTC, datetime

import pytest

from miniflux_tui.api.models import Category, Entry, Feed
from miniflux_tui.ui.screens.entry_history import EntryHistoryScreen
from miniflux_tui.ui.screens.entry_list import EntryListScreen


@pytest.fixture
def sample_entries():
    """Create sample entries for testing."""
    feed1 = Feed(
        id=1,
        title="Test Feed 1",
        site_url="https://example.com",
        feed_url="https://example.com/feed",
        category_id=1,
    )
    feed2 = Feed(
        id=2,
        title="Test Feed 2",
        site_url="https://example2.com",
        feed_url="https://example2.com/feed",
        category_id=2,
    )

    entries = []
    for i in range(10):
        entries.append(
            Entry(
                id=i,
                feed_id=1 if i < 5 else 2,
                title=f"Entry {i}",
                url=f"https://example.com/entry{i}",
                content="Test content",
                feed=feed1 if i < 5 else feed2,
                status="read" if i < 3 else "unread",
                starred=False,
                published_at=datetime(2025, 1, 1, 12, 0, i, tzinfo=UTC),
            )
        )
    return entries


@pytest.fixture
def sample_categories():
    """Create sample categories for testing."""
    return [
        Category(id=1, title="Category 1"),
        Category(id=2, title="Category 2"),
    ]


class TestEntryListKeyBindings:
    """Test key bindings for EntryListScreen."""

    def test_has_group_by_feed_binding(self, sample_entries):
        """Test that 'w' key binding exists for group by feed."""
        screen = EntryListScreen(sample_entries)

        # Check binding exists (now uses 'w' instead of 'g' since 'g' is for g-prefix mode)
        binding_keys = [b.key for b in screen.BINDINGS]  # type: ignore[attr-defined]
        assert "w" in binding_keys

        # Check it maps to correct action
        w_binding = next(b for b in screen.BINDINGS if b.key == "w")  # type: ignore[attr-defined]
        assert w_binding.action == "toggle_group_feed"  # type: ignore[attr-defined]
        assert "Group by Feed" in w_binding.description  # type: ignore[attr-defined]

    def test_has_group_by_category_binding(self, sample_entries):
        """Test that 'C' (Shift+C) key binding exists for group by category."""
        screen = EntryListScreen(sample_entries)

        # Check binding exists (now uses 'C' instead of 'c' since 'g+c' is for g-prefix mode)
        binding_keys = [b.key for b in screen.BINDINGS]  # type: ignore[attr-defined]
        assert "C" in binding_keys

        # Check it maps to correct action
        c_binding = next(b for b in screen.BINDINGS if b.key == "C")  # type: ignore[attr-defined]
        assert c_binding.action == "toggle_group_category"  # type: ignore[attr-defined]
        assert "Group by Category" in c_binding.description  # type: ignore[attr-defined]

    def test_has_history_binding(self, sample_entries):
        """Test that 'H' (Shift+H) key binding exists for history."""
        screen = EntryListScreen(sample_entries)

        # Check binding exists (should be 'H' not 'shift+h')
        binding_keys = [b.key for b in screen.BINDINGS]  # type: ignore[attr-defined]
        assert "H" in binding_keys

        # Check it maps to correct action
        h_binding = next(b for b in screen.BINDINGS if b.key == "H")  # type: ignore[attr-defined]
        assert h_binding.action == "show_history"  # type: ignore[attr-defined]
        assert "History" in h_binding.description  # type: ignore[attr-defined]

    def test_group_by_feed_respects_config(self, sample_entries, sample_categories, monkeypatch):
        """Test that enabling group by feed respects the group_collapsed config."""
        screen = EntryListScreen(sample_entries, sample_categories, group_collapsed=False)

        # Mock notify to avoid NoActiveAppError
        monkeypatch.setattr(screen, "notify", lambda *_args, **_kwargs: None)
        monkeypatch.setattr(screen, "_populate_list", lambda: None)

        # Initially not grouped, with config group_collapsed=False
        assert not screen.group_by_feed
        assert not screen.group_collapsed

        # Simulate pressing 'g' to enable grouping
        screen.action_toggle_group_feed()

        # Should be grouped, and group_collapsed should retain config value (False)
        assert screen.group_by_feed
        assert not screen.group_collapsed

        # Feed fold state should be cleared
        assert len(screen.feed_fold_state) == 0

    def test_group_by_category_respects_config(self, sample_entries, sample_categories, monkeypatch):
        """Test that enabling group by category respects the group_collapsed config."""
        screen = EntryListScreen(sample_entries, sample_categories, group_collapsed=False)

        # Mock notify to avoid NoActiveAppError
        monkeypatch.setattr(screen, "notify", lambda *_args, **_kwargs: None)
        monkeypatch.setattr(screen, "_populate_list", lambda: None)

        # Initially not grouped, with config group_collapsed=False
        assert not screen.group_by_category
        assert not screen.group_collapsed

        # Simulate pressing 'c' to enable grouping
        screen.action_toggle_group_category()

        # Should be grouped, and group_collapsed should retain config value (False)
        assert screen.group_by_category
        assert not screen.group_collapsed

        # Category fold state should be cleared
        assert len(screen.category_fold_state) == 0

    def test_group_by_feed_respects_config_when_true(self, sample_entries, sample_categories, monkeypatch):
        """Test that enabling group by feed respects group_collapsed=True config."""
        screen = EntryListScreen(sample_entries, sample_categories, group_collapsed=True)

        # Mock notify to avoid NoActiveAppError
        monkeypatch.setattr(screen, "notify", lambda *_args, **_kwargs: None)
        monkeypatch.setattr(screen, "_populate_list", lambda: None)

        # Initially not grouped, but config group_collapsed=True
        assert not screen.group_by_feed
        assert screen.group_collapsed

        # Simulate pressing 'g' to enable grouping
        screen.action_toggle_group_feed()

        # Should be grouped, and group_collapsed should retain config value (True)
        assert screen.group_by_feed
        assert screen.group_collapsed

        # Feed fold state should be cleared
        assert len(screen.feed_fold_state) == 0

    def test_group_by_category_respects_config_when_true(self, sample_entries, sample_categories, monkeypatch):
        """Test that enabling group by category respects group_collapsed=True config."""
        screen = EntryListScreen(sample_entries, sample_categories, group_collapsed=True)

        # Mock notify to avoid NoActiveAppError
        monkeypatch.setattr(screen, "notify", lambda *_args, **_kwargs: None)
        monkeypatch.setattr(screen, "_populate_list", lambda: None)

        # Initially not grouped, but config group_collapsed=True
        assert not screen.group_by_category
        assert screen.group_collapsed

        # Simulate pressing 'c' to enable grouping
        screen.action_toggle_group_category()

        # Should be grouped, and group_collapsed should retain config value (True)
        assert screen.group_by_category
        assert screen.group_collapsed

        # Category fold state should be cleared
        assert len(screen.category_fold_state) == 0

    def test_toggling_group_feed_disables_category(self, sample_entries, sample_categories, monkeypatch):
        """Test that enabling feed grouping disables category grouping."""
        screen = EntryListScreen(sample_entries, sample_categories)

        # Mock notify and populate_list to avoid app context issues
        monkeypatch.setattr(screen, "notify", lambda *_args, **_kwargs: None)
        monkeypatch.setattr(screen, "_populate_list", lambda: None)

        # Enable category grouping first
        screen.action_toggle_group_category()
        assert screen.group_by_category
        assert not screen.group_by_feed

        # Enable feed grouping
        screen.action_toggle_group_feed()

        # Category grouping should be disabled
        assert screen.group_by_feed
        assert not screen.group_by_category

    def test_toggling_group_category_disables_feed(self, sample_entries, sample_categories, monkeypatch):
        """Test that enabling category grouping disables feed grouping."""
        screen = EntryListScreen(sample_entries, sample_categories)

        # Mock notify and populate_list to avoid app context issues
        monkeypatch.setattr(screen, "notify", lambda *_args, **_kwargs: None)
        monkeypatch.setattr(screen, "_populate_list", lambda: None)

        # Enable feed grouping first
        screen.action_toggle_group_feed()
        assert screen.group_by_feed
        assert not screen.group_by_category

        # Enable category grouping
        screen.action_toggle_group_category()

        # Feed grouping should be disabled
        assert screen.group_by_category
        assert not screen.group_by_feed


class TestHistoryScreen:
    """Test history screen functionality."""

    def test_history_screen_extends_entry_list(self):
        """Test that EntryHistoryScreen properly extends EntryListScreen."""
        screen = EntryHistoryScreen()

        # Should be instance of EntryListScreen
        assert isinstance(screen, EntryListScreen)

        # Should start with empty entries
        assert screen.entries == []

    def test_history_screen_has_all_bindings(self):
        """Test that history screen inherits all key bindings."""
        screen = EntryHistoryScreen()

        # Should have all the same bindings as EntryListScreen
        binding_keys = [b.key for b in screen.BINDINGS]  # type: ignore[attr-defined]

        # Check key bindings exist (updated for new g-prefix mode)
        assert "g" in binding_keys  # g-prefix mode (for g+u, g+b, g+h, g+c, g+f, g+s)
        assert "w" in binding_keys  # Group by feed (moved from 'g')
        assert "C" in binding_keys  # Group by category (moved from 'c')
        assert "j" in binding_keys or "down" in binding_keys  # Navigation
        assert "k" in binding_keys or "up" in binding_keys  # Navigation
        assert "enter" in binding_keys  # Open entry


class TestKeyBindingNoConflicts:
    """Test that key bindings don't conflict."""

    def test_no_duplicate_visible_bindings(self, sample_entries):
        """Test that no two visible bindings use the same key."""
        screen = EntryListScreen(sample_entries)

        # Get all visible bindings (show != False)
        visible_bindings = [b for b in screen.BINDINGS if b.show]  # type: ignore[attr-defined]
        visible_keys = [b.key for b in visible_bindings]  # type: ignore[attr-defined]

        # Check for duplicates
        seen = set()
        duplicates = set()
        for key in visible_keys:
            if key in seen:
                duplicates.add(key)
            seen.add(key)

        assert len(duplicates) == 0, f"Duplicate key bindings found: {duplicates}"

    def test_h_and_shift_h_no_conflict(self, sample_entries):
        """Test that 'h' and 'H' (Shift+H) don't conflict."""
        screen = EntryListScreen(sample_entries)

        binding_keys = [b.key for b in screen.BINDINGS]  # type: ignore[attr-defined]

        # Should have 'h' for collapse
        assert "h" in binding_keys
        h_binding = next(b for b in screen.BINDINGS if b.key == "h")  # type: ignore[attr-defined]
        assert h_binding.action == "collapse_fold"  # type: ignore[attr-defined]

        # Should have 'H' for history (NOT 'shift+h')
        assert "H" in binding_keys
        shift_h_binding = next(b for b in screen.BINDINGS if b.key == "H")  # type: ignore[attr-defined]
        assert shift_h_binding.action == "show_history"  # type: ignore[attr-defined]

        # Should NOT have 'shift+h' which would conflict
        assert "shift+h" not in binding_keys
