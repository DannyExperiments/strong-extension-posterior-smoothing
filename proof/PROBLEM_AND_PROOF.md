# Exact strong-extension smoothing is NP-complete

An input specifies a finite HMM with separately specified rational local credal polytopes: an initial distribution set, one transition-row set for each time and parent state, and one emission-row set for each time and hidden state. The strong extension is the convex hull of the factorizing laws. For a single-state event Q at any hidden time and a manifest partial assignment E, assume inf P(E)>0, as in the catalog. Decide whether sup P(Q|E) ≥ a supplied rational threshold. Under the analogous universal comparison the answer is coNP-complete. Computing the exact upper or lower posterior is NP-hard.

## Upper bound

For a convex combination of factorizing laws, P(Q|E) is an average of their posteriors, weighted by their probabilities of E. Each separately chosen row appears at most linearly in the joint mass of any assignment, so by expanding rows into their vertex combinations, every factorizing law is itself a convex combination of vertex-row choices. Consequently extrema are attained at such choices. If polytopes are given by rational linear constraints, each vertex has a rational encoding of polynomial bit length by Cramer's rule applied to independent tight constraints; if listed by vertices choose a listed row. A certificate needs only one rational feasible row per local set. A forward pass for E and one for Q∩E (insert the Q indicator at the query time) evaluates the comparison exactly. The arithmetic has polynomial bit length: the product of common denominators over all time-indexed tables is a common denominator for the joint masses and its bit length is polynomial. This proves NP membership on the stipulated positive-evidence inputs. The same reasoning applies to strict comparisons.

## Reduction

Given a 3-CNF formula with n≥1 variables and m≥1 clauses, set A=m+n, L=1/4 and H=3/4. Hidden states can use a common alphabet made of three disjoint classes:

1. At time 1 there are two reachable states + and − with probabilities A/(A+n) and n/(A+n). Query Q={state at time 1 is +}.
2. At time 2 there is one positive unit per clause and one positive unit per variable, as well as a separate negative unit per variable. State + has a fixed uniform transition onto its A positive units. State − has a fixed uniform transition onto its n negative units.
3. At time 3 there is one literal state for each of the 2n signed literals. A clause unit has the full simplex of transitions supported on its clause literals. Both units for a variable have their own full simplex on its two signed literals. Rows are separate for positive and negative units. At each literal state the emission row allows any Bernoulli success probability in [L,H], separately by literal state. Observe only final success. Other emissions, rows, and unreachable states may be precise and are immaterial. Each indicated simplex can be given by its point-mass vertices.

All state counts, table lengths (even if written densely), and rational encodings are polynomial. For any rows, let S_+ and S_- be the sums of success probabilities averaged within their chosen unit rows, respectively over the A positive units and the n negative units. Individual unit contributions are in [L,H], and
`P(Q|E)=S_+/(S_++S_-)`,
since each time-2 unit receives exactly 1/(A+n) unconditional mass and P(E)=(S_++S_-)/(A+n)≥L. The posterior can attain at most
`tau=AH/(AH+nL)`.
Strict monotonicity in these two positive arguments says equality holds exactly when every positive unit contributes H and every negative unit contributes L.

If the formula is satisfiable, make each true literal H and its opposite L. Route positive units to H-literals and negative units to L-literals. Conversely, any rows achieving tau force each variable's pair to contain both an H-literal (positive unit) and an L-literal (negative unit). This assigns a unique truth value to each variable because there are just two literals with distinct endpoint values. Each clause unit also needs an H-literal. Indeed no mixture can equal either endpoint unless it is supported on literals with that endpoint. So the induced truth assignment satisfies the formula. This proves NP-hardness and hence NP-completeness.

For the strict-threshold formulation, set δ=H−L. At a vertex-row maximizing choice all literal emissions are endpoints and all units are deterministic. If unsatisfiable, S_+≤AH−δ or S_-≥nL+δ. Thus the maximum is at most the larger of (AH−δ)/(AH−δ+nL) and AH/(AH+nL+δ), strictly below tau. A rational midpoint with tau is the comparison threshold. Minimization and universal threshold comparisons follow by the complementary state at time 1 (the initial law has precisely two reachable states) and complementing the decision. The two chosen positive bounds are independent of the tested formula, and the no-instance bound has polynomial encoding.

## Scope and prior work

This addresses general finite-state smoothing, not the entirely binary network case: the latter was already covered by the 2U algorithm. The unbounded alphabet in this construction does not settle the sharp fixed-cardinality boundary above two states. Unreferenced time steps do not require observing hidden states, and the reduction does not use tied cross-row parameters, nonseparate credal sets, or an exponentially small lower probability of evidence. It allows zeros in transitions.

Primary source: Mauá, de Campos, Benavoli, and Antonucci, [Probabilistic Inference in Credal Networks: New Complexity Results](https://doi.org/10.1613/jair.4355), §3.6 and conclusion. Its strong/epistemic equality for filtering/prediction applies to a final hidden query, and its general-tree hardness gadget is not an HMM. [Author manuscript](https://ipg.idsia.ch/preprints/maua14jair.pdf). The later [Algorithms for Hidden Markov Models With Imprecisely Specified Parameters](https://pure.qub.ac.uk/en/publications/algorithms-for-hidden-markov-models-with-imprecisely-specified-pa/) treats different algorithmic tasks. This proof is independently derived for Q432; publication priority is not certified.

This file records the recovered input-threshold proof. The [manuscript](../paper/manuscript.pdf) derives the fixed-half version, extends that version to positive rows, and gives the direct check for the lower single-state comparison after mixing.
