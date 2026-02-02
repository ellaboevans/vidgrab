"""Desktop notification utilities for VidGrab"""

import sys
import subprocess
from core.logger import log_info, log_error


def show_notification(title: str, message: str, sound: bool = True):
    """
    Show a native desktop notification.
    Works on macOS, Windows, and Linux.
    
    Args:
        title: Notification title
        message: Notification message
        sound: Whether to play notification sound
    """
    try:
        if sys.platform == "darwin":  # macOS
            _notify_macos(title, message, sound)
        elif sys.platform == "win32":  # Windows
            _notify_windows(title, message)
        elif sys.platform == "linux":  # Linux
            _notify_linux(title, message)
    except Exception as e:
        log_error(f"Failed to show notification: {str(e)}", exc_info=True)


def _notify_macos(title: str, message: str, sound: bool = True):
    """Show macOS notification using osascript"""
    try:
        sound_flag = "with sound" if sound else "without sound"
        script = f'display notification "{message}" with title "{title}" {sound_flag}'
        subprocess.run(["osascript", "-e", script], check=False)
        log_info(f"Notification sent (macOS): {title}")
    except Exception as e:
        log_error(f"macOS notification failed: {str(e)}", exc_info=True)


def _notify_windows(title: str, message: str):
    """Show Windows notification using Windows 10+ toast"""
    try:
        from win10toast import ToastNotifier
        toast = ToastNotifier()
        toast.show_toast(title, message, duration=5)
        log_info(f"Notification sent (Windows): {title}")
    except ImportError:
        # Fallback: use Windows API if win10toast not available
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, message, title, 1)
            log_info(f"Notification sent (Windows fallback): {title}")
        except Exception as e:
            log_error(f"Windows notification failed: {str(e)}", exc_info=True)
    except Exception as e:
        log_error(f"Windows notification failed: {str(e)}", exc_info=True)


def _notify_linux(title: str, message: str):
    """Show Linux notification using notify-send"""
    try:
        subprocess.run(["notify-send", title, message], check=False)
        log_info(f"Notification sent (Linux): {title}")
    except FileNotFoundError:
        log_error("notify-send not found. Install libnotify-bin for desktop notifications")
    except Exception as e:
        log_error(f"Linux notification failed: {str(e)}", exc_info=True)
