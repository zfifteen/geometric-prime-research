# Next Session Context

Open this file first when resuming work in `geometric-prime-research`.

## Current center of gravity

The strongest integrated note in this repo is `docs/RETAINED_LOCAL_STRUCTURE_NOTE.md`.

That note connects the current `sha256-bounds` work back to `geofac` through one empirical claim:

- Prime-derived transport appears to preserve local structure in `theta'(·, k)` space better than scalar alignment tests suggest.
- The strongest retained-locality regime we found is near `k = 0.45`.
- That same lens regime overlaps with the one already treated as important on the `geofac` side.

This was developed locally in this repo with deterministic probes and plots.

## Files added or updated in this repo

- `docs/RETAINED_LOCAL_STRUCTURE_NOTE.md`
- `sha256-bounds/scripts/plot_prime_survival.py`
- `sha256-bounds/out/prime_survival/prime_survival_shift_spectrum.png`
- `sha256-bounds/out/prime_survival/prime_survival_rank_transfer_k0_80.png`
- `sha256-bounds/out/prime_survival/prime_survival_summary_metrics.png`
- `sha256-bounds/out/prime_survival/prime_survival_motif_amplification.png`
- `sha256-bounds/out/prime_survival/prime_survival_stronger_controls.png`
- `sha256-bounds/out/prime_survival/prime_survival_family_transform_sweep.png`

## Main `sha256-bounds` finding already established here

The interesting signal is not plain phi alignment of SHA-256 constants in isolation.

The stronger result is source-conditioned local structure retention under `theta'(n, k)`.

Operationally:

- The real source-prime to SHA-constant pairing preserves local neighborhood relations better than deterministic re-pairing controls.
- Motif amplification works at first order and weakens by deeper motif depth.
- Stronger deterministic controls suggest the effect is real but not unique to the exact SHA family.
- The best lift clusters near `k = 0.45`.

## Important `z5dp` context

Do not recreate `z5dp` evidence from scratch without checking the archive first.

The current repo still has stubbed `z5dp` code:

- `z5dp/src/z5d_predictor.c`
- `z5dp/src/z5d_cli.c`

The working `z5dp` implementation and evidence live in the archive project:

- `/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor`

## Existing archive evidence already on disk

### Exact nth-prime ground truth

Exact reference tables already exist through `10^18`:

- `/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor/data/KNOWN_PRIMES.md`
- `/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor/data/ground-truth-primes.csv`

### Cross-language parity

The archive already contains a parity run showing the shipped benchmark grid passes across C, Python, and Java:

- `/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor/scripts/output/compare_latest.csv`

### Calibration evidence

The archive already contains a recorded calibration run and the comparison output:

- `/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor/CALIBRATION_RUN_2025-12-14.md`
- `/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor/scripts/output/calibration_comparison.csv`

### Big-`n` evidence

The archive README states the big-`n` path was exercised up to `10^1233`:

- `/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor/README.md`

The benchmark artifact already records a locked prime found for `k = 1e1233`:

- `/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor/benchmarks/z5d-mersenne/z5d_mersenne_2025-11-21T071019Z.csv`

There is already a verifier for those benchmark outputs:

- `/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor/benchmarks/z5d-mersenne/verify_primes.py`

### `10^1234` start-value support

The archive also already contains a forward prime walker that explicitly supports `--start 10^1234`:

- `/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor/src/c/prime-generator/prime_generator.c`

The archive C toolkit note already separates the roles cleanly:

- `z5d-predictor-c` for the calibrated nth-prime predictor
- `z5d-mersenne` for nearby-prime scanning at huge `k`
- `prime-generator` for walking forward from a large explicit start value such as `10^1234`

Reference:

- `/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor/src/c/C-IMPLEMENTATION.md`

## Boundary that should stay explicit

Based on the archive evidence already checked:

- Exact nth-prime support is already documented through `10^18`.
- Empirical large-`n` / nearby-prime support is already documented through the `10^1233` regime.
- Explicit prime-walking support from `10^1234` already exists.
- No exact nth-prime ground-truth artifact beyond `10^18` was found in the archive during this pass.

## File the user half-remembered

The large confirmed-prime corpus is probably:

- `/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor/data/ground-truth-primes.txt`

That file is the "largest known primes" corpus. It is useful reference data, but it is not an nth-prime ground-truth table.

## Good next moves

If resuming from here, the most useful next steps are:

1. Write a compact `z5dp` evidence note inside this repo using the archive artifacts that already exist.
2. Copy or summarize the archive proof chain into this repo without recomputing it.
3. Only build a new support script if its job is to gather and present existing artifacts rather than to reproduce work already done.

## Conversation constraints worth preserving

- Do not straw man the user.
- Do not widen the claim and then qualify the widened version.
- Prefer direct use of existing evidence over rerunning old experiments.
- Keep research artifacts narrow, deterministic, and easy to audit.
