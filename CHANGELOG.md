# Changelog - VidGrab

All notable changes to VidGrab are documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-02-01

### ✨ Initial Release - Production Ready

VidGrab v1.0.0 is a fully-featured VidGrab for macOS with professional UI, queue management, and real-time progress tracking.

---

### Added

#### Core Functionality

- **Download Engine** - yt-dlp integration for YouTube video downloads
  - Support for single videos and playlists
  - Quality selection: best, 1080p, 720p, 480p, audio-only
  - Format selection: MP4, MKV, WebM
  - Automatic video+audio merging via FFmpeg

- **Queue Management** - Full batch download support
  - Add multiple URLs to download queue
  - Start/pause/stop queue processing
  - Per-item status tracking (Waiting, Downloading, Completed, Failed, Cancelled)
  - Automatic queue persistence across sessions

- **Multi-threaded Downloads** - Non-blocking UI during downloads
  - `DownloadWorker` thread for downloads
  - `MetadataWorker` thread for title fetching
  - Graceful thread shutdown with 5-second timeout
  - Qt signals/slots for thread-safe UI updates

- **Real-time Progress Tracking** - Live download feedback
  - Percentage progress (0% → 100%)
  - Download size info (e.g., "6.2MiB of 37.80MiB")
  - Speed monitoring (e.g., "494.91KiB/s")
  - ETA calculation (e.g., "01:13")
  - Per-item progress in queue list
  - Global progress bar synchronization

#### User Interface

- **Main Window** - Clean, responsive PyQt6 interface
  - URL input field with placeholder
  - Folder selection with file dialog
  - Queue list widget with color-coded status indicators
  - Overall progress bar with detailed feedback
  - Start/Stop/Clear buttons

- **Settings Dialog** - Customizable preferences
  - Quality selector (4 tiers: best, 1080p, 720p, 480p, audio-only)
  - Format selector (MP4, MKV, WebM)
  - Download folder configuration
  - Auto-persist settings on change

- **Professional Dark Theme** - Polished visual design
  - Cyan accent color (#00d9ff)
  - Dark background (#0f1419)
  - Color-coded status indicators:
    - Waiting: Gray (#a0aec0)
    - Downloading: Cyan (#00d9ff)
    - Completed: Green (#34d399)
    - Failed: Red (#f87171)
    - Cancelled: Muted (#718096)

- **Minimal Splash Screen** - 600×400 professional branding
  - Clean typography with title + subtitle
  - Cyan accent bar for brand identity
  - Progress indicator (three dots)
  - Builder attribution ("Built by Ella Boevans")
  - 1-second display for fast startup

#### Data Management

- **Settings Persistence** - Auto-save user preferences
  - Download folder location
  - Quality and format settings
  - Automatic restore on app startup
  - Location: `~/.vidgrab/config.json`

- **Queue Persistence** - Auto-save download queue
  - Incomplete items saved on exit
  - Completed items excluded for cleanliness
  - Auto-restore on app startup
  - Location: `~/.vidgrab/queue.json`

#### Error Handling & Resilience

- **Retry Logic** - Automatic recovery from failures
  - 3-attempt retry on failed downloads
  - User-friendly error messages
  - Failed items marked with error details
  - Retry counter displayed in UI

- **URL Validation** - Smart input checking
  - YouTube URL pattern detection
  - Invalid URL rejection with clear messages
  - Duplicate URL detection within queue
  - Prevention of circular/malformed inputs

#### Logging & Debugging

- **Rotating File Logger** - Comprehensive debug logs
  - Location: `~/.vidgrab/logs/app.log`
  - Max file size: 5MB
  - Backup files: 5 rotating backups
  - Levels: INFO, WARNING, ERROR
  - Accessible from app: "View Logs" button

#### Build & Distribution

- **PyInstaller Configuration** - Standalone executable creation
  - Bundle Python 3.11, PyQt6, yt-dlp, FFmpeg
  - `--onedir` distribution for macOS .app bundles
  - Hidden imports specified for yt-dlp
  - Data files included (core, ui, assets)

- **GitHub Actions CI/CD** - Automated builds on release
  - macOS build with ad-hoc code signing
  - Windows executable generation
  - Linux binary creation
  - DMG packaging for distribution

- **Code Signing** - macOS security compliance
  - Ad-hoc code signing for distribution
  - Gatekeeper workaround documentation
  - xattr command provided for users

#### Platform Support

- **FFmpeg Dual-Mode** - Flexible dependency handling
  - Primary: pyffmpeg bundled binary (no system dependency)
  - Fallback: Auto-detect system FFmpeg
  - Graceful degradation if unavailable
  - Logging tracks which FFmpeg is used

- **Node.js Detection** - YouTube extraction robustness
  - Auto-detect Node.js from common paths
  - Support for NVM installations
  - Homebrew paths (M1/M2 Macs)
  - Fallback behavior if not found

#### Documentation

- **Installation Guide** - MACOS_INSTALLATION.md
  - DMG mounting instructions
  - Gatekeeper warning explanation
  - xattr quarantine removal command
  - Right-click → Open workaround

- **Build Documentation** - BUILDING.md
  - Development setup instructions
  - Virtual environment creation
  - Build script usage
  - macOS/Windows/Linux build procedures

- **Deployment Guide** - DEPLOYMENT.md
  - Release process step-by-step
  - CI/CD pipeline explanation
  - GitHub Releases publishing
  - Landing page updates

- **Project Specification** - SPEC.md
  - Feature list and roadmap
  - Technical architecture
  - MVP requirements
  - Future enhancement ideas

---

### Improvements (Session Updates)

#### Progress Display Enhancement

- Real-time percentage updates during single video downloads
- Previously: 0% → jumps to 100%
- Now: Smooth 0% → 35% → 50% → 100% progression
- Prevents UI jumping and improves user confidence

#### Progress Details Addition

- Extended progress information to user
- Display: "6.2MiB of 37.80MiB at 494.91KiB/s ETA 01:13"
- Helper functions for human-readable formatting
- Progress signal now carries detail string

#### Main Progress Bar Synchronization

- Global progress bar updates during active downloads
- Previously: Only showed batch completion
- Now: Real-time updates every 1-2% during download
- Better visual feedback for single downloads

#### Progress Bar Visibility Fix

- Text color changed from cyan to dark (#0f1419)
- Previously: Cyan text on cyan fill (invisible)
- Now: Dark text on cyan fill (readable)
- Improved accessibility and readability

#### Performance Optimization

- Concurrent fragment downloads: 4 → 8
- HTTP chunk size: Added 10MB configuration
- Effect: Individual stream downloads faster
- Overall download speed: ~1.5-1.8 MiB/s

#### Dependency Update

- yt-dlp: 2025.12.8 → 2026.1.29
- Latest stability fixes included
- Improved YouTube compatibility
- Better handling of protected videos

#### Splash Screen Redesign

- Size reduction: 1200×800 → 600×400
- Display time: 3.5 seconds → 1 second
- Design: Modern minimal aesthetic
  - Cyan accent bar for branding
  - Clean typography with shadows
  - Three-dot progress indicator
  - Builder attribution included
- Professional appearance without bloat

---

### Technical Details

#### Architecture

- Modular design: `core/` (engine, queue, logger) + `ui/` (app, dialogs)
- Qt signals/slots for thread-safe communication
- Enum-based state management (no magic strings)
- Singleton logger pattern (prevents duplicate handlers)
- Download session encapsulation for batch tracking

#### Dependencies

- PyQt6==6.10.2 (GUI framework)
- yt-dlp==2026.1.29 (download backend)
- pyffmpeg>=2.5 (FFmpeg bundling)
- PyInstaller==6.18.0 (executable creation)
- Pillow (splash screen generation)

#### File Structure

```
app/
├── core/
│   ├── engine.py          (yt-dlp wrapper, download logic)
│   ├── hooks.py           (progress callbacks with formatting)
│   ├── queue.py           (queue state management)
│   ├── types.py           (QueueItem, ItemStatus enum)
│   ├── settings.py        (Settings dataclass)
│   ├── settings_manager.py (JSON persistence)
│   ├── queue_persistence.py (Queue save/load)
│   ├── logger.py          (rotating file logger)
│   ├── validators.py      (URL validation)
│   └── download_session.py (batch download state)
├── ui/
│   ├── app.py             (main window, workers)
│   ├── settings_dialog.py (settings UI)
│   ├── splash_screen.py   (splash handling)
│   ├── splash_generator.py (splash image generation)
│   ├── splash_background.png (splash image)
│   ├── theme.py           (color constants)
│   └── styles.qss         (stylesheet)
├── main.py                (entry point)
└── requirements.txt       (dependencies)
```

#### Performance Metrics

- Startup: ~2-3 seconds (including splash)
- Title fetch: ~1-2 seconds per video (async)
- Single video DL: ~1.5-1.8 MiB/s
- Memory (idle): ~80-120MB
- Memory (downloading): ~150-200MB
- No memory leaks detected

---

### Fixed

- Single video progress display jumps (now smooth)
- Progress bar text visibility (cyan on cyan)
- Thread cleanup on app exit
- Metadata worker tracking
- Queue item status synchronization
- Settings not persisting (now auto-save)

### Known Limitations

1. **Sequential video+audio downloads**
   - Reason: yt-dlp limitation (no native format parallelization)
   - Workaround: Optimized individual downloads (8x fragments)
   - Impact: Minimal (still fast, transparent to user)

2. **Gatekeeper warning on macOS**
   - Reason: App not notarized (requires paid Apple Developer account)
   - Workaround: Right-click → Open or `xattr -cr` command
   - Impact: One-time user action, fully documented

3. **Large app size (~150-200MB)**
   - Reason: Includes Python, PyQt6, yt-dlp, FFmpeg
   - Benefit: No system dependencies required
   - Impact: Expected for desktop Python apps

---

### Security

- ✅ No circular imports
- ✅ Enum-based state (type-safe)
- ✅ Thread-safe signal/slot communication
- ✅ Input validation on all URLs
- ✅ Graceful error handling
- ✅ No unverified third-party code

---

### Tested

- ✅ Code compilation (all Python files)
- ✅ Import chain validation
- ✅ Thread safety verification
- ✅ UI responsiveness during downloads
- ✅ Settings persistence
- ✅ Queue persistence
- ✅ Error handling with retries
- ✅ Logging system
- ✅ macOS compatibility

---

## Roadmap - Planned Features

### v1.1 (High Priority)

- [ ] Keyboard shortcuts (Ctrl+A, Ctrl+S, Ctrl+Q)
- [ ] Right-click context menu on queue items
- [ ] Download completion notifications
- [ ] Open folder button to show downloaded files

### v1.2 (Medium Priority)

- [ ] Download history tracking
- [ ] Batch URL input (paste multiple at once)
- [ ] Playlist range filtering (download videos #10-20)
- [ ] Resume interrupted downloads

### v2.0 (Future Enhancements)

- [ ] Parallel concurrent downloads (architectural change)
- [ ] Scheduled/automatic downloads
- [ ] System tray integration
- [ ] Basic video editing (trim, merge)
- [ ] Multi-language support
- [ ] Download statistics dashboard

---

## Migration Guide

### From Beta to 1.0.0

No breaking changes. Existing settings and queue files are compatible:

- Settings: `~/.vidgrab/config.json` (unchanged format)
- Queue: `~/.vidgrab/queue.json` (unchanged format)
- Logs: `~/.vidgrab/logs/app.log` (unchanged format)

Simply update the executable and restart the app.

---

## Support

**macOS Installation Issues?**
See: [MACOS_INSTALLATION.md](MACOS_INSTALLATION.md)

**Build or Deployment Questions?**
See: [DEPLOYMENT.md](app/DEPLOYMENT.md)

**Development Setup?**
See: [BUILDING.md](app/BUILDING.md)

**Found a Bug?**
Open an issue on GitHub with:

- macOS version
- App version
- Steps to reproduce
- Log file content (`~/.vidgrab/logs/app.log`)

---

## Credits

**Built by:** Elabo Evans.  
**Powered by:** yt-dlp, PyQt6, FFmpeg  
**License:** [MIT License](LICENSE)

---

_Last Updated: February 1, 2026_
