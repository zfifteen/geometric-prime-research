# Z5D Prime Predictor: Falsifiable Claim

## Hypothesis

Newton-Raphson inversion of Riemann's prime counting function R(x)
provides fast, accurate nth-prime estimates suitable for indexed
prime access at arbitrary scales.

## Primary Claim

**The Z5D prime predictor achieves:**

- Accuracy within **1-10 ppm** of the true nth prime for n up to 10^12
- Throughput of **>100M predictions/second** on Apple M1 Max
- O(1) memory usage (no sieve storage required)
- 6 Newton iterations with Gram series R(x) evaluation suffice
  for convergence at 256-bit MPFR precision

## Null Comparison

Compare against:

1. **Direct Riemann approximation** (no Newton refinement): How much
   accuracy does iterative refinement add?
2. **Cipolla's approximation**: Standard nth-prime formula from literature.
   Is R(x) inversion actually better?
3. **Sieve-based lookup**: At what scale does Z5D become faster than
   precomputing with a sieve?

## Experiment Design

### Accuracy Test

1. For known primes at n = 10^3, 10^6, 10^9, 10^12
2. Compute z5d_predict_prime(n)
3. Compare to verified prime tables
4. Report ppm error and convergence rate

### Performance Test

1. Generate 10M prime predictions in sequence
2. Measure wall-clock time and throughput
3. Compare to sieve generation at same scale
4. Report crossover point where Z5D beats sieve

### Success Criteria

- ppm error < 10 for all tested scales
- Throughput > 100M pred/s
- Beats sieve for n > 10^8

## Prior Evidence

- SPEC.md documents 3-term initializer + 6-iteration Newton scheme
- README claims 154M pred/s (needs independent verification)
- Gram series evaluation implemented in geodesic_z5d_search.c

## What This Would Mean

**If confirmed**: Production-quality indexed prime generator enabling
cryptographic-scale experiments without memory-intensive sieves.
Direct enabler for geofac scaling.

**If refuted**: Newton convergence fails at scale, or accuracy
degrades beyond useful range. Fall back to segmented sieve.
