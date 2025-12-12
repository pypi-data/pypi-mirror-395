"""
Mini theme implementation
"""

from PIL import Image, ImageDraw

from ..utils.fonts import font_manager
from ..utils.images import load_image, resize_image
from ..utils.text import draw_text_with_shadow
from .base_theme import BaseTheme


class MiniTheme(BaseTheme):
    """Mini music card theme for compact displays."""

    def render(self, image: Image.Image, draw: ImageDraw.ImageDraw, data: dict) -> None:
        # Extract data with defaults
        name = data.get("name", "Musicard")
        author = data.get("author", "By Unburn")
        thumbnail_image = data.get("thumbnailImage")
        progress = max(0, min(100, data.get("progress", 0)))
        progress_color = data.get("progressColor", "#FF7A00")
        progress_bar_color = data.get("progressBarColor", "#333333")
        menu_color = data.get("menuColor", "#FF7A00")
        background_color = data.get("backgroundColor", "#070707")
        paused = data.get("paused", False)

        # Truncate text
        if len(name) > 15:
            name = name[:15] + "..."
        if len(author) > 15:
            author = author[:15] + "..."

        # Background
        draw.rectangle([(0, 0), (image.width, image.height)], fill=background_color)

        # Thumbnail on left
        if thumbnail_image:
            try:
                thumb = load_image(thumbnail_image)
                thumb = resize_image(thumb, (100, 100))
                image.paste(thumb, (10, 10))
            except Exception:
                pass

        # Menu bar
        draw.rounded_rectangle([120, 10, 130, 110], radius=5, fill=menu_color)

        # Progress bar at bottom
        bar_width = image.width - 140
        bar_height = 10
        bar_x = 140
        bar_y = image.height - 20
        draw.rectangle(
            [bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
            fill=progress_bar_color,
        )
        progress_width = int(bar_width * progress / 100)
        draw.rectangle(
            [bar_x, bar_y, bar_x + progress_width, bar_y + bar_height],
            fill=progress_color,
        )

        # Title and artist
        title_font = font_manager.load_font("bold", 24)
        draw_text_with_shadow(draw, name, title_font, "#FFFFFF", "#000000", (140, 20))

        author_font = font_manager.load_font("regular", 18)
        draw_text_with_shadow(
            draw, author, author_font, "#CCCCCC", "#000000", (140, 50)
        )

        # Paused indicator
        if paused:
            draw.text((140, 80), "⏸️", font=title_font, fill="#FFFFFF")

        # Render logo
        self.render_logo(image, data)
