# Development Guide

Welcome to miniflux-tui-py! This guide will help you set up your development environment and contribute to the project.

## Quick Start

### Option 1: GitHub Codespaces (Recommended)

The easiest way to get started:

1. Click **"Code"** → **"Codespaces"** → **"Create codespace on main"**
2. Wait for the codespace to launch (~2-3 minutes)
3. The environment will automatically:
    - Install `uv` package manager
    - Install all dependencies (dev, test, docs, fuzzing)
    - Set up pre-commit hooks
    - Show you helpful quick-start commands

**That's it!** You're ready to develop.

### Option 2: Local Setup

```bash
# 1. Install uv (see: https://docs.astral.sh/uv/getting-started/installation/)
# On macOS/Linux: brew install uv
# On Windows: winget install astral-sh.uv

# 2. Clone and setup
git clone https://github.com/reuteras/miniflux-tui-py.git
cd miniflux-tui-py

# 3. Install all dependencies (including dev/docs)
uv sync --all-groups

# 4. Install pre-commit hooks
uv run pre-commit install

# 5. You're ready!
```

---

## Development Workflow

### Running Tests

```bash
# Run all tests
uv run pytest tests

# Run specific test
uv run pytest tests/test_api.py::test_function_name

# Run with coverage report
uv run pytest tests --cov=miniflux_tui --cov-report=html

# Watch mode (re-run on file changes)
uv run pytest-watch tests
```

**VS Code**: Press `Ctrl+Shift+T` → Select "🧪 Test (pytest)"

### Code Quality

```bash
# Lint code
uv run ruff check miniflux_tui tests

# Format code (fix style issues)
uv run ruff format miniflux_tui tests

# Type checking (strict mode)
uv run pyright miniflux_tui tests

# Run all pre-commit hooks
uv run pre-commit run --all-files
```

**VS Code**: Use `Ctrl+Shift+B` to access build tasks:
- `✨ Lint (ruff check)`
- `🎨 Format (ruff format)`
- `🔍 Type Check (pyright)`
- `✅ Run Quality Checks` (all at once)

### Running the Application

```bash
# Initialize configuration
uv run miniflux-tui --init

# Run the app
uv run miniflux-tui

# Check configuration
uv run miniflux-tui --check-config
```

**VS Code**: Press `Ctrl+Shift+B` → Select "🚀 Run App"

### Documentation

```bash
# Preview docs locally
uv run mkdocs serve

# Build static docs (output: site/)
uv run mkdocs build
```

**VS Code**: Press `Ctrl+Shift+B` → Select "📚 Build Docs (mkdocs serve)"

Then visit `http://localhost:8000` to preview.

---

## VS Code Extensions & Settings

### Pre-installed Extensions in Codespaces

- **ms-python.python** - Python support
- **ms-python.vscode-pylance** - Intelligent Python analysis
- **ms-python.debugpy** - Python debugging
- **charliermarsh.ruff** - Ruff linting & formatting
- **donjayamanne.githistory** - Git history browser
- **eamodio.gitlens** - Advanced Git features
- **esbenp.prettier-vscode** - Code formatting for JSON/YAML/Markdown
- **redhat.vscode-yaml** - YAML validation
- **ms-vscode.makefile-tools** - Makefile support

### Key Settings

- **Format on Save** - Automatically formats code with Ruff when you save
- **Strict Type Checking** - Pyright in strict mode for maximum type safety
- **Auto Test Discovery** - Tests are discovered automatically
- **pytest as Default** - Test framework is configured

---

## Pre-commit Hooks

Pre-commit hooks automatically check your code before commits:

```bash
# Install hooks (done automatically in Codespaces)
uv run pre-commit install

# Run hooks on all files
uv run pre-commit run --all-files

# Skip hooks for a commit (not recommended!)
git commit --no-verify
```

**Hooks that run:**
- ruff (linting & formatting)
- pyright (type checking)
- YAML validation
- Markdown linting
- Git conflict detection
- Secret scanning (detect leaked credentials)
- And more...

---

## Project Structure

```text
miniflux-tui-py/
├── miniflux_tui/              # Main package
│   ├── main.py                # CLI entry point
│   ├── config.py              # Configuration management
│   ├── api/
│   │   ├── client.py          # Miniflux API wrapper
│   │   └── models.py          # Data models
│   └── ui/
│       ├── app.py             # Main TUI app
│       └── screens/           # Screen implementations
├── tests/                      # Test suite
├── docs/                       # MkDocs documentation
├── .github/
│   ├── workflows/             # CI/CD pipelines
│   └── issue_templates/       # Issue/PR templates
├── .devcontainer/             # VS Code Codespaces config
├── .vscode/                   # VS Code settings
├── pyproject.toml             # Project metadata & dependencies
└── .pre-commit-config.yaml    # Pre-commit hooks config
```

---

## Common Tasks

### Adding a New Feature

1. **Create a branch**: `git checkout -b feat/your-feature`
2. **Make changes**: Edit files, add tests
3. **Run checks**: `uv run pytest tests && uv run ruff check . && uv run pyright .`
4. **Commit**: `git commit -m "feat: Description of feature"`
5. **Push**: `git push origin feat/your-feature`
6. **Create PR**: Open a pull request on GitHub

### Fixing a Bug

1. **Create a branch**: `git checkout -b fix/bug-description`
2. **Add test**: Write a test that reproduces the bug
3. **Fix the code**: Make the test pass
4. **Run checks**: Ensure all tests and linting pass
5. **Commit**: `git commit -m "fix: Description of fix"`
6. **Push and PR**: Push to origin and create a pull request

### Updating Dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update a specific package
uv pip install --upgrade package-name

# View what would change
uv pip compile --dry-run
```

Dependencies are locked in `uv.lock` for reproducible builds.

---

## Debugging

### Debug Tests in VS Code

1. Set breakpoints in test files (click on line number)
2. Press `Ctrl+Shift+D` to open Debug view
3. Select "Python: pytest" and press Play
4. Step through code with F10 (step over) / F11 (step into)

### Debug the Application

1. Create a run configuration in `.vscode/launch.json`
2. Press `F5` to start debugging
3. Use the debug console to inspect variables

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

---

## Testing Best Practices

### Test Structure

```python
import pytest
from miniflux_tui.api.models import Entry

class TestEntry:
    """Tests for Entry model."""

    def test_entry_creation(self):
        """Test creating an entry."""
        entry = Entry(...)
        assert entry.title == "Test"

    @pytest.mark.asyncio
    async def test_async_function(self):
        """Test async functions."""
        result = await some_async_function()
        assert result is not None
```

### Coverage Requirements

- Minimum 60% code coverage required
- Aim for 80%+ for new code
- Check coverage: `uv run pytest tests --cov=miniflux_tui`

---

## Type Hints

This project uses **strict type checking** with Pyright. All code should have type hints:

```python
from typing import Optional, List
from miniflux_tui.api.models import Entry

def process_entries(
    entries: List[Entry],
    filter_unread: bool = False
) -> Optional[Entry]:
    """Process entries and return the first one."""
    if not entries:
        return None

    if filter_unread:
        entries = [e for e in entries if not e.is_read]

    return entries[0] if entries else None
```

---

## Git Workflow (Important!)

**⚠️ ALL CHANGES MUST BE IN FEATURE BRANCHES - NEVER COMMIT DIRECTLY TO MAIN**

### Branch Naming Conventions

- `feat/feature-name` - New features
- `fix/bug-name` - Bug fixes
- `docs/document-name` - Documentation updates
- `refactor/component-name` - Code refactoring
- `test/feature-name` - Test additions
- `chore/task-name` - Maintenance tasks

### Workflow

```bash
# 1. Create feature branch
git checkout main
git pull origin main
git checkout -b feat/my-feature

# 2. Make changes and commit
git add .
git commit -m "feat: Clear description of what was implemented"

# 3. Push to origin
git push origin feat/my-feature

# 4. Create PR on GitHub
# - Title: Clear description
# - Body: Explain the why, link issues
# - Wait for CI to pass

# 5. After merge, clean up
git checkout main
git pull origin main
git branch -d feat/my-feature
git push origin --delete feat/my-feature
```

---

## Code Style Guide

### Line Length
- **140 characters** (configured in `pyproject.toml`)

### Formatting
- Use `ruff format` (configured with Ruff)
- No manual formatting needed (format on save!)

### Linting
- Use `ruff check` for all linting
- No bare URLs in markdown/docs (wrap in angle brackets: `<url>`)

### Type Checking
- Strict mode enabled (pyright)
- All public functions must have type hints
- Use `Optional[T]` instead of `T | None` for Python 3.11 compatibility

### Docstrings
- Use Google-style docstrings
- Document parameters, return values, exceptions

```python
def fetch_entries(feed_id: int, limit: int = 10) -> List[Entry]:
    """Fetch RSS entries from a feed.

    Args:
        feed_id: The feed ID to fetch from.
        limit: Maximum number of entries to return. Defaults to 10.

    Returns:
        List of Entry objects.

    Raises:
        APIError: If the API request fails.
    """
    pass
```

---

## Performance Considerations

- Avoid blocking operations in async code
- Use `run_in_executor` for sync calls from async context
- Cache API responses when appropriate
- Profile with the tools in `miniflux_tui/performance.py`

---

## Dependency Management

### Automated Updates
The project uses **Renovate** to keep dependencies up to date:

- **Security patches**: Created immediately when available (patch-level updates)
- **Regular updates**: Created on Mondays at 10pm (batched for reduced noise)
- **Major version updates**: Created on Sundays at 10pm (requires manual review)
- **Automatic approval**: Security and regular updates approved and merged when all CI checks pass
- **Manual review**: Major version updates require your approval before merging

### Manual Monitoring (GitHub Watches)
Some critical dependencies with frequent updates should be monitored manually:

1. **Trivy Action** - <https://github.com/aquasecurity/trivy-action>
- Container vulnerability scanner
- Watch for releases: <https://github.com/aquasecurity/trivy-action/releases>
- Latest: `v0.33.1` (September 2025)
- To watch: Go to repo → Click **Watch** → Select **Releases**

### Dependency Dashboard
Check **Issue #70** for the Renovate Dependency Dashboard:
- Shows all pending updates
- Lists security and regular updates separately
- Allows manual triggering of updates if needed

---

## Resources

- **Documentation**: <https://reuteras.github.io/miniflux-tui-py/>
- **Miniflux Docs**: <https://miniflux.app>
- **Textual TUI Framework**: <https://textual.textualize.io/>
- **uv Package Manager**: <https://docs.astral.sh/uv/>
- **Ruff Linter**: <https://docs.astral.sh/ruff/>
- **Renovate Docs**: <https://docs.renovatebot.com/>
- **Trivy Action**: <https://github.com/aquasecurity/trivy-action>

---

## Getting Help

- **Questions**: Use GitHub Discussions
- **Bugs**: Create a GitHub Issue with details and reproduction steps
- **Security Issues**: See SECURITY.md
- **Suggestions**: Start a Discussion or Issue

---

## Troubleshooting

### Pre-commit hooks not running?
```bash
uv run pre-commit install
```

### Outdated dependencies?
```bash
uv sync --all-groups --upgrade
```

### Python interpreter not found?
```bash
# Codespaces: Reload window (Ctrl+Shift+P → Reload Window)
# Local: uv sync creates .venv automatically
```

### Tests failing?
```bash
# Run with verbose output
uv run pytest tests -vv

# Run specific test
uv run pytest tests/test_file.py::test_name -vv
```

### Type errors in VS Code?
```bash
# Rebuild Pylance index
# Ctrl+Shift+P → "Python: Restart Language Server"
```

---

**Happy coding! 🚀**
