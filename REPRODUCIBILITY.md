# Reproduce the checks

Use Python 3.9 or newer from the repository root.

    python3 -I scripts/verify_repository.py
    python3 -I verification/src/replay.py

The replay uses the standard library and exact fractions. It enumerates every precise endpoint model of 44 small formulas and checks 200 seeded formulas by exact conditional optimization of the routing rows. It then constructs both full transformed transition tables and all emission rows for 1,312 small positive models. It checks both query signs and the coupling bound. [Recorded output](verification/logs/replay.txt)

The proofs of the general results appear in the [manuscript](paper/manuscript.pdf). [Build instructions](paper/BUILD.md) · [Visualization and rendering](visualization/README.md)
