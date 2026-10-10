"""Tests for the packing module."""

from sheff.packing import p8, p16, p32, p64, u8, u16, u32, u64


def test_p8():
    assert p8(0x41) == "41"
    assert p8(0xFF) == "ff"


def test_p16_le():
    assert p16(0xCAFE) == "feca"


def test_p16_be():
    assert p16(0xCAFE, big_endian=True) == "cafe"


def test_p32_le():
    assert p32(0xDEADBEEF) == "efbeadde"


def test_p32_be():
    assert p32(0xDEADBEEF, big_endian=True) == "deadbeef"


def test_p64_le():
    assert p64(0xDEADBEEFCAFEBABE) == "bebafecaefbeadde"


def test_p64_be():
    assert p64(0xDEADBEEFCAFEBABE, big_endian=True) == "deadbeefcafebabe"


def test_u8():
    assert u8("41") == 0x41
    assert u8("ff") == 0xFF


def test_u16_le():
    assert u16("feca") == 0xCAFE


def test_u16_be():
    assert u16("cafe", big_endian=True) == 0xCAFE


def test_u32_le():
    assert u32("efbeadde") == 0xDEADBEEF


def test_u32_be():
    assert u32("deadbeef", big_endian=True) == 0xDEADBEEF


def test_u64_le():
    assert u64("bebafecaefbeadde") == 0xDEADBEEFCAFEBABE


def test_u64_be():
    assert u64("deadbeefcafebabe", big_endian=True) == 0xDEADBEEFCAFEBABE


def test_pack_unpack_roundtrip():
    assert u32(p32(12345)) == 12345
    assert u64(p64(0xDEADBEEF)) == 0xDEADBEEF
    assert u16(p16(0x1234)) == 0x1234
