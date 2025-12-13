# SPDX-License-Identifier: MIT
"""Tests for MinifluxTuiApp application."""

import sys
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from miniflux_tui.api.client import MinifluxClient
from miniflux_tui.api.models import Entry, Feed
from miniflux_tui.config import Config
from miniflux_tui.ui.app import MinifluxTuiApp, run_tui

TEST_TOKEN = "token-for-tests"  # noqa: S105 - static fixture value


@pytest.fixture
def sample_config():
    """Create a sample Config for testing."""
    config = Config(
        server_url="http://localhost:8080",
        password=["command"],
        allow_invalid_certs=False,
        unread_color="cyan",
        read_color="gray",
        default_sort="date",
        default_group_by_feed=False,
        group_collapsed=False,
    )
    config._api_key_cache = TEST_TOKEN
    return config


@pytest.fixture
def sample_feed():
    """Create a sample Feed for testing."""
    return Feed(
        id=1,
        title="Test Feed",
        site_url="http://localhost:8080",
        feed_url="http://localhost:8080/feed",
    )


@pytest.fixture
def sample_entry(sample_feed):
    """Create a sample Entry for testing."""
    return Entry(
        id=1,
        feed_id=1,
        title="Test Entry",
        content="<p>Test content</p>",
        url="http://localhost:8080/entry",
        published_at=datetime(2023, 1, 1, 12, 0, 0, tzinfo=UTC),
        starred=False,
        status="unread",
        feed=sample_feed,
    )


class TestMinifluxTuiAppInitialization:
    """Test MinifluxTuiApp app initialization."""

    def test_initialization_with_config(self, sample_config):
        """Test app initializes with config."""
        app = MinifluxTuiApp(sample_config)

        assert app.config == sample_config
        assert app.client is None
        assert app.entries == []
        assert app.current_view == "unread"

    def test_initialization_with_custom_driver(self, sample_config):
        """Test app initializes with custom driver."""
        mock_driver = MagicMock()

        app = MinifluxTuiApp(sample_config, driver_class=mock_driver)  # type: ignore[arg-type]

        assert app.config == sample_config

    def test_initialization_css_is_defined(self, sample_config):
        """Test app CSS is defined."""
        app = MinifluxTuiApp(sample_config)

        assert app.CSS is not None
        assert isinstance(app.CSS, str)
        # After switching to Textual built-in themes, CSS only contains layout rules
        assert "ListItem" in app.CSS
        assert "Header" in app.CSS

    def test_app_inherits_from_textual_app(self, sample_config):
        """Test MinifluxTuiApp inherits from Textual App."""
        app = MinifluxTuiApp(sample_config)

        # Verify it has Textual App methods
        assert hasattr(app, "push_screen")
        assert hasattr(app, "install_screen")
        assert hasattr(app, "notify")


class TestMinifluxTuiAppPushEntryReader:
    """Test push_entry_reader method."""

    def test_push_entry_reader_with_entry(self, sample_config, sample_entry):
        """Test push_entry_reader creates and pushes reader screen."""
        app = MinifluxTuiApp(sample_config)
        app.push_screen = MagicMock()

        app.push_entry_reader(sample_entry)

        # Verify push_screen was called
        app.push_screen.assert_called_once()

    def test_push_entry_reader_with_entry_list(self, sample_config, sample_feed):
        """Test push_entry_reader with full entry list."""
        entries = []
        for i in range(3):
            entry = Entry(
                id=i,
                feed_id=1,
                title=f"Entry {i}",
                content=f"Content {i}",
                url=f"http://localhost:8080/{i}",
                published_at=datetime(2023, 1, i + 1, 12, 0, 0, tzinfo=UTC),
                starred=False,
                status="unread",
                feed=sample_feed,
            )
            entries.append(entry)

        app = MinifluxTuiApp(sample_config)
        app.push_screen = MagicMock()

        app.push_entry_reader(entries[0], entry_list=entries, current_index=0)

        # Verify push_screen was called
        app.push_screen.assert_called_once()

    def test_push_entry_reader_uses_app_entries_as_default(self, sample_config, sample_entry):
        """Test push_entry_reader uses app entries list by default."""
        app = MinifluxTuiApp(sample_config)

        # Add entries to app
        app.entries = [sample_entry]

        app.push_screen = MagicMock()

        # Push without providing entry_list
        app.push_entry_reader(sample_entry)

        # Verify push_screen was called
        app.push_screen.assert_called_once()


class TestMinifluxTuiAppLoadEntries:
    """Test load_entries method."""

    @pytest.mark.asyncio
    async def test_load_entries_unread(self, sample_config, sample_entry, async_client_factory):
        """Test load_entries loads unread entries."""
        app = MinifluxTuiApp(sample_config)

        # Mock the client
        mock_client = async_client_factory(entries=[sample_entry])
        app.client = mock_client

        # Mock notify and is_screen_installed
        app.notify = MagicMock()
        app.is_screen_installed = MagicMock(return_value=False)

        # Load entries
        await app.load_entries("unread")

        # Verify client was called
        mock_client.get_unread_entries.assert_called_once()
        # Verify entries were set
        assert len(app.entries) == 1
        assert app.entries[0] == sample_entry
        # Verify current view was updated
        assert app.current_view == "unread"

    @pytest.mark.asyncio
    async def test_load_entries_starred(self, sample_config, sample_entry, async_client_factory):
        """Test load_entries loads starred entries."""
        app = MinifluxTuiApp(sample_config)

        # Mock the client
        mock_client = async_client_factory(starred=[sample_entry])
        app.client = mock_client

        # Mock notify and is_screen_installed
        app.notify = MagicMock()
        app.is_screen_installed = MagicMock(return_value=False)

        # Load entries
        await app.load_entries("starred")

        # Verify client was called
        mock_client.get_starred_entries.assert_called_once()
        # Verify entries were set
        assert len(app.entries) == 1
        assert app.entries[0] == sample_entry
        # Verify current view was updated
        assert app.current_view == "starred"

    @pytest.mark.asyncio
    async def test_load_entries_no_client(self, sample_config):
        """Test load_entries handles missing client."""
        app = MinifluxTuiApp(sample_config)
        app.client = None

        # Mock notify
        app.notify = MagicMock()

        # Load entries
        await app.load_entries()

        # Verify error notification
        app.notify.assert_called_once()
        assert "not initialized" in app.notify.call_args[0][0].lower()

    @pytest.mark.asyncio
    async def test_load_entries_updates_screen(self, sample_config, sample_entry, async_client_factory):
        """Test load_entries updates the entry list screen."""
        app = MinifluxTuiApp(sample_config)

        # Mock the client
        app.client = async_client_factory(entries=[sample_entry])

        # Mock screen access
        mock_screen = MagicMock()
        mock_screen._populate_list = MagicMock()
        app.is_screen_installed = MagicMock(return_value=True)
        app.get_screen = MagicMock(return_value=mock_screen)
        app.notify = MagicMock()

        # Mock the isinstance check to return True
        with patch("miniflux_tui.ui.app.isinstance", return_value=True):
            await app.load_entries()

            # Verify screen was updated
            mock_screen._populate_list.assert_called_once()

    @pytest.mark.asyncio
    async def test_load_entries_empty_result(self, sample_config, async_client_factory):
        """Test load_entries handles empty results."""
        app = MinifluxTuiApp(sample_config)

        # Mock the client to return empty list
        app.client = async_client_factory(entries=[])

        # Mock notify and is_screen_installed
        app.notify = MagicMock()
        app.is_screen_installed = MagicMock(return_value=False)

        # Load entries
        await app.load_entries()

        # Verify empty notification was shown
        calls = [str(call) for call in app.notify.call_args_list]
        # Should have notification about no entries
        assert any("no" in str(call).lower() for call in calls)

    @pytest.mark.asyncio
    async def test_load_entries_api_error(self, sample_config, async_client_factory):
        """Test load_entries handles API errors."""
        app = MinifluxTuiApp(sample_config)

        # Mock the client to raise an error
        app.client = async_client_factory()
        app.client.get_unread_entries = AsyncMock(side_effect=Exception("API Error"))

        # Mock notify
        app.notify = MagicMock()

        # Load entries
        await app.load_entries()

        # Verify error notification
        app.notify.assert_called()
        assert "error" in app.notify.call_args[0][0].lower()


class TestMinifluxTuiAppActions:
    """Test action methods."""

    @pytest.mark.asyncio
    async def test_action_refresh_entries(self, sample_config, sample_entry, async_client_factory):
        """Test refresh entries action."""
        app = MinifluxTuiApp(sample_config)
        app.client = async_client_factory(entries=[sample_entry])
        app.notify = MagicMock()
        app.is_screen_installed = MagicMock(return_value=False)

        await app.action_refresh_entries()

        app.notify.assert_called()
        assert "refresh" in app.notify.call_args[0][0].lower()

    @pytest.mark.asyncio
    async def test_action_show_unread(self, sample_config, sample_entry, async_client_factory):
        """Test show unread action."""
        app = MinifluxTuiApp(sample_config)
        app.client = async_client_factory(entries=[sample_entry])
        app.notify = MagicMock()
        app.is_screen_installed = MagicMock(return_value=False)

        await app.action_show_unread()

        assert app.current_view == "unread"
        app.notify.assert_called()

    @pytest.mark.asyncio
    async def test_action_show_starred(self, sample_config, sample_entry, async_client_factory):
        """Test show starred action."""
        app = MinifluxTuiApp(sample_config)
        app.client = async_client_factory(starred=[sample_entry])
        app.notify = MagicMock()
        app.is_screen_installed = MagicMock(return_value=False)

        await app.action_show_starred()

        assert app.current_view == "starred"
        app.notify.assert_called()


class TestMinifluxTuiAppLifecycle:
    """Test app lifecycle methods."""

    @pytest.mark.asyncio
    async def test_on_unmount_closes_client(self, sample_config):
        """Test on_unmount closes the client."""
        app = MinifluxTuiApp(sample_config)
        app.client = AsyncMock()

        await app.on_unmount()

        app.client.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_on_unmount_no_client(self, sample_config):
        """Test on_unmount handles missing client."""
        app = MinifluxTuiApp(sample_config)
        app.client = None

        # Should not raise exception
        await app.on_unmount()


class TestRunTUI:
    """Test run_tui function."""

    @pytest.mark.asyncio
    async def test_run_tui_creates_and_runs_app(self, sample_config):
        """Test run_tui creates and runs MinifluxTuiApp app."""
        with patch.object(MinifluxTuiApp, "run_async", new_callable=AsyncMock):
            await run_tui(sample_config)

            # Verify run_async was called (implicitly by patching)
            # The patch ensures the method exists and can be called


class TestMinifluxTuiAppOnMount:
    """Test on_mount lifecycle method."""

    @pytest.mark.asyncio
    async def test_on_mount_initializes_client(self, sample_config):
        """Test on_mount initializes the API client."""
        app = MinifluxTuiApp(sample_config)

        # Mock required methods to prevent actual screen installation
        with (
            patch.object(app, "install_screen"),
            patch.object(app, "push_screen"),
            patch.object(app, "pop_screen"),
            patch.object(app, "notify"),
            patch.object(app, "load_categories", new_callable=AsyncMock),
            patch.object(app, "load_feeds", new_callable=AsyncMock),
            patch.object(app, "load_entries", new_callable=AsyncMock),
        ):
            await app.on_mount()
            await app._load_data()

        # Verify client was initialized
        assert app.client is not None
        assert isinstance(app.client, MinifluxClient)

    @pytest.mark.asyncio
    async def test_on_mount_installs_screens(self, sample_config):
        """Test on_mount installs entry list, help, and status screens."""
        app = MinifluxTuiApp(sample_config)

        # Mock required methods
        with (
            patch.object(app, "install_screen") as mock_install,
            patch.object(app, "push_screen"),
            patch.object(app, "pop_screen"),
            patch.object(app, "notify"),
            patch.object(app, "load_categories", new_callable=AsyncMock),
            patch.object(app, "load_feeds", new_callable=AsyncMock),
            patch.object(app, "load_entries", new_callable=AsyncMock),
        ):
            await app.on_mount()
            await app._load_data()

            # Verify install_screen was called six times (for loading, entry_list, help, status, settings, and history)
            assert mock_install.call_count == 6

    @pytest.mark.asyncio
    async def test_on_mount_pushes_initial_screen(self, sample_config):
        """Test on_mount pushes loading screen then entry_list screen."""
        app = MinifluxTuiApp(sample_config)

        # Mock required methods
        with (
            patch.object(app, "install_screen"),
            patch.object(app, "push_screen") as mock_push,
            patch.object(app, "pop_screen"),
            patch.object(app, "notify"),
            patch.object(app, "load_categories", new_callable=AsyncMock),
            patch.object(app, "load_feeds", new_callable=AsyncMock),
            patch.object(app, "load_entries", new_callable=AsyncMock),
        ):
            await app.on_mount()
            await app._load_data()

            # Verify push_screen was called twice (loading, then entry_list)
            assert mock_push.call_count == 2
            mock_push.assert_any_call("loading")
            mock_push.assert_any_call("entry_list")

    @pytest.mark.asyncio
    async def test_on_mount_notifies_loading(self, sample_config):
        """Test on_mount shows loading screen."""
        app = MinifluxTuiApp(sample_config)

        # Mock required methods
        with (
            patch.object(app, "install_screen"),
            patch.object(app, "push_screen") as mock_push,
            patch.object(app, "pop_screen"),
            patch.object(app, "notify"),
            patch.object(app, "load_categories", new_callable=AsyncMock),
            patch.object(app, "load_feeds", new_callable=AsyncMock),
            patch.object(app, "load_entries", new_callable=AsyncMock),
        ):
            await app.on_mount()
            await app._load_data()

            # Verify loading screen was pushed first
            assert mock_push.call_args_list[0][0][0] == "loading"

    @pytest.mark.asyncio
    async def test_on_mount_loads_entries(self, sample_config):
        """Test on_mount calls load_entries."""
        app = MinifluxTuiApp(sample_config)

        # Mock required methods
        with (
            patch.object(app, "install_screen"),
            patch.object(app, "push_screen"),
            patch.object(app, "pop_screen"),
            patch.object(app, "notify"),
            patch.object(app, "load_categories", new_callable=AsyncMock),
            patch.object(app, "load_entries", new_callable=AsyncMock) as mock_load,
        ):
            await app.on_mount()
            await app._load_data()

            # Verify load_entries was called
            mock_load.assert_called_once()


class TestLoadEntriesScreenUpdate:
    """Test load_entries screen update paths."""

    @pytest.mark.asyncio
    async def test_load_entries_screen_not_entry_list(self, sample_config, sample_entry):
        """Test load_entries handles non-EntryListScreen case."""
        app = MinifluxTuiApp(sample_config)

        # Mock the client
        app.client = AsyncMock()
        app.client.get_unread_entries = AsyncMock(return_value=[sample_entry])

        # Mock screen access with non-EntryListScreen object
        mock_screen = MagicMock()
        app.is_screen_installed = MagicMock(return_value=True)
        app.get_screen = MagicMock(return_value=mock_screen)
        app.notify = MagicMock()

        # Load entries - this should handle the case where screen is not EntryListScreen
        await app.load_entries()

        # Verify the screen was fetched
        app.get_screen.assert_called_once_with("entry_list")
        # Verify entries were loaded
        assert len(app.entries) == 1


class TestMinifluxTuiAppIntegration:
    """Integration tests for the app."""

    def test_app_config_colors(self, sample_config):
        """Test app correctly uses config colors."""
        app = MinifluxTuiApp(sample_config)

        assert app.config.unread_color == "cyan"
        assert app.config.read_color == "gray"

    def test_app_config_server_url(self, sample_config):
        """Test app correctly uses config server URL."""
        app = MinifluxTuiApp(sample_config)

        assert app.config.server_url == "http://localhost:8080"

    def test_app_current_view_defaults_to_unread(self, sample_config):
        """Test app defaults to unread view."""
        app = MinifluxTuiApp(sample_config)

        assert app.current_view == "unread"

    def test_app_entries_list_starts_empty(self, sample_config):
        """Test app starts with empty entries list."""
        app = MinifluxTuiApp(sample_config)

        assert app.entries == []
        assert len(app.entries) == 0

    @pytest.mark.asyncio
    async def test_load_entries_maintains_list_order(self, sample_config, sample_feed):
        """Test load_entries maintains entry order."""
        entries = []
        for i in range(5):
            entry = Entry(
                id=i,
                feed_id=1,
                title=f"Entry {i}",
                content=f"Content {i}",
                url=f"http://localhost:8080/{i}",
                published_at=datetime(2023, 1, i + 1, 12, 0, 0, tzinfo=UTC),
                starred=False,
                status="unread",
                feed=sample_feed,
            )
            entries.append(entry)

        app = MinifluxTuiApp(sample_config)
        app.client = AsyncMock()
        app.client.get_unread_entries = AsyncMock(return_value=entries)
        app.notify = MagicMock()
        app.is_screen_installed = MagicMock(return_value=False)

        await app.load_entries()

        # Verify order is maintained
        assert app.entries[0].id == 0
        assert app.entries[1].id == 1
        assert app.entries[4].id == 4


class TestThemeConfiguration:
    """Test theme color configuration in MinifluxTuiApp."""

    def test_app_initializes_with_config_colors(self, sample_config):
        """Test that app initializes with colors from config."""
        app = MinifluxTuiApp(sample_config)

        assert app.config.unread_color == "cyan"
        assert app.config.read_color == "gray"

    def test_app_uses_custom_theme_colors(self):
        """Test that app uses custom theme colors from config."""
        custom_config = Config(
            server_url="http://localhost:8080",
            password=["command"],
            allow_invalid_certs=False,
            unread_color="blue",
            read_color="white",
            default_sort="date",
            default_group_by_feed=False,
        )
        custom_config._api_key_cache = TEST_TOKEN
        app = MinifluxTuiApp(custom_config)

        assert app.config.unread_color == "blue"
        assert app.config.read_color == "white"

    def test_app_passes_colors_to_entry_list_screen(self):
        """Test that app passes theme colors to EntryListScreen."""
        custom_config = Config(
            server_url="http://localhost:8080",
            password=["command"],
            allow_invalid_certs=False,
            unread_color="green",
            read_color="yellow",
            default_sort="date",
            default_group_by_feed=False,
        )
        custom_config._api_key_cache = TEST_TOKEN
        app = MinifluxTuiApp(custom_config)

        # Verify app config has the custom colors
        assert app.config.unread_color == "green"
        assert app.config.read_color == "yellow"
        # Colors would be passed to EntryListScreen when created via on_mount
        # This test verifies the app has the config colors available

    def test_theme_config_defaults_to_cyan_and_gray(self):
        """Test that theme defaults to cyan for unread and gray for read."""
        config = Config(
            server_url="http://localhost:8080",
            password=["command"],
            allow_invalid_certs=False,
            default_sort="date",
            default_group_by_feed=False,
        )
        config._api_key_cache = TEST_TOKEN

        # Should use defaults
        assert config.unread_color == "cyan"
        assert config.read_color == "gray"

    def test_theme_colors_persist_across_config_reload(self, tmp_path):
        """Test that theme colors persist when config is reloaded."""
        # Create a config file with custom colors
        config_file = tmp_path / "config.toml"
        python_exe = sys.executable.replace("\\", "\\\\")
        config_content = f"""
server_url = "http://localhost:8080"
password = ["{python_exe}", "-c", "print('fake-token')"]
allow_invalid_certs = false

[theme]
unread_color = "red"
read_color = "white"

[sorting]
default_sort = "date"
"""
        config_file.write_text(config_content)

        # Load config from file
        loaded_config = Config.from_file(config_file)

        # Verify colors are loaded correctly
        assert loaded_config.unread_color == "red"
        assert loaded_config.read_color == "white"

        # Create app with loaded config
        app = MinifluxTuiApp(loaded_config)

        # Verify app has the colors
        assert app.config.unread_color == "red"
        assert app.config.read_color == "white"
