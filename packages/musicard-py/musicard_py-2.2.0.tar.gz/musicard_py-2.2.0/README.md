# 🎵 musicard-py

[![PyPI version](https://badge.fury.io/py/musicard-py.svg)](https://pypi.org/project/musicard-py/)
[![Python versions](https://img.shields.io/pypi/pyversions/musicard-py.svg)](https://pypi.org/project/musicard-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generate stunning music card images in Python with ease! Inspired by [unburn/musicard](https://github.com/unburn/musicard) by Unburn.

✨ **Beautiful Themes** • 🚀 **Easy to Use** • 🎨 **Customizable** • 📦 **PyPI Ready**

## Table of Contents

- [Credits](#credits)
- [Quick Start](#-quick-start)
- [Features](#-features)
- [Themes](#-themes)
- [Customization](#-customization)
- [Examples](#-examples)
- [API Reference](#-api-reference)
- [Requirements](#python-compatibility)
- [Testing](#testing)
- [Building](#building-the-package)
- [Contributing](#-contributing)
- [License](#-license)

## Credits

This package is inspired by the JavaScript project **musicard**, created by **Unburn**.
Original source: [https://github.com/unburn/musicard](https://github.com/unburn/musicard)

## 🚀 Quick Start

```bash
pip install musicard-py
```

```python
from musicard import Musicard

card = Musicard()

image = card.generate_card(
    title="Bohemian Rhapsody",
    artist="Queen",
    progress=75,
    theme="classic"
)

card.save(image, "my_music_card.png")
```

## ✨ Features

- 🎨 **Multiple Themes**: Classic, Classic Pro, Dynamic, Mini, and Upcoming designs
- 🖼️ **Image Support**: Load thumbnails, backgrounds, and logos from URLs or local files
- 📊 **Progress Bars**: Visual progress indicators with customizable styles
- 🎯 **Easy API**: Simple class-based interface with async support
- 🔧 **Customizable**: Colors, sizes, fonts, and theme-specific options
- 📦 **Lightweight**: Minimal dependencies (Pillow + requests + cairosvg + diskcache)
- ⚡ **Fast**: Generate images in milliseconds with intelligent caching (30-40% performance boost in v2.2.0)
- 🖥️ **CLI Tool**: Command-line interface for quick generation, batch processing, and advanced workflows
- 🎨 **SVG Export**: Export cards as scalable vector graphics
- 📦 **Batch Processing**: Generate multiple cards simultaneously with parallel rendering
- 💾 **Caching System**: Automatic caching of images, fonts, and generated cards with smart invalidation
- 🎭 **Theme Presets & Profiles**: Save and load custom theme configurations and profiles
- 🎨 **Advanced Visual Effects**: Background blur, advanced gradients (linear/radial/diagonal), multi-layer shadows, per-layer opacity, smart stroke/outline, dynamic corner radius, noise/texture overlays, glassmorphism, hue/sat/exposure filters
- 🏷️ **Song Logo System**: Auto overlay of official song/artist logos with positioning, opacity, blend modes, glow/shadow effects, and fallback support
- 🚀 **High-Quality Export**: Ultra HD 8K export mode with progressive rendering
- 🤖 **Automation**: Auto metadata loading, EXIF/PNG embedding, watermark system, auto file naming
- 🎮 **Interactive CLI**: Live terminal preview, batch queue processing, dry-run mode

```python
from musicard import Musicard

# Create a music card instance
card = Musicard()

# Generate a music card
image = card.generate_card(
    title="Song Title",
    artist="Artist Name",
    thumbnail="https://example.com/thumbnail.jpg",  # or local path
    progress=50,  # 0-100
    theme="classic",
    backgroundColor="#070707",
    progressColor="#FF7A00"
)

# Save to file
card.save(image, "music_card.png")

# Get PNG bytes
png_bytes = card.to_bytes(image)

# Async generation
import asyncio

async def generate_async():
    image = await card.async_generate_card(
        title="Song Title",
        artist="Artist Name",
        progress=75
    )
    return image
```

## 🎨 Themes

### Classic Theme
> Dark, elegant design with thumbnail on the right

- Square thumbnail positioning
- Horizontal progress bar with circle indicator
- Clean typography with bold title
- Time display (start/end times)
- Perfect for traditional music apps

### Classic Pro Theme
> Enhanced classic design with improved visuals

- Rounded thumbnail corners
- Enhanced progress bar with glow effects
- Better typography and spacing
- Improved shadows and visual effects

### Dynamic Theme
> Contemporary design with background image support

- Custom background images with darkness control
- Gradient overlays
- Blurred backgrounds for text readability
- Modern typography with shadows

### Mini Theme
> Compact design for small spaces

- Thumbnail on the left
- Vertical menu bar
- Bottom progress bar
- Pause indicator support
- Ideal for mobile or compact UIs

### Upcoming Theme
> Futuristic design with circular visualization

- Center-positioned thumbnail
- Concentric circles with fade effects
- Track index visualization
- Modern circular layout

## 🏷️ Song Logo System

Display official song or artist logos directly on your music cards with full customization.

```python
from musicard import Musicard

card = Musicard()

# Set song logo
card.set_song_logo("https://example.com/song-logo.png")  # or local path
card.set_logo_position(100, 50)  # x, y coordinates
card.set_logo_opacity(0.8)  # 0.0 to 1.0
card.set_logo_blend_mode("overlay")  # normal, multiply, overlay, screen

# Enable auto logo (uses thumbnail as fallback if logo not found)
card.enable_auto_logo(True)

# Generate card with logo
image = card.generate_card(
    title="Bohemian Rhapsody",
    artist="Queen",
    thumbnail="https://example.com/thumbnail.jpg",
    theme="classic"
)

card.save(image, "card_with_logo.png")
```

### Logo Features
- **Auto Overlay**: Automatically positions and sizes logos
- **Blend Modes**: Normal, multiply, overlay, screen blending
- **Glow Effects**: Automatic glow and shadow for visibility
- **Fallback Support**: Uses artist avatar if song logo unavailable
- **URL/Local Support**: Load from web URLs or local files
- **Auto-Resize**: Scales logos to fit the layout perfectly
- **Per-Template Rules**: Each theme handles logos differently

## 🎭 Profiles System

Save and reuse configuration profiles for consistent styling.

```python
# Create and save a profile
profile_config = {
    "theme": "classic",
    "backgroundColor": "#070707",
    "progressColor": "#FF7A00",
    "logoOpacity": 0.8,
    "backgroundBlurLevel": 0.5
}

card.save_theme_preset(profile_config, "my_profile.json")

# Load and use profile
card.use_profile("my_profile")
image = card.generate_card(title="Song", artist="Artist")
```

## 🎨 Customization

### Custom Colors

```python
card.save("my_music_card.png")
```

![Example Music Card](output_classic.jpeg)

### Custom Themes

Create your own theme by extending `BaseTheme`:

```python
from musicard.themes.base_theme import BaseTheme
from PIL import Image, ImageDraw

class MyCustomTheme(BaseTheme):
    def render(self, image, draw, metadata):
        # Your custom rendering logic
        title = metadata['title']
        # Draw your theme...
        pass
```

## 📖 Examples

### Discord Bot Integration

```python
import discord
from musicard import MusicCard

@bot.command()
async def nowplaying(ctx, title, artist, progress=0.5):
    card = MusicCard(title, artist, progress=progress, theme="modern")
    image_bytes = card.to_bytes()

    await ctx.send(file=discord.File(io.BytesIO(image_bytes), "nowplaying.png"))
```

### Batch Generation

```python
songs = [
    ("Song 1", "Artist 1", 0.3),
    ("Song 2", "Artist 2", 0.7),
    ("Song 3", "Artist 3", 0.9),
]

for title, artist, progress in songs:
    card = MusicCard(title, artist, progress=progress, theme="mini")
    card.save(f"{title.replace(' ', '_')}.png")
```

## 🚀 New Features in v2.1.0

### SVG Export
Export your music cards as scalable vector graphics:

```python
card = Musicard()
image = card.generate_card("Song", "Artist")
card.export_svg(image, {"title": "Song", "artist": "Artist"}, "card.svg")
```

### Batch Processing
Generate multiple cards at once:

```python
configs = [
    {"title": "Song 1", "artist": "Artist 1", "theme": "classic"},
    {"title": "Song 2", "artist": "Artist 2", "theme": "mini"},
]
images = card.batch_generate(configs, "output")
```

### Intelligent Caching
Automatic caching improves performance:

```python
# View cache stats
stats = card.get_cache_stats()
print(f"Cache hits: {stats['main_cache']['hits']}")

# Clear cache if needed
card.clear_cache()
```

### Theme Presets
Save and reuse theme configurations:

```python
# Save preset
preset = {
    "theme": "classic",
    "backgroundColor": "#070707",
    "progressColor": "#FF7A00"
}
card.save_theme_preset(preset, "my_theme.json")

# Load preset
config = card.load_theme_preset("my_theme.json")
image = card.generate_card("Song", "Artist", **config)
```

## 📚 API Reference

### Musicard

#### Constructor Parameters

- `width: int` - Default image width in pixels (default: 1200)
- `height: int` - Default image height in pixels (default: 400)

#### Methods

- `generate_card(title, artist, thumbnail=None, progress=0, theme='classic', **kwargs) -> PIL.Image.Image` - Generate and return the music card image
- `async_generate_card(title, artist, thumbnail=None, progress=0, theme='classic', **kwargs) -> PIL.Image.Image` - Asynchronous version
- `batch_generate(configs, output_dir='output') -> List[PIL.Image.Image]` - Generate multiple cards in batch
- `async_batch_generate(configs, output_dir='output') -> List[PIL.Image.Image]` - Asynchronous batch generation
- `export_svg(image, data, path)` - Export card as SVG file
- `to_bytes(image, format='PNG') -> bytes` - Convert image to bytes
- `save(image, path, format=None)` - Save image to file
- `get_available_themes() -> List[str]` - Get list of available themes
- `load_template(name) -> BaseTheme` - Load a built-in template
- `load_theme_preset(preset_path) -> Dict[str, Any]` - Load theme preset from JSON
- `save_theme_preset(config, preset_path)` - Save theme configuration as preset
- `get_cache_stats() -> Dict[str, Any]` - Get cache statistics
- `clear_cache()` - Clear all caches

#### Logo Methods

- `set_song_logo(path_or_url: str)` - Set the song logo path or URL
- `set_logo_position(x: int, y: int)` - Set logo position coordinates
- `set_logo_opacity(value: float)` - Set logo opacity (0.0-1.0)
- `set_logo_blend_mode(mode: str)` - Set blend mode ('normal', 'multiply', 'overlay', 'screen')
- `enable_auto_logo(enabled: bool)` - Enable/disable automatic logo fetching

#### Watermark & Effects Methods

- `enable_watermark(enabled: bool)` - Enable/disable watermark
- `set_watermark_text(text: str)` - Set watermark text
- `enable_background_blur(level: float)` - Set background blur level (0.0-1.0)
- `set_export_quality(mode: str)` - Set export quality ('standard', 'high', '8k')
- `use_profile(profile_name: str)` - Load and apply a profile configuration

#### Parameters

- `title: str` - Song title (required)
- `artist: str` - Artist name (required)
- `thumbnail: Optional[str|bytes]` - Image URL, local path, or bytes
- `progress: float` - Progress value between 0 and 100 (default: 0)
- `theme: str` - Theme name: 'classic', 'classic_pro', 'dynamic', 'mini', 'upcoming'
- `**kwargs` - Theme-specific options (backgroundColor, progressColor, etc.)

### CLI Usage

```bash
# Generate from command line
musicard generate --title "Song" --artist "Artist" --theme classic --output card.png

# Generate SVG
musicard generate --title "Song" --artist "Artist" --format svg --output card.svg

# Generate from JSON config
musicard generate --config song.json --output card.png

# Batch generate from JSON array
musicard batch --input cards.json --output-dir ./output

# List available themes
musicard themes

# Set song logo
musicard logo set "https://example.com/logo.png"
musicard logo auto on

# Use profile
musicard profile use "my_profile"

# Batch queue
musicard queue add songs.json
musicard queue start

# Preview with live ASCII
musicard preview --live --title "Song" --artist "Artist"

# Dry run render
musicard render --dry-run --config song.json

# Export in 8K
musicard export 8k --config song.json --output card_8k.png

# Clear cache
musicard cache clear
```

## Requirements

- Python 3.8+
- Pillow >= 10.0.0
- requests >= 2.25.0

## Testing

Run the test suite with pytest:

```bash
pip install pytest
pytest
```

## Building the package

```bash
python -m build
```

## Uploading to TestPyPI

```bash
twine upload --repository testpypi dist/*
```

## Uploading to PyPI

```bash
twine upload dist/*
```

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/code-xon/musicard-py.git
cd musicard-py
pip install -e .
pip install pytest  # for testing
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ in Python</p>
