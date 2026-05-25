"""Generate Solana wallet for Synthara — pure Python, no deps."""
import json
import os
import hashlib
from pathlib import Path

ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def b58encode(b):
    n = int.from_bytes(b, 'big')
    chars = []
    while n:
        n, r = divmod(n, 58)
        chars.append(ALPHABET[r])
    for byte in b:
        if byte == 0:
            chars.append(ALPHABET[0])
        else:
            break
    return ''.join(reversed(chars))

def generate_ed25519_keypair():
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    private_key = ed25519.Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    return private_bytes, public_bytes

WALLET_FILE = Path(__file__).parent / "synthara_wallet.json"

priv, pub = generate_ed25519_keypair()
address = b58encode(pub)

wallet = {
    "public_key": address,
    "private_key_hex": priv.hex(),
    "public_key_bytes": pub.hex(),
}

with open(WALLET_FILE, "w") as f:
    json.dump({"public_key": address, "private_key_hex": priv.hex()}, f, indent=2)

print(f"Synthara Wallet Created!")
print(f"Address: {address}")
print(f"Saved to: {WALLET_FILE}")
print(f"")
print(f"Set this environment variable:")
print(f'SYNTHARA_WALLET="{address}"')
