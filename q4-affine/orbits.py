# -*- coding: utf-8 -*-
"""
q4-affine/orbits.py — 雙射噴發至回歸 × 魯班鎖邊界 對偶

用戶洞察 (2026-08-28 04:48 +08:00):
> 魯班鎖不就是幻方的格格邊界
> 因陀羅網不就是雙射噴發後直到回歸的那條路
> 轉起來吧

實作把 AGL(1, F_{4096}) 拆成兩個對偶視角:

(A) 因陀羅網 = 雙射噴發至回歸
    對每個群元 g = (a, b), 從點 x 出發:
       x -> g(x) -> g(g(x)) -> ... -> x (回歸)
    軌道長 = ord_x(g), 全空間 = 有限個 orbit 之聯集

(B) 魯班鎖 = 幻方格格邊界
    相鄰位址 x, x⊕1 (bit-flip in char 2) 映射後 delta:
       delta(x) = g(x⊕1) ⊕ g(x) = a·(x⊕1) ⊕ b ⊕ (a·x ⊕ b) = a·1 = a
    delta 恆為常數 a, 只由乘子決定, 加法平移不影響邊界

結論: 邊界 (魯班鎖) 與 噴發回歸 (因陀羅網) 是同一 (a,b) 的兩面
      邊界    <-> a (乘子單獨決定)
      噴發    <-> a & b 聯合決定 orbit 分割
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agl1_4096 import (
    FIELD_SIZE, NONZERO, POLY,
    gf_add, gf_mul, gf_inv, gf_pow,
    agl_apply, agl_compose,
)


def orbit_of(a, b, x, max_steps=None):
    """從 x 出發, 反覆套 (a, b), 回歸即停. 回傳 orbit [x, g(x), g^2(x), ...]"""
    if max_steps is None:
        max_steps = FIELD_SIZE * NONZERO + 1
    orbit = [x]
    y = agl_apply(a, b, x)
    steps = 0
    while y != x:
        orbit.append(y)
        y = agl_apply(a, b, y)
        steps += 1
        if steps > max_steps:
            raise RuntimeError(f"orbit_of({a},{b},{x}) 超過 max_steps={max_steps}")
    return orbit


def order_of(a, b, max_steps=None):
    """群元 (a, b) 在 AGL 中的階: 最小 n 使 (a,b)^n = (1, 0)"""
    if (a, b) == (1, 0):
        return 1
    if max_steps is None:
        max_steps = FIELD_SIZE * NONZERO + 1
    ca, cb = a, b
    n = 1
    while (ca, cb) != (1, 0):
        ca, cb = agl_compose(a, b, ca, cb)
        n += 1
        if n > max_steps:
            raise RuntimeError(f"order_of({a},{b}) 超過 max_steps={max_steps}")
    return n


def orbit_partition(a, b):
    """(a, b) 作用下 4096 個點的 orbit partition. 回傳 list of orbits."""
    seen = [False] * FIELD_SIZE
    orbits = []
    for x in range(FIELD_SIZE):
        if seen[x]:
            continue
        orb = orbit_of(a, b, x)
        for p in orb:
            seen[p] = True
        orbits.append(orb)
    return orbits


def luoshu_boundary_delta(a, b):
    """魯班鎖邊界: 相鄰 x, x⊕1 (bit-flip 最低位) 經 (a,b) 映射後的 XOR delta 集合"""
    deltas = set()
    for x in range(FIELD_SIZE):
        d = gf_add(agl_apply(a, b, x ^ 1), agl_apply(a, b, x))
        deltas.add(d)
    return sorted(deltas)


# --------------------------------------------------------------
# self-test: 驗證兩對偶視角的公理
# --------------------------------------------------------------

def _verify_orbit_partition_axioms(a, b):
    """驗證 orbit partition 覆蓋且互斥, 且每個 orbit 長 | ord(g) (Lagrange)"""
    orbits = orbit_partition(a, b)
    total = sum(len(o) for o in orbits)
    assert total == FIELD_SIZE, f"orbit partition 不覆蓋: total={total}, expected={FIELD_SIZE}"
    seen = set()
    for orb in orbits:
        for p in orb:
            assert p not in seen, f"orbit partition 有重疊於 {p}"
            seen.add(p)
    grp_order = order_of(a, b)
    for orb in orbits:
        assert grp_order % len(orb) == 0, f"orbit 長 {len(orb)} 不整除群元階 {grp_order}"
    return orbits, grp_order


def _verify_luoshu_boundary_invariant(a, b):
    """驗證: 對線性群元 (a, b), 位址位翻轉 x⊕1 的映射 delta 恆為常數 a"""
    deltas = luoshu_boundary_delta(a, b)
    assert deltas == [a], f"魯班鎖邊界 delta 非常數 a: got {deltas}, expected [{a}]"
    return a


def _self_test():
    print("=" * 60)
    print(" q4-affine/orbits.py 自檢")
    print(" 雙射噴發回歸 (因陀羅網) × 魯班鎖邊界 對偶")
    print("=" * 60)

    test_cases = [
        (1, 1, "純加法平移 x -> x XOR 1"),
        (2, 0, "純乘法 x -> 2·x  (2 於 F_4096* 為原元, 階 4095)"),
        (3, 5, "一般仿射 x -> 3·x XOR 5"),
        (0x100, 0xFFF, "位移組合 x -> 0x100·x XOR 0xFFF"),
    ]

    for a, b, label in test_cases:
        orbits, grp_order = _verify_orbit_partition_axioms(a, b)
        boundary_a = _verify_luoshu_boundary_invariant(a, b)
        lens = sorted(set(len(o) for o in orbits))
        max_len = max(len(o) for o in orbits)
        n_orbits = len(orbits)
        print()
        print(f"  g = (a=0x{a:03X}, b=0x{b:03X})  # {label}")
        print(f"    群元階 ord(g)   = {grp_order}")
        print(f"    orbit 分割     = {n_orbits} 個 orbit, 長度集合 {lens}, 最長 {max_len}")
        print(f"    Lagrange       每個 orbit 長 | ord(g) = {grp_order}  [OK]")
        print(f"    魯班鎖邊界 delta = 0x{boundary_a:03X} (= a, 位翻轉保持) [OK]")

    print()
    print("=" * 60)
    print("結論:")
    print("  因陀羅網 = orbit 分割 (由 g=(a,b) 全體決定, 每 orbit 長 | ord(g))")
    print("  魯班鎖   = 位址位翻轉 delta = a (只由乘子決定, adjacency 保持)")
    print("  兩者是同一 AGL 群元的兩個對偶視角, 全空間覆蓋且相容.")
    print("  依 AXIOMS.A0: 此結構有內在殘差 (partition 的具體形狀依賴 a 的階),")
    print("                非終局封閉, 但於 F_{4096} 上已完備.")
    print("=" * 60)


if __name__ == "__main__":
    _self_test()
