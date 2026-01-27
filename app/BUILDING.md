# Building YouTube Downloader

This guide explains how to build standalone executables for macOS and Windows.

## Prerequisites

Ensure you have:
- Python 3.8+
- Virtual environment activated: `. .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows)
- All dependencies installed: `pip install -r requirements.txt`

## Quick Build

### macOS & Linux

```bash
# Make script executable (first time only)
chmod +x build.sh

# Run build
./build.sh
```

Output: `dist/VidGrab.app` (macOS) or `dist/VidGrab` (Linux)

### Windows

```bash
# Run build script
build.bat
```

Output: `dist\VidGrab.exe`

## Manual Build (Advanced)

If the scripts don't work, use PyInstaller directly:

### Install PyInstaller

```bash
pip install pyinstaller
```

### macOS / Linux

```bash
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
```

### Windows

```bash
pyinstaller ^
    --onefile ^
    --windowed ^
    --name VidGrab ^
    --add-data "core;core" ^
    --add-data "ui;ui" ^
    --hidden-import=yt_dlp ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    main.py
```

## Output Locations

After building, executables are in the `dist` folder:

- **macOS**: `dist/VidGrab.app` (app bundle)
- **Windows**: `dist/VidGrab.exe`
- **Linux**: `dist/VidGrab`

## Distribution

### macOS

**For App Distribution:**
```bash
# Create DMG (installer image)
hdiutil create \
    -volname "YouTube Downloader" \
    -srcfolder dist/VidGrab.app \
    -ov -format UDZO \
    YouTube-Downloader.dmg
```

Then distribute `YouTube-Downloader.dmg` to users.

**Code Signing (Optional but recommended):**
```bash
# Self-sign for local testing
codesign -s - dist/VidGrab.app

# For distribution, you'll need an Apple Developer account
```

### Windows

**For EXE Distribution:**
1. **Simple**: Just distribute `dist/VidGrab.exe`
2. **With Installer**: Use NSIS, MSI, or Inno Setup

**Example with NSIS:**
```bash
# Install NSIS: https://nsis.sourceforge.io/
# Create installer.nsi with NSIS script
makensis installer.nsi
```

**Example with InnoSetup:**
```
; installer.iss
[Setup]
AppName=YouTube Downloader
AppVersion=1.0.0
DefaultDirName={pf}\YouTube Downloader
DefaultGroupName=YouTube Downloader
OutputDir=dist
OutputBaseFilename=VidGrab-Setup

[Files]
Source: "dist\VidGrab.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\YouTube Downloader"; Filename: "{app}\VidGrab.exe"
```

### Linux

**For Distribution:**
```bash
# Create AppImage (recommended)
cd dist
wget https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
./appimagetool-x86_64.AppImage VidGrab VidGrab.AppImage

# Or create tar.gz archive
tar -czf VidGrab.tar.gz VidGrab
```

## Troubleshooting

### "Module not found" errors

If you get import errors, add the missing module to `--hidden-import`:

```bash
pyinstaller ... --hidden-import=module_name main.py
```

### App won't start

1. Check if running from terminal shows errors:
   - macOS: `./dist/VidGrab.app/Contents/MacOS/VidGrab`
   - Windows: Open Command Prompt and run `dist\VidGrab.exe`
   - Linux: `./dist/VidGrab`

2. Check the logs at `~/.vidgrab/logs/app.log`

### Large executable size

The executable includes Python, PyQt6, and yt-dlp, so it's typically:
- macOS: ~150-200MB
- Windows: ~120-150MB
- Linux: ~120-150MB

This is normal and acceptable for desktop apps.

### Missing dependencies at runtime

Ensure the built app has access to:
- `.vidgrab/config.json` (settings)
- `.vidgrab/queue.json` (saved queue)
- `.vidgrab/logs/` (log files)

These are created automatically in the user's home directory.

## CI/CD Automation

To automate builds on GitHub:

### .github/workflows/build.yml

```yaml
name: Build

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pip install pyinstaller
      - run: |
          if [ "$RUNNER_OS" == "Windows" ]; then
            powershell -Command build.bat
          else
            bash build.sh
          fi
      - uses: actions/upload-artifact@v2
        with:
          name: ${{ matrix.os }}-build
          path: dist/
```

## Next Steps

After building:

1. **Test** - Run the executable on a clean machine to ensure it works
2. **Create installer** - Package for easy distribution
3. **Upload to GitHub Releases** - Make available to users
4. **Update documentation** - Add download links to README

## Support

Having issues building? Check:
- PyInstaller docs: https://pyinstaller.org/
- yt-dlp compatibility: https://github.com/yt-dlp/yt-dlp
- PyQt6 documentation: https://www.riverbankcomputing.com/software/pyqt/

