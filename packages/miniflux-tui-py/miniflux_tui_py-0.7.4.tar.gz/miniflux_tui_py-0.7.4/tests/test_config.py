# SPDX-License-Identifier: MIT
"""Tests for configuration management."""

# pylint: disable=protected-access

import hmac
import importlib
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

try:  # pragma: no cover - allow linting without pytest installed
    import pytest
except ImportError:  # pragma: no cover
    pytest = None  # type: ignore[assignment]

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    config_module = importlib.import_module("miniflux_tui.config")
except ImportError as exc:  # pragma: no cover
    if pytest is not None:
        pytest.skip(f"miniflux_tui.config not available: {exc}", allow_module_level=True)
    raise

Config = config_module.Config
ConfigurationError = config_module.ConfigurationError
create_default_config = config_module.create_default_config
get_config_dir = config_module.get_config_dir
get_config_file_path = config_module.get_config_file_path
load_config = config_module.load_config
validate_config = config_module.validate_config

TEST_TOKEN = "token-for-tests"  # noqa: S105 - static fixture value


class TestValidateConfig:
    """Test configuration validation."""

    def test_valid_config(self, valid_config_dict):
        """Test validation of valid configuration."""
        is_valid, msg = validate_config(valid_config_dict)
        assert is_valid
        assert msg == "Configuration valid"  # nosec: CWE-208 - Test assertion, not cryptographic comparison

    def test_missing_server_url(self, valid_config_dict):
        """Test validation fails when server_url is missing."""
        del valid_config_dict["server_url"]
        is_valid, msg = validate_config(valid_config_dict)
        assert not is_valid
        assert "server_url" in msg

    def test_missing_password_command(self, valid_config_dict):
        """Test validation fails when password command is missing."""
        del valid_config_dict["password"]
        is_valid, msg = validate_config(valid_config_dict)
        assert not is_valid
        assert "password" in msg

    def test_empty_server_url(self, valid_config_dict):
        """Test validation fails with empty server_url."""
        valid_config_dict["server_url"] = ""
        is_valid, msg = validate_config(valid_config_dict)
        assert not is_valid
        assert "non-empty" in msg.lower() or "empty" in msg.lower()  # nosec: CWE-208 - Test assertion

    def test_invalid_server_url_protocol(self, valid_config_dict):
        """Test validation fails with non-http(s) server_url."""
        valid_config_dict["server_url"] = "ftp://example.com"
        is_valid, msg = validate_config(valid_config_dict)
        assert not is_valid
        assert "http" in msg.lower()

    def test_server_url_with_http(self, valid_config_dict):
        """Test validation passes with http:// server_url."""
        valid_config_dict["server_url"] = "http://miniflux.local"
        is_valid, _ = validate_config(valid_config_dict)
        assert is_valid  # nosec: CWE-208 - Test assertion

    def test_password_command_empty_string(self, valid_config_dict):
        """Test validation fails when password command is empty string."""
        valid_config_dict["password"] = ""
        is_valid, msg = validate_config(valid_config_dict)
        assert not is_valid
        assert "command" in msg.lower()  # nosec: CWE-208 - Test assertion

    def test_password_command_empty_list(self, valid_config_dict):
        """Test validation fails when password command list is empty."""
        valid_config_dict["password"] = []
        is_valid, msg = validate_config(valid_config_dict)
        assert not is_valid
        assert "command" in msg.lower()  # nosec: CWE-208 - Test assertion

    def test_password_command_invalid_argument(self, valid_config_dict):
        """Test validation fails when command arguments are not strings."""
        valid_config_dict["password"] = ["cmd", 123]  # type: ignore[list-item]
        is_valid, msg = validate_config(valid_config_dict)
        assert not is_valid
        assert "command" in msg.lower()  # nosec: CWE-208 - Test assertion

    def test_api_key_rejected(self, valid_config_dict):
        """Test validation rejects legacy api_key field."""
        valid_config_dict["api_key"] = "legacy"
        is_valid, msg = validate_config(valid_config_dict)
        assert not is_valid
        assert "no longer supported" in msg.lower()  # nosec: CWE-208 - Test assertion

    def test_invalid_sort_mode(self, valid_config_dict):
        """Test validation fails with invalid default_sort."""
        valid_config_dict["sorting"]["default_sort"] = "invalid"
        is_valid, msg = validate_config(valid_config_dict)
        assert not is_valid
        assert "default_sort" in msg  # nosec: CWE-208 - Test assertion

    def test_valid_sort_modes(self, valid_config_dict):
        """Test validation passes with all valid sort modes."""
        for sort_mode in ["date", "feed", "status"]:
            valid_config_dict["sorting"]["default_sort"] = sort_mode
            is_valid, _ = validate_config(valid_config_dict)
            assert is_valid, f"Failed for sort mode: {sort_mode}"  # nosec: CWE-208 - Test assertion

    def test_config_without_optional_fields(self):
        """Test validation of minimal valid config."""
        config = {
            "server_url": "http://localhost:8080",
            "password": ["cmd", "arg"],
        }
        is_valid, _ = validate_config(config)
        assert is_valid


class TestConfigClass:
    """Test Config class initialization and methods."""

    def test_config_initialization(self):
        """Test Config class initialization with all parameters."""
        config = Config(
            server_url="http://localhost:8080",
            password=["command"],
            allow_invalid_certs=True,
            unread_color="blue",
            read_color="white",
            default_sort="feed",
            default_group_by_feed=True,
            group_collapsed=True,
        )
        config._api_key_cache = TEST_TOKEN

        assert config.server_url == "http://localhost:8080"  # nosec: B105 - Test data, not sensitive
        assert config.api_key == TEST_TOKEN  # nosec: B105 - Test data, not sensitive
        assert config.password_command == ("command",)  # nosec: B105 - Test data, not sensitive
        assert config.allow_invalid_certs is True
        assert config.unread_color == "blue"
        assert config.read_color == "white"
        assert config.default_sort == "feed"
        assert config.default_group_by_feed is True
        assert config.group_collapsed is True

    def test_config_initialization_defaults(self):
        """Test Config class initialization with default parameters."""
        config = Config(
            server_url="http://localhost:8080",
            password=["command"],
        )
        config._api_key_cache = TEST_TOKEN

        assert config.server_url == "http://localhost:8080"  # nosec: B105 - Test data, not sensitive
        assert config.api_key == TEST_TOKEN  # nosec: B105 - Test data, not sensitive
        assert config.password_command == ("command",)  # nosec: B105 - Test data, not sensitive
        assert config.allow_invalid_certs is False
        assert config.unread_color == "cyan"
        assert config.read_color == "gray"
        assert config.default_sort == "date"
        assert config.default_group_by_feed is False
        assert config.group_collapsed is False


class TestConfigSecretCommand:
    """Tests for password command execution."""

    def test_get_api_key_executes_command(self):
        """Command output should be returned and cached."""
        config = Config(server_url="http://localhost:8080", password=["command"])

        completed = subprocess.CompletedProcess(
            args=("command",),
            returncode=0,
            stdout=f"{TEST_TOKEN}\n",
            stderr="",
        )

        with patch("miniflux_tui.config.subprocess.run", return_value=completed) as mock_run:
            token_first = config.get_api_key()
            token_second = config.get_api_key()

        assert hmac.compare_digest(token_first, TEST_TOKEN)
        assert hmac.compare_digest(token_second, TEST_TOKEN)
        mock_run.assert_called_once_with(("command",), capture_output=True, text=True, check=True)

    def test_get_api_key_refresh_executes_again(self):
        """refresh=True should bypass the cache."""
        config = Config(server_url="http://localhost:8080", password=["command"])

        completed_one = subprocess.CompletedProcess(
            args=("command",),
            returncode=0,
            stdout="first-token\n",
            stderr="",
        )
        completed_two = subprocess.CompletedProcess(
            args=("command",),
            returncode=0,
            stdout="second-token\n",
            stderr="",
        )

        with (
            patch("miniflux_tui.config.subprocess.run", side_effect=[completed_one, completed_two]) as mock_run,
        ):
            first = config.get_api_key()
            second = config.get_api_key(refresh=True)

        assert first == "first-token"
        assert second == "second-token"
        assert mock_run.call_count == 2

    def test_get_api_key_handles_missing_executable(self):
        """Missing command should raise a RuntimeError."""
        config = Config(server_url="http://localhost:8080", password=["missing"])

        with (
            patch(
                "miniflux_tui.config.subprocess.run",
                side_effect=FileNotFoundError("No such file or directory: 'missing'"),
            ),
            pytest.raises(RuntimeError, match="Password command failed"),
        ):
            config.get_api_key()

    def test_get_api_key_handles_non_zero_exit(self):
        """Non-zero exit should raise a RuntimeError with stderr."""
        config = Config(server_url="http://localhost:8080", password=["command"])
        failure = subprocess.CalledProcessError(
            returncode=1,
            cmd=("command",),
            stderr="permission denied",
        )

        with (
            patch("miniflux_tui.config.subprocess.run", side_effect=failure),
            pytest.raises(RuntimeError, match="permission denied"),
        ):
            config.get_api_key()

    def test_get_api_key_rejects_empty_output(self):
        """Empty stdout should raise a RuntimeError."""
        config = Config(server_url="http://localhost:8080", password=["command"])
        completed = subprocess.CompletedProcess(args=("command",), returncode=0, stdout="\n", stderr="")

        with (
            patch("miniflux_tui.config.subprocess.run", return_value=completed),
            pytest.raises(RuntimeError, match="empty output"),
        ):
            config.get_api_key()

    def test_config_from_file_valid(self, tmp_path):
        """Test Config.from_file() with valid config file."""
        config_file = tmp_path / "config.toml"
        config_content = """
server_url = "http://localhost:8080"
password = ["python", "-c", "print('fake-token')"]
allow_invalid_certs = true

[theme]
unread_color = "green"
read_color = "yellow"

[sorting]
default_sort = "feed"
default_group_by_feed = true
group_collapsed = false
"""
        config_file.write_text(config_content)

        config = Config.from_file(config_file)

        assert config.server_url == "http://localhost:8080"
        assert config.password_command == (
            "python",
            "-c",
            "print('fake-token')",
        )
        assert config.allow_invalid_certs is True
        assert config.unread_color == "green"
        assert config.read_color == "yellow"
        assert config.default_sort == "feed"
        assert config.default_group_by_feed is True
        assert config.group_collapsed is False

    def test_config_from_file_minimal(self, tmp_path):
        """Test Config.from_file() with minimal config file."""
        config_file = tmp_path / "config.toml"
        config_content = """
server_url = "http://localhost:8080"
password = ["python", "-c", "print('fake-token')"]
"""
        config_file.write_text(config_content)

        config = Config.from_file(config_file)

        assert config.server_url == "http://localhost:8080"
        assert config.password_command == (
            "python",
            "-c",
            "print('fake-token')",
        )
        assert config.allow_invalid_certs is False
        assert config.unread_color == "cyan"
        assert config.read_color == "gray"

    def test_config_from_file_not_found(self, tmp_path):
        """Test Config.from_file() raises FileNotFoundError when file doesn't exist."""
        config_file = tmp_path / "nonexistent.toml"

        with pytest.raises(FileNotFoundError):
            Config.from_file(config_file)

    def test_config_from_file_invalid_content(self, tmp_path):
        """Test Config.from_file() raises ValueError for invalid config."""
        config_file = tmp_path / "config.toml"
        config_content = """
server_url = "http://localhost:8080"
password = 123
"""
        config_file.write_text(config_content)

        with pytest.raises(ConfigurationError, match="Invalid configuration"):
            Config.from_file(config_file)

    def test_config_from_file_missing_required_field(self, tmp_path):
        """Test Config.from_file() raises ValueError when required field missing."""
        config_file = tmp_path / "config.toml"
        config_content = """
server_url = "http://localhost:8080"
"""
        config_file.write_text(config_content)

        with pytest.raises(ConfigurationError, match="Invalid configuration"):
            Config.from_file(config_file)

    def test_config_from_file_missing_password_hint(self, tmp_path):
        """Missing password field should include migration guidance."""
        config_file = tmp_path / "config.toml"
        config_file.write_text('server_url = "https://example.com"\n')

        with pytest.raises(ConfigurationError) as exc_info:
            Config.from_file(config_file)

        message = str(exc_info.value)
        assert "Missing required field: password" in message
        assert "password" in message.lower()
        assert "--init" in message

    def test_config_from_file_rejects_legacy_api_key(self, tmp_path):
        """Legacy api_key field should produce actionable guidance."""
        config_file = tmp_path / "config.toml"
        config_file.write_text('server_url = "https://example.com"\napi_key = "legacy-token"\n')

        with pytest.raises(ConfigurationError) as exc_info:
            Config.from_file(config_file)

        message = str(exc_info.value)
        assert "api_key" in message
        assert "password" in message


class TestConfigDirectory:
    """Test configuration directory path functions."""

    def test_get_config_dir_darwin(self):
        """Test get_config_dir() on macOS."""
        with patch.object(sys, "platform", "darwin"):
            config_dir = get_config_dir()
            assert ".config" in str(config_dir)
            assert "miniflux-tui" in str(config_dir)

    def test_get_config_dir_win32(self):
        """Test get_config_dir() on Windows."""
        with (
            patch.object(sys, "platform", "win32"),
            patch.dict("os.environ", {"APPDATA": "C:\\Users\\test\\AppData\\Roaming"}),
        ):
            config_dir = get_config_dir()
            assert "miniflux-tui" in str(config_dir)

    def test_get_config_dir_linux_with_xdg(self):
        """Test get_config_dir() on Linux with XDG_CONFIG_HOME."""
        with (
            patch.object(sys, "platform", "linux"),
            patch.dict("os.environ", {"XDG_CONFIG_HOME": "/home/test/.config"}),
        ):
            config_dir = get_config_dir()
            assert "/home/test/.config" in str(config_dir)
            assert "miniflux-tui" in str(config_dir)

    def test_get_config_dir_linux_default(self):
        """Test get_config_dir() on Linux without XDG_CONFIG_HOME."""
        with (
            patch.object(sys, "platform", "linux"),
            patch.dict("os.environ", {}, clear=True),
        ):
            config_dir = get_config_dir()
            assert ".config" in str(config_dir)
            assert "miniflux-tui" in str(config_dir)

    def test_get_config_file_path(self):
        """Test get_config_file_path() returns correct filename."""
        config_path = get_config_file_path()
        assert config_path.name == "config.toml"
        assert "miniflux-tui" in str(config_path)


class TestCreateDefaultConfig:
    """Test default configuration creation."""

    def test_create_default_config(self, tmp_path):
        """Test create_default_config() creates file with correct content."""
        config_dir = tmp_path / "miniflux-tui"

        with patch("miniflux_tui.config.get_config_dir") as mock_get_dir:
            mock_get_dir.return_value = config_dir
            config_path = create_default_config()

            assert config_path.exists()
            assert config_path.name == "config.toml"

            content = config_path.read_text()
            assert "server_url" in content
            assert "password" in content
            assert "allow_invalid_certs" in content
            assert "[theme]" in content
            assert "[sorting]" in content

    def test_create_default_config_creates_directory(self, tmp_path):
        """Test create_default_config() creates directory if it doesn't exist."""
        config_dir = tmp_path / "does" / "not" / "exist" / "miniflux-tui"

        with patch("miniflux_tui.config.get_config_dir") as mock_get_dir:
            mock_get_dir.return_value = config_dir
            config_path = create_default_config()

            assert config_dir.exists()
            assert config_path.exists()

    def test_create_default_config_overwrites_existing(self, tmp_path):
        """Test create_default_config() overwrites existing file."""
        config_dir = tmp_path / "miniflux-tui"
        config_dir.mkdir(parents=True)
        config_path = config_dir / "config.toml"
        config_path.write_text("old content")

        with patch("miniflux_tui.config.get_config_dir") as mock_get_dir:
            mock_get_dir.return_value = config_dir
            returned_path = create_default_config()

            assert returned_path == config_path
            content = config_path.read_text()
            assert "server_url" in content
            assert "old content" not in content


class TestLoadConfig:
    """Test configuration loading."""

    def test_load_config_success(self, tmp_path):
        """Test load_config() successfully loads valid config."""
        config_dir = tmp_path / "miniflux-tui"
        config_dir.mkdir()
        config_file = config_dir / "config.toml"
        config_file.write_text("""
server_url = "http://localhost:8080"
password = ["python", "-c", "print('fake-token')"]
""")

        with patch("miniflux_tui.config.get_config_file_path") as mock_get_path:
            mock_get_path.return_value = config_file
            config = load_config()

            assert config is not None
            assert config.server_url == "http://localhost:8080"
        assert config.password_command == (
            "python",
            "-c",
            "print('fake-token')",
        )

    def test_load_config_not_found(self, tmp_path):
        """Test load_config() returns None when config doesn't exist."""
        config_path = tmp_path / "nonexistent.toml"

        with patch("miniflux_tui.config.get_config_file_path") as mock_get_path:
            mock_get_path.return_value = config_path
            config = load_config()

            assert config is None

    def test_load_config_with_all_options(self, tmp_path):
        """Test load_config() with all configuration options."""
        config_dir = tmp_path / "miniflux-tui"
        config_dir.mkdir()
        config_file = config_dir / "config.toml"
        config_file.write_text("""
server_url = "http://localhost:8080"
password = ["python", "-c", "print('fake-token')"]
allow_invalid_certs = true

[theme]
unread_color = "blue"
read_color = "red"

[sorting]
default_sort = "status"
default_group_by_feed = true
group_collapsed = true
""")

        with patch("miniflux_tui.config.get_config_file_path") as mock_get_path:
            mock_get_path.return_value = config_file
            config = load_config()

            assert config is not None
            assert config.server_url == "http://localhost:8080"
            assert config.allow_invalid_certs is True
            assert config.unread_color == "blue"
            assert config.read_color == "red"
            assert config.default_sort == "status"
            assert config.default_group_by_feed is True
            assert config.group_collapsed is True


class TestCreateCodespaceConfig:
    """Test Codespace configuration creation."""

    def test_create_codespace_config_creates_file(self, tmp_path):
        """Test create_codespace_config() creates configuration file."""
        config_dir = tmp_path / "miniflux-tui"

        with patch("miniflux_tui.config.get_config_dir") as mock_get_dir:
            mock_get_dir.return_value = config_dir
            config_path = config_module.create_codespace_config()

            assert config_path.exists()
            assert config_path == config_dir / "config.toml"

    def test_create_codespace_config_content_unix(self, tmp_path):
        """Test create_codespace_config() creates correct content on Unix."""
        config_dir = tmp_path / "miniflux-tui"

        with (
            patch("miniflux_tui.config.get_config_dir") as mock_get_dir,
            patch("miniflux_tui.config.sys.platform", "linux"),
        ):
            mock_get_dir.return_value = config_dir
            config_path = config_module.create_codespace_config()

            content = config_path.read_text()
            assert "MINIFLUX_SERVER_URL" in content
            assert "MINIFLUX_API_KEY" in content
            assert '["sh", "-c", "echo $MINIFLUX_API_KEY"]' in content
            assert "PLACEHOLDER_SET_MINIFLUX_SERVER_URL_SECRET" in content
            assert "default_group_by_feed = true" in content

    def test_create_codespace_config_content_windows(self, tmp_path):
        """Test create_codespace_config() creates correct content on Windows."""
        config_dir = tmp_path / "miniflux-tui"

        with (
            patch("miniflux_tui.config.get_config_dir") as mock_get_dir,
            patch("miniflux_tui.config.sys.platform", "win32"),
        ):
            mock_get_dir.return_value = config_dir
            config_path = config_module.create_codespace_config()

            content = config_path.read_text()
            assert '["cmd", "/c", "echo %MINIFLUX_API_KEY%"]' in content

    def test_create_codespace_config_creates_directory(self, tmp_path):
        """Test create_codespace_config() creates config directory if it doesn't exist."""
        config_dir = tmp_path / "miniflux-tui"
        assert not config_dir.exists()

        with patch("miniflux_tui.config.get_config_dir") as mock_get_dir:
            mock_get_dir.return_value = config_dir
            config_path = config_module.create_codespace_config()

            assert config_dir.exists()
            assert config_path.exists()

    def test_create_codespace_config_overwrites_existing(self, tmp_path):
        """Test create_codespace_config() overwrites existing file."""
        config_dir = tmp_path / "miniflux-tui"
        config_dir.mkdir()
        config_file = config_dir / "config.toml"
        config_file.write_text("old config")

        with patch("miniflux_tui.config.get_config_dir") as mock_get_dir:
            mock_get_dir.return_value = config_dir
            config_path = config_module.create_codespace_config()

            content = config_path.read_text()
            assert "old config" not in content
            assert "MINIFLUX_SERVER_URL" in content


class TestConfigEnvVarOverride:
    """Test environment variable override functionality."""

    def test_env_var_overrides_server_url(self, tmp_path, monkeypatch):
        """Test MINIFLUX_SERVER_URL environment variable overrides config."""
        monkeypatch.setenv("MINIFLUX_SERVER_URL", "https://env-server.com")

        config_file = tmp_path / "config.toml"
        config_file.write_text("""
server_url = "https://config-server.com"
password = ["echo", "test-token"]
""")

        config = Config.from_file(config_file)
        assert config.server_url == "https://env-server.com"

    def test_config_value_used_without_env_var(self, tmp_path, monkeypatch):
        """Test config value is used when environment variable is not set."""
        monkeypatch.delenv("MINIFLUX_SERVER_URL", raising=False)

        config_file = tmp_path / "config.toml"
        config_file.write_text("""
server_url = "https://config-server.com"
password = ["echo", "test-token"]
""")

        config = Config.from_file(config_file)
        assert config.server_url == "https://config-server.com"

    def test_placeholder_without_env_var_raises_error(self, tmp_path, monkeypatch):
        """Test placeholder in config raises error without environment variable."""
        monkeypatch.delenv("MINIFLUX_SERVER_URL", raising=False)

        config_file = tmp_path / "config.toml"
        config_file.write_text("""
server_url = "https://PLACEHOLDER_SET_MINIFLUX_SERVER_URL_SECRET"
password = ["echo", "test-token"]
""")

        with pytest.raises(ConfigurationError) as exc_info:
            Config.from_file(config_file)

        assert "placeholder" in str(exc_info.value).lower()
        assert "MINIFLUX_SERVER_URL" in str(exc_info.value)

    def test_placeholder_with_env_var_succeeds(self, tmp_path, monkeypatch):
        """Test placeholder in config works with environment variable."""
        monkeypatch.setenv("MINIFLUX_SERVER_URL", "https://env-server.com")

        config_file = tmp_path / "config.toml"
        config_file.write_text("""
server_url = "https://PLACEHOLDER_SET_MINIFLUX_SERVER_URL_SECRET"
password = ["echo", "test-token"]
""")

        config = Config.from_file(config_file)
        assert config.server_url == "https://env-server.com"

    def test_env_var_override_with_all_settings(self, tmp_path, monkeypatch):
        """Test environment variable override preserves other settings."""
        monkeypatch.setenv("MINIFLUX_SERVER_URL", "https://env-server.com")

        config_file = tmp_path / "config.toml"
        config_file.write_text("""
server_url = "https://config-server.com"
password = ["echo", "test-token"]
allow_invalid_certs = true

[theme]
unread_color = "blue"
read_color = "red"

[sorting]
default_sort = "feed"
default_group_by_feed = true
group_collapsed = true
""")

        config = Config.from_file(config_file)
        assert config.server_url == "https://env-server.com"
        assert config.allow_invalid_certs is True
        assert config.unread_color == "blue"
        assert config.read_color == "red"
        assert config.default_sort == "feed"
        assert config.default_group_by_feed is True
        assert config.group_collapsed is True
