# Architecture Guide

This guide explains the overall structure and design patterns used in miniflux-tui-py.

## High-Level Overview

```text
┌─────────────────────────────────────────────────────────┐
│                    User (Terminal)                       │
└────────────────────┬────────────────────────────────────┘
  │
┌────────────────────▼────────────────────────────────────┐
│              MinifluxTuiApp (Textual App)                  │
│  - Screen Management (push/pop)                         │
│  - Event Handling                                       │
│  - Client Initialization                               │
└─┬──────────────────┬────────────────────────┬──────────┘
  │                  │                        │
  ▼                  ▼                        ▼
┌──────────────┐ ┌────────────────┐ ┌──────────────────┐
│ EntryList    │ │ EntryReader    │ │ HelpScreen       │
│ Screen       │ │ Screen         │ │                  │
│              │ │                │ │ (Static Content) │
│ - Sorting    │ │ - Display      │ │                  │
│ - Grouping   │ │ - Navigation   │ │ 100% coverage ✓  │
│ - Filtering  │ │ - HTML->MD     │ │                  │
│ - UI Updates │ │                │ │                  │
└──────────────┘ └────────────────┘ └──────────────────┘
  │                  │
  └──────────────────┴──────────┬──────────────────────┐
  │                      │
  ┌───────▼────────┐    ┌────────▼─────┐
  │ MinifluxClient │    │ Config/Utils │
  │ (Async API)    │    │              │
  └───────┬────────┘    └──────────────┘
  │
  ┌───────▼────────────┐
  │ Miniflux Server    │
  │ (Remote RSS Reader)│
  └────────────────────┘
```text

## Directory Structure

```bash
miniflux_tui/
├── __init__.py               # Package initialization
├── main.py                   # CLI entry point & argument parsing
├── config.py                 # Configuration loading/saving (100% coverage)
├── constants.py              # Application constants (100% coverage)
├── performance.py            # Performance utilities (100% coverage)
├── utils.py                  # Helper functions (100% coverage)
│
├── api/
│   ├── __init__.py
│   ├── client.py            # Async Miniflux API wrapper (100% coverage)
│   └── models.py            # Entry, Feed dataclasses (100% coverage)
│
└── ui/
  ├── __init__.py
  ├── app.py               # Main Textual app (100% coverage)
  └── screens/
  ├── __init__.py
  ├── entry_list.py    # Entry list with sorting/grouping (64% coverage)
  ├── entry_reader.py  # Entry detail view (56% coverage)
  └── help.py          # Help/shortcuts screen (100% coverage)
```text

## Core Components

### 1. Main Entry Point (main.py)

Responsibilities:
- Parse CLI arguments (`--init`, `--check-config`, `--version`)
- Load configuration
- Initialize and run the TUI app
- Handle exceptions gracefully

```python
# Usage
def main() -> int:
  if args.init:
  create_default_config()
  elif args.check_config:
  validate_config()
  else:
  asyncio.run(run_tui(config))
  return 0
```text

### 2. Configuration (config.py)

Responsibilities:
- Load/save TOML config files
- Support platform-specific paths (Linux, macOS, Windows)
- Provide sensible defaults
- Validate configuration

```bash
~/.config/miniflux-tui/config.toml  (Linux, XDG)
~/.config/miniflux-tui/config.toml  (macOS)
%APPDATA%\miniflux-tui\config.toml  (Windows)
```text

### 3. API Client (api/client.py)

Responsibilities:
- Async wrapper around Miniflux API
- Convert sync library calls to async (run_in_executor)
- Handle retries and errors
- Return typed data models

```python
class MinifluxClient:
  async def get_unread_entries(limit: int) -> list[Entry]
  async def get_starred_entries(limit: int) -> list[Entry]
  async def mark_as_read(entry_id: int) -> None
  async def toggle_star(entry_id: int) -> None
  async def save_entry(entry_id: int) -> None
```text

### 4. Main App (ui/app.py)

Responsibilities:
- Manage screens (entry_list, entry_reader, help)
- Initialize API client
- Load entries from API
- Handle async operations
- Manage app state

```python
class MinifluxTuiApp(App):
  async def on_mount() -> None:
  # Install screens and load initial data

  async def load_entries(view: str) -> None:
  # Fetch entries from API and update screen

  def push_entry_reader(entry, entry_list, index) -> None:
  # Open entry detail view
```text

### 5. Entry List Screen (ui/screens/entry_list.py)

Responsibilities:
- Display list of entries
- Handle sorting (date, feed, status)
- Handle grouping by feed
- Handle filtering (unread, starred)
- Navigate with j/k keys
- Toggle read/starred status
- Manage cursor position

**Key Features:**
- **Sorting Modes**: date (newest first), feed (alpha + date), status (unread first)
- **Grouping**: Group entries by feed title with expand/collapse
- **Filtering**: Show only unread OR only starred
- **Navigation**: j/k keys navigate, skipping hidden items in grouped mode
- **State Persistence**: Remember cursor position when returning from entry reader

```python
class EntryListScreen(Screen):
  # Sorting
  action_cycle_sort()
  _sort_entries()

  # Grouping
  action_toggle_group()
  action_collapse_feed()
  action_expand_feed()

  # Filtering
  action_show_unread()
  action_show_starred()

  # Navigation
  action_cursor_down()
  action_cursor_up()
```text

### 6. Entry Reader Screen (ui/screens/entry_reader.py)

Responsibilities:
- Display full entry content
- Convert HTML to Markdown
- Navigate between entries (J/K keys)
- Mark as read/unread
- Toggle starred status
- Open in browser
- Return to list

```python
class EntryReaderScreen(Screen):
  async def on_mount() -> None:
  # Display entry content

  def action_next_entry() -> None:
  # Navigate to next entry

  def action_previous_entry() -> None:
  # Navigate to previous entry

  async def action_toggle_read() -> None:
  # Mark entry read/unread
```text

### 7. Help Screen (ui/screens/help.py)

Responsibilities:
- Display keyboard shortcuts
- Static content (100% coverage)
- Close with 'q' or Escape

## Design Patterns

### 1. Async/Await for API Calls

All API interactions are async:

```python
# In async action method
async def action_toggle_read(self):
  if hasattr(self.app, 'client') and self.app.client:
  await self.app.client.mark_as_read(self.entry.id)
  self.entry.status = "read"
  self._refresh_display()
```text

### 2. Mocking External Dependencies

Tests mock Textual-dependent and API-dependent code:

```python
# Mock Textual operations
screen.list_view = MagicMock()
screen._populate_list = MagicMock()

# Mock API operations
app.client = AsyncMock()
app.client.get_unread_entries = AsyncMock(return_value=[entry])

# Mock UI operations
app.notify = MagicMock()
```text

### 3. Screen Parameters Instead of Global State

Screens receive data via constructor:

```python
# ✓ Good - data passed explicitly
screen = EntryReaderScreen(
  entry=entry,
  entry_list=sorted_entries,
  current_index=cursor_position,
)

# ✗ Bad - relying on global state
screen = EntryReaderScreen()  # Where does data come from?
```text

### 4. CSS for UI Updates (Grouped Mode)

Instead of rebuilding the list, use CSS visibility:

```python
# Hide collapsed entries with CSS class
if feed_is_collapsed:
  entry_item.add_class("collapsed")  # CSS: display: none

# j/k navigation naturally skips hidden items
# Cursor position is preserved
```text

### 5. Performance Optimization

```python
# Track refresh operations
optimizer = ScreenRefreshOptimizer()
optimizer.track_full_refresh()  # Rebuilds entire list
optimizer.track_partial_refresh()  # Updates single item

# Cache expensive computations
@memoize_with_ttl(ttl=1.0)
def expensive_operation():
  return compute_something()
```text

## Data Flow

### Entry Loading Flow

```bash
User presses Enter on entry
  ↓
EntryListScreen.on_list_view_selected()
  ↓
Gets current entry from list
  ↓
Calls app.push_entry_reader(entry, entry_list, index)
  ↓
EntryReaderScreen opens with entry displayed
  ↓
User presses 'q' or navigates back
  ↓
Screen is popped, cursor restored to entry_list
```text

### Sorting/Grouping Flow

```bash
User presses 's' (cycle sort)
  ↓
action_cycle_sort()
  ↓
Updates self.current_sort
  ↓
Calls _populate_list()
  ↓
Reads self.entries, applies sort
  ↓
Creates new list items (or updates with CSS if grouped)
  ↓
Display updates with new order
```text

### API Update Flow

```bash
User presses 'm' to mark as read
  ↓
async action_toggle_read()
  ↓
Updates entry.status locally
  ↓
Awaits app.client.mark_as_read(entry_id)
  ↓
Server updates entry
  ↓
Refreshes display to show new status
```text

## Error Handling

All API calls use the `api_call` context manager:

```python
from miniflux_tui.utils import api_call

async def action_toggle_read(self):
    with api_call(self, "marking entry as read") as client:
        if client is None:
            return

        await client.change_entry_status(self.entry.id, "read")

    self.entry.status = "read"
```text

This handles:
- Network errors
- API errors
- User notifications
- Logging

## Testing Strategy

### Unit Tests (52% of coverage)
- Test functions in isolation
- Mock Textual and API dependencies
- Focus on business logic

### Integration Tests (28% of coverage)
- Use Textual's `run_test()` context
- Test screens with real ListView
- Verify state management

### Quality Checks
- **Ruff**: Linting and formatting
- **Pyright**: Type checking (0 errors)
- **Pytest**: Unit and integration tests (426 tests)

## Extension Points

### Add a New Sorting Mode

1. Add to `SORT_MODES` in constants.py
2. Add logic to `_sort_entries()` in entry_list.py
3. Cycle through modes in `action_cycle_sort()`
4. Add test cases

### Add a New Binding

1. Add `Binding()` to `BINDINGS` in screen class
2. Create `action_*` method
3. Mark as `async def` if it calls API
4. Add test for the action

### Add a New Screen

1. Create `screens/my_screen.py`
2. Extend `Screen` class
3. Implement `compose()` for layout
4. Add bindings and action methods
5. Push from main app: `self.app.push_screen(MyScreen())`
6. Add tests

## Performance Considerations

### Refresh Operations

- **Full Refresh**: Rebuild entire list (slow)
- **Partial Refresh**: Update single item (fast)
- **CSS Updates**: Hide/show with CSS, no rebuild (very fast)

### Memory Usage

- Entry list keeps `sorted_entries` copy for navigation
- Cursor position persisted to avoid re-fetching
- Maps track item associations for quick lookup

### Caching

- `memoize_with_ttl()` for expensive operations
- `CachedProperty` for instance-level caching
- HTTP client connection pooling (Miniflux library)

## Coding Standards

- **Line Length**: 140 characters
- **Indentation**: 4 spaces
- **Quotes**: Double quotes
- **Type Hints**: Comprehensive
- **Documentation**: Docstrings for all public functions
- **Naming**: Descriptive, follows Python conventions

## Key Files Reference

| File                       | Lines | Coverage | Purpose         |
|----------------------------|-------|----------|-----------------|
| main.py                    | 60    | 98%      | CLI entry point |
| config.py                  | 76    | 100%     | Configuration   |
| api/client.py              | 58    | 100%     | API wrapper     |
| api/models.py              | 19    | 100%     | Data models     |
| ui/app.py                  | 71    | 100%     | Main app        |
| ui/screens/entry_list.py   | 398   | 64%      | Entry list      |
| ui/screens/entry_reader.py | 163   | 56%      | Entry detail    |
| ui/screens/help.py         | 49    | 100%     | Help screen     |

## Future Improvements

1. **Better grouping performance**: Virtual scrolling for large lists
2. **Caching layer**: Cache entries locally to reduce API calls
3. **Search functionality**: Full-text search across entries
4. **Custom themes**: User-defined color schemes
5. **Plugin system**: Allow extensions for custom feeds
6. **Offline mode**: Work with cached entries when offline
