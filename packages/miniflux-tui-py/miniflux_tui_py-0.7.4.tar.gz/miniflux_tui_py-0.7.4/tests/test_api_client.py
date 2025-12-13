# SPDX-License-Identifier: MIT
"""Tests for Miniflux API client wrapper."""

from unittest.mock import MagicMock, patch

import pytest

from miniflux_tui.api.client import MinifluxClient


class TestMinifluxClientInit:
    """Test MinifluxClient initialization."""

    def test_init_basic(self):
        """Test basic client initialization."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base:
            client = MinifluxClient("http://localhost:8080", "test-key")
            assert client.base_url == "http://localhost:8080"
            assert client.allow_invalid_certs is False
            assert client.timeout == 30.0
            mock_base.assert_called_once_with("http://localhost:8080", api_key="test-key")

    def test_init_with_trailing_slash(self):
        """Test that trailing slash is removed from base_url."""
        with patch("miniflux_tui.api.client.MinifluxClientBase"):
            client = MinifluxClient("http://localhost:8080/", "test-key")
            assert client.base_url == "http://localhost:8080"

    def test_init_with_invalid_certs(self):
        """Test initialization with allow_invalid_certs."""
        with patch("miniflux_tui.api.client.MinifluxClientBase"):
            client = MinifluxClient("http://localhost:8080", "test-key", allow_invalid_certs=True)
            assert client.allow_invalid_certs is True

    def test_init_with_custom_timeout(self):
        """Test initialization with custom timeout."""
        with patch("miniflux_tui.api.client.MinifluxClientBase"):
            client = MinifluxClient("http://localhost:8080", "test-key", timeout=60.0)
            assert client.timeout == 60.0


class TestMinifluxClientContextManager:
    """Test MinifluxClient context manager functionality."""

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test async context manager entry and exit."""
        with patch("miniflux_tui.api.client.MinifluxClientBase"):
            async with MinifluxClient("http://localhost:8080", "test-key") as client:
                assert isinstance(client, MinifluxClient)

    @pytest.mark.asyncio
    async def test_close_method(self):
        """Test close method."""
        with patch("miniflux_tui.api.client.MinifluxClientBase"):
            client = MinifluxClient("http://localhost:8080", "test-key")
            # Should not raise any exception
            await client.close()


class TestMinifluxClientRunSync:
    """Test _run_sync method."""

    @pytest.mark.asyncio
    async def test_run_sync_with_args(self):
        """Test _run_sync with positional arguments."""
        with patch("miniflux_tui.api.client.MinifluxClientBase"):
            client = MinifluxClient("http://localhost:8080", "test-key")

            def sample_func(a, b):
                return a + b

            result = await client._run_sync(sample_func, 1, 2)
            assert result == 3

    @pytest.mark.asyncio
    async def test_run_sync_with_kwargs(self):
        """Test _run_sync with keyword arguments."""
        with patch("miniflux_tui.api.client.MinifluxClientBase"):
            client = MinifluxClient("http://localhost:8080", "test-key")

            def sample_func(a=0, b=0):
                return a * b

            result = await client._run_sync(sample_func, a=3, b=4)
            assert result == 12


class TestMinifluxClientRetryLogic:
    """Test _call_with_retry method."""

    @pytest.mark.asyncio
    async def test_successful_call_on_first_try(self):
        """Test successful call without needing retries."""
        with patch("miniflux_tui.api.client.MinifluxClientBase"):
            client = MinifluxClient("http://localhost:8080", "test-key")

            def success_func():
                return "success"

            result = await client._call_with_retry(success_func)
            assert result == "success"

    @pytest.mark.asyncio
    async def test_retry_on_connection_error(self):
        """Test retry logic on connection error."""
        with patch("miniflux_tui.api.client.MinifluxClientBase"):
            client = MinifluxClient("http://localhost:8080", "test-key")

            call_count = 0

            def failing_func():
                nonlocal call_count
                call_count += 1
                if call_count < 2:
                    error_msg = "Network error"
                    raise ConnectionError(error_msg)
                return "recovered"

            result = await client._call_with_retry(failing_func, max_retries=3, backoff_factor=0.01)
            assert result == "recovered"
            assert call_count == 2

    @pytest.mark.asyncio
    async def test_retry_exhaustion(self):
        """Test that exception is raised after max retries."""
        with patch("miniflux_tui.api.client.MinifluxClientBase"):
            client = MinifluxClient("http://localhost:8080", "test-key")

            def always_failing():
                error_msg = "Network error"
                raise ConnectionError(error_msg)

            with pytest.raises(ConnectionError, match="Network error"):
                await client._call_with_retry(always_failing, max_retries=2, backoff_factor=0.01)

    @pytest.mark.asyncio
    async def test_non_network_error_no_retry(self):
        """Test that non-network errors are not retried."""
        with patch("miniflux_tui.api.client.MinifluxClientBase"):
            client = MinifluxClient("http://localhost:8080", "test-key")

            call_count = 0

            def value_error_func():
                nonlocal call_count
                call_count += 1
                error_msg = "Invalid value"
                raise ValueError(error_msg)

            with pytest.raises(ValueError, match="Invalid value"):
                await client._call_with_retry(value_error_func, max_retries=3)

            # Should only be called once (no retries for non-network errors)
            assert call_count == 1


class TestMinifluxClientGetEntries:
    """Test entry retrieval methods."""

    @pytest.mark.asyncio
    async def test_get_unread_entries(self):
        """Test getting unread entries."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock the response
            mock_client.get_entries.return_value = {"entries": []}

            client = MinifluxClient("http://localhost:8080", "test-key")
            result = await client.get_unread_entries(limit=50, offset=0)

            assert result == []
            mock_client.get_entries.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_starred_entries(self):
        """Test getting starred entries."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client
            mock_client.get_entries.return_value = {"entries": []}

            client = MinifluxClient("http://localhost:8080", "test-key")
            result = await client.get_starred_entries(limit=30, offset=0)

            assert result == []
            mock_client.get_entries.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_entries_parsing(self):
        """Test entry parsing from API response."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock a real API response structure
            mock_client.get_entries.return_value = {
                "entries": [
                    {
                        "id": 1,
                        "feed_id": 1,
                        "title": "Test Entry",
                        "content": "Test content",
                        "url": "http://localhost:8080/entry",
                        "author": "Test Author",
                        "published_at": "2023-01-01T00:00:00Z",
                        "starred": False,
                        "status": "unread",
                        "feed": {
                            "id": 1,
                            "title": "Test Feed",
                            "site_url": "http://localhost:8080",
                            "feed_url": "http://localhost:8080/feed",
                        },
                    }
                ]
            }

            client = MinifluxClient("http://localhost:8080", "test-key")
            # Just verify the entry parsing logic works
            result = await client.get_unread_entries()

            # Entry.from_dict should be called and return Entry objects
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0].title == "Test Entry"

    @pytest.mark.asyncio
    async def test_get_unread_entries_pagination(self):
        """Test automatic pagination for unread entries with default limit."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock responses: first call returns 100 entries, second returns 50
            def mock_get_entries(*args, **kwargs):
                offset = kwargs.get("offset", 0)
                if offset == 0:
                    # First page: 100 entries
                    return {
                        "entries": [
                            {
                                "id": i,
                                "feed_id": 1,
                                "title": f"Entry {i}",
                                "content": "Test",
                                "url": f"http://localhost:8080/entry/{i}",
                                "author": "Test",
                                "published_at": "2023-01-01T00:00:00Z",
                                "starred": False,
                                "status": "unread",
                                "feed": {
                                    "id": 1,
                                    "title": "Test Feed",
                                    "site_url": "http://localhost:8080",
                                    "feed_url": "http://localhost:8080/feed",
                                },
                            }
                            for i in range(100)
                        ]
                    }
                if offset == 100:
                    # Second page: 50 entries
                    return {
                        "entries": [
                            {
                                "id": i,
                                "feed_id": 1,
                                "title": f"Entry {i}",
                                "content": "Test",
                                "url": f"http://localhost:8080/entry/{i}",
                                "author": "Test",
                                "published_at": "2023-01-01T00:00:00Z",
                                "starred": False,
                                "status": "unread",
                                "feed": {
                                    "id": 1,
                                    "title": "Test Feed",
                                    "site_url": "http://localhost:8080",
                                    "feed_url": "http://localhost:8080/feed",
                                },
                            }
                            for i in range(100, 150)
                        ]
                    }
                return {"entries": []}

            mock_client.get_entries.side_effect = mock_get_entries

            client = MinifluxClient("http://localhost:8080", "test-key")
            result = await client.get_unread_entries()  # Uses default limit=100

            # Should fetch all entries across multiple pages
            assert len(result) == 150
            assert result[0].id == 0
            assert result[149].id == 149
            # Should have made 2 API calls (100 + 50 entries)
            assert mock_client.get_entries.call_count == 2

    @pytest.mark.asyncio
    async def test_get_starred_entries_pagination(self):
        """Test automatic pagination for starred entries with default limit."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock responses: first call returns 100 entries, second returns 0
            def mock_get_entries(*args, **kwargs):
                offset = kwargs.get("offset", 0)
                if offset == 0:
                    return {
                        "entries": [
                            {
                                "id": i,
                                "feed_id": 1,
                                "title": f"Entry {i}",
                                "content": "Test",
                                "url": f"http://localhost:8080/entry/{i}",
                                "author": "Test",
                                "published_at": "2023-01-01T00:00:00Z",
                                "starred": True,
                                "status": "read",
                                "feed": {
                                    "id": 1,
                                    "title": "Test Feed",
                                    "site_url": "http://localhost:8080",
                                    "feed_url": "http://localhost:8080/feed",
                                },
                            }
                            for i in range(100)
                        ]
                    }
                return {"entries": []}

            mock_client.get_entries.side_effect = mock_get_entries

            client = MinifluxClient("http://localhost:8080", "test-key")
            result = await client.get_starred_entries()  # Uses default limit=100

            # Should fetch all 100 entries in first page
            assert len(result) == 100
            # Should have made 2 API calls (100 entries + empty response)
            assert mock_client.get_entries.call_count == 2


class TestMinifluxClientActions:
    """Test entry action methods."""

    @pytest.mark.asyncio
    async def test_mark_as_read_calls_change_status(self):
        """Test marking entry as read delegates to change_entry_status."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client
            mock_client.update_entries.return_value = None

            client = MinifluxClient("http://localhost:8080", "test-key")
            # This should not raise
            await client.mark_as_read(123)

    @pytest.mark.asyncio
    async def test_mark_as_unread_calls_change_status(self):
        """Test marking entry as unread delegates to change_entry_status."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client
            mock_client.update_entries.return_value = None

            client = MinifluxClient("http://localhost:8080", "test-key")
            # This should not raise
            await client.mark_as_unread(123)

    @pytest.mark.asyncio
    async def test_toggle_starred(self):
        """Test toggling starred status."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client
            mock_client.toggle_bookmark.return_value = None

            client = MinifluxClient("http://localhost:8080", "test-key")
            # Should not raise
            await client.toggle_starred(123)

    @pytest.mark.asyncio
    async def test_save_entry(self):
        """Test saving entry."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client
            mock_client.save_entry.return_value = None

            client = MinifluxClient("http://localhost:8080", "test-key")
            # Should not raise
            await client.save_entry(123)

    @pytest.mark.asyncio
    async def test_mark_all_as_read(self):
        """Test marking multiple entries as read."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client
            mock_client.update_entries.return_value = None

            client = MinifluxClient("http://localhost:8080", "test-key")
            # Should not raise
            await client.mark_all_as_read([1, 2, 3])

    @pytest.mark.asyncio
    async def test_refresh_all_feeds(self):
        """Test refreshing all feeds."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client
            mock_client.refresh_all_feeds.return_value = None

            client = MinifluxClient("http://localhost:8080", "test-key")
            # Should not raise
            await client.refresh_all_feeds()

    @pytest.mark.asyncio
    async def test_fetch_original_content(self):
        """Test fetching original content."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock the response
            mock_client.fetch_entry_content.return_value = {"content": "<html>Original content</html>"}

            client = MinifluxClient("http://localhost:8080", "test-key")
            result = await client.fetch_original_content(123)

            # Result should be a string (possibly empty or content)
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_get_feeds_list_response(self):
        """Test getting feeds when API returns a list."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock the response as a list
            mock_client.get_feeds.return_value = [
                {
                    "id": 1,
                    "title": "Test Feed 1",
                    "site_url": "http://localhost:8080",
                    "feed_url": "http://localhost:8080/feed.xml",
                    "parsing_error_message": "",
                    "parsing_error_count": 0,
                    "disabled": False,
                },
                {
                    "id": 2,
                    "title": "Test Feed 2",
                    "site_url": "http://localhost:8081",
                    "feed_url": "http://localhost:8081/feed.xml",
                    "parsing_error_message": "SSL error",
                    "parsing_error_count": 3,
                    "disabled": True,
                },
            ]

            client = MinifluxClient("http://localhost:8080", "test-key")
            feeds = await client.get_feeds()

            # Verify we got Feed objects
            assert len(feeds) == 2
            assert feeds[0].id == 1
            assert feeds[0].title == "Test Feed 1"
            assert feeds[0].has_errors is False
            assert feeds[1].id == 2
            assert feeds[1].parsing_error_message == "SSL error"
            assert feeds[1].parsing_error_count == 3
            assert feeds[1].disabled is True
            assert feeds[1].has_errors is True

    @pytest.mark.asyncio
    async def test_get_feeds_dict_response(self):
        """Test getting feeds when API returns a dict with 'feeds' key."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock the response as a dict with 'feeds' key
            mock_client.get_feeds.return_value = {
                "feeds": [
                    {
                        "id": 10,
                        "title": "Feed from Dict",
                        "site_url": "http://localhost:8082",
                        "feed_url": "http://localhost:8082/feed.xml",
                        "parsing_error_message": "Timeout",
                        "parsing_error_count": 1,
                        "checked_at": "2024-10-24T12:00:00Z",
                        "disabled": False,
                    },
                ]
            }

            client = MinifluxClient("http://localhost:8080", "test-key")
            feeds = await client.get_feeds()

            # Verify we got Feed objects
            assert len(feeds) == 1
            assert feeds[0].id == 10
            assert feeds[0].title == "Feed from Dict"
            assert feeds[0].parsing_error_message == "Timeout"
            assert feeds[0].has_errors is True

    @pytest.mark.asyncio
    async def test_get_feeds_empty_list(self):
        """Test getting feeds when no feeds exist."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock the response as empty list
            mock_client.get_feeds.return_value = []

            client = MinifluxClient("http://localhost:8080", "test-key")
            feeds = await client.get_feeds()

            # Verify we got empty list
            assert len(feeds) == 0
            assert isinstance(feeds, list)


class TestMinifluxClientGetReadEntries:
    """Test get_read_entries method for history functionality."""

    @pytest.mark.asyncio
    async def test_get_read_entries_success(self):
        """Test getting read entries successfully."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock the response with read entries
            mock_client.get_entries.return_value = {
                "entries": [
                    {
                        "id": 1,
                        "feed_id": 10,
                        "title": "Read Entry 1",
                        "url": "https://example.com/1",
                        "content": "Content 1",
                        "published_at": "2024-01-01T12:00:00Z",
                        "status": "read",
                        "starred": False,
                        "feed": {
                            "id": 10,
                            "title": "Test Feed 1",
                            "site_url": "https://example.com",
                            "feed_url": "https://example.com/feed",
                        },
                    },
                    {
                        "id": 2,
                        "feed_id": 20,
                        "title": "Read Entry 2",
                        "url": "https://example.com/2",
                        "content": "Content 2",
                        "published_at": "2024-01-02T12:00:00Z",
                        "status": "read",
                        "starred": False,
                        "feed": {
                            "id": 20,
                            "title": "Test Feed 2",
                            "site_url": "https://example.com",
                            "feed_url": "https://example.com/feed2",
                        },
                    },
                ]
            }

            client = MinifluxClient("http://localhost:8080", "test-key")
            entries = await client.get_read_entries(limit=100, offset=0)

            # Verify API was called with correct parameters
            mock_client.get_entries.assert_called_once_with(
                status=["read"],
                limit=100,
                offset=0,
                order="changed_at",
                direction="desc",
            )

            # Verify we got Entry objects
            assert len(entries) == 2
            assert entries[0].id == 1
            assert entries[0].title == "Read Entry 1"
            assert entries[0].status == "read"
            assert entries[1].id == 2
            assert entries[1].title == "Read Entry 2"

    @pytest.mark.asyncio
    async def test_get_read_entries_with_custom_params(self):
        """Test getting read entries with custom limit and offset."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            mock_client.get_entries.return_value = {"entries": []}

            client = MinifluxClient("http://localhost:8080", "test-key")
            await client.get_read_entries(limit=200, offset=50)

            # Verify API was called with custom parameters
            mock_client.get_entries.assert_called_once_with(
                status=["read"],
                limit=200,
                offset=50,
                order="changed_at",
                direction="desc",
            )

    @pytest.mark.asyncio
    async def test_get_read_entries_empty_list(self):
        """Test getting read entries when none exist."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock empty response
            mock_client.get_entries.return_value = {"entries": []}

            client = MinifluxClient("http://localhost:8080", "test-key")
            entries = await client.get_read_entries()

            # Verify we got empty list
            assert len(entries) == 0
            assert isinstance(entries, list)

    @pytest.mark.asyncio
    async def test_get_read_entries_orders_by_changed_at_desc(self):
        """Test that read entries are ordered by changed_at descending (most recent first)."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            mock_client.get_entries.return_value = {
                "entries": [
                    {
                        "id": 2,
                        "feed_id": 20,
                        "title": "Recently Read",
                        "url": "https://example.com/2",
                        "content": "Content 2",
                        "published_at": "2024-01-01T12:00:00Z",
                        "status": "read",
                        "starred": False,
                        "feed": {
                            "id": 20,
                            "title": "Test Feed 2",
                            "site_url": "https://example.com",
                            "feed_url": "https://example.com/feed2",
                        },
                    },
                    {
                        "id": 1,
                        "feed_id": 10,
                        "title": "Older Read",
                        "url": "https://example.com/1",
                        "content": "Content 1",
                        "published_at": "2024-01-01T12:00:00Z",
                        "status": "read",
                        "starred": False,
                        "feed": {
                            "id": 10,
                            "title": "Test Feed 1",
                            "site_url": "https://example.com",
                            "feed_url": "https://example.com/feed",
                        },
                    },
                ]
            }

            client = MinifluxClient("http://localhost:8080", "test-key")
            entries = await client.get_read_entries()

            # Verify order parameter
            mock_client.get_entries.assert_called_once()
            call_kwargs = mock_client.get_entries.call_args.kwargs
            assert call_kwargs["order"] == "changed_at"
            assert call_kwargs["direction"] == "desc"

            # Verify entries are in expected order (most recent first)
            assert entries[0].id == 2
            assert entries[0].title == "Recently Read"
            assert entries[1].id == 1
            assert entries[1].title == "Older Read"


class TestMinifluxClientGetUserInfo:
    """Test get_user_info method for settings functionality."""

    @pytest.mark.asyncio
    async def test_get_user_info_success(self):
        """Test getting user information successfully."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock the response with user info
            mock_client.me.return_value = {
                "id": 1,
                "username": "john_doe",
                "is_admin": False,
                "theme": "system",
                "language": "en_US",
                "timezone": "America/New_York",
                "entry_direction": "asc",
                "entries_per_page": 100,
            }

            client = MinifluxClient("http://localhost:8080", "test-key")
            user_info = await client.get_user_info()

            # Verify API was called
            mock_client.me.assert_called_once()

            # Verify we got the user info
            assert user_info["username"] == "john_doe"
            assert user_info["timezone"] == "America/New_York"
            assert user_info["language"] == "en_US"
            assert user_info["is_admin"] is False

    @pytest.mark.asyncio
    async def test_get_user_info_minimal(self):
        """Test getting minimal user information."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock minimal response
            mock_client.me.return_value = {
                "id": 1,
                "username": "user",
            }

            client = MinifluxClient("http://localhost:8080", "test-key")
            user_info = await client.get_user_info()

            # Verify we got the minimal info
            assert user_info["id"] == 1
            assert user_info["username"] == "user"


class TestMinifluxClientGetIntegrationsStatus:
    """Test get_integrations_status method for settings functionality."""

    @pytest.mark.asyncio
    async def test_get_integrations_status_enabled(self):
        """Test checking integrations status when enabled."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock response indicating integrations are enabled
            mock_client.get_integrations_status.return_value = True

            client = MinifluxClient("http://localhost:8080", "test-key")
            status = await client.get_integrations_status()

            # Verify API was called
            mock_client.get_integrations_status.assert_called_once()

            # Verify status
            assert status is True

    @pytest.mark.asyncio
    async def test_get_integrations_status_disabled(self):
        """Test checking integrations status when disabled."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock response indicating integrations are disabled
            mock_client.get_integrations_status.return_value = False

            client = MinifluxClient("http://localhost:8080", "test-key")
            status = await client.get_integrations_status()

            # Verify API was called
            mock_client.get_integrations_status.assert_called_once()

            # Verify status
            assert status is False


class TestMinifluxClientCategoryMethods:
    """Test category-related API methods."""

    @pytest.mark.asyncio
    async def test_get_categories_list_response(self):
        """Test get_categories with list response."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock list response
            mock_client.get_categories.return_value = [
                {"id": 1, "title": "News"},
                {"id": 2, "title": "Tech"},
            ]

            client = MinifluxClient("http://localhost:8080", "test-key")
            categories = await client.get_categories()

            assert len(categories) == 2
            assert categories[0].title == "News"
            assert categories[1].title == "Tech"

    @pytest.mark.asyncio
    async def test_get_categories_dict_response(self):
        """Test get_categories with dict response (fallback)."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            # Mock dict response
            mock_client.get_categories.return_value = {
                "categories": [
                    {"id": 1, "title": "News"},
                ]
            }

            client = MinifluxClient("http://localhost:8080", "test-key")
            categories = await client.get_categories()

            assert len(categories) == 1
            assert categories[0].title == "News"

    @pytest.mark.asyncio
    async def test_create_category(self):
        """Test creating a category."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            mock_client.create_category.return_value = {"id": 3, "title": "New Category"}

            client = MinifluxClient("http://localhost:8080", "test-key")
            category = await client.create_category("New Category")

            assert category.id == 3
            assert category.title == "New Category"
            mock_client.create_category.assert_called_once_with("New Category")

    @pytest.mark.asyncio
    async def test_update_category(self):
        """Test updating a category."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            mock_client.update_category.return_value = {"id": 1, "title": "Updated"}

            client = MinifluxClient("http://localhost:8080", "test-key")
            category = await client.update_category(1, "Updated")

            assert category.title == "Updated"
            mock_client.update_category.assert_called_once_with(1, "Updated")

    @pytest.mark.asyncio
    async def test_delete_category(self):
        """Test deleting a category."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            mock_client.delete_category.return_value = None

            client = MinifluxClient("http://localhost:8080", "test-key")
            await client.delete_category(1)

            mock_client.delete_category.assert_called_once_with(1)


class TestMinifluxClientFeedMethods:
    """Test feed-related API methods."""

    @pytest.mark.asyncio
    async def test_refresh_feed(self):
        """Test refreshing a specific feed."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            mock_client.refresh_feed.return_value = None

            client = MinifluxClient("http://localhost:8080", "test-key")
            await client.refresh_feed(123)

            mock_client.refresh_feed.assert_called_once_with(123)

    @pytest.mark.asyncio
    async def test_create_feed_without_category(self):
        """Test creating a feed without category."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            mock_client.create_feed.return_value = {
                "id": 1,
                "title": "Test Feed",
                "site_url": "https://example.com",
                "feed_url": "https://example.com/feed",
            }

            client = MinifluxClient("http://localhost:8080", "test-key")
            feed = await client.create_feed("https://example.com/feed")

            assert feed.title == "Test Feed"
            mock_client.create_feed.assert_called_once_with("https://example.com/feed")

    @pytest.mark.asyncio
    async def test_create_feed_with_category(self):
        """Test creating a feed with category."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            mock_client.create_feed.return_value = {
                "id": 1,
                "title": "Test Feed",
                "site_url": "https://example.com",
                "feed_url": "https://example.com/feed",
            }

            client = MinifluxClient("http://localhost:8080", "test-key")
            feed = await client.create_feed("https://example.com/feed", category_id=5)

            assert feed.title == "Test Feed"
            mock_client.create_feed.assert_called_once_with("https://example.com/feed", category_id=5)

    @pytest.mark.asyncio
    async def test_update_feed(self):
        """Test updating a feed."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            mock_client.update_feed.return_value = {
                "id": 1,
                "title": "Updated Feed",
                "site_url": "https://example.com",
                "feed_url": "https://example.com/feed",
            }

            client = MinifluxClient("http://localhost:8080", "test-key")
            feed = await client.update_feed(1, title="Updated Feed")

            assert feed.title == "Updated Feed"
            mock_client.update_feed.assert_called_once_with(1, title="Updated Feed")

    @pytest.mark.asyncio
    async def test_get_feed(self):
        """Test getting a specific feed."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            mock_client.get_feed.return_value = {
                "id": 1,
                "title": "Test Feed",
                "site_url": "https://example.com",
                "feed_url": "https://example.com/feed",
            }

            client = MinifluxClient("http://localhost:8080", "test-key")
            feed = await client.get_feed(1)

            assert feed.title == "Test Feed"
            mock_client.get_feed.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_feed(self):
        """Test deleting a feed."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            mock_client.delete_feed.return_value = None

            client = MinifluxClient("http://localhost:8080", "test-key")
            await client.delete_feed(1)

            mock_client.delete_feed.assert_called_once_with(1)


class TestMinifluxClientContentMethods:
    """Test content fetching methods."""

    @pytest.mark.asyncio
    async def test_fetch_original_content(self):
        """Test fetching original content for an entry."""
        with patch("miniflux_tui.api.client.MinifluxClientBase") as mock_base_class:
            mock_client = MagicMock()
            mock_base_class.return_value = mock_client

            mock_client.fetch_entry_content.return_value = {"content": "<p>Original content</p>"}

            client = MinifluxClient("http://localhost:8080", "test-key")
            content = await client.fetch_original_content(123)

            assert content == "<p>Original content</p>"
            mock_client.fetch_entry_content.assert_called_once_with(123)
