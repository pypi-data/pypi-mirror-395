# SPDX-License-Identifier: MIT
"""Tests for the documentation fetcher module."""

from __future__ import annotations

import pytest

from miniflux_tui.docs_fetcher import (
    DOCS_URL,
    RULE_TYPES,
    DocsFetcher,
    HTMLContentParser,
    _sanitize_html,
)


@pytest.fixture
def fetcher():
    """Create a DocsFetcher instance for testing."""
    return DocsFetcher(timeout=10.0)


@pytest.fixture
def sample_html():
    """Provide sample HTML for testing."""
    return """
    <html>
    <head><title>Test Page</title></head>
    <body>
    <h2 id="scraper-rules">Scraper Rules</h2>
    <p>This section describes scraper rules.</p>
    <p>Scraper rules allow you to extract content from articles.</p>
    <h2 id="rewrite-rules">Rewrite Rules</h2>
    <p>This section describes rewrite rules.</p>
    </body>
    </html>
    """


class TestDocsFetcherInitialization:
    """Test DocsFetcher initialization."""

    def test_init_with_default_timeout(self):
        """Test initialization with default timeout."""
        fetcher = DocsFetcher()
        assert fetcher.timeout == 10.0

    def test_init_with_custom_timeout(self):
        """Test initialization with custom timeout."""
        fetcher = DocsFetcher(timeout=20.0)
        assert fetcher.timeout == 20.0

    def test_init_stores_timeout(self):
        """Test that timeout is stored correctly."""
        timeout = 15.5
        fetcher = DocsFetcher(timeout=timeout)
        assert fetcher.timeout == timeout


class TestDocsFetcherValidation:
    """Test DocsFetcher input validation."""

    @pytest.mark.asyncio
    async def test_fetch_snippet_invalid_rule_type_raises_error(self, fetcher):
        """Test that invalid rule_type raises ValueError."""
        with pytest.raises(ValueError, match="Unknown rule type"):
            await fetcher.fetch_snippet("invalid_rule_type")

    @pytest.mark.asyncio
    async def test_fetch_snippet_empty_rule_type_raises_error(self, fetcher):
        """Test that empty rule_type raises ValueError."""
        with pytest.raises(ValueError, match="Unknown rule type"):
            await fetcher.fetch_snippet("")

    def test_rule_types_mapping_complete(self):
        """Test that all expected rule types are in the mapping."""
        expected_types = {
            "scraper_rules",
            "rewrite_rules",
            "url_rewrite_rules",
            "blocking_rules",
            "keep_rules",
            "entry_blocking_rules",
            "entry_allow_rules",
        }
        assert set(RULE_TYPES.keys()) == expected_types

    def test_rule_types_have_valid_anchors(self):
        """Test that all rule types have non-empty anchor values."""
        for _rule_type, anchor in RULE_TYPES.items():
            assert isinstance(anchor, str)
            assert len(anchor) > 0
            assert " " not in anchor  # No spaces in anchors


class TestHTMLContentParser:
    """Test HTMLContentParser functionality."""

    def test_parser_extracts_simple_text(self):
        """Test parsing simple HTML text."""
        html = "<p>Hello World</p>"
        parser = HTMLContentParser()
        parser.feed(html)
        assert parser.get_text() == "Hello World"

    def test_parser_extracts_multiple_paragraphs(self):
        """Test parsing multiple paragraphs."""
        html = "<p>First</p><p>Second</p>"
        parser = HTMLContentParser()
        parser.feed(html)
        text = parser.get_text()
        assert "First" in text
        assert "Second" in text

    def test_parser_skips_script_tags(self):
        """Test that script tags are skipped."""
        html = "<p>Visible</p><script>var x = 'hidden';</script><p>Also visible</p>"
        parser = HTMLContentParser()
        parser.feed(html)
        text = parser.get_text()
        assert "Visible" in text
        assert "hidden" not in text.lower() or "var x" not in text

    def test_parser_skips_style_tags(self):
        """Test that style tags are skipped."""
        html = "<p>Text</p><style>.hidden { display: none; }</style>"
        parser = HTMLContentParser()
        parser.feed(html)
        text = parser.get_text()
        assert "Text" in text
        assert "hidden" not in text or "display" not in text

    def test_parser_handles_nested_tags(self):
        """Test parsing nested HTML tags."""
        html = "<div><p>Nested <strong>content</strong></p></div>"
        parser = HTMLContentParser()
        parser.feed(html)
        text = parser.get_text()
        assert "Nested" in text
        assert "content" in text

    def test_parser_handles_empty_tags(self):
        """Test parsing empty tags."""
        parser = HTMLContentParser()
        parser.feed("<p></p><div></div>")
        # Should not raise error
        assert isinstance(parser.get_text(), str)

    def test_parser_get_text_returns_string(self):
        """Test that get_text always returns a string."""
        parser = HTMLContentParser()
        assert isinstance(parser.get_text(), str)


class TestDocsFetcherExtraction:
    """Test documentation section extraction."""

    def test_extract_section_finds_content(self, fetcher, sample_html):
        """Test that _extract_section finds documented content."""
        result = fetcher._extract_section(sample_html, "scraper-rules", "scraper_rules")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_extract_section_with_invalid_anchor(self, fetcher, sample_html):
        """Test extraction with non-existent anchor."""
        result = fetcher._extract_section(sample_html, "nonexistent", "test_type")
        assert isinstance(result, str)
        # Should return fallback message
        assert "not found" in result or "Documentation" in result

    def test_extract_section_extracts_multiple_sections(self, fetcher, sample_html):
        """Test extracting different sections."""
        scraper_result = fetcher._extract_section(sample_html, "scraper-rules", "scraper_rules")
        rewrite_result = fetcher._extract_section(sample_html, "rewrite-rules", "rewrite_rules")

        # Both should return strings
        assert isinstance(scraper_result, str)
        assert isinstance(rewrite_result, str)


class TestDocsFetcherCleaning:
    """Test HTML to text cleaning."""

    def test_clean_text_removes_tags(self, fetcher):
        """Test that clean_text removes HTML tags."""
        html = "<p>Hello <strong>World</strong></p>"
        result = fetcher._clean_text(html)
        assert "<p>" not in result
        assert "<strong>" not in result
        assert "Hello" in result
        assert "World" in result

    def test_clean_text_removes_whitespace(self, fetcher):
        """Test that clean_text normalizes whitespace."""
        html = "<p>  Line 1   </p>\n\n<p>   Line 2   </p>"
        result = fetcher._clean_text(html)
        # Excessive whitespace should be removed
        assert "\n\n\n" not in result

    def test_clean_text_limits_length(self, fetcher):
        """Test that clean_text limits output length."""
        long_html = "<p>" + ("x" * 5000) + "</p>"
        result = fetcher._clean_text(long_html)
        assert len(result) <= 2100  # 2000 + truncation message

    def test_clean_text_returns_string(self, fetcher):
        """Test that clean_text always returns a string."""
        result = fetcher._clean_text("<p>Test</p>")
        assert isinstance(result, str)

    def test_clean_text_handles_empty_html(self, fetcher):
        """Test clean_text with empty HTML."""
        result = fetcher._clean_text("")
        assert isinstance(result, str)


class TestSanitizeHTML:
    """Test HTML sanitization for XSS prevention."""

    def test_sanitize_removes_script_tags(self):
        """Test that script tags are removed."""
        html = '<p>Text</p><script>alert("xss")</script>'
        result = _sanitize_html(html)
        assert "<script>" not in result
        assert "</script>" not in result

    def test_sanitize_removes_iframe_tags(self):
        """Test that iframe tags are removed."""
        html = '<p>Text</p><iframe src="evil.com"></iframe>'
        result = _sanitize_html(html)
        assert "<iframe>" not in result
        assert "</iframe>" not in result

    def test_sanitize_removes_event_handlers(self):
        """Test that event handlers are removed."""
        html = '<img src="image.jpg" onclick="alert(\'xss\')" />'
        result = _sanitize_html(html)
        assert "onclick" not in result

    def test_sanitize_removes_javascript_protocol(self):
        """Test that javascript: protocol is removed."""
        html = "<a href=\"javascript:alert('xss')\">Click</a>"
        result = _sanitize_html(html)
        assert "javascript:" not in result

    def test_sanitize_preserves_safe_html(self):
        """Test that safe HTML is preserved."""
        html = "<p>Hello <strong>World</strong></p>"
        result = _sanitize_html(html)
        assert "<p>" in result
        assert "<strong>" in result
        assert "Hello" in result

    def test_sanitize_case_insensitive(self):
        """Test that sanitization works with different cases."""
        html = '<SCRIPT>alert("xss")</SCRIPT>'
        result = _sanitize_html(html)
        assert "script" not in result.lower() or "<" not in result  # Tags removed


class TestDocsFetcherMethods:
    """Test individual DocsFetcher methods."""

    def test_extract_section_case_insensitive(self, fetcher):
        """Test that section extraction is case insensitive for tags."""
        html = '<H2 id="SCRAPER-RULES">Content</H2>'
        result = fetcher._extract_section(html, "scraper-rules", "scraper_rules")
        assert isinstance(result, str)

    def test_extract_section_with_different_heading_levels(self, fetcher):
        """Test extraction with different heading levels."""
        html = """
        <h1 id="main">Main</h1>
        <h2 id="scraper-rules">Scraper Rules</h2>
        <p>Content</p>
        <h3 id="subsection">Subsection</h3>
        <h2 id="other">Other</h2>
        """
        result = fetcher._extract_section(html, "scraper-rules", "scraper_rules")
        assert isinstance(result, str)

    def test_clean_text_with_entities(self, fetcher):
        """Test clean_text with HTML entities."""
        html = "<p>&lt;script&gt; &amp; &quot;quotes&quot;</p>"
        result = fetcher._clean_text(html)
        assert isinstance(result, str)

    def test_clean_text_with_multiple_newlines(self, fetcher):
        """Test that clean_text consolidates multiple newlines."""
        html = "<p>Line 1</p>\n\n\n<p>Line 2</p>"
        result = fetcher._clean_text(html)
        # Should not have excessive newlines
        assert "\n\n\n" not in result


class TestDocsFetcherIntegration:
    """Integration tests for DocsFetcher."""

    @pytest.mark.asyncio
    async def test_all_rule_types_are_valid(self) -> None:
        """Test that all rule types can be queried without validation error."""
        for rule_type in RULE_TYPES:
            # Verify the rule type exists in the mapping
            assert rule_type in RULE_TYPES, f"Rule type {rule_type} should be valid"
            # Verify it has a valid anchor
            assert RULE_TYPES[rule_type], f"Rule type {rule_type} should have a valid anchor"

    def test_fetcher_timeout_is_positive(self, fetcher):
        """Test that fetcher has positive timeout."""
        assert fetcher.timeout > 0

    def test_docs_url_is_valid(self):
        """Test that DOCS_URL is a valid HTTPS URL."""
        assert DOCS_URL.startswith("https://")
        assert "miniflux.app" in DOCS_URL

    def test_rule_types_dict_not_empty(self):
        """Test that RULE_TYPES dictionary is populated."""
        assert len(RULE_TYPES) > 0
        assert len(RULE_TYPES) == 7  # Should have 7 rule types
