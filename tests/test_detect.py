"""Tests for the detect and auto-decode module."""

import pytest
from cryptx.detect import auto_decode, detect_types, identify_hash
from cryptx.rainbow import lookup_hash


def test_auto_decode_base64():
    fmt, decoded = auto_decode("QXJpZWwgTWF6b3I=")
    assert fmt == "base64"
    assert decoded == "Ariel Mazor"


def test_auto_decode_hex():
    fmt, decoded = auto_decode("48656c6c6f")
    assert fmt == "hex"
    assert decoded == "Hello"


def test_auto_decode_binary():
    fmt, decoded = auto_decode("01001000 01101001")
    assert fmt == "binary"
    assert decoded == "Hi"


def test_detect_types_base64():
    matches = detect_types("QXJpZWwgTWF6b3I=")
    types = [m["type"] for m in matches]
    assert "Base64" in types


def test_detect_types_jwt():
    jwt = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.doNotVerify"
    matches = detect_types(jwt)
    types = [m["type"] for m in matches]
    assert any("JWT" in t for t in types)


def test_identify_hash_md5():
    matches = identify_hash("5d41402abc4b2a76b9719d911017c592")
    names = [m["name"] for m in matches]
    assert "MD5" in names
    assert any(m["mode"] == 0 for m in matches)


def test_identify_hash_sha256():
    matches = identify_hash("5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8")
    names = [m["name"] for m in matches]
    assert "SHA-256" in names
    assert any(m["mode"] == 1400 for m in matches)


def test_rainbow_lookup_known():
    # SHA-256 of "password"
    result = lookup_hash("5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8")
    assert result is not None
    plaintext, algo, mode = result
    assert plaintext == "password"
    assert algo == "SHA-256"
    assert mode == 1400


def test_rainbow_lookup_unknown():
    assert lookup_hash("00000000000000000000000000000000") is None
