# Architecture

## Repository Structure

```
geometric-prime-research/
  README.md               # root overview
  LICENSE                  # MIT
  .gitignore
  shared/
    params.h              # shared constants across all projects
  geofac/                 # geometric factorization
    CLAIM.md              # falsifiable hypothesis
    README.md             # project overview
    TODO.md               # extraction checklist
    Makefile
    src/                  # C source files
    tests/                # validation scripts
  z5dp/                   # Z5D nth-prime predictor
    CLAIM.md
    README.md
    TODO.md
    Makefile
    src/
    include/
    tests/
  sha256-bounds/          # SHA-256 geometric bounds
    CLAIM.md
    README.md
    TODO.md
    Makefile
    src/
    data/
  docs/                   # cross-cutting documentation
    ARCHITECTURE.md       # this file
    PROVENANCE.md         # where everything came from
    PARAMETER_REFERENCE.md # all tunable parameters
```

## Design Principles

1. **Each project is standalone** - can build and run independently
2. **Shared constants only** - `params.h` contains only mathematical constants
3. **Falsifiable claims** - every CLAIM.md has a null hypothesis and success criteria
4. **Clean extraction** - no broken imports from unified-framework
5. **No cross-project dependencies** - geofac, z5dp, sha256-bounds are independent

## Build Convention

Every project follows the same pattern:
```bash
cd <project>/
make          # build
make test     # validate
make clean    # cleanup
```

## Dependency Graph

```
shared/params.h
    |
    +-- geofac/   (GMP, MPFR, OpenSSL, OpenMP)
    +-- z5dp/     (GMP, MPFR)
    +-- sha256-bounds/ (standard C only)
```
