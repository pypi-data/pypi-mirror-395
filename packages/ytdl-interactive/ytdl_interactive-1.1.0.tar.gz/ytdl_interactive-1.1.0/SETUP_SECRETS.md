# Setting up GitHub Secrets for Automated Publishing

This guide explains how to configure GitHub Secrets to enable automated PyPI publishing.

## Prerequisites

- Repository admin access
- PyPI account (create at https://pypi.org/account/register/)

## Step-by-Step Guide

### 1. Create PyPI API Token

1. **Log in to PyPI**
   - Go to https://pypi.org/
   - Sign in with your account

2. **Navigate to API tokens**
   - Go to https://pypi.org/manage/account/token/
   - Or: Account settings → API tokens

3. **Create new token**
   - Click **"Add API token"**
   - Fill in the form:
     - **Token name**: `ytdl-github-actions` (or any descriptive name)
     - **Scope**: Choose one of:
       - **Entire account** - Token works for all your projects
       - **Project: ytdl-interactive** - Token only works for this project (more secure)

4. **Save the token**
   - Click **"Add token"**
   - **IMPORTANT**: Copy the token immediately!
   - Token format: `pypi-AgEIcHlwaS5vcmcC...` (starts with `pypi-`)
   - You won't be able to see it again!

### 2. Add Token to GitHub Secrets

1. **Navigate to repository settings**
   - Go to https://github.com/abd3lraouf/ytdl
   - Click **Settings** (tab at the top)

2. **Access Secrets section**
   - In the left sidebar, expand **Secrets and variables**
   - Click **Actions**

3. **Create new secret**
   - Click **"New repository secret"** (green button)
   - Fill in the form:
     - **Name**: `PYPI_API_TOKEN` (must be exactly this)
     - **Value**: Paste your PyPI token (the full token including `pypi-` prefix)

4. **Save the secret**
   - Click **"Add secret"**
   - You should see `PYPI_API_TOKEN` in your secrets list

### 3. Verify Setup

#### Check Secret Exists

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Verify `PYPI_API_TOKEN` is listed
3. You'll see when it was last updated, but not the value (that's secure!)

#### Test the Workflow

##### Option 1: Manual Test (Safe)

1. Go to **Actions** tab
2. Select **"Publish to PyPI"** workflow
3. Click **"Run workflow"** dropdown
4. Check **"Skip PyPI upload"** (for testing)
5. Click **"Run workflow"**
6. Watch the workflow run - it should build successfully

##### Option 2: Create Test Release

1. Create a test tag:
   ```bash
   git tag -a v1.0.1-test -m "Test release"
   git push origin v1.0.1-test
   ```

2. Create a GitHub release from this tag
3. Watch the workflow run in **Actions** tab
4. Check if package appears on PyPI

## Security Best Practices

### Token Scope

- ✅ **Recommended**: Project-specific token (only for ytdl-interactive)
- ⚠️ **Less secure**: Account-wide token (works for all projects)

### Token Rotation

- Rotate tokens periodically (every 6-12 months)
- Rotate immediately if token is exposed
- To rotate:
  1. Create new token on PyPI
  2. Update GitHub secret with new token
  3. Delete old token from PyPI

### Secret Protection

- ✅ Never commit tokens to git
- ✅ Never share tokens in issues/PRs
- ✅ Use GitHub Secrets (encrypted)
- ✅ Limit token scope when possible
- ❌ Don't use personal tokens
- ❌ Don't hardcode in workflows

## Troubleshooting

### Workflow fails with "Invalid or non-existent authentication information"

**Solution**:
- Secret name must be exactly `PYPI_API_TOKEN`
- Token must include the `pypi-` prefix
- Token must be valid (not expired or deleted)

### Workflow fails with "403 Forbidden"

**Solution**:
- Token scope doesn't include this project
- Create new token with correct scope
- Update GitHub secret

### Workflow doesn't trigger

**Solution**:
- Workflow only triggers on **published releases**, not drafts
- Check `.github/workflows/publish.yml` exists
- Verify workflow is enabled in **Actions** tab

### Can't find Secrets settings

**Solution**:
- You need **admin** access to the repository
- Settings tab only visible to admins
- Ask repository owner to add the secret

## Alternative: Trusted Publishing (PyPI 2023+)

PyPI now supports **Trusted Publishing** (no tokens needed):

1. **Configure on PyPI**
   - Go to project settings on PyPI
   - Add GitHub as trusted publisher
   - Specify: `abd3lraouf/ytdl` and workflow file

2. **Update workflow**
   - Remove `password:` line
   - GitHub OIDC handles authentication automatically

3. **Benefits**
   - No token management
   - More secure
   - Automatic rotation

See: https://docs.pypi.org/trusted-publishers/

## Workflow Files Reference

The repository includes these automated workflows:

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **Publish to PyPI** | `.github/workflows/publish.yml` | New release | Build and publish package |
| **CI** | `.github/workflows/ci.yml` | Push, PR | Run tests and checks |
| **Bump Version** | `.github/workflows/bump-version.yml` | Manual | Create new version/release |
| **Release Drafter** | `.github/workflows/release-drafter.yml` | Push to main | Auto-generate release notes |

## Getting Help

- **GitHub Secrets**: https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **PyPI Tokens**: https://pypi.org/help/#apitoken
- **Project Issues**: https://github.com/abd3lraouf/ytdl/issues

---

**Setup complete!** Your repository now has automated PyPI publishing. 🚀
