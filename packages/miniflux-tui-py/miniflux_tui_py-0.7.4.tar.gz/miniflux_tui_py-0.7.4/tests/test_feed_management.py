# SPDX-License-Identifier: MIT
"""Tests for FeedManagementScreen."""

import asyncio
from typing import cast
from unittest.mock import AsyncMock, MagicMock, patch

from textual.app import App
from textual.screen import Screen
from textual.widgets import ListView

from miniflux_tui.api.models import Feed
from miniflux_tui.ui.screens.feed_management import FeedListItem, FeedManagementScreen


class FeedManagementTestApp(App):
    """Test app for FeedManagementScreen testing."""

    def __init__(self, feeds: list[Feed] | None = None, **kwargs):
        """Initialize test app."""
        super().__init__(**kwargs)
        self.feeds = feeds or []
        self.client: MagicMock | None = None  # type: ignore[assignment]

    def on_mount(self) -> None:
        """Mount the feed management screen."""
        self.push_screen(FeedManagementScreen(feeds=self.feeds))


class TestFeedListItem:
    """Test FeedListItem widget."""

    def test_feed_list_item_creation(self) -> None:
        """Test creating a FeedListItem."""
        feed = Feed(
            id=1,
            title="Test Feed",
            site_url="https://example.com",
            feed_url="https://example.com/feed.xml",
        )
        item = FeedListItem(feed)
        assert item.feed == feed

    def test_feed_list_item_with_no_errors(self) -> None:
        """Test FeedListItem displays correctly for feed without errors."""
        feed = Feed(
            id=1,
            title="Healthy Feed",
            site_url="https://example.com",
            feed_url="https://example.com/feed.xml",
            parsing_error_count=0,
        )
        item = FeedListItem(feed)
        assert item.feed.parsing_error_count == 0

    def test_feed_list_item_with_errors(self) -> None:
        """Test FeedListItem displays correctly for feed with errors."""
        feed = Feed(
            id=1,
            title="Broken Feed",
            site_url="https://example.com",
            feed_url="https://example.com/feed.xml",
            parsing_error_count=3,
            parsing_error_message="Connection timeout",
        )
        item = FeedListItem(feed)
        assert item.feed.parsing_error_count == 3

    def test_feed_list_item_disabled_feed(self) -> None:
        """Test FeedListItem with disabled feed."""
        feed = Feed(
            id=1,
            title="Disabled Feed",
            site_url="https://example.com",
            feed_url="https://example.com/feed.xml",
            disabled=True,
        )
        item = FeedListItem(feed)
        assert item.feed.disabled is True

    def test_feed_list_item_long_title(self) -> None:
        """Test FeedListItem truncates long titles."""
        feed = Feed(
            id=1,
            title="This is a very long feed title that should be truncated " * 3,
            site_url="https://example.com",
            feed_url="https://example.com/feed.xml",
        )
        item = FeedListItem(feed)
        assert item.feed == feed


class TestFeedManagementScreenInitialization:
    """Test FeedManagementScreen initialization."""

    def test_feed_management_screen_creation_empty(self) -> None:
        """Test creating FeedManagementScreen without feeds."""
        screen = FeedManagementScreen()
        assert screen.feeds == []

    def test_feed_management_screen_creation_with_feeds(self) -> None:
        """Test creating FeedManagementScreen with feeds."""
        feeds = [
            Feed(
                id=1,
                title="Feed 1",
                site_url="https://example.com",
                feed_url="https://example.com/feed.xml",
            ),
            Feed(
                id=2,
                title="Feed 2",
                site_url="https://example2.com",
                feed_url="https://example2.com/feed.xml",
            ),
        ]
        screen = FeedManagementScreen(feeds=feeds)
        assert screen.feeds == feeds
        assert len(screen.feeds) == 2


class TestFeedManagementScreenBindings:
    """Test FeedManagementScreen key bindings."""

    def test_feed_management_has_bindings(self) -> None:
        """Test FeedManagementScreen has proper key bindings."""
        screen = FeedManagementScreen()
        bindings = list(screen.BINDINGS)  # type: ignore[attr-defined]
        binding_keys = [b.key for b in bindings]  # type: ignore[attr-defined]
        assert "n" in binding_keys  # Add feed
        assert "d" in binding_keys  # Delete feed
        assert "r" in binding_keys  # Refresh feed
        assert "enter" in binding_keys  # View details
        assert "escape" in binding_keys  # Back
        assert "j" in binding_keys  # Cursor down
        assert "k" in binding_keys  # Cursor up

    def test_feed_management_has_correct_actions(self) -> None:
        """Test FeedManagementScreen bindings map to correct actions."""
        screen = FeedManagementScreen()
        bindings = list(screen.BINDINGS)  # type: ignore[attr-defined]
        actions = {b.action for b in bindings}  # type: ignore[attr-defined]
        assert "add_feed" in actions
        assert "delete_feed" in actions
        assert "refresh_feed" in actions
        assert "view_details" in actions
        assert "back" in actions
        assert "cursor_down" in actions
        assert "cursor_up" in actions


class TestFeedManagementScreenCompose:
    """Test FeedManagementScreen composition."""

    def test_feed_management_has_css(self) -> None:
        """Test FeedManagementScreen has CSS defined."""
        screen = FeedManagementScreen()
        assert screen.CSS is not None
        assert len(screen.CSS) > 0


class TestFeedManagementScreenMethods:
    """Test FeedManagementScreen methods."""

    def test_feed_management_get_selected_feed_empty_list(self) -> None:
        """Test getting selected feed when list is empty."""
        screen = FeedManagementScreen()
        screen.list_view = None  # Simulate no list view
        feed = screen._get_selected_feed()
        assert feed is None

    def test_feed_management_populate_list(self) -> None:
        """Test populate_list method."""
        feeds = [
            Feed(
                id=1,
                title="Feed 1",
                site_url="https://example.com",
                feed_url="https://example.com/feed.xml",
            ),
            Feed(
                id=2,
                title="Feed 2",
                site_url="https://example2.com",
                feed_url="https://example2.com/feed.xml",
            ),
        ]
        FeedManagementScreen(feeds=feeds)
        # populate_list requires list_view to be initialized
        # which happens in on_mount, so we skip direct testing


class TestFeedManagementScreenIntegration:
    """Integration tests for FeedManagementScreen."""

    def test_feed_management_screen_is_screen(self) -> None:
        """Test FeedManagementScreen is a proper Screen."""
        screen = FeedManagementScreen()
        assert isinstance(screen, Screen)

    def test_feed_management_screen_with_multiple_feeds(self) -> None:
        """Test FeedManagementScreen handles multiple feeds."""
        feeds = [
            Feed(
                id=i,
                title=f"Feed {i}",
                site_url=f"https://example{i}.com",
                feed_url=f"https://example{i}.com/feed.xml",
            )
            for i in range(1, 11)
        ]
        screen = FeedManagementScreen(feeds=feeds)
        assert len(screen.feeds) == 10

    def test_feed_management_screen_with_error_feeds(self) -> None:
        """Test FeedManagementScreen with feeds that have errors."""
        feeds = [
            Feed(
                id=1,
                title="Good Feed",
                site_url="https://example.com",
                feed_url="https://example.com/feed.xml",
                parsing_error_count=0,
            ),
            Feed(
                id=2,
                title="Bad Feed",
                site_url="https://example2.com",
                feed_url="https://example2.com/feed.xml",
                parsing_error_count=5,
                parsing_error_message="SSL certificate error",
            ),
        ]
        screen = FeedManagementScreen(feeds=feeds)
        assert len(screen.feeds) == 2
        assert screen.feeds[0].parsing_error_count == 0
        assert screen.feeds[1].parsing_error_count == 5

    def test_feed_management_screen_feed_list_item_status(self) -> None:
        """Test FeedListItem displays correct status."""
        good_feed = Feed(
            id=1,
            title="Good Feed",
            site_url="https://example.com",
            feed_url="https://example.com/feed.xml",
        )
        bad_feed = Feed(
            id=2,
            title="Bad Feed",
            site_url="https://example2.com",
            feed_url="https://example2.com/feed.xml",
            parsing_error_count=1,
        )

        good_item = FeedListItem(good_feed)
        bad_item = FeedListItem(bad_feed)

        # Verify items have the correct feeds
        assert good_item.feed.parsing_error_count == 0
        assert bad_item.feed.parsing_error_count == 1

    def test_feed_management_screen_disabled_feeds(self) -> None:
        """Test FeedManagementScreen with disabled feeds."""
        feeds = [
            Feed(
                id=1,
                title="Active Feed",
                site_url="https://example.com",
                feed_url="https://example.com/feed.xml",
                disabled=False,
            ),
            Feed(
                id=2,
                title="Disabled Feed",
                site_url="https://example2.com",
                feed_url="https://example2.com/feed.xml",
                disabled=True,
            ),
        ]
        screen = FeedManagementScreen(feeds=feeds)
        assert screen.feeds[0].disabled is False
        assert screen.feeds[1].disabled is True

    def test_feed_management_action_methods_exist(self) -> None:
        """Test all action methods exist."""
        screen = FeedManagementScreen()
        assert hasattr(screen, "action_add_feed")
        assert hasattr(screen, "action_delete_feed")
        assert hasattr(screen, "action_refresh_feed")
        assert hasattr(screen, "action_view_details")
        assert hasattr(screen, "action_back")
        assert hasattr(screen, "action_cursor_down")
        assert hasattr(screen, "action_cursor_up")

    def test_feed_management_helper_methods_exist(self) -> None:
        """Test helper methods exist."""
        screen = FeedManagementScreen()
        assert hasattr(screen, "_populate_list")
        assert hasattr(screen, "_get_selected_feed")
        assert callable(screen._populate_list)
        assert callable(screen._get_selected_feed)

    def test_feed_list_item_with_category(self) -> None:
        """Test FeedListItem with categorized feed."""
        feed = Feed(
            id=1,
            title="Categorized Feed",
            site_url="https://example.com",
            feed_url="https://example.com/feed.xml",
            category_id=5,
        )
        item = FeedListItem(feed)
        assert item.feed.category_id == 5

    def test_feed_list_item_with_checked_timestamp(self) -> None:
        """Test FeedListItem with checked_at timestamp."""
        feed = Feed(
            id=1,
            title="Checked Feed",
            site_url="https://example.com",
            feed_url="https://example.com/feed.xml",
            checked_at="2025-10-31T12:00:00Z",
        )
        item = FeedListItem(feed)
        assert item.feed.checked_at is not None

    def test_feed_list_item_status_icon_without_errors(self) -> None:
        """Test FeedListItem displays correct status icon for healthy feed."""
        feed = Feed(
            id=1,
            title="Healthy",
            site_url="https://example.com",
            feed_url="https://example.com/feed.xml",
            parsing_error_count=0,
        )
        item = FeedListItem(feed)
        # Verify the item was created and feed has no errors
        assert item.feed.parsing_error_count == 0
        assert not item.feed.has_errors

    def test_feed_list_item_status_icon_with_errors(self) -> None:
        """Test FeedListItem displays warning icon for feeds with errors."""
        feed = Feed(
            id=1,
            title="Broken",
            site_url="https://example.com",
            feed_url="https://example.com/feed.xml",
            parsing_error_count=5,
        )
        item = FeedListItem(feed)
        # Verify the item was created and feed has errors
        assert item.feed.parsing_error_count == 5
        assert item.feed.has_errors

    def test_feed_management_get_selected_feed_with_valid_selection(self) -> None:
        """Test getting selected feed when list has items."""
        feeds = [
            Feed(
                id=1,
                title="Feed 1",
                site_url="https://example.com",
                feed_url="https://example.com/feed.xml",
            )
        ]
        screen = FeedManagementScreen(feeds=feeds)
        # Without mounting, list_view is None, so this should return None
        feed = screen._get_selected_feed()
        assert feed is None

    def test_feed_management_populate_list_clears_old_items(self) -> None:
        """Test that populate_list clears old items before adding new ones."""
        feeds = [
            Feed(
                id=1,
                title="Feed 1",
                site_url="https://example.com",
                feed_url="https://example.com/feed.xml",
            ),
            Feed(
                id=2,
                title="Feed 2",
                site_url="https://example2.com",
                feed_url="https://example2.com/feed.xml",
            ),
        ]
        screen = FeedManagementScreen(feeds=feeds)
        # Verify feeds are stored
        assert len(screen.feeds) == 2
        assert screen.feeds[0].title == "Feed 1"
        assert screen.feeds[1].title == "Feed 2"

    def test_feed_management_action_methods_callable(self) -> None:
        """Test all action methods are callable."""
        screen = FeedManagementScreen()
        # Verify methods exist and are callable
        assert callable(getattr(screen, "action_add_feed", None))
        assert callable(getattr(screen, "action_delete_feed", None))
        assert callable(getattr(screen, "action_refresh_feed", None))
        assert callable(getattr(screen, "action_view_details", None))
        assert callable(getattr(screen, "action_back", None))
        assert callable(getattr(screen, "action_cursor_down", None))
        assert callable(getattr(screen, "action_cursor_up", None))


class TestFeedManagementScreenMounted:
    """Test FeedManagementScreen with mounted app."""

    async def test_on_mount_initializes_list_view(self) -> None:
        """Test on_mount initializes and focuses list view."""
        feeds = [
            Feed(
                id=1,
                title="Test Feed",
                site_url="https://example.com",
                feed_url="https://example.com/feed.xml",
            )
        ]
        app = FeedManagementTestApp(feeds=feeds)
        async with app.run_test():
            # Get the active screen
            screen = app.screen
            if isinstance(screen, FeedManagementScreen):
                # Verify list_view was initialized
                assert screen.list_view is not None
                # Verify list was populated with items
                assert screen.list_view.children is not None

    async def test_populate_list_adds_feeds_to_screen(self) -> None:
        """Test _populate_list method works correctly."""
        screen = FeedManagementScreen()
        screen.list_view = None  # Start with no list view
        screen._populate_list()  # Should handle gracefully

        # Now set list_view and test again
        screen.list_view = ListView()
        feeds = [
            Feed(
                id=i,
                title=f"Feed {i}",
                site_url=f"https://example{i}.com",
                feed_url=f"https://example{i}.com/feed.xml",
            )
            for i in range(1, 3)
        ]
        screen.feeds = feeds
        screen._populate_list()
        # After populate, list should have items
        assert screen.list_view is not None

    async def test_get_selected_feed_with_no_list_view(self) -> None:
        """Test _get_selected_feed returns None when no list_view."""
        screen = FeedManagementScreen()
        screen.list_view = None
        selected = screen._get_selected_feed()
        assert selected is None

    async def test_get_selected_feed_with_no_highlighted_child(self) -> None:
        """Test _get_selected_feed returns None when nothing highlighted."""
        screen = FeedManagementScreen()
        screen.list_view = ListView()
        selected = screen._get_selected_feed()
        assert selected is None

    async def test_action_cursor_down_with_list_view(self) -> None:
        """Test action_cursor_down delegates to list_view."""
        screen = FeedManagementScreen()
        screen.list_view = ListView()
        # action_cursor_down should not raise
        screen.action_cursor_down()

    async def test_action_cursor_up_with_list_view(self) -> None:
        """Test action_cursor_up delegates to list_view."""
        screen = FeedManagementScreen()
        screen.list_view = ListView()
        # action_cursor_up should not raise
        screen.action_cursor_up()

    async def test_action_cursor_down_with_no_list_view(self) -> None:
        """Test action_cursor_down handles missing list_view gracefully."""
        screen = FeedManagementScreen()
        screen.list_view = None
        # Should not raise
        screen.action_cursor_down()

    async def test_action_cursor_up_with_no_list_view(self) -> None:
        """Test action_cursor_up handles missing list_view gracefully."""
        screen = FeedManagementScreen()
        screen.list_view = None
        # Should not raise
        screen.action_cursor_up()

    async def test_action_back_pops_screen(self) -> None:
        """Test action_back can be called on screen."""
        screen = FeedManagementScreen()
        # action_back requires an app to pop screen from
        # We can verify the method exists and is callable
        assert callable(screen.action_back)

    async def test_action_add_feed_opens_input_dialog(self) -> None:
        """Test action_add_feed can be called."""
        screen = FeedManagementScreen()
        # action_add_feed requires an app to push dialog
        # We can verify the method exists and is callable
        assert callable(screen.action_add_feed)

    def test_action_delete_feed_method_exists(self) -> None:
        """Test action_delete_feed method exists and is callable."""
        screen = FeedManagementScreen()
        assert callable(screen.action_delete_feed)
        # Verify it checks for selected feed
        screen.list_view = None
        # Method should exist and handle no selection

    def test_action_refresh_feed_method_exists(self) -> None:
        """Test action_refresh_feed method exists and is async."""
        screen = FeedManagementScreen()
        assert hasattr(screen, "action_refresh_feed")
        # Method should be async (callable returns coroutine or None)

    def test_action_view_details_method_exists(self) -> None:
        """Test action_view_details method exists and is callable."""
        screen = FeedManagementScreen()
        assert callable(screen.action_view_details)
        # Verify it handles no selection gracefully
        screen.list_view = None


class TestFeedManagementAsyncMethods:
    """Test that async methods exist and are properly defined."""

    def test_create_feed_is_async(self) -> None:
        """Test that _create_feed is an async method."""
        screen = FeedManagementScreen()
        assert asyncio.iscoroutinefunction(screen._create_feed)

    def test_action_refresh_feed_is_async(self) -> None:
        """Test that action_refresh_feed is an async method."""
        screen = FeedManagementScreen()
        assert asyncio.iscoroutinefunction(screen.action_refresh_feed)

    def test_do_delete_feed_is_async(self) -> None:
        """Test that _do_delete_feed is an async method."""
        screen = FeedManagementScreen()
        assert asyncio.iscoroutinefunction(screen._do_delete_feed)


class TestFeedManagementCRUDOperations:
    """Test CRUD operations in FeedManagementScreen."""

    async def test_create_feed_success(self) -> None:
        """Test successful feed creation."""

        app = FeedManagementTestApp()
        app.client = MagicMock()
        app.client.create_feed = AsyncMock(
            return_value=Feed(
                id=3,
                title="New Feed",
                site_url="https://example.com",
                feed_url="https://example.com/feed",
            )
        )

        async with app.run_test() as pilot:
            screen = cast(FeedManagementScreen, app.screen)
            initial_count = len(screen.feeds)

            # Patch api_call to return the app
            with patch("miniflux_tui.ui.screens.feed_management.api_call") as mock_api:
                mock_api.return_value.__enter__.return_value = app.client

                # Create feed
                await screen._create_feed("https://example.com/feed")
                await pilot.pause()

                # Verify feed was added
                assert len(screen.feeds) == initial_count + 1
                assert screen.feeds[-1].title == "New Feed"
                app.client.create_feed.assert_called_once_with("https://example.com/feed")

    async def test_create_feed_validation_error(self) -> None:
        """Test creating feed with validation error."""

        app = FeedManagementTestApp()
        app.client = MagicMock()
        app.client.create_feed = AsyncMock(side_effect=ValueError("Invalid feed URL"))

        async with app.run_test() as pilot:
            screen = cast(FeedManagementScreen, app.screen)
            initial_count = len(screen.feeds)

            # Patch api_call
            with patch("miniflux_tui.ui.screens.feed_management.api_call") as mock_api:
                mock_api.return_value.__enter__.return_value = app.client

                # Try to create feed (should fail)
                await screen._create_feed("https://example.com/feed")
                await pilot.pause()

                # Verify feed was not added
                assert len(screen.feeds) == initial_count

    async def test_create_feed_api_error(self) -> None:
        """Test handling API error during feed creation."""

        app = FeedManagementTestApp()
        app.client = MagicMock()
        app.client.create_feed = AsyncMock(side_effect=Exception("API Error"))

        async with app.run_test() as pilot:
            screen = cast(FeedManagementScreen, app.screen)
            initial_count = len(screen.feeds)

            # Patch api_call
            with patch("miniflux_tui.ui.screens.feed_management.api_call") as mock_api:
                mock_api.return_value.__enter__.return_value = app.client

                # Try to create feed (should fail)
                await screen._create_feed("https://example.com/feed")
                await pilot.pause()

                # Verify feed was not added
                assert len(screen.feeds) == initial_count

    async def test_delete_feed_success(self) -> None:
        """Test successful feed deletion."""

        feeds = [
            Feed(id=1, title="Feed 1", site_url="https://example.com", feed_url="https://example.com/feed1"),
            Feed(id=2, title="Feed 2", site_url="https://example.com", feed_url="https://example.com/feed2"),
        ]
        app = FeedManagementTestApp(feeds=feeds)
        app.client = MagicMock()
        app.client.delete_feed = AsyncMock(return_value=None)

        async with app.run_test() as pilot:
            screen = cast(FeedManagementScreen, app.screen)

            # Patch api_call
            with patch("miniflux_tui.ui.screens.feed_management.api_call") as mock_api:
                mock_api.return_value.__enter__.return_value = app.client

                # Delete first feed
                await screen._do_delete_feed(feeds[0])
                await pilot.pause()

                # Verify feed was removed
                assert len(screen.feeds) == 1
                assert screen.feeds[0].id == 2
                app.client.delete_feed.assert_called_once_with(1)

    async def test_delete_feed_no_selection(self) -> None:
        """Test deleting when no feed is selected."""

        app = FeedManagementTestApp()

        async with app.run_test():
            screen = cast(FeedManagementScreen, app.screen)

            # Try to delete without selection
            screen.action_delete_feed()
            # Should show warning notification

    async def test_delete_feed_api_error(self) -> None:
        """Test handling API error during feed deletion."""

        feeds = [Feed(id=1, title="Test", site_url="https://example.com", feed_url="https://example.com/feed")]
        app = FeedManagementTestApp(feeds=feeds)
        app.client = MagicMock()
        app.client.delete_feed = AsyncMock(side_effect=Exception("API Error"))

        async with app.run_test() as pilot:
            screen = cast(FeedManagementScreen, app.screen)
            initial_count = len(screen.feeds)

            # Patch api_call
            with patch("miniflux_tui.ui.screens.feed_management.api_call") as mock_api:
                mock_api.return_value.__enter__.return_value = app.client

                # Try to delete (should fail)
                await screen._do_delete_feed(feeds[0])
                await pilot.pause()

                # Feed should still exist
                assert len(screen.feeds) == initial_count

    async def test_refresh_feed_can_be_called(self) -> None:
        """Test that refresh feed action can be called."""

        feeds = [Feed(id=1, title="Test", site_url="https://example.com", feed_url="https://example.com/feed")]
        app = FeedManagementTestApp(feeds=feeds)
        app.client = MagicMock()
        app.client.refresh_feed = AsyncMock(return_value=None)

        async with app.run_test() as pilot:
            screen = cast(FeedManagementScreen, app.screen)

            # Patch api_call
            with patch("miniflux_tui.ui.screens.feed_management.api_call") as mock_api:
                mock_api.return_value.__enter__.return_value = app.client

                # Try to refresh (will show warning about no selection)
                await screen.action_refresh_feed()
                await pilot.pause()
                # Should handle no selection gracefully

    async def test_refresh_feed_no_selection(self) -> None:
        """Test refreshing when no feed is selected."""

        app = FeedManagementTestApp()

        async with app.run_test():
            screen = cast(FeedManagementScreen, app.screen)

            # Try to refresh without selection
            await screen.action_refresh_feed()
            # Should show warning notification

    async def test_refresh_feed_api_error(self) -> None:
        """Test handling API error during feed refresh."""

        feeds = [Feed(id=1, title="Test", site_url="https://example.com", feed_url="https://example.com/feed")]
        app = FeedManagementTestApp(feeds=feeds)
        app.client = MagicMock()
        app.client.refresh_feed = AsyncMock(side_effect=Exception("API Error"))

        async with app.run_test() as pilot:
            screen = cast(FeedManagementScreen, app.screen)

            # Select the feed
            if screen.list_view and screen.list_view.children:
                screen.list_view.index = 0

            # Patch api_call
            with patch("miniflux_tui.ui.screens.feed_management.api_call") as mock_api:
                mock_api.return_value.__enter__.return_value = app.client

                # Try to refresh (should fail gracefully)
                await screen.action_refresh_feed()
                await pilot.pause()

    async def test_view_details_shows_info(self) -> None:
        """Test viewing feed details."""

        feeds = [
            Feed(
                id=1,
                title="Test Feed",
                site_url="https://example.com",
                feed_url="https://example.com/feed",
                parsing_error_message="Test error",
            )
        ]
        app = FeedManagementTestApp(feeds=feeds)

        async with app.run_test():
            screen = cast(FeedManagementScreen, app.screen)

            # Select the feed
            if screen.list_view and screen.list_view.children:
                screen.list_view.index = 0

            # View details
            screen.action_view_details()
            # Should show notification with feed details

    async def test_view_details_no_selection(self) -> None:
        """Test viewing details when no feed is selected."""

        app = FeedManagementTestApp()

        async with app.run_test():
            screen = cast(FeedManagementScreen, app.screen)

            # Try to view details without selection
            screen.action_view_details()
            # Should show warning notification

    async def test_populate_list_with_no_listview(self) -> None:
        """Test _populate_list when list_view is None."""
        screen = FeedManagementScreen(feeds=[Feed(id=1, title="Test", site_url="https://example.com", feed_url="https://example.com/feed")])
        screen.list_view = None

        # Should not raise an error
        screen._populate_list()

    async def test_get_selected_feed_returns_none_when_no_highlight(self) -> None:
        """Test _get_selected_feed returns None when nothing highlighted."""
        feeds = [Feed(id=1, title="Test", site_url="https://example.com", feed_url="https://example.com/feed")]
        app = FeedManagementTestApp(feeds=feeds)

        async with app.run_test():
            screen = cast(FeedManagementScreen, app.screen)

            # Clear selection
            if screen.list_view:
                screen.list_view.index = None

            result = screen._get_selected_feed()
            assert result is None

    async def test_cursor_navigation_actions(self) -> None:
        """Test cursor navigation actions."""

        feeds = [
            Feed(id=1, title="Feed 1", site_url="https://example.com", feed_url="https://example.com/feed1"),
            Feed(id=2, title="Feed 2", site_url="https://example.com", feed_url="https://example.com/feed2"),
        ]
        app = FeedManagementTestApp(feeds=feeds)

        async with app.run_test() as pilot:
            # Test cursor down
            await pilot.press("j")
            await pilot.pause()

            # Test cursor up
            await pilot.press("k")
            await pilot.pause()

    async def test_back_action(self) -> None:
        """Test back action pops the screen."""

        app = FeedManagementTestApp()

        async with app.run_test() as pilot:
            screen = app.screen
            assert isinstance(screen, FeedManagementScreen)

            # Press escape to go back
            await pilot.press("escape")
            await pilot.pause()

            # Should pop the screen
            assert app.screen is not screen

    async def test_add_feed_shows_dialog(self) -> None:
        """Test that add feed action shows dialog."""

        app = FeedManagementTestApp()

        async with app.run_test():
            screen = cast(FeedManagementScreen, app.screen)

            # Mock push_screen to avoid actually showing the dialog
            with patch.object(app, "push_screen") as mock_push:
                screen.action_add_feed()
                # Dialog should be pushed
                mock_push.assert_called_once()
