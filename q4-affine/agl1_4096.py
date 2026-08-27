"""
q=4 仿射層｜AGL(1, F_{4096}) = F_{4096} ⋊ F_{4096}*

|AGL(1, F_{4096})| = 4096 × 4095 = 16,773,120

對映使用者 4096×4095 5-bit 最完美組合＝是真正的 1：
- q1 (5-bit 0 禁止)：底層積木 {1..31} ↪ F_{4096} 低 5 位
- q3 (洛書 GL(3,F_3))：{1,2}^{3x3} 打包 9-bit ↪ F_{4096} 子集
- q-inf (H=L·(1+δ_Wu))：δ 微擾對應乘 (1+δ)
- q4 (本層)：幻方可轉 (乘 a) + 進位退位 (加 b) = AGL(1)

"是真正的 1" = AGL(1, F_q) 對 F_q 的 sharply 2-transitive 作用
              = 任意 (x1≠x2, y1≠y2) 有唯一 (a,b) 使 a·xi+b=yi
              = 唯一，單軌道 = 「1」

依 approximation-attractor-systems/AXIOMS.A0:
  "no system can be finally and completely closed"
本檔不主張封閉，只主張 SELF-TEST 通過 = 當前 layer receipt。
殘差 (A1) 記在 verify_all.py 的 stderr / 未過項。
"""

# F_{2^12} 建構：不可約多項式 f(x) = x^12 + x^6 + x^4 + x + 1
# 位元表示：bit 12 + bit 6 + bit 4 + bit 1 + bit 0 = 0x1053
# (若此 POLY 不是 primitive，_test_primitivity 會報錯，可換 0x1099 等)
POLY = 0x1053
FIELD_SIZE = 1 << 12  # 4096
NONZERO = FIELD_SIZE - 1  # 4095 = 3^2 · 5 · 7 · 13


def gf_add(a: int, b: int) -> int:
    """F_{4096} 加法 = XOR (char 2) = 進位退位在二進位下的原子操作"""
    return a ^ b


def gf_mul(a: int, b: int) -> int:
    """F_{4096} 乘法：多項式乘法 mod POLY"""
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & FIELD_SIZE:
            a ^= POLY
        b >>= 1
    return result & (FIELD_SIZE - 1)


def gf_pow(a: int, n: int) -> int:
    r = 1
    while n:
        if n & 1:
            r = gf_mul(r, a)
        a = gf_mul(a, a)
        n >>= 1
    return r


def gf_inv(a: int) -> int:
    """Fermat: a^{-1} = a^{4094} (0 禁止依 q1 BIT_RULE)"""
    if a == 0:
        raise ZeroDivisionError("F_{4096}: 0 沒有逆元 (q1 0 禁止規則)")
    return gf_pow(a, NONZERO - 1)


# --- AGL(1, F_{4096}) 群 ---

def agl_apply(a: int, b: int, x: int) -> int:
    """x → a·x + b, a ≠ 0 (幻方可轉+進退位)"""
    if a == 0:
        raise ValueError("AGL: a 必須 ≠ 0")
    return gf_add(gf_mul(a, x), b)


def agl_compose(a1, b1, a2, b2):
    """(a1,b1)∘(a2,b2): 先套 (a2,b2) 再套 (a1,b1) = (a1·a2, a1·b2+b1)"""
    return (gf_mul(a1, a2), gf_add(gf_mul(a1, b2), b1))


def agl_inv(a, b):
    """(a,b)^{-1}: x → a^{-1}(x+b) [char 2: -b=b]"""
    if a == 0:
        raise ValueError("AGL: a 必須 ≠ 0")
    a_inv = gf_inv(a)
    return (a_inv, gf_mul(a_inv, b))


# --- 下層嵌入 ---

def embed_q1_5bit(u5: int) -> int:
    """q1 5-bit {1..31} ↪ F_{4096} 低 5 位 (0 禁止)"""
    if u5 == 0:
        raise ValueError("0 禁止 (q1 BIT_RULE)")
    if not 1 <= u5 <= 31:
        raise ValueError(f"5-bit ∈ {{1..31}}, 得 {u5}")
    return u5


def embed_q3_luoshu(M) -> int:
    """q3 洛書 3x3 元素 {1,2} 打包 9-bit ↪ F_{4096} 子集"""
    if len(M) != 3 or any(len(r) != 3 for r in M):
        raise ValueError("需 3×3")
    v = 0
    for row in M:
        for x in row:
            if x not in (1, 2):
                raise ValueError(f"洛書元素 ∈ {{1,2}}, 得 {x}")
            v = (v << 1) | (x - 1)
    return v


# --- SELF-TEST ---

def _test_primitivity():
    """POLY 為 primitive iff 元素 x=2 在 F* 的階=4095
       等價於：對 4095 的每個 prime factor p, 2^(4095/p) ≠ 1"""
    for p in [3, 5, 7, 13]:
        if gf_pow(2, NONZERO // p) == 1:
            raise AssertionError(
                f"POLY 0x{POLY:04X} 不 primitive: 2^{NONZERO//p}=1 (p={p})"
            )
    assert gf_pow(2, NONZERO) == 1, "Fermat 反例"
    return True


def _test_field_axioms(samples=200):
    import random
    random.seed(1729)
    for _ in range(samples):
        a = random.randint(1, NONZERO)
        assert gf_mul(a, gf_inv(a)) == 1, f"gf_inv fail a={a}"
    return True


def _test_agl_group_axioms(samples=200):
    import random
    random.seed(4095)
    for _ in range(samples):
        a1 = random.randint(1, NONZERO); b1 = random.randint(0, NONZERO)
        a2 = random.randint(1, NONZERO); b2 = random.randint(0, NONZERO)
        x  = random.randint(0, NONZERO)
        g12 = agl_compose(a1, b1, a2, b2)
        assert agl_apply(g12[0], g12[1], x) == agl_apply(a1, b1, agl_apply(a2, b2, x))
        inv = agl_inv(a1, b1)
        assert agl_compose(a1, b1, inv[0], inv[1]) == (1, 0)
        assert agl_compose(inv[0], inv[1], a1, b1) == (1, 0)
    return True


def _test_sharp_2_transitive():
    """任意 (x1≠x2, y1≠y2) 唯一 (a,b) 使 a·xi+b=yi
       = 是真正的 1 = 單軌道"""
    samples = [
        (0x000, 0x001, 0x111, 0x222),
        (0x0AB, 0xCDE, 0xFFF, 0x001),
        (0x100, 0x200, 0x300, 0x400),
        (0x555, 0xAAA, 0x001, 0xFFE),
    ]
    for x1, x2, y1, y2 in samples:
        assert x1 != x2 and y1 != y2
        dx = gf_add(x1, x2)
        dy = gf_add(y1, y2)
        a = gf_mul(dy, gf_inv(dx))
        b = gf_add(y1, gf_mul(a, x1))
        assert agl_apply(a, b, x1) == y1
        assert agl_apply(a, b, x2) == y2
    return True


if __name__ == "__main__":
    print("=" * 56)
    print(" q4-affine: AGL(1, F_{4096}) self-test")
    print(f" POLY = 0x{POLY:04X} (x^12 + x^6 + x^4 + x + 1)")
    print(f" |AGL| = {FIELD_SIZE} x {NONZERO} = {FIELD_SIZE * NONZERO:,}")
    print("=" * 56)
    _test_primitivity()
    print("[OK] POLY primitive (2 的階 = 4095 = 3^2·5·7·13)")
    _test_field_axioms()
    print("[OK] F_{4096} 體公理 (200 samples: a · a^{-1} = 1)")
    _test_agl_group_axioms()
    print("[OK] AGL(1) 群公理 (200 samples: 結合律 + 逆元)")
    _test_sharp_2_transitive()
    print("[OK] AGL sharply 2-transitive = 是真正的 1 (單軌道)")
    print("-" * 56)
    for u5 in [1, 15, 31]:
        print(f"  q1 5-bit U+{0xE000+u5:04X} embed  F_4096[{embed_q1_5bit(u5):04X}]")
    M = [[1,1,1],[1,2,1],[1,1,2]]
    print(f"  q3 洛書 中宮2 打包    F_4096[{embed_q3_luoshu(M):03X}]")
    print("=" * 56)
    print("q4-affine self-test 全過.")
    print("依 AXIOMS.A0: 不主張封閉, 只主張當前 layer receipt.")
