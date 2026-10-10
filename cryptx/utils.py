"""Shared utilities for Sheff."""

import math
import sys
from collections import Counter


def get_input(text: str | None) -> str:
    """Return *text* if given, otherwise read from stdin.

    Raises ``SystemExit`` with an error message when there is no input
    and stdin is a terminal (i.e. nothing was piped in).
    """
    if text:
        return text
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    raise SystemExit("Error: no input provided. Pass as argument or pipe via stdin.")


def parse_int(value: str) -> int:
    """Parse an integer from a string, auto-detecting base (0x, 0o, 0b, or decimal)."""
    value = value.strip()
    return int(value, 0)


def entropy(data: str) -> float:
    """Calculate Shannon entropy of a string (bits per character)."""
    if not data:
        return 0.0
    counts = Counter(data)
    length = len(data)
    return -sum(
        (count / length) * math.log2(count / length)
        for count in counts.values()
    )


def char_info(char: str) -> dict:
    """Return detailed information about a single character."""
    o = ord(char)
    return {
        "char": char,
        "decimal": o,
        "hex": hex(o),
        "octal": oct(o),
        "binary": bin(o),
        "name": _safe_unicodename(char),
    }


def _safe_unicodename(char: str) -> str:
    """Return the Unicode name of *char*, or 'UNKNOWN' on failure."""
    import unicodedata

    try:
        return unicodedata.name(char)
    except ValueError:
        return "UNKNOWN"


def string_info(data: str) -> str:
    """Return a summary of useful properties about a string."""
    raw = data.encode()
    lines = [
        f"String:   {data!r}",
        f"Length:   {len(data)} chars, {len(raw)} bytes",
        f"Entropy:  {entropy(data):.4f} bits/char",
        f"Hex:      {raw.hex()}",
        f"Decimal:  {' '.join(str(b) for b in raw)}",
        f"Binary:   {' '.join(format(b, '08b') for b in raw)}",
    ]
    return "\n".join(lines)
