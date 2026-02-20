# Geometric Factorization (geofac)

Multi-pass semiprime factorization using golden-ratio phi-coordinate geometry.

## Status: Extracting from unified-framework

## Core Idea

Map composite integers onto a phi-scaled coordinate system where factor
relationships become geometric distances. The golden angle (137.5 deg)
spiral search exploits optimal packing to find factor candidates faster
than random probing.

## Key Results (from unified-framework)

- 39.8% success rate on balanced semiprimes (geometric-factorization-repro)
- 20-26% alignment rates across parameter grid (factorization-shortcut)
- Multi-pass architecture with golden spiral candidate generation

## Provenance

Extracted from:
- `unified-framework/src/c/geometric-factorization-repro/`
- `unified-framework/src/c/factorization-shortcut/`

## Dependencies

- GMP (arbitrary precision)
- MPFR (multi-precision floating point)
- OpenSSL (primality testing)
- OpenMP (optional, parallelism)

## Build

```bash
make          # build geofac binary
make test     # run smoke tests
make clean    # cleanup
```

## Directory Structure

```
geofac/
  CLAIM.md          # falsifiable hypothesis
  README.md         # this file
  TODO.md           # extraction checklist
  Makefile
  src/
    geofac.c        # core factorization engine
    golden_spiral.c # spiral search implementation
    golden_spiral.h # spiral search header
    main.c          # CLI entry point
  tests/
    smoke_test.sh   # basic validation
```

## See Also

- [CLAIM.md](CLAIM.md) - falsifiable hypothesis and success/failure criteria
- [TODO.md](TODO.md) - extraction roadmap
- [../shared/params.h](../shared/params.h) - shared constants
