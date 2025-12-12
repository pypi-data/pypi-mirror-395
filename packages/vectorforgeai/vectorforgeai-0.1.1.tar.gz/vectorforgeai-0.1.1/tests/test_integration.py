"""
VectorForge Python SDK Integration Tests

Tests the SDK against the live VectorForge API.

Prerequisites:
- VF_API_BASE_URL environment variable set
- VF_API_KEY environment variable set

Run with:
    pytest tests/test_integration.py -v
"""

import os
import time
from datetime import datetime, timedelta

import pytest

# Skip all tests if environment variables not set
pytestmark = pytest.mark.skipif(
    not os.environ.get("VF_API_BASE_URL") or not os.environ.get("VF_API_KEY"),
    reason="VF_API_BASE_URL and VF_API_KEY environment variables required for integration tests"
)


@pytest.fixture(scope="module")
def client():
    """Create a VectorForge client for tests."""
    from vectorforge import VectorForgeClient
    return VectorForgeClient()


class TestRegisterAPI:
    """Tests for the Register API."""

    def test_register_content(self, client):
        """Should register text content with register_content()."""
        object_id = f"test:content:{int(time.time() * 1000)}"
        text = "Hello, VectorForge SDK Integration Test!"

        result = client.register_content(
            object_id=object_id,
            text=text,
            data_type="test_content_v1",
            metadata={"test": True, "timestamp": datetime.now().isoformat()},
        )

        assert result is not None
        assert "divt_id" in result
        assert result["object_id"] == object_id
        assert result["hash_mode"] == "content"
        assert result["hash_version"] == "content_v1"
        assert "hash_b64" in result
        assert "ecdsa_sig_b64" in result
        assert "ml_dsa_sig_b64" in result
        assert "sig_version" in result
        assert result["ledger_status"] == "pending"

        print(f"✓ Registered content DIVT: {result['divt_id']}")

    def test_register_json(self, client):
        """Should register JSON data with register_json()."""
        object_id = f"test:json:{int(time.time() * 1000)}"
        data = {
            "prompt": "What is the capital of France?",
            "response": "Paris",
            "model": "test-model",
            "timestamp": datetime.now().isoformat(),
        }

        result = client.register_json(
            object_id=object_id,
            data=data,
            data_type="prompt_receipt_v1",
            metadata={"test": True},
        )

        assert result is not None
        assert "divt_id" in result
        assert result["object_id"] == object_id
        assert result["hash_mode"] == "json"
        assert result["hash_version"] == "json_canon_v1"

        print(f"✓ Registered JSON DIVT: {result['divt_id']}")

    def test_register_embedding(self, client):
        """Should register embedding with register_embedding()."""
        object_id = f"test:embedding:{int(time.time() * 1000)}"
        embedding = [0.1, 0.2, 0.3, -0.4, 0.5]

        result = client.register_embedding(
            object_id=object_id,
            embedding=embedding,
            data_type="rag_chunk_v1",
            metadata={"test": True},
        )

        assert result is not None
        assert "divt_id" in result
        assert result["object_id"] == object_id
        assert result["hash_mode"] == "embedding"
        assert result["hash_version"] == "embedding_canon_v1"

        print(f"✓ Registered embedding DIVT: {result['divt_id']}")


class TestVerifyAPI:
    """Tests for the Verify API."""

    def test_verify_content_success(self, client):
        """Should verify content using hash_b64."""
        # First, register some content
        object_id = f"test:verify:{int(time.time() * 1000)}"
        data = {"test": "verify", "timestamp": int(time.time())}

        register_result = client.register_json(
            object_id=object_id,
            data=data,
            data_type="test_v1",
        )

        assert "divt_id" in register_result

        # Now verify using the verify method
        verify_result = client.verify_json(
            divt_id=register_result["divt_id"],
            data=data,
        )

        assert verify_result is not None
        assert verify_result["verified"] is True
        assert verify_result["hash_valid"] is True
        assert verify_result["ecdsa_signature_valid"] is True
        assert verify_result["ml_dsa_signature_valid"] is True
        assert verify_result["revoked"] is False
        assert verify_result["divt_id"] == register_result["divt_id"]
        assert verify_result["object_id"] == object_id

        print(f"✓ Verified DIVT: {verify_result['divt_id']}")

    def test_verify_content_failure(self, client):
        """Should fail verification with wrong content."""
        # First, register some content
        object_id = f"test:verify-wrong:{int(time.time() * 1000)}"
        data = {"test": "original", "timestamp": int(time.time())}

        register_result = client.register_json(
            object_id=object_id,
            data=data,
            data_type="test_v1",
        )

        # Now verify with WRONG data
        wrong_data = {"test": "modified", "timestamp": int(time.time())}
        verify_result = client.verify_json(
            divt_id=register_result["divt_id"],
            data=wrong_data,
        )

        assert verify_result is not None
        assert verify_result["verified"] is False
        assert verify_result["hash_valid"] is False
        assert verify_result["divt_id"] == register_result["divt_id"]

        print("✓ Correctly detected tampered content")


class TestBundleAPI:
    """Tests for the Bundle API."""

    def test_get_bundle_by_divt_id(self, client):
        """Should get verification bundle by divt_id."""
        # First, register some content
        object_id = f"test:bundle:{int(time.time() * 1000)}"
        data = {"test": "bundle", "timestamp": int(time.time())}

        register_result = client.register_json(
            object_id=object_id,
            data=data,
            data_type="test_v1",
        )

        # Get bundle by divt_id
        bundle = client.get_bundle({
            "divt_id": register_result["divt_id"],
        })

        assert bundle is not None
        assert "query" in bundle
        assert bundle["query"]["divt_id"] == register_result["divt_id"]
        assert "divt" in bundle
        assert bundle["divt"]["divt_id"] == register_result["divt_id"]
        assert bundle["divt"]["verified"] is True
        assert "worldstate" in bundle
        assert isinstance(bundle["worldstate"], list)
        assert "scoring" in bundle
        assert isinstance(bundle["scoring"], list)
        assert "generated_at" in bundle

        print(f"✓ Retrieved bundle for DIVT: {register_result['divt_id']}")

    def test_get_bundle_by_object_id(self, client):
        """Should get verification bundle by object_id."""
        # First, register some content with a unique object_id
        object_id = f"test:bundle-obj:{int(time.time() * 1000)}"
        data = {"test": "bundle-by-object", "timestamp": int(time.time())}

        client.register_json(
            object_id=object_id,
            data=data,
            data_type="test_v1",
        )

        # Get bundle by object_id
        bundle = client.get_bundle({
            "object_id": object_id,
        })

        assert bundle is not None
        assert "query" in bundle
        assert bundle["query"]["object_id"] == object_id
        assert "divt" in bundle
        assert bundle["divt"]["object_id"] == object_id

        print(f"✓ Retrieved bundle for object_id: {object_id}")


class TestScoringAPI:
    """Tests for the Scoring API."""

    def test_privacy_score(self, client):
        """Should calculate privacy score."""
        # First, register some evidence
        evidence1 = client.register_json(
            object_id=f"test:evidence1:{int(time.time() * 1000)}",
            data={"chunk": "Paris is the capital of France."},
            data_type="rag_chunk_v1",
        )

        evidence2 = client.register_json(
            object_id=f"test:evidence2:{int(time.time() * 1000)}",
            data={"chunk": "France is a country in Europe."},
            data_type="rag_chunk_v1",
        )

        # Calculate privacy score
        result = client.score_privacy({
            "query_id": f"query:{int(time.time() * 1000)}",
            "answer_id": f"answer:{int(time.time() * 1000)}",
            "evidence": [
                {
                    "object_id": evidence1["object_id"],
                    "divt_id": evidence1["divt_id"],
                    "tenant_id": evidence1["tenant_id"],
                    "similarity": 0.95,
                    "chunk_confidence": 0.9,
                },
                {
                    "object_id": evidence2["object_id"],
                    "divt_id": evidence2["divt_id"],
                    "tenant_id": evidence2["tenant_id"],
                    "similarity": 0.85,
                    "chunk_confidence": 0.8,
                },
            ],
        })

        assert result is not None
        assert isinstance(result["overall_confidence"], (int, float))
        assert isinstance(result["semantic_confidence"], (int, float))
        assert isinstance(result["integrity_score"], (int, float))
        assert result["vector_count"] == 2
        assert isinstance(result["explanation"], str)

        print(f"✓ Privacy score: {result['overall_confidence']:.3f}")

    def test_full_score(self, client):
        """Should calculate full score (if plan allows)."""
        from vectorforge import VectorForgeAPIError

        # First, register some evidence with text
        evidence = client.register_json(
            object_id=f"test:evidence-full:{int(time.time() * 1000)}",
            data={"chunk": "Paris is the capital city of France."},
            data_type="rag_chunk_v1",
        )

        try:
            result = client.score_full({
                "query": "What is the capital of France?",
                "answer": "The capital of France is Paris.",
                "evidence": [
                    {
                        "object_id": evidence["object_id"],
                        "divt_id": evidence["divt_id"],
                        "tenant_id": evidence["tenant_id"],
                        "text": "Paris is the capital city of France.",
                        "similarity": 0.95,
                    },
                ],
                "options": {
                    "log_worldstate": "none",
                },
            })

            assert result is not None
            assert isinstance(result["overall_confidence"], (int, float))
            assert isinstance(result.get("support_score"), (int, float, type(None)))
            assert isinstance(result.get("faithfulness_score"), (int, float, type(None)))

            print(f"✓ Full score: {result['overall_confidence']:.3f}")
            if result.get("support_score") is not None:
                print(f"  - Support: {result['support_score']:.3f}")
            if result.get("faithfulness_score") is not None:
                print(f"  - Faithfulness: {result['faithfulness_score']:.3f}")

        except VectorForgeAPIError as e:
            if e.status_code == 403:
                print("⚠ Full score not available on current plan (403)")
                pytest.skip("Full score not available on current plan")
            else:
                raise


class TestStreamEventsAPI:
    """Tests for the Stream Events API."""

    def test_stream_events(self, client):
        """Should stream events via SSE."""
        events = []
        one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z"

        client.stream_events(
            {
                "since": one_hour_ago,
                "types": ["divt_registered"],
                "limit": 5,
            },
            on_event=lambda event: events.append(event),
        )

        # We may or may not have events depending on recent activity
        assert isinstance(events, list)

        if len(events) > 0:
            assert "id" in events[0]
            assert "type" in events[0]
            assert "timestamp" in events[0]
            print(f"✓ Received {len(events)} events via SSE")
        else:
            print("⚠ No events in the last hour (this is OK)")


class TestErrorHandling:
    """Tests for error handling."""

    def test_404_for_nonexistent_divt(self, client):
        """Should handle 404 for non-existent DIVT."""
        from vectorforge import VectorForgeAPIError

        with pytest.raises(VectorForgeAPIError) as exc_info:
            client.verify({
                "divt_id": "00000000-0000-0000-0000-000000000000",
            })

        assert exc_info.value.status_code == 404
        print("✓ Correctly handled 404 for non-existent DIVT")


# Unit tests that run without environment variables
class TestUnitTests:
    """Unit tests that don't require API connection."""

    def test_missing_base_url(self):
        """Should throw error when VF_API_BASE_URL is not set."""
        from vectorforge import VectorForgeClient

        original_url = os.environ.get("VF_API_BASE_URL")
        original_key = os.environ.get("VF_API_KEY")

        try:
            if "VF_API_BASE_URL" in os.environ:
                del os.environ["VF_API_BASE_URL"]
            if "VF_API_KEY" in os.environ:
                del os.environ["VF_API_KEY"]

            with pytest.raises(ValueError, match="base URL is required"):
                VectorForgeClient()
        finally:
            if original_url:
                os.environ["VF_API_BASE_URL"] = original_url
            if original_key:
                os.environ["VF_API_KEY"] = original_key

    def test_missing_api_key(self):
        """Should throw error when VF_API_KEY is not set."""
        from vectorforge import VectorForgeClient

        original_url = os.environ.get("VF_API_BASE_URL")
        original_key = os.environ.get("VF_API_KEY")

        try:
            os.environ["VF_API_BASE_URL"] = "https://example.com"
            if "VF_API_KEY" in os.environ:
                del os.environ["VF_API_KEY"]

            with pytest.raises(ValueError, match="API key is required"):
                VectorForgeClient()
        finally:
            if original_url:
                os.environ["VF_API_BASE_URL"] = original_url
            else:
                if "VF_API_BASE_URL" in os.environ:
                    del os.environ["VF_API_BASE_URL"]
            if original_key:
                os.environ["VF_API_KEY"] = original_key

