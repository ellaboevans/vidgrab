import json
import os
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class Settings:
    """Application settings with defaults"""
    download_folder: str = str(Path.home() / "Downloads")
    video_quality: str = "best"  # best, 1080p, 720p, 480p, audio-only
    format: str = "mp4"  # mp4, mkv, webm
    auto_start: bool = False  # Auto-start downloads on queue add
    dark_mode: bool = False
    
    QUALITY_OPTIONS = ["best", "1080p", "720p", "480p", "audio-only"]
    FORMAT_OPTIONS = ["mp4", "mkv", "webm"]


class SettingsManager:
    """Manage app settings with file persistence"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".youtube-downloader"
        self.config_file = self.config_dir / "config.json"
        self.settings = self._load_settings()
    
    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_settings(self) -> Settings:
        """Load settings from file or create defaults"""
        self._ensure_config_dir()
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    return Settings(**data)
            except Exception as e:
                print(f"Error loading settings: {e}. Using defaults.")
        
        return Settings()
    
    def save(self, settings: Settings) -> bool:
        """Save settings to file"""
        try:
            self._ensure_config_dir()
            with open(self.config_file, 'w') as f:
                json.dump(asdict(settings), f, indent=2)
            self.settings = settings
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self) -> Settings:
        """Get current settings"""
        return self.settings
    
    def update(self, **kwargs) -> bool:
        """Update specific settings and save"""
        settings_dict = asdict(self.settings)
        settings_dict.update(kwargs)
        new_settings = Settings(**settings_dict)
        return self.save(new_settings)
