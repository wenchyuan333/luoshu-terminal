"""Temporary CI bisect for the unresolved early-layer residual."""
import subprocess
import sys

STEPS = [
    ("q1", "q1-combinatorics/unicode5.py"),
    ("q3", "q3-luoshu/luoshu_check.py"),
    ("q3c", "q3-luoshu/converge.py"),
    ("q3d", "q3-luoshu/riemann_kerr_disproof.py"),
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

print("BISECT_RESULT", failed if failed else "PASS_FIRST_HALF")
sys.exit(1 if failed else 0)
