import yt_dlp
import os
import shutil
import time
import platform
from core.logger import log_info, log_error, log_warning

FFMPEG_BINARY = None
NODE_BINARY = None
_FFMPEG_CHECKED = False
_NODE_CHECKED = False


def _resolve_ffmpeg():
    """Resolve ffmpeg location lazily to avoid hard crashes on import."""
    global FFMPEG_BINARY, _FFMPEG_CHECKED
    if _FFMPEG_CHECKED:
        return FFMPEG_BINARY
    _FFMPEG_CHECKED = True

    # Prefer system PATH for reliability across architectures
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        FFMPEG_BINARY = ffmpeg_path
        log_info(f"FFmpeg found in system PATH: {FFMPEG_BINARY}")
        return FFMPEG_BINARY

    # Optional pyffmpeg (can crash on unsupported archs if imported at module import)
    if os.environ.get("VIDGRAB_DISABLE_PYFFMPEG") == "1":
        log_warning("pyffmpeg disabled via VIDGRAB_DISABLE_PYFFMPEG=1")
        return None

    if os.sys.platform == "darwin":
        machine = platform.machine().lower()
        if machine in ("x86_64", "i386"):
            log_warning("Skipping pyffmpeg on Intel macOS; install ffmpeg via Homebrew")
            return None

    try:
        from pyffmpeg import FFmpeg
        ffmpeg_instance = FFmpeg()
        FFMPEG_BINARY = ffmpeg_instance.get_ffmpeg_bin()
        if FFMPEG_BINARY:
            log_info(f"FFmpeg found via pyffmpeg: {FFMPEG_BINARY}")
        else:
            log_error("pyffmpeg loaded but did not provide an ffmpeg binary")
    except (ImportError, Exception) as e:
        log_warning(f"pyffmpeg unavailable: {e}")

    if not FFMPEG_BINARY:
        log_error("FFmpeg not found - audio/video merging may fail")

    return FFMPEG_BINARY


def _resolve_node():
    """Resolve Node.js path lazily."""
    global NODE_BINARY, _NODE_CHECKED
    if _NODE_CHECKED:
        return NODE_BINARY
    _NODE_CHECKED = True

    node_candidates = [
        shutil.which("node"),  # System PATH
        os.path.expanduser("~/.nvm/versions/node/*/bin/node"),  # NVM pattern
        "/usr/local/bin/node",  # macOS Homebrew (Intel)
        "/opt/homebrew/bin/node",  # macOS Homebrew (Apple Silicon)
        "/usr/bin/node",  # Linux
    ]

    existing_candidates = []
    for candidate in node_candidates:
        if candidate and "*" in candidate:
            import glob
            expanded = glob.glob(candidate)
            if expanded:
                existing_candidates.extend(expanded)
        elif candidate and os.path.exists(candidate):
            existing_candidates.append(candidate)

    for node_path in existing_candidates:
        try:
            result = os.popen(f'"{node_path}" --version').read().strip()
            if result.startswith("v"):
                NODE_BINARY = node_path
                log_info(f"Node.js found: {NODE_BINARY} ({result})")
                break
        except Exception:
            continue

    if not NODE_BINARY:
        log_warning("Node.js not found - YouTube extraction may fail for protected videos")

    return NODE_BINARY

class DownloadEngine:
    def __init__(self, output_dir, hooks=None, quality="best", format="mp4"):
        self.output_dir = output_dir
        self.hooks = hooks or []
        self.quality = quality
        self.format = format

    def _get_format_string(self) -> str:
        """Generate yt-dlp format string based on quality and format"""
        quality_map = {
            "best": "bestvideo+bestaudio/best",
            "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
            "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
            "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]/best",
            "audio-only": "bestaudio/best",
        }
        return quality_map.get(self.quality, "bestvideo+bestaudio/best")

    def download(self, url):
        format_str = self._get_format_string()
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        output_template = os.path.join(
            self.output_dir,
            "%(playlist_index)s - %(title)s.%(ext)s"
        )
        
        log_info(f"Download directory: {self.output_dir}")
        log_info(f"Output template: {output_template}")
        
        # Get file count before download to detect if files were actually created
        files_before = set(os.listdir(self.output_dir)) if os.path.exists(self.output_dir) else set()
        
        log_info(f"Format string: {format_str}")
        log_info(f"Quality: {self.quality}, Merge format: {self.format if self.quality != 'audio-only' else 'm4a'}")
        
        ydl_opts = {
            "outtmpl": output_template,
            "progress_hooks": self.hooks,
            "ignoreerrors": True,  # Allow playlist downloads to continue on individual video failures
            "format": format_str,
            "merge_output_format": self.format if self.quality != "audio-only" else "m4a",
            "postprocessors": [],
            "extract_flat": False,  # Don't extract flat, actually download
            "skip_unavailable_fragments": False,  # Fail on unavailable fragments
            "no_warnings": False,  # Show all warnings for debugging
            "socket_timeout": 30,  # Increase socket timeout
            "retries": 3,  # Retry failed downloads
            "fragment_retries": 5,  # Retry failed fragments more aggressively
            "file_access_retries": 5,  # Retry file access
            "concurrent_fragment_downloads": 8,  # Download fragments in parallel (higher = faster)
            "downloader_args": {"http_chunk_size": 10485760},  # 10MB chunks for faster downloads
        }
        
        ffmpeg_bin = _resolve_ffmpeg()
        node_bin = _resolve_node()

        # Use bundled ffmpeg from pyffmpeg if available
        # This enables automatic merging of video+audio streams
        if ffmpeg_bin:
            ydl_opts["ffmpeg_location"] = ffmpeg_bin
            log_info(f"Using FFmpeg from: {ffmpeg_bin}")
        else:
            log_error("FFmpeg not available - merging may fail")
        
        # Configure Node.js for YouTube extraction
        if node_bin:
            # yt-dlp expects js_runtimes as a dict: {runtime_name: {config_dict}}
            ydl_opts["js_runtimes"] = {
                "node": {}  # Empty config uses default node from PATH
            }
            log_info(f"Using Node.js from: {node_bin}")
        else:
            # If Node.js not found, log warning but continue
            log_warning("Node.js not configured - YouTube extraction may fail for protected videos")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
        
        # Check if download actually succeeded
        # For single videos: info will be the video dict
        # For playlists: info will be a playlist dict with entries
        if not info:
            raise Exception("No video information retrieved")
        
        # Check if this was a playlist
        if 'entries' in info:
            # Playlist case: check if any videos were actually downloaded
            successful_entries = [e for e in info.get('entries', []) if e is not None]
            if not successful_entries:
                raise Exception("No videos were successfully downloaded from the playlist")
            log_info(f"Playlist download: {len(successful_entries)} of {len(info['entries'])} videos downloaded")
        else:
            # Single video: verify that a file was actually created and is complete
            # Give yt-dlp a moment to finalize file operations
            time.sleep(1.0)
            files_after = set(os.listdir(self.output_dir)) if os.path.exists(self.output_dir) else set()
            new_files = files_after - files_before
            
            if not new_files:
                # No new files created = download failed despite yt-dlp not raising an exception
                raise Exception("Download failed: no file was created (possibly HTTP 403 or stream unavailable)")
            
            # Verify that new files are actually the final output (not intermediate format files)
            # yt-dlp creates intermediate files with .f### extension (format ID) during download
            # These should be merged into a final file, so if only .f### files exist = incomplete download
            valid_files = []
            
            for filename in new_files:
                filepath = os.path.join(self.output_dir, filename)
                
                # Skip intermediate format files (e.g., video.f401.mp4, video.f251.m4a)
                # These indicate the download was incomplete and yt-dlp couldn't merge them
                if '.f' in filename and filename.split('.')[-2].lstrip('f').isdigit():
                    try:
                        file_size = os.path.getsize(filepath)
                        log_warning(f"Found incomplete intermediate file {filename} ({file_size} bytes) - download failed mid-process")
                        # Clean up the partial format file
                        try:
                            os.remove(filepath)
                            log_info(f"Removed incomplete format file: {filename}")
                        except Exception as e:
                            log_warning(f"Could not remove format file {filename}: {e}")
                    except OSError as e:
                        log_warning(f"Could not check intermediate file {filename}: {e}")
                else:
                    # This is a final output file (no .f### pattern)
                    try:
                        file_size = os.path.getsize(filepath)
                        # Even final files should have minimum size to be valid
                        if file_size >= 1_000_000:  # 1MB minimum for valid video
                            valid_files.append(filename)
                        else:
                            log_warning(f"Skipping small output file {filename} ({file_size} bytes)")
                            try:
                                os.remove(filepath)
                            except:
                                pass
                    except OSError as e:
                        log_warning(f"Could not check file size for {filename}: {e}")
            
            if not valid_files:
                raise Exception("Download failed: no complete file was created (possibly HTTP 403, connection lost, or stream unavailable)")
            
            log_info(f"Download verified: {len(valid_files)} file(s) created successfully")
        
        return info
