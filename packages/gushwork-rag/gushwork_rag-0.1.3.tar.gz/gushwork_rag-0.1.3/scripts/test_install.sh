#!/bin/bash
# Test installation script - installs the built package in a clean environment

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PYTHON_DIR"

echo "🧪 Testing package installation..."
echo ""

# Check if dist/ exists and has files
if [ ! -d "dist" ] || [ -z "$(ls -A dist/)" ]; then
    echo "❌ No distribution files found. Run build.sh first."
    exit 1
fi

# Create test directory
TEST_DIR="/tmp/gushwork_rag_test_$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo "📦 Creating test virtual environment..."
python -m venv test_env
source test_env/bin/activate

echo "📥 Installing package from wheel..."
pip install --upgrade pip --quiet
pip install "$PYTHON_DIR/dist"/*.whl

echo ""
echo "✅ Testing import..."
python -c "from gushwork_rag import GushworkRAG; print('✅ Import successful')"

echo ""
echo "✅ Testing basic functionality..."
python -c "
from gushwork_rag import GushworkRAG, __version__
print(f'✅ Version: {__version__}')
print('✅ All imports successful')
"

echo ""
echo "✅ Installation test passed!"
echo ""
echo "To test with your API:"
echo "  source test_env/bin/activate"
echo "  export GUSHWORK_API_KEY='your-key'"
echo "  export GUSHWORK_BASE_URL='your-url'"
echo "  python -c \"from gushwork_rag import GushworkRAG; client = GushworkRAG(api_key='your-key', base_url='your-url'); print(client.health_check())\""
echo ""
echo "Test environment: $TEST_DIR"
echo "To clean up: rm -rf $TEST_DIR"

