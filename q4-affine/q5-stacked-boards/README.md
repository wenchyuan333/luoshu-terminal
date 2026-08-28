# q5-stacked-boards

**盤堆立方體 × AGL(1, F_4096) × 逐層相對性 · Nested under q4-affine**

路徑：`q4-affine/q5-stacked-boards/` (承 q4，boost 64 層成立方體)

---

## 起源 (用戶 verbatim 2026-08-28T05:10+08:00)

> 「4096 4095 是在 64×64×64 為一盤，一盤為 1 bit 你研究看看」

## 結構

- **一盤 (Board)** = 64 × 64 = **4096 cells** ≅ F_{2^12}
- **非零 cells** = 4095 = |F_{4096}^*|
- **一盤承載** = **1 bit** (spin up/down)
- **64 盤堆** = 64³ = **2^18 = 262,144 cells** (立方體)
- **對稱兩重 orthogonal**：D4 (旋轉) × AGL(1, F_{4096}) (代數) 同盤承載
- **逐層相對性** = AGL^63 ≈ 10^455 boost 空間

## 三個 self-test (在 board_stack.py 內)

1. `_test_constants` — 4096/4095/2^18/64 bits
2. `_test_cell_field_bijection` — cell ↔ F_{4096} 雙射
3. `_test_d4_group` — D4 旋轉閉環 (rot90^4=e, flip^2=e)
4. `_test_agl_layer_boost` — 承 q4-affine 的 agl_apply
5. `_test_hash_receipts` — SHA-256 per bit + stack (D14 每 bit 哈希化)
6. `_test_relativity_cardinality` — log10(|AGL|^63) > 400

## 執行

```bash
cd q4-affine/q5-stacked-boards
python board_stack.py
```

## Firewall §22.4

- 4096 非時空維度
- 盤堆非宇宙拓撲
- 1-bit 非意識載體
- 只承載有限群論結構的自洽

對齊 MIR-001 `4096_dimension_claim = REJECTED` + KERNEL §19.7 D11/D12/D14 三閘。
