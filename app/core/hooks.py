def _format_size(bytes_val):
    """Format bytes to human-readable size"""
    if bytes_val is None:
        return "?"
    for unit in ["B", "KiB", "MiB", "GiB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.1f}{unit}" if unit != "B" else f"{int(bytes_val)}{unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f}TiB"

def _format_speed(bytes_per_sec):
    """Format speed in bytes/sec to human-readable format"""
    if bytes_per_sec is None:
        return "?"
    return _format_size(bytes_per_sec) + "/s"

def _format_eta(seconds):
    """Format ETA in seconds to HH:MM:SS"""
    if seconds is None or seconds < 0:
        return "?"
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def progress_hook_factory(on_progress, on_done):
    last_percent = -1  # Track last emitted percent to avoid duplicate signals
    
    def hook(d):
        nonlocal last_percent
        
        info = d.get("info_dict") or {}
        playlist_index = d.get("playlist_index") or info.get("playlist_index")
        playlist_count = (
            d.get("playlist_count")
            or d.get("n_entries")
            or info.get("playlist_count")
            or info.get("n_entries")
        )
        playlist_suffix = ""
        if playlist_index and playlist_count:
            playlist_suffix = f" • Item {playlist_index}/{playlist_count}"

        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            speed = d.get("speed")
            eta = d.get("eta")
            
            if total:
                percent = int(downloaded / total * 100)
                # Only emit if percent changed to reduce signal spam
                if percent != last_percent:
                    # Build detailed info string
                    size_str = f"{_format_size(downloaded)} of {_format_size(total)}"
                    speed_str = _format_speed(speed)
                    eta_str = _format_eta(eta)
                    detail = f"{size_str} at {speed_str} ETA {eta_str}{playlist_suffix}"
                    on_progress(percent, detail)
                    last_percent = percent
            else:
                # If we don't have total yet but are downloading, emit 0% once
                if last_percent == -1:
                    on_progress(0, f"Starting download...{playlist_suffix}")
                    last_percent = 0

        elif d["status"] == "finished":
            # Ensure we emit 100% when finished
            if last_percent != 100:
                on_progress(100, f"Complete{playlist_suffix}")
            on_done(d.get("filename"))

    return hook
