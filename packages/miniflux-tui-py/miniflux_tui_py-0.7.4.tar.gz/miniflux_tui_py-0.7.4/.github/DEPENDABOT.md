# Dependabot Configuration

This project uses Dependabot to automatically update dependencies and GitHub Actions.

## How It Works

### Schedule
- **Frequency**: Weekly (Mondays at 03:00 UTC)
- **Max PRs**: 5 open at a time
- **Packages**: Python dependencies (pip) and GitHub Actions

### Auto-Merge Strategy

Dependabot PRs are automatically approved and merged if:
1. ✅ All CI checks pass (tests, linting, type checking)
2. ✅ PR is from `dependabot[bot]`
3. ✅ Update is minor or patch version (not major)

The workflow (`dependabot-auto-merge.yml`):
- Approves the PR automatically
- Enables auto-merge with squash strategy
- Waits for all GitHub Status checks to pass
- Merges automatically when ready

### Dependency Groups

Dependencies are grouped for easier management:

**Development Dependencies** (auto-mergeable):
- pytest, pytest-asyncio, pytest-cov
- ruff (linter/formatter)
- pyright (type checker)
- mkdocs, mkdocs-material
- pylint

**Production Dependencies** (require review for major updates):
- textual (TUI framework)
- miniflux (API client)
- html2text (HTML to Markdown)

### Manual Review

Major version updates are NOT auto-merged and require manual review:
- Review the changelog
- Check for breaking changes
- Run manual tests if needed
- Approve and merge manually

### When to Disable

If Dependabot updates cause issues:

1. **Close the PR** and wait for next week's update
2. **Check the issue** - usually reported in PR comments
3. **Pin the version** in `pyproject.toml` if needed:

    ```toml
    dependencies = [
        "textual>=0.82.0,<0.83.0",  # Pin to avoid breaking changes
    ]
    ```

### GitHub Actions Updates

Dependabot also updates GitHub Actions (workflows):
- Auto-approved and merged
- Always safe as they're tested before merge
- Help keep CI/CD pipeline up to date

### Disabling Dependabot

To disable Dependabot:

1. Go to **Settings** → **Code & automation** → **Dependabot**
2. Toggle off **Dependabot alerts**, **Dependabot updates**, etc.

Or delete this config file and `.github/workflows/dependabot-auto-merge.yml`

### References

- [GitHub Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Configuring Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuring-dependabot-version-updates)
