# Branch Protection Configuration

This document describes the branch protection rules for the `main` branch.

## Current Configuration

### Required Status Checks
- **MegaLinter** - Comprehensive code quality and security checks
- **Check Issue Link** - Ensures all PRs are linked to issues

### Pull Request Requirements
- ✅ Require pull request before merging
- ✅ **Require 1 approving review** (from the maintainer)
- ✅ Dismiss stale reviews when new commits are pushed
- ✅ **Require last push approval** (prevents self-approval)
- ✅ Enforce restrictions for administrators
- ✅ Require signed commits
- ✅ Require linear history (no merge commits)

### Security Score
- **OpenSSF Scorecard Branch-Protection**: Addresses alert #293
- All recommended protections enabled

## Branch Protection Rules

### 1. All Changes via Pull Requests

**Rationale**: Ensures all code goes through CI/CD and is reviewable.

**Implementation**:
```bash
gh api -X PUT repos/reuteras/miniflux-tui-py/branches/main/protection \
  --input - << 'EOF'
{
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "require_last_push_approval": true,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "enforce_admins": true,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_signatures": true,
  "required_status_checks": {
    "strict": true,
    "contexts": ["MegaLinter", "Check Issue Link"]
  }
}
EOF
```

### 2. Required Status Checks

#### MegaLinter
- Runs comprehensive linting across multiple languages
- Checks security issues with multiple scanners
- Validates configuration files
- Ensures code quality standards

#### Check Issue Link
- Ensures PRs reference related issues
- Format: `Fixes #123`, `Closes #456`, `Related to #789`
- Exemptions:
  - Dependabot PRs (auto-generated)
  - Renovate PRs (auto-generated)
  - Release PRs (prefixed with `chore: Release` or `Release v`)

### 3. Required Signatures

All commits to `main` must be signed (GPG, SSH, or S/MIME).

**Why**: Cryptographic verification of commit authorship.

### 4. Linear History

Merge commits are not allowed. Use squash or rebase merges only.

**Why**: Keeps git history clean and easy to follow.

### 5. Enforce for Administrators

Even admins must follow the protection rules.

**Why**: Consistency and accountability for all contributors.

## Issue Linking Requirement

### Workflow: `.github/workflows/require-issue-link.yml`

This workflow ensures every PR is linked to an issue, enabling:
- Automatic issue closing when PRs merge
- Better tracking of work and context
- Clear relationship between problems and solutions

### Acceptable Formats

In PR title or body:
- `Fixes #123` - Closes issue when PR merges
- `Closes #456` - Closes issue when PR merges
- `Resolves #789` - Closes issue when PR merges
- `Addresses #100` - Closes issue when PR merges
- `Related to #200` - Doesn't close, but links

### Auto-Exemptions

The following are automatically exempted from issue linking:
1. **Dependabot PRs** - Automated dependency updates
2. **Renovate PRs** - Automated dependency management
3. **Release PRs** - Automated release preparation
4. **Bot PRs** - Other automation (step-security-bot, etc.)

## Verification

Check current branch protection:

```bash
# Full protection status
gh api repos/reuteras/miniflux-tui-py/branches/main/protection | jq

# Just required checks
gh api repos/reuteras/miniflux-tui-py/branches/main/protection \
  --jq '.required_status_checks.contexts'

# Just PR requirements
gh api repos/reuteras/miniflux-tui-py/branches/main/protection \
  --jq '.required_pull_request_reviews'
```

## Updating Branch Protection

**Important**: Changes to branch protection should be made through the GitHub UI or API, not through workflows.

### Via GitHub UI

1. Go to: Settings → Branches → Edit `main` protection rule
2. Update settings as needed
3. Save changes

### Via GitHub CLI

```bash
# Example: Add new required status check
gh api -X PATCH repos/reuteras/miniflux-tui-py/branches/main/protection/required_status_checks \
  --field contexts[]='MegaLinter' \
  --field contexts[]='Check Issue Link' \
  --field contexts[]='New Check Name' \
  --field strict=true
```

## Best Practices

### For Contributors

1. **Always create an issue first** (unless it's a tiny typo fix)
2. **Link your PR to the issue** using keywords in title/body
3. **Ensure all status checks pass** before requesting review
4. **Sign your commits** (configure GPG or SSH signing)
5. **Keep PRs focused** - one issue per PR when possible

### For Maintainers

1. **Don't bypass protection rules** (even though you can)
2. **Use squash merges** to maintain linear history
3. **Wait for all checks** before merging
4. **Review the issue context** before merging PRs

## Troubleshooting

### "Required status check is not passing"

- Check the workflow logs in the "Checks" tab
- Fix the issues identified
- Push new commits (checks will re-run)

### "No issue reference found"

- Add `Fixes #123` to PR description
- Or reference the PR in an issue
- Or create an issue first, then link it

### "Signature verification failed"

- Configure commit signing: https://docs.github.com/en/authentication/managing-commit-signature-verification
- Re-sign commits if needed: `git commit --amend --signoff`

## Security Considerations

Branch protection helps enforce:
- ✅ Code review (even if not strictly required)
- ✅ Automated testing and validation
- ✅ Security scanning (via MegaLinter)
- ✅ Traceability (issue linking)
- ✅ Authenticity (signed commits)
- ✅ Clean history (linear, no force pushes)

These protections significantly reduce the risk of:
- Accidental or malicious code introduction
- Security vulnerabilities
- Breaking changes without review
- Lost context or undocumented changes

## References

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [require-issue-link.yml](.github/workflows/require-issue-link.yml) - Our issue linking workflow
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
