"""
Command-line interface for AI Music Remixer
"""

import argparse
import sys
from .remixer import ai_remix, ai_remix_beatsync


def main():
    parser = argparse.ArgumentParser(
        description="AI Music Remixer - Intelligent music remixing with optional neural transitions"
    )
    parser.add_argument(
        "input_file",
        help="Input audio file to remix"
    )
    parser.add_argument(
        "-o", "--output",
        default="remix_output.wav",
        help="Output file path (default: remix_output.wav)"
    )
    parser.add_argument(
        "--beats",
        action="store_true",
        help="Enable beat-synchronized remixing"
    )
    parser.add_argument(
        "--bpm",
        type=float,
        help="Beats per minute (auto-detected if not specified)"
    )
    parser.add_argument(
        "--style",
        choices=["default", "aggressive", "smooth"],
        default="default",
        help="Remix style (default: default)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.beats:
            ai_remix_beatsync(args.input_file, args.output, beats_per_minute=args.bpm)
        else:
            ai_remix(args.input_file, args.output, style=args.style)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

