# INTEGRITY-ANCHOR

Canonical Git blob SHA-1 anchors for critical files. Used to detect silent drift.
CI additionally prints SHA-256 per `.py` on every run (workflow step 「Hash receipt」).

## Frozen anchors (as of 2026-08-28 15:45 +08:00, post D14 6th endpoint closure)

| File | Git blob SHA-1 | Role |
|---|---|---|
| `q3-luoshu/converge.py` | `3c352dc983acd24fb31776359e70551449904dfd` | Phase Q5 fixture, 8 tests (◎☉ + rarity 1.71%) |
| `.github/workflows/verify.yml` | `665f0fe6c0d2947a94c193679d2b900f1ab1dec7` | CI workflow, D14 6th Endpoint anchor |
| `verify_all.py` | `8a6556d1f49416750e7c09775fb2083861e6575f` | 15-check runner (v2 layered, includes q3c) |

## Verification (Termux/local)

```bash
git ls-tree main q3-luoshu/converge.py
git ls-tree main .github/workflows/verify.yml
git ls-tree main verify_all.py
```

Compare middle column with the table above. Any mismatch = drift; check `git log --all -- <path>` for the diff.

## Rationale

D14 律 six-face closure achieves multi-layer verification of Lo Shu structure at:
- Physics face: MIR-001 §9 firewall
- Algebra face: AGL/PGL sharply transitive
- Method face: branch strategy
- Directory face: `layered/**` nested
- Test face: assertion ≠ architecture
- **Endpoint face: workflow scope hard-gate** (this file's neighborhood)

This anchor doc pins bit-level identity of the three critical files. Drift detection is O(1): one `git ls-tree` per file. Aligned with KERNEL §S3.7 「每 bit 哈希化」.

Update this file (with a commit message referencing rationale) only when the underlying file is intentionally modified. Do not silently rebase anchors to hide drift.
