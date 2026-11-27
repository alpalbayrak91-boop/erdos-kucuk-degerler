#!/usr/bin/env bash
# Reproduces every file in out/. Needs gcc; method C also needs PySDD
# (pip install pysdd) and takes about 5 CPU minutes (skip with NO_SDD=1).
# Methods A, B, B1, B2 take about 2 CPU minutes in total.
set -euo pipefail
cd "$(dirname "$0")"
for f in s2_direct s2_extend s2_twopoint s2_onepoint; do gcc -O2 -o "$f" "$f.c"; done
mkdir -p out
./s2_direct 7   > out/method_A_m1_7.txt          # direct backtracking, m <= 7
./s2_extend 7   > out/method_B_m1_7.txt          # one-point extension, all colourings, m <= 7
./s2_twopoint   > out/method_B2_twopoint_m7_8.txt  # S6-orbits + two new points, m = 7, 8
./s2_onepoint   > out/method_B1_onepoint_m7_8.txt  # S7-orbits + one new point, m = 7, 8
if [ "${NO_SDD:-0}" != 1 ]; then python3 s2_sdd.py 7 > out/method_C_sdd_m1_7.txt; fi
cat out/*.txt
