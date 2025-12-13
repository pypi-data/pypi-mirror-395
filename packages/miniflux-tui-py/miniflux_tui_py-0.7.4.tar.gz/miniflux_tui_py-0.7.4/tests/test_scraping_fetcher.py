# SPDX-License-Identifier: MIT
"""Tests for secure content fetcher."""

from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from miniflux_tui.scraping.fetcher import SecureFetcher


class TestSecureFetcher:
    """Test suite for SecureFetcher class."""

    def test_init(self):
        """Test fetcher initialization."""
        fetcher = SecureFetcher()
        assert fetcher.MAX_SIZE == 5 * 1024 * 1024
        assert fetcher.TIMEOUT == 10
        assert {"http", "https"} == fetcher.ALLOWED_SCHEMES
        assert fetcher.client is not None

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            # Valid URLs
            ("https://example.com", True),
            ("http://example.com", True),
            ("https://example.com/path", True),
            ("https://subdomain.example.com", True),
            ("http://example.com:8080/path", True),
            # Invalid schemes
            ("ftp://example.com", False),
            ("file:///etc/passwd", False),
            ("javascript:alert(1)", False),
            ("data:text/html,<script>", False),
            # Localhost variants
            ("http://localhost", False),
            ("http://localhost:8080", False),
            ("https://LOCALHOST", False),
            # Loopback IPs
            ("http://127.0.0.1", False),
            ("http://127.0.0.2", False),
            ("http://127.255.255.255", False),
            # Private IP ranges
            ("http://10.0.0.1", False),
            ("http://192.168.1.1", False),
            ("http://192.168.255.255", False),
            ("http://172.16.0.1", False),
            ("http://172.31.255.255", False),
            # Link-local
            ("http://169.254.1.1", False),
            # Current network
            ("http://0.0.0.0", False),
            # Invalid formats
            ("", False),
            ("not-a-url", False),
            ("//example.com", False),
        ],
    )
    def test_is_safe_url(self, url, expected):
        """Test URL safety validation."""
        fetcher = SecureFetcher()
        assert fetcher._is_safe_url(url) == expected

    @pytest.mark.asyncio
    async def test_fetch_success(self):
        """Test successful content fetch."""
        fetcher = SecureFetcher()

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"content-length": "1000"}
        mock_response.content = b"<html>Test content</html>"
        mock_response.text = "<html>Test content</html>"

        with patch.object(fetcher.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            result = await fetcher.fetch("https://example.com")

            assert result == "<html>Test content</html>"
            mock_get.assert_called_once_with("https://example.com")

    @pytest.mark.asyncio
    async def test_fetch_unsafe_url(self):
        """Test fetch rejects unsafe URLs."""
        fetcher = SecureFetcher()

        with pytest.raises(ValueError, match="Unsafe URL"):
            await fetcher.fetch("http://localhost")

        with pytest.raises(ValueError, match="Unsafe URL"):
            await fetcher.fetch("file:///etc/passwd")

    @pytest.mark.asyncio
    async def test_fetch_response_too_large_header(self):
        """Test fetch rejects oversized responses via header."""
        fetcher = SecureFetcher()

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"content-length": str(10 * 1024 * 1024)}  # 10MB

        with patch.object(fetcher.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            with pytest.raises(ValueError, match="Response too large"):
                await fetcher.fetch("https://example.com")

    @pytest.mark.asyncio
    async def test_fetch_response_too_large_content(self):
        """Test fetch rejects oversized responses via actual content."""
        fetcher = SecureFetcher()

        # Create content > 5MB
        large_content = b"x" * (6 * 1024 * 1024)

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.content = large_content

        with patch.object(fetcher.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            with pytest.raises(ValueError, match="Response too large"):
                await fetcher.fetch("https://example.com")

    @pytest.mark.asyncio
    async def test_fetch_timeout(self):
        """Test fetch handles timeout errors."""
        fetcher = SecureFetcher()

        with patch.object(fetcher.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = httpx.TimeoutException("Timeout")

            with pytest.raises(TimeoutError, match="Timeout fetching"):
                await fetcher.fetch("https://example.com")

    @pytest.mark.asyncio
    async def test_fetch_http_error(self):
        """Test fetch handles HTTP errors."""
        fetcher = SecureFetcher()

        mock_response = Mock()
        mock_response.status_code = 404

        with patch.object(fetcher.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = httpx.HTTPStatusError("Not Found", request=Mock(), response=mock_response)

            with pytest.raises(RuntimeError, match="HTTP error 404"):
                await fetcher.fetch("https://example.com/notfound")

    @pytest.mark.asyncio
    async def test_fetch_generic_error(self):
        """Test fetch handles unexpected errors."""
        fetcher = SecureFetcher()

        with patch.object(fetcher.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = Exception("Network error")

            with pytest.raises(RuntimeError, match="Fetch error"):
                await fetcher.fetch("https://example.com")

    @pytest.mark.asyncio
    async def test_close(self):
        """Test fetcher cleanup."""
        fetcher = SecureFetcher()

        with patch.object(fetcher.client, "aclose", new_callable=AsyncMock) as mock_close:
            await fetcher.close()
            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test fetcher as async context manager."""
        async with SecureFetcher() as fetcher:
            assert fetcher is not None
            assert fetcher.client is not None

        # Client should be closed after context exit
        # We can't easily verify this without accessing internals

    def test_private_ip_ranges_comprehensive(self):
        """Test all private IP range prefixes are blocked."""
        fetcher = SecureFetcher()

        # Test all Class B private ranges
        for i in range(16, 32):
            url = f"http://172.{i}.0.1"
            assert not fetcher._is_safe_url(url), f"Should block {url}"

        # Test public IPs that should be allowed
        public_ips = [
            "http://8.8.8.8",  # Google DNS
            "http://1.1.1.1",  # Cloudflare DNS
            "http://172.15.0.1",  # Just before private range
            "http://172.32.0.1",  # Just after private range
            "http://192.167.0.1",  # Before 192.168
            "http://192.169.0.1",  # After 192.168
        ]

        for url in public_ips:
            assert fetcher._is_safe_url(url), f"Should allow {url}"
