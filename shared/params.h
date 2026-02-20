/**
 * params.h - Shared constants for Geometric Prime Research
 *
 * Central parameter definitions used across all three projects.
 * Values derived from empirical analysis in unified-framework.
 */

#ifndef GPR_PARAMS_H
#define GPR_PARAMS_H

/* Golden ratio and related constants */
#define GPR_PHI           1.6180339887498948482
#define GPR_PHI_INV       0.6180339887498948482  /* 1/phi = phi - 1 */
#define GPR_SQRT5         2.2360679774997896964

/* Z-Framework calibration parameters */
#define GPR_KAPPA_STAR    0.04449   /* Cryptographic calibration constant */
#define GPR_KAPPA_GEO     0.3       /* Geodesic exponent (default) */

/* Precision defaults */
#define GPR_MPFR_PREC     256       /* Default MPFR precision in bits */
#define GPR_MILLER_RABIN_DEFAULT_REPS  25

/* Geometric factorization k-values (multi-pass sequence) */
#define GPR_K_WIDE        0.200     /* Wide-angle geometric lens */
#define GPR_K_BALANCED    0.450     /* Balanced precision/recall */
#define GPR_K_TELEPHOTO   0.800     /* High-precision targeting */

/* Epsilon sequence for multi-pass factorization */
#define GPR_EPS_TIGHT     0.02
#define GPR_EPS_MEDIUM    0.03
#define GPR_EPS_STANDARD  0.04
#define GPR_EPS_WIDE      0.05

#endif /* GPR_PARAMS_H */
