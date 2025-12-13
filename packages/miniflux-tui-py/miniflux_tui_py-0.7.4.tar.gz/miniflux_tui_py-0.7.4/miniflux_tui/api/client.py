# SPDX-License-Identifier: MIT
"""Miniflux API client wrapper using official miniflux package."""

import asyncio
from collections.abc import Callable
from functools import partial
from typing import TypeVar

from miniflux import Client as MinifluxClientBase

from miniflux_tui.constants import BACKOFF_FACTOR, MAX_RETRIES

from .models import Category, Entry, Feed

T = TypeVar("T")


class MinifluxClient:
    """Wrapper around official Miniflux client for our app."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        allow_invalid_certs: bool = False,
        timeout: float = 30.0,
    ):
        """
        Initialize the Miniflux API client.

        Args:
            base_url: Base URL of the Miniflux server
            api_key: API key for authentication
            allow_invalid_certs: Whether to allow invalid SSL certificates (not supported by official client)
            timeout: Request timeout in seconds (not supported by official client)
        """
        self.base_url = base_url.rstrip("/")

        # Create official Miniflux client (synchronous)
        # The official client expects api_key as a keyword argument
        self.client = MinifluxClientBase(base_url, api_key=api_key)

        # Allow invalid certs
        self.allow_invalid_certs: bool = allow_invalid_certs

        # Timeout for network calls
        self.timeout: float = timeout

    async def close(self):
        """Close the HTTP client (no-op for official client)."""

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    @staticmethod
    async def _run_sync(func, *args, **kwargs):
        """Run a synchronous function in an executor."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    async def _call_with_retry(
        self,
        func: Callable[..., T],
        *args,
        max_retries: int = MAX_RETRIES,
        backoff_factor: float = BACKOFF_FACTOR,
        **kwargs,
    ) -> T:
        """Call function with exponential backoff retry logic.

        Automatically retries on network errors (ConnectionError, TimeoutError, OSError)
        with exponential backoff. Other exceptions are raised immediately.

        Backoff calculation:
        - Attempt 0: Immediate retry
        - Attempt 1: Wait backoff_factor^1 = 1 second
        - Attempt 2: Wait backoff_factor^2 = 1 second (with factor=1.0)

        Example with backoff_factor=2.0:
        - Attempt 1: Wait 2 seconds
        - Attempt 2: Wait 4 seconds
        - Attempt 3: Wait 8 seconds

        Args:
            func: Synchronous function to call
            *args: Positional arguments for func
            max_retries: Maximum number of retry attempts (default 3)
            backoff_factor: Multiplier for exponential backoff (default 1.0)
            **kwargs: Keyword arguments for func

        Returns:
            Result from func call

        Raises:
            ConnectionError/TimeoutError/OSError: Last network error if all retries fail
            Exception: Other exceptions are raised immediately without retry
        """
        last_exception = None

        for attempt in range(max_retries):
            try:
                # Try the function call
                return await self._run_sync(func, *args, **kwargs)
            except (ConnectionError, TimeoutError, OSError, BrokenPipeError) as e:
                # Transient network errors - retry with backoff
                # OSError covers socket-level errors including stale connections
                # BrokenPipeError occurs when connection is closed unexpectedly
                last_exception = e
                if attempt < max_retries - 1:
                    # Calculate exponential backoff delay
                    wait_time = backoff_factor**attempt
                    await asyncio.sleep(wait_time)
            except Exception:
                # Non-network errors - don't retry, raise immediately
                raise

        # All retries exhausted - raise last exception
        raise last_exception or Exception("Unknown error in retry logic")

    async def get_unread_entries(self, limit: int = 100, offset: int = 0) -> list[Entry]:
        """
        Get unread feed entries with retry logic and automatic pagination.

        Fetches all available entries if limit > 100 by making multiple API calls.

        Args:
            limit: Maximum number of entries to retrieve (if > 100, fetches all)
            offset: Offset for pagination

        Returns:
            List of unread Entry objects
        """
        # If limit is exactly 100 (default), fetch all entries
        if limit == 100:
            all_entries = []
            current_offset = offset
            batch_size = 100

            while True:
                response = await self._call_with_retry(
                    self.client.get_entries,
                    status=["unread"],
                    limit=batch_size,
                    offset=current_offset,
                    order="published_at",
                    direction="desc",
                )

                entries = [Entry.from_dict(entry) for entry in response.get("entries", [])]

                if not entries:
                    break

                all_entries.extend(entries)

                # If we got fewer entries than requested, we've reached the end
                if len(entries) < batch_size:
                    break

                current_offset += batch_size

            return all_entries

        # For explicit limits other than default, use single request
        response = await self._call_with_retry(
            self.client.get_entries, status=["unread"], limit=limit, offset=offset, order="published_at", direction="desc"
        )

        return [Entry.from_dict(entry) for entry in response.get("entries", [])]

    async def get_starred_entries(self, limit: int = 100, offset: int = 0) -> list[Entry]:
        """
        Get starred feed entries with retry logic and automatic pagination.

        Fetches all available entries if limit > 100 by making multiple API calls.

        Args:
            limit: Maximum number of entries to retrieve (if > 100, fetches all)
            offset: Offset for pagination

        Returns:
            List of starred Entry objects
        """
        # If limit is exactly 100 (default), fetch all entries
        if limit == 100:
            all_entries = []
            current_offset = offset
            batch_size = 100

            while True:
                response = await self._call_with_retry(
                    self.client.get_entries, starred=True, limit=batch_size, offset=current_offset, order="published_at", direction="desc"
                )

                entries = [Entry.from_dict(entry) for entry in response.get("entries", [])]

                if not entries:
                    break

                all_entries.extend(entries)

                # If we got fewer entries than requested, we've reached the end
                if len(entries) < batch_size:
                    break

                current_offset += batch_size

            return all_entries

        # For explicit limits other than default, use single request
        response = await self._call_with_retry(
            self.client.get_entries, starred=True, limit=limit, offset=offset, order="published_at", direction="desc"
        )

        return [Entry.from_dict(entry) for entry in response.get("entries", [])]

    async def get_read_entries(self, limit: int = 100, offset: int = 0) -> list[Entry]:
        """
        Get read feed entries (history) with retry logic.

        Args:
            limit: Maximum number of entries to retrieve
            offset: Offset for pagination

        Returns:
            List of read Entry objects ordered by most recently read first (changed_at)
        """
        response = await self._call_with_retry(
            self.client.get_entries, status=["read"], limit=limit, offset=offset, order="changed_at", direction="desc"
        )

        return [Entry.from_dict(entry) for entry in response.get("entries", [])]

    async def change_entry_status(self, entry_id: int, status: str) -> None:
        """
        Change the read status of an entry with retry logic.

        Args:
            entry_id: ID of the entry
            status: New status ("read" or "unread")
        """
        await self._call_with_retry(self.client.update_entries, entry_ids=[entry_id], status=status)

    async def mark_as_read(self, entry_id: int) -> None:
        """Mark an entry as read with retry logic."""
        await self.change_entry_status(entry_id, "read")

    async def mark_as_unread(self, entry_id: int) -> None:
        """Mark an entry as unread with retry logic."""
        await self.change_entry_status(entry_id, "unread")

    async def toggle_starred(self, entry_id: int) -> None:
        """
        Toggle the starred status of an entry with retry logic.

        Args:
            entry_id: ID of the entry
        """
        await self._call_with_retry(self.client.toggle_bookmark, entry_id)

    async def save_entry(self, entry_id: int) -> None:
        """
        Save an entry to third-party service (e.g., Wallabag, Shiori, Shaarli) with retry logic.

        Args:
            entry_id: ID of the entry
        """
        await self._call_with_retry(self.client.save_entry, entry_id)

    async def mark_all_as_read(self, entry_ids: list[int]) -> None:
        """
        Mark multiple entries as read with retry logic.

        Args:
            entry_ids: List of entry IDs to mark as read
        """
        await self._call_with_retry(self.client.update_entries, entry_ids=entry_ids, status="read")

    async def refresh_all_feeds(self) -> None:
        """Trigger a refresh of all feeds with retry logic."""
        await self._call_with_retry(self.client.refresh_all_feeds)

    async def refresh_feed(self, feed_id: int) -> None:
        """Refresh a specific feed with retry logic.

        Args:
            feed_id: ID of the feed to refresh
        """
        await self._call_with_retry(self.client.refresh_feed, feed_id)

    async def get_categories(self) -> list[Category]:
        """Get all categories with retry logic.

        Returns:
            List of Category objects
        """
        response = await self._call_with_retry(self.client.get_categories)
        # The official client returns a list directly, not wrapped in a dict
        if isinstance(response, list):
            return [Category.from_dict(cat) for cat in response]
        # Fallback for dict response with 'categories' key
        categories_data = response.get("categories", []) if isinstance(response, dict) else []
        return [Category.from_dict(cat) for cat in categories_data]

    async def create_category(self, title: str) -> Category:
        """Create a new category with retry logic.

        Args:
            title: Title of the new category

        Returns:
            The created Category object
        """
        response = await self._call_with_retry(self.client.create_category, title)
        return Category.from_dict(response)

    async def update_category(self, category_id: int, title: str) -> Category:
        """Update a category with retry logic.

        Args:
            category_id: ID of the category to update
            title: New title for the category

        Returns:
            The updated Category object
        """
        response = await self._call_with_retry(self.client.update_category, category_id, title)
        return Category.from_dict(response)

    async def delete_category(self, category_id: int) -> None:
        """Delete a category with retry logic.

        Args:
            category_id: ID of the category to delete
        """
        await self._call_with_retry(self.client.delete_category, category_id)

    async def create_feed(
        self,
        feed_url: str,
        category_id: int | None = None,
    ) -> Feed:
        """Create a new feed with retry logic (Issue #58 - Feed Management).

        Args:
            feed_url: URL of the feed to add
            category_id: Optional category ID to assign feed to

        Returns:
            The created Feed object
        """
        # Build kwargs for create_feed
        kwargs: dict = {}
        if category_id is not None:
            kwargs["category_id"] = category_id

        response = await self._call_with_retry(
            self.client.create_feed,
            feed_url,
            **kwargs,
        )
        return Feed.from_dict(response)  # type: ignore[arg-type]

    async def update_feed(
        self,
        feed_id: int,
        **kwargs,
    ) -> Feed:
        """Update feed settings with retry logic (Issue #58 - Feed Management).

        Args:
            feed_id: ID of the feed to update
            **kwargs: Feed attributes to update (title, category_id, etc.)

        Returns:
            The updated Feed object
        """
        response = await self._call_with_retry(
            self.client.update_feed,
            feed_id,
            **kwargs,
        )
        return Feed.from_dict(response)  # type: ignore[arg-type]

    async def get_feed(self, feed_id: int) -> Feed:
        """Get feed details with retry logic (Issue #58 - Feed Management).

        Args:
            feed_id: ID of the feed to retrieve

        Returns:
            The Feed object
        """
        response = await self._call_with_retry(
            self.client.get_feed,
            feed_id,
        )
        return Feed.from_dict(response)  # type: ignore[arg-type]

    async def delete_feed(self, feed_id: int) -> None:
        """Delete a feed with retry logic (Issue #58 - Feed Management).

        Args:
            feed_id: ID of the feed to delete
        """
        await self._call_with_retry(self.client.delete_feed, feed_id)

    async def fetch_original_content(self, entry_id: int) -> str:
        """
        Fetch the original content of an entry with retry logic.

        Args:
            entry_id: ID of the entry

        Returns:
            Original content HTML
        """
        response = await self._call_with_retry(self.client.fetch_entry_content, entry_id)
        return response.get("content", "")

    async def get_version(self) -> dict:
        """Get Miniflux server version information.

        Returns:
            Dictionary with version information from the server
        """
        return await self._call_with_retry(self.client.get_version)

    async def get_user_info(self) -> dict:
        """Get current user information.

        Returns:
            Dictionary with current user details (username, timezone, language, etc.)
        """
        return await self._call_with_retry(self.client.me)

    async def get_integrations_status(self) -> bool:
        """Get integrations status from the server.

        Returns:
            bool: True if at least one third-party integration is enabled
        """
        return await self._call_with_retry(self.client.get_integrations_status)

    async def update_user_settings(self, user_id: int, **settings) -> dict:
        """Update user settings.

        Args:
            user_id: User ID to update
            **settings: Settings to update (language, timezone, theme, entries_per_page, etc.)

        Returns:
            Dictionary with updated user information
        """
        return await self._call_with_retry(self.client.update_user, user_id, **settings)

    async def get_feeds(self) -> list[Feed]:
        """Get all feeds with retry logic.

        Returns:
            List of Feed objects with error/status information
        """
        response = await self._call_with_retry(self.client.get_feeds)
        # The official client returns a list directly
        if isinstance(response, list):
            return [Feed.from_dict(feed) for feed in response]
        # Fallback for dict response with 'feeds' key
        feeds_data = response.get("feeds", []) if isinstance(response, dict) else []
        return [Feed.from_dict(feed) for feed in feeds_data]

    async def get_category_entries(self, category_id: int, **kwargs) -> list[Entry]:
        """Get all entries for a specific category with retry logic.

        This is useful for building a category_id → entry mapping when the
        feeds endpoint doesn't include category_id information.

        Args:
            category_id: ID of the category to fetch entries for
            **kwargs: Additional parameters (limit, offset, status, etc.)

        Returns:
            List of Entry objects in the category
        """
        response = await self._call_with_retry(self.client.get_category_entries, category_id, **kwargs)
        # Handle both dict and list responses
        if isinstance(response, list):
            return [Entry.from_dict(entry) for entry in response]
        entries_data = response.get("entries", []) if isinstance(response, dict) else []
        return [Entry.from_dict(entry) for entry in entries_data]
