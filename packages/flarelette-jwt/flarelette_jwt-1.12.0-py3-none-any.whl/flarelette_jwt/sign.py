"""
JWT Signing Utilities

This module provides functions to sign JWT tokens using HS512 or EdDSA algorithms.
It supports custom claims and configuration overrides.

@module util

"""

from __future__ import annotations

import base64
import json
import time

# NOTE: 'js' module imported lazily inside functions - only available in Cloudflare Workers
from .env import AlgType, JwtPayload, common, get_hs_secret_bytes, mode


def _b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")


async def sign(
    payload: JwtPayload,
    *,
    iss: str | None = None,
    aud: str | list[str] | None = None,
    ttl_seconds: int | None = None,
) -> str:
    """Sign a JWT token with HS512 or EdDSA algorithm.

    Args:
        payload: Claims to include in the token (can include custom claims beyond standard JWT fields)
        iss: Optional issuer override
        aud: Optional audience override (string or list)
        ttl_seconds: Optional TTL override in seconds

    Returns:
        Signed JWT token string

    Raises:
        RuntimeError: If EdDSA signing is attempted (not supported in Python)
    """
    m: AlgType = mode("producer")
    cfg = common()
    iss = iss or cfg["iss"]
    aud = aud or cfg["aud"]
    ttl = int(ttl_seconds or cfg["ttl_seconds"])
    now = int(time.time())
    body = dict(payload)
    body.setdefault("iss", iss)
    body.setdefault("aud", aud)
    body.setdefault("iat", now)
    body.setdefault("exp", now + ttl)

    if m == "HS512":
        # Lazy import - only available in Cloudflare Workers/Pyodide runtime
        from js import crypto  # noqa: PLC0415
        from pyodide.ffi import to_py  # noqa: PLC0415

        header = {"alg": "HS512", "typ": "JWT"}
        h = _b64url(json.dumps(header, separators=(",", ":")).encode())
        p = _b64url(json.dumps(body, separators=(",", ":")).encode())
        signing_input = f"{h}.{p}".encode()
        key = await crypto.subtle.importKey(
            "raw",
            get_hs_secret_bytes(),
            {"name": "HMAC", "hash": "SHA-512"},
            False,
            ["sign"],
        )
        sig = await crypto.subtle.sign({"name": "HMAC"}, key, signing_input)

        return f"{h}.{p}.{_b64url(bytes(to_py(sig)))}"
    else:
        raise RuntimeError(
            "EdDSA signing is not supported in Workers Python; produce tokens with the Node gateway"
        )
