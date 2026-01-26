import yt_dlp
import os

class DownloadEngine:
    def __init__(self, output_dir, hooks=None):
        self.output_dir = output_dir
        self.hooks = hooks or []

    def download(self, url):
        ydl_opts = {
            "outtmpl": os.path.join(
                self.output_dir,
                "%(playlist_index)s - %(title)s.%(ext)s"
            ),
            "progress_hooks": self.hooks,
            "ignoreerrors": True,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=True)
