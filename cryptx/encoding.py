"""Encoding and decoding utilities.

Supports: Base16 (hex), Base32, Base58, Base64, Base85,
URL encoding, HTML entities, binary, octal, morse code, and decimal.
"""

import base64 as _base64
import html as _html
import urllib.parse

# ─── Base58 (Bitcoin alphabet) ───────────────────────────────────────────────

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

# ─── Morse Code ──────────────────────────────────────────────────────────────

MORSE_TABLE = {
    "A": ".-",    "B": "-...",  "C": "-.-.",  "D": "-..",   "E": ".",
    "F": "..-.",  "G": "--.",   "H": "....",  "I": "..",    "J": ".---",
    "K": "-.-",   "L": ".-..", "M": "--",    "N": "-.",    "O": "---",
    "P": ".--.",  "Q": "--.-",  "R": ".-.",   "S": "...",   "T": "-",
    "U": "..-",   "V": "...-",  "W": ".--",   "X": "-..-",  "Y": "-.--",
    "Z": "--..",  "0": "-----", "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..",
    "9": "----.", ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.",
    "!": "-.-.--", "/": "-..-.", "(": "-.--.", ")": "-.--.-", "&": ".-...",
    ":": "---...", ";": "-.-.-.", "=": "-...-", "+": ".-.-.", "-": "-....-",
    "_": "..--.-", '"': ".-..-.", "$": "...-..-", "@": ".--.-.", " ": "/",
}

MORSE_REVERSE = {v: k for k, v in MORSE_TABLE.items()}


# ─── Base16 / Hex ────────────────────────────────────────────────────────────

def base16_encode(data: str) -> str:
    """Encode string to hexadecimal."""
    return data.encode().hex()


def base16_decode(data: str) -> str:
    """Decode hexadecimal string."""
    return bytes.fromhex(data).decode()


# ─── Base32 ──────────────────────────────────────────────────────────────────

def base32_encode(data: str) -> str:
    """Encode string to Base32."""
    return _base64.b32encode(data.encode()).decode()


def base32_decode(data: str) -> str:
    """Decode Base32 string."""
    # Add padding if necessary
    missing = len(data) % 8
    if missing:
        data += "=" * (8 - missing)
    return _base64.b32decode(data).decode()


# ─── Base58 ──────────────────────────────────────────────────────────────────

def base58_encode(data: str) -> str:
    """Encode string to Base58 (Bitcoin alphabet)."""
    raw = data.encode()
    n = int.from_bytes(raw, "big") if raw else 0
    result = ""
    while n > 0:
        n, remainder = divmod(n, 58)
        result = BASE58_ALPHABET[remainder] + result
    # Preserve leading zero bytes
    for byte in raw:
        if byte == 0:
            result = "1" + result
        else:
            break
    return result or "1"


def base58_decode(data: str) -> str:
    """Decode Base58 (Bitcoin alphabet) string."""
    n = 0
    for char in data:
        idx = BASE58_ALPHABET.index(char)
        n = n * 58 + idx
    # Count leading '1's (zero bytes)
    pad = 0
    for char in data:
        if char == "1":
            pad += 1
        else:
            break
    if n > 0:
        result = n.to_bytes((n.bit_length() + 7) // 8, "big")
    else:
        result = b""
    return (b"\x00" * pad + result).decode()


# ─── Base64 ──────────────────────────────────────────────────────────────────

def base64_encode(data: str) -> str:
    """Encode string to Base64."""
    return _base64.b64encode(data.encode()).decode()


def base64_decode(data: str) -> str:
    """Decode Base64 string."""
    # Add padding if necessary
    missing = len(data) % 4
    if missing:
        data += "=" * (4 - missing)
    return _base64.b64decode(data).decode()


# ─── Base85 (ASCII85) ───────────────────────────────────────────────────────

def base85_encode(data: str) -> str:
    """Encode string to Base85 (ASCII85)."""
    return _base64.b85encode(data.encode()).decode()


def base85_decode(data: str) -> str:
    """Decode Base85 (ASCII85) string."""
    return _base64.b85decode(data.encode()).decode()


# ─── URL Encoding ────────────────────────────────────────────────────────────

def url_encode(data: str) -> str:
    """URL-encode a string (percent encoding)."""
    return urllib.parse.quote(data, safe="")


def url_decode(data: str) -> str:
    """Decode a URL-encoded string."""
    return urllib.parse.unquote(data)


# ─── HTML Entities ───────────────────────────────────────────────────────────

def html_encode(data: str) -> str:
    """Encode special characters as HTML entities."""
    return _html.escape(data)


def html_decode(data: str) -> str:
    """Decode HTML entities back to characters."""
    return _html.unescape(data)


# ─── Binary ──────────────────────────────────────────────────────────────────

def binary_encode(data: str) -> str:
    """Encode string to space-separated binary octets."""
    return " ".join(format(b, "08b") for b in data.encode())


def binary_decode(data: str) -> str:
    """Decode space-separated binary octets to string."""
    bits = data.replace(" ", "")
    return bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8)).decode()


# ─── Octal ───────────────────────────────────────────────────────────────────

def octal_encode(data: str) -> str:
    """Encode string to space-separated octal values."""
    return " ".join(format(b, "03o") for b in data.encode())


def octal_decode(data: str) -> str:
    """Decode space-separated octal values to string."""
    return bytes(int(o, 8) for o in data.split()).decode()


# ─── Morse Code ──────────────────────────────────────────────────────────────

def morse_encode(data: str) -> str:
    """Encode string to Morse code (/ separates words)."""
    return " ".join(MORSE_TABLE.get(c.upper(), c) for c in data)


def morse_decode(data: str) -> str:
    """Decode Morse code to string (/ separates words)."""
    return "".join(MORSE_REVERSE.get(code, code) for code in data.split(" "))


# ─── Decimal (ASCII values) ─────────────────────────────────────────────────

def decimal_encode(data: str) -> str:
    """Encode string to space-separated decimal byte values."""
    return " ".join(str(b) for b in data.encode())


def decimal_decode(data: str) -> str:
    """Decode space-separated decimal byte values to string."""
    return bytes(int(d) for d in data.split()).decode()


# ─── Classical Ciphers as Encodings ──────────────────────────────────────────

from .crypto import atbash as _atbash, rot13 as _rot13, rot47 as _rot47


# ─── Registry ────────────────────────────────────────────────────────────────

ENCODINGS = {
    "base16":  (base16_encode,  base16_decode),
    "hex":     (base16_encode,  base16_decode),
    "base32":  (base32_encode,  base32_decode),
    "base58":  (base58_encode,  base58_decode),
    "base64":  (base64_encode,  base64_decode),
    "b64":     (base64_encode,  base64_decode),
    "base85":  (base85_encode,  base85_decode),
    "ascii85": (base85_encode,  base85_decode),
    "url":     (url_encode,     url_decode),
    "html":    (html_encode,    html_decode),
    "binary":  (binary_encode,  binary_decode),
    "bin":     (binary_encode,  binary_decode),
    "octal":   (octal_encode,   octal_decode),
    "oct":     (octal_encode,   octal_decode),
    "morse":   (morse_encode,   morse_decode),
    "decimal": (decimal_encode, decimal_decode),
    "dec":     (decimal_encode, decimal_decode),
    "rot13":   (_rot13,         _rot13),
    "rot47":   (_rot47,         _rot47),
    "atbash":  (_atbash,        _atbash),
}
