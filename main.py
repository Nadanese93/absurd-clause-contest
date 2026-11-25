#!/usr/bin/env python3
"""Generate the absurd-clause entry for the make.fun bounty.

Writes the single-sentence entry to <MAKEFUN_OUTPUT_DIR>/entry.txt
as UTF-8 bytes with no trailing newline. Deterministic: the same
bytes are produced on every run.
"""

import os
from pathlib import Path

ENTRY_TEXT = (
    "In the event of a power cut, the User shall continue to use the "
    "Service by candlelight and shall not hold the Company liable for wax."
)

MAX_LENGTH = 200


class BlankError(ValueError):
    """Entry text is empty or whitespace-only."""


class MultiLineError(ValueError):
    """Entry text spans more than one line."""


class LengthError(ValueError):
    """Entry text exceeds the maximum length."""


class VerificationError(RuntimeError):
    """Re-read entry.txt bytes differ from the expected text."""


def validate(text):
    """Raise if the entry text breaks the contest gate."""
    if not text or not text.strip():
        raise BlankError("entry text is blank or whitespace-only")
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry text must be a single line")
    if len(text) > MAX_LENGTH:
        raise LengthError(
            "entry text got %d chars, exceeds max %d" % (len(text), MAX_LENGTH)
        )


def verify_written(path, expected_text):
    """Re-read the written file and raise if the bytes differ."""
    data = path.read_bytes()
    if data != expected_text.encode("utf-8"):
        raise VerificationError("written entry.txt bytes differ from expected text")


def main():
    out_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    validate(ENTRY_TEXT)
    out_path = Path(out_dir) / "entry.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(ENTRY_TEXT.encode("utf-8"))
    verify_written(out_path, ENTRY_TEXT)


if __name__ == "__main__":
    main()
