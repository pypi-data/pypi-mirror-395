"""
Font management system for Musicard
"""

import importlib.resources as res
import os
from typing import Any, Dict, Optional

from PIL import ImageFont


class FontManager:
    """Manages font loading and caching."""

    def __init__(self):
        self._font_cache: Dict[str, Any] = {}
        self._default_fonts = {
            "bold": "PlusJakartaSans-Bold.ttf",
            "regular": "PlusJakartaSans-Regular.ttf",
            "light": "PlusJakartaSans-Light.ttf",
            "medium": "PlusJakartaSans-Medium.ttf",
            "extra_bold": "PlusJakartaSans-ExtraBold.ttf",
            "extra_light": "PlusJakartaSans-ExtraLight.ttf",
            "semi_bold": "PlusJakartaSans-SemiBold.ttf",
        }

    def load_font(self, name: str, size: int) -> Any:
        """Load a font by name and size.

        Args:
            name: Font name or path
            size: Font size

        Returns:
            PIL ImageFont object
        """
        cache_key = f"{name}_{size}"

        if cache_key in self._font_cache:
            return self._font_cache[cache_key]

        # Check if it's a default font
        if name in self._default_fonts:
            try:
                font_path = str(res.files("musicard.fonts") / self._default_fonts[name])
                font = ImageFont.truetype(font_path, size)
            except Exception:
                font = ImageFont.load_default()
        elif os.path.isfile(name):
            # Load from file path
            font = ImageFont.truetype(name, size)
        else:
            # Fallback to default
            font = ImageFont.load_default()

        self._font_cache[cache_key] = font
        return font

    def get_font_path(self, name: str) -> Optional[str]:
        """Get the path to a default font."""
        if name in self._default_fonts:
            try:
                return str(res.files("musicard.fonts") / self._default_fonts[name])
            except Exception:
                return None
        return None


# Global font manager instance
font_manager = FontManager()
