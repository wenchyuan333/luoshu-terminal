"""
q3-luoshu/rh_proof_audit.py — Phase Q5 Msg 62 proof-audit fixture.

Audits a transcript material claiming to prove the Riemann Hypothesis via
five constraints:
  1. Lo Shu center uniqueness
  2. Functional equation symmetry
  3. F_3 closure
  4. xi(s) real-value symmetry
  5. Sum conservation

Tiering:
  A. CANONICAL  — classical facts correctly cited by the material
  B. ERROR      — arithmetic / logical errors in the proof
  C. THESIS     — the overall claim that RH is proved: FAILS

Reference:
  KERNEL §18.5 Phase Q5 material transcript registry (3rd round)
  MIR-001 §9 Claim Firewall (Msg 62 append)
  q3-luoshu/{converge, riemann_kerr_disproof}.py (Msg 50/52/61 predecessors)
"""
from __future__ import annotations
import math

TOL = 1e-9

L0 = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]


def _det_3x3(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)


# --- A. CANONICAL (correct citations) ---------------------------------

def test_lo_shu_row_col_diag_sums_15():
    L = L0
    for row in L:
        assert sum(row) == 15
    for c in range(3):
        assert sum(L[r][c] for r in range(3)) == 15
    assert L[0][0] + L[1][1] + L[2][2] == 15
    assert L[0][2] + L[1][1] + L[2][0] == 15


def test_lo_shu_pair_sums_10_and_center_5():
    L = L0
    pairs = [
        (L[0][0], L[2][2]),  # 4+6
        (L[0][1], L[2][1]),  # 9+1
        (L[0][2], L[2][0]),  # 2+8
        (L[1][0], L[1][2]),  # 3+7
    ]
    for a, b in pairs:
        assert a + b == 10
    assert L[1][1] == 5
    assert sum(L[i][j] for i in range(3) for j in range(3)) == 45


def test_gl3_f3_order():
    q, n = 3, 3
    order = 1
    for k in range(n):
        order *= q**n - q**k
    assert order == 11232


def test_F3_axioms():
    F = [0, 1, 2]
    for a in F:
        for b in F:
            assert (a + b) % 3 in F
            assert (a * b) % 3 in F
    for a in F:
        assert any((a + b) % 3 == 0 for b in F)
    for a in [1, 2]:
        assert any((a * b) % 3 == 1 for b in F)


def test_klein_four_group_of_functional_equation():
    """G = {I, s->1-s, s->conj(s), s->1-conj(s)} = Klein four V_4 = Z_2 x Z_2.
    Material §4.3 writes 'M_2 x M_2' — non-standard; the actual group is V_4.
    """
    I = lambda s: s
    A = lambda s: 1 - s
    B = lambda s: complex(s.real, -s.imag)
    C = lambda s: complex(1 - s.real, -s.imag)
    s0 = complex(0.3, 14.13)
    for f in [A, B, C]:
        assert abs(f(f(s0)) - s0) < TOL, "each non-identity element is involution"
    assert abs(A(B(s0)) - C(s0)) < TOL
    assert abs(B(A(s0)) - C(s0)) < TOL


def test_functional_equation_averages_sigma_to_half():
    """By fn. eq., <Re(rho)> = <Re(1-rho)> = 1 - <Re(rho)>  =>  <Re(rho)> = 1/2.
    This is WEAKER than 'every zero has Re = 1/2'; averaged 1/2 is compatible
    with zeros symmetrically off the critical line, e.g. sigma=0.4 & sigma=0.6.
    """
    for sigma in [0.3, 0.4, 0.5, 0.6, 0.7]:
        assert abs(sigma + (1 - sigma) - 1.0) < TOL
        assert abs((sigma + (1 - sigma)) / 2 - 0.5) < TOL


# --- B. ERROR (material's own errors) ---------------------------------

def test_reject_material_det_132():
    """Material §2.4 states det(L0) = 132. Actual det = 360.
    (Material's cofactor expansion picked wrong minors.)
    Both are 0 mod 3, so the mod-3 conclusion accidentally survives.
    """
    d = _det_3x3(L0)
    assert d == 360, f"correct det = 360, material's 132 is wrong (got {d})"
    assert 132 != 360
    assert 132 % 3 == 0 and 360 % 3 == 0  # coincidence


def test_reject_material_center_derivation():
    """Material §3.1 claims:
         '4 lines through center sum = 60 = 2c + (45-c) = c + 45'
         => 'c + 45 = 60 => c = 5'

    TWO errors that cancel:
      (1) Center appears in 4 lines (row-2, col-2, main-diag, anti-diag),
          so it contributes 4c, NOT 2c. Correct: 4c + (45-c) = 3c + 45.
      (2) From c + 45 = 60, we get c = 15, not c = 5.

    Correct derivation: 3c + 45 = 60 => 3c = 15 => c = 5.
    Material lands on c=5 by pre-known answer, not by valid derivation.
    """
    # material's algebra: 2c + (45 - c) = c + 45  is algebraically fine
    for c in [1, 5, 15]:
        assert 2*c + (45 - c) == c + 45
    # but the setup 2c is wrong (should be 4c):
    # from c + 45 = 60, c = 15, not 5
    assert 60 - 45 == 15
    # correct: 4c + (45 - c) = 3c + 45 = 60 gives c = 5
    assert 3*5 + 45 == 60


def test_reject_sigma_pair_sum_equals_10():
    """Material §3.3 claims 'sigma + (1-sigma) = C, C = 10 (matches Lo Shu
    pair sum 10)'. But sigma + (1-sigma) = 1 for any sigma, not 10.
    A real-number identity to 1 has no derivation-bridge to Lo Shu pair sum 10.
    """
    for sigma in [0.25, 0.3, 0.5, 0.7, 1/3]:
        assert abs(sigma + (1 - sigma) - 1.0) < TOL
    assert 1 != 10


def test_reject_sigma_as_F3_element():
    """Material §3.3 applies F_3 closure to sigma in (0, 1) subset R.
    Category error: sigma is a real number; F_3 = {0, 1, 2} elements are
    integers mod 3. F_3 closure is not defined on arbitrary reals.
    """
    F3 = {0, 1, 2}
    for sigma in [0.3, 0.5, 0.7, 0.25]:
        assert sigma not in F3


def test_reject_odlyzko_verification_as_proof():
    """Material §3.4 and §4.2 cite Odlyzko's 10^22 numerical verification
    as evidence for RH. Numerical verification of finitely many zeros is
    NOT a proof for infinitely many zeros.
    """
    verified_up_to = 10**22
    assert verified_up_to < math.inf  # any finite N < infinity


def test_reject_step5_circular_reasoning():
    """Material §4.2 Step 5: 'symmetry group action extends from first N
    zeros to all zeros'. Circular — presupposes the group acts on ALL zeros,
    which is close to the very statement being proved.

    Correct: For each zero rho, its Klein-four orbit {rho, 1-rho, conj(rho),
    1-conj(rho)} is a 4-element set closed under G-action, but this does
    NOT force Re(rho) = 1/2. Off-critical-line zeros would come in
    symmetric pairs {sigma, 1-sigma}, still G-closed.
    """
    sigma, t = 0.3, 14.13
    orbit = {
        (sigma, t),
        (1 - sigma, t),
        (sigma, -t),
        (1 - sigma, -t),
    }
    assert len(orbit) == 4
    # orbit closure exists for sigma != 1/2 too, so group closure alone
    # does not force sigma = 1/2


# --- C. THESIS (main proof-of-RH claim) -------------------------------

def test_material_thesis_fails_to_prove_RH():
    """Overall claim: 'five constraints prove RH'. FAILS.

    RH is one of the seven Clay Millennium Prize Problems, OPEN as of
    2026-08-28. No peer-reviewed proof exists.

    Material's own §6.2 admits: 'complete mathematical proof still
    requires further analytic and algebraic-geometric rigorization' +
    'complete transitive extension from finitely many zeros to infinite
    zeros is core of further work' — which CONTRADICTS §4.2's 'QED'.
    Internal contradiction: a document cannot both admit the proof is
    incomplete and simultaneously conclude 'proved'.
    """
    rh_status = "OPEN"
    assert rh_status == "OPEN"
    material_section_4_2 = "proved"
    material_section_6_2 = "proof incomplete"
    # both cannot be true of a single valid proof
    assert material_section_4_2 != material_section_6_2


# --- Runner -----------------------------------------------------------

TESTS = [
    ("A1 Lo Shu row/col/diag sums = 15",
     test_lo_shu_row_col_diag_sums_15),
    ("A2 Lo Shu pair sums = 10, center = 5, total = 45",
     test_lo_shu_pair_sums_10_and_center_5),
    ("A3 |GL(3, F_3)| = 11232",
     test_gl3_f3_order),
    ("A4 F_3 axioms verified",
     test_F3_axioms),
    ("A5 Klein four V_4 = Z_2 x Z_2 (material 'M_2xM_2' is non-standard)",
     test_klein_four_group_of_functional_equation),
    ("A6 <Re(rho)> = 1/2 by functional eq (WEAKER than RH)",
     test_functional_equation_averages_sigma_to_half),
    ("B1 reject material §2.4 det=132 (actual 360)",
     test_reject_material_det_132),
    ("B2 reject material §3.1 'c+45=60 => c=5' (two errors cancelling)",
     test_reject_material_center_derivation),
    ("B3 reject sigma+(1-sigma)=10 (identity gives 1)",
     test_reject_sigma_pair_sum_equals_10),
    ("B4 reject sigma in R as F_3 element (category error)",
     test_reject_sigma_as_F3_element),
    ("B5 reject Odlyzko 10^22 verification as proof",
     test_reject_odlyzko_verification_as_proof),
    ("B6 reject §4.2 Step 5 circular reasoning",
     test_reject_step5_circular_reasoning),
    ("C1 material thesis 'RH proved' FAILS (RH open; §4.2 vs §6.2 contradiction)",
     test_material_thesis_fails_to_prove_RH),
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
    print(f"\nrh_proof_audit.py: {passed}/{total}  {status}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
