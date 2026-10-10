<div align="center">

# ⚡ cryptx

### **The Swiss Army Knife for Encoding, Crypto, Hashing, Packing & Bitwise Math**
*100% Offline • Zero Telemetry • Instant Terminal Workflow • Unix Pipe-Friendly*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![Platform: Linux | macOS | Windows](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-brightgreen.svg)]()
[![Offline First](https://img.shields.io/badge/Security-100%25%20Offline-red.svg)]()

```bash
# Recommended for macOS / Linux CLI tools
pipx install cryptx

# Or standard pip
pip install cryptx
```

</div>

---

## 💡 Why cryptx?

When working on CTFs, exploit development, reverse engineering, or daily security tasks, workflow is constantly fragmented across browser tabs and bloated scripts:

- Pasting secrets into **CyberChef** or **dcode.fr** risks leaking tokens and requires an internet connection.
- Booting up **Python** or **pwntools** just to do `p32(0xdeadbeef)` or calculate `(0xdead << 16) | 0xbeef` is slow and repetitive.
- Checking 5 different hash types requires running 5 different shell utilities.

**cryptx** brings all of these into one unified, blazing-fast, offline terminal interface with an interactive **TUI Calculator**.

---

## 🗺️ Migration & Replacement Map

Replacing your daily tools with `cryptx`:

| Tool Being Replaced | Previous Workflow | ⚡ The `cryptx` Way |
|---|---|---|
| 🌐 **CyberChef** | Open browser, find `To Base64`, paste data | **`cryptx encode base64 "Hello"`** |
| 🌐 **CyberChef** | Build recipe: `From Hex` ➔ `XOR` | **`cryptx crypto xor "3b0a041a01" -k secret -d`** |
| 🌐 **dcode.fr** | Open website, paste ciphertext for Caesar | **`cryptx crypto caesar "Khoor" --bruteforce`** |
| 🌐 **dcode.fr** | Online Vigenère / Atbash solvers | **`cryptx crypto vigenere "ATTACK" -k KEY`** |
| 🐍 **pwntools** | `python3 -c "from pwn import *; print(p32(0xdeadbeef))"` | **`cryptx pack p32 0xdeadbeef`** |
| 🐍 **pwntools** | `python3 -c "from pwn import *; print(hex(u32(...)))"` | **`cryptx unpack u32 efbeadde`** |
| 🧮 **bc / Python REPL** | `python3 -c "print(hex(0xff & 0x0f))"` | **`cryptx calc`** *(Interactive TUI)* |
| 🔐 **hash utilities** | Run `md5sum`, `sha256sum`, etc. separately | **`cryptx hash all "my_string"`** |

---

## 🧮 Interactive TUI Calculator

Launch a persistent, multi-base bitwise REPL by simply running:

```bash
cryptx calc
```

### Terminal Interface:

```text
┌──────────────────────────────────────────────────────────┐
│                   cryptx  calculator                     │
├──────────────────────────────────────────────────────────┤
│  Operators   +  -  *  /  //  %  **                       │
│  Bitwise     &  |  ^  ~  <<  >>                          │
│  Bases       0xff (hex)  0b11 (bin)  0o77 (oct)          │
│  Variables   ans = last result  ·  x = <expr>            │
│  Commands    help · vars · clear · quit                  │
└──────────────────────────────────────────────────────────┘
» (0xdead << 16) | 0xbeef
  Dec:  3735928559
  Hex:  0xdeadbeef
  Oct:  0o33653337357
  Bin:  0b11011110101011011011111011101111

» mask = 0b11110000
  Dec:  240
  Hex:  0xf0
  Oct:  0o360
  Bin:  0b11110000

» ans & 0xff
  Dec:  240
  Hex:  0xf0
  Oct:  0o360
  Bin:  0b11110000

» quit
```

> **Need a one-liner for a shell script?**  
> `cryptx calc "0xff & 0b11110000"` evaluates and exits directly.

---

## 🚀 Feature Tour & Examples

### 1. Encodings & Decodings
Supports **Base16/Hex**, **Base32**, **Base58 (Bitcoin)**, **Base64**, **Base85/ASCII85**, **URL**, **HTML Entities**, **Binary**, **Octal**, **Morse Code**, and **Decimal ASCII**.

```bash
# Base64
cryptx encode base64 "Hello, World!"
# SGVsbG8sIFdvcmxkIQ==

cryptx decode base64 "SGVsbG8sIFdvcmxkIQ=="
# Hello, World!

# Hex
cryptx encode hex "flag{offline_tool}"
cryptx decode hex "666c6167"

# Base58 (Crypto addresses)
cryptx encode base58 "Satoshi"

# URL & HTML
cryptx encode url "admin=true&role=root"
cryptx decode html "&lt;svg onload=alert(1)&gt;"

# Morse & Binary
cryptx encode morse "SOS"
# ... --- ...
cryptx encode binary "CTF"
# 01000011 01010100 01000110
```

---

### 2. Classical Ciphers & XOR
Cryptographic transformations with cracking utilities:

```bash
# Caesar with bruteforce (tries all 26 shifts)
cryptx crypto caesar "Khoor" --bruteforce

# ROT13 and ROT47
cryptx crypto rot13 "Uryyb, Jbeyq!"
cryptx crypto rot47 "w6==@"

# XOR encryption / decryption
cryptx crypto xor "secret message" --key "mykey"
cryptx crypto xor "1e160e1707" --key "mykey" --decrypt

# Single-byte XOR bruteforce (auto-filters printable plaintexts)
cryptx crypto xor-bruteforce "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

# Vigenère Cipher
cryptx crypto vigenere "ATTACKATDAWN" --key "LEMON"
cryptx crypto vigenere "LXFOPVEFRNHR" --key "LEMON" --decrypt

# Atbash Cipher
cryptx crypto atbash "Hello"
```

---

### 3. Hashes & Checksums
Generate digests quickly or inspect all algorithms simultaneously:

```bash
# Single hash
cryptx hash sha256 "password123"
cryptx hash md5 "admin"
cryptx hash crc32 "data"

# All hashes at once
cryptx hash all "Hello"
#      MD5:  8b1a9953c4611296a827abf8c47804d7
#     SHA1:  f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0
#   SHA224:  70c57ff9e42e4726bfcfbc122cdcf8c51f49fa46811a2f9ffbd7be0a
#   SHA256:  185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969
#   SHA384:  3519c72c12f7e0a2b165a17922b4136dd5496a566cb347d5dae0cbede9dc0d52dced7...
#   SHA512:  361524111393430030def9840eb5b97d87b3bf914c63200c489ca22c...
#    CRC32:  f7d18982
```

---

### 4. Binary Packing & Unpacking (pwntools replacement)
Pack integer words into bytes, or inspect raw hex buffers in both little-endian and big-endian order:

```bash
# Pack integer to byte string (LE default, or --big-endian)
cryptx pack p32 0xdeadbeef
# Hex:    efbeadde
# Bytes:  ef be ad de
# Python: b'\xef\xbe\xad\xde'
# C:      {0xef, 0xbe, 0xad, 0xde}

cryptx pack p64 0x401156
cryptx pack p16 0x1337 --big-endian

# Unpack bytes to integer
cryptx unpack u32 efbeadde
# Dec:  3735928559
# Hex:  0xdeadbeef
# Oct:  0o33653337357
# Bin:  0b11011110101011011011111011101111
```

---

### 5. String & Payload Analysis
Get instant insight into payload length, Shannon entropy, byte representation, and encodings:

```bash
cryptx analyze "super_secret_payload"
```

---

## 🔗 Unix Piping & Shell Scripting

`cryptx` automatically detects whether data is passed as a positional CLI argument or piped through `stdin`:

```bash
# Pipe from curl or file
curl -s https://example.com | cryptx hash sha256

# Chain cryptx operations
echo "my_token" | cryptx encode base64 | cryptx hash md5

# Extract and decode hex strings
cat memory_dump.txt | grep -oE '[0-9a-fA-F]{8,}' | cryptx unpack u32 -
```

---

## 📦 Installation

### macOS (Recommended: `pipx`)
On macOS with Homebrew Python (PEP 668), use **`pipx`** to install command-line tools into an isolated environment accessible anywhere:

```bash
# Install via pipx (recommended for macOS)
pipx install .

# Or install directly from GitHub
pipx install git+https://github.com/arielmazor/cryptx.git
```

> If you don't have `pipx`: `brew install pipx && pipx ensurepath`

### Standard pip (Linux / Windows)

```bash
git clone https://github.com/arielmazor/cryptx.git
cd cryptx
pip install .

# On macOS without pipx:
pip3 install --user --break-system-packages .
```

### Development Mode

```bash
git clone https://github.com/arielmazor/cryptx.git
cd cryptx
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pytest -v
```

---

## 📋 Command Quick Reference

```
cryptx encode <format> [text]       Encode text into chosen format
cryptx decode <format> [text]       Decode formatted text to raw string
cryptx crypto caesar [text]         Caesar shift cipher (-s, -d, -b)
cryptx crypto rot13 [text]          ROT13 cipher (symmetric)
cryptx crypto rot47 [text]          ROT47 printable ASCII cipher
cryptx crypto xor [text]            XOR with repeating key (-k, -d)
cryptx crypto xor-bruteforce [hex]  Bruteforce 1-byte XOR key
cryptx crypto vigenere [text]       Vigenère polyalphabetic cipher (-k, -d)
cryptx crypto atbash [text]         Atbash mirror cipher
cryptx hash <algo> [text]           Compute cryptographic hash or 'all'
cryptx pack <p8|p16|p32|p64> <val>  Pack integer into bytes
cryptx unpack <u8|u16|u32|u64> <hex>Unpack bytes into integer
cryptx calc [expression]            Multi-base bitwise calculator (or TUI REPL)
cryptx analyze [text]               String stats, entropy, hashes & encodings
```

---

## 👤 Author

Developed by **Ariel Mazor**  
GitHub: [@arielmazor](https://github.com/arielmazor)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
