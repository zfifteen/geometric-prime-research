# Z5D nth-Prime Predictor (z5dp)

High-precision nth-prime prediction via Riemann R(x) inversion with Newton-Halley refinement.

## Status: Extracting from unified-framework

## Core Idea

Solve R(x) = n for x, where R(x) is the Riemann prime-counting function.
The Z5D approach uses a 3-term Dusart initializer with Newton-Halley
refinement to achieve 1-10 ppm accuracy at speeds exceeding 100M predictions
per second.

## Key Results (from unified-framework)

- 1-10 ppm accuracy verified against known prime tables
- 100M+ predictions/second throughput
- K=10 Riemann zeta zeros for correction terms
- 3-term Dusart asymptotic initializer

## Provenance

Extracted from:
- `unified-framework/src/c/z5d-predictor-c/`

## Dependencies

- GMP (arbitrary precision)
- MPFR (multi-precision floating point)

## Build

```bash
make          # build z5dp binary
make bench    # run benchmark suite
make test     # run accuracy tests
make clean    # cleanup
```

## Directory Structure

```
z5dp/
  CLAIM.md            # falsifiable hypothesis
  README.md           # this file
  TODO.md             # extraction checklist
  Makefile
  src/
    z5d_predictor.c   # core predictor engine
    z5d_math.c        # mathematical utilities
    z5d_math.h        # math header
    z5d_cli.c         # CLI entry point
    z5d_bench.c       # benchmark harness
  include/
    z5d.h             # public API header
  tests/
    test_accuracy.sh  # ppm accuracy validation
```

## See Also

- [CLAIM.md](CLAIM.md) - falsifiable hypothesis and success/failure criteria
- [TODO.md](TODO.md) - extraction roadmap
- [../shared/params.h](../shared/params.h) - shared constants
