# Claims and evidence

| Claim | Evidence |
| --- | --- |
| Exact existential threshold comparisons are in NP | Manuscript §2. A vertex-row witness, polynomial rational encodings, exact two-pass verification. |
| NP-hardness at fixed one half | Manuscript §§3–4. Literal emissions are shared within each state. The variable-unit pairs enforce opposite endpoints and clause units test satisfiability. |
| Positivity and evidence lower bound | Manuscript §4. The fixed-half comparison has a signed gap, four relevant draws admit a coupling, and terminal success remains between one quarter and three quarters. |
| Lower and universal comparisons | Manuscript §4. Coupling checks the negative initial-state event directly. Complementation interchanges existential and universal comparisons. |
| Exact rational bound computation | Manuscript §5. NP-hardness and a polynomial-time upper bound with an NP oracle. |
| Scope relative to prior algorithms | Source and literature audit. Fully binary and final-query tractability and earlier general credal-tree hardness receive credit. |

### Scoped Lean result

A normalized finite mixture of rational emissions bounded by an upper endpoint attains that endpoint exactly when all positive-weight emissions attain it. This is the support implication used when recovering a truth assignment from the threshold gadget. The full posterior model, real-valued credal rows, the reduction and its complexity bounds are in the paper. [Declaration and replay](formalization/README.md)
