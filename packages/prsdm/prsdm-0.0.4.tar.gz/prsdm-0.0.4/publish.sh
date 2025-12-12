#!/bin/bash

# Load .env file and export variables for uv publish
set -a
source .env
set +a

# Change to script directory
cd "$(dirname "$0")"

# Build the package (this will add new files to dist/)
uv build

# Get the current version from pyproject.toml
VERSION=$(grep '^version' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')
PACKAGE_NAME=$(grep '^name' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')

# Set uv publish environment variables
export UV_PUBLISH_USERNAME="__token__"
export UV_PUBLISH_PASSWORD="$PYPI_API_TOKEN"

# Publish only the current version files (keeps old versions in dist/ for reference)
# Best practice: Publish both wheel (.whl) and source distribution (.tar.gz)
# - Wheel: Faster installation, no build tools needed
# - Source: Required for some platforms, allows inspection of source code
# Note: PyPI doesn't require both, but publishing both ensures maximum compatibility
uv publish "dist/${PACKAGE_NAME}-${VERSION}-"* "dist/${PACKAGE_NAME}-${VERSION}.tar.gz"

echo "Published version ${VERSION} to PyPI"
echo "Old versions in dist/ are preserved"

