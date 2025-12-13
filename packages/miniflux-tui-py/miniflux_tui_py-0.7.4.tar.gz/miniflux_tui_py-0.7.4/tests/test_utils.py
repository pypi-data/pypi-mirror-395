# SPDX-License-Identifier: MIT
"""Tests for utility functions."""

import tomllib
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from miniflux_tui import utils
from miniflux_tui.utils import api_call, get_star_icon, get_status_icon


class TestGetStarIcon:
    """Test get_star_icon function."""

    def test_starred_returns_filled_star(self):
        """Test that starred=True returns filled star."""
        assert get_star_icon(True) == "★"

    def test_unstarred_returns_empty_star(self):
        """Test that starred=False returns empty star."""
        assert get_star_icon(False) == "☆"

    def test_star_icons_are_different(self):
        """Test that filled and empty stars are different."""
        filled = get_star_icon(True)
        empty = get_star_icon(False)
        assert filled != empty


class TestGetStatusIcon:
    """Test get_status_icon function."""

    def test_unread_returns_filled_circle(self):
        """Test that is_unread=True returns filled circle."""
        assert get_status_icon(True) == "●"

    def test_read_returns_empty_circle(self):
        """Test that is_unread=False returns empty circle."""
        assert get_status_icon(False) == "○"

    def test_status_icons_are_different(self):
        """Test that filled and empty circles are different."""
        unread = get_status_icon(True)
        read = get_status_icon(False)
        assert unread != read


class TestApiCallContextManager:
    """Test api_call context manager."""

    @pytest.mark.asyncio
    async def test_api_call_yields_client(self):
        """Test that api_call context manager yields the client."""
        # Create mock screen and app
        mock_client = AsyncMock()
        mock_app = MagicMock()
        mock_app.client = mock_client

        mock_screen = MagicMock()
        mock_screen.app = mock_app
        mock_screen.notify = MagicMock()
        mock_screen.log = MagicMock()

        # Use context manager
        with api_call(mock_screen, "test operation") as client:
            assert client is mock_client

    @pytest.mark.asyncio
    async def test_api_call_handles_connection_error(self):
        """Test that api_call handles ConnectionError."""
        # Create mock screen and app
        mock_client = AsyncMock()
        mock_app = MagicMock()
        mock_app.client = mock_client

        mock_screen = MagicMock()
        mock_screen.app = mock_app
        mock_screen.notify = MagicMock()
        mock_screen.log = MagicMock()

        # Test that ConnectionError is caught and handled
        error_msg = "Network failed"
        with api_call(mock_screen, "test operation") as _:
            raise ConnectionError(error_msg)

        # Verify error was logged
        mock_screen.notify.assert_called()
        assert "Connection failed" in mock_screen.notify.call_args[0][0]

    @pytest.mark.asyncio
    async def test_api_call_handles_timeout_error(self):
        """Test that api_call handles TimeoutError."""
        # Create mock screen and app
        mock_client = AsyncMock()
        mock_app = MagicMock()
        mock_app.client = mock_client

        mock_screen = MagicMock()
        mock_screen.app = mock_app
        mock_screen.notify = MagicMock()
        mock_screen.log = MagicMock()

        # Test that TimeoutError is caught and handled
        error_msg = "Request timed out"
        with api_call(mock_screen, "test operation") as _:
            raise TimeoutError(error_msg)

        # Verify error was logged
        mock_screen.notify.assert_called()
        assert "timeout" in mock_screen.notify.call_args[0][0].lower()

    @pytest.mark.asyncio
    async def test_api_call_handles_value_error(self):
        """Test that api_call handles ValueError."""
        # Create mock screen and app
        mock_client = AsyncMock()
        mock_app = MagicMock()
        mock_app.client = mock_client

        mock_screen = MagicMock()
        mock_screen.app = mock_app
        mock_screen.notify = MagicMock()
        mock_screen.log = MagicMock()

        # Test that ValueError is caught and handled
        error_msg = "Invalid input"
        with api_call(mock_screen, "test operation") as _:
            raise ValueError(error_msg)

        # Verify error was logged
        mock_screen.notify.assert_called()
        assert "Invalid input" in mock_screen.notify.call_args[0][0]

    @pytest.mark.asyncio
    async def test_api_call_handles_generic_exception(self):
        """Test that api_call handles generic Exception."""
        # Create mock screen and app
        mock_client = AsyncMock()
        mock_app = MagicMock()
        mock_app.client = mock_client

        mock_screen = MagicMock()
        mock_screen.app = mock_app
        mock_screen.notify = MagicMock()
        mock_screen.log = MagicMock()

        # Test that generic Exception is caught and handled
        error_msg = "Some error"
        try:
            with api_call(mock_screen, "test operation") as _:
                raise Exception(error_msg)
        finally:
            # Verify error was logged (generic exceptions are only logged, not notified)
            mock_screen.log.assert_called()

    @pytest.mark.asyncio
    async def test_api_call_no_client_available(self):
        """Test that api_call handles missing client by notifying user."""
        # Create mock screen without client
        mock_screen = MagicMock()
        mock_screen.app = MagicMock()
        # Don't set app.client
        if hasattr(mock_screen.app, "client"):
            delattr(mock_screen.app, "client")
        mock_screen.notify = MagicMock()

        # The context manager yields ``None`` when the client is unavailable so callers can
        # exit early without attempting API operations.
        with api_call(mock_screen, "test operation") as client:
            assert client is None

        # Verify that the user was notified
        mock_screen.notify.assert_called()
        assert "not available" in mock_screen.notify.call_args[0][0]


class TestGetAppVersion:
    """Tests for :func:`miniflux_tui.utils.get_app_version`."""

    def test_get_app_version_uses_package_metadata(self, monkeypatch):
        """Version information comes from package metadata when available."""

        # Mock git version to return None so we test metadata fallback
        monkeypatch.setattr(utils, "_get_git_version", lambda: None)
        monkeypatch.setattr(utils.metadata, "version", lambda _: "9.9.9")

        assert utils.get_app_version() == "9.9.9"

    def test_get_app_version_falls_back_to_pyproject(self, monkeypatch):
        """If metadata is missing, fall back to reading pyproject.toml."""

        # Mock git version to return None so we test pyproject fallback
        monkeypatch.setattr(utils, "_get_git_version", lambda: None)

        def raise_not_found(_: str) -> str:
            raise utils.metadata.PackageNotFoundError

        monkeypatch.setattr(utils.metadata, "version", raise_not_found)
        monkeypatch.setattr(utils.metadata, "packages_distributions", dict)

        expected_data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
        expected_version = expected_data.get("project", {}).get("version")

        assert utils.get_app_version() == expected_version

    def test_get_app_version_tries_alternative_distribution_names(self, monkeypatch):
        """Lookup falls back to alternative distributions that provide the package."""

        # Mock git version to return None so we test metadata fallback
        monkeypatch.setattr(utils, "_get_git_version", lambda: None)

        calls = []

        def fake_version(name: str) -> str:
            calls.append(name)
            if name == "miniflux-tui-py":
                raise utils.metadata.PackageNotFoundError
            if name == "alt-dist":
                return "1.2.3"
            message = f"Unexpected distribution lookup for {name}"
            raise AssertionError(message)

        monkeypatch.setattr(utils.metadata, "version", fake_version)
        monkeypatch.setattr(
            utils.metadata,
            "packages_distributions",
            lambda: {"miniflux_tui": ["alt-dist"]},
        )

        assert utils.get_app_version() == "1.2.3"
        assert calls == ["miniflux-tui-py", "alt-dist"]

    def test_get_app_version_handles_metadata_errors(self, monkeypatch):
        """Unexpected metadata errors still fall back to the file lookup."""

        # Mock git version to return None so we test metadata error fallback
        monkeypatch.setattr(utils, "_get_git_version", lambda: None)

        def raise_runtime_error(_: str) -> str:
            message = "boom"
            raise RuntimeError(message)

        monkeypatch.setattr(utils.metadata, "version", raise_runtime_error)
        monkeypatch.setattr(utils.metadata, "packages_distributions", dict)

        expected_data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
        expected_version = expected_data.get("project", {}).get("version")

        assert utils.get_app_version() == expected_version

    def test_get_app_version_recovers_from_metadata_error_with_other_candidates(self, monkeypatch):
        """Continue trying alternative distributions after metadata errors."""

        # Mock git version to return None so we test metadata error handling
        monkeypatch.setattr(utils, "_get_git_version", lambda: None)

        calls = []

        def fake_version(name: str) -> str:
            calls.append(name)
            if name == "miniflux-tui-py":
                message = "boom"
                raise RuntimeError(message)
            if name == "alt-dist":
                return "1.2.3"
            raise utils.metadata.PackageNotFoundError

        monkeypatch.setattr(utils.metadata, "version", fake_version)
        monkeypatch.setattr(
            utils.metadata,
            "packages_distributions",
            lambda: {"miniflux_tui": ["alt-dist"]},
        )
        monkeypatch.setattr(
            utils,
            "_get_version_from_pyproject",
            lambda: "from-pyproject",
            raising=False,
        )

        assert utils.get_app_version() == "1.2.3"
        assert calls == ["miniflux-tui-py", "alt-dist"]

    def test_get_app_version_returns_unknown_when_version_missing(self, monkeypatch, tmp_path):
        """Missing metadata and pyproject should return "unknown"."""

        # Mock git version to return None so we test unknown fallback
        monkeypatch.setattr(utils, "_get_git_version", lambda: None)

        def raise_not_found(_: str) -> str:
            raise utils.metadata.PackageNotFoundError

        monkeypatch.setattr(utils.metadata, "version", raise_not_found)
        monkeypatch.setattr(utils, "PYPROJECT_PATH", tmp_path / "pyproject.toml", raising=False)

        assert utils.get_app_version() == "unknown"

    def test_get_app_version_returns_git_info_when_in_repo(self, monkeypatch):
        """When running from a git repo, version shows branch/commit."""

        monkeypatch.setattr(utils, "_get_git_version", lambda: "main/abc123de")

        assert utils.get_app_version() == "main/abc123de"

    def test_get_git_version_returns_none_when_not_in_repo(self, monkeypatch):
        """_get_git_version returns None when not in a git repository."""

        # Mock the git directory check to return False
        def mock_exists(self):
            return False

        monkeypatch.setattr("pathlib.Path.exists", mock_exists)

        result = utils._get_git_version()
        assert result is None

    def test_get_git_version_returns_none_when_git_not_found(self, monkeypatch):
        """_get_git_version returns None when git executable is not found."""

        monkeypatch.setattr(utils.shutil, "which", lambda _: None)

        result = utils._get_git_version()
        assert result is None
