# Release & Publishing Guide

This guide explains how to prepare and publish releases of `chroma-ingestion` to PyPI.

## Release Checklist

### 1. Preparation (Local)

```bash
# Ensure all tests pass
cd /home/ob/Development/Tools/chroma
./activate/bin/python -m pytest tests/ -v

# Update version in pyproject.toml (if needed)
# Check CHANGELOG.md is up to date

# Build locally to test
./activate/bin/python -m build --wheel

# Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "chore: prepare release v0.X.Y"
git push origin main
```

### 2. Create Release Tag

```bash
# Tag the release
# Format: v<major>.<minor>.<patch>
git tag -a v0.2.0 -m "Release version 0.2.0

- Feature X
- Feature Y
- Bugfix Z"

# Push tag to trigger workflow
git push origin v0.2.0
```

### 3. Choose Release Type

#### Production Release (v0.2.0)
- Triggers automatic publishing to **PyPI**
- Creates GitHub Release
- Tests installation from PyPI
- Tags format: `v[0-9]+.[0-9]+.[0-9]+` (e.g., v0.2.0, v1.0.0)

#### Pre-Release (v0.2.0rc1)
- Triggers automatic publishing to **TestPyPI** only
- Good for testing before production
- Tags format: `v*rc*`, `v*a*`, `v*b*` (e.g., v0.2.0rc1, v0.2.0a1)

#### Manual Release (for testing)
- Run via GitHub Actions UI
- Go to Actions → "Publish to TestPyPI" → Run workflow
- Manual workflow_dispatch trigger

## GitHub Actions Workflows

### publish.yml (Production PyPI)

**Triggers:** On tag push matching `v[0-9]+.[0-9]+.[0-9]+` (e.g., v0.2.0)

**Steps:**
1. Checkout code
2. Set up Python 3.11
3. Install build tools (build, twine)
4. **Verify tag version matches pyproject.toml version** (safety check)
5. Build distribution (wheel + sdist)
6. Check distribution with twine
7. Upload to PyPI (requires PYPI_API_TOKEN secret)
8. Verify package installs from PyPI
9. Test CLI entry points
10. Create GitHub Release with artifacts

**Required Secrets:**
- `PYPI_API_TOKEN` - Your PyPI API token for production

### publish-test.yml (TestPyPI)

**Triggers:**
- On tag push matching pre-release patterns (rc, a, b)
- Manual workflow_dispatch from GitHub Actions UI

**Steps:**
1. Checkout code
2. Set up Python 3.11
3. Install build tools
4. Build distribution
5. Check distribution
6. Upload to TestPyPI (requires PYPI_API_TOKEN_TEST secret)
7. Test installation from TestPyPI
8. Test CLI

**Required Secrets:**
- `PYPI_API_TOKEN_TEST` - Your TestPyPI API token

## Setting Up GitHub Secrets

### Step 1: Generate API Tokens

**For PyPI (Production):**
1. Go to https://pypi.org/account/api-tokens/
2. Create token: "chroma-ingestion release token"
3. Scope: "Entire account"
4. Copy token (you won't see it again!)

**For TestPyPI (Pre-release Testing):**
1. Go to https://test.pypi.org/account/api-tokens/
2. Create token: "chroma-ingestion test token"
3. Scope: "Entire account"
4. Copy token

### Step 2: Add to GitHub Secrets

1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `PYPI_API_TOKEN` with production token
4. Add `PYPI_API_TOKEN_TEST` with TestPyPI token

## Version Management

Version is defined in `pyproject.toml`:

```toml
[project]
version = "0.2.0"
```

### Semantic Versioning

Format: `MAJOR.MINOR.PATCH[-PRERELEASE]`

- **MAJOR**: Breaking API changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes
- **PRERELEASE**: rc1, a1, b1 for pre-releases

Examples:
- `0.2.0` - Stable release
- `0.2.1` - Patch release
- `0.3.0` - Minor release with new features
- `1.0.0` - Major release
- `0.2.0rc1` - Release candidate

## Release Workflow Example

### Scenario: Release v0.2.0

**Step 1: Prepare (Local)**
```bash
cd /home/ob/Development/Tools/chroma

# Update CHANGELOG.md
# - Add [0.2.0] section
# - List features, bugfixes
# - Set date to today

# Update version in pyproject.toml
# version = "0.2.0"

# Commit
git add pyproject.toml CHANGELOG.md
git commit -m "chore: release v0.2.0"
git push
```

**Step 2: Test Release (Optional)**
```bash
# Create pre-release tag
git tag -a v0.2.0rc1 -m "Release candidate v0.2.0rc1"
git push origin v0.2.0rc1

# Wait for publish-test.yml workflow to complete
# Test installation:
pip install -i https://test.pypi.org/simple/ chroma-ingestion==0.2.0rc1
```

**Step 3: Production Release**
```bash
# Create release tag
git tag -a v0.2.0 -m "Release v0.2.0

Features:
- Modern package structure
- Comprehensive testing
- GitHub Actions CI/CD
- CLI interface

Bugfixes:
- Singleton client connection stability"

# Push to trigger publish.yml
git push origin v0.2.0

# Workflow will:
# - Build distribution
# - Verify version matches tag
# - Upload to PyPI
# - Test installation
# - Create GitHub Release
```

**Step 4: Verify**
```bash
# Check PyPI page
open https://pypi.org/project/chroma-ingestion/

# Test installation
pip install --upgrade chroma-ingestion
chroma-ingest --help

# Check GitHub Release
open https://github.com/chroma-core/chroma-ingestion/releases/tag/v0.2.0
```

## Troubleshooting

### Workflow Fails to Publish

**Check logs:**
1. Go to Actions tab
2. Find failed workflow
3. Click to see error details

**Common issues:**
- API token invalid/expired → Regenerate on PyPI
- Version mismatch → Ensure tag matches pyproject.toml
- Network error → Retry workflow

### Package Already Exists

**Error:** "File already exists"

**Solution:**
- Update version and re-tag: `v0.2.1`
- Or use pre-release: `v0.2.0rc2`
- TestPyPI allows skipping if already exists

### Installation Fails After Upload

**Check:**
1. Package visible on PyPI: `pip index versions chroma-ingestion`
2. Wait 5-10 minutes for CDN propagation
3. Clear pip cache: `pip cache purge`
4. Try again: `pip install --force-reinstall chroma-ingestion`

## Post-Release

### 1. Update Documentation
- [ ] Update installation instructions if needed
- [ ] Update changelog with release notes
- [ ] Add migration guide if breaking changes

### 2. Announce Release
- [ ] Create GitHub release notes
- [ ] Post to community channels
- [ ] Update project website

### 3. Next Development Cycle
```bash
# Update version to next dev version
# version = "0.3.0.dev0"

git add pyproject.toml
git commit -m "chore: bump version to 0.3.0.dev0"
git push
```

## Advanced: Custom Distribution

For special cases (emergency patches, etc.):

```bash
# Build locally
python -m build

# Upload with twine
twine upload dist/chroma-ingestion-0.2.0.post1-py3-none-any.whl

# Or use GitHub workflow with manual dispatch
```

## FAQ

**Q: Can I release from a branch?**
A: Currently no - releases are only from version tags. To test, create a pre-release tag.

**Q: What if I mess up a release?**
A: You can:
1. Delete tag: `git tag -d v0.2.0 && git push origin :v0.2.0`
2. Re-create with correct version
3. Or create patch: `v0.2.0.post1`

**Q: How do I roll back?**
A: Release a new version (`0.2.1`) with the good code.

**Q: Can I release multiple versions at once?**
A: No - each tag triggers one release. Push tags one by one.

## References

- [PyPI Help](https://pypi.org/help/)
- [TestPyPI](https://test.pypi.org/)
- [Python Versioning (PEP 440)](https://www.python.org/dev/peps/pep-0440/)
- [GitHub Actions Workflows](https://docs.github.com/en/actions)
