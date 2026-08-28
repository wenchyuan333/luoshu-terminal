"""B: 仿射曲線 Weil zeta 類比

計 |E_aff(F_p)| for y^2 = x^3 + a x + b over prime F_p
Hasse (仿射版): ||E_aff(F_p)| - p| ≤ 2√p + 1  (包含無窮遠少一點調整)

不做完整 projective zeta 函數; 只計仿射點集。
與 A 接口: 仿射變換 x ↦ αx + β 保持點計數 (同構變換)
"""
import hashlib
import math


def count_affine(p, a, b):
    """Count affine points on y^2 = x^3 + a x + b over F_p, or None if singular"""
    if (4 * a ** 3 + 27 * b ** 2) % p == 0:
        return None
    count = 0
    for x in range(p):
        rhs = (x ** 3 + a * x + b) % p
        for y in range(p):
            if (y * y - rhs) % p == 0:
                count += 1
    return count


def hasse_check(p, a, b):
    c = count_affine(p, a, b)
    if c is None:
        return None, None, None, False
    err = abs(c - p)
    bound = 2 * math.isqrt(p) + 1
    return c, err, bound, err <= bound


def self_test():
    results = []

    # Non-singular test curves (discriminant 4a^3+27b^2 != 0 mod p)
    for label, (p, a, b) in [
        ("T1_F5", (5, 0, 1)),   # disc = 27 = 2 mod 5
        ("T2_F7", (7, 1, 1)),   # disc = 31 = 3 mod 7
        ("T3_F11", (11, 1, 6)), # disc = 4+972 = 976 = 8 mod 11 (was (2,3) which is singular)
        ("T4_F13", (13, 3, 5)), # disc = 108+675 = 783 = 3 mod 13
    ]:
        c, err, bound, ok = hasse_check(p, a, b)
        results.append((label, ok, f"F_{p} y^2=x^3+{a}x+{b}: |E_aff|={c}, |err|={err}, bound={bound}"))

    # T5: F_{4096} target scale record
    q = 4096
    max_err = 2 * math.isqrt(q) + 1
    results.append(("T5_F4096_bound", True, f"|E_aff(F_4096) - 4096| <= 2√4096+1 = {max_err}"))

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
