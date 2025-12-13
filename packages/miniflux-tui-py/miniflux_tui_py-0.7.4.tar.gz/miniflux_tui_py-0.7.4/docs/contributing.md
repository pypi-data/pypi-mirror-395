# Contributing

Thank you for your interest in contributing to miniflux-tui-py! This document provides guidelines and instructions for getting involved.

## Code of Conduct

Please read our [Code of Conduct](https://github.com/reuteras/miniflux-tui-py/blob/main/CODE_OF_CONDUCT.md) before contributing. We are committed to providing a welcoming and inspiring community for all.

## Development Setup

### Prerequisites

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- Git

### Setting Up Your Development Environment

1. **Fork and clone the repository:**

```bash
git clone https://github.com/YOUR_USERNAME/miniflux-tui-py.git
cd miniflux-tui-py
```

2. **Install dependencies with uv:**

```bash
uv sync --all-groups
```

This will install all development and documentation dependencies including pytest, ruff, pyright, and mkdocs.

3. **Verify your setup:**

```bash
uv run miniflux-tui --check-config
```

## Making Changes

### Creating a Feature Branch

Create a feature branch from `main`:

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### Running Tests Locally

Before submitting a pull request, make sure all checks pass:

```bash
# Run linting with ruff
uv run ruff check miniflux_tui tests

# Format code
uv run ruff format miniflux_tui tests

# Type checking with pyright
uv run pyright miniflux_tui tests

# Run tests with coverage
uv run pytest tests --cov=miniflux_tui --cov-report=term-missing
```

All checks are also run automatically when you commit (via pre-commit hooks).

### Code Style

- **Line length**: 140 characters
- **Quotes**: Double quotes
- **Formatting**: Follow ruff/black style
- **Type hints**: Add type hints where possible
- **Docstrings**: Use Google-style docstrings

### Commit Messages

Write clear, concise commit messages:

```text
Add feature: brief description

Longer description of what changed and why.
```

## Submitting Changes

### Pre-Submission Checklist

1. ✅ Code passes all checks (`ruff check`, `ruff format`, `pyright`, `pytest`)
2. ✅ Tests have been written/updated for new functionality
3. ✅ Documentation has been updated if needed
4. ✅ CHANGELOG.md has been updated (see below)
5. ✅ Commit messages are clear and descriptive

### Creating a Pull Request

1. **Push your branch to your fork:**

```bash
git push origin feature/your-feature-name
```

2. **Create a pull request on GitHub:**
- Go to the main repository
- Click "New Pull Request"
- Select your feature branch
- Fill in a descriptive title and description
- Reference any related issues

### What to Expect

- Automated checks will run (tests, linting, type checking)
- A maintainer will review your code
- We may request changes before merging
- Once approved, your changes will be merged to `main`

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest tests

# Run with coverage
uv run pytest tests --cov=miniflux_tui

# Run a specific test file
uv run pytest tests/test_entry_list.py

# Run tests matching a pattern
uv run pytest tests -k "test_navigation"
```

### Writing Tests

- Place tests in the `tests/` directory
- Use `test_*.py` file naming convention
- Use descriptive test function names
- Tests should be independent and fast

Example:

```python
import pytest
from miniflux_tui.api.models import Entry

def test_entry_properties():
    """Test Entry model properties."""
    entry = Entry(
        id=1,
        title="Test Entry",
        content="Test content",
        # ... other properties
    )
    assert entry.is_unread is True
```

### Test Coverage Requirements

- **Minimum coverage threshold**: 60% line coverage
- **Target coverage**: 75%+ for maintainability
- Coverage is checked automatically in CI/CD
- PRs that reduce coverage may be rejected

Check local coverage:
```bash
uv run pytest tests --cov=miniflux_tui --cov-report=term-missing
```

### Python Version Support

miniflux-tui-py is tested on:
- **Supported versions**: Python 3.13, 3.14
- **Preview versions**: Python 3.15 (optional, may fail)
- **All platforms**: Linux (Ubuntu), macOS, Windows

Tests run automatically on all combinations in CI/CD. If your changes have version-specific behavior, test locally:

```bash
# Test with specific Python version
uv python install 3.13
uv run -p 3.13 pytest tests
```

## Updating Documentation

Documentation is built with MkDocs and located in the `docs/` folder.

### Editing Docs

1. Edit files in the `docs/` folder (Markdown format)
2. Preview locally:
  ```bash
  uv run mkdocs serve
  ```
3. View at <http://localhost:8000>

### Documentation Guidelines

- Use clear, simple language
- Include code examples where helpful
- Keep the table of contents in `mkdocs.yml` updated
- Use relative links between docs

## Updating CHANGELOG

Keep the CHANGELOG.md updated with your changes.

Format your entry under the current "Unreleased" section:

```markdown
## Unreleased

### Added
- New feature description

### Fixed
- Bug fix description

### Changed
- Breaking change description
```

We follow [Keep a Changelog](https://keepachangelog.com/) format.

## Release Process

(For maintainers)

When ready to release:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with version and date
3. Commit: `git commit -m "Release v0.2.0"`
4. Tag: `git tag v0.2.0`
5. Push: `git push origin main --tags`
6. GitHub Actions automatically publishes to PyPI and creates a GitHub Release

## Getting Help

- Check existing issues and discussions
- Ask questions in GitHub Discussions
- Report bugs in GitHub Issues
- See [Security](security.md) for security-related concerns

## Thank You

We appreciate all contributions, whether code, documentation, bug reports, or feature suggestions. You're helping make miniflux-tui-py better for everyone!
