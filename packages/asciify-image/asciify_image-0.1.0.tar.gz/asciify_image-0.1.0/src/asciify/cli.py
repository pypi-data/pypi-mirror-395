"""Command-line interface for asciify."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from asciify.charsets import CHARSETS
from asciify.converter import ASCIIArtConverter


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="asciify",
        description="Convert images to ASCII art",
    )
    parser.add_argument(
        "image",
        type=Path,
        help="Path to the image file",
    )
    parser.add_argument(
        "-W",
        "--width",
        type=int,
        help="Output width in characters",
    )
    parser.add_argument(
        "-H",
        "--height",
        type=int,
        help="Output height in characters",
    )
    parser.add_argument(
        "-c",
        "--charset",
        choices=list(CHARSETS.keys()),
        default="simple",
        help="Character set to use (default: simple)",
    )
    parser.add_argument(
        "--color",
        action="store_true",
        help="Enable colored output",
    )
    parser.add_argument(
        "--dither",
        action="store_true",
        help="Enable Floyd-Steinberg dithering",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Invert the image colors",
    )
    parser.add_argument(
        "-b",
        "--brightness",
        type=float,
        default=1.0,
        help="Brightness adjustment (0.0-2.0, default: 1.0)",
    )
    parser.add_argument(
        "--contrast",
        type=float,
        default=1.0,
        help="Contrast adjustment (0.0-2.0, default: 1.0)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Save output to file",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    converter = ASCIIArtConverter(
        charset=args.charset,
        colored=args.color,
        dither=args.dither,
    )

    try:
        ascii_art = converter.convert(
            args.image,
            width=args.width,
            height=args.height,
            invert=args.invert,
            brightness=args.brightness,
            contrast=args.contrast,
        )
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.output:
        try:
            args.output.write_text(ascii_art, encoding="utf-8")
            print(f"ASCII art saved to {args.output}")
        except OSError as e:
            print(f"Error saving file: {e}", file=sys.stderr)
            return 1
    else:
        print(ascii_art)

    return 0


if __name__ == "__main__":
    sys.exit(main())
