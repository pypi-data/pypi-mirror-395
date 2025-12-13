# SPDX-License-Identifier: MIT
"""Protocol definition for MinifluxTUI app interface.

This module provides a Protocol that defines the interface screens expect from
the main application, breaking cyclic dependencies between app.py and screen modules.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from miniflux_tui.api.client import MinifluxClient
    from miniflux_tui.api.models import Entry


@runtime_checkable
class MinifluxAppProtocol(Protocol):
    """Protocol defining the interface that screens expect from the app.

    This protocol breaks the cyclic import between app.py and screen modules
    by defining the expected interface without importing the actual MinifluxTuiApp class.
    """

    # API client
    client: MinifluxClient | None

    # Application state
    current_view: str
    entry_category_map: dict[int, int]

    # Logging and notifications
    def log(self, message: str, /) -> None:
        """Log a message."""
        raise NotImplementedError

    def notify(
        self,
        message: str,
        /,
        *,
        title: str = "",
        severity: str = "information",
        timeout: float = ...,
    ) -> None:
        """Send a notification to the user."""
        raise NotImplementedError

    # Screen navigation
    def pop_screen(self) -> None:
        """Pop the current screen from the stack."""
        raise NotImplementedError

    def push_screen(self, screen: str | object, /) -> None:
        """Push a screen onto the stack."""
        raise NotImplementedError

    def exit(self, return_code: int = 0, /) -> None:
        """Exit the application."""
        raise NotImplementedError

    # Custom app methods
    def push_entry_reader(
        self,
        entry: Entry,
        entry_list: list | None = None,
        current_index: int = 0,
        group_info: dict[str, str | int] | None = None,
    ) -> None:
        """Push entry reader screen for a specific entry."""
        raise NotImplementedError

    async def push_category_management_screen(self) -> None:
        """Push category management screen."""
        raise NotImplementedError

    async def load_entries(self, view: str = "unread") -> None:
        """Load entries from Miniflux API."""
        raise NotImplementedError

    async def _build_entry_category_mapping(self) -> dict[int, int]:
        """Build a mapping of entry_id → category_id."""
        raise NotImplementedError
