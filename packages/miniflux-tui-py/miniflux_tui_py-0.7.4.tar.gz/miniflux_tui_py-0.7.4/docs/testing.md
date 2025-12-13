# Testing Guide

This guide covers testing patterns, best practices, and how to write tests for miniflux-tui-py.

## Overview

The miniflux-tui-py project has **78% test coverage** with **426 tests**. Tests are organized into:

- **Unit Tests**: Test individual functions and classes in isolation
- **Integration Tests**: Test components working together with Textual app context
- **Quality Checks**: Ruff (linting), Pyright (type checking)

## Running Tests

### Run All Tests
```bash
uv run pytest tests/
```text

### Run Specific Test File
```bash
uv run pytest tests/test_entry_list.py
```text

### Run with Coverage Report
```bash
uv run pytest tests/ --cov=miniflux_tui --cov-report=term-missing
```text

### Run Specific Test Class
```bash
uv run pytest tests/test_entry_list.py::TestSorting
```text

### Run with Verbose Output
```bash
uv run pytest tests/ -v
```text

## Test Organization

### Directory Structure
```bash
tests/
├── test_api_client.py          # API client tests (100% coverage)
├── test_api_models.py          # Data models tests (100% coverage)
├── test_app.py                 # Main app tests (100% coverage)
├── test_config.py              # Configuration tests (100% coverage)
├── test_entry_list.py          # Entry list screen unit tests (52% coverage)
├── test_entry_list_integration.py  # Entry list integration tests
├── test_entry_reader.py        # Entry reader screen tests (56% coverage)
├── test_help.py                # Help screen tests (100% coverage)
├── test_main.py                # CLI entry point tests (98% coverage)
├── test_performance.py         # Performance utilities tests (100% coverage)
├── test_utils.py               # Utility functions tests (100% coverage)
└── conftest.py                 # Shared fixtures
```text

## Test Patterns

### 1. Unit Testing with Mocks

Test isolated functions without external dependencies:

```python
from unittest.mock import MagicMock
from miniflux_tui.ui.screens.entry_list import EntryListScreen

def test_cycle_sort_changes_mode(diverse_entries):
  """Test that cycling sort mode works."""
  screen = EntryListScreen(entries=diverse_entries, default_sort="date")
  screen._populate_list = MagicMock()  # Mock Textual-dependent method

  # Execute
  screen.action_cycle_sort()

  # Assert
  assert screen.current_sort == "feed"
  screen._populate_list.assert_called_once()
```text

### 2. Integration Testing with Textual App

Test screens in a real Textual application context:

```python
from textual.app import App, ComposeResult
from miniflux_tui.ui.screens.entry_list import EntryListScreen

class TestApp(App):
  def __init__(self, entries):
  super().__init__()
  self.entries = entries
  self.entry_list_screen = None

  def compose(self) -> ComposeResult:
  self.entry_list_screen = EntryListScreen(
  entries=self.entries,
  unread_color="cyan",
  read_color="gray",
  )
  yield self.entry_list_screen

async def test_screen_initialization():
  """Test screen with real app context."""
  app = TestApp(entries=[...])

  async with app.run_test():
  screen = app.entry_list_screen
  assert screen.current_sort == "date"
  assert len(screen.entries) == 3
```text

### 3. Async Test Pattern

For async methods, use `pytest.mark.asyncio`:

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_load_entries_unread():
  """Test loading unread entries."""
  app = MinifluxTuiApp(config)
  app.client = AsyncMock()
  app.client.get_unread_entries = AsyncMock(return_value=[entry])
  app.is_screen_installed = MagicMock(return_value=False)
  app.notify = MagicMock()

  # Execute
  await app.load_entries("unread")

  # Assert
  app.client.get_unread_entries.assert_called_once()
  assert len(app.entries) == 1
```text

### 4. Filtering & Sorting Tests

Test data transformation logic:

```python
def test_filter_unread_only(diverse_entries):
  """Test filtering entries."""
  screen = EntryListScreen(entries=diverse_entries)
  screen.filter_unread_only = True

  # Execute
  filtered = screen._filter_entries(screen.entries)

  # Assert
  assert len(filtered) < len(screen.entries)
  assert all(e.is_unread for e in filtered)
```text

## Test Fixtures

### Common Fixtures (conftest.py)

```python
@pytest.fixture
def sample_feed():
  """Create a test feed."""
  return Feed(
  id=1,
  title="Test Feed",
  site_url="https://example.com",
  feed_url="https://example.com/feed.xml",
  )

@pytest.fixture
def sample_entry(sample_feed):
  """Create a test entry."""
  return Entry(
  id=1,
  feed_id=1,
  title="Test Entry",
  url="https://example.com/1",
  content="<p>Test</p>",
  feed=sample_feed,
  status="unread",
  starred=False,
  published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
  )

@pytest.fixture
def diverse_entries(sample_feed):
  """Create entries with varying attributes."""
  return [
  Entry(..., status="unread", starred=False),
  Entry(..., status="read", starred=True),
  Entry(..., status="unread", starred=True),
  ]
```text

## Coverage Goals

### Current Coverage by Module

| Module                     | Coverage | Status                        |
|----------------------------|----------|-------------------------------|
| api/client.py              | 100%     | ✅ Perfect                     |
| api/models.py              | 100%     | ✅ Perfect                     |
| config.py                  | 100%     | ✅ Perfect                     |
| constants.py               | 100%     | ✅ Perfect                     |
| performance.py             | 100%     | ✅ Perfect                     |
| ui/app.py                  | 100%     | ✅ Perfect                     |
| ui/screens/help.py         | 100%     | ✅ Perfect                     |
| utils.py                   | 100%     | ✅ Perfect                     |
| main.py                    | 98%      | ⚠️ Module-level if `__name__` |
| ui/screens/entry_list.py   | 64%      | 📈 Integration tests          |
| ui/screens/entry_reader.py | 56%      | 📝 Needs integration tests    |
| **Overall**                | **78%**  | 🎯 Production-ready           |

### Why 78% is Good

- **Core business logic**: 100% (api, config, utils)
- **Simple UI screens**: 100% (help)
- **Main app**: 100% (on_mount, lifecycle)
- **Complex UI screens**: 56-64% (require full Textual context)

The 78% coverage is excellent for a TUI application because:
1. All critical code paths are tested
2. All non-UI modules are at 100%
3. Complex UI behaviors are tested with integration tests
4. Type checking (Pyright) catches many issues

## Best Practices

### 1. Test Naming
- Use descriptive names: `test_action_cycle_sort_changes_mode`
- Include the behavior being tested
- Use `test_*_error` for exception testing

### 2. Test Structure (AAA Pattern)
```python
def test_something():
  # Arrange - set up test data
  screen = EntryListScreen(entries=entries)
  screen._populate_list = MagicMock()

  # Act - perform the action
  screen.action_cycle_sort()

  # Assert - verify the result
  assert screen.current_sort == "feed"
```text

### 3. Mock External Dependencies
```python
# Mock Textual-dependent methods
screen._populate_list = MagicMock()

# Mock API calls
app.client = AsyncMock()
app.client.get_unread_entries = AsyncMock(return_value=[entry])

# Mock user interactions
app.notify = MagicMock()
```text

### 4. Test Edge Cases
```python
def test_filter_empty_entries():
  """Test filtering with no entries."""
  screen = EntryListScreen(entries=[])
  filtered = screen._filter_entries([])
  assert len(filtered) == 0

def test_cursor_navigation_single_item():
  """Test cursor movement with one item."""
  screen = EntryListScreen(entries=[entry])
  screen.list_view = MagicMock()
  screen.action_cursor_down()  # Should handle gracefully
```text

### 5. Integration Test Guidelines

Use `run_test()` for full app context:
```python
async def test_screen_with_app():
  app = TestApp(entries=entries)

  async with app.run_test():
  screen = app.entry_list_screen
  # Screen is fully initialized with list_view, etc.
  assert screen.list_view is not None
```text

## Quality Checks

### Run All Quality Checks
```bash
# Linting
uv run ruff check .

# Code formatting
uv run ruff format .

# Type checking
uv run pyright

# All tests with coverage
uv run pytest tests/ --cov=miniflux_tui
```text

### Pre-commit Hooks
Hooks run automatically before commit:
- Ruff linting and formatting
- Pyright type checking
- YAML validation
- Security checks

## Writing Tests for New Features

### Step-by-Step Guide

1. **Create a test class** for your feature:
  ```python
  class TestMyNewFeature:
  """Test my new feature."""
```text

2. **Write unit tests** for isolated logic:
  ```python
  def test_feature_does_something(fixtures):
  # Test the feature
```text

3. **Write integration tests** for Textual interactions:
  ```python
  async def test_feature_with_app(fixtures):
  app = TestApp(...)
  async with app.run_test():
  # Test with full app context
```text

4. **Add fixtures** if needed:
  ```python
  @pytest.fixture
  def feature_data():
  return {"key": "value"}
```text

5. **Run tests** and check coverage:
  ```bash
  uv run pytest tests/test_myfeature.py --cov
```text

## Common Testing Scenarios

### Testing API Calls

```python
@pytest.mark.asyncio
async def test_api_call(sample_entry):
  app = MinifluxTuiApp(config)
  app.client = AsyncMock()
  app.client.mark_as_read = AsyncMock()
  app.notify = MagicMock()

  await app.client.mark_as_read(sample_entry.id)

  app.client.mark_as_read.assert_called_once_with(sample_entry.id)
```text

### Testing State Changes

```python
def test_state_change():
  screen = EntryListScreen(entries=entries, group_by_feed=False)
  screen._populate_list = MagicMock()

  assert screen.group_by_feed is False
  screen.action_toggle_group()
  assert screen.group_by_feed is True
```text

### Testing Filtering Logic

```python
def test_complex_filter():
  screen = EntryListScreen(entries=diverse_entries)

  # Test unread filter
  screen.filter_unread_only = True
  result = screen._filter_entries(screen.entries)
  assert all(e.is_unread for e in result)

  # Test precedence
  screen.filter_starred_only = True
  result = screen._filter_entries(screen.entries)
  assert all(e.is_unread for e in result)  # unread takes precedence
```text

## Troubleshooting Tests

### Issue: AttributeError with Textual components
**Solution**: Use mocks or run_test() context:
```python
# Instead of:
screen.list_view.action_cursor_down()

# Do this:
screen.list_view = MagicMock()
screen.action_cursor_down()

# Or use integration test:
async with app.run_test():
  screen = app.entry_list_screen
  screen.action_cursor_down()  # Works with real list_view
```text

### Issue: Async tests failing
**Solution**: Add `@pytest.mark.asyncio` and use AsyncMock:
```python
@pytest.mark.asyncio
async def test_async_method():
  app.client = AsyncMock()
  app.client.some_method = AsyncMock(return_value=result)
```text

### Issue: Coverage not improving
**Solution**: Check what code paths aren't covered:
```bash
uv run pytest tests/ --cov=miniflux_tui --cov-report=term-missing
# Look at the "Missing" column
```text

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Textual Testing Guide](https://textual.textualize.io/guide/testing/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)

## Contributing Tests

When contributing tests:
1. Follow the AAA pattern (Arrange, Act, Assert)
2. Use descriptive test names
3. Mock external dependencies
4. Add docstrings explaining what's tested
5. Ensure all tests pass: `uv run pytest tests/`
6. Check coverage doesn't decrease
7. Run quality checks: `uv run ruff check . && uv run pyright`
