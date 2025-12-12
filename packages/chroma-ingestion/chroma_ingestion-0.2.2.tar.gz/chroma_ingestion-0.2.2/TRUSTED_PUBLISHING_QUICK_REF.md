# Trusted Publishing Migration - Quick Reference

**Status:** ✅ Complete - Ready for Setup
**Updated:** December 3, 2025

---

## What Changed (TL;DR)

| Aspect | Before | After |
|--------|--------|-------|
| **Authentication** | API Token in GitHub Secrets | OIDC from GitHub Actions |
| **Token Lifespan** | Long-lived (months/years) | Ephemeral (~5 minutes) |
| **Token Storage** | GitHub Secrets | Generated automatically |
| **Setup Complexity** | Create tokens, add secrets | Register publisher (5 min) |
| **Security** | Manual rotation needed | Automatic |
| **Error Message** | None | ✅ No more warnings! |

---

## Files Updated

### Workflows
- ✅ `.github/workflows/publish-test.yml` - Removed `password` parameter, added `permissions.id-token`
- ✅ `.github/workflows/publish.yml` - Removed `password` parameter, added `permissions.id-token`

### Documentation
- ✅ `TRUSTED_PUBLISHING_SETUP.md` - Complete setup guide (NEW)
- ✅ `NEXT_STEPS.md` - Updated with new process

---

## Setup Checklist

- [ ] Read: [TRUSTED_PUBLISHING_SETUP.md](TRUSTED_PUBLISHING_SETUP.md)
- [ ] Register TestPyPI Publisher: https://test.pypi.org/manage/project/chroma-ingestion/settings/publishing/
- [ ] Register PyPI Publisher: https://pypi.org/manage/project/chroma-ingestion/settings/publishing/
- [ ] Test with: `git tag -a v0.2.0rc1 -m "test" && git push origin v0.2.0rc1`
- [ ] Verify: Check GitHub Actions → "Publish to TestPyPI" passes
- [ ] Release with: `git tag -a v0.2.0 -m "Release" && git push origin v0.2.0`
- [ ] (Optional) Delete old API token secrets from GitHub

---

## Key Difference: No More Secrets!

### Old Way
```bash
# 1. Create token on PyPI
# 2. Add to GitHub as secret
# 3. Workflow uses: password: ${{ secrets.PYPI_API_TOKEN }}
```

### New Way
```bash
# 1. Register publisher on PyPI (proves it's really you)
# 2. GitHub Actions automatically generates temporary token
# 3. Workflow uses: (no password needed!)
```

---

## One-Minute Test

After registering publishers:

```bash
cd /home/ob/Development/Tools/chroma
git tag -a v0.2.0rc1 -m "test"
git push origin v0.2.0rc1
# Watch: GitHub Actions → Publish to TestPyPI
# Should see: No authentication errors!
```

---

## Why This Matters

**Old way:**
- ⚠️ API token could be stolen from GitHub
- ⚠️ Token could be leaked in logs
- ⚠️ Token could be found in git history
- ⚠️ Manual rotation required

**New way:**
- ✅ No token to steal (generated temporarily)
- ✅ No token in logs (handled by GitHub)
- ✅ No token in git history (not in code)
- ✅ Automatic expiration (5 minutes)

---

## FAQ

**Q: Do I need to do anything else?**
A: Just register the two publishers (10 minutes total). Done!

**Q: What if I have other projects?**
A: Each project needs its own publisher registration on PyPI.

**Q: Can I go back to API tokens?**
A: Yes, but not recommended. Trusted Publishing is more secure.

**Q: Does this break existing API tokens?**
A: No, you can keep them during transition. But eventually remove them.

---

## Next Action

👉 **Open [TRUSTED_PUBLISHING_SETUP.md](TRUSTED_PUBLISHING_SETUP.md) and follow Steps 1-2 (takes ~10 minutes)**

Then test with Step 3, then release with Step 4!

---

**chroma-ingestion v0.2.0 - Trusted Publishing Ready** ✅
