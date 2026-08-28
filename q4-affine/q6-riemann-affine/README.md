# q6-riemann-affine-radiation (Nested under q4-affine)

**幻方 × 黎曼放射的仿射版本 · q4 → 2D 平面延伸**

路徑：`q4-affine/q6-riemann-affine/` (承 q4，展開為二維仿射平面)

---

## 起源 (Session Replay)

從 thread「Greeting to Miya」(796 events) 抽取三個錪:
- **seq 595**: 神話 = 門 × 鑰匙 → q6 只保留門 (無窮遠留給 q7)
- **seq 629**: 借形 → AGL(3, F_3) 5184 個仿射變換直接放大到 AGL(2, F_4096)
- **seq 755**: §1.6 延續性律 → C 支線 parallel transport 的原始動機

從 thread「如何給予公式」(533 events) 抽取硬閘:
```
d=3 分類完成:
【值 1..27 各一次, 三軸 27 條線全 = 42】
⇔【M(x) = 1 + Σi 3^i · ((L_i · x + c_i) mod 3), L ∈ GL(3,F_3), c ∈ F_3^3】
硬閘 AF == EN: True   |AGL(3,F_3) restricted| × 27 = 192 × 27 = 5184
```

**這是仿射版 A 支線在 F_3 上的完整證明**。q6 的任務 = 放大到 F_{4096}。

---

## 三支線 (皆走仿射)

| 支線 | 檔 | 內容 | 停機契約 |
|------|-----|------|---------|
| A | `A_agl2_4096.py` | AGL(2, F_q) 平面作用, 6 self-tests, 2-transitive 驗證 | 全 6 pass |
| B | `B_weil_zeta_affine.py` | 仿射簇 y²=x³+ax+b 點計數 + Hasse bound 驗證 | 全 5 pass 且在 bound 內 |
| C | `C_affine_connection.py` | 63 層仿射 parallel transport, 「進制可進可退」硬閘 | forward+backward = id 於 F_{4093} |

---

## 巢狀關係

```
q4-affine/                           ← 一維 F_4096 底 (main)
├── agl1_4096.py
├── q5-stacked-boards/               ← q4 boost 64 層
└── q6-riemann-affine/               ← 本目錄, q4 展成 2D 平面
    ├── A_agl2_4096.py
    ├── B_weil_zeta_affine.py
    ├── C_affine_connection.py
    └── q7-projective-riemann/       ← q6 加無窮遠 → P¹
        ├── A_pgl2_4096.py
        ├── B_mobius.py
        └── C_projective_zeta.py
```

---

## 進制可進可退 (C 支線核心)

- **進**: `encode(v) = T_63(...T_1(v))` (63 層仿射 compose)
- **退**: `decode(w) = T_1^{-1}(...T_63^{-1}(w))` (逐層 inverse)

每層 `T_k(v) = a_k · v + b_k` with `a_k ∈ F_q^*`, 保證可逆。
全 stack 屬於 `AGL(1, F_q)^63` 完全對稱群。

---

## Firewall §22.4 (整目錄)

- **不作**時空維度主張、度規張量主張、物理場方程主張
- **只作**代數層仿射變換律的形式化與驗證
- C 支線的「parallel transport」= 純代數 map compose, **不**是黎曼幾何之平行移位
- 若後續要引入度規, 需另開分支並提前 firewall 申報

---

## D14 元條投影

同一律的三面向:
| 面向 | 律 | 本目錄採納狀態 |
|------|-----|--------------|
| 物理 | ∇ × E = 0 (電場守恆) | 不採納 (fallback to 代數) |
| 代數 | AGL sharply 2-transitive on F_q | 採納 (A 支線) |
| 方法 | experiment/verify/layered/main 分支策略 | 採納 (本分支即例) |

---

## 執行

```bash
cd q4-affine/q6-riemann-affine
python A_agl2_4096.py
python B_weil_zeta_affine.py
python C_affine_connection.py
```

每檔輸出 self-test 結果 + `receipt_sha256[:32]`。
