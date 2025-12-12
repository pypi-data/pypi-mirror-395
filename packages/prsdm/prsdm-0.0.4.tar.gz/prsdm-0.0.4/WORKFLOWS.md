# GitHub Actions Workflows

## CI Workflow (`.github/workflows/ci.yml`)
**Purpose:** Build and test on code changes (no publishing)

**Triggers:** Regular commits, pull requests

```bash
# Regular code update
git add .
git commit -m "Fix bug"
git push
# ✅ Runs CI (builds, tests, no publish)
```

## Publish Workflow (`.github/workflows/publish.yml`)
**Purpose:** Build and publish to PyPI

**Triggers:** Version tags (e.g., `v0.0.4`)

```bash
# Release new version
uv version --bump patch
git add pyproject.toml
git commit -m "Bump version to 0.0.4"
git push

git tag v0.0.4
git push origin v0.0.4
# ✅ Runs publish workflow (builds and publishes)
```

## Setup

1. Add `PYPI_API_TOKEN` to GitHub Secrets:
   - Settings → Secrets and variables → Actions
   - New secret: `PYPI_API_TOKEN` = your PyPI token

2. Workflow files:
   - `.github/workflows/ci.yml` - CI workflow
   - `.github/workflows/publish.yml` - Publish workflow

## Summary

- **Regular commits** → CI workflow (no publish)
- **Version tags** → Publish workflow (publishes to PyPI)
