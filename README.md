# Geometric Prime Research

Focused research into three validated ideas extracted from [unified-framework](https://github.com/zfifteen/unified-framework).

## Projects

| Project | Description | Status |
|---------|-------------|--------|
| **[geofac/](geofac/)** | Geometric factorization heuristic using phi-space filtering | Skeleton |
| **[z5dp/](z5dp/)** | Z5D prime predictor via Riemann R(x) Newton solver | Skeleton |
| **[sha256-bounds/](sha256-bounds/)** | SHA-256 constant geometric bound analysis | Skeleton |

## Quick Start

### Prerequisites

```bash
# macOS
brew install gmp mpfr

# Ubuntu/Debian
sudo apt-get install libgmp-dev libmpfr-dev
```

### Build

```bash
make all        # Build all projects
make test       # Run all tests
make clean      # Clean build artifacts
```

## Repository Structure

```
geometric-prime-research/
  shared/           Shared MPFR/GMP utilities and constants
  geofac/           Geometric factorization heuristic
  z5dp/             Z5D prime predictor
  sha256-bounds/    SHA-256 bound analysis
  docs/             Architecture, provenance, parameter reference
```

## Provenance

This repo contains carefully extracted and validated code from the
[unified-framework](https://github.com/zfifteen/unified-framework) `src/c/` directory.
See [docs/PROVENANCE.md](docs/PROVENANCE.md) for exact source mappings.

## Key Principle

Each project has a `CLAIM.md` stating a falsifiable hypothesis with an explicit
null comparison. No code gets written until the claim is defined.

## License

MIT - see [LICENSE](LICENSE)
