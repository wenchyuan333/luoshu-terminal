"""
GF(3) bit-rule 基礎建設 v0.1
純 Python 標準庫，無 numpy。用於 LSHU-F3-RARE-001 與後續洛書問題底層算術。
"""
from itertools import product

# --- 純量算術 mod 3 ---
def gf3_add(a, b): return (a + b) % 3
def gf3_sub(a, b): return (a - b) % 3
def gf3_mul(a, b): return (a * b) % 3
def gf3_inv(a):
    """𝔽₃ 逆元：1↔1, 2↔2（因 2·2=4≡1）。0 無逆元。"""
    if a % 3 == 0: raise ZeroDivisionError("GF(3): 0 沒有逆元")
    return a % 3

# --- 矩陣運算（list-of-lists） ---
def mat_mul_mod3(A, B):
    n, m, p = len(A), len(A[0]), len(B[0])
    return [[sum(A[i][k]*B[k][j] for k in range(m)) % 3
             for j in range(p)] for i in range(n)]

def mat_det(M):
    """Laplace 展開整數 det（未 mod）。"""
    n = len(M)
    if n == 1: return M[0][0]
    if n == 2: return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    total = 0
    for j in range(n):
        minor = [[M[i][k] for k in range(n) if k != j] for i in range(1, n)]
        total += (-1)**j * M[0][j] * mat_det(minor)
    return total

def mat_det_mod3(M): return mat_det(M) % 3

# --- 洛書判定與計數 ---
def is_loshu(M):
    """LSHU-F3-RARE-001 定義：所有元素 ∈ {1,2} 且 det ≢ 0 (mod 3)。"""
    for row in M:
        for x in row:
            if x not in (1, 2): return False
    return mat_det_mod3(M) != 0

def count_loshu(d):
    """精算 N(d)。d≤4 秒級；d=5 分鐘級；d≥6 需切演算法。"""
    c = 0
    for flat in product([1, 2], repeat=d*d):
        M = [list(flat[i*d:(i+1)*d]) for i in range(d)]
        if mat_det_mod3(M) != 0: c += 1
    return c

# --- 自檢 ---
if __name__ == "__main__":
    assert gf3_inv(1) == 1 and gf3_inv(2) == 2, "GF(3) inv"
    assert count_loshu(1) == 2, "N(1)"
    assert count_loshu(2) == 8, "N(2)"
    n3 = count_loshu(3)
    assert n3 == 192, f"N(3) expected 192, got {n3}"
    print("GF(3) inv        ✓  (1↔1, 2↔2)")
    print(f"N(1) = 2         ✓  trivial")
    print(f"N(2) = 8         ✓  |GL(2,𝔽₃)|=48, r=16.7%")
    print(f"N(3) = {n3}       ✓  |GL(3,𝔽₃)|=11232, r=1.71%")
    print("--- bits.py self-test 全過 ---")
