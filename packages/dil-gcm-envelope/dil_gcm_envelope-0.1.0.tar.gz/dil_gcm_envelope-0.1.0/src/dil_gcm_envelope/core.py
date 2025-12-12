# src/dil_gcm_envelope/core.py
"""
dil_gcm_envelope.core
AES-256-GCM envelope encryption compatible with other language implementations.
Outputs dict with base64 strings: { payload, iv, tag }.
"""

from __future__ import annotations

import os
import json
import base64
import hashlib
from typing import Any, Dict, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes, kdf

# Defaults
_IV_LEN = 12  # bytes
_TAG_LEN = 16  # bytes (GCM)
_KEY_LEN = 32  # 256-bit key


def _b64(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def _unb64(s: str) -> bytes:
    return base64.b64decode(s)


def derive_key_sha256(password: str) -> bytes:
    """
    Deterministic: key = SHA256(password). Good for cross-language compatibility.
    Not as strong as PBKDF2/Argon2 vs brute force.
    """
    return hashlib.sha256(password.encode("utf-8")).digest()


def derive_key_pbkdf2(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
    """
    Stronger KDF: PBKDF2-HMAC-SHA256. Returns 32-byte key.
    """
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=_KEY_LEN,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt(
    password: str,
    plaintext: Any,
    *,
    use_pbkdf2: bool = False,
    pbkdf2_iterations: int = 100_000,
) -> Dict[str, str]:
    """
    Encrypt JSON-serializable object / string / bytes.
    Returns dict with base64 strings:
      { payload, iv, tag }  (and if use_pbkdf2 True, includes 'salt' and 'kdf' metadata)
    """
    if isinstance(plaintext, (dict, list)):
        pt_bytes = json.dumps(plaintext, separators=(",", ":")).encode("utf-8")
    elif isinstance(plaintext, str):
        pt_bytes = plaintext.encode("utf-8")
    elif isinstance(plaintext, (bytes, bytearray)):
        pt_bytes = bytes(plaintext)
    else:
        # fallback to JSON-serializing arbitrary object
        pt_bytes = json.dumps(plaintext, default=str, separators=(",", ":")).encode("utf-8")

    # derive key
    salt = None
    if use_pbkdf2:
        salt = os.urandom(16)
        key = derive_key_pbkdf2(password, salt, iterations=pbkdf2_iterations)
    else:
        key = derive_key_sha256(password)

    aesgcm = AESGCM(key)
    iv = os.urandom(_IV_LEN)
    ct_and_tag = aesgcm.encrypt(iv, pt_bytes, associated_data=None)
    tag = ct_and_tag[-_TAG_LEN:]
    ciphertext = ct_and_tag[:-_TAG_LEN]

    out = {
        "payload": _b64(ciphertext),
        "iv": _b64(iv),
        "tag": _b64(tag),
    }
    if use_pbkdf2:
        out["salt"] = _b64(salt)
        out["kdf"] = "pbkdf2"
        out["pbkdf2_iterations"] = str(pbkdf2_iterations)
    else:
        out["kdf"] = "sha256"

    return out


def decrypt(
    password: str,
    payload_b64: str,
    iv_b64: str,
    tag_b64: str,
    *,
    salt_b64: Optional[str] = None,
    pbkdf2_iterations: int = 100_000,
) -> bytes:
    """
    Decrypt and return plaintext bytes.
    If the original used PBKDF2, pass salt_b64 (base64).
    Raises cryptography.exceptions.InvalidTag on auth failure.
    """
    ciphertext = _unb64(payload_b64)
    iv = _unb64(iv_b64)
    tag = _unb64(tag_b64)

    if salt_b64 is not None:
        salt = _unb64(salt_b64)
        key = derive_key_pbkdf2(password, salt, iterations=pbkdf2_iterations)
    else:
        key = derive_key_sha256(password)

    aesgcm = AESGCM(key)
    ct_and_tag = ciphertext + tag
    plaintext = aesgcm.decrypt(iv, ct_and_tag, associated_data=None)
    return plaintext
