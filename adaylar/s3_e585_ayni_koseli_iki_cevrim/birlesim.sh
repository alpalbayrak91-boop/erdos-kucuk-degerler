#!/bin/bash
# Joins K_2 v H (two adjacent vertices joined to every vertex of H) for graphs H with no 3-cycle
# and no 4-cycle, tested with e585.  See "Structure" in README.md.
# usage: birlesim.sh OUTDIR [KMAX]      (KMAX = 14 by default; 15 and 16 take much longer)
#   k = 3..11 : every H of girth >= 5 on k vertices            (nauty-geng -tf k)
#   k = 12..  : every extremal H, i.e. with A006856(k) edges   (nauty-geng -tf k m:m)
# Log: OUTDIR/birlesim.log, one line per k: number of graphs H, good joins, bad joins.
set -euo pipefail
D=$(cd "$(dirname "$0")" && pwd)
OUT=$1; KMAX=${2:-14}
mkdir -p "$OUT"; LOG="$OUT/birlesim.log"; : > "$LOG"
EX=(0 0 1 2 3 5 6 8 10 12 15 16 18 21 23 26 28)   # A006856(k), k = 0..16
for k in $(seq 3 "$KMAX"); do
  if [ "$k" -le 11 ]; then sel=""; what="all girth >= 5"; else sel="${EX[$k]}:${EX[$k]}"; what="extremal (${EX[$k]} edges)"; fi
  nauty-geng -q -tf "$k" $sel 2>/dev/null > "$OUT/H$k.g6"
  python3 -I "$D/yapi.py" --join < "$OUT/H$k.g6" > "$OUT/J$k.g6"
  res=$(nice -n 19 "$D/e585" check -c < "$OUT/J$k.g6" 2>&1 >"$OUT/J$k.cert" | tail -1)
  ver=""; [ -s "$OUT/J$k.cert" ] && ver=" $(python3 -I "$D/sertifika_dogrula.py" < "$OUT/J$k.cert")"
  echo "k=$k n=$((k + 2)) H: $what, $res$ver" >> "$LOG"
done
cat "$LOG"
