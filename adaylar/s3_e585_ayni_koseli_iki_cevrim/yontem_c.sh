#!/bin/bash
# Method (c): CERTIFIED vertex-extension ladder.
# usage: yontem_c.sh OUTDIR "1:t1 2:t2 ... N:tN"   (thresholds, need t_{n-1} <= t_n - floor(2 t_n / n))
#   L_n = good graphs on n vertices with >= t_n edges (up to isomorphism).
#   Every candidate (L_{n-1} + one vertex of minimum degree, >= t_n edges, 'e585 extend -a')
#   is tested ('check -C -l': only sets S through the new vertex, sound as L_{n-1} is good): good ones go to L_n (nauty-labelg | sort -u),
#   bad ones get a certificate (two edge-disjoint cycles on one vertex set) that is checked
#   by sertifika_dogrula.py.  So L_n is complete given L_{n-1}, using only the candidate
#   enumeration, nauty-labelg and the verifier; a wrongly 'good' verdict can only enlarge L_n.
#   Log: OUTDIR/yontem_c.log
set -euo pipefail
D=$(cd "$(dirname "$0")" && pwd)
OUT=$1; TH=$2
mkdir -p "$OUT"; echo "@" > "$OUT/L1.g6"; : > "$OUT/yontem_c.log"
prev=""
for p in $TH; do
  n=${p%%:*}; t=${p##*:}
  if [ -n "$prev" ]; then
    pt=${prev##*:}; need=$(( t - (2 * t) / n ))
    [ "$pt" -le "$need" ] || { echo "threshold check failed at n=$n: t_{n-1}=$pt > $need" >> "$OUT/yontem_c.log"; exit 1; }
    while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 18 ]; do sleep 30; done
    t0=$(date +%s)
    # 3 parallel parts (split of L_{n-1}); certificates verified on the fly, good graphs kept
    split -n l/3 -d "$OUT/L$((n-1)).g6" "$OUT/part$n."
    for f in "$OUT"/part$n.0?; do
      ( nice -n 15 "$D/e585" extend "$t" -a < "$f" 2>/dev/null \
          | nice -n 15 "$D/e585" check -C -l 2>/dev/null \
          | tee >(awk 'NF==4' | nice -n 15 python3 -I "$D/sertifika_dogrula.py" > "$f.cert") \
          | awk 'NF!=4' > "$f.good" ) &
    done
    wait; sleep 5
    good=$(cat "$OUT"/part$n.0?.good | wc -l)
    cat "$OUT"/part$n.0?.good | nice -n 15 /usr/bin/nauty-labelg -q 2>/dev/null | LC_ALL=C sort -u > "$OUT/L$n.g6"
    cert=$(cat "$OUT"/part$n.0?.cert | tr ' ' '\n' | awk -F= '{s[$1]+=$2} END{printf "certificates=%d valid=%d errors=%d missing=0", s["certificates"], s["valid"], s["errors"]}')
    nc=${cert#certificates=}; nc=${nc%% *}; cand=$(( good + nc ))
    rm -f "$OUT"/part$n.0? "$OUT"/part$n.0?.good
    sec=$(( $(date +%s) - t0 ))
  else cand=1; good=1; cert="certificates=0 valid=0 errors=0 missing=0"; sec=0; fi
  hist=$("$D/e585" check < "$OUT/L$n.g6" 2>/dev/null | sed 's/.*kenar=//' | sort -n | uniq -c | awk '{printf "%s:%s ", $2, $1}')
  echo "n=$n t=$t candidates=$cand good=$good $cert classes=$(wc -l < "$OUT/L$n.g6") edges:count=[ $hist] sec=$sec" >> "$OUT/yontem_c.log"
  prev=$p
done
