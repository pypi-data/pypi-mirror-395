# Trusted Publisher Registration - Copy & Paste Values

**Your Repository Details:**
- GitHub Username: `ollieb89`
- Repository Name: `chroma-tool`
- Package Name: `chroma-ingestion`

---

## ✅ TestPyPI - Copy These Exact Values

**URL:** https://test.pypi.org/manage/project/chroma-ingestion/settings/publishing/

| Field | Value | Copy |
|-------|-------|------|
| Publisher name | `GitHub` | ✂️ |
| Repository owner | `ollieb89` | ✂️ |
| Repository name | `chroma-tool` | ✂️ |
| Workflow name | `publish-test.yml` | ✂️ |
| Environment name | _(leave empty)_ | — |

---

## ✅ Production PyPI - Copy These Exact Values

**URL:** https://pypi.org/manage/project/chroma-ingestion/settings/publishing/

| Field | Value | Copy |
|-------|-------|------|
| Publisher name | `GitHub` | ✂️ |
| Repository owner | `ollieb89` | ✂️ |
| Repository name | `chroma-tool` | ✂️ |
| Workflow name | `publish.yml` | ✂️ |
| Environment name | _(leave empty)_ | — |

---

## Steps to Register

### For TestPyPI:

1. Go to: https://test.pypi.org/manage/project/chroma-ingestion/settings/publishing/
2. Click **"Add a new pending publisher"**
3. Copy-paste the TestPyPI values above
4. Click **"Save pending publisher"**
5. Check email for approval link from TestPyPI
6. Click link and approve
7. ✅ Done!

### For Production PyPI:

1. Go to: https://pypi.org/manage/project/chroma-ingestion/settings/publishing/
2. Click **"Add a new pending publisher"**
3. Copy-paste the Production PyPI values above
4. Click **"Save pending publisher"**
5. Check email for approval link from PyPI
6. Click link and approve
7. ✅ Done!

---

## What This Does

After registering, your workflows can publish to PyPI without API tokens:

```yaml
# ✅ This now works! (no password needed)
- name: Upload to TestPyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    repository-url: https://test.pypi.org/legacy/
```

PyPI will:
1. See the request comes from GitHub Actions
2. Check: "Is this the registered publisher for chroma-ingestion?"
3. Verify: "Yes, it's from ollieb89/chroma-tool/publish-test.yml"
4. Issue temporary token and allow publish ✅

---

## Next Steps After Registration

```bash
cd /home/ob/Development/Tools/chroma

# Clean up old tag if it exists
git tag -d v0.2.0rc1 2>/dev/null || true
git push origin :refs/tags/v0.2.0rc1 2>/dev/null || true

# Create new test tag
git tag -a v0.2.0rc1 -m "Testing Trusted Publishing - now with registered publishers"
git push origin v0.2.0rc1

# Watch GitHub Actions:
# https://github.com/ollieb89/chroma-tool/actions
# Look for: "Publish to TestPyPI" workflow
# Should complete in 2-3 minutes with NO authentication errors ✅
```

---

## Questions?

**Q: What if I fill in wrong values?**
A: You can delete and recreate the publisher registration.

**Q: Do I need an environment?**
A: No, leave it empty. (Advanced users can set up GitHub Environments for extra security.)

**Q: How do I know it worked?**
A: On TestPyPI/PyPI, you'll see the publisher listed with ✅ "Active" status.

---

**Total time:** ~10 minutes for both registrations
**Result:** Automatic PyPI publishing without API tokens! 🚀
