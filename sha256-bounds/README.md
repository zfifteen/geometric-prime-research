# SHA-256 Geometric Bounds (sha256-bounds)

Testing whether SHA-256 round constants exhibit geometric structure
beyond what random 32-bit primes would produce.

## Status: New investigation (extracted from 4096-pipeline observations)

## Core Idea

SHA-256 uses 64 round constants derived from the fractional parts of
cube roots of the first 64 primes. This project tests whether these
constants show statistically significant alignment with the phi-based
geometric framework at rates exceeding random chance.

## Key Observations (from unified-framework)

- 23-30% alignment rates observed across parameter grid
- H7 (8th hash value) shows notably lower alignment (18.2%)
- Bit correlation heatmaps generated for 5000-sample runs
- Effect needs rigorous null hypothesis testing

## Provenance

Extracted from:
- `unified-framework/src/c/4096-pipeline/VALIDATION_SUMMARY.md`
- `unified-framework/src/c/factorization-shortcut/experiment_summary.txt`

## Dependencies

- Standard C library (no GMP/MPFR needed for basic analysis)
- Optional: Python/matplotlib for visualization

## Build

```bash
make          # build sha256_bounds binary
make test     # run statistical tests
make clean    # cleanup
```

## Directory Structure

```
sha256-bounds/
  CLAIM.md          # falsifiable hypothesis
  README.md         # this file
  TODO.md           # research checklist
  Makefile
  src/
    sha256_bounds.c # alignment metric computation
    random_baseline.c # null hypothesis generator
    main.c          # CLI entry point
  data/
    sha256_constants.h  # the 64 round constants
```

## See Also

- [CLAIM.md](CLAIM.md) - falsifiable hypothesis and success/failure criteria
- [TODO.md](TODO.md) - research roadmap
- [../shared/params.h](../shared/params.h) - shared constants
