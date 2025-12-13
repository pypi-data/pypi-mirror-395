# Usage Guide

## Starting the Application

```bash
miniflux-tui
```

The application will load your feeds and display them in the entry list.

If you installed via the container image, use:

The `latest` tag follows the default branch. Replace it with a release tag (for example `v0.4.0`) if you want to pin a specific version.

```bash
docker run --rm -it \
  -v ~/.config/miniflux-tui:/home/miniflux/.config/miniflux-tui \
  ghcr.io/reuteras/miniflux-tui:latest
```

## Main Screen Layout

The main screen is divided into three sections:

1. **Header** - Shows the application title and current view
2. **Entry List** - The main content area showing your feeds and entries
3. **Footer** - Shows available keyboard shortcuts

## Navigation

### Basic Movement

| Key | Action           |
|-----|------------------|
| `j` | Move cursor down |
| `k` | Move cursor up   |
| `↓` | Move cursor down |
| `↑` | Move cursor up   |

### Opening and Reading Entries

| Key     | Action                                                                         |
|---------|--------------------------------------------------------------------------------|
| `Enter` | Open the selected entry for reading (or first entry in feed if on feed header) |
| `J`     | Next entry (when reading)                                                      |
| `K`     | Previous entry (when reading)                                                  |

## Managing Entries

### Mark as Read/Unread

| Key | Action                                         |
|-----|------------------------------------------------|
| `m` | Toggle read/unread status of the current entry |

When you read an entry, it's automatically marked as read when you navigate away.

### Star/Unstar Entries

| Key | Action                                  |
|-----|-----------------------------------------|
| `*` | Toggle star status of the current entry |

### Save Entries

| Key | Action                                                       |
|-----|--------------------------------------------------------------|
| `e` | Save entry to a third-party service (configured in Miniflux) |

## Viewing Modes

### Sort Mode

Press `s` to cycle through sort modes:

- **Date** - Newest entries first (default)
- **Feed** - Alphabetically by feed name (A-Z), then by date within each feed (newest first)
- **Status** - Unread entries first, then by date (oldest first)

### Group by Feed

Press `g` to toggle grouping by feed. When enabled:

- Entries are grouped under their feed name
- Press `l` (or `→`) to expand a feed and see its entries
- Press `h` (or `←`) to collapse a feed

### Filter Views

| Key | Action                    |
|-----|---------------------------|
| `u` | Show only unread entries  |
| `t` | Show only starred entries |

Press again to return to all entries in the current feed list.

### Search Entries

Press `/` to open an interactive search dialog where you can enter search terms to filter entries by title or content. The search is case-insensitive and will show all matching entries.

To clear the search, press `/` again and submit an empty search term.

### Reading History

Press `Shift+H` to toggle the reading history view, which shows your 200 most recently read entries. Press `Shift+H` again to return to the main entry list.

In history view:
- All entry list keys work the same way
- Navigate with `j/k` or arrow keys
- Open entries with `Enter`
- Mark entries or toggle stars as usual

## Feed Management

### Expand/Collapse Feeds (Grouped Mode)

When in grouped mode (`g` to toggle):

| Key       | Action                                       |
|-----------|----------------------------------------------|
| `l` / `→` | Expand the highlighted feed/category         |
| `h` / `←` | Collapse the highlighted feed/category       |
| `Shift+G` | Enable grouping by feed and expand all feeds |
| `Shift+Z` | Collapse all feeds/categories                |

## Feed Settings

### Accessing Feed Settings

From the entry list, you can edit individual feed settings by pressing `X` (uppercase). This opens the Feed Settings screen where you can comprehensively configure a feed.

### Feed Configuration Sections

The Feed Settings screen is organized into several sections:

#### General Settings
- **Title** - Custom name for the feed
- **Site URL** - URL to the website the feed covers
- **Feed URL** - Read-only feed URL (for reference)
- **Category** - Organize feeds by category
- **Disabled** - Temporarily disable feed from checking

#### Network Settings
- **Feed Username** - HTTP authentication username for feed server (optional)
- **Feed Password** - HTTP authentication password for feed server (optional)
- **Override Default User Agent** - Custom User-Agent header to use for requests (optional)
- **Proxy URL** - Proxy server for feed requests (optional)
- **HTTPS Settings** - Toggle HTTPS certificate verification

#### Rules & Filtering
Configure how Miniflux processes feed content:

- **Scraper Rules** - Custom CSS selectors to extract article content
- **Rewrite Rules** - Regex patterns to modify fetched content
- **URL Rewrite Rules** - Rewrite URLs in articles
- **Blocking Rules** - Exclude articles matching patterns
- **Keep Rules** - Keep articles matching patterns (whitelist mode)

For detailed documentation on rule syntax, focus on any rule field and press `x` to open the helper screen.

#### Feed Information
- **Last Checked** - Timestamp of the last successful fetch
- **Parsing Errors** - Count of recent parsing errors
- **Error Message** - Details of the last parsing error (if any)
- **Check Interval** - Custom refresh interval in minutes (optional)
- **Feed ID** - Unique identifier for the feed

#### Danger Zone
- **Delete Feed** - Permanently delete this feed (with confirmation)

### Editing Feed Settings

#### Making Changes

When you modify any field:
- An **unsaved indicator** appears showing the number of changed fields
- Changes are **auto-saved** to a local draft every second
- Your changes are preserved even if the app closes unexpectedly

#### Keyboard Shortcuts in Feed Settings

| Key         | Action                               |
|-------------|--------------------------------------|
| `Tab`       | Move to next field                   |
| `Shift+Tab` | Move to previous field               |
| `x`         | Show help for the focused rule field |
| `Enter`     | Save all changes                     |
| `Escape`    | Cancel editing                       |

#### Saving Changes

Press `Enter` to save all changes to your Miniflux server.

- A saving indicator appears while the request is in progress
- On success, a confirmation message displays with a ✓ icon
- On error, you'll see an error message and changes stay in the draft
- Drafts are cleared only after successful save

#### Canceling Changes

Press `Escape` to cancel editing:

- First press shows a warning message
- Second press confirms and discards all changes
- If you had a recovery draft from a previous session, it's discarded too

#### Recovering Previous Changes

If the application crashes or closes while editing:
1. Open the feed settings again
2. A recovery dialog appears asking if you want to recover the previous session
3. Choose to **Recover** (restore previous changes), **Discard** (start fresh), or **Cancel** (stay in recovery mode)

### Rule Help

Each rule field has an associated help screen. To view help:
1. Focus on a rule field (Scraper, Rewrite, URL Rewrite, Blocking, or Keep Rules)
2. Press `x` to open the help screen
3. Review the rule syntax and examples
4. Press `Escape` to close the help screen

The help screen provides:
- Complete rule syntax documentation
- Common patterns and examples
- Best practices for rule creation

### Deleting a Feed

To delete a feed:
1. Navigate to the "Danger Zone" section (scroll down)
2. Press the delete button twice (first press shows confirmation)
3. The feed is permanently removed from Miniflux

## Category Management

### Accessing Category Management

Press `Shift+M` to open the category management screen where you can:

- View all categories
- Create new categories
- Edit category names
- Delete categories

### Group by Category

Press `c` to toggle grouping by category. When enabled:

- Entries are grouped under their category name
- Press `l` (or `→`) to expand a category and see its entries
- Press `h` (or `←`) to collapse a category

### Category Management Actions

In the category management screen:

| Key       | Action                                           |
|-----------|--------------------------------------------------|
| `j` / `↓` | Move cursor down                                 |
| `k` / `↑` | Move cursor up                                   |
| `n`       | Create new category                              |
| `e`       | Edit the selected category name                  |
| `d`       | Delete the selected category (with confirmation) |
| `Esc`     | Return to entry list                             |

### Organizing Feeds with Categories

You can organize your feeds into categories via the Miniflux web interface or API. Then:

1. Press `Shift+M` to open category management
2. Create categories as needed by pressing `n`
3. Assign feeds to categories through Miniflux
4. Press `c` to group entries by category in the entry list

### Category Information

When deleting a category:
- Feeds in that category will be moved to the default "Uncategorized" category
- No feeds are deleted, only reassigned

## Feed Status and Error Indicators

### Feed Error Badges

When viewing entries in grouped mode, feed headers display status information:
- **⚠ ERRORS**: Feed has parsing errors (shown in yellow)
- **⊘ DISABLED**: Feed is disabled (shown in red)
- **(Category Name)**: Category assignment shown in parentheses

This allows you to quickly identify problematic feeds without opening the status screen.

### Status Screen

For detailed feed health information and error messages:

| Key | Action                                       |
|-----|----------------------------------------------|
| `i` | Show system status with detailed feed health |

The status screen displays:
- Total feed count and health summary
- Detailed list of all problematic feeds
- Error messages and last check timestamps

## Refreshing and Syncing

There are two types of refresh operations:

### Refresh Feeds on Server

Tell the Miniflux server to fetch new content from RSS feeds:

| Key       | Action                         |
|-----------|--------------------------------|
| `r`       | Refresh current feed on server |
| `Shift+R` | Refresh all feeds on server    |

This tells the Miniflux server to check the RSS feeds for new articles. After refreshing, use `,` to sync.

### Sync Entries from Server

Fetch the latest entries from your Miniflux server to the TUI:

| Key | Action                               |
|-----|--------------------------------------|
| `,` | Sync entries from server (fetch new) |

The sync will:
1. Fetch the latest entries from your server
2. Preserve your view settings and position
3. Update the display with new/changed entries

**Non-blocking sync (v0.7.0+):**
- The sync runs in the background, so you can **continue navigating and reading entries** while it's happening
- A loading animation shows sync progress in the header
- You'll see a notification when sync completes showing what changed (e.g., "+5 new, -2 removed")
- All operations (`r`, `R`, `,`, `g+u`, `g+b`) are non-blocking and keep the UI responsive

**Typical workflow:**
1. Press `r` or `Shift+R` to tell server to refresh feeds (non-blocking)
2. Continue using the app while server fetches RSS content
3. Press `,` to sync new entries to your TUI (non-blocking)
4. Keep reading while entries sync in background

## Appearance

### Theme Toggle

Press `Shift+T` to toggle between dark and light themes:

| Key | Action                                       |
|-----|----------------------------------------------|
| `T` | Toggle theme (dark/light, applies instantly) |

- **Dark Theme** - Using Textual's built-in dark theme (default)
- **Light Theme** - Using Textual's built-in light theme

When you toggle the theme (v0.7.0+):
1. The theme changes **instantly** without requiring a restart
2. Your preference is saved to the config file
3. A notification displays the selected theme

You can also set your preferred theme in the config file:

```toml
[theme]
name = "dark"  # or "light"
```

The theme will be applied automatically when you start the application.

## Getting Help

| Key | Action                       |
|-----|------------------------------|
| `?` | Show keyboard shortcuts help |

## Quitting

| Key | Action               |
|-----|----------------------|
| `q` | Quit the application |

## Entry Reader

When you open an entry with `Enter`:

- The entry's full content is displayed in a dedicated view
- Use `J` and `K` (uppercase) to navigate to the next/previous entry in your current list
- The order follows the current sort mode and grouping
- Press `Escape` or `q` to return to the entry list

### Entry Reader Actions

In the entry reader, you can also:

| Key       | Action                             |
|-----------|------------------------------------|
| `u`       | Mark the entry as unread           |
| `*`       | Toggle star status                 |
| `e`       | Save the entry                     |
| `o`       | Open in your default browser       |
| `f`       | Fetch the original article content |
| `Shift+X` | Open scraping rule helper for feed |
| `i`       | Show system status                 |
| `Shift+S` | Show TUI settings                  |
| `?`       | Show keyboard help                 |

## Tips and Tricks

### Efficient Navigation

1. **Use grouped mode** - Press `g` to group by feed for easier organization
2. **Collapse inactive feeds** - Press `h` to hide feeds you don't want to read right now
3. **Sort by status** - Press `s` to quickly find unread entries

### Working with Many Entries

1. **Filter by status** - Use `u` for unread or `t` for starred entries
2. **Search efficiently** - Use `/` to search by title or content
3. **Refresh and sync** - Use `r` or `Shift+R` to refresh feeds on server, then `,` to sync
4. **Star for later** - Use `*` to bookmark entries for review later
5. **Review history** - Use `Shift+H` to check recently read entries

### Navigation Shortcuts

- Keep your hands on the keyboard - avoid using mouse when possible
- Use `j/k` for precise movement; arrow keys work but j/k is faster
- Use `J/K` in entry reader to quickly scan through articles

## Keyboard Shortcut Reference

Press `?` in the application to see all available shortcuts in a help screen.

## Common Workflows

### Reading Today's News

1. Start the application
2. Press `u` to see only unread entries
3. Use `j/k` to navigate, `Enter` to read
4. Use `m` to mark entries as read as you go
5. Use `*` to star important articles for later reading

### Organizing Feeds

1. Press `g` to enable grouping by feed
2. Press `h` on busy feeds you want to skip
3. Press `l` on feeds you want to catch up on
4. Navigate through visible entries with `j/k`

### Catching Up Quickly

1. Press `u` for unread only
2. Press `s` twice to sort by status (unread first)
3. Use `m` to mark entries as you review them
4. Press `s` to change sort order as needed
