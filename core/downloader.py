import yt_dlp
import sys
import os
import json

def progress_hook(d):
    """YT-DLP progress hook for sending JSON updates."""
    if d['status'] == 'downloading':
        print(json.dumps({
            'type': 'progress',
            'downloaded': d.get('downloaded_bytes', 0),
            'total': d.get('total_bytes') or d.get('total_bytes_estimate'),
            'speed': d.get('speed'),
            'eta': d.get('eta'),
        }), flush=True)

    elif d['status'] == 'finished':
        # This triggers after merging formats
        print(json.dumps({'type': 'finished', 'filename': d['filename']}), flush=True)

def main():
    if len(sys.argv) < 3:
        print(json.dumps({'type': 'error', 'message': 'Usage: downloader.py <url> <output_path>'}), flush=True)
        sys.exit(1)

    url = sys.argv[1]
    output_path = sys.argv[2]

    # Ensure output folder exists
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'quiet': True,           # suppress normal logs
        'no_warnings': True,     # suppress warnings
        'merge_output_format': 'mp4',
        'overwrites': False,     # prevent overwriting existing files
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(result)
            if os.path.exists(filename):
                print(json.dumps({'type': 'done', 'filename': filename, 'message': 'Download complete or already exists'}), flush=True)
        except yt_dlp.utils.DownloadError as e:
            print(json.dumps({'type': 'error', 'message': str(e)}), flush=True)
            sys.exit(1)

if __name__ == "__main__":
    main()
