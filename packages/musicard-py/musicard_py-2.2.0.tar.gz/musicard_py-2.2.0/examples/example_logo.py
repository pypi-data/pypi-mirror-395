#!/usr/bin/env python3
"""
Example usage of Musicard with Song Logo System
"""

from musicard import Musicard


def main():
    # Create a music card instance
    card = Musicard()

    # Configure logo
    card.set_song_logo("https://example.com/song-logo.png")  # Replace with real logo URL
    card.set_logo_position(100, 50)
    card.set_logo_opacity(0.8)
    card.set_logo_blend_mode("overlay")
    card.enable_auto_logo(True)  # Fallback to thumbnail if logo fails

    # Enable additional effects
    card.enable_background_blur(0.3)
    card.enable_watermark(True)
    card.set_watermark_text("Musicard v2.2.0")

    # Generate card with logo
    print("Generating card with song logo...")
    image = card.generate_card(
        title="Bohemian Rhapsody",
        artist="Queen",
        thumbnail="https://example.com/thumbnail.jpg",  # Replace with real thumbnail
        progress=75,
        theme="classic",
        backgroundColor="#070707",
        progressColor="#FF7A00",
    )
    card.save(image, "example_with_logo.png")

    # Generate high quality version
    card.set_export_quality("high")
    print("Generating high quality version...")
    high_quality = card.generate_card(
        title="Bohemian Rhapsody",
        artist="Queen",
        progress=75,
        theme="classic"
    )
    card.save(high_quality, "example_high_quality.png")

    print("Logo examples generated successfully!")


if __name__ == "__main__":
    main()