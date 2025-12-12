# Trusted Publishing Setup Guide

**Updated:** December 3, 2025
**Status:** ✅ Workflows configured for Trusted Publishing

---

## What Changed

Your GitHub Actions workflows have been updated to use **Trusted Publishing** (OIDC) instead of API token authentication. This is:

- ✅ **More Secure** - No long-lived API tokens stored as secrets
- ✅ **Automatic** - GitHub Actions generates ephemeral tokens for each publish
- ✅ **Best Practice** - Recommended by PyPI and OpenID Foundation
- ✅ **Future-Proof** - Aligns with PyPI's long-term security strategy

---

## What to Do Now

### Step 1: Register Trusted Publisher (TestPyPI) - 5 minutes

1. Go to: https://test.pypi.org/manage/project/chroma-ingestion/settings/publishing/
2. Click **"Add a new pending publisher"**
3. Fill in the form:
   - **Publisher name:** GitHub (or similar)
   - **Repository owner:** `<your-github-username>`
   - **Repository name:** `chroma`
   - **Workflow name:** `publish-test.yml`
   - **Environment name:** (leave blank)

4. Click **"Save pending publisher"**
5. GitHub will prompt you to verify - click the link in the GitHub notification
6. Click **"Approve"** on TestPyPI

✅ Done! TestPyPI is configured.

### Step 2: Register Trusted Publisher (Production PyPI) - 5 minutes

1. Go to: https://pypi.org/manage/project/chroma-ingestion/settings/publishing/
2. Click **"Add a new pending publisher"**
3. Fill in the form:
   - **Publisher name:** GitHub (or similar)
   - **Repository owner:** `<your-github-username>`
   - **Repository name:** `chroma`
   - **Workflow name:** `publish.yml`
   - **Environment name:** (leave blank)

4. Click **"Save pending publisher"**
5. GitHub will prompt you to verify - click the link in the GitHub notification
6. Click **"Approve"** on PyPI

✅ Done! Production PyPI is configured.

### Step 3: (Optional) Revoke Old API Tokens

If you're no longer using the old `PYPI_API_TOKEN` and `PYPI_API_TOKEN_TEST` secrets, you should:

1. Go to https://pypi.org/account/api-tokens/ (Production)
2. Go to https://test.pypi.org/account/api-tokens/ (Test)
3. Find your tokens and click **"Delete"**
4. Go to your GitHub repo → Settings → Secrets and variables → Actions
5. Delete the secrets: `PYPI_API_TOKEN` and `PYPI_API_TOKEN_TEST`

This reduces the attack surface - if your GitHub account is compromised, attackers can no longer use those tokens.

---

## How It Works

### Before (API Token)
```
1. GitHub Actions stores API token as secret
2. Workflow runs and uses token directly
3. ⚠️ Token is long-lived and can be misused if stolen
4. ⚠️ Need to manually update if token expires
```

### After (Trusted Publishing)
```
1. GitHub Actions OIDC provider generates ephemeral token
2. PyPI validates it came from your specific workflow
3. ✅ Token expires after ~5 minutes (automatic)
4. ✅ Token only works for your repository
5. ✅ No manual secret management needed
```

---

## Updated Workflows

Both workflows now include:

```yaml
permissions:
  id-token: write  # Enable OIDC token generation
```

This allows GitHub Actions to generate temporary OIDC tokens for PyPI authentication.

### TestPyPI Workflow (`publish-test.yml`)

Triggered on pre-release tags: `v0.2.0rc1`, `v0.2.0a1`, `v0.2.0b1`

```yaml
- name: Upload to TestPyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    repository-url: https://test.pypi.org/legacy/
    skip-existing: true
```

**Note:** No `password` parameter - Trusted Publishing handles authentication automatically.

### Production PyPI Workflow (`publish.yml`)

Triggered on release tags: `v0.2.0`, `v1.0.0`, etc.

```yaml
- name: Upload to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
```

**Note:** No `password` parameter - Trusted Publishing handles authentication automatically.

---

## Release Process (Updated)

Once Trusted Publishers are configured:

### Pre-Release Testing

```bash
# Create pre-release tag
git tag -a v0.2.0rc1 -m "Release candidate"
git push origin v0.2.0rc1

# Watch: GitHub repo → Actions → "Publish to TestPyPI"
# Should complete in 2-3 minutes with no authentication errors
```

### Production Release

```bash
# Create production release tag
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0

# Watch: GitHub repo → Actions → "Publish to PyPI"
# Should complete in 2-3 minutes with no authentication errors
```

---

## Testing Your Setup

### Quick Verification

1. Go to your GitHub repo → **Actions** tab
2. Look for recent workflow runs under:
   - "Publish to TestPyPI" (for rc/a/b tags)
   - "Publish to PyPI" (for release tags)
3. Click the most recent run
4. All steps should pass without authentication errors

### Full Integration Test

After setup, trigger a test release:

```bash
cd /home/ob/Development/Tools/chroma

# Test the TestPyPI workflow
git tag -a v0.2.0rc1 -m "Testing Trusted Publishing"
git push origin v0.2.0rc1

# Wait for GitHub Actions to complete (~3 minutes)
# Then verify on TestPyPI:
pip install -i https://test.pypi.org/simple/ chroma-ingestion==0.2.0rc1
```

If it works, you're ready for production!

---

## Troubleshooting

### "Publisher not found" error

**Problem:** Workflow fails with "Publisher not found" or authentication error.

**Solution:**
1. Verify you completed **Step 1** and **Step 2** above
2. Check the publisher details match exactly:
   - Repository owner (your GitHub username)
   - Repository name (should be `chroma`)
   - Workflow name (should be `publish-test.yml` or `publish.yml`)
3. Try triggering the workflow again - sometimes it takes a minute for PyPI to register the publisher

### Old token still in workflow

**Problem:** You see a warning about `password` parameter still being used.

**Solution:**
1. Verify the workflow files were updated correctly:
   ```bash
   grep -n "password:" /home/ob/Development/Tools/chroma/.github/workflows/publish*.yml
   # Should return 0 results (no matches)
   ```
2. If you see matches, the update didn't complete. Contact support.

### Package not appearing on PyPI

**Problem:** Package uploaded but doesn't appear on PyPI.

**Solution:**
1. Wait 5-10 minutes for PyPI's cache to update
2. Check the GitHub Actions logs for any warnings
3. Visit: https://pypi.org/project/chroma-ingestion/ to verify
4. If still missing, check the workflow output for errors

---

## Security Benefits

### Eliminated Risks

- ❌ No long-lived API tokens in GitHub Secrets
- ❌ No token rotation needed (automatic)
- ❌ No risk of token leakage through GitHub's Secret management
- ❌ No accidental token commits to version control

### New Protections

- ✅ Tokens are automatically short-lived (~5 minutes)
- ✅ Tokens only work from your specific GitHub repository
- ✅ Tokens only work for your specific PyPI project
- ✅ Full audit trail in PyPI logs
- ✅ GitHub's OIDC provider is cryptographically verified

---

## FAQ

### Q: Can I still use API tokens?
**A:** Yes, but Trusted Publishing is recommended. You can use both simultaneously during transition.

### Q: What if I lose my GitHub account?
**A:** Someone who gains control of your GitHub account could publish packages. However:
- The workflow is locked to specific branches/tags
- PyPI's Trusted Publishing logs all actions
- You can revoke publishers immediately from PyPI settings

### Q: How do I revoke a publisher?
**A:**
1. Go to PyPI project settings → Publishing
2. Click the publisher you want to remove
3. Click "Remove this publisher"
4. Confirm deletion

### Q: Can I use this for private packages?
**A:** No, Trusted Publishing is currently only for public PyPI packages. For private packages, continue using API tokens.

### Q: Does this work with Test PyPI and Production PyPI?
**A:** Yes! You can register separate publishers for:
- `publish-test.yml` → test.pypi.org
- `publish.yml` → pypi.org

---

## Next Steps

1. ✅ **Set up Trusted Publishers** (Step 1 & 2 above)
2. ✅ **Test with pre-release** (v0.2.0rc1 tag)
3. ✅ **Release to production** (v0.2.0 tag)
4. ✅ **(Optional) Remove old API token secrets**

---

## References

- [PyPI Documentation: Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [GitHub Documentation: OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [GitHub Actions: PyPI Publish Action](https://github.com/pypa/gh-action-pypi-publish)

---

## Summary

Your workflows are now configured for **Trusted Publishing**, which is:
- ✅ More secure (no long-lived tokens)
- ✅ Easier to manage (automatic)
- ✅ Industry best practice
- ✅ Ready for production

**Next action:** Register Trusted Publishers on PyPI (Steps 1 & 2 above), then test with v0.2.0rc1!

---

**Generated:** December 3, 2025
**chroma-ingestion v0.2.0**
**Status:** ✅ **TRUSTED PUBLISHING CONFIGURED**
