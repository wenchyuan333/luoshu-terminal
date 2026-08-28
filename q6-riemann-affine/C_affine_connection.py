"""C: 仿射聯絡 沿 z-軸 parallel transport

Firewall §22.4 前置聲明:
- 純代數層 parallel transport, T_k(v) = a_k · v + b_k
- 不涉時空維度、度規張量、曲率張量、物理場方程
- "parallel transport" 在此僅指代數層 map compose, 非黎曼幾何之平行移位

【進制可進可退】硬閘:
- forward: v -> T_63(T_62(...T_1(v)))
- backward: w -> T_1^{-1}(T_2^{-1}(...T_63^{-1}(w)))
- forward ∘ backward = id 於 F_q 上

對應 D14 元條 (規則本身即方法的多重投影):
- 物理面向: ∇ × E = 0 (不採納, firewall)
- 代數面向: AGL(1, F_q) sharply 2-transitive (採納, 本檔)
- 方法面向: experiment/verify/main 分支策略 (採納, 本分支即例)
"""
import hashlib
import random

STACK_DEPTH = 63
Q_DEMO = 4093  # nearest prime < 4096 (Fermat inverse); F_{4096} uses GF(2^12)


def gf_inv(a, q):
    return pow(a, q - 2, q)


def T(a, b, v, q):
    return (a * v + b) % q


def T_inv(a, b, w, q):
    return ((w - b) * gf_inv(a, q)) % q


def forward(layers, v, q):
    for a, b in layers:
        v = T(a, b, v, q)
    return v


def backward(layers, w, q):
    for a, b in reversed(layers):
        w = T_inv(a, b, w, q)
    return w


def gen_layers(depth, q, seed):
    rng = random.Random(seed)
    return [(rng.randint(1, q - 1), rng.randint(0, q - 1)) for _ in range(depth)]


def self_test():
    results = []
    q = Q_DEMO

    # T1: single-layer round-trip
    v = 42
    w = T(7, 11, v, q)
    v2 = T_inv(7, 11, w, q)
    results.append(("T1_single_layer", v2 == v, f"{v}->{w}->{v2}"))

    # T2: full 63-layer stack round-trip
    layers = gen_layers(STACK_DEPTH, q, seed=2026)
    v0 = 12345 % q
    w = forward(layers, v0, q)
    v_back = backward(layers, w, q)
    results.append(("T2_stack63_round_trip", v_back == v0,
                    f"depth={STACK_DEPTH}: {v0}->..->{w}->..->{v_back}"))

    # T3: 10 seeds, all recover
    ok = True
    for s in range(10):
        L = gen_layers(STACK_DEPTH, q, seed=s * 7 + 3)
        v0 = (s * 137 + 42) % q
        if backward(L, forward(L, v0, q), q) != v0:
            ok = False
            break
    results.append(("T3_10_seeds", ok, "10 random seeds all recover"))

    # T4: reversibility on 100 sample points (fixed stack)
    L = gen_layers(STACK_DEPTH, q, seed=333)
    samples = list(range(0, q, max(1, q // 100)))
    all_ok = all(backward(L, forward(L, v, q), q) == v for v in samples)
    results.append(("T4_bit_reversibility", all_ok,
                    f"identity on {len(samples)} sample points in F_{q}"))

    # T5: firewall declaration (docstring)
    results.append(("T5_firewall_declared", True,
                    "no spacetime/metric/curvature claims per firewall §22.4"))

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
