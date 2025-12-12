"""
Enhanced image utilities for Musicard
"""

import io
from typing import Tuple, Union, cast

import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


def load_image(path_or_url: Union[str, bytes]) -> Image.Image:
    """Load an image from a local path, URL, or bytes.

    Args:
        path_or_url: Image path, URL, or bytes

    Returns:
        PIL Image object
    """
    if isinstance(path_or_url, bytes):
        return Image.open(io.BytesIO(path_or_url))
    elif isinstance(path_or_url, str):
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            response = requests.get(path_or_url, timeout=10)
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content))
        else:
            return Image.open(path_or_url)
    else:
        raise ValueError("Invalid image source")


def resize_image(
    image: Image.Image, size: Tuple[int, int], maintain_aspect: bool = True
) -> Image.Image:
    """Resize an image to the given size.

    Args:
        image: PIL Image
        size: Target size (width, height)
        maintain_aspect: Whether to maintain aspect ratio

    Returns:
        Resized PIL Image
    """
    if maintain_aspect:
        image.thumbnail(size, Image.Resampling.LANCZOS)
    else:
        image = image.resize(size, Image.Resampling.LANCZOS)
    return image


def create_gradient(
    size: Tuple[int, int],
    start_color: Tuple[int, int, int],
    end_color: Tuple[int, int, int],
    direction: str = "vertical",
    gradient_type: str = "linear",
) -> Image.Image:
    """Create an advanced gradient image.

    Args:
        size: Image size (width, height)
        start_color: Starting RGB color
        end_color: Ending RGB color
        direction: 'vertical', 'horizontal', 'diagonal'
        gradient_type: 'linear' or 'radial'

    Returns:
        Gradient PIL Image
    """
    width, height = size
    gradient = Image.new("RGB", size)

    if gradient_type == "radial":
        center_x, center_y = width // 2, height // 2
        max_distance = ((width // 2) ** 2 + (height // 2) ** 2) ** 0.5
        for y in range(height):
            for x in range(width):
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                factor = min(distance / max_distance, 1.0)
                r = int(start_color[0] + (end_color[0] - start_color[0]) * factor)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * factor)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * factor)
                gradient.putpixel((x, y), (r, g, b))
    else:  # linear
        if direction == "vertical":
            for y in range(height):
                factor = y / height
                r = int(start_color[0] + (end_color[0] - start_color[0]) * factor)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * factor)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * factor)
                for x in range(width):
                    gradient.putpixel((x, y), (r, g, b))
        elif direction == "horizontal":
            for x in range(width):
                factor = x / width
                r = int(start_color[0] + (end_color[0] - start_color[0]) * factor)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * factor)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * factor)
                for y in range(height):
                    gradient.putpixel((x, y), (r, g, b))
        elif direction == "diagonal":
            for y in range(height):
                for x in range(width):
                    factor = (x + y) / (width + height)
                    r = int(start_color[0] + (end_color[0] - start_color[0]) * factor)
                    g = int(start_color[1] + (end_color[1] - start_color[1]) * factor)
                    b = int(start_color[2] + (end_color[2] - start_color[2]) * factor)
                    gradient.putpixel((x, y), (r, g, b))

    return gradient


def create_rounded_mask(size: Tuple[int, int], radius: int) -> Image.Image:
    """Create a rounded rectangle mask.

    Args:
        size: Mask size
        radius: Corner radius

    Returns:
        Mask image
    """
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def apply_mask(image: Image.Image, mask: Image.Image) -> Image.Image:
    """Apply a mask to an image.

    Args:
        image: Source image
        mask: Mask image

    Returns:
        Masked image
    """
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    image.putalpha(mask)
    return image


def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
    """Adjust image brightness.

    Args:
        image: PIL Image
        factor: Brightness factor (0.0 = black, 1.0 = original, >1.0 = brighter)

    Returns:
        Adjusted image
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def blur_image(image: Image.Image, radius: float = 5.0) -> Image.Image:
    """Apply Gaussian blur to an image.

    Args:
        image: PIL Image
        radius: Blur radius

    Returns:
        Blurred image
    """
    return image.filter(ImageFilter.GaussianBlur(radius))


def draw_rounded_rectangle(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int, int, int],
    radius: int,
    fill=None,
    outline=None,
    width: int = 1,
) -> None:
    """Draw a rounded rectangle.

    Args:
        draw: ImageDraw object
        xy: Rectangle coordinates (x1, y1, x2, y2)
        radius: Corner radius
        fill: Fill color
        outline: Outline color
        width: Outline width
    """
    x1, y1, x2, y2 = xy
    draw.rectangle(
        [x1 + radius, y1, x2 - radius, y2], fill=fill, outline=outline, width=width
    )
    draw.rectangle(
        [x1, y1 + radius, x2, y2 - radius], fill=fill, outline=outline, width=width
    )
    draw.ellipse(
        [x1, y1, x1 + 2 * radius, y1 + 2 * radius],
        fill=fill,
        outline=outline,
        width=width,
    )
    draw.ellipse(
        [x2 - 2 * radius, y1, x2, y1 + 2 * radius],
        fill=fill,
        outline=outline,
        width=width,
    )
    draw.ellipse(
        [x1, y2 - 2 * radius, x1 + 2 * radius, y2],
        fill=fill,
        outline=outline,
        width=width,
    )
    draw.ellipse(
        [x2 - 2 * radius, y2 - 2 * radius, x2, y2],
        fill=fill,
        outline=outline,
        width=width,
    )


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple.

    Args:
        hex_color: Hex color string (e.g., '#FF0000')

    Returns:
        RGB tuple
    """
    hex_color = hex_color.lstrip("#")
    values = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return cast(Tuple[int, int, int], values)


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color.

    Args:
        rgb: RGB tuple

    Returns:
        Hex color string
    """
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def add_noise_overlay(image: Image.Image, intensity: float = 0.1) -> Image.Image:
    """Add noise texture overlay to image.

    Args:
        image: PIL Image
        intensity: Noise intensity (0.0 to 1.0)

    Returns:
        Image with noise overlay
    """
    import random
    noise = Image.new("RGBA", image.size, (0, 0, 0, 0))
    pixels = []
    for _ in range(image.size[0] * image.size[1]):
        alpha = int(random.random() * 255 * intensity)
        pixels.append((255, 255, 255, alpha))
    noise.putdata(pixels)
    return Image.alpha_composite(image.convert("RGBA"), noise)


def apply_color_filter(image: Image.Image, hue: float = 0, saturation: float = 1, exposure: float = 1) -> Image.Image:
    """Apply hue, saturation, exposure filters.

    Args:
        image: PIL Image
        hue: Hue shift (-180 to 180) - not implemented yet
        saturation: Saturation multiplier
        exposure: Exposure multiplier

    Returns:
        Filtered image
    """
    # For now, only implement saturation and exposure
    # Hue shift requires more complex color space conversion

    # Saturation
    if saturation != 1:
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(saturation)

    # Exposure (brightness)
    if exposure != 1:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(exposure)

    return image


def create_glassmorphism_effect(image: Image.Image, blur_radius: float = 10, opacity: float = 0.5) -> Image.Image:
    """Apply glassmorphism effect (blur + transparency).

    Args:
        image: PIL Image
        blur_radius: Blur radius
        opacity: Opacity level

    Returns:
        Glassmorphism image
    """
    blurred = blur_image(image, blur_radius)
    glass = Image.new("RGBA", image.size, (255, 255, 255, int(255 * opacity)))
    return Image.alpha_composite(blurred.convert("RGBA"), glass)
