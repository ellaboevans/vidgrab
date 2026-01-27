import logging
import logging.handlers
from pathlib import Path
from datetime import datetime


class AppLogger:
    """Application logger with file and console output"""
    
    def __init__(self, name="VidGrab"):
        self.log_dir = Path.home() / ".vidgrab" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove any existing handlers to avoid duplicates
        self.logger.handlers = []
        
        # File handler - rotated daily
        log_file = self.log_dir / f"app.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=5*1024*1024,  # 5MB per file
            backupCount=5  # Keep 5 old files
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        return self.logger
    
    def get_log_file(self):
        """Get the current log file path"""
        return self.log_dir / "app.log"


# Global logger instance
_logger = AppLogger().get_logger()


def get_logger():
    """Get the global logger instance"""
    return _logger


def log_debug(msg, *args):
    _logger.debug(msg, *args)


def log_info(msg, *args):
    _logger.info(msg, *args)


def log_warning(msg, *args):
    _logger.warning(msg, *args)


def log_error(msg, *args, exc_info=False):
    _logger.error(msg, *args, exc_info=exc_info)


def log_critical(msg, *args):
    _logger.critical(msg, *args)
