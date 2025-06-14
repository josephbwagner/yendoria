#!/bin/bash
# Release Analytics Script

echo "📊 Yendoria Release Analytics"
echo "============================"

# Get repository information
REPO_URL="https://api.github.com/repos/josephbwagner/yendoria"

echo "🏷️  Latest Releases:"
echo "-------------------"
curl -s "${REPO_URL}/releases" | \
    jq -r '.[] | "\(.tag_name) - \(.name) (\(.published_at | split("T")[0]))"' | \
    head -5 2>/dev/null || echo "API request failed or jq not available"

echo ""
echo "📈 Repository Stats:"
echo "-------------------"
curl -s "${REPO_URL}" | \
    jq -r '"Stars: \(.stargazers_count), Forks: \(.forks_count), Issues: \(.open_issues_count)"' \
    2>/dev/null || echo "API request failed or jq not available"

echo ""
echo "📦 Latest Release Assets:"
echo "------------------------"
curl -s "${REPO_URL}/releases/latest" | \
    jq -r '.assets[] | "\(.name) (\(.download_count) downloads)"' \
    2>/dev/null || echo "API request failed or jq not available"

echo ""
echo "🏗️  Build Status (Local):"
echo "------------------------"
if [ -f "dist/yendoria-0.1.0-py3-none-any.whl" ]; then
    echo "✅ Wheel package: $(ls -lh dist/*.whl | awk '{print $5 " " $9}')"
fi

if [ -f "dist/yendoria-0.1.0.tar.gz" ]; then
    echo "✅ Source package: $(ls -lh dist/*.tar.gz | awk '{print $5 " " $9}')"
fi

echo ""
echo "🎯 Next Steps:"
echo "-------------"
echo "• Share your release with the roguelike community"
echo "• Submit to Python Package Index (PyPI) for easier installation"
echo "• Create release notes and showcase features"
echo "• Monitor download metrics and user feedback"
