# Features Overview

This page provides a comprehensive overview of all features available in miniflux-tui-py v0.7.3.

## Core Functionality

### Reading and Navigation

**Browse RSS Entries**
- Keyboard-driven navigation with Vim-style keybindings (j/k)
- Arrow key support for traditional navigation
- Fast scrolling with PageUp/PageDown in entry reader
- Navigate between entries with J/K in reader view

**Entry Management**
- Mark entries as read/unread with a single keystroke (`m`)
- Star/unstar entries to bookmark for later (`*`)
- Automatically mark entries as read when navigating away
- Save entries to third-party services like Pocket or Instapaper (`e`)

**Content Display**
- HTML to Markdown conversion for readable terminal display
- Full entry content with preserved formatting
- Metadata display: feed name, publish date, URL
- Fetch original content for truncated articles (`f`)

**Browser Integration**
- Open entries in your default web browser (`o`)
- Seamless integration with system browser

## Organization & Filtering

### Sort Modes

**Date Sort** (Default)
- Newest entries first
- Chronological ordering across all feeds
- Best for staying current with latest content

**Feed Sort**
- Alphabetical by feed name (A-Z)
- Within each feed: newest entries first
- Best for feed-by-feed reading

**Status Sort**
- Unread entries first
- Then read entries by date (oldest first)
- Best for catching up on unread content

Cycle through modes with `s` key.

### Grouping

**Group by Feed** (`g` to toggle)
- Entries organized under feed headers
- Expand/collapse individual feeds with `l`/`h`
- Expand all feeds with `Shift+G`
- Collapse all feeds with `Shift+Z`
- Visual feed status indicators (errors, disabled state)

**Group by Category** (`c` to toggle)
- Entries organized by category
- Same expand/collapse controls as feed grouping
- Category names displayed as headers
- Uncategorized feeds grouped separately

### Filtering

**Status Filters**
- `u` - Show only unread entries
- `t` - Show only starred entries
- Press again to show all entries

**Search** (`/`)
- Interactive search dialog
- Search by entry title or content
- Case-insensitive matching
- Real-time filtering as you type
- Clear search with empty query

## Feed Management

### Feed Discovery and Creation

**Auto-Discovery**
- Automatically detect RSS/Atom feeds from website URLs
- Support for multiple feed formats
- Add feeds to specific categories during creation

**Feed Creation**
- Create new feeds from URLs
- Assign to categories immediately
- Set initial configuration options

### Feed Settings

Access comprehensive feed configuration with `X` key.

**General Settings**
- Custom feed title
- Site URL
- Category assignment
- Enable/disable feed

**Network Settings**
- HTTP authentication (username/password)
- Custom User-Agent headers
- Proxy configuration
- HTTPS certificate verification

**Content Processing**
- **Scraper Rules** - CSS selectors to extract article content
- **Rewrite Rules** - Regex patterns to modify content
- **URL Rewrite Rules** - Transform URLs in articles
- **Blocking Rules** - Exclude articles by pattern (blacklist)
- **Keep Rules** - Keep only matching articles (whitelist)

**Feed Information**
- Last check timestamp
- Parsing error count
- Error messages
- Check interval customization
- Feed ID

**Danger Zone**
- Delete feed (with confirmation)

### Feed Status Monitoring

**Status Dashboard** (`i`)
- Total feed count
- Health summary
- Problematic feeds list
- Error messages and timestamps
- Server version and URL

**Visual Indicators**
- ⚠ ERRORS - Feed has parsing errors (yellow)
- ⊘ DISABLED - Feed is disabled (red)
- Category assignment in parentheses

### Feed Refresh Operations

**Current Feed Refresh** (`r`)
- Tell server to fetch new content from current feed
- Updates feed on Miniflux server
- Use `,` to sync changes to TUI

**All Feeds Refresh** (`Shift+R`)
- Tell server to refresh all feeds
- Bulk update operation
- Use `,` to sync changes to TUI

**Sync from Server** (`,`) - Non-blocking in v0.7.0+
- Fetch latest entries from Miniflux to TUI
- **Runs in background** - continue using UI while syncing
- Preserves view settings and position
- Updates display with new/changed entries
- Shows notification with change summary (+X new, -Y removed)

Typical workflow: `Shift+R` → keep reading → `,` → continue using app while syncing

## Category Management

Access with `Shift+M` key.

**Category Operations**
- Create new categories (`n`)
- Rename categories (`e`)
- Delete categories (`d` with confirmation)
- View all categories and feed counts

**Category Organization**
- Move feeds between categories via feed settings
- Organize entries by category with `c` key
- Uncategorized feeds handled automatically
- No feeds deleted when deleting categories (moved to default)

## Reading History

Access with `Shift+H` key.

**History Features**
- View 200 most recently read entries
- Same navigation and actions as main entry list
- Filter by date range
- Filter by specific feed
- Search through history
- Toggle back to main list with `Shift+H`

**History Actions**
- Open entries with `Enter`
- Mark as unread
- Toggle star status
- All standard entry operations available

## User Experience

### Theme Support

**Runtime Theme Toggle** (`Shift+T`) - v0.7.0+
- Dark theme (Textual built-in dark theme) - default
- Light theme (Textual built-in light theme)
- **Instant theme switching** - no restart required
- Preference automatically saved to config file
- Changes apply immediately to entire UI

Set in config:
```toml
[theme]
name = "dark"  # or "light"
```

### Keyboard Shortcuts

**Help Screen** (`?`)
- Complete keyboard reference
- Context-aware shortcuts
- Available in all views

**System Status** (`i`)
- Server information
- Feed health summary
- Problematic feeds list

### Security

**Password Manager Integration**
- Store API token in password manager
- Execute command to retrieve token
- No plaintext credentials in config
- Support for 1Password, Bitwarden, pass, etc.

Example:
```toml
password = ["op", "read", "op://Personal/Miniflux/API Token"]
```

**Environment Variables**
```toml
password = ["/bin/sh", "-c", "printf %s \"$MINIFLUX_TOKEN\""]
```

### Configuration

**Platform-Specific Paths**
- Linux: `~/.config/miniflux-tui/config.toml`
- macOS: `~/.config/miniflux-tui/config.toml`
- Windows: `%APPDATA%\miniflux-tui\config.toml`

**Configuration Options**
- Server URL
- API authentication
- Theme selection
- Default sort mode
- Default grouping preference
- Color customization
- SSL certificate handling

## Advanced Features

### Scraping Rule Helper

Access with `Shift+X` from entry reader or feed settings.

**Features**
- Interactive rule editor
- Syntax reference
- Common patterns and examples
- Best practices guidance
- Test rules against current entry

### Settings Management

Access with `Shift+S` key.

**User Settings**
- View global feed settings
- Edit default preferences
- Integration status
- Links to web UI for advanced settings

**Integration Support**
- View enabled integrations
- Service status
- Quick access to configuration

## Multi-Platform Support

### Supported Platforms

**Linux**
- x86_64 architecture
- All major distributions
- Wayland and X11 support

**macOS**
- arm64 (Apple Silicon)
- Intel support via Rosetta
- Terminal.app, iTerm2, Alacritty compatible

**Windows**
- x86_64 architecture
- Windows Terminal recommended
- PowerShell and Command Prompt support

### Installation Methods

- PyPI package (uv/pip)
- Prebuilt binaries
- Container images (Docker/Podman)
- From source

## Performance

**Optimization Features**
- Incremental feed sync
- Efficient entry caching
- Minimal memory footprint
- Fast startup time
- Responsive UI with async operations

**Large Feed Support**
- Handles thousands of entries
- Efficient filtering and sorting
- Background refresh operations
- Paginated history view

## Accessibility

**Keyboard-Only Operation**
- Complete functionality without mouse
- Vim-style navigation
- Consistent keybindings across views

**Visual Clarity**
- High-contrast themes
- Clear status indicators
- Error highlighting
- Feed/category badges

## Next Steps

- [Installation Guide](../installation.md) - Get started
- [Configuration](../configuration.md) - Set up your preferences
- [Usage Guide](../usage.md) - Learn keyboard shortcuts
- [Feed Settings Integration](../feed-settings-integration.md) - Configure feeds
- [Scraping Helper](scraping-helper.md) - Advanced content extraction
