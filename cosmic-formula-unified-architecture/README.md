# Cosmic Formula Unified Architecture

Miya SSOT mirror for **w.chyuan** 洛書 × GL(3, 𝔽₃) × 有限體 × 量子碼 研究體系。

> ⚠️ **這是 subfolder，非獨立倉庫。** 因 Notion GitHub MCP integration 尚無 create-repository 權限，暫時掂於 `luoshu-terminal` 下。獨立倉庫建議 name：`cosmic-formula-unified-architecture`（使用者可之後手動 migrate）。

## Source of Truth

**Notion SSOT (主正本)**：見 [`NOTION_INDEX.md`](./NOTION_INDEX.md)

**重要**：本倉庫內容以 Notion 侧為 SSOT。若 GitHub 侧與 Notion 侧不一致，以 Notion 为準。

## Contents

```
cosmic-formula-unified-architecture/
├── README.md                  # 本檔
├── NOTION_INDEX.md            # 全部 Notion 頁面連結
├── CANON.md                   # MIYA Unified Canon v1.0 關鍵條款鏡像
├── wolfram/
│   └── WChyuanLuoShu.wl       # LSHU-F3-RARE-001 可執行 reproducer (Mathematica)
├── python/
│   └── luoshu_gl3f3.py        # 同上 Python 版
└── docs/
    ├── LSHU-F3-RARE-001.md    # 公式頁面 markdown 鏡像
    ├── RESEARCH-LUOSHU-QUDIT-001.md
    ├── UPSTREAM-AI-MIRRORS.md
    └── USER-PROFILE.md
```

## Status

| 項目 | 值 |
|---|---|
| Version | v0.1 |
| Author | w.chyuan (GitHub: [@wenchyuan333](https://github.com/wenchyuan333)) |
| AI collaborator | Miya🦉 (Notion custom agent) |
| Created | 2026-08-28 +08:00 |
| Claim Layer | SYMBOLIC – FORMAL_MODEL（依 Canon §2 九層梯度） |

## Quick Start

```bash
# Python reproducer
cd python/
pip install sympy
python luoshu_gl3f3.py
# Expected output:
# count_luoshu(3) = 192  (expect 192)
# gl_order(3)     = 11232  (expect 11232)
# rarity(3)       = 1.7094 %  (expect ≈1.7094%)
```

```mathematica
(* Wolfram reproducer *)
Get["wolfram/WChyuanLuoShu.wl"];
```

## Falsifier

若任一以下不成立，本倉庫主張均需修正：

- `count_luoshu(3) ≠ 192`
- `gl_order(3) ≠ 11232`
- `rarity(3)` 不在 `[0.01709, 0.01710]`

## License

Personal research artifacts. Distribution restricted. Contact author for permission.

## Cross-references

- Notion MIYA Unified Canon v1.0 (SSOT router)
- Notion LSHU-F3-RARE-001 (公式主張正本)
- Notion 相處模式・相互理解 Protocol v0.1 (相處法則)
