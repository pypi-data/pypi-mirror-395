# aevion-verify

**Zero-dependency cryptographic verification for Aevion AI proofs**

[![PyPI version](https://badge.fury.io/py/aevion-verify.svg)](https://badge.fury.io/py/aevion-verify)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Installation

```bash
pip install aevion-verify
```

---

## Quick Start

```python
from aevion_verify import AevionVerifier

# Initialize verifier
verifier = AevionVerifier()

# Verify a proof locally
proof = {
    "content_hash": "abc123...",
    "signature": "def456...",
    "public_key": "ghi789..."
}
is_valid = verifier.verify(proof, "AI output content")

if is_valid:
    print("Proof verified!")
else:
    print("Verification failed")
```

---

## Features

- **Ed25519 Signature Verification** - Industry-standard cryptographic signatures
- **SHA-256 Content Hashing** - Tamper detection
- **XGML Proof Support** - Human-readable proof format
- **Registry Verification** - Check proofs against blockchain registry

---

## API Reference

### `AevionVerifier`

```python
class AevionVerifier:
    def verify(self, proof: dict, content: str) -> bool:
        """Verify a proof against content."""

    def verify_from_registry(self, proof_id: str) -> dict:
        """Verify a proof from the Aevion registry."""

    def parse_xgml(self, xgml: str) -> dict:
        """Parse an XGML proof document."""
```

---

## Proof Structure

```python
{
    "proof_id": "aevion_abc123...",
    "content_hash": "sha256_hex_64_chars",
    "signature": "ed25519_hex_128_chars",
    "public_key": "ed25519_hex_64_chars",
    "timestamp": "2025-01-15T10:30:00Z",
    "model": "claude-3.5-sonnet",
    "domain": "healthcare",
    "algorithm": "Ed25519+SHA256"
}
```

---

## License

MIT - See [LICENSE](LICENSE) file.

---

## Links

- **Website:** https://aevion.ai
- **GitHub:** https://github.com/Aevion-ai/aevion-verify-py
- **Documentation:** https://docs.aevion.ai

---

*Built by Aevion LLC - Veteran-Owned, Making AI Verifiable*
