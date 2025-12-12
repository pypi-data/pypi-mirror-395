#!/usr/bin/env python3
"""
Musicard CLI tool for generating music cards from JSON or command line arguments.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from musicard import Musicard


def load_config(json_path: Path) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    with open(json_path, "r") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Generate music card images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  musicard generate --title "Song Title" --artist "Artist" --theme classic --output card.png
  musicard generate --config song.json --output card.png
  musicard themes  # List available themes
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a music card")
    generate_parser.add_argument("--title", "-t", help="Song title")
    generate_parser.add_argument("--artist", "-a", help="Artist name")
    generate_parser.add_argument("--thumbnail", help="Thumbnail URL or path")
    generate_parser.add_argument(
        "--progress", "-p", type=float, default=0, help="Progress (0-100)"
    )
    generate_parser.add_argument("--theme", default="classic", help="Theme name")
    generate_parser.add_argument("--config", "-c", type=Path, help="JSON config file")
    generate_parser.add_argument(
        "--output", "-o", required=True, help="Output file path"
    )
    generate_parser.add_argument(
        "--format",
        choices=["png", "jpg", "jpeg", "svg"],
        default="png",
        help="Output format",
    )
    generate_parser.add_argument("--width", type=int, default=1200, help="Image width")
    generate_parser.add_argument("--height", type=int, default=400, help="Image height")

    # Theme-specific options
    generate_parser.add_argument("--background-color", help="Background color")
    generate_parser.add_argument("--progress-color", help="Progress bar color")
    generate_parser.add_argument("--name-color", help="Title color")
    generate_parser.add_argument("--author-color", help="Artist color")

    # Batch command
    batch_parser = subparsers.add_parser(
        "batch", help="Generate multiple cards from JSON array"
    )
    batch_parser.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="JSON file with card configurations",
    )
    batch_parser.add_argument(
        "--output-dir", "-o", default="output", help="Output directory"
    )
    batch_parser.add_argument(
        "--format", choices=["png", "jpg", "jpeg"], default="png", help="Output format"
    )

    # Themes command
    subparsers.add_parser("themes", help="List available themes")

    # Logo commands
    logo_parser = subparsers.add_parser("logo", help="Logo management")
    logo_subparsers = logo_parser.add_subparsers(dest="logo_command")
    logo_set_parser = logo_subparsers.add_parser("set", help="Set logo")
    logo_set_parser.add_argument("logo", help="Logo path or URL")
    logo_auto_parser = logo_subparsers.add_parser("auto", help="Enable/disable auto logo")
    logo_auto_parser.add_argument("state", choices=["on", "off"], help="Auto logo state")

    # Profile commands
    profile_parser = subparsers.add_parser("profile", help="Profile management")
    profile_subparsers = profile_parser.add_subparsers(dest="profile_command")
    profile_use_parser = profile_subparsers.add_parser("use", help="Use profile")
    profile_use_parser.add_argument("name", help="Profile name")

    # Queue commands
    queue_parser = subparsers.add_parser("queue", help="Batch queue management")
    queue_subparsers = queue_parser.add_subparsers(dest="queue_command")
    queue_add_parser = queue_subparsers.add_parser("add", help="Add to queue")
    queue_add_parser.add_argument("file", help="JSON file with configurations")
    queue_start_parser = queue_subparsers.add_parser("start", help="Start processing queue")

    # Preview command
    preview_parser = subparsers.add_parser("preview", help="Preview card")
    preview_parser.add_argument("--live", action="store_true", help="Live terminal preview")
    preview_parser.add_argument("--title", "-t", help="Song title")
    preview_parser.add_argument("--artist", "-a", help="Artist name")
    preview_parser.add_argument("--theme", default="classic", help="Theme name")

    # Render command
    render_parser = subparsers.add_parser("render", help="Render with options")
    render_parser.add_argument("--dry-run", action="store_true", help="Dry run")
    render_parser.add_argument("--config", "-c", type=Path, help="JSON config file")
    render_parser.add_argument("--output", "-o", help="Output file")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export in high quality")
    export_parser.add_argument("quality", choices=["8k", "high"], help="Export quality")
    export_parser.add_argument("--config", "-c", type=Path, help="JSON config file")
    export_parser.add_argument("--output", "-o", required=True, help="Output file")

    args = parser.parse_args()

    if args.command == "themes":
        card = Musicard()
        themes = card.get_available_themes()
        print("Available themes:")
        for theme in themes:
            print(f"  - {theme}")
        return

    if args.command == "generate":
        # Load config from file or arguments
        config = {}
        if args.config:
            config = load_config(args.config)

        # Override with command line args
        if args.title:
            config["title"] = args.title
        if args.artist:
            config["artist"] = args.artist
        if args.thumbnail:
            config["thumbnailImage"] = args.thumbnail
        if args.progress is not None:
            config["progress"] = args.progress
        if args.theme:
            config["theme"] = args.theme
        if args.background_color:
            config["backgroundColor"] = args.background_color
        if args.progress_color:
            config["progressColor"] = args.progress_color
        if args.name_color:
            config["nameColor"] = args.name_color
        if args.author_color:
            config["authorColor"] = args.author_color

        # Validate required fields
        if not config.get("title"):
            print("Error: Title is required", file=sys.stderr)
            sys.exit(1)
        if not config.get("artist"):
            print("Error: Artist is required", file=sys.stderr)
            sys.exit(1)

        try:
            # Generate card
            card = Musicard(args.width, args.height)
            image = card.generate_card(**config)

            if args.format == "svg":
                card.export_svg(image, config, args.output)
                print(f"SVG music card saved to {args.output}")
            else:
                card.save(image, args.output)
                print(f"Music card saved to {args.output}")

        except Exception as e:
            print(f"Error generating card: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "batch":
        try:
            # Load batch configurations
            configs = load_config(args.input)
            if not isinstance(configs, list):
                print("Error: Batch input must be a JSON array", file=sys.stderr)
                sys.exit(1)

            card = Musicard()
            images = card.batch_generate(configs, args.output_dir)
            print(f"Generated {len(images)} cards in {args.output_dir}")

        except Exception as e:
            print(f"Error in batch generation: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "logo":
        card = Musicard()
        if args.logo_command == "set":
            card.set_song_logo(args.logo)
            print(f"Logo set to {args.logo}")
        elif args.logo_command == "auto":
            enabled = args.state == "on"
            card.enable_auto_logo(enabled)
            print(f"Auto logo {'enabled' if enabled else 'disabled'}")

    elif args.command == "profile":
        if args.profile_command == "use":
            card = Musicard()
            card.use_profile(args.name)
            print(f"Using profile {args.name}")

    elif args.command == "queue":
        if args.queue_command == "add":
            # TODO: Implement queue
            print(f"Added {args.file} to queue")
        elif args.queue_command == "start":
            # TODO: Implement queue processing
            print("Starting queue processing")

    elif args.command == "preview":
        # Load config
        config = {}
        if args.title:
            config["title"] = args.title
        if args.artist:
            config["artist"] = args.artist
        if args.theme:
            config["theme"] = args.theme

        if args.live:
            # Simple ASCII preview
            print("ASCII Preview:")
            print("+-------------------+")
            print("|                   |")
            print("|     MUSIC CARD    |")
            print("|                   |")
            print("+-------------------+")
        else:
            card = Musicard()
            image = card.generate_card(**config)
            # For preview, just generate without saving
            print("Preview generated")

    elif args.command == "render":
        if args.dry_run:
            print("Dry run: would render card")
        else:
            config = load_config(args.config) if args.config else {}
            card = Musicard()
            image = card.generate_card(**config)
            if args.output:
                card.save(image, args.output)
                print(f"Rendered to {args.output}")

    elif args.command == "export":
        config = load_config(args.config) if args.config else {}
        config["exportQuality"] = args.quality
        card = Musicard()
        image = card.generate_card(**config)
        card.save(image, args.output)
        print(f"Exported {args.quality} quality to {args.output}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
