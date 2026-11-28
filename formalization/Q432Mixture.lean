import Std
namespace EndpointMixture
/-- For a list of (weight, emission) pairs, this sum measures the distance of
the mixture from the upper endpoint multiplied by its total weight. -/
def gap (upper : Rat) (rows : List (Rat × Rat)) : Rat :=
  (rows.map fun (w,v) => w * (upper - v)).sum

theorem gap_nonnegative (upper : Rat) (rows : List (Rat × Rat))
    (h : ∀ p ∈ rows, 0 ≤ p.1 ∧ p.2 ≤ upper) : 0 ≤ gap upper rows := by
  induction rows with
  | nil => simp [gap]
  | cons p t ih =>
    have hh := h p (by simp)
    have ht := ih (by grind)
    have hp : 0 ≤ p.1 * (upper - p.2) := Rat.mul_nonneg hh.1 (by grind)
    change 0 ≤ p.1 * (upper-p.2) + gap upper t
    grind

theorem equality_iff (upper : Rat) (rows : List (Rat × Rat))
    (h : ∀ p ∈ rows, 0 ≤ p.1 ∧ p.2 ≤ upper) :
    gap upper rows = 0 ↔ ∀ p ∈ rows, 0 < p.1 → p.2 = upper := by
  induction rows with
  | nil => simp [gap]
  | cons p t ih =>
    have hh := h p (by simp)
    have bound : ∀ q ∈ t, 0 ≤ q.1 ∧ q.2 ≤ upper := by grind
    have ht := gap_nonnegative upper t bound
    have hp : 0 ≤ p.1 * (upper - p.2) := Rat.mul_nonneg hh.1 (by grind)
    change p.1 * (upper-p.2) + gap upper t = 0 ↔ _
    constructor
    · intro hz q hm hq
      have g : gap upper t = 0 := by grind
      rcases List.mem_cons.mp hm with rfl | hm
      · have product : q.1 * (upper-q.2) = 0 := by grind
        rcases Rat.mul_eq_zero.mp product with hzero | hzero <;> grind
      · exact (ih bound).mp g q hm hq
    · intro support
      have g : gap upper t = 0 := (ih bound).mpr (by grind)
      by_cases hz : 0 < p.1
      · have he := support p (by simp) hz
        grind
      · have he : p.1 = 0 := by grind
        grind
theorem gap_formula (upper : Rat) (rows : List (Rat × Rat)) :
    gap upper rows = (rows.map Prod.fst).sum * upper - (rows.map (fun p => p.1 * p.2)).sum := by
  induction rows with
  | nil => simp [gap]; grind
  | cons p t ih =>
    change p.1 * (upper - p.2) + gap upper t = _
    rw [ih]
    simp only [List.map_cons, List.sum_cons]
    grind

theorem normalized_endpoint (upper : Rat) (rows : List (Rat × Rat))
    (h : ∀ p ∈ rows, 0 ≤ p.1 ∧ p.2 ≤ upper) (unit : (rows.map Prod.fst).sum = 1) :
    (rows.map (fun p => p.1 * p.2)).sum = upper ↔
    ∀ p ∈ rows, 0 < p.1 → p.2 = upper := by
  rw [← equality_iff upper rows h, gap_formula, unit]
  grind
#print axioms normalized_endpoint
end EndpointMixture
