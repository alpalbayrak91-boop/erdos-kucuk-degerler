#!/usr/bin/env bash
# Reproduces every file in out/. Needs gcc, python3 and nauty (geng, countg;
# Debian/Ubuntu package "nauty", binaries nauty-geng / nauty-countg).
# Total CPU time on one core: about 1 minute.
set -euo pipefail
cd "$(dirname "$0")"
GENG=$(command -v nauty-geng || command -v geng)
COUNTG=$(command -v nauty-countg || command -v countg)
for f in s1_direct s1_bruteforce_small s1_filter s1_extend s1_extend2; do
  gcc -O2 -o "$f" "$f.c"
done
mkdir -p out g6
# sanity: plain bitmask enumeration of all graphs, n <= 7
./s1_bruteforce_small 7 > out/bruteforce_n1_7.txt
# method A: direct labeled enumeration (no nauty), n <= 8
./s1_direct 8 > out/method_A_n1_8.txt
# unlabeled induced-C4-free graphs: geng | filter (class counts = OEIS A352068)
for n in $(seq 1 10); do "$GENG" -q "$n" | ./s1_filter > "g6/ic4free_$n.g6"; done
# method B: n!/|Aut| summed over classes, |Aut| from countg, n <= 10
: > out/method_B_n1_10.txt
for n in $(seq 1 10); do
  "$COUNTG" -q --a "g6/ic4free_$n.g6" > "out/countg_a_n$n.txt"
  python3 s1_sum.py B "$n" "out/countg_a_n$n.txt" >> out/method_B_n1_10.txt
done
# method C: one labeled vertex added to unlabeled (n-1)-vertex graphs, own |Aut|
: > out/method_C_n2_11.txt
for n in $(seq 2 11); do m=$((n-1))
  ./s1_extend < "g6/ic4free_$m.g6" > "out/extend_from_n$m.txt"
  python3 s1_sum.py C "$n" "out/extend_from_n$m.txt" >> out/method_C_n2_11.txt
done
# method D: two labeled vertices added to unlabeled (n-2)-vertex graphs
: > out/method_D_n3_11.txt
for n in $(seq 3 11); do m=$((n-2))
  ./s1_extend2 < "g6/ic4free_$m.g6" > "out/extend2_from_n$m.txt"
  python3 s1_sum.py D "$n" "out/extend2_from_n$m.txt" >> out/method_D_n3_11.txt
done
cat out/method_A_n1_8.txt out/method_B_n1_10.txt out/method_C_n2_11.txt out/method_D_n3_11.txt
