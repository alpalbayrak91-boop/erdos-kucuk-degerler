"""Erdos #934, t = 2: h_2(d) - 1 = largest number of edges in a graph with maximum degree <= d
and no induced 2K2. Closed form by Chung, Gyarfas, Tuza, Trotter (Discrete Math. 81 (1990) 129-135):
5d^2/4 for even d, (5d^2 - 2d + 1)/4 for odd d."""
import sys
def cgtt(d):
    return 5 * d * d // 4 if d % 2 == 0 else (5 * d * d - 2 * d + 1) // 4
N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
print([cgtt(d) for d in range(1, N + 1)])
