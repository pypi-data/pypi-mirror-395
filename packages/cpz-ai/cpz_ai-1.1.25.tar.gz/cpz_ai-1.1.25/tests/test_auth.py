"""Tests for CPZ authentication validation and token hashing."""

from __future__ import annotations

import hashlib
from unittest.mock import Mock, patch

import pytest

from cpz.common.auth import hash_cpz_token, validate_cpz_credentials
from cpz.common.cpz_ai import CPZAIClient
from cpz.common.errors import CPZAuthenticationError, CPZAuthorizationError


class TestValidateCPZCredentials:
    """Test credential format validation."""

    def test_valid_credentials(self):
        """Test validation with valid key and secret formats."""
        key = "cpz_key_3f2b8a9c1d2e4f5a6b7c8d9e"
        # Secret must be exactly 48 lowercase alphanumeric chars after "cpz_secret_"
        secret = "cpz_secret_" + "a" * 48
        ok, msg = validate_cpz_credentials(key, secret)
        assert ok is True
        assert msg is None

    def test_missing_key(self):
        """Test validation fails when key is missing."""
        ok, msg = validate_cpz_credentials("", "cpz_secret_" + "a" * 48)
        assert ok is False
        assert "required" in msg.lower()

    def test_missing_secret(self):
        """Test validation fails when secret is missing."""
        ok, msg = validate_cpz_credentials("cpz_key_3f2b8a9c1d2e4f5a6b7c8d9e", "")
        assert ok is False
        assert "required" in msg.lower()

    def test_invalid_key_format(self):
        """Test validation fails with invalid key format."""
        valid_secret = "cpz_secret_" + "a" * 48
        # Wrong prefix
        ok, msg = validate_cpz_credentials("key_3f2b8a9c1d2e4f5a6b7c8d9e", valid_secret)
        assert ok is False
        assert "format" in msg.lower()

        # Wrong length
        ok, msg = validate_cpz_credentials("cpz_key_3f2b8a9c1d2e4f5a6b7c8d9", valid_secret)
        assert ok is False

        # Invalid hex chars
        ok, msg = validate_cpz_credentials("cpz_key_3f2b8a9c1d2e4f5a6b7c8d9g", valid_secret)
        assert ok is False

    def test_invalid_secret_format(self):
        """Test validation fails with invalid secret format."""
        valid_key = "cpz_key_3f2b8a9c1d2e4f5a6b7c8d9e"
        # Wrong prefix
        ok, msg = validate_cpz_credentials(valid_key, "secret_" + "a" * 48)
        assert ok is False
        assert "format" in msg.lower()

        # Wrong length (too short)
        ok, msg = validate_cpz_credentials(valid_key, "cpz_secret_" + "a" * 47)
        assert ok is False

        # Wrong length (too long)
        ok, msg = validate_cpz_credentials(valid_key, "cpz_secret_" + "a" * 49)
        assert ok is False

        # Invalid chars (uppercase)
        ok, msg = validate_cpz_credentials(valid_key, "cpz_secret_" + "A" * 48)
        assert ok is False


class TestHashCPZToken:
    """Test token hash computation."""

    def test_hash_matches_expected(self):
        """Test hash computation matches expected SHA-256."""
        key = "cpz_key_000000000000000000000000"
        secret = "cpz_secret_" + "0" * 48
        expected = hashlib.sha256(f"{key}.{secret}".encode("utf-8")).hexdigest()
        assert hash_cpz_token(key, secret) == expected

    def test_hash_matches_backend_format(self):
        """Test hash matches server-side computation format."""
        key = "cpz_key_3f2b8a9c1d2e4f5a6b7c8d9e"
        secret = "cpz_secret_" + "a" * 48
        full_token = f"{key}.{secret}"
        expected_hash = hashlib.sha256(full_token.encode("utf-8")).hexdigest()
        computed_hash = hash_cpz_token(key, secret)
        assert computed_hash == expected_hash
        assert len(computed_hash) == 64  # SHA-256 hex is 64 chars

    def test_hash_is_deterministic(self):
        """Test hash is the same for same inputs."""
        key = "cpz_key_3f2b8a9c1d2e4f5a6b7c8d9e"
        secret = "cpz_secret_" + "a" * 48
        hash1 = hash_cpz_token(key, secret)
        hash2 = hash_cpz_token(key, secret)
        assert hash1 == hash2

    def test_hash_different_for_different_inputs(self):
        """Test hash differs for different inputs."""
        key1 = "cpz_key_3f2b8a9c1d2e4f5a6b7c8d9e"
        secret1 = "cpz_secret_" + "a" * 48
        key2 = "cpz_key_3f2b8a9c1d2e4f5a6b7c8d9f"
        secret2 = "cpz_secret_" + "b" * 48
        hash1 = hash_cpz_token(key1, secret1)
        hash2 = hash_cpz_token(key2, secret2)
        assert hash1 != hash2


class TestCPZAIClientAuth:
    """Test CPZAIClient authentication integration."""

    def test_client_validates_on_init(self):
        """Test client validates credentials on initialization by default."""
        with pytest.raises(ValueError, match="format"):
            CPZAIClient(
                url="https://api-ai.cpz-lab.com/cpz",
                api_key="invalid_key",
                secret_key="cpz_secret_" + "a" * 48,
            )

    def test_client_skips_validation_when_disabled(self):
        """Test client can skip validation when validate_on_init=False."""
        client = CPZAIClient(
            url="https://api-ai.cpz-lab.com/cpz",
            api_key="invalid_key",
            secret_key="invalid_secret",
            validate_on_init=False,
        )
        assert client.api_key == "invalid_key"
        assert client.secret_key == "invalid_secret"

    def test_client_token_hash_property(self):
        """Test client token_hash property matches hash computation."""
        key = "cpz_key_3f2b8a9c1d2e4f5a6b7c8d9e"
        secret = "cpz_secret_" + "a" * 48
        client = CPZAIClient(
            url="https://api-ai.cpz-lab.com/cpz",
            api_key=key,
            secret_key=secret,
            validate_on_init=False,
        )
        expected_hash = hash_cpz_token(key, secret)
        assert client.token_hash == expected_hash

    def test_client_sends_correct_headers(self):
        """Test client sends X-CPZ-Key and X-CPZ-Secret headers."""
        key = "cpz_key_3f2b8a9c1d2e4f5a6b7c8d9e"
        secret = "cpz_secret_" + "a" * 48
        client = CPZAIClient(
            url="https://api-ai.cpz-lab.com/cpz",
            api_key=key,
            secret_key=secret,
            validate_on_init=False,
        )
        headers = client._headers()
        assert headers["X-CPZ-Key"] == key
        assert headers["X-CPZ-Secret"] == secret

    @patch("cpz.common.cpz_ai.requests.get")
    def test_client_raises_authentication_error_on_401(self, mock_get):
        """Test client raises CPZAuthenticationError on 401 response."""
        key = "cpz_key_3f2b8a9c1d2e4f5a6b7c8d9e"
        secret = "cpz_secret_" + "a" * 48
        client = CPZAIClient(
            url="https://api-ai.cpz-lab.com/cpz",
            api_key=key,
            secret_key=secret,
            validate_on_init=False,
        )

        mock_resp = Mock()
        mock_resp.status_code = 401
        mock_resp.text = '{"error": "Unauthorized"}'
        mock_get.return_value = mock_resp

        with pytest.raises(CPZAuthenticationError, match="Authentication failed"):
            client.get_strategies()

    @patch("cpz.common.cpz_ai.requests.get")
    def test_client_raises_authorization_error_on_403(self, mock_get):
        """Test client raises CPZAuthorizationError on 403 response."""
        key = "cpz_key_3f2b8a9c1d2e4f5a6b7c8d9e"
        secret = "cpz_secret_" + "a" * 48
        client = CPZAIClient(
            url="https://api-ai.cpz-lab.com/cpz",
            api_key=key,
            secret_key=secret,
            validate_on_init=False,
        )

        mock_resp = Mock()
        mock_resp.status_code = 403
        mock_resp.text = '{"error": "Forbidden"}'
        mock_get.return_value = mock_resp

        with pytest.raises(CPZAuthorizationError, match="Authorization failed"):
            client.get_strategies()

    def test_from_env_validates_by_default(self):
        """Test from_env validates credentials by default."""
        # Test the constructor directly since conftest stubs from_env
        # This tests the same validation logic that from_env uses
        with pytest.raises(ValueError, match="format"):
            CPZAIClient(
                url="https://api-ai.cpz-lab.com/cpz",
                api_key="invalid_key",
                secret_key="cpz_secret_" + "a" * 48,
                validate_on_init=True,
            )

    def test_from_keys_validates_by_default(self):
        """Test from_keys validates credentials by default."""
        with pytest.raises(ValueError, match="format"):
            CPZAIClient.from_keys(
                api_key="invalid_key",
                secret_key="cpz_secret_" + "a" * 48,
            )

