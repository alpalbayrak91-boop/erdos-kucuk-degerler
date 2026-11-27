#!/usr/bin/env python3
"""Replay the Erdős #642 witnesses and, optionally, an n=13 enumeration shard."""

import argparse
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parent
SHARDS = 16
EXPECTED_TOTAL = 27_472_319_548


def graph6_neighbors(record):
    size = ord(record[0]) - 63
    pairs = [(i, j) for j in range(size) for i in range(j)]
    if not 1 <= size <= 62 or len(record) != 1 + (len(pairs) + 5) // 6:
        raise ValueError(f"Invalid short graph6 record: {record!r}")
    values = [ord(char) - 63 for char in record[1:]]
    if any(not 0 <= value <= 63 for value in values):
        raise ValueError(f"Invalid graph6 character: {record!r}")
    neighbors = [0] * size
    for index, (i, j) in enumerate(pairs):
        if values[index // 6] & (1 << (5 - index % 6)):
            neighbors[i] |= 1 << j
            neighbors[j] |= 1 << i
    return neighbors


def cycle_statistics(neighbors):
    """Visit simple cycles directly, counting edges induced by their vertices."""
    circumference = 0
    for start, adjacent in enumerate(neighbors):
        # Start at the least vertex of a cycle. Both traversal directions are harmless.
        larger = ~((1 << (start + 1)) - 1)
        stack = [(start, 1 << start, 1, 0)]
        while stack:
            end, vertices, size, induced_edges = stack.pop()
            if size >= 3 and adjacent & (1 << end):
                if induced_edges >= 2 * size:
                    raise ValueError(f"Cycle of length {size} has too many chords")
                circumference = max(circumference, size)
            choices = neighbors[end] & larger & ~vertices
            while choices:
                bit = choices & -choices
                choices ^= bit
                next_vertex = bit.bit_length() - 1
                edges_added = (neighbors[next_vertex] & vertices).bit_count()
                stack.append((next_vertex, vertices | bit, size + 1, induced_edges + edges_added))
    edge_count = sum(mask.bit_count() for mask in neighbors) // 2
    return len(neighbors), edge_count, circumference


def witness_checks():
    cases = {
        "counterexample_n13_n14.g6": [(13, 27, 12), (14, 30, 12)],
        "counterexamples_excess.g6": [(16, 35, 14), (19, 43, 16)],
    }
    for filename, expected in cases.items():
        records = (ROOT / "circumference" / filename).read_text().splitlines()
        actual = [cycle_statistics(graph6_neighbors(line)) for line in records]
        if actual != expected:
            raise ValueError(f"{filename}: expected {expected}, got {actual}")
        for size, edges, circumference in actual:
            excess = edges - (3 * size - circumference - 1)
            print(f"good: n={size}, edges={edges}, circumference={circumference}, excess={excess}")

    # K_{1,2,10}, the lower-bound witness for f(13) >= 32.
    parts = [0, 1, 1] + [2] * 10
    neighbors = [sum(1 << j for j, other in enumerate(parts) if part != other) for part in parts]
    if cycle_statistics(neighbors)[:2] != (13, 32):
        raise ValueError("Unexpected K_{1,2,10} witness")
    print("good: K_{1,2,10}, n=13, edges=32")


def recorded_counts():
    lines = (ROOT / "core" / "results_core_n13.txt").read_text().splitlines()
    rows = [re.fullmatch(r"r=(\d+)/16 total=(\d+) good=(\d+)", line)
            for line in lines if line and not line.startswith("#")]
    if not all(rows) or len(rows) != SHARDS:
        raise ValueError("Expected 16 enumeration shard rows")
    counts = {}
    for row in rows:
        index, total, good = map(int, row.groups())
        if index in counts or total <= 0 or good != 0:
            raise ValueError(f"Invalid shard result: {row.group()}")
        counts[index] = total
    if set(counts) != set(range(SHARDS)) or sum(counts.values()) != EXPECTED_TOTAL:
        raise ValueError("Incomplete shard coverage or unexpected recorded total")
    return counts


def replay_shard(shard, expected):
    geng = shutil.which("nauty-geng") or shutil.which("geng")
    compiler = shutil.which("cc")
    if not geng or not compiler:
        raise RuntimeError("Shard replay requires nauty geng and a 64-bit Linux C compiler (cc)")
    with TemporaryDirectory() as temporary:
        binary = str(Path(temporary) / "good_check")
        subprocess.run([compiler, "-O2", "-o", binary, str(ROOT / "core" / "good_check.c")], check=True)
        command = [geng, "-q", "-d4", "13", "32:32", f"{shard}/{SHARDS}"]
        with subprocess.Popen(command, stdout=subprocess.PIPE) as generator:
            with subprocess.Popen([binary, "-q"], stdin=generator.stdout, stderr=subprocess.PIPE,
                                  text=True) as checker:
                generator.stdout.close()
                _, report = checker.communicate()
                if checker.returncode or generator.wait():
                    raise RuntimeError(f"Shard {shard} pipeline failed: {report.strip()}")
    if report.strip() != f"total={expected} good=0":
        raise ValueError(f"Shard {shard}: unexpected checker report: {report.strip()}")
    print(f"replayed shard {shard}/{SHARDS}: {report.strip()}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    replay = parser.add_mutually_exclusive_group()
    replay.add_argument("--shard", type=int, choices=range(SHARDS), help="replay one recorded shard")
    replay.add_argument("--all-shards", action="store_true", help="replay every shard (hours of CPU time)")
    args = parser.parse_args()

    witness_checks()
    counts = recorded_counts()
    print(f"recorded n=13 log: {SHARDS} shards, {sum(counts.values()):,} graphs, 0 good")
    if args.all_shards:
        for shard, expected in sorted(counts.items()):
            replay_shard(shard, expected)
    elif args.shard is not None:
        replay_shard(args.shard, counts[args.shard])
    else:
        print("Verified witnesses and log consistency. Enumeration was not replayed.")


if __name__ == "__main__":
    main()
