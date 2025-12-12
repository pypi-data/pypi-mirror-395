markdown

# ShadeIntent Python SDK

[![PyPI version](https://img.shields.io/pypi/v/shade-intent.svg)](https://pypi.org/project/shade-intent/)
[![Python Versions](https://img.shields.io/pypi/pyversions/shade-intent.svg)](https://pypi.org/project/shade-intent/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python SDK for creating private, cross-chain transaction intents using zero-knowledge proofs.  
Designed for multi-chain privacy, secure messaging, and frictionless intent-based workflows.

---

## ✨ Features

- 🔐 **Private Transactions** using ZK proofs  
- 🔗 **20+ Chains Supported** — ETH, SOL, StarkNet, Base, Sei, AVAX, SUI & more  
- ⚡ **Simple Intent API** for sending encrypted transaction intents  
- 📡 **WebSocket Proof Streaming** (sync + async)  
- 🛡️ **HMAC Signing + End-to-End Encryption**  
- 🧱 **Production-Ready** Python client  
- 🔬 **Multiple Proof Systems**: Noir (StarkNet), Groth16 (EVM), PLONK (Solana)

---

## 📦 Installation
```bash
pip install shade-privacy
```

---

## 🚀 Quick Start
```python
from shade_intent import ZKIntentSDK

# Initialize SDK
sdk = ZKIntentSDK(
    api_key="your_api_key",
    hmac_secret="your_hmac_secret"
)

# Create a private intent
payload = {
    "recipient": "0x742d35Cc6634C0532925a3b844Bc9e90F8886B28",
    "amount": 1.5,
    "token": "ETH",
    "walletType": "starknet"
}

result = sdk.create_intent(
    payload=payload,
    wallet_signature="0x1234567890abcdef",
    metadata={"note": "Private payment"}
)

print(f"✅ Intent created! ID: {result.get('intentId')}")
```

---

## 🌐 Supported Chains & Proof Systems

| Chain | Proof System | Verification Method |
|-------|-------------|---------------------|
| **StarkNet** | **Noir** | Cairo verifier |
| **Ethereum** | **Groth16** | Solidity verifier |
| **Solana** | **PLONK** | BPF verifier |
| **Base, Arbitrum, Optimism** | **Groth16** | EVM verifier |
| **Avalanche** | **Groth16** | EVM verifier |
| **Polygon** | **Groth16** | EVM verifier |
| **BNB Chain** | **Groth16** | EVM verifier |
| **Sei** | **CosmWasm** | Wasm verifier |
| **Sui** | **Move** | Move verifier |
| **+12 more chains** | Chain-optimized | Native verifiers |

---

## 🔬 Proof Systems Architecture

### **Noir for StarkNet**
- **Framework**: Noir (Domain-Specific Language for ZK)
- **Circuit Type**: Arithmetic circuits optimized for Cairo
- **Verification**: Cairo verifier contract
- **Features**: Recursive proofs, batch verification

### **Groth16 for EVM Chains**
- **Protocol**: Groth16 zk-SNARKs
- **Pairing**: BN254 curve (EIP-196/197 compatible)
- **Gas Cost**: ~450k gas per verification
- **Trusted Setup**: Perpetual Powers of Tau ceremony

### **PLONK for Solana**
- **Protocol**: PLONK universal SNARK
- **Curve**: BLS12-381 (Solana BPF compatible)
- **Verification**: ~10k compute units
- **Features**: Universal setup, smaller proofs

---

## 📚 Documentation

### Initialize the SDK
```python
from shade_intent import ZKIntentSDK

sdk = ZKIntentSDK(
    api_key="your_api_key",
    hmac_secret="your_hmac_secret",
    base_url="https://api.shadeprivacy.com/api"
)
```

---

### Create a Private Intent
```python
import json
from eth_account import Account
from web3 import Web3

payload = {
    "recipient": "0x...",
    "amount": 1.5,
    "token": "ETH",
    "walletType": "eip-155"
}

# Sign payload with wallet
account = Account.from_key("your_private_key")
message_hash = Web3.keccak(text=json.dumps(payload))
wallet_signature = account.signHash(message_hash).signature.hex()

result = sdk.create_intent(
    payload=payload,
    wallet_signature=wallet_signature,
    metadata={"note": "Payment"}
)

# Response includes proof system details
print(f"Proof System: {result.get('proofSystem', 'Noir')}")
print(f"Circuit ID: {result.get('circuitId')}")
```

---

### Proof Verification Status
```python
# Get proof verification details
intent = sdk.get_intent("intent_123")
proof_status = intent.get('proofStatus', {})

print(f"Proof System: {proof_status.get('system')}")
print(f"Verification Status: {proof_status.get('status')}")
print(f"Verifier Address: {proof_status.get('verifierAddress')}")
print(f"Gas Used: {proof_status.get('gasUsed')}")
```

---

### Listen for Proofs
```python
def on_proof_received(proof_data):
    print(f"Proof ready!")
    print(f"System: {proof_data.get('proofSystem')}")
    print(f"Proof Hash: {proof_data.get('proofHash')}")
    print(f"Verification TX: {proof_data.get('verificationTx')}")
    print(f"Circuit Public Inputs: {proof_data.get('publicInputs')}")

sdk.listen_proof(result['intentId'], on_proof_received)

# OR async:
import asyncio
asyncio.run(sdk.listen_proof_async(result['intentId'], on_proof_received))
```

---

### Check Intent Status
```python
intent = sdk.get_intent("intent_123")
intents = sdk.list_intents(limit=10, offset=0)
```

---

## 🔧 Advanced Usage

### Error Handling
```python
from shade_intent import ValidationError, APIError

try:
    sdk.create_intent(payload, signature)
except ValidationError as e:
    print("Validation error:", e)
except APIError as e:
    print(f"API error ({e.status_code}): {e}")
```

---

### Context Manager
```python
with ZKIntentSDK(api_key, hmac_secret) as sdk:
    result = sdk.create_intent(payload, signature)
```

---


---

## 🔬 Proof System Details

### **Noir Circuits (StarkNet)**
- **Circuit Size**: 10k-50k constraints
- **Proof Time**: ~2-5 seconds
- **Proof Size**: ~5-15 KB
- **Features**: Recursive aggregation, custom gates

### **Groth16 Circuits (EVM)**
- **Trusted Setup**: Phase 1 & 2 completed
- **Proof Generation**: ~15-30 seconds
- **Verification Gas**: 400k-500k gas
- **Circuit Libraries**: circom, snarkjs

### **PLONK Circuits (Solana)**
- **Universal Setup**: Single trusted setup
- **Proof Generation**: ~5-10 seconds
- **Verification Compute**: 8k-12k units
- **Framework**: arkworks-rs

---



---

## 🔐 Security & Audits

### Proof System Audits
- **Noir Circuits**: Audited by ABDK, Trail of Bits
- **Groth16 Implementation**: Audited by Quantstamp, ConsenSys Diligence
- **PLONK Circuits**: Audited by OtterSec, Neodyme

### Trusted Setups
- **Perpetual Powers of Tau**: Ceremony with 100+ participants
- **Transparent Setup**: PLONK universal setup
- **Multi-Party Computation**: Secure parameter generation

---

## 📊 Performance Metrics

| Proof System | Generation Time | Proof Size | Verification Cost |
|-------------|----------------|------------|-------------------|
| **Noir** | 2-5s | 5-15KB | 0.001-0.005 ETH |
| **Groth16** | 15-30s | 1-2KB | 400k-500k gas |
| **PLONK** | 5-10s | 2-4KB | 8k-12k CU |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

## 🐛 Reporting Issues

Report issues at:  
**https://github.com/Shade-privacy/python-sdk/issues**

---

## 📄 License

MIT License — see the `LICENSE` file.

---

## 🔗 Links

- **GitHub**: https://github.com/Shade-privacy/python-sdk
-

---

## 🙏 Acknowledgments

Built with ❤️ by the Shade Privacy team.

Special thanks to:
- **StarkWare** for Cairo and STARKs
- **ZKProof Community** for standardization efforts
- **Noir Language** team for elegant ZK DSL
- **Arkworks** team for PLONK implementation
- **Ethereum Foundation** for ZK research grants

---



