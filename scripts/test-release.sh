#!/bin/bash
# Test script for semantic-release setup

echo "🔍 Testing Semantic Release Setup"
echo "================================="

# Check current status
echo "📋 Current version: $(grep '^version = ' pyproject.toml | cut -d'"' -f2)"
echo "🏷️  Current tags:"
git tag -l | sort -V

echo ""
echo "📊 Checking commit history since last tag..."
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -z "$LAST_TAG" ]; then
    echo "No previous tags found"
    COMMIT_COUNT=$(git rev-list --count HEAD)
    echo "Total commits: $COMMIT_COUNT"
else
    echo "Last tag: $LAST_TAG"
    COMMIT_COUNT=$(git rev-list $LAST_TAG..HEAD --count)
    echo "Commits since last tag: $COMMIT_COUNT"
fi

echo ""
echo "🔧 Testing semantic-release commands..."
echo "Version calculation:"
poetry run semantic-release version --print 2>/dev/null || echo "Error in version calculation"

echo ""
echo "✅ Test complete"
