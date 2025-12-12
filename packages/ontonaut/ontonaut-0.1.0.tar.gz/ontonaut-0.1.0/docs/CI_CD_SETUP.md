# CI/CD Pipeline Setup

Complete guide for setting up Continuous Integration and Continuous Deployment for Ontonaut.

## 📋 Overview

We have three automated workflows:

1. **CI Pipeline** - Tests and linting on PRs
2. **Release Pipeline** - Auto-publish to PyPI on version tags
3. **Documentation Pipeline** - Deploy docs to GitHub Pages

## 🔄 CI Pipeline (`.github/workflows/ci.yml`)

### Triggers
- Pull requests to `main`
- Pushes to `main`

### Jobs

#### 1. Test (Matrix)
Runs tests on multiple Python versions:
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

**Steps:**
- Checkout code
- Setup Python
- Install dependencies with `uv`
- Run pytest with coverage
- Upload coverage to Codecov (Python 3.11 only)

#### 2. Lint
Code quality checks:
- **Black** - Code formatting check
- **Ruff** - Fast Python linter
- **mypy** - Static type checking

#### 3. Build
Package building:
- Build wheel and sdist
- Check with `twine`
- Upload artifacts

#### 4. Status
Final status check ensuring all jobs passed.

### Local Testing

Before pushing, test locally:

```bash
# Run all checks
make test
make lint

# Or individually
pytest
black --check src tests
ruff check src tests
mypy src/ontonaut
```

## 🚀 Release Pipeline (`.github/workflows/release.yml`)

### Triggers
Version tags matching: `v[0-9]+.[0-9]+.[0-9]+`

Examples:
- `v1.0.0` ✅
- `v0.1.0` ✅
- `v2.5.13` ✅
- `v1.0.0-beta` ❌
- `1.0.0` ❌

### Jobs

#### 1. Verify
- Check tag format
- Extract version
- Verify `pyproject.toml` version matches tag

#### 2. Test
- Run full test suite
- Run linting checks

#### 3. Build
- Build wheel and sdist
- Validate with twine

#### 4. Publish
- Upload to PyPI
- Uses `PYPI_API_TOKEN` secret

#### 5. GitHub Release
- Create GitHub release
- Attach distribution files
- Generate release notes

### Setup PyPI Token

1. **Generate Token on PyPI**
   - Go to https://pypi.org/manage/account/
   - Scroll to "API tokens"
   - Click "Add API token"
   - Name: `ontonaut-github-actions`
   - Scope: "Entire account" (or specific to ontonaut)
   - Copy the token (starts with `pypi-`)

2. **Add to GitHub Secrets**
   - Go to repository Settings
   - Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: paste your PyPI token
   - Click "Add secret"

## 📦 Release Process

### Step 1: Update Version

Edit `pyproject.toml`:

```toml
[project]
name = "ontonaut"
version = "0.2.0"  # Update this
```

### Step 2: Update Changelog (Optional but Recommended)

Create/update `CHANGELOG.md`:

```markdown
# Changelog

## [0.2.0] - 2024-12-06

### Added
- New ChatBot widget with streaming
- Automatic tab creation
- Code formatting in output

### Changed
- Improved UI styling
- Better error handling

### Fixed
- Tab switching issue
```

### Step 3: Commit Changes

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to 0.2.0"
git push origin main
```

### Step 4: Create Tag

```bash
# Create annotated tag
git tag -a v0.2.0 -m "Release v0.2.0"

# Push tag
git push origin v0.2.0
```

### Step 5: Watch Automation

1. **Check Actions Tab**
   - Go to repository → Actions
   - Watch "Release to PyPI" workflow

2. **Workflow Steps** (takes ~5-10 minutes):
   - ✅ Verify tag and version
   - ✅ Run tests
   - ✅ Build package
   - ✅ Publish to PyPI
   - ✅ Create GitHub release

3. **Verify Release**
   - Check PyPI: https://pypi.org/project/ontonaut/
   - Check GitHub Releases tab
   - Test installation: `pip install ontonaut==0.2.0`

## 🐛 Troubleshooting

### CI Failing on PR

#### Test Failures
```bash
# Run tests locally
make test

# Check specific test
pytest tests/test_editor.py -v

# Check coverage
pytest --cov=ontonaut --cov-report=html
open htmlcov/index.html
```

#### Linting Errors
```bash
# Format code
make format

# Check linting
make lint

# Fix auto-fixable issues
ruff check --fix src tests
```

#### Type Errors
```bash
# Check types
mypy src/ontonaut

# Add type ignores if needed
# type: ignore[error-code]
```

### Release Failing

#### Version Mismatch
```bash
# Error: pyproject.toml version doesn't match tag

# Fix:
1. Check pyproject.toml version
2. Delete wrong tag: git tag -d v0.2.0
3. Push deletion: git push origin :refs/tags/v0.2.0
4. Update pyproject.toml
5. Create correct tag
```

#### PyPI Token Invalid
```bash
# Error: 403 Forbidden or Authentication error

# Fix:
1. Generate new token on PyPI
2. Update PYPI_API_TOKEN secret in GitHub
3. Re-run workflow
```

#### Build Errors
```bash
# Test build locally
make build

# Check distribution
twine check dist/*

# If errors, fix and commit before tagging
```

### Workflow Not Triggering

#### Wrong Tag Format
```bash
# ❌ These won't trigger release:
git tag 1.0.0           # Missing 'v'
git tag v1.0.0-beta     # Has suffix
git tag v1.0            # Missing patch version

# ✅ These will trigger:
git tag v1.0.0
git tag v0.1.0
git tag v2.5.13
```

#### Tag Not Pushed
```bash
# Create tag
git tag v0.2.0

# Must push it!
git push origin v0.2.0
```

## 📊 CI/CD Status Badges

Add to your README.md:

```markdown
![CI](https://github.com/yourusername/ontonaut/actions/workflows/ci.yml/badge.svg)
![Release](https://github.com/yourusername/ontonaut/actions/workflows/release.yml/badge.svg)
![Docs](https://github.com/yourusername/ontonaut/actions/workflows/deploy-docs.yml/badge.svg)
```

## 🔒 Security Best Practices

### Secrets Management
- ✅ Use GitHub Secrets for tokens
- ✅ Never commit tokens to repository
- ✅ Rotate tokens periodically
- ✅ Use minimal scope (project-specific if possible)

### Workflow Permissions
- ✅ Use minimal required permissions
- ✅ Pin action versions (`@v4` not `@latest`)
- ✅ Review action source code
- ✅ Enable required status checks

### Protected Branches
Configure in Settings → Branches → Branch protection rules:

For `main` branch:
- ✅ Require pull request reviews
- ✅ Require status checks to pass (CI)
- ✅ Require branches to be up to date
- ✅ Include administrators
- ✅ Restrict who can push

## 📈 Workflow Optimizations

### Speed Up CI

```yaml
# Use caching (add to ci.yml)
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('pyproject.toml') }}
```

### Parallel Jobs

Already configured with matrix strategy for testing multiple Python versions in parallel.

### Skip CI

Add to commit message:
```bash
git commit -m "docs: Update README [skip ci]"
```

## 🎯 Complete Workflow Examples

### Bug Fix Release

```bash
# 1. Create bug fix branch
git checkout -b fix-streaming-issue

# 2. Fix bug and test
make test
make lint

# 3. Push and create PR
git push origin fix-streaming-issue
# Create PR on GitHub

# 4. After PR approved and merged
git checkout main
git pull

# 5. Update version (patch)
# 0.1.0 → 0.1.1
vim pyproject.toml

# 6. Commit and tag
git commit -am "Bump version to 0.1.1"
git push
git tag v0.1.1
git push origin v0.1.1

# 7. Wait for automatic release
```

### Feature Release

```bash
# 1. Develop feature in branch
git checkout -b feature-new-widget

# 2. Implement, test, push PR
# ... development work ...
make test
make lint

# 3. After PR merged, update version (minor)
# 0.1.0 → 0.2.0
git checkout main
git pull
vim pyproject.toml

# 4. Release
git commit -am "Bump version to 0.2.0"
git push
git tag v0.2.0
git push origin v0.2.0
```

### Major Release

```bash
# For breaking changes
# 0.1.0 → 1.0.0

# Same process as feature release
# but update major version
```

## 🔗 Related Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [PyPI Publishing Guide](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

## ✅ Checklist

Before releasing:
- [ ] All tests passing locally
- [ ] All linting checks passing
- [ ] Version updated in `pyproject.toml`
- [ ] Changelog updated (optional)
- [ ] Changes committed and pushed to `main`
- [ ] PyPI token configured in GitHub secrets
- [ ] Tag created with correct format (`vX.Y.Z`)
- [ ] Tag pushed to GitHub

After releasing:
- [ ] Check PyPI package page
- [ ] Check GitHub release page
- [ ] Test installation: `pip install ontonaut==X.Y.Z`
- [ ] Verify documentation updated
- [ ] Announce release (optional)

---

**Your CI/CD pipeline is ready!** 🚀

All workflows will run automatically:
- CI on every PR
- Release on every version tag
- Docs on every push to main
