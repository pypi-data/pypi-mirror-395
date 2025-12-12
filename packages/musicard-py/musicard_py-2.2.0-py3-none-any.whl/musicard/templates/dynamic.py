"""
Dynamic theme implementation
"""

from PIL import Image, ImageDraw

from ..utils.fonts import font_manager
from ..utils.images import (
    adjust_brightness,
    blur_image,
    create_gradient,
    load_image,
    resize_image,
)
from ..utils.text import draw_text_with_shadow
from .base_theme import BaseTheme


class DynamicTheme(BaseTheme):
    """Dynamic music card theme with gradient backgrounds."""

    def render(self, image: Image.Image, draw: ImageDraw.ImageDraw, data: dict) -> None:
        # Extract data with defaults
        name = data.get("name", "Musicard")
        author = data.get("author", "By Unburn")
        thumbnail_image = data.get("thumbnailImage")
        background_image = data.get("backgroundImage")
        progress = max(0, min(100, data.get("progress", 0)))
        progress_color = data.get("progressColor", "#FF7A00")
        progress_bar_color = data.get("progressBarColor", "#5F2D00")
        name_color = data.get("nameColor", "#FFFFFF")
        author_color = data.get("authorColor", "#CCCCCC")
        image_darkness = data.get("imageDarkness", 50)

        # Truncate text
        if len(name) > 22:
            name = name[:22] + "..."
        if len(author) > 22:
            author = author[:22] + "..."

        # Background
        if background_image:
            try:
                bg_img = load_image(background_image)
                bg_img = resize_image(
                    bg_img, (image.width, image.height), maintain_aspect=False
                )
                # Apply darkness
                darkness_factor = (100 - image_darkness) / 100
                bg_img = adjust_brightness(bg_img, darkness_factor)
                # Blur for better text readability + background blur level
                blur_level = 3 + data.get("backgroundBlurLevel", 0.0) * 10
                bg_img = blur_image(bg_img, blur_level)
                image.paste(bg_img, (0, 0))
            except Exception:
                # Fallback to gradient
                gradient = create_gradient(
                    (image.width, image.height), (26, 26, 26), (10, 10, 10)
                )
                image.paste(gradient, (0, 0))
        else:
            # Default gradient background
            gradient = create_gradient(
                (image.width, image.height), (26, 26, 26), (10, 10, 10)
            )
            image.paste(gradient, (0, 0))

        # Thumbnail
        if thumbnail_image:
            try:
                thumb = load_image(thumbnail_image)
                thumb = resize_image(thumb, (320, 320))
                image.paste(thumb, (image.width - 350, 30))
            except Exception:
                pass

        # Progress bar
        bar_width = 800
        bar_height = 20
        bar_x = 50
        bar_y = image.height - 80

        # Background bar
        draw.rectangle(
            [bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
            fill=progress_bar_color,
        )

        # Progress fill
        progress_width = int(bar_width * progress / 100)
        draw.rectangle(
            [bar_x, bar_y, bar_x + progress_width, bar_y + bar_height],
            fill=progress_color,
        )

        # Title
        title_font = font_manager.load_font("bold", 75)
        draw_text_with_shadow(draw, name, title_font, name_color, "#000000", (50, 120))

        # Author
        author_font = font_manager.load_font("medium", 55)
        draw_text_with_shadow(
            draw, author, author_font, author_color, "#000000", (50, 220)
        )

        # Render logo
        self.render_logo(image, data)
