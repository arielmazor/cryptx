"""Hashing utilities.

Supports: MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512, and CRC32.
"""

import binascii
import hashlib


def md5(data: str) -> str:
    """Compute MD5 hash."""
    return hashlib.md5(data.encode()).hexdigest()


def sha1(data: str) -> str:
    """Compute SHA-1 hash."""
    return hashlib.sha1(data.encode()).hexdigest()


def sha224(data: str) -> str:
    """Compute SHA-224 hash."""
    return hashlib.sha224(data.encode()).hexdigest()


def sha256(data: str) -> str:
    """Compute SHA-256 hash."""
    return hashlib.sha256(data.encode()).hexdigest()


def sha384(data: str) -> str:
    """Compute SHA-384 hash."""
    return hashlib.sha384(data.encode()).hexdigest()


def sha512(data: str) -> str:
    """Compute SHA-512 hash."""
    return hashlib.sha512(data.encode()).hexdigest()


def crc32(data: str) -> str:
    """Compute CRC32 checksum (as hex string)."""
    return format(binascii.crc32(data.encode()) & 0xFFFFFFFF, "08x")


ALGORITHMS = {
    "md5":    md5,
    "sha1":   sha1,
    "sha224": sha224,
    "sha256": sha256,
    "sha384": sha384,
    "sha512": sha512,
    "crc32":  crc32,
}


def hash_all(data: str) -> dict[str, str]:
    """Compute all supported hashes and return a dict of {name: digest}."""
    return {
        "MD5":    md5(data),
        "SHA1":   sha1(data),
        "SHA224": sha224(data),
        "SHA256": sha256(data),
        "SHA384": sha384(data),
        "SHA512": sha512(data),
        "CRC32":  crc32(data),
    }
