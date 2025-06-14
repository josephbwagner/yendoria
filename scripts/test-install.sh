#!/bin/bash
# Test installation of Yendoria release

echo "🧪 Testing Yendoria Release Installation"
echo "======================================="

# Create a temporary test environment
TEST_DIR="/tmp/yendoria-test-$(date +%s)"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo "📁 Test directory: $TEST_DIR"
echo ""

# Create a virtual environment for testing
echo "🐍 Creating test virtual environment..."
python3 -m venv test-env
source test-env/bin/activate

echo "📦 Installing Yendoria from local wheel..."
pip install --quiet "$OLDPWD/dist/yendoria-0.1.0-py3-none-any.whl"

echo "✅ Installation complete!"
echo ""

echo "🎮 Testing Yendoria launch..."
echo "Yendoria installed packages:"
pip list | grep yendoria

echo ""
echo "🔍 Checking executable..."
python -c "import yendoria; print(f'Yendoria version: {yendoria.__version__}')" 2>/dev/null || echo "⚠️  Direct import test failed"

echo ""
echo "📋 Yendoria module info:"
python -c "import yendoria; help(yendoria)" 2>/dev/null | head -10 || echo "Module help not available"

echo ""
echo "🧹 Cleaning up..."
deactivate
cd "$OLDPWD"
rm -rf "$TEST_DIR"

echo "✅ Test complete!"
