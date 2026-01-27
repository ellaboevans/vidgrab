import yt_dlp
import os
from core.logger import log_info, log_error

try:
    from pyffmpeg import FFmpeg
    ffmpeg_instance = FFmpeg()
    FFMPEG_BINARY = ffmpeg_instance.get_ffmpeg_bin()
    log_info(f"FFmpeg binary located at: {FFMPEG_BINARY}")
except (ImportError, Exception) as e:
    FFMPEG_BINARY = None
    log_error(f"Failed to locate FFmpeg: {e}")

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
        
        ydl_opts = {
            "outtmpl": output_template,
            "progress_hooks": self.hooks,
            "ignoreerrors": True,
            "format": format_str,
            "merge_output_format": self.format if self.quality != "audio-only" else "m4a",
            "postprocessors": [],
        }
        
        # Use bundled ffmpeg from pyffmpeg if available
        # This enables automatic merging of video+audio streams
        if FFMPEG_BINARY:
            ydl_opts["ffmpeg_location"] = FFMPEG_BINARY
            log_info(f"Using FFmpeg from: {FFMPEG_BINARY}")
        else:
            log_error("FFmpeg not available - merging may fail")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=True)
