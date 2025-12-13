# UV Commands for PyPI Package Development

## Project Setup

### `uv init` - Create a package project
```bash
uv init --package [name]   # Create a Python package project
uv init --package mypackage --name mypackage
```

## Version Management

### `uv version` - Manage project version
```bash
uv version                  # Show current version
uv version --short          # Show version only
uv version 0.0.2            # Set version to 0.0.2
uv version --bump patch     # Bump patch version (0.0.1 -> 0.0.2)
uv version --bump minor     # Bump minor version (0.0.1 -> 0.1.0)
uv version --bump major     # Bump major version (0.0.1 -> 1.0.0)
uv version --dry-run        # Preview version change
```

## Building Packages

### `uv build` - Build packages
```bash
uv build                    # Build from current directory
uv build --package mypkg    # Build specific package
uv build -o dist/           # Specify output directory
uv build --sdist             # Build only source distribution
uv build --wheel             # Build only wheel
```

## Publishing to PyPI

### `uv publish` - Publish to PyPI
```bash
# ⚠️ WARNING: By default, uv publish publishes ALL files in dist/
# This includes old versions if they're still in the dist/ directory!

# Option 1: Publish only current version (SAFEST - preserves old files)
# Get version from pyproject.toml and publish only that version
VERSION=$(grep '^version' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')
PACKAGE_NAME=$(grep '^name' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')
uv build
uv publish "dist/${PACKAGE_NAME}-${VERSION}-"* "dist/${PACKAGE_NAME}-${VERSION}.tar.gz"

# Option 2: Publish only specific files explicitly
uv publish dist/prsdm-0.0.2-py3-none-any.whl dist/prsdm-0.0.2.tar.gz

# Option 3: Clean dist/ first, then publish (deletes old files)
rm -rf dist/*
uv build
uv publish

# Option 4: Publish only wheels
uv publish dist/*.whl

# Using environment variables:
export UV_PUBLISH_USERNAME="__token__"
export UV_PUBLISH_PASSWORD="your_pypi_token"
VERSION=$(grep '^version' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')
PACKAGE_NAME=$(grep '^name' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')
uv publish "dist/${PACKAGE_NAME}-${VERSION}-"* "dist/${PACKAGE_NAME}-${VERSION}.tar.gz"

# Or using command line:
uv publish -u __token__ -p $TOKEN dist/prsdm-0.0.2-*
```

## Development Installation

### `uv pip install` - Install package in editable mode
```bash
uv pip install -e .         # Install in editable mode (for development)
uv pip install -e . --system  # Install to system Python
```

## Complete Package Development Workflow

### Create and publish a package
```bash
# 1. Initialize package project
uv init --package mypackage

# 2. Add dependencies
uv add numpy pandas

# 3. Install in editable mode for development
uv pip install -e .

# 4. Build package
uv build

# 5. Update version before release
uv version --bump patch

# 6. Rebuild with new version
uv build

# 7. Publish to PyPI (using .env file) - only current version
VERSION=$(grep '^version' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')
PACKAGE_NAME=$(grep '^name' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')
export UV_PUBLISH_USERNAME="__token__"
export UV_PUBLISH_PASSWORD=$(grep PYPI_API_TOKEN .env | cut -d '=' -f2)
uv publish "dist/${PACKAGE_NAME}-${VERSION}-"* "dist/${PACKAGE_NAME}-${VERSION}.tar.gz"
```

### Development workflow
```bash
# Install package in editable mode
uv pip install -e .

# Add new dependencies
uv add newpackage
uv lock

# Check dependency tree
uv tree

# Update version for release
uv version --bump patch
uv build
```

## Environment Variables for PyPI Publishing

- `UV_PUBLISH_USERNAME` - Username (use `__token__` for API tokens)
- `UV_PUBLISH_PASSWORD` - Password or token
- `UV_PUBLISH_TOKEN` - Alternative token variable

## Using .env file for PyPI token

Create a `.env` file in your project root:
```
PYPI_API_TOKEN=pypi-your_token_here
```

Then use it when publishing:
```bash
# Build the package
uv build

# Get version and publish only current version (preserves old files)
VERSION=$(grep '^version' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')
PACKAGE_NAME=$(grep '^name' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')
export UV_PUBLISH_USERNAME="__token__"
export UV_PUBLISH_PASSWORD=$(grep PYPI_API_TOKEN .env | cut -d '=' -f2)
uv publish "dist/${PACKAGE_NAME}-${VERSION}-"* "dist/${PACKAGE_NAME}-${VERSION}.tar.gz"
```

Or create a `publish.sh` script (SAFER - preserves old versions):
```bash
#!/bin/bash
set -a
source .env
set +a

cd "$(dirname "$0")"

# Build the package
uv build

# Get current version from pyproject.toml
VERSION=$(grep '^version' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')
PACKAGE_NAME=$(grep '^name' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')

# Publish only current version (keeps old versions in dist/ for reference)
export UV_PUBLISH_USERNAME="__token__"
export UV_PUBLISH_PASSWORD="$PYPI_API_TOKEN"
uv publish "dist/${PACKAGE_NAME}-${VERSION}-"* "dist/${PACKAGE_NAME}-${VERSION}.tar.gz"

echo "Published version ${VERSION} to PyPI"
echo "Old versions in dist/ are preserved"
```

## GitHub Actions Workflows

See `WORKFLOWS.md` for complete workflow documentation.

**Quick Summary:**
- **CI Workflow** - Runs on regular commits (builds, tests, no publish)
- **Publish Workflow** - Runs on version tags (builds and publishes to PyPI)

For detailed setup and usage instructions, see `WORKFLOWS.md`.
