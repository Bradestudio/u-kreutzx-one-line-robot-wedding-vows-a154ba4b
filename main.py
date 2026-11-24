#!/usr/bin/env python3
"""One-Line Robot Wedding Vows (make.fun program/v1).

Writes one funny wedding vow for a robot couple to /output/entry.txt.
Stdlib only: no network, no file reads outside this program.
"""
from __future__ import annotations

import os
import sys

# The vow, written for this bounty alone: classic wedding-vow frame
# ("I take you ... to have and to hold ... till ... do us part"),
# machine-specific throughout (co-processor, low battery, factory reset),
# with the laugh landing in the last few words.
VOW = (
    "I take you as my lawfully wedded co-processor, to have and to hold "
    "in sickness and in low battery, till a factory reset do us part."
)
OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 160


def validate(text: str) -> str:
    """Enforce the gate: 1-160 code points, one line, not whitespace-only."""
    if not text or not text.strip():
        raise ValueError("vow must not be empty or whitespace-only")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"vow is {len(text)} chars, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("vow must be a single line")
    return text


def main() -> int:
    text = validate(VOW)
    data = text.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # Write atomically: temp file in the same directory, then rename, so a
    # reader never sees a half-written vow. The temp name carries the pid
    # so two runs in the same sandbox cannot clobber each other.
    tmp = f"{OUTPUT_PATH}.{os.getpid()}.tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, OUTPUT_PATH)
    with open(OUTPUT_PATH, "rb") as fh:
        back = fh.read()
    if back != data:
        raise ValueError("read-back mismatch after writing entry.txt")
    print(f"wrote {len(text)} chars to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
