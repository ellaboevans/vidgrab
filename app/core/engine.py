import yt_dlp
import os

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
        
        ydl_opts = {
            "outtmpl": os.path.join(
                self.output_dir,
                "%(playlist_index)s - %(title)s.%(ext)s"
            ),
            "progress_hooks": self.hooks,
            "ignoreerrors": True,
            "format": format_str,
            "merge_output_format": self.format if self.quality != "audio-only" else "m4a",
            "postprocessors": [],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=True)
