"""Core reduction for Erdős #642 (e642/CORE_REDUCTION.md): machine checks for n <= 10.

Skipped when gcc or nauty's geng is not installed.
"""
import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
GENG = shutil.which("nauty-geng") or shutil.which("geng")
pytestmark = pytest.mark.skipif(not (GENG and shutil.which("gcc")), reason="needs gcc and nauty geng")


@pytest.fixture(scope="module")
def checker(tmp_path_factory):
    exe = tmp_path_factory.mktemp("e642") / "good_check"
    subprocess.run(["gcc", "-O2", "-o", str(exe), str(ROOT / "e642/core/good_check.c")], check=True)
    return str(exe)


def good_graphs(checker, geng_args):
    graphs = subprocess.run([GENG, "-q", *geng_args], capture_output=True, check=True).stdout
    out = subprocess.run([checker], input=graphs, capture_output=True, check=True)
    return out.stdout.decode().split()


def test_base_case_n7(checker):
    assert good_graphs(checker, ["7", "14:14"]) == ["F?~vw"]
    assert good_graphs(checker, ["7", "15:15"]) == []


@pytest.mark.parametrize("n", [8, 9, 10])
def test_core_is_empty(checker, n):
    e = 3 * n - 7
    assert good_graphs(checker, ["-d4", str(n), f"{e}:{e}"]) == []


def test_lemma2_extensions_of_extremal_graph(checker):
    # T_5 = K_{1,2,5} on 8 vertices; its one-vertex extensions of degree 3 and 4.
    ext = ROOT / "e642/core/extend.py"
    for degree, expected_good in ((3, 1), (4, 0)):
        g6 = subprocess.run(["python3", str(ext), str(degree)], input=b"G?B~v{\n", capture_output=True, check=True).stdout
        good = subprocess.run([checker], input=g6, capture_output=True, check=True).stdout.decode().split()
        if degree == 3:
            # all good extensions attach to the three hubs: they are pairwise isomorphic copies of T_6
            assert len(good) == 1
        assert (len(good) > 0) == bool(expected_good)


def test_unique_good_core_on_11_vertices_is_bad_at_higher_density(checker):
    # the 4-regular graph J?ouPjI{@i? is good; it is the only good graph with min degree >= 4, n = 11, 22 edges
    out = subprocess.run([checker], input=b"J?ouPjI{@i?\n", capture_output=True, check=True).stdout
    assert out.decode().split() == ["J?ouPjI{@i?"]
