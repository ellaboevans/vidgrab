"""Theme and color management for VidGrab"""

from pathlib import Path


class Colors:
    """Color constants for the application"""
    # Dark theme
    BG_PRIMARY = "#0f1419"      # Main background
    BG_SECONDARY = "#1a1f28"    # Secondary background (input fields, lists)
    BG_TERTIARY = "#252d38"     # Tertiary (hover states)
    
    TEXT_PRIMARY = "#e8eaed"    # Main text
    TEXT_SECONDARY = "#a0aec0"  # Secondary text
    TEXT_MUTED = "#718096"      # Muted text
    
    BORDER = "#2d3748"          # Border color
    BORDER_HOVER = "#4a5568"    # Border hover
    
    ACCENT = "#00d9ff"          # Primary accent (cyan)
    SUCCESS = "#34d399"         # Success (green)
    ERROR = "#f87171"           # Error (red)
    WARNING = "#fbbf24"         # Warning (yellow)
    
    # Status colors for download items
    STATUS_WAITING = "#a0aec0"
    STATUS_DOWNLOADING = "#00d9ff"
    STATUS_COMPLETED = "#34d399"
    STATUS_FAILED = "#f87171"
    STATUS_CANCELLED = "#718096"


def load_stylesheet():
    """Load the QSS stylesheet file"""
    stylesheet_path = Path(__file__).parent / "styles.qss"
    if stylesheet_path.exists():
        with open(stylesheet_path, "r") as f:
            return f.read()
    return ""
