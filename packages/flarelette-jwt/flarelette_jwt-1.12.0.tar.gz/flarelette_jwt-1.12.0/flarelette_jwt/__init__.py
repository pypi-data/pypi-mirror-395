"""
Flarelette JWT Python Library

This package provides utilities for JWT signing, verification, and management.
It includes support for both symmetric (HS512) and asymmetric (EdDSA) algorithms.
"""

from .env import (
    ActorClaim,
    AlgType,
    JwtCommonConfig,
    JwtHeader,
    JwtPayload,
    JwtProfile,
    JwtValue,
    common,
    mode,
    profile,
)
from .explicit import (
    AuthUser as AuthUserWithConfig,
)
from .explicit import (
    AuthzOptsWithConfig,
    BaseJwtConfig,
    EdDSASignConfig,
    EdDSAVerifyConfig,
    HS512Config,
    SignConfig,
    VerifyConfig,
    check_auth_with_config,
    create_delegated_token_with_config,
    create_eddsa_sign_config,
    create_eddsa_verify_config,
    create_hs512_config,
    create_token_with_config,
    sign_with_config,
    verify_with_config,
)
from .high import AuthUser, check_auth, create_delegated_token, create_token, policy
from .secret import generate_secret, is_valid_base64url_secret
from .sign import sign
from .util import ParsedJwt, is_expiring_soon, map_scopes_to_permissions, parse
from .verify import verify

__version__ = "1.12.0-next.1765166794"

__all__ = [
    # Types
    "AlgType",
    "JwtValue",
    "JwtProfile",
    "JwtCommonConfig",
    "JwtHeader",
    "JwtPayload",
    "ActorClaim",
    "ParsedJwt",
    "AuthUser",
    # Explicit config types
    "BaseJwtConfig",
    "HS512Config",
    "EdDSASignConfig",
    "EdDSAVerifyConfig",
    "SignConfig",
    "VerifyConfig",
    "AuthzOptsWithConfig",
    "AuthUserWithConfig",
    # Environment-based functions
    "common",
    "mode",
    "profile",
    "check_auth",
    "create_token",
    "create_delegated_token",
    "policy",
    "generate_secret",
    "is_valid_base64url_secret",
    "sign",
    "is_expiring_soon",
    "map_scopes_to_permissions",
    "parse",
    "verify",
    # Explicit config functions
    "sign_with_config",
    "verify_with_config",
    "create_token_with_config",
    "create_delegated_token_with_config",
    "check_auth_with_config",
    "create_hs512_config",
    "create_eddsa_sign_config",
    "create_eddsa_verify_config",
]
