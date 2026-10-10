"""Detection and identification of string types, encodings, and hash signatures."""

import base64
import html
import re
import urllib.parse

from .encoding import (
    BASE58_ALPHABET,
    MORSE_REVERSE,
    base16_decode,
    base32_decode,
    base58_decode,
    base64_decode,
    base85_decode,
    binary_decode,
    html_decode,
    morse_decode,
    octal_decode,
    url_decode,
)


# ─── Hash Signature Profiles ─────────────────────────────────────────────────

_HASH_PROFILES = [
    # (regex_pattern, [dict(name=..., mode=..., bits=...)])
    (
        r"^[0-9a-fA-F]{32}$",
        [
            {"name": "MD5", "mode": 0, "bits": 128},
            {"name": "NTLM", "mode": 1000, "bits": 128},
            {"name": "MD4", "mode": 900, "bits": 128},
        ],
    ),
    (
        r"^[0-9a-fA-F]{40}$",
        [
            {"name": "SHA-1", "mode": 100, "bits": 160},
            {"name": "MySQL 4.1+", "mode": 300, "bits": 160},
            {"name": "RIPEMD-160", "mode": 6000, "bits": 160},
        ],
    ),
    (
        r"^[0-9a-fA-F]{56}$",
        [
            {"name": "SHA-224", "mode": 1300, "bits": 224},
            {"name": "SHA3-224", "mode": 17300, "bits": 224},
        ],
    ),
    (
        r"^[0-9a-fA-F]{64}$",
        [
            {"name": "SHA-256", "mode": 1400, "bits": 256},
            {"name": "SHA3-256", "mode": 17400, "bits": 256},
            {"name": "BLAKE2b-256", "mode": 17700, "bits": 256},
        ],
    ),
    (
        r"^[0-9a-fA-F]{96}$",
        [
            {"name": "SHA-384", "mode": 10800, "bits": 384},
            {"name": "SHA3-384", "mode": 17500, "bits": 384},
        ],
    ),
    (
        r"^[0-9a-fA-F]{128}$",
        [
            {"name": "SHA-512", "mode": 1700, "bits": 512},
            {"name": "SHA3-512", "mode": 17600, "bits": 512},
            {"name": "Whirlpool", "mode": 6100, "bits": 512},
        ],
    ),
    (
        r"^[0-9a-fA-F]{8}$",
        [
            {"name": "CRC32", "mode": 11500, "bits": 32},
        ],
    ),
    (
        r"^\$1\$[a-zA-Z0-9./]{1,8}\$[a-zA-Z0-9./]{22}$",
        [
            {"name": "MD5-Crypt (Linux /etc/shadow)", "mode": 500, "bits": 128},
        ],
    ),
    (
        r"^\$5\$(rounds=\d+\$)?[a-zA-Z0-9./]{1,16}\$[a-zA-Z0-9./]{43}$",
        [
            {"name": "SHA256-Crypt (Linux /etc/shadow)", "mode": 7400, "bits": 256},
        ],
    ),
    (
        r"^\$6\$(rounds=\d+\$)?[a-zA-Z0-9./]{1,16}\$[a-zA-Z0-9./]{86}$",
        [
            {"name": "SHA512-Crypt (Linux /etc/shadow)", "mode": 1800, "bits": 512},
        ],
    ),
    (
        r"^\$2[aby]\$[0-9]{2}\$[a-zA-Z0-9./]{53}$",
        [
            {"name": "bcrypt", "mode": 3200, "bits": 184},
        ],
    ),
    (
        r"^\$argon2(i|d|id)\$v=\d+\$m=\d+,t=\d+,p=\d+\$[a-zA-Z0-9+/=]+\$[a-zA-Z0-9+/=]+$",
        [
            {"name": "Argon2", "mode": 10900, "bits": 0},
        ],
    ),
]


def identify_hash(hash_str: str) -> list[dict]:
    """Identify possible hash types from a hash string."""
    cleaned = hash_str.strip()
    results: list[dict] = []
    for pattern, candidates in _HASH_PROFILES:
        if re.match(pattern, cleaned):
            for cand in candidates:
                results.append(
                    {
                        "name": cand["name"],
                        "mode": cand["mode"],
                        "bits": cand["bits"],
                        "command": f"hashcat -m {cand['mode']} '{cleaned}' /usr/share/wordlists/rockyou.txt",
                    }
                )
    return results


def _is_mostly_printable(text: str) -> bool:
    """Return True if at least 90% of characters are printable ASCII/UTF-8."""
    if not text:
        return False
    printable = sum(1 for c in text if c.isprintable() or c in "\n\r\t")
    return (printable / len(text)) >= 0.90


# ─── Encoding Detectors ──────────────────────────────────────────────────────

def detect_types(data: str) -> list[dict]:
    """Analyze a string and detect all matching types / encodings with decoded previews."""
    cleaned = data.strip()
    matches: list[dict] = []

    # 1. JWT (JSON Web Token)
    if cleaned.count(".") == 2 and re.match(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$", cleaned):
        parts = cleaned.split(".")
        try:
            p1 = base64.urlsafe_b64decode(parts[0] + "==").decode(errors="replace")
            p2 = base64.urlsafe_b64decode(parts[1] + "==").decode(errors="replace")
            matches.append({
                "type": "JWT (JSON Web Token)",
                "confidence": "Very High",
                "preview": f"Header: {p1} | Payload: {p2}",
            })
        except Exception:
            pass

    # 2. Hashes
    hashes = identify_hash(cleaned)
    if hashes:
        names = ", ".join(f"{h['name']} (m: {h['mode']})" for h in hashes)
        matches.append({
            "type": f"Cryptographic Hash ({hashes[0]['name']})",
            "confidence": "High",
            "preview": f"Possible types: {names}",
        })

    # 3. Base64
    b64_pattern = r"^[A-Za-z0-9+/]+={0,2}$"
    if len(cleaned) >= 4 and len(cleaned) % 4 in (0, 2, 3) and re.match(b64_pattern, cleaned):
        try:
            decoded = base64_decode(cleaned)
            if _is_mostly_printable(decoded) and len(decoded) > 0 and decoded != cleaned:
                # Disqualify if it's purely a single short word that happens to have base64 chars
                is_pure_word = cleaned.isalpha() and len(cleaned) < 8
                if not is_pure_word or "=" in cleaned or not decoded.isascii():
                    matches.append({
                        "type": "Base64",
                        "confidence": "High" if "=" in cleaned or len(cleaned) >= 8 else "Medium",
                        "preview": decoded,
                    })
        except Exception:
            pass

    # 4. Hex (Base16)
    if len(cleaned) >= 2 and len(cleaned) % 2 == 0 and re.match(r"^[0-9a-fA-F]+$", cleaned):
        try:
            decoded = base16_decode(cleaned)
            if _is_mostly_printable(decoded) and decoded != cleaned:
                matches.append({
                    "type": "Hex (Base16)",
                    "confidence": "High" if not cleaned.isdigit() else "Medium",
                    "preview": decoded,
                })
        except Exception:
            pass

    # 5. Binary
    binary_tokens = cleaned.split()
    if all(re.match(r"^[01]{8}$", b) for b in binary_tokens) and len(binary_tokens) >= 1:
        try:
            decoded = binary_decode(cleaned)
            if _is_mostly_printable(decoded):
                matches.append({
                    "type": "Binary",
                    "confidence": "Very High",
                    "preview": decoded,
                })
        except Exception:
            pass
    elif re.match(r"^[01]{8,}$", cleaned) and len(cleaned) % 8 == 0:
        try:
            decoded = binary_decode(cleaned)
            if _is_mostly_printable(decoded):
                matches.append({
                    "type": "Binary (compact)",
                    "confidence": "High",
                    "preview": decoded,
                })
        except Exception:
            pass

    # 6. URL Encoded
    if "%" in cleaned and re.search(r"%[0-9a-fA-F]{2}", cleaned):
        try:
            decoded = url_decode(cleaned)
            if decoded != cleaned:
                matches.append({
                    "type": "URL Encoded",
                    "confidence": "High",
                    "preview": decoded,
                })
        except Exception:
            pass

    # 7. HTML Entities
    if "&" in cleaned and re.search(r"&[a-zA-Z]+;|&#\d+;|&#x[0-9a-fA-F]+;", cleaned):
        try:
            decoded = html_decode(cleaned)
            if decoded != cleaned:
                matches.append({
                    "type": "HTML Entities",
                    "confidence": "High",
                    "preview": decoded,
                })
        except Exception:
            pass

    # 8. Morse Code
    morse_chars = set(cleaned.replace(" ", "").replace("/", ""))
    if morse_chars.issubset({".", "-"}) and len(cleaned) >= 2:
        try:
            decoded = morse_decode(cleaned)
            if decoded and any(c.isalnum() for c in decoded):
                matches.append({
                    "type": "Morse Code",
                    "confidence": "High",
                    "preview": decoded,
                })
        except Exception:
            pass

    # 9. Octal (space separated)
    octal_tokens = cleaned.split()
    if len(octal_tokens) >= 2 and all(re.match(r"^[0-7]{3}$", o) for o in octal_tokens):
        try:
            decoded = octal_decode(cleaned)
            if _is_mostly_printable(decoded):
                matches.append({
                    "type": "Octal",
                    "confidence": "High",
                    "preview": decoded,
                })
        except Exception:
            pass

    # 10. Base32
    if len(cleaned) >= 8 and re.match(r"^[A-Z2-7=]+$", cleaned):
        try:
            decoded = base32_decode(cleaned)
            if _is_mostly_printable(decoded) and decoded != cleaned:
                matches.append({
                    "type": "Base32",
                    "confidence": "High" if "=" in cleaned else "Medium",
                    "preview": decoded,
                })
        except Exception:
            pass

    # 11. Base58 (Bitcoin alphabet)
    if len(cleaned) >= 4 and all(c in BASE58_ALPHABET for c in cleaned):
        try:
            decoded = base58_decode(cleaned)
            if _is_mostly_printable(decoded) and decoded != cleaned:
                matches.append({
                    "type": "Base58",
                    "confidence": "Medium",
                    "preview": decoded,
                })
        except Exception:
            pass

    # 12. Base85
    if len(cleaned) >= 5:
        try:
            decoded = base85_decode(cleaned)
            if _is_mostly_printable(decoded) and decoded != cleaned:
                matches.append({
                    "type": "Base85",
                    "confidence": "Medium",
                    "preview": decoded,
                })
        except Exception:
            pass

    return matches


def auto_decode(data: str) -> tuple[str, str]:
    """Auto-detect the encoding of *data* and return ``(format_name, decoded_text)``.

    Prioritizes highest confidence encodings (Base64, Hex, Binary, URL, Morse, Base32, etc.).
    Raises ValueError if no valid encoding can be identified.
    """
    cleaned = data.strip()
    detected = detect_types(cleaned)

    # Filter out hash and JWT from direct textual decoders
    text_decoders = [d for d in detected if d["type"] not in ("JWT (JSON Web Token)",) and not d["type"].startswith("Cryptographic Hash")]

    if not text_decoders:
        raise ValueError(f"Could not automatically detect encoding for: '{data[:30]}...'")

    # Pick the top match (if '=' is in Base64 or Base32, prioritize it)
    best = text_decoders[0]
    for d in text_decoders:
        if d["confidence"] == "Very High":
            best = d
            break
        if d["confidence"] == "High" and best["confidence"] != "Very High":
            best = d

    fmt = best["type"].split()[0].lower()
    return fmt, best["preview"]
