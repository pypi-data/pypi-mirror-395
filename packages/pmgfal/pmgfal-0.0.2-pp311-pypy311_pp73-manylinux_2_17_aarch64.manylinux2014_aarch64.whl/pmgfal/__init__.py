"""pydantic model generator for atproto lexicons."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from pmgfal._pmgfal import __version__, generate, hash_lexicons

__all__ = ["__version__", "generate", "get_cache_dir", "hash_lexicons", "main"]


def get_cache_dir() -> Path:
    """get the user cache directory for pmgfal."""
    if sys.platform == "darwin":
        base = Path.home() / "Library" / "Caches"
    elif sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / "pmgfal"


def is_git_url(path: str) -> bool:
    """check if path looks like a git url."""
    return path.startswith(("https://", "git@", "ssh://", "git://"))


def main(args: list[str] | None = None) -> int:
    """cli entry point."""
    parser = argparse.ArgumentParser(
        prog="pmgfal",
        description="pydantic model generator for atproto lexicons",
    )
    parser.add_argument(
        "lexicon_source",
        nargs="?",
        help="directory or git url containing lexicon json files (default: ./lexicons or .)",
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
        "--no-cache",
        action="store_true",
        help="force regeneration, ignoring cache",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parsed = parser.parse_args(args)

    temp_dir = None
    try:
        # handle git urls by cloning to temp dir
        if parsed.lexicon_source and is_git_url(parsed.lexicon_source):
            temp_dir = tempfile.mkdtemp(prefix="pmgfal-")
            print(f"cloning {parsed.lexicon_source}...")
            result = subprocess.run(
                ["git", "clone", "--depth=1", parsed.lexicon_source, temp_dir],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print(f"error: git clone failed: {result.stderr}", file=sys.stderr)
                return 1
            # look for lexicons subdir in cloned repo
            if (Path(temp_dir) / "lexicons").is_dir():
                lexicon_dir = Path(temp_dir) / "lexicons"
            else:
                lexicon_dir = Path(temp_dir)
        # auto-detect lexicon directory
        elif parsed.lexicon_source is None:
            if Path("./lexicons").is_dir():
                lexicon_dir = Path("./lexicons")
            else:
                lexicon_dir = Path(".")
        else:
            lexicon_dir = Path(parsed.lexicon_source)

        if not lexicon_dir.is_dir():
            print(f"error: not a directory: {lexicon_dir}", file=sys.stderr)
            return 1
        # compute hash of lexicons (in rust)
        lexicon_hash = hash_lexicons(str(lexicon_dir), parsed.prefix)
        cache_dir = get_cache_dir() / lexicon_hash

        # check cache
        if not parsed.no_cache and cache_dir.exists():
            # cache hit - copy cached files to output
            parsed.output.mkdir(parents=True, exist_ok=True)
            cached_files = list(cache_dir.glob("*.py"))
            for cached in cached_files:
                dest = parsed.output / cached.name
                shutil.copy2(cached, dest)
            print(f"cache hit ({lexicon_hash}) - copied {len(cached_files)} file(s):")
            for f in cached_files:
                print(f"  {parsed.output / f.name}")
            return 0

        # cache miss - generate
        files = generate(
            str(lexicon_dir),
            str(parsed.output),
            parsed.prefix,
        )

        # store in cache
        cache_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            shutil.copy2(f, cache_dir / Path(f).name)

        print(f"generated {len(files)} file(s) (cached as {lexicon_hash}):")
        for f in files:
            print(f"  {f}")
        return 0
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    finally:
        if temp_dir and Path(temp_dir).exists():
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    sys.exit(main())
