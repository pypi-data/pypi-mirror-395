"""
Legacy tests for backward compatibility.
These tests use the old MusicCard API which is now deprecated.
"""

from PIL import Image

# Import the old API for backward compatibility testing
from musicard.card import MusicCard


def test_card_generation():
    card = MusicCard("Test Song", "Test Artist", progress=0.5)
    img = card.generate()
    assert isinstance(img, Image.Image)
    assert img.size == (1200, 400)


def test_to_bytes():
    card = MusicCard("Test", "Artist")
    data = card.to_bytes()
    assert isinstance(data, bytes)
    # Check PNG header
    assert data[:8] == b"\x89PNG\r\n\x1a\n"


def test_theme_switching():
    card = MusicCard("Test", "Artist", theme="modern")
    img = card.generate()
    assert isinstance(img, Image.Image)


def test_mini_theme():
    card = MusicCard("Test", "Artist", theme="mini")
    img = card.generate()
    assert isinstance(img, Image.Image)


def test_invalid_theme():
    try:
        card = MusicCard("Test", "Artist", theme="invalid")
        card.generate()
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Unknown theme" in str(e)
