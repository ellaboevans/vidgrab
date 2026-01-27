# YouTube Downloader

A fast, user-friendly desktop application to download YouTube videos and playlists with a clean PyQt6 interface.

## Features

✨ **Easy to Use**
- Paste YouTube URLs (videos, playlists, channels, handles)
- Clean, intuitive interface
- Real-time progress tracking

📦 **Batch Downloading**
- Queue multiple URLs at once
- Download entire playlists
- Saved queue persists between sessions

⚙️ **Customizable**
- Choose video quality (best, 1080p, 720p, 480p, audio-only)
- Select output format (MP4, MKV, WebM)
- Set default download folder

🛡️ **Reliable**
- Automatic retry on failures (up to 3 times)
- Thread-safe multi-threaded downloads
- Detailed error messages
- View application logs for debugging

⏸️ **Control**
- Pause/stop downloads at any time
- Cancel individual items in queue
- Clear completed items

## Installation

### Option 1: Standalone Executable (Easiest)

Visit the **[Official Download Page](https://yourusername.github.io/vidgrab/)** to download the latest version for your operating system.

The page automatically detects your OS and offers the right download button. Or manually download:

- **macOS**: `VidGrab.dmg` (drag to Applications)
- **Windows**: `VidGrab.exe` (double-click to run)
- **Linux**: `VidGrab` (make executable and run)

No installation needed, just download and run!

### Option 2: From Source

If you prefer to run from source or want to modify the code:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vidgrab.git
cd vidgrab
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
python -m main
```

### Building Your Own Executable

Want to build an executable yourself? See [BUILDING.md](BUILDING.md) for detailed instructions on building for macOS, Windows, and Linux.

## Usage

### Adding Downloads

1. **Paste a URL** in the input field (e.g., `https://www.youtube.com/watch?v=...`)
2. **Click "Add to Queue"** - the app fetches the video title automatically
3. **Repeat** to add multiple videos/playlists

### Configuring Settings

Click **Settings** to customize:
- **Download Folder**: Where videos are saved (default: ~/Downloads)
- **Video Quality**: best, 1080p, 720p, 480p, or audio-only
- **Format**: MP4, MKV, or WebM

### Starting Downloads

1. **Choose a download folder** (if not using default)
2. **Click "Start Downloads"** to begin processing the queue
3. **Watch progress** in real-time on each item and overall

### Stopping Downloads

- **Click "Stop"** to pause the queue and cancel current download
- **Resume** by clicking "Start Downloads" again

### Viewing Logs

Click **View Logs** to open the application log file. Useful for:
- Troubleshooting failed downloads
- Checking detailed error messages
- Understanding what happened during a download session

## Supported URL Types

✅ Single videos
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/dQw4w9WgXcQ
```

✅ Playlists
```
https://www.youtube.com/playlist?list=PLxxx
```

✅ Channels
```
https://www.youtube.com/channel/UCxxx
```

✅ Handles (custom URLs)
```
https://www.youtube.com/@username
```

## File Locations

- **Downloads**: Saved to your configured download folder (default: ~/Downloads)
- **Settings**: `~/.vidgrab/config.json`
- **Queue**: `~/.vidgrab/queue.json` (auto-saved)
- **Logs**: `~/.vidgrab/logs/app.log`

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+A | Add to Queue (when input focused) |
| Ctrl+Q | Quit application |

*More shortcuts coming soon*

## Troubleshooting

### "Download Failed" Error

1. Check the error message in the dialog
2. Click **View Logs** for more details
3. Verify the URL is still valid (video might be deleted/private)
4. The app will automatically retry up to 3 times

### App Freezes During Download

- This is normal for large files
- The app is downloading in the background
- If frozen for >2 minutes, try clicking **Stop** then **Start Downloads** again

### Settings Not Saving

- Ensure you clicked **Save** in the Settings dialog
- Check `~/.vidgrab/config.json` file exists
- Restart the app and try again

### Log File Not Found

- Logs are created after the first download
- Click **View Logs** only after attempting a download
- Check `~/.vidgrab/logs/` directory

## Performance Tips

- **Quality Selection**: Lower quality downloads faster (720p instead of best)
- **Audio-Only**: Much faster if you just want the audio
- **Batch Downloads**: Queue multiple items to download continuously

## Limitations

- **Age-restricted videos** may not download without authentication
- **Private videos** cannot be downloaded (as expected)
- **Very large playlists** (1000+ videos) may take time to process
- **Network-dependent**: Slow internet = slower downloads

## Privacy

- **No data collection** - all processing is local
- **No account tracking** - works completely offline after yt-dlp update
- **No advertisements** - open-source and free

## Reporting Issues

Found a bug? Help us improve:

1. **Check the logs** - Click "View Logs" to see error details
2. **Collect info** - Note the exact URL, settings, and error message
3. **Report** - Open an issue on GitHub with:
   - What you were trying to do
   - The error message
   - Your OS and Python version
   - Log file contents (optional but helpful)

## Contributing

We welcome contributions! Whether bug fixes, features, or documentation:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Credits

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Roadmap

- [x] Basic download functionality
- [x] Queue management
- [x] Settings customization
- [x] Error handling & retry
- [x] Queue persistence
- [ ] Dark mode
- [ ] Parallel downloads (multiple simultaneous)
- [ ] Video conversion tools
- [ ] Scheduled downloads
- [ ] YouTube channel subscriptions

## Support

Need help? Check:
- **FAQ**: Common questions and answers (coming soon)
- **Logs**: Application logs for error details
- **GitHub Issues**: Search existing issues or create a new one

---

Made with ❤️ for the YouTube download community
