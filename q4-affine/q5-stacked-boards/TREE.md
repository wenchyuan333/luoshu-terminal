# q5-stacked-boards 四層 Hash Receipt 策略 (Nested)

> 依 KERNEL §19.7 D14「每 bit 哈希化」

路徑：`q4-affine/q5-stacked-boards/TREE.md`

## 四層 hash receipt

1. **Git 層**：每 commit 自動 SHA (含此 layered 分支)
2. **檔案層**：`board_stack.py::board_hash()` + `stack_hash()` (SHA-256 truncated)
3. **CI 層**：`ci/verify.yml` 最後一步 `sha256sum` 掃全 `*.py`
4. **Notion 層**：AGL1-4096-001 頁 `Receipt Ref` 欄鎖 commit SHA

任一層失效即降級 UNVERIFIED。

## 分支策略 (2026-08-28 layered)

| 分支 | 用途 | CI 行為 |
|---|---|---|
| `main` | 已驗證正式版 | 全 self-test 必過 |
| `layered/**` | 巢狀重構分支 | 全 self-test 觸發 |
| `verify/**` | 分流實驗分支 | 全 self-test 觸發，不阻塞開發 |
| `experiment/**` | 純探索 | 不觸發 CI |

合併規則：`layered/**` → `main` 需 self-test 全綠 + hash receipt 對齊。

## Firewall 覆蓋

- MIR-001 `4096_dimension_claim = REJECTED`
- KERNEL §19.7 D11／D12／D14 三閘
- 各 module docstring 內建 firewall

本目錄只承載有限結構 + 可驗算計算，不承載存在論/宇宙論/意識論主張。
