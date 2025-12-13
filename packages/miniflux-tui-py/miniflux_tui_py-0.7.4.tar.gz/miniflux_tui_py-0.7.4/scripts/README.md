# Scripts Directory

This directory contains utility scripts for project maintenance and automation.

## Scripts Overview

### `update_branch_protection.sh`

Updates GitHub branch protection rules for the `main` branch with strong security and quality standards.

**Purpose:**
- Configures branch protection to enforce code quality and security
- Prevents direct pushes to main branch (requires pull requests)
- Ensures all changes go through proper review process
- Maintains strong security posture with signed commits and admin enforcement

**Usage:**

```bash
./scripts/update_branch_protection.sh
```

**Protection Rules Applied:**
- **Require pull requests**: No direct commits to main branch
- **Require 1 approving review**: Single maintainer review required
- **Dismiss stale pull request approvals**: Reapproval needed after new commits
- **Require status checks to pass**: All CI/CD checks must pass before merge
- **Require branches to be up to date**: Must rebase before merging
- **Require code owner review**: Code owners must approve changes
- **Require signed commits**: All commits must be signed
- **Include administrators**: Branch protection applies to everyone, including admins
- **Block force pushes**: Prevent force push to main
- **Block deletions**: Prevent branch deletion

**Security Features:**
- Enforces conventional commits (feat, fix, docs, etc.)
- Blocks unapproved direct commits
- Requires signed commits for audit trail
- Ensures linear history (no merge commits)
- Admin enforcement prevents bypass

---

### `add_spdx_headers.py`

Adds SPDX license headers to Python source files for license compliance.

**Purpose:**
- Ensures all Python files have proper SPDX license identifiers
- Supports REUSE compliance for license management

**Usage:**

```bash
uv run scripts/add_spdx_headers.py
```

---

### `build_binary.py`

Builds standalone binary distributions of miniflux-tui using PyInstaller.

**Purpose:**
- Creates single-file executable for distribution
- Useful for users without Python installed

**Usage:**

```bash
uv run scripts/build_binary.py
```

## Best Practices

1. **Always test scripts in a fork first** before running on main repository
2. **Review script output** for errors or unexpected behavior
3. **Keep accounts secured** with 2FA and strong passwords
4. **Update scripts** when GitHub API or workflow changes occur
5. **Document changes** to scripts in commit messages

## Contributing

When adding new scripts:

1. Follow bash best practices:
  - Use `set -euo pipefail` for error handling
  - Add clear comments and documentation
  - Include usage examples
  - Add colored output for better UX
2. Make scripts executable: `chmod +x scripts/your_script.sh`
3. Update this README with script description and usage
4. Test thoroughly before committing

## Security

- Scripts use GitHub CLI authentication (no hardcoded tokens)
- Account switching uses `gh auth switch` (secure method)
- Scripts include timeout protection against infinite loops
- All API calls go through authenticated `gh` CLI

## Related Documentation

- [RELEASE.md](../RELEASE.md) - Release process documentation
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [AGENT.md](../AGENT.md) - Project architecture and workflows
