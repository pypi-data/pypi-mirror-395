# Installation

## Prerequisites

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip
- A running Miniflux instance (see [miniflux.app](https://miniflux.app))

## From PyPI (Recommended with uv)

The recommended way to install miniflux-tui-py is using [uv](https://docs.astral.sh/uv/), which is faster and more reliable:

```bash
# Install uv - see https://docs.astral.sh/uv/getting-started/installation/
# On macOS/Linux: brew install uv
# On Windows: choco install uv

# Install miniflux-tui-py
uv tool install miniflux-tui-py

# Run the application
miniflux-tui
```

### Alternative: Using pip

If you prefer using pip:

```bash
pip install miniflux-tui-py
miniflux-tui
```

## Prebuilt Binaries (GitHub Releases)

Every tagged release includes standalone executables for Linux (x86_64), macOS (arm64), and Windows (x86_64). This is the easiest way to try miniflux-tui-py without installing Python.

1. Visit the [GitHub Releases](https://github.com/reuteras/miniflux-tui-py/releases) page and download the archive named `miniflux-tui-<os>-<arch>`.
2. Extract the archive into a directory of your choice.
    - Linux/macOS: `tar -xzf miniflux-tui-<os>-<arch>.tar.gz`
    - Windows: right-click the `.zip` file and choose **Extract All…**
3. (Linux/macOS) Make the binary executable if necessary: `chmod +x miniflux-tui`
4. Run the application from the extracted directory: `./miniflux-tui --init`

If macOS reports that the binary is from an unidentified developer, remove the quarantine attribute once after extraction:

```bash
xattr -d com.apple.quarantine miniflux-tui
```

## From Source (For Development)

To install from source for development:

```bash
# Clone the repository
git clone https://github.com/reuteras/miniflux-tui-py.git
cd miniflux-tui-py

# Install all dependencies (including dev and docs)
uv sync --all-groups

# Run the application
uv run miniflux-tui
```

## GitHub Codespaces

miniflux-tui-py can run in GitHub Codespaces with secure credential management via GitHub Secrets:

```bash
# Install miniflux-tui-py
pip install miniflux-tui-py

# Create a Codespaces-optimized configuration
miniflux-tui --init-codespace
```

This configuration reads credentials from environment variables (`MINIFLUX_SERVER_URL` and `MINIFLUX_API_KEY`) that you set as Codespaces secrets in your repository or user settings.

For detailed setup instructions including Tailscale support for private networks, see the [GitHub Codespaces Guide](codespaces.md).

## Container Image (Docker or Podman)

A signed container image is published to GitHub Container Registry on every push to `main` and for releases. To use it:

```bash
# Pull the image
# `latest` follows the default branch. Use a release tag (e.g. v0.4.0) to pin builds.
docker pull ghcr.io/reuteras/miniflux-tui:latest

# Create a configuration directory on the host if it does not exist
mkdir -p ~/.config/miniflux-tui

# Generate a configuration file
docker run --rm -it \
  -v ~/.config/miniflux-tui:/home/miniflux/.config/miniflux-tui \
  ghcr.io/reuteras/miniflux-tui:latest \
  --init

# Launch the TUI with the shared configuration
docker run --rm -it \
  -v ~/.config/miniflux-tui:/home/miniflux/.config/miniflux-tui \
  ghcr.io/reuteras/miniflux-tui:latest
```

The build workflow signs the image with [Sigstore Cosign](https://docs.sigstore.dev/cosign/overview/). You can verify the signature using GitHub's OIDC identity:

```bash
cosign verify ghcr.io/reuteras/miniflux-tui:latest
```

## Setup Your Configuration

Before running the application for the first time, you need to configure it:

```bash
miniflux-tui --init
```

This will create a starter configuration file in your system's config directory.
Edit the file to set your server URL and the password command that retrieves
your Miniflux API token.

### Configuration File Location

The configuration is saved to a platform-specific location:

- **Linux**: `~/.config/miniflux-tui/config.toml`
- **macOS**: `~/.config/miniflux-tui/config.toml`
- **Windows**: `%APPDATA%\miniflux-tui\config.toml`

## Getting Your Miniflux API Token Securely

1. Log in to your Miniflux instance.
2. Click on "Settings" → "API Tokens".
3. Create a new API token or copy an existing one.
4. Store the token in your password manager of choice.
5. Configure the `password` command in `config.toml` so it prints the token
    when run (for example, using 1Password's `op read` command or Bitwarden's
    `bw get password`).

## Verifying Installation

To verify your installation is working:

```bash
miniflux-tui --check-config
```

This will validate your configuration without launching the application.

## Updating

To update to the latest version:

```bash
# With uv (recommended)
uv tool upgrade miniflux-tui-py
```

Or with pip:

```bash
pip install --upgrade miniflux-tui-py
```
