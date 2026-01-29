# VidGrab - Project Synopsis

## Overview

**VidGrab** is a cross-platform desktop application for downloading YouTube videos, playlists, and channels. Built with PyQt6 and powered by yt-dlp, it provides users with a clean, intuitive interface for batch downloading with full queue management, customizable quality/format options, and persistent state across sessions.

## Project Goals

1. **User-Friendly**: Provide an accessible desktop application without requiring command-line knowledge
2. **Reliable**: Implement robust error handling, automatic retries, and detailed logging
3. **Flexible**: Offer customizable quality and format options for different use cases
4. **Persistent**: Save queue and settings so users can resume downloads across sessions
5. **Cross-Platform**: Support macOS, Windows, and Linux with identical functionality

## Core Features

### Essential Features (MVP)
- ✅ Download single YouTube videos
- ✅ Download entire playlists and channels
- ✅ Queue management with pause/resume/cancel controls
- ✅ Customizable quality (best, 1080p, 720p, 480p, audio-only)
- ✅ Format selection (MP4, MKV, WebM)
- ✅ Real-time progress tracking
- ✅ Automatic retry on failure (up to 3 attempts)
- ✅ Settings persistence (download folder, quality, format)
- ✅ Queue persistence between sessions
- ✅ Application logging with log viewer

### Planned Features
- [ ] Dark mode UI
- [ ] Parallel downloads (multiple simultaneous)
- [ ] Video conversion/post-processing tools
- [ ] Scheduled downloads
- [ ] YouTube channel subscriptions
- [ ] Download history

## Technical Architecture

### Tech Stack
- **Frontend**: PyQt6 (desktop UI framework)
- **Backend**: Python 3.8+
- **Video Download**: yt-dlp (YouTube downloader library)
- **Storage**: JSON (config and queue persistence)
- **Logging**: Python's logging module with file rotation
- **Build**: PyInstaller (executable generation)

### Project Structure

```
youtube-downloader/
├── app/                          # PyQt6 desktop application
│   ├── main.py                   # Application entry point
│   └── core/                     # Core business logic
│       ├── engine.py             # DownloadEngine (yt-dlp wrapper)
│       ├── queue.py              # QueueManager (queue state/logic)
│       ├── types.py              # QueueItem dataclass, status enums
│       ├── hooks.py              # progress_hook_factory for yt-dlp callbacks
│       ├── settings.py           # Settings dataclass & SettingsManager
│       ├── queue_persistence.py  # QueuePersistence (save/load JSON)
│       ├── validators.py         # URLValidator (YouTube URL pattern matching)
│       └── logger.py             # Rotating file logger setup
│   └── ui/                       # User interface components
│       ├── app.py                # Main window, DownloadWorker, MetadataWorker
│       ├── settings_dialog.py    # Settings configuration UI
│       └── splash_screen.py      # Splash screen utilities
├── www/                          # (Future) Web/landing page
├── build.sh                      # macOS/Linux build script
├── build.bat                     # Windows build script
├── requirements.txt              # Python dependencies
├── AGENTS.md                     # Development guidelines
└── README.md                     # User documentation
```

### Key Components

#### Core Engine (`core/engine.py`)
- **DownloadEngine**: Wrapper around yt-dlp for video downloads
- Handles quality/format string generation
- Executes downloads with progress callbacks
- Maps user-friendly quality names to yt-dlp format codes

#### Queue Management (`core/queue.py`)
- **QueueManager**: Manages download queue state
- Tracks current index, completion status, next item
- Provides `add()`, `next_item()`, `mark_completed()` methods
- Stateless operations (state stored separately in QueueItem instances)

#### Data Models (`core/types.py`)
- **QueueItem**: Dataclass with URL, title, status (Waiting/Downloading/Completed/Failed/Cancelled)
- Status enums drive UI updates and persistence logic

#### Threading Model (`ui/app.py`)
- **DownloadWorker**: QThread subclass for non-blocking downloads
- **MetadataWorker**: QThread subclass for fetching video titles
- Main thread: UI responsiveness
- Worker threads: Long-running operations
- Cleanup: Workers tracked in `self.metadata_workers` list, terminated on app close

#### Settings Persistence (`core/settings.py`)
- **SettingsManager**: Handles config.json at `~/.vidgrab/config.json`
- Persists: download folder, quality preference, format preference
- Auto-loads on app startup

#### Queue Persistence (`core/queue_persistence.py`)
- **QueuePersistence**: Saves/loads queue.json at `~/.vidgrab/queue.json`
- Only persists incomplete items (excludes completed)
- Loads on app startup, saves on app close

#### Validation (`core/validators.py`)
- **URLValidator**: YouTube URL pattern matching
- Duplicate detection to prevent adding same URL twice
- Supports: video URLs, playlists, channels, handles

#### Logging (`core/logger.py`)
- Rotating file logger to `~/.vidgrab/logs/app.log`
- Max file size: 5MB with 5 backups
- Accessible via "View Logs" button

### Data Flow

```
User Action → Validation → Metadata Fetch → Queue Add
     ↓           ↓              ↓              ↓
  [URL]   → URLValidator  → MetadataWorker → QueueManager
            (duplicate?)      (get title)      (add item)
                                                ↓
                                          [QueueItem]
                                                ↓
                                        QueuePersistence
                                        (saves to JSON)

Start Downloads → QueueManager.next_item() → DownloadWorker
       ↓                 ↓                        ↓
  [Button]       → [get next URL]        → DownloadEngine
                                            (yt-dlp)
                                              ↓
                                         progress_hook
                                              ↓
                                         UI Updates
                                              ↓
                                         mark_completed()
```

## User Data Storage

All application data stored in user's home directory:

| Location | Purpose | Format |
|----------|---------|--------|
| `~/.vidgrab/config.json` | Settings (quality, format, download folder) | JSON |
| `~/.vidgrab/queue.json` | Incomplete queue items | JSON |
| `~/.vidgrab/logs/app.log` | Application logs | Text (rotating) |

No data is uploaded or stored remotely. All processing is local.

## Quality & Format Options

### Quality Levels
- `best` - Highest available quality
- `1080p` - Full HD
- `720p` - HD
- `480p` - Standard definition
- `audio-only` - Extract audio only (faster)

### Output Formats
- `mp4` - Most compatible (H.264 video + AAC audio)
- `mkv` - Matroska (supports multiple audio/subtitle tracks)
- `webm` - Web format (VP9 video + Opus audio)

These map to yt-dlp format strings in `DownloadEngine._get_format_string()`.

## Threading & Concurrency

### Design Principles
- **Non-blocking UI**: All long-running operations in separate threads
- **Signal-based communication**: QThreads emit signals to update UI
- **Safe cleanup**: Workers tracked and gracefully terminated on close
- **Single-threaded downloads**: One DownloadWorker at a time (queued model)

### Stop Mechanism
1. Set `_is_running = False` flag
2. Wait for worker with timeout: `wait(timeout)`
3. Force terminate if needed: `terminate()`
4. Clear metadata_workers list on close

## Error Handling

### Retry Logic
- Automatic retry up to 3 times on download failure
- Configurable via DownloadEngine parameters
- Status updated: Failed → Waiting (on retry)

### User Feedback
- Modal dialogs for critical errors
- Detailed error messages in logs
- View Logs button for troubleshooting
- Status indicators per queue item

## Cross-Platform Distribution

### macOS
- **Ad-hoc code signing** in CI/CD
- Users must right-click → Open on first launch (or run `xattr -cr /Applications/VidGrab.app`)
- **Proper solution**: Requires Apple Developer account ($99/year) for Developer ID signing + notarization

### Windows
- Direct executable distribution
- No special signing required (local apps run freely)

### Linux
- Executable with bundled dependencies
- Users make executable: `chmod +x VidGrab && ./VidGrab`

## Building & Distribution

### Development Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m main
```

### Building Executables
- **macOS/Linux**: `./build.sh` → `dist/VidGrab.app` or `dist/VidGrab`
- **Windows**: `build.bat` → `dist/VidGrab.exe`

### Distribution
- GitHub Releases: Upload .dmg (macOS), .exe (Windows), executable (Linux)
- Landing page: Auto-detects OS, offers correct download

## Security & Privacy

### Privacy Guarantees
- ✅ No data collection or tracking
- ✅ No remote analytics
- ✅ No account requirements
- ✅ Works completely offline (after yt-dlp update)
- ✅ All settings stored locally in user's home directory

### Security Considerations
- yt-dlp is open-source and actively maintained
- User input (URLs) validated before processing
- No code injection vectors (yt-dlp handles video processing)

## Known Limitations

1. **Age-restricted videos**: May not download without proper authentication headers
2. **Private/deleted videos**: Cannot be downloaded (expected behavior)
3. **Very large playlists** (1000+): Metadata fetching takes time
4. **Network-dependent**: Download speed depends on ISP and YouTube's servers
5. **Video format availability**: Not all videos available in all formats/qualities

## Performance Characteristics

### Metadata Fetching
- Per video: ~1-2 seconds (network dependent)
- Playlists: Linear time relative to number of videos

### Download Speed
- Depends on: video bitrate, user's internet speed, YouTube rate limiting
- Typical: 1-10 MB/s on modern connections

### Resource Usage
- RAM: ~50-200 MB baseline + video download buffering
- CPU: Low (I/O bound)
- Disk: Sufficient space for video files

## Future Enhancements

### Short-term
- Dark mode UI
- Keyboard shortcuts expansion
- Configurable retry count
- Download speed throttling

### Medium-term
- Parallel downloads (multiple simultaneous)
- Video conversion pipeline
- Scheduled downloads
- Channel subscription monitoring

### Long-term
- Web dashboard
- REST API
- Mobile companion app
- Advanced filtering (video length, date, etc.)

## Development Notes

- **Python Version**: 3.8+ (f-strings, type hints)
- **Testing**: Unit tests for core logic (engine, queue, validators)
- **Code Style**: PEP 8 compliant
- **Dependencies**: Minimal external packages (PyQt6, yt-dlp, requests)
- **Maintenance**: yt-dlp updates tracked and integrated regularly

## Contact & Support

- **Issues**: GitHub Issues tracker
- **Documentation**: README.md, AGENTS.md
- **Contributing**: Fork, feature branch, PR workflow
- **License**: MIT

---

*Last updated: 2026-01-29*
