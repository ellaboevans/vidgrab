import re
from urllib.parse import urlparse


class URLValidator:
    """Validate YouTube URLs"""
    
    # YouTube URL patterns
    YOUTUBE_PATTERNS = [
        r'(?:https?:)?//(?:www\.)?youtube\.com/watch\?v=[\w-]+',  # Standard video
        r'(?:https?:)?//youtu\.be/[\w-]+',  # Short URL
        r'(?:https?:)?//(?:www\.)?youtube\.com/playlist\?list=[\w-]+',  # Playlist
        r'(?:https?:)?//(?:www\.)?youtube\.com/channel/[\w-]+',  # Channel
        r'(?:https?:)?//(?:www\.)?youtube\.com/@[\w-]+',  # Handle
    ]

    TYPE_PATTERNS = {
        "video": [
            r'(?:https?:)?//(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(?:https?:)?//youtu\.be/[\w-]+',
        ],
        "playlist": [
            r'(?:https?:)?//(?:www\.)?youtube\.com/playlist\?list=[\w-]+',
            r'(?:https?:)?//(?:www\.)?youtube\.com/watch\?v=[\w-]+&list=[\w-]+',
        ],
        "channel": [
            r'(?:https?:)?//(?:www\.)?youtube\.com/channel/[\w-]+',
            r'(?:https?:)?//(?:www\.)?youtube\.com/@[\w-]+',
        ],
    }
    
    @staticmethod
    def is_valid_youtube_url(url: str) -> tuple[bool, str]:
        """
        Validate if URL is a YouTube URL
        Returns: (is_valid, error_message)
        """
        url = url.strip()
        
        if not url:
            return False, "URL cannot be empty"
        
        # Check if it looks like a URL at all
        if not any(protocol in url.lower() for protocol in ['http://', 'https://', 'youtu.be', 'youtube.com']):
            return False, "Invalid URL. Please paste a valid YouTube link (e.g., https://www.youtube.com/watch?v=...)"
        
        # Check against YouTube patterns
        for pattern in URLValidator.YOUTUBE_PATTERNS:
            if re.search(pattern, url, re.IGNORECASE):
                return True, ""
        
        # If it contains youtube.com or youtu.be, it might be a different type
        if 'youtube.com' in url.lower() or 'youtu.be' in url.lower():
            return True, ""  # Let yt-dlp handle it, as it supports many formats
        
        return False, "URL doesn't appear to be a valid YouTube link. Supported: videos, playlists, channels, handles"
    
    @staticmethod
    def is_duplicate(url: str, queue_items: list) -> tuple[bool, str]:
        """
        Check if URL already exists in queue
        Returns: (is_duplicate, item_title)
        """
        url = url.strip().lower()
        for item in queue_items:
            if item.url.strip().lower() == url:
                return True, item.title
        return False, ""

    @staticmethod
    def matches_type(url: str, download_type: str) -> tuple[bool, str]:
        """
        Validate if URL matches the selected download type.
        Returns: (is_match, error_message)
        """
        normalized_type = (download_type or "auto").lower()
        if normalized_type == "auto":
            return True, ""

        patterns = URLValidator.TYPE_PATTERNS.get(normalized_type, [])
        for pattern in patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True, ""

        if normalized_type == "video" and "list=" in url.lower():
            return False, "This looks like a playlist link. Choose Playlist or Auto."
        if normalized_type == "playlist":
            return False, "Please paste a playlist link (looks like ...playlist?list=...)."
        if normalized_type == "channel":
            return False, "Please paste a channel link (channel/...) or handle link (@...)."

        return False, "URL doesn't match the selected download type."
