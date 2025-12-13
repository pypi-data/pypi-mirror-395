"""
Utility Functions for JWT Operations

This module provides helper functions for parsing JWTs, checking expiration,
and mapping OAuth scopes to permissions.

@module util

"""

import base64
import json
import time
from typing import Any, TypedDict

from .env import JwtHeader, JwtPayload


class ParsedJwt(TypedDict, total=True):
    """Parsed JWT token structure.

    Result of parsing a JWT without verification. Useful for inspecting claims
    before verification (e.g., routing decisions) or debugging token issues.
    Never trust the payload from parse() alone - always verify() for security-sensitive operations.
    """

    header: JwtHeader
    payload: JwtPayload


def parse(token: str) -> ParsedJwt:
    """Parse a JWT token into header and payload without verification.

    Args:
        token: JWT token string

    Returns:
        Dictionary with 'header' and 'payload' keys
    """
    hb, pb, *_ = token.split(".")

    def dec(s: str) -> Any:
        s = s + "=" * (-len(s) % 4)
        return json.loads(base64.urlsafe_b64decode(s.encode("utf-8")))

    return {"header": dec(hb), "payload": dec(pb)}


def is_expiring_soon(payload: JwtPayload, seconds: int) -> bool:
    """Check if JWT payload will expire within specified seconds.

    Args:
        payload: JWT payload with 'exp' claim
        seconds: Number of seconds threshold

    Returns:
        True if token expires within the threshold
    """
    now = int(time.time())
    return (int(payload.get("exp", 0)) - now) <= int(seconds)


def map_scopes_to_permissions(scopes: list[str]) -> list[str]:
    """Map OAuth scopes to permission strings.

    Args:
        scopes: List of OAuth scope strings

    Returns:
        List of permission strings (currently identity mapping)
    """
    return scopes
