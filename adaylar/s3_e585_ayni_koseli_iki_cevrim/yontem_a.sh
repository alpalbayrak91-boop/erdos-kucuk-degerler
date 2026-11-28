#!/bin/sh
# Method (a): exhaustive nauty-geng scan.
# usage: yontem_a.sh OUTDIR n m [geng-extra-options]
#   Generates every graph on n vertices with exactly m edges (up to isomorphism),
#   keeps the good ones (graph6) in OUTDIR/a_n<n>_m<m>.g6 and appends a
#   summary line to OUTDIR/yontem_a.log:
#     n m geng_opts graphs good seconds
# Wait while the 1-minute load is above 18 (shared machine).
set -e
D=$(cd "$(dirname "$0")" && pwd)
OUT=$1; n=$2; m=$3; shift 3; EXTRA="$*"
mkdir -p "$OUT"
while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 18 ]; do sleep 30; done
t0=$(date +%s)
nice -n 15 /usr/bin/nauty-geng -q $EXTRA "$n" "$m:$m" \
  | nice -n 15 "$D/e585" check -g > "$OUT/a_n${n}_m${m}.g6" 2> "$OUT/a_n${n}_m${m}.err"
t1=$(date +%s)
s=$(cat "$OUT/a_n${n}_m${m}.err")
g=$(echo "$s" | sed 's/.*graphs=\([0-9]*\).*/\1/'); k=$(echo "$s" | sed 's/.*good=\([0-9]*\).*/\1/')
echo "$n $m opts=[$EXTRA] graphs=$g good=$k sec=$((t1-t0))" >> "$OUT/yontem_a.log"
