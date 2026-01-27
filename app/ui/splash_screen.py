from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtGui import QPixmap, QColor, QFont, QPainter
from PyQt6.QtCore import Qt, QTimer
import sys


def create_splash_screen():
    """Create a professional splash screen with gradient and text"""
    # Create a pixmap for the splash screen
    pixmap = QPixmap(600, 400)
    pixmap.fill(QColor(255, 255, 255))  # White background

    # Create painter for custom drawing
    painter = QPainter(pixmap)

    # Draw gradient background
    from PyQt6.QtGui import QLinearGradient
    gradient = QLinearGradient(0, 0, 0, pixmap.height())
    gradient.setColorAt(0, QColor(102, 126, 234))      # Purple top
    gradient.setColorAt(1, QColor(118, 75, 162))       # Darker purple bottom
    painter.fillRect(pixmap.rect(), gradient)
    
    # Draw main title
    title_font = QFont()
    title_font.setPointSize(32)
    title_font.setBold(True)
    painter.setFont(title_font)
    painter.setPen(QColor(255, 255, 255))
    painter.drawText(pixmap.rect().adjusted(0, 80, 0, 0), Qt.AlignmentFlag.AlignHCenter, "📥 VidGrab")
    
    # Draw subtitle
    subtitle_font = QFont()
    subtitle_font.setPointSize(12)
    painter.setFont(subtitle_font)
    painter.drawText(pixmap.rect().adjusted(0, 140, 0, 0), Qt.AlignmentFlag.AlignHCenter, "Starting up...")
    
    # Draw features/info
    info_font = QFont()
    info_font.setPointSize(10)
    painter.setFont(info_font)
    painter.setPen(QColor(220, 220, 220))
    painter.drawText(
        pixmap.rect().adjusted(0, 200, 0, -80),
        Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
        "✓ 100% Free & Open Source\n✓ No Ads, No Tracking\n✓ Download Videos & Playlists"
    )
    
    # Draw attribution at bottom
    attribution_font = QFont()
    attribution_font.setPointSize(9)
    painter.setFont(attribution_font)
    painter.setPen(QColor(200, 200, 200))
    painter.drawText(
        pixmap.rect().adjusted(0, 0, 0, -10),
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
        "Built with ❤ by Evans Elabo"
    )
    
    painter.end()
    
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


def hide_splash(splash):
    """Hide splash screen when app is ready with minimum duration"""
    if splash:
        # Keep splash visible for at least 2 seconds
        QTimer.singleShot(10000, lambda: splash.finish(None) if splash else None)
