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


S3 = ROOT / "adaylar" / "s3_e585_ayni_koseli_iki_cevrim"


def _e585_good(n: int, edges: set) -> bool:
    """True if no vertex set spans two edge-disjoint Hamiltonian cycles (brute force)."""
    from itertools import permutations

    for size in range(5, n + 1):
        for S in combinations(range(n), size):
            cycles = []
            for perm in permutations(S[1:]):
                cyc = (S[0],) + perm
                es = frozenset(tuple(sorted(p)) for p in zip(cyc, cyc[1:] + (S[0],)))
                if es <= edges:
                    cycles.append(es)
            if any(not (a & b) for a, b in combinations(cycles, 2)):
                return False
    return True


def test_s3_small_terms() -> None:
    data = _data(S3 / "oeis_draft.txt")
    pairs5 = list(combinations(range(5), 2))
    best = max(
        bin(mask).count("1")
        for mask in range(1 << 10)
        if _e585_good(5, {p for i, p in enumerate(pairs5) if mask >> i & 1})
    )
    assert data[:5] == [0, 1, 3, 6, best] == [0, 1, 3, 6, 9]


def test_s3_logs_agree_with_draft() -> None:
    data = _data(S3 / "oeis_draft.txt")
    good = {}
    for line in (S3 / "out" / "yontem_a.log").read_text(encoding="utf-8").splitlines():
        n, m = map(int, line.split()[:2])
        good[(n, m)] = int(re.search(r"good=(\d+)", line).group(1))
    for n in range(5, 11):
        assert good[(n, data[n - 1])] > 0 and good[(n, data[n - 1] + 1)] == 0
    f11 = (S3 / "out" / "f11_tarama.log").read_text(encoding="utf-8")
    assert re.search(r"11 32:32\): graphs=2173681 good=0", f11)
    assert re.search(r"11 31:31\): graphs=27749332 good=8", f11)
    assert data[10] == 31
    for n in range(1, 12):
        assert (S3 / "tanik" / f"uc_n{n}_m{data[n - 1]}.g6").exists()


def test_s3_certified_ladder_logs() -> None:
    data = _data(S3 / "oeis_draft.txt")
    lines = (S3 / "out" / "yontem_c_n12_t35.log").read_text(encoding="utf-8").splitlines()
    for line in lines:
        assert "errors=0" in line
        v = dict(re.findall(r"(\w+)=(\d+)", line))
        assert int(v["certificates"]) == int(v["valid"])
        assert int(v["candidates"]) == int(v["good"]) + int(v["certificates"])
    top = {int(re.search(r"^n=(\d+)", l).group(1)): max(int(k) for k in re.findall(r"(\d+):\d+", l.split("[")[1]))
           for l in lines}
    assert [top[n] for n in range(5, 13)] == data[4:12]
    n13 = (S3 / "out" / "yontem_c_n13_t41.log").read_text(encoding="utf-8")
    assert "candidates=792 good=0 certificates=792 valid=792 errors=0" in n13
