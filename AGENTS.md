# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

VidGrab is a PyQt6 desktop application for downloading YouTube videos using yt-dlp. It features queue management, batch downloading, settings persistence, and cross-platform builds.

## Development Commands

### Setup
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run Application
```bash
python -m main
```

### Build Executable
```bash
# macOS/Linux
chmod +x build.sh && ./build.sh

# Windows
build.bat
```

Output goes to `dist/VidGrab.app` (macOS), `dist/VidGrab.exe` (Windows), or `dist/VidGrab` (Linux).

## Architecture

### Core Module (`core/`)
- `engine.py` - `DownloadEngine` class wrapping yt-dlp. Handles quality/format selection and download execution
- `queue.py` - `QueueManager` for download queue state (current_index, has_next, next_item)
- `types.py` - `QueueItem` dataclass with status states: Waiting, Downloading, Completed, Failed, Cancelled
- `hooks.py` - `progress_hook_factory()` creates yt-dlp progress callbacks
- `settings.py` - `Settings` dataclass and `SettingsManager` for JSON config persistence at `~/.vidgrab/config.json`
- `queue_persistence.py` - `QueuePersistence` saves/loads queue to `~/.vidgrab/queue.json`
- `validators.py` - `URLValidator` with YouTube URL pattern matching and duplicate detection
- `logger.py` - Rotating file logger to `~/.vidgrab/logs/app.log`

### UI Module (`ui/`)
- `app.py` - Main window (`YouTubeDownloader` QWidget), `DownloadWorker` (QThread for downloads), `MetadataWorker` (QThread for title fetching)
- `settings_dialog.py` - Settings dialog for quality, format, download folder
- `splash_screen.py` - Splash screen utilities

### Threading Model
- Downloads run in `DownloadWorker` QThread to prevent UI freezing
- Metadata fetches run in separate `MetadataWorker` threads
- Workers tracked in `self.metadata_workers` list; cleaned up in `closeEvent()`
- Stop mechanism: set `_is_running = False`, then `wait(timeout)` before `terminate()`

### Data Flow
1. User adds URL → `URLValidator` checks → `MetadataWorker` fetches title → `QueueManager.add()`
2. Start downloads → `QueueManager.next_item()` → `DownloadWorker` → `DownloadEngine.download()`
3. Progress hooks emit signals → UI updates list widget
4. On close → `QueuePersistence.save_queue()` (excludes completed items)

## User Data Locations
All user data stored in `~/.vidgrab/`:
- `config.json` - Settings (download folder, quality, format)
- `queue.json` - Persisted queue (incomplete items only)
- `logs/app.log` - Rotating logs (5MB max, 5 backups)

## Quality/Format Options
- Quality: `best`, `1080p`, `720p`, `480p`, `audio-only`
- Format: `mp4`, `mkv`, `webm`

These map to yt-dlp format strings in `DownloadEngine._get_format_string()`.

## macOS Distribution & Gatekeeper

### Issue
Apps downloaded from GitHub releases are blocked by Gatekeeper with "cannot verify is free of malware".

### Current Solution
CI/CD performs ad-hoc code signing (`codesign --sign -`) which allows users to bypass with right-click → Open.

### User Instructions (add to README)
Users must right-click the app → **Open** (not double-click) on first launch, or run:
```bash
xattr -cr /Applications/VidGrab.app
```

### Proper Solution (requires Apple Developer account $99/year)
1. Add secrets to GitHub: `MACOS_CERTIFICATE`, `MACOS_CERTIFICATE_PWD`, `APPLE_ID`, `APPLE_TEAM_ID`
2. Sign with Developer ID: `codesign --sign "Developer ID Application: Your Name (TEAMID)"`
3. Notarize: `xcrun notarytool submit --apple-id ... --password ... --team-id ...`
4. Staple: `xcrun stapler staple dist/VidGrab.app`
