# SPDX-License-Identifier: MIT
"""Help screen showing keyboard shortcuts and application information."""

import platform
import sys

import textual
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from miniflux_tui.utils import get_app_version


class HelpScreen(Screen):
    """Screen displaying keyboard shortcuts and help information."""

    BINDINGS: list[Binding] = [  # noqa: RUF012
        Binding("escape", "close", "Close"),
        Binding("q", "close", "Close"),
    ]

    def __init__(self, **kwargs):
        """Initialize help screen with server info placeholders."""
        super().__init__(**kwargs)
        self.server_version: str = "Loading..."
        self.api_version: str = "Loading..."
        self.username: str = "Loading..."

    def compose(self) -> ComposeResult:  # noqa: PLR0915
        """Create child widgets."""
        yield Header()

        with VerticalScroll():
            yield Static("[bold cyan]Miniflux TUI - Keyboard Shortcuts[/bold cyan]\n")

            yield Static("[bold yellow]Entry List View[/bold yellow]")
            yield Static("[bold white]Section Navigation (g-prefix)[/bold white]")
            yield Static("  g+u             Go to unread entries")
            yield Static("  g+b             Go to starred/bookmarked entries")
            yield Static("  g+h             Go to history")
            yield Static("  g+c             Group entries by category (with counts)")
            yield Static("  g+C             Go to category management")
            yield Static("  g+f             Go to feed management")
            yield Static("  g+s             Go to settings")
            yield Static("  gg              Go to top of list")
            yield Static("  G               Go to bottom of list")
            yield Static("")
            yield Static("[bold white]Navigation[/bold white]")
            yield Static("  ↑/↓ or k/j/p/n  Navigate entries")
            yield Static("  h or ←          Collapse individual feed/category")
            yield Static("  l or →          Expand individual feed/category")
            yield Static("  Enter           Open entry (or first in feed if on header)")
            yield Static("")
            yield Static("[bold white]Entry Actions[/bold white]")
            yield Static("  m               Toggle read/unread")
            yield Static("  M               Toggle read/unread (focus previous)")
            yield Static("  f               Toggle star/bookmark")
            yield Static("  e               Save entry to third-party service")
            yield Static("  A               Mark all entries as read")
            yield Static("")
            yield Static("[bold white]View Controls[/bold white]")
            yield Static("  s               Cycle sort mode (date/feed/status)")
            yield Static("  w               Toggle grouping by feed")
            yield Static("  C               Toggle grouping by category")
            yield Static("  Shift+L         Expand all feeds")
            yield Static("  Z               Collapse all feeds")
            yield Static("  /               Search entries (interactive dialog)")
            yield Static("  [dim]Feed headers show category and error status[/dim]")
            yield Static("")
            yield Static("[bold white]Feed Operations[/bold white]")
            yield Static("  r               Refresh current feed on server")
            yield Static("  R               Refresh all feeds on server")
            yield Static("  ,               Sync entries from server (fetch new)")
            yield Static("  [dim]Use 'r' or 'R' to tell server to fetch RSS, then ',' to sync[/dim]")
            yield Static("")
            yield Static("[bold white]Other Actions[/bold white]")
            yield Static("  X               Edit feed settings")
            yield Static("  T               Toggle theme (dark/light)")
            yield Static("  ?               Show this help")
            yield Static("  i               Show system status")
            yield Static("  H               Go to reading history (or g+h)")
            yield Static("  S               Go to settings (or g+s)")
            yield Static("  q               Quit application\n")

            yield Static("[bold yellow]Reading History View[/bold yellow]")
            yield Static("  [dim]Shows your 200 most recently read entries[/dim]")
            yield Static("  ↑/↓ or k/j      Navigate entries")
            yield Static("  Enter           Open entry")
            yield Static("  m               Toggle read/unread")
            yield Static("  *               Toggle star")
            yield Static("  H               Return to main entry list")
            yield Static("  [dim]All other entry list keys work the same[/dim]\n")

            yield Static("[bold yellow]Category Management View[/bold yellow]")
            yield Static("  ↑/↓ or k/j      Navigate categories")
            yield Static("  n               Create new category")
            yield Static("  e               Edit selected category name")
            yield Static("  d               Delete selected category")
            yield Static("  Esc or q        Return to entry list\n")

            yield Static("[bold yellow]Entry Reader View[/bold yellow]")
            yield Static("[bold white]Navigation[/bold white]")
            yield Static("  ↑/↓ or k/j      Scroll up/down")
            yield Static("  PageUp/PageDown Fast scroll")
            yield Static("  J               Next entry")
            yield Static("  K               Previous entry")
            yield Static("  b or Esc        Back to list")
            yield Static("")
            yield Static("[bold white]Entry Actions[/bold white]")
            yield Static("  m               Mark as read")
            yield Static("  u               Mark as unread")
            yield Static("  f               Toggle star/bookmark")
            yield Static("  e               Save entry to third-party service")
            yield Static("  o or v          Open in browser")
            yield Static("  d               Download/fetch original content")
            yield Static("  Tab/Shift+Tab   Navigate links in content")
            yield Static("  Enter           Open focused link")
            yield Static("  c               Clear link focus")
            yield Static("")
            yield Static("[bold white]Other Actions[/bold white]")
            yield Static("  X               Edit feed settings")
            yield Static("  ?               Show this help")
            yield Static("  i               Show system status")
            yield Static("  S               Go to settings")
            yield Static("  q               Quit application\n")

            yield Static("[bold yellow]About[/bold yellow]")
            yield Static(self._get_about_text())
            yield Static()

            yield Static("[bold yellow]System Information[/bold yellow]")
            # Use id for easier reference and initial placeholder
            yield Static(id="system-info-widget")
            yield Static()

            yield Static("[dim]Press Esc or q to close this help screen[/dim]")

        yield Footer()

    @staticmethod
    def _get_about_text() -> str:
        """Generate about section text with application information.

        Returns:
            Formatted text with app info
        """
        app_version = get_app_version()
        return (
            f"  Application:     Miniflux TUI\n"
            f"  Version:         {app_version}\n"
            f"  Repository:      github.com/reuteras/miniflux-tui-py\n"
            f"  License:         MIT"
        )

    def _get_system_info_text(self) -> str:
        """Generate system information text.

        Returns:
            Formatted text with system and server info
        """
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        platform_name = platform.system()

        return (
            f"  Python:          {python_version}\n"
            f"  Platform:        {platform_name}\n"
            f"  Textual:         {textual.__version__}\n"
            f"  Miniflux API:    {self.api_version}\n"
            f"  Miniflux Server: {self.server_version}\n"
            f"  Username:        {self.username}"
        )

    async def on_mount(self) -> None:
        """Called when screen is mounted - load server information."""
        await self._load_server_info()

    async def _load_server_info(self) -> None:
        """Load server version and user information from API."""
        if not hasattr(self.app, "client") or not getattr(self.app, "client", None):
            self.api_version = "unavailable"
            self.server_version = "unavailable"
            self.username = "unavailable"
            return

        try:
            client = getattr(self.app, "client", None)
            # Get version info
            version_info = await client.get_version()
            self.api_version = version_info.get("version", "unknown")

            # Get user info
            user_info = await client.get_user_info()
            self.username = user_info.get("username", "unknown")
            self.server_version = version_info.get("version", "unknown")

            # Update the screen to show new info
            self._update_system_info()
        except Exception as e:
            self.app.log(f"Error loading server info: {e}")
            self.api_version = f"error: {type(e).__name__}"
            self.server_version = "error"
            self.username = "error"
            self._update_system_info()

    def _update_system_info(self) -> None:
        """Update the system information display."""
        # Update the system info widget by ID
        try:
            widget = self.query_one("#system-info-widget", Static)
            widget.update(self._get_system_info_text())
        except Exception as e:
            # If widget not found, silently fail (widget might not be mounted yet)
            self.app.log(f"Could not update system info widget: {e}")

    def action_close(self):
        """Close the help screen."""
        self.app.pop_screen()
