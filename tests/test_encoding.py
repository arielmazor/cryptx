"""Tests for the encoding module."""

from cryptx.encoding import (
    base16_encode, base16_decode,
    base32_encode, base32_decode,
    base58_encode, base58_decode,
    base64_encode, base64_decode,
    base85_encode, base85_decode,
    url_encode, url_decode,
    html_encode, html_decode,
    binary_encode, binary_decode,
    octal_encode, octal_decode,
    morse_encode, morse_decode,
    decimal_encode, decimal_decode,
)


def test_base16_roundtrip():
    assert base16_decode(base16_encode("Hello")) == "Hello"


def test_base16_known():
    assert base16_encode("Hi") == "4869"
    assert base16_decode("4869") == "Hi"


def test_base32_roundtrip():
    assert base32_decode(base32_encode("Hello, World!")) == "Hello, World!"


def test_base58_roundtrip():
    assert base58_decode(base58_encode("Hello, World!")) == "Hello, World!"


def test_base64_roundtrip():
    assert base64_decode(base64_encode("Hello, World!")) == "Hello, World!"


def test_base64_known():
    assert base64_encode("Hello") == "SGVsbG8="
    assert base64_decode("SGVsbG8=") == "Hello"


def test_base64_no_padding():
    assert base64_decode("SGVsbG8") == "Hello"


def test_base85_roundtrip():
    assert base85_decode(base85_encode("Hello, World!")) == "Hello, World!"


def test_url_roundtrip():
    original = "Hello World! @#$%"
    assert url_decode(url_encode(original)) == original


def test_url_known():
    assert url_encode("hello world") == "hello%20world"


def test_html_roundtrip():
    original = '<script>alert("xss")</script>'
    assert html_decode(html_encode(original)) == original


def test_html_known():
    assert html_encode("<>&") == "&lt;&gt;&amp;"


def test_binary_roundtrip():
    assert binary_decode(binary_encode("Hi")) == "Hi"


def test_binary_known():
    assert binary_encode("A") == "01000001"


def test_octal_roundtrip():
    assert octal_decode(octal_encode("Hi")) == "Hi"


def test_morse_roundtrip():
    assert morse_decode(morse_encode("HELLO WORLD")) == "HELLO WORLD"


def test_morse_known():
    assert morse_encode("SOS") == "... --- ..."


def test_decimal_roundtrip():
    assert decimal_decode(decimal_encode("Hello")) == "Hello"


def test_decimal_known():
    assert decimal_encode("AB") == "65 66"
    assert decimal_decode("65 66") == "AB"
