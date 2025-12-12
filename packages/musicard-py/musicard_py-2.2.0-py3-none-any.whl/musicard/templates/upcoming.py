"""
Upcoming theme implementation
"""

from PIL import Image, ImageDraw

from ..utils.fonts import font_manager
from ..utils.images import adjust_brightness, blur_image, load_image, resize_image
from ..utils.text import draw_text_centered
from .base_theme import BaseTheme


class UpcomingTheme(BaseTheme):
    """Upcoming music card theme with track index visualization."""

    def render(self, image: Image.Image, draw: ImageDraw.ImageDraw, data: dict) -> None:
        # Extract data with defaults
        name = data.get("title", "Musicard")
        author = data.get("author", "By Unburn")
        thumbnail_image = data.get("thumbnailImage")
        background_image = data.get("backgroundImage")
        image_darkness = data.get("imageDarkness", 70)
        track_index_background_radii = data.get(
            "trackIndexBackgroundRadii", [10, 20, 30, 40, 50, 60, 70, 80, 80, 100]
        )

        # Background
        if background_image:
            try:
                bg_img = load_image(background_image)
                bg_img = resize_image(
                    bg_img, (image.width, image.height), maintain_aspect=False
                )
                darkness_factor = (100 - image_darkness) / 100
                bg_img = adjust_brightness(bg_img, darkness_factor)
                blur_level = 5 + data.get("backgroundBlurLevel", 0.0) * 10
                bg_img = blur_image(bg_img, blur_level)
                image.paste(bg_img, (0, 0))
            except Exception:
                draw.rectangle([(0, 0), (image.width, image.height)], fill="#1a1a1a")

        # Track index visualization (circles)
        center_x = image.width // 2
        center_y = image.height // 2
        num_circles = len(track_index_background_radii)

        for i, radius in enumerate(track_index_background_radii):
            alpha = int(255 * (i + 1) / num_circles * 0.3)  # Fade effect
            color = (255, 255, 255, alpha)
            circle_img = Image.new("RGBA", (image.width, image.height), (0, 0, 0, 0))
            circle_draw = ImageDraw.Draw(circle_img)
            circle_draw.ellipse(
                [
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                ],
                fill=color,
            )
            image = Image.alpha_composite(image.convert("RGBA"), circle_img)

        # Thumbnail
        if thumbnail_image:
            try:
                thumb = load_image(thumbnail_image)
                thumb = resize_image(thumb, (200, 200))
                # Position in center
                thumb_x = center_x - 100
                thumb_y = center_y - 100
                image.paste(thumb, (thumb_x, thumb_y))
            except Exception:
                pass

        # Title
        title_font = font_manager.load_font("bold", 48)
        draw_text_centered(
            draw, name, title_font, "#FFFFFF", (center_x, center_y + 150)
        )

        # Author
        author_font = font_manager.load_font("regular", 32)
        draw_text_centered(
            draw, author, author_font, "#CCCCCC", (center_x, center_y + 200)
        )

        # Render logo
        self.render_logo(image, data)
