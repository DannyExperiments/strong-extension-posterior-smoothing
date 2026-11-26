#!/usr/bin/env python3
"""Check finite instances of the Q432 reduction using rational arithmetic."""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from random import Random

L, H, HALF = F(1, 4), F(3, 4), F(1, 2)


def satisfies(n, clauses):
    return any(all(any(bits[lit // 2] == lit % 2 for lit in clause)
                   for clause in clauses)
               for bits in product(range(2), repeat=n))


def units(n, clauses):
    variable = tuple((2*i, 2*i+1) for i in range(n))
    return tuple(clauses) + variable, variable


def extrema(n, clauses, enumerate_routes=False):
    positive, negative = units(n, clauses)
    gamma = F(1, 8*len(positive))
    prior = L + gamma/2
    best_score = best_revised = -1
    best_posterior = 0
    checked = 0
    for emissions in product((L, H), repeat=2*n):
        if enumerate_routes:
            route_scores = (
                (sum(emissions[x] for x in pos), sum(emissions[x] for x in neg))
                for pos, neg in product(product(*positive), product(*negative))
            )
        else:
            route_scores = [(
                sum(max(emissions[x] for x in u) for u in positive),
                sum(min(emissions[x] for x in u) for u in negative),
            )]
        for pos, neg in route_scores:
            rplus, rminus = pos/len(positive), neg/len(negative)
            evidence = L*rplus + H*rminus
            assert evidence >= L
            best_posterior = max(best_posterior, L*rplus/evidence)
            best_score = max(best_score, L*rplus - H*rminus)
            best_revised = max(best_revised, prior*rplus - (1-prior)*rminus)
            checked += 1
    sat = satisfies(n, clauses)
    assert (best_posterior == HALF) == sat and best_posterior <= HALF
    assert best_score == 0 if sat else best_score <= -gamma
    assert best_revised >= gamma/2 if sat else best_revised <= -gamma/4
    return best_posterior, checked


def literal_clauses(n):
    return [c for size in range(1, 4) for c in combinations(range(2*n), size)
            if len({x // 2 for x in c}) == size]


def weighted(row, values):
    return sum(p*v for p, v in zip(row, values))


def smoothed(row, eps):
    return tuple((1-eps)*p + eps/len(row) for p in row)


def branch_masses(prior, transition1, transition2, emission):
    likelihood2 = tuple(weighted(row, emission) for row in transition2)
    likelihood1 = tuple(weighted(row, likelihood2) for row in transition1)
    return tuple(p*r for p, r in zip(prior, likelihood1))


def signed(masses, initial):
    return 2*masses[initial] - sum(masses)


def check_positive_model(n, clauses):
    pos, neg = units(n, clauses)
    unit_count = len(pos) + len(neg)
    literal_offset = 2 + unit_count
    d = literal_offset + 2*n
    gamma, sat = F(1, 8*len(pos)), satisfies(n, clauses)
    prior_plus = L + gamma/2
    eps = gamma/128
    prior = (prior_plus, 1-prior_plus) + (F(0),)*(d-2)

    def uniform_on(indices):
        return tuple(F(1, len(indices)) if i in indices else F(0) for i in range(d))

    default = uniform_on((0,))
    transition1 = (uniform_on(tuple(range(2, 2+len(pos)))),
                   uniform_on(tuple(range(2+len(pos), 2+unit_count)))) + (default,)*(d-2)
    pos_prior = smoothed(prior, eps)
    pos_first = tuple(smoothed(row, eps) for row in transition1)
    best_upper, best_lower, cases = -1, 1, 0
    for emission_endpoints in product((L, H), repeat=2*n):
        emission = (HALF,)*literal_offset + emission_endpoints
        pos_emission = tuple(smoothed((p, 1-p), eps)[0] for p in emission)
        assert all(L <= p <= H for p in pos_emission)
        for selection in product(*(pos + neg)):
            rows = tuple(uniform_on((literal_offset + k,)) for k in selection)
            transition2 = (default,)*2 + rows + (default,)*(2*n)
            pos_second = tuple(smoothed(row, eps) for row in transition2)
            assert all(min(row) > 0 for row in (pos_prior,) + pos_first + pos_second)

            base = branch_masses(prior, transition1, transition2, emission)
            actual = branch_masses(pos_prior, pos_first, pos_second, pos_emission)
            assert sum(base) >= L and sum(actual) >= L
            assert sum(actual[2:]) > 0
            for q in (0, 1):
                assert abs(signed(actual, q)-signed(base, q)) <= 8*eps
            best_upper = max(best_upper, signed(actual, 0))
            best_lower = min(best_lower, signed(actual, 1))
            cases += 1
    assert (best_upper > 0) == sat and (best_lower < 0) == sat
    assert best_upper > 0 if sat else best_upper < 0
    assert best_lower < 0 if sat else best_lower > 0
    return cases


def main():
    example_a = ((0,), (0,))
    example_b = ((0,), (1,))
    assert extrema(1, example_a, True)[0] == HALF
    assert extrema(1, example_b, True)[0] == F(7, 16)
    print("Worked cases x AND x and x AND NOT x: maxima 1/2 and 7/16.")

    all_small = [c for m in (1, 2) for c in combinations_with_replacement(literal_clauses(2), m)]
    checked = sum(extrema(2, clauses, True)[1] for clauses in all_small)
    print(f"Full route/endpoint enumeration: {len(all_small)} formulas, {checked:,} precise models.")

    rng = Random(432)
    for _ in range(200):
        count = rng.randrange(1, 12)
        extrema(3, rng.choices(literal_clauses(3), k=count))
    print("Branchwise endpoint maximization: 200 seeded formulas.")

    positive_cases = ((1, example_a), (1, example_b),
                      (2, ((0, 2), (1, 2))), (2, ((0,), (1,), (2,))))
    checks = sum(check_positive_model(n, clauses) for n, clauses in positive_cases)
    print(f"Positive-row model checks: {checks:,} precise models, both single-state signs.")
    print("PASS: fixed-half threshold, evidence bound, and positive perturbation.")


if __name__ == "__main__":
    main()
