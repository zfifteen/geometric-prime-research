# Provenance

Traceability map from `geometric-prime-research` back to `unified-framework`.

## Origin

All code and ideas in this repository were originally developed inside:

```
zfifteen/unified-framework  (private -> public)
  src/c/4096-pipeline/       # Z5D key gen, factorization shortcut
  src/c/geometric-factorization-repro/  # geofac multi-pass
```

This repo extracts the three cleanest, most falsifiable research threads
into standalone projects that can each build and test independently.

## File Mapping

### shared/params.h

| This repo | Origin in unified-framework |
|-----------|----------------------------|
| `shared/params.h` | Constants extracted from `src/c/4096-pipeline/z5d_key_gen.c` (kappa_star, kappa_geo, phi) and `src/c/geometric-factorization-repro/main.c` (k-values, epsilon sequence) |

### geofac/

| This repo | Origin in unified-framework |
|-----------|----------------------------|
| `geofac/src/main.c` | Stub extracted from `src/c/geometric-factorization-repro/main.c` |
| `geofac/CLAIM.md` | New — formalizes the hypothesis that was implicit in the original code |
| `geofac/Makefile` | Simplified from `src/c/geometric-factorization-repro/Makefile` |

### z5dp/

| This repo | Origin in unified-framework |
|-----------|----------------------------|
| `z5dp/src/z5d_cli.c` | Entry point extracted from `src/c/4096-pipeline/z5d_key_gen.c` (predictor logic only) |
| `z5dp/CLAIM.md` | New — formalizes the Z5D accuracy claim |
| `z5dp/Makefile` | Simplified from `src/c/4096-pipeline/Makefile` |

### sha256-bounds/

| This repo | Origin in unified-framework |
|-----------|----------------------------|
| `sha256-bounds/src/main.c` | New investigation inspired by observations in 4096-pipeline testing |
| `sha256-bounds/CLAIM.md` | New |
| `sha256-bounds/Makefile` | New |

## Key Commits in unified-framework

| Commit | Description |
|--------|-------------|
| `90adb1f` | Z5D factorization shortcut header and implementation |
| `d0b4646` | H7+Z recursive reduction benchmark on M1 Max |
| `6948cda` | AMX fast path and performance harness |
| `0c803bc` | Z5D factorization shortcut reference implementation |
| `548d77a` | Merge geometric factorization feature branch |

## What Changed During Extraction

1. **Removed**: Benchmark logs, temporary files, compiled binaries
2. **Removed**: GPU-specific code (Metal, AMX) — not part of core claims
3. **Added**: CLAIM.md files with null hypotheses and success criteria
4. **Added**: Shared params.h to centralize constants
5. **Restructured**: Flat pipeline directory into project-per-claim layout
6. **Simplified**: Makefiles to standard `make / make test / make clean` pattern
