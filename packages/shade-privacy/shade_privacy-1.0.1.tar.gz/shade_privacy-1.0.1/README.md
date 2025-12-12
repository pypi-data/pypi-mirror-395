
```markdown
# Shade Privacy Python SDK

Python SDK for private, cross-chain transactions with zero-knowledge proofs. Break sender-receiver links across 20+ blockchains.

## Features

- 🛡️ **True Privacy**: Break sender-receiver link with ZK proofs
- 🔗 **Multi-Chain**: ETH, SOL, StarkNet, Base, Sei, AVAX, SUI, +13 more
- ⚡ **Simple API**: Intent-based transactions, real-time WebSocket updates
- 🔐 **Secure**: End-to-end encryption, HMAC signing, enterprise-ready

## Installation

```bash
pip install shade-privacy
```

## Quick Start

```python
from shade_privacy import ZKIntentSDK

# Initialize
sdk = ZKIntentSDK(
    api_key="your_api_key",
    hmac_secret="your_hmac_secret"
)

# Create private intent
payload = {
    "recipient": "0x...",
    "amount": 1.5,
    "token": "ETH",
    "walletType": "starknet"  # or 'eip-155', 'solana', etc.
}

result = sdk.create_intent(
    payload=payload,
    wallet_signature="0x...",
    metadata={"note": "Private payment"}
)

print(f"✅ Intent ID: {result.get('intentId')}")
```

## Supported Chains

- **Ethereum** (`eip-155`)
- **Solana** (`solana`)
- **StarkNet** (`starknet`)
- **Base** (`eip-155`)
- **Sei** (`sei`)
- **Avalanche** (`eip-155`)
- **Sui** (`sui`)
- **Polygon, Arbitrum, Optimism, BNB Chain, +12 more**

## Documentation

Full documentation: [docs.shadeprivacy.com](https://docs.shadeprivacy.com)

## License

MIT License - see [LICENSE](LICENSE)
```

## For PyPI (setup.py short description):

```python
setup(
    name="shade-privacy",
    version="1.0.0",
    description="Python SDK for private cross-chain transactions with ZK proofs. Supports ETH, SOL, StarkNet, Base, Sei, AVAX, SUI + 13 chains.",
    # ... rest of setup
)
```

## Version checking snippet for docs:

```python
import shade_privacy
print(f"Shade Privacy SDK version: {shade_privacy.__version__}")

# Check if compatible
from packaging import version
current = version.parse(shade_privacy.__version__)
required = version.parse("1.0.0")
if current >= required:
    print("✅ Version compatible")
```
