"""Erdos 585 a(14) sertifikali merdiven (Fable tasarimi, 28 Kas). CPU calisma zamani. ONERI [Claude Opus 5.5]."""
import os, shutil, subprocess, sys, time, pathlib
IS = pathlib.Path(__file__).resolve().parent
K = IS / "kaynak"; CIKTI = IS / "cikti"; CIKTI.mkdir(exist_ok=True)
def kos(c, **kw):
    print("$", c, flush=True); return subprocess.run(c, shell=True, check=True, **kw)
kos("apt-get -qq update >/dev/null && apt-get -qq install -y nauty >/dev/null")
kos(f"gcc -O3 -march=native -o {K}/e585 {K}/e585.c")
for f in (IS / "devam").glob("*"):          # onceki oturumdan suren duzeyler
    shutil.copy(f, CIKTI / f.name)
esik = "1:0 2:1 3:2 4:4 5:6 6:9 7:12 8:15 9:19 10:23 11:28 12:33 13:38 14:44"
t0 = time.time()
env = dict(os.environ, PARCA=str(os.cpu_count() or 2))
r = subprocess.run([str(K / "yontem_c_colab.sh"), str(CIKTI), esik], env=env)
(CIKTI / "BITTI.txt").write_text(f"cikis={r.returncode} sure_sn={int(time.time()-t0)} cekirdek={os.cpu_count()}\n")
print(open(CIKTI / "yontem_c.log").read())
