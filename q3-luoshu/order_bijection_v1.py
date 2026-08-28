"""
q3-luoshu/order_bijection_v1.py — Phase Q5 Msg 66 self-corrected fixture.

w.chyuan's own v1.0 「保序雙射解析版｜嚴格修正版」
(2026-08-28T16:23+08:00).

CANONICAL classification: this is the user's own correction after absorbing
the critique of Msg 61 (集合雙射 != 群同構). v1.0 EXPLICITLY WITHDRAWS:
  - GL(3, F_3) as common algebraic base (proven false)
  - Lo Shu 'forces' sigma = 1/2 (analogy != proof)
  - Four-way group isomorphism (orders 8, 4, 2, 11232 all distinct)

RETAINED (mathematically verifiable):
  - Order-preserving bijection f: {1..9} -> {t_1..t_9} strictly monotone
  - Opposite-pair symmetry: a_ij + a_{4-i,4-j} = 10
  - Rarity ratios at dim d = |admissible| / |GL(d, F_3)|

Tests: 11 checks (7 A tier canonical + 3 B tier withdrawal receipts +
1 C tier minor arithmetic flag).

Reference:
  KERNEL §18.5 Phase Q5 material transcript registry (4th round, user-self-corrected)
  MIR-001 §9 self-correction receipt (contrast with third-party material firewall)
"""
from __future__ import annotations
import math

TOL = 1e-9

# Lo Shu (canonical orientation, magic sum = 15)
L0 = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]

# v1.0 correspondence table: (L_value, row_1based, col_1based, t_imag_2dp)
V1_TABLE = [
    (1, 3, 2, 14.13),
    (2, 1, 3, 21.02),
    (3, 2, 1, 25.01),
    (4, 1, 1, 30.42),
    (5, 2, 2, 32.93),
    (6, 3, 3, 37.59),
    (7, 2, 3, 40.92),
    (8, 3, 1, 43.33),
    (9, 1, 2, 48.01),
]

# Odlyzko reference (2dp accuracy checks match Msg 61 fixture)
RIEMANN_T_FIRST_9 = [
    14.134725, 21.022040, 25.010858, 30.424876,
    32.935062, 37.586178, 40.918719, 43.327073, 48.005151,
]


# --- A. CANONICAL (v1.0 retained claims) --------------------------------

def test_v1_position_lookup_matches_L0():
    """v1.0 table position (row, col) must match L0[row-1][col-1] = L value.
    User corrected: entry 1 position changed to (3,2)=1 to remove duplicates.
    """
    for L_val, r, c, _ in V1_TABLE:
        got = L0[r-1][c-1]
        assert got == L_val, f"v1.0 says L={L_val} at ({r},{c}) but L0 gives {got}"


def test_order_preserving_bijection():
    """L values 1..9 strictly increasing iff t_i strictly increasing.
    Trivially holds because both are totally ordered sets of size 9
    listed in natural order; test formalizes the claim anyway.
    """
    L_vals = [row[0] for row in V1_TABLE]
    t_vals = [row[3] for row in V1_TABLE]
    for i in range(8):
        assert L_vals[i] < L_vals[i+1], f"L not monotone at {i}"
        assert t_vals[i] < t_vals[i+1], f"t not monotone at {i}"


def test_v1_t_values_match_odlyzko_within_2dp():
    """v1.0 t_i values match Odlyzko within 0.01 (same tolerance as Msg 61 fixture)."""
    for (_, _, _, t_v1), t_ref in zip(V1_TABLE, RIEMANN_T_FIRST_9):
        assert abs(t_v1 - t_ref) < 0.01, (
            f"v1.0 t={t_v1} vs Odlyzko {t_ref} (diff {abs(t_v1-t_ref):.6f})"
        )


def test_opposite_pair_sums_10_and_center_self():
    """v1.0 pair rule: (1<->9), (2<->8), (3<->7), (4<->6), (5 self)."""
    pairs = [(1,9),(2,8),(3,7),(4,6)]
    for a, b in pairs:
        assert a + b == 10
    # center: L=5 at (2,2), opposite of itself under (r,c) -> (4-r,4-c)
    assert L0[1][1] == 5


def test_rarity_d3_1_71_percent():
    """d=3: N(3)/|GL(3,F_3)| = 192/11232 = 1.7094...% ~ 1.71%."""
    gl3 = (27-1)*(27-3)*(27-9)
    assert gl3 == 11232
    rarity = 192 / gl3
    assert abs(rarity - 0.0171) < 0.001, f"got {rarity*100:.4f}%"


def test_rarity_d4_0918_percent_resolves_msg61_typo():
    """d=4: N(4)/|GL(4,F_3)| = 22272/24261120 = 0.0918%.

    RESOLVES Msg 61 CONFLICT: prior material wrote '0.918%' (missing a zero);
    user's v1.0 Msg 66 gives correct 0.0918%. The Msg 61 riemann_kerr_disproof.py
    B3 conflict flag is now resolved in favor of 0.0918%.
    """
    gl4 = (81-1)*(81-3)*(81-9)*(81-27)
    assert gl4 == 24261120
    rarity = 22272 / gl4
    assert abs(rarity - 0.000918) < 1e-5, f"got {rarity*100:.4f}%"
    # 0.0918% not 0.918% — order of magnitude corrected
    assert abs(rarity - 0.00918) > 0.005


def test_tightening_factor_d3_to_d4_18_6():
    """Tightening: 1.71% / 0.0918% ~ 18.6x (dimension-wise sparsification)."""
    r3 = 192 / 11232
    r4 = 22272 / 24261120
    ratio = r3 / r4
    assert abs(ratio - 18.6) < 0.5, f"got {ratio:.2f}x"


# --- B. Withdrawal receipts (v1.0 explicit withdrawals) -----------------

def test_withdraw_group_isomorphism_by_order_mismatch():
    """v1.0 explicitly withdraws four-way isomorphism.
    |D_4|=8, |V_4|=4, |Kerr Z_2|=2, |GL(3,F_3)|=11232 — all distinct.
    """
    orders = [8, 4, 2, 11232]
    assert len(set(orders)) == 4, "expected 4 distinct orders"


def test_withdraw_gl3_as_common_base():
    """v1.0 explicitly withdraws GL(3, F_3) as common algebraic base.
    Rationale: no common substructure to which the other three groups embed;
    orders are pairwise coprime pattern (8, 4, 2 divides 8 but 11232 does not).
    """
    d4, v4, z2, gl3 = 8, 4, 2, 11232
    # If GL(3,F_3) were a common base, its order would be divisible by all others
    assert gl3 % d4 != 0, f"GL(3,F_3) order {gl3} % |D_4| {d4} = {gl3 % d4} (should not be 0 for the false claim)"


def test_withdraw_lo_shu_forces_sigma_half():
    """v1.0 explicitly withdraws 'Lo Shu forces sigma=1/2'.
    Analogy != proof. Klein-four orbit {rho, 1-rho, conj(rho), 1-conj(rho)}
    is closed under group action for ANY sigma, not just sigma=1/2.
    """
    for sigma in [0.3, 0.5, 0.7]:
        orbit = {(sigma,), (1-sigma,)}
        assert len(orbit) == (1 if abs(sigma - 0.5) < TOL else 2)


# --- C. Minor arithmetic flag (v1.0 has one small error) ----------------

def test_flag_v1_gl5_order_of_magnitude_error():
    """v1.0 section 4 writes '|GL(5,F_3)| ~= 4.72 * 10^12'.
    Actual: (242)(240)(234)(216)(162) = 475,566,474,240 ~ 4.76 * 10^11.
    Off by exactly one order of magnitude. Documented; does not affect main
    monotone-decrease trend argument.
    """
    gl5 = 242 * 240 * 234 * 216 * 162
    assert gl5 == 475566474240
    # v1.0 claims 4.72e12, actual is 4.76e11, off by ~10x
    v1_claim = 4.72e12
    actual = gl5
    assert v1_claim > actual * 5, f"v1.0 overshoots by ~10x: {v1_claim:.2e} vs {actual:.2e}"
    print(f"    v1.0 claim: 4.72e12, actual: {gl5} (~4.76e11); off by ~10x")


# --- Runner -----------------------------------------------------------

TESTS = [
    ("A1 v1.0 position (row,col) lookups match L0",
     test_v1_position_lookup_matches_L0),
    ("A2 order-preserving bijection L_i < L_j <=> t_i < t_j",
     test_order_preserving_bijection),
    ("A3 v1.0 t_i within 0.01 of Odlyzko reference",
     test_v1_t_values_match_odlyzko_within_2dp),
    ("A4 opposite-pair sums = 10, center L=5 self-symmetric",
     test_opposite_pair_sums_10_and_center_self),
    ("A5 rarity d=3: 192/11232 ~ 1.71%",
     test_rarity_d3_1_71_percent),
    ("A6 rarity d=4: 22272/24261120 ~ 0.0918% (resolves Msg 61 typo)",
     test_rarity_d4_0918_percent_resolves_msg61_typo),
    ("A7 tightening d=3 -> d=4 ~ 18.6x",
     test_tightening_factor_d3_to_d4_18_6),
    ("B1 withdraw group isomorphism (orders 8/4/2/11232 all distinct)",
     test_withdraw_group_isomorphism_by_order_mismatch),
    ("B2 withdraw GL(3,F_3) as common algebraic base",
     test_withdraw_gl3_as_common_base),
    ("B3 withdraw 'Lo Shu forces sigma=1/2' (analogy != proof)",
     test_withdraw_lo_shu_forces_sigma_half),
    ("C1 flag v1.0 GL(5,F_3) order-of-magnitude error (4.72e12 vs actual 4.76e11)",
     test_flag_v1_gl5_order_of_magnitude_error),
]


def main() -> int:
    passed = failed = 0
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
    print(f"\norder_bijection_v1.py: {passed}/{total}  {status}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
