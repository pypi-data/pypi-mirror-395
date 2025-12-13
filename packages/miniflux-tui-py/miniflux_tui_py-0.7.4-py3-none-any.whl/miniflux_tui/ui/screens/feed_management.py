# SPDX-License-Identifier: MIT
"""Feed management screen for viewing and managing feeds."""

import asyncio
from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView

from miniflux_tui.api.models import Feed
from miniflux_tui.security import sanitize_error_message, validate_feed_url
from miniflux_tui.ui.screens.confirm_dialog import ConfirmDialog
from miniflux_tui.ui.screens.input_dialog import InputDialog
from miniflux_tui.utils import api_call


class FeedListItem(ListItem):
    """Custom list item for displaying a feed with metadata.

    Attributes:
        feed: The Feed object to display
    """

    def __init__(self, feed: Feed):
        """Initialize feed list item.

        Args:
            feed: Feed object to display
        """
        self.feed = feed

        # Build display label with status indicators
        status_icon = "⚠️" if feed.has_errors else "✓"
        disabled_flag = " [disabled]" if feed.disabled else ""

        # Truncate title if too long
        title = feed.title[:40]
        label_text = f"{status_icon} {title}{disabled_flag}"

        super().__init__(Label(label_text))


class FeedManagementScreen(Screen):
    """Screen for managing feeds (add, edit, delete, view status).

    Features:
    - List all feeds with status indicators
    - Add new feeds by URL
    - View feed details and errors
    - Delete feeds with confirmation
    - Refresh individual feeds
    """

    BINDINGS: ClassVar = [
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("up", "cursor_up", "Up", show=False),
        Binding("n", "add_feed", "Add Feed"),
        Binding("d", "delete_feed", "Delete"),
        Binding("r", "refresh_feed", "Refresh"),
        Binding("enter", "view_details", "Details"),
        Binding("escape", "back", "Back"),
    ]

    CSS = """
    FeedManagementScreen {
        layout: vertical;
    }

    FeedManagementScreen > Header {
        dock: top;
    }

    FeedManagementScreen > Footer {
        dock: bottom;
    }

    FeedManagementScreen #feed-list {
        border: solid $accent;
        height: 1fr;
    }

    FeedManagementScreen ListItem {
        padding: 0 1;
        height: 1;
    }

    FeedManagementScreen ListItem Label {
        width: 1fr;
    }
    """

    def __init__(self, feeds: list[Feed] | None = None, **kwargs):
        """Initialize feed management screen.

        Args:
            feeds: List of feeds to display
        """
        super().__init__(**kwargs)
        self.feeds = feeds or []
        self.list_view: ListView | None = None

    def compose(self) -> ComposeResult:
        """Create screen layout."""
        yield Header(show_clock=False)
        with Container():
            yield ListView(id="feed-list")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize screen."""
        self.list_view = self.query_one("#feed-list", ListView)
        self._populate_list()
        self.list_view.focus()

    def _populate_list(self) -> None:
        """Populate feed list with items."""
        if not self.list_view:
            return

        self.list_view.clear()
        for feed in self.feeds:
            self.list_view.append(FeedListItem(feed))

    def _get_selected_feed(self) -> Feed | None:
        """Get currently selected feed.

        Returns:
            Selected Feed or None if no selection
        """
        if not self.list_view or self.list_view.highlighted_child is None:
            return None

        highlighted = self.list_view.highlighted_child
        if isinstance(highlighted, FeedListItem):
            return highlighted.feed

        return None

    def action_add_feed(self) -> None:
        """Open dialog to add a new feed."""

        def on_submit(url: str) -> None:
            url = url.strip()

            # Validate URL format and prevent SSRF attacks
            is_valid, error_msg = validate_feed_url(url)
            if not is_valid:
                self.app.notify(f"Invalid URL: {error_msg}", severity="error")
                return

            # Create feed in background
            asyncio.create_task(self._create_feed(url))  # noqa: RUF006

        self.app.push_screen(
            InputDialog(
                title="Add Feed",
                label="Enter feed URL or website URL:",
                on_submit=on_submit,
            )
        )

    async def _create_feed(self, url: str) -> None:
        """Create a new feed from URL.

        Args:
            url: Feed URL or website URL
        """
        with api_call(self.app, "creating feed") as client:
            if client is None:
                return

            try:
                feed = await client.create_feed(url)
                self.feeds.append(feed)
                self._populate_list()
                self.app.notify(f"Feed '{feed.title}' added successfully")
            except ValueError as e:
                # Log full error for debugging
                self.app.log(f"ValueError creating feed: {e}")
                # Show safe message to user
                self.app.notify(sanitize_error_message(e, "adding feed"), severity="error")
            except Exception as e:
                # Log full error for debugging
                self.app.log(f"Error creating feed: {e}")
                # Show safe message to user
                self.app.notify(sanitize_error_message(e, "adding feed"), severity="error")

    def action_delete_feed(self) -> None:
        """Delete the selected feed with confirmation."""
        feed = self._get_selected_feed()
        if not feed:
            self.app.notify("No feed selected", severity="warning")
            return

        def on_confirm() -> None:
            asyncio.create_task(self._do_delete_feed(feed))  # noqa: RUF006

        self.app.push_screen(
            ConfirmDialog(
                title="Delete Feed?",
                message=f"Delete '{feed.title}'?\nThis cannot be undone.",
                on_confirm=on_confirm,
                confirm_label="Delete",
                cancel_label="Cancel",
            )
        )

    async def _do_delete_feed(self, feed: Feed) -> None:
        """Actually delete the feed.

        Args:
            feed: Feed to delete
        """
        with api_call(self.app, "deleting feed") as client:
            if client is None:
                return

            try:
                await client.delete_feed(feed.id)
                self.feeds.remove(feed)
                self._populate_list()
                self.app.notify(f"Feed '{feed.title}' deleted")
            except Exception as e:
                # Log full error for debugging
                self.app.log(f"Error deleting feed: {e}")
                # Show safe message to user
                self.app.notify(sanitize_error_message(e, "deleting feed"), severity="error")

    async def action_refresh_feed(self) -> None:
        """Refresh the selected feed."""
        feed = self._get_selected_feed()
        if not feed:
            self.app.notify("No feed selected", severity="warning")
            return

        with api_call(self.app, "refreshing feed") as client:
            if client is None:
                return

            try:
                await client.refresh_feed(feed.id)
                self.app.notify(f"Feed '{feed.title}' refreshed")
            except Exception as e:
                # Log full error for debugging
                self.app.log(f"Error refreshing feed: {e}")
                # Show safe message to user
                self.app.notify(sanitize_error_message(e, "refreshing feed"), severity="error")

    def action_view_details(self) -> None:
        """View details of selected feed (TODO: implement feed details screen)."""
        feed = self._get_selected_feed()
        if not feed:
            self.app.notify("No feed selected", severity="warning")
            return

        # TODO: Push to feed details screen
        detail_text = f"""Feed: {feed.title}
URL: {feed.feed_url}
Site: {feed.site_url}
Errors: {feed.parsing_error_count}
Last checked: {feed.checked_at or "Never"}
Status: {"Disabled" if feed.disabled else "Active"}"""

        self.app.notify(detail_text)

    def action_cursor_down(self) -> None:
        """Move cursor down in feed list."""
        if self.list_view:
            self.list_view.action_cursor_down()

    def action_cursor_up(self) -> None:
        """Move cursor up in feed list."""
        if self.list_view:
            self.list_view.action_cursor_up()

    def action_back(self) -> None:
        """Return to entry list."""
        self.app.pop_screen()
