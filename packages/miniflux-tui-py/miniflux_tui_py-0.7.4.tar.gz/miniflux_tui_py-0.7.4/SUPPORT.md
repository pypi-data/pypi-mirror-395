# Support

Thank you for using miniflux-tui-py! This document provides information on how to get help and support.

## Quick Links

- **Documentation**: <https://reuteras.github.io/miniflux-tui-py/>
- **Issues**: <https://github.com/reuteras/miniflux-tui-py/issues>
- **Discussions**: <https://github.com/reuteras/miniflux-tui-py/discussions>
- **Security**: [SECURITY.md](SECURITY.md)

## Getting Help

### Documentation

Before opening an issue, please check the comprehensive documentation:

- [Installation Guide](https://reuteras.github.io/miniflux-tui-py/installation/) - Installation methods and requirements
- [Configuration](https://reuteras.github.io/miniflux-tui-py/configuration/) - Configuration options and examples
- [Usage Guide](https://reuteras.github.io/miniflux-tui-py/usage/) - Keyboard shortcuts and features
- [API Reference](https://reuteras.github.io/miniflux-tui-py/api/client/) - Technical documentation

### GitHub Discussions

For questions, ideas, or general discussions:

1. Visit [GitHub Discussions](https://github.com/reuteras/miniflux-tui-py/discussions)
2. Search existing discussions to see if your question has been answered
3. Create a new discussion if needed

**Best for:**
- General questions about usage
- Feature ideas and suggestions
- Sharing tips and tricks
- Community discussions

### GitHub Issues

For bug reports and feature requests:

1. Visit [GitHub Issues](https://github.com/reuteras/miniflux-tui-py/issues)
2. Search existing issues to avoid duplicates
3. Create a new issue using the appropriate template

**Best for:**
- Bug reports with reproducible steps
- Feature requests with specific use cases
- Documentation improvements

**Before reporting a bug:**
- Update to the latest version: `uv tool upgrade miniflux-tui-py` or `pip install --upgrade miniflux-tui-py`
- Check if the issue is already reported
- Gather relevant information (version, OS, error messages)

### Security Issues

**Do not open public issues for security vulnerabilities.**

Please report security concerns privately by following the instructions in [SECURITY.md](SECURITY.md).

## Common Issues

### Configuration Problems

If miniflux-tui fails to start or shows configuration errors:

```bash
# Validate your configuration
miniflux-tui --check-config

# Reinitialize configuration (backs up existing config)
miniflux-tui --init
```

Configuration file locations:
- **Linux**: `~/.config/miniflux-tui/config.toml`
- **macOS**: `~/.config/miniflux-tui/config.toml`
- **Windows**: `%APPDATA%\miniflux-tui\config.toml`

### Connection Issues

If you cannot connect to your Miniflux server:

1. Verify your server URL is correct (include `https://`)
2. Check your API key is valid
3. Ensure the Miniflux server is accessible from your machine
4. Check for firewall or network issues

### Keyboard Shortcuts Not Working

Press `?` within the application to view the help screen with all available keyboard shortcuts.

## Contributing

Interested in contributing? See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Setting up the development environment
- Running tests
- Submitting pull requests
- Code style requirements

## Community

- Follow project updates on [GitHub](https://github.com/reuteras/miniflux-tui-py)
- Star the repository if you find it useful
- Share feedback and suggestions

## Support the Project

If you find miniflux-tui-py useful, consider:

- **Contributing code**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Reporting bugs**: Help improve quality by reporting issues
- **Improving documentation**: Submit PRs for docs improvements
- **Spreading the word**: Share the project with others
- **Sponsoring development**: Support ongoing maintenance and new features

While this is a volunteer-driven open source project, sponsorship helps sustain development, infrastructure costs, and maintenance efforts.

## Contact

For other inquiries not covered above, you can reach the maintainer:

- **Email**: <peter@reuteras.net>
- **GitHub**: [@reuteras](https://github.com/reuteras)

**Response time**: As this is an open source project maintained in spare time, please allow reasonable time for responses. GitHub Issues and Discussions are monitored regularly.

## Code of Conduct

All interactions in this project are governed by our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to providing a welcoming and inclusive environment for everyone.

---

Thank you for being part of the miniflux-tui-py community!
