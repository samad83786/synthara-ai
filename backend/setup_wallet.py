"""Generate a Solana wallet for Synthara to receive payments."""
import json
import os
from pathlib import Path

WALLET_FILE = Path(__file__).parent / "synthara_wallet.json"

def generate_wallet():
    try:
        from solders.keypair import Keypair
        keypair = Keypair()
        pubkey = str(keypair.pubkey())
        secret = bytes(keypair).hex()
        wallet = {"public_key": pubkey, "private_key_hex": secret}
        with open(WALLET_FILE, "w") as f:
            json.dump(wallet, f, indent=2)
        os.chmod(WALLET_FILE, 0o600)
        print(f"Wallet created!")
        print(f"Public Key: {pubkey}")
        print(f"Saved to: {WALLET_FILE}")
        print(f"\nSet this env var:")
        print(f'SYNTHARA_WALLET="{pubkey}"')
        return wallet
    except ImportError:
        print("solders not installed. Install with: pip install solders")
        return None

if __name__ == "__main__":
    generate_wallet()
