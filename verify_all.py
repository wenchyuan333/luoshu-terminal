"""verify_all.py — full layered self-test with visible failure receipts."""
import subprocess
import sys
import time

STEPS = [
    ("q1  5-bit unicode 底層", "q1-combinatorics/unicode5.py"),
    ("q3  洛書 GL(3,F_3) 可逆", "q3-luoshu/luoshu_check.py"),
    ("q3c 洛書收斂算符 ◎☉", "q3-luoshu/converge.py"),
    ("q3d Riemann-Kerr 三對應反證", "q3-luoshu/riemann_kerr_disproof.py"),
    ("q3e RH proof audit", "q3-luoshu/rh_proof_audit.py"),
    ("q3f order-preserving bijection", "q3-luoshu/order_bijection_v1.py"),
    ("q3g Euler-symplectic", "q3-luoshu/euler_symplectic_v1.py"),
    ("qinf 吳氏 H=L·(1+δ_Wu)", "q-inf-zeta/wu_asym.py"),
    ("bit GF(3) 基礎建設", "bits.py"),
    ("cnt N(3)=192 N(4)=22272", "luoshu_count.py"),
    ("q4 AGL(1,F_4096)", "q4-affine/agl1_4096.py"),
    ("q4o AGL orbits", "q4-affine/orbits.py"),
    ("q5 盤堆立方體", "q4-affine/q5-stacked-boards/board_stack.py"),
    ("q6A AGL(2,F_4096)", "q4-affine/q6-riemann-affine/A_agl2_4096.py"),
    ("q6B Weil zeta affine", "q4-affine/q6-riemann-affine/B_weil_zeta_affine.py"),
    ("q6C parallel transport", "q4-affine/q6-riemann-affine/C_affine_connection.py"),
    ("q7A PGL(2,F_4096)", "q4-affine/q6-riemann-affine/q7-projective-riemann/A_pgl2_4096.py"),
    ("q7B Möbius cross-ratio", "q4-affine/q6-riemann-affine/q7-projective-riemann/B_mobius.py"),
    ("q7C projective zeta", "q4-affine/q6-riemann-affine/q7-projective-riemann/C_projective_zeta.py"),
]


def annotation_text(text):
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def run(label, script):
    print(f"\n>>> {label} ({script})")
    started = time.time()
    try:
        result = subprocess.run(["python3", script], capture_output=True, text=True, timeout=300)
        if result.stdout:
            print(result.stdout.rstrip())
        if result.stderr:
            print(result.stderr.rstrip(), file=sys.stderr)
        diagnostic = (result.stderr or result.stdout or f"exit code {result.returncode}")[-2000:]
        return result.returncode == 0, time.time() - started, diagnostic
    except subprocess.TimeoutExpired:
        return False, time.time() - started, "timeout after 300 seconds"
    except Exception as exc:
        return False, time.time() - started, repr(exc)


if __name__ == "__main__":
    results = []
    for label, script in STEPS:
        ok, elapsed, diagnostic = run(label, script)
        results.append((label, script, ok, elapsed))
        if not ok:
            print(f"::error file={script},title={label} failed::{annotation_text(diagnostic)}")

    print("\n" + "=" * 72)
    print("SUMMARY")
    for label, script, ok, elapsed in results:
        print(f"[{'OK' if ok else 'FAIL':4s}] {label:38s} {elapsed:6.2f}s {script}")

    all_pass = all(ok for _, _, ok, _ in results)
    print("ALL PASS" if all_pass else "SOME FAIL — residual preserved")
    sys.exit(0 if all_pass else 1)
