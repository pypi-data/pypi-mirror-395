"""
VectorForge SDK Client

HTTP client implementation for VectorForge Cloud APIs.

ALIGNMENT NOTE: This client is aligned with the VectorForge API V2 Implementation Plan
and the live HTTP API behavior. See docs/IMPLEMENTATION_GAPS.md for details.
"""

import os
from typing import Any, Callable, Dict, Optional

import requests

from .types import (
    BundleInput,
    BundleResult,
    RegisterInput,
    RegisterResult,
    StreamEvent,
    StreamEventsInput,
    VectorForgeAPIError,
    VerifyInput,
    VerifyResult,
    PrivacyScoreInput,
    FullScoreInput,
    ScoreResult,
    GetWorldstateInput,
    ListWorldstateInput,
    WorldstateItem,
    ListWorldstateResult,
)


class VectorForgeClient:
    """VectorForge API client for Python."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Initialize VectorForge client.

        Args:
            base_url: API base URL (default: VF_API_BASE_URL env var)
            api_key: API key (default: VF_API_KEY env var)

        Raises:
            ValueError: If base_url or api_key are not provided and env vars are not set
        """
        # Load from config or environment variables
        self.base_url = base_url or os.environ.get("VF_API_BASE_URL", "")
        self.api_key = api_key or os.environ.get("VF_API_KEY", "")

        # Validate configuration
        if not self.base_url:
            raise ValueError(
                "VectorForge base URL is required. Set VF_API_BASE_URL environment "
                "variable or pass base_url to VectorForgeClient constructor."
            )

        if not self.api_key:
            raise ValueError(
                "VectorForge API key is required. Set VF_API_KEY environment "
                "variable or pass api_key to VectorForgeClient constructor."
            )

        # Normalize base URL (remove trailing slash)
        self.base_url = self.base_url.rstrip("/")

        # Create session for connection pooling
        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-Api-Key": self.api_key,
                "Content-Type": "application/json",
            }
        )

    def _request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Make an HTTP request to the VectorForge API.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (e.g., '/v1/register')
            json: Optional JSON body for POST requests
            params: Optional query parameters

        Returns:
            Parsed JSON response

        Raises:
            VectorForgeAPIError: If the API returns an error
        """
        url = f"{self.base_url}{path}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json,
                params=params,
                timeout=30,
            )

            # Parse response body
            try:
                response_data = response.json()
            except Exception:
                response_data = {}

            # Handle error responses
            if not response.ok:
                error_message = (
                    response_data.get("message")
                    or response_data.get("error")
                    or "API request failed"
                )
                raise VectorForgeAPIError(
                    message=error_message,
                    status_code=response.status_code,
                    error=response_data.get("error", "unknown_error"),
                    details=response_data.get("details"),
                )

            return response_data

        except VectorForgeAPIError:
            # Re-raise VectorForgeAPIError as-is
            raise
        except requests.exceptions.RequestException as e:
            # Wrap requests exceptions
            raise VectorForgeAPIError(
                message=f"Request failed: {str(e)}",
                status_code=0,
                error="network_error",
            ) from e
        except Exception as e:
            # Wrap other exceptions
            raise VectorForgeAPIError(
                message=f"Unexpected error: {str(e)}",
                status_code=0,
                error="unknown_error",
            ) from e

    def register(self, input: RegisterInput) -> RegisterResult:
        """
        Register a new DIVT (Digital Integrity Verification Token).

        Args:
            input: Registration input containing object_id, hash, and metadata

        Returns:
            RegisterResult with divt_id and cryptographic signatures

        Raises:
            VectorForgeAPIError: If the API request fails
        """
        return self._request("POST", "/v1/register", json=input)

    def verify(self, input: VerifyInput) -> VerifyResult:
        """
        Verify content against a registered DIVT.

        Per Implementation Plan Section 8.0:
        - Content Mode (recommended): Provide divt_id + content
        - Hash Mode (advanced): Provide divt_id + hash_b64

        Args:
            input: Verification input containing divt_id and content or hash_b64

        Returns:
            VerifyResult with validation status and DIVT details

        Raises:
            VectorForgeAPIError: If the API request fails
        """
        return self._request("POST", "/v1/verify", json=input)

    def get_bundle(self, input: BundleInput) -> BundleResult:
        """
        Get verification bundle for a DIVT or object.

        Per Implementation Plan (Phase 3 Sprint 4):
        Returns comprehensive verification bundle including DIVT verification,
        worldstate context, and scoring results in a single API call.

        Args:
            input: Bundle input with divt_id OR object_id (not arrays)

        Returns:
            BundleResult with DIVT verification, worldstate, and scoring

        Raises:
            VectorForgeAPIError: If the API request fails
        """
        params: Dict[str, Any] = {}
        
        if input.get("divt_id"):
            params["divt_id"] = input["divt_id"]
        if input.get("object_id"):
            params["object_id"] = input["object_id"]
        if input.get("include_history") is not None:
            params["include_history"] = str(input["include_history"]).lower()
        
        return self._request("GET", "/v1/verify/bundle", params=params)

    def score_privacy(self, input: PrivacyScoreInput) -> ScoreResult:
        """
        Calculate privacy score (hash/ID-only inputs, no raw content sent).

        Per Implementation Plan Section 2.4:
        Privacy Score uses only IDs, hashes, similarity scores, and metadata.
        No raw content leaves the user's environment.

        Args:
            input: Privacy scoring input with evidence array

        Returns:
            ScoreResult with confidence scores

        Raises:
            VectorForgeAPIError: If the API request fails
        """
        return self._request("POST", "/v1/score/privacy", json=input)

    def score_full(self, input: FullScoreInput) -> ScoreResult:
        """
        Calculate full score (sends query, answer, and evidence text to Groq judge).

        Per Implementation Plan Section 2.4:
        Full Score inspects the question, answer, and evidence to score
        semantic support, faithfulness, and cryptographic integrity.

        Args:
            input: Full scoring input with query, answer, and evidence

        Returns:
            ScoreResult with full confidence breakdown

        Raises:
            VectorForgeAPIError: If the API request fails
        """
        return self._request("POST", "/v1/score/full", json=input)

    # ==================== Worldstate Read Methods ====================

    def get_worldstate_item(self, input: GetWorldstateInput) -> WorldstateItem:
        """
        Get a single worldstate record by ID.

        Per Implementation Plan Section 2.3, Section 8:
        Returns metadata + optional blob data for a worldstate record.
        Enforces tenant isolation.

        Args:
            input: Worldstate ID and options (wsl_id required, include_data optional)

        Returns:
            WorldstateItem with metadata and optional data

        Raises:
            VectorForgeAPIError: If the API request fails or record not found
        """
        params: Dict[str, Any] = {}
        if input.get("include_data"):
            params["include_data"] = "true"
        
        wsl_id = input["wsl_id"]
        return self._request("GET", f"/v1/worldstate/{wsl_id}", params=params)

    def list_worldstate(
        self,
        input: Optional[ListWorldstateInput] = None,
    ) -> ListWorldstateResult:
        """
        List worldstate records with filters and pagination.

        Per Implementation Plan Section 2.3, Section 8:
        Returns paginated list of worldstate records for the authenticated tenant.

        Args:
            input: List filters (kind, time range, limit, cursor)

        Returns:
            Paginated list of worldstate items with cursor for next page

        Raises:
            VectorForgeAPIError: If the API request fails
        """
        params: Dict[str, Any] = {}
        
        if input:
            if input.get("kind"):
                params["kind"] = input["kind"]
            if input.get("created_from"):
                params["created_from"] = input["created_from"]
            if input.get("created_to"):
                params["created_to"] = input["created_to"]
            if input.get("limit") is not None:
                params["limit"] = input["limit"]
            if input.get("cursor"):
                params["cursor"] = input["cursor"]
        
        return self._request("GET", "/v1/worldstate", params=params)

    def stream_events(
        self,
        input: StreamEventsInput,
        on_event: Callable[[StreamEvent], None],
    ) -> None:
        """
        Stream events from VectorForge using Server-Sent Events (SSE).

        Per Implementation Plan Section 9:
        Streams recent events for the authenticated tenant.

        Args:
            input: Stream input with optional filters (since, types, limit)
            on_event: Callback function called for each event

        Raises:
            VectorForgeAPIError: If the stream request fails
        """
        # Build query parameters
        params: Dict[str, Any] = {}
        if input.get("since"):
            params["since"] = input["since"]
        # API uses 'types' parameter (comma-separated)
        if input.get("types"):
            params["types"] = ",".join(input["types"])
        if input.get("limit") is not None:
            params["limit"] = input["limit"]

        url = f"{self.base_url}/v1/stream/events"

        try:
            # Make streaming request
            response = self.session.get(
                url,
                params=params,
                headers={"Accept": "text/event-stream"},
                stream=True,
                timeout=None,  # No timeout for streaming
            )

            # Handle error responses
            if not response.ok:
                try:
                    error_data = response.json()
                except Exception:
                    error_data = {}

                raise VectorForgeAPIError(
                    message=error_data.get("message", "Stream request failed"),
                    status_code=response.status_code,
                    error=error_data.get("error", "stream_error"),
                    details=error_data.get("details"),
                )

            # Process SSE stream
            buffer = ""
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    buffer += chunk

                    # Process complete lines
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.rstrip("\r")

                        if line.startswith("data: "):
                            data = line[6:].strip()

                            if data == "[DONE]":
                                return

                            try:
                                import json

                                event = json.loads(data)
                                on_event(event)
                            except Exception as e:
                                print(f"Warning: Failed to parse SSE event: {data}, {e}")

        except VectorForgeAPIError:
            raise
        except requests.exceptions.RequestException as e:
            raise VectorForgeAPIError(
                message=f"Stream failed: {str(e)}",
                status_code=0,
                error="stream_error",
            ) from e
        except Exception as e:
            raise VectorForgeAPIError(
                message=f"Stream failed: {str(e)}",
                status_code=0,
                error="stream_error",
            ) from e

    # ==================== High-Level Helper Methods ====================

    def register_content(
        self,
        object_id: str,
        text: str,
        data_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> RegisterResult:
        """
        Register text content with automatic canonicalization and hashing.

        This is a high-level helper that:
        1. Canonicalizes text using content_v1 rules (NFC, normalize line endings, trim)
        2. Computes SHA3-512 hash
        3. Calls the low-level register() method

        Args:
            object_id: Unique identifier for the object
            text: Text content to register
            data_type: Logical data type (e.g., 'prompt_receipt_v1')
            metadata: Optional metadata dictionary

        Returns:
            RegisterResult with divt_id and signatures

        Raises:
            VectorForgeAPIError: If the API request fails
            ValueError: If text is invalid
        """
        from .canon import hash_content_v1

        hash_b64 = hash_content_v1(text)

        return self.register({
            "object_id": object_id,
            "hash_mode": "content",
            "hash_version": "content_v1",
            "hash_b64": hash_b64,
            "data_type": data_type,
            "metadata": metadata,
        })

    def register_json(
        self,
        object_id: str,
        data: Any,
        data_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> RegisterResult:
        """
        Register JSON data with automatic canonicalization and hashing.

        This is a high-level helper that:
        1. Canonicalizes JSON using json_canon_v1 rules (sort keys, minimal JSON)
        2. Computes SHA3-512 hash
        3. Calls the low-level register() method

        Args:
            object_id: Unique identifier for the object
            data: JSON-serializable data structure
            data_type: Logical data type (e.g., 'prompt_receipt_v1')
            metadata: Optional metadata dictionary

        Returns:
            RegisterResult with divt_id and signatures

        Raises:
            VectorForgeAPIError: If the API request fails
            ValueError: If data is not JSON-serializable
        """
        from .canon import hash_json_v1

        hash_b64 = hash_json_v1(data)

        return self.register({
            "object_id": object_id,
            "hash_mode": "json",
            "hash_version": "json_canon_v1",
            "hash_b64": hash_b64,
            "data_type": data_type,
            "metadata": metadata,
        })

    def register_embedding(
        self,
        object_id: str,
        embedding: list,
        data_type: str,
        metadata: Optional[Dict[str, Any]] = None,
        precision: int = 6,
    ) -> RegisterResult:
        """
        Register an embedding vector with automatic canonicalization and hashing.

        This is a high-level helper that:
        1. Validates embedding (rejects NaN/Infinity)
        2. Canonicalizes using embedding_canon_v1 rules (fixed precision, no spaces)
        3. Computes SHA3-512 hash
        4. Calls the low-level register() method

        Args:
            object_id: Unique identifier for the object
            embedding: List of float values
            data_type: Logical data type (e.g., 'rag_chunk_v1')
            metadata: Optional metadata dictionary
            precision: Decimal precision for floats (default: 6)

        Returns:
            RegisterResult with divt_id and signatures

        Raises:
            VectorForgeAPIError: If the API request fails
            ValueError: If embedding contains NaN or Infinity
        """
        from .canon import hash_embedding_v1

        hash_b64 = hash_embedding_v1(embedding, precision)

        return self.register({
            "object_id": object_id,
            "hash_mode": "embedding",
            "hash_version": "embedding_canon_v1",
            "hash_b64": hash_b64,
            "data_type": data_type,
            "metadata": metadata,
        })

    def register_image(
        self,
        object_id: str,
        image_bytes: bytes,
        data_type: str,
        metadata: Optional[Dict[str, Any]] = None,
        max_dimension: Optional[int] = 1024,
    ) -> RegisterResult:
        """
        Register an image with automatic canonicalization and hashing.

        This is a high-level helper that:
        1. Decodes image from bytes
        2. Normalizes to sRGB, optionally resizes
        3. Re-encodes as deterministic PNG
        4. Computes SHA3-512 hash
        5. Calls the low-level register() method

        Note: Requires Pillow to be installed: pip install vectorforgeai[image]

        Args:
            object_id: Unique identifier for the object
            image_bytes: Raw image bytes (PNG, JPEG, WebP, etc.)
            data_type: Logical data type (e.g., 'image_receipt_v1')
            metadata: Optional metadata dictionary
            max_dimension: Maximum dimension for resizing (default: 1024, None to disable)

        Returns:
            RegisterResult with divt_id and signatures

        Raises:
            VectorForgeAPIError: If the API request fails
            ImportError: If Pillow is not installed
            ValueError: If image cannot be decoded
        """
        from .canon import hash_image_v1

        hash_b64 = hash_image_v1(image_bytes, max_dimension)

        return self.register({
            "object_id": object_id,
            "hash_mode": "image",
            "hash_version": "image_norm_v1",
            "hash_b64": hash_b64,
            "data_type": data_type,
            "metadata": metadata,
        })

    def verify_content(
        self,
        divt_id: str,
        text: str,
    ) -> VerifyResult:
        """
        Verify text content against a registered DIVT.

        High-level helper that re-computes the hash and verifies.

        Args:
            divt_id: DIVT ID to verify against
            text: Text content to verify

        Returns:
            VerifyResult with validation status

        Raises:
            VectorForgeAPIError: If the API request fails
        """
        from .canon import hash_content_v1

        hash_b64 = hash_content_v1(text)
        
        return self.verify({
            "divt_id": divt_id,
            "hash_b64": hash_b64,
        })

    def verify_json(
        self,
        divt_id: str,
        data: Any,
    ) -> VerifyResult:
        """
        Verify JSON data against a registered DIVT.

        High-level helper that re-computes the hash and verifies.

        Args:
            divt_id: DIVT ID to verify against
            data: JSON data to verify

        Returns:
            VerifyResult with validation status

        Raises:
            VectorForgeAPIError: If the API request fails
        """
        from .canon import hash_json_v1

        hash_b64 = hash_json_v1(data)
        
        return self.verify({
            "divt_id": divt_id,
            "hash_b64": hash_b64,
        })

    # ==================== Session Management ====================

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self) -> "VectorForgeClient":
        """Support context manager protocol."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Support context manager protocol."""
        self.close()
