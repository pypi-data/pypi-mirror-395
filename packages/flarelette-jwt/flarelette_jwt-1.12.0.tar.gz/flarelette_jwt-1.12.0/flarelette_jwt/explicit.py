"""
Explicit Configuration API for JWT Operations

This module provides functions that accept explicit configuration objects
instead of relying on environment variables or global state. Use this API
when you need full control over configuration, especially in development
environments or when working with multiple JWT configurations.

@module explicit
"""

from __future__ import annotations

import base64
import json
import time
from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from collections.abc import Callable

    from .env import JwtPayload


class BaseJwtConfig(TypedDict, total=False):
    """Base JWT configuration shared by HS512 and EdDSA modes.

    Attributes:
        iss: Token issuer (iss claim)
        aud: Token audience (aud claim) - can be string or list
        ttl_seconds: Token lifetime in seconds (default: 900 = 15 minutes)
        leeway: Clock skew tolerance in seconds for verification (default: 90)
    """

    iss: str
    aud: str | list[str]
    ttl_seconds: int
    leeway: int


class HS512Config(BaseJwtConfig):
    """HS512 (HMAC-SHA512) symmetric configuration.

    Uses a shared secret for both signing and verification.

    Attributes:
        alg: Must be 'HS512'
        secret: Shared secret key as bytes (minimum 32 bytes)
    """

    alg: Literal["HS512"]
    secret: bytes


class EdDSASignConfig(BaseJwtConfig):
    """EdDSA (Ed25519) asymmetric configuration for signing.

    Uses a private key to sign tokens.

    Attributes:
        alg: Must be 'EdDSA'
        private_jwk: Private JWK dictionary for signing
        kid: Key ID to include in JWT header (optional)
    """

    alg: Literal["EdDSA"]
    private_jwk: dict[str, Any]
    kid: str | None


class EdDSAVerifyConfig(BaseJwtConfig):
    """EdDSA (Ed25519) asymmetric configuration for verification.

    Uses a public key to verify tokens.

    Attributes:
        alg: Must be 'EdDSA'
        public_jwk: Public JWK dictionary for verification
    """

    alg: Literal["EdDSA"]
    public_jwk: dict[str, Any]


# Union types for convenience
SignConfig = HS512Config | EdDSASignConfig
VerifyConfig = HS512Config | EdDSAVerifyConfig


def _b64url(b: bytes) -> str:
    """Encode bytes to base64url without padding."""
    return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")


def _b64url_decode(s: str) -> bytes:
    """Decode base64url string (with or without padding)."""
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


async def sign_with_config(
    payload: JwtPayload,
    config: SignConfig,
    *,
    iss: str | None = None,
    aud: str | list[str] | None = None,
    ttl_seconds: int | None = None,
) -> str:
    """Sign a JWT token with explicit configuration.

    Examples:
        HS512 mode:
        >>> config: HS512Config = {
        ...     'alg': 'HS512',
        ...     'secret': b'your-32-byte-secret-here...',
        ...     'iss': 'https://gateway.example.com',
        ...     'aud': 'api.example.com',
        ...     'ttl_seconds': 900
        ... }
        >>> token = await sign_with_config({'sub': 'user123'}, config)

        EdDSA mode:
        >>> config: EdDSASignConfig = {
        ...     'alg': 'EdDSA',
        ...     'private_jwk': {'kty': 'OKP', 'crv': 'Ed25519', 'd': '...', 'x': '...'},
        ...     'kid': 'ed25519-2025-01',
        ...     'iss': 'https://gateway.example.com',
        ...     'aud': 'api.example.com'
        ... }
        >>> token = await sign_with_config({'sub': 'user123'}, config)

    Args:
        payload: Claims to include in the token
        config: Explicit JWT configuration
        iss: Optional per-call override for issuer
        aud: Optional per-call override for audience
        ttl_seconds: Optional per-call override for TTL

    Returns:
        Signed JWT token string

    Raises:
        ValueError: If secret is too short (< 32 bytes)
        RuntimeError: If EdDSA signing is attempted (not supported in Python Workers)
    """
    iss_val = iss or config.get("iss", "")
    aud_val = aud or config.get("aud", "")
    ttl = ttl_seconds or config.get("ttl_seconds", 900)

    now = int(time.time())
    body = dict(payload)
    body.setdefault("iss", iss_val)
    body.setdefault("aud", aud_val)
    body.setdefault("iat", now)
    body.setdefault("exp", now + ttl)

    if config["alg"] == "HS512":
        secret = config["secret"]
        if len(secret) < 32:
            raise ValueError(f"JWT secret too short: {len(secret)} bytes, need >= 32")

        # Lazy import - only available in Cloudflare Workers/Pyodide runtime
        from js import crypto  # noqa: PLC0415
        from pyodide.ffi import to_py  # noqa: PLC0415

        header = {"alg": "HS512", "typ": "JWT"}
        h = _b64url(json.dumps(header, separators=(",", ":")).encode())
        p = _b64url(json.dumps(body, separators=(",", ":")).encode())
        signing_input = f"{h}.{p}".encode()

        key = await crypto.subtle.importKey(
            "raw",
            secret,
            {"name": "HMAC", "hash": "SHA-512"},
            False,
            ["sign"],
        )
        sig = await crypto.subtle.sign({"name": "HMAC"}, key, signing_input)

        return f"{h}.{p}.{_b64url(bytes(to_py(sig)))}"
    else:
        # EdDSA mode
        raise RuntimeError(
            "EdDSA signing is not supported in Workers Python; produce tokens with the Node gateway"
        )


async def verify_with_config(
    token: str,
    config: VerifyConfig,
    *,
    iss: str | None = None,
    aud: str | list[str] | None = None,
    leeway: int | None = None,
) -> JwtPayload | None:
    """Verify a JWT token with explicit configuration.

    Examples:
        HS512 mode:
        >>> config: HS512Config = {
        ...     'alg': 'HS512',
        ...     'secret': b'your-32-byte-secret-here...',
        ...     'iss': 'https://gateway.example.com',
        ...     'aud': 'api.example.com'
        ... }
        >>> payload = await verify_with_config(token, config)

        EdDSA mode:
        >>> config: EdDSAVerifyConfig = {
        ...     'alg': 'EdDSA',
        ...     'public_jwk': {'kty': 'OKP', 'crv': 'Ed25519', 'x': '...'},
        ...     'iss': 'https://gateway.example.com',
        ...     'aud': 'api.example.com'
        ... }
        >>> payload = await verify_with_config(token, config)

    Args:
        token: JWT token string to verify
        config: Explicit JWT configuration
        iss: Optional per-call override for issuer
        aud: Optional per-call override for audience
        leeway: Optional per-call override for clock skew tolerance

    Returns:
        Payload if valid, None if invalid
    """
    iss_val = iss or config.get("iss", "")
    aud_val = aud or config.get("aud", "")
    leeway_val = leeway or config.get("leeway", 90)

    try:
        h_b64, p_b64, s_b64 = token.split(".")
        header = json.loads(_b64url_decode(h_b64))
        payload: JwtPayload = json.loads(_b64url_decode(p_b64))
        sig = _b64url_decode(s_b64)
    except Exception:
        return None

    # Lazy import - only available in Cloudflare Workers/Pyodide runtime
    from js import crypto  # noqa: PLC0415

    if config["alg"] == "HS512":
        if header.get("alg") != "HS512":
            return None

        secret = config["secret"]
        if len(secret) < 32:
            return None

        key = await crypto.subtle.importKey(
            "raw",
            secret,
            {"name": "HMAC", "hash": "SHA-512"},
            False,
            ["verify"],
        )
        ok = await crypto.subtle.verify(
            {"name": "HMAC"}, key, sig, (h_b64 + "." + p_b64).encode()
        )
        if not ok:
            return None
    else:
        # EdDSA mode
        if header.get("alg") != "EdDSA":
            return None

        jwk = config["public_jwk"]
        x_b64 = jwk.get("x")
        if not x_b64:
            return None

        x = _b64url_decode(x_b64)
        key = await crypto.subtle.importKey(
            "raw", x, {"name": "Ed25519"}, False, ["verify"]
        )
        ok = await crypto.subtle.verify(
            {"name": "Ed25519"}, key, sig, (h_b64 + "." + p_b64).encode()
        )
        if not ok:
            return None

    # Validate claims
    now = int(time.time())
    if payload.get("iss") != iss_val:
        return None
    if payload.get("aud") != aud_val:
        return None
    if now > int(payload.get("exp", 0)) + leeway_val:
        return None
    nbf = int(payload.get("nbf", payload.get("iat", 0)))
    if now + leeway_val < nbf:
        return None

    return payload


async def create_token_with_config(
    claims: JwtPayload,
    config: SignConfig,
    *,
    iss: str | None = None,
    aud: str | list[str] | None = None,
    ttl_seconds: int | None = None,
) -> str:
    """Create a signed JWT token with explicit configuration.

    Higher-level wrapper around sign_with_config for convenience.

    Args:
        claims: Claims to include in the token
        config: Explicit JWT configuration
        iss: Optional per-call override for issuer
        aud: Optional per-call override for audience
        ttl_seconds: Optional per-call override for TTL

    Returns:
        Signed JWT token string
    """
    return await sign_with_config(
        claims, config, iss=iss, aud=aud, ttl_seconds=ttl_seconds
    )


async def create_delegated_token_with_config(
    original_payload: JwtPayload,
    actor_service: str,
    config: SignConfig,
    *,
    iss: str | None = None,
    aud: str | list[str] | None = None,
    ttl_seconds: int | None = None,
) -> str:
    """Create a delegated JWT token with explicit configuration.

    Implements RFC 8693 actor claim pattern for service-to-service delegation.

    Example:
        >>> config: HS512Config = {
        ...     'alg': 'HS512',
        ...     'secret': b'my-secret...',
        ...     'iss': 'https://gateway.example.com',
        ...     'aud': 'internal-api'
        ... }
        >>> # Gateway receives Auth0 token and creates delegated token
        >>> auth0_payload = await verify_auth0_token(external_token)
        >>> internal_token = await create_delegated_token_with_config(
        ...     auth0_payload,
        ...     'gateway-service',
        ...     config
        ... )

    Args:
        original_payload: The verified JWT payload from external auth
        actor_service: Identifier of the service creating this delegated token
        config: Explicit JWT configuration
        iss: Optional per-call override for issuer
        aud: Optional per-call override for audience
        ttl_seconds: Optional per-call override for TTL

    Returns:
        Signed JWT token string with delegation claim
    """
    # Preserve original user context and permissions
    delegated_claims: dict[str, Any] = {
        "sub": original_payload.get("sub"),
        "permissions": original_payload.get("permissions", []),
        "roles": original_payload.get("roles", []),
    }

    # Add actor claim
    existing_act = original_payload.get("act")
    if existing_act:
        delegated_claims["act"] = {"sub": actor_service, "act": existing_act}
    else:
        delegated_claims["act"] = {"sub": actor_service}

    # Preserve additional context fields
    if "email" in original_payload:
        delegated_claims["email"] = original_payload["email"]
    if "name" in original_payload:
        delegated_claims["name"] = original_payload["name"]
    if "groups" in original_payload:
        delegated_claims["groups"] = original_payload["groups"]
    if "tid" in original_payload:
        delegated_claims["tid"] = original_payload["tid"]
    if "org_id" in original_payload:
        delegated_claims["org_id"] = original_payload["org_id"]
    if "department" in original_payload:
        delegated_claims["department"] = original_payload["department"]

    return await sign_with_config(
        delegated_claims,  # type: ignore[arg-type]
        config,
        iss=iss,
        aud=aud,
        ttl_seconds=ttl_seconds,
    )


class AuthzOptsWithConfig(TypedDict, total=False):
    """Authorization options for check_auth_with_config.

    Attributes:
        require_all_permissions: All permissions must be present
        require_any_permission: At least one permission must be present
        require_roles_all: All roles must be present
        require_roles_any: At least one role must be present
        predicates: Custom predicate functions that must all return True
    """

    require_all_permissions: list[str]
    require_any_permission: list[str]
    require_roles_all: list[str]
    require_roles_any: list[str]
    predicates: list[Callable[[JwtPayload], bool]]


class AuthUser(TypedDict, total=False):
    """Authenticated user information.

    Returned when a token passes both verification and authorization.

    Attributes:
        sub: Subject identifier
        permissions: List of permission strings
        roles: List of role strings
        jti: JWT ID
        payload: Complete JWT payload
    """

    sub: str | None
    permissions: list[str]
    roles: list[str]
    jti: str | None
    payload: JwtPayload


async def check_auth_with_config(
    token: str,
    config: VerifyConfig,
    authz_opts: AuthzOptsWithConfig | None = None,
    *,
    iss: str | None = None,
    aud: str | list[str] | None = None,
    leeway: int | None = None,
) -> AuthUser | None:
    """Verify and authorize a JWT token with explicit configuration.

    Example:
        >>> config: HS512Config = {
        ...     'alg': 'HS512',
        ...     'secret': b'my-secret...',
        ...     'iss': 'https://gateway.example.com',
        ...     'aud': 'api.example.com'
        ... }
        >>> user = await check_auth_with_config(token, config, {
        ...     'require_all_permissions': ['read:data'],
        ...     'require_any_permission': ['admin', 'editor']
        ... })
        >>> if user:
        ...     print('Authorized user:', user['sub'])

    Args:
        token: JWT token string to verify
        config: Explicit JWT configuration
        authz_opts: Authorization policy requirements
        iss: Optional per-call override for issuer
        aud: Optional per-call override for audience
        leeway: Optional per-call override for clock skew tolerance

    Returns:
        AuthUser if valid and authorized, None otherwise
    """
    payload = await verify_with_config(token, config, iss=iss, aud=aud, leeway=leeway)
    if not payload:
        return None

    opts = authz_opts or {}
    perms = payload.get("permissions", [])
    roles = payload.get("roles", [])

    # Check all required permissions
    if opts.get("require_all_permissions") and not all(
        p in perms for p in opts["require_all_permissions"]
    ):
        return None

    # Check any required permission
    if opts.get("require_any_permission") and not any(
        p in perms for p in opts["require_any_permission"]
    ):
        return None

    # Check all required roles
    if opts.get("require_roles_all") and not all(
        r in roles for r in opts["require_roles_all"]
    ):
        return None

    # Check any required role
    if opts.get("require_roles_any") and not any(
        r in roles for r in opts["require_roles_any"]
    ):
        return None

    # Check custom predicates
    for pred in opts.get("predicates", []):
        if not pred(payload):
            return None

    return {
        "sub": payload.get("sub"),
        "permissions": perms,
        "roles": roles,
        "jti": payload.get("jti"),
        "payload": payload,
    }


def create_hs512_config(
    secret: str | bytes,
    *,
    iss: str,
    aud: str | list[str],
    ttl_seconds: int = 900,
    leeway: int = 90,
) -> HS512Config:
    """Helper function to create HS512 config from base64url-encoded secret.

    Args:
        secret: Base64url-encoded secret string or raw bytes (minimum 32 bytes)
        iss: Token issuer
        aud: Token audience (string or list)
        ttl_seconds: Token lifetime in seconds (default: 900 = 15 minutes)
        leeway: Clock skew tolerance in seconds (default: 90)

    Returns:
        HS512Config

    Raises:
        ValueError: If secret is too short (< 32 bytes)
    """
    if isinstance(secret, str):
        # Decode base64url
        secret_bytes = _b64url_decode(secret.replace("-", "+").replace("_", "/"))
    else:
        secret_bytes = secret

    if len(secret_bytes) < 32:
        raise ValueError(f"JWT secret too short: {len(secret_bytes)} bytes, need >= 32")

    return {
        "alg": "HS512",
        "secret": secret_bytes,
        "iss": iss,
        "aud": aud,
        "ttl_seconds": ttl_seconds,
        "leeway": leeway,
    }


def create_eddsa_sign_config(
    private_jwk: dict[str, Any] | str,
    *,
    iss: str,
    aud: str | list[str],
    kid: str | None = None,
    ttl_seconds: int = 900,
    leeway: int = 90,
) -> EdDSASignConfig:
    """Helper function to create EdDSA sign config from JWK.

    Args:
        private_jwk: Private JWK dictionary or JSON string
        iss: Token issuer
        aud: Token audience (string or list)
        kid: Key ID (optional)
        ttl_seconds: Token lifetime in seconds (default: 900 = 15 minutes)
        leeway: Clock skew tolerance in seconds (default: 90)

    Returns:
        EdDSASignConfig
    """
    jwk = json.loads(private_jwk) if isinstance(private_jwk, str) else private_jwk

    return {
        "alg": "EdDSA",
        "private_jwk": jwk,
        "kid": kid,
        "iss": iss,
        "aud": aud,
        "ttl_seconds": ttl_seconds,
        "leeway": leeway,
    }


def create_eddsa_verify_config(
    public_jwk: dict[str, Any] | str,
    *,
    iss: str,
    aud: str | list[str],
    ttl_seconds: int = 900,
    leeway: int = 90,
) -> EdDSAVerifyConfig:
    """Helper function to create EdDSA verify config from JWK.

    Args:
        public_jwk: Public JWK dictionary or JSON string
        iss: Token issuer
        aud: Token audience (string or list)
        ttl_seconds: Token lifetime in seconds (default: 900 = 15 minutes)
        leeway: Clock skew tolerance in seconds (default: 90)

    Returns:
        EdDSAVerifyConfig
    """
    jwk = json.loads(public_jwk) if isinstance(public_jwk, str) else public_jwk

    return {
        "alg": "EdDSA",
        "public_jwk": jwk,
        "iss": iss,
        "aud": aud,
        "ttl_seconds": ttl_seconds,
        "leeway": leeway,
    }
