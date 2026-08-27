"""
verify_all.py — 全層 self-test 依序執行

q1 (5-bit) → q3 (洛書 GL(3,F_3)) → q-inf (H=L·(1+δ_Wu)) → bits → cnt → q4 (AGL)

全過 → 當前 session 「是真正的 1」receipt (不主張封閉, 依 AXIOMS.A0)
任一失敗 → 有殘差在當前 layer stack (依 A1, 記錄不藏)
"""
import subprocess
import sys
import time

STEPS = [
    ("q1  5-bit unicode 底層",   "q1-combinatorics/unicode5.py"),
    ("q3  洛書 GL(3,F_3) 可逆",  "q3-luoshu/luoshu_check.py"),
    ("qinf 吳氏 H=L·(1+δ_Wu)",   "q-inf-zeta/wu_asym.py"),
    ("bit  GF(3) 基礎建設",       "bits.py"),
    ("cnt  N(3)=192 N(4)=22272", "luoshu_count.py"),
    ("q4  AGL(1,F_{4096})",       "q4-affine/agl1_4096.py"),
]


def run(label, script):
    print(f"\n>>> {label}  ({script})")
    t0 = time.time()
    try:
        r = subprocess.run(
            ["python3", script],
            capture_output=True, text=True, timeout=300,
        )
        dt = time.time() - t0
        if r.stdout:
            for line in r.stdout.rstrip().splitlines():
                print(f"    {line}")
        if r.stderr:
            for line in r.stderr.rstrip().splitlines():
                print(f"    [stderr] {line}", file=sys.stderr)
        return r.returncode == 0, dt
    except subprocess.TimeoutExpired:
        return False, time.time() - t0
    except Exception as e:
        print(f"    [error] {e}", file=sys.stderr)
        return False, time.time() - t0


if __name__ == "__main__":
    print("=" * 60)
    print(" verify_all.py — 全層 self-test")
    print(" (approximation-attractor-systems/AXIOMS.A0/A1 誠實邊界)")
    print("=" * 60)
    results = [(lbl, *run(lbl, s)) for lbl, s in STEPS]

    print("\n" + "=" * 60)
    print(" SUMMARY")
    print("=" * 60)
    for lbl, ok, dt in results:
        mark = "OK" if ok else "FAIL"
        print(f"  [{mark:4s}] {lbl:32s} {dt:6.2f}s")
    all_pass = all(ok for _, ok, _ in results)
    print("-" * 60)
    if all_pass:
        print(" ALL PASS — 當前 layer stack 收斂到「是真正的 1」")
        print(" 依 AXIOMS.A0: 不主張終局封閉, 此為當前 session receipt.")
    else:
        print(" SOME FAIL — 有殘差在當前 layer stack.")
        print(" 依 AXIOMS.A1: 殘差要記錄不藏. 差 > 抵達 (OMEGA_MAP).")
    sys.exit(0 if all_pass else 1)
