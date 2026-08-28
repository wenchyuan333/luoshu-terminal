"""Temporary CI isolation for q3e."""
import subprocess
import sys

label = "q3e"
script = "q3-luoshu/rh_proof_audit.py"
result = subprocess.run(["python3", script], capture_output=True, text=True)
print(f"[{label}] exit={result.returncode}")
if result.stdout:
    print(result.stdout)
if result.stderr:
    print(result.stderr, file=sys.stderr)
if result.returncode != 0:
    print(f"::error file={script},title={label} failed::exit {result.returncode}")
sys.exit(result.returncode)
