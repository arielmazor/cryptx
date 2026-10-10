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
- Identifying unknown hashes and looking up Hashcat mode flags requires external web searches.

**cryptx** brings all of these into one unified, blazing-fast, offline terminal interface with an interactive **TUI Calculator** and **Offline Rainbow Cracker**.

---

## 🗺️ Migration & Replacement Map

Replacing your daily tools with `cryptx`:

| Tool Being Replaced | Previous Workflow | ⚡ The `cryptx` Way |
|---|---|---|
| 🌐 **CyberChef** | Guess format, find `From Base64` | **`cryptx decode "QXJpZWwgTWF6b3I="`** *(Auto-detect!)* |
| 🌐 **CyberChef** | Open browser, find `To Base64`, paste data | **`cryptx encode base64 "Hello"`** |
| 🌐 **CyberChef** | Build recipe: `From Hex` ➔ `XOR` | **`cryptx xor "3b0a041a01" -k secret -d`** |
| 🌐 **dcode.fr** | Open website, paste ciphertext for Caesar | **`cryptx caesar "Khoor" --bruteforce`** |
| 🌐 **dcode.fr** | Navigate online cipher tools | **`cryptx rot13 "Uryyb"`** / **`cryptx atbash "Hello"`** |
| 🔍 **hash-identifier** | Run external python script to inspect hash | **`cryptx crack <hash>`** *(Identifies algorithm & Hashcat mode)* |
| ⚡ **Hashcat** | Memorize `-m` flags and syntax for rockyou | **`cryptx crack <hash>`** *(Generates exact Hashcat commands)* |
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

### 1. Smart Auto-Decode & Encodings
Pass encoded data directly — `cryptx decode` automatically identifies the encoding and decodes it without needing you to specify the format:

```bash
# Auto-detects Base64 automatically!
cryptx decode "QXJpZWwgTWF6b3I="
# Ariel Mazor

# Auto-detects Hex automatically!
cryptx decode "48656c6c6f"
# Hello

# Auto-detects from pipes!
echo "QXJpZWwgTWF6b3I=" | cryptx decode
# Ariel Mazor

# Or specify format explicitly:
cryptx encode base64 "Hello, World!"
cryptx decode base64 "SGVsbG8sIFdvcmxkIQ=="

# Formats supported:
# base16/hex, base32, base58, base64/b64, base85/ascii85,
# url, html, binary/bin, octal/oct, morse, decimal/dec,
# rot13, rot47, atbash
```

---

### 2. Hashcat Identifier & Offline Rainbow Table Cracker
Identify any hash, crack common/CTF hashes instantly **100% offline**, or generate copy-pasteable Hashcat commands:

```bash
# Instant offline rainbow cracking:
cryptx crack 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

Output:
```text
─── Hash Identification & Cracker ───
Hash:   5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
Length: 64 characters

[✓] CRACKED (Offline Rainbow Table)!
Plaintext:     'password'
Algorithm:     SHA-256
Hashcat Mode:  -m 1400
```

When given an unknown or complex hash:
```bash
cryptx crack 1111111111111111111111111111111111111111111111111111111111111111
```

Output:
```text
─── Hash Identification & Cracker ───
Hash:   1111111111111111111111111111111111111111111111111111111111111111
Length: 64 characters

[-] Not found in built-in offline table.

[!] Likely Hash Candidates:
    • SHA-256                  (Hashcat: -m 1400) (256-bit)
    • SHA3-256                 (Hashcat: -m 17400) (256-bit)
    • BLAKE2b-256              (Hashcat: -m 17700) (256-bit)

[*] Suggested Hashcat Commands:
    # Dictionary attack:
    hashcat -m 1400 '1111111...' /usr/share/wordlists/rockyou.txt

    # Brute-force mask attack (8 chars):
    hashcat -m 1400 -a 3 '1111111...' ?a?a?a?a?a?a?a?a
```

---

### 3. Classical Ciphers & XOR (Merged Workflow)
All ciphers can be invoked **directly as top-level commands**, or via `crypto`, or inside `encode`/`decode`:

```bash
# Top-level direct commands:
cryptx rot13 "Hello, World!"
# Uryyb, Jbeyq!

cryptx rot47 "Hello!"
# w6==@P

cryptx caesar "Khoor" --bruteforce
# [shift  0]  Khoor
# [shift  1]  Jgnnq
# [shift  2]  Ifmmp
# [shift  3]  Hello    ← cracked!

cryptx xor "secret message" --key "mykey"
cryptx xor "1e160e1707" --key "mykey" --decrypt
cryptx xor-bruteforce "3b0a041a01"

cryptx vigenere "ATTACKATDAWN" --key "LEMON"
cryptx atbash "Hello"

# Also available through encode/decode:
cryptx encode rot13 "Hello"
cryptx decode rot13 "Uryyb"
```

---

### 4. String & Payload Analysis (Type Detection)
`cryptx analyze` identifies if a string is Base64, Hex, Binary, JWT, or a Hash, and displays decoded previews:

```bash
cryptx analyze "QXJpZWwgTWF6b3I="
```

Output:
```text
─── Detected Types ───
                  Base64 (High):  Ariel Mazor

─── String Info ───
String:   'QXJpZWwgTWF6b3I='
Length:   16 chars, 16 bytes
Entropy:  3.8750 bits/char
Hex:      51584a705a577767545746366233493d

─── Hashes ───
     MD5:  5b83984be8bf99f57df520ae1aa3a186
  SHA256:  fe05183f3286f32e92c10b7db0a0dc23805eb31e03886561f36341490ee53676
...
```

---

### 5. Binary Packing & Unpacking (pwntools replacement)
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

## 🔗 Unix Piping & Shell Scripting

`cryptx` automatically detects whether data is passed as a positional CLI argument or piped through `stdin`:

```bash
# Pipe from curl or file
curl -s https://example.com | cryptx hash sha256

# Auto-decode from pipe
echo "QXJpZWwgTWF6b3I=" | cryptx decode

# Pipe hash into cracker
echo "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8" | cryptx crack
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
cryptx help [command]               Show global help or command help (also cryptx <command> help)
cryptx -v / --version               Show current version
cryptx -h / -help / --help          Show help options
cryptx decode [format] [text]       Decode data (auto-detects format if omitted!)
cryptx encode <format> [text]       Encode text into chosen format
cryptx crack <hash>                 Identify hash & crack with offline rainbow table / Hashcat
cryptx calc [expression]            Multi-base bitwise calculator (or TUI REPL)
cryptx analyze [text]               String stats, detected type, entropy & hashes
cryptx rot13 / rot47 [text]         Direct ROT13/ROT47 cipher
cryptx caesar [text]                Caesar shift cipher (-s, -d, -b)
cryptx xor [text]                   XOR with repeating key (-k, -d)
cryptx xor-bruteforce [hex]         Bruteforce 1-byte XOR key
cryptx vigenere [text]              Vigenère polyalphabetic cipher (-k, -d)
cryptx atbash [text]                Atbash mirror cipher
cryptx hash <algo> [text]           Compute cryptographic hash or 'all'
cryptx pack <p8|p16|p32|p64> <val>  Pack integer into bytes
cryptx unpack <u8|u16|u32|u64> <hex>Unpack bytes into integer
```

---

## 👤 Author

Developed by **Ariel Mazor**  
GitHub: [@arielmazor](https://github.com/arielmazor)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
