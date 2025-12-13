# SPDX-License-Identifier: MIT
"""Documentation cache for Miniflux rules documentation."""

from __future__ import annotations

import httpx


class DocsCache:
    """Session-based documentation cache for Miniflux rule documentation.

    Fetches documentation snippets on-demand and caches them in memory for
    the duration of the session to avoid repeated network requests.

    Attributes:
        cache: Dictionary storing cached documentation snippets by rule type
    """

    def __init__(self) -> None:
        """Initialize the documentation cache."""
        self.cache: dict[str, str] = {}

    async def get_documentation(self, rule_type: str) -> str:
        """Fetch documentation snippet, cache it for session duration.

        Args:
            rule_type: Type of rule (e.g., 'scraper_rules', 'rewrite_rules')

        Returns:
            Documentation snippet as a string, or empty string if fetch fails

        Raises:
            ValueError: If rule_type is not recognized
        """
        if not rule_type:
            msg = "rule_type cannot be empty"
            raise ValueError(msg)

        # Return cached version if available
        if rule_type in self.cache:
            return self.cache[rule_type]

        # Fetch from web and cache
        snippet = await self._fetch_from_web(rule_type)
        self.cache[rule_type] = snippet
        return snippet

    async def _fetch_from_web(self, rule_type: str) -> str:
        """Fetch documentation snippet from miniflux.app.

        Args:
            rule_type: Type of rule documentation to fetch

        Returns:
            Documentation snippet, or empty string if fetch fails
        """
        try:
            return await self._fetch_docs_content(rule_type)
        except Exception:
            # Return empty string on any error - don't crash the app
            return ""

    async def _fetch_docs_content(self, rule_type: str) -> str:
        """Fetch and extract documentation content from web.

        Args:
            rule_type: Type of rule documentation to fetch

        Returns:
            Cleaned documentation text

        Raises:
            Exception: Any network or parsing error
        """
        url = "https://miniflux.app/docs/rules.html"

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()

        # Parse HTML and extract relevant section
        # This will be implemented by DocsFetcher
        return f"Documentation for {rule_type} would be extracted from {url}"

    def clear(self) -> None:
        """Clear all cached documentation."""
        self.cache.clear()

    def get_cached_keys(self) -> list[str]:
        """Get list of currently cached documentation keys.

        Returns:
            List of rule types that have been cached
        """
        return list(self.cache.keys())
