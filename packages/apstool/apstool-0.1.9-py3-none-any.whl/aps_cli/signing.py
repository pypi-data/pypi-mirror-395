import os, base64
from pathlib import Path
try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
    from cryptography.hazmat.primitives import serialization
except Exception as e:
    raise SystemExit("pip install cryptography")

KEY_DIR = Path.home()/".aps"/"keys"
PRIV = KEY_DIR/"ed25519.key"
PUB = KEY_DIR/"ed25519.pub"

def ensure_keypair():
    KEY_DIR.mkdir(parents=True, exist_ok=True)
    if PRIV.exists() and PUB.exists(): return
    sk = Ed25519PrivateKey.generate()
    pk = sk.public_key()
    PRIV.write_bytes(sk.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    ))
    PUB.write_bytes(pk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    ))

def load_privkey():
    ensure_keypair()
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    return Ed25519PrivateKey.from_private_bytes(PRIV.read_bytes())

def load_pubkey():
    ensure_keypair()
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    return Ed25519PublicKey.from_public_bytes(PUB.read_bytes())

def ed25519_sign(sk, payload: bytes) -> bytes:
    return sk.sign(payload)

def ed25519_verify(pk, payload: bytes, sig: bytes) -> bool:
    try:
        pk.verify(sig, payload); return True
    except Exception:
        return False
