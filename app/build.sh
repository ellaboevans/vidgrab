#!/bin/bash

# VidGrab Build Script
# Builds executables for the current platform (or cross-platform on macOS)

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

# Determine platform and architecture
if [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macOS"
    OUTPUT_NAME="VidGrab.app"
    CURRENT_ARCH=$(uname -m)
    
    # Check for --universal flag
    BUILD_UNIVERSAL=false
    if [[ "$1" == "--universal" ]]; then
        BUILD_UNIVERSAL=true
    fi
    
    if [[ "$CURRENT_ARCH" == "arm64" && "$BUILD_UNIVERSAL" == "false" ]]; then
        # On Apple Silicon, default to building for Intel to help Intel users
        TARGET_ARCH="x86_64"
        echo "🍎 Detected: Apple Silicon (arm64)"
        echo "🔨 Building for: macOS x86_64 (Intel) to support Intel Mac users"
        echo ""
        echo "   Tip: Use './build.sh --universal' to create a universal binary (arm64 + x86_64)"
    elif [[ "$CURRENT_ARCH" == "arm64" && "$BUILD_UNIVERSAL" == "true" ]]; then
        TARGET_ARCH="universal2"
        echo "🍎 Detected: Apple Silicon (arm64)"
        echo "🔨 Building for: macOS universal2 (arm64 + x86_64)"
    elif [[ "$CURRENT_ARCH" == "x86_64" ]]; then
        TARGET_ARCH="x86_64"
        echo "💻 Detected: Intel Mac (x86_64)"
        echo "🔨 Building for: macOS x86_64"
    else
        TARGET_ARCH=$CURRENT_ARCH
        echo "🍎 Detected: $CURRENT_ARCH"
        echo "🔨 Building for: macOS $CURRENT_ARCH"
    fi
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    PLATFORM="Windows"
    OUTPUT_NAME="VidGrab.exe"
    TARGET_ARCH="x86_64"
    echo "🪟 Detected: Windows"
    echo "🔨 Building for: Windows x86_64"
else
    PLATFORM="Linux"
    OUTPUT_NAME="VidGrab"
    TARGET_ARCH=$(uname -m)
    echo "🐧 Detected: Linux $TARGET_ARCH"
    echo "🔨 Building for: Linux $TARGET_ARCH"
fi

echo ""

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist *.spec

# Build
echo "⏳ Building executable (this may take a minute)..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    pyinstaller \
        --onefile \
        --windowed \
        --name VidGrab \
        --target-arch=$TARGET_ARCH \
        --add-data "core:core" \
        --add-data "ui:ui" \
        --hidden-import=yt_dlp \
        --hidden-import=PyQt6.QtCore \
        --hidden-import=PyQt6.QtGui \
        --hidden-import=PyQt6.QtWidgets \
        main.py
else
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
fi

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo ""
echo "✅ Build successful!"
echo ""

# Show output location and next steps
if [[ "$OSTYPE" == "darwin"* ]]; then
    if [[ "$TARGET_ARCH" == "universal2" ]]; then
        echo "📦 Output: dist/VidGrab.app (universal binary: arm64 + x86_64)"
        echo ""
        echo "To verify:"
        echo "  lipo -info dist/VidGrab.app/Contents/MacOS/VidGrab"
    else
        echo "📦 Output: dist/VidGrab.app ($TARGET_ARCH)"
    fi
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
    if [[ "$CURRENT_ARCH" == "arm64" && "$BUILD_UNIVERSAL" == "false" ]]; then
        echo ""
        echo "  ℹ️  For Intel Mac users, this binary supports x86_64 architecture."
        echo "     To create a universal binary supporting both arm64 and x86_64:"
        echo "     ./build.sh --universal"
    fi
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  • Create installer with NSIS, MSI, or Inno Setup"
    echo "  • Or just zip: dist/VidGrab.exe"
else
    echo "  • Create AppImage or .tar.gz archive"
fi

echo ""
