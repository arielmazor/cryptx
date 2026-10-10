"""cryptx CLI — The Swiss Army Knife for encoding, crypto & hacking in your terminal.

Usage examples:
    cryptx encode base64 "Hello, World!"
    cryptx decode "QXJpZWwgTWF6b3I="        # auto-detects format!
    cryptx decode hex "48656c6c6f"
    cryptx rot13 "Uryyb"                   # direct top-level cipher
    cryptx crypto rot13 "Uryyb"            # grouped crypto cipher
    cryptx crack 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
    cryptx hash sha256 "password"
    cryptx pack p32 0xdeadbeef
    cryptx unpack u32 efbeadde
    cryptx calc                            # interactive TUI
    cryptx analyze "QXJpZWwgTWF6b3I="      # shows detected string types
    echo "secret" | cryptx encode base64
"""

import sys

import click

from . import __version__
from .calculator import calc_repl, calculate
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
from .detect import auto_decode, detect_types, identify_hash
from .encoding import ENCODINGS
from .hashing import ALGORITHMS, hash_all
from .packing import (
    format_pack,
    format_unpack,
    p8, p16, p32, p64,
    u8, u16, u32, u64,
)
from .rainbow import lookup_hash
from .utils import get_input, parse_int, string_info


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _styled(label: str, value: str) -> str:
    """Return a click-styled label: value line."""
    return f"{click.style(label, fg='cyan', bold=True)}  {value}"


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "-help"])


class CryptxCommand(click.Command):
    """Custom command that intercepts 'help', '-help', '-h', '--help' arguments."""

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        if args and args[0] in ("help", "-help", "-h", "--help"):
            click.echo(self.get_help(ctx))
            ctx.exit()
        return super().parse_args(ctx, args)


class CryptxGroup(click.Group):
    """Custom group that supports 'help', 'help <cmd>', '<cmd> help', '-h', etc."""

    command_class = CryptxCommand

    def group(self, *args, **kwargs):
        kwargs.setdefault("cls", CryptxGroup)
        return super().group(*args, **kwargs)

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        if args and args[0] in ("help", "-help", "-h", "--help"):
            if args[0] == "help" and len(args) > 1:
                cmd = self.get_command(ctx, args[1])
                if cmd is not None:
                    sub_ctx = click.Context(cmd, info_name=args[1], parent=ctx)
                    click.echo(cmd.get_help(sub_ctx))
                    ctx.exit()
            if len(args) == 1:
                click.echo(self.get_help(ctx))
                ctx.exit()
        return super().parse_args(ctx, args)


# ─── Root ────────────────────────────────────────────────────────────────────

@click.group(cls=CryptxGroup, context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(__version__, "-v", "--version", prog_name="cryptx")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """cryptx — offline encoding, decoding, crypto, hashing, packing & calculator.

    \b
    Like CyberChef, but lives in your terminal and works offline.
    Run `cryptx <command> --help` or `cryptx help` for details on any command.
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
             octal/oct, morse, decimal/dec, rot13, rot47, atbash

    \b
    Examples:
      cryptx encode base64 "Hello, World!"
      cryptx encode hex "secret"
      cryptx encode rot13 "Hello"
      echo "pipe me" | cryptx encode url
    """
    data = get_input(text)
    encoder, _ = ENCODINGS[format.lower()]
    click.echo(encoder(data))


# ─── Decode ──────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("format_or_text", required=False)
@click.argument("text", required=False)
def decode(format_or_text: str | None, text: str | None) -> None:
    """Decode data. Automatically detects format if only data is provided.

    \b
    Formats: base16/hex, base32, base58, base64/b64,
             base85/ascii85, url, html, binary/bin,
             octal/oct, morse, decimal/dec, rot13, rot47, atbash

    \b
    Examples:
      cryptx decode "QXJpZWwgTWF6b3I="                # auto-detects Base64!
      cryptx decode "48656c6c6f"                      # auto-detects Hex!
      cryptx decode base64 "SGVsbG8sIFdvcmxkIQ=="     # explicit format
      echo "QXJpZWwgTWF6b3I=" | cryptx decode         # auto-detects from pipe
      echo "SGVsbG8=" | cryptx decode base64          # explicit format from pipe
    """
    if format_or_text is None and text is None:
        # Piped input without format -> auto-detect
        data = get_input(None)
        _, decoded = auto_decode(data)
        click.echo(decoded)
        return

    if text is not None:
        # Two arguments passed: cryptx decode base64 "..."
        fmt = format_or_text.lower()
        if fmt not in ENCODINGS:
            raise click.BadParameter(f"Unknown format '{format_or_text}'.", param_hint="format")
        _, decoder = ENCODINGS[fmt]
        click.echo(decoder(text))
        return

    # One argument passed
    fmt_candidate = format_or_text.lower()
    if fmt_candidate in ENCODINGS and not sys.stdin.isatty():
        # echo "..." | cryptx decode base64
        data = sys.stdin.read().strip()
        _, decoder = ENCODINGS[fmt_candidate]
        click.echo(decoder(data))
        return

    # User ran: cryptx decode "<data>"
    try:
        _, decoded = auto_decode(format_or_text)
        click.echo(decoded)
    except ValueError:
        if fmt_candidate in ENCODINGS:
            raise SystemExit(f"Error: no input provided for format '{format_or_text}'.")
        raise SystemExit(f"Error: could not automatically detect encoding for: '{format_or_text}'.")


# ─── Classical Ciphers (Shared Implementation) ───────────────────────────────

def _run_caesar(text: str | None, shift: int, decrypt: bool, bruteforce: bool) -> None:
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


def _run_xor(text: str | None, key: str, decrypt: bool) -> None:
    data = get_input(text)
    if decrypt:
        click.echo(xor_decrypt_hex(data, key))
    else:
        click.echo(xor_encrypt(data, key))


def _run_xor_bf(hex_data: str | None) -> None:
    data = get_input(hex_data)
    results = xor_single_byte_bruteforce(data)
    if not results:
        click.echo("No printable results found.")
        return
    for key_byte, plaintext in results:
        label = click.style(f"[0x{key_byte:02x}]", fg="yellow")
        click.echo(f"{label}  {plaintext}")


def _run_vigenere(text: str | None, key: str, decrypt: bool) -> None:
    data = get_input(text)
    if decrypt:
        click.echo(vigenere_decrypt(data, key))
    else:
        click.echo(vigenere_encrypt(data, key))


# ─── Top-Level Direct Cipher Commands ────────────────────────────────────────

@cli.command("caesar")
@click.argument("text", required=False)
@click.option("-s", "--shift", type=int, default=3, show_default=True, help="Shift value.")
@click.option("-d", "--decrypt", is_flag=True, help="Decrypt instead of encrypt.")
@click.option("-b", "--bruteforce", is_flag=True, help="Try all 26 shifts.")
def caesar_root(text: str | None, shift: int, decrypt: bool, bruteforce: bool) -> None:
    """Caesar cipher — shift letters by N positions."""
    _run_caesar(text, shift, decrypt, bruteforce)


@cli.command("rot13")
@click.argument("text", required=False)
def rot13_root(text: str | None) -> None:
    """ROT13 cipher (symmetric)."""
    click.echo(rot13(get_input(text)))


@cli.command("rot47")
@click.argument("text", required=False)
def rot47_root(text: str | None) -> None:
    """ROT47 cipher — rotates all printable ASCII (symmetric)."""
    click.echo(rot47(get_input(text)))


@cli.command("atbash")
@click.argument("text", required=False)
def atbash_root(text: str | None) -> None:
    """Atbash cipher — mirror the alphabet (symmetric)."""
    click.echo(atbash(get_input(text)))


@cli.command("xor")
@click.argument("text", required=False)
@click.option("-k", "--key", required=True, help="XOR key (string).")
@click.option("-d", "--decrypt", is_flag=True, help="Decrypt hex input (instead of encrypting plaintext).")
def xor_root(text: str | None, key: str, decrypt: bool) -> None:
    """XOR encrypt / decrypt with a repeating key."""
    _run_xor(text, key, decrypt)


@cli.command("xor-bruteforce")
@click.argument("hex_data", required=False)
def xor_bf_root(hex_data: str | None) -> None:
    """Brute-force single-byte XOR (tries all 256 key bytes)."""
    _run_xor_bf(hex_data)


@cli.command("vigenere")
@click.argument("text", required=False)
@click.option("-k", "--key", required=True, help="Vigenère key (letters only).")
@click.option("-d", "--decrypt", is_flag=True, help="Decrypt instead of encrypt.")
def vigenere_root(text: str | None, key: str, decrypt: bool) -> None:
    """Vigenère cipher — polyalphabetic substitution."""
    _run_vigenere(text, key, decrypt)


# ─── Grouped Crypto Subcommands (Preserved for compatibility) ────────────────

@cli.group()
def crypto() -> None:
    """Cryptographic ciphers and operations.

    \b
    Ciphers: caesar, rot13, rot47, xor, vigenere, atbash
    """


@crypto.command("caesar")
@click.argument("text", required=False)
@click.option("-s", "--shift", type=int, default=3, show_default=True, help="Shift value.")
@click.option("-d", "--decrypt", is_flag=True, help="Decrypt instead of encrypt.")
@click.option("-b", "--bruteforce", is_flag=True, help="Try all 26 shifts.")
def caesar_grouped(text: str | None, shift: int, decrypt: bool, bruteforce: bool) -> None:
    """Caesar cipher — shift letters by N positions."""
    _run_caesar(text, shift, decrypt, bruteforce)


@crypto.command("rot13")
@click.argument("text", required=False)
def rot13_grouped(text: str | None) -> None:
    """ROT13 cipher (symmetric)."""
    click.echo(rot13(get_input(text)))


@crypto.command("rot47")
@click.argument("text", required=False)
def rot47_grouped(text: str | None) -> None:
    """ROT47 cipher — rotates all printable ASCII (symmetric)."""
    click.echo(rot47(get_input(text)))


@crypto.command("xor")
@click.argument("text", required=False)
@click.option("-k", "--key", required=True, help="XOR key (string).")
@click.option("-d", "--decrypt", is_flag=True, help="Decrypt hex input.")
def xor_grouped(text: str | None, key: str, decrypt: bool) -> None:
    """XOR encrypt / decrypt with a repeating key."""
    _run_xor(text, key, decrypt)


@crypto.command("xor-bruteforce")
@click.argument("hex_data", required=False)
def xor_bf_grouped(hex_data: str | None) -> None:
    """Brute-force single-byte XOR (tries all 256 key bytes)."""
    _run_xor_bf(hex_data)


@crypto.command("vigenere")
@click.argument("text", required=False)
@click.option("-k", "--key", required=True, help="Vigenère key (letters only).")
@click.option("-d", "--decrypt", is_flag=True, help="Decrypt instead of encrypt.")
def vigenere_grouped(text: str | None, key: str, decrypt: bool) -> None:
    """Vigenère cipher — polyalphabetic substitution."""
    _run_vigenere(text, key, decrypt)


@crypto.command("atbash")
@click.argument("text", required=False)
def atbash_grouped(text: str | None) -> None:
    """Atbash cipher — mirror the alphabet (symmetric)."""
    click.echo(atbash(get_input(text)))


# ─── Hash & Cracking ─────────────────────────────────────────────────────────

def _run_crack(target: str) -> None:
    """Identify hash format and crack using offline rainbow tables or generate Hashcat commands."""
    click.echo(click.style("─── Hash Identification & Cracker ───", fg="green", bold=True))
    click.echo(f"Hash:   {target}")
    click.echo(f"Length: {len(target)} characters")

    # 1. Attempt offline rainbow table lookup
    match = lookup_hash(target)
    if match:
        plaintext, algo, mode = match
        click.echo()
        click.echo(click.style("[✓] CRACKED (Offline Rainbow Table)!", fg="yellow", bold=True))
        click.echo(_styled("Plaintext:", f"'{plaintext}'"))
        click.echo(_styled("Algorithm:", algo))
        click.echo(_styled("Hashcat Mode:", f"-m {mode}"))
        return

    # 2. Identify candidates and hashcat command
    candidates = identify_hash(target)
    click.echo()
    click.echo(click.style("[-] Not found in built-in offline table.", fg="red"))
    if candidates:
        click.echo()
        click.echo(click.style("[!] Likely Hash Candidates:", fg="cyan", bold=True))
        for cand in candidates:
            bits_info = f" ({cand['bits']}-bit)" if cand["bits"] else ""
            click.echo(f"    • {cand['name']:<24} (Hashcat: -m {cand['mode']}){bits_info}")

        best = candidates[0]
        click.echo()
        click.echo(click.style("[*] Suggested Hashcat Commands:", fg="green", bold=True))
        click.echo(f"    # Dictionary attack:")
        click.echo(f"    hashcat -m {best['mode']} '{target}' /usr/share/wordlists/rockyou.txt")
        click.echo()
        click.echo(f"    # Brute-force mask attack (e.g. 8 characters):")
        click.echo(f"    hashcat -m {best['mode']} -a 3 '{target}' ?a?a?a?a?a?a?a?a")
    else:
        click.echo()
        click.echo(click.style("[?] Unknown hash format.", fg="yellow"))


@cli.command("crack")
@click.argument("hash_value", required=False)
def crack(hash_value: str | None) -> None:
    """Identify a hash and crack it with offline rainbow tables or Hashcat command.

    \b
    Examples:
      cryptx crack 5d41402abc4b2a76b9719d911017c592
      cryptx crack 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
      echo "098f6bcd4621d373cade4e832627b4f6" | cryptx crack
    """
    target = get_input(hash_value).strip()
    _run_crack(target)


@cli.command("hashcat")
@click.argument("hash_value", required=False)
def hashcat_alias(hash_value: str | None) -> None:
    """Alias for 'cryptx crack'."""
    target = get_input(hash_value).strip()
    _run_crack(target)


@cli.command("hash-id")
@click.argument("hash_value", required=False)
def hash_id_alias(hash_value: str | None) -> None:
    """Identify a hash and generate Hashcat command."""
    target = get_input(hash_value).strip()
    _run_crack(target)


@cli.command("hash")
@click.argument("algorithm", type=click.Choice(["all", "crack", "identify"] + sorted(ALGORITHMS.keys()), case_sensitive=False))
@click.argument("text", required=False)
def hash_cmd(algorithm: str, text: str | None) -> None:
    """Hash data with the specified algorithm or crack/identify a hash.

    \b
    Algorithms: md5, sha1, sha224, sha256, sha384, sha512, crc32, all, crack, identify
    """
    algo_lower = algorithm.lower()
    if algo_lower in ("crack", "identify"):
        target = get_input(text).strip()
        _run_crack(target)
        return

    data = get_input(text)
    if algo_lower == "all":
        for name, digest in hash_all(data).items():
            click.echo(_styled(f"{name:>8}:", digest))
    else:
        func = ALGORITHMS[algo_lower]
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
      cryptx pack p32 0xdeadbeef
      cryptx pack p64 255
      cryptx pack p16 0xcafe --big-endian
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
      cryptx unpack u32 efbeadde
      cryptx unpack u64 efbeaddeefbeadde
      cryptx unpack u16 cafe --big-endian
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
@click.argument("expression", required=False)
def calc(expression: str | None) -> None:
    """Multi-base calculator with bitwise operations.

    \b
    Run without arguments to open the interactive TUI calculator.
    Pass an expression for a one-shot evaluation.
    """
    if expression is None:
        calc_repl()
    else:
        try:
            _, formatted = calculate(expression)
            click.echo(formatted)
        except ValueError as exc:
            raise SystemExit(f"Error: {exc}") from exc


# ─── Analyze ─────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("text", required=False)
def analyze(text: str | None) -> None:
    """Show detailed information and auto-detected string type.

    \b
    Identifies if input is Base64, Hex, Binary, JWT, or a Hash,
    and displays length, entropy, hex dump, all hashes, and encodings.

    \b
    Example:  cryptx analyze "QXJpZWwgTWF6b3I="
    """
    data = get_input(text)

    # 1. Detected string types
    detected = detect_types(data)
    if detected:
        click.echo(click.style("─── Detected Types ───", fg="green", bold=True))
        for item in detected:
            label = f"{item['type']} ({item['confidence']}):"
            click.echo(_styled(f"{label:>32}", item["preview"]))

        # Check offline rainbow table if it matches a hash
        rainbow_match = lookup_hash(data)
        if rainbow_match:
            plain, algo, mode = rainbow_match
            click.echo()
            click.echo(click.style(f"  [✓] Cracked (Rainbow Table): '{plain}' ({algo}, Hashcat: -m {mode})", fg="yellow", bold=True))
        click.echo()

    # 2. String info
    click.echo(click.style("─── String Info ───", fg="green", bold=True))
    click.echo(string_info(data))

    # 3. All hashes
    click.echo()
    click.echo(click.style("─── Hashes ───", fg="green", bold=True))
    for name, digest in hash_all(data).items():
        click.echo(_styled(f"{name:>8}:", digest))

    # 4. All encodings
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
