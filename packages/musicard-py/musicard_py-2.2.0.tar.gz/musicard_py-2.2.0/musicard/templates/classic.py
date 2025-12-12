"""
Classic theme implementation
"""

from PIL import Image, ImageDraw

from ..utils.fonts import FontManager
from ..utils.images import draw_rounded_rectangle, load_image, resize_image
from ..utils.text import draw_text_with_shadow
from .base_theme import BaseTheme

font_manager = FontManager()


class ClassicTheme(BaseTheme):
    """Classic music card theme."""

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
        if len(name) > 18:
            name = name[:18] + "..."
        if len(author) > 18:
            author = author[:18] + "..."

        # Background
        draw.rectangle([(0, 0), (image.width, image.height)], fill=background_color)

        # Thumbnail
        if thumbnail_image:
            try:
                thumb = load_image(thumbnail_image)
                thumb = resize_image(thumb, (320, 320))
                image.paste(thumb, (image.width - 350, 20))
            except Exception:
                pass  # Use default if loading fails

        # Progress bar
        bar_width = 800
        bar_height = 20
        bar_x = 50
        bar_y = image.height - 80

        # Background bar
        draw_rounded_rectangle(
            draw,
            (bar_x, bar_y, bar_x + bar_width, bar_y + bar_height),
            radius=10,
            fill=progress_bar_color,
        )

        # Progress fill
        progress_width = int(bar_width * progress / 100)
        if progress_width > 0:
            draw_rounded_rectangle(
                draw,
                (bar_x, bar_y, bar_x + progress_width, bar_y + bar_height),
                radius=10,
                fill=progress_color,
            )

        # Progress circle
        if progress > 0:
            circle_x = bar_x + progress_width - 15
            circle_y = bar_y - 10
            draw.ellipse(
                [circle_x, circle_y, circle_x + 30, circle_y + 30],
                fill=progress_color,
                outline=background_color,
                width=3,
            )

        # Time display
        time_font = font_manager.load_font("regular", 20)
        draw.text((bar_x, bar_y - 30), start_time, font=time_font, fill=time_color)
        draw.text(
            (bar_x + bar_width - 40, bar_y - 30),
            end_time,
            font=time_font,
            fill=time_color,
        )

        # Title
        title_font = font_manager.load_font("extra_bold", 80)
        draw_text_with_shadow(draw, name, title_font, name_color, "#000000", (50, 100))

        # Author
        author_font = font_manager.load_font("regular", 60)
        draw_text_with_shadow(
            draw, author, author_font, author_color, "#000000", (50, 200)
        )

        # Render logo
        self.render_logo(image, data)

        # Render watermark
        self.render_watermark(image, data)
