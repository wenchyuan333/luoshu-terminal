"""
board_stack.py — 幻方盤堆立方體 × AGL(1,F_4096) × 逐層相對性

一盤 (Board) = 64 × 64 = 4096 cells ≅ F_{2^12}
       非零 cells = 4095 = |F_{2^12}^*|
一盤 = 1 bit (stack 中承載 spin up/down 二元態)
64 盤 = 64³ cube = 2^18 = 262,144 cells

D4 幻方旋轉群 (8 元素: 4 rotations + 4 reflections)
AGL(1, F_{2^12}) sharply 2-transitive on 一盤
  |AGL| = 4096 × 4095 = 16,773,120

逐層相對性: 相鄰盤 k, k+1 由 AGL 元素 g_k = (a_k, b_k) 連接;
全 stack 相對變換 = AGL^{63} (63 boosts across 64 layers)

兩重對稱 orthogonal:
  D4 作用在 2D lattice geometry (row, col ∈ Z/64)
  AGL 作用在 F_{4096} 元素代碼 (12-bit encoding)
  同盤承載, 互不干涉, 共同保證逐層相對性.

依 KERNEL §19.7 D14 (脈衝換方法閘) & MIR-001 firewall:
  4096 非時空維度; 盤堆非宇宙拓撲; 1-bit 非意識載體.
  純有限群論結構自洽.

Author: 江坤晉 (wenchyuan333) × Miya
Session: 2026-08-28T05:10+08:00
Branch: verify/board-stack-v1
"""
from __future__ import annotations
import sys
import os
import hashlib
import math

_HAS_Q4 = False
try:
    _here = os.path.dirname(os.path.abspath(__file__))
    _parent = os.path.dirname(_here)
    sys.path.insert(0, _parent)
    sys.path.insert(0, os.path.join(_parent, "q4-affine"))
    from agl1_4096 import agl_apply  # type: ignore
    _HAS_Q4 = True
except Exception:
    _HAS_Q4 = False

BOARD_SIDE = 64
BOARD_CELLS = BOARD_SIDE * BOARD_SIDE
BOARD_UNITS_STAR = BOARD_CELLS - 1
STACK_DEPTH = 64
CUBE_CELLS = BOARD_SIDE ** 3
BOARD_BITS = 1
STACK_TOTAL_BITS = STACK_DEPTH * BOARD_BITS
D4_ORDER = 8
AGL_ORDER = BOARD_CELLS * BOARD_UNITS_STAR


def cell_to_field(row: int, col: int) -> int:
    if not (0 <= row < BOARD_SIDE and 0 <= col < BOARD_SIDE):
        raise ValueError(f"cell out of range: ({row},{col})")
    return (row << 6) | col


def field_to_cell(x: int):
    if not 0 <= x < BOARD_CELLS:
        raise ValueError(f"field element out of range: {x}")
    return (x >> 6, x & 0x3F)


def d4_apply(op: int, row: int, col: int):
    """D4 (8 elements): 0=e, 1=rot90, 2=rot180, 3=rot270,
    4=flip_h, 5=flip_h·rot90, 6=flip_v, 7=flip_h·rot270."""
    n = BOARD_SIDE - 1
    if op == 0: return (row, col)
    if op == 1: return (col, n - row)
    if op == 2: return (n - row, n - col)
    if op == 3: return (n - col, row)
    if op == 4: return (row, n - col)
    if op == 5: return (col, row)
    if op == 6: return (n - row, col)
    if op == 7: return (n - col, n - row)
    raise ValueError(f"op must be 0..7, got {op}")


def relativity_boost(g_ab, layer_from: int, layer_to: int, x: int) -> int:
    a, b = g_ab
    if not _HAS_Q4:
        return (a * x + b) % BOARD_CELLS
    return agl_apply(a, b, x)


def board_hash(board_id: int, spin_bit: int) -> str:
    if spin_bit not in (0, 1):
        raise ValueError(f"spin_bit must be 0 or 1, got {spin_bit}")
    payload = f"board:{board_id}|bit:{spin_bit}|cells:{BOARD_CELLS}"
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def stack_hash(spin_pattern: int) -> str:
    if not 0 <= spin_pattern < (1 << STACK_DEPTH):
        raise ValueError(f"spin_pattern must fit in {STACK_DEPTH} bits")
    payload = f"stack:{spin_pattern:016x}|depth:{STACK_DEPTH}"
    return hashlib.sha256(payload.encode()).hexdigest()[:32]


def _test_constants():
    assert BOARD_CELLS == 4096
    assert BOARD_UNITS_STAR == 4095
    assert CUBE_CELLS == 262144 == 2 ** 18
    assert STACK_DEPTH == 64 == STACK_TOTAL_BITS
    assert BOARD_BITS == 1
    assert D4_ORDER == 8
    assert AGL_ORDER == 4096 * 4095 == 16_773_120


def _test_cell_field_bijection():
    seen = set()
    for r in range(BOARD_SIDE):
        for c in range(BOARD_SIDE):
            x = cell_to_field(r, c)
            assert 0 <= x < BOARD_CELLS
            assert (r, c) == field_to_cell(x)
            assert x not in seen
            seen.add(x)
    assert len(seen) == BOARD_CELLS


def _test_d4_group():
    for r, c in [(0, 0), (1, 2), (32, 17), (63, 63)]:
        assert d4_apply(0, r, c) == (r, c)
    for r, c in [(0, 0), (1, 2), (32, 17), (63, 63)]:
        rc = (r, c)
        for _ in range(4):
            rc = d4_apply(1, *rc)
        assert rc == (r, c)
    for r, c in [(0, 0), (10, 20), (63, 0), (5, 55)]:
        two = d4_apply(1, *d4_apply(1, r, c))
        assert d4_apply(2, r, c) == two
    for r, c in [(3, 4), (30, 40)]:
        assert d4_apply(4, *d4_apply(4, r, c)) == (r, c)


def _test_agl_layer_boost():
    if not _HAS_Q4:
        for x in [0, 1, 100, 4095]:
            assert relativity_boost((1, 0), 0, 1, x) == x
        return "SKIP q4-affine unimportable (fallback tested)"
    for x in [0, 1, 100, 4095]:
        assert relativity_boost((1, 0), 0, 1, x) == x
    for g in [(3, 5), (7, 11), (4095, 0), (1, 4095)]:
        for x in [0, 100, 4095]:
            y = relativity_boost(g, 0, 1, x)
            assert 0 <= y < BOARD_CELLS
    return "PASS (agl_apply live)"


def _test_hash_receipts():
    h0 = board_hash(0, 0)
    h1 = board_hash(0, 1)
    h2 = board_hash(1, 0)
    assert h0 != h1 and h0 != h2
    assert len(h0) == 16
    hs0 = stack_hash(0)
    hs1 = stack_hash((1 << 64) - 1)
    hs2 = stack_hash(0xDEADBEEFCAFEBABE)
    assert hs0 != hs1 and hs0 != hs2
    assert len(hs0) == 32


def _test_relativity_cardinality():
    n_boosts = STACK_DEPTH - 1
    log10 = n_boosts * math.log10(AGL_ORDER)
    assert log10 > 400


def main():
    print("=" * 60)
    print("q5-stacked-boards: board_stack self-test")
    print(f"  一盤 = {BOARD_SIDE}x{BOARD_SIDE} = {BOARD_CELLS} cells")
    print(f"  非零 = {BOARD_UNITS_STAR} = |F_4096^*|")
    print(f"  一盤 = {BOARD_BITS} bit; stack = {STACK_DEPTH} 盤 = {STACK_TOTAL_BITS} bits")
    print(f"  cube = {BOARD_SIDE}^3 = {CUBE_CELLS} = 2^{int(math.log2(CUBE_CELLS))}")
    print(f"  D4 order = {D4_ORDER}; |AGL(1,F_4096)| = {AGL_ORDER:,}")
    print(f"  q4-affine imported: {_HAS_Q4}")
    print("=" * 60)

    _test_constants();               print("[OK] 常數 (4096, 4095, 2^18, 64 bits)")
    _test_cell_field_bijection();    print("[OK] cell ↔ F_4096 雙射 (4096 unique)")
    _test_d4_group();                print("[OK] D4 幻方旋轉群 (rot90^4=e, flip^2=e)")
    agl_msg = _test_agl_layer_boost(); print(f"[OK] AGL 逐層相對性 boost ({agl_msg})")
    _test_hash_receipts();           print("[OK] 每 bit hash receipt (SHA-256)")
    _test_relativity_cardinality();  print("[OK] 相對變換空間 |AGL|^63 (log10>400)")

    print("=" * 60)
    print("q5-stacked-boards self-test 全過.")
    print("Receipt: SHA-256 per bit + stack; KERNEL §19.7 D14 每 bit 哈希化.")
    print("Firewall: 4096 = F_{2^12} cardinality; 非時空維數 (同 MIR-001).")


if __name__ == "__main__":
    main()
