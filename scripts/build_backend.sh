#!/bin/bash
# Build script for bundling Python backend with PyInstaller

set -e

echo "🔨 Building Python backend..."

cd "$(dirname "$0")/../backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup script first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade PyInstaller
pip install -q --upgrade pyinstaller

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist __pycache__

# Build with PyInstaller
echo "📦 Building executable..."
pyinstaller build_backend.spec --clean --noconfirm

# Check if build succeeded
if [ -f "dist/homestock-backend" ]; then
    echo "✅ Backend built successfully: dist/homestock-backend"
    chmod +x dist/homestock-backend
elif [ -f "dist/homestock-backend.exe" ]; then
    echo "✅ Backend built successfully: dist/homestock-backend.exe"
else
    echo "❌ Build failed - executable not found"
    exit 1
fi

deactivate

echo "✅ Backend build complete!"

