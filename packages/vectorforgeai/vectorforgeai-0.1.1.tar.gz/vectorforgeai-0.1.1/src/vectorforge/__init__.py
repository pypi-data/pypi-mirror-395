"""
VectorForge Python SDK

Official Python client for VectorForge Cloud APIs.

VectorForge is a trust and confidence layer for AI and automations.
"""

__version__ = "0.1.0"

from .client import VectorForgeClient
from .types import (
    BundleInput,
    BundleResult,
    BundleDivtVerification,
    BundleWorldstateEvent,
    BundleScoringEvent,
    RegisterInput,
    RegisterResult,
    StreamEvent,
    StreamEventsInput,
    VectorForgeAPIError,
    VerifyInput,
    VerifyResult,
    ScoringEvidence,
    PrivacyScoreInput,
    FullScoreInput,
    ScoreResult,
    # Worldstate read types
    WorldstateKind,
    GetWorldstateInput,
    ListWorldstateInput,
    WorldstateItem,
    ListWorldstateResult,
)

# Canonicalization utilities (optional import)
from . import canon

__all__ = [
    "__version__",
    "VectorForgeClient",
    "VectorForgeAPIError",
    "RegisterInput",
    "RegisterResult",
    "VerifyInput",
    "VerifyResult",
    "BundleInput",
    "BundleResult",
    "BundleDivtVerification",
    "BundleWorldstateEvent",
    "BundleScoringEvent",
    "StreamEventsInput",
    "StreamEvent",
    "ScoringEvidence",
    "PrivacyScoreInput",
    "FullScoreInput",
    "ScoreResult",
    # Worldstate read
    "WorldstateKind",
    "GetWorldstateInput",
    "ListWorldstateInput",
    "WorldstateItem",
    "ListWorldstateResult",
    "canon",
]
