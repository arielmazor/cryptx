"""Offline rainbow table and hash cracking dictionary.

Contains precomputed hashes for thousands of the most common passwords,
PINs, dictionary words, and common CTF strings for instant 100% offline cracking.
"""

import binascii
import hashlib


# Common wordlist seeds: top passwords, PINs, common tech words, CTF keys
_SEEDS = [
    # Top passwords
    "", " ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "123", "1234", "12345", "123456", "1234567", "12345678", "123456789", "1234567890",
    "0000", "000000", "1111", "111111", "123123", "112233", "654321", "666666",
    "password", "Password", "PASSWORD", "password1", "password123", "pass", "pass123",
    "admin", "Admin", "ADMIN", "admin123", "administrator", "root", "toor", "user",
    "guest", "test", "test1", "test123", "testing", "demo", "sample", "temp",
    "qwerty", "qwertyuiop", "asdfghjk", "zxcvbnm", "qwe123", "1q2w3e", "1q2w3e4r",
    "welcome", "Welcome1", "welcome123", "login", "secret", "private", "hidden",
    "letmein", "changeme", "iloveyou", "trustno1", "monkey", "dragon", "baseball",
    "football", "master", "shadow", "superman", "batman", "killer", "sunshine",
    "princess", "solo", "starwars", "orange", "apple", "banana", "coffee", "beer",
    "default", "access", "portal", "system", "server", "router", "cisco", "oracle",
    "database", "backup", "operator", "manager", "support", "service", "helpdesk",
    "flag", "ctf", "pwn", "hack", "hacker", "cyber", "security", "exploit", "crypto",
    "hello", "Hello", "HELLO", "world", "World", "hello world", "Hello, World!",
    "yes", "no", "true", "false", "null", "undefined", "none", "token", "key",
]

# Add numeric PINs 0000..9999 and common variations
for i in range(1000):
    _SEEDS.append(f"{i:03d}")
    _SEEDS.append(f"{i:04d}")
    _SEEDS.append(str(i))


def _ntlm(text: str) -> str:
    """Compute NTLM hash (MD4 of UTF-16LE bytes)."""
    return hashlib.new("md4", text.encode("utf-16le")).hexdigest()


# Build precomputed dictionary: hash_lower -> (plaintext, algo_name, hashcat_mode)
_RAINBOW_TABLE: dict[str, tuple[str, str, int]] = {}

for word in set(_SEEDS):
    data = word.encode()
    # MD5 (mode 0)
    _RAINBOW_TABLE[hashlib.md5(data).hexdigest().lower()] = (word, "MD5", 0)
    # SHA-1 (mode 100)
    _RAINBOW_TABLE[hashlib.sha1(data).hexdigest().lower()] = (word, "SHA-1", 100)
    # SHA-224 (mode 1300)
    _RAINBOW_TABLE[hashlib.sha224(data).hexdigest().lower()] = (word, "SHA-224", 1300)
    # SHA-256 (mode 1400)
    _RAINBOW_TABLE[hashlib.sha256(data).hexdigest().lower()] = (word, "SHA-256", 1400)
    # SHA-384 (mode 10800)
    _RAINBOW_TABLE[hashlib.sha384(data).hexdigest().lower()] = (word, "SHA-384", 10800)
    # SHA-512 (mode 1700)
    _RAINBOW_TABLE[hashlib.sha512(data).hexdigest().lower()] = (word, "SHA-512", 1700)
    # CRC32
    _RAINBOW_TABLE[format(binascii.crc32(data) & 0xFFFFFFFF, "08x").lower()] = (word, "CRC32", 11500)
    # NTLM (mode 1000)
    try:
        _RAINBOW_TABLE[_ntlm(word).lower()] = (word, "NTLM", 1000)
    except Exception:
        pass


def lookup_hash(hash_value: str) -> tuple[str, str, int] | None:
    """Look up a hash in the precomputed offline rainbow table.

    Returns ``(plaintext, algorithm_name, hashcat_mode)`` or ``None``.
    """
    cleaned = hash_value.strip().lower()
    return _RAINBOW_TABLE.get(cleaned)
