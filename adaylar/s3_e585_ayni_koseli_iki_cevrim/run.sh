#!/usr/bin/env bash
# Reproduces out/. Needs gcc, python3 and nauty (nauty-geng, nauty-labelg).
set -euo pipefail
cd "$(dirname "$0")"
gcc -O3 -o e585 e585.c
W=${W:-work}; mkdir -p "$W" out
# checker vs reference, all graphs n <= 7 (n = 8 takes ~10 min in Python; set FULL8=1)
: > out/capraz_run.txt
for n in 1 2 3 4 5 6 7 ${FULL8:+8}; do
  nauty-geng -q "$n" > "$W/all$n.g6"
  d=$(diff <(./e585 check < "$W/all$n.g6" 2>/dev/null | cut -d' ' -f1,2) <(python3 e585_ref.py < "$W/all$n.g6") | wc -l)
  echo "n=$n graphs=$(wc -l < "$W/all$n.g6") diff_lines=$d" >> out/capraz_run.txt
done
# method (a), n <= 10
rm -f "$W/a/yontem_a.log"
for nm in "1 0" "2 1" "3 3" "4 6" "5 9" "5 10" "6 12" "6 13" "7 16" "7 17" "8 19" "8 20" "9 23" "9 24" "10 27" "10 28"; do
  ./yontem_a.sh "$W/a" $nm
done
cp "$W/a/yontem_a.log" out/yontem_a.log
# method (a), n = 11 (writes a line per scan to $W/DURUM.md)
for M in 32 31 30; do ./f11_tarama.sh "$W/f11_m$M" "$M"; done
grep "F(11) taramasi" "$W/DURUM.md" > out/f11_tarama.log
# method (b), ladder up to n = 11 with threshold 30
./yontem_b.sh "$W/b11" 11 30 && cp "$W/b11/yontem_b.log" out/yontem_b_n11_t30.log
# certified upper bounds
for spec in "10 28:28" "-d5 11 32:32"; do
  nauty-geng -q $spec > "$W/cert.g6"
  ./e585 check -c < "$W/cert.g6" | python3 sertifika_dogrula.py "$W/cert.g6"
done
# method (c): certified ladder to n = 12, then n = 13 above 40 edges
./yontem_c.sh "$W/c12" "1:0 2:1 3:2 4:4 5:6 6:9 7:12 8:16 9:20 10:25 11:30 12:35"
mkdir -p "$W/c13" && cp "$W/c12/L12.g6" "$W/c13/" && ./yontem_c.sh "$W/c13" "12:35 13:41"
cat "$W/c12/yontem_c.log" "$W/c13/yontem_c.log"
cat out/yontem_a.log out/f11_tarama.log out/yontem_b_n11_t30.log
