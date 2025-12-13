# SPDX-License-Identifier: MIT
"""Tests for SettingsScreen."""

import re
from typing import cast
from unittest.mock import MagicMock
from urllib.parse import urlparse

from textual.app import App

from miniflux_tui.config import Config
from miniflux_tui.ui.screens.settings_management import SettingsScreen


class SettingsTestApp(App):
    """Test app for SettingsScreen testing."""

    def __init__(self, **kwargs):
        """Initialize test app."""
        super().__init__(**kwargs)
        self.config = Config(
            server_url="https://miniflux.example.com",
            password=["echo", "test-token"],
            allow_invalid_certs=False,
            unread_color="cyan",
            read_color="gray",
            default_sort="date",
            default_group_by_feed=False,
            show_info_messages=True,
        )
        self.show_info_messages = True
        self.toggle_info_messages = MagicMock()

    def on_mount(self) -> None:
        """Mount the settings screen."""
        self.push_screen(SettingsScreen())


class TestSettingsScreenInitialization:
    """Test SettingsScreen initialization."""

    def test_settings_screen_creation(self) -> None:
        """Test creating a SettingsScreen."""
        screen = SettingsScreen()
        assert screen is not None

    def test_settings_screen_has_bindings(self) -> None:
        """Test that SettingsScreen has proper key bindings."""
        screen = SettingsScreen()
        binding_keys = [binding.key for binding in screen.BINDINGS]
        assert "escape" in binding_keys
        assert "q" in binding_keys
        assert "i" in binding_keys
        # These bindings should NOT exist anymore
        assert "r" not in binding_keys  # No refresh
        assert "o" not in binding_keys  # No open web settings
        assert "e" not in binding_keys  # No edit


class TestSettingsScreenComposition:
    """Test SettingsScreen composition and rendering."""

    def test_settings_screen_css(self) -> None:
        """Test that SettingsScreen has the correct CSS."""
        screen = SettingsScreen()
        assert "overflow-y: hidden;" in screen.CSS

    async def test_screen_composes_with_header_and_footer(self) -> None:
        """Test that SettingsScreen composes with header and footer."""
        app = SettingsTestApp()

        async with app.run_test():
            screen = cast(SettingsScreen, app.screen)
            assert isinstance(screen, SettingsScreen)
            assert screen._header_widget is not None
            assert screen._footer_widget is not None
            assert screen._scroll_container is not None

    async def test_screen_has_required_widgets(self) -> None:
        """Test that SettingsScreen has all required static widgets."""
        app = SettingsTestApp()

        async with app.run_test():
            screen = cast(SettingsScreen, app.screen)
            # Should have TUI config widgets
            assert screen.query_one("#title")
            assert screen.query_one("#tui-config")
            assert screen.query_one("#config-file")


class TestSettingsScreenDisplay:
    """Test SettingsScreen display updates."""

    async def test_update_tui_config_display(self) -> None:
        """Test updating TUI configuration display."""
        app = SettingsTestApp()

        async with app.run_test():
            screen = cast(SettingsScreen, app.screen)

            tui_config = screen.query_one("#tui-config")
            content = tui_config.render().plain  # type: ignore[attr-defined]

            # Should show TUI settings
            assert "cyan" in content  # unread_color
            assert "gray" in content  # read_color
            assert "date" in content  # default_sort
            assert "Enabled" in content or "Disabled" in content  # show_info_messages

    async def test_update_config_file_display(self) -> None:
        """Test updating config file information display."""
        app = SettingsTestApp()

        async with app.run_test():
            screen = cast(SettingsScreen, app.screen)

            config_file = screen.query_one("#config-file")
            content = config_file.render().plain  # type: ignore[attr-defined]

            # Should show config file info
            assert "config.toml" in content
            # Extract and parse URL to ensure it's exactly "https://miniflux.example.com"
            # Using urlparse prevents incomplete URL substring sanitization vulnerability
            urls = re.findall(r"https?://[^\s,]+", content)
            assert any(urlparse(url).netloc == "miniflux.example.com" and urlparse(url).scheme == "https" for url in urls), (
                f"Expected to find https://miniflux.example.com in content, but found URLs: {urls}"
            )

    async def test_toggle_info_messages_updates_display(self) -> None:
        """Test that toggling info messages updates the display."""
        app = SettingsTestApp()

        async with app.run_test() as pilot:
            # Toggle info messages
            await pilot.press("i")
            await pilot.pause()

            # Verify toggle was called
            app.toggle_info_messages.assert_called_once()

            # Note: Display update depends on app.toggle_info_messages actually
            # changing app.show_info_messages, which our mock doesn't do


class TestSettingsScreenActions:
    """Test SettingsScreen actions."""

    async def test_action_close(self) -> None:
        """Test closing the settings screen."""
        app = SettingsTestApp()

        async with app.run_test() as pilot:
            screen = cast(SettingsScreen, app.screen)
            assert isinstance(screen, SettingsScreen)

            # Close the screen
            await pilot.press("escape")
            await pilot.pause()

            # Should return to previous screen
            assert app.screen is not screen

    async def test_action_close_with_q(self) -> None:
        """Test closing with 'q' key."""
        app = SettingsTestApp()

        async with app.run_test() as pilot:
            screen = cast(SettingsScreen, app.screen)
            await pilot.press("q")
            await pilot.pause()
            assert app.screen is not screen

    async def test_action_toggle_info_messages(self) -> None:
        """Test toggling info messages."""
        app = SettingsTestApp()

        async with app.run_test() as pilot:
            # Toggle info messages
            await pilot.press("i")
            await pilot.pause()

            # Should call the app's toggle function
            app.toggle_info_messages.assert_called_once()


class TestSettingsScreenErrorHandling:
    """Test SettingsScreen error handling."""

    async def test_display_without_config(self) -> None:
        """Test graceful handling when config not available."""
        app = SettingsTestApp()
        app.config = None  # type: ignore[assignment]

        async with app.run_test():
            screen = cast(SettingsScreen, app.screen)

            # Should not crash
            tui_config = screen.query_one("#tui-config")
            content = tui_config.render().plain  # type: ignore[attr-defined]
            assert "not available" in content
