"""pydantic model generator for atproto lexicons."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from pmgfal._pmgfal import __version__, generate, hash_lexicons

__all__ = ["__version__", "generate", "get_cache_dir", "hash_lexicons", "main"]

# ansi color codes
_RESET = "\033[0m"
_DIM = "\033[2m"
_CYAN = "\033[36m"
_YELLOW = "\033[33m"
_GREEN = "\033[32m"
_RED = "\033[31m"

# git provider templates (tried in order)
GIT_PROVIDERS = [
    ("github", "https://github.com/{}.git"),
    ("tangled", "https://tangled.org/{}.git"),
]


def _supports_color() -> bool:
    """check if terminal supports color."""
    if os.environ.get("NO_COLOR"):
        return False
    if not hasattr(sys.stdout, "isatty"):
        return False
    return sys.stdout.isatty()


def _log(msg: str, color: str = "", dim: bool = False) -> None:
    """print a log message with optional color."""
    if _supports_color():
        prefix = _DIM if dim else ""
        print(f"{prefix}{color}{msg}{_RESET}")
    else:
        print(msg)


def _log_info(msg: str) -> None:
    _log(msg, _CYAN)


def _log_warn(msg: str) -> None:
    _log(msg, _YELLOW)


def _log_success(msg: str) -> None:
    _log(msg, _GREEN)


def _log_error(msg: str) -> None:
    _log(msg, _RED)


def _log_dim(msg: str) -> None:
    _log(msg, dim=True)


def get_cache_dir() -> Path:
    """get the user cache directory for pmgfal."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        # XDG standard for all unix-like systems (linux, macos, bsd)
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / "pmgfal"


def is_git_url(path: str) -> bool:
    """check if path looks like a git url."""
    return path.startswith(("https://", "git@", "ssh://", "git://"))


def is_shorthand(path: str) -> bool:
    """check if path looks like owner/repo shorthand."""
    return bool(re.match(r"^[\w.-]+/[\w.-]+$", path))


def clone_repo(source: str, dest: str) -> tuple[bool, str]:
    """clone a git repo, returns (success, url_used)."""
    if is_git_url(source):
        # full url - just try it
        _log_info(f"cloning {source}...")
        result = subprocess.run(
            ["git", "clone", "--depth=1", source, dest],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0, source

    if is_shorthand(source):
        # try providers in order
        for provider_name, url_template in GIT_PROVIDERS:
            url = url_template.format(source)
            _log_info(f"trying {provider_name}: {url}")
            result = subprocess.run(
                ["git", "clone", "--depth=1", url, dest],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return True, url
            _log_dim(f"  not found on {provider_name}")
            # clean up failed clone attempt
            if Path(dest).exists():
                shutil.rmtree(dest)

        _log_error(f"could not find '{source}' on any provider")
        _log_error("tried: " + ", ".join(name for name, _ in GIT_PROVIDERS))
        _log_error("use a full git url instead")
        return False, ""

    return False, ""


def main(args: list[str] | None = None) -> int:
    """cli entry point."""
    parser = argparse.ArgumentParser(
        prog="pmgfal",
        description="pydantic model generator for atproto lexicons",
    )
    parser.add_argument(
        "lexicon_source",
        nargs="?",
        help="directory, git url, or owner/repo shorthand (default: ./lexicons or .)",
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
    parser.add_argument(
        "--show-cache",
        action="store_true",
        help="print cache directory path and exit",
    )

    parsed = parser.parse_args(args)

    if parsed.show_cache:
        print(get_cache_dir())
        return 0

    temp_dir = None
    try:
        source = parsed.lexicon_source

        # handle git urls or shorthand by cloning to temp dir
        if source and (is_git_url(source) or is_shorthand(source)):
            temp_dir = tempfile.mkdtemp(prefix="pmgfal-")
            success, _ = clone_repo(source, temp_dir)
            if not success:
                return 1
            # look for lexicons subdir in cloned repo
            if (Path(temp_dir) / "lexicons").is_dir():
                lexicon_dir = Path(temp_dir) / "lexicons"
            else:
                lexicon_dir = Path(temp_dir)
        # auto-detect lexicon directory
        elif source is None:
            if Path("./lexicons").is_dir():
                lexicon_dir = Path("./lexicons")
            else:
                lexicon_dir = Path(".")
        else:
            lexicon_dir = Path(source)

        if not lexicon_dir.is_dir():
            _log_error(f"not a directory: {lexicon_dir}")
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
            _log_success(
                f"cache hit ({lexicon_hash}) - copied {len(cached_files)} file(s):"
            )
            for f in cached_files:
                _log_dim(f"  {parsed.output / f.name}")
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

        _log_success(f"generated {len(files)} file(s) (cached as {lexicon_hash}):")
        for f in files:
            _log_dim(f"  {f}")
        return 0
    except Exception as e:
        _log_error(f"error: {e}")
        return 1
    finally:
        if temp_dir and Path(temp_dir).exists():
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    sys.exit(main())
