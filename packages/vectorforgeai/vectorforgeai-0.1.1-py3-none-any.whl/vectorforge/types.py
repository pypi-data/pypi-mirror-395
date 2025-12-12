"""
VectorForge SDK Types

Type definitions for VectorForge Cloud API requests and responses.

ALIGNMENT NOTE: These types match the VectorForge API V2 Implementation Plan
and the live HTTP API behavior. See docs/IMPLEMENTATION_GAPS.md for details.
"""

from typing import Any, Dict, List, Literal, Optional, TypedDict


# ==================== Register API ====================

class RegisterInput(TypedDict, total=False):
    """Input for register operation."""
    object_id: str
    hash_mode: Literal["content", "json", "embedding", "image", "custom"]
    hash_version: str
    hash_b64: str
    data_type: str
    metadata: Optional[Dict[str, Any]]


class RegisterResult(TypedDict):
    """Result from register operation."""
    divt_version: str
    divt_id: str
    tenant_id: str
    object_id: str
    hash_b64: str
    hash_mode: str
    hash_version: str
    # Cryptographic signatures
    ecdsa_sig_b64: str
    ml_dsa_sig_b64: str
    sig_version: str  # Note: API returns sig_version, not signature_version
    kms_key_arn: str
    # Ledger status
    ledger_status: Literal["pending", "anchored"]
    ledger_tx_id: Optional[str]
    created_at: str
    metadata: Optional[Dict[str, Any]]


# ==================== Verify API ====================

class VerifyInput(TypedDict, total=False):
    """
    Input for verify operation.
    
    Per Implementation Plan Section 8.0:
    - Content Mode (recommended): Provide divt_id + content, server re-computes hash
    - Hash Mode (advanced): Provide divt_id + hash_b64, server compares hashes
    """
    divt_id: str
    content: Any  # Content to verify - server will canonicalize and hash
    hash_b64: Optional[str]  # Pre-computed hash (advanced mode)


class VerifyResult(TypedDict):
    """
    Result from verify operation.
    
    Per Implementation Plan Section 8.0:
    - verified: true only if hash_valid && ecdsa_signature_valid && ml_dsa_signature_valid && !revoked
    """
    verified: bool
    hash_valid: bool
    ecdsa_signature_valid: bool
    ml_dsa_signature_valid: bool
    revoked: bool
    # DIVT details
    divt_version: str
    divt_id: str
    tenant_id: str
    object_id: str
    hash_mode: str
    stored_hash: str
    computed_hash: str
    # Signatures
    ecdsa_sig_b64: str
    ml_dsa_sig_b64: str
    sig_version: str
    # Ledger status
    ledger_status: Literal["pending", "anchored"]
    ledger_tx_id: Optional[str]
    created_at: str


# ==================== Bundle API ====================

class BundleInput(TypedDict, total=False):
    """
    Input for bundle operation.
    
    Per Implementation Plan (Phase 3 Sprint 4):
    Query by divt_id OR object_id (not arrays).
    """
    divt_id: Optional[str]  # DIVT ID to look up (singular)
    object_id: Optional[str]  # Object ID to look up (singular)
    include_history: Optional[bool]  # Include full event history timeline


class BundleDivtVerification(TypedDict):
    """DIVT verification details within a bundle."""
    verified: bool
    hash_valid: bool
    ecdsa_signature_valid: bool
    ml_dsa_signature_valid: bool
    revoked: bool
    divt_version: str
    divt_id: str
    tenant_id: str
    object_id: str
    hash_mode: str
    hash_version: str
    hash_b64: str
    ecdsa_sig_b64: str
    ml_dsa_sig_b64: str
    sig_version: str
    kms_key_arn: str
    ledger_status: Literal["pending", "anchored"]
    ledger_tx_id: Optional[str]
    created_at: str
    data_type: Optional[str]
    metadata: Optional[Dict[str, Any]]


class BundleWorldstateEvent(TypedDict):
    """Worldstate event in a bundle."""
    wsl_id: str
    kind: str
    timestamp: str
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]]
    ledger_status: Literal["pending", "anchored"]
    ledger_tx_id: Optional[str]
    created_at: str


class BundleScoringEvent(TypedDict):
    """Scoring event in a bundle."""
    wsl_id: str
    mode: Literal["privacy", "full"]
    overall_confidence: float
    semantic_confidence: float
    integrity_score: float
    support_score: Optional[float]
    faithfulness_score: Optional[float]
    vector_count: int
    verified_count: int
    degraded_mode: Optional[bool]
    timestamp: str


class BundleQuery(TypedDict):
    """Query metadata in bundle result."""
    divt_id: Optional[str]
    object_id: Optional[str]
    include_history: bool


class BundleResult(TypedDict):
    """
    Result from bundle operation.
    
    Per Implementation Plan (Phase 3 Sprint 4):
    Returns comprehensive verification bundle including DIVT verification,
    worldstate context, and scoring results.
    """
    query: BundleQuery
    divt: BundleDivtVerification
    worldstate: List[BundleWorldstateEvent]
    scoring: List[BundleScoringEvent]
    generated_at: str


# ==================== Stream Events API ====================

# Supported event types for streaming
StreamEventType = Literal[
    "divt_registered",
    "scoring_event",
    "worldstate_write",
    "worldstate_erasure",
    "divt_revocation",
]


class StreamEventsInput(TypedDict, total=False):
    """Input for stream events operation."""
    since: Optional[str]  # ISO timestamp cursor
    types: Optional[List[str]]  # Event types to filter (API parameter name is 'types')
    limit: Optional[int]  # Maximum events to return (default: 50, max: 100)


class StreamEvent(TypedDict):
    """Event from stream."""
    id: str
    type: str
    timestamp: str
    data: Dict[str, Any]


# ==================== Scoring API ====================

class ScoringEvidence(TypedDict, total=False):
    """Evidence item for scoring."""
    object_id: str
    divt_id: str
    tenant_id: str
    similarity: Optional[float]
    chunk_confidence: Optional[float]
    hash_b64: Optional[str]
    hash_mode: Optional[str]
    hash_version: Optional[str]
    data_type: Optional[str]
    text: Optional[str]  # Required for full scoring


class PrivacyScoreInput(TypedDict, total=False):
    """Input for privacy score operation."""
    query_id: Optional[str]
    answer_id: Optional[str]
    evidence: List[ScoringEvidence]
    model_signals: Optional[Dict[str, Any]]


class FullScoreInput(TypedDict, total=False):
    """Input for full score operation."""
    query: str
    answer: str
    evidence: List[ScoringEvidence]
    options: Optional[Dict[str, Any]]


class ScoreResult(TypedDict):
    """Result from scoring operations."""
    overall_confidence: float
    semantic_confidence: float
    integrity_score: float
    support_score: Optional[float]
    faithfulness_score: Optional[float]
    vector_count: int
    verified_count: int
    explanation: str
    degraded_mode: Optional[bool]
    breakdown: Optional[Dict[str, Any]]
    worldstate_ref: Optional[str]


# ==================== Worldstate Read API ====================

# Supported worldstate event kinds
WorldstateKind = Literal[
    "prompt_receipt",
    "rag_snapshot",
    "agent_action",
    "rf_snapshot",
    "pcap_chunk",
    "weather_feed",
    "scoring_event",
    "custom",
]


class GetWorldstateInput(TypedDict, total=False):
    """Input for get worldstate item operation."""
    wsl_id: str
    include_data: Optional[bool]


class ListWorldstateInput(TypedDict, total=False):
    """Input for list worldstate operation."""
    kind: Optional[str]  # WorldstateKind
    created_from: Optional[str]  # ISO 8601
    created_to: Optional[str]    # ISO 8601
    limit: Optional[int]         # Max 100, default 50
    cursor: Optional[str]        # Pagination cursor


class WorldstateItem(TypedDict):
    """Worldstate item response."""
    wsl_id: str
    tenant_id: str
    kind: str  # WorldstateKind
    timestamp: str
    s3_ref: str
    canon: Dict[str, Any]
    data_summary: Optional[str]
    metadata: Optional[Dict[str, Any]]
    ledger_status: Literal["pending", "anchored"]
    ledger_tx_id: Optional[str]
    created_at: str
    # Erasure status (if erased)
    erasure_status: Optional[str]
    erasure_completed_at: Optional[str]
    # Full data (only when include_data=true)
    data: Optional[Any]


class ListWorldstateResult(TypedDict):
    """Result from listing worldstate records."""
    items: List[WorldstateItem]
    cursor: Optional[str]
    count: int


# ==================== Error Types ====================

class VectorForgeAPIError(Exception):
    """Exception raised when VectorForge API returns an error."""

    def __init__(
        self,
        message: str,
        status_code: int,
        error: str,
        details: Optional[Any] = None,
    ):
        """
        Initialize VectorForge API error.

        Args:
            message: Human-readable error message
            status_code: HTTP status code (0 for non-HTTP errors)
            error: Error code identifier
            details: Optional additional error details
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error = error
        self.details = details

    def __str__(self) -> str:
        """Return string representation of error."""
        if self.status_code > 0:
            return f"[{self.status_code}] {self.error}: {self.message}"
        return f"{self.error}: {self.message}"

    def __repr__(self) -> str:
        """Return detailed representation of error."""
        return (
            f"VectorForgeAPIError(message={self.message!r}, "
            f"status_code={self.status_code}, error={self.error!r}, "
            f"details={self.details!r})"
        )
