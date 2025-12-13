# SPDX-License-Identifier: MIT
"""Settings screen showing TUI application configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from miniflux_tui.config import get_config_file_path

if TYPE_CHECKING:
    pass


class SettingsScreen(Screen):
    """Screen displaying TUI application settings."""

    BINDINGS: list[Binding] = [  # noqa: RUF012
        Binding("escape", "close", "Close"),
        Binding("q", "close", "Close"),
        Binding("i", "toggle_info_messages", "Toggle Info Messages"),
    ]

    CSS = """
    SettingsScreen {
        overflow-y: hidden;
    }
    """

    def __init__(self, **kwargs):
        """Initialize settings screen."""
        super().__init__(**kwargs)
        self._header_widget: Header | None = None
        self._scroll_container: VerticalScroll | None = None
        self._footer_widget: Footer | None = None

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
            yield Static("[bold cyan]TUI Settings[/bold cyan]\n", id="title")

            yield Static("[bold yellow]Application Configuration[/bold yellow]")
            yield Static(id="tui-config")
            yield Static()

            yield Static("[bold yellow]Configuration File[/bold yellow]")
            yield Static(id="config-file")
            yield Static()

            yield Static("[dim]Press 'i' to toggle info messages, Esc or q to close[/dim]")
            yield Static("[dim]To manage server settings, use the Miniflux web UI[/dim]")

        yield footer

    def on_mount(self) -> None:
        """Called when screen is mounted - update display."""
        self._update_display()

    def _update_display(self) -> None:
        """Update all settings displays."""
        self._update_tui_config()
        self._update_config_file_info()

    def _update_tui_config(self) -> None:
        """Update the TUI configuration display."""
        try:
            widget = self.query_one("#tui-config", Static)

            # Get config from app
            config = getattr(self.app, "config", None)
            if config:
                show_info = getattr(self.app, "show_info_messages", config.show_info_messages)

                lines = [
                    "[bold white]Colors & Display[/bold white]",
                    f"  Unread Color:        {config.unread_color}",
                    f"  Read Color:          {config.read_color}",
                    "",
                    "[bold white]Default Settings[/bold white]",
                    f"  Default Sort:        {config.default_sort}",
                    f"  Group by Feed:       {'Yes' if config.default_group_by_feed else 'No'}",
                    "",
                    "[bold white]Notifications[/bold white]",
                    f"  Show Info Messages:  {'Enabled' if show_info else 'Disabled'}",
                    "  [dim]Press 'i' to toggle info messages[/dim]",
                ]
                widget.update("\n".join(lines))
            else:
                widget.update("[dim]TUI configuration not available[/dim]")
        except Exception as e:
            self.app.log(f"Could not update TUI config: {e}")

    def _update_config_file_info(self) -> None:
        """Update the config file information display."""
        try:
            widget = self.query_one("#config-file", Static)

            # Get config from app
            config = getattr(self.app, "config", None)
            if config:
                config_path = get_config_file_path()

                lines = [
                    f"  Location:  {config_path!s}",
                    f"  Server:    {config.server_url}",
                    "",
                    "  [dim]Edit config.toml to change colors, defaults, and API settings[/dim]",
                ]
                widget.update("\n".join(lines))
            else:
                widget.update("[dim]Configuration file information not available[/dim]")
        except Exception as e:
            self.app.log(f"Could not update config file info: {e}")

    def action_toggle_info_messages(self):
        """Toggle the display of information messages."""
        toggle_func = getattr(self.app, "toggle_info_messages", None)
        if toggle_func and callable(toggle_func):
            toggle_func()
            # Update the display to show the new state
            self._update_tui_config()

    def action_close(self):
        """Close the settings screen."""
        self.app.pop_screen()
