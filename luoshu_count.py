from itertools import product

def det(M):
    n = len(M)
    if n == 2: return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    total = 0
    for j in range(n):
        minor = [[M[i][k] for k in range(n) if k != j] for i in range(1, n)]
        total += (-1)**j * M[0][j] * det(minor)
    return total

def count(d):
    c = 0
    for f in product([1, 2], repeat=d*d):
        M = [list(f[i*d:(i+1)*d]) for i in range(d)]
        if det(M) % 3 != 0:
            c += 1
    return c

print("N(3) =", count(3), " (LSHU 聲稱 192)")
print("N(4) =", count(4), " (LSHU 聲稱 22272, ~30-60s)")
