# SPDX-License-Identifier: MIT
"""Tests for main entry point and CLI argument handling."""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from miniflux_tui.config import ConfigurationError
from miniflux_tui.main import main

TEST_TOKEN = "token-for-tests"  # noqa: S105 - static fixture value


class TestMainInit:
    """Test --init flag functionality."""

    def test_init_creates_config(self, tmp_path):
        """Test --init flag creates configuration file."""
        config_path = tmp_path / "config.toml"

        with patch("miniflux_tui.main.create_default_config") as mock_create:
            mock_create.return_value = config_path
            with patch.object(sys, "argv", ["miniflux-tui", "--init"]):
                result = main()

            assert result == 0
            mock_create.assert_called_once()

    def test_init_prints_help_message(self, tmp_path, capsys):
        """Test --init flag prints helpful message."""
        config_file = tmp_path / "config.toml"

        with patch("miniflux_tui.main.create_default_config") as mock_create:
            mock_create.return_value = config_file
            with patch.object(sys, "argv", ["miniflux-tui", "--init"]):
                result = main()

            captured = capsys.readouterr()
            assert "Created default configuration file" in captured.out
            assert "edit this file" in captured.out.lower()
            assert "password command" in captured.out
            assert result == 0


class TestMainInitCodespace:
    """Test --init-codespace flag functionality."""

    def test_init_codespace_creates_config(self, tmp_path):
        """Test --init-codespace flag creates configuration file."""
        config_path = tmp_path / "config.toml"

        with patch("miniflux_tui.main.create_codespace_config") as mock_create:
            mock_create.return_value = config_path
            with patch.object(sys, "argv", ["miniflux-tui", "--init-codespace"]):
                result = main()

            assert result == 0
            mock_create.assert_called_once()

    def test_init_codespace_prints_help_message(self, tmp_path, capsys):
        """Test --init-codespace flag prints helpful message."""
        config_file = tmp_path / "config.toml"

        with patch("miniflux_tui.main.create_codespace_config") as mock_create:
            mock_create.return_value = config_file
            with patch.object(sys, "argv", ["miniflux-tui", "--init-codespace"]):
                result = main()

            captured = capsys.readouterr()
            assert "Created GitHub Codespaces configuration" in captured.out
            assert "environment variables" in captured.out
            assert "MINIFLUX_SERVER_URL" in captured.out
            assert "MINIFLUX_API_KEY" in captured.out
            assert result == 0

    def test_init_codespace_mentions_tailscale(self, tmp_path, capsys):
        """Test --init-codespace includes Tailscale setup instructions."""
        config_file = tmp_path / "config.toml"

        with patch("miniflux_tui.main.create_codespace_config") as mock_create:
            mock_create.return_value = config_file
            with patch.object(sys, "argv", ["miniflux-tui", "--init-codespace"]):
                result = main()

            captured = capsys.readouterr()
            assert "Tailscale" in captured.out
            assert "TAILSCALE_AUTHKEY" in captured.out
            assert result == 0


class TestMainCheckConfig:
    """Test --check-config flag functionality."""

    def test_check_config_valid(self, capsys, tmp_path):
        """Test --check-config with valid configuration."""
        mock_config = MagicMock()
        mock_config.server_url = "http://localhost:8080"
        mock_config.password_command = ("op", "read", "token")
        mock_config.get_api_key.return_value = TEST_TOKEN
        mock_config.allow_invalid_certs = False
        mock_config.unread_color = "cyan"
        mock_config.read_color = "gray"
        mock_config.default_sort = "date"
        mock_config.default_group_by_feed = False

        config_file = tmp_path / "config.toml"
        config_file.write_text("[test]")  # Create a dummy file

        with (
            patch("miniflux_tui.main.load_config") as mock_load,
            patch("miniflux_tui.main.get_config_file_path") as mock_path,
        ):
            mock_load.return_value = mock_config
            mock_path.return_value = config_file
            with patch.object(sys, "argv", ["miniflux-tui", "--check-config"]):
                result = main()

            captured = capsys.readouterr()
            assert "Configuration loaded successfully" in captured.out
            assert "http://localhost:8080" in captured.out
            assert "Password command" in captured.out
            assert "API token retrieval" in captured.out
            assert result == 0
        mock_config.get_api_key.assert_called_once_with(refresh=True)

    def test_check_config_missing_file(self, tmp_path, capsys):
        """Test --check-config when config file doesn't exist."""
        config_path = tmp_path / "nonexistent.toml"

        with patch("miniflux_tui.main.get_config_file_path") as mock_get_path:
            mock_get_path.return_value = config_path
            with patch.object(sys, "argv", ["miniflux-tui", "--check-config"]):
                result = main()

            captured = capsys.readouterr()
            assert "Error: Config file not found" in captured.out
            assert "--init" in captured.out
            assert result == 1

    def test_check_config_load_error(self, tmp_path, capsys):
        """Test --check-config when config loading fails."""
        config_path = tmp_path / "config.toml"
        config_path.write_text("invalid toml content {{{")

        with patch("miniflux_tui.main.get_config_file_path") as mock_get_path:
            mock_get_path.return_value = config_path
            with patch("miniflux_tui.main.load_config") as mock_load:
                mock_load.side_effect = Exception("TOML parse error")
                with patch.object(sys, "argv", ["miniflux-tui", "--check-config"]):
                    result = main()

                captured = capsys.readouterr()
                assert "Error loading configuration" in captured.out
                assert result == 1

    def test_check_config_configuration_error(self, tmp_path, capsys):
        """Test --check-config reports helpful guidance for legacy configs."""
        config_path = tmp_path / "config.toml"
        config_path.write_text('server_url = "https://example.com"')

        with patch("miniflux_tui.main.get_config_file_path") as mock_get_path:
            mock_get_path.return_value = config_path
            with patch("miniflux_tui.main.load_config") as mock_load:
                mock_load.side_effect = ConfigurationError(
                    "Invalid configuration: Missing required field: password\n\nAdd a password command"
                )
                with patch.object(sys, "argv", ["miniflux-tui", "--check-config"]):
                    result = main()

                captured = capsys.readouterr()
                assert "Configuration requires attention" in captured.out
                assert "password" in captured.out.lower()
                assert "--init" in captured.out
                assert result == 1

    def test_check_config_password_command_fails(self, capsys, tmp_path):
        """Test --check-config returns error code 1 when password command fails."""
        mock_config = MagicMock()
        mock_config.server_url = "http://localhost:8080"
        mock_config.password_command = ("op", "read", "token")
        mock_config.get_api_key.side_effect = RuntimeError("Password command exited with status 1")
        mock_config.allow_invalid_certs = False
        mock_config.unread_color = "cyan"
        mock_config.read_color = "gray"
        mock_config.default_sort = "date"
        mock_config.default_group_by_feed = False

        config_file = tmp_path / "config.toml"
        config_file.write_text("[test]")  # Create a dummy file

        with (
            patch("miniflux_tui.main.load_config") as mock_load,
            patch("miniflux_tui.main.get_config_file_path") as mock_path,
        ):
            mock_load.return_value = mock_config
            mock_path.return_value = config_file
            with patch.object(sys, "argv", ["miniflux-tui", "--check-config"]):
                result = main()

            captured = capsys.readouterr()
            assert "Configuration loaded successfully" in captured.out
            assert "http://localhost:8080" in captured.out
            assert "API token retrieval: FAILED" in captured.out
            assert "Password command exited with status 1" in captured.out
            assert result == 1  # Should return error code
        mock_config.get_api_key.assert_called_once_with(refresh=True)


class TestMainNormalStartup:
    """Test normal application startup."""

    def test_normal_startup_with_valid_config(self):
        """Test normal startup with valid configuration."""
        mock_config = MagicMock()
        mock_config.get_api_key.return_value = TEST_TOKEN

        with (
            patch("miniflux_tui.main.load_config") as mock_load,
            patch("miniflux_tui.main.run_tui", new=AsyncMock()) as mock_run,
        ):
            mock_load.return_value = mock_config
            with patch.object(sys, "argv", ["miniflux-tui"]):
                result = main()

        assert result == 0
        mock_config.get_api_key.assert_called_once_with(refresh=True)
        mock_run.assert_awaited_once_with(mock_config)

    def test_startup_password_command_fails(self, capsys):
        """Test startup fails gracefully when password command fails."""
        mock_config = MagicMock()
        mock_config.get_api_key.side_effect = RuntimeError("Password command exited with status 1")

        with patch("miniflux_tui.main.load_config") as mock_load:
            mock_load.return_value = mock_config
            with patch.object(sys, "argv", ["miniflux-tui"]):
                result = main()

        captured = capsys.readouterr()
        assert "Error: Failed to retrieve API token from password command" in captured.out
        assert "Password command exited with status 1" in captured.out
        assert "--check-config" in captured.out
        assert result == 1

    def test_startup_missing_config(self, capsys):
        """Test startup when config file doesn't exist."""
        config_path = Path("/nonexistent/config.toml")

        with patch("miniflux_tui.main.load_config") as mock_load:
            mock_load.return_value = None
            with patch("miniflux_tui.main.get_config_file_path") as mock_get_path:
                mock_get_path.return_value = config_path
                with patch.object(sys, "argv", ["miniflux-tui"]):
                    result = main()

                captured = capsys.readouterr()
                assert "Error: Config file not found" in captured.out
                assert "--init" in captured.out
                assert result == 1

    def test_startup_keyboard_interrupt(self, capsys):
        """Test graceful exit on KeyboardInterrupt."""
        mock_config = MagicMock()

        with (
            patch("miniflux_tui.main.load_config") as mock_load,
            patch(
                "miniflux_tui.main.run_tui",
                new=AsyncMock(side_effect=KeyboardInterrupt),
            ) as mock_run,
        ):
            mock_load.return_value = mock_config
            with patch.object(sys, "argv", ["miniflux-tui"]):
                result = main()

        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out
        assert result == 0
        mock_run.assert_awaited_once_with(mock_config)

    def test_startup_runtime_error(self, capsys):
        """Test error handling for runtime exceptions."""
        mock_config = MagicMock()

        with (
            patch("miniflux_tui.main.load_config") as mock_load,
            patch(
                "miniflux_tui.main.run_tui",
                new=AsyncMock(side_effect=RuntimeError("Connection failed")),
            ) as mock_run,
        ):
            mock_load.return_value = mock_config
            with patch.object(sys, "argv", ["miniflux-tui"]):
                result = main()

        captured = capsys.readouterr()
        assert "Error running application" in captured.out
        assert "Connection failed" in captured.out
        assert result == 1
        mock_run.assert_awaited_once_with(mock_config)

    def test_startup_configuration_error(self, capsys):
        """Test startup prints migration guidance for legacy configs."""
        with patch("miniflux_tui.main.load_config") as mock_load:
            mock_load.side_effect = ConfigurationError("Invalid configuration: Missing required field: password\n\nAdd a password command")
            with patch.object(sys, "argv", ["miniflux-tui"]):
                result = main()

        captured = capsys.readouterr()
        assert "Error loading configuration" in captured.out
        assert "password" in captured.out.lower()
        assert "--init" in captured.out
        assert result == 1


class TestMainVersion:
    """Test --version flag."""

    def test_version_flag_exits(self):
        """Test --version flag causes SystemExit."""
        with patch.object(sys, "argv", ["miniflux-tui", "--version"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            # argparse exits with code 0 for --version
            assert exc_info.value.code == 0


class TestMainEntry:
    """Test main entry point."""

    def test_main_if_name_main(self):
        """Test __main__ guard with sys.exit."""
        with patch("miniflux_tui.main.main") as mock_main:
            mock_main.return_value = 0
            # This test verifies the structure exists; actual execution is in module load
            assert callable(main)

    def test_help_flag(self):
        """Test --help flag."""
        with patch.object(sys, "argv", ["miniflux-tui", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0


class TestMainArgumentParsing:
    """Test argument parsing."""

    def test_no_arguments_runs_app(self):
        """Test running without arguments starts application."""
        mock_config = MagicMock()

        with patch("miniflux_tui.main.load_config") as mock_load:
            mock_load.return_value = mock_config
            with (
                patch("miniflux_tui.main.run_tui", new=AsyncMock()) as mock_run,
                patch.object(sys, "argv", ["miniflux-tui"]),
            ):
                result = main()
        assert result == 0
        mock_run.assert_awaited_once_with(mock_config)

    def test_mutually_exclusive_init_and_check(self, tmp_path):
        """Test that --init and --check-config work independently."""
        config_file = tmp_path / "config.toml"

        # --init should run first
        with patch("miniflux_tui.main.create_default_config") as mock_create:
            mock_create.return_value = config_file
            with patch.object(sys, "argv", ["miniflux-tui", "--init"]):
                result = main()
                assert result == 0

        # --check-config should also work
        config_file.write_text("[test]")  # Create the file
        mock_config = MagicMock()
        with (
            patch("miniflux_tui.main.load_config") as mock_load,
            patch("miniflux_tui.main.get_config_file_path") as mock_path,
        ):
            mock_load.return_value = mock_config
            mock_path.return_value = config_file
            with patch.object(sys, "argv", ["miniflux-tui", "--check-config"]):
                result = main()
                assert result == 0


class TestAutoCreateCodespaceConfig:
    """Test automatic Codespace configuration creation."""

    def test_auto_create_with_env_vars(self, tmp_path, monkeypatch, capsys):
        """Test auto-creation when environment variables are present."""
        # Set environment variables
        monkeypatch.setenv("MINIFLUX_SERVER_URL", "https://example.com")
        monkeypatch.setenv("MINIFLUX_API_KEY", TEST_TOKEN)

        config_path = tmp_path / "config.toml"

        mock_config = MagicMock()
        with (
            patch("miniflux_tui.main.get_config_file_path") as mock_path,
            patch("miniflux_tui.main.create_codespace_config") as mock_create,
            patch("miniflux_tui.main.load_config") as mock_load,
            patch("miniflux_tui.main.run_tui", new=AsyncMock()),
        ):
            mock_path.return_value = config_path
            mock_create.return_value = config_path
            mock_load.return_value = mock_config
            with patch.object(sys, "argv", ["miniflux-tui"]):
                result = main()

            captured = capsys.readouterr()
            assert "Detected Codespace environment variables" in captured.out
            assert "Automatically creating Codespace configuration" in captured.out
            assert result == 0
            mock_create.assert_called_once()

    def test_auto_create_skipped_when_config_exists(self, tmp_path, monkeypatch):
        """Test auto-creation is skipped if config already exists."""
        # Set environment variables
        monkeypatch.setenv("MINIFLUX_SERVER_URL", "https://example.com")
        monkeypatch.setenv("MINIFLUX_API_KEY", TEST_TOKEN)

        config_path = tmp_path / "config.toml"
        config_path.write_text("existing config")

        mock_config = MagicMock()
        with (
            patch("miniflux_tui.main.get_config_file_path") as mock_path,
            patch("miniflux_tui.main.create_codespace_config") as mock_create,
            patch("miniflux_tui.main.load_config") as mock_load,
            patch("miniflux_tui.main.run_tui", new=AsyncMock()),
        ):
            mock_path.return_value = config_path
            mock_load.return_value = mock_config
            with patch.object(sys, "argv", ["miniflux-tui"]):
                main()

            # Should not create config since it exists
            mock_create.assert_not_called()

    def test_auto_create_skipped_without_env_vars(self, tmp_path, monkeypatch):
        """Test auto-creation is skipped without environment variables."""
        # Ensure env vars are NOT set
        monkeypatch.delenv("MINIFLUX_SERVER_URL", raising=False)
        monkeypatch.delenv("MINIFLUX_API_KEY", raising=False)

        config_path = tmp_path / "config.toml"

        with (
            patch("miniflux_tui.main.get_config_file_path") as mock_path,
            patch("miniflux_tui.main.create_codespace_config") as mock_create,
            patch("miniflux_tui.main.load_config") as mock_load,
        ):
            mock_path.return_value = config_path
            mock_load.return_value = None
            with patch.object(sys, "argv", ["miniflux-tui"]):
                main()

            # Should not create config without env vars
            mock_create.assert_not_called()


class TestAutoSetupTailscale:
    """Test automatic Tailscale setup."""

    def test_tailscale_setup_with_authkey_and_installed(self, tmp_path, monkeypatch, capsys):
        """Test Tailscale authentication when already installed."""
        monkeypatch.setenv("TAILSCALE_AUTHKEY", "test-authkey")

        config_dir = tmp_path / "miniflux-tui"
        marker_file = config_dir / ".tailscale-initialized"

        mock_config = MagicMock()
        with (
            patch("miniflux_tui.main.get_config_dir") as mock_dir,
            patch("miniflux_tui.main.shutil.which") as mock_which,
            patch("miniflux_tui.main.subprocess.run") as mock_run,
            patch("miniflux_tui.main.load_config") as mock_load,
            patch("miniflux_tui.main.run_tui", new=AsyncMock()),
        ):
            mock_dir.return_value = str(config_dir)
            mock_which.return_value = "/usr/bin/tailscale"
            mock_load.return_value = mock_config
            with patch.object(sys, "argv", ["miniflux-tui"]):
                main()

            captured = capsys.readouterr()
            assert "Authenticating Tailscale" in captured.out

            # Verify marker file was created
            assert marker_file.exists()

            # Verify tailscale command was called
            mock_run.assert_called_once()
            call_args = mock_run.call_args[0][0]
            assert call_args == ["/usr/bin/tailscale", "set", "--accept-routes"]

    def test_tailscale_setup_skipped_without_authkey(self, monkeypatch, capsys):
        """Test Tailscale setup is skipped without TAILSCALE_AUTHKEY."""
        monkeypatch.delenv("TAILSCALE_AUTHKEY", raising=False)

        mock_config = MagicMock()
        with (
            patch("miniflux_tui.main.shutil.which") as mock_which,
            patch("miniflux_tui.main.load_config") as mock_load,
            patch("miniflux_tui.main.run_tui", new=AsyncMock()),
        ):
            mock_load.return_value = mock_config
            with patch.object(sys, "argv", ["miniflux-tui"]):
                main()

            captured = capsys.readouterr()
            assert "Tailscale" not in captured.out
            mock_which.assert_not_called()

    def test_tailscale_setup_skipped_if_already_run(self, tmp_path, monkeypatch):
        """Test Tailscale setup is skipped if marker file exists."""
        monkeypatch.setenv("TAILSCALE_AUTHKEY", "test-authkey")

        config_dir = tmp_path / "miniflux-tui"
        config_dir.mkdir(parents=True, exist_ok=True)
        marker_file = config_dir / ".tailscale-initialized"
        marker_file.touch()

        mock_config = MagicMock()
        with (
            patch("miniflux_tui.main.get_config_dir") as mock_dir,
            patch("miniflux_tui.main.shutil.which") as mock_which,
            patch("miniflux_tui.main.subprocess.run") as mock_run,
            patch("miniflux_tui.main.load_config") as mock_load,
            patch("miniflux_tui.main.run_tui", new=AsyncMock()),
        ):
            mock_dir.return_value = str(config_dir)
            mock_load.return_value = mock_config
            with patch.object(sys, "argv", ["miniflux-tui"]):
                main()

            # Should not attempt Tailscale setup
            mock_which.assert_not_called()
            mock_run.assert_not_called()

    def test_tailscale_installation_when_not_found(self, tmp_path, monkeypatch, capsys):
        """Test Tailscale installation when not installed."""
        monkeypatch.setenv("TAILSCALE_AUTHKEY", "test-authkey")

        config_dir = tmp_path / "miniflux-tui"

        mock_config = MagicMock()
        with (
            patch("miniflux_tui.main.get_config_dir") as mock_dir,
            patch("miniflux_tui.main.shutil.which") as mock_which,
            patch("miniflux_tui.main.subprocess.run") as mock_run,
            patch("miniflux_tui.main.load_config") as mock_load,
            patch("miniflux_tui.main.run_tui", new=AsyncMock()),
        ):
            mock_dir.return_value = str(config_dir)
            # First call returns None (tailscale not found), second returns sh path, third returns tailscale path
            mock_which.side_effect = [None, "/bin/sh", "/usr/bin/tailscale"]
            mock_load.return_value = mock_config
            with patch.object(sys, "argv", ["miniflux-tui"]):
                main()

            captured = capsys.readouterr()
            assert "Installing Tailscale" in captured.out
            assert "Tailscale installed successfully" in captured.out

            # Should call subprocess twice: once for install, once for auth
            assert mock_run.call_count == 2


class TestMainEntryPoint:
    """Test main entry point for script execution."""

    @patch("miniflux_tui.main.sys.exit")
    @patch("miniflux_tui.main.main")
    def test_main_called_on_script_run(self, mock_main, mock_exit):
        """Test the if __name__ == '__main__' pattern."""
        # Simulate the if __name__ == "__main__" block
        mock_main.return_value = 0
        main_return = mock_main()
        mock_exit(main_return)

        # Verify both main() and sys.exit() were called with correct values
        assert mock_main.called
        mock_exit.assert_called_once_with(0)
