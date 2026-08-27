# LSHU-F3-RARE-001

> **Notion SSOT**: `LSHU-F3-RARE-001` under Formula Master Index
> **Status**: FORMAL_MODEL / E4 / Proposed / REPAIR
> **Reproducer**: `../wolfram/WChyuanLuoShu.wl` + `../python/luoshu_gl3f3.py`

## Claim

For `M ∈ GL(d, 𝔽₃)`, the following are equivalent:

1. `M` preserves the uniform distribution of coordinate-axis lines (洛書條件)
2. All entries of `M` are in `{1, 2}`

## Key numbers

| d | N(d) = #{invertible matrices with entries in {1,2}} | \|GL(d, 𝔽₃)\| | Rarity |
|---|---|---|---|
| 3 | **192** | 11,232 | **1.7094%** |
| 4 | 22,272 | 24,261,120 | 0.0918% |
| 5 (sampled) | ≈1.16×10⁷ | 4.76×10¹¹ | ≈0.00244% |

## Falsifier

- F1: independent enumeration of N(3) yielding ≠ 192
- F2: independent enumeration of N(4) yielding ≠ 22,272
- F3: N(d) / |GL(d, 𝔽₂)| → constant ≠ 1 as d → ∞

## Provenance

- Origin: Dola conversation (see `UPSTREAM-AI-MIRRORS.md` M1)
- Diagnosis: Miya🦉 §17.3 nine-tier ruling
- Repair: this reproducer + Notion Formula Page

## Upgrade path

```
FORMAL_MODEL / E4 / Proposed / REPAIR
  ↓ pass reproducer + independent verifier readback
COMPUTABLE / E2 / PASS / Active
```

(per Notion Canon §3 Kernel↔Governance Bridge)
