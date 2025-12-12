# dil-gcm-envelope

AES-256-GCM Envelope Encryption for Python  
Outputs `{ payload, iv, tag }` compatible with JavaScript, Node.js, Dart/Flutter, and other languages.

This package provides simple, secure, interoperable encryption using **AES-256-GCM**.  
It is designed for **cross-platform encrypted API communication**, **secure app-to-server payloads**, and **lightweight secrets encryption**.

## Features

- 🔐 AES-256-GCM encryption
- 📦 Returns `{ payload, iv, tag }` — same as the JS NPM package  
- 🔄 Cross-language compatible (Node.js, Python, Flutter/Dart)
- ⚙️ Two key-derivation modes:
  - SHA256(password) — deterministic, ideal for interoperability  
  - PBKDF2-HMAC-SHA256 — stronger security with salt  
- 🔧 Encrypts:
  - JSON objects  
  - Strings  
  - Bytes  
- 🧪 Includes automated tests
- 📁 Optional CLI tool for encryption/decryption
- 🛡 Authenticated encryption with AES-GCM (rejects tampered data)

## Installation

```
pip install dil-gcm-envelope
```

## Usage Examples

### 1️ Basic SHA-256 Key Mode (cross-language)

```python
from dil_gcm_envelope import encrypt, decrypt
import json

password = "my-secret-key"
data = {"message": "Hello World", "n": 123}

encrypted = encrypt(password, data)
print(encrypted)

plaintext_bytes = decrypt(
    password,
    encrypted["payload"],
    encrypted["iv"],
    encrypted["tag"]
)
print(json.loads(plaintext_bytes.decode()))
```

### 2️ Strong Mode (PBKDF2)

```python
encrypted = encrypt(
    "my-password",
    "sensitive text",
    use_pbkdf2=True,
    pbkdf2_iterations=200_000
)
print(encrypted)
```

Decrypt:

```python
pt = decrypt(
    "my-password",
    encrypted["payload"],
    encrypted["iv"],
    encrypted["tag"],
    salt_b64=encrypted["salt"],
    pbkdf2_iterations=200_000
)
print(pt.decode())
```

### 3️ Encrypt Bytes

```python
binary_data = b"\x01\x02\x03ABC123"
enc = encrypt("pw", binary_data)
pt = decrypt("pw", enc["payload"], enc["iv"], enc["tag"])
print(pt)
```

## 🧰 CLI Usage

Encrypt:

```
dil-gcm-envelope encrypt mypass --text "Hello World"
```

PBKDF2:

```
dil-gcm-envelope encrypt mypass --text "Top Secret" --pbkdf2
```

Decrypt:

```
dil-gcm-envelope decrypt mypass --payload "..." --iv "..." --tag "..." --salt "..."
```

## Cross-Language Compatibility

Compatible with:

| Language | Package |
|---------|---------|
| Node.js | @dev_innovations_labs/dil-gcm-envelope/node |
| Browser | @dev_innovations_labs/dil-gcm-envelope/browser |
| Flutter/Dart | dil_gcm_envelope.dart (coming soon) |
| Python | dil-gcm-envelope |

## Security Notes

- AES-256-GCM provides authenticated encryption  
- SHA-256 derivation is deterministic (simple + compatible)  
- PBKDF2 recommended for production  
- Never reuse IV for same key (library auto-generates IV)

## Testing

```
pytest -q
```

## Build & Publish

```
python -m build
twine upload dist/*
```

## Use Cases

- Secure mobile → server communication  
- Encrypted API payloads  
- End-to-end encrypted messaging  
- Secure local storage  
