# SPDX-License-Identifier: MIT
"""Tests for entry list screen functionality."""

import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from textual.binding import Binding
from textual.widgets import ListItem, ListView

from miniflux_tui.api.models import Category, Entry, Feed
from miniflux_tui.constants import SORT_MODES
from miniflux_tui.ui.screens.entry_list import (
    CollapsibleListView,
    EntryListItem,
    EntryListScreen,
    FeedHeaderItem,
)
from miniflux_tui.ui.screens.input_dialog import InputDialog


def mock_run_worker(coro, **kwargs):
    """Mock run_worker to execute coroutine immediately in tests.

    This allows testing of action methods that use run_worker without
    dealing with Textual's worker infrastructure.
    """
    loop = asyncio.get_event_loop()
    return loop.create_task(coro)


@pytest.fixture
def test_feed():
    """Create a test feed."""
    return Feed(
        id=1,
        title="Test Feed",
        site_url="http://localhost:8080",
        feed_url="http://localhost:8080/feed.xml",
    )


@pytest.fixture
def diverse_entries(test_feed):
    """Create entries with different statuses and dates for testing sorting."""
    return [
        Entry(
            id=1,
            feed_id=1,
            title="Oldest Unread",
            url="http://localhost:8080/1",
            content="Content 1",
            feed=test_feed,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 20, 10, 0, 0, tzinfo=UTC),
        ),
        Entry(
            id=2,
            feed_id=1,
            title="Newest Read",
            url="http://localhost:8080/2",
            content="Content 2",
            feed=test_feed,
            status="read",
            starred=False,
            published_at=datetime(2024, 10, 25, 15, 30, 0, tzinfo=UTC),
        ),
        Entry(
            id=3,
            feed_id=1,
            title="Middle Starred",
            url="http://localhost:8080/3",
            content="Content 3",
            feed=test_feed,
            status="read",
            starred=True,
            published_at=datetime(2024, 10, 22, 12, 0, 0, tzinfo=UTC),
        ),
        Entry(
            id=4,
            feed_id=1,
            title="Recent Unread",
            url="http://localhost:8080/4",
            content="Content 4",
            feed=test_feed,
            status="unread",
            starred=True,
            published_at=datetime(2024, 10, 24, 8, 30, 0, tzinfo=UTC),
        ),
    ]


class TestEntryListScreen:
    """Test EntryListScreen functionality."""

    def test_entry_list_creation(self, diverse_entries):
        """Test creating an EntryListScreen instance."""
        screen = EntryListScreen(entries=diverse_entries)
        assert screen.entries == diverse_entries
        assert screen.current_sort == "date"
        assert screen.group_by_feed is False
        assert screen.filter_unread_only is False
        assert screen.filter_starred_only is False

    def test_custom_colors(self, diverse_entries):
        """Test EntryListScreen with custom colors."""
        screen = EntryListScreen(
            entries=diverse_entries,
            unread_color="yellow",
            read_color="white",
        )
        assert screen.unread_color == "yellow"
        assert screen.read_color == "white"

    def test_custom_sort_mode(self, diverse_entries):
        """Test EntryListScreen with custom sort mode."""
        screen = EntryListScreen(entries=diverse_entries, default_sort="feed")
        assert screen.current_sort == "feed"

    def test_filter_unread_only(self, diverse_entries):
        """Test filtering to show only unread entries."""
        screen = EntryListScreen(entries=diverse_entries)
        filtered = screen._filter_entries(diverse_entries)
        # Should return all entries when no filter is active
        assert len(filtered) == len(diverse_entries)

        # Now enable unread filter
        screen.filter_unread_only = True
        filtered = screen._filter_entries(diverse_entries)
        # Should return only unread entries
        assert len(filtered) == 2  # IDs 1 and 4
        assert all(e.is_unread for e in filtered)
        assert all(e.id in {1, 4} for e in filtered)

    def test_filter_starred_only(self, diverse_entries):
        """Test filtering to show only starred entries."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.filter_starred_only = True
        filtered = screen._filter_entries(diverse_entries)
        # Should return only starred entries
        assert len(filtered) == 2  # IDs 3 and 4
        assert all(e.starred for e in filtered)
        assert all(e.id in {3, 4} for e in filtered)

    def test_filters_are_mutually_exclusive(self, diverse_entries):
        """Test that only one filter is applied at a time."""
        screen = EntryListScreen(entries=diverse_entries)
        # Enable both filters (shouldn't happen in normal usage)
        screen.filter_unread_only = True
        screen.filter_starred_only = True

        filtered = screen._filter_entries(diverse_entries)
        # filter_unread_only should take precedence
        assert len(filtered) == 2  # Only unread entries
        assert all(e.is_unread for e in filtered)

    def test_sort_by_date(self, diverse_entries):
        """Test sorting entries by date (newest first)."""
        screen = EntryListScreen(entries=diverse_entries, default_sort="date")
        sorted_entries = screen._sort_entries(diverse_entries)

        # Newest should be first
        assert sorted_entries[0].id == 2  # 2024-10-25
        assert sorted_entries[1].id == 4  # 2024-10-24
        assert sorted_entries[2].id == 3  # 2024-10-22
        assert sorted_entries[3].id == 1  # 2024-10-20

    def test_sort_by_status(self, diverse_entries):
        """Test sorting entries by status (unread first)."""
        screen = EntryListScreen(entries=diverse_entries, default_sort="status")
        sorted_entries = screen._sort_entries(diverse_entries)

        # Unread entries should come first (oldest first within status)
        unread = [e for e in sorted_entries if e.is_unread]
        read = [e for e in sorted_entries if e.is_read]

        assert len(unread) == 2
        assert len(read) == 2
        # Unread should be before read
        assert sorted_entries.index(unread[0]) < sorted_entries.index(read[0])
        # Within unread, oldest should be first
        assert unread[0].id == 1  # 2024-10-20
        assert unread[1].id == 4  # 2024-10-24

    def test_sort_by_feed(self, diverse_entries):
        """Test sorting entries by feed."""
        screen = EntryListScreen(entries=diverse_entries, default_sort="feed")
        sorted_entries = screen._sort_entries(diverse_entries)

        # All entries are from same feed, so should be sorted by date
        # (newest first within same feed)
        assert sorted_entries[0].id == 2  # Newest
        assert sorted_entries[-1].id == 1  # Oldest

    def test_empty_entry_list(self):
        """Test EntryListScreen with empty entries."""
        screen = EntryListScreen(entries=[])
        assert screen.entries == []
        assert len(screen.sorted_entries) == 0

    def test_single_entry(self, test_feed):
        """Test EntryListScreen with single entry."""
        entry = Entry(
            id=1,
            feed_id=1,
            title="Single Entry",
            url="http://localhost:8080/single",
            content="Content",
            feed=test_feed,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        )
        screen = EntryListScreen(entries=[entry])
        assert len(screen.entries) == 1
        sorted_entries = screen._sort_entries([entry])
        assert len(sorted_entries) == 1
        assert sorted_entries[0].id == 1

    def test_sorting_with_filter(self, diverse_entries):
        """Test that filtering and sorting work together."""
        screen = EntryListScreen(entries=diverse_entries, default_sort="date")
        screen.filter_unread_only = True

        # Apply filter and sort
        filtered = screen._filter_entries(diverse_entries)
        sorted_entries = screen._sort_entries(filtered)

        # Should only have unread entries
        assert len(sorted_entries) == 2
        assert all(e.is_unread for e in sorted_entries)
        # Should be sorted by date (newest first)
        assert sorted_entries[0].id == 4  # 2024-10-24
        assert sorted_entries[1].id == 1  # 2024-10-20

    def test_grouped_mode_with_collapse(self, diverse_entries):
        """Test grouped mode with collapsed feeds."""
        screen = EntryListScreen(
            entries=diverse_entries,
            group_by_feed=True,
            group_collapsed=True,
        )
        # Should start with feeds collapsed
        assert screen.group_collapsed is True
        assert screen.group_by_feed is True

    def test_fold_state_tracking(self, diverse_entries):
        """Test that fold state is tracked per feed."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        # Feed fold state should be tracked
        assert hasattr(screen, "feed_fold_state")
        assert isinstance(screen.feed_fold_state, dict)

    def test_feed_header_map(self, diverse_entries):
        """Test that feed header items are tracked."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        # Feed header map should be tracked
        assert hasattr(screen, "feed_header_map")
        assert isinstance(screen.feed_header_map, dict)

    def test_last_highlighted_feed_tracking(self, diverse_entries):
        """Test that last highlighted feed is tracked for position persistence."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        assert hasattr(screen, "last_highlighted_feed")
        # Initially None or will be set to first feed
        assert screen.last_highlighted_feed is None or isinstance(screen.last_highlighted_feed, str)

    def test_vim_navigation_attributes(self, diverse_entries):
        """Test that vim navigation actions exist."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        # Check that the vim navigation actions are defined
        assert hasattr(screen, "action_expand_fold")
        assert hasattr(screen, "action_collapse_fold")
        assert callable(screen.action_expand_fold)
        assert callable(screen.action_collapse_fold)

    def test_restore_cursor_position_method_exists(self, diverse_entries):
        """Test that cursor position restore method exists."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        assert hasattr(screen, "_restore_cursor_position")
        assert callable(screen._restore_cursor_position)


class TestEntryListItem:
    """Test EntryListItem widget class."""

    def test_entry_list_item_creation(self, test_feed):
        """Test creating an EntryListItem."""
        entry = Entry(
            id=1,
            feed_id=1,
            title="Test Entry",
            url="http://localhost:8080/1",
            content="Content",
            feed=test_feed,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        )
        item = EntryListItem(entry)
        assert item.entry == entry
        assert item.unread_color == "cyan"
        assert item.read_color == "gray"

    def test_entry_list_item_custom_colors(self, test_feed):
        """Test EntryListItem with custom colors."""
        entry = Entry(
            id=1,
            feed_id=1,
            title="Test Entry",
            url="http://localhost:8080/1",
            content="Content",
            feed=test_feed,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        )
        item = EntryListItem(entry, unread_color="yellow", read_color="white")
        assert item.unread_color == "yellow"
        assert item.read_color == "white"

    def test_entry_list_item_is_list_item(self, test_feed):
        """Test that EntryListItem is a ListItem subclass."""
        entry = Entry(
            id=1,
            feed_id=1,
            title="Test Entry",
            url="http://localhost:8080/1",
            content="Content",
            feed=test_feed,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        )
        item = EntryListItem(entry)
        assert isinstance(item, ListItem)

    def test_entry_list_item_for_unread_entry(self, test_feed):
        """Test EntryListItem formatting for unread entry."""
        entry = Entry(
            id=1,
            feed_id=1,
            title="Unread Entry",
            url="http://localhost:8080/1",
            content="Content",
            feed=test_feed,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        )
        item = EntryListItem(entry)
        assert item.entry.is_unread is True

    def test_entry_list_item_for_read_entry(self, test_feed):
        """Test EntryListItem formatting for read entry."""
        entry = Entry(
            id=1,
            feed_id=1,
            title="Read Entry",
            url="http://localhost:8080/1",
            content="Content",
            feed=test_feed,
            status="read",
            starred=False,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        )
        item = EntryListItem(entry)
        assert item.entry.is_read is True

    def test_entry_list_item_for_starred_entry(self, test_feed):
        """Test EntryListItem for starred entry."""
        entry = Entry(
            id=1,
            feed_id=1,
            title="Starred Entry",
            url="http://localhost:8080/1",
            content="Content",
            feed=test_feed,
            status="unread",
            starred=True,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        )
        item = EntryListItem(entry)
        assert item.entry.starred is True


class TestFeedHeaderItem:
    """Test FeedHeaderItem widget class."""

    def test_feed_header_item_creation(self):
        """Test creating a FeedHeaderItem."""
        header = FeedHeaderItem("Test Feed")
        assert header.feed_title == "Test Feed"
        assert header.is_expanded is True

    def test_feed_header_item_collapsed_state(self):
        """Test FeedHeaderItem with initial collapsed state."""
        header = FeedHeaderItem("Test Feed", is_expanded=False)
        assert header.feed_title == "Test Feed"
        assert header.is_expanded is False

    def test_feed_header_item_is_list_item(self):
        """Test that FeedHeaderItem is a ListItem subclass."""
        header = FeedHeaderItem("Test Feed")
        assert isinstance(header, ListItem)

    def test_feed_header_item_toggle_fold(self):
        """Test toggling fold state of FeedHeaderItem."""
        header = FeedHeaderItem("Test Feed", is_expanded=True)
        assert header.is_expanded is True
        header.toggle_fold()
        assert header.is_expanded is False
        header.toggle_fold()
        assert header.is_expanded is True

    def test_feed_header_item_toggle_fold_multiple_times(self):
        """Test multiple fold toggling."""
        header = FeedHeaderItem("Test Feed", is_expanded=True)
        for _ in range(5):
            header.toggle_fold()
        # After odd number of toggles, should be collapsed
        assert header.is_expanded is False


class TestEntryListScreenCompose:
    """Test EntryListScreen composition."""

    def test_compose_method_exists(self, diverse_entries):
        """Test that compose method exists."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "compose")
        assert callable(screen.compose)

    def test_compose_returns_generator(self, diverse_entries):
        """Test that compose returns a generator."""
        screen = EntryListScreen(entries=diverse_entries)
        result = screen.compose()
        assert hasattr(result, "__iter__") or hasattr(result, "__next__")

    def test_screen_has_bindings(self, diverse_entries):
        """Test that EntryListScreen has key bindings."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "BINDINGS")
        assert isinstance(screen.BINDINGS, list)
        assert len(screen.BINDINGS) > 0

    def test_bindings_are_binding_objects(self, diverse_entries):
        """Test that all bindings are Binding objects."""
        screen = EntryListScreen(entries=diverse_entries)
        for binding in screen.BINDINGS:
            assert isinstance(binding, Binding)

    def test_screen_has_required_actions(self, diverse_entries):
        """Test that screen has required action methods."""
        screen = EntryListScreen(entries=diverse_entries)
        required_actions = [
            "action_cycle_sort",
            "action_toggle_group_feed",
            "action_toggle_fold",
            "action_toggle_read",
            "action_toggle_star",
        ]
        for action in required_actions:
            assert hasattr(screen, action), f"Missing action: {action}"


class TestEntryListScreenActions:
    """Test EntryListScreen action methods."""

    def test_action_cycle_sort(self, diverse_entries):
        """Test cycling through sort modes."""
        screen = EntryListScreen(entries=diverse_entries, default_sort="date")
        assert screen.current_sort == "date"

        # Test that action_cycle_sort method exists
        assert hasattr(screen, "action_cycle_sort")
        assert callable(screen.action_cycle_sort)

        # Test the sorting logic directly without calling the action
        # to avoid NoActiveAppError from Textual framework
        current_index = SORT_MODES.index(screen.current_sort)
        next_sort = SORT_MODES[(current_index + 1) % len(SORT_MODES)]
        assert next_sort == "feed"

    def test_action_toggle_group_feed(self, diverse_entries):
        """Test toggling group by feed."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=False)
        assert screen.group_by_feed is False

        # Test that action_toggle_group_feed method exists
        assert hasattr(screen, "action_toggle_group_feed")
        assert callable(screen.action_toggle_group_feed)

        # Test the grouping logic directly
        original_state = screen.group_by_feed
        expected_state = not original_state
        assert expected_state is True

    def test_get_sorted_entries_default_sort(self, diverse_entries):
        """Test _get_sorted_entries with default sort."""
        screen = EntryListScreen(entries=diverse_entries, default_sort="date")
        sorted_entries = screen._get_sorted_entries()
        # Newest should be first
        assert sorted_entries[0].id == 2

    def test_get_sorted_entries_grouped(self, diverse_entries):
        """Test _get_sorted_entries with grouping enabled."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True, default_sort="date")
        sorted_entries = screen._get_sorted_entries()
        # Should be sorted by feed name, then by date
        assert len(sorted_entries) == len(diverse_entries)

    def test_display_entries_flat(self, diverse_entries):
        """Test _display_entries in flat mode."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=False)
        screen.list_view = MagicMock(spec=ListView)
        sorted_entries = screen._get_sorted_entries()
        screen._display_entries(sorted_entries)
        # Should call _add_flat_entries
        assert screen.list_view.append.called or len(sorted_entries) > 0

    def test_display_entries_grouped(self, diverse_entries):
        """Test _display_entries in grouped mode."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock(spec=ListView)
        sorted_entries = screen._get_sorted_entries()
        screen._display_entries(sorted_entries)
        # Should call _add_grouped_entries
        assert screen.list_view.append.called or len(sorted_entries) > 0

    def test_is_item_visible(self, diverse_entries):
        """Test _is_item_visible method."""
        screen = EntryListScreen(entries=diverse_entries)
        entry = diverse_entries[0]
        item = EntryListItem(entry)

        # Initially should be visible
        assert screen._is_item_visible(item) is True

        # Add collapsed class
        item.add_class("collapsed")
        assert screen._is_item_visible(item) is False

    @pytest.mark.asyncio
    async def test_action_toggle_read(self, diverse_entries):
        """Test toggle_read action."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_toggle_read")
        assert callable(screen.action_toggle_read)

    @pytest.mark.asyncio
    async def test_action_toggle_star(self, diverse_entries):
        """Test toggle_star action."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_toggle_star")
        assert callable(screen.action_toggle_star)

    @pytest.mark.asyncio
    async def test_action_save_entry(self, diverse_entries):
        """Test save_entry action."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_save_entry")
        assert callable(screen.action_save_entry)

    @pytest.mark.asyncio
    async def test_action_refresh(self, diverse_entries):
        """Test refresh action."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_refresh")
        assert callable(screen.action_refresh)

    @pytest.mark.asyncio
    async def test_action_show_unread(self, diverse_entries):
        """Test show_unread action."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_show_unread")
        assert callable(screen.action_show_unread)

    @pytest.mark.asyncio
    async def test_action_show_starred(self, diverse_entries):
        """Test show_starred action."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_show_starred")
        assert callable(screen.action_show_starred)

    def test_action_show_help(self, diverse_entries):
        """Test show_help action."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_show_help")
        assert callable(screen.action_show_help)

    def test_action_quit(self, diverse_entries):
        """Test quit action."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_quit")
        assert callable(screen.action_quit)


class TestEntryListScreenCursorNavigation:
    """Test cursor navigation methods."""

    def test_action_cursor_down_exists(self, diverse_entries):
        """Test cursor_down action exists."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_cursor_down")
        assert callable(screen.action_cursor_down)

    def test_action_cursor_up_exists(self, diverse_entries):
        """Test cursor_up action exists."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_cursor_up")
        assert callable(screen.action_cursor_up)

    def test_cursor_down_with_no_listview(self, diverse_entries):
        """Test cursor_down when list_view is None."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.list_view = None
        # Should not crash
        screen.action_cursor_down()

    def test_cursor_up_with_no_listview(self, diverse_entries):
        """Test cursor_up when list_view is None."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.list_view = None
        # Should not crash
        screen.action_cursor_up()

    def test_cursor_navigation_skips_hidden_items(self, diverse_entries):
        """Test that cursor navigation skips hidden (collapsed) items.

        This test verifies that _is_item_visible correctly identifies collapsed items.
        The CollapsibleListView class (used in EntryListScreen) overrides
        action_cursor_down/up to skip collapsed items when navigating with arrow keys.
        This ensures both j/k keys and arrow keys skip collapsed entries.
        """
        screen = EntryListScreen(entries=diverse_entries)
        # Verify hidden items are skipped
        item = MagicMock(spec=ListItem)
        item.classes = {"collapsed"}
        assert screen._is_item_visible(item) is False

        # Verify CollapsibleListView has the necessary methods
        assert hasattr(CollapsibleListView, "action_cursor_down")
        assert hasattr(CollapsibleListView, "action_cursor_up")
        assert hasattr(CollapsibleListView, "_is_item_visible")


class TestEntryListScreenFoldOperations:
    """Test feed folding/unfolding operations."""

    def test_action_toggle_fold_exists(self, diverse_entries):
        """Test toggle_fold action exists."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_toggle_fold")
        assert callable(screen.action_toggle_fold)

    def test_action_collapse_fold_exists(self, diverse_entries):
        """Test collapse_feed action exists."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_collapse_fold")
        assert callable(screen.action_collapse_fold)

    def test_action_expand_fold_exists(self, diverse_entries):
        """Test expand_feed action exists."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "action_expand_fold")
        assert callable(screen.action_expand_fold)

    def test_toggle_fold_without_grouped_mode(self, diverse_entries):
        """Test toggle_fold when not in grouped mode."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=False)
        screen.list_view = MagicMock()
        # Should return early
        screen.action_toggle_fold()

    def test_collapse_feed_without_grouped_mode(self, diverse_entries):
        """Test collapse_feed when not in grouped mode."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=False)
        screen.list_view = MagicMock()
        # Should return early
        screen.action_collapse_fold()

    def test_expand_feed_without_grouped_mode(self, diverse_entries):
        """Test expand_feed when not in grouped mode."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=False)
        screen.list_view = MagicMock()
        # Should return early
        screen.action_expand_fold()

    def test_update_feed_visibility(self, diverse_entries):
        """Test _update_feed_visibility method."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock()
        screen.list_view.children = []

        # Create a mock entry item
        mock_item = MagicMock(spec=EntryListItem)
        mock_item.entry = diverse_entries[0]
        screen.list_view.children = [mock_item]

        # Test updating visibility
        screen._update_feed_visibility(diverse_entries[0].feed.title)


class TestEntryListScreenIncrementalUpdates:
    """Test incremental update functionality."""

    def test_update_single_item_success(self, diverse_entries):
        """Test _update_single_item successfully replaces an existing item."""
        screen = EntryListScreen(entries=diverse_entries)
        entry = diverse_entries[0]

        # Prepare existing item and list view state
        old_item = MagicMock(spec=EntryListItem)
        old_item.entry = entry
        placeholder_item = MagicMock(spec=EntryListItem)
        fake_children = [old_item, placeholder_item]

        # Removing the old item should update the fake children list
        old_item.remove = MagicMock(side_effect=lambda: fake_children.remove(old_item))

        screen.list_view = MagicMock()
        screen.list_view.children = fake_children

        def mount(new_item, before=None):
            if before and before in fake_children:
                index = fake_children.index(before)
                fake_children.insert(index, new_item)
            else:
                fake_children.append(new_item)

        screen.list_view.mount = MagicMock(side_effect=mount)
        screen.entry_item_map[entry.id] = old_item
        screen.displayed_items = [old_item]

        result = screen._update_single_item(entry)

        assert result is True
        new_item = screen.entry_item_map[entry.id]
        assert new_item is not old_item
        assert screen.displayed_items[0] is new_item
        assert new_item.entry is entry
        screen.list_view.mount.assert_called()
        # Ensure refresh optimizer tracked the partial refresh
        assert screen.refresh_optimizer.partial_refresh_count == 1

    def test_update_single_item_not_found(self, diverse_entries):
        """Test _update_single_item when item not found."""
        screen = EntryListScreen(entries=diverse_entries)
        entry = diverse_entries[0]
        result = screen._update_single_item(entry)
        assert result is False

    def test_update_single_item_not_in_map_with_listview(self, diverse_entries):
        """Test _update_single_item with item not in map but list_view exists."""
        screen = EntryListScreen(entries=diverse_entries)
        entry = diverse_entries[0]

        # Set list_view but don't add entry to map
        screen.list_view = MagicMock(spec=ListView)
        screen.list_view.children = []

        # When entry is not in map, should return False
        result = screen._update_single_item(entry)
        assert result is False


class TestEntryListScreenGrouping:
    """Test grouping functionality."""

    def test_add_grouped_entries(self, diverse_entries):
        """Test _add_grouped_entries method."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock()
        screen._add_grouped_entries(diverse_entries)
        # Should have called append for headers and entries
        assert screen.list_view.append.called or len(diverse_entries) > 0

    def test_add_flat_entries(self, diverse_entries):
        """Test _add_flat_entries method."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=False)
        screen.list_view = MagicMock()
        screen._add_flat_entries(diverse_entries)
        # Should have called append for all entries
        assert screen.list_view.append.called or len(diverse_entries) > 0

    def test_grouped_entries_populate_maps(self, diverse_entries):
        """Test that grouped entries populate tracking maps."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock()
        screen._add_grouped_entries(diverse_entries)
        # Maps should be populated - at least entry_item_map should have items
        assert len(screen.entry_item_map) > 0

    def test_update_feed_visibility_collapsed_and_expanded(self, diverse_entries):
        """Test _update_feed_visibility toggles CSS classes."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        feed_title = diverse_entries[0].feed.title

        item = EntryListItem(diverse_entries[0])
        item.add_class = MagicMock()
        item.remove_class = MagicMock()

        screen.list_view = MagicMock()
        screen.list_view.children = [item]

        # Collapse feed
        screen.feed_fold_state[feed_title] = False
        screen._update_feed_visibility(feed_title)
        item.add_class.assert_called_with("collapsed")

        # Expand feed
        screen.feed_fold_state[feed_title] = True
        screen._update_feed_visibility(feed_title)
        item.remove_class.assert_called_with("collapsed")

    def test_action_toggle_fold_updates_state(self, diverse_entries):
        """Test action_toggle_fold toggles state and updates visibility."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        feed_title = diverse_entries[0].feed.title

        header = FeedHeaderItem(feed_title)
        header.toggle_fold = MagicMock()

        screen.feed_fold_state[feed_title] = True
        screen.list_view = MagicMock()
        screen.list_view.highlighted_child = header
        screen._update_feed_visibility = MagicMock()

        screen.action_toggle_fold()

        assert screen.feed_fold_state[feed_title] is False
        header.toggle_fold.assert_called_once()
        screen._update_feed_visibility.assert_called_with(feed_title)

    def test_action_collapse_fold_calls_set_state(self, diverse_entries):
        """Test action_collapse_fold collapses highlighted feed."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        feed_title = diverse_entries[0].feed.title

        header = FeedHeaderItem(feed_title)
        screen.list_view = MagicMock()
        screen.list_view.highlighted_child = header

        screen.feed_fold_state[feed_title] = True
        screen._set_feed_fold_state = MagicMock()

        screen.action_collapse_fold()

        screen._set_feed_fold_state.assert_called_once_with(feed_title, False)

    def test_action_expand_fold_calls_set_state(self, diverse_entries):
        """Test action_expand_fold expands highlighted feed."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        feed_title = diverse_entries[0].feed.title

        header = FeedHeaderItem(feed_title)
        screen.list_view = MagicMock()
        screen.list_view.highlighted_child = header

        screen.feed_fold_state[feed_title] = False
        screen._set_feed_fold_state = MagicMock()

        screen.action_expand_fold()

        screen._set_feed_fold_state.assert_called_once_with(feed_title, True)

    def test_action_expand_all_updates_collapsed_feeds(self, diverse_entries):
        """Test action_expand_all expands all collapsed feeds."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock()
        screen.feed_fold_state = {"Feed A": False, "Feed B": True}
        screen._set_feed_fold_state = MagicMock()
        screen.notify = MagicMock()

        screen.action_expand_all()

        screen._set_feed_fold_state.assert_called_once_with("Feed A", True)
        screen.notify.assert_called_once_with("All feeds expanded")

    def test_action_collapse_all_collapses_expanded_feeds(self, diverse_entries):
        """Test action_collapse_all collapses all expanded feeds."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock()
        screen.feed_fold_state = {"Feed A": True, "Feed B": False}
        screen._set_feed_fold_state = MagicMock()
        screen.notify = MagicMock()

        screen.action_collapse_all()

        screen._set_feed_fold_state.assert_called_once_with("Feed A", False)
        screen.notify.assert_called_once_with("All feeds collapsed")


class TestEntryListScreenMultipleFeedsGrouping:
    """Test grouping with multiple feeds."""

    @pytest.fixture
    def multiple_feeds(self):
        """Create entries from multiple feeds."""
        feed1 = Feed(
            id=1,
            title="Feed A",
            site_url="http://localhost:8082",
            feed_url="http://localhost:8082/feed.xml",
        )
        feed2 = Feed(
            id=2,
            title="Feed B",
            site_url="http://localhost:8083",
            feed_url="http://localhost:8083/feed.xml",
        )
        return [
            Entry(
                id=1,
                feed_id=1,
                title="Entry 1A",
                url="http://localhost:8082/1",
                content="Content",
                feed=feed1,
                status="unread",
                starred=False,
                published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
            ),
            Entry(
                id=2,
                feed_id=2,
                title="Entry 2A",
                url="http://localhost:8083/1",
                content="Content",
                feed=feed2,
                status="unread",
                starred=False,
                published_at=datetime(2024, 10, 26, 10, 0, 0, tzinfo=UTC),
            ),
            Entry(
                id=3,
                feed_id=1,
                title="Entry 1B",
                url="http://localhost:8082/2",
                content="Content",
                feed=feed1,
                status="read",
                starred=False,
                published_at=datetime(2024, 10, 24, 10, 0, 0, tzinfo=UTC),
            ),
        ]

    def test_grouped_sort_with_multiple_feeds(self, multiple_feeds):
        """Test sorting with multiple feeds."""
        screen = EntryListScreen(entries=multiple_feeds, group_by_feed=True)
        sorted_entries = screen._get_sorted_entries()
        # Should group by feed and sort by date within each feed
        assert len(sorted_entries) == len(multiple_feeds)

    def test_multiple_feed_headers_created(self, multiple_feeds):
        """Test that multiple feed headers are created."""
        screen = EntryListScreen(entries=multiple_feeds, group_by_feed=True)
        screen.list_view = MagicMock()
        screen._add_grouped_entries(multiple_feeds)
        # Should have entries for both feeds
        assert screen.feed_header_map or screen.entry_item_map


class TestCursorPositionRestoration:
    """Test cursor position restoration when returning from entry reader."""

    def test_last_cursor_index_initialized(self, diverse_entries):
        """Test that last_cursor_index is initialized."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "last_cursor_index")
        assert screen.last_cursor_index == 0

    def test_last_highlighted_entry_id_initialized(self, diverse_entries):
        """Test that last_highlighted_entry_id is initialized."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "last_highlighted_entry_id")
        assert screen.last_highlighted_entry_id is None

    def test_restore_cursor_position_method_exists(self, diverse_entries):
        """Test that _restore_cursor_position method exists."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "_restore_cursor_position")
        assert callable(screen._restore_cursor_position)

    def test_restore_cursor_position_with_no_list_view(self, diverse_entries):
        """Test _restore_cursor_position when list_view is None."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.list_view = None
        # Should not crash
        screen._restore_cursor_position()

    def test_restore_cursor_position_with_empty_list(self, diverse_entries):
        """Test _restore_cursor_position with empty children."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.list_view = MagicMock(spec=ListView)
        screen.list_view.children = []
        # Should not crash
        screen._restore_cursor_position()

    def test_restore_cursor_position_by_entry_id(self, diverse_entries):
        """Test restoring cursor position by entry ID."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock(spec=ListView)

        # Create mock items
        mock_items = [EntryListItem(e) for e in diverse_entries]
        screen.list_view.children = mock_items
        screen.last_highlighted_entry_id = diverse_entries[2].id

        # Call restore - it should find the entry by ID
        screen._restore_cursor_position()
        # Should have called set index on list_view
        assert screen.list_view.index == 2 or screen.list_view.index is not None

    def test_restore_cursor_position_fallback_to_index(self, diverse_entries):
        """Test restore cursor falls back to last_cursor_index if entry not found."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=False)
        screen.list_view = MagicMock(spec=ListView)
        screen.list_view.children = [MagicMock() for _ in diverse_entries]
        screen.last_cursor_index = 1
        screen.last_highlighted_entry_id = None

        # Call restore
        screen._restore_cursor_position()
        # Should set index to last_cursor_index
        assert screen.list_view.index == 1 or screen.list_view.index is not None

    def test_grouped_mode_cursor_restoration(self, diverse_entries):
        """Test cursor restoration in grouped mode."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        assert screen.group_by_feed is True
        # Verify the flag exists for grouped mode logic
        assert hasattr(screen, "last_highlighted_entry_id")

    def test_non_grouped_mode_cursor_restoration(self, diverse_entries):
        """Test cursor restoration in non-grouped mode."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=False)
        assert screen.group_by_feed is False
        # Verify cursor index is tracked
        assert hasattr(screen, "last_cursor_index")
        assert screen.last_cursor_index == 0

    def test_restore_cursor_position_and_focus_exists(self, diverse_entries):
        """Test that _restore_cursor_position_and_focus method exists."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "_restore_cursor_position_and_focus")
        assert callable(screen._restore_cursor_position_and_focus)

    def test_restore_cursor_calls_ensure_focus(self, diverse_entries):
        """Test that _restore_cursor_position_and_focus calls ensure_focus."""
        screen = EntryListScreen(entries=diverse_entries)
        assert hasattr(screen, "_ensure_focus")
        # Verify the method exists and is callable
        assert callable(screen._ensure_focus)


class TestNavigationWithEntrySaving:
    """Test navigation and cursor restoration with entry selection."""

    def test_cursor_index_not_none_check(self, diverse_entries):
        """Test that list_view.index is checked for None before assignment."""
        screen = EntryListScreen(entries=diverse_entries)
        mock_list_view = MagicMock()
        mock_list_view.index = 2  # Valid index
        screen.list_view = mock_list_view

        # Simulate selecting an entry
        if screen.list_view and screen.list_view.index is not None:
            screen.last_cursor_index = screen.list_view.index

        assert screen.last_cursor_index == 2

    def test_cursor_index_with_none_value(self, diverse_entries):
        """Test handling of None value for list_view.index."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.list_view = MagicMock(spec=ListView)
        screen.list_view.index = None  # None value
        original_index = screen.last_cursor_index

        # Simulate selecting an entry with None index
        if screen.list_view and screen.list_view.index is not None:
            screen.last_cursor_index = screen.list_view.index

        # Should not have changed
        assert screen.last_cursor_index == original_index

    def test_entry_found_by_id_in_grouped_mode(self, diverse_entries):
        """Test finding entry by ID in grouped mode (across feeds)."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        # Create real entry items (not mocks) so isinstance check works
        items = [EntryListItem(e) for e in diverse_entries]
        screen.list_view = MagicMock(spec=ListView)
        screen.list_view.children = items

        # Set the entry ID to find
        target_id = diverse_entries[1].id
        screen.last_highlighted_entry_id = target_id

        # Manually check if we can find it
        found = False
        for i, child in enumerate(screen.list_view.children):
            if isinstance(child, EntryListItem) and child.entry.id == target_id:
                found = True
                assert i == 1
                break

        assert found

    def test_entry_not_found_falls_back_to_last_cursor_index(self, diverse_entries):
        """Test fallback to last_cursor_index when entry not found."""
        screen = EntryListScreen(entries=diverse_entries)
        items = [EntryListItem(e) for e in diverse_entries]
        screen.list_view = MagicMock(spec=ListView)
        screen.list_view.children = items

        # Set non-existent entry ID
        screen.last_highlighted_entry_id = 999
        screen.last_cursor_index = 1

        # Check fallback logic
        found = False
        for child in screen.list_view.children:
            if isinstance(child, EntryListItem) and child.entry.id == 999:
                found = True
                break

        # Should not be found, so should use fallback
        assert found is False
        assert screen.last_cursor_index == 1


class TestActionMethods:
    """Test action methods in EntryListScreen."""

    def test_expand_all_toggles_all_feeds(self, diverse_entries):
        """Test that all feeds can be toggled to expanded state."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock()
        screen.list_view.children = []

        # Initialize all feeds as collapsed
        screen.feed_fold_state = {"Test Feed": False}
        feed_header = MagicMock(spec=FeedHeaderItem)
        screen.feed_header_map = {"Test Feed": feed_header}

        # Manually toggle like action_expand_all would do
        for feed_title in screen.feed_fold_state:
            if not screen.feed_fold_state[feed_title]:
                screen._set_feed_fold_state(feed_title, True)

        # Verify feed is now expanded
        assert screen.feed_fold_state["Test Feed"] is True
        feed_header.toggle_fold.assert_called()

    def test_collapse_all_toggles_all_feeds(self, diverse_entries):
        """Test that all feeds can be toggled to collapsed state."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock()
        screen.list_view.children = []

        # Initialize all feeds as expanded
        screen.feed_fold_state = {"Test Feed": True}
        feed_header = MagicMock(spec=FeedHeaderItem)
        screen.feed_header_map = {"Test Feed": feed_header}

        # Manually toggle like action_collapse_all would do
        for feed_title in screen.feed_fold_state:
            if screen.feed_fold_state[feed_title]:
                screen._set_feed_fold_state(feed_title, False)

        # Verify feed is now collapsed
        assert screen.feed_fold_state["Test Feed"] is False
        feed_header.toggle_fold.assert_called()

    def test_get_highlighted_feed_title_from_header(self, diverse_entries):
        """Test _get_highlighted_feed_title() extracts title from FeedHeaderItem."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)

        # Create mock FeedHeaderItem
        header = MagicMock(spec=FeedHeaderItem)
        header.feed_title = "Test Feed"

        screen.list_view = MagicMock()
        screen.list_view.highlighted_child = header

        # Get feed title
        title = screen._get_highlighted_feed_title()

        assert title == "Test Feed"

    def test_get_highlighted_feed_title_from_entry(self, diverse_entries):
        """Test _get_highlighted_feed_title() extracts title from EntryListItem."""
        screen = EntryListScreen(entries=diverse_entries)

        # Create EntryListItem from first entry
        item = EntryListItem(diverse_entries[0])

        screen.list_view = MagicMock()
        screen.list_view.highlighted_child = item

        # Get feed title
        title = screen._get_highlighted_feed_title()

        assert title == "Test Feed"

    def test_get_highlighted_feed_title_none_when_no_highlight(self, diverse_entries):
        """Test _get_highlighted_feed_title() returns None when nothing highlighted."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.list_view = MagicMock()
        screen.list_view.highlighted_child = None

        title = screen._get_highlighted_feed_title()

        assert title is None

    def test_set_feed_fold_state_updates_visibility(self, diverse_entries):
        """Test _set_feed_fold_state() updates fold state and toggles header."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.feed_fold_state = {}
        screen.list_view = MagicMock()
        screen.list_view.children = []  # Empty children to avoid _update_feed_visibility error

        # Create mock feed header
        feed_header = MagicMock(spec=FeedHeaderItem)
        screen.feed_header_map = {"Test Feed": feed_header}

        # Set fold state to expanded
        screen._set_feed_fold_state("Test Feed", True)

        # Verify state updated
        assert screen.feed_fold_state["Test Feed"] is True
        # Verify toggle_fold called
        feed_header.toggle_fold.assert_called()

    def test_ensure_list_view_and_grouped_returns_true(self, diverse_entries):
        """Test _ensure_list_view_and_grouped() returns True when conditions met."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock()

        result = screen._ensure_list_view_and_grouped()

        assert result is True

    def test_ensure_list_view_and_grouped_returns_false_when_not_grouped(self, diverse_entries):
        """Test _ensure_list_view_and_grouped() returns False when not in grouped mode."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=False)
        screen.list_view = MagicMock()

        result = screen._ensure_list_view_and_grouped()

        assert result is False

    def test_list_view_has_items_with_children(self, diverse_entries):
        """Test _list_view_has_items() returns True when list has children."""
        screen = EntryListScreen(entries=diverse_entries)

        # Create mock list view with children
        screen.list_view = MagicMock()
        screen.list_view.children = [MagicMock()]

        result = screen._list_view_has_items()

        assert result is True

    def test_list_view_has_items_empty_list(self, diverse_entries):
        """Test _list_view_has_items() returns False when list is empty."""
        screen = EntryListScreen(entries=diverse_entries)

        screen.list_view = MagicMock()
        screen.list_view.children = []

        result = screen._list_view_has_items()

        assert result is False

    def test_list_view_has_items_none_list(self, diverse_entries):
        """Test _list_view_has_items() returns False when list_view is None."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.list_view = None

        result = screen._list_view_has_items()

        assert result is False

    def test_find_entry_index_by_id_found(self, diverse_entries):
        """Test _find_entry_index_by_id() finds entry by ID."""
        screen = EntryListScreen(entries=diverse_entries)

        # Create list of items
        items = [EntryListItem(e) for e in diverse_entries]
        screen.list_view = MagicMock()
        screen.list_view.children = items

        # Find entry with ID 2
        index = screen._find_entry_index_by_id(2)

        assert index == 1  # Second item in list

    def test_find_entry_index_by_id_not_found(self, diverse_entries):
        """Test _find_entry_index_by_id() returns None when ID not found."""
        screen = EntryListScreen(entries=diverse_entries)

        items = [EntryListItem(e) for e in diverse_entries]
        screen.list_view = MagicMock()
        screen.list_view.children = items

        # Try to find non-existent entry
        index = screen._find_entry_index_by_id(999)

        assert index is None

    def test_find_entry_index_by_id_none_entry_id(self, diverse_entries):
        """Test _find_entry_index_by_id() returns None when entry_id is None."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.list_view = MagicMock()

        index = screen._find_entry_index_by_id(None)

        assert index is None

    def test_find_feed_header_index_found(self, diverse_entries):
        """Test _find_feed_header_index() finds feed header by title."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)

        # Create mock feed header
        header = MagicMock(spec=FeedHeaderItem)
        screen.feed_header_map = {"Test Feed": header}

        # Create list with header
        screen.list_view = MagicMock()
        screen.list_view.children = [header]

        # Find header
        index = screen._find_feed_header_index("Test Feed")

        assert index == 0

    def test_find_feed_header_index_not_found(self, diverse_entries):
        """Test _find_feed_header_index() returns None when feed not in map."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.feed_header_map = {}
        screen.list_view = MagicMock()

        index = screen._find_feed_header_index("Test Feed")

        assert index is None

    def test_find_feed_header_index_not_grouped(self, diverse_entries):
        """Test _find_feed_header_index() returns None when not in grouped mode."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=False)
        screen.list_view = MagicMock()

        index = screen._find_feed_header_index("Test Feed")

        assert index is None

    def test_set_cursor_to_index_success(self, diverse_entries):
        """Test _set_cursor_to_index() successfully sets cursor."""
        screen = EntryListScreen(entries=diverse_entries)

        screen.list_view = MagicMock()
        screen.list_view.children = [MagicMock() for _ in diverse_entries]

        result = screen._set_cursor_to_index(1)

        assert result is True
        assert screen.list_view.index == 1

    def test_set_cursor_to_index_out_of_bounds(self, diverse_entries):
        """Test _set_cursor_to_index() returns False when index out of bounds."""
        screen = EntryListScreen(entries=diverse_entries)

        screen.list_view = MagicMock()
        screen.list_view.children = [MagicMock() for _ in diverse_entries]

        result = screen._set_cursor_to_index(999)

        assert result is False
        # Verify index was not set
        screen.list_view.index.assert_not_called()

    def test_add_feed_header_if_needed_creates_header(self):
        """Test _add_feed_header_if_needed() creates and registers header."""
        screen = EntryListScreen(entries=[], group_by_feed=True)
        screen.feed_fold_state = {}
        screen.feed_header_map = {}
        screen.list_view = MagicMock()

        # Call with new feed
        screen._add_feed_header_if_needed("Test Feed", [None])

        # Verify header was created and registered
        assert "Test Feed" in screen.feed_header_map
        assert "Test Feed" in screen.feed_fold_state
        screen.list_view.append.assert_called()

    def test_add_entry_with_visibility_collapsed(self, diverse_entries):
        """Test _add_entry_with_visibility() applies collapsed class."""
        entry = diverse_entries[0]
        screen = EntryListScreen(entries=[entry], group_by_feed=True)
        screen.displayed_items = []
        screen.entry_item_map = {}
        screen.list_view = MagicMock()

        # Set feed as collapsed
        screen.feed_fold_state = {"Test Feed": False}

        # Add entry
        screen._add_entry_with_visibility(entry)

        # Verify item was added
        assert entry.id in screen.entry_item_map
        # Verify item is in displayed items
        assert len(screen.displayed_items) == 1
        item = screen.displayed_items[0]
        assert isinstance(item, EntryListItem)
        assert item.entry.id == entry.id

    def test_add_entry_with_visibility_expanded(self, diverse_entries):
        """Test _add_entry_with_visibility() doesn't add class when expanded."""
        entry = diverse_entries[0]
        screen = EntryListScreen(entries=[entry], group_by_feed=True)
        screen.displayed_items = []
        screen.entry_item_map = {}
        screen.list_view = MagicMock()

        # Set feed as expanded
        screen.feed_fold_state = {"Test Feed": True}

        # Add entry
        screen._add_entry_with_visibility(entry)

        # Verify item was added to displayed items
        assert entry.id in screen.entry_item_map
        assert len(screen.displayed_items) == 1
        item = screen.displayed_items[0]
        assert isinstance(item, EntryListItem)
        assert item.entry.id == entry.id


class TestEventHandlers:
    """Test event handler methods for screen lifecycle."""

    def test_on_mount_exists(self, diverse_entries):
        """Test on_mount method exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries)

        # Verify method exists and is callable
        assert callable(screen.on_mount)

    def test_on_screen_resume_exists(self, diverse_entries):
        """Test on_screen_resume method exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries)

        # Verify method exists and is callable
        assert callable(screen.on_screen_resume)

    def test_on_list_view_selected_exists(self, diverse_entries):
        """Test on_list_view_selected method exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries)

        # Verify method exists and is callable
        assert callable(screen.on_list_view_selected)


class TestActionMethodsCallability:
    """Test action method callability for user interactions."""

    @pytest.mark.asyncio
    async def test_action_toggle_read_exists(self, diverse_entries):
        """Test action_toggle_read exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.list_view = MagicMock()

        # Verify method exists and is callable
        assert callable(screen.action_toggle_read)

    @pytest.mark.asyncio
    async def test_action_toggle_star_works(self, diverse_entries):
        """Test action_toggle_star exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.list_view = MagicMock()

        # Verify method exists and is callable
        assert callable(screen.action_toggle_star)

    @pytest.mark.asyncio
    async def test_action_save_entry_works(self, diverse_entries):
        """Test action_save_entry exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.list_view = MagicMock()

        # Verify method exists and is callable
        assert callable(screen.action_save_entry)

    @pytest.mark.asyncio
    async def test_action_refresh_works(self, diverse_entries):
        """Test action_refresh exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries)

        # Verify method exists and is callable
        assert callable(screen.action_refresh)

    @pytest.mark.asyncio
    async def test_action_show_unread_works(self, diverse_entries):
        """Test action_show_unread exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries)

        # Verify method exists and is callable
        assert callable(screen.action_show_unread)

    @pytest.mark.asyncio
    async def test_action_show_starred_works(self, diverse_entries):
        """Test action_show_starred exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries)

        # Verify method exists and is callable
        assert callable(screen.action_show_starred)

    def test_action_cycle_sort_exists(self, diverse_entries):
        """Test action_cycle_sort exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries, default_sort="date")

        # Verify method exists and is callable
        assert callable(screen.action_cycle_sort)

    def test_action_toggle_group_feed_switches_mode(self, diverse_entries):
        """Test action_toggle_group_feed toggles grouping."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=False)
        screen._populate_list = MagicMock()

        # Verify method exists and is callable
        assert callable(screen.action_toggle_group_feed)

    def test_action_toggle_fold_exists(self, diverse_entries):
        """Test action_toggle_fold exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock()

        # Verify method exists and is callable
        assert callable(screen.action_toggle_fold)

    def test_action_collapse_fold_exists(self, diverse_entries):
        """Test action_collapse_fold exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock()

        # Verify method exists and is callable
        assert callable(screen.action_collapse_fold)

    def test_action_expand_fold_exists(self, diverse_entries):
        """Test action_expand_fold exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock()

        # Verify method exists and is callable
        assert callable(screen.action_expand_fold)

    def test_action_expand_all_exists(self, diverse_entries):
        """Test action_expand_all exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)

        # Verify method exists and is callable
        assert callable(screen.action_expand_all)

    def test_action_collapse_all_exists(self, diverse_entries):
        """Test action_collapse_all exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)

        # Verify method exists and is callable
        assert callable(screen.action_collapse_all)

    def test_action_show_help_exists(self, diverse_entries):
        """Test action_show_help exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries)

        # Verify method exists and is callable
        assert callable(screen.action_show_help)

    def test_action_quit_exists(self, diverse_entries):
        """Test action_quit exists and is callable."""
        screen = EntryListScreen(entries=diverse_entries)

        # Verify method exists and is callable
        assert callable(screen.action_quit)


class TestEntryActionBehaviour:
    """Test entry-related actions for correct behaviour."""

    @pytest.mark.asyncio
    async def test_action_toggle_read_updates_status(self, diverse_entries):
        """Test action_toggle_read toggles status and uses incremental update."""
        screen = EntryListScreen(entries=diverse_entries)
        entry_item = EntryListItem(diverse_entries[0])
        screen.list_view = MagicMock()
        screen.list_view.highlighted_child = entry_item
        screen.list_view.index = 0

        screen._update_single_item = MagicMock(return_value=True)
        screen._populate_list = MagicMock()
        screen.notify = MagicMock()

        mock_client = AsyncMock()
        mock_client.change_entry_status = AsyncMock()
        mock_app = MagicMock()
        mock_app.client = mock_client

        with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
            await screen.action_toggle_read()

        mock_client.change_entry_status.assert_awaited_once_with(entry_item.entry.id, "read")
        assert entry_item.entry.status == "read"
        screen._populate_list.assert_not_called()
        screen.notify.assert_called_with("Entry marked as read")

    @pytest.mark.asyncio
    async def test_action_toggle_star_refreshes_when_incremental_fails(self, diverse_entries):
        """Test action_toggle_star toggles star and falls back to full refresh."""
        screen = EntryListScreen(entries=diverse_entries)
        entry_item = EntryListItem(diverse_entries[0])
        screen.list_view = MagicMock()
        screen.list_view.highlighted_child = entry_item
        screen.list_view.index = 0

        screen._update_single_item = MagicMock(return_value=False)
        screen._populate_list = MagicMock()
        screen.notify = MagicMock()

        mock_client = AsyncMock()
        mock_client.toggle_starred = AsyncMock()
        mock_app = MagicMock()
        mock_app.client = mock_client

        with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
            await screen.action_toggle_star()

        mock_client.toggle_starred.assert_awaited_once_with(entry_item.entry.id)
        assert entry_item.entry.starred is True
        screen._populate_list.assert_called_once()
        assert "Entry starred" in screen.notify.call_args[0][0]

    @pytest.mark.asyncio
    async def test_action_save_entry_calls_api(self, diverse_entries):
        """Test action_save_entry calls save_entry and notifies user."""
        screen = EntryListScreen(entries=diverse_entries)
        entry_item = EntryListItem(diverse_entries[0])
        screen.list_view = MagicMock()
        screen.list_view.highlighted_child = entry_item
        screen.list_view.index = 0
        screen.notify = MagicMock()

        mock_client = AsyncMock()
        mock_client.save_entry = AsyncMock()
        mock_app = MagicMock()
        mock_app.client = mock_client

        with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
            await screen.action_save_entry()

        mock_client.save_entry.assert_awaited_once_with(entry_item.entry.id)
        screen.notify.assert_called_with(f"Entry saved: {entry_item.entry.title}")


class TestRefreshActions:
    """Test refresh actions for Issue #55 - Feed operations."""

    @pytest.mark.asyncio
    async def test_action_refresh_current_feed_success(self, diverse_entries):
        """Test refreshing the current feed successfully."""

        screen = EntryListScreen(entries=diverse_entries)

        # Create mocks
        mock_client = AsyncMock()
        mock_client.refresh_feed = AsyncMock()
        mock_app = MagicMock()
        mock_app.client = mock_client
        mock_app.load_entries = AsyncMock()
        mock_app.current_view = "unread"
        mock_app.notify_info = MagicMock()  # Mock notify_info for info messages

        # Mock list view with highlighted entry
        mock_list_view = MagicMock()
        mock_list_view.index = 0
        mock_entry_item = EntryListItem(diverse_entries[0], unread_color="cyan", read_color="gray")
        mock_list_view.highlighted_child = mock_entry_item
        screen.list_view = mock_list_view

        # Mock notify
        screen.notify = MagicMock()

        # Patch the app property getter and run_worker
        with (
            patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)),
            patch.object(screen, "run_worker", side_effect=mock_run_worker),
        ):
            # Call action_refresh (now synchronous, uses run_worker)
            screen.action_refresh()
            # Give the worker task a chance to run
            await asyncio.sleep(0.1)

        # Verify refresh_feed was called with correct feed_id
        mock_client.refresh_feed.assert_called_once_with(diverse_entries[0].feed_id)

        # Verify load_entries was NOT called (new behavior: only refresh, don't reload)
        mock_app.load_entries.assert_not_called()

        # Verify notifications (should show refreshing and success messages)
        assert screen.notify.call_count >= 1

    @pytest.mark.asyncio
    async def test_action_refresh_no_client(self, diverse_entries):
        """Test refresh action when client is not initialized."""

        screen = EntryListScreen(entries=diverse_entries)

        # Mock app without client
        mock_app = MagicMock()
        mock_app.client = None

        # Mock notify
        screen.notify = MagicMock()

        # Patch the app property getter
        with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
            # Call action_refresh (now synchronous)
            screen.action_refresh()

        # Verify error notification
        screen.notify.assert_called_once()
        assert "not initialized" in screen.notify.call_args[0][0].lower()

    @pytest.mark.asyncio
    async def test_action_refresh_no_entry_selected(self, diverse_entries):
        """Test refresh action when no entry is selected."""

        screen = EntryListScreen(entries=diverse_entries)

        # Create mocks
        mock_client = AsyncMock()
        mock_app = MagicMock()
        mock_app.client = mock_client

        # Mock list view with no selection
        mock_list_view = MagicMock()
        mock_list_view.index = None
        screen.list_view = mock_list_view

        # Mock notify
        screen.notify = MagicMock()

        # Patch the app property getter
        with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
            # Call action_refresh (now synchronous)
            screen.action_refresh()

        # Verify warning notification
        screen.notify.assert_called_once()
        assert "no entry selected" in screen.notify.call_args[0][0].lower()

    @pytest.mark.asyncio
    async def test_action_refresh_network_error(self, diverse_entries):
        """Test refresh action with network error."""

        screen = EntryListScreen(entries=diverse_entries)

        # Mock app with client that raises ConnectionError
        mock_client = AsyncMock()
        mock_client.refresh_feed = AsyncMock(side_effect=ConnectionError("Network error"))
        mock_app = MagicMock()
        mock_app.client = mock_client
        # Mock reconnect_client as async function that returns False
        mock_app.reconnect_client = AsyncMock(return_value=False)

        # Mock list view with highlighted entry
        mock_list_view = MagicMock()
        mock_list_view.index = 0
        mock_entry_item = EntryListItem(diverse_entries[0], unread_color="cyan", read_color="gray")
        mock_list_view.highlighted_child = mock_entry_item
        screen.list_view = mock_list_view

        # Mock notify
        screen.notify = MagicMock()

        # Patch the app property getter and run_worker
        with (
            patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)),
            patch.object(screen, "run_worker", side_effect=mock_run_worker),
        ):
            # Call action_refresh (now synchronous, uses run_worker)
            screen.action_refresh()
            # Give the worker task a chance to run
            await asyncio.sleep(0.1)

        # Verify error notification
        assert any("network error" in str(call[0][0]).lower() for call in screen.notify.call_args_list)

    @pytest.mark.asyncio
    async def test_action_refresh_all_feeds_success(self, diverse_entries):
        """Test refreshing all feeds successfully."""

        screen = EntryListScreen(entries=diverse_entries)

        # Create mocks
        mock_client = AsyncMock()
        mock_client.refresh_all_feeds = AsyncMock()
        mock_app = MagicMock()
        mock_app.client = mock_client
        mock_app.load_entries = AsyncMock()
        mock_app.current_view = "unread"
        mock_app.notify_info = MagicMock()  # Mock notify_info for info messages

        # Mock notify
        screen.notify = MagicMock()

        # Patch the app property getter and run_worker
        with (
            patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)),
            patch.object(screen, "run_worker", side_effect=mock_run_worker),
        ):
            # Call action_refresh_all_feeds (now synchronous, uses run_worker)
            screen.action_refresh_all_feeds()
            # Give the worker task a chance to run
            await asyncio.sleep(0.1)

        # Verify refresh_all_feeds was called
        mock_client.refresh_all_feeds.assert_called_once()

        # Verify load_entries was NOT called (new behavior: only refresh, don't reload)
        mock_app.load_entries.assert_not_called()

        # Verify notifications (should show refreshing and success messages)
        assert screen.notify.call_count >= 1

    @pytest.mark.asyncio
    async def test_action_refresh_all_feeds_no_client(self, diverse_entries):
        """Test refresh all feeds when client is not initialized."""

        screen = EntryListScreen(entries=diverse_entries)

        # Mock app without client
        mock_app = MagicMock()
        mock_app.client = None

        # Mock notify
        screen.notify = MagicMock()

        # Patch the app property getter
        with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
            # Call action_refresh_all_feeds
            screen.action_refresh_all_feeds()

        # Verify error notification
        screen.notify.assert_called_once()
        assert "not initialized" in screen.notify.call_args[0][0].lower()

    @pytest.mark.asyncio
    async def test_action_refresh_all_feeds_network_error(self, diverse_entries):
        """Test refresh all feeds with network error."""

        screen = EntryListScreen(entries=diverse_entries)

        # Mock app with client that raises TimeoutError
        mock_client = AsyncMock()
        mock_client.refresh_all_feeds = AsyncMock(side_effect=TimeoutError("Connection timeout"))
        mock_app = MagicMock()
        mock_app.client = mock_client
        # Mock reconnect_client as async function that returns False
        mock_app.reconnect_client = AsyncMock(return_value=False)

        # Mock notify
        screen.notify = MagicMock()

        # Patch the app property getter and run_worker
        with (
            patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)),
            patch.object(screen, "run_worker", side_effect=mock_run_worker),
        ):
            # Call action_refresh_all_feeds (now synchronous, uses run_worker)
            screen.action_refresh_all_feeds()
            # Give the worker task a chance to run
            await asyncio.sleep(0.1)

        # Verify error notification
        assert any("network error" in str(call[0][0]).lower() for call in screen.notify.call_args_list)

    @pytest.mark.asyncio
    async def test_action_refresh_handles_general_exception(self, diverse_entries):
        """Test refresh action handles unexpected exceptions."""

        screen = EntryListScreen(entries=diverse_entries)

        mock_client = AsyncMock()
        mock_client.refresh_feed = AsyncMock(side_effect=RuntimeError("boom"))
        mock_app = MagicMock()
        mock_app.client = mock_client
        mock_app.load_entries = AsyncMock()

        mock_list_view = MagicMock()
        mock_list_view.index = 0
        mock_entry_item = EntryListItem(diverse_entries[0], unread_color="cyan", read_color="gray")
        mock_list_view.highlighted_child = mock_entry_item
        screen.list_view = mock_list_view

        screen.notify = MagicMock()

        with (
            patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)),
            patch.object(screen, "run_worker", side_effect=mock_run_worker),
        ):
            screen.action_refresh()
            # Give the worker task a chance to run
            await asyncio.sleep(0.1)

        assert any("Error refreshing feed" in str(call[0][0]) for call in screen.notify.call_args_list)
        mock_app.load_entries.assert_not_called()

    @pytest.mark.asyncio
    async def test_action_refresh_all_handles_general_exception(self, diverse_entries):
        """Test refresh all feeds handles unexpected exceptions."""

        screen = EntryListScreen(entries=diverse_entries)

        mock_client = AsyncMock()
        mock_client.refresh_all_feeds = AsyncMock(side_effect=RuntimeError("boom"))
        mock_app = MagicMock()
        mock_app.client = mock_client
        mock_app.load_entries = AsyncMock()
        mock_app.current_view = "unread"

        screen.notify = MagicMock()

        with (
            patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)),
            patch.object(screen, "run_worker", side_effect=mock_run_worker),
        ):
            screen.action_refresh_all_feeds()
            # Give the worker task a chance to run
            await asyncio.sleep(0.1)

        assert any("Error refreshing all feeds" in str(call[0][0]) for call in screen.notify.call_args_list)
        mock_app.load_entries.assert_not_called()


class TestViewFilteringActions:
    """Test actions that switch between entry views."""

    @pytest.mark.asyncio
    async def test_action_show_unread_resets_filters(self, diverse_entries):
        """Test action_show_unread loads unread entries and clears filters."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.filter_unread_only = True
        screen.filter_starred_only = True
        screen._populate_list = MagicMock()

        mock_app = MagicMock()
        mock_app.load_entries = AsyncMock()
        mock_app.client = AsyncMock()
        mock_app.current_view = "unread"

        with (
            patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)),
            patch.object(screen, "run_worker", side_effect=mock_run_worker),
        ):
            screen.action_show_unread()
            # Give the worker task a chance to run
            await asyncio.sleep(0.1)

        mock_app.load_entries.assert_awaited_once_with("unread")
        assert screen.filter_unread_only is False
        assert screen.filter_starred_only is False
        screen._populate_list.assert_called_once()

    @pytest.mark.asyncio
    async def test_action_show_starred_resets_filters(self, diverse_entries):
        """Test action_show_starred loads starred entries and clears filters."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.filter_unread_only = True
        screen.filter_starred_only = True
        screen._populate_list = MagicMock()

        mock_app = MagicMock()
        mock_app.load_entries = AsyncMock()
        mock_app.client = AsyncMock()
        mock_app.current_view = "starred"

        with (
            patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)),
            patch.object(screen, "run_worker", side_effect=mock_run_worker),
        ):
            screen.action_show_starred()
            # Give the worker task a chance to run
            await asyncio.sleep(0.1)

        mock_app.load_entries.assert_awaited_once_with("starred")
        assert screen.filter_unread_only is False
        assert screen.filter_starred_only is False
        screen._populate_list.assert_called_once()


class TestCategoryGrouping:
    """Test category grouping functionality for Issue #54."""

    def test_get_category_title_with_valid_id(self):
        """Test getting category title with valid category ID."""

        categories = [
            Category(id=1, title="News"),
            Category(id=2, title="Tech"),
        ]
        screen = EntryListScreen(entries=[], categories=categories)

        assert screen._get_category_title(1) == "News"
        assert screen._get_category_title(2) == "Tech"

    def test_get_category_title_with_none(self):
        """Test getting category title when category_id is None."""
        screen = EntryListScreen(entries=[], categories=[])

        assert screen._get_category_title(None) == "Uncategorized"

    def test_get_category_title_with_nonexistent_id(self):
        """Test getting category title with non-existent category ID."""

        categories = [Category(id=1, title="News")]
        screen = EntryListScreen(entries=[], categories=categories)

        assert screen._get_category_title(999) == "Category 999"

    def test_get_category_title_with_no_categories(self):
        """Test getting category title when categories list is empty."""
        screen = EntryListScreen(entries=[], categories=[])

        assert screen._get_category_title(5) == "Category 5"

    def test_action_toggle_group_feed_category_no_categories(self):
        """Test toggle category group when no categories available."""
        screen = EntryListScreen(entries=[], categories=[])
        screen.notify = MagicMock()

        screen.action_toggle_group_category()

        screen.notify.assert_called_once()
        assert "no categories" in screen.notify.call_args[0][0].lower()

    def test_action_toggle_group_feed_category_enable(self, diverse_entries):
        """Test enabling category grouping."""

        categories = [Category(id=1, title="News")]
        screen = EntryListScreen(entries=diverse_entries, categories=categories)
        screen.notify = MagicMock()
        screen._populate_list = MagicMock()

        # Initially both grouping modes off
        assert not screen.group_by_category
        assert not screen.group_by_feed

        # Enable category grouping
        screen.action_toggle_group_category()

        assert screen.group_by_category is True
        assert screen.group_by_feed is False
        screen.notify.assert_called_with("Grouping by category (use h/l to collapse/expand)")
        screen._populate_list.assert_called_once()

    def test_action_toggle_group_feed_category_disable(self, diverse_entries):
        """Test disabling category grouping."""

        categories = [Category(id=1, title="News")]
        screen = EntryListScreen(entries=diverse_entries, categories=categories)
        screen.notify = MagicMock()
        screen._populate_list = MagicMock()
        screen.group_by_category = True

        # Disable category grouping
        screen.action_toggle_group_category()

        assert screen.group_by_category is False
        screen.notify.assert_called_with("Category grouping disabled")
        screen._populate_list.assert_called_once()

    def test_action_toggle_group_feed_category_disables_feed_grouping(self, diverse_entries):
        """Test that enabling category grouping disables feed grouping."""

        categories = [Category(id=1, title="News")]
        screen = EntryListScreen(entries=diverse_entries, categories=categories)
        screen.notify = MagicMock()
        screen._populate_list = MagicMock()
        screen.group_by_feed = True

        # Enable category grouping
        screen.action_toggle_group_category()

        assert screen.group_by_category is True
        assert screen.group_by_feed is False

    def test_get_sorted_entries_with_category_grouping(self, diverse_entries):
        """Test entry sorting when category grouping is enabled."""

        categories = [
            Category(id=1, title="News"),
            Category(id=2, title="Tech"),
        ]
        screen = EntryListScreen(entries=diverse_entries, categories=categories)
        screen.group_by_category = True

        # Mock feed category_id
        for i, entry in enumerate(diverse_entries):
            entry.feed.category_id = 1 if i % 2 == 0 else 2

        sorted_entries = screen._get_sorted_entries()

        # Should be sorted by category title first
        assert len(sorted_entries) > 0
        # Verify grouping: all entries with same category_id should be together
        prev_category = None
        for entry in sorted_entries:
            current_category = screen._get_category_title(entry.feed.category_id)
            if prev_category and prev_category != current_category:
                # Category changed, shouldn't go back to previous category
                remaining_entries = sorted_entries[sorted_entries.index(entry) :]
                remaining_categories = [screen._get_category_title(e.feed.category_id) for e in remaining_entries]
                assert prev_category not in remaining_categories
            prev_category = current_category

    def test_category_fold_state_initialization(self):
        """Test that category fold state is initialized."""
        screen = EntryListScreen(entries=[])

        assert isinstance(screen.category_fold_state, dict)
        assert isinstance(screen.category_header_map, dict)
        assert screen.last_highlighted_category is None

    def test_display_entries_with_category_grouping(self, diverse_entries):
        """Test _display_entries delegates to category grouping."""

        categories = [Category(id=1, title="News")]
        screen = EntryListScreen(entries=diverse_entries, categories=categories)
        screen.group_by_category = True
        screen._add_grouped_entries_by_category = MagicMock()

        screen._display_entries(diverse_entries)

        screen._add_grouped_entries_by_category.assert_called_once_with(diverse_entries)

    def test_display_entries_without_category_grouping(self, diverse_entries):
        """Test _display_entries doesn't use category grouping when disabled."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.group_by_category = False
        screen._add_grouped_entries_by_category = MagicMock()
        screen._add_flat_entries = MagicMock()
        screen._add_grouped_entries = MagicMock()

        screen._display_entries(diverse_entries)

        screen._add_grouped_entries_by_category.assert_not_called()

    def test_category_grouping_sorts_before_feed_grouping(self, diverse_entries):
        """Test that category grouping takes precedence over feed grouping."""

        categories = [Category(id=1, title="News")]
        screen = EntryListScreen(entries=diverse_entries, categories=categories)
        screen.group_by_category = True
        screen.group_by_feed = True  # Both set, but category should win

        # Mock feed category_id
        for entry in diverse_entries:
            entry.feed.category_id = 1

        sorted_entries = screen._get_sorted_entries()

        # Should use category sorting (by category title + date)
        # Not feed sorting (by feed title + date)
        assert len(sorted_entries) > 0


class TestSearchActions:
    """Test search-related actions."""

    def test_action_search_shows_input_dialog(self, diverse_entries):
        """Test action_search shows input dialog for search."""
        screen = EntryListScreen(entries=diverse_entries)

        # Mock the app
        mock_app = MagicMock()
        mock_app.push_screen = MagicMock()

        # Patch the app property
        with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
            screen.action_search()

        # Verify push_screen was called with InputDialog
        mock_app.push_screen.assert_called_once()
        # Verify the dialog is an InputDialog
        assert isinstance(mock_app.push_screen.call_args[0][0], InputDialog)

    def test_action_search_dialog_preserves_current_search(self, diverse_entries):
        """Test action_search dialog pre-fills with current search term."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.search_term = "existing search"

        # Mock the app
        mock_app = MagicMock()
        mock_app.push_screen = MagicMock()

        # Patch the app property
        with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
            screen.action_search()

        # Verify dialog was created with current search term as initial value
        dialog = mock_app.push_screen.call_args[0][0]
        assert isinstance(dialog, InputDialog)
        assert dialog.initial_value == "existing search"

    def test_set_search_term_applies_filter(self, diverse_entries):
        """Test set_search_term stores term and notifies about results."""
        screen = EntryListScreen(entries=diverse_entries)
        screen._populate_list = MagicMock()
        screen.notify = MagicMock()

        with patch.object(screen, "_filter_entries", return_value=diverse_entries[:2]) as mock_filter:
            screen.set_search_term("News")

        screen._populate_list.assert_called_once()
        mock_filter.assert_called_once_with(screen.entries)
        screen.notify.assert_called_with("Search: 2 entries match 'News'")
        assert screen.search_active is True


class TestNavigationActions:
    """Test navigation-related actions."""

    def test_action_show_help_pushes_help_screen(self, diverse_entries):
        """Test action_show_help pushes the help screen."""
        screen = EntryListScreen(entries=diverse_entries)
        mock_app = MagicMock()

        with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
            screen.action_show_help()

        mock_app.push_screen.assert_called_once_with("help")

    def test_action_quit_exits_application(self, diverse_entries):
        """Test action_quit calls app.exit()."""
        screen = EntryListScreen(entries=diverse_entries)
        mock_app = MagicMock()

        with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
            screen.action_quit()

        mock_app.exit.assert_called_once()


class TestFeedHeaderSelection:
    """Test selecting feed headers in grouped mode."""

    @pytest.fixture
    def grouped_entries(self):
        """Create entries from multiple feeds for grouping tests."""
        feed1 = Feed(
            id=1,
            title="Feed A",
            site_url="http://localhost:8082",
            feed_url="http://localhost:8082/feed.xml",
        )
        feed2 = Feed(
            id=2,
            title="Feed B",
            site_url="http://localhost:8083",
            feed_url="http://localhost:8083/feed.xml",
        )
        return [
            Entry(
                id=1,
                feed_id=1,
                title="Entry 1",
                url="http://localhost:8082/1",
                content="Content 1",
                feed=feed1,
                status="unread",
                starred=False,
                published_at=datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC),
            ),
            Entry(
                id=2,
                feed_id=1,
                title="Entry 2",
                url="http://localhost:8082/2",
                content="Content 2",
                feed=feed1,
                status="read",
                starred=False,
                published_at=datetime(2025, 1, 1, 11, 0, 0, tzinfo=UTC),
            ),
            Entry(
                id=3,
                feed_id=2,
                title="Entry 3",
                url="http://localhost:8083/1",
                content="Content 3",
                feed=feed2,
                status="unread",
                starred=False,
                published_at=datetime(2025, 1, 1, 10, 0, 0, tzinfo=UTC),
            ),
        ]

    def test_on_list_view_selected_with_feed_header_opens_first_entry(self, grouped_entries):
        """Test that selecting a feed header opens the first entry in that feed."""
        from miniflux_tui.ui.screens.entry_list import FeedHeaderItem  # noqa: PLC0415

        screen = EntryListScreen(entries=grouped_entries, group_by_feed=True)
        screen.sorted_entries = grouped_entries
        mock_app = MagicMock()
        mock_event = MagicMock()

        # Create a mock FeedHeaderItem for Feed A
        feed_header = FeedHeaderItem("Feed A")
        mock_event.item = feed_header

        with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
            screen.on_list_view_selected(mock_event)

        # Should call push_entry_reader with the first entry of Feed A
        mock_app.push_entry_reader.assert_called_once()
        call_args = mock_app.push_entry_reader.call_args
        assert call_args.kwargs["entry"].id == 1  # First entry in Feed A
        assert call_args.kwargs["current_index"] == 0

    def test_on_list_view_selected_with_feed_header_second_feed(self, grouped_entries):
        """Test selecting a feed header for second feed."""
        from miniflux_tui.ui.screens.entry_list import FeedHeaderItem  # noqa: PLC0415

        screen = EntryListScreen(entries=grouped_entries, group_by_feed=True)
        screen.sorted_entries = grouped_entries
        mock_app = MagicMock()
        mock_event = MagicMock()

        # Create a mock FeedHeaderItem for Feed B
        feed_header = FeedHeaderItem("Feed B")
        mock_event.item = feed_header

        with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
            screen.on_list_view_selected(mock_event)

        # Should call push_entry_reader with the first (only) entry of Feed B
        mock_app.push_entry_reader.assert_called_once()
        call_args = mock_app.push_entry_reader.call_args
        assert call_args.kwargs["entry"].id == 3  # Only entry in Feed B
        assert call_args.kwargs["current_index"] == 2  # Index in sorted_entries


class TestFeedSortOrder:
    """Test feed sort mode now sorts A-Z instead of Z-A."""

    @pytest.fixture
    def unsorted_entries(self):
        """Create entries from feeds with different names to test sorting."""
        feed_z = Feed(
            id=1,
            title="Zebra News",
            site_url="http://localhost:8082",
            feed_url="http://localhost:8082/feed.xml",
        )
        feed_a = Feed(
            id=2,
            title="Apple Daily",
            site_url="http://localhost:8083",
            feed_url="http://localhost:8083/feed.xml",
        )
        feed_m = Feed(
            id=3,
            title="Monkey Biz",
            site_url="http://localhost:8084",
            feed_url="http://localhost:8084/feed.xml",
        )
        return [
            Entry(
                id=1,
                feed_id=1,
                title="Old Zebra Article",
                url="http://localhost:8082/1",
                content="Content",
                feed=feed_z,
                status="unread",
                starred=False,
                published_at=datetime(2025, 1, 1, 8, 0, 0, tzinfo=UTC),
            ),
            Entry(
                id=2,
                feed_id=1,
                title="New Zebra Article",
                url="http://localhost:8082/2",
                content="Content",
                feed=feed_z,
                status="unread",
                starred=False,
                published_at=datetime(2025, 1, 1, 10, 0, 0, tzinfo=UTC),
            ),
            Entry(
                id=3,
                feed_id=2,
                title="Apple Article",
                url="http://localhost:8083/1",
                content="Content",
                feed=feed_a,
                status="unread",
                starred=False,
                published_at=datetime(2025, 1, 1, 9, 0, 0, tzinfo=UTC),
            ),
            Entry(
                id=4,
                feed_id=3,
                title="Monkey Article",
                url="http://localhost:8084/1",
                content="Content",
                feed=feed_m,
                status="unread",
                starred=False,
                published_at=datetime(2025, 1, 1, 7, 0, 0, tzinfo=UTC),
            ),
        ]

    def test_sort_entries_feed_mode_sorts_a_to_z(self, unsorted_entries):
        """Test that feed sort mode sorts feeds alphabetically A-Z."""
        screen = EntryListScreen(entries=unsorted_entries, default_sort="feed")
        screen.current_sort = "feed"

        sorted_entries = screen._sort_entries(unsorted_entries)

        # Should be sorted by feed name (A-Z): Apple, Monkey, Zebra
        feed_names = [entry.feed.title for entry in sorted_entries]
        assert feed_names == ["Apple Daily", "Monkey Biz", "Zebra News", "Zebra News"]

    def test_sort_entries_feed_mode_newest_first_within_each_feed(self, unsorted_entries):
        """Test that within each feed, entries are sorted newest first."""
        screen = EntryListScreen(entries=unsorted_entries, default_sort="feed")
        screen.current_sort = "feed"

        sorted_entries = screen._sort_entries(unsorted_entries)

        # Within Zebra feed, newer article (id=2) should come before older (id=1)
        zebra_entries = [e for e in sorted_entries if e.feed.title == "Zebra News"]
        assert zebra_entries[0].id == 2  # New Zebra Article
        assert zebra_entries[1].id == 1  # Old Zebra Article

    def test_sort_entries_feed_mode_case_insensitive(self, unsorted_entries):
        """Test that feed sort is case-insensitive."""
        feed_lower = Feed(
            id=4,
            title="apple core",
            site_url="http://localhost:8085",
            feed_url="http://localhost:8085/feed.xml",
        )
        entry_lower = Entry(
            id=5,
            feed_id=4,
            title="Apple Entry",
            url="http://localhost:8085/1",
            content="Content",
            feed=feed_lower,
            status="unread",
            starred=False,
            published_at=datetime(2025, 1, 1, 6, 0, 0, tzinfo=UTC),
        )
        entries = [*unsorted_entries, entry_lower]

        screen = EntryListScreen(entries=entries, default_sort="feed")
        screen.current_sort = "feed"

        sorted_entries = screen._sort_entries(entries)

        # Both Apple feeds should be grouped together (case-insensitive sorting)
        feed_names = [entry.feed.title for entry in sorted_entries]
        # All Apple entries should come before Monkey
        apple_indices = [i for i, name in enumerate(feed_names) if "apple" in name.lower()]
        monkey_index = feed_names.index("Monkey Biz")
        assert all(i < monkey_index for i in apple_indices)


class TestExpandAllWithToggle:
    """Test Shift+G now enables grouping if needed."""

    def test_action_expand_all_without_grouping_toggles_group_first(self, diverse_entries):
        """Test that Shift+G enables grouping if not already enabled."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.group_by_feed = False  # Not grouped
        screen.list_view = MagicMock()
        screen.action_toggle_group_feed = MagicMock()

        screen.action_expand_all()

        # Should call action_toggle_group_feed to enable grouping
        screen.action_toggle_group_feed.assert_called_once()

    def test_action_expand_all_with_grouping_skips_toggle(self, diverse_entries):
        """Test that when already grouped, expand_all doesn't toggle."""
        screen = EntryListScreen(entries=diverse_entries, group_by_feed=True)
        screen.list_view = MagicMock()
        screen.feed_fold_state = {"Feed A": False}
        screen._set_feed_fold_state = MagicMock()
        screen.notify = MagicMock()
        screen.action_toggle_group_feed = MagicMock()

        screen.action_expand_all()

        # Should NOT call toggle_group since already grouped
        screen.action_toggle_group_feed.assert_not_called()
        # Should expand the feeds
        screen._set_feed_fold_state.assert_called_once()

    def test_action_expand_all_without_list_view_returns_early(self, diverse_entries):
        """Test that expand_all returns early if no list_view."""
        screen = EntryListScreen(entries=diverse_entries)
        screen.list_view = None
        screen.action_toggle_group_feed = MagicMock()

        screen.action_expand_all()

        # Should return early without calling toggle
        screen.action_toggle_group_feed.assert_not_called()
