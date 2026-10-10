"""Sheff CLI — The Swiss Army Knife for encoding, crypto & hacking in your terminal.

Usage examples:
    sheff encode base64 "Hello, World!"
    sheff decode hex "48656c6c6f"
    sheff crypto rot13 "Uryyb"
    sheff hash sha256 "password"
    sheff pack p32 0xdeadbeef
    sheff unpack u32 efbeadde
    sheff calc "0xff & 0b11110000"
    sheff analyze "Hello"
    echo "secret" | sheff encode base64
"""

import sys

import click

from . import __version__
from .calculator import calculate
from .crypto import (
    atbash,
    caesar_bruteforce,
    caesar_decrypt,
    caesar_encrypt,
    rot13,
    rot47,
    vigenere_decrypt,
    vigenere_encrypt,
    xor_decrypt_hex,
    xor_encrypt,
    xor_single_byte_bruteforce,
)
from .encoding import ENCODINGS
from .hashing import ALGORITHMS, hash_all
from .packing import (
    format_pack,
    format_unpack,
    p8, p16, p32, p64,
    u8, u16, u32, u64,
)
from .utils import get_input, parse_int, string_info


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _styled(label: str, value: str) -> str:
    """Return a click-styled label: value line."""
    return f"{click.style(label, fg='cyan', bold=True)}  {value}"


# ─── Root ────────────────────────────────────────────────────────────────────

@click.group(invoke_without_command=True)
@click.version_option(__version__, prog_name="sheff")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Sheff — offline encoding, decoding, crypto, hashing, packing & calculator.

    \b
    Like CyberChef, but lives in your terminal and works offline.
    Run `sheff <command> --help` for details on any command.
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# ─── Encode ──────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("format", type=click.Choice(sorted(set(ENCODINGS.keys())), case_sensitive=False))
@click.argument("text", required=False)
def encode(format: str, text: str | None) -> None:
    """Encode data into the specified format.

    \b
    Formats: base16/hex, base32, base58, base64/b64,
             base85/ascii85, url, html, binary/bin,
             octal/oct, morse, decimal/dec

    \b
    Examples:
      sheff encode base64 "Hello, World!"
      sheff encode hex "secret"
      echo "pipe me" | sheff encode url
    """
    data = get_input(text)
    encoder, _ = ENCODINGS[format.lower()]
    click.echo(encoder(data))


# ─── Decode ──────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("format", type=click.Choice(sorted(set(ENCODINGS.keys())), case_sensitive=False))
@click.argument("text", required=False)
def decode(format: str, text: str | None) -> None:
    """Decode data from the specified format.

    \b
    Formats: base16/hex, base32, base58, base64/b64,
             base85/ascii85, url, html, binary/bin,
             octal/oct, morse, decimal/dec

    \b
    Examples:
      sheff decode base64 "SGVsbG8sIFdvcmxkIQ=="
      sheff decode hex "48656c6c6f"
    """
    data = get_input(text)
    _, decoder = ENCODINGS[format.lower()]
    click.echo(decoder(data))


# ─── Crypto ──────────────────────────────────────────────────────────────────

@cli.group()
def crypto() -> None:
    """Cryptographic ciphers and operations.

    \b
    Ciphers: caesar, rot13, rot47, xor, vigenere, atbash
    """


@crypto.command()
@click.argument("text", required=False)
@click.option("-s", "--shift", type=int, default=3, show_default=True, help="Shift value.")
@click.option("-d", "--decrypt", is_flag=True, help="Decrypt instead of encrypt.")
@click.option("-b", "--bruteforce", is_flag=True, help="Try all 26 shifts.")
def caesar(text: str | None, shift: int, decrypt: bool, bruteforce: bool) -> None:
    """Caesar cipher — shift letters by N positions.

    \b
    Examples:
      sheff crypto caesar "Hello"
      sheff crypto caesar "Khoor" -d -s 3
      sheff crypto caesar "Khoor" --bruteforce
    """
    data = get_input(text)
    if bruteforce:
        results = caesar_bruteforce(data)
        for s, plaintext in results:
            label = click.style(f"[shift {s:>2}]", fg="yellow")
            click.echo(f"{label}  {plaintext}")
    elif decrypt:
        click.echo(caesar_decrypt(data, shift))
    else:
        click.echo(caesar_encrypt(data, shift))


@crypto.command("rot13")
@click.argument("text", required=False)
def rot13_cmd(text: str | None) -> None:
    """ROT13 cipher (symmetric).

    \b
    Example:  sheff crypto rot13 "Hello, World!"
    """
    click.echo(rot13(get_input(text)))


@crypto.command("rot47")
@click.argument("text", required=False)
def rot47_cmd(text: str | None) -> None:
    """ROT47 cipher — rotates all printable ASCII (symmetric).

    \b
    Example:  sheff crypto rot47 "Hello, World!"
    """
    click.echo(rot47(get_input(text)))


@crypto.command()
@click.argument("text", required=False)
@click.option("-k", "--key", required=True, help="XOR key (string).")
@click.option("-d", "--decrypt", is_flag=True, help="Decrypt hex input (instead of encrypting plaintext).")
def xor(text: str | None, key: str, decrypt: bool) -> None:
    """XOR encrypt / decrypt with a repeating key.

    \b
    Encrypt returns hex.  Decrypt expects hex input.

    \b
    Examples:
      sheff crypto xor "Hello" -k "secret"
      sheff crypto xor "3b0a041a01" -k "secret" -d
    """
    data = get_input(text)
    if decrypt:
        click.echo(xor_decrypt_hex(data, key))
    else:
        click.echo(xor_encrypt(data, key))


@crypto.command("xor-bruteforce")
@click.argument("hex_data", required=False)
def xor_bf(hex_data: str | None) -> None:
    """Brute-force single-byte XOR (tries all 256 key bytes).

    \b
    Input must be a hex string.

    \b
    Example:  sheff crypto xor-bruteforce "3b0a041a01"
    """
    data = get_input(hex_data)
    results = xor_single_byte_bruteforce(data)
    if not results:
        click.echo("No printable results found.")
        return
    for key_byte, plaintext in results:
        label = click.style(f"[0x{key_byte:02x}]", fg="yellow")
        click.echo(f"{label}  {plaintext}")


@crypto.command()
@click.argument("text", required=False)
@click.option("-k", "--key", required=True, help="Vigenère key (letters only).")
@click.option("-d", "--decrypt", is_flag=True, help="Decrypt instead of encrypt.")
def vigenere(text: str | None, key: str, decrypt: bool) -> None:
    """Vigenère cipher — polyalphabetic substitution.

    \b
    Examples:
      sheff crypto vigenere "Hello" -k SECRET
      sheff crypto vigenere "Zincs" -k SECRET -d
    """
    data = get_input(text)
    if decrypt:
        click.echo(vigenere_decrypt(data, key))
    else:
        click.echo(vigenere_encrypt(data, key))


@crypto.command("atbash")
@click.argument("text", required=False)
def atbash_cmd(text: str | None) -> None:
    """Atbash cipher — mirror the alphabet (symmetric).

    \b
    Example:  sheff crypto atbash "Hello"
    """
    click.echo(atbash(get_input(text)))


# ─── Hash ────────────────────────────────────────────────────────────────────

@cli.command("hash")
@click.argument("algorithm", type=click.Choice(["all"] + sorted(ALGORITHMS.keys()), case_sensitive=False))
@click.argument("text", required=False)
def hash_cmd(algorithm: str, text: str | None) -> None:
    """Hash data with the specified algorithm.

    \b
    Algorithms: md5, sha1, sha224, sha256, sha384, sha512, crc32, all

    \b
    Examples:
      sheff hash sha256 "password"
      sheff hash all "Hello"
      echo -n "data" | sheff hash md5
    """
    data = get_input(text)
    if algorithm.lower() == "all":
        for name, digest in hash_all(data).items():
            click.echo(_styled(f"{name:>8}:", digest))
    else:
        func = ALGORITHMS[algorithm.lower()]
        click.echo(func(data))


# ─── Pack ────────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("width", type=click.Choice(["p8", "p16", "p32", "p64"], case_sensitive=False))
@click.argument("value")
@click.option("-b", "--big-endian", is_flag=True, help="Use big-endian byte order.")
def pack(width: str, value: str, big_endian: bool) -> None:
    """Pack an integer into bytes (pwntools-style).

    \b
    VALUE can be decimal, hex (0x…), octal (0o…), or binary (0b…).

    \b
    Examples:
      sheff pack p32 0xdeadbeef
      sheff pack p64 255
      sheff pack p16 0xcafe --big-endian
    """
    n = parse_int(value)
    pack_funcs = {"p8": p8, "p16": p16, "p32": p32, "p64": p64}
    func = pack_funcs[width.lower()]
    if width.lower() == "p8":
        result = func(n)
    else:
        result = func(n, big_endian=big_endian)
    click.echo(format_pack(result))


# ─── Unpack ──────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("width", type=click.Choice(["u8", "u16", "u32", "u64"], case_sensitive=False))
@click.argument("hex_data")
@click.option("-b", "--big-endian", is_flag=True, help="Use big-endian byte order.")
def unpack(width: str, hex_data: str, big_endian: bool) -> None:
    """Unpack bytes into an integer (pwntools-style).

    \b
    HEX_DATA is a hex string (e.g. "efbeadde").

    \b
    Examples:
      sheff unpack u32 efbeadde
      sheff unpack u64 efbeaddeefbeadde
      sheff unpack u16 cafe --big-endian
    """
    unpack_funcs = {"u8": u8, "u16": u16, "u32": u32, "u64": u64}
    func = unpack_funcs[width.lower()]
    if width.lower() == "u8":
        result = func(hex_data)
    else:
        result = func(hex_data, big_endian=big_endian)
    click.echo(format_unpack(result))


# ─── Calc ────────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("expression")
def calc(expression: str) -> None:
    """Multi-base calculator with bitwise operations.

    \b
    Accepts integers in decimal, hex (0x), octal (0o), binary (0b).

    \b
    Operators:
      Arithmetic:  +  -  *  /  //  %  **
      Bitwise:     &  |  ^  ~  <<  >>

    \b
    Examples:
      sheff calc "0xff + 1"
      sheff calc "0b1111 & 0b1010"
      sheff calc "255 << 8"
      sheff calc "~0xff"
      sheff calc "(0xdead << 16) | 0xbeef"
    """
    try:
        _, formatted = calculate(expression)
        click.echo(formatted)
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}") from exc


# ─── Analyze ─────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("text", required=False)
def analyze(text: str | None) -> None:
    """Show detailed information about a string.

    \b
    Displays length, entropy, hex dump, all hashes, and more.

    \b
    Example:  sheff analyze "Hello, World!"
    """
    data = get_input(text)

    # String info
    click.echo(click.style("─── String Info ───", fg="green", bold=True))
    click.echo(string_info(data))

    # All hashes
    click.echo()
    click.echo(click.style("─── Hashes ───", fg="green", bold=True))
    for name, digest in hash_all(data).items():
        click.echo(_styled(f"{name:>8}:", digest))

    # All encodings
    click.echo()
    click.echo(click.style("─── Encodings ───", fg="green", bold=True))
    shown = set()
    for fmt_name, (encoder, _) in ENCODINGS.items():
        if encoder in shown:
            continue
        shown.add(encoder)
        try:
            encoded = encoder(data)
            click.echo(_styled(f"{fmt_name:>8}:", encoded))
        except Exception:
            pass
