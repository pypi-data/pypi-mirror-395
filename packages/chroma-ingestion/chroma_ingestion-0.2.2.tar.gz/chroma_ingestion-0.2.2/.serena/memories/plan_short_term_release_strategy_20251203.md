# Short-Term Release Strategy Plan (1-2 weeks)
**Created:** December 3, 2025
**Status:** ✅ PLANNING PHASE - Ready for execution

## Objective
Execute three strategic initiatives to prepare chroma-ingestion for production distribution and community adoption:
1. Package Release to PyPI (TestPyPI first, then production)
2. Expand CI/CD with integration testing
3. Enhance API documentation

---

## Current State Assessment

### ✅ What's Already Done
- **Package Structure:** Modern, complete (src/chroma_ingestion)
- **pyproject.toml:** Properly configured with metadata, scripts, dependencies
- **CI/CD:** GitHub Actions workflow with lint, type-check, test (3 parallel jobs)
- **Tests:** ~140 tests (74 unit + 70+ integration), ~100% coverage
- **Type Safety:** 100% type hints, mypy strict mode
- **Public API:** 5 exports (CodeIngester, AgentIngester, CodeRetriever, MultiCollectionSearcher, get_chroma_client)

### 🔍 What Needs Work
| Task | Priority | Effort | Dependencies |
|------|----------|--------|--------------|
| 1. PyPI Release Setup | High | Medium | None (can start now) |
| 2. CI/CD Integration Tests | High | Medium | Package ready (1→2) |
| 3. API Documentation | High | Medium | Package ready (1→3) |

---

## Implementation Plan

### Phase 1: Package Release (2-3 days)

#### 1.1 Pre-Release Checklist
- [ ] Verify version in pyproject.toml (0.2.0) ✓
- [ ] Review CHANGELOG.md for clear release notes
- [ ] Verify long_description and description render correctly
- [ ] Test build locally: `python -m pip install build && python -m build`
- [ ] Create MANIFEST.in if needed for additional files
- [ ] Add GitHub release metadata (version tags, descriptions)

#### 1.2 TestPyPI Upload (Staging)
- [ ] Create PyPI account (if not exists)
- [ ] Generate API token on TestPyPI
- [ ] Store token in GitHub Secrets: PYPI_API_TOKEN_TEST
- [ ] Create GitHub Actions "publish-test.yml" workflow
  - Trigger: manual dispatch or on pre-release tags
  - Build distribution files
  - Upload to TestPyPI
  - Verify package page renders correctly
- [ ] Test installation: `pip install -i https://test.pypi.org chroma-ingestion`
- [ ] Verify CLI works: `chroma-ingestion --help`

#### 1.3 Production PyPI Upload
- [ ] Generate production PyPI API token
- [ ] Store in GitHub Secrets: PYPI_API_TOKEN
- [ ] Create GitHub Actions "publish.yml" workflow
  - Trigger: on release tag (e.g., v0.2.0)
  - Build distribution files
  - Upload to PyPI
  - Create GitHub release with changelog
- [ ] First release process:
  1. Commit and push to main
  2. Create git tag: `git tag v0.2.0`
  3. Push tag: `git push origin v0.2.0`
  4. GitHub Actions automatically publishes to PyPI

#### 1.4 Documentation Updates
- [ ] Update README.md with PyPI installation badge
- [ ] Add installation instructions to docs
- [ ] Create CHANGELOG.md with v0.2.0 release notes
- [ ] Document changelog format for future releases

---

### Phase 2: CI/CD Integration Testing (2-3 days)

#### 2.1 Expand Current Workflow
Add to `.github/workflows/ci.yml`:
- [ ] Integration tests with real Chroma instance
  - Option A: Chroma Docker container in CI
  - Option B: Chroma Cloud test account (requires creds in secrets)
- [ ] Performance benchmarks (optional but recommended)
- [ ] Python version matrix testing (3.11, 3.12)

#### 2.2 New Workflow: "integration-tests.yml"
```yaml
# Runs on:
# - Every push to main
# - PRs to main
# - Manual dispatch

# Jobs:
# 1. Integration Tests (with real Chroma)
#    - Spin up Chroma Docker container
#    - Run integration tests
#    - Upload coverage
#
# 2. Multi-Version Testing
#    - Test against Python 3.11, 3.12
#    - Verify compatibility across versions
#
# 3. Package Build Test
#    - Build wheel and sdist
#    - Test installation in clean environment
#    - Verify CLI entry points work
```

#### 2.3 Environment Setup
- [ ] Create docker-compose.yml for local integration test development
- [ ] Update conftest.py with real Chroma fixture (vs mock)
- [ ] Add integration test markers to pytest
- [ ] Document how to run integration tests locally

---

### Phase 3: API Documentation Expansion (2-3 days)

#### 3.1 Auto-Documentation from Docstrings
- [ ] Install mkdocs and mkdocs-material (already in dev deps)
- [ ] Create mkdocs.yml configuration
- [ ] Use mkdocs-autoreferencer or mkdocstrings plugin
- [ ] Generate API reference from docstrings

#### 3.2 API Reference Documentation
Create `docs/api/` with:
- [ ] `overview.md` - High-level API introduction
- [ ] `chroma-ingestion.md` - Main package export docs
- [ ] `ingestion.md` - CodeIngester, AgentIngester docs
- [ ] `retrieval.md` - CodeRetriever, MultiCollectionSearcher docs
- [ ] `clients.md` - Singleton client pattern docs
- [ ] `config.md` - Configuration guide

#### 3.3 Usage Examples Documentation
Create `docs/guides/` with:
- [ ] `basic-usage.md` - Getting started example
- [ ] `ingestion-workflow.md` - Complete ingestion flow
- [ ] `retrieval-patterns.md` - Query patterns and best practices
- [ ] `chunking-strategy.md` - Chunk size tuning guide
- [ ] `metadata-filtering.md` - Advanced metadata queries
- [ ] `troubleshooting.md` - Common issues and solutions

#### 3.4 Documentation Site Deployment
- [ ] Add GitHub Pages deployment workflow
- [ ] Build and deploy docs on every push to main
- [ ] Set up ReadTheDocs integration (optional, advanced)

---

## Timeline & Sequencing

### Week 1
- **Days 1-2:** Phase 1 (PyPI Release Setup)
  - ✓ Update README, CHANGELOG
  - ✓ Create publish workflows
  - ✓ Test locally with build
  - ✓ Upload to TestPyPI
  - ✓ Verify installation works

- **Days 3-4:** Phase 2 (CI/CD Integration Tests)
  - ✓ Design integration test architecture
  - ✓ Add docker-compose for local testing
  - ✓ Create integration-tests.yml workflow
  - ✓ Test multi-version compatibility

- **Days 5-7:** Phase 3 (API Documentation)
  - ✓ Generate mkdocs site skeleton
  - ✓ Create API reference docs
  - ✓ Write usage guides
  - ✓ Deploy to GitHub Pages

### Week 2
- **Days 1-3:** Final validation and testing
  - ✓ Full test suite locally
  - ✓ Verify documentation rendering
  - ✓ Test production PyPI workflow with test release
  - ✓ Get community feedback if possible

- **Days 4-5:** Production release
  - ✓ Create v0.2.0 release on GitHub
  - ✓ Push tag to trigger PyPI publishing
  - ✓ Verify package on PyPI
  - ✓ Update social/channels with release announcement

---

## Dependencies & Prerequisites

| Item | Status | Action |
|------|--------|--------|
| PyPI Account | ⚠️ Unknown | Create if needed |
| PyPI API Token | ⚠️ Unknown | Generate and add to GitHub Secrets |
| GitHub Secrets Configured | ❓ Check | Add PYPI_API_TOKEN_TEST, PYPI_API_TOKEN |
| mkdocs plugins | ❓ Check | May need to add mkdocstrings to dev deps |
| Docker (for CI) | ⚠️ Check | GitHub Actions includes Docker |

---

## Success Criteria

### Phase 1: Package Release ✅
- [ ] Package builds without errors: `python -m build`
- [ ] TestPyPI package installs: `pip install -i https://test.pypi.org chroma-ingestion`
- [ ] CLI works post-install: `chroma-ingestion --help` succeeds
- [ ] Package page shows on PyPI with correct metadata
- [ ] Production PyPI workflow configured and tested

### Phase 2: CI/CD Integration Testing ✅
- [ ] Integration tests run in GitHub Actions
- [ ] Multi-version testing (3.11, 3.12) passes
- [ ] Package build test succeeds
- [ ] Coverage reports generated and accessible
- [ ] Documentation in place for running tests locally

### Phase 3: API Documentation ✅
- [ ] Documentation site builds without errors
- [ ] API reference covers all 5 public exports
- [ ] At least 3 usage guides with examples
- [ ] Site deployed to GitHub Pages
- [ ] Links in README point to docs

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| PyPI upload fails | High | Test extensively on TestPyPI first |
| Import errors on clean install | High | Test in fresh venv before release |
| CI workflow syntax errors | Medium | Test workflow locally with act or similar |
| Documentation build fails | Low | Test mkdocs build locally first |
| Chroma Docker in CI times out | Medium | Set appropriate timeouts, use slim images |

---

## Key Files to Create/Modify

### New Files
- `.github/workflows/publish-test.yml` - TestPyPI publishing
- `.github/workflows/publish.yml` - Production PyPI publishing
- `mkdocs.yml` - Documentation site configuration
- `CHANGELOG.md` - Release notes template
- `docs/api/overview.md` - API intro
- `docs/guides/basic-usage.md` - Getting started
- `docker-compose.yml` - Local Chroma for testing

### Modified Files
- `pyproject.toml` - Update version if needed, add mkdocstrings
- `README.md` - Add PyPI badge, link to docs
- `.github/workflows/ci.yml` - Add integration tests, multi-version testing
- `README.md` - Installation instructions

---

## Notes

1. **Version Management:** Current is 0.2.0 - adequate for first public release
2. **Licensing:** MIT license present - good for open source
3. **Documentation:** Will be hosted on GitHub Pages (free tier)
4. **CI/CD:** Already solid - just expanding with integration tests
5. **Dependencies:** All pinned to reasonable minimum versions

---

**Next Step:** Start with Phase 1 (PyPI Release)
