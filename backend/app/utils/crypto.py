import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.core.config import get_settings


def _aesgcm() -> AESGCM:
    raw = base64.b64decode(get_settings().encryption_key)
    if len(raw) != 32:
        raise ValueError("ENCRYPTION_KEY must decode to 32 bytes")
    return AESGCM(raw)


def encrypt_secret(secret: str) -> tuple[bytes, bytes]:
    nonce = os.urandom(12)
    encrypted = _aesgcm().encrypt(nonce, secret.encode(), None)
    return encrypted, nonce


def decrypt_secret(encrypted: bytes, nonce: bytes) -> str:
    return _aesgcm().decrypt(nonce, encrypted, None).decode()


def key_hint(secret: str) -> str:
    return f"...{secret[-4:]}" if len(secret) >= 4 else "****"
