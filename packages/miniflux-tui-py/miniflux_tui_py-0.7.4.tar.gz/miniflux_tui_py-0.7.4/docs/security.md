# Security

This document outlines the security practices and features of the miniflux-tui-py project.

## OpenSSF Scorecard

The miniflux-tui-py project maintains a strong security posture as measured by the [OpenSSF Scorecard](https://securityscorecards.dev/). View the current scorecard at:

[https://securityscorecards.dev/viewer/?uri=github.com/reuteras/miniflux-tui-py](https://securityscorecards.dev/viewer/?uri=github.com/reuteras/miniflux-tui-py)

### Security Scorecard Features

#### ✅ Code Review
All changes to the main branch require at least one code review and approval before merging. This ensures:
- **Peer review** of all code changes
- **Knowledge sharing** across the team
- **Early detection** of potential issues
- **Accountability** for code quality

**Configuration**:
- Required approving reviews: 1
- Dismiss stale reviews: Yes
- Code owner reviews: No

#### ✅ Signed Releases
All releases are cryptographically signed with **Sigstore Gitsign** (keyless signing), providing:
- **Authenticity verification** - confirms releases come from authorized maintainers via OIDC
- **Integrity assurance** - detects tampering with release artifacts
- **Non-repudiation** - signatures logged in public transparency log (Rekor)
- **No long-lived secrets** - uses short-lived OIDC tokens instead of stored keys

**Verify a signed release**:
```bash
git verify-tag v0.5.2
# Output shows signature from Gitsign with Sigstore certificate chain
```

All release signatures are publicly logged in the [Sigstore Rekor transparency log](https://rekor.sigstore.dev/).

#### ✅ Branch Protection
The main branch is protected with the following rules:
1. **Requires pull requests** - all changes must go through review
2. **Requires approvals** - at least 1 approval required
3. **Dismisses stale reviews** - new commits require new reviews
4. **Requires status checks** - all CI checks must pass
5. **Requires commit signatures** - all commits must be signed
6. **Disallows force pushes** - prevents history rewriting
7. **Disallows deletions** - prevents accidental branch deletion

This multi-layered protection follows the **principle of least privilege**.

#### ℹ️ CII Best Practices Badge
The project meets the criteria for the OpenSSF (formerly CII) Best Practices badge. To view or apply for the badge, visit:

[https://www.bestpractices.dev/](https://www.bestpractices.dev/)

**Project meets these criteria**:
- ✅ Open source license (MIT)
- ✅ Branch protection with code review
- ✅ Signed releases and commits
- ✅ Automated testing with coverage
- ✅ Security scanning and analysis
- ✅ Security policy (SECURITY.md)

## Automated Security Scanning

### CodeQL Static Analysis
- **Trigger**: Every push to main and pull request
- **Purpose**: Detects potential security vulnerabilities in Python code
- **Configuration**: See `.github/workflows/codeql.yml`

### OpenSSF Scorecard Analysis
- **Trigger**: Weekly on Sundays at midnight
- **Purpose**: Evaluates repository for security best practices
- **Configuration**: See `.github/workflows/scorecard.yml`

### OSV-Scanner
- **Trigger**: Every push to main
- **Purpose**: Scans for known open source vulnerabilities
- **Configuration**: See `.github/workflows/osv-scanner.yml`

### Pre-commit Hooks
- **Trigger**: Before each local commit
- **Purpose**: Enforces code quality and security before pushing
- **Tools**:
  - ruff (formatting and linting)
  - pyright (type checking)
  - YAML validation
  - Security checks

## Dependency Management

### Renovate Bot
The project uses [Renovate Bot](https://docs.renovatebot.com/) for automated dependency updates:

- **GitHub Actions**: Updates pinned to commit SHAs
- **Schedule**: Monday after 10pm (off-peak hours)
- **Auto-merge**: Enabled for Dependabot updates
- **Configuration**: See `.renovaterc.json`

### Pinned Action Versions
All GitHub Actions are pinned to their commit SHA for security:
```yaml
- uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8 # v5
```

This prevents supply chain attacks from compromised action versions.

## Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email security details to: [peter@reuteras.net](mailto:peter@reuteras.net)
3. Include the following details:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

See the [full security policy](https://github.com/reuteras/miniflux-tui-py/blob/main/SECURITY.md) for more details.

## Development Security Practices

### Commit Signing
All commits to main must be signed with GPG or SSH keys. This ensures:
- Commits are authentic
- Developers cannot impersonate each other
- Git history is tamper-proof

**Enable commit signing locally**:
```bash
git config user.signingkey <your-key-id>
git config commit.gpgsign true
git config tag.gpgsign true
```

### OIDC Publishing
PyPI publishing uses OpenID Connect (OIDC) for secure, keyless authentication:
- No long-lived credentials stored in secrets
- Time-limited tokens generated per release
- Better auditability and security

See `.github/workflows/publish.yml` for implementation.

## Security Compliance

### Standards & Frameworks
- **OpenSSF Scorecard**: Evaluated regularly
- **CII Best Practices**: Eligible for badge certification
- **OWASP Secure Coding**: Follows OWASP guidelines
- **GitHub Security**: Uses GitHub's security features

### Vulnerability Scanning
- CodeQL for Python-specific issues
- OSV-Scanner for dependency vulnerabilities
- Dependabot for dependency updates
- Renovate for GitHub Actions updates

## Contact

For security questions or concerns, contact the project maintainer:
- **Email**: [peter@reuteras.net](mailto:peter@reuteras.net)
- **GitHub**: [@reuteras](https://github.com/reuteras)

## References

- [OpenSSF Scorecard Documentation](https://github.com/ossf/scorecard)
- [OpenSSF Best Practices Badge](https://www.bestpractices.dev/)
- [GitHub Branch Protection Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [Git Signing Documentation](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
