# Branch Protection Setup (Manual, one-time)

GitHub API token available to Miya lacks admin scope; branch protection must be set once via the web UI.

## Steps

1. Open https://github.com/wenchyuan333/luoshu-terminal/settings/branches
2. Click **Add branch ruleset** (or classic **Add branch protection rule**)
3. Rule name: `main-protection`
4. Target branches: `main`
5. Enable:
   - [x] **Require a pull request before merging** (optional for solo repo, keep off if you push directly)
   - [x] **Require status checks to pass before merging**
     - Required check: `self-test` (from `verify_all` workflow)
   - [x] **Require branches to be up to date before merging**
   - [x] **Do not allow bypassing the above settings** (self-lock, prevents accidental force-push override)
6. Save

## 4-Layer defense-in-depth (防誤保護)

| Layer | Where | Catches |
|---|---|---|
| **1. CI self-test** | `.github/workflows/verify.yml` | Broken code on any push, all branches (15 checks + SHA-256 receipt) |
| **2. Pre-push hook** | `hooks/pre-push` (install locally) | Broken code **before** it hits remote |
| **3. Integrity anchor** | `INTEGRITY-ANCHOR.md` | Silent drift on critical files (Git blob SHA-1 pins) |
| **4. Branch protection** | GitHub settings (this doc) | Bypass of layers 1–3 via force-push / bad merge |

## Alignment

- Layer 1 = D14 律 第六面向 Endpoint (already active @ commit `f70f7aa`)
- Layer 2 = Termux 側本地防御 (呼應 §12 Level C 直接執行 credentials 在 user 手)
- Layer 3 = KERNEL §S3.7 「每 bit 哈希化」自動化層
- Layer 4 = 側翼镈枕, 防止 admin 權限自己路過前三層

四層共同 = 信任公理。同一錯要同時穿透四層才會漏，實際上 = 0。

## Non-goals

- Not preventing intentional deletion of the repo (that's the user's sovereign right)
- Not preventing pre-push bypass (`git push --no-verify` still works, but leaves accountability trail on CI)
- Not preventing typo commits (those go through, but CI fails visibly)
