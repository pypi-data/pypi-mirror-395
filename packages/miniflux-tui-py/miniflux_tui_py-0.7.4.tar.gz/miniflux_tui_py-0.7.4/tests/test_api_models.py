# SPDX-License-Identifier: MIT
"""Tests for API data models."""

from datetime import UTC, datetime

from miniflux_tui.api.models import Entry, Feed


class TestFeed:
    """Test Feed model."""

    def test_feed_creation(self):
        """Test creating a Feed instance."""
        feed = Feed(
            id=1,
            title="Test Feed",
            site_url="http://localhost:8080",
            feed_url="http://localhost:8080/feed.xml",
        )
        assert feed.id == 1
        assert feed.title == "Test Feed"
        assert feed.site_url == "http://localhost:8080"
        assert feed.feed_url == "http://localhost:8080/feed.xml"

    def test_feed_from_dict(self):
        """Test creating a Feed from dictionary."""
        data = {
            "id": 2,
            "title": "Another Feed",
            "site_url": "http://localhost:8081",
            "feed_url": "http://localhost:8081/rss",
        }
        feed = Feed.from_dict(data)
        assert feed.id == 2
        assert feed.title == "Another Feed"

    def test_feed_with_error_fields(self):
        """Test creating a Feed with error/status fields."""
        feed = Feed(
            id=3,
            title="Feed with Errors",
            site_url="http://localhost:8082",
            feed_url="http://localhost:8082/feed.xml",
            parsing_error_message="Connection timeout",
            parsing_error_count=5,
            checked_at="2024-10-24T12:00:00Z",
            disabled=True,
        )
        assert feed.parsing_error_message == "Connection timeout"
        assert feed.parsing_error_count == 5
        assert feed.checked_at == "2024-10-24T12:00:00Z"
        assert feed.disabled is True

    def test_feed_has_errors_property_with_message(self):
        """Test has_errors property returns True when error message exists."""
        feed = Feed(
            id=4,
            title="Feed with Error Message",
            site_url="http://localhost:8083",
            feed_url="http://localhost:8083/feed.xml",
            parsing_error_message="SSL certificate error",
            parsing_error_count=0,
        )
        assert feed.has_errors is True

    def test_feed_has_errors_property_with_count(self):
        """Test has_errors property returns True when error count > 0."""
        feed = Feed(
            id=5,
            title="Feed with Error Count",
            site_url="http://localhost:8084",
            feed_url="http://localhost:8084/feed.xml",
            parsing_error_message="",
            parsing_error_count=3,
        )
        assert feed.has_errors is True

    def test_feed_has_errors_property_no_errors(self):
        """Test has_errors property returns False when no errors."""
        feed = Feed(
            id=6,
            title="Healthy Feed",
            site_url="http://localhost:8085",
            feed_url="http://localhost:8085/feed.xml",
            parsing_error_message="",
            parsing_error_count=0,
        )
        assert feed.has_errors is False

    def test_feed_from_dict_with_error_fields(self):
        """Test creating a Feed from dict with error/status fields."""
        data = {
            "id": 7,
            "title": "Feed from Dict with Errors",
            "site_url": "http://localhost:8086",
            "feed_url": "http://localhost:8086/rss",
            "parsing_error_message": "Parse error",
            "parsing_error_count": 2,
            "checked_at": "2024-10-24T14:30:00Z",
            "disabled": False,
        }
        feed = Feed.from_dict(data)
        assert feed.id == 7
        assert feed.parsing_error_message == "Parse error"
        assert feed.parsing_error_count == 2
        assert feed.checked_at == "2024-10-24T14:30:00Z"
        assert feed.disabled is False
        assert feed.has_errors is True

    def test_feed_from_dict_with_missing_optional_fields(self):
        """Test creating a Feed from dict with missing optional error fields."""
        data = {
            "id": 8,
            "title": "Minimal Feed",
            "site_url": "http://localhost:8087",
            "feed_url": "http://localhost:8087/feed.xml",
        }
        feed = Feed.from_dict(data)
        assert feed.id == 8
        assert not feed.parsing_error_message
        assert feed.parsing_error_count == 0
        assert feed.checked_at is None
        assert feed.disabled is False
        assert feed.has_errors is False


class TestEntry:
    """Test Entry model."""

    def test_entry_creation(self, sample_feed):
        """Test creating an Entry instance."""
        entry = Entry(
            id=1,
            feed_id=1,
            title="Test Entry",
            url="http://localhost:8080/article",
            content="<p>Content</p>",
            feed=sample_feed,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 24, 12, 0, 0, tzinfo=UTC),
        )
        assert entry.id == 1
        assert entry.title == "Test Entry"
        assert entry.status == "unread"
        assert entry.starred is False

    def test_entry_is_unread(self, sample_entry):
        """Test is_unread property."""
        sample_entry.status = "unread"
        assert sample_entry.is_unread is True

        sample_entry.status = "read"
        assert sample_entry.is_unread is False

    def test_entry_is_read(self, sample_entry):
        """Test is_read property."""
        sample_entry.status = "read"
        assert sample_entry.is_read is True

        sample_entry.status = "unread"
        assert sample_entry.is_read is False

    def test_entry_from_dict(self):
        """Test creating an Entry from dictionary."""
        data = {
            "id": 5,
            "feed_id": 1,
            "title": "From Dict Entry",
            "url": "http://localhost:8080/test",
            "content": "<p>Test</p>",
            "feed": {
                "id": 1,
                "title": "Test Feed",
                "site_url": "http://localhost:8080",
                "feed_url": "http://localhost:8080/feed.xml",
            },
            "status": "read",
            "starred": True,
            "published_at": "2024-10-24T12:30:00Z",
            "original_content": None,
        }
        entry = Entry.from_dict(data)
        assert entry.id == 5
        assert entry.title == "From Dict Entry"
        assert entry.status == "read"
        assert entry.starred is True
        assert entry.is_read is True
        assert entry.is_unread is False

    def test_entry_starred_property(self, sample_entry):
        """Test starred status of entry."""
        sample_entry.starred = True
        assert sample_entry.starred is True

        sample_entry.starred = False
        assert sample_entry.starred is False

    def test_entry_with_optional_content(self, sample_feed):
        """Test Entry with optional original_content."""
        entry = Entry(
            id=10,
            feed_id=1,
            title="Entry with Original",
            url="http://localhost:8080/original",
            content="<p>Excerpt</p>",
            feed=sample_feed,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 24, 12, 0, 0, tzinfo=UTC),
            original_content="<p>Full original content</p>",
        )
        assert entry.original_content == "<p>Full original content</p>"
