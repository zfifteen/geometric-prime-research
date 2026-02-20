/**
 * z5d_predictor.h - Z5D nth-Prime Predictor Interface
 *
 * Predicts the nth prime via Riemann R(x) inversion with
 * Newton-Halley refinement. Uses Dusart 3-term initializer.
 *
 * Extracted from: unified-framework/src/c/4096-pipeline/z5d_key_gen.c
 * See: docs/PROVENANCE.md for full lineage.
 */

#ifndef Z5D_PREDICTOR_H
#define Z5D_PREDICTOR_H

#include <mpfr.h>
#include "../../shared/params.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Configuration for the Z5D predictor.
 * All fields have sane defaults from params.h.
 */
typedef struct {
    double kappa_star;   /* Calibration constant (default: GPR_KAPPA_STAR) */
    double kappa_geo;    /* Geodesic exponent   (default: GPR_KAPPA_GEO)  */
    double phi;          /* Golden ratio         (default: GPR_PHI)       */
    mp_prec_t precision; /* MPFR precision bits  (default: GPR_MPFR_PREC) */
} z5d_config_t;

/**
 * Result from a single prediction.
 */
typedef struct {
    int converged;         /* 1 if Newton-Halley converged */
    int iterations;        /* Number of refinement iterations used */
    double elapsed_ms;     /* Wall-clock time in milliseconds */
    char *predicted_prime; /* Decimal string of predicted prime (caller frees) */
    double index_ratio;    /* Predicted index / actual index (1.0 = exact) */
} z5d_result_t;

/**
 * Initialize config with default parameters from params.h.
 */
void z5d_config_defaults(z5d_config_t *cfg);

/**
 * Predict the nth prime using Z5D method.
 *
 * @param n       The prime index (1-based: n=1 gives 2, n=2 gives 3, ...)
 * @param cfg     Configuration (NULL for defaults)
 * @param result  Output result struct
 * @return        0 on success, nonzero on error
 */
int z5d_predict(unsigned long n, const z5d_config_t *cfg, z5d_result_t *result);

/**
 * Free resources in a result struct.
 */
void z5d_result_free(z5d_result_t *result);

/**
 * Compute Riemann R(x) using MPFR arithmetic.
 *
 * R(x) = sum_{k=1}^{K} mu(k)/k * li(x^{1/k})
 *
 * @param rop     Output: R(x)
 * @param x       Input value
 * @param terms   Number of terms in Gram series (0 = auto)
 * @param prec    MPFR precision
 */
void z5d_riemann_R(mpfr_t rop, const mpfr_t x, int terms, mp_prec_t prec);

/**
 * Invert R(x) = n using Newton-Halley iteration.
 *
 * @param rop     Output: x such that R(x) ~ n
 * @param n       Target prime count
 * @param cfg     Configuration
 * @return        Number of iterations, or -1 on failure
 */
int z5d_invert_R(mpfr_t rop, unsigned long n, const z5d_config_t *cfg);

#ifdef __cplusplus
}
#endif

#endif /* Z5D_PREDICTOR_H */
