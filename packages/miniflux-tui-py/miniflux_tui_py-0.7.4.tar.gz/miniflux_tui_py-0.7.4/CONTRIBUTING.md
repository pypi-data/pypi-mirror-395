# Contributing to miniflux-tui-py

Thank you for your interest in contributing! This document provides guidelines for how to contribute.

## Quick Links

- [Development Setup](docs/contributing.md#development-setup)
- [Running Tests](docs/contributing.md#running-tests)
- [Code Style](docs/contributing.md#code-style)
- [Submitting Changes](docs/contributing.md#submitting-changes)

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/miniflux-tui-py.git`
3. Create a feature branch: `git checkout -b feature/my-feature`
4. Set up development environment: `uv sync --all-groups`
5. Make your changes
6. Run tests: `uv run pytest tests`
7. Push and create a pull request

## Quick Checks Before PR

```bash
# Format code
uv run ruff format miniflux_tui tests

# Check linting
uv run ruff check miniflux_tui tests

# Type checking
uv run pyright miniflux_tui tests

# Run tests
uv run pytest tests --cov=miniflux_tui
```

## Code of Conduct

Please review our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). We expect all contributors to follow it.

## Full Contributing Guide

For detailed contributing guidelines, see [docs/contributing.md](docs/contributing.md).

## Questions or Issues?

- Open an issue for bugs or feature requests
- Use GitHub Discussions for questions
- See [SECURITY.md](SECURITY.md) for security concerns

Thank you for contributing! 🎉
