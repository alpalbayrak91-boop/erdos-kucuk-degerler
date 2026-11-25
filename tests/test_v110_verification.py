"""Comprehensive verification suite for erdos-kucuk-degerler v1.1.0."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from e151_audit.even_cycle_audit import run_audit  # noqa: E402
from e642.verify_e642 import (  # noqa: E402
    construct_k3_bipartite_plus_p3,
    is_erdos642_valid_bitmask,
    is_valid_by_cycle_enumeration,
    solve_erdos642_max_edges,
)
from e983.e983_exact_z3 import brute_e983_both, verify_adversarial_witness  # noqa: E402

FORBIDDEN_TOKEN_SHA256 = frozenset(
    {
        "23ae65de3e23466e0a258ce6919553b77a107bb4c6dcd92bf6c32fe75d6e34a0",
        "3c96af1ad0d139aa11b6f768cd816892ecfe1ee59d873049f3a09619c3080218",
        "8b5727cdcd93895d8bf2bbd016848c351e289e65af038c9618221480f8da7d0a",
        "995b84db0d9e98732b69fde4743792996d7fdde7c731da6cb5749266d5334492",
    }
)


def test_e642_witnesses_and_exact_values() -> None:
    data = json.loads((ROOT / "e642" / "witnesses_n0_to_9.json").read_text(encoding="utf-8"))
    expected_2_to_9 = [1, 3, 6, 9, 11, 14, 17, 20]
    assert data["f_seq_2_to_9"] == expected_2_to_9
    assert data["f_seq_0_to_9"] == [0, 0] + expected_2_to_9

    by_n = {row["n"]: row for row in data["witnesses"]}
    for idx, n in enumerate(range(2, 10)):
        row = by_n[n]
        edges = row["edges"]
        assert len(edges) == expected_2_to_9[idx]
        assert is_valid_by_cycle_enumeration(n, edges), f"Cycle chord check failed at n={n}"
        adj = [0] * n
        for u, v in edges:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        assert is_erdos642_valid_bitmask(n, adj), f"Bitmask cycle check failed at n={n}"

    # Verify independent Python branch-and-bound solver up to n = 8
    bnb_vals = [solve_erdos642_max_edges(n)[0] for n in range(2, 9)]
    assert bnb_vals == [1, 3, 6, 9, 11, 14, 17]

    # Verify general 3n - 7 construction K_{3, n-3} + P_3 for n = 6..10
    for n in range(6, 11):
        gn = construct_k3_bipartite_plus_p3(n)
        assert len(gn) == 3 * n - 7
        adj = [0] * n
        for u, v in gn:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        assert is_erdos642_valid_bitmask(n, adj)

    gcc = shutil.which("gcc")
    if gcc is not None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bin_path = Path(tmpdir) / "e642_exact"
            comp = subprocess.run(
                [gcc, "-O3", "-Wall", "-Wextra", str(ROOT / "e642" / "e642_exact.c"), "-o", str(bin_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            assert comp.returncode == 0, comp.stderr
            canon = subprocess.run([str(bin_path), "--test-canon"], capture_output=True, text=True, check=False)
            assert canon.returncode == 0, canon.stdout + canon.stderr


def test_e983_json_witnesses_and_bruteforce() -> None:
    data = json.loads((ROOT / "e983" / "e983_exact_46.json").read_text(encoding="utf-8"))
    assert data["n_range"] == [2, 46]
    assert data["f_le_seq"] == data["f_eq_seq"]
    assert data["divergences"] == []
    assert len(data["rows"]) == 45

    expected_prefix_2_to_16 = [0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4]
    assert data["f_eq_seq"][:15] == expected_prefix_2_to_16

    for row in data["rows"]:
        n = row["n"]
        f_le = row["f_le"]
        f_eq = row["f_eq"]
        assert f_le == f_eq
        assert f_eq <= row["erdos_straus_ub"]
        wit = row.get("lower_bound_witness_A")
        if f_eq == 0:
            assert n in (2, 3)
        else:
            assert isinstance(wit, list) and len(wit) == row["k"]
            assert verify_adversarial_witness(n, wit, f_eq - 1, exact_eq=True), f"Invalid eq witness at n={n}"
            assert verify_adversarial_witness(n, wit, f_le - 1, exact_eq=False), f"Invalid le witness at n={n}"

    # Direct brute-force cross-check on n = 2..16
    for n in range(2, 17):
        bf_le, bf_eq = brute_e983_both(n)
        expected_val = data["f_eq_seq"][n - 2]
        assert bf_le == expected_val and bf_eq == expected_val


def test_e151_even_cycle_audit_and_lean4_proof() -> None:
    audit_res = run_audit()
    assert audit_res["even_cycle_free_n1_to_8"] == [0, 1, 3, 4, 6, 7, 9, 10]
    assert audit_res["oeis_exact"] == "A032766"
    assert audit_res["a380408_div_24"] == [37, 36]

    lean_file = ROOT / "formal" / "Erdos151EvenCycleA032766Audit.lean"
    lean_src = lean_file.read_text(encoding="utf-8")
    # Strip comments before scanning for sorry / axiom declarations
    no_block = re.sub(r"/-.*?-/", "", lean_src, flags=re.DOTALL)
    no_comments = re.sub(r"--.*$", "", no_block, flags=re.MULTILINE)
    assert re.search(r"\bsorry\b", no_comments) is None
    assert re.search(r"\baxiom\b", no_comments) is None

    lean_bin = shutil.which("lean") or str(Path.home() / ".elan" / "bin" / "lean")
    assert Path(lean_bin).exists(), f"Lean 4 binary not found at {lean_bin}"
    proc = subprocess.run(
        [lean_bin, "--trust=0", str(lean_file)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "sorryAx" not in proc.stdout


def test_metadata_and_opsec_cleanliness() -> None:
    zenodo = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    assert zenodo["version"] == "1.1.0"

    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert 'version: "1.1.0"' in cff
    assert 'date-released: "2026-11-25"' in cff

    internal_prefix = "/" + "home" + "/" + "alp"
    secret_prefixes = (
        "ghp" + "_",
        "github_pat" + "_",
        "AIza" + "Sy",
        "ntn" + "_",
        "sk-proj" + "-",
        "BEGIN RSA " + "PRIVATE KEY",
        "BEGIN OPENSSH " + "PRIVATE KEY",
    )

    skip_dirs = {".git", "__pycache__", ".pytest_cache"}
    for path in ROOT.rglob("*"):
        if any(part in skip_dirs for part in path.parts) or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert internal_prefix not in text, f"Internal path leaked in {path.relative_to(ROOT)}"
        for sp in secret_prefixes:
            assert sp not in text, f"Secret pattern leaked in {path.relative_to(ROOT)}"
        for tok in re.findall(r"[a-z0-9_]{6,}", text.lower()):
            digest = hashlib.sha256(tok.encode("utf-8")).hexdigest()
            assert digest not in FORBIDDEN_TOKEN_SHA256, (
                f"Forbidden identifier token found in {path.relative_to(ROOT)}"
            )
