from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtGui import QPixmap, QColor, QFont, QPainter
from PyQt6.QtCore import Qt, QTimer
import sys


def create_splash_screen():
    """Create a professional splash screen using a pre-designed image"""
    from pathlib import Path
    
    # Load the professional splash screen image
    splash_image_path = Path(__file__).parent / "splash_background.png"
    
    if splash_image_path.exists():
        # Use the professional image (600x400, minimal and modern)
        pixmap = QPixmap(str(splash_image_path))
    else:
        # Fallback to solid color if image not found
        pixmap = QPixmap(600, 400)
        pixmap.fill(QColor(15, 20, 25))  # Dark background
    
    # Create splash screen
    splash = QSplashScreen(pixmap)
    splash.setWindowTitle("VidGrab")
    
    return splash


def show_splash(app):
    """Show splash screen during app startup"""
    splash = create_splash_screen()
    splash.show()
    app.processEvents()
    return splash


def hide_splash(splash, window=None, delay_ms=1000):
    """Hide splash screen after delay and show main window
    
    Args:
        splash: The splash screen widget
        window: Main window to show after splash hides
        delay_ms: Milliseconds to keep splash visible (default 1000ms - faster for minimal design)
    """
    if splash:
        def finish_splash():
            splash.finish(window)
            if window:
                window.show()
        
        QTimer.singleShot(delay_ms, finish_splash)
