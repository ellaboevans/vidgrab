#!/bin/bash

# VidGrab Build Script
# Builds executables for the current platform

set -e

echo "==================================="
echo "VidGrab Build Script"
echo "==================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Virtual environment not activated"
    echo "Please activate it first:"
    echo "  source .venv/bin/activate"
    exit 1
fi

# Check if PyInstaller is installed
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo "📦 Installing PyInstaller..."
    pip install pyinstaller
fi

# Determine platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macOS"
    OUTPUT_NAME="VidGrab.app"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    PLATFORM="Windows"
    OUTPUT_NAME="VidGrab.exe"
else
    PLATFORM="Linux"
    OUTPUT_NAME="VidGrab"
fi

echo "🔨 Building for: $PLATFORM"
echo ""

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist *.spec

# Build
echo "⏳ Building executable (this may take a minute)..."
pyinstaller \
    --onefile \
    --windowed \
    --name VidGrab \
    --add-data "core:core" \
    --add-data "ui:ui" \
    --hidden-import=yt_dlp \
    --hidden-import=PyQt6.QtCore \
    --hidden-import=PyQt6.QtGui \
    --hidden-import=PyQt6.QtWidgets \
    main.py

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo ""
echo "✅ Build successful!"
echo ""

# Show output location
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📦 Output: dist/VidGrab.app"
    echo ""
    echo "To run:"
    echo "  open dist/VidGrab.app"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "📦 Output: dist/VidGrab.exe"
    echo ""
    echo "To run:"
    echo "  dist/VidGrab.exe"
else
    echo "📦 Output: dist/VidGrab"
    echo ""
    echo "To run:"
    echo "  ./dist/VidGrab"
fi

echo ""
echo "📝 To distribute:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "  • Create a .dmg: hdiutil create -volname 'VidGrab' -srcfolder dist -ov -format UDZO VidGrab.dmg"
    echo "  • Sign app (optional): codesign -s - dist/VidGrab.app"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  • Create installer with NSIS or MSI"
    echo "  • Or just zip: dist/VidGrab.exe"
else
    echo "  • Create AppImage or .tar.gz archive"
fi

echo ""
