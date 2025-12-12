# VCL Python SDK

A drop-in replacement for OpenAI and Anthropic clients that generates cryptographically signed receipts for every AI inference request.

## Installation

```bash
pip install vcl-sdk
```

Or install from source:

```bash
cd sdk/python
pip install -e .
```

## Quick Start

```python
from vcl import VCLClient

# Initialize client
client = VCLClient(
    api_key="vcl_your_api_key",
    base_url="https://your-vcl-server.com"
)

# OpenAI-compatible usage
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response["choices"][0]["message"]["content"])

# Get the receipt for this request
receipt = client.last_receipt
print(f"Receipt ID: {receipt.receipt_id}")
print(f"Input tokens: {receipt.execution.input_tokens}")
print(f"Output tokens: {receipt.execution.output_tokens}")
print(f"Compute units: {receipt.execution.compute_units}")
```

## Anthropic-Compatible Usage

```python
from vcl import VCLClient

client = VCLClient(
    api_key="vcl_your_api_key",
    base_url="https://your-vcl-server.com"
)

response = client.messages.create(
    model="claude-3-sonnet-20240229",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=1024
)

print(response["content"][0]["text"])
```

## Streaming

```python
# OpenAI streaming
for chunk in client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
):
    if chunk.get("choices"):
        content = chunk["choices"][0].get("delta", {}).get("content", "")
        print(content, end="", flush=True)

# Anthropic streaming
for chunk in client.messages.create(
    model="claude-3-sonnet-20240229",
    messages=[{"role": "user", "content": "Tell me a story"}],
    max_tokens=1024,
    stream=True
):
    if chunk.get("type") == "content_block_delta":
        print(chunk["delta"]["text"], end="", flush=True)
```

## Receipt Verification

```python
from vcl import VCLClient, verify_receipt

client = VCLClient(api_key="vcl_...", base_url="https://...")

# Make a request
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Verify the receipt
result = client.verify_receipt(client.last_receipt_id)
print(f"Valid: {result['valid']}")
print(f"Model: {result['model']}")
print(f"Timestamp: {result['timestamp']}")

# Or verify any receipt by ID (public endpoint)
result = verify_receipt("https://your-vcl-server.com", "receipt-id-here")
```

## Receipt Details

```python
receipt = client.last_receipt

# Basic info
print(f"Receipt ID: {receipt.receipt_id}")
print(f"Timestamp: {receipt.timestamp}")
print(f"Provider: {receipt.provider['name']}")

# Execution details
print(f"Model: {receipt.execution.model_name}")
print(f"Input tokens: {receipt.execution.input_tokens}")
print(f"Output tokens: {receipt.execution.output_tokens}")
print(f"Total tokens: {receipt.total_tokens}")
print(f"Compute units: {receipt.execution.compute_units}")

# Verification
print(f"Receipt hash: {receipt.verification.receipt_hash}")
print(f"Signature: {receipt.verification.signature}")

# On-chain anchor (if available)
if receipt.is_anchored:
    anchor = receipt.verification.anchor
    print(f"Chain: {anchor.chain}")
    print(f"TX Hash: {anchor.tx_hash}")
    print(f"Block: {anchor.block_num}")
    print(f"Merkle Root: {anchor.merkle_root}")

# TEE attestation (if available)
if receipt.is_tee_attested:
    tee = receipt.tee_attestation
    print(f"TEE Type: {tee.type}")
    print(f"MR Enclave: {tee.mr_enclave}")
```

## API Key Management

```python
# List your API keys
keys = client.list_api_keys()
for key in keys["keys"]:
    print(f"{key['name']}: {key['key_prefix']}...")

# Create a new key
new_key = client.create_api_key(name="Production")
print(f"New key: {new_key['key']}")  # Save this!

# Delete a key
client.delete_api_key(key_id="key-id-here")
```

## Usage Statistics

```python
stats = client.get_stats()
print(f"Total receipts: {stats['total_receipts']}")
print(f"Total compute units: {stats['total_compute_units']}")
```

## Error Handling

```python
from vcl import VCLClient, VCLError, AuthenticationError, RateLimitError

client = VCLClient(api_key="vcl_...", base_url="https://...")

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded, try again later")
except VCLError as e:
    print(f"Error: {e.message} (status: {e.status_code})")
```

## Local Merkle Proof Verification

```python
from vcl.receipts import verify_merkle_proof

receipt = client.last_receipt

if receipt.is_anchored:
    # Verify the Merkle proof locally
    is_valid = verify_merkle_proof(
        leaf_hash=receipt.verification.receipt_hash,
        merkle_root=receipt.verification.anchor.merkle_root,
        proof=receipt.verification.anchor.proof,
        leaf_index=receipt.verification.anchor.leaf_index,
    )
    print(f"Merkle proof valid: {is_valid}")
```

## License

MIT
