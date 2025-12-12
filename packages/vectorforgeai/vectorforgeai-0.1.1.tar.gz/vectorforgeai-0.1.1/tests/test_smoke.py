"""
Smoke tests for VectorForge SDK

Simple tests to verify basic functionality without making live API calls.
"""

import os
import pytest

from vectorforge import VectorForgeClient, VectorForgeAPIError


def test_client_requires_config():
    """Test that client raises error when config is missing."""
    # Clear env vars if present
    old_url = os.environ.pop("VF_API_BASE_URL", None)
    old_key = os.environ.pop("VF_API_KEY", None)

    try:
        with pytest.raises(ValueError, match="base URL is required"):
            VectorForgeClient()
    finally:
        # Restore env vars
        if old_url:
            os.environ["VF_API_BASE_URL"] = old_url
        if old_key:
            os.environ["VF_API_KEY"] = old_key


def test_client_accepts_explicit_config():
    """Test that client accepts explicit configuration."""
    client = VectorForgeClient(
        base_url="https://api.vectorforge.ai",
        api_key="test_key"
    )
    
    assert client.base_url == "https://api.vectorforge.ai"
    assert client.api_key == "test_key"


def test_client_normalizes_base_url():
    """Test that client removes trailing slash from base URL."""
    client = VectorForgeClient(
        base_url="https://api.vectorforge.ai/",
        api_key="test_key"
    )
    
    assert client.base_url == "https://api.vectorforge.ai"


def test_client_reads_from_env():
    """Test that client reads from environment variables."""
    os.environ["VF_API_BASE_URL"] = "https://test.api.com"
    os.environ["VF_API_KEY"] = "env_test_key"

    try:
        client = VectorForgeClient()
        assert client.base_url == "https://test.api.com"
        assert client.api_key == "env_test_key"
    finally:
        os.environ.pop("VF_API_BASE_URL", None)
        os.environ.pop("VF_API_KEY", None)


def test_context_manager():
    """Test that client works as context manager."""
    with VectorForgeClient(
        base_url="https://api.vectorforge.ai",
        api_key="test_key"
    ) as client:
        assert client.base_url == "https://api.vectorforge.ai"
    
    # Session should be closed after exiting context


def test_version_accessible():
    """Test that version is accessible from module."""
    import vectorforge
    assert hasattr(vectorforge, "__version__")
    assert isinstance(vectorforge.__version__, str)
    assert vectorforge.__version__ == "0.1.0"


def test_exports():
    """Test that all expected symbols are exported."""
    import vectorforge
    
    expected_exports = [
        "VectorForgeClient",
        "VectorForgeAPIError",
        "RegisterInput",
        "RegisterResult",
        "VerifyInput",
        "VerifyResult",
        "BundleInput",
        "BundleResult",
        "StreamEventsInput",
        "StreamEvent",
    ]
    
    for export in expected_exports:
        assert hasattr(vectorforge, export), f"Missing export: {export}"

