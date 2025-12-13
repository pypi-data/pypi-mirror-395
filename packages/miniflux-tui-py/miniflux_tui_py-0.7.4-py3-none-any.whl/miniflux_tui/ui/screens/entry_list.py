# SPDX-License-Identifier: MIT
"""Entry list screen with feed sorting capabilities."""

import asyncio
from contextlib import suppress
from typing import TYPE_CHECKING, Any, cast

from textual import events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView

from miniflux_tui.api.models import Category, Entry
from miniflux_tui.constants import (
    DEFAULT_ENTRY_LIMIT,
    FOLD_COLLAPSED,
    FOLD_EXPANDED,
    SORT_MODES,
)
from miniflux_tui.performance import ScreenRefreshOptimizer
from miniflux_tui.utils import api_call, get_star_icon, get_status_icon

if TYPE_CHECKING:
    MinifluxTuiApp = Any


class CollapsibleListView(ListView):
    """Custom ListView that skips collapsed items when navigating with arrow keys."""

    @staticmethod
    def _is_item_visible(item: ListItem) -> bool:
        """Check if an item is visible (not hidden by CSS class)."""
        return "collapsed" not in item.classes

    def action_cursor_down(self) -> None:
        """Move cursor down to next visible item, skipping collapsed ones."""
        if len(self.children) == 0:
            return

        current_index = self.index
        if current_index is None:
            current_index = -1

        # Find next visible item
        for i in range(current_index + 1, len(self.children)):
            widget = self.children[i]
            if isinstance(widget, ListItem) and self._is_item_visible(widget):
                self.index = i
                return

    def action_cursor_up(self) -> None:
        """Move cursor up to previous visible item, skipping collapsed ones."""
        if len(self.children) == 0:
            return

        current_index = self.index
        if current_index is None:
            current_index = len(self.children)

        # Find previous visible item
        for i in range(current_index - 1, -1, -1):
            widget = self.children[i]
            if isinstance(widget, ListItem) and self._is_item_visible(widget):
                self.index = i
                return


class EntryListItem(ListItem):
    """Custom list item for displaying a feed entry."""

    def __init__(self, entry: Entry, unread_color: str = "cyan", read_color: str = "gray"):
        self.entry = entry
        self.unread_color = unread_color
        self.read_color = read_color

        # Format the entry display
        status_icon = get_status_icon(entry.is_unread)
        star_icon = get_star_icon(entry.starred)

        # Determine color based on read status
        color = unread_color if entry.is_unread else read_color

        # Create the label text with color markup
        label_text = f"[{color}]{status_icon} {star_icon} {entry.feed.title} | {entry.title}[/{color}]"

        # Initialize with the label
        super().__init__(Label(label_text))


class FeedHeaderItem(ListItem):
    """Custom list item for feed header with fold/unfold capability."""

    def __init__(
        self,
        feed_title: str,
        is_expanded: bool = True,
        category_title: str | None = None,
        has_errors: bool = False,
        feed_disabled: bool = False,
        unread_count: int = 0,
        total_count: int = 0,
    ):
        self.feed_title = feed_title
        self.is_expanded = is_expanded
        self.category_title = category_title
        self.has_errors = has_errors
        self.feed_disabled = feed_disabled
        self.unread_count = unread_count
        self.total_count = total_count

        # Format header with fold indicator, category, and error indicators
        fold_icon = FOLD_EXPANDED if is_expanded else FOLD_COLLAPSED
        error_indicators = []

        if feed_disabled:
            error_indicators.append("[red]⊘ DISABLED[/red]")
        elif has_errors:
            error_indicators.append("[yellow]⚠ ERRORS[/yellow]")

        error_text = " ".join(error_indicators)
        count_text = f"[dim]({unread_count} unread / {total_count} total)[/dim]" if total_count > 0 else ""

        if category_title:
            category_part = f"[dim]({category_title})[/dim]"
            if error_text:
                header_text = f"[bold]{fold_icon} {feed_title}[/bold] {category_part} {count_text} {error_text}".strip()
            else:
                header_text = f"[bold]{fold_icon} {feed_title}[/bold] {category_part} {count_text}".strip()
        elif error_text:
            header_text = f"[bold]{fold_icon} {feed_title}[/bold] {count_text} {error_text}".strip()
        else:
            header_text = f"[bold]{fold_icon} {feed_title}[/bold] {count_text}".strip()

        label = Label(header_text, classes="feed-header")

        # Initialize with the label
        super().__init__(label)

    def toggle_fold(self) -> None:
        """Toggle the fold state and update display."""
        self.is_expanded = not self.is_expanded
        fold_icon = FOLD_EXPANDED if self.is_expanded else FOLD_COLLAPSED

        error_indicators = []
        if self.feed_disabled:
            error_indicators.append("[red]⊘ DISABLED[/red]")
        elif self.has_errors:
            error_indicators.append("[yellow]⚠ ERRORS[/yellow]")

        error_text = " ".join(error_indicators)
        count_text = f"[dim]({self.unread_count} unread / {self.total_count} total)[/dim]" if self.total_count > 0 else ""

        if self.category_title:
            category_part = f"[dim]({self.category_title})[/dim]"
            if error_text:
                header_text = f"[bold]{fold_icon} {self.feed_title}[/bold] {category_part} {count_text} {error_text}".strip()
            else:
                header_text = f"[bold]{fold_icon} {self.feed_title}[/bold] {category_part} {count_text}".strip()
        elif error_text:
            header_text = f"[bold]{fold_icon} {self.feed_title}[/bold] {count_text} {error_text}".strip()
        else:
            header_text = f"[bold]{fold_icon} {self.feed_title}[/bold] {count_text}".strip()

        # Update the label
        if self.children:
            cast(Label, self.children[0]).update(header_text)


class CategoryHeaderItem(ListItem):
    """Custom list item for category header with fold/unfold capability and entry counts."""

    def __init__(self, category_title: str, is_expanded: bool = True, unread_count: int = 0, read_count: int = 0):
        self.category_title = category_title
        self.is_expanded = is_expanded
        self.unread_count = unread_count
        self.read_count = read_count

        # Format header with fold indicator and counts
        fold_icon = FOLD_EXPANDED if is_expanded else FOLD_COLLAPSED
        total = unread_count + read_count
        if total > 0:
            counts = f"({unread_count} unread / {total} total)"
            header_text = f"[bold cyan]{fold_icon} [CATEGORY] {category_title} {counts}[/bold cyan]"
        else:
            header_text = f"[bold cyan]{fold_icon} [CATEGORY] {category_title}[/bold cyan]"
        label = Label(header_text, classes="category-header")

        # Initialize with the label
        super().__init__(label)

    def toggle_fold(self) -> None:
        """Toggle the fold state and update display."""
        self.is_expanded = not self.is_expanded
        fold_icon = FOLD_EXPANDED if self.is_expanded else FOLD_COLLAPSED
        total = self.unread_count + self.read_count
        if total > 0:
            counts = f"({self.unread_count} unread / {total} total)"
            header_text = f"[bold cyan]{fold_icon} [CATEGORY] {self.category_title} {counts}[/bold cyan]"
        else:
            header_text = f"[bold cyan]{fold_icon} [CATEGORY] {self.category_title}[/bold cyan]"
        # Update the label
        if self.children:
            cast(Label, self.children[0]).update(header_text)


class EntryListScreen(Screen):
    """Screen for displaying a list of feed entries with sorting."""

    BINDINGS = [  # noqa: RUF012
        # Navigation (vim-style)
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("n", "cursor_down", "Next Item", show=False),
        Binding("p", "cursor_up", "Previous Item", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("up", "cursor_up", "Up", show=False),
        # Entry selection and actions
        Binding("enter", "select_entry", "Open Entry"),
        Binding("m", "toggle_read", "Mark Read/Unread"),
        Binding("M", "toggle_read_previous", "Mark Read/Unread (Focus Prev)", show=False),
        Binding("f", "toggle_star", "Toggle Starred"),
        Binding("e", "save_entry", "Save Entry"),
        Binding("A", "mark_all_as_read", "Mark All as Read", show=False),
        # Grouping and collapsing (note: g-prefix now used for section nav)
        Binding("s", "cycle_sort", "Cycle Sort"),
        Binding("w", "toggle_group_feed", "Group by Feed", show=False),
        Binding("C", "toggle_group_category", "Group by Category", show=False),
        Binding("shift+l", "expand_all", "Expand All", show=False),
        Binding("Z", "collapse_all", "Collapse All"),
        Binding("G", "go_to_bottom", "Go to Bottom", show=False),
        Binding("h", "collapse_fold", "Collapse Feed/Category"),
        Binding("l", "expand_fold", "Expand Feed/Category"),
        Binding("left", "collapse_fold", "Collapse Feed/Category", show=False),
        Binding("right", "expand_fold", "Expand Feed/Category", show=False),
        # Feed operations
        Binding("r", "refresh", "Refresh Current Feed"),
        Binding("R", "refresh_all_feeds", "Refresh All Feeds"),
        Binding("comma", "sync_entries", "Sync Entries", show=False),
        # Section navigation (g prefix)
        Binding("g", "g_prefix_mode", "Section Navigation", show=False),
        # Feed settings
        Binding("X", "feed_settings", "Feed Settings"),
        # Search and help
        Binding("slash", "search", "Search"),
        Binding("question_mark", "show_help", "Help"),
        # Mode-specific (these are handled by g_prefix_mode)
        # g+u = unread, g+b = starred, g+c = categories, g+f = feeds, g+h = history, g+s = settings
        # Status, settings, history (also accessible via g-prefix, but keep for compatibility)
        Binding("i", "show_status", "Status"),
        Binding("H", "show_history", "History"),
        Binding("S", "show_settings", "Settings"),
        Binding("T", "toggle_theme", "Toggle Theme"),
        Binding("q", "quit", "Quit"),
    ]

    app: "MinifluxTuiApp"

    def __init__(
        self,
        entries: list[Entry],
        categories: list[Category] | None = None,
        *,
        unread_color: str = "cyan",
        read_color: str = "gray",
        default_sort: str = "date",
        group_by_feed: bool = False,
        group_collapsed: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.entries = entries
        self.categories = categories or []
        self.sorted_entries = entries.copy()  # Store sorted entries for navigation
        self.unread_color = unread_color
        self.read_color = read_color
        self.current_sort = default_sort
        self.group_by_feed = group_by_feed
        self.group_by_category = False  # Option to group by category instead of feed
        self.group_collapsed = group_collapsed  # Start feeds collapsed in grouped mode
        self.filter_unread_only = False  # Filter to show only unread entries
        self.filter_starred_only = False  # Filter to show only starred entries
        self.filter_category_id: int | None = None  # Filter to show entries from selected category only
        self.search_active = False  # Flag to indicate search is active
        self.search_term = ""  # Current search term
        self.list_view: CollapsibleListView | None = None
        self.displayed_items: list[ListItem] = []  # Track items in display order
        self.refresh_optimizer = ScreenRefreshOptimizer()  # Track refresh performance
        self.entry_item_map: dict[int, EntryListItem] = {}  # Map entry IDs to list items
        self.feed_header_map: dict[str, FeedHeaderItem] = {}  # Map feed names to header items
        self.category_header_map: dict[str, CategoryHeaderItem] = {}  # Map category names to header items
        self.feed_fold_state: dict[str, bool] = {}  # Track fold state per feed (True = expanded)
        self.category_fold_state: dict[str, bool] = {}  # Track fold state per category (True = expanded)
        self.last_highlighted_feed: str | None = None  # Track last highlighted feed for position persistence
        self.last_highlighted_category: str | None = None  # Track last highlighted category for position persistence
        self.last_highlighted_entry_id: int | None = None  # Track last highlighted entry ID for position
        self.last_cursor_index: int = 0  # Track cursor position for non-grouped mode
        self._is_initial_mount: bool = True  # Track if this is the first time mounting the screen
        self._header_widget: Header | None = None
        self._footer_widget: Footer | None = None
        # Loading animation state
        self._loading_animation_timer = None  # Timer for loading animation
        self._loading_animation_frame = 0  # Current animation frame
        self._loading_animation_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]  # Spinner frames
        self._loading_message = ""  # Message to show during loading
        self._g_prefix_mode = False  # Flag to track if waiting for g-prefix command

    def _safe_log(self, message: str) -> None:
        """Safely log a message, handling cases where app is not available."""
        # Silently ignore logging errors (e.g., in tests without app context)
        with suppress(Exception):
            self.log(message)

    def _start_loading_animation(self, message: str = "Loading") -> None:
        """Start the loading animation in the subtitle.

        Args:
            message: The message to display with the spinner
        """
        self._loading_message = message
        self._loading_animation_frame = 0
        # Update subtitle with first frame
        self._update_loading_animation()
        # Start timer to update animation every 100ms
        self._loading_animation_timer = self.set_interval(0.1, self._update_loading_animation)

    def _update_loading_animation(self) -> None:
        """Update the loading animation frame."""
        if not self._loading_message:
            return

        # Get current spinner frame
        spinner = self._loading_animation_frames[self._loading_animation_frame]
        # Update subtitle with spinner and message (safely handle if screen is unmounted)
        with suppress(Exception):
            self.sub_title = f"{spinner} {self._loading_message}"
        # Move to next frame (loop back to 0 after last frame)
        self._loading_animation_frame = (self._loading_animation_frame + 1) % len(self._loading_animation_frames)

    def _stop_loading_animation(self) -> None:
        """Stop the loading animation and clear the subtitle."""
        # Stop the timer if it exists
        if self._loading_animation_timer:
            with suppress(Exception):
                self._loading_animation_timer.stop()
            self._loading_animation_timer = None
        # Clear the subtitle (safely handle if screen is unmounted)
        with suppress(Exception):
            self.sub_title = ""
        self._loading_message = ""
        self._loading_animation_frame = 0

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        header = Header()
        list_view = CollapsibleListView()
        footer = Footer()

        # Store references for later use (e.g. focus management)
        self._header_widget = header
        self.list_view = list_view
        self._footer_widget = footer

        yield header
        yield list_view
        yield footer

    def on_mount(self) -> None:
        """Called when screen is mounted."""
        # Get reference to the ListView after it's mounted
        self.list_view = self.query_one(CollapsibleListView)
        self._safe_log(f"on_mount: list_view is now {self.list_view}")

        # Only populate if we have entries
        if self.entries:
            self._safe_log(f"on_mount: Populating with {len(self.entries)} entries")
            # _populate_list() now handles cursor restoration via call_later
            self._populate_list()
            # Note: _is_initial_mount is cleared in on_screen_resume after first display
        else:
            self._safe_log("on_mount: No entries yet, skipping initial population")

    def on_unmount(self) -> None:
        """Called when screen is unmounted - cleanup resources."""
        # Stop loading animation timer if it's running
        self._stop_loading_animation()

    def on_screen_resume(self) -> None:
        """Called when screen is resumed (e.g., after returning from entry reader)."""
        # On first resume (after on_mount), skip population and just clear the flag
        # on_mount already populated the list
        if self._is_initial_mount:
            self._safe_log("on_screen_resume: initial mount, clearing flag and skipping population")
            self._is_initial_mount = False
            return

        # Refresh the list to reflect any status changes when returning from other screens
        if self.entries and self.list_view:
            # _populate_list() now handles cursor restoration and focus via call_later
            self._populate_list()
        elif self.list_view and len(self.list_view.children) > 0:
            # If no entries, just ensure focus
            self.call_later(self._ensure_focus)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle ListView selection (Enter key)."""
        if event.item and isinstance(event.item, FeedHeaderItem):
            # Open first entry in the selected feed
            self._open_first_entry_by_feed(event.item.feed_title)
        elif event.item and isinstance(event.item, CategoryHeaderItem):
            # Open first entry in the selected category
            self._open_first_entry_by_category(event.item.category_title)
        elif event.item and isinstance(event.item, EntryListItem):
            # Open the selected entry directly
            self._open_entry(event.item.entry)

    def _open_first_entry_by_feed(self, feed_title: str) -> None:
        """Find and open the first entry in a feed."""
        for entry in self.sorted_entries:
            if entry.feed.title == feed_title:
                self._open_entry(entry)
                return

    def _open_first_entry_by_category(self, category_title: str) -> None:
        """Find and open the first entry in a category."""
        for entry in self.sorted_entries:
            if self._get_category_title(entry.feed.category_id) == category_title:
                self._open_entry(entry)
                return

    def _build_group_info(self) -> dict[str, str | int] | None:
        """Build group info dictionary based on current grouping mode.

        Returns:
            Dictionary with 'mode' key ('feed' or 'category'), or None if not grouped
        """
        if self.group_by_feed:
            return {"mode": "feed"}
        if self.group_by_category:
            return {"mode": "category"}
        return None

    def _open_entry(self, entry: Entry) -> None:
        """Open an entry in the entry reader screen."""
        # Save the entry for position restoration
        self.last_highlighted_feed = entry.feed.title
        self.last_highlighted_entry_id = entry.id

        # Save the cursor index in the list view
        if self.list_view and self.list_view.index is not None:
            self.last_cursor_index = self.list_view.index

        # Find the index of this entry in the sorted entry list
        entry_index = 0
        for i, e in enumerate(self.sorted_entries):
            if e.id == entry.id:
                entry_index = i
                break

        # Prepare group info if in grouped mode
        group_info = self._build_group_info()

        # Open entry reader screen with navigation context
        if isinstance(self.app, self.app.__class__) and hasattr(self.app, "push_entry_reader"):
            self.app.push_entry_reader(
                entry=entry,
                entry_list=self.sorted_entries,
                current_index=entry_index,
                group_info=group_info,
            )

    def _populate_list(self):
        """Populate the list with sorted and filtered entries."""
        if not self._ensure_list_view():
            return

        # Log the current index before clearing
        self._safe_log(f"_populate_list: current index before clear = {self.list_view.index}")
        self._safe_log(f"_populate_list: current children count before clear = {len(self.list_view.children)}")

        self.list_view.clear()

        # Log after clearing
        self._safe_log(f"_populate_list: current index after clear = {self.list_view.index}")
        self._safe_log(f"_populate_list: current children count after clear = {len(self.list_view.children)}")

        # CRITICAL: Reset index to None after clearing to ensure clean state
        # This prevents issues where the old index persists after clearing
        self.list_view.index = None  # type: ignore[assignment]
        self._safe_log("_populate_list: reset index to None")

        sorted_entries = self._get_sorted_entries()
        self.sorted_entries = sorted_entries
        self._display_entries(sorted_entries)

        # Log after adding entries
        self._safe_log(f"_populate_list: current children count after display = {len(self.list_view.children)}")
        self._safe_log(f"_populate_list: current index after display = {self.list_view.index}")
        self._safe_log(f"_populate_list: highlighted_child = {self.list_view.highlighted_child}")

        self.refresh_optimizer.track_full_refresh()

        # Restore cursor position after list is updated
        # This ensures cursor is initialized even when called directly (e.g., from tests)
        # Uses call_later to defer until ListView has fully updated
        # On initial mount, use simple positioning; otherwise restore previous position
        if self._is_initial_mount:
            self.call_later(self._set_initial_position_and_focus)
        else:
            self.call_later(self._restore_cursor_position_and_focus)

    def _find_entry_index_by_id(self, entry_id: int | None) -> int | None:
        """Find the index of an entry by its ID.

        Searches the list view for an EntryListItem with matching entry ID.
        Returns None if not found or if entry_id is not set.

        Args:
            entry_id: ID of the entry to find

        Returns:
            Index of the entry in list view, or None if not found
        """
        if not entry_id:
            return None

        for i, child in enumerate(self.list_view.children):
            if isinstance(child, EntryListItem) and child.entry.id == entry_id:
                return i

        return None

    def _find_feed_header_index(self, feed_title: str | None) -> int | None:
        """Find the index of a feed header by title.

        Searches the list view for a FeedHeaderItem with matching feed title.
        Returns None if not found or feed not in map.

        Args:
            feed_title: Title of the feed to find

        Returns:
            Index of the feed header in list view, or None if not found
        """
        if not feed_title or not self.group_by_feed or feed_title not in self.feed_header_map:
            return None

        feed_header = self.feed_header_map[feed_title]
        for i, child in enumerate(self.list_view.children):
            if child is feed_header:
                return i

        return None

    def _set_cursor_to_index(self, index: int) -> bool:
        """Safely set cursor to a specific index.

        Handles boundary checking and suppresses exceptions.
        Scrolls the entry to center of viewport for better visibility.

        Args:
            index: Target index

        Returns:
            True if successful, False otherwise
        """
        self._safe_log(f"_set_cursor_to_index: Setting index to {index}")
        max_index = len(self.list_view.children) - 1
        self._safe_log(f"  max_index = {max_index}, current index = {self.list_view.index}")

        if index > max_index:
            self._safe_log(f"  Index {index} > max_index {max_index}, returning False")
            return False

        try:
            self.list_view.index = index
            self._safe_log(f"  After setting index: list_view.index = {self.list_view.index}")
            # Scroll to center the entry in the viewport for better visibility
            # This prevents the entry from appearing at the bottom of the screen
            if self.list_view.highlighted_child:
                self._safe_log(f"  highlighted_child = {self.list_view.highlighted_child}")
                self.list_view.scroll_to_center(self.list_view.highlighted_child, animate=False)
            else:
                self._safe_log("  No highlighted_child after setting index!")
            return True
        except Exception as e:
            self._safe_log(f"  Exception caught while setting index: {type(e).__name__}: {e}")
            return False

    def _restore_cursor_position(self) -> None:
        """Restore cursor position based on mode.

        Attempts restoration in this order:
        1. Restore to the last highlighted entry by ID (all modes)
        2. Restore to the last highlighted feed header (grouped mode only)
        3. Restore to the last cursor index (fallback)

        Used after rebuilding the list to restore user's position.
        On initial mount, defaults to first item.
        """
        self._safe_log("_restore_cursor_position: Starting restoration")
        self._safe_log(f"  current index = {self.list_view.index if self.list_view else 'N/A'}")
        self._safe_log(f"  children count = {len(self.list_view.children) if self.list_view else 0}")
        self._safe_log(f"  last_highlighted_entry_id = {self.last_highlighted_entry_id}")
        self._safe_log(f"  last_highlighted_feed = {self.last_highlighted_feed}")
        self._safe_log(f"  last_cursor_index = {self.last_cursor_index}")
        self._safe_log(f"  group_by_feed = {self.group_by_feed}")

        if not self.list_view or len(self.list_view.children) == 0:
            self._safe_log("_restore_cursor_position: No list view or no children, returning")
            return

        # Try to restore to last highlighted entry by ID
        entry_index = self._find_entry_index_by_id(self.last_highlighted_entry_id)
        self._safe_log(f"_restore_cursor_position: entry_index from ID = {entry_index}")
        if entry_index is not None and self._set_cursor_to_index(entry_index):
            self._safe_log(f"Restoring cursor to entry {self.last_highlighted_entry_id} at index {entry_index}")
            self._safe_log(f"  After restore: index = {self.list_view.index}, highlighted = {self.list_view.highlighted_child}")
            return

        # In grouped mode, try to restore to feed header
        feed_index = self._find_feed_header_index(self.last_highlighted_feed)
        self._safe_log(f"_restore_cursor_position: feed_index from header = {feed_index}")
        if feed_index is not None and self._set_cursor_to_index(feed_index):
            self._safe_log(f"Restoring cursor to feed header '{self.last_highlighted_feed}' at index {feed_index}")
            self._safe_log(f"  After restore: index = {self.list_view.index}, highlighted = {self.list_view.highlighted_child}")
            return

        # Fallback: restore to last cursor index
        max_index = len(self.list_view.children) - 1
        cursor_index = min(self.last_cursor_index, max_index)
        self._safe_log(f"_restore_cursor_position: Fallback to cursor_index = {cursor_index} (max = {max_index})")
        if self._set_cursor_to_index(cursor_index):
            self._safe_log(f"Restoring cursor to last index {cursor_index}")
            self._safe_log(f"  After restore: index = {self.list_view.index}, highlighted = {self.list_view.highlighted_child}")
        else:
            self._safe_log(f"_restore_cursor_position: Failed to set cursor to {cursor_index}")
            # Final emergency fallback: if all else fails, force index to 0
            self._safe_log("_restore_cursor_position: Emergency fallback - forcing index to 0")
            try:
                self.list_view.index = 0
                self._safe_log(f"  Emergency fallback result: index = {self.list_view.index}")
            except Exception as e:
                self._safe_log(f"  Emergency fallback failed: {type(e).__name__}: {e}")

    def _set_initial_position_and_focus(self) -> None:
        """Set cursor to first item on initial mount and ensure focus."""
        if not self.list_view or len(self.list_view.children) == 0:
            return

        # Start at the first item (index 0)
        self._set_cursor_to_index(0)
        self._ensure_focus()
        self._safe_log("Initial mount: cursor set to first item (index 0)")

    def _restore_cursor_position_and_focus(self) -> None:
        """Restore cursor position and ensure focus (called after ListView update)."""
        self._restore_cursor_position()
        self._ensure_focus()

    def _ensure_focus(self) -> None:
        """Ensure ListView has focus for keyboard input."""
        list_view_exists = self.list_view is not None
        children_count = len(self.list_view.children) if self.list_view else 0
        self._safe_log(f"_ensure_focus: list_view={list_view_exists}, children={children_count}")
        if self.list_view and len(self.list_view.children) > 0:
            try:
                self.list_view.focus()
                self._safe_log(f"_ensure_focus: Focus set successfully, focused={self.app.focused}")
            except Exception as e:
                self._safe_log(f"_ensure_focus: Exception while setting focus: {type(e).__name__}: {e}")

    def _ensure_list_view(self) -> bool:
        """Ensure list_view is available. Returns False if unavailable."""
        if not self.list_view:
            try:
                self.list_view = self.query_one(CollapsibleListView)
            except Exception as e:
                self._safe_log(f"Failed to get list_view: {e}")
                return False
        return True

    def _get_highlighted_feed_title(self) -> str | None:
        """Extract feed title from currently highlighted list item.

        Returns the feed title from either a FeedHeaderItem or EntryListItem.
        This eliminates the repeated pattern of checking item type and
        extracting feed title across multiple methods.

        Returns:
            Feed title if found, None otherwise
        """
        if not self.list_view:
            return None

        highlighted = self.list_view.highlighted_child
        if not highlighted:
            return None

        if isinstance(highlighted, FeedHeaderItem):
            return highlighted.feed_title
        if isinstance(highlighted, EntryListItem):
            return highlighted.entry.feed.title
        return None

    def _set_feed_fold_state(self, feed_title: str, is_expanded: bool) -> None:
        """Set fold state for a feed and update UI.

        Updates the feed's fold state, toggles the header visual indicator,
        and updates the CSS visibility of feed entries. This eliminates the
        repeated pattern of state management across collapse/expand methods.

        Args:
            feed_title: Title of the feed to update
            is_expanded: True to expand feed, False to collapse
        """
        # Ensure fold state entry exists
        if feed_title not in self.feed_fold_state:
            self.feed_fold_state[feed_title] = not self.group_collapsed

        # Update fold state
        self.feed_fold_state[feed_title] = is_expanded

        # Update header visual indicator
        if feed_title in self.feed_header_map:
            self.feed_header_map[feed_title].toggle_fold()

        # Update CSS visibility
        self._update_feed_visibility(feed_title)

    def _set_category_fold_state(self, category_title: str, is_expanded: bool) -> None:
        """Set fold state for a category and update UI.

        Updates the category's fold state, toggles the header visual indicator,
        and updates the CSS visibility of category entries.

        Args:
            category_title: Title of the category to update
            is_expanded: True to expand category, False to collapse
        """
        # Ensure fold state entry exists
        if category_title not in self.category_fold_state:
            self.category_fold_state[category_title] = not self.group_collapsed

        # Update fold state
        self.category_fold_state[category_title] = is_expanded

        # Update header visual indicator
        if category_title in self.category_header_map:
            self.category_header_map[category_title].toggle_fold()

        # Update CSS visibility
        self._update_category_visibility(category_title)

    def _ensure_list_view_and_grouped(self) -> bool:
        """Ensure list view is available and we're in grouped mode.

        Consolidates the common check: list_view exists and group_by_feed is True.
        This eliminates repeated `if not self.list_view or not self.group_by_feed` checks.

        Returns:
            True if list_view is available and grouped mode is enabled, False otherwise
        """
        return self._ensure_list_view() and self.group_by_feed

    def _list_view_has_items(self) -> bool:
        """Check if list view exists and has children.

        Consolidates the common check for both list view availability and
        checking if it has items. Used to determine if there are entries to work with.

        Returns:
            True if list_view exists and has children, False otherwise
        """
        return self.list_view is not None and len(self.list_view.children) > 0

    def _get_sorted_entries(self) -> list[Entry]:
        """Get entries sorted/grouped according to current settings."""
        entries = self._filter_entries(self.entries)

        if self.group_by_category:
            # When grouping by category, sort by category title then by date
            # Get category title from entry's feed's category_id
            return sorted(
                entries,
                key=lambda e: (self._get_category_title(e.feed.category_id).lower(), e.published_at),
                reverse=False,
            )
        if self.group_by_feed:
            # When grouping by feed, sort by feed name then by date
            return sorted(
                entries,
                key=lambda e: (e.feed.title.lower(), e.published_at),
                reverse=False,
            )
        return self._sort_entries(entries)

    def _display_entries(self, entries: list[Entry]):
        """Display entries in list view based on grouping setting."""
        if self.group_by_category:
            self._add_grouped_entries_by_category(entries)
        elif self.group_by_feed:
            self._add_grouped_entries(entries)
        else:
            self._add_flat_entries(entries)

    def _sort_entries(self, entries: list[Entry]) -> list[Entry]:
        """Sort entries based on current sort mode.

        Sort modes:
        - "feed": Alphabetically by feed name (A-Z), then newest entries first within each feed
        - "date": Newest entries first (most recent publication date)
        - "status": Unread entries first, then by date (oldest first)
        """
        if self.current_sort == "feed":
            # Sort by feed name (A-Z), then by date (newest first within each feed)
            # Use a tuple key with negative date for newest-first within each feed
            return sorted(
                entries,
                key=lambda e: (e.feed.title.lower(), -e.published_at.timestamp()),
                reverse=False,
            )
        if self.current_sort == "date":
            # Sort by published date (newest entries first)
            # reverse=True puts most recent at top
            return sorted(entries, key=lambda e: e.published_at, reverse=True)
        if self.current_sort == "status":
            # Sort by read status (unread first), then by date (oldest first)
            # is_read sorts False (unread) before True (read)
            # reverse=False keeps oldest first within each status group
            return sorted(
                entries,
                key=lambda e: (e.is_read, e.published_at),
                reverse=False,
            )
        return entries

    def _filter_entries(self, entries: list[Entry]) -> list[Entry]:
        """Apply active filters to entries.

        Filters are applied in order:
        1. Category filter (if set)
        2. Search filter (if active)
        3. Status filters (unread/starred - mutually exclusive)

        Args:
            entries: List of entries to filter

        Returns:
            Filtered list of entries
        """
        # Apply category filter first if set
        if self.filter_category_id is not None:
            entries = [e for e in entries if e.feed.category_id == self.filter_category_id]

        # Apply search filter if active
        if self.search_active and self.search_term:
            entries = self._filter_search(entries)

        # Apply status filters (mutually exclusive - only one can be active at a time)
        if self.filter_unread_only:
            # Show only unread entries
            return [e for e in entries if e.is_unread]
        if self.filter_starred_only:
            # Show only starred entries
            return [e for e in entries if e.starred]
        # No status filters active, return all entries (after other filters if applied)
        return entries

    def _filter_search(self, entries: list[Entry]) -> list[Entry]:
        """Filter entries by search term in title and content.

        Searches across both entry titles and HTML content. Search is case-insensitive.

        Args:
            entries: List of entries to search

        Returns:
            Filtered list of matching entries
        """
        search_lower = self.search_term.lower()
        return [e for e in entries if search_lower in e.title.lower() or search_lower in e.content.lower()]

    def _add_feed_header_if_needed(self, current_feed: str, first_feed_ref: list, entry: Entry | None = None) -> None:
        """Add a feed header if transitioning to a new feed.

        Initializes fold state and creates a FeedHeaderItem for the new feed.

        Args:
            current_feed: Title of the current feed
            first_feed_ref: List with one element to track first feed (mutable ref pattern)
            entry: Entry object to extract category information from
        """
        # Track first feed for default positioning
        if first_feed_ref[0] is None:
            first_feed_ref[0] = current_feed
            # Set default position to first feed if not already set
            if not self.last_highlighted_feed:
                self.last_highlighted_feed = first_feed_ref[0]

        # Initialize fold state for this feed if needed
        if current_feed not in self.feed_fold_state:
            # Default: expanded if not set, unless group_collapsed is True
            self.feed_fold_state[current_feed] = not self.group_collapsed

        # Get category title and error status if entry is provided
        category_title = None
        has_errors = False
        feed_disabled = False
        if entry is not None:
            category_title = self._get_category_title(entry.feed.category_id)
            has_errors = entry.feed.has_errors
            feed_disabled = entry.feed.disabled

        # Get feed statistics
        unread_count, total_count = self._get_feed_stats(current_feed, self.sorted_entries)

        # Create and add a fold-aware header item
        is_expanded = self.feed_fold_state[current_feed]
        header = FeedHeaderItem(
            current_feed,
            is_expanded=is_expanded,
            category_title=category_title,
            has_errors=has_errors,
            feed_disabled=feed_disabled,
            unread_count=unread_count,
            total_count=total_count,
        )
        self.feed_header_map[current_feed] = header
        self.list_view.append(header)

    def _add_entry_with_visibility(self, entry: Entry) -> None:
        """Add an entry item with appropriate visibility based on feed state.

        Applies "collapsed" CSS class if the entry's feed is collapsed.

        Args:
            entry: The entry to add
        """
        item = EntryListItem(entry, self.unread_color, self.read_color)
        self.displayed_items.append(item)
        self.entry_item_map[entry.id] = item

        # Apply "collapsed" class if this feed is collapsed
        # We can safely access feed_fold_state since headers are created first
        if not self.feed_fold_state.get(entry.feed.title, not self.group_collapsed):
            item.add_class("collapsed")

        self.list_view.append(item)

    def _add_grouped_entries(self, entries: list[Entry]):
        """Add entries grouped by feed with optional collapsible headers.

        All entries are added to the list, but entries in collapsed feeds
        are hidden via CSS class. This preserves cursor position during expand/collapse.
        """
        current_feed = None
        first_feed = [None]  # Use list as mutable reference for tracking first feed
        self.displayed_items = []
        self.entry_item_map.clear()
        self.feed_header_map.clear()

        for entry in entries:
            # Add feed header if this is a new feed
            if current_feed != entry.feed.title:
                current_feed = entry.feed.title
                self._add_feed_header_if_needed(current_feed, first_feed, entry)

            # Add the entry with appropriate visibility
            self._add_entry_with_visibility(entry)

    def _add_flat_entries(self, entries: list[Entry]):
        """Add entries as a flat list."""
        self.displayed_items = []
        self.entry_item_map.clear()
        for entry in entries:
            item = EntryListItem(entry, self.unread_color, self.read_color)
            self.displayed_items.append(item)
            self.entry_item_map[entry.id] = item
            self.list_view.append(item)

    def _get_category_title(self, category_id: int | None) -> str:
        """Get category title from category ID.

        Args:
            category_id: The category ID to lookup

        Returns:
            Category title, or "Uncategorized" if not found
        """
        if category_id is None:
            return "Uncategorized"

        if not self.categories:
            return f"Category {category_id}"

        for category in self.categories:
            if category.id == category_id:
                return category.title

        return f"Category {category_id}"

    def _get_feed_stats(self, feed_title: str, entries: list[Entry]) -> tuple[int, int]:
        """Calculate unread and total counts for a feed.

        Args:
            feed_title: Title of the feed
            entries: List of entries to count from

        Returns:
            Tuple of (unread_count, total_count) for the feed
        """
        unread = 0
        total = 0
        for entry in entries:
            if entry.feed.title == feed_title:
                total += 1
                if entry.is_unread:
                    unread += 1
        return unread, total

    def _add_category_header_if_needed(self, category_title: str, first_category_ref: list) -> None:
        """Add a category header if transitioning to a new category.

        Initializes fold state and creates a CategoryHeaderItem for the new category.

        Args:
            category_title: Title of the current category
            first_category_ref: List with one element to track first category (mutable ref pattern)
        """
        # Track first category for default positioning
        if first_category_ref[0] is None:
            first_category_ref[0] = category_title
            # Set default position to first category if not already set
            if not self.last_highlighted_category:
                self.last_highlighted_category = first_category_ref[0]

        # Initialize fold state for this category if needed
        if category_title not in self.category_fold_state:
            # Default: expanded if not set, unless group_collapsed is True
            self.category_fold_state[category_title] = not self.group_collapsed

        # Calculate entry counts for this category
        category_id = None
        for entry in self.sorted_entries:
            entry_category = self._get_category_title(entry.feed.category_id)
            if entry_category == category_title:
                category_id = entry.feed.category_id
                break

        unread_count = 0
        read_count = 0
        if category_id is not None:
            unread_count = sum(1 for e in self.sorted_entries if e.feed.category_id == category_id and e.is_unread)
            read_count = sum(1 for e in self.sorted_entries if e.feed.category_id == category_id and not e.is_unread)

        # Create and add a fold-aware header item with counts
        is_expanded = self.category_fold_state[category_title]
        header = CategoryHeaderItem(category_title, is_expanded=is_expanded, unread_count=unread_count, read_count=read_count)
        self.category_header_map[category_title] = header
        self.list_view.append(header)

    def _add_entry_with_category_visibility(self, entry: Entry, category_title: str) -> None:
        """Add an entry item with appropriate visibility based on category state.

        Applies "collapsed" CSS class if the entry's category is collapsed.

        Args:
            entry: The entry to add
            category_title: Title of the category this entry belongs to
        """
        item = EntryListItem(entry, self.unread_color, self.read_color)
        self.displayed_items.append(item)
        self.entry_item_map[entry.id] = item

        # Apply "collapsed" class if this category is collapsed
        if not self.category_fold_state.get(category_title, not self.group_collapsed):
            item.add_class("collapsed")

        self.list_view.append(item)

    def _add_grouped_entries_by_category(self, entries: list[Entry]):
        """Add entries grouped by category with optional collapsible headers.

        All entries are added to the list, but entries in collapsed categories
        are hidden via CSS class. This preserves cursor position during expand/collapse.
        """
        current_category = None
        first_category = [None]  # Use list as mutable reference for tracking first category
        self.displayed_items = []
        self.entry_item_map.clear()
        self.category_header_map.clear()

        for entry in entries:
            # Get category title for this entry
            category_title = self._get_category_title(entry.feed.category_id)

            # Add category header if this is a new category
            if current_category != category_title:
                current_category = category_title
                self._add_category_header_if_needed(current_category, first_category)

            # Add the entry with appropriate visibility
            self._add_entry_with_category_visibility(entry, category_title)

    def _update_single_item(self, entry: Entry) -> bool:
        """Update a single entry item in the list (incremental refresh).

        This avoids rebuilding the entire list when only one entry changes.

        Args:
            entry: The entry to update

        Returns:
            True if item was updated, False if item not found or refresh needed
        """
        # Check if item is in the current view
        if entry.id not in self.entry_item_map:
            return False

        old_item = self.entry_item_map[entry.id]

        # Create new item with updated data
        new_item = EntryListItem(entry, self.unread_color, self.read_color)
        self.entry_item_map[entry.id] = new_item

        # Find the index of the old item in the list view
        try:
            children_list = list(self.list_view.children)
            index = children_list.index(old_item)
            # Remove the old item
            old_item.remove()
            # Get the item that's now at that position (if exists)
            current_children = list(self.list_view.children)
            # Mount new item before the item that's now at that index
            if index < len(current_children):
                self.list_view.mount(new_item, before=current_children[index])
            else:
                self.list_view.mount(new_item)
            # Update displayed_items if it's in there
            if old_item in self.displayed_items:
                item_index = self.displayed_items.index(old_item)
                self.displayed_items[item_index] = new_item
            self.refresh_optimizer.track_partial_refresh()
            return True
        except (ValueError, IndexError):
            return False

    @staticmethod
    def _is_item_visible(item: ListItem) -> bool:
        """Check if an item is visible (not hidden by CSS class)."""
        return "collapsed" not in item.classes

    async def _on_key(self, event: events.Key) -> None:
        """Handle key events, with special support for g-prefix commands.

        When _g_prefix_mode is True, the next key after 'g' is interpreted as a command:
        - u = show unread
        - b = show starred
        - h = show history
        - c = group entries by category
        - C = go to category management
        - f = go to feeds
        - s = go to settings
        """
        if self._g_prefix_mode:
            self._g_prefix_mode = False
            key = event.character

            if key == "u":
                self.action_show_unread()
            elif key == "b":
                self.action_show_starred()
            elif key == "h":
                self.action_show_history()
            elif key == "c":
                # g+c: Group entries by category and show counts
                self.action_toggle_group_category()
            elif key == "C":
                # g+C: Go to category management screen
                await self.action_show_categories()
            elif key == "f":
                self.action_show_feeds()
            elif key == "s":
                self.action_show_settings()
            elif key == "g":
                # Allow 'gg' to go to top (vim-style)
                self.action_go_to_top()
            else:
                # Unrecognized g-command, cancel mode
                pass
            event.prevent_default()
        else:
            await super()._on_key(event)

    def action_cursor_down(self):
        """Move cursor down to next visible entry item, skipping collapsed entries."""
        if not self.list_view or len(self.list_view.children) == 0:
            self._safe_log("action_cursor_down: No list view or no children")
            return

        try:
            current_index = self.list_view.index
            self._safe_log(f"action_cursor_down: current_index = {current_index}, children count = {len(self.list_view.children)}")

            # If index is None, start searching from -1 so range(0, ...) includes index 0
            if current_index is None:
                current_index = -1
                self._safe_log("action_cursor_down: index was None, starting from -1")

            # Move to next item and skip hidden ones
            for i in range(current_index + 1, len(self.list_view.children)):
                widget = self.list_view.children[i]
                if isinstance(widget, ListItem):
                    is_visible = self._is_item_visible(widget)
                    self._safe_log(f"  Checking index {i}: type={type(widget).__name__}, visible={is_visible}")
                    if is_visible:
                        self._safe_log(f"action_cursor_down: Moving to visible item at index {i}")
                        self.list_view.index = i
                        return

            # If no visible item found below, stay at current position
            self._safe_log("action_cursor_down: No visible item found below current position")
        except (IndexError, ValueError, TypeError) as e:
            # Silently ignore index errors when navigating beyond list bounds
            self._safe_log(f"action_cursor_down: Exception: {type(e).__name__}: {e}")

    def action_cursor_up(self):
        """Move cursor up to previous visible entry item, skipping collapsed entries."""
        if not self.list_view or len(self.list_view.children) == 0:
            return

        try:
            current_index = self.list_view.index
            # If index is None, start from len so we search backwards from end
            if current_index is None:
                current_index = len(self.list_view.children)

            # Move to previous item and skip hidden ones
            for i in range(current_index - 1, -1, -1):
                widget = self.list_view.children[i]
                if isinstance(widget, ListItem) and self._is_item_visible(widget):
                    self.list_view.index = i
                    return

            # If no visible item found above, stay at current position
        except (IndexError, ValueError, TypeError):
            # Silently ignore index errors when navigating beyond list bounds
            pass

    def action_g_prefix_mode(self) -> None:
        """Activate g-prefix mode for section navigation.

        Sets the flag to wait for the next key, which will be interpreted as:
        - g: go to top (gg)
        - u: show unread entries
        - b: show starred entries
        - h: show history
        - c: go to categories
        - f: go to feeds
        - s: go to settings
        """
        self._g_prefix_mode = True
        self.notify("g-prefix mode (press g/u/b/h/c/f/s)", timeout=2)

    async def action_show_categories(self) -> None:
        """Go to categories (g+c)."""
        await self.action_manage_categories()

    def action_show_feeds(self) -> None:
        """Go to feeds management (g+f)."""
        if hasattr(self.app, "push_feed_management_screen"):
            self.app.push_feed_management_screen()
        else:
            self.notify("Feed management not available", severity="warning")

    def action_go_to_top(self) -> None:
        """Go to top of entry list (gg)."""
        if self.list_view and len(self.list_view.children) > 0:
            # Find first visible item
            for i, child in enumerate(self.list_view.children):
                if isinstance(child, ListItem) and self._is_item_visible(child):
                    self.list_view.index = i
                    if self.list_view.highlighted_child:
                        self.list_view.scroll_to_center(self.list_view.highlighted_child, animate=False)
                    self.notify("Jumped to top", timeout=1)
                    return

    def action_go_to_bottom(self) -> None:
        """Go to bottom of entry list (G)."""
        if self.list_view and len(self.list_view.children) > 0:
            # Find last visible item (search backwards)
            for i in range(len(self.list_view.children) - 1, -1, -1):
                child = self.list_view.children[i]
                if isinstance(child, ListItem) and self._is_item_visible(child):
                    self.list_view.index = i
                    if self.list_view.highlighted_child:
                        self.list_view.scroll_to_center(self.list_view.highlighted_child, animate=False)
                    self.notify("Jumped to bottom", timeout=1)
                    return

    async def action_toggle_read(self):
        """Toggle read/unread status of current entry."""
        if not self.list_view:
            return

        highlighted = self.list_view.highlighted_child
        if highlighted and isinstance(highlighted, EntryListItem):
            # Determine new status
            new_status = "read" if highlighted.entry.is_unread else "unread"

            # Use consistent error handling context
            with api_call(self, f"marking entry as {new_status}") as client:
                if client is None:
                    return

                # Call API to persist change
                await client.change_entry_status(highlighted.entry.id, new_status)

                # Update local state
                highlighted.entry.status = new_status

                # Try incremental update first; fall back to full refresh if needed
                if not self._update_single_item(highlighted.entry):
                    # Fall back to full refresh if incremental update fails
                    self._populate_list()

                # Notify user of success
                self.notify(f"Entry marked as {new_status}")

    async def action_toggle_read_previous(self):
        """Toggle read/unread status and focus previous entry (M key)."""
        if not self.list_view:
            return

        # First toggle the read status
        highlighted = self.list_view.highlighted_child
        if highlighted and isinstance(highlighted, EntryListItem):
            # Determine new status
            new_status = "read" if highlighted.entry.is_unread else "unread"

            # Use consistent error handling context
            with api_call(self, f"marking entry as {new_status}") as client:
                if client is None:
                    return

                # Call API to persist change
                await client.change_entry_status(highlighted.entry.id, new_status)

                # Update local state
                highlighted.entry.status = new_status

                # Try incremental update first; fall back to full refresh if needed
                if not self._update_single_item(highlighted.entry):
                    # Fall back to full refresh if incremental update fails
                    self._populate_list()

                # Notify user of success
                self.notify(f"Entry marked as {new_status}")

        # Then move to previous entry
        self.action_cursor_up()

    async def action_toggle_star(self):
        """Toggle star status of current entry."""
        if not self.list_view:
            return

        highlighted = self.list_view.highlighted_child
        if highlighted and isinstance(highlighted, EntryListItem):
            # Use consistent error handling context
            with api_call(self, "toggling star status") as client:
                if client is None:
                    return

                # Call API to toggle star
                await client.toggle_starred(highlighted.entry.id)

                # Update local state
                highlighted.entry.starred = not highlighted.entry.starred

                # Try incremental update first; fall back to full refresh if needed
                if not self._update_single_item(highlighted.entry):
                    # Fall back to full refresh if incremental update fails
                    self._populate_list()

                # Notify user of success
                status = "starred" if highlighted.entry.starred else "unstarred"
                self.notify(f"Entry {status}")

    async def action_save_entry(self):
        """Save entry to third-party service."""
        if not self.list_view:
            return

        highlighted = self.list_view.highlighted_child
        if highlighted and isinstance(highlighted, EntryListItem):
            # Use consistent error handling context
            with api_call(self, "saving entry") as client:
                if client is None:
                    return

                await client.save_entry(highlighted.entry.id)
                self.notify(f"Entry saved: {highlighted.entry.title}")

    async def action_mark_all_as_read(self):
        """Mark all visible entries as read (A key) with confirmation."""
        if not self.list_view or len(self.list_view.children) == 0:
            self.notify("No entries to mark", severity="warning")
            return

        # Import here to avoid circular dependency
        from miniflux_tui.ui.screens.confirm_dialog import ConfirmDialog  # noqa: PLC0415

        # Count unread entries
        unread_count = sum(1 for entry in self.sorted_entries if entry.is_unread)
        if unread_count == 0:
            self.notify("No unread entries to mark", severity="warning")
            return

        def on_confirm() -> None:
            """Handle confirmation to mark all as read."""
            asyncio.create_task(self._do_mark_all_as_read())  # noqa: RUF006

        # Create confirmation dialog
        dialog = ConfirmDialog(
            title="Mark All as Read",
            message=f"Mark all {unread_count} unread entries as read?",
            confirm_label="Yes",
            cancel_label="No",
            on_confirm=on_confirm,
        )
        self.app.push_screen(dialog)

    async def _do_mark_all_as_read(self) -> None:
        """Mark all entries as read via API.

        This is called after user confirms the action.
        """
        # Use consistent error handling context
        with api_call(self, "marking all entries as read") as client:
            if client is None:
                return

            try:
                # Mark all entries as read via API
                await client.mark_all_as_read()

                # Update local state for all visible entries
                for entry in self.sorted_entries:
                    if entry.is_unread:
                        entry.status = "read"

                # Refresh the list to show updated states
                self._populate_list()

                # Notify user
                self.notify("All entries marked as read")
            except Exception as e:
                self.notify(f"Error marking all as read: {e}", severity="error")

    def action_cycle_sort(self):
        """Cycle through sort modes."""
        current_index = SORT_MODES.index(self.current_sort)
        self.current_sort = SORT_MODES[(current_index + 1) % len(SORT_MODES)]

        # Update title to show current sort
        self.sub_title = f"Sort: {self.current_sort.title()}"

        # Re-populate list
        self._populate_list()

    def action_toggle_group_feed(self):
        """Toggle grouping by feed (g key)."""
        # Disable category grouping when enabling feed grouping
        if not self.group_by_feed and self.group_by_category:
            self.group_by_category = False

        self.group_by_feed = not self.group_by_feed

        if self.group_by_feed:
            # Clear existing fold states so new groups use config default
            self.feed_fold_state.clear()
            self.notify("Grouping by feed (use h/l to collapse/expand)")
        else:
            self.notify("Feed grouping disabled")

        self._populate_list()

    def action_toggle_group_category(self):
        """Toggle grouping by category (c key - Issue #54 - Category support)."""
        if not self.categories:
            self.notify("No categories available", severity="warning")
            return

        # Disable feed grouping when enabling category grouping
        if not self.group_by_category and self.group_by_feed:
            self.group_by_feed = False

        # Toggle category grouping
        self.group_by_category = not self.group_by_category

        if self.group_by_category:
            # Clear existing fold states so new groups use config default
            self.category_fold_state.clear()
            self.notify("Grouping by category (use h/l to collapse/expand)")
        else:
            self.notify("Category grouping disabled")

        self._populate_list()

    def action_toggle_fold(self):
        """Toggle fold state of highlighted feed or category (o key)."""
        if not self.list_view or (not self.group_by_feed and not self.group_by_category):
            return

        highlighted = self.list_view.highlighted_child

        # Handle feed grouping mode
        if self.group_by_feed and isinstance(highlighted, FeedHeaderItem):
            feed_title = highlighted.feed_title
            self.last_highlighted_feed = feed_title
            self.feed_fold_state[feed_title] = not self.feed_fold_state[feed_title]
            highlighted.toggle_fold()
            self._update_feed_visibility(feed_title)

        # Handle category grouping mode
        elif self.group_by_category and isinstance(highlighted, CategoryHeaderItem):
            category_title = highlighted.category_title
            self.last_highlighted_category = category_title
            self.category_fold_state[category_title] = not self.category_fold_state[category_title]
            highlighted.toggle_fold()
            self._update_category_visibility(category_title)

    def _update_feed_visibility(self, feed_title: str) -> None:
        """Update CSS visibility for all entries of a feed based on fold state.

        If feed is collapsed, adds 'collapsed' class to hide entries.
        If feed is expanded, removes 'collapsed' class to show entries.
        """
        is_expanded = self.feed_fold_state.get(feed_title, True)

        # Find all entries for this feed and update their CSS class
        for item in self.list_view.children:
            if isinstance(item, EntryListItem) and item.entry.feed.title == feed_title:
                if is_expanded:
                    item.remove_class("collapsed")
                else:
                    item.add_class("collapsed")

    def _update_category_visibility(self, category_title: str) -> None:
        """Update CSS visibility for all entries of a category based on fold state.

        If category is collapsed, adds 'collapsed' class to hide entries.
        If category is expanded, removes 'collapsed' class to show entries.
        """
        is_expanded = self.category_fold_state.get(category_title, True)

        # Find all entries for this category and update their CSS class
        for item in self.list_view.children:
            if isinstance(item, EntryListItem) and self._get_category_title(item.entry.feed.category_id) == category_title:
                if is_expanded:
                    item.remove_class("collapsed")
                else:
                    item.add_class("collapsed")

    def action_collapse_fold(self):
        """Collapse the highlighted feed or category (h or left arrow)."""
        if not self.list_view or (not self.group_by_feed and not self.group_by_category):
            return

        highlighted = self.list_view.highlighted_child

        # Handle feed grouping mode
        if self.group_by_feed and isinstance(highlighted, FeedHeaderItem):
            feed_title = highlighted.feed_title
            self.last_highlighted_feed = feed_title
            is_currently_expanded = self.feed_fold_state.get(feed_title, not self.group_collapsed)
            if is_currently_expanded:
                self._set_feed_fold_state(feed_title, False)

        # Handle category grouping mode
        elif self.group_by_category and isinstance(highlighted, CategoryHeaderItem):
            category_title = highlighted.category_title
            self.last_highlighted_category = category_title
            is_currently_expanded = self.category_fold_state.get(category_title, not self.group_collapsed)
            if is_currently_expanded:
                self._set_category_fold_state(category_title, False)

        # Fallback for entry items: collapse their parent feed/category
        elif isinstance(highlighted, EntryListItem):
            if self.group_by_feed:
                feed_title = highlighted.entry.feed.title
                self.last_highlighted_feed = feed_title
                is_currently_expanded = self.feed_fold_state.get(feed_title, not self.group_collapsed)
                if is_currently_expanded:
                    self._set_feed_fold_state(feed_title, False)
            elif self.group_by_category:
                category_title = self._get_category_title(highlighted.entry.feed.category_id)
                self.last_highlighted_category = category_title
                is_currently_expanded = self.category_fold_state.get(category_title, not self.group_collapsed)
                if is_currently_expanded:
                    self._set_category_fold_state(category_title, False)

    def action_expand_fold(self):
        """Expand the highlighted feed or category (l or right arrow)."""
        if not self.list_view or (not self.group_by_feed and not self.group_by_category):
            return

        highlighted = self.list_view.highlighted_child

        # Handle feed grouping mode
        if self.group_by_feed and isinstance(highlighted, FeedHeaderItem):
            feed_title = highlighted.feed_title
            self.last_highlighted_feed = feed_title
            is_currently_collapsed = not self.feed_fold_state.get(feed_title, not self.group_collapsed)
            if is_currently_collapsed:
                self._set_feed_fold_state(feed_title, True)

        # Handle category grouping mode
        elif self.group_by_category and isinstance(highlighted, CategoryHeaderItem):
            category_title = highlighted.category_title
            self.last_highlighted_category = category_title
            is_currently_collapsed = not self.category_fold_state.get(category_title, not self.group_collapsed)
            if is_currently_collapsed:
                self._set_category_fold_state(category_title, True)

        # Fallback for entry items: expand their parent feed/category
        elif isinstance(highlighted, EntryListItem):
            if self.group_by_feed:
                feed_title = highlighted.entry.feed.title
                self.last_highlighted_feed = feed_title
                is_currently_collapsed = not self.feed_fold_state.get(feed_title, not self.group_collapsed)
                if is_currently_collapsed:
                    self._set_feed_fold_state(feed_title, True)
            elif self.group_by_category:
                category_title = self._get_category_title(highlighted.entry.feed.category_id)
                self.last_highlighted_category = category_title
                is_currently_collapsed = not self.category_fold_state.get(category_title, not self.group_collapsed)
                if is_currently_collapsed:
                    self._set_category_fold_state(category_title, True)

    def action_expand_all(self):
        """Expand all feeds or categories (Shift+G).

        If not in grouped mode, enable feed grouping first.
        Then expand all collapsed items.
        """
        if not self.list_view:
            return

        # If not in grouped mode, enable feed grouping first
        if not self.group_by_feed and not self.group_by_category:
            self.action_toggle_group_feed()
            return

        # Expand all feeds that are currently collapsed
        if self.group_by_feed:
            for feed_title in self.feed_fold_state:
                if not self.feed_fold_state[feed_title]:
                    self._set_feed_fold_state(feed_title, True)
            self.notify("All feeds expanded")

        # Expand all categories that are currently collapsed
        elif self.group_by_category:
            for category_title in self.category_fold_state:
                if not self.category_fold_state[category_title]:
                    self._set_category_fold_state(category_title, True)
            self.notify("All categories expanded")

    def action_collapse_all(self):
        """Collapse all feeds or categories (Shift+Z)."""
        if not self.list_view or (not self.group_by_feed and not self.group_by_category):
            return

        # Collapse all feeds that are currently expanded
        if self.group_by_feed:
            for feed_title in self.feed_fold_state:
                if self.feed_fold_state[feed_title]:
                    self._set_feed_fold_state(feed_title, False)
            self.notify("All feeds collapsed")

        # Collapse all categories that are currently expanded
        elif self.group_by_category:
            for category_title in self.category_fold_state:
                if self.category_fold_state[category_title]:
                    self._set_category_fold_state(category_title, False)
            self.notify("All categories collapsed")

    def action_refresh(self):
        """Refresh the current feed on the server (Issue #55 - Feed operations)."""
        if not hasattr(self.app, "client") or not self.app.client:
            self.notify("API client not initialized", severity="error")
            return

        # Get the currently highlighted item to determine which feed to refresh
        if not self.list_view or self.list_view.index is None:
            self.notify("No entry selected", severity="warning")
            return

        highlighted = self.list_view.highlighted_child
        feed_title = None
        feed_id = None

        # Handle both feed headers and entry items
        if isinstance(highlighted, FeedHeaderItem):
            # User is on a feed header - get feed info from first entry in that feed
            feed_title = highlighted.feed_title
            # Find the first entry for this feed to get the feed_id
            for entry in self.sorted_entries:
                if entry.feed.title == feed_title:
                    feed_id = entry.feed_id
                    break
            if feed_id is None:
                self.notify("No entries found for this feed", severity="warning")
                return
        elif isinstance(highlighted, EntryListItem):
            # User is on an entry - get feed info from the entry
            feed_title = highlighted.entry.feed.title
            feed_id = highlighted.entry.feed_id
        else:
            self.notify("No feed selected", severity="warning")
            return

        # Run the refresh in background to keep UI responsive
        self.run_worker(self._do_refresh(feed_id, feed_title), exclusive=True)

    async def _do_refresh(self, feed_id: int, feed_title: str):
        """Background worker for refreshing a feed."""
        try:
            # Start loading animation in header
            self._start_loading_animation(f"Refreshing {feed_title}...")

            await self.app.client.refresh_feed(feed_id)

            # Show success message
            self.notify(f"Feed '{feed_title}' refreshed. Use ',' to sync new entries.", severity="information")
        except (ConnectionError, TimeoutError, OSError, BrokenPipeError) as e:
            # Connection error - try to reconnect and retry once
            self.notify("Connection error, attempting to reconnect...", severity="warning")
            if await self.app.reconnect_client():
                try:
                    await self.app.client.refresh_feed(feed_id)
                    self.notify(f"Feed '{feed_title}' refreshed after reconnection. Use ',' to sync new entries.", severity="information")
                except Exception as retry_error:
                    self.notify(f"Error after reconnection: {retry_error}", severity="error")
            else:
                self.notify(f"Network error refreshing feed: {e}", severity="error")
        except Exception as e:
            self.notify(f"Error refreshing feed: {e}", severity="error")
        finally:
            # Always stop the loading animation
            self._stop_loading_animation()

    def action_refresh_all_feeds(self):
        """Refresh all feeds on the server (Issue #55 - Feed operations).

        This tells the Miniflux server to fetch new content from RSS feeds.
        It does NOT reload entries - use 'comma' (,) to sync entries from server.
        """
        if not hasattr(self.app, "client") or not self.app.client:
            self.notify("API client not initialized", severity="error")
            return

        # Run the refresh in background to keep UI responsive
        self.run_worker(self._do_refresh_all_feeds(), exclusive=True)

    async def _do_refresh_all_feeds(self):
        """Background worker for refreshing all feeds."""
        try:
            # Start loading animation in header
            self._start_loading_animation("Refreshing all feeds...")

            await self.app.client.refresh_all_feeds()

            # Show success message
            self.notify("All feeds refreshed successfully. Use ',' to sync new entries.", severity="information")
        except (ConnectionError, TimeoutError, OSError, BrokenPipeError) as e:
            # Connection error - try to reconnect and retry once
            self.notify("Connection error, attempting to reconnect...", severity="warning")
            if await self.app.reconnect_client():
                try:
                    await self.app.client.refresh_all_feeds()
                    self.notify("All feeds refreshed after reconnection. Use ',' to sync new entries.", severity="information")
                except Exception as retry_error:
                    self.notify(f"Error after reconnection: {retry_error}", severity="error")
            else:
                self.notify(f"Network error refreshing feeds: {e}", severity="error")
        except Exception as e:
            self.notify(f"Error refreshing all feeds: {e}", severity="error")
        finally:
            # Always stop the loading animation
            self._stop_loading_animation()

    def _remove_entry_from_ui(self, entry_id: int) -> None:
        """Remove an entry from the UI by ID.

        Args:
            entry_id: The ID of the entry to remove
        """
        self.entries = [e for e in self.entries if e.id != entry_id]
        self.sorted_entries = [e for e in self.sorted_entries if e.id != entry_id]
        if entry_id in self.entry_item_map:
            del self.entry_item_map[entry_id]

    def _add_entry_to_ui(self, entry: Entry) -> None:
        """Add an entry to the UI.

        Args:
            entry: The entry to add
        """
        self.entries.append(entry)
        list_item = EntryListItem(
            entry=entry,
            unread_color=self.unread_color,
            read_color=self.read_color,
        )
        self.entry_item_map[entry.id] = list_item

    async def _fetch_entries_for_sync(self) -> list[Entry] | None:
        """Fetch entries from server based on current view.

        Returns:
            List of entries or None if error occurred
        """
        try:
            if self.app.current_view == "starred":
                return await self.app.client.get_starred_entries(limit=DEFAULT_ENTRY_LIMIT)
            return await self.app.client.get_unread_entries(limit=DEFAULT_ENTRY_LIMIT)
        except Exception as e:
            self.notify(f"Error fetching entries: {e}", severity="error")
            return None

    async def _enrich_entries_with_categories(self, entries: list[Entry]) -> None:
        """Enrich entries with category information from app state.

        Args:
            entries: List of entries to enrich
        """
        # Rebuild category mapping for fresh data
        if hasattr(self.app, "_build_entry_category_mapping"):
            self.app.entry_category_map = await self.app._build_entry_category_mapping()

        # Enrich entries with category information
        if self.app.entry_category_map:
            for entry in entries:
                if entry.id in self.app.entry_category_map:
                    entry.feed.category_id = self.app.entry_category_map[entry.id]

    def _apply_entry_changes(self, added_ids: set[int], removed_ids: set[int], new_entry_map: dict[int, Entry]) -> None:
        """Apply entry changes to the UI.

        Args:
            added_ids: Set of entry IDs to add
            removed_ids: Set of entry IDs to remove
            new_entry_map: Map of entry ID to Entry object for new entries
        """
        # Remove entries that are no longer in the view
        for entry_id in removed_ids:
            self._remove_entry_from_ui(entry_id)

        # Add new entries
        for entry_id in added_ids:
            self._add_entry_to_ui(new_entry_map[entry_id])

        # Update app state and re-sort
        self.app.entries = self.entries
        self.sorted_entries = self._sort_entries(self.entries)

        # Refresh the list view
        if self.list_view:
            self._populate_list()

    async def _perform_incremental_sync(self) -> tuple[int, int, int]:
        """Perform incremental sync of entries from the server.

        Fetches new entries from the server and dynamically updates the UI by:
        - Adding new entries to the list
        - Removing entries that were marked read elsewhere
        - Preserving UI state (cursor position, sort order, etc.)

        Returns:
            Tuple of (new_count, removed_count, updated_count)
        """
        if not hasattr(self.app, "client") or not self.app.client:
            self.notify("API client not initialized", severity="error")
            return (0, 0, 0)

        # Get current entry IDs before sync
        current_ids = {entry.id for entry in self.entries}

        # Fetch fresh data from server
        new_entries = await self._fetch_entries_for_sync()
        if new_entries is None:
            return (0, 0, 0)

        # Enrich with category data
        await self._enrich_entries_with_categories(new_entries)

        # Calculate changes
        new_ids = {entry.id for entry in new_entries}
        added_ids = new_ids - current_ids
        removed_ids = current_ids - new_ids

        # If no changes, return early
        if not added_ids and not removed_ids:
            return (0, 0, 0)

        # Apply changes to UI
        new_entry_map = {entry.id: entry for entry in new_entries}
        self._apply_entry_changes(added_ids, removed_ids, new_entry_map)

        return (len(added_ids), len(removed_ids), 0)

    def action_sync_entries(self):
        """Sync/reload entries from server without refreshing feeds.

        This fetches the latest entries that already exist on the Miniflux server
        without telling the server to fetch new content from RSS feeds.
        Use this to get entries that were added elsewhere or by another client.

        Uses run_worker to execute the sync in the background, keeping UI responsive.
        """
        self.run_worker(self._do_sync_entries(), exclusive=True)

    def _format_sync_summary(self, new_count: int, removed_count: int, after_reconnect: bool = False) -> None:
        """Format and display sync summary message.

        Args:
            new_count: Number of new entries
            removed_count: Number of removed entries
            after_reconnect: Whether this is after a reconnection
        """
        if new_count == 0 and removed_count == 0:
            message = "Entries are up to date after reconnection" if after_reconnect else "Entries are up to date"
            self.notify(message, severity="information", timeout=2)
        else:
            details = []
            if new_count > 0:
                details.append(f"+{new_count} new")
            if removed_count > 0:
                details.append(f"-{removed_count} removed")
            summary = ", ".join(details)
            prefix = "Synced entries after reconnection: " if after_reconnect else "Synced entries: "
            self.notify(f"{prefix}{summary}", severity="information")

    async def _do_sync_entries(self):
        """Background worker for syncing entries.

        This runs in the background allowing the UI to remain responsive
        while the sync operation completes.
        """
        try:
            # Start loading animation in header
            self._start_loading_animation("Syncing entries...")

            # Perform incremental sync
            new_count, removed_count, _ = await self._perform_incremental_sync()

            # Show summary message
            self._format_sync_summary(new_count, removed_count)

        except (ConnectionError, TimeoutError, OSError, BrokenPipeError) as e:
            # Connection error - try to reconnect and retry once
            self.notify("Connection error, attempting to reconnect...", severity="warning")
            if await self.app.reconnect_client():
                try:
                    new_count, removed_count, _ = await self._perform_incremental_sync()
                    self._format_sync_summary(new_count, removed_count, after_reconnect=True)
                except Exception as retry_error:
                    self.notify(f"Error after reconnection: {retry_error}", severity="error")
            else:
                self.notify(f"Network error syncing entries: {e}", severity="error")
        except Exception as e:
            self.notify(f"Error syncing entries: {e}", severity="error")
        finally:
            # Always stop the loading animation
            self._stop_loading_animation()

    def action_show_unread(self):
        """Load and show only unread entries."""
        self.run_worker(self._do_show_unread(), exclusive=True)

    async def _do_show_unread(self):
        """Background worker for loading unread entries."""
        if hasattr(self.app, "load_entries"):
            try:
                # Start loading animation in header
                self._start_loading_animation("Loading unread entries...")

                await self.app.load_entries("unread")
                self.filter_unread_only = False
                self.filter_starred_only = False
                self._populate_list()
            finally:
                # Always stop the loading animation
                self._stop_loading_animation()

    def action_show_starred(self):
        """Load and show only starred entries."""
        self.run_worker(self._do_show_starred(), exclusive=True)

    async def _do_show_starred(self):
        """Background worker for loading starred entries."""
        if hasattr(self.app, "load_entries"):
            try:
                # Start loading animation in header
                self._start_loading_animation("Loading starred entries...")

                await self.app.load_entries("starred")
                self.filter_unread_only = False
                self.filter_starred_only = False
                self._populate_list()
            finally:
                # Always stop the loading animation
                self._stop_loading_animation()

    def action_clear_filters(self) -> None:
        """Clear all active filters and show all entries.

        Clears category, search, unread, and starred filters.
        """
        self.filter_category_id = None
        self.filter_unread_only = False
        self.filter_starred_only = False
        self.search_active = False
        self.search_term = ""
        self._populate_list()
        self.notify("All filters cleared")

    def set_category_filter(self, category_id: int | None) -> None:
        """Set category filter to show entries from a specific category.

        Args:
            category_id: ID of the category to filter by, or None to show all entries
        """
        self.filter_category_id = category_id
        self.filter_unread_only = False
        self.filter_starred_only = False
        self.search_active = False
        self.search_term = ""
        self._populate_list()

        # Find category name for notification
        category_name = "All entries"
        if category_id is not None:
            for cat in self.categories:
                if cat.id == category_id:
                    category_name = cat.title
                    break

        self.notify(f"Filtered to: {category_name}")

    def action_search(self):
        """Open search dialog to filter entries by search term.

        Shows an interactive input dialog for entering search terms.
        Searches entry titles and content.
        """
        # Import InputDialog locally to avoid circular dependency
        from miniflux_tui.ui.screens.input_dialog import InputDialog  # noqa: PLC0415

        # Callback when user submits search
        def on_search_submit(search_term: str) -> None:
            self.set_search_term(search_term)

        # Show input dialog with current search term as initial value
        dialog = InputDialog(
            title="Search Entries",
            label="Search in titles and content:",
            value=self.search_term,
            on_submit=on_search_submit,
        )
        self.app.push_screen(dialog)

    def set_search_term(self, search_term: str) -> None:
        """Set search term and filter entries.

        Args:
            search_term: The search term to filter entries by (title or content)
        """
        self.search_term = search_term.strip()
        self.search_active = bool(self.search_term)
        self._populate_list()

        # Notify user of search results
        if self.search_active:
            result_count = len(self._filter_entries(self.entries))
            self.notify(f"Search: {result_count} entries match '{self.search_term}'")
        else:
            self.notify("Search cleared")

    async def action_manage_categories(self) -> None:
        """Open the category management screen."""
        await self.app.push_category_management_screen()

    def action_show_help(self):
        """Show keyboard help."""
        self.app.push_screen("help")

    def action_show_status(self):
        """Show system status and feed health."""
        self.app.push_screen("status")

    def action_show_settings(self):
        """Show user settings and integrations."""
        self.app.push_screen("settings")

    def action_show_history(self):
        """Show reading history."""
        self.app.log("action_show_history called - pushing history screen")
        try:
            self.app.push_screen("history")
            self.app.log("Successfully pushed history screen")
        except Exception as e:
            self.app.log(f"Error pushing history screen: {type(e).__name__}: {e}")
            self.app.notify(f"Failed to show history: {e}", severity="error")

    async def action_feed_settings(self) -> None:
        """Open feed settings screen for selected entry's feed."""
        # Import here to avoid circular dependency
        from miniflux_tui.ui.screens.feed_settings import FeedSettingsScreen  # noqa: PLC0415

        # Get the currently selected item
        if not self.list_view or not self.list_view.highlighted_child:
            self.notify("No entry selected", severity="warning")
            return

        # Get entry from selected item
        selected_item = self.list_view.highlighted_child
        if not isinstance(selected_item, EntryListItem):
            self.notify("Please select an entry first", severity="warning")
            return

        entry = selected_item.entry

        if not self.app.client:
            self.notify("API client not available", severity="error")
            return

        # Save the entry position for restoration when returning from feed settings
        # This matches the behavior in _open_entry()
        self.last_highlighted_feed = entry.feed.title
        self.last_highlighted_entry_id = entry.id

        # Save the cursor index in the list view
        if self.list_view and self.list_view.index is not None:
            self.last_cursor_index = self.list_view.index

        # Push feed settings screen
        screen = FeedSettingsScreen(
            feed_id=entry.feed.id,
            feed=entry.feed,
            client=self.app.client,  # type: ignore[arg-type]
        )

        self.app.push_screen(screen)  # type: ignore[arg-type]

    def action_toggle_theme(self) -> None:
        """Toggle between dark and light themes."""
        self.app.toggle_theme()

    def action_quit(self):
        """Quit the application."""
        self.app.exit()
