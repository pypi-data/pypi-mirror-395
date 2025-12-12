"""
Text rendering utilities for Musicard
"""

from typing import Optional, Tuple, Union

from PIL import Image, ImageDraw, ImageFont


def draw_text_with_shadow(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: Union[ImageFont.FreeTypeFont, ImageFont.ImageFont],
    color: str,
    shadow_color: str,
    position: Tuple[int, int],
    shadow_offset: Tuple[int, int] = (2, 2),
    shadow_layers: int = 1,
    outline_color: Optional[str] = None,
    outline_width: int = 0,
) -> None:
    """Draw text with advanced shadow and outline effects.

    Args:
        draw: ImageDraw object
        text: Text to draw
        font: Font to use
        color: Text color
        shadow_color: Shadow color
        position: Text position (x, y)
        shadow_offset: Shadow offset (dx, dy)
        shadow_layers: Number of shadow layers
        outline_color: Outline color
        outline_width: Outline width
    """
    x, y = position
    dx, dy = shadow_offset

    # Draw shadow layers
    for layer in range(shadow_layers, 0, -1):
        offset_x = dx * layer
        offset_y = dy * layer
        alpha = 255 // (layer + 1)  # Fade with distance
        shadow_col = shadow_color
        if shadow_color.startswith("#"):
            # Apply alpha to shadow
            r, g, b = tuple(int(shadow_color[i:i+2], 16) for i in (1, 3, 5))
            shadow_img = Image.new("RGBA", (1, 1), (r, g, b, alpha))
            shadow_col = f"#{r:02x}{g:02x}{b:02x}{alpha:02x}"
        draw.text((x + offset_x, y + offset_y), text, font=font, fill=shadow_col)

    # Draw outline
    if outline_color and outline_width > 0:
        for ox in range(-outline_width, outline_width + 1):
            for oy in range(-outline_width, outline_width + 1):
                if ox == 0 and oy == 0:
                    continue
                draw.text((x + ox, y + oy), text, font=font, fill=outline_color)

    # Draw main text
    draw.text((x, y), text, font=font, fill=color)


def draw_text_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: Union[ImageFont.FreeTypeFont, ImageFont.ImageFont],
    color: str,
    position: Tuple[int, int],
) -> None:
    """Draw centered text at the given position.

    Args:
        draw: ImageDraw object
        text: Text to draw
        font: Font to use
        color: Text color
        position: Center position (x, y)
    """
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = position[0] - text_width // 2
    y = position[1] - text_height // 2
    draw.text((x, y), text, font=font, fill=color)


def wrap_text(
    text: str, font: Union[ImageFont.FreeTypeFont, ImageFont.ImageFont], max_width: int
) -> str:
    """Wrap text to fit within max_width.

    Args:
        text: Text to wrap
        font: Font to use
        max_width: Maximum width in pixels

    Returns:
        Wrapped text
    """
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = font.getbbox(test_line)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)


def fit_text_to_width(
    text: str,
    font: Union[ImageFont.FreeTypeFont, ImageFont.ImageFont],
    max_width: int,
    max_length: int = 50,
) -> str:
    """Fit text to width by truncating if necessary.

    Args:
        text: Original text
        font: Font to use
        max_width: Maximum width in pixels
        max_length: Maximum character length

    Returns:
        Fitted text
    """
    if len(text) > max_length:
        text = text[: max_length - 3] + "..."

    bbox = font.getbbox(text)
    if bbox[2] - bbox[0] <= max_width:
        return text

    # Truncate until it fits
    while len(text) > 3 and font.getbbox(text)[2] - font.getbbox(text)[0] > max_width:
        text = text[:-1]

    return text[:-3] + "..." if len(text) > 3 else text
