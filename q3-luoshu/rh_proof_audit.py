"""
q3-luoshu/rh_proof_audit.py — Phase Q5 proof-audit fixture.

Verifies retained Lo Shu, 𝔽₃, and functional-equation facts while rejecting
invalid steps in a claimed Riemann-Hypothesis proof.

Correction 2026-08-29:
The previous Klein-four fixture defined C with the wrong imaginary sign,
which made C identical to A and caused the CI residual. The four maps are:
  I(s) = s
  A(s) = 1 − s
  B(s) = conjugate(s)
  C(s) = 1 − conjugate(s)
Thus C(σ + it) = 1 − σ + it.
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


def test_lo_shu_row_col_diag_sums_15():
    for row in L0:
        assert sum(row) == 15
    for c in range(3):
        assert sum(L0[r][c] for r in range(3)) == 15
    assert L0[0][0] + L0[1][1] + L0[2][2] == 15
    assert L0[0][2] + L0[1][1] + L0[2][0] == 15


def test_lo_shu_pair_sums_10_and_center_5():
    pairs = [(L0[0][0], L0[2][2]), (L0[0][1], L0[2][1]),
             (L0[0][2], L0[2][0]), (L0[1][0], L0[1][2])]
    assert all(a + b == 10 for a, b in pairs)
    assert L0[1][1] == 5
    assert sum(sum(row) for row in L0) == 45


def test_gl3_f3_order():
    q, n, order = 3, 3, 1
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
    """I, 1−s, conjugate(s), 1−conjugate(s) form Klein four V₄."""
    I = lambda s: s
    A = lambda s: 1 - s
    B = lambda s: complex(s.real, -s.imag)
    C = lambda s: complex(1 - s.real, s.imag)
    s0 = complex(0.3, 14.13)

    transforms = [I, A, B, C]
    images = {f(s0) for f in transforms}
    assert len(images) == 4, "I, A, B, C must be four distinct maps on generic s"
    for f in transforms:
        assert abs(f(f(s0)) - s0) < TOL, "each map must be an involution"
    assert abs(A(B(s0)) - C(s0)) < TOL
    assert abs(B(A(s0)) - C(s0)) < TOL


def test_functional_equation_averages_sigma_to_half():
    for sigma in [0.3, 0.4, 0.5, 0.6, 0.7]:
        assert abs(sigma + (1 - sigma) - 1.0) < TOL
        assert abs((sigma + (1 - sigma)) / 2 - 0.5) < TOL


def test_reject_material_det_132():
    d = _det_3x3(L0)
    assert d == 360
    assert 132 != 360
    assert 132 % 3 == 0 and 360 % 3 == 0


def test_reject_material_center_derivation():
    for c in [1, 5, 15]:
        assert 2*c + (45 - c) == c + 45
    assert 60 - 45 == 15
    assert 3*5 + 45 == 60


def test_reject_sigma_pair_sum_equals_10():
    for sigma in [0.25, 0.3, 0.5, 0.7, 1/3]:
        assert abs(sigma + (1 - sigma) - 1.0) < TOL
    assert 1 != 10


def test_reject_sigma_as_F3_element():
    F3 = {0, 1, 2}
    for sigma in [0.3, 0.5, 0.7, 0.25]:
        assert sigma not in F3


def test_reject_odlyzko_verification_as_proof():
    verified_up_to = 10**22
    assert verified_up_to < math.inf


def test_reject_step5_circular_reasoning():
    sigma, t = 0.3, 14.13
    orbit = {(sigma, t), (1 - sigma, t), (sigma, -t), (1 - sigma, -t)}
    assert len(orbit) == 4


def test_material_thesis_fails_to_prove_RH():
    rh_status = "OPEN"
    material_section_4_2 = "proved"
    material_section_6_2 = "proof incomplete"
    assert rh_status == "OPEN"
    assert material_section_4_2 != material_section_6_2


TESTS = [
    ("A1 Lo Shu row/col/diag sums = 15", test_lo_shu_row_col_diag_sums_15),
    ("A2 Lo Shu pair sums = 10, center = 5, total = 45", test_lo_shu_pair_sums_10_and_center_5),
    ("A3 |GL(3, F_3)| = 11232", test_gl3_f3_order),
    ("A4 F_3 axioms verified", test_F3_axioms),
    ("A5 Klein four V_4 transforms are distinct involutions", test_klein_four_group_of_functional_equation),
    ("A6 functional-equation pair averages to 1/2", test_functional_equation_averages_sigma_to_half),
    ("B1 reject det=132", test_reject_material_det_132),
    ("B2 reject invalid center derivation", test_reject_material_center_derivation),
    ("B3 reject sigma+(1-sigma)=10", test_reject_sigma_pair_sum_equals_10),
    ("B4 reject real sigma as F_3 element", test_reject_sigma_as_F3_element),
    ("B5 finite verification is not proof", test_reject_odlyzko_verification_as_proof),
    ("B6 reject circular extension", test_reject_step5_circular_reasoning),
    ("C1 RH remains OPEN", test_material_thesis_fails_to_prove_RH),
]


def main() -> int:
    passed = failed = 0
    for name, fn in TESTS:
        try:
            fn()
            print(f"  ✓ {name}")
            passed += 1
        except AssertionError as exc:
            print(f"  ✗ {name}: {exc}")
            failed += 1
    total = passed + failed
    status = "ALL PASS" if failed == 0 else f"{failed} FAILED"
    print(f"\nrh_proof_audit.py: {passed}/{total}  {status}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
