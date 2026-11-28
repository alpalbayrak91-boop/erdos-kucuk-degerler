#!/bin/bash
# Method (d): certified proof that no good graph on 13 vertices has 40 edges, so a(13) <= 39.
# usage: yontem_d.sh OUTDIR L12.g6 [PARTS] [JOBS] ["PARTLIST"]
#   PARTLIST (optional, for a quick test): run only these parts of the d = 6 scan, e.g. "0 100".
#   L12.g6 = all good graphs on 12 vertices with >= 35 edges, up to isomorphism
#            (output OUT/L12.g6 of: yontem_c.sh OUT "1:0 2:1 3:2 4:4 5:6 6:9 7:12 8:16 9:20 10:25 11:30 12:35").
#
# Let G be good on 13 vertices with 40 edges and let v be a vertex of minimum degree d.
# Then d <= floor(80/13) = 6, and G - v is good on 12 vertices with 40 - d <= a(12) = 36 edges,
# so d is 4, 5 or 6.
#   d = 4 or 5: G - v has 36 or 35 edges, so it is in L12, and G is obtained from it by adding a
#               vertex of minimum degree.  These candidates are produced by 'e585 extend 40 -a'.
#   d = 6:      every degree is >= 6 and the degree sum is 80, so every degree is <= 8.
#               These candidates are produced by 'nauty-geng -d6 -D8 13 40:40' (split in PARTS).
# Every candidate must come with a certificate (two edge-disjoint cycles on one vertex set).
# sertifika_dogrula.py checks each certificate and checks that no candidate lacks one.
# Log: OUTDIR/yontem_d.log
set -euo pipefail
D=$(cd "$(dirname "$0")" && pwd)
OUT=$1; L12=$2; PARTS=${3:-256}; JOBS=${4:-3}; LIST=${5:-$(seq 0 $((${3:-256} - 1)))}
mkdir -p "$OUT/part"; LOG="$OUT/yontem_d.log"; : > "$LOG"

# d = 4, 5
"$D/e585" extend 40 -a < "$L12" 2>/dev/null > "$OUT/ext.g6"
"$D/e585" check -c -l < "$OUT/ext.g6" 2> "$OUT/ext.err" | python3 -I "$D/sertifika_dogrula.py" "$OUT/ext.g6" > "$OUT/ext.cert"
echo "extensions of L12 (d = 4, 5): candidates=$(wc -l < "$OUT/ext.g6") $(tail -1 "$OUT/ext.err") $(cat "$OUT/ext.cert")" >> "$LOG"

# d = 6
one() {
  r=$1; f="$OUT/part/p$r.g6"
  nauty-geng -q -d6 -D8 13 40:40 "$r/$PARTS" > "$f" 2>/dev/null
  cert=$("$D/e585" check -c < "$f" 2> "$f.err" | python3 -I "$D/sertifika_dogrula.py" "$f")
  echo "part=$r/$PARTS candidates=$(wc -l < "$f") $(tail -1 "$f.err") $cert"
  rm -f "$f" "$f.err"
}
export -f one; export D OUT PARTS
printf '%s\n' $LIST | nice -n 19 xargs -P "$JOBS" -I{} bash -c 'one {}' > "$OUT/parts.log"
awk '{for (i = 2; i <= NF; i++) { split($i, a, "="); s[a[1]] += a[2] }}
     END { printf "minimum degree 6 (d = 6): parts=%d candidates=%d graphs=%d good=%d bad=%d certificates=%d valid=%d errors=%d missing=%d\n",
           NR, s["candidates"], s["graphs"], s["good"], s["bad"], s["certificates"], s["valid"], s["errors"], s["missing"] }' "$OUT/parts.log" >> "$LOG"
cat "$LOG"
