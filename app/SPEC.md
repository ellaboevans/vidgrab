# YouTube Downloader - Project Specification

## Overview
A PyQt6-based desktop application for downloading YouTube videos and playlists with a clean GUI, queue management, and progress tracking.

---

## ✅ Completed Features

### Core Functionality
- **Download Engine** - Uses `yt-dlp` to download videos in best quality (video+audio merged to MP4)
- **Playlist Support** - Can handle individual videos and playlists
- **Queue Management** - Add multiple URLs to a queue for batch downloading
- **Metadata Fetching** - Asynchronously fetches video titles before downloading
- **Progress Tracking** - Real-time progress bar and per-item progress display

### UI Features
- **Clean PyQt6 Interface** with intuitive layout
- **Folder Selection** - Choose download destination via file dialog
- **URL Input Field** - Paste single videos or playlist URLs
- **Download List Widget** - Visual queue showing:
  - Status indicators (⏳ Waiting, ▶️ In Progress, ✅ Completed, ❌ Failed)
  - Video titles
  - Individual progress percentages
- **Overall Progress Bar** - Track completion across all downloads
- **Status Label** - Display current operation status

### Controls
- **Add to Queue Button** - Add URLs to the download queue
- **Start Downloads Button** - Begin batch downloads from queue
- **Stop Button** - Pause/cancel current download and queue
- **Choose Folder Button** - Select destination directory

### Thread Management & Stability
- **Multi-threaded Downloads** - Prevents UI freezing during downloads
- **Graceful Thread Shutdown** - Proper cleanup with 5-second timeout before force-termination
- **Background Metadata Workers** - Fetch titles without blocking
- **Worker Thread Tracking** - Prevents orphaned threads
- **closeEvent() Handler** - Ensures all threads terminate before app closes

### Bug Fixes
- Fixed "QThread: Destroyed while thread still running" crash
- Implemented thread-safe stop/cancel mechanism
- Added timeout-based termination to prevent freezing

---

## 🔄 In Progress / Partially Done

### App Icon & Branding
- [x] Foundation for window icon in code
- [ ] Actual icon files created (.png, .ico, .icns)
- [ ] Icon integrated into executable builds

---

## ⏳ To Be Done

### High Priority (Essential for Community Release)

#### 1. **Application Branding & Packaging**
- [ ] Create professional app icon (256x256+ PNG minimum)
  - macOS `.icns` format (1024x1024)
  - Windows `.ico` format
  - Linux `.png` format
- [ ] Add icon to window and builds
- [ ] Create app name/logo assets
- [ ] Design splash screen (optional)

#### 2. **Settings & Preferences**
- [ ] Save user preferences (default download folder, quality settings)
- [ ] Configuration file (JSON/YAML) for persistent settings
- [ ] Settings dialog UI with:
  - Default download location
  - Video quality options (best, 1080p, 720p, audio-only)
  - Format selection (MP4, MKV, WebM)
  - Auto-start downloads on queue add (toggle)
  - Dark mode toggle

#### 3. **Enhanced Download Options**
- [ ] Audio-only extraction option
- [ ] Format selection menu
- [ ] Quality presets (480p, 720p, 1080p, best)
- [ ] Subtitle download option
- [ ] Thumbnail download option

#### 4. **Queue Persistence**
- [ ] Save queue to file on exit
- [ ] Load queue on app startup
- [ ] Clear queue button
- [ ] Remove individual items from queue
- [ ] Move items up/down in queue

#### 5. **Error Handling & Logging**
- [ ] Detailed error messages displayed to user
- [ ] Log file for debugging (`~/.vidgrab/logs/`)
- [ ] Retry mechanism for failed downloads
- [ ] Network error detection and user notification

#### 6. **User Experience Improvements**
- [ ] Right-click context menu on queue items (remove, retry, open folder)
- [ ] Drag-and-drop URL input support
- [ ] Keyboard shortcuts (Ctrl+A for Add, Ctrl+S for Start, Ctrl+Q for Quit)
- [ ] Notification on download completion
- [ ] Open folder button to show downloaded files
- [ ] Copy download link functionality

#### 7. **Build & Distribution**
- [ ] PyInstaller configuration for macOS app bundle
- [ ] Windows executable (.exe) with installer
- [ ] GitHub Releases with built artifacts
- [ ] Auto-update mechanism
- [ ] Code signing (macOS)

### Medium Priority (Polish & Features)

#### 8. **Advanced Download Features**
- [ ] Playlist filtering (download specific range of videos)
- [ ] Batch URL input (paste multiple URLs at once)
- [ ] Download history/recent downloads
- [ ] Duplicate URL detection in queue
- [ ] Resume interrupted downloads

#### 9. **Performance & Optimization**
- [ ] Cache metadata fetches to reduce API calls
- [ ] Parallel downloads (multiple simultaneous downloads with limit)
- [ ] Memory optimization for large playlists
- [ ] Download speed monitoring

#### 10. **Accessibility & Localization**
- [ ] Dark mode support
- [ ] Keyboard-only navigation
- [ ] Multi-language support (EN, ES, FR, DE, etc.)
- [ ] Accessibility labels for screen readers

### Low Priority (Nice-to-Have)

#### 11. **Analytics & Feedback**
- [ ] Download statistics dashboard
- [ ] Total videos downloaded count
- [ ] Total data downloaded
- [ ] Average download speed
- [ ] Crash reporting (optional, opt-in)

#### 12. **Advanced Features**
- [ ] Scheduled downloads
- [ ] Integration with system tray
- [ ] Watch folder for `.txt` files with URLs
- [ ] Video preview thumbnail in queue
- [ ] Conversion tools (format, codec)
- [ ] Basic video editing (trim, merge)

---

## 📋 Technical Debt & Maintenance

- [ ] Unit tests for core modules
- [ ] Integration tests for download flow
- [ ] Code documentation and docstrings
- [ ] Type hints throughout codebase
- [ ] Refactor UI into separate components
- [ ] Configuration management class
- [ ] Proper exception hierarchy
- [ ] CI/CD pipeline (GitHub Actions)

---

## 🚀 Minimum Viable Product (MVP) for Community Release

To make this app immediately useful to the community, prioritize these:

1. ✅ **Core download functionality** (DONE)
2. ✅ **Queue management** (DONE)
3. ✅ **Thread safety & stability** (DONE)
4. **Settings persistence** (saves user preferences)
5. **Professional app icon** (branding)
6. **Build executables** (macOS, Windows)
7. **Error handling & logging** (user-friendly errors)
8. **Queue persistence** (save progress between sessions)
9. **Documentation** (README with screenshots)
10. **Keyboard shortcuts** (productivity)

---

## 📦 Dependencies

Current:
- `PyQt6==6.10.2` - GUI framework
- `yt-dlp==2025.12.8` - Download backend
- `PyQt6-Qt6==6.10.1` - Qt bindings
- `PyQt6_sip==13.11.0` - SIP bindings

Future considerations:
- `pydantic` - Settings validation
- `python-dotenv` - Environment config
- `pytest` - Unit testing
- `pyinstaller` - Build executables

---

## 📁 Project Structure

```
vidgrab/
├── ui/
│   ├── app.py              # Main PyQt6 GUI application
│   └── __init__.py
├── core/
│   ├── engine.py           # yt-dlp download wrapper
│   ├── queue.py            # Queue management
│   ├── hooks.py            # Download progress hooks
│   ├── types.py            # Data classes
│   └── __init__.py
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── SPEC.md                 # This file
└── README.md               # User documentation (TODO)
```

---

## 🎯 Success Metrics

The app will be community-ready when:
- ✅ No crashes or freezes during normal operation
- ✅ Successfully downloads videos from YouTube
- ✅ Can handle playlists and batch downloads
- ✅ Professional appearance (icon, branding)
- ✅ Can be built as standalone executables
- ✅ Basic documentation exists
- ✅ Settings are persisted between sessions
- ✅ User-friendly error messages
- ✅ All downloads can be paused/stopped gracefully

---

## 🤝 Community Feedback Needed

Before full release, gather feedback on:
1. Which download format/quality options are most wanted?
2. Should parallel downloads be a feature?
3. Are there missing quality-of-life features?
4. Which platforms are most important (macOS/Windows/Linux)?
5. Would users pay for premium features (conversion, editing)?

