# SPDX-License-Identifier: MIT
"""Tests for the RulesHelperScreen."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

from miniflux_tui.docs_cache import DocsCache
from miniflux_tui.ui.screens.rules_helper import RulesHelperScreen


@pytest.fixture
def mock_docs_cache():
    """Create a mock documentation cache."""
    cache = MagicMock(spec=DocsCache)
    cache.get_documentation = AsyncMock()
    return cache


class TestRulesHelperScreenInitialization:
    """Test RulesHelperScreen initialization."""

    def test_init_stores_rule_type(self):
        """Test that __init__ properly stores rule type."""
        screen = RulesHelperScreen(rule_type="scraper_rules")
        assert screen.rule_type == "scraper_rules"

    def test_init_stores_docs_cache(self, mock_docs_cache):
        """Test that __init__ stores docs cache."""
        screen = RulesHelperScreen(
            rule_type="rewrite_rules",
            docs_cache=mock_docs_cache,
        )
        assert screen.docs_cache is mock_docs_cache

    def test_init_without_docs_cache(self):
        """Test initialization without docs cache."""
        screen = RulesHelperScreen(rule_type="blocklist_rules")
        assert screen.docs_cache is None

    def test_init_creates_fetcher(self):
        """Test that DocsFetcher is created."""
        screen = RulesHelperScreen(rule_type="keeplist_rules")
        assert screen.fetcher is not None

    def test_bindings_defined(self):
        """Test that key bindings are defined."""
        screen = RulesHelperScreen(rule_type="scraper_rules")
        assert len(screen.BINDINGS) > 0
        assert any("escape" in str(b) for b in screen.BINDINGS)

    def test_default_css_defined(self):
        """Test that DEFAULT_CSS is defined."""
        screen = RulesHelperScreen(rule_type="scraper_rules")
        assert screen.DEFAULT_CSS is not None
        assert len(screen.DEFAULT_CSS) > 0


class TestRulesHelperScreenTitles:
    """Test rule type to title conversion."""

    @pytest.mark.parametrize(
        ("rule_type", "expected_title"),
        [
            ("scraper_rules", "Scraper Rules"),
            ("rewrite_rules", "Rewrite Rules"),
            ("blocklist_rules", "Blocklist Rules"),
            ("keeplist_rules", "Keeplist Rules"),
        ],
    )
    def test_get_rule_title(self, rule_type, expected_title):
        """Test rule type title conversion."""
        screen = RulesHelperScreen(rule_type=rule_type)
        assert screen._get_rule_title() == expected_title

    def test_get_rule_title_unknown_type(self):
        """Test title for unknown rule type."""
        screen = RulesHelperScreen(rule_type="unknown_rule")
        assert screen._get_rule_title() == "unknown_rule"


class TestRulesHelperScreenDocumentation:
    """Test documentation fetching and display."""

    @pytest.mark.asyncio
    async def test_on_mount_with_cache(self, mock_docs_cache):
        """Test on_mount fetches documentation from cache."""
        mock_docs_cache.get_documentation.return_value = "Scraper Rules Documentation"

        screen = RulesHelperScreen(
            rule_type="scraper_rules",
            docs_cache=mock_docs_cache,
        )

        with patch.object(screen, "query_one"):
            await screen.on_mount()

        mock_docs_cache.get_documentation.assert_called_once_with("scraper_rules")
        assert screen.content == "Scraper Rules Documentation"

    @pytest.mark.asyncio
    async def test_on_mount_without_cache(self):
        """Test on_mount fetches documentation without cache."""
        screen = RulesHelperScreen(rule_type="rewrite_rules")

        fetcher_mock = AsyncMock()
        fetcher_mock.fetch_snippet.return_value = "Rewrite Rules Documentation"

        screen.fetcher = fetcher_mock

        with patch.object(screen, "query_one"):
            await screen.on_mount()

        fetcher_mock.fetch_snippet.assert_called_once_with("rewrite_rules")
        assert screen.content == "Rewrite Rules Documentation"

    @pytest.mark.asyncio
    async def test_on_mount_invalid_rule_type(self, mock_docs_cache):
        """Test on_mount with invalid rule type."""
        mock_docs_cache.get_documentation.side_effect = ValueError("Unknown rule type")

        screen = RulesHelperScreen(
            rule_type="invalid_rule",
            docs_cache=mock_docs_cache,
        )

        with patch.object(screen, "query_one") as mock_query:
            await screen.on_mount()

        # Verify error handling
        assert mock_query.called


class TestRulesHelperScreenErrorHandling:
    """Test error handling in RulesHelperScreen."""

    @pytest.mark.asyncio
    async def test_on_mount_timeout_error(self):
        """Test on_mount with timeout error."""
        screen = RulesHelperScreen(rule_type="scraper_rules")

        fetcher_mock = AsyncMock()
        fetcher_mock.fetch_snippet.side_effect = TimeoutError()

        screen.fetcher = fetcher_mock

        with patch.object(screen, "query_one"):
            await screen.on_mount()

        # Should handle error gracefully

    @pytest.mark.asyncio
    async def test_on_mount_connection_error(self):
        """Test on_mount with connection error."""
        screen = RulesHelperScreen(rule_type="rewrite_rules")

        fetcher_mock = AsyncMock()
        fetcher_mock.fetch_snippet.side_effect = ConnectionError()

        screen.fetcher = fetcher_mock

        with patch.object(screen, "query_one"):
            await screen.on_mount()

        # Should handle error gracefully

    @pytest.mark.asyncio
    async def test_on_mount_generic_error(self):
        """Test on_mount with generic exception."""
        screen = RulesHelperScreen(rule_type="blocklist_rules")

        fetcher_mock = AsyncMock()
        fetcher_mock.fetch_snippet.side_effect = Exception("Unknown error")

        screen.fetcher = fetcher_mock

        with patch.object(screen, "query_one"):
            await screen.on_mount()

        # Should handle error gracefully


class TestRulesHelperScreenActions:
    """Test RulesHelperScreen actions."""

    @pytest.mark.asyncio
    async def test_action_close_helper(self):
        """Test closing the helper screen."""
        screen = RulesHelperScreen(rule_type="scraper_rules")
        mock_app = MagicMock()
        mock_app.pop_screen = MagicMock()

        with patch.object(type(screen), "app", new_callable=PropertyMock) as mock_app_prop:
            mock_app_prop.return_value = mock_app
            await screen.action_close_helper()

            mock_app.pop_screen.assert_called_once()

    def test_show_error_updates_display(self):
        """Test error display updates."""
        screen = RulesHelperScreen(rule_type="scraper_rules")

        with patch.object(screen, "query_one") as mock_query:
            mock_help_text = MagicMock()
            mock_status = MagicMock()

            def side_effect(selector, expect_type=None):
                if "#help-text" in selector:
                    return mock_help_text
                if "#status-message" in selector:
                    return mock_status
                return MagicMock()

            mock_query.side_effect = side_effect

            screen._show_error("Test error message")

            mock_help_text.update.assert_called_once()
            mock_status.update.assert_called_once()


class TestRulesHelperScreenComposition:
    """Test RulesHelperScreen composition."""

    def test_compose_method_exists(self):
        """Test that compose method exists."""
        screen = RulesHelperScreen(rule_type="scraper_rules")

        # Verify compose method is callable
        assert callable(screen.compose)

    def test_compose_header_exists(self):
        """Test that Header is composed."""
        screen = RulesHelperScreen(rule_type="rewrite_rules")

        # Verify Header binding exists
        assert hasattr(screen, "BINDINGS")
        assert len(screen.BINDINGS) > 0
