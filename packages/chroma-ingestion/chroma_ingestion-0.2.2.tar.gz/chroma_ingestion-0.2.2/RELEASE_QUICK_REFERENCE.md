# Quick Reference: Release Process

**Keep this file handy during releases.**

## Pre-Release Checklist

```bash
cd /home/ob/Development/Tools/chroma

# 1. Verify everything is committed
git status  # Should be clean

# 2. Update version (if needed)
# Edit pyproject.toml: version = "0.X.Y"

# 3. Update CHANGELOG.md
# Add section: ## [0.X.Y] - YYYY-MM-DD

# 4. Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "chore: prepare release v0.X.Y"
git push origin main

# 5. Verify tests pass
pytest tests/ -v

# 6. Build locally
python -m build

# 7. Check distribution
twine check dist/*
```

## TestPyPI Pre-Release (Optional)

```bash
# Create pre-release tag
git tag -a v0.2.0rc1 -m "Release candidate v0.2.0rc1"
git push origin v0.2.0rc1

# Workflow publish-test.yml will:
# - Build distribution
# - Upload to TestPyPI
# - Test installation
# - Test CLI

# Once complete, verify:
pip install -i https://test.pypi.org/simple/ chroma-ingestion==0.2.0rc1
chroma-ingest --help
```

## Production PyPI Release

```bash
# Create release tag (MUST match pyproject.toml version)
git tag -a v0.2.0 -m "Release v0.2.0

- Feature 1
- Feature 2
- Bugfix 1"

# Push tag to trigger publication
git push origin v0.2.0

# Workflow publish.yml will:
# - Verify tag matches pyproject.toml
# - Build distribution
# - Upload to PyPI
# - Test installation
# - Create GitHub Release

# Check PyPI (wait 5-10 min for CDN):
open https://pypi.org/project/chroma-ingestion/

# Verify installation:
pip install --upgrade chroma-ingestion
python -c "from chroma_ingestion import CodeIngester; print('✅')"
```

## GitHub Secrets Setup (One-time)

Go to: Repository → Settings → Secrets and variables → Actions

**Add two secrets:**

1. **PYPI_API_TOKEN**
   - Value: Your PyPI API token from https://pypi.org/account/api-tokens/
   - Scope: "Entire account"

2. **PYPI_API_TOKEN_TEST**
   - Value: Your TestPyPI API token from https://test.pypi.org/account/api-tokens/
   - Scope: "Entire account"

## Troubleshooting

### "File already exists"
```bash
# Use post-release tag
git tag -a v0.2.0.post1 -m "Post-release patch"
git push origin v0.2.0.post1
```

### "Version mismatch"
```bash
# Ensure tag matches pyproject.toml
# Tag: v0.2.0
# pyproject.toml: version = "0.2.0"
```

### "Workflow failed to publish"
```bash
# Check Actions tab for error details
# Verify API tokens are correct
# Try pre-release first with v0.2.0rc1
```

## Version Numbering

- **v0.2.0** - Stable release
- **v0.2.0rc1** - Release candidate (pre-release)
- **v0.2.0a1** - Alpha (pre-release)
- **v0.2.0b1** - Beta (pre-release)
- **v0.2.0.post1** - Post-release patch

## Important URLs

- **PyPI:** https://pypi.org/project/chroma-ingestion/
- **TestPyPI:** https://test.pypi.org/project/chroma-ingestion/
- **GitHub:** https://github.com/chroma-core/chroma-ingestion
- **Documentation:** docs/ folder (build with mkdocs)

## Workflow Status

Check GitHub Actions:
```
Settings → Actions → All workflows
→ Publish to PyPI (or Publish to TestPyPI)
```

Watch for:
- ✅ Build succeeds
- ✅ Package check passes
- ✅ Upload succeeds
- ✅ Installation test passes
- ✅ CLI test passes
- ✅ Release created

## Post-Release

```bash
# Verify package is on PyPI
pip index versions chroma-ingestion

# Test installation fresh
python -m venv test_env
source test_env/bin/activate
pip install chroma-ingestion
chroma-ingest --help

# Check GitHub release
open https://github.com/chroma-core/chroma-ingestion/releases/tag/v0.2.0

# Announce release (optional)
# - GitHub discussion
# - Community channels
# - Email list
```

---

**Key Reminder:** Tag version MUST match `pyproject.toml` version!

Example:
- Tag: `v0.2.0`
- File: `version = "0.2.0"` in pyproject.toml
