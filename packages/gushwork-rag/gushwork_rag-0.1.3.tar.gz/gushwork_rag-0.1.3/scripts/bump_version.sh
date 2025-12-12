#!/bin/bash
# Version bumping script for gushwork-rag SDK

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PYTHON_DIR"

# Get current version
CURRENT_VERSION=$(grep -E '^version = ' pyproject.toml | sed -E 's/version = "([^"]+)"/\1/')
echo "Current version: $CURRENT_VERSION"

# Parse version parts
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

echo ""
echo "What type of version bump?"
echo "1) Patch (0.1.1 -> 0.1.2) - Bug fixes"
echo "2) Minor (0.1.1 -> 0.2.0) - New features"
echo "3) Major (0.1.1 -> 1.0.0) - Breaking changes"
echo "4) Custom version"
echo ""
read -p "Choice [1-4]: " choice

case $choice in
    1)
        PATCH=$((PATCH + 1))
        NEW_VERSION="$MAJOR.$MINOR.$PATCH"
        ;;
    2)
        MINOR=$((MINOR + 1))
        PATCH=0
        NEW_VERSION="$MAJOR.$MINOR.$PATCH"
        ;;
    3)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        NEW_VERSION="$MAJOR.$MINOR.$PATCH"
        ;;
    4)
        read -p "Enter new version (e.g., 0.2.0): " NEW_VERSION
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "Bumping version: $CURRENT_VERSION -> $NEW_VERSION"
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cancelled."
    exit 1
fi

# Update pyproject.toml
echo "Updating pyproject.toml..."
sed -i.bak "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
rm -f pyproject.toml.bak

# Update __init__.py
echo "Updating __init__.py..."
INIT_FILE="gushwork_rag/__init__.py"
if [ -f "$INIT_FILE" ]; then
    sed -i.bak "s/^__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" "$INIT_FILE"
    rm -f "$INIT_FILE.bak"
fi

echo ""
echo "✅ Version bumped to $NEW_VERSION"
echo ""
echo "Files updated:"
echo "  - pyproject.toml"
echo "  - gushwork_rag/__init__.py"
echo ""
echo "Next steps:"
echo "  1. Review the changes: git diff"
echo "  2. Commit: git commit -am \"Bump version to $NEW_VERSION\""
echo "  3. Build: ./scripts/build.sh"
echo "  4. Test: ./scripts/test_install.sh"
echo "  5. Publish: ./scripts/publish.sh"

