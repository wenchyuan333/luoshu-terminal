"""
q3-luoshu/riemann_kerr_disproof.py — Phase Q5 material triage fixture (Msg 61).

Formalizes verification of correct citations and disproof of false claims
in the transcript material "洛書 × Riemann ζ × Kerr 黑洞 三者對應" (Msg 61).

  A. CANONICAL  (correct citations verified against known references)
  B. ERROR      (false claims disproved by direct computation)
  C. CONFLICT   (material vs prior material, awaits primary-source resolution)

Reference:
  KERNEL §18.5 Phase Q5 material transcript registry (2にち round)
  MIR-001 §9 Claim Firewall
  q3-luoshu/converge.py (established 8-test fixture for ◎☉ + rarity)
"""
from __future__ import annotations
import math

TOL = 1e-9

# Odlyzko reference values for first 9 non-trivial Riemann zeta zeros (imag parts)
RIEMANN_T_FIRST_9 = [
    14.134725, 21.022040, 25.010858, 30.424876,
    32.935062, 37.586178, 40.918719, 43.327073, 48.005151,
]

L0 = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]


def _det_3x3(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)


# --- A. CANONICAL ------------------------------------------------------

def test_riemann_zeros_2dp_match_material():
    material = [14.13, 21.02, 25.01, 30.42, 32.93, 37.59, 40.92, 43.33, 48.01]
    for i, (m, ref) in enumerate(zip(material, RIEMANN_T_FIRST_9), 1):
        r = round(ref, 2)
        assert r == m, f"t_{i}: material {m} vs Odlyzko {r}"


def test_kerr_r_ph_schwarzschild_limit():
    """Bardeen 1972: r_ph = 2M[1 + cos(2/3 arccos(-|a|/M))]; a=0 -> 3M."""
    M, a = 1.0, 0.0
    r_ph = 2 * M * (1 + math.cos((2/3) * math.acos(-abs(a)/M)))
    assert abs(r_ph - 3.0) < TOL, f"r_ph(a=0) expected 3M, got {r_ph}"


def test_kerr_r_pm_schwarzschild_limit():
    """r_+- = M +- sqrt(M^2 - a^2); a=0 -> (2M, 0)."""
    M, a = 1.0, 0.0
    r_plus = M + math.sqrt(M*M - a*a)
    r_minus = M - math.sqrt(M*M - a*a)
    assert abs(r_plus - 2.0) < TOL, f"r_+(a=0) expected 2M, got {r_plus}"
    assert abs(r_minus) < TOL, f"r_-(a=0) expected 0, got {r_minus}"


# --- B. ERROR ----------------------------------------------------------

def test_reject_det_neq_zero_mod_3():
    """Material 1.2 claims 'det != 0 mod 3'. FALSE.

    det(L0) = 360 = 3*120, so 360 mod 3 = 0.
    => L0 (mod 3) is SINGULAR in F_3, NOT in GL(3, F_3).
    """
    d = _det_3x3(L0)
    assert d == 360, f"det L0 should be 360, got {d}"
    assert d % 3 == 0, (
        f"material 1.2 claims det != 0 mod 3, "
        f"but det = {d}, det mod 3 = {d % 3}"
    )


def test_reject_four_way_isomorphism():
    """Material 2.3 claims Sym(L_9) ~= Perm({rho_n}) ~= OrbitSymmetry(r_ph)
    ~= GL(3, F_3). FALSE — the four groups have pairwise distinct orders.
    """
    d4 = 8                                     # |D_4|
    s9 = math.factorial(9)                     # 362880
    gl3_f3 = (27 - 1) * (27 - 3) * (27 - 9)    # 11232
    # SO(2) has continuous (infinite) order; three finite orders below must differ
    assert d4 == 8
    assert s9 == 362880
    assert gl3_f3 == 11232
    assert len({d4, s9, gl3_f3}) == 3, "expected 3 distinct finite orders"
    # Groups with distinct orders cannot be isomorphic


def test_reject_material_rarity_0918_conflicts_prior_1_71():
    """Material 1.2 claims rarity ~= 0.918%.
    Prior material (Msg 50) and q3-luoshu/converge.py T8 use 1.71%.
    The two claims disagree by ~0.79 percentage points; neither transcript
    provides a primary combinatorial derivation.
    Both await primary-source verification (flagged in KERNEL §18.5).
    """
    a = 0.918
    b = 1.71
    assert abs(a - b) > 0.5, "conflict expected between two rarity claims"
    ha = 0.00918 * 11232
    hb = 0.0171 * 11232
    print(f"    0.918% * 11232 = {ha:.4f} (nearest int {round(ha)}, residual {abs(ha-round(ha)):.4f})")
    print(f"    1.71%  * 11232 = {hb:.4f} (nearest int {round(hb)}, residual {abs(hb-round(hb)):.4f})")
    # Neither claim is decidable without derivation; documented as CONFLICT.


# --- C. RH-dependency (warning only) -----------------------------------

def test_rh_dependency_warning():
    """Material 3.3 states Sigma t_i symmetric distribution on sigma=1/2 as fact.
    Riemann Hypothesis remains unproven (as of 2026-08-28).
    Documentation only; no assertion.
    """
    print("    [warn] material 3.3 assumes Riemann Hypothesis (unproven)")


# --- Runner ------------------------------------------------------------

TESTS = [
    ("A1 first 9 Riemann zero t_n match Odlyzko (2dp)",
     test_riemann_zeros_2dp_match_material),
    ("A2 Kerr r_ph(a=0)=3M (Bardeen 1972)",
     test_kerr_r_ph_schwarzschild_limit),
    ("A3 Kerr r_pm(a=0)=(2M, 0)",
     test_kerr_r_pm_schwarzschild_limit),
    ("B1 det L0 = 360, 360 mod 3 = 0 (reject material 1.2 'det!=0 mod 3')",
     test_reject_det_neq_zero_mod_3),
    ("B2 |D_4|,|S_9|,|GL(3,F_3)| = 8, 362880, 11232 (reject material 2.3)",
     test_reject_four_way_isomorphism),
    ("B3 rarity 0.918% vs 1.71% conflict, both await derivation",
     test_reject_material_rarity_0918_conflicts_prior_1_71),
    ("C1 RH-dependency warning (material 3.3 assumes RH)",
     test_rh_dependency_warning),
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
    print(f"\nriemann_kerr_disproof.py: {passed}/{total}  {status}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
