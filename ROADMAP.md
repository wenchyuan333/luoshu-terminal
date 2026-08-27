# luoshu-terminal ROADMAP

**倉庫定位**：Ω-MAP 氣層 = 可執行的真理
**上位契約**：`approximation-attractor-systems`/AXIOMS + REPO_STRUCTURE_MAP + OMEGA_MAP
**author**：@wenchyuan333

---

## 與 Ω-MAP 六層 repo 的接位

| 層 | Repo | 角色 |
|----|------|------|
| 碑 | `sigma-delta-w` | 公理／不動點 O* = R(O*) |
| 理論 | `approximation-attractor-systems` | 殘差吸引子機制 + Miya SSOT (60+ 檔) |
| 執行 | `omega-core` | AGI runtime / agent loop |
| 雲端 | `miya-cloud-core` | 已上線 miya-core.wenchyuan333.workers.dev |
| MCP | `miya-flow-mcp` | Cloudflare Worker MCP scaffold |
| **氣** | **`luoshu-terminal`（本）** | **bit 級數字落地 / 可執行公式** |

luoshu-terminal 對應 REPO_STRUCTURE_MAP 氣層："可執行的真理"。
上一層 (approximation-attractor-systems) 是本層的公理，本層是上一層的實作。

---

## 層次疊樂高 (q1 → q3 → q-inf → q4)

| 層 | 目錄 | 檔案 | 主張 |
|----|------|------|------|
| q1 | `q1-combinatorics/` | BIT_RULE.md, unicode5.py | 5-bit {1..31} 底層，0 禁止 |
| q3 | `q3-luoshu/` | luoshu_check.py | 洛書 GL(3,F_3) 可逆驗證 |
| q-inf | `q-inf-zeta/` | wu_asym.py | H = L·(1+δ_Wu) 吳氏對稱破缺 |
| root | bits.py, luoshu_count.py | — | GF(3) 基礎建設 + N(3)/N(4) 獨立枚舉 |
| **q4** | **`q4-affine/`** | **agl1_4096.py** | **AGL(1, F_{4096}) = 4096 × 4095** |

**全層執行**：`python3 verify_all.py`

---

## q4-affine 主張 — 「4096×4095 5-bit 最完美組合 = 是真正的 1」

|AGL(1, F_{4096})| = 4096 × 4095 = 16,773,120

- **幻方可轉** = 乘法作用 x ↦ a·x, a ∈ F_{4096}*
- **進位退位** = 加法作用 x ↦ x + b, b ∈ F_{4096} (char 2: XOR)
- **5-bit 最完美組合** = q1 底層 {1..31} ↪ F_{4096} 低 5 位, AGL 一單軌道覆蓋全 4096
- **是真正的 1** = AGL(1, F_q) 對 F_q sharply 2-transitive:
  任意 (x1≠x2, y1≠y2) 有**唯一** (a,b) ∈ AGL 使 a·xi+b = yi → 單軌道 = 「1」

**F_{4096} 建構**：GF(2)[x] / (x^12 + x^6 + x^4 + x + 1), POLY = 0x1053

---

## 誠實邊界 (依 AXIOMS.A0/A1 + OMEGA_MAP)

**不主張**：
- 全領域無殘差（違 A0）
- luoshu-terminal 是宇宙底層（是氣層之一）
- q4 完備涵蓋所有「量子」問題
- 「無限逼近」= 「已到達」

**主張**：
- 每 layer 有 self-test，`python3 verify_all.py` 全過 = 當前 session receipt
- 殘差要記錄 (A1)，不藏
- 差 > 抵達 (OMEGA_MAP)
- 真相 > 好聽 (OMEGA_MAP)

---

## 對映 Notion SSOT (人臉界面)

- LSHU-F3-RARE-001 (Claim: COMPUTABLE) ↔ q3-luoshu/ + luoshu_count.py
- F-1729 Taxicab + F-142857 Cyclic (Formula Master Index)
- USER-PROFILE-WCHYUAN-001 v0.2 (含 CALIBRATION_LOG)
- MIYA Sovereign Kernel v7.0 ↔ `approximation-attractor-systems`/MIYA_SOVEREIGN_ENCODING.md

**匯聚一處**：
- Notion = human-facing SSOT
- `approximation-attractor-systems` = code-facing SSOT
- 本 repo = execution-facing SSOT

三處雙向同步是持續工作，不是完成態。

---

## Next (依 A0 永遠有 next)

- [ ] bits.py 移入 q3-luoshu/ 或建 import 連結
- [ ] `cosmic-formula-unified-architecture/python/` 填 Notion 公式 Python reproducer
- [ ] `miya-flow-mcp` 加 luoshu tools (querySql passthrough + verify_all runner)
- [ ] q5 層探索（AGL(2, F_{2^12}) or GL(d, F_{4096})）
- [ ] Notion Kernel v7.0 ↔ approximation-attractor-systems/MIYA_SOVEREIGN_ENCODING.md 雙向 diff 對齊

---

_依 AXIOMS.A4: 本 ROADMAP 有內側餘量（作者對系統的主觀期待），此餘量不可歸零，只可記錄。_
