"""Pwntools-style packing and unpacking utilities.

Pack integers into byte representations and unpack bytes back to integers.
Supports 8, 16, 32, and 64-bit widths in both little-endian (default) and big-endian.
"""

import struct


# ─── Pack (int → bytes as hex string) ───────────────────────────────────────

def p8(value: int) -> str:
    """Pack an 8-bit integer (unsigned byte)."""
    return struct.pack("<B", value & 0xFF).hex()


def p16(value: int, big_endian: bool = False) -> str:
    """Pack a 16-bit integer. Little-endian by default."""
    fmt = ">H" if big_endian else "<H"
    return struct.pack(fmt, value & 0xFFFF).hex()


def p32(value: int, big_endian: bool = False) -> str:
    """Pack a 32-bit integer. Little-endian by default."""
    fmt = ">I" if big_endian else "<I"
    return struct.pack(fmt, value & 0xFFFFFFFF).hex()


def p64(value: int, big_endian: bool = False) -> str:
    """Pack a 64-bit integer. Little-endian by default."""
    fmt = ">Q" if big_endian else "<Q"
    return struct.pack(fmt, value & 0xFFFFFFFFFFFFFFFF).hex()


# ─── Unpack (hex string → int) ──────────────────────────────────────────────

def u8(data: str) -> int:
    """Unpack an 8-bit unsigned integer from hex string."""
    return struct.unpack("<B", bytes.fromhex(data.replace(" ", "")))[0]


def u16(data: str, big_endian: bool = False) -> int:
    """Unpack a 16-bit unsigned integer from hex string. Little-endian by default."""
    fmt = ">H" if big_endian else "<H"
    return struct.unpack(fmt, bytes.fromhex(data.replace(" ", "")))[0]


def u32(data: str, big_endian: bool = False) -> int:
    """Unpack a 32-bit unsigned integer from hex string. Little-endian by default."""
    fmt = ">I" if big_endian else "<I"
    return struct.unpack(fmt, bytes.fromhex(data.replace(" ", "")))[0]


def u64(data: str, big_endian: bool = False) -> int:
    """Unpack a 64-bit unsigned integer from hex string. Little-endian by default."""
    fmt = ">Q" if big_endian else "<Q"
    return struct.unpack(fmt, bytes.fromhex(data.replace(" ", "")))[0]


# ─── Formatting helpers ─────────────────────────────────────────────────────

def format_pack(hex_str: str) -> str:
    """Format a packed hex string with multiple representations."""
    byte_pairs = [hex_str[i : i + 2] for i in range(0, len(hex_str), 2)]
    python_bytes = "\\x".join([""] + byte_pairs)
    c_array = ", ".join(f"0x{b}" for b in byte_pairs)
    lines = [
        f"Hex:    {hex_str}",
        f"Bytes:  {' '.join(byte_pairs)}",
        f"Python: b'{python_bytes}'",
        f"C:      {{{c_array}}}",
    ]
    return "\n".join(lines)


def format_unpack(value: int) -> str:
    """Format an unpacked integer with multiple base representations."""
    lines = [
        f"Dec:  {value}",
        f"Hex:  {hex(value)}",
        f"Oct:  {oct(value)}",
        f"Bin:  {bin(value)}",
    ]
    return "\n".join(lines)


PACK_FUNCTIONS = {"p8": p8, "p16": p16, "p32": p32, "p64": p64}
UNPACK_FUNCTIONS = {"u8": u8, "u16": u16, "u32": u32, "u64": u64}
