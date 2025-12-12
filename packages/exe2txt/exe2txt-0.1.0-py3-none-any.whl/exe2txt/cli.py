"""Command-line interface for exe2txt."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from exe2txt import __version__
from exe2txt.core import analyze_pe


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="exe2txt",
        description="Convert Windows EXE/DLL files into text representations for LLM prompting.",
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to the PE file (EXE or DLL) to analyze.",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output file path. If not specified, prints to stdout.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the CLI.

    Args:
        argv: Command-line arguments. If None, uses sys.argv[1:].

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        info = analyze_pe(args.file)
        output_text = info.to_text()

        if args.output:
            args.output.write_text(output_text, encoding="utf-8")
            print(f"Output written to: {args.output}", file=sys.stderr)
        else:
            print(output_text)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error analyzing PE file: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
