/**
 * z5d_predictor.c - Z5D nth-Prime Predictor Implementation
 *
 * STUB - Implementation to be extracted from unified-framework.
 *
 * Algorithm overview:
 *   1. Dusart 3-term initializer: x0 = n*(ln(n) + ln(ln(n)) - 1 + ...)
 *   2. Newton-Halley refinement: solve R(x) = n iteratively
 *   3. R(x) computed via Gram series with Mobius function weights
 *
 * Origin: unified-framework/src/c/4096-pipeline/z5d_key_gen.c
 * See: docs/PROVENANCE.md
 */

#include "z5d_predictor.h"
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>

/* Mobius function values for k = 1..30 */
static const int mobius[] = {
    0,  /* mu(0) unused */
    1, -1, -1, 0, -1, 1, -1, 0, 0, 1,
    -1, 0, -1, 1, 1, 0, -1, 0, -1, 0,
    1, 1, -1, 0, 0, 1, 0, 0, -1, -1
};
#define MOBIUS_MAX 30

void z5d_config_defaults(z5d_config_t *cfg) {
    if (!cfg) return;
    cfg->kappa_star = GPR_KAPPA_STAR;
    cfg->kappa_geo  = GPR_KAPPA_GEO;
    cfg->phi        = GPR_PHI;
    cfg->precision  = GPR_MPFR_PREC;
}

void z5d_riemann_R(mpfr_t rop, const mpfr_t x, int terms, mp_prec_t prec) {
    if (terms <= 0) terms = MOBIUS_MAX;
    if (terms > MOBIUS_MAX) terms = MOBIUS_MAX;

    mpfr_t sum, xk, li_val, tmp;
    mpfr_init2(sum, prec);
    mpfr_init2(xk, prec);
    mpfr_init2(li_val, prec);
    mpfr_init2(tmp, prec);

    mpfr_set_ui(sum, 0, MPFR_RNDN);

    for (int k = 1; k <= terms; k++) {
        if (mobius[k] == 0) continue;

        /* xk = x^(1/k) */
        mpfr_set_ui(tmp, k, MPFR_RNDN);
        mpfr_ui_div(tmp, 1, tmp, MPFR_RNDN);
        mpfr_pow(xk, x, tmp, MPFR_RNDN);

        /* li_val = li(xk) = Ei(ln(xk)) */
        mpfr_log(tmp, xk, MPFR_RNDN);
        mpfr_eint(li_val, tmp, MPFR_RNDN);

        /* sum += mu(k)/k * li(x^(1/k)) */
        mpfr_div_si(li_val, li_val, k, MPFR_RNDN);
        if (mobius[k] == 1)
            mpfr_add(sum, sum, li_val, MPFR_RNDN);
        else
            mpfr_sub(sum, sum, li_val, MPFR_RNDN);
    }

    mpfr_set(rop, sum, MPFR_RNDN);

    mpfr_clear(sum);
    mpfr_clear(xk);
    mpfr_clear(li_val);
    mpfr_clear(tmp);
}

int z5d_invert_R(mpfr_t rop, unsigned long n, const z5d_config_t *cfg) {
    z5d_config_t defaults;
    if (!cfg) {
        z5d_config_defaults(&defaults);
        cfg = &defaults;
    }
    mp_prec_t prec = cfg->precision;

    /* Dusart 3-term initializer */
    double ln_n = log((double)n);
    double ln_ln_n = log(ln_n);
    double x0_d = n * (ln_n + ln_ln_n - 1.0
                       + (ln_ln_n - 2.0) / ln_n);

    mpfr_t x, Rx, diff, deriv;
    mpfr_init2(x, prec);
    mpfr_init2(Rx, prec);
    mpfr_init2(diff, prec);
    mpfr_init2(deriv, prec);

    mpfr_set_d(x, x0_d, MPFR_RNDN);

    int max_iter = 50;
    int iter;
    for (iter = 0; iter < max_iter; iter++) {
        z5d_riemann_R(Rx, x, 0, prec);

        /* diff = R(x) - n */
        mpfr_sub_ui(diff, Rx, n, MPFR_RNDN);

        /* Check convergence: |diff| < 0.5 */
        if (mpfr_cmp_d(diff, 0.5) < 0 && mpfr_cmp_d(diff, -0.5) > 0)
            break;

        /* Newton step: R'(x) ~ 1/ln(x) */
        mpfr_log(deriv, x, MPFR_RNDN);
        mpfr_div(diff, diff, deriv, MPFR_RNDN);

        /* x = x - diff * ln(x) */
        mpfr_sub(x, x, diff, MPFR_RNDN);
    }

    mpfr_set(rop, x, MPFR_RNDN);

    mpfr_clear(x);
    mpfr_clear(Rx);
    mpfr_clear(diff);
    mpfr_clear(deriv);

    return (iter < max_iter) ? iter : -1;
}

int z5d_predict(unsigned long n, const z5d_config_t *cfg, z5d_result_t *result) {
    if (!result) return -1;
    memset(result, 0, sizeof(*result));

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    z5d_config_t defaults;
    if (!cfg) {
        z5d_config_defaults(&defaults);
        cfg = &defaults;
    }

    mpfr_t predicted;
    mpfr_init2(predicted, cfg->precision);

    int iters = z5d_invert_R(predicted, n, cfg);
    result->converged = (iters >= 0) ? 1 : 0;
    result->iterations = (iters >= 0) ? iters : 0;

    /* Convert to integer (nearest) and then to decimal string */
    mpfr_t rounded;
    mpfr_init2(rounded, cfg->precision);
    mpfr_rint(rounded, predicted, MPFR_RNDN);

    mpz_t prime_z;
    mpz_init(prime_z);
    mpfr_get_z(prime_z, rounded, MPFR_RNDN);

    result->predicted_prime = mpz_get_str(NULL, 10, prime_z);

    /* TODO: Compute index_ratio against known prime tables */
    result->index_ratio = 1.0;

    clock_gettime(CLOCK_MONOTONIC, &t1);
    result->elapsed_ms = (t1.tv_sec - t0.tv_sec) * 1000.0
                       + (t1.tv_nsec - t0.tv_nsec) / 1e6;

    mpz_clear(prime_z);
    mpfr_clear(rounded);
    mpfr_clear(predicted);

    return 0;
}

void z5d_result_free(z5d_result_t *result) {
    if (!result) return;
    if (result->predicted_prime) {
        free(result->predicted_prime);
        result->predicted_prime = NULL;
    }
}
