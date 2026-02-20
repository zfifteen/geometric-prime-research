# Parameter Reference

All tunable parameters defined in `shared/params.h`, with origins and usage.

## Mathematical Constants

| Macro | Value | Description |
|-------|-------|-------------|
| `GPR_PHI` | 1.6180339887498948482 | Golden ratio (phi) |
| `GPR_PHI_INV` | 0.6180339887498948482 | 1/phi = phi - 1 |
| `GPR_SQRT5` | 2.2360679774997896964 | Square root of 5 |

These are exact to 19 decimal places. MPFR versions use full precision at runtime.

## Z-Framework Calibration

| Macro | Value | Used by | Description |
|-------|-------|---------|-------------|
| `GPR_KAPPA_STAR` | 0.04449 | z5dp, geofac | Cryptographic calibration constant. Derived empirically from 4096-pipeline testing. Controls the Z5D predictor's scaling behavior. |
| `GPR_KAPPA_GEO` | 0.3 | z5dp | Geodesic exponent (default). Maps prime index to search space via geometric scaling. |

### Origin of kappa_star = 0.04449

This value emerged from systematic parameter sweeps in `unified-framework/src/c/4096-pipeline/z5d_key_gen.c`.
It minimizes the average search distance from Z5D prediction to nearest prime for 2048-bit targets.
The value is not theoretically derived — it is an empirical fit.

### Origin of kappa_geo = 0.3

Default geodesic exponent for the Z5D predictor. Controls how aggressively the search
space expands with prime index. Values tested in the 0.1–0.8 range; 0.3 balances
precision and convergence speed for RSA-scale primes.

## Precision Defaults

| Macro | Value | Description |
|-------|-------|-------------|
| `GPR_MPFR_PREC` | 256 | Default MPFR precision in bits. Sufficient for 2048-bit prime work. |
| `GPR_MILLER_RABIN_DEFAULT_REPS` | 25 | Miller-Rabin primality test iterations. Gives error probability < 4^(-25). |

## Geometric Factorization Parameters (geofac)

### k-values (lens sequence)

| Macro | Value | Description |
|-------|-------|-------------|
| `GPR_K_WIDE` | 0.200 | Wide-angle geometric lens. Broad candidate sweep. |
| `GPR_K_BALANCED` | 0.450 | Balanced precision/recall. Default first pass. |
| `GPR_K_TELEPHOTO` | 0.800 | High-precision targeting. Narrow focused search. |

The multi-pass factorization runs k-values in sequence: wide -> balanced -> telephoto.
Each pass narrows the search space using phi-coordinate geometry.

### Epsilon sequence (tolerance bands)

| Macro | Value | Description |
|-------|-------|-------------|
| `GPR_EPS_TIGHT` | 0.02 | Tightest tolerance. Fewest false candidates. |
| `GPR_EPS_MEDIUM` | 0.03 | Medium tolerance. |
| `GPR_EPS_STANDARD` | 0.04 | Standard tolerance. Default for initial testing. |
| `GPR_EPS_WIDE` | 0.05 | Widest tolerance. Most candidates, highest recall. |

Epsilon controls the phi-distance threshold for accepting a candidate factor.
Smaller epsilon = fewer candidates but higher precision per candidate.

## CLI Overrides

The z5dp CLI allows runtime override of key parameters:

```
./z5d_predict --kappa-geo 0.25 --kappa-star 0.04449 --bits 4096
```

The geofac CLI accepts k and epsilon overrides:

```
./geofac --k 0.450 --eps 0.03 <semiprime>
```

All CLI values take precedence over `params.h` defaults.
