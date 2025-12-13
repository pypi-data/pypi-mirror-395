"""pydantic model generator for atproto lexicons."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pmgfal._pmgfal import __version__, generate

__all__ = ["__version__", "generate", "main"]


def main(args: list[str] | None = None) -> int:
    """cli entry point."""
    parser = argparse.ArgumentParser(
        prog="pmgfal",
        description="pydantic model generator for atproto lexicons",
    )
    parser.add_argument(
        "lexicon_dir",
        nargs="?",
        type=Path,
        help="directory containing lexicon json files (default: ./lexicons or .)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("./generated"),
        help="output directory (default: ./generated)",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        default=None,
        help="namespace prefix filter (e.g. 'fm.plyr')",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parsed = parser.parse_args(args)

    # auto-detect lexicon directory
    if parsed.lexicon_dir is None:
        if Path("./lexicons").is_dir():
            lexicon_dir = Path("./lexicons")
        else:
            lexicon_dir = Path(".")
    else:
        lexicon_dir = parsed.lexicon_dir

    if not lexicon_dir.is_dir():
        print(f"error: not a directory: {lexicon_dir}", file=sys.stderr)
        return 1

    try:
        files = generate(
            str(lexicon_dir),
            str(parsed.output),
            parsed.prefix,
        )
        print(f"generated {len(files)} file(s):")
        for f in files:
            print(f"  {f}")
        return 0
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
