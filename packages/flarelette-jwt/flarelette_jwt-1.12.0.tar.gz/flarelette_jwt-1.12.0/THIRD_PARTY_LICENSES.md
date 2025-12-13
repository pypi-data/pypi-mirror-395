# Third-Party Licenses

This document lists all third-party software used by Flarelette JWT Kit, including:

- **TypeScript Package**: NPM dependencies for `@chrislyons-dev/flarelette-jwt`
- **Python Package**: Dependencies for `flarelette-jwt` (spoiler: zero runtime dependencies!)

---

## TypeScript Package (`@chrislyons-dev/flarelette-jwt`)

The TypeScript package depends on the following NPM packages:

### TypeScript Package Dependencies Summary

```
@flarelette/jwt-kit-env@1.8.1
│ C:\Users\chris\git\flarelette-jwt-kit
│
└─┬ @chrislyons-dev/flarelette-jwt@1.11.0 -> .\packages\flarelette-jwt-ts
  │ Environment-driven JWT authentication for Cloudflare Workers with secret-name indirection
  └── jose@6.1.3
      JWA, JWS, JWE, JWT, JWK, JWKS for Node.js, Browser, Cloudflare Workers, Deno, Bun, and other Web-interoperable runtimes
```

---

## Python Package (`flarelette-jwt`)

### Python Package Dependencies

**Runtime Dependencies**: None (zero external dependencies)

The Python package (`flarelette-jwt`) has **zero runtime dependencies**. It uses only the Cloudflare Workers Pyodide runtime and the built-in `js` module for WebCrypto operations.

**Development Dependencies** (not included in published package):

```
black>=23.0.0       # Code formatter (MIT)
ruff>=0.1.0         # Linter (MIT)
mypy>=1.7.0         # Type checker (MIT)
pytest>=7.4.0       # Test framework (MIT)
pytest-cov>=4.1.0   # Coverage plugin (MIT)
pytest-asyncio>=0.21.0  # Async test support (Apache-2.0)
```

---

## Cloudflare Workers Runtime

Both packages are designed for **Cloudflare Workers** which provides:

- **Node.js/V8 JavaScript Runtime**: Apache-2.0 / MIT  
  [https://github.com/cloudflare/workerd](https://github.com/cloudflare/workerd)

- **Pyodide (Python in WebAssembly)**: MPL-2.0  
  [https://github.com/pyodide/pyodide](https://github.com/pyodide/pyodide)

- **WebCrypto API**: Web standard implemented by Cloudflare Workers  
  Used for all cryptographic operations (HMAC-SHA512, EdDSA/Ed25519)

---

## Regenerating This File

To regenerate this file with the latest dependency information:

```bash
npm run licenses:generate
```

This script:

1. Scans TypeScript production dependencies via `license-checker`
2. Documents Python dependencies (development only - zero runtime deps)
3. Combines into this comprehensive license document

---

**Last generated**: 2025-12-08
