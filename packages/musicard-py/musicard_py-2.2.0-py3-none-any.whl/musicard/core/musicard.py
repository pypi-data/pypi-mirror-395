"""
Main Musicard class for generating music card images
"""

import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from PIL import Image, ImageDraw

from musicard.templates.base_theme import BaseTheme
from musicard.templates.classic import ClassicTheme
from musicard.templates.classic_pro import ClassicProTheme
from musicard.templates.dynamic import DynamicTheme
from musicard.templates.mini import MiniTheme
from musicard.templates.upcoming import UpcomingTheme
from musicard.utils.cache import cache
from musicard.utils.svg import export_svg


class Musicard:
    """
    Main class for generating music card images with various themes.

    Example:
        card = Musicard()
        image = card.generate_card(
            title="Song Title",
            artist="Artist Name",
            theme="classic",
            progress=75
        )
        card.save(image, "output.png")
    """

    def __init__(self, width: int = 1200, height: int = 400):
        """Initialize Musicard.

        Args:
            width: Default image width
            height: Default image height
        """
        self.width = width
        self.height = height
        self._themes = {
            "classic": ClassicTheme,
            "classic_pro": ClassicProTheme,
            "dynamic": DynamicTheme,
            "mini": MiniTheme,
            "upcoming": UpcomingTheme,
        }
        self._custom_themes: Dict[str, BaseTheme] = {}

        # Logo settings
        self.logo_path: Optional[str] = None
        self.logo_position: tuple[int, int] = (50, 50)
        self.logo_opacity: float = 1.0
        self.logo_blend_mode: str = "normal"
        self.auto_logo: bool = False

        # Watermark settings
        self.watermark_enabled: bool = False
        self.watermark_text: str = ""

        # Export settings
        self.export_quality: str = "standard"

        # Background blur
        self.background_blur_level: float = 0.0

        # Profiles
        self.current_profile: Optional[str] = None

    def generate_card(
        self,
        title: str,
        artist: str,
        thumbnail: Optional[Union[str, bytes]] = None,
        progress: float = 0.0,
        theme: str = "classic",
        **kwargs,
    ) -> Image.Image:
        """Generate a music card image.

        Args:
            title: Song title
            artist: Artist name
            thumbnail: Thumbnail image URL, path, or bytes
            progress: Progress (0-100)
            theme: Theme name
            **kwargs: Additional theme-specific options

        Returns:
            PIL Image object
        """
        # Prepare data
        data = {
            "name": title,
            "author": artist,
            "thumbnailImage": thumbnail,
            "progress": progress,
            "logoPath": self.logo_path,
            "logoPosition": self.logo_position,
            "logoOpacity": self.logo_opacity,
            "logoBlendMode": self.logo_blend_mode,
            "autoLogo": self.auto_logo,
            "watermarkEnabled": self.watermark_enabled,
            "watermarkText": self.watermark_text,
            "backgroundBlurLevel": self.background_blur_level,
            "exportQuality": self.export_quality,
            **kwargs,
        }

        # Create image
        image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Get theme
        if theme in self._custom_themes:
            theme_instance = self._custom_themes[theme]
        elif theme in self._themes:
            theme_instance = self._themes[theme](self.width, self.height)  # type: ignore
        else:
            raise ValueError(
                f"Unknown theme: {theme}. Available: {list(self._themes.keys()) + list(self._custom_themes.keys())}"
            )

        # Render
        theme_instance.render(image, draw, data)

        # Apply export quality scaling
        quality = data.get("exportQuality", "standard")
        if quality == "8k":
            # Scale to 8K resolution (7680x4320 aspect maintained)
            scale_factor = 7680 / self.width
            new_size = (int(self.width * scale_factor), int(self.height * scale_factor))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        elif quality == "high":
            # 4K
            scale_factor = 3840 / self.width
            new_size = (int(self.width * scale_factor), int(self.height * scale_factor))
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        return image

    async def async_generate_card(
        self,
        title: str,
        artist: str,
        thumbnail: Optional[Union[str, bytes]] = None,
        progress: float = 0.0,
        theme: str = "classic",
        **kwargs,
    ) -> Image.Image:
        """Asynchronously generate a music card image.

        Args:
            title: Song title
            artist: Artist name
            thumbnail: Thumbnail image URL, path, or bytes
            progress: Progress (0-100)
            theme: Theme name
            **kwargs: Additional theme-specific options

        Returns:
            PIL Image object
        """
        # For now, PIL operations are synchronous
        # In future, could make image loading async
        return self.generate_card(title, artist, thumbnail, progress, theme, **kwargs)

    def to_bytes(self, image: Image.Image, format: str = "PNG") -> bytes:
        """Convert image to bytes.

        Args:
            image: PIL Image
            format: Image format ('PNG', 'JPEG', etc.)

        Returns:
            Image data as bytes
        """
        buffer = BytesIO()
        image.save(buffer, format=format)
        return buffer.getvalue()

    def save(
        self, image: Image.Image, path: Union[str, Path], format: Optional[str] = None
    ) -> None:
        """Save image to file.

        Args:
            image: PIL Image
            path: File path
            format: Image format (auto-detected from extension if None)
        """
        if format is None:
            format = Path(path).suffix[1:].upper()
        image.save(path, format=format)

    def load_template(self, name: str) -> BaseTheme:
        """Load a built-in template.

        Args:
            name: Template name

        Returns:
            Theme instance
        """
        if name in self._themes:
            return self._themes[name](self.width, self.height)  # type: ignore
        raise ValueError(f"Unknown template: {name}")

    def register_custom_template(
        self, name: str, template_path: Union[str, Path]
    ) -> None:
        """Register a custom template from file.

        Args:
            name: Template name
            template_path: Path to template file (not implemented yet)
        """
        # TODO: Implement custom template loading
        raise NotImplementedError("Custom templates not yet implemented")

    def set_font(self, font_path: Union[str, Path]) -> None:
        """Set a custom font.

        Args:
            font_path: Path to font file
        """
        # TODO: Implement custom font loading
        raise NotImplementedError("Custom fonts not yet implemented")

    def set_theme(self, theme_name_or_dict: Union[str, Dict[str, Any]]) -> None:
        """Set theme configuration.

        Args:
            theme_name_or_dict: Theme name or configuration dict
        """
        if isinstance(theme_name_or_dict, str):
            # Set default theme
            self._default_theme = theme_name_or_dict
        else:
            # TODO: Implement theme configuration
            raise NotImplementedError("Theme configuration not yet implemented")

    def get_available_themes(self) -> List[str]:
        """Get list of available themes.

        Returns:
            List of theme names
        """
        return list(self._themes.keys()) + list(self._custom_themes.keys())

    def batch_generate(
        self, configs: List[Dict[str, Any]], output_dir: Union[str, Path] = "output"
    ) -> List[Image.Image]:
        """Generate multiple cards in batch.

        Args:
            configs: List of card configurations
            output_dir: Directory to save cards (optional)

        Returns:
            List of generated images
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        images = []
        for i, config in enumerate(configs):
            # Check cache first
            cached = cache.get_card(config)
            if cached:
                images.append(cached)
                continue

            # Generate new card
            image = self.generate_card(**config)
            images.append(image)

            # Cache the result
            cache.set_card(config, image)

            # Save if output_dir provided
            if output_dir:
                filename = config.get("filename", f"card_{i+1}.png")
                self.save(image, output_dir / filename)

        return images

    async def async_batch_generate(
        self, configs: List[Dict[str, Any]], output_dir: Union[str, Path] = "output"
    ) -> List[Image.Image]:
        """Asynchronously generate multiple cards in batch.

        Args:
            configs: List of card configurations
            output_dir: Directory to save cards (optional)

        Returns:
            List of generated images
        """
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            tasks = [
                loop.run_in_executor(
                    executor, self.batch_generate, [config], output_dir
                )
                for config in configs
            ]
            results = await asyncio.gather(*tasks)
            return [img for sublist in results for img in sublist]

    def export_svg(
        self, image: Image.Image, data: Dict[str, Any], path: Union[str, Path]
    ) -> None:
        """Export card as SVG.

        Args:
            image: Generated card image
            data: Card data used for generation
            path: Output SVG path
        """
        export_svg(image, data, path)

    def load_theme_preset(self, preset_path: Union[str, Path]) -> Dict[str, Any]:
        """Load theme preset from JSON file.

        Args:
            preset_path: Path to preset JSON file

        Returns:
            Preset configuration
        """
        with open(preset_path, "r") as f:
            return json.load(f)

    def save_theme_preset(
        self, config: Dict[str, Any], preset_path: Union[str, Path]
    ) -> None:
        """Save theme configuration as preset.

        Args:
            config: Theme configuration
            preset_path: Path to save preset
        """
        with open(preset_path, "w") as f:
            json.dump(config, f, indent=2)

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics.

        Returns:
            Cache statistics
        """
        return cache.stats()

    def clear_cache(self) -> None:
        """Clear all caches."""
        cache.clear()

    def set_song_logo(self, path_or_url: str) -> None:
        """Set the song logo path or URL.

        Args:
            path_or_url: Path to logo image or URL
        """
        self.logo_path = path_or_url

    def set_logo_position(self, x: int, y: int) -> None:
        """Set the logo position.

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.logo_position = (x, y)

    def set_logo_opacity(self, value: float) -> None:
        """Set the logo opacity.

        Args:
            value: Opacity value between 0.0 and 1.0
        """
        self.logo_opacity = max(0.0, min(1.0, value))

    def set_logo_blend_mode(self, mode: str) -> None:
        """Set the logo blend mode.

        Args:
            mode: Blend mode ('normal', 'multiply', 'overlay', 'screen')
        """
        valid_modes = ['normal', 'multiply', 'overlay', 'screen']
        if mode not in valid_modes:
            raise ValueError(f"Invalid blend mode. Must be one of: {valid_modes}")
        self.logo_blend_mode = mode

    def enable_auto_logo(self, enabled: bool) -> None:
        """Enable or disable automatic logo fetching.

        Args:
            enabled: Whether to enable auto logo
        """
        self.auto_logo = enabled

    def enable_watermark(self, enabled: bool) -> None:
        """Enable or disable watermark.

        Args:
            enabled: Whether to enable watermark
        """
        self.watermark_enabled = enabled

    def set_watermark_text(self, text: str) -> None:
        """Set the watermark text.

        Args:
            text: Watermark text
        """
        self.watermark_text = text

    def use_profile(self, profile_name: str) -> None:
        """Load and apply a profile configuration.

        Args:
            profile_name: Name of the profile to load
        """
        # TODO: Implement profile loading
        self.current_profile = profile_name

    def enable_background_blur(self, level: float) -> None:
        """Enable background blur effect.

        Args:
            level: Blur level (0.0 to 1.0)
        """
        self.background_blur_level = max(0.0, min(1.0, level))

    def set_export_quality(self, mode: str) -> None:
        """Set export quality mode.

        Args:
            mode: Quality mode ('standard', 'high', '8k')
        """
        valid_modes = ['standard', 'high', '8k']
        if mode not in valid_modes:
            raise ValueError(f"Invalid quality mode. Must be one of: {valid_modes}")
        self.export_quality = mode

    @classmethod
    def from_json(cls, json_path: Union[str, Path]) -> "Musicard":
        """Create Musicard instance from JSON configuration.

        Args:
            json_path: Path to JSON config file

        Returns:
            Musicard instance
        """
        with open(json_path, "r") as f:
            config = json.load(f)

        width = config.get("width", 1200)
        height = config.get("height", 400)

        instance = cls(width, height)

        # Load custom themes if any
        # TODO: Implement

        return instance
