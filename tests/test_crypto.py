"""Tests for the crypto module."""

from cryptx.crypto import (
    caesar_encrypt, caesar_decrypt, caesar_bruteforce,
    rot13, rot47,
    xor_encrypt, xor_decrypt_hex,
    vigenere_encrypt, vigenere_decrypt,
    atbash,
)


def test_caesar_encrypt():
    assert caesar_encrypt("abc", 3) == "def"
    assert caesar_encrypt("xyz", 3) == "abc"
    assert caesar_encrypt("Hello, World!", 13) == "Uryyb, Jbeyq!"


def test_caesar_decrypt():
    assert caesar_decrypt("def", 3) == "abc"
    assert caesar_decrypt("Uryyb, Jbeyq!", 13) == "Hello, World!"


def test_caesar_roundtrip():
    for shift in range(26):
        assert caesar_decrypt(caesar_encrypt("Test 123!", shift), shift) == "Test 123!"


def test_caesar_bruteforce():
    results = caesar_bruteforce("Khoor")
    shifts = dict(results)
    assert shifts[3] == "Hello"


def test_rot13():
    assert rot13("Hello") == "Uryyb"
    assert rot13(rot13("Hello")) == "Hello"  # symmetric


def test_rot47():
    assert rot47(rot47("Hello, World!")) == "Hello, World!"  # symmetric
    assert rot47("Hello") == "w6==@"


def test_xor_roundtrip():
    encrypted = xor_encrypt("Hello", "key")
    decrypted = xor_decrypt_hex(encrypted, "key")
    assert decrypted == "Hello"


def test_vigenere_roundtrip():
    cipher = vigenere_encrypt("Hello, World!", "SECRET")
    plain = vigenere_decrypt(cipher, "SECRET")
    assert plain == "Hello, World!"


def test_vigenere_known():
    assert vigenere_encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"


def test_atbash():
    assert atbash("Hello") == "Svool"
    assert atbash(atbash("Hello")) == "Hello"  # symmetric
    assert atbash("abcxyz") == "zyxcba"
