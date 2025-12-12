"""CPZ Authentication utilities for validating credentials and computing token hashes."""

from __future__ import annotations

import hashlib
import re
from typing import Tuple, Optional

_KEY_RE = re.compile(r"^cpz_key_[a-f0-9]{24}$")
# Secret format: cpz_secret_ + exactly 48 base36-ish chars (0-9, a-z)
# Server validates against database, so SDK format check is just a sanity check
_SECRET_RE = re.compile(r"^cpz_secret_[a-z0-9]{48}$")


def validate_cpz_credentials(
    key: str,
    secret: str,
) -> Tuple[bool, Optional[str]]:
    """
    Validate CPZ key & secret format only.

    Mirrors server expectations:
      - key:  cpz_key_ + 24 hex chars
      - secret: cpz_secret_ + 48 base36-ish chars (0-9, a-z)

    Args:
        key: CPZ API key to validate
        secret: CPZ API secret to validate

    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is None.
    """
    if not key:
        return False, "CPZ API key is required"
    if not secret:
        return False, "CPZ API secret is required"

    if not _KEY_RE.match(key):
        return False, (
            "Invalid CPZ API key format. Expected 'cpz_key_' followed by 24 "
            "hex characters."
        )

    if not _SECRET_RE.match(secret):
        return False, (
            "Invalid CPZ API secret format. Expected 'cpz_secret_' followed by "
            "exactly 48 lowercase alphanumeric characters."
        )

    return True, None


def hash_cpz_token(key: str, secret: str) -> str:
    """
    Compute the same hash the backend stores in public.api_keys.key_hash.

    On the server:
      full_token = f"{key}.{secret}"
      key_hash   = sha256(full_token).hex()

    This function does exactly that, so tests can confirm the SDK matches
    server behavior, and for optional debugging (never log the secret itself).

    Args:
        key: CPZ API key
        secret: CPZ API secret

    Returns:
        SHA-256 hex digest of f"{key}.{secret}"
    """
    full_token = f"{key}.{secret}"
    return hashlib.sha256(full_token.encode("utf-8")).hexdigest()

