"""Möbius transformations on P^1(F_p) for small prime p.

f(z) = (a z + b) / (c z + d) with ad - bc != 0.
Cross-ratio (z1, z2; z3, z4) is Möbius-invariant.

Contrast:
- q6 (affine): preserves origin, no infinity
- q7 (projective): preserves cross-ratio, includes infinity
"""

Q_DEMO = 5


def _inv(x: int, p: int) -> int:
    return pow(x, p - 2, p)


def mobius(a: int, b: int, c: int, d: int, z, p: int):
    if z == "inf":
        return "inf" if c % p == 0 else (a * _inv(c % p, p)) % p
    denom = (c * z + d) % p
    if denom == 0:
        return "inf"
    return ((a * z + b) * _inv(denom, p)) % p


def det(a: int, b: int, c: int, d: int, p: int) -> int:
    return (a * d - b * c) % p


def cross_ratio(z1, z2, z3, z4, p: int):
    num = ((z1 - z3) * (z2 - z4)) % p
    den = ((z1 - z4) * (z2 - z3)) % p
    if den == 0:
        return "inf"
    return (num * _inv(den, p)) % p


def _test_identity():
    p = Q_DEMO
    for z in range(p):
        assert mobius(1, 0, 0, 1, z, p) == z
    assert mobius(1, 0, 0, 1, "inf", p) == "inf"


def _test_composition():
    p = Q_DEMO
    f = (1, 2, 3, 4)
    g = (2, 1, 1, 4)
    assert det(*f, p) == 3
    assert det(*g, p) == 2
    a, b, c, d = f
    e, ff, gg, hh = g
    fg = ((a * e + b * gg) % p, (a * ff + b * hh) % p,
          (c * e + d * gg) % p, (c * ff + d * hh) % p)
    for z in range(p):
        assert mobius(*fg, z, p) == mobius(*f, mobius(*g, z, p), p)


def _test_cross_ratio_invariance():
    p = Q_DEMO
    z1, z2, z3, z4 = 1, 2, 3, 4
    cr_orig = cross_ratio(z1, z2, z3, z4, p)
    f = (2, 1, 3, 2)
    assert det(*f, p) == 1
    w = [mobius(*f, z, p) for z in (z1, z2, z3, z4)]
    if all(v != "inf" for v in w):
        cr_new = cross_ratio(*w, p)
        assert cr_orig == cr_new, f"CR not invariant: {cr_orig} vs {cr_new}"


def _test_infinity_handling():
    p = Q_DEMO
    assert det(0, 1, 1, 0, p) == 4
    assert mobius(0, 1, 1, 0, 0, p) == "inf"
    assert mobius(0, 1, 1, 0, "inf", p) == 0


def _test_p1_transitive():
    p = Q_DEMO
    for b in range(p):
        assert mobius(1, b, 0, 1, 0, p) == b


if __name__ == "__main__":
    _test_identity()
    _test_composition()
    _test_cross_ratio_invariance()
    _test_infinity_handling()
    _test_p1_transitive()
    print("q7 B_mobius: all 5 self-tests pass.")
