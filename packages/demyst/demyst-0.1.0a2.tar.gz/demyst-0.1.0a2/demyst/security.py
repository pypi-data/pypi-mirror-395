"""
Demyst Security Module.

Handles cryptographic signing and verification of code integrity.
"""

import hashlib
import hmac
import os
from datetime import datetime
from typing import Dict, Optional

# Minimum key length for cryptographic security (256 bits = 32 bytes)
MIN_KEY_LENGTH = 32

# Track if we're in a context that allows missing key (e.g., when not using cert features)
_SECRET_KEY_CACHE: Optional[bytes] = None


def _get_secret_key() -> bytes:
    """
    Get the secret key from environment, with validation.

    Raises:
        ValueError: If DEMYST_SECRET_KEY is not set or is too short.
    """
    global _SECRET_KEY_CACHE

    if _SECRET_KEY_CACHE is not None:
        return _SECRET_KEY_CACHE

    key = os.environ.get("DEMYST_SECRET_KEY")
    if not key:
        raise ValueError(
            "DEMYST_SECRET_KEY environment variable must be set for certificate signing.\n"
            "Generate a secure key with: python -c 'from secrets import token_hex; print(token_hex(32))'"
        )

    if len(key) < MIN_KEY_LENGTH:
        raise ValueError(
            f"DEMYST_SECRET_KEY must be at least {MIN_KEY_LENGTH} characters (256 bits).\n"
            "Generate a secure key with: python -c 'from secrets import token_hex; print(token_hex(32))'"
        )

    _SECRET_KEY_CACHE = key.encode()
    return _SECRET_KEY_CACHE


def sign_code(code: str, verdict: str) -> Dict[str, str]:
    """
    Generates a cryptographic certificate of integrity for verified code.

    Args:
        code: The verified Python code.
        verdict: The result of the checks (e.g., "PASS", "FAIL").

    Returns:
        Dictionary containing the certificate details.

    Raises:
        ValueError: If DEMYST_SECRET_KEY environment variable is not set or invalid.
    """
    # Get validated secret key (raises if not configured)
    secret_key = _get_secret_key()

    timestamp = datetime.now().isoformat()
    code_hash = hashlib.sha256(code.encode()).hexdigest()

    # Create payload to sign
    payload = f"{code_hash}|{verdict}|{timestamp}"

    # Generate HMAC signature
    signature = hmac.new(secret_key, payload.encode(), hashlib.sha256).hexdigest()

    return {
        "code_hash": code_hash,
        "verdict": verdict,
        "timestamp": timestamp,
        "signature": signature,
    }


def verify_certificate(certificate: Dict[str, str]) -> bool:
    """
    Verifies a cryptographic certificate of integrity.

    Args:
        certificate: The certificate dictionary returned by sign_code.

    Returns:
        True if the certificate is valid, False otherwise.

    Raises:
        ValueError: If DEMYST_SECRET_KEY environment variable is not set or invalid.
    """
    try:
        secret_key = _get_secret_key()
    except ValueError:
        return False

    required_fields = ["code_hash", "verdict", "timestamp", "signature"]
    if not all(field in certificate for field in required_fields):
        return False

    code_hash = certificate["code_hash"]
    verdict = certificate["verdict"]
    timestamp = certificate["timestamp"]
    signature = certificate["signature"]

    # Reconstruct payload
    payload = f"{code_hash}|{verdict}|{timestamp}"

    # Generate expected signature
    expected_signature = hmac.new(secret_key, payload.encode(), hashlib.sha256).hexdigest()

    # Verify signature using constant-time comparison
    return hmac.compare_digest(signature, expected_signature)
