#!/bin/bash

# Exit on error
set -e

# Unset custom index URLs to use public PyPI only
unset UV_INDEX_URL
unset UV_EXTRA_INDEX_URL
unset PIP_INDEX_URL
unset PIP_EXTRA_INDEX_URL

uv sync --extra dev

echo "=== Markdeck PyPI Publishing Script ==="
echo ""

# Check if we're on the main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "❌ Error: Not on main branch (currently on: $CURRENT_BRANCH)"
    echo "   Please switch to main branch before publishing."
    exit 1
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Error: Working directory is not clean"
    echo "   Please commit or stash your changes before publishing."
    git status --short
    exit 1
fi

# Pull latest changes
echo "📥 Pulling latest changes from remote..."
git pull

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Please fix before publishing."
    exit 1
fi

# Build the package
echo "📦 Building package..."
python -m build

# Check the package
echo "🔍 Checking package..."
python -m twine check dist/*

# Show package info
echo ""
echo "📋 Package contents:"
tar -tzf dist/*.tar.gz | head -20

echo ""
echo "📊 Package size:"
ls -lh dist/

# Prompt for confirmation
echo ""
echo "Ready to publish to PyPI!"
echo "Package: markdeck"
echo "Version: $(python -c "import tomllib; f = open('pyproject.toml', 'rb'); data = tomllib.load(f); print(data['project']['version']); f.close()")"
echo ""
read -p "Do you want to proceed? (yes/no): " -r
echo

if [[ ! $REPLY =~ ^[Yy]es$ ]]; then
    echo "❌ Publishing cancelled."
    exit 1
fi

# Upload to PyPI
echo "🚀 Uploading to PyPI..."
python -m twine upload dist/*

# Create git tag
VERSION=$(python -c "import tomllib; f = open('pyproject.toml', 'rb'); data = tomllib.load(f); print(data['project']['version']); f.close()")
echo ""
echo "📌 Creating git tag v$VERSION..."
git tag -a "v$VERSION" -m "Release version $VERSION"
git push origin "v$VERSION"

echo ""
echo "✅ Successfully published markdeck v$VERSION to PyPI!"
echo "🔗 https://pypi.org/project/markdeck/"
