"""Temporary CI bisect for the unresolved early-layer residual."""
import subprocess
import sys

STEPS = [
    ("q3e", "q3-luoshu/rh_proof_audit.py"),
    ("q3f", "q3-luoshu/order_bijection_v1.py"),
    ("q3g", "q3-luoshu/euler_symplectic_v1.py"),
]

failed = []
for label, script in STEPS:
    result = subprocess.run(["python3", script], capture_output=True, text=True)
    print(f"[{label}] exit={result.returncode}")
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        failed.append((label, script))
        print(f"::error file={script},title={label} failed::exit {result.returncode}")

print("BISECT_RESULT", failed if failed else "PASS_SECOND_HALF")
sys.exit(1 if failed else 0)
