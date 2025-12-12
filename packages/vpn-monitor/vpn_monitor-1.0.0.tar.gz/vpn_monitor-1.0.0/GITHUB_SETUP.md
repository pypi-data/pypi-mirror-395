# GitHub Repository Configuration Guide

This document provides step-by-step instructions for configuring the GitHub repository to use the recommended branching strategy and CI/CD workflows.

## Table of Contents

- [Branch Strategy Overview](#branch-strategy-overview)
- [Initial Setup](#initial-setup)
- [Branch Protection Rules](#branch-protection-rules)
- [Merge Settings](#merge-settings)
- [Release Workflow](#release-workflow)
- [Required Secrets and Permissions](#required-secrets-and-permissions)
- [Enabling GitHub Features](#enabling-github-features)

---

## Branch Strategy Overview

```
main (protected)
  │
  ├── feature/add-new-vpn-check
  ├── feature/improve-tray-menu
  ├── fix/memory-leak
  ├── docs/update-readme
  └── chore/update-dependencies
```

| Branch | Purpose | Protection |
|--------|---------|------------|
| `main` | Production releases, always stable | ✅ Protected |
| `feature/*` | New features development | ❌ Not protected |
| `fix/*` | Bug fixes | ❌ Not protected |
| `docs/*` | Documentation updates | ❌ Not protected |
| `chore/*` | Maintenance tasks | ❌ Not protected |

---

## Initial Setup

### 1. Set Default Branch

1. Go to **Settings** → **General**
2. Under "Default branch", ensure `main` is selected
3. Click **Update** if needed

### 2. Enable Required Features

1. Go to **Settings** → **General**
2. Under "Features":
   - ✅ Enable **Issues**
   - ✅ Enable **Discussions** (for Q&A)
   - ✅ Enable **Projects** (optional)

---

## Branch Protection Rules

### Configure Main Branch Protection

1. Go to **Settings** → **Branches**
2. Click **Add branch protection rule** (or edit existing)
3. Set **Branch name pattern**: `main`

### Recommended Settings

```yaml
Branch name pattern: main

☑️ Require a pull request before merging
  ☑️ Require approvals: 1
  ☑️ Dismiss stale pull request approvals when new commits are pushed
  ☐ Require review from Code Owners (enable if team grows)
  ☑️ Require approval of the most recent reviewable push

☑️ Require status checks to pass before merging
  ☑️ Require branches to be up to date before merging
  Status checks that are required:
    - Lint
    - Test (Python 3.8)
    - Test (Python 3.9)
    - Test (Python 3.10)
    - Test (Python 3.11)
    - Test (Python 3.12)
    - Build Executable
    - Validate Commits

☑️ Require conversation resolution before merging

☑️ Require signed commits (optional but recommended)

☑️ Require linear history

☐ Include administrators (uncheck for emergency fixes)

☐ Allow force pushes: NEVER

☐ Allow deletions: NEVER
```

### Important Notes

- **Status checks** will only appear after the first workflow run
- Run a test PR first, then configure required status checks

---

## Merge Settings

### Configure Pull Request Merge Options

1. Go to **Settings** → **General**
2. Scroll to "Pull Requests"
3. Configure:

```yaml
☐ Allow merge commits
  - Uncheck to enforce cleaner history

☑️ Allow squash merging
  - Default commit message: Pull request title and description
  
☐ Allow rebase merging
  - Uncheck for consistency

☑️ Always suggest updating pull request branches

☑️ Automatically delete head branches
  - Keeps repository clean after PR merges
```

### Why Squash Merging?

- Creates clean, linear history on `main`
- Each PR = one commit on `main`
- PR title becomes commit message (should follow conventional commits)

---

## Release Workflow

### Creating a Release

Releases are automated via GitHub Actions when you push a version tag.

#### Step-by-Step Release Process

1. **Ensure `main` is stable**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Update version in `pyproject.toml`** (if needed)
   ```toml
   version = "1.0.0"
   ```

3. **Create and push a version tag**
   ```bash
   # For stable releases
   git tag v1.0.0
   git push origin v1.0.0
   
   # For pre-releases
   git tag v1.0.0-beta.1
   git push origin v1.0.0-beta.1
   ```

4. **GitHub Actions will automatically**:
   - Build the Windows executable
   - Generate changelog from conventional commits
   - Create a GitHub Release
   - Upload `vpn-monitor.exe` as release artifact
   - Update `CHANGELOG.md` on `main`

### Version Tagging Convention

| Tag Format | Type | GitHub Release |
|------------|------|----------------|
| `v1.0.0` | Stable | Regular release |
| `v1.0.0-alpha.1` | Pre-release | Marked as pre-release |
| `v1.0.0-beta.1` | Pre-release | Marked as pre-release |
| `v1.0.0-rc.1` | Pre-release | Marked as pre-release |

---

## Required Secrets and Permissions

### GitHub Actions Permissions

The workflows use `GITHUB_TOKEN` which is automatically provided. Ensure:

1. Go to **Settings** → **Actions** → **General**
2. Under "Workflow permissions":
   - Select **Read and write permissions**
   - ✅ Allow GitHub Actions to create and approve pull requests

### No Additional Secrets Required

The current setup uses only the built-in `GITHUB_TOKEN`.

---

## Enabling GitHub Features

### 1. Enable Dependabot

1. Go to **Settings** → **Code security and analysis**
2. Enable:
   - ✅ Dependency graph
   - ✅ Dependabot alerts
   - ✅ Dependabot security updates
   - ✅ Dependabot version updates

### 2. Configure Issue Labels

Create these labels for better organization:

| Label | Color | Description |
|-------|-------|-------------|
| `bug` | `#d73a4a` | Something isn't working |
| `enhancement` | `#a2eeef` | New feature or request |
| `documentation` | `#0075ca` | Documentation improvements |
| `dependencies` | `#0366d6` | Dependency updates |
| `python` | `#3572A5` | Python-related |
| `github-actions` | `#000000` | CI/CD related |
| `good first issue` | `#7057ff` | Good for newcomers |
| `help wanted` | `#008672` | Extra attention needed |

### 3. Set Up Discussions (Optional)

1. Go to **Settings** → **General** → **Features**
2. Enable **Discussions**
3. Set up categories:
   - 💡 Ideas
   - 🙏 Q&A
   - 📣 Announcements
   - 💬 General

---

## Feature Branch Workflow

### For Contributors

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/vpn_status_monitor.git
cd vpn_status_monitor

# 2. Add upstream
git remote add upstream https://github.com/OWNER/vpn_status_monitor.git

# 3. Create feature branch
git checkout main
git pull upstream main
git checkout -b feature/my-new-feature

# 4. Make changes with conventional commits
git add .
git commit -m "feat(tray): add custom snooze duration"

# 5. Push and create PR
git push origin feature/my-new-feature
```

### For Maintainers

```bash
# Review PR locally
gh pr checkout 123

# After PR is merged, clean up
git checkout main
git pull origin main
git branch -d feature/my-new-feature
```

---

## Quick Reference

### Conventional Commit Types

```
feat:     New feature
fix:      Bug fix
docs:     Documentation
style:    Formatting
refactor: Code restructuring
perf:     Performance
test:     Tests
build:    Build system
ci:       CI/CD
chore:    Maintenance
```

### Common Commands

```bash
# Create release
git tag v1.0.0 && git push origin v1.0.0

# Update from upstream
git fetch upstream && git rebase upstream/main

# Run CI locally
flake8 vpn_monitor tests
pytest tests/
```

---

## Troubleshooting

### CI Checks Not Appearing

- Wait for first workflow run to complete
- Check **Actions** tab for any errors
- Verify workflow files are in `.github/workflows/`

### Release Not Created

- Ensure tag follows `v*` pattern
- Check Actions tab for workflow errors
- Verify `GITHUB_TOKEN` has write permissions

### Dependabot PRs Failing

- Check if `requirements-dev.txt` exists
- Verify `pyproject.toml` is valid
- Review Dependabot logs in Security tab

---

## Additional Resources

- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

