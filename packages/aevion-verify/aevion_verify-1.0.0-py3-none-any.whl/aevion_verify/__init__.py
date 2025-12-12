"""
aevion-verify - Zero-dependency cryptographic verification for AI proofs
MIT License
"""

import hashlib
import json
import ipaddress
from enum import Enum
from typing import Dict, Optional, Tuple, Union
from urllib.parse import urlparse
from dataclasses import dataclass
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives import serialization


class VerificationError(Enum):
    """Verification error types for clear error messaging."""

    INVALID_PROOF_FORMAT = "Proof is missing required fields (signature, public_key, content_hash)"
    MISSING_CONTENT = "Content is required for verification"
    HASH_MISMATCH = "Content hash doesn't match - the content may have been tampered with"
    INVALID_SIGNATURE = "Signature verification failed - the proof may be forged or corrupted"
    INVALID_PUBLIC_KEY = "Public key is malformed or invalid"
    EXPIRED_PROOF = "Proof has expired"
    REGISTRY_UNREACHABLE = "Could not reach the verification registry"
    INVALID_PROOF_ID = "Proof ID must be alphanumeric with underscores only"
    UNKNOWN_ERROR = "An unexpected error occurred during verification"


@dataclass
class VerificationResult:
    """Detailed verification result with error information."""

    valid: bool
    error: Optional[VerificationError] = None
    error_detail: Optional[str] = None
    proof_id: Optional[str] = None

    def __bool__(self) -> bool:
        return self.valid

    def __str__(self) -> str:
        if self.valid:
            return f"Verified (proof_id={self.proof_id})"
        return f"Failed: {self.error.value if self.error else 'Unknown error'}"

# Allowed registry hostnames (whitelist)
ALLOWED_REGISTRY_HOSTS = frozenset([
    "api.aevion.ai",
    "registry.aevion.ai",
    "localhost",  # For local development only
    "127.0.0.1",
])


def _validate_registry_url(url: str) -> None:
    """
    Validate registry URL to prevent SSRF attacks.

    Args:
        url: The URL to validate

    Raises:
        ValueError: If URL is not allowed
    """
    parsed = urlparse(url)

    # Must be HTTPS (or HTTP for localhost)
    if parsed.scheme not in ("https", "http"):
        raise ValueError(f"Invalid URL scheme: {parsed.scheme}. Must be https.")

    if parsed.scheme == "http" and parsed.hostname not in ("localhost", "127.0.0.1"):
        raise ValueError("HTTP is only allowed for localhost. Use HTTPS for remote registries.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Invalid URL: missing hostname")

    # Check against whitelist
    if hostname not in ALLOWED_REGISTRY_HOSTS:
        raise ValueError(
            f"Registry host '{hostname}' is not in the allowed list. "
            f"Allowed hosts: {', '.join(sorted(ALLOWED_REGISTRY_HOSTS))}"
        )

    # Block private IP ranges (additional protection)
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private and hostname not in ("127.0.0.1", "localhost"):
            raise ValueError(f"Private IP addresses are not allowed: {hostname}")
    except ValueError:
        # Not an IP address, hostname already validated via whitelist
        pass


class AevionVerifier:
    """Verify cryptographic proofs for AI outputs."""

    def verify(
        self, proof: Dict, content: str, detailed: bool = False
    ) -> Union[bool, VerificationResult]:
        """
        Verify a cryptographic proof.

        Args:
            proof: Dictionary containing signature, public_key, content_hash
            content: The original AI output that was proven
            detailed: If True, returns VerificationResult with error details

        Returns:
            bool if detailed=False, VerificationResult if detailed=True

        Example:
            >>> verifier = AevionVerifier()
            >>> result = verifier.verify(proof, content, detailed=True)
            >>> if not result:
            ...     print(f"Failed: {result.error.value}")
        """
        proof_id = proof.get("proof_id") if proof else None

        # Validate proof format
        if not proof or "signature" not in proof or "public_key" not in proof:
            if detailed:
                return VerificationResult(
                    valid=False,
                    error=VerificationError.INVALID_PROOF_FORMAT,
                    proof_id=proof_id,
                )
            return False

        # Validate content
        if not content:
            if detailed:
                return VerificationResult(
                    valid=False,
                    error=VerificationError.MISSING_CONTENT,
                    proof_id=proof_id,
                )
            return False

        try:
            # Recreate content hash
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            expected_hash = proof.get("content_hash", "")

            # Verify hash matches
            if content_hash != expected_hash:
                if detailed:
                    return VerificationResult(
                        valid=False,
                        error=VerificationError.HASH_MISMATCH,
                        error_detail=f"Expected {expected_hash[:16]}..., got {content_hash[:16]}...",
                        proof_id=proof_id,
                    )
                return False

            # Verify Ed25519 signature
            try:
                signature = bytes.fromhex(proof["signature"])
                public_key_bytes = bytes.fromhex(proof["public_key"])
            except ValueError as e:
                if detailed:
                    return VerificationResult(
                        valid=False,
                        error=VerificationError.INVALID_PUBLIC_KEY,
                        error_detail=str(e),
                        proof_id=proof_id,
                    )
                return False

            message = expected_hash.encode("utf-8")

            try:
                public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
                public_key.verify(signature, message)
            except Exception:
                if detailed:
                    return VerificationResult(
                        valid=False,
                        error=VerificationError.INVALID_SIGNATURE,
                        proof_id=proof_id,
                    )
                return False

            # Success!
            if detailed:
                return VerificationResult(valid=True, proof_id=proof_id)
            return True

        except Exception as e:
            if detailed:
                return VerificationResult(
                    valid=False,
                    error=VerificationError.UNKNOWN_ERROR,
                    error_detail=str(e),
                    proof_id=proof_id,
                )
            return False

    def verify_from_registry(
        self,
        proof_id: str,
        registry_url: str = "https://api.aevion.ai"
    ) -> Dict:
        """
        Verify a proof from the blockchain registry.

        Args:
            proof_id: The proof identifier
            registry_url: Optional custom registry URL (must be in allowed list)

        Returns:
            Dictionary with verification result and details

        Raises:
            ValueError: If registry_url is not in the allowed list
        """
        import requests

        # Validate URL to prevent SSRF
        _validate_registry_url(registry_url)

        # Sanitize proof_id (alphanumeric and underscores only)
        if not proof_id or not all(c.isalnum() or c == '_' for c in proof_id):
            return {'valid': False, 'error': 'Invalid proof_id format'}

        try:
            response = requests.get(
                f"{registry_url}/proofs/{proof_id}/verify",
                timeout=10  # Add timeout to prevent slowloris attacks
            )
            result = response.json()

            if result.get('verified'):
                return {
                    'valid': True,
                    'proof': result['proof'],
                    'ipfs_hash': result['ipfsHash'],
                    'blockchain_tx': result['blockchainTx'],
                    'timestamp': result['timestamp']
                }

            return {'valid': False, 'error': result.get('error')}

        except Exception as e:
            return {'valid': False, 'error': str(e)}

    def get_proof_details(
        self,
        proof_id: str,
        registry_url: str = "https://api.aevion.ai"
    ) -> Dict:
        """
        Get proof details without verification.

        Args:
            proof_id: The proof identifier
            registry_url: Optional custom registry URL (must be in allowed list)

        Returns:
            Proof metadata dictionary

        Raises:
            ValueError: If registry_url is not in the allowed list
        """
        import requests

        # Validate URL to prevent SSRF
        _validate_registry_url(registry_url)

        # Sanitize proof_id
        if not proof_id or not all(c.isalnum() or c == '_' for c in proof_id):
            return {'error': 'Invalid proof_id format'}

        response = requests.get(
            f"{registry_url}/proofs/{proof_id}",
            timeout=10
        )
        return response.json()


# Example usage
if __name__ == "__main__":
    verifier = AevionVerifier()

    # Example proof
    example_proof = {
        "content_hash": "abc123...",
        "signature": "def456...",
        "public_key": "ghi789..."
    }

    example_content = "The quick brown fox jumps over the lazy dog."

    is_valid = verifier.verify(example_proof, example_content)
    print(f"Proof valid: {is_valid}")
