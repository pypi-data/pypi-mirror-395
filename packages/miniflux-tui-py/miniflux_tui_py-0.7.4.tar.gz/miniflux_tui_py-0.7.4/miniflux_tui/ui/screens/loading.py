# SPDX-License-Identifier: MIT
"""Loading screen with ASCII art."""

from textual.app import ComposeResult
from textual.containers import Center, Middle
from textual.screen import Screen
from textual.widgets import Static

from miniflux_tui.utils import get_app_version

# editorconfig-checker-disable
ASCII_ART_TEMPLATE = r"""
                  _           _    __   _                          _             _
      _ __ ___   (_)  _ __   (_)  / _| | |  _   _  __  __         | |_   _   _  (_)
     | '_ ` _ \  | | | '_ \  | | | |_  | | | | | | \ \/ /  _____  | __| | | | | | |
     | | | | | | | | | | | | | | |  _| | | | |_| |  >  <  |_____| | |_  | |_| | | |
     |_| |_| |_| |_| |_| |_| |_| |_|   |_|  \__,_| /_/\_\          \__|  \__,_| |_|

     version {version}

     ~ Loading your feeds ~
"""
# editorconfig-checker-enable


class LoadingScreen(Screen):
    """A loading screen with ASCII art."""

    CSS = """
    LoadingScreen {
        align: center middle;
        background: $surface;
    }

    LoadingScreen Static {
        width: auto;
        height: auto;
        color: $accent;
        text-style: bold;
    }
    """

    def compose(self) -> ComposeResult:
        """Create the loading screen layout."""
        version = get_app_version()
        ascii_art = ASCII_ART_TEMPLATE.format(version=version)
        with Center(), Middle():
            yield Static(ascii_art)
