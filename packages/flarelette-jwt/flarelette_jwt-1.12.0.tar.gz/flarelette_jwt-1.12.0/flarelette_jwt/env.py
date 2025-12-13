"""
Environment Configuration for JWT Operations

This module provides functions to read environment variables and derive JWT-related configurations.
It supports both symmetric (HS512) and asymmetric (EdDSA) algorithms.

@module util

"""

import base64
import os
from typing import Any, Literal, TypedDict

# JWT algorithm types
# Only two algorithms supported by design:
# - HS512: Symmetric signing for trusted producer-consumer pairs (shared secret)
# - EdDSA: Asymmetric signing for public verification with key rotation support
# No RSA/ECDSA to reduce attack surface and simplify key management.
AlgType = Literal["HS512", "EdDSA"]

# JWT value types (JSON-compatible values used in claims and predicates)
# Constrains claim values to JSON-serializable types instead of Any.
# Enables type-safe claim handling while maintaining flexibility for custom claims.
# Used throughout signing, verification, and policy evaluation.
JwtValue = str | int | float | bool | list[str] | dict[str, Any] | None

# Type alias for JWT claims dictionary
# Standard pattern for passing claims with type safety.
# Maps string keys to JwtValue-constrained values, preventing unsafe Any types
# while allowing custom claims beyond the standard JwtPayload fields.
ClaimsDict = dict[str, JwtValue]


class JwtHeader(TypedDict, total=False):
    """JWT token header structure.

    Standard JWT header (RFC 7519) with algorithm and optional key ID.
    The `kid` field enables key rotation in EdDSA mode by identifying which
    public key in a JWKS should be used for verification. Required for production
    EdDSA deployments with multiple active keys.
    """

    alg: AlgType  # Algorithm: HS512 or EdDSA
    typ: str  # Token type, typically "JWT"
    kid: str  # Key ID for key rotation (optional)


class ActorClaim(TypedDict, total=False):
    """Actor claim for service delegation (RFC 8693).

    Identifies a service acting on behalf of another principal.
    Can be nested for delegation chains.

    Structure:
        sub: Service identifier acting on behalf of original subject
        iss: The issuer of the actor token.
        act: Nested ActorClaim with same structure (recursive delegation chain)
    """

    sub: str
    iss: str
    act: dict[
        str, JwtValue
    ]  # Nested ActorClaim (recursive, breaks TypedDict limitation)


class JwtPayload(TypedDict, total=False):
    """JWT token payload/claims structure.

    Includes standard JWT claims, OIDC claims, and common custom claims.
    Note: At runtime, can contain any string key with JwtValue-compatible values,
    but only defined fields get type checking.
    """

    # Standard JWT claims (RFC 7519)
    iss: str  # Issuer
    aud: str | list[str]  # Audience (single or multiple)
    sub: str  # Subject
    exp: int  # Expiration time (Unix timestamp)
    iat: int  # Issued at (Unix timestamp)
    nbf: int  # Not before (Unix timestamp)
    jti: str  # JWT ID

    # OIDC standard claims
    name: str  # Full name
    email: str  # Email address
    email_verified: bool  # Email verification status
    client_id: str  # OAuth2 client identifier
    cid: str  # Client ID (alternative)
    azp: str  # Authorized party
    scope: str  # Space-separated scope string (OAuth2)
    scopes: list[str]  # Scopes as array

    # Multi-tenant claims
    tid: str  # Tenant ID
    org_id: str  # Organization ID

    # Authorization claims
    permissions: list[str]  # Permission strings
    roles: list[str]  # Role strings
    groups: list[str]  # Group memberships
    user_role: str  # Primary user role
    department: str  # Department/division

    # Delegation claims (RFC 8693)
    act: ActorClaim  # Service acting on behalf of subject


class JwtProfile(TypedDict, total=False):
    """JWT Profile structure matching flarelette-jwt.profile.schema.json.

    Represents the complete configuration profile for JWT operations.
    Environment-driven: populated from JWT_* environment variables via profile() function.
    Validates against the JSON Schema at project root for consistency across languages.
    """

    version: int  # Optional, >= 1
    alg: AlgType  # Required: HS512 (symmetric) or EdDSA (asymmetric)
    aud: str | list[str]  # Required: single string or array of audience values
    iss: str  # Required: token issuer
    leeway_seconds: int  # Optional: clock skew tolerance in seconds (default: 90)


class JwtCommonConfig(TypedDict):
    """Common JWT configuration from environment variables.

    Subset of JwtProfile containing the fields shared across all operations
    (signing, verification, policy checks). Extracted by common() function
    and merged with algorithm-specific configuration in profile().
    """

    iss: str
    aud: str
    leeway: int
    ttl_seconds: int


def mode(role: str) -> AlgType:
    """Detect JWT algorithm mode from environment variables based on role.

    Args:
        role: Either "producer" (signing) or "consumer" (verification)

    Returns:
        AlgType: Either "HS512" or "EdDSA"
    """

    # Producers use private keys to sign
    if role == "producer" and (
        os.getenv("JWT_PRIVATE_JWK")
        or os.getenv("JWT_PRIVATE_JWK_PATH")
        or os.getenv("JWT_PRIVATE_JWK_NAME")
    ):
        return "EdDSA"

    # Consumers use public keys or JWKS to verify
    if role == "consumer" and (
        os.getenv("JWT_PUBLIC_JWK")
        or os.getenv("JWT_PUBLIC_JWK_NAME")
        or os.getenv("JWT_JWKS_URL")
        or os.getenv("JWT_JWKS_URL_NAME")
    ):
        return "EdDSA"

    return "HS512"


def common() -> JwtCommonConfig:
    """Get common JWT configuration from environment.

    Returns:
        JwtCommonConfig: Configuration with iss, aud, leeway, ttl_seconds
    """
    return {
        "iss": os.getenv("JWT_ISS", ""),
        "aud": os.getenv("JWT_AUD", ""),
        "leeway": int(os.getenv("JWT_LEEWAY", "90")),
        "ttl_seconds": int(os.getenv("JWT_TTL_SECONDS", "900")),
    }


def profile(role: str) -> dict[str, Any]:
    """Get JWT profile from environment.

    Returns complete JwtProfile-compatible configuration with detected algorithm.

    Args:
        role: Either "producer" (signing) or "consumer" (verification)

    Returns:
        dict containing alg, iss, aud, leeway_seconds, and ttl_seconds
    """
    alg = mode(role)
    cfg = common()

    return {
        "alg": alg,
        "iss": cfg["iss"],
        "aud": cfg["aud"],
        "leeway_seconds": cfg["leeway"],
        "ttl_seconds": cfg["ttl_seconds"],
    }


def _get_indirect(name_var: str, direct_var: str) -> str | None:
    name = os.getenv(name_var)
    if name and os.getenv(name):
        return os.getenv(name)
    return os.getenv(direct_var)


def get_hs_secret_bytes() -> bytes:
    s = _get_indirect("JWT_SECRET_NAME", "JWT_SECRET") or ""
    if not s:
        raise RuntimeError(
            "JWT secret missing: set JWT_SECRET_NAME -> bound secret, or JWT_SECRET"
        )
    try:
        b = base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
        if len(b) >= 32:
            return b
    except Exception:
        pass
    return s.encode("utf-8")


def get_public_jwk_string() -> str | None:
    return _get_indirect("JWT_PUBLIC_JWK_NAME", "JWT_PUBLIC_JWK")
