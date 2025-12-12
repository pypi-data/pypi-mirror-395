"""
Simple at-rest encryption utilities for sensitive credential files.

Design goals:
- Zero-prompt, local-only key material stored in config dir with 0600 perms
- AES-256-GCM authenticated encryption
- Backward compatible: if key missing or decryption fails, return None

This is not intended to protect against a determined local attacker with root,
but to avoid casual disclosure and accidental leaks while preserving UX.
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Optional, Union

from .config import Config

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM  # type: ignore
    _CRYPTO_OK = True
except Exception:
    AESGCM = None  # type: ignore
    _CRYPTO_OK = False


def _get_key_path(config: Config) -> Path:
    return config.config_dir / "crypto_key.bin"


def _load_or_create_key(config: Config) -> Optional[bytes]:
    if not _CRYPTO_OK:
        return None
    key_path = _get_key_path(config)
    try:
        if key_path.exists():
            data = key_path.read_bytes()
            if len(data) == 32:
                return data
            # If wrong length, ignore and recreate
    except Exception:
        pass
    try:
        key = os.urandom(32)
        key_path.parent.mkdir(parents=True, exist_ok=True)
        key_path.write_bytes(key)
        try:
            key_path.chmod(0o600)
        except Exception:
            pass
        return key
    except Exception:
        return None


def encrypt_json(config: Config, obj: Union[dict, list]) -> Optional[bytes]:
    """Encrypt a JSON-serializable object. Returns bytes or None on failure."""
    if not _CRYPTO_OK:
        return None
    try:
        plaintext = json.dumps(obj, separators=(",", ":")).encode("utf-8")
        key = _load_or_create_key(config)
        if not key:
            return None
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, plaintext, None)
        return b"EV1" + nonce + ct  # Simple versioned envelope
    except Exception:
        return None


def decrypt_json(config: Config, data: bytes) -> Optional[Union[dict, list]]:
    """Decrypt bytes produced by encrypt_json. Returns obj or None on failure."""
    if not _CRYPTO_OK:
        return None
    try:
        if not data or len(data) < 3 or data[:3] != b"EV1":
            return None
        nonce = data[3:15]
        ct = data[15:]
        key = _load_or_create_key(config)
        if not key:
            return None
        aesgcm = AESGCM(key)
        pt = aesgcm.decrypt(nonce, ct, None)
        return json.loads(pt.decode("utf-8"))
    except Exception:
        return None


