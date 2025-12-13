"""Example test file for Python JWT package.

Run with: npm run test:py or pytest packages/flarelette-jwt-py
"""

from __future__ import annotations

import pytest


def test_example() -> None:
    """Example test - should always pass."""
    assert True


def test_python_version() -> None:
    """Test that we're running Python 3.11+."""
    import sys

    assert sys.version_info >= (3, 11)


class TestEnvironmentSetup:
    """Test environment setup."""

    def test_pytest_configured(self) -> None:
        """Test that pytest is configured correctly."""
        assert pytest is not None


# TODO: Add actual JWT tests
# - HS512 signing and verification
# - EdDSA verification (with mock public keys)
# - Token expiration validation
# - Claim validation (iss, aud, exp, nbf)
# - Policy authorization (roles, permissions)
# - Secret-name indirection
# - Error cases (invalid tokens, expired tokens, etc.)
# - WebCrypto integration tests

# Note: EdDSA signing tests will fail in Python (by design)
# Mark those with @pytest.mark.skip(reason="EdDSA signing not supported in Python")
