"""
Classic Pro theme implementation
"""

from PIL import Image, ImageDraw

from ..utils.fonts import font_manager
from ..utils.images import (
    apply_mask,
    create_rounded_mask,
    draw_rounded_rectangle,
    load_image,
    resize_image,
)
from ..utils.text import draw_text_with_shadow
from .base_theme import BaseTheme


class ClassicProTheme(BaseTheme):
    """Classic Pro music card theme with enhanced features."""

    def render(self, image: Image.Image, draw: ImageDraw.ImageDraw, data: dict) -> None:
        # Extract data with defaults
        name = data.get("name", "Musicard")
        author = data.get("author", "By Unburn")
        thumbnail_image = data.get("thumbnailImage")
        progress = max(0, min(100, data.get("progress", 0)))
        progress_color = data.get("progressColor", "#FF7A00")
        progress_bar_color = data.get("progressBarColor", "#5F2D00")
        background_color = data.get("backgroundColor", "#070707")
        name_color = data.get("nameColor", "#FF7A00")
        author_color = data.get("authorColor", "#FFFFFF")
        start_time = data.get("startTime", "0:00")
        end_time = data.get("endTime", "4:00")
        time_color = data.get("timeColor", "#FF7A00")

        # Truncate text if too long
        if len(name) > 20:
            name = name[:20] + "..."
        if len(author) > 20:
            author = author[:20] + "..."

        # Background
        draw.rectangle([(0, 0), (image.width, image.height)], fill=background_color)

        # Thumbnail with rounded corners
        if thumbnail_image:
            try:
                thumb = load_image(thumbnail_image)
                thumb = resize_image(thumb, (350, 350))
                # Create rounded mask
                mask = create_rounded_mask((350, 350), 20)
                thumb = apply_mask(thumb, mask)
                image.paste(thumb, (image.width - 400, 25), thumb)
            except Exception:
                pass  # Use default if loading fails

        # Progress bar with enhanced styling
        bar_width = 750
        bar_height = 25
        bar_x = 50
        bar_y = image.height - 90

        # Background bar with rounded corners
        draw_rounded_rectangle(
            draw,
            (bar_x, bar_y, bar_x + bar_width, bar_y + bar_height),
            radius=12,
            fill=progress_bar_color,
        )

        # Progress fill
        progress_width = int(bar_width * progress / 100)
        if progress_width > 0:
            draw_rounded_rectangle(
                draw,
                (bar_x, bar_y, bar_x + progress_width, bar_y + bar_height),
                radius=12,
                fill=progress_color,
            )

        # Progress circle with glow effect
        if progress > 0:
            circle_x = bar_x + progress_width - 17
            circle_y = bar_y - 12
            # Glow effect
            for i in range(3):
                draw.ellipse(
                    [circle_x - i, circle_y - i, circle_x + 34 + i, circle_y + 34 + i],
                    fill=None,
                    outline=progress_color,
                    width=1,
                )
            draw.ellipse(
                [circle_x, circle_y, circle_x + 34, circle_y + 34],
                fill=progress_color,
                outline=background_color,
                width=4,
            )

        # Time display with better positioning
        time_font = font_manager.load_font("medium", 22)
        draw.text((bar_x, bar_y - 35), start_time, font=time_font, fill=time_color)
        draw.text(
            (bar_x + bar_width - 50, bar_y - 35),
            end_time,
            font=time_font,
            fill=time_color,
        )

        # Title with enhanced shadow
        title_font = font_manager.load_font("extra_bold", 85)
        draw_text_with_shadow(
            draw, name, title_font, name_color, "#000000", (50, 100), (3, 3)
        )

        # Author with enhanced shadow
        author_font = font_manager.load_font("regular", 65)
        draw_text_with_shadow(
            draw, author, author_font, author_color, "#000000", (50, 210), (2, 2)
        )

        # Render logo
        self.render_logo(image, data)
