# 🔪 Sheff

**The Swiss Army Knife for encoding, decoding, crypto & hacking in your terminal.**

Like CyberChef, but lives in your terminal and works **100% offline**. No more juggling between CyberChef, dcode.fr, pwntools, and random online tools — Sheff puts everything in one place.

```
pip install sheff
```

---

## Features

| Category | What you get |
|---|---|
| **Encoding** | Base16/Hex, Base32, Base58, Base64, Base85/ASCII85, URL, HTML entities, Binary, Octal, Morse, Decimal |
| **Crypto** | Caesar (+ bruteforce), ROT13, ROT47, XOR (+ single-byte bruteforce), Vigenère, Atbash |
| **Hashing** | MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512, CRC32 |
| **Packing** | pwntools-style p8/p16/p32/p64 and u8/u16/u32/u64 (LE & BE) |
| **Calculator** | Multi-base (dec/hex/oct/bin) with full bitwise ops: `& \| ^ ~ << >>` |
| **Analysis** | String info, entropy, hex dump, all hashes + all encodings at once |

✅ Works completely offline  
✅ Pipe-friendly (stdin support)  
✅ Single dependency (`click`)  
✅ Python 3.10+  

---

## Installation

```bash
# From source
git clone https://github.com/arielmazor/sheff.git
cd sheff
pip install .

# Or install in development mode
pip install -e .
```

---

## Usage

### Encode & Decode

```bash
sheff encode base64 "Hello, World!"
# SGVsbG8sIFdvcmxkIQ==

sheff decode base64 "SGVsbG8sIFdvcmxkIQ=="
# Hello, World!

sheff encode hex "secret"
# 736563726574

sheff decode hex "736563726574"
# secret

sheff encode url "hello world & more"
# hello%20world%20%26%20more

sheff encode binary "Hi"
# 01001000 01101001

sheff encode morse "SOS"
# ... --- ...

# All formats: base16/hex, base32, base58, base64/b64,
#              base85/ascii85, url, html, binary/bin,
#              octal/oct, morse, decimal/dec
```

### Crypto

```bash
sheff crypto rot13 "Hello, World!"
# Uryyb, Jbeyq!

sheff crypto rot47 "Hello!"
# w6==@P

sheff crypto caesar "Hello" --shift 7
# Olssv

sheff crypto caesar "Khoor" --bruteforce
# [shift  0]  Khoor
# [shift  1]  Jgnnq
# [shift  2]  Ifmmp
# [shift  3]  Hello    ← found it!
# ...

sheff crypto xor "Hello" --key "secret"
# 3b0a041a01

sheff crypto xor "3b0a041a01" --key "secret" --decrypt
# Hello

sheff crypto vigenere "ATTACKATDAWN" --key LEMON
# LXFOPVEFRNHR

sheff crypto atbash "Hello"
# Svool
```

### Hashing

```bash
sheff hash sha256 "password"
# 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8

sheff hash md5 "Hello"
# 8b1a9953c4611296a827abf8c47804d7

sheff hash all "test"
#      MD5:  098f6bcd4621d373cade4e832627b4f6
#     SHA1:  a94a8fe5ccb19ba61c4c0873d391e987982fbbd3
#   SHA224:  90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809
#   SHA256:  9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
#   SHA384:  ...
#   SHA512:  ...
#    CRC32:  d87f7e0c
```

### Packing (pwntools-style)

```bash
sheff pack p32 0xdeadbeef
# Hex:    efbeadde
# Bytes:  ef be ad de
# Python: b'\xef\xbe\xad\xde'
# C:      {0xef, 0xbe, 0xad, 0xde}

sheff pack p64 0xcafebabe
sheff pack p16 0x1337 --big-endian

sheff unpack u32 efbeadde
# Dec:  3735928559
# Hex:  0xdeadbeef
# Oct:  0o33653337357
# Bin:  0b11011110101011011011111011101111
```

### Calculator

Supports **decimal, hex (0x), octal (0o), binary (0b)** input and outputs in **all bases**.  
Full arithmetic and bitwise operations.

```bash
sheff calc "0xff + 1"
# Dec:  256
# Hex:  0x100
# Oct:  0o400
# Bin:  0b100000000

sheff calc "0b1111 & 0b1010"
# Dec:  10
# Hex:  0xa
# Oct:  0o12
# Bin:  0b1010

sheff calc "(0xdead << 16) | 0xbeef"
# Dec:  3735928559
# Hex:  0xdeadbeef
# Oct:  0o33653337357
# Bin:  0b11011110101011011011111011101111

sheff calc "255 >> 4"
sheff calc "~0xff"
sheff calc "2 ** 32 - 1"
```

### Analyze

Get **everything** about a string at once — length, entropy, hex, all hashes, all encodings:

```bash
sheff analyze "Hello"
```

### Piping

Everything supports stdin, so you can pipe data through:

```bash
echo "Hello" | sheff encode base64
echo "SGVsbG8K" | sheff decode base64
cat file.txt | sheff hash sha256
echo "secret" | sheff encode hex
```

---

## All Commands

```
sheff encode <format> <text>    Encode data
sheff decode <format> <text>    Decode data
sheff crypto caesar <text>      Caesar cipher (--shift, --bruteforce, --decrypt)
sheff crypto rot13 <text>       ROT13
sheff crypto rot47 <text>       ROT47
sheff crypto xor <text>         XOR encrypt/decrypt (--key, --decrypt)
sheff crypto xor-bruteforce     Single-byte XOR bruteforce
sheff crypto vigenere <text>    Vigenère cipher (--key, --decrypt)
sheff crypto atbash <text>      Atbash cipher
sheff hash <algo> <text>        Hash data (md5, sha256, all, ...)
sheff pack <width> <value>      Pack integer (p8, p16, p32, p64)
sheff unpack <width> <hex>      Unpack bytes (u8, u16, u32, u64)
sheff calc "<expression>"       Multi-base calculator
sheff analyze <text>            Full analysis of input
```

Run `sheff <command> --help` for detailed usage of any command.

---

## License

MIT — See [LICENSE](LICENSE) for details.
