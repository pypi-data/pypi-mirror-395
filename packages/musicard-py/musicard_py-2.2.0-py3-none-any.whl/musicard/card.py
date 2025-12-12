"""
Music Card Generator

A Python library for generating music card images, inspired by unburn/musicard.
"""

from io import BytesIO
from typing import Any, Optional

from PIL import Image, ImageDraw

from .themes import ClassicTheme, MiniTheme, ModernTheme


class MusicCard:
    """
    A class to generate music card images with various themes.

    Attributes:
        title (str): The song title.
        artist (str): The artist name.
        thumbnail (Optional[str]): URL or path to the thumbnail image.
        progress (float): Progress value between 0.0 and 1.0.
        width (int): Image width in pixels.
        height (int): Image height in pixels.
        theme (str): Theme name ('classic', 'modern', or 'mini').
    """

    def __init__(
        self,
        title: str,
        artist: str,
        thumbnail: Optional[str] = None,
        progress: float = 0.0,
        width: int = 1200,
        height: int = 400,
        theme: str = "classic",
        **kwargs: Any,
    ) -> None:
        """
        Initialize the MusicCard.

        Args:
            title: Song title
            artist: Artist name
            thumbnail: URL or path to thumbnail image
            progress: Progress (0.0 to 1.0)
            width: Image width
            height: Image height
            theme: Theme name
            **kwargs: Additional theme-specific options
        """
        self.title = title
        self.artist = artist
        self.thumbnail = thumbnail
        self.progress = max(0.0, min(1.0, progress))
        self.width = width
        self.height = height
        self.theme = theme
        self.kwargs = kwargs

    def generate(self) -> Image.Image:
        """
        Generate the music card image.

        Returns:
            PIL Image object
        """
        image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        metadata = {
            "title": self.title,
            "artist": self.artist,
            "thumbnail": self.thumbnail,
            "progress": self.progress,
            **self.kwargs,
        }

        theme_map = {
            "classic": ClassicTheme,
            "modern": ModernTheme,
            "mini": MiniTheme,
        }

        if self.theme not in theme_map:
            available = ", ".join(theme_map.keys())
            raise ValueError(
                f"Unknown theme: {self.theme}. Available themes: {available}"
            )

        theme_instance = theme_map[self.theme]()
        theme_instance.render(image, draw, metadata)
        return image

    async def async_generate(self) -> Image.Image:
        """
        Asynchronously generate the music card image.

        Returns:
            PIL Image object
        """
        # For now, since PIL is not async, just call sync
        # In future, could make image loading async
        return self.generate()

    def to_bytes(self) -> bytes:
        """
        Generate the image and return as PNG bytes.

        Returns:
            PNG image data as bytes
        """
        img = self.generate()
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()

    def save(self, path: str) -> None:
        """
        Generate the image and save to file.

        Args:
            path: File path to save the image
        """
        img = self.generate()
        img.save(path)
