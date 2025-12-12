"""
SVG export utilities for Musicard
"""

import base64
import io
import xml.etree.ElementTree as ET  # nosec B405
from pathlib import Path
from typing import Any, Dict, List, Union
from xml.dom import minidom  # nosec B408

from PIL import Image


def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """Convert PIL image to base64 data URL."""
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/{format.lower()};base64,{image_data}"


def create_svg_card(width: int, height: int, elements: List[Dict[str, Any]]) -> str:
    """Create SVG from card elements.

    Args:
        width: Card width
        height: Card height
        elements: List of SVG elements

    Returns:
        SVG string
    """
    # Create SVG root
    svg = ET.Element(
        "svg",
        {
            "width": str(width),
            "height": str(height),
            "viewBox": f"0 0 {width} {height}",
            "xmlns": "http://www.w3.org/2000/svg",
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
        },
    )

    # Add elements
    for element in elements:
        elem_type = element.pop("type")
        elem = ET.SubElement(svg, elem_type, element)

        # Add text content if present
        if "text" in element:
            elem.text = element["text"]

    # Convert to string with pretty formatting
    rough_string = ET.tostring(svg, encoding="unicode")
    reparsed = minidom.parseString(rough_string)  # nosec B318
    return reparsed.toprettyxml(indent="  ")


def card_to_svg_elements(
    image: Image.Image, data: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Convert a music card to SVG elements.

    This is a simplified conversion - for full SVG export,
    each theme would need custom SVG rendering logic.

    Args:
        image: PIL Image of the card
        data: Card data

    Returns:
        List of SVG elements
    """
    elements = []

    # Convert image to base64
    image_data = image_to_base64(image)

    # Add background image
    elements.append(
        {
            "type": "image",
            "x": "0",
            "y": "0",
            "width": str(image.width),
            "height": str(image.height),
            "xlink:href": image_data,
        }
    )

    return elements


def export_svg(
    image: Image.Image, data: Dict[str, Any], path: Union[str, Path]
) -> None:
    """Export card as SVG.

    Args:
        image: PIL Image
        data: Card data
        path: Output path
    """
    elements = card_to_svg_elements(image, data)
    svg_content = create_svg_card(image.width, image.height, elements)

    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_content)
