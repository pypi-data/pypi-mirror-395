# SPDX-License-Identifier: MIT
"""Secure web content fetcher with strict validation and safety measures."""

from typing import ClassVar, NoReturn
from urllib.parse import urlparse

import httpx


class SecureFetcher:
    """Safely fetch and validate web content with security constraints."""

    MAX_SIZE: ClassVar[int] = 5 * 1024 * 1024  # 5MB max response size
    TIMEOUT: ClassVar[int] = 10  # seconds
    ALLOWED_SCHEMES: ClassVar[set[str]] = {"http", "https"}

    def __init__(self):
        """Initialize secure HTTP client with safety settings."""
        self.client = httpx.AsyncClient(
            timeout=self.TIMEOUT,
            follow_redirects=True,
            max_redirects=5,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; MinifluxTUI/0.6.0)",
            },
        )

    async def fetch(self, url: str) -> str:
        """Safely fetch URL content with validation and size limits.

        Args:
            url: The URL to fetch

        Returns:
            The response text content

        Raises:
            ValueError: If URL is unsafe or response too large
            TimeoutError: If request times out
            RuntimeError: For other fetch errors
        """
        self._validate_url(url)

        try:
            response = await self.client.get(url)
            response.raise_for_status()
            self._validate_response_size(response, url)
            return response.text
        except ValueError:
            raise
        except httpx.TimeoutException as e:
            self._handle_timeout(url, e)
        except httpx.HTTPStatusError as e:
            self._handle_http_error(url, e)
        except Exception as e:
            self._handle_generic_error(url, e)

    def _validate_url(self, url: str) -> None:
        """Validate that URL is safe to fetch.

        Args:
            url: The URL to validate

        Raises:
            ValueError: If URL is unsafe
        """
        if not self._is_safe_url(url):
            msg = f"Unsafe URL: {url}"
            raise ValueError(msg)

    def _validate_response_size(self, response: httpx.Response, url: str) -> None:
        """Validate response size is within limits.

        Checks both headers and actual content size.

        Args:
            response: The HTTP response object
            url: The URL being fetched (for error messages)

        Raises:
            ValueError: If response exceeds MAX_SIZE
        """
        self._check_content_length_header(response, url)
        self._check_actual_content_size(response, url)

    def _check_content_length_header(self, response: httpx.Response, url: str) -> None:
        """Check Content-Length header before reading full content.

        Args:
            response: The HTTP response object
            url: The URL being fetched (for error messages)

        Raises:
            ValueError: If Content-Length header exceeds MAX_SIZE
        """
        content_length = response.headers.get("content-length")
        if content_length and int(content_length) > self.MAX_SIZE:
            msg = f"Response too large: {content_length} bytes from {url}"
            raise ValueError(msg)

    def _check_actual_content_size(self, response: httpx.Response, url: str) -> None:
        """Check actual content size after reading.

        Args:
            response: The HTTP response object
            url: The URL being fetched (for error messages)

        Raises:
            ValueError: If actual content exceeds MAX_SIZE
        """
        content = response.content
        if len(content) > self.MAX_SIZE:
            msg = f"Response too large: {len(content)} bytes from {url}"
            raise ValueError(msg)

    def _handle_timeout(self, url: str, e: httpx.TimeoutException) -> NoReturn:
        """Handle timeout exceptions.

        Args:
            url: The URL that timed out
            e: The timeout exception

        Raises:
            TimeoutError: Always raises with formatted message
        """
        msg = f"Timeout fetching {url}"
        raise TimeoutError(msg) from e

    def _handle_http_error(self, url: str, e: httpx.HTTPStatusError) -> NoReturn:
        """Handle HTTP status errors.

        Args:
            url: The URL that returned an error
            e: The HTTP status error

        Raises:
            RuntimeError: Always raises with formatted message
        """
        msg = f"HTTP error {e.response.status_code}: {url}"
        raise RuntimeError(msg) from e

    def _handle_generic_error(self, url: str, e: Exception) -> NoReturn:
        """Handle generic fetch errors.

        Args:
            url: The URL being fetched
            e: The exception that occurred

        Raises:
            RuntimeError: Always raises with formatted message
        """
        msg = f"Fetch error for {url}: {e}"
        raise RuntimeError(msg) from e

    def _is_safe_url(self, url: str) -> bool:
        """Validate URL is safe to fetch.

        Checks for:
        - Valid http/https scheme
        - Valid domain name
        - No localhost or private IPs
        - No file:// or other dangerous schemes

        Args:
            url: The URL to validate

        Returns:
            True if URL is safe to fetch, False otherwise
        """
        try:
            parsed = urlparse(url)

            # Must have valid scheme
            if parsed.scheme not in self.ALLOWED_SCHEMES:
                return False

            # Must have a network location (domain)
            if not parsed.netloc:
                return False

            netloc_lower = parsed.netloc.lower()

            # Block localhost
            if netloc_lower.startswith("localhost"):
                return False

            # Block common private IP ranges
            private_prefixes = (
                "127.",  # Loopback
                "0.",  # Current network
                "10.",  # Private Class A
                "192.168.",  # Private Class C
                "172.16.",  # Private Class B
                "172.17.",
                "172.18.",
                "172.19.",
                "172.20.",
                "172.21.",
                "172.22.",
                "172.23.",
                "172.24.",
                "172.25.",
                "172.26.",
                "172.27.",
                "172.28.",
                "172.29.",
                "172.30.",
                "172.31.",
                "169.254.",  # Link-local
            )

            # Check if any private prefix matches
            return all(not netloc_lower.startswith(prefix) for prefix in private_prefixes)
        except Exception:
            return False

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
