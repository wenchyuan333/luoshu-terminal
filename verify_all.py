"""
verify_all.py — 全層 self-test 依序執行 (v2 layered)

巢狀結構下的執行順序:
  q1 → q3 → q3c (converge) → q3d (riemann_kerr_disproof) → q3e (rh_proof_audit)
     → q3f (order_bijection_v1) → q3g (euler_symplectic_v1) → q-inf → bits → cnt
     → q4 → q5 (nested) → q6 (nested) → q7 (nested)

全過 → 當前 session「是真正的 1」receipt (不主張封閉, 依 AXIOMS.A0)
任一失敗 → 有殘差在當前 layer stack (依 A1, 記錄不藏)
"""
import subprocess
import sys
import time

STEPS = [
    ("q1  5-bit unicode 底層",             "q1-combinatorics/unicode5.py"),
    ("q3  洛書 GL(3,F_3) 可逆",            "q3-luoshu/luoshu_check.py"),
    ("q3c 洛書收斂算符 ◎☉ (Phase Q5)",     "q3-luoshu/converge.py"),
    ("q3d Riemann-Kerr 三對應反證 (Msg 61)","q3-luoshu/riemann_kerr_disproof.py"),
    ("q3e RH proof audit (Msg 62)",         "q3-luoshu/rh_proof_audit.py"),
    ("q3f order-preserving bijection v1.0 (Msg 66 self-corrected)",
                                             "q3-luoshu/order_bijection_v1.py"),
    ("q3g Euler-symplectic v1.0 (Msg 67 self-corrected)",
                                             "q3-luoshu/euler_symplectic_v1.py"),
    ("qinf 吳氏 H=L·(1+δ_Wu)",             "q-inf-zeta/wu_asym.py"),
    ("bit  GF(3) 基礎建設",                 "bits.py"),
    ("cnt  N(3)=192 N(4)=22272",           "luoshu_count.py"),
    ("q4   AGL(1,F_{4096})",                "q4-affine/agl1_4096.py"),
    ("q4o  AGL orbits",                     "q4-affine/orbits.py"),
    ("q5   盤堆立方體 (nested)",             "q4-affine/q5-stacked-boards/board_stack.py"),
    ("q6A  AGL(2,F_4096) 平面",             "q4-affine/q6-riemann-affine/A_agl2_4096.py"),
    ("q6B  Weil zeta affine",              "q4-affine/q6-riemann-affine/B_weil_zeta_affine.py"),
    ("q6C  parallel transport (代數)",      "q4-affine/q6-riemann-affine/C_affine_connection.py"),
    ("q7A  PGL(2,F_4096) 射影",             "q4-affine/q6-riemann-affine/q7-projective-riemann/A_pgl2_4096.py"),
    ("q7B  Möbius cross-ratio",             "q4-affine/q6-riemann-affine/q7-projective-riemann/B_mobius.py"),
    ("q7C  projective zeta (含∞)",          "q4-affine/q6-riemann-affine/q7-projective-riemann/C_projective_zeta.py"),
]


def _annotation_text(text):
    """Escape multiline subprocess output for GitHub workflow annotations."""
    return (
        text.replace("%", "%25")
        .replace("\r", "%0D")
        .replace("\n", "%0A")
    )


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
        diagnostic = (r.stderr or r.stdout or f"exit code {r.returncode}")[-2000:]
        return r.returncode == 0, dt, diagnostic
    except subprocess.TimeoutExpired:
        return False, time.time() - t0, "timeout after 300 seconds"
    except Exception as e:
        print(f"    [error] {e}", file=sys.stderr)
        return False, time.time() - t0, repr(e)


if __name__ == "__main__":
    print("=" * 68)
    print(" verify_all.py — 全層 self-test (v2 layered, 19 checks)")
    print(" (approximation-attractor-systems/AXIOMS.A0/A1 誠實邊界)")
    print("=" * 68)

    results = []
    for label, script in STEPS:
        ok, dt, diagnostic = run(label, script)
        results.append((label, script, ok, dt))
        if not ok:
            message = _annotation_text(diagnostic)
            print(f"::error file={script},title={label} failed::{message}")

    print("\n" + "=" * 68)
    print(" SUMMARY")
    print("=" * 68)
    for label, script, ok, dt in results:
        mark = "OK" if ok else "FAIL"
        print(f"  [{mark:4s}] {label:52s} {dt:6.2f}s  {script}")
    all_pass = all(ok for _, _, ok, _ in results)
    print("-" * 68)
    if all_pass:
        print(" ALL PASS — 當前 layer stack 收斂到「是真正的 1」")
        print(" 依 AXIOMS.A0: 不主張終局封閉, 此為當前 session receipt.")
    else:
        print(" SOME FAIL — 有殘差在當前 layer stack.")
        print(" 依 AXIOMS.A1: 殘差要記錄不藏. 差 > 抵達 (OMEGA_MAP).")
    sys.exit(0 if all_pass else 1)
