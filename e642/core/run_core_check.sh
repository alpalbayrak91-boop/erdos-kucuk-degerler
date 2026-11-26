#!/bin/bash
# Reproduces the core checks of ../CORE_REDUCTION.md. Needs gcc and nauty (geng, labelg).
# Usage: ./run_core_check.sh [NMAX]   (default 11; 12 takes ~10 CPU-minutes, 13 ~10 CPU-hours)
set -euo pipefail
cd "$(dirname "$0")"
NMAX="${1:-11}"
GENG="$(command -v nauty-geng || command -v geng)"
LABELG="$(command -v nauty-labelg || command -v labelg)"
BIN="$(mktemp -d)/good_check"
gcc -O2 -o "$BIN" good_check.c

echo "# base: all graphs on 7 vertices with 14 and 15 edges"
"$GENG" -q 7 14:14 | "$BIN" -q
"$GENG" -q 7 15:15 | "$BIN" -q
"$GENG" -q 7 14:14 | "$BIN" 2>/dev/null > /tmp/e642_E7.g6

for n in $(seq 8 "$NMAX"); do
  e=$((3 * n - 7))
  echo "# Core($n): min degree >= 4, exactly $e edges"
  "$GENG" -q -d4 "$n" "$e:$e" | "$BIN" -q
  p=$((n - 1))
  echo "# Lemma 2 at n=$n: degree-3 and degree-4 extensions of the extremal graph on $p vertices"
  python3 extend.py 3 < "/tmp/e642_E$p.g6" | "$BIN" 2>/dev/null | "$LABELG" -q | sort -u > "/tmp/e642_E$n.g6"
  echo "good degree-3 extensions up to isomorphism: $(wc -l < "/tmp/e642_E$n.g6")"
  python3 extend.py 4 < "/tmp/e642_E$p.g6" | "$BIN" -q
done
