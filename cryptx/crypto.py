"""Cryptographic ciphers and operations.

Supports: Caesar cipher, ROT13, ROT47, XOR, Vigenère, and Atbash.
"""

import string


# ─── Caesar Cipher ───────────────────────────────────────────────────────────

def caesar_encrypt(text: str, shift: int) -> str:
    """Encrypt text using Caesar cipher with the given shift."""
    result = []
    for c in text:
        if c in string.ascii_lowercase:
            result.append(chr((ord(c) - ord("a") + shift) % 26 + ord("a")))
        elif c in string.ascii_uppercase:
            result.append(chr((ord(c) - ord("A") + shift) % 26 + ord("A")))
        else:
            result.append(c)
    return "".join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    """Decrypt Caesar cipher text with the given shift."""
    return caesar_encrypt(text, -shift)


def caesar_bruteforce(text: str) -> list[tuple[int, str]]:
    """Try all 26 Caesar shifts and return a list of (shift, decrypted) tuples."""
    return [(i, caesar_decrypt(text, i)) for i in range(26)]


# ─── ROT13 ───────────────────────────────────────────────────────────────────

def rot13(text: str) -> str:
    """Apply ROT13 cipher (symmetric — encrypt and decrypt are identical)."""
    return caesar_encrypt(text, 13)


# ─── ROT47 ───────────────────────────────────────────────────────────────────

def rot47(text: str) -> str:
    """Apply ROT47 cipher (rotates printable ASCII 33–126)."""
    result = []
    for c in text:
        o = ord(c)
        if 33 <= o <= 126:
            result.append(chr(33 + (o - 33 + 47) % 94))
        else:
            result.append(c)
    return "".join(result)


# ─── XOR ─────────────────────────────────────────────────────────────────────

def xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR data with a repeating key."""
    if not key:
        raise ValueError("Key cannot be empty")
    return bytes(d ^ key[i % len(key)] for i, d in enumerate(data))


def xor_encrypt(text: str, key: str) -> str:
    """XOR-encrypt text with the given key. Returns hex string."""
    return xor_bytes(text.encode(), key.encode()).hex()


def xor_decrypt_hex(hex_data: str, key: str) -> str:
    """XOR-decrypt a hex string with the given key. Returns plaintext."""
    data = bytes.fromhex(hex_data)
    return xor_bytes(data, key.encode()).decode(errors="replace")


def xor_single_byte_bruteforce(hex_data: str) -> list[tuple[int, str]]:
    """Brute-force single-byte XOR and return all (key_byte, plaintext) results."""
    data = bytes.fromhex(hex_data)
    results = []
    for key_byte in range(256):
        try:
            plaintext = bytes(b ^ key_byte for b in data).decode()
            if plaintext.isprintable() or all(c in string.printable for c in plaintext):
                results.append((key_byte, plaintext))
        except (UnicodeDecodeError, ValueError):
            continue
    return results


# ─── Vigenère Cipher ─────────────────────────────────────────────────────────

def vigenere_encrypt(text: str, key: str) -> str:
    """Encrypt text using the Vigenère cipher."""
    if not key:
        raise ValueError("Key cannot be empty")
    result = []
    key_upper = key.upper()
    ki = 0
    for c in text:
        if c in string.ascii_lowercase:
            shift = ord(key_upper[ki % len(key_upper)]) - ord("A")
            result.append(chr((ord(c) - ord("a") + shift) % 26 + ord("a")))
            ki += 1
        elif c in string.ascii_uppercase:
            shift = ord(key_upper[ki % len(key_upper)]) - ord("A")
            result.append(chr((ord(c) - ord("A") + shift) % 26 + ord("A")))
            ki += 1
        else:
            result.append(c)
    return "".join(result)


def vigenere_decrypt(text: str, key: str) -> str:
    """Decrypt Vigenère cipher text."""
    if not key:
        raise ValueError("Key cannot be empty")
    result = []
    key_upper = key.upper()
    ki = 0
    for c in text:
        if c in string.ascii_lowercase:
            shift = ord(key_upper[ki % len(key_upper)]) - ord("A")
            result.append(chr((ord(c) - ord("a") - shift) % 26 + ord("a")))
            ki += 1
        elif c in string.ascii_uppercase:
            shift = ord(key_upper[ki % len(key_upper)]) - ord("A")
            result.append(chr((ord(c) - ord("A") - shift) % 26 + ord("A")))
            ki += 1
        else:
            result.append(c)
    return "".join(result)


# ─── Atbash Cipher ──────────────────────────────────────────────────────────

def atbash(text: str) -> str:
    """Apply Atbash cipher (A↔Z, B↔Y, ... symmetric)."""
    result = []
    for c in text:
        if c in string.ascii_lowercase:
            result.append(chr(ord("z") - (ord(c) - ord("a"))))
        elif c in string.ascii_uppercase:
            result.append(chr(ord("Z") - (ord(c) - ord("A"))))
        else:
            result.append(c)
    return "".join(result)
