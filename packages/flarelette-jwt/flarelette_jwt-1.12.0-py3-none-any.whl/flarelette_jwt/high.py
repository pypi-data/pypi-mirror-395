"""
High-Level JWT API

This module provides high-level functions for creating and verifying JWT tokens.
It includes support for delegated tokens and policy-based authorization.

@module util

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, TypedDict

from .sign import sign
from .verify import verify

if TYPE_CHECKING:
    from collections.abc import Callable

    from .env import JwtPayload


class AuthUser(TypedDict, total=False):
    """Authenticated user information returned by check_auth.

    Returned when a token passes both verification (signature valid, not expired)
    and authorization (all policy requirements met). Contains extracted identity
    and permission information for use in downstream authorization decisions.
    Never returned on verification/authorization failure - check_auth returns None instead.
    """

    sub: str | None
    permissions: list[str]
    roles: list[str]
    jti: str | None
    payload: JwtPayload


class PolicyBuilder(Protocol):
    """Builder interface for creating JWT authorization policies.

    Fluent API for composing authorization requirements used by check_auth().
    Chain methods to combine multiple requirements (all must pass for authorization).
    Enables readable, declarative policy definitions that separate authorization
    logic from business logic.
    """

    def base(self, **b: Any) -> PolicyBuilder: ...
    def need_all(self, *p: str) -> PolicyBuilder: ...
    def need_any(self, *p: str) -> PolicyBuilder: ...
    def roles_all(self, *r: str) -> PolicyBuilder: ...
    def roles_any(self, *r: str) -> PolicyBuilder: ...
    def where(self, fn: Callable[[JwtPayload], bool]) -> PolicyBuilder: ...
    def build(self) -> dict[str, Any]: ...


async def create_token(
    claims: JwtPayload,
    *,
    iss: str | None = None,
    aud: str | list[str] | None = None,
    ttl_seconds: int | None = None,
) -> str:
    """Create a signed JWT token with optional claims.

    Args:
        claims: Claims to include in the token (can include custom claims beyond standard JWT fields)
        iss: Optional issuer override
        aud: Optional audience override (string or list)
        ttl_seconds: Optional TTL override in seconds

    Returns:
        Signed JWT token string
    """
    return await sign(claims, iss=iss, aud=aud, ttl_seconds=ttl_seconds)


async def create_delegated_token(
    original_payload: JwtPayload,
    actor_service: str,
    *,
    iss: str | None = None,
    aud: str | list[str] | None = None,
    ttl_seconds: int | None = None,
) -> str:
    """Create a delegated JWT token following RFC 8693 actor claim pattern.

    Mints a new short-lived token for use within service boundaries where a service
    acts on behalf of the original end user. This implements zero-trust delegation:
    - Preserves original user identity (sub) and permissions
    - Identifies the acting service via 'act' claim
    - Prevents permission escalation by copying original permissions

    Pattern: "I'm <actor_service> doing work on behalf of <original user>"

    Example:
        Gateway receives Auth0 token for user@example.com with ["read:data"].
        Gateway creates delegated token for internal API service:

        ```python
        auth0_payload = await verify_auth0_token(external_token)
        internal_token = await create_delegated_token(
            original_payload=auth0_payload,
            actor_service="gateway-service",
            aud="internal-api"
        )
        # Result: {
        #   "sub": "user@example.com",
        #   "permissions": ["read:data"],  # Preserved from original
        #   "act": {"sub": "gateway-service"}
        # }
        ```

    Args:
        original_payload: The verified JWT payload from external auth (e.g., Auth0)
        actor_service: Identifier of the service creating this delegated token
        iss: Optional issuer override (defaults to env JWT_ISS)
        aud: Optional audience override (defaults to env JWT_AUD)
        ttl_seconds: Optional TTL override (defaults to env JWT_TTL_SECONDS)

    Returns:
        Signed JWT token string with delegation claim

    See Also:
        - RFC 8693: OAuth 2.0 Token Exchange
        - security.md: Service Delegation Pattern section
    """
    # Preserve original user context and permissions
    delegated_claims: dict[str, Any] = {
        "sub": original_payload.get("sub"),  # Original end user
        "permissions": original_payload.get("permissions", []),  # NO escalation
        "roles": original_payload.get("roles", []),
    }

    # Add actor claim - who is acting on behalf of the original user
    existing_act = original_payload.get("act")
    if existing_act:
        # Delegation chain: new actor wraps previous actor
        delegated_claims["act"] = {
            "sub": actor_service,
            "act": existing_act,
        }
    else:
        # First delegation
        delegated_claims["act"] = {"sub": actor_service}

    # Preserve additional context fields if present
    if original_payload.get("email"):
        delegated_claims["email"] = original_payload["email"]
    if original_payload.get("name"):
        delegated_claims["name"] = original_payload["name"]
    if original_payload.get("groups"):
        delegated_claims["groups"] = original_payload["groups"]
    if original_payload.get("tid"):
        delegated_claims["tid"] = original_payload["tid"]
    if original_payload.get("org_id"):
        delegated_claims["org_id"] = original_payload["org_id"]
    if original_payload.get("department"):
        delegated_claims["department"] = original_payload["department"]

    # Type cast to JwtPayload for type checking - safe because we control the structure
    return await sign(delegated_claims, iss=iss, aud=aud, ttl_seconds=ttl_seconds)  # type: ignore[arg-type]


async def check_auth(
    token: str,
    *,
    iss: str | None = None,
    aud: str | list[str] | None = None,
    leeway: int | None = None,
    require_all_permissions: list[str] | None = None,
    require_any_permission: list[str] | None = None,
    require_roles_all: list[str] | None = None,
    require_roles_any: list[str] | None = None,
    predicates: list[Callable[[JwtPayload], bool]] | None = None,
) -> AuthUser | None:
    """Verify and authorize a JWT token with policy enforcement.

    Args:
        token: JWT token string to verify
        iss: Optional issuer override
        aud: Optional audience override (string or list)
        leeway: Optional clock skew tolerance override in seconds
        require_all_permissions: All permissions that must be present
        require_any_permission: At least one of these permissions must be present
        require_roles_all: All roles that must be present
        require_roles_any: At least one of these roles must be present
        predicates: Custom validation functions

    Returns:
        AuthUser if valid and authorized, None otherwise
    """
    payload = await verify(token, iss=iss, aud=aud, leeway=leeway)
    if not payload:
        return None
    perms = payload.get("permissions") or []
    roles = payload.get("roles") or []
    if require_all_permissions and not set(require_all_permissions).issubset(perms):
        return None
    if require_any_permission and not set(require_any_permission).intersection(perms):
        return None
    if require_roles_all and not set(require_roles_all).issubset(roles):
        return None
    if require_roles_any and not set(require_roles_any).intersection(roles):
        return None
    if predicates:
        for fn in predicates:
            if not fn(payload):
                return None
    return {
        "sub": payload.get("sub"),
        "permissions": perms,
        "roles": roles,
        "payload": payload,
    }


def policy() -> PolicyBuilder:
    """Fluent builder for creating authorization policies.

    Returns:
        PolicyBuilder with chainable methods
    """
    opts: dict[str, Any] = {}

    class Builder:
        def base(self, **b: Any) -> PolicyBuilder:
            opts.update(b)
            return self

        def need_all(self, *p: str) -> PolicyBuilder:
            opts.setdefault("require_all_permissions", [])
            opts["require_all_permissions"].extend(p)
            return self

        def need_any(self, *p: str) -> PolicyBuilder:
            opts.setdefault("require_any_permission", [])
            opts["require_any_permission"].extend(p)
            return self

        def roles_all(self, *r: str) -> PolicyBuilder:
            opts.setdefault("require_roles_all", [])
            opts["require_roles_all"].extend(r)
            return self

        def roles_any(self, *r: str) -> PolicyBuilder:
            opts.setdefault("require_roles_any", [])
            opts["require_roles_any"].extend(r)
            return self

        def where(self, fn: Callable[[JwtPayload], bool]) -> PolicyBuilder:
            opts.setdefault("predicates", [])
            opts["predicates"].append(fn)
            return self

        def build(self) -> dict[str, Any]:
            return opts

    return Builder()
