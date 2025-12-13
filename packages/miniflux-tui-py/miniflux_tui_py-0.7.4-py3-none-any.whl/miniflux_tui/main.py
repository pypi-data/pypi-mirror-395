# SPDX-License-Identifier: MIT
"""Main entry point for Miniflux TUI application."""

import argparse
import asyncio
import os
import shutil
import subprocess  # nosec B404
import sys
import traceback
from pathlib import Path

from .config import (
    Config,
    ConfigurationError,
    create_codespace_config,
    create_default_config,
    get_config_dir,
    get_config_file_path,
    load_config,
)
from .ui.app import run_tui


def _print_config_summary(config: Config) -> bool:
    """Display configuration values without revealing secrets.

    Returns:
        True if all configuration checks passed, False if validation failed.
    """
    print("Configuration loaded successfully!")
    print(f"\nServer URL: {config.server_url}")
    print("Password command: (hidden)")
    validation_passed = True
    try:
        config.get_api_key(refresh=True)
    except RuntimeError as exc:
        print(f"API token retrieval: FAILED ({exc})")
        validation_passed = False
    else:
        print("API token retrieval: success")
    print(f"Allow Invalid Certs: {config.allow_invalid_certs}")
    print("\nTheme:")
    print(f"  Unread Color: {config.unread_color}")
    print(f"  Read Color: {config.read_color}")
    print("\nSorting:")
    print(f"  Default Sort: {config.default_sort}")
    print(f"  Group by Feed: {config.default_group_by_feed}")
    return validation_passed


def _handle_init() -> int:
    """Handle the --init CLI flag."""
    config_path = create_default_config()
    print(f"Created default configuration file at: {config_path}")
    print("\nPlease edit this file and add your Miniflux server URL and password command.")
    print("The password command should retrieve your API token from a password manager.")
    return 0


def _handle_init_codespace() -> int:
    """Handle the --init-codespace CLI flag."""
    config_path = create_codespace_config()
    print(f"Created GitHub Codespaces configuration at: {config_path}")
    print("\nThis configuration reads credentials from environment variables.")
    print("\nTo use this configuration, set these secrets in GitHub:")
    print("  1. Go to your repository Settings → Secrets and variables → Codespaces")
    print("  2. Add the following secrets:")
    print("     - MINIFLUX_SERVER_URL: Your Miniflux server URL (e.g., https://miniflux.example.com)")
    print("     - MINIFLUX_API_KEY: Your Miniflux API token")
    print("\nOptional: Using Tailscale for private server access")
    print("  If your Miniflux server is on a private network:")
    print("  1. Add a Codespace secret: TAILSCALE_AUTHKEY (get from https://login.tailscale.com/admin/settings/keys)")
    print("  2. In your codespace, run:")
    print("     curl -fsSL https://tailscale.com/install.sh | sh")
    print("     sudo tailscale up --authkey=$TAILSCALE_AUTHKEY")
    print("  3. Your server will be accessible via its Tailscale hostname")
    print("  4. See https://tailscale.com/kb/1160/github-codespaces for details")
    print("\nThe TUI will start in grouped mode by default for better organization.")
    return 0


def _handle_check_config() -> int:
    """Handle the --check-config CLI flag."""
    config_path = get_config_file_path()
    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}")
        print("Run 'miniflux-tui --init' to create a default configuration.")
        return 1

    try:
        config = load_config()
    except ConfigurationError as exc:
        print("Configuration requires attention:\n")
        print(exc)
        print("\nRefer to the release notes or regenerate a template with `miniflux-tui --init`.\n")
        return 1
    except Exception as exc:
        print(f"Error loading configuration: {exc}")
        return 1

    if not config:
        print("Error: Configuration could not be loaded.")
        return 1

    validation_passed = _print_config_summary(config)
    return 0 if validation_passed else 1


def _auto_create_codespace_config() -> bool:
    """
    Automatically create Codespace config if environment variables are present.

    Returns:
        True if config was created, False otherwise
    """
    config_path = get_config_file_path()

    # Check if config already exists
    if config_path.exists():
        return False

    # Check if Codespace environment variables are present
    miniflux_server = os.environ.get("MINIFLUX_SERVER_URL")
    miniflux_api_key = os.environ.get("MINIFLUX_API_KEY")

    if miniflux_server and miniflux_api_key:
        print("Detected Codespace environment variables.")
        print("Automatically creating Codespace configuration...")
        create_codespace_config()
        print(f"✓ Configuration created at: {config_path}")
        return True

    return False


def _auto_setup_tailscale() -> None:
    """
    Automatically install and authenticate Tailscale on first startup if TAILSCALE_AUTHKEY is set.

    This function checks for a marker file to ensure it only runs once per Codespace.
    """
    # Check if Tailscale auth key is present
    if not os.environ.get("TAILSCALE_AUTHKEY"):
        return

    # Check if we've already run Tailscale setup
    config_dir = Path(get_config_dir())
    marker_file = config_dir / ".tailscale-initialized"

    if marker_file.exists():
        return

    # Check if tailscale command is available
    tailscale_path = shutil.which("tailscale")

    if not tailscale_path:
        # Tailscale not installed - install it
        print("\nDetected TAILSCALE_AUTHKEY environment variable.")
        print("Tailscale not found. Installing Tailscale...")

        # Get full path to sh for security
        sh_path = shutil.which("sh")
        if not sh_path:
            print("⚠ Shell (sh) not found. Cannot install Tailscale automatically.")
            print("Please install Tailscale manually:")
            print("  curl -fsSL https://tailscale.com/install.sh | sh")
            return

        try:
            # Download and run the Tailscale install script
            subprocess.run(  # noqa: S603 # nosec B603
                [sh_path, "-c", "curl -fsSL https://tailscale.com/install.sh | sh"],
                check=True,
                capture_output=True,
                text=True,
            )
            print("✓ Tailscale installed successfully!")

            # Get the tailscale path after installation
            tailscale_path = shutil.which("tailscale")
            if not tailscale_path:
                print("⚠ Tailscale installation completed but command not found in PATH.")
                print("You may need to restart your shell or manually authenticate:")
                print("  tailscale set --accept-routes")
                return

        except subprocess.CalledProcessError as exc:
            print(f"\n⚠ Tailscale installation failed: {exc}")
            print("You can manually install Tailscale by running:")
            print("  curl -fsSL https://tailscale.com/install.sh | sh")
            return
        except FileNotFoundError:
            print("\n⚠ Required commands not found.")
            print("Please install Tailscale manually.")
            return

    print("\nAuthenticating Tailscale for first-time setup...")
    print("Please visit the URL that appears to complete authentication.\n")

    try:
        # Run tailscale set --accept-routes (interactive authentication)
        # Using full path from shutil.which for security
        subprocess.run(  # noqa: S603 # nosec B603
            [tailscale_path, "set", "--accept-routes"],
            check=True,
        )
        print("\n✓ Tailscale authentication completed successfully!")

        # Create marker file to prevent running again
        config_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        marker_file.touch(mode=0o600)

    except subprocess.CalledProcessError as exc:
        print(f"\n⚠ Tailscale authentication failed: {exc}")
        print("You can manually authenticate later by running:")
        print("  tailscale set --accept-routes")


def _run_application() -> int:
    """Run the main TUI application."""
    # Auto-create Codespace config if environment variables are present
    _auto_create_codespace_config()

    # Auto-setup Tailscale authentication on first startup
    _auto_setup_tailscale()

    try:
        config = load_config()
    except ConfigurationError as exc:
        print("Error loading configuration:\n")
        print(exc)
        print("\nRun 'miniflux-tui --init' to create a fresh configuration template, then migrate your settings.")
        return 1
    except Exception as exc:
        print(f"Error loading configuration: {exc}")
        return 1

    if not config:
        config_path = get_config_file_path()
        print(f"Error: Config file not found at {config_path}")
        print("\nRun 'miniflux-tui --init' to create a default configuration.")
        return 1

    # Validate password command works before starting TUI
    try:
        config.get_api_key(refresh=True)
    except RuntimeError as exc:
        print("Error: Failed to retrieve API token from password command")
        print(f"Details: {exc}")
        print("\nVerify your password command is correct by running:")
        print("  miniflux-tui --check-config")
        return 1

    # Start the TUI application

    try:
        asyncio.run(run_tui(config))
        error_code = 0
    except KeyboardInterrupt:
        print("\nGoodbye!")
        error_code = 0
    except Exception as e:
        print(f"\nError running application: {e}")
        traceback.print_exc()
        error_code = 1

    return error_code


def main() -> int:
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="A Python TUI client for Miniflux RSS reader")
    parser.add_argument(
        "--init",
        action="store_true",
        help="Create a default configuration file",
    )
    parser.add_argument(
        "--init-codespace",
        action="store_true",
        help="Create a configuration file optimized for GitHub Codespaces with environment variable support",
    )
    parser.add_argument(
        "--check-config",
        action="store_true",
        help="Check configuration and display settings",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    args = parser.parse_args()

    if args.init:
        return _handle_init()
    if args.init_codespace:
        return _handle_init_codespace()
    if args.check_config:
        return _handle_check_config()
    return _run_application()


if __name__ == "__main__":
    sys.exit(main())
