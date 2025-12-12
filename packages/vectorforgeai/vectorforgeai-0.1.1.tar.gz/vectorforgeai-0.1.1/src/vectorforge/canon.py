"""
VectorForge Canonicalization Utilities

Implements canonicalization rules from IMPLEMENTATION_PLAN.md for computing
stable, deterministic hashes of content.

All canonicalization functions return bytes ready for hashing.
"""

import base64
import hashlib
import json
import unicodedata
from typing import Any, Dict, List, Optional

# Optional image processing support
try:
    from PIL import Image
    import io
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


def sha3_512_digest(data: bytes) -> str:
    """
    Compute SHA3-512 hash and return base64-encoded digest.

    Args:
        data: Bytes to hash

    Returns:
        Base64-encoded SHA3-512 digest (hash_b64)
    """
    hash_bytes = hashlib.sha3_512(data).digest()
    return base64.b64encode(hash_bytes).decode('ascii')


def canonicalize_content_v1(text: str) -> bytes:
    """
    Canonicalize text content using content_v1 rules.

    Rules from IMPLEMENTATION_PLAN.md:
    1. Interpret as UTF-8 (already a Python str)
    2. Normalize to Unicode NFC
    3. Replace any \\r\\n or \\r with \\n
    4. Trim leading and trailing whitespace once
    5. Encode to UTF-8 bytes

    Args:
        text: Text content to canonicalize

    Returns:
        Canonicalized bytes ready for hashing

    Raises:
        ValueError: If text contains invalid characters
    """
    if not isinstance(text, str):
        raise TypeError("Content must be a string")

    # Normalize to Unicode NFC
    normalized = unicodedata.normalize('NFC', text)

    # Replace \\r\\n and \\r with \\n
    normalized = normalized.replace('\r\n', '\n').replace('\r', '\n')

    # Trim leading and trailing whitespace once
    normalized = normalized.strip()

    # Encode to UTF-8 bytes
    return normalized.encode('utf-8')


def canonicalize_json_v1(data: Any) -> bytes:
    """
    Canonicalize JSON data using json_canon_v1 rules.

    Rules from IMPLEMENTATION_PLAN.md:
    1. Parse JSON (data should already be parsed)
    2. Sort object keys lexicographically at every level
    3. Serialize to minimal JSON (no spaces, deterministic number formatting)

    Args:
        data: Python object (dict, list, etc.) to canonicalize

    Returns:
        Canonicalized JSON bytes ready for hashing

    Raises:
        ValueError: If data is not JSON-serializable
    """
    try:
        # Use separators for minimal JSON (no spaces)
        # sort_keys=True ensures deterministic key ordering
        canonical_json = json.dumps(
            data,
            separators=(',', ':'),
            sort_keys=True,
            ensure_ascii=True,
        )
        return canonical_json.encode('utf-8')
    except (TypeError, ValueError) as e:
        raise ValueError(f"Data is not JSON-serializable: {e}") from e


def canonicalize_embedding_v1(embedding: List[float], precision: int = 6) -> bytes:
    """
    Canonicalize embedding vector using embedding_canon_v1 rules.

    Rules from IMPLEMENTATION_PLAN.md:
    1. Reject embeddings with NaN or Infinity values
    2. Represent floats as decimal strings with fixed precision (default: 6 decimals)
    3. Build JSON array string with no spaces: "[0.123456,-0.987654,...]"

    Args:
        embedding: List of float values
        precision: Decimal precision for floats (default: 6)

    Returns:
        Canonicalized embedding bytes ready for hashing

    Raises:
        ValueError: If embedding contains NaN or Infinity, or is empty
    """
    if not isinstance(embedding, list):
        raise TypeError("Embedding must be a list")

    if len(embedding) == 0:
        raise ValueError("Embedding cannot be empty")

    # Check for NaN and Infinity
    for i, value in enumerate(embedding):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Embedding value at index {i} is not a number: {value}")
        if not (-float('inf') < value < float('inf')):
            raise ValueError(
                f"Embedding contains invalid value at index {i}: {value} "
                "(NaN or Infinity not allowed)"
            )

    # Format each float with fixed precision
    formatted_values = [f"{value:.{precision}f}" for value in embedding]

    # Build JSON array with no spaces
    canonical_json = '[' + ','.join(formatted_values) + ']'

    return canonical_json.encode('utf-8')


def canonicalize_image_v1(
    image_bytes: bytes,
    max_dimension: Optional[int] = 1024,
) -> bytes:
    """
    Canonicalize image using image_norm_v1 rules.

    Rules from IMPLEMENTATION_PLAN.md:
    1. Decode supported image formats (PNG, JPEG, WebP) into bitmap
    2. Convert to sRGB color space
    3. Optionally resize so max dimension is fixed (default: 1024px), preserving aspect ratio
    4. Re-encode as PNG with deterministic options (no metadata)

    Args:
        image_bytes: Raw image bytes (PNG, JPEG, WebP, etc.)
        max_dimension: Maximum dimension for resizing (default: 1024, None to disable)

    Returns:
        Canonicalized PNG bytes ready for hashing

    Raises:
        ValueError: If image cannot be decoded
        ImportError: If Pillow is not installed
    """
    if not PILLOW_AVAILABLE:
        raise ImportError(
            "Pillow is required for image canonicalization. "
            "Install it with: pip install Pillow"
        )

    try:
        # Load image from bytes
        image = Image.open(io.BytesIO(image_bytes))

        # Convert to RGB (sRGB color space)
        # This handles RGBA, grayscale, palette, etc.
        if image.mode != 'RGB':
            # Convert RGBA to RGB by compositing on white background
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])  # Use alpha channel as mask
                image = background
            else:
                image = image.convert('RGB')

        # Resize if max_dimension is set
        if max_dimension is not None:
            width, height = image.size
            max_current = max(width, height)

            if max_current > max_dimension:
                # Calculate new dimensions preserving aspect ratio
                scale = max_dimension / max_current
                new_width = int(width * scale)
                new_height = int(height * scale)

                # Use LANCZOS for high-quality downsampling
                image = image.resize((new_width, new_height), Image.LANCZOS)

        # Encode as PNG with deterministic settings
        output = io.BytesIO()
        image.save(
            output,
            format='PNG',
            optimize=False,  # Deterministic output
            compress_level=6,  # Default compression (deterministic)
        )

        return output.getvalue()

    except Exception as e:
        raise ValueError(f"Failed to canonicalize image: {e}") from e


# Convenience functions that combine canonicalization + hashing

def hash_content_v1(text: str) -> str:
    """
    Canonicalize text content and return SHA3-512 hash_b64.

    Args:
        text: Text content

    Returns:
        Base64-encoded SHA3-512 hash
    """
    canonical_bytes = canonicalize_content_v1(text)
    return sha3_512_digest(canonical_bytes)


def hash_json_v1(data: Any) -> str:
    """
    Canonicalize JSON data and return SHA3-512 hash_b64.

    Args:
        data: JSON-serializable data

    Returns:
        Base64-encoded SHA3-512 hash
    """
    canonical_bytes = canonicalize_json_v1(data)
    return sha3_512_digest(canonical_bytes)


def hash_embedding_v1(embedding: List[float], precision: int = 6) -> str:
    """
    Canonicalize embedding vector and return SHA3-512 hash_b64.

    Args:
        embedding: List of float values
        precision: Decimal precision (default: 6)

    Returns:
        Base64-encoded SHA3-512 hash
    """
    canonical_bytes = canonicalize_embedding_v1(embedding, precision)
    return sha3_512_digest(canonical_bytes)


def hash_image_v1(image_bytes: bytes, max_dimension: Optional[int] = 1024) -> str:
    """
    Canonicalize image and return SHA3-512 hash_b64.

    Args:
        image_bytes: Raw image bytes
        max_dimension: Maximum dimension for resizing (default: 1024)

    Returns:
        Base64-encoded SHA3-512 hash
    """
    canonical_bytes = canonicalize_image_v1(image_bytes, max_dimension)
    return sha3_512_digest(canonical_bytes)

