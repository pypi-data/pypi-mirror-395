# SPDX-License-Identifier: MIT
"""Entry reader screen for viewing feed entry content."""

import re
import traceback
import webbrowser
from contextlib import suppress
from urllib.parse import urlparse

import html2text
from textual.app import ComposeResult
from textual.binding import Binding

# No longer using VerticalScroll - Markdown is the scrollable container
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown, Static

from miniflux_tui.api.models import Entry
from miniflux_tui.constants import CONTENT_SEPARATOR
from miniflux_tui.ui.protocols import EntryReaderAppProtocol
from miniflux_tui.utils import get_star_icon


class EntryReaderScreen(Screen):
    """Screen for reading a single feed entry."""

    BINDINGS: list[Binding] = [  # noqa: RUF012
        # Scrolling
        Binding("j", "scroll_down", "Scroll Down", show=False),
        Binding("k", "scroll_up", "Scroll Up", show=False),
        Binding("pagedown", "page_down", "Page Down"),
        Binding("pageup", "page_up", "Page Up"),
        # Entry navigation (matches web interface)
        Binding("J", "next_entry", "Next Entry", show=True),
        Binding("K", "previous_entry", "Previous Entry", show=True),
        # Entry actions
        Binding("m", "mark_read", "Mark Read", show=False),
        Binding("u", "mark_unread", "Mark Unread"),
        Binding("f", "toggle_star", "Toggle Starred"),
        Binding("e", "save_entry", "Save Entry"),
        Binding("o", "open_browser", "Open in Browser"),
        Binding("v", "open_browser", "Open URL", show=False),
        Binding("d", "fetch_original", "Download Original"),
        # Link navigation
        Binding("tab", "next_link", "Next Link", show=True),
        Binding("shift+tab", "previous_link", "Previous Link", show=True),
        Binding("n", "next_link", "Next Link", show=False),
        Binding("p", "previous_link", "Previous Link", show=False),
        Binding("enter", "open_focused_link", "Open Link", show=True),
        Binding("c", "clear_link_focus", "Clear Link", show=True),
        # Navigation and settings
        Binding("b", "back", "Back to List"),
        Binding("escape", "back", "Back", show=False),
        Binding("X", "feed_settings", "Feed Settings"),
        # Help and status
        Binding("question_mark", "show_help", "Help"),
        Binding("i", "show_status", "Status"),
        Binding("S", "show_settings", "Settings"),
        Binding("q", "quit", "Quit"),
    ]

    app: EntryReaderAppProtocol

    DEFAULT_CSS = """
    EntryReaderScreen {
        layout: vertical;
    }

    .entry-title {
        height: auto;
    }

    .entry-meta {
        height: auto;
    }

    .entry-url {
        height: auto;
    }

    .separator {
        height: auto;
    }

    .entry-content {
        height: 1fr;
        overflow: auto;
    }

    /* Highlight focused links within Markdown */
    Markdown:focus-within {
        border: tall $accent;
    }

    #link-indicator {
        height: auto;
    }

    .link-highlight {
        background: $accent;
        color: $text;
        text-style: bold;
    }
    """

    def __init__(
        self,
        entry: Entry,
        entry_list: list | None = None,
        current_index: int = 0,
        unread_color: str = "cyan",
        read_color: str = "gray",
        group_info: dict[str, str | int] | None = None,
        link_highlight_bg: str | None = None,
        link_highlight_fg: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.entry = entry
        self.entry_list = entry_list or []
        self.current_index = current_index
        self.unread_color = unread_color
        self.read_color = read_color
        self.group_info = group_info  # Contains: mode, name, total, unread
        self.link_highlight_bg = link_highlight_bg or "#ff79c6"  # Default: pink/magenta
        self.link_highlight_fg = link_highlight_fg or "#282a36"  # Default: dark text
        self.scroll_container = None
        self.group_stats_widget: Static | None = None  # Reference to group stats widget for updates
        self.links: list[dict[str, str]] = []  # List of {text: str, url: str}
        self.focused_link_index: int | None = None  # Currently focused link index
        self.link_indicator: Static | None = None  # Widget to show focused link
        self.original_content: str = ""  # Store original markdown content for highlighting

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()

        # Entry metadata
        star_icon = get_star_icon(self.entry.starred)

        # Title and metadata (fixed height)
        yield Static(
            f"[bold cyan]{star_icon} {self.entry.title}[/bold cyan]",
            classes="entry-title",
        )
        yield Static(
            f"[dim]{self.entry.feed.title} | {self.entry.published_at.strftime('%Y-%m-%d %H:%M')}[/dim]",
            classes="entry-meta",
        )

        # Add group statistics if available
        group_stats_text = self._get_group_stats_text()
        if group_stats_text:
            group_stats_widget = Static(group_stats_text, classes="entry-meta")
            self.group_stats_widget = group_stats_widget
            yield group_stats_widget

        yield Static(f"[dim]{self.entry.url}[/dim]", classes="entry-url")
        yield Static(CONTENT_SEPARATOR, classes="separator")

        # Convert HTML content to markdown for better display
        content = self._html_to_markdown(self.entry.content)

        # Store original content for highlighting
        self.original_content = content

        # Extract links from content
        self.links = self._extract_links(content)

        # Scrollable markdown content (takes remaining height)
        yield Markdown(content, id="entry-content", classes="entry-content")

        # Link navigation indicator (fixed height)
        link_indicator = Static("", id="link-indicator", classes="link-indicator")
        self.link_indicator = link_indicator
        yield link_indicator

        yield Footer()

    async def on_mount(self) -> None:
        """Called when screen is mounted."""
        # Get reference to the Markdown widget (now the scrollable container)
        self.scroll_container = self.query_one(Markdown)

        # Set title to just the application name (no feed name or entry title)
        self.title = ""
        # Clear subtitle (remove counts from there)
        self.sub_title = ""

        # Check terminal size constraints
        self._check_terminal_size()

        # Mark entry as read when opened
        if self.entry.is_unread:
            await self._mark_entry_as_read()

    def _check_terminal_size(self) -> None:
        """Check if terminal meets minimum size requirements.

        Validates:
        - Minimum 60 columns for readable content
        - Minimum 10 rows for Markdown content (plus ~2-3 rows for header/footer/metadata)

        Emits warning notifications if constraints aren't met.
        """
        # Get terminal size from app
        terminal_width = self.app.size.width  # type: ignore[attr-defined]
        terminal_height = self.app.size.height  # type: ignore[attr-defined]

        # Calculate available space for content (excluding header, footer, and metadata)
        # Header: 1 row
        # Footer: 1 row
        # Title: 1 row
        # Metadata: 1-2 rows
        # Separator: 1 row
        # Link indicator: 1 row
        # Total non-content rows: ~6-7 rows
        min_content_rows = 10
        min_content_width = 60
        min_total_rows = min_content_rows + 6

        warnings = []

        if terminal_height < min_total_rows:
            available_content_rows = max(1, terminal_height - 6)
            warnings.append(
                f"Terminal height ({terminal_height} rows) is below recommended minimum ({min_total_rows} rows). "
                f"Content area will have only ~{available_content_rows} rows for scrolling."
            )

        if terminal_width < min_content_width:
            warnings.append(
                f"Terminal width ({terminal_width} columns) is below recommended minimum ({min_content_width} columns). "
                f"Text may wrap awkwardly."
            )

        # Emit warnings
        for warning in warnings:
            self.notify(warning, severity="warning")

    def on_resize(self) -> None:
        """Handle terminal resize events.

        Re-checks terminal size constraints when terminal is resized.
        """
        self._check_terminal_size()

    def _resolve_app(self) -> EntryReaderAppProtocol | None:
        """Return the parent TUI app if it satisfies the expected protocol."""

        app = self.app
        if isinstance(app, EntryReaderAppProtocol):
            return app
        return None

    def _calculate_group_info(self) -> dict[str, str | int] | None:
        """Calculate group statistics from current entry and entry list.

        Returns:
            Dictionary with keys: mode, name, total, unread
            None if not in grouped mode
        """
        if not self.group_info:
            return None

        mode = self.group_info.get("mode")
        if mode not in ("feed", "category"):
            return None

        # Determine group identifier based on mode
        group_key = self.entry.feed.title if mode == "feed" else self._get_category_name()

        # Count entries in the same group
        total = 0
        unread = 0
        for entry in self.entry_list:
            entry_group = entry.feed.title if mode == "feed" else self._get_entry_category_name(entry)
            if entry_group == group_key:
                total += 1
                if entry.is_unread:
                    unread += 1

        return {
            "mode": mode,
            "name": group_key,
            "total": total,
            "unread": unread,
        }

    def _get_category_name(self) -> str:
        """Get category name for current entry.

        Returns:
            Category name or "Uncategorized"
        """
        if not hasattr(self.entry.feed, "category_id") or self.entry.feed.category_id is None:
            return "Uncategorized"

        # Try to get category name from app's categories
        app_obj = self.app
        if hasattr(app_obj, "categories"):
            # Type: ignore because protocol doesn't include categories
            for category in app_obj.categories:  # type: ignore[attr-defined]
                if category.id == self.entry.feed.category_id:
                    return category.title

        return f"Category {self.entry.feed.category_id}"

    def _get_entry_category_name(self, entry: Entry) -> str:
        """Get category name for a given entry.

        Args:
            entry: Entry to get category name for

        Returns:
            Category name or "Uncategorized"
        """
        if not hasattr(entry.feed, "category_id") or entry.feed.category_id is None:
            return "Uncategorized"

        # Try to get category name from app's categories
        app_obj = self.app
        if hasattr(app_obj, "categories"):
            # Type: ignore because protocol doesn't include categories
            for category in app_obj.categories:  # type: ignore[attr-defined]
                if category.id == entry.feed.category_id:
                    return category.title

        return f"Category {entry.feed.category_id}"

    def _update_sub_title(self) -> None:
        """Clear the sub_title (counts are now in feed header)."""
        # Subtitle is no longer used - title shows entry and feed info
        self.sub_title = ""

    def _get_group_stats_text(self) -> str:
        """Get formatted group statistics text for display in entry view.

        Returns:
            Formatted string with group statistics, or empty string if not in grouped mode
        """
        group_stats = self._calculate_group_info()
        if group_stats:
            mode = group_stats["mode"]
            unread = group_stats["unread"]
            total = group_stats["total"]
            mode_label = "Feed" if mode == "feed" else "Category"
            # Format as: "Feed: 5 unread / 20 total"
            return f"[dim]{mode_label}: {unread} unread / {total} total[/dim]"
        return ""

    async def _mark_entry_as_read(self):
        """Mark the current entry as read via API."""
        app = self._resolve_app()
        if app and app.client:
            try:
                await app.client.mark_as_read(self.entry.id)
                self.entry.status = "read"

                # Also update the entry in the entry_list if it exists there
                for entry in self.entry_list:
                    if entry.id == self.entry.id:
                        entry.status = "read"
                        break

                # Update group stats widget to reflect new unread count
                if self.group_stats_widget:
                    updated_stats = self._get_group_stats_text()
                    self.group_stats_widget.update(updated_stats)

                # Update sub_title to reflect new unread count
                self._update_sub_title()
            except Exception as e:
                self.log(f"Error marking as read: {e}")
                self.log(traceback.format_exc())
                self.notify(f"Error marking as read: {e}", severity="error")

    @staticmethod
    def _html_to_markdown(html_content: str) -> str:
        """Convert HTML content to markdown for display.

        Converts HTML from RSS feed entries to markdown format for better
        terminal display. Preserves links, images, and formatting information.

        Args:
            html_content: Raw HTML content from the entry

        Returns:
            Markdown-formatted string suitable for terminal display
        """
        h = html2text.HTML2Text()
        # Preserve links, images, and emphasis in the output
        h.ignore_links = False
        h.ignore_images = False
        h.ignore_emphasis = False
        # Disable body width wrapping - let Textual handle terminal wrapping
        h.body_width = 0
        return h.handle(html_content)

    @staticmethod
    def _extract_links(markdown_content: str) -> list[dict[str, str]]:
        """Extract all links from markdown content.

        Finds both markdown-style links [text](url) and plain URLs in the content.

        Args:
            markdown_content: Markdown-formatted content

        Returns:
            List of dictionaries with 'text' and 'url' keys for each link found
        """
        links = []

        # Extract markdown links: [text](url)
        markdown_link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        for match in re.finditer(markdown_link_pattern, markdown_content):
            text, url = match.groups()
            links.append({"text": text.strip(), "url": url.strip()})

        # Extract plain URLs (http/https) that aren't already in markdown links
        # This is a simple pattern - doesn't catch all edge cases
        plain_url_pattern = r"(?<!\()(https?://[^\s)\]]+)"
        for match in re.finditer(plain_url_pattern, markdown_content):
            url = match.group(1).strip()
            # Only add if not already in our links list
            if not any(link["url"] == url for link in links):
                links.append({"text": url, "url": url})

        return links

    def _ensure_scroll_container(self) -> Markdown:
        """Ensure markdown widget (scrollable container) is initialized and return it.

        Lazily initializes the markdown widget reference if not already set.
        This eliminates the repeated pattern of checking and initializing
        the markdown widget across multiple scroll action methods.

        Returns:
            The Markdown widget
        """
        if not self.scroll_container:
            self.scroll_container = self.query_one(Markdown)
        return self.scroll_container

    def action_scroll_down(self):
        """Scroll down one line."""
        self._ensure_scroll_container().scroll_down()

    def action_scroll_up(self):
        """Scroll up one line."""
        self._ensure_scroll_container().scroll_up()

    def action_page_down(self):
        """Scroll down one page."""
        self._ensure_scroll_container().scroll_page_down()

    def action_page_up(self):
        """Scroll up one page."""
        self._ensure_scroll_container().scroll_page_up()

    def action_back(self):
        """Return to entry list."""
        app = self._resolve_app()
        if app:
            app.pop_screen()

    async def action_mark_read(self):
        """Mark entry as read."""
        await self._mark_entry_as_read()
        self.notify("Marked as read")

    async def action_mark_unread(self):
        """Mark entry as unread."""
        app = self._resolve_app()
        if app and app.client:
            try:
                await app.client.mark_as_unread(self.entry.id)
                self.entry.status = "unread"
                self.notify("Marked as unread")
                # Update sub_title to reflect new unread count
                self._update_sub_title()
            except Exception as e:
                self.notify(f"Error marking as unread: {e}", severity="error")

    async def action_toggle_star(self):
        """Toggle star status."""
        app = self._resolve_app()
        if app and app.client:
            try:
                await app.client.toggle_starred(self.entry.id)
                self.entry.starred = not self.entry.starred
                status = "starred" if self.entry.starred else "unstarred"
                self.notify(f"Entry {status}")

                # Refresh display to update star icon
                await self.refresh_screen()
            except Exception as e:
                self.notify(f"Error toggling star: {e}", severity="error")

    async def action_save_entry(self):
        """Save entry to third-party service."""
        app = self._resolve_app()
        if app and app.client:
            try:
                await app.client.save_entry(self.entry.id)
                self.notify(f"Entry saved: {self.entry.title}")
            except Exception as e:
                self.notify(f"Failed to save entry: {e}", severity="error")

    @staticmethod
    def _is_safe_external_url(url: str) -> bool:
        """Return True if the URL uses an allowed scheme and has a hostname."""
        if not url:
            return False

        parsed = urlparse(url.strip())
        if parsed.scheme not in {"http", "https"}:
            return False
        if not parsed.netloc:
            return False

        return not any(ord(char) < 32 for char in url)

    def action_open_browser(self):
        """Open entry URL in web browser."""
        url = (self.entry.url or "").strip()
        if not url:
            self.notify("Entry does not contain a URL to open", severity="warning")
            return
        if not self._is_safe_external_url(url):
            self.notify("Refused to open unsafe entry URL", severity="error")
            if url:
                with suppress(Exception):
                    self.log(f"Blocked attempt to open unsafe URL: {url!r}")
            return

        try:
            webbrowser.open(url)
            self.notify(f"Opened in browser: {url}")
        except Exception as e:
            self.notify(f"Error opening browser: {e}", severity="error")

    async def action_fetch_original(self):
        """Fetch original content from source."""
        app = self._resolve_app()
        if app and app.client:
            try:
                self.notify("Fetching original content...")

                # Fetch original content from API
                original_content = await app.client.fetch_original_content(self.entry.id)

                if original_content:
                    # Update the entry's content
                    self.entry.content = original_content

                    # Refresh the screen to show new content
                    await self.refresh_screen()

                    self.notify("Original content loaded")
                else:
                    self.notify("No original content available", severity="warning")
            except Exception as e:
                self.log(f"Error fetching original content: {e}")
                self.log(traceback.format_exc())
                self.notify(f"Error fetching content: {e}", severity="error")

    async def action_next_entry(self):
        """Navigate to next entry."""
        if not self.entry_list or self.current_index >= len(self.entry_list) - 1:
            self.notify("No next entry", severity="warning")
            return

        # Move to next entry
        self.current_index += 1
        self.entry = self.entry_list[self.current_index]

        # Refresh the screen with new entry
        await self.refresh_screen()

        # Update sub_title with new group stats
        self._update_sub_title()

    async def action_previous_entry(self):
        """Navigate to previous entry."""
        if not self.entry_list or self.current_index <= 0:
            self.notify("No previous entry", severity="warning")
            return

        # Move to previous entry
        self.current_index -= 1
        self.entry = self.entry_list[self.current_index]

        # Refresh the screen with new entry
        await self.refresh_screen()

        # Update sub_title with new group stats
        self._update_sub_title()

    async def refresh_screen(self):
        """Refresh the screen with current entry.

        Updates all entry content widgets with the new entry's information
        and scrolls back to the top.
        """
        # Update title widget
        title_widgets = self.query(".entry-title")
        if title_widgets:
            star_icon = get_star_icon(self.entry.starred)
            title_widgets[0].update(f"[bold cyan]{star_icon} {self.entry.title}[/bold cyan]")  # type: ignore[union-attr]

        # Update metadata widget (feed name and date)
        meta_widgets = self.query(".entry-meta")
        if meta_widgets:
            meta_widgets[0].update(f"[dim]{self.entry.feed.title} | {self.entry.published_at.strftime('%Y-%m-%d %H:%M')}[/dim]")  # type: ignore[union-attr]

        # Update group stats if available (second meta widget if it exists)
        group_stats_text = self._get_group_stats_text()
        if group_stats_text:
            if len(meta_widgets) > 1:
                meta_widgets[1].update(group_stats_text)  # type: ignore[union-attr]
                self.group_stats_widget = meta_widgets[1]  # type: ignore[assignment]
            else:
                # Create new group stats widget if it doesn't exist
                title_widget = title_widgets[0] if title_widgets else None
                if title_widget and title_widget.parent:
                    group_stats = Static(group_stats_text, classes="entry-meta")
                    self.group_stats_widget = group_stats
                    # Insert after first meta widget
                    title_widget.parent.mount(group_stats, before=meta_widgets[0] if meta_widgets else None)  # type: ignore[union-attr]

        # Update URL widget
        url_widgets = self.query(".entry-url")
        if url_widgets:
            url_widgets[0].update(f"[dim]{self.entry.url}[/dim]")  # type: ignore[union-attr]

        # Update content (Markdown widget)
        markdown_widgets = self.query_one("#entry-content", expect_type=Markdown)  # type: ignore[arg-type]
        content = self._html_to_markdown(self.entry.content)
        markdown_widgets.update(content)

        # Extract links from new content
        self.links = self._extract_links(content)
        self.focused_link_index = None  # Reset link focus on new content

        # Update link indicator
        self._update_link_indicator()

        # Scroll back to top
        markdown_widgets.scroll_home(animate=False)

        # Mark as read after displaying
        if self.entry.is_unread:
            await self._mark_entry_as_read()

    async def action_feed_settings(self) -> None:
        """Open feed settings screen for current entry's feed."""
        # Import here to avoid circular dependency
        from miniflux_tui.ui.screens.feed_settings import FeedSettingsScreen  # noqa: PLC0415

        if not self.app.client:
            self.notify("API client not available", severity="error")
            return

        # Push feed settings screen
        screen = FeedSettingsScreen(
            feed_id=self.entry.feed.id,
            feed=self.entry.feed,
            client=self.app.client,  # type: ignore[arg-type]
        )
        self.app.push_screen(screen)  # type: ignore[arg-type]

    def action_show_help(self):
        """Show keyboard help."""
        app = self._resolve_app()
        if app:
            app.push_screen("help")

    def action_show_status(self):
        """Show system status and feed health."""
        app = self._resolve_app()
        if app:
            app.push_screen("status")

    def action_show_settings(self):
        """Show user settings and integrations."""
        app = self._resolve_app()
        if app:
            app.push_screen("settings")

    def _get_markdown_link_widgets(self) -> list:
        """Get all link widgets from the Markdown widget.

        Returns:
            List of link widgets found in the Markdown content
        """
        try:
            markdown_widget = self.query_one("#entry-content", expect_type=Markdown)
            # Try to find link widgets within the Markdown widget
            # Links in Markdown might be nested in various ways
            return list(markdown_widget.query("Link"))
        except Exception:
            # If we can't query links, return empty list
            return []

    def _scroll_to_link(self, link_index: int):
        """Scroll to make the focused link visible.

        Args:
            link_index: Index of the link in self.links to scroll to
        """
        if not self.links or link_index < 0 or link_index >= len(self.links):
            return

        try:
            # Try to get link widgets from the Markdown widget
            link_widgets = self._get_markdown_link_widgets()

            if link_widgets and link_index < len(link_widgets):
                # If we have actual link widgets, focus and scroll to the specific one
                target_link = link_widgets[link_index]
                target_link.focus()
                target_link.scroll_visible(animate=True, duration=0.3, top=True)
            else:
                # Fallback: estimate position based on markdown content
                # This is an approximation since we don't have exact widget positions
                self._estimate_and_scroll_to_link(link_index)
        except Exception:  # nosec B110  # noqa: S110
            # Silently fail if scrolling isn't possible (e.g., screen not mounted)
            # This is expected in test contexts or when the widget isn't available
            # Intentional silent failure for graceful degradation
            pass

    def _estimate_and_scroll_to_link(self, link_index: int):
        """Estimate link position and scroll there (fallback method).

        Args:
            link_index: Index of the link to scroll to
        """
        try:
            markdown_widget = self.query_one("#entry-content", expect_type=Markdown)
            link = self.links[link_index]

            # Get the markdown content
            content = self._html_to_markdown(self.entry.content)

            # Find the position of the link in the content
            # For markdown links: [text](url)
            link_pattern = f"[{link['text']}]({link['url']})"
            pos = content.find(link_pattern)

            # If not found, try finding just the URL
            if pos == -1:
                pos = content.find(link["url"])

            if pos != -1:
                # Estimate the line number (rough approximation)
                # Count newlines before the link position
                lines_before = content[:pos].count("\n")

                # Get terminal height to calculate scroll position
                # Using screen size instead of app.size (which isn't in protocol)
                terminal_height = self.screen.size.height if hasattr(self.screen, "size") else 24
                content_height = markdown_widget.virtual_size.height

                # Calculate approximate Y position
                # This is rough - assumes even line distribution
                if content_height > 0:
                    y_pos = (lines_before / content.count("\n")) * content_height if content.count("\n") > 0 else 0

                    # Scroll to position (centered if possible)
                    offset = terminal_height // 3  # Show link in upper third of screen
                    scroll_y = max(0, y_pos - offset)

                    markdown_widget.scroll_to(y=scroll_y, animate=True, duration=0.3)
        except Exception:  # nosec B110  # noqa: S110
            # Silently fail if scrolling isn't possible (e.g., screen not mounted)
            # This is expected in test contexts or when the widget isn't available
            # Intentional silent failure for graceful degradation
            pass

    def _update_link_indicator(self):
        """Update the link indicator widget with current focused link info."""
        if not self.link_indicator:
            return

        if self.focused_link_index is None or not self.links:
            self.link_indicator.update("")
            return

        # Show focused link info
        link = self.links[self.focused_link_index]
        link_num = self.focused_link_index + 1
        total_links = len(self.links)

        # Truncate long URLs/text for display
        display_text = link["text"]
        if len(display_text) > 60:
            display_text = display_text[:57] + "..."

        display_url = link["url"]
        if len(display_url) > 80:
            display_url = display_url[:77] + "..."

        indicator_text = f"[bold yellow]Link {link_num}/{total_links}:[/bold yellow] [cyan]{display_text}[/cyan]\n[dim]{display_url}[/dim]"

        self.link_indicator.update(indicator_text)

    def _generate_highlighted_markdown(self, original_content: str) -> str:
        """Generate markdown with visual highlight for the focused link.

        This method re-renders the original markdown to add visual highlighting
        around the currently focused link using markdown formatting that the
        Markdown widget will interpret.

        Args:
            original_content: The original markdown content

        Returns:
            Markdown content with highlighting added for the focused link
        """
        if self.focused_link_index is None or not self.links or self.focused_link_index >= len(self.links):
            return original_content

        try:
            content = original_content
            focused_link = self.links[self.focused_link_index]
            link_url = focused_link["url"].strip()
            link_text = focused_link["text"].strip()

            # Find and replace the markdown link pattern with a highlighted version
            # Pattern: [text](url)
            # Use markdown's bold (**) and code block style for background effect
            # We'll wrap it with visual markers that work in terminal: ***text***
            markdown_pattern = rf"\[{re.escape(link_text)}\]\({re.escape(link_url)}\)"

            # Use markdown's emphasis to make it stand out: ***bold italic***
            # Or use code styling: `[text](url)` for monospace/highlight effect
            # Since we can't easily do background colors in markdown, we'll use
            # bold + inversion via combining multiple emphasis styles
            replacement = f"***[{link_text}]({link_url})***"

            return re.sub(markdown_pattern, replacement, content, count=1)
        except Exception:  # nosec B110
            # Silently fail and return original content if highlighting fails
            return original_content

    def _focus_link_widget(self) -> None:
        """Focus the Link widget corresponding to the current focused_link_index.

        This method attempts to manipulate link widgets if available, and falls back
        to re-rendering markdown with visual highlighting.
        """
        if self.focused_link_index is None or not self.links:
            return

        try:
            # Try the widget approach first (may not work in all cases)
            link_widgets = self._get_markdown_link_widgets()

            if link_widgets and self.focused_link_index < len(link_widgets):
                # Clear previous link styling
                for i, link_widget in enumerate(link_widgets):
                    if i != self.focused_link_index:
                        # Reset to default styles (remove inline styles)
                        link_widget.styles.clear()

                # Focus and style the specific link widget at the focused index
                target_link = link_widgets[self.focused_link_index]
                target_link.focus()

                # Apply inline styles with configured colors
                target_link.styles.background = self.link_highlight_bg
                target_link.styles.color = self.link_highlight_fg
                target_link.styles.text_style = "bold"

                # Scroll to make it visible
                target_link.scroll_visible(animate=True, duration=0.3, top=True)
        except Exception:  # nosec B110  # noqa: S110
            # Silently fail if focusing isn't possible (e.g., screen not mounted)
            # This is expected in test contexts or when the widget isn't available
            # Intentional silent failure for graceful degradation
            pass

    def _update_markdown_display(self):
        """Update the markdown display to highlight the currently focused link.

        This method regenerates the markdown content with visual highlighting
        for the focused link and scrolls to ensure it's visible on screen.
        """
        # Generate markdown with highlighting for the focused link
        if self.original_content:
            highlighted_md = self._generate_highlighted_markdown(self.original_content)

            try:
                markdown_widget = self.query_one("#entry-content", expect_type=Markdown)
                markdown_widget.update(highlighted_md)

                # Scroll to approximately where the link should be
                # Estimate based on link position in content
                if self.focused_link_index is not None:
                    self._scroll_to_link(self.focused_link_index)
            except Exception:  # nosec B110  # noqa: S110
                # If markdown update fails, that's okay - highlighting is optional
                pass

        # Also try the widget focusing approach as a fallback
        self._focus_link_widget()

    def action_next_link(self):
        """Navigate to the next link in the content."""
        if not self.links:
            self.notify("No links found in this entry", severity="warning")
            return

        if self.focused_link_index is None:
            # Start at first link
            self.focused_link_index = 0
        else:
            # Move to next link (wrap around)
            self.focused_link_index = (self.focused_link_index + 1) % len(self.links)

        self._update_link_indicator()
        # Update markdown display with highlighting (includes scrolling)
        self._update_markdown_display()

    def action_previous_link(self):
        """Navigate to the previous link in the content."""
        if not self.links:
            self.notify("No links found in this entry", severity="warning")
            return

        if self.focused_link_index is None:
            # Start at last link
            self.focused_link_index = len(self.links) - 1
        else:
            # Move to previous link (wrap around)
            self.focused_link_index = (self.focused_link_index - 1) % len(self.links)

        self._update_link_indicator()
        # Update markdown display with highlighting (includes scrolling)
        self._update_markdown_display()

    def action_open_focused_link(self):
        """Open the currently focused link in the browser."""
        if self.focused_link_index is None or not self.links:
            self.notify("No link focused. Use Tab to focus a link first.", severity="warning")
            return

        link = self.links[self.focused_link_index]
        url = link["url"].strip()

        if not self._is_safe_external_url(url):
            self.notify("Refused to open unsafe URL", severity="error")
            if url:
                with suppress(Exception):
                    self.log(f"Blocked attempt to open unsafe URL: {url!r}")
            return

        try:
            webbrowser.open(url)
            self.notify(f"Opened link: {link['text']}")
        except Exception as e:
            self.notify(f"Error opening link: {e}", severity="error")

    def action_clear_link_focus(self):
        """Clear the current link focus."""
        # First blur the currently focused link widget if any
        try:
            link_widgets = self._get_markdown_link_widgets()
            if link_widgets and self.focused_link_index is not None and self.focused_link_index < len(link_widgets):
                link_widgets[self.focused_link_index].blur()
        except Exception:  # nosec B110  # noqa: S110
            # Intentional silent failure for graceful degradation
            pass

        self.focused_link_index = None
        self._update_link_indicator()
        self.notify("Link focus cleared")

    def action_quit(self):
        """Quit the application."""
        app = self._resolve_app()
        if app:
            app.exit()
