"""Small-n checks for the sequence candidates in adaylar/ (pure Python, independent code)."""
from __future__ import annotations

import re
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S1 = ROOT / "adaylar" / "s1_induced_c4_free_labeled"
S2 = ROOT / "adaylar" / "s2_k43_free_colorings"


def labeled_no_induced_c4(n: int) -> int:
    pairs = list(combinations(range(n), 2))
    quads = list(combinations(range(n), 4))
    count = 0
    for mask in range(1 << len(pairs)):
        edges = {p for i, p in enumerate(pairs) if mask >> i & 1}
        ok = True
        for q in quads:
            if all(sum((min(v, w), max(v, w)) in edges for w in q if w != v) == 2 for v in q):
                ok = False
                break
        count += ok
    return count


def colorings_no_mono_4set(m: int) -> int:
    triples = list(combinations(range(m), 3))
    index = {t: i for i, t in enumerate(triples)}
    quads = [[index[t] for t in combinations(q, 3)] for q in combinations(range(m), 4)]
    count = 0
    for mask in range(1 << len(triples)):
        if all(0 < sum(mask >> i & 1 for i in q) < 4 for q in quads):
            count += 1
    return count


def _data(path: Path) -> list[int]:
    line = next(l for l in path.read_text(encoding="utf-8").splitlines() if l.startswith("%D"))
    return [int(x) for x in re.findall(r"\d+", line)]


def test_s1_small_terms() -> None:
    data = _data(S1 / "oeis_draft.txt")
    assert [labeled_no_induced_c4(n) for n in range(1, 6)] == data[:5] == [1, 2, 8, 61, 834]


def test_s2_small_terms() -> None:
    data = _data(S2 / "oeis_draft.txt")
    assert [colorings_no_mono_4set(m) for m in range(1, 6)] == data[:5] == [1, 1, 2, 14, 512]


def test_raw_outputs_agree_with_drafts() -> None:
    s1 = _data(S1 / "oeis_draft.txt")
    for name in ("method_B_n1_10.txt", "method_C_n2_11.txt", "method_D_n3_11.txt"):
        for line in (S1 / "out" / name).read_text(encoding="utf-8").split("\n"):
            if line.strip():
                n, _, total = map(int, line.split())
                assert s1[n - 1] == total
    s2 = _data(S2 / "oeis_draft.txt")
    for name in ("method_B1_onepoint_m7_8.txt", "method_B2_twopoint_m7_8.txt"):
        found = dict(re.findall(r"^([78]) (\d+)$", (S2 / "out" / name).read_text(encoding="utf-8"), re.M))
        assert int(found["7"]) == s2[6] and int(found["8"]) == s2[7]
