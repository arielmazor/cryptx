"""Tests for the hashing module."""

from cryptx.hashing import md5, sha1, sha256, sha512, crc32, hash_all


def test_md5():
    assert md5("Hello") == "8b1a9953c4611296a827abf8c47804d7"


def test_sha1():
    assert sha1("Hello") == "f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0"


def test_sha256():
    assert sha256("Hello") == "185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969"


def test_sha512():
    # Just verify it returns a 128-char hex string
    result = sha512("Hello")
    assert len(result) == 128
    assert all(c in "0123456789abcdef" for c in result)


def test_crc32():
    result = crc32("Hello")
    assert len(result) == 8
    assert all(c in "0123456789abcdef" for c in result)


def test_hash_all():
    results = hash_all("test")
    assert "MD5" in results
    assert "SHA1" in results
    assert "SHA256" in results
    assert "SHA512" in results
    assert "CRC32" in results
    assert len(results) == 7  # md5, sha1, sha224, sha256, sha384, sha512, crc32
