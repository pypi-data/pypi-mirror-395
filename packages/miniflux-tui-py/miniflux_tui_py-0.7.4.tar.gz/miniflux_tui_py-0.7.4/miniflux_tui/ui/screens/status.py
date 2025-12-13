# SPDX-License-Identifier: MIT
"""Status screen showing server information and problematic feeds."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from miniflux_tui.api.models import Feed


class StatusScreen(Screen):
    """Screen displaying server status and feed health information."""

    BINDINGS: list[Binding] = [  # noqa: RUF012
        Binding("escape", "close", "Close"),
        Binding("q", "close", "Close"),
        Binding("r", "refresh", "Refresh"),
    ]

    def __init__(self, **kwargs):
        """Initialize status screen."""
        super().__init__(**kwargs)
        self.server_version: str = "Loading..."
        self.server_url: str = "Loading..."
        self.username: str = "Loading..."
        self.feeds: list[Feed] = []
        self.error_feeds: list[Feed] = []
        self._header_widget: Header | None = None
        self._scroll_container: VerticalScroll | None = None
        self._footer_widget: Footer | None = None

    app: App

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        header = Header()
        scroll = VerticalScroll()
        footer = Footer()

        self._header_widget = header
        self._scroll_container = scroll
        self._footer_widget = footer

        yield header

        with scroll:
            yield Static("[bold cyan]System Status[/bold cyan]\n", id="title")

            yield Static("[bold yellow]Server Information[/bold yellow]")
            yield Static(id="server-info")
            yield Static()

            yield Static("[bold yellow]Feed Health[/bold yellow]")
            yield Static(id="feed-health-summary")
            yield Static()

            yield Static("[bold yellow]Problematic Feeds[/bold yellow]")
            yield Static(id="error-feeds-list")
            yield Static()

            yield Static("[dim]Press r to refresh, Esc or q to close[/dim]")

        yield footer

    async def on_mount(self) -> None:
        """Called when screen is mounted - load status information."""
        await self._load_status()

    async def _load_status(self) -> None:
        """Load server and feed status from API."""
        if not hasattr(self.app, "client") or not getattr(self.app, "client", None):
            self._update_error_state("API client not available")
            return

        try:
            client = getattr(self.app, "client", None)

            # Get server version
            version_info = await client.get_version()
            self.server_version = version_info.get("version", "unknown")

            # Get user info
            user_info = await client.get_user_info()
            self.username = user_info.get("username", "unknown")

            # Get server URL from client
            self.server_url = client.base_url

            # Get all feeds
            self.feeds = await client.get_feeds()

            # Filter feeds with errors
            self.error_feeds = [feed for feed in self.feeds if feed.has_errors or feed.disabled]

            # Update the display
            self._update_display()

        except Exception as e:
            self.app.log(f"Error loading status: {e}")
            self._update_error_state(f"Error: {type(e).__name__}: {e}")

    def _update_error_state(self, error_message: str) -> None:
        """Update display when an error occurs."""
        try:
            server_info = self.query_one("#server-info", Static)
            server_info.update(f"[red]{error_message}[/red]")

            feed_health = self.query_one("#feed-health-summary", Static)
            feed_health.update("[dim]Unable to load feed health information[/dim]")

            error_feeds = self.query_one("#error-feeds-list", Static)
            error_feeds.update("[dim]Unable to load feed list[/dim]")
        except Exception as e:
            self.app.log(f"Could not update error state: {e}")

    def _update_display(self) -> None:
        """Update all status displays."""
        self._update_server_info()
        self._update_feed_health()
        self._update_error_feeds()

    def _update_server_info(self) -> None:
        """Update the server information display."""
        try:
            widget = self.query_one("#server-info", Static)
            lines = [
                f"  Server URL:      {self.server_url}",
                f"  Server Version:  {self.server_version}",
                f"  Username:        {self.username}",
            ]
            widget.update("\n".join(lines))
        except Exception as e:
            self.app.log(f"Could not update server info: {e}")

    def _update_feed_health(self) -> None:
        """Update the feed health summary."""
        try:
            widget = self.query_one("#feed-health-summary", Static)

            total_feeds = len(self.feeds)
            error_count = len(self.error_feeds)
            disabled_count = len([f for f in self.feeds if f.disabled])
            healthy_count = total_feeds - error_count

            if error_count == 0:
                status_text = "[green]All feeds are healthy ✓[/green]"
            else:
                status_text = f"[yellow]{error_count} feed(s) have issues[/yellow]"

            text = (
                f"  Total Feeds:     {total_feeds}\n"
                f"  Healthy:         {healthy_count}\n"
                f"  With Errors:     {error_count}\n"
                f"  Disabled:        {disabled_count}\n\n"
                f"  {status_text}"
            )
            widget.update(text)
        except Exception as e:
            self.app.log(f"Could not update feed health: {e}")

    def _update_error_feeds(self) -> None:
        """Update the list of problematic feeds."""
        try:
            widget = self.query_one("#error-feeds-list", Static)

            if not self.error_feeds:
                widget.update("  [green]No problematic feeds found ✓[/green]")
                return

            lines = []
            for feed in self.error_feeds:
                # Feed title and status
                status_parts = []
                if feed.disabled:
                    status_parts.append("[red]DISABLED[/red]")
                if feed.parsing_error_count > 0:
                    status_parts.append(f"[yellow]{feed.parsing_error_count} error(s)[/yellow]")

                status = " ".join(status_parts)
                lines.append(f"\n  [bold]{feed.title}[/bold] - {status}")
                lines.append(f"    URL: {feed.feed_url}")

                if feed.parsing_error_message:
                    # Truncate long error messages
                    error_msg = feed.parsing_error_message[:200]
                    if len(feed.parsing_error_message) > 200:
                        error_msg += "..."
                    lines.append(f"    Error: [red]{error_msg}[/red]")

                if feed.checked_at:
                    lines.append(f"    Last checked: {feed.checked_at}")

            widget.update("\n".join(lines))
        except Exception as e:
            self.app.log(f"Could not update error feeds list: {e}")

    def action_close(self):
        """Close the status screen."""
        self.app.pop_screen()

    async def action_refresh(self):
        """Refresh the status information."""
        # Show loading message
        try:
            server_info = self.query_one("#server-info", Static)
            server_info.update("[dim]Refreshing...[/dim]")
        except Exception as e:
            # Widget might not be mounted yet, silently continue
            self.app.log(f"Could not update refresh message: {e}")

        # Reload status
        await self._load_status()

        # Notify user
        self.app.notify("Status refreshed")
