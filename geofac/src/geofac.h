/**
 * geofac.h - Geometric Factorization Interface
 *
 * Multi-pass semiprime factorization using golden-ratio
 * phi-coordinate geometry. Maps composite integers onto a
 * phi-scaled coordinate system where factor relationships
 * become geometric distances.
 *
 * Extracted from: unified-framework/src/c/geometric-factorization-repro/
 * See: docs/PROVENANCE.md for full lineage.
 */

#ifndef GEOFAC_H
#define GEOFAC_H

#include <gmp.h>
#include <mpfr.h>
#include "../../shared/params.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Configuration for a single factorization pass.
 */
typedef struct {
    double k;         /* Geometric lens parameter (e.g., GPR_K_WIDE) */
    double epsilon;   /* Phi-distance tolerance   (e.g., GPR_EPS_STANDARD) */
} geofac_pass_t;

/**
 * Result from a factorization attempt.
 */
typedef struct {
    int    success;          /* 1 if factor found, 0 otherwise */
    int    pass_index;       /* Which pass found the factor (0-based) */
    int    candidates_tried; /* Total candidates evaluated across all passes */
    double elapsed_ms;       /* Wall-clock time in milliseconds */
    char  *factor_p;         /* Decimal string of factor p (caller frees) */
    char  *factor_q;         /* Decimal string of factor q (caller frees) */
} geofac_result_t;

/**
 * Default multi-pass sequence: wide -> balanced -> telephoto
 * with standard epsilon at each stage.
 */
#define GEOFAC_DEFAULT_PASSES 3
extern const geofac_pass_t geofac_default_passes[GEOFAC_DEFAULT_PASSES];

/**
 * Attempt to factor a semiprime using geometric multi-pass.
 *
 * @param n           The semiprime to factor (decimal string)
 * @param passes      Array of pass configurations (NULL for defaults)
 * @param num_passes  Number of passes (0 for GEOFAC_DEFAULT_PASSES)
 * @param result      Output result struct
 * @return            0 on success (even if factor not found), nonzero on error
 */
int geofac_factor(const char *n_decimal,
                  const geofac_pass_t *passes,
                  int num_passes,
                  geofac_result_t *result);

/**
 * Compute phi-distance for a candidate factor.
 *
 * Maps the ratio (candidate / sqrt(n)) through the golden angle
 * and returns the fractional distance to the nearest phi-lattice point.
 *
 * @param distance  Output: phi-distance (0.0 = exact lattice hit)
 * @param n         The semiprime
 * @param candidate The candidate factor
 * @param k         Geometric lens parameter
 */
void geofac_phi_distance(mpfr_t distance,
                         const mpz_t n,
                         const mpz_t candidate,
                         double k);

/**
 * Free resources in a result struct.
 */
void geofac_result_free(geofac_result_t *result);

#ifdef __cplusplus
}
#endif

#endif /* GEOFAC_H */
