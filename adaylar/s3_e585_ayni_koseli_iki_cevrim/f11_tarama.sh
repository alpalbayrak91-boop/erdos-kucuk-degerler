#!/bin/sh
# Method (a) at n = 11: exhaustive scan of 11-vertex graphs with M edges.
# A good 11-vertex graph with M edges and a vertex of degree d has a good
# 10-vertex subgraph with M - d edges; F(10) = 27 forces d >= M - 27.  Hence
# 'nauty-geng -d<M-27> 11 M:M' contains every good graph with M edges.
#   M = 32 (-d5): no good graph  => F(11) <= 31 (edge-deletion closure)
#   M = 31 (-d4): good classes   => F(11) >= 31 and the extremal classes
#   M = 30 (-d3): good classes with 30 edges
# usage: f11_tarama.sh OUTDIR M   (3 parts via geng res/mod, run in parallel)
# Writes OUTDIR/part<r>.err (summary), OUTDIR/part<r>.good.g6, and on completion
# appends the result to OUTDIR/../DURUM.md.
D=$(cd "$(dirname "$0")" && pwd)
OUT=$1; M=${2:-31}; DM=$((M - 27)); mkdir -p "$OUT"
date -Is > "$OUT/basla.txt"
for r in 0 1 2; do
  ( nice -n 15 /usr/bin/nauty-geng -q -d$DM 11 $M:$M $r/3 \
      | nice -n 15 "$D/e585" check -g > "$OUT/part$r.good.g6" 2> "$OUT/part$r.err" ) &
done
wait
date -Is > "$OUT/bitis.txt"
tot=0; good=0
for r in 0 1 2; do
  g=$(sed 's/.*graphs=\([0-9]*\).*/\1/' "$OUT/part$r.err"); k=$(sed 's/.*good=\([0-9]*\).*/\1/' "$OUT/part$r.err")
  tot=$((tot + g)); good=$((good + k))
done
echo "- F(11) taramasi (geng -d$DM 11 $M:$M): graphs=$tot good=$good basla=$(cat "$OUT/basla.txt") bitis=$(cat "$OUT/bitis.txt")" >> "$OUT/../DURUM.md"
