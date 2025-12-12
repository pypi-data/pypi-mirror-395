"""
Musicard - A Python library for generating music card images
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from PIL import Image, ImageDraw, ImageFilter

from ..utils.images import load_image, resize_image


class BaseTheme(ABC):
    """Abstract base class for all music card themes."""

    def __init__(self, width: int = 1200, height: int = 400):
        self.width = width
        self.height = height

    @abstractmethod
    def render(
        self, image: Image.Image, draw: ImageDraw.ImageDraw, data: Dict[str, Any]
    ) -> None:
        """Render the theme on the image.

        Args:
            image: PIL Image to draw on
            draw: PIL ImageDraw object
            data: Dictionary containing theme-specific data
        """
        pass

    def get_default_data(self) -> Dict[str, Any]:
        """Get default data for the theme."""
        return {
            "name": "Musicard",
            "author": "By Unburn",
            "thumbnailImage": None,
            "progress": 0,
            "progressColor": "#FF7A00",
            "progressBarColor": "#5F2D00",
            "backgroundColor": "#070707",
            "nameColor": "#FF7A00",
            "authorColor": "#FFFFFF",
            "logoPath": None,
            "logoPosition": (50, 50),
            "logoOpacity": 1.0,
            "logoBlendMode": "normal",
            "autoLogo": False,
            "watermarkEnabled": False,
            "watermarkText": "",
            "backgroundBlurLevel": 0.0,
            "exportQuality": "standard",
        }

    def render_logo(self, image: Image.Image, data: Dict[str, Any]) -> None:
        """Render the song logo on the image.

        Args:
            image: PIL Image to draw on
            data: Theme data dictionary
        """
        logo_path = data.get("logoPath")
        if not logo_path and not data.get("autoLogo"):
            return

        # If auto logo enabled and no logo, try to use thumbnail as fallback
        if not logo_path and data.get("autoLogo"):
            logo_path = data.get("thumbnailImage")
            if not logo_path:
                return

        try:
            if not logo_path or not isinstance(logo_path, (str, bytes)):
                return
            logo = load_image(logo_path)
            if logo is None:
                return

            # Auto-resize logo to fit (max 200x200)
            logo = resize_image(logo, (200, 200))

            # Apply opacity
            opacity = data.get("logoOpacity", 1.0)
            if opacity < 1.0:
                logo = logo.convert("RGBA")
                alpha = logo.split()[-1]
                alpha = alpha.point(lambda p: p * opacity)
                logo.putalpha(alpha)

            # Position
            pos = data.get("logoPosition", (50, 50))

            # Blend mode
            blend_mode = data.get("logoBlendMode", "normal")
            if blend_mode == "normal":
                image.paste(logo, pos, logo if logo.mode == "RGBA" else None)
            else:
                # For other blend modes, use composite
                mask = logo if logo.mode == "RGBA" else None
                if blend_mode == "multiply":
                    image.paste(logo, pos, mask)
                    # Multiply blend: darken the image
                    blended = Image.new("RGBA", image.size)
                    blended.paste(image, (0, 0))
                    blended.paste(logo, pos, mask)
                    image.paste(blended, (0, 0))
                elif blend_mode == "overlay":
                    # Simple overlay approximation
                    image.paste(logo, pos, mask)
                elif blend_mode == "screen":
                    # Screen blend: lighten
                    image.paste(logo, pos, mask)

            # Add glow effect (simple drop shadow)
            glow_color = (255, 255, 255, 128)
            glow_offset = (2, 2)
            glow_logo = logo.filter(ImageFilter.GaussianBlur(3))
            image.paste(glow_color, (pos[0] + glow_offset[0], pos[1] + glow_offset[1]), glow_logo)

        except Exception:
            # Silently fail if logo loading/rendering fails
            pass

    def render_watermark(self, image: Image.Image, data: Dict[str, Any]) -> None:
        """Render watermark on the image.

        Args:
            image: PIL Image to draw on
            data: Theme data dictionary
        """
        if not data.get("watermarkEnabled", False):
            return

        text = data.get("watermarkText", "")
        if not text:
            return

        from ..utils.fonts import font_manager
        from ..utils.text import draw_text_with_shadow

        # Simple watermark at bottom right
        font = font_manager.load_font("regular", 20)
        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = image.width - text_width - 10
        y = image.height - text_height - 10
        draw_text_with_shadow(draw, text, font, "#FFFFFF", "#000000", (int(x), int(y)))
