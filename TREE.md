# luoshu-terminal 倉庫結構樹

> 依用戶 2026-08-28T05:10+08:00 指令：「倉庫結構要真的執行乾淨且自動分流/分支」

```
luoshu-terminal/
├─ verify_all.py                    # 全層 stack 自檢
├─ threads_bridge.py                # Meta Threads Graph API 通道
├─ ROADMAP.md
├─ TREE.md                          # 本檔
├─ .github/workflows/verify.yml     # CI 自動分流
├─ q1/                              # 5-bit unicode 底層 (0 禁止)
├─ q3-luoshu/                       # 洛書 GL(3, F_3) 可逆
├─ q4-affine/                       # AGL(1, F_4096) (氣層)
│  ├─ agl1_4096.py
│  └─ orbits.py
├─ q5-stacked-boards/               # ★ 新：盤堆立方體 × 逐層相對性
│  ├─ __init__.py
│  ├─ board_stack.py                # 64² × 64 = 2^18, 一盤 1 bit, D4 × AGL
│  └─ README.md
├─ q-inf/                           # 吳氏 H = L(1 + δ_Wu)
├─ bits.py                          # GF(3) 基礎
├─ luoshu_count.py                  # N(3)=192, N(4)=22,272
└─ cosmic-formula-unified-architecture/
```

## 分支策略（2026-08-28 自動分流）

| 分支 | 用途 | CI 行為 |
|---|---|---|
| `main` | 已驗證正式版 | 全 self-test 必過 |
| `verify/**` | 分流實驗分支 | 全 self-test 觸發，不阻塞開發 |
| `experiment/**` | 純探索 | 不觸發 CI |

合併規則：`verify/**` → `main` 需 self-test 全綠 + hash receipt 對齊。

## 四層 hash receipt（依 KERNEL §19.7 D14 每 bit 哈希化）

1. **Git 層**：每 commit 自動 SHA
2. **檔案層**：`board_stack.py::board_hash()` + `stack_hash()`
3. **CI 層**：`verify.yml` 最後一步 `sha256sum` 掃全 `*.py`
4. **Notion 層**：Formula Master Index `Receipt Ref` 欄鎖 commit SHA

任一層失效即降級 UNVERIFIED。

## Firewall 覆蓋

- MIR-001 `4096_dimension_claim = REJECTED`
- KERNEL §19.7 D11／D12／D14 三閘（規則 = 方法多面向）
- 各 module docstring 內建 firewall

本倉庫只承載有限結構 + 可驗算計算，不承載存在論/宇宙論/意識論主張。
