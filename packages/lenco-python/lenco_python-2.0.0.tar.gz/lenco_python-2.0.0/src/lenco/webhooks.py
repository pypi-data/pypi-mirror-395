"""Webhook verification utilities"""

import hashlib
import hmac
from typing import Any


def verify_webhook(payload: str | bytes | dict[str, Any], signature: str, secret: str) -> bool:
    """
    Verify a webhook signature.

    Args:
        payload: The raw request body (string, bytes, or dict)
        signature: The X-Lenco-Signature header value
        secret: Your API key (used as the signing secret)

    Returns:
        True if the signature is valid, False otherwise
    """
    if isinstance(payload, dict):
        import json
        body = json.dumps(payload, separators=(",", ":"))
    elif isinstance(payload, bytes):
        body = payload.decode("utf-8")
    else:
        body = payload

    expected_signature = hmac.new(
        secret.encode("utf-8"),
        body.encode("utf-8"),
        hashlib.sha512,
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)
