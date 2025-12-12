# GitHub Actions Workflows

## Setup

### Option 1: Trusted Publishing (Recommended - like OpenAI)
1. Go to PyPI: https://pypi.org/manage/account/publishing/
2. Add a new pending publisher for your GitHub repository
3. Configure the GitHub environment in your repo:
   - Settings → Environments → New environment → Name: `pypi`
   - The workflow will use OIDC for authentication (no token needed)

### Option 2: API Token (Simpler)
1. Add `PYPI_API_TOKEN` to GitHub Secrets:
   - Settings → Secrets and variables → Actions → Repository secrets
   - New secret: `PYPI_API_TOKEN` = your PyPI token
2. Update `publish.yml` to use the token (remove trusted publishing parts)

## Workflow Files

- `.github/workflows/tests.yml` - Tests workflow
- `.github/workflows/publish.yml` - Publish workflow

## Publication Workflow

### Quick Checklist

1. **Make sure everything is committed:**
```bash
git status
git add .
git commit -m "Prepare for release"
git push
```

2. **Bump version:**
```bash
uv version --bump patch
git add pyproject.toml
git commit -m "Bump version to 0.0.4"
git push
```

3. **Create GitHub Release (triggers publish workflow):**
   - Option A: Push a tag (GitHub auto-creates release):
     ```bash
     git tag v0.0.4
     git push origin v0.0.4
     # Then go to Releases and click "Publish release"
     ```
   
   - Option B: Create release manually:
     - Go to repository → **Releases** → **Draft a new release**
     - Tag: `v0.0.4` (must match version in pyproject.toml)
     - Click **Publish release**
   
   - This triggers the publish workflow automatically

4. **Check GitHub Actions:**
   - Go to your repository → **Actions** tab
   - You should see the "Publish to PyPI" workflow running
   - Wait for it to complete and verify it published successfully

## Summary

- **Regular commits/PRs** → Tests workflow (builds, no publish)
- **GitHub Releases** → Publish workflow (publishes to PyPI)
