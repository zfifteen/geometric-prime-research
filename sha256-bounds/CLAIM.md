# CLAIM: SHA-256 Round Constants Exhibit Geometric Structure

## Hypothesis

The 64 SHA-256 round constants (derived from cube roots of the first 64 primes)
show statistically significant alignment with phi-based geometric predictions
beyond what random 32-bit primes would produce.

## Null Hypothesis (H0)

The observed phi-alignment rates of SHA-256 round constants are consistent
with random 32-bit prime-derived constants. Any apparent geometric structure
is due to chance.

## Alternative Hypothesis (H1)

SHA-256 round constants exhibit phi-alignment rates that exceed the random
baseline by a statistically significant margin (p < 0.05), suggesting the
cube-root derivation from small primes introduces geometric structure.

## Preliminary Observations (from unified-framework)

- 23-30% alignment rates observed across parameter grid
- Random baseline expected around 15-18% for equivalent bit-width constants
- Effect appears strongest for constants derived from the smallest primes (2-19)
- Alignment measured using phi-distance metric with epsilon tolerance bands

## Success Criteria

1. **Reproduce**: Replicate the 23-30% alignment observation independently
2. **Quantify**: Compute exact p-value against random baseline via Monte Carlo
3. **Bound**: Determine whether the effect is specific to SHA-256 or generalizes
   to any cube-root-derived constants from small primes

## Test Protocol

1. Compute phi-distance for each of the 64 SHA-256 round constants
2. Count alignment hits at each epsilon in {0.02, 0.03, 0.04, 0.05}
3. Generate 10,000 random 32-bit constant sets (64 values each)
4. Compute alignment rates for random sets to establish baseline distribution
5. Report p-value: fraction of random sets with alignment >= observed

## Status

**Phase**: Skeleton (test protocol defined, implementation pending)

## Falsification

This claim is falsified if:
- The Monte Carlo p-value exceeds 0.05 at all epsilon values
- The alignment rate falls within the random baseline distribution
- The effect disappears when using cube roots of arbitrary (non-prime) integers
