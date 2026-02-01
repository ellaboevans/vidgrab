"""
Generate a professional splash screen image for VidGrab.
Minimal, modern aesthetic with careful typography and elegant motion indicators.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math

def create_modern_splash():
    """Create a minimal, modern splash screen (600x400)"""
    
    # Dimensions
    width, height = 600, 400
    
    # Create image with dark gradient background
    img = Image.new('RGB', (width, height), color='#0f1419')
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Create subtle gradient background (dark gray to slightly lighter)
    for y in range(height):
        # Subtle gradient: top is darker, bottom is slightly lighter
        ratio = y / height
        r = int(15 + (25 - 15) * ratio)
        g = int(20 + (35 - 20) * ratio)
        b = int(25 + (50 - 25) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add subtle top accent bar (cyan accent)
    accent_height = 4
    for y in range(accent_height):
        draw.line([(0, y), (width, y)], fill=(0, 217, 255, 255 - int(255 * y / accent_height)))
    
    # Draw title "VidGrab"
    # Using a clean, modern approach with shadow effect
    title_text = "VidGrab"
    subtitle_text = "YouTube Downloader"
    status_text = "Initializing..."
    builder_text = "Built by Evans Elabo"
    
    # Create text with PIL (we'll use default fonts, but make them large and clean)
    try:
        # Try to load a nice font, fallback to default
        title_font = ImageFont.truetype("/System/Library/Fonts/SF-Pro-Display-Semibold.otf", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/SF-Pro-Text-Regular.otf", 18)
        status_font = ImageFont.truetype("/System/Library/Fonts/SF-Pro-Text-Regular.otf", 14)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        status_font = ImageFont.load_default()
    
    # Title position (centered horizontally, upper-middle vertically)
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = 80
    
    # Draw title with subtle shadow
    shadow_offset = 2
    draw.text(
        (title_x + shadow_offset, title_y + shadow_offset),
        title_text,
        font=title_font,
        fill=(0, 0, 0, 40)
    )
    # Draw title in cyan/white
    draw.text(
        (title_x, title_y),
        title_text,
        font=title_font,
        fill=(232, 234, 237, 255)  # Light white
    )
    
    # Subtitle position
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 80
    
    draw.text(
        (subtitle_x, subtitle_y),
        subtitle_text,
        font=subtitle_font,
        fill=(160, 174, 192, 255)  # Muted gray-blue
    )
    
    # Draw animated progress indicator (3 dots)
    dot_y = 240
    dot_radius = 5
    dot_spacing = 20
    dot_x_start = (width - (dot_spacing * 2 + dot_radius * 2)) // 2
    
    # Three circles representing progress
    for i in range(3):
        dot_x = dot_x_start + (i * dot_spacing)
        # Vary opacity for animation effect (static image, but suggesting motion)
        opacity = 255 if i == 0 else (180 if i == 1 else 120)
        draw.ellipse(
            [(dot_x - dot_radius, dot_y - dot_radius), 
             (dot_x + dot_radius, dot_y + dot_radius)],
            fill=(0, 217, 255, opacity)  # Cyan accent
        )
    
    # Status text
    status_bbox = draw.textbbox((0, 0), status_text, font=status_font)
    status_width = status_bbox[2] - status_bbox[0]
    status_x = (width - status_width) // 2
    status_y = height - 90
    
    draw.text(
        (status_x, status_y),
        status_text,
        font=status_font,
        fill=(113, 128, 150, 255)  # Darker muted gray
    )
    
    # Builder attribution text (very subtle)
    builder_font_size = 10
    try:
        builder_font = ImageFont.truetype("/System/Library/Fonts/SF-Pro-Text-Regular.otf", builder_font_size)
    except:
        builder_font = status_font
    
    builder_bbox = draw.textbbox((0, 0), builder_text, font=builder_font)
    builder_width = builder_bbox[2] - builder_bbox[0]
    builder_x = (width - builder_width) // 2
    builder_y = height - 30
    
    draw.text(
        (builder_x, builder_y),
        builder_text,
        font=builder_font,
        fill=(113, 128, 150, 200)  # Very subtle gray
    )
    
    # Add subtle accent line below title
    line_y = title_y + 110
    line_width = 60
    line_x_start = (width - line_width) // 2
    line_x_end = line_x_start + line_width
    
    draw.line(
        [(line_x_start, line_y), (line_x_end, line_y)],
        fill=(0, 217, 255, 200),  # Cyan accent
        width=3
    )
    
    # Save the splash screen
    splash_path = Path(__file__).parent / "splash_background.png"
    img.save(str(splash_path), 'PNG')
    print(f"✅ Splash screen created: {splash_path}")
    print(f"   Size: {width}x{height}")

if __name__ == "__main__":
    create_modern_splash()
