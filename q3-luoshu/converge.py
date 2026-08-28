"""
q3-luoshu/converge.py — Phase Q5 material triage fixture.

Formalizes the ◎☉⇄ operators from Msg 52 transcript material.
Registers positive fixtures for the correct parts and negative
counterexamples for the material's high-report errors.

Operators (per material definition):
    ◎(x)     = (x + 5) / 2          converge toward center 5
    ☉_ij(x)  = (x + L0[i][j]) / 2   release back toward original

8 checks:

  POSITIVE (three conservation laws, correct per material):
    T1 ◎ preserves magic sum S=15
    T2 ◎☉ chain preserves magic sum S=15
    T3 ◎ preserves opposite-pair sum = 10
    T4 ◎ preserves total sum = 45

  NEGATIVE (reject material's false algebra claims):
    T5 ◎∘☉ ≠ ☉∘◎ except at center cell (rejects 材料 假交換律)
    T6 ◎² ≠ ◎  (affine contraction terminates but no period;
                rejects 材料 ⇄⇄=⇄ 假冪等律)
    T7 eigenvalues of Lo Shu are {15, +2i√6, -2i√6}, not real
       (rejects 材料 λ₁≈15.37 / λ₂≈4.56 / λ₃≈-4.93)

  CROSS-SESSION VERIFICATION:
    T8 rarity 1.71% ≡ N(3)=192 / |GL(3,F_3)|=26·24·18=11232
       matches material's independent GL group-theory derivation

Reference:
    KERNEL §18.5 Phase Q5 material transcript registry
           (2026-08-28T15:15+08:00)
    MIR-001 §9 Claim Firewall additions
"""
from __future__ import annotations
from typing import Callable, List

# Lo Shu magic square (canonical orientation, magic sum = 15)
L0: List[List[int]] = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]
CENTER = 5
MAGIC_SUM = 15
TOTAL_SUM = 45
OPPOSITE_PAIR_SUM = 10
TOL = 1e-9


def apply_matrix(
    f: Callable[[float, int, int], float],
    M: List[List[float]],
) -> List[List[float]]:
    """Apply per-cell operator f(x, i, j) to matrix M."""
    return [[f(M[i][j], i, j) for j in range(3)] for i in range(3)]


def op_convergence(x: float, i: int, j: int) -> float:
    """◎(x) = (x + 5) / 2 — pull toward center 5."""
    return (x + CENTER) / 2


def op_release(x: float, i: int, j: int) -> float:
    """☉_ij(x) = (x + L0[i][j]) / 2 — pull back to original Lo Shu value."""
    return (x + L0[i][j]) / 2


def magic_sums(M: List[List[float]]) -> List[float]:
    """Return 8 line sums: 3 rows + 3 cols + 2 diagonals."""
    sums = [sum(row) for row in M]
    sums += [sum(M[i][j] for i in range(3)) for j in range(3)]
    sums.append(M[0][0] + M[1][1] + M[2][2])
    sums.append(M[0][2] + M[1][1] + M[2][0])
    return sums


def total_sum(M: List[List[float]]) -> float:
    return sum(sum(row) for row in M)


def opposite_pair_sums(M: List[List[float]]) -> List[float]:
    """L_ij + L_{2-i, 2-j} for all 9 pairs (center pairs with itself → 10)."""
    return [M[i][j] + M[2 - i][2 - j] for i in range(3) for j in range(3)]


# ── Positive fixtures ────────────────────────────────────────────────

def test_magic_sum_preserved_under_convergence() -> None:
    M = apply_matrix(op_convergence, L0)
    for s in magic_sums(M):
        assert abs(s - MAGIC_SUM) < TOL, f"◎ broke magic sum: got {s}"


def test_magic_sum_preserved_under_release_chain() -> None:
    M = apply_matrix(op_convergence, L0)
    M = apply_matrix(op_release, M)
    for s in magic_sums(M):
        assert abs(s - MAGIC_SUM) < TOL, f"◎☉ broke magic sum: got {s}"


def test_opposite_pair_sum_preserved() -> None:
    M = apply_matrix(op_convergence, L0)
    for s in opposite_pair_sums(M):
        assert abs(s - OPPOSITE_PAIR_SUM) < TOL, (
            f"◎ broke opposite-pair sum: got {s}"
        )


def test_total_sum_preserved() -> None:
    M = apply_matrix(op_convergence, L0)
    got = total_sum(M)
    assert abs(got - TOTAL_SUM) < TOL, f"◎ broke total sum: got {got}"


# ── Negative fixtures: reject material's false algebra ───────────────

def test_convergence_release_NOT_commutative_off_center() -> None:
    """◎∘☉ ≠ ☉∘◎ except at center cell (1,1) where L0=5.

    Rejects Msg 52 material's claim `◎☉ = ☉◎ = ⇄`.
    Formal:  ◎∘☉(x) = (x + L0 + 10) / 4
             ☉∘◎(x) = (x + 5 + 2·L0) / 4
    Equal iff L0 = 5, i.e. only the center cell.
    """
    x_test = 7.0
    for i in range(3):
        for j in range(3):
            circ_then_sun = op_convergence(op_release(x_test, i, j), i, j)
            sun_then_circ = op_release(op_convergence(x_test, i, j), i, j)
            if (i, j) == (1, 1):
                assert abs(circ_then_sun - sun_then_circ) < TOL, (
                    f"expected commute at center, got "
                    f"{circ_then_sun} vs {sun_then_circ}"
                )
            else:
                assert abs(circ_then_sun - sun_then_circ) > TOL, (
                    f"expected NON-commute at ({i},{j}), "
                    f"got equal {circ_then_sun}"
                )


def test_convergence_NOT_idempotent() -> None:
    """◎² ≠ ◎ ; affine contraction has termination but no period.

    Rejects Msg 52 material's ⇄⇄ = ⇄ (週期閉合) claim.
    Only λ ∈ {0, 1} yields idempotent affine contraction.
    """
    x_test = 3.0
    once = op_convergence(x_test, 0, 0)
    twice = op_convergence(once, 0, 0)
    assert abs(twice - once) > TOL, (
        f"◎² should differ from ◎, got ◎(3)={once}, ◎²(3)={twice}"
    )
    # verify iteration converges monotonically to 5 (fixed point, not periodic)
    x = x_test
    for _ in range(60):
        x = op_convergence(x, 0, 0)
    assert abs(x - CENTER) < 1e-15, f"◎ⁿ should → 5, got {x}"


def _lo_shu_char_poly(lam: complex) -> complex:
    """p(λ) = λ³ − 15λ² + 24λ − 360   (Lo Shu characteristic polynomial).

    Derived from det(L − λI):
        trace L = 4+5+6 = 15
        Σ 2x2 principal minors = 23 + 8 + (-7) = 24
        det L = 4·23 − 9·(−38) + 2·(−37) = 92 + 342 − 74 = 360
    Factors as (λ − 15)(λ² + 24) ⇒ roots {15, ±2i√6}.
    """
    return lam ** 3 - 15 * lam ** 2 + 24 * lam - 360


def test_eigenvalues_are_15_and_pure_imaginary() -> None:
    """True spectrum {15, +2i√6, −2i√6} — one real, two purely imaginary.

    Rejects Msg 50 material's claim of three real eigenvalues
    15.37 / 4.56 / -4.93 (whose product ≈ -345.5 ≠ det L = 360).
    """
    assert abs(_lo_shu_char_poly(15)) < TOL, "15 must be an eigenvalue"
    plus = complex(0, 2 * (6 ** 0.5))
    minus = complex(0, -2 * (6 ** 0.5))
    assert abs(_lo_shu_char_poly(plus)) < 1e-9, (
        f"+2i√6 should be root, got p={_lo_shu_char_poly(plus)}"
    )
    assert abs(_lo_shu_char_poly(minus)) < 1e-9, (
        f"−2i√6 should be root, got p={_lo_shu_char_poly(minus)}"
    )
    for bad in (15.37, 4.56, -4.93):
        r = _lo_shu_char_poly(bad)
        assert abs(r) > 1.0, (
            f"material's alleged eigenvalue {bad} should NOT be a root, "
            f"but |p({bad})| = {abs(r):.3f}"
        )


# ── Cross-session verification ───────────────────────────────────────

def test_rarity_1_71_percent_match_N3() -> None:
    """|GL(3, F_3)| = (27−1)(27−3)(27−9) = 26·24·18 = 11232.

    N(3) admissible Lo Shu-type magic patterns over F_3 = 192
    (from q3-luoshu/luoshu_check.py, LSHU-F3-RARE-001 骨架).

    192 / 11232 = 1.7094% ≈ Msg 52 material's independently-derived 1.71%.
    Cross-session GL group-theory path converges to same rarity number.
    """
    gl3_f3 = (27 - 1) * (27 - 3) * (27 - 9)
    assert gl3_f3 == 11232, f"|GL(3,F_3)| computation error: {gl3_f3}"
    N3 = 192
    rarity = N3 / gl3_f3
    assert abs(rarity - 0.0171) < 0.001, (
        f"expected ~1.71%, got {rarity * 100:.4f}%"
    )


# ── Test runner ──────────────────────────────────────────────────────

TESTS = [
    ("T1 ◎ preserves magic sum (S=15)",
     test_magic_sum_preserved_under_convergence),
    ("T2 ◎☉ chain preserves magic sum",
     test_magic_sum_preserved_under_release_chain),
    ("T3 ◎ preserves opposite-pair sum (=10)",
     test_opposite_pair_sum_preserved),
    ("T4 ◎ preserves total sum (=45)",
     test_total_sum_preserved),
    ("T5 ◎∘☉ ≠ ☉∘◎ except at center (reject 假交換律)",
     test_convergence_release_NOT_commutative_off_center),
    ("T6 ◎² ≠ ◎ (reject 假冪等律 ⇄⇄=⇄)",
     test_convergence_NOT_idempotent),
    ("T7 eigenvalues {15, ±2i√6} (reject 15.37/4.56/-4.93)",
     test_eigenvalues_are_15_and_pure_imaginary),
    ("T8 rarity 1.71% ≡ N(3)=192 / |GL(3,F_3)|=11232",
     test_rarity_1_71_percent_match_N3),
]


def main() -> int:
    passed = 0
    failed = 0
    for name, fn in TESTS:
        try:
            fn()
            print(f"  ✓ {name}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {name}: {e}")
            failed += 1
    total = passed + failed
    status = "ALL PASS" if failed == 0 else f"{failed} FAILED"
    print(f"\nconverge.py: {passed}/{total}  {status}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
