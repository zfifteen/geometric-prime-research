# z5dp - Extraction TODO

Checklist for extracting Z5D nth-prime predictor from unified-framework.

## Phase 1: Core Extraction

- [ ] Copy `z5d_predictor.c` (core engine with Newton-Halley refinement)
- [ ] Copy `z5d_math.c` / `z5d_math.h` (Riemann R(x), Mobius, zeta zeros)
- [ ] Copy `z5d_cli.c` (CLI entry point)
- [ ] Copy `z5d_bench.c` (benchmark harness)
- [ ] Copy `include/z5d.h` public API header
- [ ] Verify 3-term Dusart initializer is intact
- [ ] Verify K=10 zeta zeros hardcoded correctly

## Phase 2: Build System

- [ ] Create standalone Makefile (no 4096-pipeline deps)
- [ ] Verify build with only GMP/MPFR
- [ ] Add `make bench` and `make test` targets

## Phase 3: Validation

- [ ] Reproduce 1-10 ppm accuracy against known prime tables
- [ ] Reproduce 100M+ predictions/second benchmark
- [ ] Verify Newton-Halley convergence rate
- [ ] Test edge cases (small n, large n, boundary primes)

## Phase 4: Cleanup

- [ ] Remove any 4096-pipeline integration code
- [ ] Remove geofac cross-references
- [ ] Ensure standalone operation
- [ ] Update README.md with final benchmarks

## Files to Extract From

| Source | What to Take |
|--------|-------------|
| `z5d-predictor-c/src/z5d_predictor.c` | Core predictor with Newton-Halley |
| `z5d-predictor-c/src/z5d_math.c` | R(x), Mobius function, zeta zeros |
| `z5d-predictor-c/src/z5d_math.h` | Math function declarations |
| `z5d-predictor-c/src/z5d_cli.c` | CLI interface |
| `z5d-predictor-c/src/z5d_bench.c` | Performance benchmarking |
| `z5d-predictor-c/include/` | Public headers |
| `z5d-predictor-c/SPEC.md` | Formal specification |
| `z5d-predictor-c/VERIFICATION.md` | Verification results |
