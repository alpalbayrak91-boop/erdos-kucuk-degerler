"""Combine helper outputs into labeled counts (exact integer arithmetic).

method B: parse `countg --a` histograms ("<k> graphs : groupsize=<a>") of the
          induced-C4-free unlabeled n-vertex graphs; labeled = sum k * n!/a.
method C: parse s1_extend output ("<aut> <sum_v> <count>") for the (n-1)-vertex
          graphs; labeled(n) = sum (n-1)!/aut * sum_v.
method D: parse s1_extend2 output ("<aut> <sum_w> <count>") for the (n-2)-vertex
          graphs; labeled(n) = sum (n-2)!/aut * sum_w.
Usage: python3 s1_sum.py {B|C|D} n file
"""
import re
import sys
from math import factorial


def method_b(n, text):
    total, classes = 0, 0
    for k, a in re.findall(r"(\d+) graphs? : groupsize=(\d+)", text):
        k, a = int(k), int(a)
        assert factorial(n) % a == 0
        total += k * factorial(n) // a
        classes += k
    return classes, total


def method_c(n, text):
    total, classes = 0, 0
    for line in text.split("\n"):
        if not line.strip():
            continue
        aut, sv, cnt = map(int, line.split())
        assert factorial(n - 1) % aut == 0
        total += factorial(n - 1) // aut * sv
        classes += cnt
    return classes, total


def method_d(n, text):
    total, classes = 0, 0
    for line in text.split("\n"):
        if not line.strip():
            continue
        aut, sw, cnt = map(int, line.split())
        assert factorial(n - 2) % aut == 0
        total += factorial(n - 2) // aut * sw
        classes += cnt
    return classes, total


if __name__ == "__main__":
    mode, n, path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    text = open(path, encoding="utf-8").read()
    classes, total = {"B": method_b, "C": method_c, "D": method_d}[mode](n, text)
    print(n, classes, total)
