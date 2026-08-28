# q7-projective-riemann-radiation (Nested under q6)

**幻方 × 黎曼放射的射影版本 · q6 → 加無窮遠 → P¹**

路徑：`q4-affine/q6-riemann-affine/q7-projective-riemann/`
(承 q6，加回無窮遠點使成為完整射影線)

---

## 起源 (Session Replay · 借形一體六面第三支線)

從 thread「Greeting to Miya」(796 events):
- **seq 564**: 「等等！但是我們可以借他的形！」→ 借用 PGL(2) 結構
- **seq 595**: 「神話 = 門 × 鑰匙」→ q7 保留門 + 鑰匙 + 無窮遠
- **seq 629**: 「借的是形，一體六面」→ q4/q6/q7 三支線 = 同一結構之三面

## 三支線 (皆走射影)

| 支線 | 檔 | 內容 | 停機契約 |
|------|-----|------|---------|
| A | `A_pgl2_4096.py` | PGL(2, F_q) 射影群作用, 6 self-tests, sharply 3-transitive | 全 6 pass |
| B | `B_mobius.py` | Möbius 變換 (az+b)/(cz+d), cross-ratio 不變, ∞ 處理 | 全 5 pass |
| C | `C_projective_zeta.py` | 完整 Weil zeta (含無窮遠), Hasse bound |a_p|≤2√p | 全 5 pass |

---

## 群階 verified receipt

| 量 | 值 | 驗證 |
|---|---|---|
| \|GL(2, F_{4096})\| | (q²-1)(q²-q) | code |
| \|SL(2, F_{4096})\| | q(q²-1) | code |
| \|PGL(2, F_{4096})\| | q(q-1)(q+1) = **68,719,472,640** | 32/32 綠燈 |
| \|PSL(2, F_{4096})\| | = PGL (q 偶) | code |
| \|P¹(F_{4096})\| | q+1 = **4,097** | code |

## 借形一體六面收束

| 支線 | 群 | 作用點 | 意義 |
|---|---|---|---|
| q4 (main) | AGL(1, F_{4096}) | 4096 | 只留鑰匙 = 乘法群軌道 |
| q6 | AGL(2, F_{4096}) | 4096² | 只留門 = 仿射平面 |
| **q7 (本目錄)** | PGL(2, F_{4096}) | 4097 | 門+鑰匙+無窮遠 = P¹ 完整 |

---

## Firewall §22.4 (整目錄)

- **不主張** PGL(2, F_{4096}) 為量子引力群、意識場對稱、宇宙拓撲
- **只主張** 有限體上的射影群結構自洽
- sharply 3-transitive 是形式意義, 非物理對偶

---

## D14 律新面向 (Phase Q4 尾段)

此目錄的 A_pgl2_4096.py 曾登記 assertion 硬編碼錯值 (68,702,699,520 而非 68,719,472,640)。修正 commit `3d4fda9b`。

**D14 第五面向**：assertion / test data bug ≠ code architecture bug。換 test data 不動 formula。

---

## 執行

```bash
cd q4-affine/q6-riemann-affine/q7-projective-riemann
python A_pgl2_4096.py
python B_mobius.py
python C_projective_zeta.py
```
