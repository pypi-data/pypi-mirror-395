# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [0.7.4] - 2025-12-07

### BUG FIXES

- Add automatic reconnection on stale connection errors (#644)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.7.3] - 2025-12-01

### BUG FIXES

- Improve link highlighting visibility in entry reader using CSS-based widget focus (#605)
- remove double scrollbar in settings screen (#606)
- Restore non-blocking sync and fix theme switching to use Textual… (#611)
- Pin CodeQL actions to commit SHA (#636)

### DOCUMENTATION

- Clean up outdated development documentation (#597)

### FEATURES

- Respect group_collapsed config when toggling group modes (#599)
- Implement visual link highlighting and improved scrolling for entry reader (#609)
- Implement runtime theme switching and incremental feed sync (#610)

### MAINTENANCE

- Release v0.7.3 (#600)
- bump peter-evans/create-pull-request from 7.0.8 to 7.0.9 (#617) 🤖
- bump google/osv-scanner-action/.github/workflows/osv-scanner-reusable.yml (#618) 🤖
- bump zizmorcore/zizmor-action from 0.2.0 to 0.3.0 (#626) 🤖
- bump coverallsapp/github-action from 2.3.6 to 2.3.7 (#624) 🤖
- bump actions/checkout from 5.0.0 to 6.0.0 (#623) 🤖
- bump actions/dependency-review-action (#621) 🤖
- bump chainguard-dev/actions from 1.5.7 to 1.5.10 (#630) 🤖
- bump astral-sh/setup-uv from 7.1.2 to 7.1.4 (#632) 🤖
- pin CodeQL action versions with commit hashes (#637)
- Release v0.7.3 (#638)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant), dependabot[bot] (Dependencies)
## [v0.7.2] - 2025-11-17

### BUG FIXES

- Add missing ID to Markdown widget to fix NoMatches error (#594)

### MAINTENANCE

- Release v0.7.2 (#595)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.7.1] - 2025-11-17

### BUG FIXES

- Prevent immutable release error in publish workflow (#591)

### FEATURES

- Dark/Light theme toggle for v0.7.0 (#579)

### MAINTENANCE

- bump actions/dependency-review-action (#580) 🤖
- bump docker/setup-qemu-action from 3.6.0 to 3.7.0 (#582) 🤖
- bump step-security/harden-runner from 2.13.1 to 2.13.2 (#584) 🤖
- Use uv tool install for pre-commit in workflow (#587)
- pre-commit autoupdate (#588)
- Release v0.7.0 (#589)
- Release v0.7.1 (#592)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant), dependabot[bot] (Dependencies)
## [v0.6.5] - 2025-11-16

### BUG FIXES

- Enhance scorecard workflow to properly detect branch protection rules (#558)
- Fix unawaited coroutine in EntryHistoryScreen causing non-deterministic test failures (#559)
- Add missing Scorecard configuration file (#560)
- Connect FeedSettingsScreen to entry reader X key binding (#562)
- Make mutation testing failures visible without blocking pytest (#563)
- Implement comprehensive SafeHeader watcher-based exception handling for Windows Python 3.11+ (#566)
- Resolve CodeQL alert about unreachable code in test_api_call_handles_generic_exception (#565)
- Fix unreachable code in test_api_call_handles_generic_exception (CodeQL alert #309) (#567)
- Fix TextArea visibility in FeedSettingsScreen (#568)
- Fix mutation testing configuration and workflow (#571)
- Replace SafeHeader with standard Header in all screens (#572)
- Return error code 1 when --check-config password command fails (#577)

### FEATURES

- Phase 11 - UX Polish & Documentation (Full Scope) (#557)

### MAINTENANCE

- Disable automatic container builds on every commit (#570)
- Release v0.6.5 (#578)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.6.4] - 2025-11-14

### BUG FIXES

- Apply SafeHeader to all screens that use Header widget (#536)

### MAINTENANCE

- Release v0.6.4 (#537)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.6.3] - 2025-11-14

### BUG FIXES

- Add SafeHeader widget to handle Windows Header lifecycle issues (#532)
- Correct SafeHeader._on_mount implementation to properly catch NoMatches (#534)

### MAINTENANCE

- Release v0.6.3 (#535)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.6.2] - 2025-11-14

### BUG FIXES

- Resolve intermittent race condition in grouping and sorting test (#526)
- Correct group statistics display when navigating between entries in grouped feeds (#528)
- Handle widget lifecycle exceptions in _get_entry_list_screen (#529)

### FEATURES

- Clean application heading and fix group statistics display (#527)

### MAINTENANCE

- Release v0.6.1 (#525)
- Release v0.6.2 (#530)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.6.1] - 2025-11-13

### BUG FIXES

- Exclude timing attack false positive for config.py password error check (#513)
- Exclude timing attack false positives in test files (#514)
- Remove duplicate and malformed docstring in config.py (#517)
- Correct header title alignment from center to left (#518)
- Resolve code quality errors in analyzer, security, and config modules (#519)
- Replace grep -c with wc -l in complexity check for cross-platform CI compatibility (#520)
- Move entry count statistics from subtitle to feed header row (#521)
- Display feed statistics row on all entries in grouped mode and mark as read on open (#523)

### FEATURES

- Add group statistics to entry reader view (#522)

### MAINTENANCE

- bump google/osv-scanner-action/.github/workflows/osv-scanner-reusable.yml (#503) 🤖
- Update pre-commit hooks and cleanup code formatting (#507)
- Release v0.6.1 (#524)

### REFACTORING

- Reduce SecureFetcher.fetch complexity from 33 to acceptable level (#510)
- Fix remaining 5 complexity issues in config, security, and analyzer (#511)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant), dependabot[bot] (Dependencies)
## [v0.6.0] - 2025-11-09

### BUG FIXES

- prevent cursor position mismatch on startup (#490)

### FEATURES

- add Tailscale support to GitHub Codespaces (#489)

### MAINTENANCE

- Update roadmap priorities for v0.7.0 features (#500)
- Release v0.6.0 (#502)

### TESTING

- add comprehensive tests for codespace configuration (#488)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.16] - 2025-11-07

### BUG FIXES

- correct pytest path for VS Code test discovery (#483)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.15] - 2025-11-07

### MAINTENANCE

- Release v0.5.15 (#482)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.14] - 2025-11-07

### BUG FIXES

- resolve ruff linting errors in settings screens (#476)
- resolve pyright type errors in test files (#480)

### FEATURES

- add group/category counter in entry reader header (#477)

### MAINTENANCE

- Release v0.5.13 (#478)
- Release v0.5.14 (#479)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.13] - 2025-11-07

### FEATURES

- implement user settings management with edit dialog (#471)

### MAINTENANCE

- Release v0.5.13 (#475)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.12] - 2025-11-07

### BUG FIXES

- Enable git credentials persistence in release workflow (#466)
- re-add persist-credentials false to all checkouts (#468)
- configure Codespaces to auto-activate Python venv (#469)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.11] - 2025-11-05

### BUG FIXES

- Enable git credentials persistence in release workflow (#462)
- Remove paths filter from CodeQL push trigger for 10/10 SAST score (#463)
- prevent credential persistence in GitHub Actions (#465)

### FEATURES

- Add multi-account PR approval automation script (#461)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.10] - 2025-11-05

### MAINTENANCE

- Release v0.5.10 (#459)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.8] - 2025-11-05

### BUG FIXES

- replace overly broad exception handlers with specific exception types (#452)
- suppress pyright import errors for textual_image on Python 3.14+ (#454)

### MAINTENANCE

- Release v0.5.8 (#456)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.7] - 2025-11-05

### BUG FIXES

- enable manual triggering and automatic chaining of publish workflow (#447)

### MAINTENANCE

- migrate semgrep workflow from pip to uv (#448)
- migrate semgrep workflow from pip to uv (#449)
- Release v0.5.7 (#451)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.6] - 2025-11-05

### BUG FIXES

- use SCORECARD_TOKEN instead of GITHUB_TOKEN for scorecard action (#430)
- make release workflow PR creation more robust (#436)
- ensure release PR is fully merged before creating tag (#438)
- enable auto-merge and poll for PR merge completion in release workflow (#441)
- add Gitsign commit signing to release workflow (#442)
- handle PR number suffix in release commit message validation (#444)
- enable auto-merge and poll for PR merge completion in release workflow (#445)

### DOCUMENTATION

- improve license compliance for OpenSSF Scorecard 10/10 (#435)
- update branch protection and CODEOWNERS for perfect Scorecard 10/10 (#434)

### FEATURES

- fully automate release process (#431)
- add keyboard navigation for links in entry reader (#439)
- add image display support in entry reader (#433)

### MAINTENANCE

- update all Python dependencies and pre-commit hooks (#428)
- Release v0.5.9 (#437)
- Release v0.5.6 (#440)
- Release v0.5.6 (#443)
- Release v0.5.6 (#446)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.5] - 2025-11-04

### BUG FIXES

- Remove hash-based container tags and add release notes (#400)
- Disable Red Hat YAML telemetry prompts in Codespaces (#402)
- Improve Codespaces configuration for test discovery (#404)
- Add scraping helper (Shift+X) to entry reader screen (#408)
- Change scraping helper binding from shift+x to X (#409)
- Change scraping helper binding from shift+x to X (#409) (#411)
- improve content scraper UI layout (#421)
- add extra pause in test to wait for loading screen (#422)
- change shift+key bindings to uppercase keys (#424)
- resolve MegaLinter formatting warnings (#425)

### CI/CD

- ensure detached signatures uploaded (#417)
- restrict workflow token permissions (#416)
- add Python 3.14 to test matrix (#420)

### DOCUMENTATION

- Add comprehensive scraping helper feature documentation
- add last commit badge to README (#419)

### FEATURES

- Interactive scraping rule helper for content extraction (#405)
- Integrate scraping helper into entry list (closes #391) (#406)
- Add ASCII art loading screen on startup (#418)
- add __main__.py module and clarify running methods (#426)
- add automatic pagination for >100 entries and fix arrow key navigation (#427)

### MAINTENANCE

- Release v0.5.5 (#429)

### TESTING

- Phase 2 - Comprehensive UI screen tests (#391) (#403)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.4] - 2025-11-03

### DOCUMENTATION

- Comprehensively document release process (#397)

### MAINTENANCE

- Release v0.5.3 (#396)
- Release v0.5.4 (#399)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.3] - 2025-11-03

### BUG FIXES

- Address remaining 10 code scanning security alerts (#329)
- Resolve remaining code scanning security alerts to achieve zero alerts (#332)
- Add dependabot[bot] to auto-approve workflow to fix auto-merge (#348)
- Restrict auto-merge to verified dependabot[bot] account type (#349)
- Resolve cyclic import warnings with Protocol-based app interface (#353)
- Exclude CodeQL config from YAML v8r schema validation (#355)
- Exclude .yaml-lint.yml from YAML v8r schema validation (#357)
- Remove ellipsis statements from Protocol methods to resolve code scanning alerts (#359)
- Clean up Codespaces configuration (#361)
- Use raise NotImplementedError in Protocol methods (#363)
- Configure VS Code to run pytest via uv in Codespaces (#364)
- Exclude problematic YAML files from v8r schema validation (#368)
- Add pytest path to workspace settings for reliable test discovery (#369)
- Use unique coverage filenames to prevent overwriting during merge (#371)
- Set VALIDATE_ALL_CODEBASE to true in MegaLinter (#374)
- Add pull-requests write permission for coverage comments (#378)
- Update VS Code test plugin configuration for proper pytest discovery
- Set VALIDATE_ALL_CODEBASE to true in MegaLinter (#374)
- Add pull-requests write permission for coverage comments (#378)
- Enable editorconfig-checker in pre-commit hooks (#380)
- Add final newline to .vscode/settings.json
- Remove merge-multiple to preserve coverage data files (#381)
- Start groups collapsed when toggling group by category/feed (#383)
- Remove Python 3.14 from test matrix (#389)
- Rewrite history screen to extend EntryListScreen and sort by read time (#390)
- Copy .coverage file for python-coverage-comment-action (#393)
- Run coverage-report job only on PRs, not main pushes (#394)
- Require git-cliff and fix configuration (#395)

### FEATURES

- Auto-close Dependabot tracking issues when PRs are merged (#347)
- Add comprehensive GitHub labels configuration (#372)
- Enhance pre-commit checks to catch more errors before CI (#377)
- Enhance pre-commit checks to catch more errors before CI (#377)
- Replace custom changelog generator with git-cliff (#385)

### MAINTENANCE

- bump actions/setup-python from 5.1.0 to 6.0.0 (#338) 🤖
- bump actions/github-script from 7.0.1 to 8.0.0 (#339) 🤖
- bump actions/checkout from 4.2.2 to 5.0.0 (#344) 🤖
- bump chainguard-dev/actions (#342) 🤖
- Increase dependabot cooldown from 1 to 4 days (#351)
- Use "explicit" instead of true for VS Code code actions (#373)

### REFACTORING

- Rename MinifluxTUI class to MinifluxTuiApp for clarity (#336)
- Use uvx for tool execution instead of pip install + run (#346)

### TESTING

- Add key binding tests and coverage analysis (#392)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant), dependabot[bot] (Dependencies)
## [v0.5.2] - 2025-11-02

### BUG FIXES

- Remove --system flag from pip-licenses installation in license check (#323)
- Address GitHub code scanning security alerts (#326)

### MAINTENANCE

- Release v0.5.2 (#320)

### SECURITY

- Replace GPG signing with Sigstore Gitsign for keyless signing (#324)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.5.1] - 2025-11-02

### BUG FIXES

- Prioritize version tags over commit SHA in Docker container builds (#225)
- Remove commit SHA tags from Docker container images (#228)
- Fix grouping by category expand/collapse and improve keybinding UX (#233)
- Update Renovate config to extend shared preset and add missing managers (#254)
- Update Renovate config to extend shared preset and fix GitHub Actions hashing (#254) (#255)
- Use generateSarif parameter for Semgrep output (#259)
- Correct datetime handling in entry_history.py (Issue #260) (#261)
- Remove configurationFile parameter from Renovate workflow
- Add RENOVATE_CONFIG_FILE environment variable to workflow
- Add RENOVATE_REPOSITORIES env var to explicitly specify repo (#267)
- Resolve pyright type errors in entry_history.py (#271)
- Add pytest-benchmark to dev dependencies (#272)
- Add workflows permission to Renovate job (#269)
- Update GitHub Actions workflows for compatibility (#273)
- Add vulnerability alerts permission and configuration to Renovate (#274)
- Wrap bare URLs in angle brackets for markdown linting compliance (#277)
- Fix YAML and markdown linting violations across workflows and templates (#279)
- Add markdown-link-check ignore patterns for dead links (#280)
- Resolve MegaLinter validation failures (#281) (#282)
- Resolve Renovate dependency issues and code quality problems (#283)
- Enable all Renovate dependency updates without schedule delays (#285)
- Remove external Renovate config override and use immediate schedules (#268) (#286)
- Fix Renovate PR creation with BOT_TOKEN and config fixes (#287)
- Enable Renovate PR recreation for merged PRs (#268) (#289)
- Remove invalid configuration option blocking Renovate (#291)
- Remove invalid Renovate configuration options (#299)
- Remove remaining invalid configuration options from Renovate and Dependabot (#301)
- Enable Dependabot auto-merge for all dependency updates (#306)
- guard entry browser launches against unsafe URLs (#312)
- address outstanding code scanning alerts (#314)

### CI/CD

- Add workflow to retroactively add bot reviews to closed PRs (#231)

### DOCUMENTATION

- Update roadmap to reflect v0.5.0 release completion
- Update roadmap to reflect v0.5.0 release completion (#248)

### FEATURES

- Add cosign signing and SLSA provenance to release workflow (#230)
- Add Semgrep SAST security scanning (#241)
- Replace Super-Linter with MegaLinter (#242)
- Add Coveralls and GitHub Pages for coverage tracking (#240)
- Implement user settings management screen (Issue #57) (#249)
- Add license compliance checking workflow (#250)
- Add Renovate workflow for automated dependency updates
- Implement entry history view screen (Issue #56) (#253)
- Add code complexity analysis to CI (#251)
- Add performance benchmarking with pytest-benchmark (#257)
- Add coverage differential and parallel testing (#258)
- Enhance CodeQL and add pip-audit to dependency review (#266)
- Add mutation testing for test quality verification (#252)
- Configure Renovate to group all updates into single PR with labels (#297)
- Add Dependabot PR to Issue tracker workflow (#304)

### FIX

- Add category header enter key support for consistent grouping behavior (#244)

### MAINTENANCE

- Improve Renovate configuration for better dependency management (#246)
- Remove Codecov and archive workflow improvements (#270)
- Update docker/dockerfile Docker tag to v1.19 (#293)
- migrate config .renovaterc.json (#296)
- Update mcr.microsoft.com/devcontainers/python Docker tag to v3.14 (#294)
- Update ghcr.io/astral-sh/uv:latest Docker digest to ba4857b (#292)
- bump coverallsapp/github-action from 2.3.0 to 2.3.6 (#302) 🤖
- Pin GitHub Actions to commit hashes with version comments (#309)
- bump oxsecurity/megalinter from 8 to 9 (#303) 🤖
- Release v0.5.1 (#315)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant), dependabot[bot] (Dependencies)
## [v0.5.0] - 2025-11-01

### BUG FIXES

- Create release as draft to allow asset uploads
- Force refresh of OpenSSF Best Practices badge cache
- Remove path filters from linter.yml to ensure build check runs (#219)
- Add explanatory comment to empty except clause (#218)
- Enable malcontent to run on all PRs (#222)

### DOCUMENTATION

- Improve scorecard workflow comments for clarity

### FEATURES

- Add sponsorship support and improved badges
- Comprehensive developer experience improvements
- Phase 1 feed management with security hardening (#58) (#215)
- Phase 2 - Comprehensive category management implementation (#216)
- Implement v0.5.0 category support and feed management enhancements (#217)

### MAINTENANCE

- Add auto-approve workflow for solo developer (#212)
- Configure Renovate for dependency automation (#214)
- Release v0.5.0 (#224)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.22] - 2025-10-31

### BUG FIXES

- use correct syft flags --source-name and --source-version 🤖
- Wrap bare email URL in angle brackets for markdown linting

### DOCUMENTATION

- Add SUPPORT.md community health file 🤖

### FEATURES

- Add GitHub issue templates for bugs and features 🤖

### MAINTENANCE

- Release v0.4.22



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.21] - 2025-10-30

### MAINTENANCE

- Release v0.4.21



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.20] - 2025-10-30

### BUG FIXES

- use syft flags supported by v1.36.0 (#200)

### CI/CD

- add malcontent diff workflow (#198)
- disable credential persistence in malcontent workflow (#199)

### MAINTENANCE

- bump syft to v1.46.1
- Release v0.4.20



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.19] - 2025-10-30

### MAINTENANCE

- Release v0.4.19 (#197)

### DX

- make codespaces testing-ready out of the box (#194)

### SECURITY

- resolve remaining code scanning alerts (#195)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.18] - 2025-10-29

### CI/CD

- improve sbom generation and release reruns (#188)

### MAINTENANCE

- Release v0.4.18 (#189)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.17] - 2025-10-29

### CI/CD

- ensure release sbom step handles binary artifacts (#185)

### MAINTENANCE

- Release v0.4.16 (#186)
- Release v0.4.17 (#187)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.15] - 2025-10-29

### BUG FIXES

- detect branch protection in release
- detect branch protection in release (#180)
- detect branch protection in release (#182)

### MAINTENANCE

- Release v0.4.14 (#183)
- Release v0.4.15 (#184)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.12] - 2025-10-29

### BUG FIXES

- surface git push failures
- satisfy lint and add healthcheck
- handle tomllib type errors in config parsing
- address code scanning alerts (#179)

### CI/CD

- run uv sync with locked lockfile
- tighten publish workflow token permissions (#143)
- remove unsupported editorconfig options
- add CIFuzz workflow and configuration fuzz target
- avoid installing fuzz extras in docs workflow
- install clang for fuzzing workflow
- quote fuzz extras install
- update cifuzz action pins
- limit workflows to relevant paths (#165)
- expand security coverage (#166)
- fix gitleaks and zizmor regressions (#175)

### FEATURES

- load api token via password command (#177)
- load api token via password command (#178)

### MAINTENANCE

- sync uv metadata after release
- align uv lockfile with project version
- refresh container base image tooling
- restore unreleased changelog section
- fix CIFuzz workflow and docs indentation
- bump actions/attest-build-provenance from 1.4.4 to 3.0.0 (#168) 🤖
- migrate config .renovaterc.json (#176) 🤖
- Release v0.4.12



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant), dependabot[bot] (Dependencies), renovate[bot] (Dependencies)
## [v0.4.9] - 2025-10-28

### CI/CD

- align container image publishing

### FEATURES

- publish signed container image
- publish standalone binaries

### MAINTENANCE

- Release v0.4.9
- Release v0.4.9



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.11] - 2025-10-28

### MAINTENANCE

- Release v0.4.11



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.8] - 2025-10-28

### BUG FIXES

- Add attestations:write permission for GitHub attestations

### MAINTENANCE

- Release v0.4.8



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.7] - 2025-10-28

### BUG FIXES

- Correct release title and add GitHub attestations

### MAINTENANCE

- Release v0.4.7



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.6] - 2025-10-28

### BUG FIXES

- bump dependency floors to resolve security alerts
- Resolve grouped mode, feed sort, and shift+G issues
- Resolve linting issues in test file
- Resolve markdown linting issues
- resolve version lookup issues
- harden version lookup metadata fallback
- continue metadata lookup after errors
- address new lint rules
- Correct markdown list indentation for MD007 linter
- Use 4-space indentation for markdown sub-lists
- Use jsDelivr CDN for logo to avoid rate limits
- Remove broken SLSA provenance job from publish workflow
- remove trailing blank lines from checklists
- Standardize macOS config path to ~/.config
- Set restrictive top-level permissions in pre-commit workflow

### DOCUMENTATION

- fix README logo URL (#107)
- use shields.io PyPI badge (#108)
- add comprehensive manual testing checklists for releases (#109)

### MAINTENANCE

- autoupdate pre-commit hooks
- Release v0.4.6

### TESTING

- Add comprehensive tests for patch release fixes
- fix formatting in utils tests
- Update macOS config path test to expect ~/.config



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.5] - 2025-10-27

### BUG FIXES

- Update Renovate SLSA constraint to only allow versions <=2.0.0 (#88)
- Replace example.com with localhost in tests to prevent DNS lookups (#94)
- break cyclic import for CodeQL (#106)

### CI/CD

- harden workflows per zizmor findings (#102)
- allow manual zizmor runs (#105)

### DOCUMENTATION

- Add comprehensive release process section to AGENT.md (#100)

### FEATURES

- Implement feed-specific refresh for v0.5.0 (Issue #55) (#93)
- Add feed status screen showing server info and problematic feeds (#104)

### MAINTENANCE

- Configure Renovate to exclude SLSA v2.1.0
- Update Renovate to exclude only SLSA v2.1.0
- Configure Renovate to exclude SLSA v2.1.0 (#87)
- Bump actions/checkout from 4.3.0 to 5.0.0 (#89) 🤖
- Bump github/codeql-action from 3.31.0 to 4.31.0 (#90) 🤖
- Bump astral-sh/setup-uv from 7.1.1 to 7.1.2 (#92) 🤖
- align agent guide and entry list tests (#96)
- repo housekeeping and headless smoke test (#97)
- repo housekeeping and headless smoke test (#101)
- Release v0.4.5



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant), dependabot[bot] (Dependencies)
## [v0.4.4] - 2025-10-26

### BUG FIXES

- Improve system information widget update in help screen
- Use SLSA action v2.1.0 version tag instead of invalid commit SHA
- Downgrade SLSA action to v2.0.0 (v2.1.0 has incompatible directory structure)

### MAINTENANCE

- Release v0.4.4



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.4.3] - 2025-10-26

### BUG FIXES

- Improve Scorecard Branch-Protection detection (#82)
- Correct PyPI publish action reference

### DOCUMENTATION

- Add OpenSSF Security Scorecard improvements documentation (#77)
- Add OpenSSF Best Practices badge to README (#83)

### FEATURES

- Add application and server version display (Issue #59) (#80)
- Add SLSA provenance generation for signed releases (#81)

### MAINTENANCE

- Update slsa-framework/slsa-github-generator action to v2.1.0 (#84) 🤖
- Update version to 0.4.3 and update CHANGELOG



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant), renovate[bot] (Dependencies)
## [v0.4.1] - 2025-10-26

### BUG FIXES

- Remove unsafe curl | sh installation pattern from documentation
- Resolve markdown and YAML linting errors
- Resolve bare URL in markdown documentation
- Handle list response from official miniflux client's get_categories()
- Update OpenSSF Scorecard action to valid version @v2.4.1
- Resolve OpenSSF Scorecard and ruff linting issues
- Resolve OpenSSF Scorecard, ruff linting, and CodeQL security alerts
- Resolve OpenSSF Scorecard, ruff linting, and all CodeQL security alerts (#67)
- Replace invalid action SHAs with valid version tags in main branch
- Move workflow permissions to job-level for better scope management
- Use @release/v1 for pypa/gh-action-pypi-publish

### CI/CD

- Set up Release Drafter for automated release notes

### DOCUMENTATION

- Add comprehensive release process documentation
- Add comprehensive feature roadmap for v0.5.0 and beyond
- Add comprehensive Git workflow documentation to CLAUDE.md

### FEATURES

- Comprehensive project quality and security improvements
- Add Category model and API methods for v0.5.0
- Add Category UI support foundation for v0.5.0
- Add refresh all feeds operation for v0.5.0 (Issue #55)
- Add feed management API methods for v0.5.0 (Issue #58) (#66)
- Pin GitHub Actions to commit SHAs and add Renovate for automation
- Pin GitHub Actions to commit SHAs and add Renovate for automation (#68)

### MAINTENANCE

- Update GitHub Actions (#75) 🤖
- Pin dependencies (#74) 🤖

### REFACTORING

- Rename renovate config to .renovaterc.json and remove docker rules (#76)

### SECURITY

- Complete security alert remediation - Renovate + TokenPermissions review (#69)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant), renovate[bot] (Dependencies)
## [v0.4.0] - 2025-10-26

### BUG FIXES

- Add type ignore for memoize_with_ttl cache attribute access
- Resolve markdown linting errors in documentation
- Properly add language specifiers to all bare code blocks

### DOCUMENTATION

- Add comprehensive testing, architecture, and patterns guides

### FEATURES

- Add search functionality to EntryListScreen (#50)
- Add comprehensive tests for theme configuration (#51)

### MAINTENANCE

- Prepare v0.4.0 release

### TESTING

- Add integration tests for entry_list.py (52% → 64% coverage)
- Add 24 integration tests for entry_reader.py (56% → 65%) (#49)



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.3.0] - 2025-10-26

### FEATURES

- Achieve 100% test coverage for ui/app.py (90% → 100%)

### MAINTENANCE

- Release v0.3.0 - Comprehensive test suite and production readiness

### TESTING

- Significantly improve test coverage for entry_reader and app screens
- Achieve 100% coverage for help.py and performance.py
- Add event handler and action method existence tests for entry_list.py
- Add action method and helper tests for entry_reader.py



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.2.9] - 2025-10-26

### BUG FIXES

- Add type hints to test assertions for mypy compliance

### FEATURES

- Apply retry logic to all API client methods
- Apply consistent error handling to entry_list screen
- Extract repeated code patterns from screens
- Refactor long functions for improved readability

### MAINTENANCE

- Release v0.2.9

### TESTING

- Add comprehensive tests for cursor position restoration
- Add 22 comprehensive tests for entry_list helpers



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.2.8] - 2025-10-25

### MAINTENANCE

- Release v0.2.8



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.2.7] - 2025-10-25

### BUG FIXES

- Fix markdown linter errors
- Resolve all remaining markdown linter errors
- Restore ListView focus when returning from entry reader
- Restore ListView focus when returning from entry reader
- Resolve markdown linting errors and prevent IndexError on entry list screen
- Defer ListView focus and cursor restoration to prevent navigation hang in grouped mode
- Resolve linting errors and navigation persistence bug
- Resolve linting errors and navigation persistence bug
- Properly restore cursor position to entry in grouped mode
- Don't reset cursor index to 0 in _populate_list
- Find entries by ID not object identity when restoring cursor
- Wrap bare URLs in markdown links in RELEASE.md checklist
- Handle None value for list_view.index in type checking

### FEATURES

- Add Python 3.15 preview testing without blocking releases
- Add expand/collapse all feeds in group mode
- Add expand/collapse all feeds in group mode

### MAINTENANCE

- Release v0.2.7



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.2.6] - 2025-10-25

### MAINTENANCE

- Release v0.2.6



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.2.5] - 2025-10-25

### BUG FIXES

- Download artifacts in release job for GitHub Release creation
- Add write permissions to release job for GitHub Release creation
- Improve GitHub Actions workflows and fix linter errors

### FEATURES

- Add comprehensive PyPI classifiers to pyproject.toml

### MAINTENANCE

- Release v0.2.5



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.2.4] - 2025-10-25

### MAINTENANCE

- Release v0.2.4



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.2.3] - 2025-10-25

### BUG FIXES

- Remove bash release script and fix test indentation

### FEATURES

- Update release script defaults per user preferences

### MAINTENANCE

- Release v0.2.3



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.2.2] - 2025-10-25

### BUG FIXES

- Use timezone.utc instead of datetime.UTC for Python 3.11 compatibility

### DOCUMENTATION

- Add release troubleshooting guide and update README

### FEATURES

- Add changelog automation from conventional commits

### MAINTENANCE

- Release v0.2.2



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.2.1] - 2025-10-25

### BUG FIXES

- Resolve type checking errors for pyright

### DOCUMENTATION

- Add release automation scripts and documentation

### MAINTENANCE

- Add coverage.xml to .gitignore
- Release v0.2.1



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)
## [v0.2.0] - 2025-10-25

### BUG FIXES

- Resolve entry list display and improve error handling
- Fix entry selection and switch to official Miniflux client
- Pass api_key as keyword argument to official Miniflux client
- Fix entry reader screen to properly display content
- Use ListView.Selected event handler instead of key binding
- Remove incorrect import that was causing ModuleNotFoundError
- Properly implement refresh_screen to avoid IndexError
- Refresh entry list display when returning from reader
- Use correct method name fetch_entry_content for official client
- Fix type checking errors for Python 3.13 compatibility
- Add GitHub Actions permissions and fix EditorConfig indentation

### DOCUMENTATION

- Promote uv as primary installation method on README and homepage
- Promote uv as primary installation method on all pages

### FEATURES

- Initial project setup for Python Miniflux TUI
- Implement complete TUI with Textual framework
- Implement j/k scrolling and J/K entry navigation in reader
- Implement automatic mark as read and entry status updates
- Add q key to quit from entry reader and debug mark as read
- Implement refresh to remove read entries and fetch original content

### FIX

- Include starred entries in default view, even if read
- Make u/t filters load entries from API, not just toggle local filters

### MAINTENANCE

- Release v0.2.0 - Comprehensive test coverage expansion

### TESTING

- Lower coverage threshold and add 22 client tests
- Phase 2 - Add main.py and expand config.py tests
- Phase 3 - Add entry_reader.py and help.py tests
- Phase 4 - Expand entry_list.py coverage from 22% to 43%



#### Contributors

Thank you to everyone who contributed to this release!

**Humans:** 👤 Peter Reuterås

**AI & Automation:** 🤖 Claude (AI Assistant)

