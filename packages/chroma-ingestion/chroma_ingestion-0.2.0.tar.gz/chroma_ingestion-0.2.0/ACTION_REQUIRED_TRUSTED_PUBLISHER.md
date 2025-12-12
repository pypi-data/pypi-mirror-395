# 🚨 Action Required: Register Trusted Publisher on TestPyPI

**Status:** Workflow attempted but failed - Publisher not registered yet
**Error:** 403 Forbidden (authentication failed)
**Cause:** Trusted Publisher not configured on TestPyPI

---

## Quick Fix (5 minutes)

### Step 1: Go to TestPyPI Settings

Open this URL in your browser:
```
https://test.pypi.org/manage/project/chroma-ingestion/settings/publishing/
```

**You must be logged in as the project owner.**

### Step 2: Add Trusted Publisher

Click **"Add a new pending publisher"** and fill in these EXACT values:

| Field | Value |
|-------|-------|
| **Publisher name** | `GitHub` |
| **Repository owner** | `ollieb89` |
| **Repository name** | `chroma-tool` |
| **Workflow name** | `publish-test.yml` |
| **Environment name** | (leave empty - optional) |

⚠️ **Important:** Use the values above exactly - they must match your GitHub repository!

### Step 3: Save and Approve

1. Click **"Save pending publisher"**
2. GitHub will send you a verification link
3. Click the link and approve on TestPyPI
4. Done! ✅

---

## Then: Do the Same for Production PyPI

After TestPyPI works, register production:

```
https://pypi.org/manage/project/chroma-ingestion/settings/publishing/
```

Same steps, but with these values:

| Field | Value |
|-------|-------|
| **Publisher name** | `GitHub` |
| **Repository owner** | `ollieb89` |
| **Repository name** | `chroma-tool` |
| **Workflow name** | `publish.yml` |
| **Environment name** | (leave empty - optional) |

---

## Why This is Needed

**Before (with API token):**
- Workflow had password in secrets
- Workflow authenticated as "ob with password"

**After (with Trusted Publishing):**
- Workflow has NO password
- Workflow says "I'm GitHub running chroma/publish-test.yml"
- PyPI verifies this is legitimate
- PyPI issues temporary token

**Current issue:**
- Workflow is saying "I'm GitHub"
- PyPI doesn't recognize it (not registered)
- PyPI rejects with 403 Forbidden

---

## Timeline

| Step | Time | Action |
|------|------|--------|
| Register TestPyPI | 5 min | Visit TestPyPI settings, add publisher |
| Test rc1 release | 5 min | `git tag v0.2.0rc1 && git push origin v0.2.0rc1` |
| Register Production PyPI | 5 min | Visit PyPI settings, add publisher |
| Release v0.2.0 | 2 min | `git tag v0.2.0 && git push origin v0.2.0` |
| **Total** | **17 min** | Live on PyPI! |

---

## ✅ Checklist

- [ ] Open TestPyPI settings: https://test.pypi.org/manage/project/chroma-ingestion/settings/publishing/
- [ ] Click "Add a new pending publisher"
- [ ] Fill in: GitHub, `ollieb89`, `chroma-tool`, `publish-test.yml`, (leave environment empty)
- [ ] Click "Save pending publisher"
- [ ] Check your email or GitHub notifications for approval link from TestPyPI
- [ ] Click the link and approve on TestPyPI
- [ ] Verify on TestPyPI (you should see your publisher listed with ✅ Active)
- [ ] Repeat for Production PyPI with `publish.yml` workflow name
- [ ] Done! Ready to test

---

## Next Steps After Registration

Once TestPyPI publisher is registered:

```bash
cd /home/ob/Development/Tools/chroma

# Delete old rc1 tag (if you pushed it)
git tag -d v0.2.0rc1
git push origin :refs/tags/v0.2.0rc1

# Create new rc1 tag for testing
git tag -a v0.2.0rc1 -m "Pre-release testing with Trusted Publishing"
git push origin v0.2.0rc1

# Watch: GitHub Actions → Publish to TestPyPI
# Should succeed now! (no 403 error)
```

---

## Questions?

**Q: Where's my GitHub username?**
A: Go to github.com → your profile → shows at top left

**Q: How do I know if it worked?**
A: TestPyPI shows "✅ Active" next to your publisher

**Q: What if I see a different error?**
A: Check docs/guides/troubleshooting.md or TRUSTED_PUBLISHING_SETUP.md

---

**Next action:** Register the Trusted Publisher on TestPyPI (takes 5 minutes)

Then test with `git tag v0.2.0rc1 && git push origin v0.2.0rc1`
