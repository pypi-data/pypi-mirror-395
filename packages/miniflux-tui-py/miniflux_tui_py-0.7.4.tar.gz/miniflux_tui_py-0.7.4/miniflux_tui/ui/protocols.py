# SPDX-License-Identifier: MIT
"""Type protocols shared across UI components."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


class EntryApiClientProtocol(Protocol):
    """Subset of Miniflux API client operations used by UI screens."""

    async def mark_as_read(self, entry_id: int) -> None:
        """Mark the entry as read in Miniflux."""
        raise NotImplementedError

    async def mark_as_unread(self, entry_id: int) -> None:
        """Re-open the entry in Miniflux."""
        raise NotImplementedError

    async def toggle_starred(self, entry_id: int) -> None:
        """Toggle the starred state of the entry."""
        raise NotImplementedError

    async def save_entry(self, entry_id: int) -> None:
        """Save the entry as a bookmark."""
        raise NotImplementedError

    async def fetch_original_content(self, entry_id: int) -> str:
        """Fetch the original HTML content for the entry."""
        raise NotImplementedError


@runtime_checkable
class EntryReaderAppProtocol(Protocol):
    """Capabilities required from the TUI application by entry reader screens."""

    client: EntryApiClientProtocol | None

    def pop_screen(self) -> None:
        """Close the active screen."""
        raise NotImplementedError

    def push_screen(self, screen: str) -> None:
        """Open a new screen by name."""
        raise NotImplementedError

    def exit(self) -> None:
        """Exit the application."""
        raise NotImplementedError
