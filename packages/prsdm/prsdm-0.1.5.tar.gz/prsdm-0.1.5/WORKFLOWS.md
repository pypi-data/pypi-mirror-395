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

1. **Normal Commit:**
```bash
git status
git add .
git commit -m "Prepare for release"
git push
```

2. **Bump version and create tag:**

   **Recommended (using script):**
```bash
   ./release.sh patch   # Bumps patch version (0.0.4 → 0.0.5)
   # or
   ./release.sh minor   # Bumps minor version (0.0.4 → 0.1.0)
   # or
   ./release.sh major   # Bumps major version (0.0.4 → 1.0.0)
   ```

   **Manual approach:**
```bash
   uv version --bump patch
   git add pyproject.toml
   git commit -m "v0.0.4"  # Use tag name as commit message (like OpenAI)
   git tag -a v0.0.4 -m "v0.0.4"  # Create annotated tag (required for --follow-tags)
   git push --follow-tags  # Pushes commit + annotated tag in one command
   ```

   **Note on tags:**
   - `git tag v0.0.4` creates a lightweight tag (just a pointer) - won't work with `--follow-tags`
   - `git tag -a v0.0.4 -m "v0.0.4"` creates an annotated tag (includes metadata) - required for `--follow-tags`
   - `--follow-tags` only pushes annotated tags that point to commits being pushed (prevents pushing unwanted tags)
   - Reference: [Git documentation](https://git-scm.com/docs/git-push.html) and [release-it issue #43](https://github.com/release-it/release-it/issues/43)

3. **Create GitHub Release (triggers publish workflow):**
   - Go to repository → **Releases** → You should see a draft release for `v0.0.4`
   - Click **Publish release** (or edit and then publish)
   - This triggers the publish workflow automatically

4. **Check GitHub Actions:**
   - Go to your repository → **Actions** tab
   - You should see the "Publish to PyPI" workflow running
   - Wait for it to complete and verify it published successfully

## Summary

- **Regular commits/PRs** → Tests workflow (builds, no publish)
- **GitHub Releases** → Publish workflow (publishes to PyPI)
