# q5-stacked-boards ｜ 幻方盤堆立方體 × AGL 逐層相對性

> 依用戶 2026-08-28T05:10+08:00 指令：「4096 4095 是在 64×64×64 為一盤，一盤為 1 bit」

## 核心結構

| 量 | 數值 | 意義 |
|---|---:|---|
| 一盤邊長 | 64 | 2D lattice |
| 一盤 cells | 64² = **4096** | ≅ F_{2^12} 有限體元素 |
| 一盤非零 cells | **4095** | = \|F_{4096}^*\| |
| 一盤承載 | **1 bit** | spin up / spin down |
| stack 層數 | 64 | 64 個盤堆疊 |
| 全 cube cells | 64³ = **262,144** | = 2^18 |
| 全 stack bits | 64 | 唯一 64-bit spin pattern |

## 兩重對稱（同盤 orthogonal 承載）

| 對稱 | 作用域 | 群階 |
|---|---|---:|
| **D4 幻方旋轉** | 2D lattice geometry (row, col) | 8 |
| **AGL(1, F_{4096}) 仿射** | F_{4096} 元素代碼 (12-bit) | 16,773,120 |

D4 作用在整數座標，AGL 作用在有限體元素代碼。兩者 orthogonal，同盤同時承載，互不干涉。

## 逐層相對性

相鄰盤 k, k+1 由 AGL 元素 g_k = (a_k, b_k) 連接：

```
x_{k+1} = a_k · x_k + b_k   (in F_{4096})
```

全 stack 相對變換空間 = |AGL|^{63} ≈ 10^{455}。
**保證**：sharply 2-transitive 結構在整堆立方體逐層不變。

## 每 bit hash 化（KERNEL §19.7 D14）

- `board_hash(board_id, spin_bit)` → SHA-256[:16]
- `stack_hash(spin_pattern)` → SHA-256[:32]

## Self-test

```bash
python q5-stacked-boards/board_stack.py
```

CI 自動：push 到 `main` 或 `verify/**` 觸發 `.github/workflows/verify.yml`。

## Firewall（依 MIR-001 + KERNEL §19.7）

- 4096 = F_{2^12} cardinality，**非時空維度**
- 盤堆 = 有限群作用容器，**非宇宙拓撲**
- 一盤 = 1 bit **非意識載體**
- 全 stack ≠ 統一場論
