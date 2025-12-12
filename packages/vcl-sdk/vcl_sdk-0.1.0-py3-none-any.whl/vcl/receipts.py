"""VCL Receipt handling and verification"""

import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests

from .exceptions import ReceiptNotFoundError, VCLError


@dataclass
class Anchor:
    """On-chain anchor information"""

    type: str
    tx_hash: Optional[str] = None
    merkle_root: Optional[str] = None
    leaf_index: Optional[int] = None
    proof: Optional[List[str]] = None
    chain: Optional[str] = None
    block_num: Optional[int] = None


@dataclass
class TEEAttestation:
    """TEE attestation information"""

    type: str
    mr_enclave: Optional[str] = None
    hardware_id: Optional[str] = None
    timestamp: Optional[str] = None
    signature: Optional[str] = None


@dataclass
class Execution:
    """Execution details"""

    model_name: str
    input_tokens: int
    output_tokens: int
    compute_units: float
    latency_ms: Optional[int] = None


@dataclass
class Verification:
    """Verification information"""

    receipt_hash: str
    signature: str
    public_key: str
    algorithm: str = "ED25519"
    anchor: Optional[Anchor] = None


@dataclass
class Receipt:
    """VCL Receipt representing a verified inference request"""

    receipt_id: str
    vcl_version: str
    timestamp: str
    provider: Dict[str, str]
    execution: Execution
    verification: Verification
    tee_attestation: Optional[TEEAttestation] = None
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Receipt":
        """Create a Receipt from a dictionary"""
        execution_data = data.get("execution", {})
        execution = Execution(
            model_name=execution_data.get("model_name", ""),
            input_tokens=execution_data.get("input", {}).get("token_count", 0),
            output_tokens=execution_data.get("output", {}).get("token_count", 0),
            compute_units=execution_data.get("compute_units", 0.0),
            latency_ms=execution_data.get("latency_ms"),
        )

        verification_data = data.get("verification", {})
        anchor_data = verification_data.get("anchor")
        anchor = None
        if anchor_data and anchor_data.get("type") != "NONE":
            anchor = Anchor(
                type=anchor_data.get("type", ""),
                tx_hash=anchor_data.get("tx_hash"),
                merkle_root=anchor_data.get("merkle_root"),
                leaf_index=anchor_data.get("leaf_index"),
                proof=anchor_data.get("proof"),
                chain=anchor_data.get("chain"),
                block_num=anchor_data.get("block_num"),
            )

        verification = Verification(
            receipt_hash=verification_data.get("receipt_hash", ""),
            signature=verification_data.get("signature", ""),
            public_key=verification_data.get("public_key", ""),
            algorithm=verification_data.get("algorithm", "ED25519"),
            anchor=anchor,
        )

        tee_data = data.get("tee_attestation")
        tee_attestation = None
        if tee_data and tee_data.get("type"):
            tee_attestation = TEEAttestation(
                type=tee_data.get("type", ""),
                mr_enclave=tee_data.get("mr_enclave"),
                hardware_id=tee_data.get("hardware_id"),
                timestamp=tee_data.get("timestamp"),
                signature=tee_data.get("signature"),
            )

        return cls(
            receipt_id=data.get("receipt_id", ""),
            vcl_version=data.get("vcl_version", ""),
            timestamp=data.get("timestamp", ""),
            provider=data.get("provider", {}),
            execution=execution,
            verification=verification,
            tee_attestation=tee_attestation,
            metadata=data.get("metadata"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Receipt to dictionary"""
        result = {
            "receipt_id": self.receipt_id,
            "vcl_version": self.vcl_version,
            "timestamp": self.timestamp,
            "provider": self.provider,
            "execution": {
                "model_name": self.execution.model_name,
                "input": {"token_count": self.execution.input_tokens},
                "output": {"token_count": self.execution.output_tokens},
                "compute_units": self.execution.compute_units,
            },
            "verification": {
                "receipt_hash": self.verification.receipt_hash,
                "signature": self.verification.signature,
                "public_key": self.verification.public_key,
                "algorithm": self.verification.algorithm,
            },
        }

        if self.execution.latency_ms:
            result["execution"]["latency_ms"] = self.execution.latency_ms

        if self.verification.anchor:
            result["verification"]["anchor"] = {
                "type": self.verification.anchor.type,
                "tx_hash": self.verification.anchor.tx_hash,
                "merkle_root": self.verification.anchor.merkle_root,
                "leaf_index": self.verification.anchor.leaf_index,
                "proof": self.verification.anchor.proof,
                "chain": self.verification.anchor.chain,
                "block_num": self.verification.anchor.block_num,
            }

        if self.tee_attestation:
            result["tee_attestation"] = {
                "type": self.tee_attestation.type,
                "mr_enclave": self.tee_attestation.mr_enclave,
                "hardware_id": self.tee_attestation.hardware_id,
                "timestamp": self.tee_attestation.timestamp,
                "signature": self.tee_attestation.signature,
            }

        if self.metadata:
            result["metadata"] = self.metadata

        return result

    @property
    def is_anchored(self) -> bool:
        """Check if receipt is anchored on-chain"""
        return (
            self.verification.anchor is not None
            and self.verification.anchor.tx_hash is not None
        )

    @property
    def is_tee_attested(self) -> bool:
        """Check if receipt has TEE attestation"""
        return self.tee_attestation is not None

    @property
    def total_tokens(self) -> int:
        """Total tokens (input + output)"""
        return self.execution.input_tokens + self.execution.output_tokens


def verify_receipt(
    base_url: str,
    receipt_id: str,
) -> Dict[str, Any]:
    """
    Verify a receipt using the public verification endpoint.

    Args:
        base_url: The VCL server URL
        receipt_id: The receipt ID to verify

    Returns:
        Verification result dict with 'valid' boolean and receipt details

    Raises:
        ReceiptNotFoundError: If receipt not found
        VCLError: If verification fails
    """
    url = f"{base_url.rstrip('/')}/public/verify/{receipt_id}"

    try:
        response = requests.get(url, timeout=30)

        if response.status_code == 404:
            raise ReceiptNotFoundError(
                f"Receipt {receipt_id} not found",
                status_code=404,
            )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        raise VCLError(f"Verification request failed: {e}")


def verify_merkle_proof(
    leaf_hash: str,
    merkle_root: str,
    proof: List[str],
    leaf_index: int,
) -> bool:
    """
    Verify a Merkle proof locally.

    Args:
        leaf_hash: The hash of the leaf (receipt)
        merkle_root: The expected Merkle root
        proof: List of sibling hashes
        leaf_index: Index of the leaf in the tree

    Returns:
        True if proof is valid
    """
    current = bytes.fromhex(leaf_hash.replace("0x", ""))
    index = leaf_index

    for sibling_hex in proof:
        sibling = bytes.fromhex(sibling_hex.replace("0x", ""))

        if index % 2 == 0:
            # Current is left child
            combined = current + sibling
        else:
            # Current is right child
            combined = sibling + current

        current = hashlib.sha256(combined).digest()
        index //= 2

    computed_root = current.hex()
    expected_root = merkle_root.replace("0x", "")

    return computed_root == expected_root
