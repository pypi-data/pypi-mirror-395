# Code Patterns & Best Practices

This guide covers common patterns used throughout miniflux-tui-py and how to apply them to new code.

## Pattern 1: Async API Calls with Error Handling

All API interactions should use the `api_call` context manager for consistent error handling.

### Bad Pattern (Pattern 1) - Avoid
```python
async def action_toggle_read(self):
  """Mark entry as read."""
  try:
  await self.app.client.mark_as_read(self.entry.id)
  self.entry.status = "read"
  except Exception as e:
  self.app.notify(f"Error: {e}")
```text

### Good Pattern (Pattern 1) - Use This
```python
from miniflux_tui.utils import api_call

async def action_toggle_read(self):
    """Mark entry as read."""
    with api_call(self, "marking entry as read") as client:
        if client is None:
            return

        await client.change_entry_status(self.entry.id, "read")

    self.entry.status = "read"
    self._refresh_display()
```text

**Benefits:**
- Consistent error handling across the app
- Automatic user notifications
- Unified logging
- Better error messages

## Pattern 2: Screen Initialization with Parameters

Always pass data to screens via constructor parameters, never rely on global state.

### Bad Pattern (Pattern 2) - Avoid
```python
# Global entry storage
current_entry = None
current_index = None

class EntryReaderScreen(Screen):
  def on_mount(self):
  # Access from globals
  self.entry = current_entry
  self.index = current_index
```text

### Good Pattern (Pattern 2) - Use This
```python
class EntryReaderScreen(Screen):
  def __init__(
  self,
  entry: Entry,
  entry_list: list[Entry],
  current_index: int,
  **kwargs,
  ):
  super().__init__(**kwargs)
  self.entry = entry
  self.entry_list = entry_list
  self.current_index = current_index

# Usage
self.app.push_screen(EntryReaderScreen(
  entry=entry,
  entry_list=sorted_entries,
  current_index=cursor_position,
))
```text

**Benefits:**
- Explicit dependencies
- Easier testing
- Multiple instances work correctly
- Clear data flow

## Pattern 3: Mocking Textual Dependencies

Don't test Textual internals; mock them and test your logic.

### Bad Pattern (Pattern 3) - Avoid
```python
def test_action():
  screen = EntryListScreen(entries=entries)
  # Try to use real list_view - fails without app context
  screen.list_view.scroll_visible(item)  # Error!
```text

### Good Pattern (Unit Test)
```python
def test_action():
  screen = EntryListScreen(entries=entries)
  screen.list_view = MagicMock()
  screen._populate_list = MagicMock()

  screen.action_cycle_sort()

  screen._populate_list.assert_called_once()
  assert screen.current_sort == "feed"
```text

### Good Pattern (Integration Test)
```python
async def test_action_with_app():
  app = TestApp(entries=entries)

  async with app.run_test():
  screen = app.entry_list_screen
  screen.action_cycle_sort()

  # list_view is real, populated, and works
  assert isinstance(screen.list_view, ListView)
  assert len(screen.list_view.children) > 0
```text

**Benefits:**
- Tests focus on your code, not Textual
- Faster execution (unit tests)
- More reliable tests
- Easier debugging

## Pattern 4: State Management in Screens

Track state explicitly, update UI consistently.

### Bad Pattern (Pattern 4) - Avoid
```python
def action_toggle_read(self):
  """Mark entry as read."""
  # State is implicit, hard to track
  if something:
  self.entry.status = "read"
  # UI might not update
```text

### Good Pattern (Pattern 4) - Use This
```python
async def action_toggle_read(self):
    """Toggle entry read/unread status."""
    # 1. Update desired state
    new_status = "read" if self.entry.is_unread else "unread"

    # 2. Persist to server with unified error handling
    with api_call(self, f"marking entry as {new_status}") as client:
        if client is None:
            return

        if new_status == "read":
            await client.change_entry_status(self.entry.id, "read")
        else:
            await client.change_entry_status(self.entry.id, "unread")

    # 3. Update local state
    self.entry.status = new_status

    # 4. Update UI
    self._update_entry_display()
```text

**Pattern:**
1. Update state first
2. Persist to server (with error handling)
3. Update local model
4. Refresh UI

## Pattern 5: Sorting and Filtering Logic

Separate data transformation from UI updates.

### Good Pattern (Pattern 5)
```python
def _filter_entries(self, entries: list[Entry]) -> list[Entry]:
  """Filter entries based on current filters."""
  result = entries

  # Apply filters in order
  if self.filter_unread_only:
  result = [e for e in result if e.is_unread]
  elif self.filter_starred_only:
  result = [e for e in result if e.starred]

  return result

def _sort_entries(self, entries: list[Entry]) -> list[Entry]:
  """Sort entries based on current mode."""
  if self.current_sort == "date":
  return sorted(entries, key=lambda e: e.published_at, reverse=True)
  elif self.current_sort == "feed":
  return sorted(
  entries,
  key=lambda e: (e.feed.title.lower(), e.published_at),
  reverse=True,
  )
  elif self.current_sort == "status":
  return sorted(
  entries,
  key=lambda e: (e.is_unread, e.published_at),
  reverse=True,
  )
  return entries

async def action_refresh(self):
  """Refresh and re-sort entries."""
  # Fetch fresh data
  await self.app.load_entries()

  # Apply current filters and sorts
  filtered = self._filter_entries(self.entries)
  self.sorted_entries = self._sort_entries(filtered)

  # Update UI
  self._populate_list()
```text

**Benefits:**
- Pure functions (testable)
- Composable logic
- Easy to debug
- Easy to add new sort modes

## Pattern 6: CSS for Dynamic UI Updates

Use CSS classes for visibility, not rebuilding lists.

### Good Pattern (Grouped Mode)
```python
def action_collapse_feed(self):
  """Collapse a feed in grouped mode."""
  if not self.list_view or not self.group_by_feed:
  return

  highlighted = self.list_view.highlighted_child
  if highlighted and isinstance(highlighted, FeedHeaderItem):
  feed_title = highlighted.feed_title

  # Update fold state
  self.feed_fold_state[feed_title] = False
  highlighted.toggle_fold()

  # Hide entries for this feed using CSS
  for item in self.list_view.children:
  if isinstance(item, EntryListItem):
  if item.entry.feed.title == feed_title:
  item.add_class("collapsed")  # CSS: display: none

  # Cursor naturally skips hidden items
```text

**Benefits:**
- Preserves cursor position
- Instant visual feedback
- No need to rebuild list
- Natural keyboard navigation

## Pattern 7: Caching Expensive Operations

Use caching utilities for repeated calculations.

### Using Memoization
```python
from miniflux_tui.performance import memoize_with_ttl

@memoize_with_ttl(ttl=1.0)  # Cache for 1 second
def get_sort_key(entry: Entry, sort_mode: str) -> tuple:
  """Get sort key for entry (expensive calculation)."""
  if sort_mode == "date":
  return (entry.published_at,)
  elif sort_mode == "feed":
  return (entry.feed.title.lower(), entry.published_at)
  elif sort_mode == "status":
  return (entry.is_unread, entry.published_at)
  return (entry.id,)
```text

### Using Cached Properties
```python
from miniflux_tui.performance import CachedProperty

class Entry:
  @CachedProperty
  def display_title(self) -> str:
  """Display title (with HTML stripping, caching)."""
  # Expensive operation - result cached per instance
  return strip_html(self.title)
```text

**When to Use:**
- Repeated calculations in loops
- API responses that don't change often
- UI rendering logic
- Text processing

## Pattern 8: Type Hints and Type Safety

Always use type hints for better code quality.

### Good Pattern (Pattern 8)
```python
from typing import Optional
from miniflux_tui.api.models import Entry, Feed

def get_entry_by_id(
  entries: list[Entry],
  entry_id: int,
) -> Optional[Entry]:
  """Find entry by ID, return None if not found."""
  for entry in entries:
  if entry.id == entry_id:
  return entry
  return None

async def process_entries(
  client: MinifluxClient,
  entries: list[Entry],
) -> dict[str, int]:
  """Process entries and return stats."""
  stats: dict[str, int] = {"read": 0, "unread": 0}

  for entry in entries:
  if entry.is_unread:
  stats["unread"] += 1
  else:
  stats["read"] += 1

  return stats
```text

**Benefits:**
- IDE autocomplete
- Type checking with Pyright
- Self-documenting code
- Easier refactoring

## Pattern 9: Docstring Format

Follow Google-style docstrings for consistency.

### Good Pattern (Pattern 9)
```python
async def mark_as_read(self, entry_id: int) -> None:
  """Mark an entry as read.

  Updates the entry status on the server and refreshes the local
  state. Handles errors with user notifications.

  Args:
  entry_id: ID of the entry to mark as read

  Raises:
  HTTPError: If the server request fails
  """
  await self._client.mark_as_read(entry_id)
  self._update_local_state(entry_id, "read")
```text

### For Classes
```python
class EntryListScreen(Screen):
  """Display and interact with a list of feed entries.

  Supports sorting by date/feed/status, grouping by feed,
  filtering by read status, and keyboard navigation.

  Attributes:
  entries: List of all entries to display
  current_sort: Current sort mode ("date", "feed", or "status")
  group_by_feed: Whether to group entries by feed title
  """
```text

## Pattern 10: Exception Handling

Use specific exceptions, not bare except.

### Bad Pattern (Pattern 10) - Avoid
```python
try:
  result = await something()
except:  # Catches everything, including KeyboardInterrupt!
  print("Error")
```text

### Good Pattern (Pattern 10) - Use This
```python
try:
  result = await something()
except (ValueError, TypeError) as e:
  self.app.notify(f"Invalid input: {e}")
except asyncio.TimeoutError:
  self.app.notify("Request timed out")
except Exception as e:
  self.app.notify(f"Unexpected error: {e}")
  self.logger.exception("Unexpected error")
```text

**Or Use the api_call Context Manager:**
```python
with api_call(self, "marking entry as read") as client:
    if client is None:
        return

    await client.change_entry_status(entry_id, "read")
```text

## Pattern 11: Constants Instead of Magic Numbers

Use constants defined in constants.py.

### Bad Pattern (Pattern 11) - Avoid
```python
if len(entries) > 100:  # What does 100 mean?
  show_warning()
```text

### Good Pattern (Pattern 11) - Use This
```python
# constants.py
DEFAULT_ENTRY_LIMIT = 100
SORT_MODES = ["date", "feed", "status"]

# In code
if len(entries) > DEFAULT_ENTRY_LIMIT:
  show_warning()
```text

## Pattern 12: Testing Patterns

### Test Naming Convention
```python
# Good: test_[feature]_[behavior]_[expectation]
def test_filter_unread_only_shows_unread_entries():
  """Test that unread filter excludes read entries."""
```text

### AAA Pattern (Arrange, Act, Assert)
```python
def test_cycle_sort():
  # Arrange
  screen = EntryListScreen(entries=entries, default_sort="date")
  screen._populate_list = MagicMock()

  # Act
  screen.action_cycle_sort()

  # Assert
  assert screen.current_sort == "feed"
  screen._populate_list.assert_called_once()
```text

## Summary

Key principles to follow:

1. **Consistency**: Use established patterns, don't create new ones
2. **Type Safety**: Always use type hints
3. **Error Handling**: Use `api_call` context manager
4. **Testing**: Mock external dependencies, test business logic
5. **Documentation**: Clear docstrings and comments
6. **Performance**: Cache expensive operations
7. **Separation**: Keep UI logic separate from business logic
8. **State Management**: Track state explicitly, update UI consistently

## Code Review Checklist

When reviewing code, verify:

- [ ] Type hints present on all functions
- [ ] Async API calls use `api_call` context manager
- [ ] Screens receive data via constructor parameters
- [ ] Textual dependencies are mocked in unit tests
- [ ] Tests follow AAA pattern
- [ ] Docstrings follow Google style
- [ ] No magic numbers (use constants)
- [ ] No bare `except:` statements
- [ ] Performance: No O(n²) loops, reasonable caching
- [ ] Passes: `ruff check`, `ruff format`, `pyright`
