# geofac - Extraction TODO

Checklist for extracting geometric factorization from unified-framework.

## Phase 1: Core Extraction

- [ ] Copy `golden_spiral.h` and `golden_spiral.c` from geometric-factorization-repro
- [ ] Copy `main.c` entry point, strip non-geofac dependencies
- [ ] Extract phi-coordinate factorization logic from factorization-shortcut
- [ ] Merge multi-pass engine into single clean `geofac.c`
- [ ] Verify all MPFR constant definitions match `shared/params.h`

## Phase 2: Build System

- [ ] Create standalone Makefile (no cross-directory deps)
- [ ] Verify build on clean system with only GMP/MPFR/OpenSSL
- [ ] Add `make test` target wired to smoke_test.sh

## Phase 3: Validation

- [ ] Reproduce 39.8% success rate on balanced semiprimes
- [ ] Reproduce 20-26% alignment rates from parameter sweep
- [ ] Run null hypothesis test (random vs geometric) per CLAIM.md
- [ ] Document any parameter changes from original

## Phase 4: Cleanup

- [ ] Remove all references to rsa-4096-solver, golden-galois
- [ ] Remove any 4096-pipeline dependencies
- [ ] Ensure no broken imports or dead code paths
- [ ] Update README.md with final results

## Files to Extract From

| Source | What to Take |
|--------|-------------|
| `geometric-factorization-repro/golden_spiral.h` | Spiral search header |
| `geometric-factorization-repro/golden_spiral.c` | Spiral search impl |
| `geometric-factorization-repro/main.c` | CLI + multi-pass orchestration |
| `factorization-shortcut/experiment_summary.txt` | Parameter grid results |
| `factorization-shortcut/geofac_*.c` | Core factorization kernels |
