"""Temporary q3e test-level bisect: A5."""
import runpy
import sys

module = runpy.run_path("q3-luoshu/rh_proof_audit.py", run_name="q3e_probe")
name = "test_klein_four_group_of_functional_equation"
try:
    module[name]()
    print("PASS", name)
    sys.exit(0)
except Exception as exc:
    print("FAIL", name, repr(exc))
    sys.exit(1)
