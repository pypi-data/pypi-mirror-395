# SPDX-License-Identifier: MIT
"""Pytest configuration and fixtures."""

import sys
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock

import pytest

from miniflux_tui.api.models import Category, Entry, Feed


@pytest.fixture
def sample_feed():
    """Create a sample feed for testing."""
    return Feed(
        id=1,
        title="Example Feed",
        site_url="http://localhost:8080",
        feed_url="http://localhost:8080/feed.xml",
    )


@pytest.fixture
def sample_entry(sample_feed):
    """Create a sample entry for testing."""
    return Entry(
        id=1,
        feed_id=1,
        title="Sample Entry Title",
        url="http://localhost:8080/article",
        content="<p>This is HTML content</p>",
        feed=sample_feed,
        status="unread",
        starred=False,
        published_at=datetime(2024, 10, 24, 12, 30, 0, tzinfo=UTC),
    )


@pytest.fixture
def sample_entries(sample_feed):
    """Create multiple sample entries for testing."""
    return [
        Entry(
            id=1,
            feed_id=1,
            title="Unread Entry 1",
            url="http://localhost:8080/article1",
            content="<p>Content 1</p>",
            feed=sample_feed,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 24, 12, 30, 0, tzinfo=UTC),
        ),
        Entry(
            id=2,
            feed_id=1,
            title="Read Entry 2",
            url="http://localhost:8080/article2",
            content="<p>Content 2</p>",
            feed=sample_feed,
            status="read",
            starred=False,
            published_at=datetime(2024, 10, 23, 10, 15, 0, tzinfo=UTC),
        ),
        Entry(
            id=3,
            feed_id=1,
            title="Starred Unread Entry 3",
            url="http://localhost:8080/article3",
            content="<p>Content 3</p>",
            feed=sample_feed,
            status="unread",
            starred=True,
            published_at=datetime(2024, 10, 22, 15, 45, 0, tzinfo=UTC),
        ),
        Entry(
            id=4,
            feed_id=1,
            title="Starred Read Entry 4",
            url="http://localhost:8080/article4",
            content="<p>Content 4</p>",
            feed=sample_feed,
            status="read",
            starred=True,
            published_at=datetime(2024, 10, 21, 9, 0, 0, tzinfo=UTC),
        ),
    ]


@pytest.fixture
def sample_categories():
    """Create sample categories."""
    return [
        Category(id=1, title="Tech"),
        Category(id=2, title="News"),
    ]


@pytest.fixture
def valid_config_dict():
    """Create a valid configuration dictionary."""
    return {
        "server_url": "http://localhost:8080",
        "password": [sys.executable, "-c", "print('1234567890abcdef')"],
        "allow_invalid_certs": False,
        "theme": {
            "unread_color": "cyan",
            "read_color": "gray",
        },
        "sorting": {
            "default_sort": "date",
            "default_group_by_feed": False,
            "group_collapsed": False,
        },
    }


@pytest.fixture
def config_factory():
    """Factory for creating Config-like dictionaries."""

    def _factory(**overrides: Any) -> dict[str, Any]:
        base = {
            "server_url": "http://localhost:8080",
            "password": [sys.executable, "-c", "print('1234567890abcdef')"],
            "allow_invalid_certs": False,
            "theme": {
                "unread_color": "cyan",
                "read_color": "gray",
            },
            "sorting": {
                "default_sort": "date",
                "default_group_by_feed": False,
                "group_collapsed": False,
            },
        }
        base.update(overrides)
        return base

    return _factory


@pytest.fixture
def async_client_factory(sample_entries, sample_categories):
    """Factory that produces AsyncMock Miniflux clients."""

    def _factory(
        entries: list[Entry] | None = None,
        categories: list[Category] | None = None,
        starred: list[Entry] | None = None,
    ) -> AsyncMock:
        client = AsyncMock()
        client.get_categories = AsyncMock(return_value=sample_categories if categories is None else categories)
        client.get_unread_entries = AsyncMock(return_value=sample_entries if entries is None else entries)
        client.get_starred_entries = AsyncMock(return_value=(sample_entries[:1] if starred is None else starred))
        client.refresh_feed = AsyncMock()
        client.refresh_all_feeds = AsyncMock()
        client.toggle_starred = AsyncMock()
        client.change_entry_status = AsyncMock()
        client.save_entry = AsyncMock()
        return client

    return _factory
