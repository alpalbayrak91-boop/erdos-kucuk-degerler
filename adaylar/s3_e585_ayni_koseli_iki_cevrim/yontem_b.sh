#!/bin/sh
# Method (b): vertex-extension ladder (independent of geng).
# usage: yontem_b.sh OUTDIR NMAX MTARGET
#   Builds L_n = all good graphs on n vertices with >= t_n edges, up to
#   isomorphism (nauty-labelg + sort -u), for n = 1..NMAX, where
#   t_NMAX = MTARGET and t_{n-1} = t_n - floor(2 t_n / n).
#   Completeness: a good graph G on n vertices with m >= t_n edges has a vertex
#   v of minimum degree d <= floor(2m/n); G - v is good with m - d >= t_{n-1}
#   edges (m - floor(2m/n) is nondecreasing in m), so G arises from L_{n-1} by
#   adding a vertex of minimum degree ('e585 extend').
#   Log: OUTDIR/yontem_b.log, one line per n: n t_n classes max_edges histogram.
set -e
D=$(cd "$(dirname "$0")" && pwd)
OUT=$1; NMAX=$2; M=$3
mkdir -p "$OUT"
# thresholds, top-down
t=$M; i=$NMAX; TH=""
while [ $i -ge 1 ]; do TH="$i:$t $TH"; t=$((t - (2 * t) / i)); [ $t -lt 0 ] && t=0; i=$((i - 1)); done
echo "@" > "$OUT/L1.g6"
: > "$OUT/yontem_b.log"
for p in $TH; do
  n=${p%%:*}; tn=${p##*:}
  if [ "$n" -gt 1 ]; then
    t0=$(date +%s)
    nice -n 15 "$D/e585" extend "$tn" < "$OUT/L$((n-1)).g6" 2> "$OUT/L$n.err" \
      | nice -n 15 /usr/bin/nauty-labelg -q | LC_ALL=C sort -u > "$OUT/L$n.g6"
    sec=$(( $(date +%s) - t0 ))
  else sec=0; fi
  hist=$(nice -n 15 "$D/e585" check < "$OUT/L$n.g6" 2>/dev/null | sed 's/.*kenar=//' | sort -n | uniq -c | awk '{printf "%s:%s ", $2, $1}')
  echo "n=$n t=$tn classes=$(wc -l < "$OUT/L$n.g6") edges:count=[ $hist] sec=$sec" >> "$OUT/yontem_b.log"
done
