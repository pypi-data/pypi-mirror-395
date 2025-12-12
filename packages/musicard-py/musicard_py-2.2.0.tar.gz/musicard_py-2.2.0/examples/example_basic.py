#!/usr/bin/env python3
"""
Example usage of Musicard
"""

from musicard import Musicard


def main():
    # Create a music card instance
    card = Musicard()

    # Generate classic theme
    print("Generating classic theme...")
    image = card.generate_card(
        title="Bohemian Rhapsody",
        artist="Queen",
        progress=75,
        theme="classic",
        backgroundColor="#070707",
        progressColor="#FF7A00",
    )
    card.save(image, "example_classic.png")

    # Generate mini theme
    print("Generating mini theme...")
    mini_image = card.generate_card(
        title="Stairway to Heaven",
        artist="Led Zeppelin",
        progress=50,
        theme="mini",
        paused=True,
    )
    card.save(mini_image, "example_mini.png")

    # Generate dynamic theme with background image
    print("Generating dynamic theme...")
    dynamic_image = card.generate_card(
        title="Hotel California",
        artist="Eagles",
        progress=90,
        theme="dynamic",
        backgroundImage="https://example.com/bg.jpg",  # Replace with real URL
        imageDarkness=60,
    )
    card.save(dynamic_image, "example_dynamic.png")

    print("Examples generated successfully!")


if __name__ == "__main__":
    main()
