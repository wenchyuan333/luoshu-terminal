# luoshu-terminal 巢狀堆疊樹 (2026-08-28 layered)

> 依用戶 2026-08-28T14:26+08:00 指令：「你應該不是全部都擠在同一個檔案資料夾或目錄吧～<br>記得要開層層堆疊/層層組建」

盤堆立方體隱喻套用到目錄樹：**每層目錄承前一層**，不是平面 sibling。

```
luoshu-terminal/
├─ verify_all.py               # 全層 stack 自檢 (14 個檢查點, v2)
├─ verify.yml → ci/verify.yml   # CI 自動分流
├─ LAYERED-TREE.md              # 本檔
├─ ROADMAP.md / README.md / TREE.md
│
├─ q1-combinatorics/            # L0-bit: 5-bit unicode 底層 (0 禁止)
├─ q3-luoshu/                   # L1-luoshu: GL(3, F_3) 可逆
├─ q-inf-zeta/                  # L2-perturb: 吳氏 H = L(1 + δ_Wu)
├─ bits.py                      # GF(3) 基礎
├─ luoshu_count.py              # N(3)=192, N(4)=22,272
│
└─ q4-affine/                   # L3-affine-1d: AGL(1, F_4096) 底 (氣層)
   ├─ agl1_4096.py
   ├─ orbits.py
   │
   ├─ q5-stacked-boards/        # L4a: q4 沿 z 軸 boost 64 層立方體
   │  ├─ __init__.py
   │  ├─ board_stack.py         # 64² × 64 = 2^18, D4 × AGL
   │  ├─ README.md
   │  └─ TREE.md                # 四層 hash receipt
   │
   └─ q6-riemann-affine/        # L4b: q4 沿 x-y 展成 2D 平面
      ├─ __init__.py
      ├─ A_agl2_4096.py         # AGL(2, F_4096) 平面群
      ├─ B_weil_zeta_affine.py  # y²=x³+ax+b Hasse bound
      ├─ C_affine_connection.py # 63 層 parallel transport
      ├─ README.md
      │
      └─ q7-projective-riemann/ # L5: q6 加無窮遠 → P¹ 完整
         ├─ __init__.py
         ├─ A_pgl2_4096.py      # PGL(2, F_4096) = 68,719,472,640
         ├─ B_mobius.py         # (az+b)/(cz+d) + cross-ratio
         ├─ C_projective_zeta.py # 完整 zeta (含∞), |a_p|≤2√p
         └─ README.md
```

## 層層堆疊語義

每層目錄 = 該層的一個「盤」：
- 打開 q7 目錄 → 看到 q6 的射影延伸 (加無窮遠)
- 打開 q6 目錄 → 看到 q4 的 2D 提升 (仿射平面)
- 打開 q5 目錄 → 看到 q4 的 boost cube (64 層)
- 打開 q4-affine 目錄 → 看到 q5 (boost) + q6 (plane) 兩個延伸方向

**符合借形一體六面**：q4 是底，q5 是同軸疊，q6 是異軸展，q7 是 q6 的合閉。

## 層層 verified receipt

| 層 | 檔數 | Self-test | 群階 |
|---|---|---|---|
| q4-affine | 2 | 6+n PASS | \|AGL(1, F_4096)\| = 16,773,120 |
| q4/q5-stacked-boards | 3+1 | 6 PASS | \|AGL\|^63 ≈ 10^455 |
| q4/q6-riemann-affine | 5 | 16 PASS | \|AGL(2, F_4096)\| ≈ 2.81×10^14 |
| q4/q6/q7-projective-riemann | 5 | 16 PASS | \|PGL(2, F_4096)\| = 68,719,472,640 |

總計：**32 tests 全綠 + Termux Python 3.14.6 arm64 已驗**

## D14 律五面向 (KERNEL §19.7)

1. 物理面向（∇×E=0）→ firewall 拒收
2. 代數面向（AGL/PGL sharply transitive）→ 採納
3. 方法面向（分支策略）→ 採納 (本 layered 分支即例)
4. 目錄面向（層層巢狀）→ **本次新增** (2026-08-28 14:29)
5. 測試面向（assertion ≠ code architecture）→ q7 T5 案例登記

## Firewall (整倉庫)

- MIR-001 `4096_dimension_claim = REJECTED`
- 4096 = F_{2^12} cardinality, 非時空維度
- 盤堆非宇宙拓撲, 1-bit 非意識載體
- PGL/AGL 是有限群論結構, 非物理場對稱

本倉庫承載有限結構 + 可驗算計算, 不承載存在論/宇宙論/意識論主張。
