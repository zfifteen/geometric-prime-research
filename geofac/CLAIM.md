# Geometric Factorization: Falsifiable Claim

## Hypothesis

Prime factors of semiprimes N = p * q cluster non-uniformly in golden ratio
fractional-part space under the mapping:

```
theta'(n, k) = phi * {n / phi}^k  mod 1
```

This clustering enables a **pre-filtering heuristic** that reduces the number
of trial division candidates needed to find a factor.

## Primary Claim

**For balanced semiprimes N < 10^6 with epsilon = 0.05:**

- Phi-space filtering achieves **20-26% factorization success rate**
  (at least one factor passes the geometric filter)
- This produces a **~3x speedup** over naive trial division
  (testing only ~30% of primes instead of all primes up to sqrt(N))
- Multi-pass k-sequence (k = 0.200, 0.450, 0.800) achieves **30-40%**
  combined success rate

## Null Hypothesis (CRITICAL)

A **random filter** of equivalent selectivity (accepting ~30% of candidates)
achieves the same or better success rate as phi-space filtering.

If the null cannot be rejected, the geometric structure is illusory and the
speedup is purely from random candidate reduction.

## Experiment Design

### Test Protocol

1. Generate 1000 random balanced semiprimes N < 10^6
2. For each N, enumerate all primes up to sqrt(N)
3. **Phi filter**: Keep primes where |theta'(p,k) - theta'(N,k)| < epsilon
4. **Random filter**: Keep a random ~30% subset of primes (matched selectivity)
5. Test divisibility on filtered candidates
6. Compare success rates with Wilson 95% confidence intervals

### Success Criteria

- Phi-filter success rate **significantly exceeds** random-filter success rate
  (non-overlapping 95% CIs)
- Effect persists across multiple random seeds
- Effect persists as N scales (10^4, 10^6, 10^8)

### Failure Criteria

- Confidence intervals overlap: geometric structure is not statistically
  significant
- Success rate decreases with scale: artifact of small numbers

## Prior Evidence

- Python gist (validated): 23% success, 3x speedup at N < 10^6
- Multi-pass experimental report: 25-40% projected combined success
- C implementation: BROKEN (random generation, not sieve-based)

## What This Would Mean

**If confirmed**: Novel constant-factor improvement to trial division based on
previously unknown geometric structure in prime distribution. Publishable as
arXiv preprint. NOT sub-exponential, NOT RSA-breaking.

**If refuted**: The phi-space mapping produces visually appealing patterns
but no actual information about factor location. Close this project.
