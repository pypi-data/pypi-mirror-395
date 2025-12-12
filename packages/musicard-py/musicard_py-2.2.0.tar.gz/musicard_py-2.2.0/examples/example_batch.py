#!/usr/bin/env python3
"""
Batch processing example for Musicard
"""

import json

from musicard import Musicard


def main():
    # Create a music card instance
    card = Musicard()

    # Define multiple card configurations
    configs = [
        {
            "title": "Bohemian Rhapsody",
            "artist": "Queen",
            "progress": 75,
            "theme": "classic",
            "backgroundColor": "#070707",
            "progressColor": "#FF7A00",
            "filename": "queen_classic.png",
        },
        {
            "title": "Stairway to Heaven",
            "artist": "Led Zeppelin",
            "progress": 50,
            "theme": "mini",
            "paused": True,
            "filename": "zeppelin_mini.png",
        },
        {
            "title": "Hotel California",
            "artist": "Eagles",
            "progress": 90,
            "theme": "dynamic",
            "backgroundColor": "#1a1a1a",
            "filename": "eagles_dynamic.png",
        },
        {
            "title": "Imagine",
            "artist": "John Lennon",
            "progress": 30,
            "theme": "classic_pro",
            "backgroundColor": "#0a0a0a",
            "progressColor": "#00ff88",
            "filename": "lennon_classic_pro.png",
        },
    ]

    # Save configs to JSON for demonstration
    with open("batch_configs.json", "w") as f:
        json.dump(configs, f, indent=2)

    print("Generating batch of music cards...")

    # Generate all cards in batch
    images = card.batch_generate(configs, "batch_output")

    print(f"Generated {len(images)} cards successfully!")

    # Demonstrate SVG export
    print("Exporting first card as SVG...")
    card.export_svg(images[0], configs[0], "batch_output/queen_classic.svg")

    # Show cache stats
    stats = card.get_cache_stats()
    print(f"Cache stats: {stats}")


if __name__ == "__main__":
    main()
