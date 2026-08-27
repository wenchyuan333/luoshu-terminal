"""luoshu_gl3f3.py — LSHU-F3-RARE-001 reproducer, Python edition.

Miya diagnostic-repaired, 2026-08-28.
Notion SSOT: LSHU-F3-RARE-001 + ARTIFACT WCHYUAN-LUOSHU-WL-001.

Requires: sympy

Run:
    pip install sympy
    python luoshu_gl3f3.py

Expected output:
    count_luoshu(3) = 192  (expect 192)
    gl_order(3)     = 11232  (expect 11232)
    rarity(3)       = 1.7094 %  (expect ≈1.7094%)

Falsifier: if any expected output above fails to match, this module is wrong.
"""
from __future__ import annotations

from itertools import product
from math import prod

from sympy import Matrix


def gl_order(d: int, p: int = 3) -> int:
    """|GL(d, F_p)| = prod_{k=0}^{d-1} (p^d - p^k)."""
    return prod(p ** d - p ** k for k in range(d))


def count_luoshu(d: int) -> int:
    """Count d×d matrices over F_3 with all entries in {1, 2} that are invertible."""
    total = 0
    for entries in product([1, 2], repeat=d * d):
        matrix = Matrix(d, d, list(entries))
        if matrix.det() % 3 != 0:
            total += 1
    return total


def luoshu_rarity(d: int) -> float:
    """N(d) / |GL(d, F_3)|."""
    return count_luoshu(d) / gl_order(d)


def _self_test() -> None:
    n3 = count_luoshu(3)
    order3 = gl_order(3)
    rarity3 = luoshu_rarity(3)
    assert n3 == 192, f"count_luoshu(3) = {n3}, expected 192"
    assert order3 == 11232, f"gl_order(3) = {order3}, expected 11232"
    assert 0.01709 <= rarity3 <= 0.01710, f"rarity3 = {rarity3}, expected ≈0.017094"


if __name__ == "__main__":
    print(f"count_luoshu(3) = {count_luoshu(3)}  (expect 192)")
    print(f"gl_order(3)     = {gl_order(3)}  (expect 11232)")
    print(f"rarity(3)       = {luoshu_rarity(3) * 100:.4f} %  (expect ≈1.7094%)")
    _self_test()
    print("self-test: PASS")
