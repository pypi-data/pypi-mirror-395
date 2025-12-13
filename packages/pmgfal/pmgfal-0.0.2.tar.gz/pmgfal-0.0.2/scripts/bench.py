#!/usr/bin/env -S uv run python
"""benchmark pmgfal on real lexicons."""

import subprocess
import tempfile
import time
from pathlib import Path


def bench_atproto():
    """benchmark against full atproto lexicons."""
    with tempfile.TemporaryDirectory() as tmp:
        # clone atproto
        print("cloning atproto lexicons...")
        subprocess.run(
            ["git", "clone", "--depth=1", "https://github.com/bluesky-social/atproto.git", tmp],
            capture_output=True,
            check=True,
        )

        lexicon_dir = Path(tmp) / "lexicons"
        output_dir = Path(tmp) / "output"
        json_files = list(lexicon_dir.rglob("*.json"))

        print(f"found {len(json_files)} lexicon files")

        # benchmark generation (cold)
        start = time.perf_counter()
        subprocess.run(
            ["uv", "run", "pmgfal", str(lexicon_dir), "-o", str(output_dir), "--no-cache"],
            check=True,
        )
        cold_time = time.perf_counter() - start

        # count output
        models_file = output_dir / "models.py"
        lines = len(models_file.read_text().splitlines()) if models_file.exists() else 0

        # benchmark cache hit
        start = time.perf_counter()
        subprocess.run(
            ["uv", "run", "pmgfal", str(lexicon_dir), "-o", str(output_dir)],
            check=True,
        )
        cache_time = time.perf_counter() - start

        print(f"\nresults:")
        print(f"  lexicons: {len(json_files)}")
        print(f"  output: {lines} lines")
        print(f"  cold generation: {cold_time:.3f}s")
        print(f"  cache hit: {cache_time:.3f}s")


if __name__ == "__main__":
    bench_atproto()
