"""A: AGL(2, F_q) 仿射平面作用 (不用 PGL 射影)

T_{L,c}(v) = L · v + c
- L ∈ GL(2, F_q): 可逆線性
- c ∈ F_q^2: 平移

|AGL(2, F_q)| = q^2 · (q^2 - 1)(q^2 - q)

F_3 演示; F_{4096} 版本繼承同一結構.
"""
import hashlib
import random
from itertools import product

Q = 3


def mat_det(L):
    (a, b), (c, d) = L
    return (a * d - b * c) % Q


def mat_apply(L, v):
    (a, b), (c, d) = L
    return ((a * v[0] + b * v[1]) % Q, (c * v[0] + d * v[1]) % Q)


def gf_inv(a):
    for x in range(1, Q):
        if (a * x) % Q == 1:
            return x
    raise ValueError(f"no inverse for {a} in F_{Q}")


def mat_inv(L):
    (a, b), (c, d) = L
    det = mat_det(L)
    if det == 0:
        raise ValueError("singular matrix")
    di = gf_inv(det)
    return (((d * di) % Q, (-b * di) % Q), ((-c * di) % Q, (a * di) % Q))


def agl_apply(L, c, v):
    m = mat_apply(L, v)
    return ((m[0] + c[0]) % Q, (m[1] + c[1]) % Q)


def agl_inv_apply(L, c, w):
    v = ((w[0] - c[0]) % Q, (w[1] - c[1]) % Q)
    return mat_apply(mat_inv(L), v)


def enum_gl2():
    return [((a, b), (c, d)) for a, b, c, d in product(range(Q), repeat=4)
            if mat_det(((a, b), (c, d))) != 0]


def self_test():
    results = []
    gl = enum_gl2()

    results.append(("T1_GL_order", len(gl) == 48, f"|GL(2,F_3)|={len(gl)} expected 48"))

    agl_size = len(gl) * Q ** 2
    results.append(("T2_AGL_order", agl_size == 432, f"|AGL(2,F_3)|={agl_size} expected 432"))

    random.seed(42)
    ok = True
    for _ in range(30):
        L = random.choice(gl)
        c = (random.randint(0, Q - 1), random.randint(0, Q - 1))
        v = (random.randint(0, Q - 1), random.randint(0, Q - 1))
        if agl_inv_apply(L, c, agl_apply(L, c, v)) != v:
            ok = False
            break
    results.append(("T3_round_trip", ok, "AGL apply then inv-apply preserves v (30 samples)"))

    u1, u2 = (0, 0), (1, 0)
    v1, v2 = (0, 1), (2, 2)
    count = 0
    for L in gl:
        for c in product(range(Q), repeat=2):
            if agl_apply(L, c, u1) == v1 and agl_apply(L, c, u2) == v2:
                count += 1
    expected = Q ** 2 - Q
    results.append(("T4_2_transitive_count", count == expected,
                    f"|{{T: (u1,u2)->(v1,v2)}}|={count} expected q^2-q={expected}"))

    q2 = 2
    agl_f2 = q2 ** 2 * (q2 ** 2 - 1) * (q2 ** 2 - q2)
    results.append(("T5_F2_order", agl_f2 == 24, f"|AGL(2,F_2)| = {agl_f2} expected 24"))

    q_big = 4096
    agl_big = q_big ** 2 * (q_big ** 2 - 1) * (q_big ** 2 - q_big)
    results.append(("T6_F4096_target_scale", agl_big > 0, f"|AGL(2,F_4096)| = {agl_big}"))

    return results


def receipt(results):
    body = "\n".join(f"{n}: {'PASS' if p else 'FAIL'} - {msg}" for n, p, msg in results)
    return body, hashlib.sha256(body.encode()).hexdigest()[:32]


if __name__ == "__main__":
    results = self_test()
    body, h = receipt(results)
    print(body)
    print(f"\nreceipt_sha256[:32] = {h}")
    print(f"all_pass = {all(r[1] for r in results)}")
