# Release Guide

This guide documents the **fully automated** release process for miniflux-tui-py. The entire process is handled by GitHub Actions - no local tools or manual steps required!

## Quick Start (TL;DR)

1. Go to: https://github.com/reuteras/miniflux-tui-py/actions/workflows/release.yml
2. Click "Run workflow"
3. Enter version (e.g., `0.5.3`) or choose bump type
4. Click "Run workflow"
5. Done! ☕ (Wait ~10 minutes for full release)

## What Happens Automatically

When you trigger the release workflow, GitHub Actions will:

1. ✅ Create a release branch with version bump and changelog
2. ✅ Create a PR to main
3. ✅ Wait for all CI checks to pass
4. ✅ Auto-merge the PR
5. ✅ Create a signed git tag (using Sigstore Gitsign)
6. ✅ Trigger the publish workflow:
  - Build Python packages (wheel + sdist)
  - Publish to PyPI with attestations
  - Build binaries for Linux, macOS, Windows
  - Generate SBOMs (CycloneDX + SPDX)
  - Sign all artifacts with cosign
  - Generate SLSA provenance
  - **Publish GitHub release** (not a draft!)
  - Mark as "latest" release

**Total time**: ~10-15 minutes from trigger to published release on PyPI and GitHub.

## Detailed Process

### Step 1: Trigger the Release Workflow

Navigate to the Actions tab and run the "Create Release" workflow:

```bash
# Option 1: Via GitHub UI
# Go to: https://github.com/reuteras/miniflux-tui-py/actions/workflows/release.yml
# Click "Run workflow" → Enter version → Run

# Option 2: Via GitHub CLI
gh workflow run release.yml --ref main --field version=0.5.3

# Option 3: Auto-bump with type
gh workflow run release.yml --ref main --field bump_type=patch  # or minor, major
```

### Step 2: Monitor Progress

```bash
# Watch the workflow
gh run watch

# Or check status
gh run list --workflow=release.yml --limit 1
```

The workflow will automatically:
- Create release PR
- Wait for CI to pass
- Merge the PR
- Create signed tag
- Trigger publish workflow

### Step 3: Verify Release

```bash
# Check PyPI
curl -s https://pypi.org/pypi/miniflux-tui-py/json | jq -r '.info.version'

# Check GitHub release
gh release view v0.5.3

# Test installation
pip install miniflux-tui-py --upgrade
```

## Release Artifacts

Each release includes:

### Python Packages
- `miniflux-tui-py-X.Y.Z.tar.gz` - Source distribution
- `miniflux_tui_py-X.Y.Z-py3-none-any.whl` - Wheel

### Standalone Binaries
- `miniflux-tui-linux-x86_64.tar.gz`
- `miniflux-tui-macos.tar.gz`
- `miniflux-tui-windows.zip`

### Security Artifacts
- `*.sig` - Cosign signatures for all artifacts
- `*.sig.bundle` - Signature bundles with certificates
- `*.cdx.json` - CycloneDX SBOMs
- `*.spdx.json` - SPDX SBOMs
- `provenance.json` - SLSA provenance document
- GitHub attestations (build provenance)

### Signatures and Verification

All artifacts are signed using Sigstore cosign with keyless signing (OIDC):

```bash
# Verify a release artifact
cosign verify-blob \
  --bundle miniflux-tui-py-0.5.3.tar.gz.sig.bundle \
  --certificate-identity-regexp "https://github.com/reuteras/miniflux-tui-py" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  miniflux-tui-py-0.5.3.tar.gz

# Verify git tag
git verify-tag v0.5.3
```

## Monitoring & Troubleshooting

### Check Workflow Status

```bash
# List recent runs
gh run list --limit 5

# Watch a specific run
gh run watch <RUN-ID>

# View logs
gh run view <RUN-ID> --log
```

### Common Issues

#### Problem: CI checks fail on release PR

**Solution**: The workflow will stop and the PR won't be merged. Fix the issues, then manually merge the PR or re-run the workflow.

#### Problem: Workflow fails at tag creation

**Solution**: Check if the version already exists. Delete the tag if needed:

```bash
git tag -d vX.Y.Z
git push origin :vX.Y.Z
```

Then re-run the workflow.

#### Problem: Release published but not showing as "latest"

**Solution**: This shouldn't happen anymore (we removed `--draft`), but if it does:

```bash
gh release edit vX.Y.Z --latest
```

### Re-running Failed Workflows

If any job fails, you can re-run it:

```bash
# Re-run entire workflow
gh run rerun <RUN-ID>

# Or via GitHub UI
# Go to Actions → Click on failed run → Re-run all jobs
```

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backwards compatible
- **PATCH** (0.0.X): Bug fixes, backwards compatible

When using `bump_type`:
- `patch`: 0.5.2 → 0.5.3
- `minor`: 0.5.2 → 0.6.0
- `major`: 0.5.2 → 1.0.0

## Security & Signing

### Keyless Signing with Sigstore

The release process uses **Sigstore Gitsign** and **Cosign** for keyless cryptographic signing:

- ✅ **No long-lived secrets** - Uses short-lived OIDC tokens
- ✅ **Automatic transparency log** - All signatures logged publicly
- ✅ **Consistent security** - Same approach for tags and artifacts
- ✅ **Reduced attack surface** - No private keys to manage

### Prerequisites

All signing is automatic! No local setup needed. The workflows require:
1. `id-token: write` permission (already configured)
2. GitHub provides OIDC tokens automatically
3. Gitsign/Cosign use these tokens for signing

### Transparency Logs

All signatures are publicly logged:
- Git tags: [Sigstore Rekor](https://rekor.sigstore.dev/)
- Artifacts: [Sigstore Rekor](https://rekor.sigstore.dev/)
- Attestations: [GitHub](https://github.com/reuteras/miniflux-tui-py/attestations)

## Changelog Generation

Changelogs are automatically generated using [git-cliff](https://git-cliff.org/) based on conventional commits:

### Conventional Commit Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `chore`: Maintenance tasks
- `refactor`: Code refactoring
- `test`: Test changes
- `ci`: CI/CD changes

### Examples

```bash
git commit -m "feat: add dark mode support"
git commit -m "fix: resolve crash on startup"
git commit -m "docs: update installation instructions"
```

## PyPI Trusted Publisher (One-Time Setup)

The first release requires PyPI trusted publisher configuration:

1. Visit https://pypi.org/account/publishing/
2. Add a trusted publisher with:
  - **Project:** `miniflux-tui-py`
  - **Repository owner:** `reuteras`
  - **Repository name:** `miniflux-tui-py`
  - **Workflow filename:** `publish.yml`
  - **Environment:** `pypi`

This is already configured for this project.

## Migration from Old Process

### What Changed?

**Old Process:**
1. Run `uv run scripts/release.py` locally
2. Create PR manually
3. Wait for CI
4. Merge PR manually
5. Run `create-signed-tag.yml` workflow
6. Manually push tag
7. Wait for publish
8. Manually publish draft release

**New Process:**
1. Click "Run workflow" in GitHub UI
2. ☕ Wait ~10 minutes
3. Done!

### Removed Files

The following files are **no longer needed**:
- `scripts/release.py` - Replaced by `release.yml` workflow
- `.github/workflows/create-signed-tag.yml` - Integrated into `release.yml`

### Backwards Compatibility

You can still create releases manually if needed:

```bash
# Manual tag creation (emergency only)
git checkout main
git pull --ff-only
git tag -s vX.Y.Z -m "vX.Y.Z"
git push origin vX.Y.Z
```

This will trigger the publish workflow, but won't have the automatic PR/merge steps.

## Complete Release Checklist

For the paranoid (or those who like checklists):

- [ ] Go to Actions → Create Release workflow
- [ ] Enter version or choose bump type
- [ ] Click "Run workflow"
- [ ] Wait for workflow to complete (~10 min)
- [ ] Verify PyPI has new version
- [ ] Verify GitHub release exists and is published
- [ ] Test installation: `pip install miniflux-tui-py --upgrade`
- [ ] 🎉 Celebrate!

## Timeline

**Total release time: ~10-15 minutes**

1. **Prepare** (1-2 min): Create branch, update version, generate changelog
2. **CI** (3-5 min): Run tests, checks on PR
3. **Merge** (1 min): Auto-merge PR
4. **Publish** (5-7 min): Build, sign, publish to PyPI, create GitHub release

No manual intervention required at any step!


## Prerequisites

### Required Tools

1. **git-cliff** - Automatic changelog generation from conventional commits

```bash
# macOS
brew install git-cliff

# Linux (Cargo)
cargo install git-cliff

# See https://git-cliff.org/docs/installation for other options
```

2. **GitHub CLI** - For triggering workflows

```bash
# macOS
brew install gh

# Linux
# See https://cli.github.com/manual/installation
```

3. **uv** - Python package manager (should already be installed for development)

## Release Process Overview

The release process has **THREE critical stages** that must be completed in order:

1. **Stage 1**: Prepare release PR (version bump + changelog)
2. **Stage 2**: Merge the PR to main (**REQUIRED** - don't skip!)
3. **Stage 3**: Manually push the tag to trigger publish workflow

⚠️ **CRITICAL**: You must merge the release PR before creating the tag, or the build will use the wrong version!

## Stage 1: Prepare Release PR

Run the release script from a clean main branch:

```bash
# Ensure you're on main and up-to-date
git checkout main
git pull --ff-only

# Run the release preparation script
uv run scripts/release.py
```

The script will:
1. ✅ Verify you're on a clean, up-to-date `main`
2. ✅ Run quality gates (pytest, ruff, pyright)
3. ✅ Prompt for the new semantic version (suggests next patch)
4. ✅ Update `pyproject.toml` with new version
5. ✅ Regenerate `uv.lock` to keep dependencies in sync
6. ✅ Use `git-cliff` to auto-generate `CHANGELOG.md` from commits
7. ✅ Open your `$EDITOR` to review/edit the changelog
8. ✅ Create a branch named `release/vX.Y.Z`
9. ✅ Commit version + changelog changes
10. ✅ Push the release branch to origin

**Action Required**: The script will print a URL to create a pull request. Open that URL and create the PR.

## Stage 2: Merge Release PR ⚠️ DO NOT SKIP

**This step is CRITICAL!** The release PR must be merged to main before creating the tag.

```bash
# Wait for CI to pass on the PR, then merge it
gh pr merge <PR-NUMBER> --squash  # or merge via GitHub UI

# After merge, update your local main
git checkout main
git pull --ff-only

# VERIFY the version is correct in main
grep "^version" pyproject.toml
# Should show: version = "X.Y.Z" (your new version)
```

If you skip this step, the build will use the old version from main and upload the wrong version to PyPI!

## Stage 3: Create Tag and Trigger Publish

⚠️ **Important**: The GitHub Actions `create-signed-tag` workflow **CANNOT** trigger the publish workflow due to GitHub's security restrictions (GITHUB_TOKEN doesn't trigger other workflows). You must manually push the tag.

### Option A: Manual Tag Push (Recommended)

```bash
# Ensure you're on the updated main branch
git checkout main
git pull --ff-only

# Create and push the signed tag locally
git tag -s v0.5.3 -m "v0.5.3"
git push origin v0.5.3
```

### Option B: Use Workflow Then Manual Push

```bash
# First, trigger the workflow to create the signed tag
gh workflow run create-signed-tag.yml --ref main --field version=0.5.3

# Wait 30 seconds for it to complete, then manually push
sleep 30
git fetch --tags
git push origin v0.5.3
```

The manual push triggers the `Publish to PyPI` workflow which will:
- ✅ Build distribution packages (wheel + sdist)
- ✅ Publish to PyPI via Trusted Publisher (OIDC)
- ✅ Create binaries for Linux, macOS, Windows
- ✅ Generate SBOMs (CycloneDX + SPDX)
- ✅ Create GitHub Release with all artifacts
- ✅ Generate build attestations

## Monitoring Release Progress

### Check Workflow Status

```bash
# List recent workflow runs
gh run list --limit 5

# Watch a specific run
gh run watch <RUN-ID>

# View run details
gh run view <RUN-ID>
```

### Verify PyPI Publication

```bash
# Check latest version on PyPI
curl -s https://pypi.org/pypi/miniflux-tui-py/json | jq -r '.info.version'

# Or visit: https://pypi.org/project/miniflux-tui-py/
```

### Verify GitHub Release

```bash
# List releases
gh release list --limit 5

# View specific release
gh release view v0.5.3

# Or visit: https://github.com/reuteras/miniflux-tui-py/releases
```

## Troubleshooting

### Problem: Publish workflow didn't trigger after creating tag

**Cause**: GitHub Actions using `GITHUB_TOKEN` don't trigger other workflows (security feature).

**Solution**: Manually push the tag from your local machine:

```bash
git fetch --tags
git push origin vX.Y.Z
```

### Problem: Wrong version published to PyPI

**Cause**: You created the tag before merging the release PR, so main still had the old version.

**Solution**:
1. Delete the incorrect tag and release
2. Merge the release PR
3. Create the tag again

```bash
# Delete tag locally and remotely
git tag -d vX.Y.Z
git push origin :vX.Y.Z

# Delete GitHub release
gh release delete vX.Y.Z

# Merge release PR
gh pr merge <PR-NUMBER> --squash

# Update main and verify version
git checkout main
git pull --ff-only
grep "^version" pyproject.toml

# Create tag again
git tag -s vX.Y.Z -m "vX.Y.Z"
git push origin vX.Y.Z
```

### Problem: Release is in draft state

**Cause**: The release workflow creates drafts by default.

**Solution**: Publish the release manually:

```bash
gh release edit vX.Y.Z --draft=false
```

Or publish via GitHub UI: https://github.com/reuteras/miniflux-tui-py/releases

### Problem: git-cliff fails with template errors

**Cause**: The cliff.toml configuration has syntax errors.

**Solution**: Test git-cliff locally before running release script:

```bash
git-cliff --config cliff.toml --tag 0.5.3 --unreleased
```

## Complete Release Checklist

Use this checklist to ensure you don't miss any steps:

- [ ] Install git-cliff (`brew install git-cliff`)
- [ ] Checkout main and pull latest (`git checkout main && git pull`)
- [ ] Run release script (`uv run scripts/release.py`)
- [ ] Review and edit generated changelog
- [ ] Create PR from the release branch
- [ ] **Wait for CI to pass on the PR**
- [ ] **Merge the release PR** ⚠️ CRITICAL STEP
- [ ] Update local main (`git checkout main && git pull`)
- [ ] **Verify version in pyproject.toml** (`grep "^version" pyproject.toml`)
- [ ] Create and push tag (`git tag -s vX.Y.Z -m "vX.Y.Z" && git push origin vX.Y.Z`)
- [ ] Wait for publish workflow to complete (~3 minutes)
- [ ] Verify PyPI has new version
- [ ] Verify GitHub release exists
- [ ] If release is draft, publish it (`gh release edit vX.Y.Z --draft=false`)
- [ ] Test installation: `pip install miniflux-tui-py --upgrade`

## Release Timeline

Typical release timeline:

1. **Stage 1** (5-10 min): Run release script, create PR
2. **Stage 2** (2-5 min): CI passes, merge PR
3. **Stage 3** (3-5 min): Push tag, publish workflow completes

**Total**: ~10-20 minutes from start to PyPI publication

## Keyless Signing with Sigstore

The release workflow uses **Sigstore Gitsign** for keyless cryptographic signing. This provides:

- ✅ **No long-lived secrets** - Uses short-lived OIDC tokens (valid only during workflow execution)
- ✅ **Automatic transparency log** - All signatures are logged in Sigstore's public transparency log
- ✅ **Consistent security** - Aligns with existing Cosign usage for artifact signing
- ✅ **Reduced attack surface** - No private keys to rotate or store in secrets

### Prerequisites

1. The workflow requires `id-token: write` permission (already configured)
2. GitHub automatically provides OIDC tokens to workflows
3. Gitsign detects these tokens and generates signing certificates via Fulcio

### Verifying Signed Tags

To verify a Gitsign-signed tag:

```bash
# Verify tag signature
git verify-tag v0.5.2

# View signature details
git show --show-signature v0.5.2
```

All signatures are publicly logged in the [Sigstore Rekor transparency log](https://rekor.sigstore.dev/).

## What GitHub Actions Handles

Triggered by a `v*.*.*` tag, the workflow:

1. **Build job**
    - Checks out the repository
    - Runs ruff, pyright, and pytest
    - Builds the source distribution and wheel with `uv build`
2. **Publish job**
    - Publishes the distributions to PyPI using the Trusted Publisher integration
3. **Binaries job**
    - Builds standalone executables for Linux, macOS, and Windows
    - Uploads the binary archives as artifacts
4. **Release job**
    - Downloads all artifacts
    - Generates SBOMs (CycloneDX and SPDX) via Syft
    - Attaches distributions, binaries, and SBOMs to the GitHub release
    - Generates build attestations

Monitor progress at <https://github.com/reuteras/miniflux-tui-py/actions>.

## PyPI Trusted Publisher Setup (One-Time)

Ensure PyPI trusts the workflow before your first tag-triggered release:

1. Visit <https://pypi.org/account/publishing/>.
2. Add a trusted publisher with:
    - **Project:** `miniflux-tui-py`
    - **Repository owner:** `reuteras`
    - **Repository name:** `miniflux-tui-py`
    - **Workflow filename:** `publish.yml`
    - **Environment:** `pypi`

## Fallback / Manual Steps

- If the signed-tag workflow fails in GitHub Actions, press "Re-run all jobs" or:
  ```bash
  gh run rerun <run-id>
  ```
- To create a tag locally in an emergency (only if the workflow is unavailable):
  ```bash
  git checkout main
  git pull --ff-only
  git tag -s vX.Y.Z -m "vX.Y.Z"
  git push origin vX.Y.Z
  ```
  **Note:** Local tags will use your personal signing key (SSH or GPG) rather than Gitsign. This is acceptable for emergency releases, but prefer the automated workflow for consistent provenance.

The publish workflow can be re-run from the GitHub Actions UI if needed.
