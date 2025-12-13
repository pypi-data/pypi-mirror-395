# SPDX-License-Identifier: MIT
"""Headless smoke tests for the Textual application."""

from typing import cast
from unittest.mock import AsyncMock, patch

import pytest

from miniflux_tui.config import Config
from miniflux_tui.ui.app import MinifluxTuiApp
from miniflux_tui.ui.screens.entry_list import EntryListScreen

TEST_TOKEN = "token-for-tests"  # noqa: S105 - static fixture value


class _FakeClient:
    """Minimal Miniflux client stub for smoke testing."""

    def __init__(self, entries, categories):
        self._entries = entries
        self._categories = categories
        self.refresh_feed = AsyncMock()
        self.refresh_all_feeds = AsyncMock()

    async def get_categories(self):
        return self._categories

    async def get_unread_entries(self, limit):
        return self._entries[:limit]

    async def get_starred_entries(self, limit):
        return self._entries[:limit]

    async def toggle_starred(self, _entry_id):  # pragma: no cover - side-effect free
        return None

    async def change_entry_status(self, _entry_id, _status):  # pragma: no cover
        return None

    async def save_entry(self, _entry_id):  # pragma: no cover
        return None

    async def close(self):  # pragma: no cover - smoke clean-up
        return None


@pytest.mark.asyncio
async def test_app_initializes_in_headless_mode(sample_entries, sample_categories):
    """Ensure the TUI boots, loads data, and shuts down cleanly headlessly."""

    config = Config(server_url="https://example.com", password=["command"])
    config._api_key_cache = TEST_TOKEN

    fake_client = _FakeClient(sample_entries, sample_categories)

    with patch("miniflux_tui.ui.app.MinifluxClient", return_value=fake_client):
        app = MinifluxTuiApp(config)
        async with app.run_test(headless=True) as pilot:
            # Wait for loading screen to complete and entry_list to be installed
            await pilot.pause()
            await pilot.pause()
            assert app.is_screen_installed("entry_list")
            entry_screen = cast(EntryListScreen, app.get_screen("entry_list"))
            assert entry_screen.entries

            await pilot.exit(result=None)
