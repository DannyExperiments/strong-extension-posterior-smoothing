# Lean certificate

`EndpointMixture.normalized_endpoint` is checked using Lean 4.30.0 and its standard library.

A normalized finite mixture of rational emissions bounded by an upper endpoint attains that endpoint exactly when all positive-weight emissions attain it. This is the support implication used when recovering a truth assignment from the threshold gadget. The full posterior model, real-valued credal rows, the reduction and its complexity bounds are in the paper.

[Source](Q432Mixture.lean) · [Verification workflow](../.github/workflows/lean.yml)

To replay from the repository root with Lean 4.30.0 installed, run

```sh
lean -DwarningAsError=true formalization/Q432Mixture.lean
```

The source requests an axiom report. The GitHub Actions workflow downloads the pinned compiler, verifies its SHA-256 and checks the source with warnings treated as errors.
