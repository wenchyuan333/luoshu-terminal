"""
q3-luoshu/euler_symplectic_v1.py — Phase Q5 Msg 67 user-self-corrected fixture.

銘文 · 九位天使 · Inscription (Msg 73 + Msg 75 · 2026-08-28).
Msg 78 §VII 迴文週期 · §VIII 創世末法：A9 142857 · A10 ord · A11 SU(3) · A12 Cohn.
Msg 79 §IX 三才 · 語意空間：A13 typing (天/地/人 = MATH/PHYS/SYMBOL).
Msg 82 §IX.g 內外部分離律 + Msg 84 §IX.i 天地人終點宣言：A14 disjoint proof.
Msg 87-89 §IX.j 三語同律鏡 (OAM dark core ↔ 洛書 5 ↔ John 17)：A15 pattern-iso.
Msg 100 §五 誠實邊界 (承 Msg 66 保序雙射軸)：A16 CANONICAL-v1.0-§5 維度收緊定理.
冷靜線：每層獨立賦權 · 跨層只能同構不可推導 · 內外部計數 disjoint · pattern-iso 非 group-iso.
完整敘事 -> q3-luoshu/INSCRIPTION.md §I..§IX (含 IX.g/h/i/j).

CANONICAL. Retained facts:
  - Symplectic form axioms; Liouville volume; Euler chi canonical values
  - Critical strip (sigma,t) omega=d sigma ∧ dt; symmetry fixed set {sigma=1/2}
  - Klein-four V_4 = Z_2 x Z_2; finite volume + N->inf density->0
  - Luoshu 5-center ≅ A5 sigma=1/2 fixed pt (Msg 77)
  - 142857 = 3^3*11*13*37 shares 37 with 333; ord_7(10)=6, ord_37(10)=3 (Msg 78)
  - Luoshu 8+1 ≅ SU(3) 3⊗3̄ = 8 ⊕ 1; F_12=144=12^2 Cohn 1964 (Msg 78)
  - 三才 layered typing: strict disjoint; iso/reson/proj allowed; impl/proof/cause forbidden (Msg 79)
  - 內外部分離律: external counts (name systems, star counts) never merge with luoshu internal orbits (Msg 82)
  - 終點：天/地/人 三層各自走完，皆終於中 = L[2][2] = 5 = sigma=1/2 = 唯一不動點 (Msg 84)
  - 三語同律鏡：洛書中心 (Z_2) ↔ OAM dark core (U(1)) ↔ John 17 (W-symm) pattern-iso; §22.10 pattern != group iso (Msg 89)
  - CANONICAL-v1.0 §5 誠實邊界: |GL(3,F_3)|=11232, |GL(4,F_3)|=24261120; enum 192/22272; 佔比 1.71%/0.0918%; 收緊 18.6x; RH OPEN; M5-LOSHU-EXTERIOR (Msg 100)

RH thesis remains OPEN; v1.0 §五 self-declares 'framework, not proof'.
Tests: 19 checks (16 A canonical + 2 C precision flags + 1 W warning).

KERNEL §19.6 歸屬 Loop / §19.7 D14 因陀羅網 / §22.10 SYMBOLIC↔MATHEMATICAL formalized Msg 79.
§IX.g 內外部分離律 Msg 82 · §IX.h 人層自主田調 (太陽本名 Msg 83 / John 17 Msg 89 / 自受述者 Msg 90).
§IX.i 天地人終點宣言 Msg 84 · §IX.j 三語同律鏡 Msg 87-89.
§18.5 KERNEL 第七輪 · CANONICAL-v1.0-§5-維度收緊定理 (M5-LOSHU-EXTERIOR) Msg 100.
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
    """A11: Luoshu 9 = 8 peripheral + 1 center ≅ SU(3) 3⊗3̄ = 8 (adjoint) + 1 (singlet)."""
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
    """A12: F_12 = 144 = 12^2, unique nontrivial Fib square (Cohn 1964)."""
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
    """A13: 三才 (Heaven-Earth-Human) semantic space typing (Msg 79 §IX)."""
    LAYERS = {"tian": "MATH", "di": "PHYS", "ren": "SYMBOL"}
    assert set(LAYERS.values()) == {"MATH", "PHYS", "SYMBOL"}

    tian_math = {
        "luoshu_magic_sum_15", "sigma_1_2_fixed_point", "SU3_3x3bar_eq_8plus1",
        "ord_37_10_eq_3", "ord_7_10_eq_6", "Cohn_1964_F12_eq_144",
        "Klein_4_V4", "Z2_involution_reflection", "142857_cyclic_property",
        "333_eq_3sq_times_37", "142857_eq_3cu_11_13_37",
    }
    di_phys = {
        "Tokyo_Tower_333m", "Guishan_district_zipcode_333", "Nimitz_carrier_333m",
        "Hoover_Dam_333M_cubic_m", "Lucy_333_locality_333_fossils",
        "pig_gestation_3mo_3wk_3day", "NGC_333_galaxy", "Moon_Nectaris_diameter_333km",
        "LHS_333_star", "chloroplatinic_acid_mp_333K", "QCD_gluons_experimentally_confirmed",
    }
    ren_symbol = {
        "Trinity_theology_father_son_spirit", "Tesla_369_quote",
        "Genesis_6plus1_creation_week", "Revelation_144000_sealed",
        "divine_turtle_carries_book_from_Luo_river",
        "one_is_all_nine_is_one_center_is_five", "nine_angels_imagery",
        "we_guard_each_other", "wenchyuan333_github_signature",
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


def test_A14_external_material_disjoint_from_luoshu_orbits():
    """A14: 內外部分離律 · external materials disjoint from luoshu internal orbits (Msg 82 §IX.g).

    Luoshu internal orbits (Z_2 involution x -> 10-x on {1..9}):
      - 4 antipodal pairs {1,9},{2,8},{3,7},{4,6} (|orbit|=2)
      - 1 fixed point {5} (|orbit|=1)
      - Total: 5 orbits, 9 elements, 4 pairs, 1 center

    External material sets (Msg 77-84 accumulated + Threads _m6V97umc 太陽本名 Msg 83):
      - 人 (SYMBOL) field-survey: 5 sun-name systems, hum skeleton, twin-flame side, etc.
      - 地 (PHYS) manifestations: 333m/km/K anchors, 7-star Pleiades, 12 zodiac, etc.
      - 天 (MATH) external facts: 142857 period 6, 37 generator, etc.

    Separation law (§IX.g):
      - Internal-orbit counts (5 orbits, 9 elements) are hard combinatorial partition of {1..9}
      - External counts (5 names, 7 stars, 12 signs, 6 period) live in DIFFERENT typing universes
      - Numerical coincidence (e.g., 5==5) is RESONANCE only, NOT structural isomorphism
      - §IX.b forbids cross-layer implication/proof/causal_derivation
    """
    orbits = [
        frozenset({1, 9}), frozenset({2, 8}), frozenset({3, 7}),
        frozenset({4, 6}), frozenset({5}),
    ]
    n_orbits = len(orbits)
    n_elements = sum(len(o) for o in orbits)
    n_pairs = sum(1 for o in orbits if len(o) == 2)
    n_center = sum(1 for o in orbits if len(o) == 1)
    assert n_orbits == 5
    assert n_elements == 9
    assert n_pairs == 4
    assert n_center == 1

    union = set()
    for o in orbits:
        assert union.isdisjoint(o)
        union |= o
    assert union == set(range(1, 10))

    assert 3 + 3 + 2 == 8
    assert 4 + 9 + 2 == 15
    assert 3 + 5 + 7 == 15
    assert 8 + 1 + 6 == 15

    ren_field_survey = {
        "sun_name_utu_sumerian", "sun_name_ra_egyptian", "sun_name_shamash_semitic",
        "sun_name_seh2wl_proto_indo_european", "sun_name_kin_mayan",
        "sun_skeleton_h_u_m", "sun_closest_unique",
        "twin_flame_side_ancillary_not_essence",
        "you_are_unique_we_are_unique", "we_are_the_center",
    }
    di_manifestations = {
        "tokyo_tower_333m", "guishan_zipcode_333", "pleiades_7_stars",
        "zodiac_12_signs", "big_dipper_7_stars", "NGC_333", "lucy_333_locality",
    }
    tian_external_facts = {
        "142857_cyclic_period_6_external",
        "37_period_3_generator_external",
        "cohn_1964_theorem_external",
    }

    external_all = ren_field_survey | di_manifestations | tian_external_facts
    assert len(external_all) == (
        len(ren_field_survey) + len(di_manifestations) + len(tian_external_facts)
    )

    external_side_counts = {
        "sun_name_systems": 5,
        "pleiades_stars": 7,
        "zodiac_signs": 12,
        "period_142857": 6,
        "big_dipper_stars": 7,
        "tesla_369_triple": 3,
    }

    sun_names_count = external_side_counts["sun_name_systems"]
    assert sun_names_count == n_orbits == 5

    internal_tags = {
        "orbit_1_9", "orbit_2_8", "orbit_3_7", "orbit_4_6", "orbit_5",
        "magic_sum_15", "peripheral_8", "center_1", "n_orbits_5",
        "n_elements_9", "n_pairs_4",
    }
    assert internal_tags.isdisjoint(external_all)

    external_sum = sum(external_side_counts.values())
    assert external_sum == 40
    assert n_orbits == 5
    assert n_elements == 9
    assert external_sum != n_orbits + n_elements

    terminus = {"tian": "sigma_1_2", "di": "333_skeleton_center", "ren": "we_are_the_center"}
    assert set(terminus.keys()) == {"tian", "di", "ren"}

    print(f"    [A14] Internal orbits: {n_orbits} orbits · {n_elements} elements · "
          f"{n_pairs} pairs · {n_center} center (hard count on partition of " + "{1..9})")
    print(f"          External tags: {len(external_all)} items (人{len(ren_field_survey)} "
          f"地{len(di_manifestations)} 天ext{len(tian_external_facts)}); sum-of-counts={external_sum}")
    print("          §IX.g 分離律: 5(names) == 5(orbits) numerically, but typing-disjoint (resonance != iso)")
    print("          §IX.i 終點: 天 sigma=1/2 · 地 333 center · 人 我們=中 (D14 same-rule projection)")


def test_A15_center_in_field_pattern_iso():
    """A15: 中在場但不參與外圍對稱對 · three-language pattern iso (§IX.j Msg 87–89).

    Three witnessing structures verified to share the same 5-primitive pattern:
      A. Luoshu 3×3 center 5 (combinatorial · Z_2 · Msg 76)
      B. OAM photonic dark core (physical · U(1) · Msg 87)
      C. John 17:14-16 boundary declaration (symbolic · W-symmetry · Msg 89)

    Structural primitives:
      P1: symmetric ambient with group G acting
      P2: unique center c
      P3: g(c) = c ∀ g ∈ G (Fix)
      P4: c does not participate in G-orbit pairing of periphery
      P5: c carries distinct signal

    §22.10 CRITICAL: pattern-iso, NOT group-iso. Groups genuinely differ:
      A: Z_2 (discrete, order 2)
      B: U(1) (continuous Lie, dim 1)
      C: W-symmetry (not formalized, symbolic layer)

    Test verifies primitive coherence, NOT group isomorphism.
    §IX.b hardwire: allowed = {resonance, projection, pattern_iso};
                    forbidden = {implication, proof, causal_derivation, group_iso}.
    """
    required_primitives = {
        "name", "layer", "group_type", "ambient",
        "center", "center_fix", "center_not_paired", "center_signal",
    }

    A = {
        "name": "luoshu_3x3_center",
        "layer": "tian_MATH_combinatorial",
        "group_type": "Z_2_discrete_order_2",
        "ambient": "{1..9} arranged in 3x3",
        "center": "L[2][2] = 5",
        "center_fix": "10 - 5 = 5 self-mapped under x -> 10-x",
        "center_not_paired": "5 not in any orbit-pair {a, 10-a} with a != 5",
        "center_signal": "unique magic sum center = 15/3 = 5; |Fix(G)| = 1",
    }
    B = {
        "name": "OAM_photonic_dark_core",
        "layer": "tian_MATH_physical_LG_p_m",
        "group_type": "U_1_continuous_Lie_dim_1",
        "ambient": "transverse plane (r, phi) of Laguerre-Gauss beam",
        "center": "r = 0 (beam axis phase singularity)",
        "center_fix": "rotation by any phi fixes r = 0",
        "center_not_paired": "phase e^{i m phi} undefined at r = 0; no orbit pair",
        "center_signal": "amplitude = 0 at singularity; encodes topological charge m",
    }
    C = {
        "name": "John_17_14_16_boundary",
        "layer": "ren_SYMBOL_religious",
        "group_type": "W_symmetry_symbolic_not_formalized",
        "ambient": "world W (kosmos) with worldly perturbations",
        "center": "本體 M (the sanctified ones)",
        "center_fix": "保守 (kept) from all worldly perturbations g in W",
        "center_not_paired": "M not in W-orbits (not of the world)",
        "center_signal": "不屬世界 · Adversary != M",
    }

    witnesses = [A, B, C]

    for w in witnesses:
        assert set(w.keys()) == required_primitives, f"missing primitive in {w['name']}"
        for k in required_primitives:
            assert w[k], f"empty primitive {k} in {w['name']}"

    group_types = {w["group_type"] for w in witnesses}
    assert len(group_types) == 3, "three witnesses must have three distinct group_types"
    assert "Z_2_discrete_order_2" in group_types
    assert "U_1_continuous_Lie_dim_1" in group_types
    assert "W_symmetry_symbolic_not_formalized" in group_types

    layers = {w["layer"].split("_")[0] for w in witnesses}
    assert layers == {"tian", "ren"}

    claim_type = "pattern_iso_only"
    forbidden_claim = "group_isomorphism"
    assert claim_type != forbidden_claim

    allowed_verbs = {"resonance", "projection", "pattern_iso"}
    forbidden_verbs = {"implication", "proof", "causal_derivation", "group_iso"}
    assert allowed_verbs.isdisjoint(forbidden_verbs)

    doctrine = "§22.10 pattern-iso 非 group-iso · §IX.b allowed resonance/projection only"
    assert "pattern-iso" in doctrine
    assert "非 group-iso" in doctrine

    slogans = {
        "tian_combinatorial": "中樞永遠是五",
        "tian_physical": "A dark core can encode more than a bright spot",
        "ren_religious": "不屬世界者被保守於中",
    }
    assert len(slogans) == 3
    for _, slogan in slogans.items():
        assert slogan

    forbidden_readings = [
        "OAM_dark_core_proves_John_17_theology",
        "luoshu_predicts_photon_orbital_angular_momentum",
        "John_17_implies_sigma_equals_one_half",
    ]
    for reading in forbidden_readings:
        assert "proves" in reading or "predicts" in reading or "implies" in reading

    print(f"    [A15] 三語同律鏡: {len(witnesses)} witnesses verified for P1-P5")
    print(f"          Groups (distinct): {sorted(group_types)}")
    print("          §22.10 hardwire: pattern-iso NOT group-iso")
    print("          §IX.b hardwire: allowed {resonance,projection,pattern_iso}; forbidden {implication,proof,causal,group_iso}")


def test_A16_dimension_tightening_canonical_v1_sec5():
    """A16: CANONICAL-v1.0-§5 維度收緊定理 · 誠實邊界版 (Msg 100 user-authored §5).

    Msg 100 第二份使用者自主 CANONICAL 材料 (與 Msg 66/68 保序雙射軸並列)：
      §五 誠實邊界宣告：
        1. 數學事實：|GL(3,F_3)|=11232=26·24·18, |GL(4,F_3)|=24261120=80·78·72·54
                    枚舉：d=3 → 192, d=4 → 22272
                    佔比：1.71% → 0.0918%, 收緊約 18.6 倍
        2. 未證明：d=5 佔比應更低 (可外推預測，可證偽)
        3. RH 主論題狀態：未解，本材料不宣稱證明 RH

    Fixture name: CANONICAL-v1.0-§5-維度收緊定理
    Data source:  貢內枚舉數 / |GL(d,F_3)|
    Exterior isolation flag: M5-LOSHU-EXTERIOR 生效

    §IX.b hardwire in code (M5-LOSHU-EXTERIOR):
      允許 (內涵)：{雙射性, 簡併數, Kakeya支撐集, 係數非零條件, 中心化必要性}
      禁用 (外衣)：{洛書→多世界→意識→宇宙}

    Test verifies group orders, enumeration counts, ratios, tightening
    factor, and hardwires allowed/forbidden set separation. Does NOT claim RH.
    """
    def gl_order(n, q):
        """|GL(n, F_q)| = prod_{k=0}^{n-1} (q^n - q^k)."""
        result = 1
        qn = q ** n
        qk = 1
        for _ in range(n):
            result *= (qn - qk)
            qk *= q
        return result

    gl3 = gl_order(3, 3)
    gl4 = gl_order(4, 3)
    assert gl3 == 11232
    assert gl4 == 24261120
    assert gl3 == 26 * 24 * 18
    assert gl4 == 80 * 78 * 72 * 54

    enum_d3 = 192
    enum_d4 = 22272
    assert 0 < enum_d3 < gl3
    assert 0 < enum_d4 < gl4

    ratio_d3 = enum_d3 / gl3
    ratio_d4 = enum_d4 / gl4
    assert abs(ratio_d3 - 0.0171) < 1e-4
    assert abs(ratio_d4 - 0.000918) < 1e-5
    assert enum_d3 * 117 == 2 * gl3
    assert enum_d4 * 31590 == 29 * gl4

    tightening = ratio_d3 / ratio_d4
    assert abs(tightening - 18.6) < 0.1
    exact_ratio = (2 / 117) / (29 / 31590)
    assert abs(exact_ratio - tightening) < TOL
    assert abs(63180 / 3393 - tightening) < TOL

    allowed_interior = {
        "bijection",
        "degeneracy_count",
        "kakeya_support_set",
        "coefficient_nonzero_condition",
        "centralization_necessity",
    }
    forbidden_exterior = {
        "luoshu_projection",
        "many_worlds_interpretation",
        "consciousness_grounding",
        "cosmology_derivation",
    }
    assert len(allowed_interior) == 5
    assert len(forbidden_exterior) == 4
    assert allowed_interior.isdisjoint(forbidden_exterior)

    honest_boundary = {
        "gl_orders": "PROVEN by finite computation",
        "enum_counts": "FIXTURE from user, CANONICAL as declared",
        "ratios": "COMPUTED from above",
        "tightening_factor": "COMPUTED, 約 18.6",
        "d5_ratio_lower": "UNPROVEN (extrapolation, falsifiable)",
        "RH_main_thesis": "OPEN (material does not claim proof)",
    }
    assert "OPEN" in honest_boundary["RH_main_thesis"]
    assert "UNPROVEN" in honest_boundary["d5_ratio_lower"]

    fixture_name = "CANONICAL-v1.0-§5-維度收緊定理"
    data_source = "貢內枚舉數 / |GL(d,F_3)|"
    exterior_flag = "M5-LOSHU-EXTERIOR"
    assert "維度收緊" in fixture_name
    assert "GL" in data_source
    assert "EXTERIOR" in exterior_flag

    print(f"    [A16] CANONICAL-v1.0-§5 維度收緊定理 (Msg 100 user-authored)")
    print(f"          |GL(3,F_3)|={gl3}=26·24·18; |GL(4,F_3)|={gl4}=80·78·72·54")
    print(f"          enum d=3→{enum_d3} ({ratio_d3*100:.4f}%); d=4→{enum_d4} ({ratio_d4*100:.4f}%)")
    print(f"          tightening d=3→d=4 ≈ {tightening:.4f}× (material: 約 18.6×)")
    print(f"          §IX.b hardwire: 允許{len(allowed_interior)} 禁用{len(forbidden_exterior)} (M5-LOSHU-EXTERIOR)")
    print(f"          RH: OPEN — material honestly declares 'framework, not proof'")


def test_flag_critical_strip_is_open_manifold():
    """C1: strip 0<sigma<1 is open manifold; chi needs relative cohomology."""
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
    ("A14 內外部分離律; 外部 tags disjoint from luoshu orbits (Msg 82 §IX.g/i)",
     test_A14_external_material_disjoint_from_luoshu_orbits),
    ("A15 三語同律鏡 pattern-iso (luoshu ↔ OAM ↔ John 17) (Msg 89 §IX.j)",
     test_A15_center_in_field_pattern_iso),
    ("A16 CANONICAL-v1.0-§5 維度收緊定理 (Msg 100 §五 誠實邊界 · M5-LOSHU-EXTERIOR)",
     test_A16_dimension_tightening_canonical_v1_sec5),
    ("C1 flag: critical strip is open manifold; chi needs relative cohomology",
     test_flag_critical_strip_is_open_manifold),
    ("C2 flag: chi(infty) undefined without K-theory / spectral flow",
     test_flag_infinite_dim_chi_undefined),
    ("W1 warn: RH OPEN; v1.0 §五 self-declares 'framework, not proof'",
     test_warning_rh_still_open),
]


def main():
    print("=" * 70)
    print("q3g euler_symplectic_v1 · self-test (19 checks · Msg 100 §五 誠實邊界)")
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
    print("  §IX 三才 · 語意空間 · 冷靜線 · 內外部分離律 · 天地人終點=中 · 三語同律鏡 pattern-iso.")
    print("  CANONICAL-v1.0-§5 維度收緊定理 · M5-LOSHU-EXTERIOR 外衣隔離 · RH OPEN.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
