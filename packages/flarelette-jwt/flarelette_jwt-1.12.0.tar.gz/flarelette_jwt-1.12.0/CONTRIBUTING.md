# Contributing to Flarelette JWT

Thank you for your interest in contributing! This document provides guidelines for contributing to Flarelette JWT.

## Project Overview

**Flarelette JWT** is a polyglot JWT authentication toolkit with identical APIs for TypeScript and Python. Environment-driven JWT authentication for Cloudflare Workers. Like Starlette, but for the edge.

**Key principles:**

- Environment-driven configuration (no config files)
- Cross-language API parity (TypeScript ↔ Python)
- Security-first design with explicit trade-offs
- Zero external dependencies for Python (WebCrypto only)

## Getting Started

### Prerequisites

- **Node.js** 18+ and npm (for TypeScript)
- **Python** 3.11+ (for Python package)
- **Wrangler** CLI (for Cloudflare Workers testing)
- **Make** (optional, for convenience commands)

### Setup

See **[SETUP.md](SETUP.md)** for detailed setup instructions including pre-commit hooks and quality gates.

**Quick start:**

```bash
# Clone the repository
git clone https://github.com/your-org/flarelette-jwt-kit.git
cd flarelette-jwt-kit

# Install all dependencies (Node.js + Python)
npm install
pip install -e ".[dev]"

# Initialize git hooks (done automatically by npm install)
npm run prepare

# Build TypeScript package
npm run build
```

## Development Workflow

### Making Changes

1. **Create a feature branch** from `main`
2. **Make your changes** following the coding standards below
3. **Run quality checks** — Pre-commit hooks will run automatically, or use `npm run check`
4. **Test thoroughly** across both TypeScript and Python implementations
5. **Update documentation** if adding features or changing behavior
6. **Commit with conventional commits** (see below) — Commit message format is enforced
7. **Submit a pull request**

### Quality Gates

**Automatic (on commit):**

- Linting (ESLint for TS/JS, Ruff for Python)
- Formatting (Prettier for TS/JS/JSON/MD, Black for Python)
- Commit message validation (Conventional Commits)

**Manual (before push):**

```bash
# Run all checks
npm run check

# Or individual checks
npm run lint              # Lint TypeScript/JavaScript
npm run typecheck         # TypeScript type checking
npm run py:lint           # Lint Python
npm run py:typecheck      # Python type checking (MyPy)
```

See **[SETUP.md](SETUP.md)** for detailed information on quality gates and tooling.

### Documentation Syncing

The project maintains a single source of truth for documentation in the root directory (`README.md`, `CONTRIBUTING.md`, `THIRD_PARTY_LICENSES.md`, `LICENSE`). These files are automatically copied to packages during builds.

**When to sync:**

After editing any root documentation file (especially `README.md`), sync to the Python package:

```bash
npm run sync:docs
```

This runs `prepare.py` and stages the updated `README.md` in the Python package. Other files (`CONTRIBUTING.md`, `LICENSE`, etc.) are gitignored and only copied during CI/CD builds.

**Automated sync:**

- ✅ CI/CD builds automatically sync docs before publishing
- ✅ Package build scripts include doc copying
- ⚠️ Local development requires manual `npm run sync:docs`

**Why this matters:**

The Python package README is committed to the repository and must stay in sync with the root README. If out of sync, CI checks may fail with "Uncommitted changes detected."

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**

- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation only
- `refactor:` — Code restructuring without behavior change
- `test:` — Adding or updating tests
- `chore:` — Maintenance tasks

**Examples:**

```
feat(ts): add thumbprint pinning for EdDSA verification
fix(py): handle missing JWT_ISS gracefully
docs(security): clarify HS512 vs EdDSA trade-offs
```

## Code Standards

### General Principles

- **Security first:** Validate inputs, sanitize outputs, handle errors safely
- **Cross-language parity:** Maintain identical APIs between TypeScript and Python
- **Platform awareness:** Respect Cloudflare Workers limitations (especially for Python)
- **Fail-silent verification:** Return `null`/`None` on errors, don't throw
- **Environment-driven:** No configuration files or hardcoded defaults
- **Code must speak to us:** Use descriptive, intention-revealing names that eliminate the need for comments

For comprehensive coding standards including naming conventions and best practices, see **[docs/CODING_STANDARDS.md](docs/CODING_STANDARDS.md)**.

### TypeScript Guidelines

- Enable `strict` mode in `tsconfig.json`
- Use explicit types for public APIs
- Only `jose` library for cryptography (no other crypto dependencies)
- Prefer type narrowing over type assertions
- Use PascalCase for types/interfaces, camelCase for variables/functions

### Python Guidelines

- Use type hints for all public functions
- Follow PEP 8 style guidelines
- **Zero external dependencies** (use WebCrypto via `js` module only)
- All JWT operations must be `async` (Pyodide requirement)
- Use snake_case for functions/variables, PascalCase for classes

### Security Requirements

When modifying cryptographic code:

1. Validate against **docs/security.md** security baseline
2. Test both HS512 and EdDSA modes
3. Document key size requirements explicitly
4. Handle clock skew with `JWT_LEEWAY` for time-based claims
5. Never bypass or weaken signature verification

## Adding Features

### Cross-Language Feature Checklist

When adding a feature:

- [ ] Implement in TypeScript (`packages/flarelette-jwt-ts/src/`)
- [ ] Implement in Python (`packages/flarelette-jwt-py/flarelette_jwt/`)
- [ ] Ensure identical API surface (function names, parameters, return types)
- [ ] Test on Node.js and Cloudflare Workers (both languages)
- [ ] Respect Python limitations (no EdDSA signing, no remote JWKS)
- [ ] Support secret-name indirection pattern if adding new secrets
- [ ] Update **project documentation** with implementation details
- [ ] Update **COPILOT_INSTRUCTIONS.md** with key patterns
- [ ] Update **docs/usage.md** with user-facing examples
- [ ] Add type definitions and JSDoc/docstrings

### Mode Detection

**Do not add explicit `JWT_ALG` configuration.** Mode is auto-detected:

- EdDSA mode: Presence of `JWT_PRIVATE_JWK*` or `JWT_PUBLIC_JWK*` or `JWT_JWKS_URL*`
- HS512 mode: Otherwise (default)

If adding new algorithms, update `envMode()` in both `config.ts` and `env.py`.

## Testing

**Current state:** No test suite exists yet.

When implementing tests:

- Test both HS512 and EdDSA modes via environment variable injection
- Verify cross-language parity (same inputs produce same outputs)
- Cover authorization policy evaluation (roles, permissions, predicates)
- Test secret-name indirection resolution
- Test JWKS caching behavior (TypeScript only)
- Validate claim enforcement (`iss`, `aud`, `exp`, `nbf`)
- Test signature verification (positive and negative cases)

## Documentation Standards

**Target audience:** Software architects and engineers

**Tone:** Security-conscious, clear, and trustworthy (see **[notes/tone-of-voice.md](notes/tone-of-voice.md)**)

**Guidelines:**

- Be concise: 3–7 bullets or ≤120 words per section
- **Exception:** Security features may expand as needed
- Explain "why" behind patterns, not just "how"
- Use tables and executable code examples
- Keep documentation updated alongside code changes

**What to avoid:**

- Marketing speak or hyperbole
- Vague promises without technical specifics
- Academic abstractions that obscure practical meaning
- Downplaying security complexity

## Pull Request Process

1. **Ensure cross-language parity** — Both TypeScript and Python must work
2. **Update documentation** — Code without docs is incomplete
3. **Self-review** — Check against coding standards and tone guidelines
4. **Describe changes** — Include rationale and security implications
5. **Link related issues** — Reference GitHub issues if applicable

### PR Description Template

```markdown
## Summary

[Brief description of changes]

## Changes

- [List specific changes]

## Security Considerations

[Any security implications or trade-offs]

## Cross-Language Verification

- [ ] TypeScript implementation tested
- [ ] Python implementation tested
- [ ] API parity maintained
- [ ] Documentation updated

## Testing

[How you tested the changes]
```

## Code Review Expectations

Reviewers will check for:

- Cross-language API consistency
- Security best practices
- Platform compatibility awareness
- Documentation completeness
- Code clarity and maintainability
- Proper error handling (fail-silent for verification)

## Releases

The project uses automated releases via [release-please](https://github.com/googleapis/release-please):

- **Commits to main** using Conventional Commits trigger release automation
- **Release PRs** are automatically created with version bumps and CHANGELOG
- **Merging release PRs** publishes to npm and PyPI automatically

See **[RELEASING.md](RELEASING.md)** for detailed release process and **[RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)** for setup.

**For maintainers:** Ensure `NPM_TOKEN` and `PYPI_TOKEN` secrets are configured in repository settings.

## Questions?

- Review **docs/CODING_STANDARDS.md** for code quality standards
- See **docs/security.md** for security baseline
- See **RELEASING.md** for release process
- Open a GitHub issue for questions or discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
