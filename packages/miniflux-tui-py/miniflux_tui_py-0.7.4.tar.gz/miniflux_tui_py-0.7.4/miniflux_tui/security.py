# SPDX-License-Identifier: MIT
"""Security utilities for input validation and sanitization."""

import re
from urllib.parse import urlparse


def _check_url_basic_validity(url: str) -> str | None:
    """Check URL length and emptiness.

    Args:
        url: The URL to validate

    Returns:
        Error message if invalid, None if valid
    """
    if len(url) > 2048:
        return "URL too long (max 2048 characters)"
    if not url.strip():
        return "URL cannot be empty"
    return None


def _check_url_scheme(parsed) -> str | None:
    """Check that URL uses allowed scheme (HTTP/HTTPS).

    Args:
        parsed: Parsed URL from urlparse

    Returns:
        Error message if invalid, None if valid
    """
    if parsed.scheme not in ["http", "https"]:
        return "Only HTTP and HTTPS URLs are allowed"
    if not parsed.netloc:
        return "URL must have a valid hostname"
    return None


def _check_url_hostname(parsed) -> str | None:
    """Check that hostname is not local or private.

    Args:
        parsed: Parsed URL from urlparse

    Returns:
        Error message if invalid, None if valid
    """
    # Extract hostname without port
    hostname = parsed.netloc.split(":")[0].lower()

    # Block localhost/loopback addresses
    if hostname in ["localhost", "127.0.0.1", "::1", "[::1]"]:
        return "Cannot add local URLs (localhost)"

    # Block private IP ranges
    if _is_private_ip(hostname):
        return "Cannot add private network URLs"

    # Block IPv6 loopback and link-local
    if hostname.startswith(("fe80:", "[fe80:")):
        return "Cannot add link-local IPv6 addresses"

    return None


def _is_private_ip(hostname: str) -> bool:
    """Check if hostname is a private IP address.

    Args:
        hostname: The hostname/IP to check

    Returns:
        True if hostname is a private IP, False otherwise
    """
    private_patterns = [
        r"^192\.168\.",
        r"^10\.",
        r"^172\.(1[6-9]|2[0-9]|3[01])\.",  # 172.16.0.0 - 172.31.255.255
        r"^127\.",  # Loopback
        r"^169\.254\.",  # Link-local
    ]
    return any(re.match(pattern, hostname) for pattern in private_patterns)


def _check_url_suspicious_content(url: str) -> str | None:
    """Check for control characters and suspicious patterns.

    Args:
        url: The URL to validate

    Returns:
        Error message if invalid, None if valid
    """
    # Check for control characters
    if any(ord(c) < 32 for c in url):
        return "URL contains invalid control characters"

    # Check for newlines (header injection)
    if "\n" in url or "\r" in url:
        return "URL contains invalid characters (newlines)"

    # Check for shell metacharacters and null bytes
    if _has_suspicious_patterns(url):
        return "URL contains suspicious characters"

    return None


def _has_suspicious_patterns(url: str) -> bool:
    """Check if URL contains suspicious patterns.

    Args:
        url: The URL to validate

    Returns:
        True if suspicious patterns found, False otherwise
    """
    suspicious_patterns = [
        r"[;|&$`<>]",  # Shell metacharacters
        r"%00",  # Null byte
    ]
    return any(re.search(pattern, url) for pattern in suspicious_patterns)


def validate_feed_url(url: str) -> tuple[bool, str]:
    """Validate and sanitize feed URL for SSRF prevention.

    Args:
        url: The URL to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Basic validation
    error = _check_url_basic_validity(url)
    if error:
        return False, error

    # Parse URL (urlparse doesn't raise exceptions, just returns parsed components)
    parsed = urlparse(url)

    # Protocol validation
    error = _check_url_scheme(parsed)
    if error:
        return False, error

    # Hostname validation
    error = _check_url_hostname(parsed)
    if error:
        return False, error

    # Suspicious content validation
    error = _check_url_suspicious_content(url)
    if error:
        return False, error

    return True, ""


def sanitize_error_message(error: Exception, operation: str) -> str:
    """Sanitize error messages before displaying to user.

    Prevents information disclosure by mapping exception types to generic messages.

    Args:
        error: The caught exception
        operation: Description of what was being done (e.g., "adding feed")

    Returns:
        Safe error message for display to user
    """
    error_type = type(error).__name__

    # Map specific exception types to safe messages
    safe_messages = {
        "ValueError": f"Invalid input for {operation}",
        "TimeoutError": f"Request timed out during {operation}",
        "ConnectionError": f"Network error during {operation}",
        "PermissionError": f"Permission denied for {operation}",
        "OSError": f"System error during {operation}",
        "RuntimeError": f"Unable to complete {operation}",
    }

    # Return mapped message or generic fallback
    return safe_messages.get(error_type, f"Failed to complete {operation}")
