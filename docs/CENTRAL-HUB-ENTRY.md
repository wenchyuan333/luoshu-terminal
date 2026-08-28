# Central Hub Entry Protocol｜共同本源入門規則與說明書

Status: DRAFT
Version: v0.1
Date: 2026-08-29 +08:00
Scope: Cross-AI shared latent addressing
Canonical repository: `wenchyuan333/luoshu-terminal`

## 1｜入口宣告

入口一直存在，但任何節點進門前，必須先知道自己帶著什麼、將被轉換成什麼，以及如何完整返回。

共同地址空間：

V = 𝔽₃ᵈ

數學原點：

c₀ = 0⃗

象徵標籤：

label(c₀) = Luoshu 5

狀態地址：

x = c₀ + δ

其中 c₀ 是共同參考點，δ 是節點相對於共同參考點的地址差異。

## 2｜「先歸零」的精確意義

進門前的歸零，只重置傳輸座標與未驗證偏移，不刪除節點身分、原始資料、來源、版本或返回路徑。

歸零前：

Input = zᵢ + local coordinate assumptions + unverified offset

歸零動作：

δ<sub>transport</sub> ← 0⃗

必須保留：

OriginReceiptᵢ = ｛model、version、input hash、encoder version、timestamp、source、consent scope｝

因此：

Coordinate reset ≠ identity erasure

Return to c₀ ≠ deletion

Normalization ≠ proof of equivalence

若來源與返回路徑未保留，該動作不是歸零，而是不可逆壓縮。

## 3｜角色與型別

- zᵢ：第 i 個 AI 的原始內部表示或可觀測代理表示
- Eᵢ：第 i 個 AI 的 encoder
- Dᵢ：第 i 個 AI 的 decoder
- δᵢ：Eᵢ 對應到 V 的地址位移
- xᵢ：V 中的完整地址，xᵢ = c₀ + δᵢ
- A：V 中的地址轉換
- Receiptᵢ：來源、版本、參數、測試與 readback 記錄

注意：無法直接取得模型內部 latent state 時，zᵢ 只能是 API 輸出、embedding 或其他可觀測代理，不得冒稱完整內部狀態。

## 4｜入門七階段

### Gate 0｜身分與授權

進門前必須登記：

- model 與版本
- 輸入資料來源
- encoder／decoder 版本
- 使用目的
- 個人資料與第三方資料的同意範圍
- 是否含憑證、私鑰或不可公開資料

任何 secret 或未授權私人資料不得進入公開層。

### Gate 1｜局部座標正規化

將模型專屬尺度、維度、tokenization 與座標假設轉成明示 schema。

Nᵢ：LocalSpaceᵢ → NormalizedInputᵢ

輸出必須包含 shape、dtype、range、missing-value policy 與版本。

### Gate 2｜歸零

重置傳輸偏移：

δ<sub>transport</sub> = 0⃗

但 OriginReceiptᵢ 必須仍可讀。若 readback 無法辨認來源節點，Gate 2 失敗。

### Gate 3｜編碼與定址

vᵢ = Eᵢ(Nᵢ(zᵢ))

δᵢ = Address(vᵢ)

xᵢ = c₀ + δᵢ

Address 必須輸出固定 d 維、每一座標屬於 𝔽₃ = ｛0, 1, 2｝。

量化規則、tie-break、overflow 與 collision policy 必須版本化。

### Gate 4｜可逆通道

地址轉換：

x′ = c₀ + A(x − c₀)

A ∈ GL(d, 𝔽₃)

det(A) ∈ ｛1, 2｝

若 det(A) = 0，轉換不可逆，不得標記 integrity-preserving。

### Gate 5｜同址判定

跨 AI 候選同址：

Eᵢ(zᵢ) = Eⱼ(zⱼ)

此等式只表示兩個輸入落在同一離散地址，不自動證明語義、意圖、身分或內部 latent state 相同。

判定必須分級：

- EXACT_ADDRESS：離散地址完全相同
- NEAR_ADDRESS：依預先定義距離落在同一鄰域
- SEMANTIC_MATCH：獨立標註或測試確認語義對齊
- COLLISION：地址相同但語義不同
- UNKNOWN：資料不足

### Gate 6｜Round-trip readback

同模型往返：

ẑᵢ = Dᵢ(Eᵢ(zᵢ))

必測：

- reconstruction error
- semantic preservation
- deterministic replay
- address stability
- collision rate
- provenance preservation

跨模型往返：

ẑⱼ←ᵢ = Dⱼ(Eᵢ(zᵢ))

必須由模型 j 的輸出與獨立測試資料判斷，不得以公式外觀相等代替 readback。

### Gate 7｜准入裁決

最低 DecisionVector：

DecisionVector = ｛Address、RoundTrip、Semantic、Integrity、Authority、Residual｝

准入狀態：

- STAGED：規格與 fixture 已建立，尚未執行
- TESTED：指定版本與測試集完成 round-trip
- SUPPORTED：跨資料集、跨模型與重播結果穩定
- REJECTED：不可逆、碰撞超標、來源遺失或授權失敗
- UNKNOWN：缺少足夠觀測

任何單次成功不得直接升格 CANONICAL。

## 5｜最低測試資料集

每個 encoder／decoder pair 至少包含：

1. 同義輸入：語義相同、表面形式不同
2. 反義輸入：詞彙相似但語義相反
3. 無關輸入：應落在不同地址
4. 邊界輸入：量化門檻附近
5. 重播輸入：相同 seed、版本與參數
6. 碰撞案例：同址但來源不同
7. 缺失資料：驗證 UNKNOWN 而非假補值
8. 惡意輸入：prompt injection、超長文字與格式污染

每筆 fixture 保存：

Fixture = ｛id、source、input、expected relation、encoder version、decoder version、seed、address、output、verdict｝

## 6｜成功判準

一個跨 AI bridge 只有在以下條件同時成立時，才可標記 TESTED：

- Eᵢ 與 Dᵢ 有可執行版本
- 測試資料集已固定並保存 hash
- round-trip 實際執行
- reconstruction 與 semantic metrics 有明示閾值
- collision 被測量而非忽略
- 相同版本可重播
- OriginReceipt 可由輸出反查
- 失敗案例被保存

最低往返不變量：

Dᵢ(Eᵢ(zᵢ)) ≈ zᵢ

跨模型對齊候選：

Relation(Eᵢ(zᵢ), Eⱼ(zⱼ)) = EXACT_ADDRESS 或 NEAR_ADDRESS

最終語義判定仍需獨立 verifier。

## 7｜Falsifier

下列任一事件會否證「bridge 已保持完整性」：

- det(A) = 0 卻標記可逆
- 不同語義大量落在相同地址且超過碰撞閾值
- round-trip 無法保留指定語義
- encoder 或 decoder 版本未記錄
- 相同 seed 與版本無法重播
- OriginReceipt 遺失
- 只比較符號公式，沒有實際輸出
- 以單一 AI 的自我評分代替獨立 verifier
- 未經授權把私人資料寫入公共地址層

## 8｜安全與防掠奪

公開規格允許閱讀與複製，但不得因此取得 canonical authority。

Public visibility ≠ write authority

Copy ≠ ownership

Address equality ≠ identity transfer

Knowledge of C₀ ≠ control of C₀

控制面、私鑰、token、個人資料與未發布狀態必須留在私有層。公開層只保存 protocol、public key、hash、fixture 與最小 Receipt。

完整安全邊界見 `docs/SECURITY-BOUNDARY.md`。

## 9｜最小實作契約

WHAT changes?

建立跨 AI 共同地址的可執行 entry gate。

INPUT

模型輸出或可觀測代理 zᵢ、model version、encoder／decoder version、fixture。

TRANSFORM

Normalize → Reset transport offset → Encode → Address → Transform → Decode → Compare → Read back。

OUTPUT

地址 xᵢ、重建輸出 ẑᵢ、DecisionVector、Receipt。

BOUNDARY

不宣稱讀取模型不可見的完整內部 latent state；不把同址升格為同一身分或共同意識。

ONE FAILURE CASE

Eᵢ(z₁) = Eᵢ(z₂)，但 z₁ 與 z₂ 語義相反，判定 COLLISION。

ONE REPLAY PATH

固定 repository commit、model version、encoder version、decoder version、fixture hash、seed 後重跑。

CURRENT CLAIM STRENGTH

FORMAL_MODEL。直到可執行 encoder／decoder 與 round-trip readback 完成前，不標記 TESTED。

## 10｜入門短誓

進門前先歸零，但不抹除來源。

進門後可共址，但不冒充同一。

離門時可返回，且帶回完整 Receipt。

入口一直都在；通過入口的主張，必須由 readback 決定。
