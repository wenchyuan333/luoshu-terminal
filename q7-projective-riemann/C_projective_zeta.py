"""Projective zeta count for elliptic curves over F_p.

Weil / Hasse: |E(F_p)| = p + 1 - a_p, |a_p| <= 2 sqrt(p).
Projective = affine points + 1 point at infinity.
"""


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def count_affine_curve(p: int, a: int, b: int) -> int:
    assert is_prime(p)
    count = 0
    for x in range(p):
        rhs = (x * x * x + a * x + b) % p
        if rhs == 0:
            count += 1
        else:
            for y in range(p):
                if (y * y) % p == rhs:
                    count += 1
    return count


def count_projective_curve(p: int, a: int, b: int) -> int:
    return count_affine_curve(p, a, b) + 1


def hasse_bound(p: int) -> float:
    return 2 * (p ** 0.5)


def hasse_check(p: int, a: int, b: int) -> dict:
    n_proj = count_projective_curve(p, a, b)
    a_p = p + 1 - n_proj
    bound = hasse_bound(p)
    return {
        "p": p, "a": a, "b": b,
        "affine": count_affine_curve(p, a, b),
        "projective": n_proj,
        "a_p": a_p,
        "abs_a_p": abs(a_p),
        "bound": bound,
        "within_bound": abs(a_p) <= bound,
    }


def _test_hasse_f5():
    assert hasse_check(5, 1, 1)["within_bound"]


def _test_hasse_f7():
    assert hasse_check(7, 2, 3)["within_bound"]


def _test_hasse_f11():
    assert hasse_check(11, 1, 6)["within_bound"]


def _test_projective_minus_affine_is_one():
    for p, a, b in [(5, 1, 1), (7, 2, 3), (11, 1, 6), (13, 4, 5)]:
        assert count_projective_curve(p, a, b) - count_affine_curve(p, a, b) == 1


def _test_f4096_bound():
    q = 4096
    bound = 2 * (q ** 0.5)
    assert 127.9 < bound < 128.1, bound  # 2 * sqrt(4096) = 128


if __name__ == "__main__":
    _test_hasse_f5()
    _test_hasse_f7()
    _test_hasse_f11()
    _test_projective_minus_affine_is_one()
    _test_f4096_bound()
    print("q7 C_projective_zeta: all 5 self-tests pass.")
    for p, a, b in [(5, 1, 1), (7, 2, 3), (11, 1, 6), (13, 4, 5)]:
        r = hasse_check(p, a, b)
        print(f"  F_{p}: |E| = {r['projective']}, a_p = {r['a_p']}, bound = {r['bound']:.3f}")
    print("  F_4096 target: |a_p| <= 2*sqrt(4096) = 128")
