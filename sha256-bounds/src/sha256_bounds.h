/**
 * sha256_bounds.h - SHA-256 Geometric Bounds Analysis Interface
 *
 * Tests whether SHA-256 round constants exhibit phi-based
 * geometric structure beyond random 32-bit primes.
 *
 * New investigation based on observations from 4096-pipeline.
 * See: sha256-bounds/CLAIM.md for hypothesis and test protocol.
 */

#ifndef SHA256_BOUNDS_H
#define SHA256_BOUNDS_H

#include <stdint.h>
#include "../../shared/params.h"

#ifdef __cplusplus
extern "C" {
#endif

/* The 64 SHA-256 round constants (first 32 bits of fractional
 * parts of cube roots of first 64 primes) */
#define SHA256_NUM_CONSTANTS 64
extern const uint32_t sha256_k[SHA256_NUM_CONSTANTS];

/**
 * Result from alignment analysis at a single epsilon.
 */
typedef struct {
    double epsilon;        /* Tolerance used */
    int    hits;           /* Number of constants that aligned */
    double alignment_rate; /* hits / SHA256_NUM_CONSTANTS */
    double p_value;        /* Monte Carlo p-value vs random baseline */
} sha256_alignment_t;

/**
 * Full analysis result across all epsilon values.
 */
typedef struct {
    int num_epsilons;
    sha256_alignment_t *results; /* Array of per-epsilon results */
    int monte_carlo_trials;      /* Number of random trials used */
    double elapsed_ms;
} sha256_analysis_t;

/**
 * Compute phi-distance for a single 32-bit constant.
 *
 * phi_distance = frac(value * phi) mapped to [0, 0.5]
 *
 * @param value  The 32-bit constant
 * @return       Phi-distance in [0, 0.5]
 */
double sha256_phi_distance(uint32_t value);

/**
 * Count alignment hits for SHA-256 constants at given epsilon.
 *
 * @param epsilon  Tolerance threshold
 * @return         Number of constants with phi_distance < epsilon
 */
int sha256_count_hits(double epsilon);

/**
 * Run full analysis with Monte Carlo baseline.
 *
 * @param epsilons     Array of epsilon values to test
 * @param num_epsilons Number of epsilon values
 * @param mc_trials    Number of Monte Carlo trials (0 = default 10000)
 * @param result       Output analysis result
 * @return             0 on success
 */
int sha256_analyze(const double *epsilons,
                   int num_epsilons,
                   int mc_trials,
                   sha256_analysis_t *result);

/**
 * Free resources in an analysis result.
 */
void sha256_analysis_free(sha256_analysis_t *result);

#ifdef __cplusplus
}
#endif

#endif /* SHA256_BOUNDS_H */
