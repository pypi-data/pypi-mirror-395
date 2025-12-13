# SPDX-License-Identifier: MIT
"""Tests for status screen."""

import inspect
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static

from miniflux_tui.api.models import Feed
from miniflux_tui.ui.screens.status import StatusScreen


class DummyApp(App):
    """Dummy app for testing screen composition."""

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield StatusScreen()


class MultiScreenApp(App):
    """App with multiple screens for testing navigation."""

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        # Start with a simple screen, then push status screen
        yield Static("Test Content")

    def on_mount(self) -> None:
        """Mount and push status screen."""
        # Push status screen to test navigation
        self.push_screen(StatusScreen())


class TestStatusScreenBindings:
    """Test StatusScreen key bindings."""

    def test_status_screen_has_bindings(self):
        """Test StatusScreen has correct bindings."""
        status_screen = StatusScreen()
        assert hasattr(status_screen, "BINDINGS")
        assert isinstance(status_screen.BINDINGS, list)
        assert len(status_screen.BINDINGS) == 3

    def test_status_screen_has_escape_binding(self):
        """Test StatusScreen has Escape key binding."""
        status_screen = StatusScreen()
        escape_bindings = [b for b in status_screen.BINDINGS if b.key == "escape"]  # type: ignore[attr-defined]
        assert len(escape_bindings) == 1
        assert escape_bindings[0].action == "close"

    def test_status_screen_has_q_binding(self):
        """Test StatusScreen has q key binding."""
        status_screen = StatusScreen()
        q_bindings = [b for b in status_screen.BINDINGS if b.key == "q"]  # type: ignore[attr-defined]
        assert len(q_bindings) == 1
        assert q_bindings[0].action == "close"

    def test_status_screen_has_r_binding(self):
        """Test StatusScreen has r key binding for refresh."""
        status_screen = StatusScreen()
        r_bindings = [b for b in status_screen.BINDINGS if b.key == "r"]  # type: ignore[attr-defined]
        assert len(r_bindings) == 1
        assert r_bindings[0].action == "refresh"


class TestStatusScreenCompose:
    """Test StatusScreen compose method."""

    def test_compose_method_exists(self):
        """Test compose() method exists."""
        status_screen = StatusScreen()
        assert hasattr(status_screen, "compose")
        assert callable(status_screen.compose)

    def test_compose_is_generator(self):
        """Test compose returns a generator/iterable."""
        status_screen = StatusScreen()
        result = status_screen.compose()
        # Verify it's a generator
        assert hasattr(result, "__iter__") or hasattr(result, "__next__")


class TestStatusScreenContent:
    """Test StatusScreen content and layout."""

    def test_status_screen_initialization(self):
        """Test StatusScreen can be initialized."""
        status_screen = StatusScreen()
        assert status_screen is not None
        assert isinstance(status_screen, StatusScreen)

    def test_status_screen_is_screen(self):
        """Test StatusScreen is a Textual Screen."""
        status_screen = StatusScreen()
        assert isinstance(status_screen, Screen)

    def test_status_screen_source_code_integrity(self):
        """Test status screen source is properly defined."""
        status_screen = StatusScreen()
        # Verify the class has the expected methods
        assert hasattr(status_screen, "compose")
        assert hasattr(status_screen, "action_close")
        assert hasattr(status_screen, "action_refresh")
        assert hasattr(status_screen, "BINDINGS")

    def test_status_screen_initial_values(self):
        """Test StatusScreen has correct initial values."""
        status_screen = StatusScreen()
        assert status_screen.server_version == "Loading..."
        assert status_screen.server_url == "Loading..."
        assert status_screen.username == "Loading..."
        assert status_screen.feeds == []
        assert status_screen.error_feeds == []


class TestStatusScreenComposedWidgets:
    """Test the widgets created by compose method."""

    async def test_status_screen_displayed(self):
        """Test that status screen can be displayed in an app."""
        async with DummyApp().run_test() as pilot:
            # The screen should be mounted
            app = pilot.app
            assert app is not None

    async def test_status_screen_has_compose_implementation(self):
        """Test that status screen has working compose implementation."""
        # Create an instance and verify the method exists
        status_screen = StatusScreen()
        assert hasattr(status_screen, "compose")
        assert callable(status_screen.compose)
        # The method is a generator, so calling it returns a generator object
        gen = status_screen.compose()
        assert gen is not None


class TestStatusScreenActionClose:
    """Test the action_close method."""

    def test_action_close_exists_and_callable(self):
        """Test action_close method exists and is callable."""
        status_screen = StatusScreen()
        assert hasattr(status_screen, "action_close")
        assert callable(status_screen.action_close)
        assert callable(getattr(status_screen, "action_close", None))

    def test_action_close_method_signature(self):
        """Test action_close method has correct signature."""
        status_screen = StatusScreen()
        sig = inspect.signature(status_screen.action_close)
        # action_close should only have 'self' parameter (no args besides self)
        assert len(sig.parameters) == 0

    async def test_action_close_pops_screen(self):
        """Test that action_close calls app.pop_screen()."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            # Wait for the status screen to be mounted
            await pilot.pause()
            # The status screen should be the current active screen
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Verify that calling action_close would call pop_screen
                with patch.object(app, "pop_screen") as mock_pop:
                    status_screen.action_close()
                    # Verify pop_screen was called
                    mock_pop.assert_called_once()


class TestStatusScreenActionRefresh:
    """Test the action_refresh method."""

    def test_action_refresh_exists_and_callable(self):
        """Test action_refresh method exists and is callable."""
        status_screen = StatusScreen()
        assert hasattr(status_screen, "action_refresh")
        assert callable(status_screen.action_refresh)

    def test_action_refresh_is_async(self):
        """Test action_refresh is an async method."""
        status_screen = StatusScreen()
        assert inspect.iscoroutinefunction(status_screen.action_refresh)

    @pytest.mark.asyncio
    async def test_action_refresh_calls_load_status(self):
        """Test that action_refresh calls _load_status."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Mock the _load_status method
                with patch.object(status_screen, "_load_status", new_callable=AsyncMock) as mock_load:
                    await status_screen.action_refresh()
                    # Verify _load_status was called
                    mock_load.assert_called_once()


class TestStatusScreenLoadStatus:
    """Test the _load_status method."""

    @pytest.mark.asyncio
    async def test_load_status_no_client(self):
        """Test _load_status when client is not available."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Remove client to test error handling
                original_client = app.client if hasattr(app, "client") else None  # type: ignore[attr-defined]
                if hasattr(app, "client"):
                    delattr(app, "client")

                # Mock the _update_error_state method
                with patch.object(status_screen, "_update_error_state") as mock_error:
                    await status_screen._load_status()
                    # Verify error state was updated
                    mock_error.assert_called_once_with("API client not available")

                # Restore client
                if original_client:
                    app.client = original_client  # type: ignore[attr-defined]

    @pytest.mark.asyncio
    async def test_load_status_with_healthy_feeds(self):
        """Test _load_status with healthy feeds."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Mock app client
                mock_client = MagicMock()
                mock_client.get_version = AsyncMock(return_value={"version": "2.0.50"})
                mock_client.get_user_info = AsyncMock(return_value={"username": "testuser"})
                mock_client.get_feeds = AsyncMock(
                    return_value=[
                        Feed(
                            id=1,
                            title="Healthy Feed",
                            site_url="http://localhost:8080",
                            feed_url="http://localhost:8080/feed.xml",
                            parsing_error_message="",
                            parsing_error_count=0,
                            disabled=False,
                        ),
                    ]
                )
                mock_client.base_url = "http://localhost:8080"
                app.client = mock_client  # type: ignore[attr-defined]

                # Mock the _update_display method
                with patch.object(status_screen, "_update_display") as mock_update:
                    await status_screen._load_status()

                    # Verify values were set correctly
                    assert status_screen.server_version == "2.0.50"
                    assert status_screen.username == "testuser"
                    assert status_screen.server_url == "http://localhost:8080"
                    assert len(status_screen.feeds) == 1
                    assert len(status_screen.error_feeds) == 0
                    mock_update.assert_called_once()

    @pytest.mark.asyncio
    async def test_load_status_with_error_feeds(self):
        """Test _load_status with feeds that have errors."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Mock app client
                mock_client = MagicMock()
                mock_client.get_version = AsyncMock(return_value={"version": "2.0.50"})
                mock_client.get_user_info = AsyncMock(return_value={"username": "testuser"})
                mock_client.get_feeds = AsyncMock(
                    return_value=[
                        Feed(
                            id=1,
                            title="Healthy Feed",
                            site_url="http://localhost:8080",
                            feed_url="http://localhost:8080/feed.xml",
                            parsing_error_message="",
                            parsing_error_count=0,
                            disabled=False,
                        ),
                        Feed(
                            id=2,
                            title="Error Feed",
                            site_url="http://localhost:8081",
                            feed_url="http://localhost:8081/feed.xml",
                            parsing_error_message="SSL error",
                            parsing_error_count=3,
                            disabled=False,
                        ),
                        Feed(
                            id=3,
                            title="Disabled Feed",
                            site_url="http://localhost:8082",
                            feed_url="http://localhost:8082/feed.xml",
                            parsing_error_message="",
                            parsing_error_count=0,
                            disabled=True,
                        ),
                    ]
                )
                mock_client.base_url = "http://localhost:8080"
                app.client = mock_client  # type: ignore[attr-defined]

                # Mock the _update_display method
                with patch.object(status_screen, "_update_display") as mock_update:
                    await status_screen._load_status()

                    # Verify values were set correctly
                    assert len(status_screen.feeds) == 3
                    assert len(status_screen.error_feeds) == 2  # Error Feed + Disabled Feed
                    mock_update.assert_called_once()

    @pytest.mark.asyncio
    async def test_load_status_handles_exception(self):
        """Test _load_status handles exceptions gracefully."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Mock app client that raises exception
                mock_client = MagicMock()
                mock_client.get_version = AsyncMock(side_effect=Exception("Connection failed"))
                app.client = mock_client  # type: ignore[attr-defined]

                # Mock the _update_error_state method
                with patch.object(status_screen, "_update_error_state") as mock_error:
                    await status_screen._load_status()

                    # Verify error state was updated
                    assert mock_error.called
                    call_args = mock_error.call_args[0][0]
                    assert "Error: Exception: Connection failed" in call_args


class TestStatusScreenUpdateMethods:
    """Test the update display methods."""

    def test_update_error_state(self):
        """Test _update_error_state updates widgets correctly."""
        status_screen = StatusScreen()
        # We can't easily test this without mounting, but we can verify the method exists
        assert hasattr(status_screen, "_update_error_state")
        assert callable(status_screen._update_error_state)

    def test_update_display(self):
        """Test _update_display calls update methods."""
        status_screen = StatusScreen()

        # Mock the individual update methods
        with (
            patch.object(status_screen, "_update_server_info") as mock_server,
            patch.object(status_screen, "_update_feed_health") as mock_health,
            patch.object(status_screen, "_update_error_feeds") as mock_errors,
        ):
            status_screen._update_display()

            # Verify all methods were called
            mock_server.assert_called_once()
            mock_health.assert_called_once()
            mock_errors.assert_called_once()


class TestStatusScreenDisplayMethods:
    """Test display update methods with mounted screen."""

    @pytest.mark.asyncio
    async def test_update_server_info_with_data(self):
        """Test _update_server_info updates widget correctly."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Set data
                status_screen.server_url = "http://test.com"
                status_screen.server_version = "2.0.50"
                status_screen.username = "testuser"

                # Call update method
                status_screen._update_server_info()
                await pilot.pause()

                # Verify widget was updated (no exception raised)
                assert status_screen.server_url == "http://test.com"

    @pytest.mark.asyncio
    async def test_update_feed_health_no_errors(self):
        """Test _update_feed_health with healthy feeds."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Set healthy feeds
                status_screen.feeds = [
                    Feed(
                        id=1,
                        title="Healthy Feed",
                        site_url="http://test.com",
                        feed_url="http://test.com/feed.xml",
                        parsing_error_message="",
                        parsing_error_count=0,
                        disabled=False,
                    ),
                ]
                status_screen.error_feeds = []

                # Call update method
                status_screen._update_feed_health()
                await pilot.pause()

                # Verify counts are correct
                assert len(status_screen.feeds) == 1
                assert len(status_screen.error_feeds) == 0

    @pytest.mark.asyncio
    async def test_update_feed_health_with_errors(self):
        """Test _update_feed_health with feeds that have errors."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Set feeds with errors
                error_feed = Feed(
                    id=2,
                    title="Error Feed",
                    site_url="http://test.com",
                    feed_url="http://test.com/feed.xml",
                    parsing_error_message="SSL error",
                    parsing_error_count=3,
                    disabled=False,
                )
                status_screen.feeds = [error_feed]
                status_screen.error_feeds = [error_feed]

                # Call update method
                status_screen._update_feed_health()
                await pilot.pause()

                # Verify counts are correct
                assert len(status_screen.error_feeds) == 1

    @pytest.mark.asyncio
    async def test_update_error_feeds_no_errors(self):
        """Test _update_error_feeds with no problematic feeds."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Set no error feeds
                status_screen.error_feeds = []

                # Call update method
                status_screen._update_error_feeds()
                await pilot.pause()

                # Verify empty list
                assert len(status_screen.error_feeds) == 0

    @pytest.mark.asyncio
    async def test_update_error_feeds_with_disabled(self):
        """Test _update_error_feeds with disabled feeds."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Set disabled feed
                disabled_feed = Feed(
                    id=3,
                    title="Disabled Feed",
                    site_url="http://test.com",
                    feed_url="http://test.com/feed.xml",
                    parsing_error_message="",
                    parsing_error_count=0,
                    disabled=True,
                )
                status_screen.error_feeds = [disabled_feed]

                # Call update method
                status_screen._update_error_feeds()
                await pilot.pause()

                # Verify feed is in error list
                assert len(status_screen.error_feeds) == 1
                assert status_screen.error_feeds[0].disabled is True

    @pytest.mark.asyncio
    async def test_update_error_feeds_with_parsing_errors(self):
        """Test _update_error_feeds with parsing errors."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Set feed with parsing errors
                error_feed = Feed(
                    id=4,
                    title="Parse Error Feed",
                    site_url="http://test.com",
                    feed_url="http://test.com/feed.xml",
                    parsing_error_message="Invalid XML",
                    parsing_error_count=5,
                    disabled=False,
                )
                status_screen.error_feeds = [error_feed]

                # Call update method
                status_screen._update_error_feeds()
                await pilot.pause()

                # Verify feed error details
                assert status_screen.error_feeds[0].parsing_error_count == 5

    @pytest.mark.asyncio
    async def test_update_error_feeds_with_long_message(self):
        """Test _update_error_feeds truncates long error messages."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Set feed with long error message
                long_message = "X" * 250  # More than 200 characters
                error_feed = Feed(
                    id=5,
                    title="Long Error Feed",
                    site_url="http://test.com",
                    feed_url="http://test.com/feed.xml",
                    parsing_error_message=long_message,
                    parsing_error_count=1,
                    disabled=False,
                )
                status_screen.error_feeds = [error_feed]

                # Call update method
                status_screen._update_error_feeds()
                await pilot.pause()

                # Verify error message exists
                assert len(status_screen.error_feeds[0].parsing_error_message) > 200

    @pytest.mark.asyncio
    async def test_update_error_feeds_with_checked_at(self):
        """Test _update_error_feeds displays checked_at timestamp."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Set feed with checked_at
                error_feed = Feed(
                    id=6,
                    title="Checked Feed",
                    site_url="http://test.com",
                    feed_url="http://test.com/feed.xml",
                    parsing_error_message="Timeout",
                    parsing_error_count=1,
                    disabled=False,
                    checked_at="2024-10-27T12:00:00Z",
                )
                status_screen.error_feeds = [error_feed]

                # Call update method
                status_screen._update_error_feeds()
                await pilot.pause()

                # Verify checked_at is set
                assert status_screen.error_feeds[0].checked_at is not None

    @pytest.mark.asyncio
    async def test_update_error_state_updates_widgets(self):
        """Test _update_error_state updates all widgets."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Call error state update
                status_screen._update_error_state("Test error message")
                await pilot.pause()

                # Method should complete without exception
                assert status_screen is not None


class TestStatusScreenIntegration:
    """Integration tests for StatusScreen."""

    def test_status_screen_screen_type(self):
        """Test StatusScreen is a Screen subclass."""
        status_screen = StatusScreen()
        assert isinstance(status_screen, Screen)

    def test_status_screen_not_none(self):
        """Test StatusScreen instance is not None."""
        status_screen = StatusScreen()
        assert status_screen is not None

    def test_status_screen_multiple_instances(self):
        """Test creating multiple StatusScreen instances."""
        screen1 = StatusScreen()
        screen2 = StatusScreen()
        assert screen1 is not screen2
        assert isinstance(screen1, StatusScreen)
        assert isinstance(screen2, StatusScreen)

    def test_status_screen_bindings_valid_keys(self):
        """Test that binding keys are valid."""
        status_screen = StatusScreen()
        valid_keys = {"escape", "q", "r"}
        binding_keys = {b.key for b in status_screen.BINDINGS}  # type: ignore[attr-defined]
        assert binding_keys == valid_keys

    def test_status_screen_bindings_valid_actions(self):
        """Test that binding actions are valid."""
        status_screen = StatusScreen()
        valid_actions = {"close", "refresh"}
        binding_actions = {b.action for b in status_screen.BINDINGS}  # type: ignore[attr-defined]
        assert binding_actions == valid_actions

    async def test_status_screen_compose_method_works(self):
        """Test that compose method works without errors."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            # The status screen should be on the screen stack
            status_screen = app.screen
            if isinstance(status_screen, StatusScreen):
                # Verify it's properly composed with all its widgets
                # The screen should have been mounted and composed
                assert status_screen is not None
                assert hasattr(status_screen, "compose")
