# sha256-bounds - Research TODO

Checklist for SHA-256 geometric bounds investigation.

## Phase 1: Tooling

- [ ] Implement alignment metric computation for 64 SHA-256 round constants
- [ ] Implement random baseline generator (1000 sets of 64 random 32-bit constants)
- [ ] Implement two-sample t-test and KS test comparison
- [ ] Hardcode SHA-256 K constants in data/sha256_constants.h

## Phase 2: Parameter Sweep

- [ ] Sweep k_star: [0.02, 0.03, 0.04]
- [ ] Sweep width_factor: [0.3, 0.35, 0.4]
- [ ] Record alignment rates for each combination
- [ ] Compare against random baseline at each parameter point

## Phase 3: Statistical Testing

- [ ] Run t-test: SHA-256 alignment vs random alignment (target p < 0.01)
- [ ] Run KS test for distribution shape comparison
- [ ] Investigate H7 anomaly (18.2% vs 23-30% average)
- [ ] Generate bit correlation heatmaps

## Phase 4: Interpretation

- [ ] If p < 0.01: Document as previously unknown geometric structure
- [ ] If p > 0.05: Document null result and parameter sensitivity
- [ ] Write up findings regardless of outcome
- [ ] Assess cryptanalytic implications (likely none, but document)

## Data Sources

| Source | What to Extract |
|--------|----------------|
| `4096-pipeline/VALIDATION_SUMMARY.md` | Observed alignment rates |
| `factorization-shortcut/experiment_summary.txt` | Parameter grid results |
| NIST FIPS 180-4 | Official SHA-256 constants |
