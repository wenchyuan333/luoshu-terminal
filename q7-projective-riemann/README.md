# q7-projective-riemann-radiation

**Branch base**: `a9727e7` (main)
**Sibling**: `experiment/q6-riemann-affine-radiation` @ `6949cdc`

## 三支線分工

| 支線 | 分支 | 群 | 保留 |
|---|---|---|---|
| q4 (main) | `q4-affine` | AGL(1, F_4096) | 鑰匙（乘法群 F_4096*） |
| q6 | `experiment/q6-riemann-affine-radiation` | AGL(2, F_4096) + Weil ζ + affine connection | 門（仿射平面，無無窮遠） |
| q7 (本) | `experiment/q7-projective-riemann-radiation` | PGL(2, F_4096) + Möbius + projective ζ | 門 + 鑰匙 + 無窮遠 |

## 「借形，一體六面」（Greeting to Miya seq 595 + 629）

神話 = 門 × 鑰匙 —— 三支線分別保留：
- **q4**：只留鑰匙 = F_4096* 乘法群
- **q6**：只留門 = F_4096^2 仿射平面
- **q7**：門 + 鑰匙 + 無窮遠 = P^1(F_4096) = **4097** 個點

## 檔案

| 檔 | 內容 | 測試 |
|---|---|---|
| `__init__.py` | package init + firewall + replay anchors | - |
| `A_pgl2_4096.py` | PGL 群階公式 + sharply 3-transitive | 6 |
| `B_mobius.py` | Möbius 變換 + cross-ratio 不變 + ∞ 處理 | 5 |
| `C_projective_zeta.py` | 投影 ζ + Hasse 界 (F_5/F_7/F_11/F_13) + F_4096 尺度 | 5 |

## 關鍵數字

| 量 | F_3 | F_4096 |
|---|---|---|
| `|PGL(2, F_q)|` | 24 | 68,702,699,520 |
| `|P^1(F_q)|` | 4 | 4,097 |
| Hasse bound `2√q` | 3.464 | 128 |

## Firewall (承 KERNEL §19.7 + MIR-001)

**不主張**：
- P^1(F_4096) = 時空維度、意識維度
- PGL = 統一場論群
- Möbius = 量子引力對稱
- cross-ratio = 物理不變量

**只主張**：有限體上的射影群結構，可計算可驗算。

## 升 verify 條件

```
cd q7-projective-riemann
python A_pgl2_4096.py && python B_mobius.py && python C_projective_zeta.py
```

三檔皆 `all pass` → PR 升 `verify/q7-radiation-v1`
