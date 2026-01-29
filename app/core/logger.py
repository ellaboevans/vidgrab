import logging
import logging.handlers
from pathlib import Path


class _LoggerSingleton(logging.Logger):
    """Singleton logger that ensures only one instance is created"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if self._initialized:
            return
        
        _LoggerSingleton._initialized = True
        
        super().__init__("VidGrab")
        self.setLevel(logging.DEBUG)
        
        # Setup log directory
        self.log_dir = Path.home() / ".vidgrab" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # File handler - rotating file handler
        log_file = self.log_dir / "app.log"
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
        
        # Add handlers only if not already present
        if not self.handlers:
            self.addHandler(file_handler)
            self.addHandler(console_handler)
    
    def get_log_file(self):
        """Get the current log file path"""
        return self.log_dir / "app.log"


# Global logger instance
_logger = _LoggerSingleton()


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
