"""PGL(2, F_q) 射影線性群 self-test.

|GL(2, F_q)|  = (q^2 - 1)(q^2 - q)
|SL(2, F_q)|  = q(q^2 - 1)
|PGL(2, F_q)| = |GL|/(q-1) = q(q^2 - 1) = q(q-1)(q+1)
|PSL(2, F_q)| = |PGL|/gcd(2, q-1)

sharply 3-transitive on P^1(F_q) —— 對比 AGL(2, F_q) 只是 2-transitive。
"""
from math import gcd


def gl2_order(q: int) -> int:
    return (q * q - 1) * (q * q - q)


def sl2_order(q: int) -> int:
    return q * (q * q - 1)


def pgl2_order(q: int) -> int:
    return sl2_order(q)


def psl2_order(q: int) -> int:
    return pgl2_order(q) // gcd(2, q - 1)


def p1_points_count(q: int) -> int:
    return q + 1


def _test_orders_f3():
    q = 3
    assert gl2_order(q) == 48
    assert sl2_order(q) == 24
    assert pgl2_order(q) == 24
    assert psl2_order(q) == 12
    assert p1_points_count(q) == 4


def _test_orders_f2():
    q = 2
    assert gl2_order(q) == 6
    assert pgl2_order(q) == 6
    assert p1_points_count(q) == 3


def _test_sharp_3_transitive_count_f3():
    q = 3
    assert pgl2_order(q) == (q + 1) * q * (q - 1) == 24


def _test_target_scale():
    q = 4096
    n = pgl2_order(q)
    assert n == q * (q * q - 1)
    assert n == 68_719_472_640, f"expected 68719472640, got {n}"
    assert p1_points_count(q) == 4097


def _test_pgl_vs_agl_domain_check():
    q = 3
    assert p1_points_count(q) == 4
    assert q * q == 9


def _test_psl_equals_pgl_when_q_even():
    for q in (4, 16, 4096):
        assert psl2_order(q) == pgl2_order(q)


if __name__ == "__main__":
    _test_orders_f3()
    _test_orders_f2()
    _test_sharp_3_transitive_count_f3()
    _test_target_scale()
    _test_pgl_vs_agl_domain_check()
    _test_psl_equals_pgl_when_q_even()
    print("q7 A_pgl2_4096: all 6 self-tests pass.")
    print(f"|PGL(2, F_4096)| = {pgl2_order(4096):,}")
    print(f"|P^1(F_4096)|    = {p1_points_count(4096):,}")
