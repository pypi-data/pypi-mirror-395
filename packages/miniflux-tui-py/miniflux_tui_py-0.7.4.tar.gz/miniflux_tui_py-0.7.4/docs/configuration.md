# Configuration

## Config File Format

The configuration is stored in TOML format. You can edit it manually or use `miniflux-tui --init` to set it up interactively.

## Configuration Options

### Server Settings

```toml
server_url = "https://miniflux.example.com"
password = ["op", "read", "op://Personal/Miniflux/API Token"]
allow_invalid_certs = false
```

- **server_url**: The URL of your Miniflux instance
- **password**: Command that prints your Miniflux API token (kept in your password manager)
- **allow_invalid_certs**: Set to `true` if your server uses a self-signed certificate (not recommended for production)

### Theme Settings

```toml
[theme]
name = "dark"
unread_color = "cyan"
read_color = "gray"
```

- **name**: Choose between `"dark"` or `"light"` theme (default: `"dark"`)
  - `"dark"` - Dracula-inspired dark theme with high contrast
  - `"light"` - Solarized-inspired light theme
  - Press `T` in the app to toggle between themes (applies on restart)

- **unread_color**: Color for unread entries (default: `"cyan"`)
- **read_color**: Color for read entries (default: `"gray"`)

Available colors depend on your terminal, but common options include:
- `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
- `bright_*` variants (e.g., `bright_blue`)
- `gray`, `dark_gray`

### Sorting Settings

```toml
[sorting]
default_sort = "date"
default_group_by_feed = false
group_collapsed = false
```

- **default_sort**: Default sort mode on startup
  - `"date"` - Newest entries first (default)
  - `"feed"` - Alphabetically by feed name
  - `"status"` - Unread entries first

- **default_group_by_feed**: Whether to group by feed on startup
  - `false` - Show flat list (default)
  - `true` - Show grouped by feed

- **group_collapsed**: Default expand/collapse state when toggling group modes
  - `false` - Groups start expanded (default)
  - `true` - Groups start collapsed
  - Applies to:
    - Initial startup when `default_group_by_feed = true`
    - When toggling feed grouping with `g` key
    - When toggling category grouping with `c` key
  - Tip: Set to `true` for a cleaner view with many feeds/categories

### UI Settings

```toml
[ui]
show_info_messages = true
```

- **show_info_messages**: Control information message display
  - `true` - Show all messages including info (default)
  - `false` - Show only warnings and errors

## Example Configuration

```toml
server_url = "https://miniflux.example.com"
password = ["op", "read", "op://Personal/Miniflux/API Token"]
allow_invalid_certs = false

[theme]
name = "dark"
unread_color = "cyan"
read_color = "gray"

[sorting]
default_sort = "date"
default_group_by_feed = false
group_collapsed = false

[ui]
show_info_messages = true
```

### Retrieving your API token securely

Miniflux authenticates using API tokens. To keep the token out of your config
file, store it in a password manager and configure the `password` command to
print the token to stdout.

Examples:

```toml
# 1Password CLI
password = ["op", "read", "op://Personal/Miniflux/API Token"]

# Bitwarden CLI
password = ["bw", "get", "password", "miniflux"]

# Environment variable via shell
password = ["/bin/sh", "-c", "printf %s \"$MINIFLUX_TOKEN\""]
```

Make sure the command outputs only the token with no additional text or
trailing newline (other than the typical newline printed by `printf`/`echo`).

### Using GitHub Codespaces secrets

[Codespaces secrets](https://docs.github.com/codespaces/managing-your-codespaces/managing-secrets-for-your-codespaces)
let every contributor keep their own Miniflux token private while working in a
shared repository:

1. Create a Codespaces secret (repository or personal) named `MINIFLUX_TOKEN`.
    Only Codespaces that you start can read your personal secrets.
2. Start the Codespace. The secret is exposed as the `MINIFLUX_TOKEN`
    environment variable inside the running container.
3. The repository's `.devcontainer` installs `uv` and runs `uv sync --locked --all-groups`
    automatically so the CLI and dependencies are ready for testing.
4. Configure `password` to run a shell command that echoes the variable, e.g.:

    ```toml
    password = ["/bin/sh", "-c", "printf %s \"$MINIFLUX_TOKEN\""]
    ```

Every collaborator needs to define their own secret. Secrets are scoped to the
person who created them, so they are not shared when someone else opens the
repository in Codespaces.

The Codespace automatically configures the VS Code Testing view to discover and
run the project's pytest tests. It also enables Ruff formatting on save and
points VS Code at the workspace `.venv`, so linting, formatting, and test runs
work out of the box.

## Configuration File Location

### Linux

The config file is stored in `$XDG_CONFIG_HOME` (defaults to `~/.config`):

```text
~/.config/miniflux-tui/config.toml
```

### macOS

The config file is stored in `~/.config`:

```text
~/.config/miniflux-tui/config.toml
```

### Windows

The config file is stored in `%APPDATA%`:

```text
%APPDATA%\miniflux-tui\config.toml
```

## Verifying Your Configuration

To check if your configuration is valid without launching the app:

```bash
miniflux-tui --check-config
```

## Troubleshooting

### Configuration not found

Run `miniflux-tui --init` to create a new configuration.

### Cannot connect to server

- Verify your `server_url` is correct (including `https://` or `http://`)
- Check that your Miniflux instance is accessible
- Run your password command manually to verify it outputs the expected API token

### SSL certificate errors

If you're using a self-signed certificate, set `allow_invalid_certs = true` in your config. Note: This is only recommended for local development.

### Wrong colors

Not all terminals support all colors. Try using standard colors like `cyan`, `yellow`, `blue`, etc. If colors still don't work, your terminal may not support 24-bit colors.
