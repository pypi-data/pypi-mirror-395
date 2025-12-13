# SPDX-License-Identifier: MIT
"""Tests for the entry history screen."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from miniflux_tui.api.models import Entry, Feed
from miniflux_tui.ui.screens.entry_history import EntryHistoryScreen
from miniflux_tui.ui.screens.entry_list import EntryListScreen


@pytest.fixture
def mock_app():
    """Create a mock app with a client."""
    app = MagicMock()
    app.client = MagicMock()
    app.log = MagicMock()
    app.notify = MagicMock()
    return app


@pytest.fixture
def sample_feed():
    """Create a sample feed."""
    return Feed(
        id=1,
        title="Test Feed",
        site_url="https://example.com",
        feed_url="https://example.com/feed",
    )


@pytest.fixture
def sample_entries(sample_feed):
    """Create sample read entries."""
    return [
        Entry(
            id=1,
            feed_id=1,
            title="Read Entry 1",
            url="https://example.com/1",
            content="Content 1",
            feed=sample_feed,
            status="read",
            starred=False,
            published_at=datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC),
        ),
        Entry(
            id=2,
            feed_id=2,
            title="Read Entry 2",
            url="https://example.com/2",
            content="Content 2",
            feed=sample_feed,
            status="read",
            starred=False,
            published_at=datetime(2024, 1, 2, 12, 0, 0, tzinfo=UTC),
        ),
    ]


def test_entry_history_screen_initialization():
    """Test that EntryHistoryScreen initializes with empty entries."""
    screen = EntryHistoryScreen()
    assert screen.entries == []


@pytest.mark.asyncio
async def test_load_history_success(mock_app, sample_entries):
    """Test successful loading of history entries."""
    mock_app.client.get_read_entries = AsyncMock(return_value=sample_entries)

    screen = EntryHistoryScreen()
    screen._populate_list = MagicMock()

    # Patch the app property
    with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
        await screen._load_history()

    # Verify API was called correctly
    mock_app.client.get_read_entries.assert_called_once_with(limit=200, offset=0)

    # Verify entries were set
    assert screen.entries == sample_entries
    assert len(screen.entries) == 2

    # Verify UI updates
    screen._populate_list.assert_called_once()
    assert mock_app.notify.call_count == 2  # Loading + success message
    mock_app.notify.assert_any_call("Loading history...")
    mock_app.notify.assert_any_call("Loaded 2 entries", severity="information")


@pytest.mark.asyncio
async def test_load_history_empty(mock_app):
    """Test loading history when no read entries exist."""
    mock_app.client.get_read_entries = AsyncMock(return_value=[])

    screen = EntryHistoryScreen()
    screen._populate_list = MagicMock()

    # Patch the app property
    with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
        await screen._load_history()

    # Verify empty state
    assert screen.entries == []
    screen._populate_list.assert_called_once()

    # Verify informative message
    mock_app.notify.assert_any_call("No read entries found. Read some articles first!", severity="information")


@pytest.mark.asyncio
async def test_load_history_no_client(mock_app):
    """Test loading history when API client is not available."""
    screen = EntryHistoryScreen()
    mock_no_client_app = MagicMock()
    mock_no_client_app.client = None
    mock_no_client_app.notify = MagicMock()

    # Patch the app property
    with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_no_client_app)):
        await screen._load_history()

    # Verify error notification
    mock_no_client_app.notify.assert_called_once_with("API client not available", severity="error")


@pytest.mark.asyncio
async def test_load_history_api_error(mock_app):
    """Test handling of API errors during history load."""
    mock_app.client.get_read_entries = AsyncMock(side_effect=Exception("Network error"))

    screen = EntryHistoryScreen()
    screen._populate_list = MagicMock()

    # Patch the app property
    with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
        await screen._load_history()

    # Verify error handling
    assert screen.entries == []
    screen._populate_list.assert_called_once()
    mock_app.log.assert_called()
    # Check that error notification includes the actual error message
    notify_calls = [call for call in mock_app.notify.call_args_list if call[1].get("severity") == "error"]
    assert len(notify_calls) > 0
    assert "Failed to load history:" in notify_calls[0][0][0]
    assert "Network error" in notify_calls[0][0][0]


@pytest.mark.asyncio
async def test_load_history_logs_correctly(mock_app, sample_entries):
    """Test that history loading logs appropriate messages."""
    mock_app.client.get_read_entries = AsyncMock(return_value=sample_entries)

    screen = EntryHistoryScreen()
    screen._populate_list = MagicMock()

    # Patch the app property
    with patch.object(type(screen), "app", new_callable=lambda: property(lambda _: mock_app)):
        await screen._load_history()

    # Verify logging
    mock_app.log.assert_called_with("Loaded 2 history entries")


def test_entry_history_inherits_from_entry_list():
    """Test that EntryHistoryScreen properly inherits from EntryListScreen."""
    screen = EntryHistoryScreen()
    assert isinstance(screen, EntryListScreen)


@pytest.mark.asyncio
async def test_on_mount_triggers_history_load(mock_app, sample_entries):
    """Test that on_mount properly triggers history loading."""
    mock_app.client.get_read_entries = AsyncMock(return_value=sample_entries)

    with (
        patch.object(EntryHistoryScreen, "run_worker") as mock_run_worker,
        patch.object(type(EntryHistoryScreen()), "app", new_callable=lambda: property(lambda _: mock_app)),
        patch("miniflux_tui.ui.screens.entry_list.EntryListScreen.on_mount"),
    ):
        screen = EntryHistoryScreen()
        screen.on_mount()

        # Verify run_worker was called
        mock_run_worker.assert_called_once()
        # Verify it was called with exclusive=True
        call_args = mock_run_worker.call_args
        assert call_args.kwargs.get("exclusive") is True
