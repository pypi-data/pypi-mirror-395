"""
Tests for Musicard
"""

import pytest
from PIL import Image

from musicard import Musicard


def test_musicard_initialization():
    """Test Musicard class initialization."""
    card = Musicard()
    assert card.width == 1200
    assert card.height == 400


def test_generate_classic_theme():
    """Test generating a card with classic theme."""
    card = Musicard()
    image = card.generate_card(
        title="Test Song", artist="Test Artist", progress=50, theme="classic"
    )
    assert isinstance(image, Image.Image)
    assert image.size == (1200, 400)


def test_generate_mini_theme():
    """Test generating a card with mini theme."""
    card = Musicard()
    image = card.generate_card(
        title="Test Song", artist="Test Artist", progress=75, theme="mini"
    )
    assert isinstance(image, Image.Image)
    assert image.size == (1200, 400)


def test_invalid_theme():
    """Test error handling for invalid theme."""
    card = Musicard()
    with pytest.raises(ValueError):
        card.generate_card(title="Test", artist="Artist", theme="invalid")


def test_to_bytes():
    """Test converting image to bytes."""
    card = Musicard()
    image = card.generate_card("Test", "Artist")
    data = card.to_bytes(image)
    assert isinstance(data, bytes)
    assert len(data) > 0


def test_available_themes():
    """Test getting available themes."""
    card = Musicard()
    themes = card.get_available_themes()
    assert "classic" in themes
    assert "mini" in themes
    assert len(themes) >= 5  # All built-in themes


def test_custom_dimensions():
    """Test custom image dimensions."""
    card = Musicard(width=800, height=300)
    image = card.generate_card("Test", "Artist")
    assert image.size == (800, 300)
