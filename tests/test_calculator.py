"""Tests for the calculator module."""

import pytest
from cryptx.calculator import safe_eval, calculate, format_result


def test_basic_arithmetic():
    assert safe_eval("2 + 3") == 5
    assert safe_eval("10 - 3") == 7
    assert safe_eval("4 * 5") == 20
    assert safe_eval("10 / 3") == pytest.approx(3.333333)
    assert safe_eval("10 // 3") == 3
    assert safe_eval("10 % 3") == 1
    assert safe_eval("2 ** 8") == 256


def test_hex_input():
    assert safe_eval("0xff") == 255
    assert safe_eval("0xff + 1") == 256
    assert safe_eval("0xdead") == 0xDEAD


def test_binary_input():
    assert safe_eval("0b1111") == 15
    assert safe_eval("0b1010 + 0b0101") == 15


def test_octal_input():
    assert safe_eval("0o777") == 511
    assert safe_eval("0o10") == 8


def test_bitwise_and():
    assert safe_eval("0xff & 0x0f") == 0x0F


def test_bitwise_or():
    assert safe_eval("0xf0 | 0x0f") == 0xFF


def test_bitwise_xor():
    assert safe_eval("0xff ^ 0x0f") == 0xF0


def test_bitwise_not():
    assert safe_eval("~0") == -1
    assert safe_eval("~0xff") == -256


def test_bitwise_shift():
    assert safe_eval("1 << 8") == 256
    assert safe_eval("256 >> 4") == 16


def test_complex_expression():
    assert safe_eval("(0xdead << 16) | 0xbeef") == 0xDEADBEEF


def test_unary_minus():
    assert safe_eval("-5") == -5
    assert safe_eval("-0xff") == -255


def test_context_variables():
    ctx = {"ans": 256, "x": 10}
    assert safe_eval("ans >> 4", ctx) == 16
    assert safe_eval("ans + x", ctx) == 266


def test_unknown_variable():
    with pytest.raises(ValueError, match="Unknown variable: 'foobar'"):
        safe_eval("foobar + 1", {})


def test_format_result_integer():
    result = format_result(255)
    assert "255" in result
    assert "0xff" in result
    assert "0o377" in result
    assert "0b11111111" in result


def test_format_result_float():
    result = format_result(3.14)
    assert "3.14" in result


def test_calculate():
    value, formatted = calculate("0xff + 1")
    assert value == 256
    assert "256" in formatted


def test_invalid_expression():
    with pytest.raises(ValueError):
        safe_eval("import os")


def test_no_function_calls():
    with pytest.raises(ValueError):
        safe_eval("print(1)")
