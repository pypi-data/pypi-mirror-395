"""
VCL Python SDK - Verified Compute Ledger

A drop-in replacement for OpenAI and Anthropic clients that generates
cryptographically signed receipts for every inference request.

Usage:
    from vcl import VCLClient

    client = VCLClient(
        api_key="vcl_...",
        base_url="https://your-vcl-server.com"
    )

    # OpenAI-compatible
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )

    # Get the receipt
    receipt = client.last_receipt
    print(f"Receipt ID: {receipt['receipt_id']}")
"""

from .client import VCLClient
from .receipts import Receipt, verify_receipt
from .exceptions import VCLError, AuthenticationError, ReceiptNotFoundError

__version__ = "0.1.0"
__all__ = [
    "VCLClient",
    "Receipt",
    "verify_receipt",
    "VCLError",
    "AuthenticationError",
    "ReceiptNotFoundError",
]
