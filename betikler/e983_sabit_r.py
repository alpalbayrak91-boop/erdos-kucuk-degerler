"""Compute f(pi(n)+1, n) with the quantifier order of the Erdős 983 definition."""

from itertools import combinations
from math import isqrt
import sys


def f983(n):
    if n < 2:
        return 0
    primes = [p for p in range(2, n + 1) if all(p % d for d in range(2, isqrt(p) + 1))]
    k = len(primes) + 1

    # A set of primes covers 1 and those integers whose prime divisors it contains.
    factors = [{p for p in primes if a % p == 0} for a in range(1, n + 1)]
    bits = [1 << i for i in range(n)]
    for r in range(len(primes) + 1):
        # Primes above n can be replaced by unused primes <= n without losing coverage.
        covers = []
        for choice in combinations(primes, r):
            selected = set(choice)
            mask = sum(bit for bit, required in zip(bits, factors) if required <= selected)
            if mask.bit_count() > r:
                covers.append(mask)
        # Larger covers first is only a search heuristic.
        covers.sort(key=int.bit_count, reverse=True)
        for subset in combinations(bits, k):
            a_mask = sum(subset)
            if not any((a_mask & cover).bit_count() > r for cover in covers):
                break
        else:
            return r
    raise AssertionError("Taking all primes <= n always covers all k elements")


if __name__ == "__main__":
    limit = int(sys.argv[1])
    print([f983(n) for n in range(2, limit + 1)])
