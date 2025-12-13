# SPDX-License-Identifier: MIT
"""Documentation fetcher for Miniflux rule documentation."""

from __future__ import annotations

import re
from html.parser import HTMLParser

import httpx

# Mapping of rule types to their documentation anchors
RULE_TYPES = {
    "scraper_rules": "scraper-rules",
    "rewrite_rules": "rewrite-rules",
    "url_rewrite_rules": "url-rewrite-rules",
    "blocking_rules": "regex-based-blocking-filters",
    "keep_rules": "regex-based-keep-filters",
    "entry_blocking_rules": "entry-blocking-rules",
    "entry_allow_rules": "entry-allow-rules",
}

DOCS_URL = "https://miniflux.app/docs/rules.html"


class DocsFetcher:
    """Fetch and parse Miniflux documentation from miniflux.app.

    Responsible for fetching HTML from the Miniflux documentation site,
    extracting relevant sections for each rule type, and cleaning the
    content for TUI display.
    """

    def __init__(self, timeout: float = 10.0) -> None:
        """Initialize the documentation fetcher.

        Args:
            timeout: HTTP request timeout in seconds
        """
        self.timeout = timeout

    async def fetch_snippet(self, rule_type: str) -> str:
        """Fetch documentation snippet for a rule type.

        Args:
            rule_type: Type of rule (must be a key in RULE_TYPES)

        Returns:
            Clean text documentation snippet

        Raises:
            ValueError: If rule_type is not recognized
            Exception: Any network or parsing errors
        """
        if rule_type not in RULE_TYPES:
            valid_types = ", ".join(RULE_TYPES.keys())
            msg = f"Unknown rule type: {rule_type}. Valid types: {valid_types}"
            raise ValueError(msg)

        html = await self._fetch_html()
        anchor = RULE_TYPES[rule_type]
        snippet = self._extract_section(html, anchor, rule_type)
        return self._clean_text(snippet)

    async def _fetch_html(self) -> str:
        """Fetch HTML content from documentation URL.

        Returns:
            Raw HTML content

        Raises:
            Exception: Network errors or HTTP errors
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(DOCS_URL)
            response.raise_for_status()
            return response.text

    def _extract_section(self, html: str, anchor: str, rule_type: str) -> str:
        """Extract documentation section for a rule type.

        Args:
            html: Raw HTML content
            anchor: Documentation anchor/ID (e.g., "scraper-rules")
            rule_type: Rule type name for fallback message

        Returns:
            Extracted section text
        """
        # Look for the section heading with the anchor
        # Common patterns: id="anchor", id='anchor', or anchor in href
        patterns = [
            rf'<h[1-6][^>]*id=["\']?{anchor}["\']?[^>]*>(.*?)</h[1-6]>',
            rf'<a[^>]*id=["\']?{anchor}["\']?[^>]*>(.*?)</a>',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                # Extract content until next heading or end
                start_pos = match.start()
                # Find next h2 or h3 heading
                next_heading = re.search(r"<h[23]", html[start_pos + 1 :], re.IGNORECASE)
                if next_heading:
                    end_pos = start_pos + next_heading.start() + 1
                    section = html[start_pos:end_pos]
                else:
                    section = html[start_pos : start_pos + 3000]
                return section

        # Return placeholder if not found
        return f"Documentation section for {rule_type} not found in fetched content."

    def _clean_text(self, html_snippet: str) -> str:
        """Clean HTML snippet to plain text for TUI display.

        Args:
            html_snippet: HTML content to clean

        Returns:
            Cleaned plain text
        """
        # Parse HTML to extract text
        parser = HTMLContentParser()
        parser.feed(html_snippet)
        text = parser.get_text()

        # Remove excessive whitespace
        lines = text.split("\n")
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        cleaned_text = "\n".join(cleaned_lines)

        # Limit to reasonable length for display
        max_length = 2000
        if len(cleaned_text) > max_length:
            cleaned_text = cleaned_text[:max_length] + "\n... (truncated)"

        return cleaned_text


class HTMLContentParser(HTMLParser):
    """Custom HTML parser to extract text content safely."""

    def __init__(self) -> None:
        """Initialize the HTML parser."""
        super().__init__()
        self.text_parts: list[str] = []
        self.skip_tags = {"script", "style", "noscript"}
        self.current_tag_stack: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],  # noqa: ARG002
    ) -> None:
        """Handle opening tags."""
        self.current_tag_stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        """Handle closing tags."""
        if self.current_tag_stack and self.current_tag_stack[-1] == tag:
            self.current_tag_stack.pop()

    def handle_data(self, data: str) -> None:
        """Extract text data, skip content from certain tags."""
        if not self.current_tag_stack:
            return

        current_tag = self.current_tag_stack[-1]
        if current_tag not in self.skip_tags:
            self.text_parts.append(data)

    def get_text(self) -> str:
        """Get extracted text content."""
        return "".join(self.text_parts)


def _sanitize_html(html: str) -> str:
    """Sanitize HTML to prevent XSS when displaying in TUI.

    Args:
        html: Raw HTML content

    Returns:
        Sanitized HTML
    """
    # Remove potentially dangerous tags and attributes
    dangerous_patterns = [
        r"<script[^>]*>.*?</script>",  # Remove script tags
        r"<iframe[^>]*>.*?</iframe>",  # Remove iframes
        r"on\w+\s*=",  # Remove event handlers
        r"javascript:",  # Remove javascript: protocol
    ]

    sanitized = html
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE | re.DOTALL)

    return sanitized
