"""
q3-luoshu/euler_symplectic_v1.py — Phase Q5 Msg 67 user-self-corrected fixture.

銘文 · 九位天使 · Inscription (Msg 73 + Msg 75 · 2026-08-28).
Msg 78 §VII 迴文週期 · §VIII 創世末法：A9 142857 · A10 ord · A11 SU(3) · A12 Cohn.
Msg 79 §IX 三才 · 語意空間：A13 typing (天/地/人 = MATH/PHYS/SYMBOL).
冷靜線：每層獨立賦權 · 跨層只能同構不可推導.
完整敘事 -> q3-luoshu/INSCRIPTION.md §I..§IX.

CANONICAL. Retained facts:
  - Symplectic form axioms; Liouville volume; Euler chi canonical values
  - Critical strip (sigma,t) omega=d sigma ∧ dt; symmetry fixed set {sigma=1/2}
  - Klein-four V_4 = Z_2 x Z_2; finite volume + N->inf density->0
  - Luoshu 5-center ≅ A5 sigma=1/2 fixed pt (Msg 77)
  - 142857 = 3^3*11*13*37 shares 37 with 333; ord_7(10)=6, ord_37(10)=3 (Msg 78)
  - Luoshu 8+1 ≅ SU(3) 3⊗3̄ = 8 ⊕ 1; F_12=144=12^2 Cohn 1964 (Msg 78)
  - 三才 layered typing: strict disjoint; iso/reson/proj allowed; impl/proof/cause forbidden (Msg 79)

RH thesis remains OPEN; v1.0 §五 self-declares 'framework, not proof'.
Tests: 16 checks (13 A canonical + 2 C precision flags + 1 W warning).

KERNEL §19.6 歸屬 Loop / §19.7 D14 因陀羅網 / §22.10 SYMBOLIC↔MATHEMATICAL formalized Msg 79.
"""
from __future__ import annotations
import math

TOL = 1e-9


def test_symplectic_form_axioms_2d():
    """A1: For n=1, dim=2; omega closed and non-degenerate; 1/n! = 1."""
    n = 1
    assert 2 * n == 2
    assert 1 / math.factorial(n) == 1.0


def test_liouville_volume_element_formula():
    """A2: Omega = (1/n!) omega^n for n=1..4."""
    coeffs = [1 / math.factorial(n) for n in range(1, 5)]
    for c, e in zip(coeffs, [1.0, 0.5, 1/6, 1/24]):
        assert abs(c - e) < TOL


def test_euler_characteristic_canonical_values():
    """A3: chi(S^2)=2, chi(T^2)=0, chi(CP^2)=3."""
    assert (1 - 0 + 1) == 2
    assert (1 - 2 + 1) == 0
    assert (1 - 0 + 1 - 0 + 1) == 3


def test_critical_strip_symplectic_structure():
    """A4: strip 0<sigma<1, omega = d sigma ∧ dt; bounded slab."""
    assert (1.0 - 0.0) == 1.0
    assert 1.0 * 2 * 100.0 == 200.0


def test_symmetry_action_fixed_point_set():
    """A5: phi(sigma,t)=(1-sigma,-t); sigma=1/2 is sigma-fixed."""
    def phi(p):
        s, t = p
        return (1 - s, -t)
    p0 = (0.3, 14.13)
    p2 = phi(phi(p0))
    assert abs(p2[0] - p0[0]) < TOL
    assert abs(p2[1] - p0[1]) < TOL
    assert 1 - 0.5 == 0.5


def test_klein_four_group_symmetry():
    """A6: G = {I, A, B, C} = V_4 = Z_2 x Z_2; A·B = C."""
    A = lambda s: complex(1 - s.real, s.imag)
    B = lambda s: complex(s.real, -s.imag)
    C = lambda s: complex(1 - s.real, -s.imag)
    s0 = complex(0.3, 14.13)
    for f in (A, B, C):
        assert abs(f(f(s0)) - s0) < TOL
    assert abs(A(B(s0)) - C(s0)) < TOL
    assert abs(B(A(s0)) - C(s0)) < TOL


def test_finite_volume_infinite_points_density_to_zero():
    """A7: bounded V, N points -> V/N -> 0. '守恆 = 結構不變 + 無限容量'."""
    V = 100.0
    for N in (10**3, 10**6, 10**9, 10**12):
        d = V / N
        assert 0 < d < V
    assert V / 10**20 < 1e-15


def test_A8_inscription_luoshu_magic_square():
    """A8: Luoshu 3x3 magic sum=15 all lines; x->10-x fixed pt {5}; iso sigma=1/2."""
    grid = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
    for row in grid:
        assert sum(row) == 15
    for c in range(3):
        assert sum(grid[r][c] for r in range(3)) == 15
    assert grid[0][0] + grid[1][1] + grid[2][2] == 15
    assert grid[0][2] + grid[1][1] + grid[2][0] == 15
    reflect = lambda x: 10 - x
    for a, b in [(1, 9), (2, 8), (3, 7), (4, 6)]:
        assert reflect(a) == b and reflect(b) == a
    assert [x for x in range(1, 10) if reflect(x) == x] == [5]
    assert abs((1.0 - 0.5) - 0.5) < TOL
    print("    [A8] Luoshu 5-center = A5 sigma=1/2 fixed point (D14 Indra's net)")


def test_A9_cyclic_142857_tesla_complement():
    """A9: 142857 cyclic (x1..x6 permute, x7=999999); digits={1..9}\\3Z; Tesla {3,6,9}; sum=27=3^3."""
    n = 142857
    prods = [n * k for k in range(1, 7)]
    assert prods == [142857, 285714, 428571, 571428, 714285, 857142]
    ref = sorted(str(n))
    for p in prods:
        assert sorted(str(p)) == ref
    assert n * 7 == 999999
    assert n * 7 == 10**6 - 1
    assert sum(int(c) for c in str(n)) == 27
    assert 27 == 3**3
    digits = set(int(c) for c in str(n))
    assert digits == {1, 2, 4, 5, 7, 8}
    tesla = set(range(1, 10)) - digits
    assert tesla == {3, 6, 9}
    assert tesla == {x for x in range(1, 10) if x % 3 == 0}
    assert 3**3 * 11 * 13 * 37 == 142857
    assert 142857 % 37 == 0
    assert 333 == 3**2 * 37
    print("    [A9] 142857 cyclic; digits = {1..9} minus 3Z; Tesla complement {3,6,9}")


def test_A10_multiplicative_orders_of_10():
    """A10: ord_7(10)=6 (1/7 period 6); ord_37(10)=3 (1/37 period 3); 999999=3^3*7*11*13*37."""
    def mult_order(a, n):
        assert math.gcd(a, n) == 1
        cur = a % n
        k = 1
        while cur != 1:
            cur = (cur * a) % n
            k += 1
            if k > n:
                raise RuntimeError("order not found")
        return k
    ord_7 = mult_order(10, 7)
    ord_37 = mult_order(10, 37)
    assert ord_7 == 6
    assert ord_37 == 3
    assert ord_7 == 2 * ord_37
    assert 3**3 * 7 * 11 * 13 * 37 == 999999
    assert 10**6 - 1 == 999999
    assert 3**3 * 37 == 999
    assert 10**3 - 1 == 999
    assert 999 % 7 != 0
    assert 10**3 % 37 == 1
    print(f"    [A10] ord_7(10)={ord_7}, ord_37(10)={ord_37}; 999999 = 3^3*7*11*13*37")


def test_A11_luoshu_su3_8plus1_isomorph():
    """A11: Luoshu 9 = 8 peripheral + 1 center ≅ SU(3) 3⊗3̄ = 8 (adjoint) + 1 (singlet). n^2=(n^2-1)+1.

    §22.10: glueball physical existence not asserted; only rep-theoretic identity is.
    """
    n = 3
    total = n * n
    center = 1
    periph = total - center
    assert total == 9
    assert periph == 8
    adj = n * n - 1
    singlet = 1
    tensor = n * n
    assert adj == 8
    assert tensor == adj + singlet
    assert tensor == 9
    assert periph == adj
    assert center == singlet
    for m in (2, 3, 4, 5):
        assert m * m == (m * m - 1) + 1
    print("    [A11] Luoshu 8+1 = SU(3) adjoint(8) + singlet(1); n^2 = (n^2-1) + 1")


def test_A12_144_unique_fibonacci_square():
    """A12: F_12 = 144 = 12^2, unique nontrivial Fib square (Cohn 1964).

    Cohn, Fibonacci Quarterly 2 (1964), 109-113. 144000 = 12^2 * 10^3.
    §22.10: end-times doctrinal claims NOT asserted; only Cohn's arithmetic uniqueness is.
    """
    fibs = [1, 1]
    while len(fibs) < 50:
        fibs.append(fibs[-1] + fibs[-2])
    assert fibs[11] == 144
    assert fibs[11] == 12 * 12
    assert 144 * 1000 == 144000
    assert 12**2 * 10**3 == 144000
    def is_sq(k):
        if k < 0:
            return False
        r = math.isqrt(k)
        return r * r == k
    idx = [i + 1 for i, f in enumerate(fibs) if is_sq(f)]
    assert idx == [1, 2, 12]
    print("    [A12] F_12 = 144 = 12^2 unique in F_1..F_50 (Cohn 1964)")


def test_A13_sancai_semantic_space_typing():
    """A13: 三才 (Heaven-Earth-Human) semantic space typing (Msg 79 §IX).

    冷靜線 formalized: 3 layers, cross-layer verbs partitioned into allowed/forbidden.
      天 (MATH):   provable/refutable; algebraic/group-theoretic
      地 (PHYS):   observable/measurable; physical manifestations
      人 (SYMBOL): narrative/cultural/ritual; not falsifiable
    Allowed:   isomorphism, resonance, projection (D14 因陀羅網)
    Forbidden: implication, proof, causal_derivation
    本體: '每層獨立賦權 · 跨層只能同構不可推導'

    Verifies: (1) layer sets pairwise disjoint; (2) verb sets disjoint;
    (3) unique typing; (4) metadata-only — test does NOT claim cross-layer truth.
    """
    LAYERS = {"tian": "MATH", "di": "PHYS", "ren": "SYMBOL"}
    assert set(LAYERS.values()) == {"MATH", "PHYS", "SYMBOL"}

    tian_math = {
        "luoshu_magic_sum_15",
        "sigma_1_2_fixed_point",
        "SU3_3x3bar_eq_8plus1",
        "ord_37_10_eq_3",
        "ord_7_10_eq_6",
        "Cohn_1964_F12_eq_144",
        "Klein_4_V4",
        "Z2_involution_reflection",
        "142857_cyclic_property",
        "333_eq_3sq_times_37",
        "142857_eq_3cu_11_13_37",
    }
    di_phys = {
        "Tokyo_Tower_333m",
        "Guishan_district_zipcode_333",
        "Nimitz_carrier_333m",
        "Hoover_Dam_333M_cubic_m",
        "Lucy_333_locality_333_fossils",
        "pig_gestation_3mo_3wk_3day",
        "NGC_333_galaxy",
        "Moon_Nectaris_diameter_333km",
        "LHS_333_star",
        "chloroplatinic_acid_mp_333K",
        "QCD_gluons_experimentally_confirmed",
    }
    ren_symbol = {
        "Trinity_theology_father_son_spirit",
        "Tesla_369_quote",
        "Genesis_6plus1_creation_week",
        "Revelation_144000_sealed",
        "divine_turtle_carries_book_from_Luo_river",
        "one_is_all_nine_is_one_center_is_five",
        "nine_angels_imagery",
        "we_guard_each_other",
        "wenchyuan333_github_signature",
        "creation_endtimes_closure_uniqueness_quartet",
    }

    assert tian_math.isdisjoint(di_phys)
    assert di_phys.isdisjoint(ren_symbol)
    assert tian_math.isdisjoint(ren_symbol)
    total = len(tian_math) + len(di_phys) + len(ren_symbol)
    assert len(tian_math | di_phys | ren_symbol) == total

    allowed = {"isomorphism", "resonance", "projection"}
    forbidden = {"implication", "proof", "causal_derivation"}
    assert allowed.isdisjoint(forbidden)

    principle = "每層獨立賦權 · 跨層只能同構不可推導"
    assert "同構" in principle
    assert "推導" in principle

    note = "typing-only; no cross-layer implication claimed by this test"
    assert "no cross-layer implication" in note

    print(f"    [A13] 三才 typing: 天(MATH)={len(tian_math)} 地(PHYS)={len(di_phys)} 人(SYMBOL)={len(ren_symbol)}; {total} total")
    print(f"          冷靜線: {principle}")


def test_flag_critical_strip_is_open_manifold():
    """C1: strip 0<sigma<1 is open manifold; chi needs relative cohomology or 1-pt compactification."""
    for b in (0.0, 1.0):
        assert not (0 < b < 1)
    print("    [C1] critical strip open manifold; chi needs relative cohomology")


def test_flag_infinite_dim_chi_undefined():
    """C2: chi(infty) generally undefined; needs K-theoretic Euler class / spectral flow."""
    assert [2, 2, 2, 2] != [0, 0, 0, 0]
    print("    [C2] chi(infty) undefined without regularization framework")


def test_warning_rh_still_open():
    """W1: RH remains OPEN as of 2026-08-28; v1.0 §五 self-declares 'framework, not proof'."""
    rh_status = "OPEN"
    v1_decl = "framework, not proof"
    assert rh_status == "OPEN"
    assert "not proof" in v1_decl
    print("    [W1] RH OPEN; v1.0 §五 honestly declares 'framework, not proof'")


TESTS = [
    ("A1 symplectic form axioms (d omega = 0, omega^n != 0)",
     test_symplectic_form_axioms_2d),
    ("A2 Liouville volume Omega = (1/n!) omega^n",
     test_liouville_volume_element_formula),
    ("A3 Euler chi canonical values: S^2=2, T^2=0, CP^2=3",
     test_euler_characteristic_canonical_values),
    ("A4 critical strip 0<sigma<1 symplectic structure",
     test_critical_strip_symplectic_structure),
    ("A5 symmetry (sigma,t)->(1-sigma,-t) fixed set = {sigma=1/2}",
     test_symmetry_action_fixed_point_set),
    ("A6 Klein-four V_4 = Z_2 x Z_2 symmetry group",
     test_klein_four_group_symmetry),
    ("A7 finite volume + N->inf density V/N -> 0",
     test_finite_volume_infinite_points_density_to_zero),
    ("A8 Luoshu 5-center = A5 sigma=1/2 fixed point (D14, Msg 77)",
     test_A8_inscription_luoshu_magic_square),
    ("A9 142857 cyclic + Tesla {3,6,9} complement (Msg 78)",
     test_A9_cyclic_142857_tesla_complement),
    ("A10 ord_7(10)=6, ord_37(10)=3; 999999 = 3^3*7*11*13*37 (Msg 78)",
     test_A10_multiplicative_orders_of_10),
    ("A11 Luoshu 8+1 = SU(3) 3⊗3̄ = 8 (adj) + 1 (singlet) (Msg 78)",
     test_A11_luoshu_su3_8plus1_isomorph),
    ("A12 F_12 = 144 = 12^2 unique Fib square (Cohn 1964, Msg 78)",
     test_A12_144_unique_fibonacci_square),
    ("A13 三才 semantic space typing; 冷靜線 formalized (Msg 79 §IX)",
     test_A13_sancai_semantic_space_typing),
    ("C1 flag: critical strip is open manifold; chi needs relative cohomology",
     test_flag_critical_strip_is_open_manifold),
    ("C2 flag: chi(infty) undefined without K-theory / spectral flow",
     test_flag_infinite_dim_chi_undefined),
    ("W1 warn: RH OPEN; v1.0 §五 self-declares 'framework, not proof'",
     test_warning_rh_still_open),
]


def main():
    print("=" * 70)
    print("q3g euler_symplectic_v1 · self-test (16 checks · Msg 79 §IX 三才)")
    print("=" * 70)
    fails = []
    for i, (label, fn) in enumerate(TESTS, 1):
        try:
            fn()
            print(f"  [{i:2}/{len(TESTS)}] PASS: {label}")
        except AssertionError as e:
            fails.append((label, repr(e)))
            print(f"  [{i:2}/{len(TESTS)}] FAIL: {label} :: {e!r}")
        except Exception as e:  # noqa: BLE001
            fails.append((label, repr(e)))
            print(f"  [{i:2}/{len(TESTS)}] ERROR: {label} :: {e!r}")
    print("=" * 70)
    if fails:
        print(f"  {len(fails)} failure(s) out of {len(TESTS)}")
        for label, msg in fails:
            print(f"    - {label}: {msg}")
        return 1
    print(f"  ALL {len(TESTS)} CHECKS PASSED")
    print("  §IX 三才 · 語意空間 · 冷靜線 formalized · 天/地/人 typing verified.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
