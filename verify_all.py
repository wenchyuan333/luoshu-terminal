"""Temporary q3e test-level bisect: canonical tests A1–A6."""
import runpy
import sys

module = runpy.run_path("q3-luoshu/rh_proof_audit.py", run_name="q3e_probe")
tests = [
    "test_lo_shu_row_col_diag_sums_15",
    "test_lo_shu_pair_sums_10_and_center_5",
    "test_gl3_f3_order",
    "test_F3_axioms",
    "test_klein_four_group_of_functional_equation",
    "test_functional_equation_averages_sigma_to_half",
]

failed = []
for name in tests:
    try:
        module[name]()
        print("PASS", name)
    except Exception as exc:
        failed.append(name)
        print("FAIL", name, repr(exc))

print("Q3E_A_RESULT", failed if failed else "PASS")
sys.exit(1 if failed else 0)
