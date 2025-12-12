# VectorForge Python SDK

Official Python client for [VectorForge Cloud APIs](https://vectorforge.ai).

VectorForge is a **trust and confidence layer for AI and automations**, providing:
- **DIVTs (Digital Integrity Verification Tokens)** - Cryptographic "birth certificates" for data
- **AI Answer Confidence Scoring** - Privacy-preserving and comprehensive scoring  
- **Worldstate Logging** - Immutable event capture for AI operations
- **Hybrid Post-Quantum Cryptography** - ECDSA P-521 + ML-DSA-65 signatures

---

## Installation

### From PyPI (Recommended)

```bash
pip install vectorforgeai
```

For image support:

```bash
pip install vectorforgeai[image]
```

### From Source (Development)

```bash
git clone https://github.com/VectorForgeAI/API
cd API/sdk/python
pip install -e .
```

---

## Quick Start

### Configuration

```python
from vectorforge import VectorForgeClient

# Option 1: Use environment variables (recommended)
# export VF_API_BASE_URL="https://api.vectorforge.ai"
# export VF_API_KEY="vf_prod_YourApiKeyHere"
client = VectorForgeClient()

# Option 2: Pass config directly
client = VectorForgeClient(
    base_url="https://api.vectorforge.ai",
    api_key="vf_prod_YourApiKeyHere",
)

# Option 3: Context manager (auto cleanup)
with VectorForgeClient() as client:
    result = client.register_content(
        object_id="doc-123",
        text="Hello, World!",
        data_type="prompt_receipt_v1",
    )
```

---

## High-Level API (Recommended)

The SDK provides high-level methods that handle **canonicalization and hashing automatically**. These are the recommended way to use VectorForge.

### Register Text Content

```python
from vectorforge import VectorForgeClient

with VectorForgeClient() as client:
    result = client.register_content(
        object_id="prompt:123",
        text="What is the capital of France?",
        data_type="prompt_receipt_v1",
        metadata={"user_id": "user-456", "session": "sess-789"},
    )
    
    print(f"DIVT ID: {result['divt_id']}")
    print(f"ECDSA signature: {result['ecdsa_sig_b64'][:32]}...")
    print(f"ML-DSA signature: {result['ml_dsa_sig_b64'][:32]}...")
    print(f"Ledger status: {result['ledger_status']}")
```

**What it does:**
1. Normalizes text (Unicode NFC, line endings, trim whitespace)
2. Computes SHA3-512 hash
3. Creates DIVT with hybrid post-quantum signatures
4. Returns `divt_id` for future verification

---

### Register JSON Data

```python
result = client.register_json(
    object_id="rag_snapshot:v42",
    data={
        "snapshot_type": "rag-corpus",
        "doc_hashes": ["hash1", "hash2"],
        "index_hash": "index_hash_value",
        "timestamp": "2025-11-21T10:00:00Z",
    },
    data_type="rag_snapshot_v1",
    metadata={"project": "hr-assistant", "env": "prod"},
)

print(f"RAG snapshot registered: {result['divt_id']}")
```

**What it does:**
1. Canonical JSON serialization (sorted keys, minimal whitespace)
2. Computes SHA3-512 hash
3. Creates DIVT

---

### Register Embedding Vector

```python
result = client.register_embedding(
    object_id="chunk:doc-123:p5",
    embedding=[0.123456, -0.987654, 0.456789, ...],  # Your embedding vector
    data_type="rag_chunk_v1",
    metadata={"document_id": "doc-123", "paragraph": 5},
    precision=6,  # Decimal places for deterministic hashing
)

print(f"Embedding registered: {result['divt_id']}")
```

**What it does:**
1. Validates embedding (rejects NaN/Infinity)
2. Formats with fixed precision for deterministic hashing
3. Computes SHA3-512 hash
4. Creates DIVT

---

### Register Image

**Requires:** `pip install vectorforgeai[image]`

```python
with open("receipt.png", "rb") as f:
    image_bytes = f.read()

result = client.register_image(
    object_id="image:receipt-456",
    image_bytes=image_bytes,
    data_type="image_receipt_v1",
    metadata={"source": "mobile_app", "user_id": "user-789"},
    max_dimension=1024,  # Resize to max 1024px
)

print(f"Image registered: {result['divt_id']}")
```

**What it does:**
1. Decodes image (supports PNG, JPEG, WebP)
2. Normalizes to sRGB color space
3. Resizes if needed (preserves aspect ratio)
4. Re-encodes as deterministic PNG
5. Computes SHA3-512 hash
6. Creates DIVT

---

## Complete Example: Prompt Receipt with Verification

```python
from vectorforge import VectorForgeClient

with VectorForgeClient() as client:
    # Register AI prompt + response
    prompt_data = {
        "prompt": "What is the capital of France?",
        "response": "Paris",
        "model": "gpt-4",
        "timestamp": "2025-11-21T10:00:00Z",
    }
    
    register_result = client.register_json(
        object_id="prompt_receipt:flow-abc-123",
        data=prompt_data,
        data_type="prompt_receipt_v1",
        metadata={"workflow": "customer_support"},
    )
    
    divt_id = register_result["divt_id"]
    print(f"✓ Prompt receipt registered: {divt_id}")
    
    # Later: Verify the prompt receipt
    verify_result = client.verify_json(
        divt_id=divt_id,
        data=prompt_data,
    )
    
    if verify_result["verified"]:
        print("✓ DIVT is valid")
        print(f"  - Hash valid: {verify_result['hash_valid']}")
        print(f"  - ECDSA signature valid: {verify_result['ecdsa_signature_valid']}")
        print(f"  - ML-DSA signature valid: {verify_result['ml_dsa_signature_valid']}")
        print(f"  - Object ID: {verify_result['object_id']}")
        print(f"  - Created: {verify_result['created_at']}")
        print(f"  - Ledger status: {verify_result['ledger_status']}")
    else:
        print("✗ DIVT verification failed")
        print(f"  - Hash valid: {verify_result['hash_valid']}")
        print(f"  - Revoked: {verify_result['revoked']}")
```

---

## Low-Level API (Advanced)

For advanced use cases where you want to **compute hashes yourself**, use the low-level `register()` method:

```python
from vectorforge import canon

# Compute hash manually
text = "Hello, World!"
hash_b64 = canon.hash_content_v1(text)

# Register with pre-computed hash
result = client.register({
    "object_id": "doc-123",
    "hash_mode": "content",
    "hash_version": "content_v1",
    "hash_b64": hash_b64,
    "data_type": "prompt_receipt_v1",
})
```

### Canonicalization Utilities

```python
from vectorforge import canon

# Text canonicalization
hash_b64 = canon.hash_content_v1("Hello, World!")

# JSON canonicalization
hash_b64 = canon.hash_json_v1({"key": "value", "nested": {"a": 1}})

# Embedding canonicalization
hash_b64 = canon.hash_embedding_v1([0.1, 0.2, 0.3], precision=6)

# Image canonicalization (requires Pillow)
with open("image.png", "rb") as f:
    hash_b64 = canon.hash_image_v1(f.read(), max_dimension=1024)

# Or get canonical bytes without hashing
canonical_bytes = canon.canonicalize_content_v1("Hello")
hash_b64 = canon.sha3_512_digest(canonical_bytes)
```

---

## Verification

### Verify a Single DIVT

```python
# Using hash_b64 (advanced)
result = client.verify({
    "divt_id": "019abc12-3456-7890-abcd-ef0123456789",
    "hash_b64": "your-precomputed-hash-base64",
})

if result["verified"]:
    print("✓ DIVT is valid")
    print(f"  - Hash valid: {result['hash_valid']}")
    print(f"  - ECDSA valid: {result['ecdsa_signature_valid']}")
    print(f"  - ML-DSA valid: {result['ml_dsa_signature_valid']}")
    print(f"  - Revoked: {result['revoked']}")
else:
    print("✗ DIVT verification failed")
```

### Verify with High-Level Helpers

```python
# Verify text content
result = client.verify_content(divt_id, "Hello, World!")

# Verify JSON data
result = client.verify_json(divt_id, {"key": "value"})
```

---

## Bundle API

Get comprehensive verification bundles for DIVTs including worldstate context and scoring results.

### Get Bundle by DIVT ID

```python
bundle = client.get_bundle({
    "divt_id": "019abc12-3456-7890-abcd-ef0123456789",
})

print("DIVT Verification:")
print(f"  - Verified: {bundle['divt']['verified']}")
print(f"  - Hash valid: {bundle['divt']['hash_valid']}")
print(f"  - Ledger status: {bundle['divt']['ledger_status']}")

print(f"Worldstate events: {len(bundle['worldstate'])}")
print(f"Scoring events: {len(bundle['scoring'])}")
print(f"Generated at: {bundle['generated_at']}")
```

### Get Bundle by Object ID

```python
bundle = client.get_bundle({
    "object_id": "prompt_receipt:flow-abc-123",
    "include_history": True,
})
```

---

## Scoring API

### Privacy Score (No Raw Content Sent)

```python
result = client.score_privacy({
    "query_id": "query-123",
    "answer_id": "answer-456",
    "evidence": [
        {
            "object_id": "chunk:doc-1:p1",
            "divt_id": "019abc...",
            "tenant_id": "my-tenant",
            "similarity": 0.95,
            "chunk_confidence": 0.9,
        },
    ],
})

print(f"Overall confidence: {result['overall_confidence']}")
print(f"Semantic confidence: {result['semantic_confidence']}")
print(f"Integrity score: {result['integrity_score']}")
print(f"Verified count: {result['verified_count']}/{result['vector_count']}")
```

### Full Score (With Groq Judge)

```python
result = client.score_full({
    "query": "What is the capital of France?",
    "answer": "The capital of France is Paris.",
    "evidence": [
        {
            "object_id": "chunk:doc-1:p1",
            "divt_id": "019abc...",
            "tenant_id": "my-tenant",
            "text": "Paris is the capital city of France.",
            "similarity": 0.95,
        },
    ],
    "options": {
        "log_worldstate": "minimal",
    },
})

print(f"Overall confidence: {result['overall_confidence']}")
print(f"Support score: {result.get('support_score')}")
print(f"Faithfulness score: {result.get('faithfulness_score')}")
```

---

## Worldstate Read

### Get Single Worldstate Record

```python
# Get worldstate record metadata
item = client.get_worldstate_item({
    "wsl_id": "019abc12-3456-7890-abcd-ef0123456789",
})

print(f"Kind: {item['kind']}")
print(f"Timestamp: {item['timestamp']}")
print(f"Ledger status: {item['ledger_status']}")
print(f"Summary: {item.get('data_summary')}")

# Get worldstate record with full data from S3
item_with_data = client.get_worldstate_item({
    "wsl_id": "019abc12-3456-7890-abcd-ef0123456789",
    "include_data": True,
})

print("Full data:", item_with_data.get("data"))
```

### List Worldstate Records

```python
# List all records
result = client.list_worldstate()
print(f"Found {result['count']} records")

# List with filters
prompt_receipts = client.list_worldstate({
    "kind": "prompt_receipt",
    "created_from": "2025-11-01T00:00:00Z",
    "created_to": "2025-11-30T23:59:59Z",
    "limit": 50,
})

# Paginate through all results
cursor = prompt_receipts.get("cursor")
while cursor:
    page = client.list_worldstate({"cursor": cursor})
    for item in page["items"]:
        print(f"{item['wsl_id']}: {item.get('data_summary')}")
    cursor = page.get("cursor")
```

**Available Filters:**
- `kind`: Filter by event type (`prompt_receipt`, `scoring_event`, `rag_snapshot`, etc.)
- `created_from`: Start of time range (ISO 8601)
- `created_to`: End of time range (ISO 8601)
- `limit`: Page size (max 100, default 50)
- `cursor`: Pagination cursor from previous response

---

## Stream Events (SSE)

```python
from datetime import datetime, timedelta

def handle_event(event):
    print(f"[{event['type']}] {event['id']} at {event['timestamp']}")

one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z"

client.stream_events(
    {
        "since": one_hour_ago,
        "types": ["divt_registered", "scoring_event"],
        "limit": 50,
    },
    on_event=handle_event,
)
```

---

## Error Handling

```python
from vectorforge import VectorForgeClient, VectorForgeAPIError

client = VectorForgeClient()

try:
    result = client.register_content(
        object_id="doc-123",
        text="Hello, World!",
        data_type="prompt_receipt_v1",
    )
except VectorForgeAPIError as e:
    print(f"API Error: {e.message}")
    print(f"Status: {e.status_code}")
    print(f"Code: {e.error}")
    if e.details:
        print(f"Details: {e.details}")
except ValueError as e:
    print(f"Validation Error: {e}")
except ImportError as e:
    print(f"Missing Dependency: {e}")
```

**Common Error Codes:**
- `invalid_api_key` (401) - API key invalid or expired
- `quota_exceeded` (429) - Monthly request limit reached
- `rate_limit_exceeded` (429) - Too many requests
- `plan_limitation` (403) - Feature not available on your plan
- `network_error` (0) - Network connectivity issue

---

## Type Hints

Full type support for Python 3.9+:

```python
from vectorforge import (
    VectorForgeClient,
    VectorForgeAPIError,
    RegisterInput,
    RegisterResult,
    VerifyInput,
    VerifyResult,
    BundleInput,
    BundleResult,
    PrivacyScoreInput,
    FullScoreInput,
    ScoreResult,
    StreamEventsInput,
    StreamEvent,
)
```

---

## Integration Tests

To run integration tests against the live API:

```bash
export VF_API_BASE_URL="https://api.vectorforge.ai"
export VF_API_KEY="your-api-key"
cd sdk/python
pip install -e ".[dev]"
pytest tests/test_integration.py -v
```

---

## Requirements

- **Python**: >= 3.9
- **Dependencies**:
  - `requests` >= 2.28.0
- **Optional**:
  - `Pillow` >= 10.0.0 (for image registration)

---

## Related Documentation

- **[API Reference](../../docs/API_REFERENCE.md)** - Complete HTTP API documentation
- **[Implementation Plan](../../docs/VectorForge%20API%20V2%20Implementation%20Plan.md)** - Full system specification
- **[Node SDK](../node/README.md)** - Node.js/TypeScript SDK

---

## Support

- **Issues**: [GitHub Issues](https://github.com/vectorforge/api/issues)
- **Website**: [https://vectorforge.ai](https://vectorforge.ai)

---

## License

MIT © VectorForge
