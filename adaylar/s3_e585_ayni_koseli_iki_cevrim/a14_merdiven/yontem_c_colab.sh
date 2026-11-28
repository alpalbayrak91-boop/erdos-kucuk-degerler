#!/bin/bash
# yontem_c.sh'in Colab uyarlamasi (claude 2026-11-28, Fable tasarimi): PARCA=cekirdek sayisi, yuk bekcisi yok,
# var olan L<n>.g6 duzeyi atlanir (kesintiden surme). Mantik ve dogrulayici bagimsizligi aynen korunur.
set -euo pipefail
D=$(cd "$(dirname "$0")" && pwd)
OUT=$1; TH=$2; P=${PARCA:-$(nproc)}
LABELG=$(command -v nauty-labelg || command -v labelg)
mkdir -p "$OUT"; [ -s "$OUT/L1.g6" ] || echo "@" > "$OUT/L1.g6"; touch "$OUT/yontem_c.log"
prev=""
for p in $TH; do
  n=${p%%:*}; t=${p##*:}
  if [ -n "$prev" ]; then
    pt=${prev##*:}; need=$(( t - (2 * t) / n ))
    [ "$pt" -le "$need" ] || { echo "threshold check failed at n=$n" >> "$OUT/yontem_c.log"; exit 1; }
    if [ -f "$OUT/L$n.g6" ] && grep -q "^n=$n t=$t " "$OUT/yontem_c.log"; then prev=$p; echo "n=$n atlandi (var)" >&2; continue; fi
    t0=$(date +%s)
    awk -v P="$P" -v B="$OUT/part$n." '{ f = sprintf("%s%03d", B, (NR-1) % P); print > f } END { for (i = 0; i < P; i++) { f = sprintf("%s%03d", B, i); printf "" >> f } }' "$OUT/L$((n-1)).g6"
    for f in "$OUT"/part$n.[0-9][0-9][0-9]; do
      ( "$D/e585" extend "$t" -a < "$f" 2>/dev/null \
          | "$D/e585" check -C -l 2>/dev/null \
          | tee >(awk 'NF==4' | python3 -I "$D/sertifika_dogrula.py" > "$f.cert") \
          | awk 'NF!=4' > "$f.good" ) &
    done
    wait; sleep 5
    good=$(cat "$OUT"/part$n.[0-9][0-9][0-9].good | wc -l)
    cat "$OUT"/part$n.[0-9][0-9][0-9].good | "$LABELG" -q 2>/dev/null | LC_ALL=C sort -u > "$OUT/L$n.g6"
    cert=$(cat "$OUT"/part$n.[0-9][0-9][0-9].cert | tr ' ' '\n' | awk -F= '{s[$1]+=$2} END{printf "certificates=%d valid=%d errors=%d missing=0", s["certificates"], s["valid"], s["errors"]}')
    nc=${cert#certificates=}; nc=${nc%% *}; cand=$(( good + nc ))
    rm -f "$OUT"/part$n.[0-9][0-9][0-9] "$OUT"/part$n.[0-9][0-9][0-9].good
    sec=$(( $(date +%s) - t0 ))
  else grep -q "^n=1 " "$OUT/yontem_c.log" && { prev=$p; continue; }; cand=1; good=1; cert="certificates=0 valid=0 errors=0 missing=0"; sec=0; fi
  hist=$("$D/e585" check < "$OUT/L$n.g6" 2>/dev/null | sed 's/.*kenar=//' | sort -n | uniq -c | awk '{printf "%s:%s ", $2, $1}')
  echo "n=$n t=$t candidates=$cand good=$good $cert classes=$(wc -l < "$OUT/L$n.g6") edges:count=[ $hist] sec=$sec parca=$P" >> "$OUT/yontem_c.log"
  prev=$p
done
