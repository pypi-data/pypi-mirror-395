"""
Utils
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Generator


def downloader(
    handler: Generator[tuple[int, int, bytes], None, None],
    out: Path
):
    """
    Download to 'out' with progress bar

    Args:
        handler: generator of (current, total, chunk)
        out: output file path, where will be saved content
    """
    try:
        # Animation of activity indicator
        spinner = ["-", "\\", "|", "/"]
        spin_i = 0

        start_time = time.time()
        last_update = 0

        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("wb") as f:
            for current, total, chunk in handler:
                f.write(chunk)

                # Update progress bar not very quickly
                now = time.time()
                if now - last_update < 0.05:
                    continue
                last_update = now

                percent = current * 100 / total if total else 0

                # speed
                elapsed = now - start_time
                speed = current / elapsed if elapsed > 0 else 0

                # progress bar
                bar_len = 30
                filled = int(bar_len * percent / 100)
                bar = "█" * filled + "." * (bar_len - filled)

                # rotation
                spin = spinner[spin_i]
                spin_i = (spin_i + 1) % len(spinner)

                # output
                sys.stdout.write(
                    f"\r{spin} [{bar}] {percent:6.2f}%  {speed/1024:.1f} KB/s"
                )
                sys.stdout.flush()
    except (Exception, KeyboardInterrupt):
        # Remove file
        if out.exists():
            out.unlink()
        raise

    sys.stdout.write("\nDone!\n")
