#!/bin/bash
# Comprehensive Validation Script for chroma-ingestion v0.2.0
# Runs all checks to verify production readiness

set -e

echo "🔍 chroma-ingestion v0.2.0 - Production Readiness Verification"
echo "================================================================"
echo ""

cd "$(dirname "$0")"

# Color output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_mark="${GREEN}✓${NC}"
cross_mark="${RED}✗${NC}"

# Track results
PASS=0
FAIL=0

# Helper function
check_result() {
    if [ $1 -eq 0 ]; then
        echo "${check_mark} $2"
        ((PASS++))
    else
        echo "${cross_mark} $2"
        ((FAIL++))
    fi
}

# 1. Verify file structure
echo "📁 Checking File Structure..."
[ -d "src/chroma_ingestion" ] && check_result 0 "Package directory exists" || check_result 1 "Package directory missing"
[ -f "src/chroma_ingestion/__init__.py" ] && check_result 0 "Package init exists" || check_result 1 "Package init missing"
[ -f "pyproject.toml" ] && check_result 0 "pyproject.toml exists" || check_result 1 "pyproject.toml missing"
[ -d "docs" ] && check_result 0 "Documentation directory exists" || check_result 1 "Documentation missing"
[ -d ".github/workflows" ] && check_result 0 "Workflows directory exists" || check_result 1 "Workflows missing"
echo ""

# 2. Check documentation
echo "📚 Checking Documentation..."
[ -f "docs/index.md" ] && check_result 0 "Home page exists" || check_result 1 "Home page missing"
[ -f "docs/getting-started/quick-start.md" ] && check_result 0 "Quick start exists" || check_result 1 "Quick start missing"
[ -f "docs/guides/basic-usage.md" ] && check_result 0 "Basic usage guide exists" || check_result 1 "Basic usage missing"
[ -f "docs/guides/ingestion-workflow.md" ] && check_result 0 "Ingestion workflow guide exists" || check_result 1 "Ingestion guide missing"
[ -f "docs/guides/retrieval-patterns.md" ] && check_result 0 "Retrieval patterns guide exists" || check_result 1 "Retrieval guide missing"
[ -f "docs/guides/chunking-strategy.md" ] && check_result 0 "Chunking strategy guide exists" || check_result 1 "Chunking guide missing"
[ -f "docs/guides/advanced-filtering.md" ] && check_result 0 "Advanced filtering guide exists" || check_result 1 "Filtering guide missing"
[ -f "docs/guides/troubleshooting.md" ] && check_result 0 "Troubleshooting guide exists" || check_result 1 "Troubleshooting missing"
[ -f "docs/guides/deployment.md" ] && check_result 0 "Deployment guide exists" || check_result 1 "Deployment guide missing"
[ -f "docs/api/reference.md" ] && check_result 0 "API reference exists" || check_result 1 "API reference missing"
echo ""

# 3. Check release files
echo "🚀 Checking Release Files..."
[ -f "CHANGELOG.md" ] && check_result 0 "CHANGELOG.md exists" || check_result 1 "CHANGELOG missing"
[ -f "RELEASE_GUIDE.md" ] && check_result 0 "RELEASE_GUIDE.md exists" || check_result 1 "RELEASE_GUIDE missing"
[ -f "PRODUCTION_RELEASE_CHECKLIST.md" ] && check_result 0 "PRODUCTION_RELEASE_CHECKLIST exists" || check_result 1 "Checklist missing"
[ -f "COMPLETION_SUMMARY.md" ] && check_result 0 "COMPLETION_SUMMARY exists" || check_result 1 "Summary missing"
echo ""

# 4. Check workflows
echo "⚙️  Checking GitHub Actions Workflows..."
[ -f ".github/workflows/integration-tests.yml" ] && check_result 0 "CI/CD pipeline exists" || check_result 1 "CI/CD missing"
[ -f ".github/workflows/publish-test.yml" ] && check_result 0 "TestPyPI workflow exists" || check_result 1 "TestPyPI workflow missing"
[ -f ".github/workflows/publish.yml" ] && check_result 0 "PyPI workflow exists" || check_result 1 "PyPI workflow missing"
[ -f ".github/workflows/deploy-docs.yml" ] && check_result 0 "Docs deployment workflow exists" || check_result 1 "Docs workflow missing"
echo ""

# 5. Check configuration
echo "⚙️  Checking Configuration Files..."
[ -f "mkdocs.yml" ] && check_result 0 "mkdocs.yml exists" || check_result 1 "mkdocs.yml missing"
[ -f "docker-compose.yml" ] && check_result 0 "docker-compose.yml exists" || check_result 1 "docker-compose missing"
echo ""

# 6. Check version consistency
echo "📦 Checking Version Consistency..."
VERSION=$(grep -E "^version = " pyproject.toml | head -1 | cut -d'"' -f2)
echo "   Found version: $VERSION"
grep -q "__version__ = \"$VERSION\"" src/chroma_ingestion/__init__.py && \
    check_result 0 "__init__.py version matches" || check_result 1 "__init__.py version mismatch"
grep -q "v$VERSION" CHANGELOG.md && \
    check_result 0 "CHANGELOG version matches" || check_result 1 "CHANGELOG version mismatch"
echo ""

# 7. Check Python package (if available)
echo "🐍 Checking Python Package..."
if command -v python3 &> /dev/null; then
    python3 -c "import sys; sys.path.insert(0, 'src'); from chroma_ingestion import CodeIngester" && \
        check_result 0 "Package imports correctly" || check_result 1 "Package import failed"

    python3 -c "import sys; sys.path.insert(0, 'src'); from chroma_ingestion import __version__" && \
        check_result 0 "Version accessible" || check_result 1 "Version not accessible"
else
    echo "   ${YELLOW}Python not found, skipping package import checks${NC}"
fi
echo ""

# 8. Check documentation count
echo "📊 Checking Documentation Statistics..."
DOC_COUNT=$(find docs -name "*.md" -type f | wc -l)
echo "   Documentation pages: $DOC_COUNT"
if [ "$DOC_COUNT" -ge 10 ]; then
    check_result 0 "Sufficient documentation pages ($DOC_COUNT)"
else
    check_result 1 "Insufficient documentation pages ($DOC_COUNT)"
fi

DOC_LINES=$(find docs -name "*.md" -type f -exec wc -l {} + | awk '{sum+=$1} END {print sum}')
echo "   Documentation lines: $DOC_LINES"
if [ "$DOC_LINES" -ge 3000 ]; then
    check_result 0 "Comprehensive documentation ($DOC_LINES lines)"
else
    check_result 1 "Insufficient documentation ($DOC_LINES lines)"
fi
echo ""

# 9. Summary
echo "================================================================"
echo "📈 Results Summary"
echo "================================================================"
TOTAL=$((PASS + FAIL))
echo "Total checks: $TOTAL"
echo "${GREEN}Passed: $PASS${NC}"
if [ $FAIL -gt 0 ]; then
    echo "${RED}Failed: $FAIL${NC}"
    echo ""
    echo "⚠️  Some checks failed. Review above for details."
    exit 1
else
    echo "${RED}Failed: 0${NC}"
    echo ""
    echo "🎉 ${GREEN}ALL CHECKS PASSED - READY FOR PRODUCTION RELEASE${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Add GitHub Secrets (PYPI_API_TOKEN, PYPI_API_TOKEN_TEST)"
    echo "2. Create pre-release tag: git tag -a v${VERSION}rc1 -m \"Release candidate\""
    echo "3. Push tag: git push origin v${VERSION}rc1"
    echo "4. After testing, create production tag: git tag -a v${VERSION} -m \"Release v${VERSION}\""
    echo "5. Push production tag: git push origin v${VERSION}"
    exit 0
fi
