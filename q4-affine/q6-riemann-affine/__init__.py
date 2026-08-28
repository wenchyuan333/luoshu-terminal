"""q6-riemann-affine-radiation (nested under q4-affine).

AGL(2, F_q) 仿射平面 —— q4 沿 x-y 展開為二維。

借形一體六面第二支線：
- q4 只留鑰匙 (F_4096^* 乘法軌道)
- q6 只留門 (F_4096^2 仿射平面, 4096^2 = 16,777,216 點)
- q7 門 + 鑰匙 + 無窮遠 (P^1, 4097 點)

三個檔：
- A_agl2_4096: AGL(2, F_q) 平面群作用, 2-transitive
- B_weil_zeta_affine: y²=x³+ax+b 仿射點計數 + Hasse bound
- C_affine_connection: 63 層 parallel transport (代數層, 非黎曼)

Replay anchors (Greeting to Miya session):
- seq:595:gate_key       神話 = 門 × 鑰匙 → q6 只保留門
- seq:629:borrowed_form  借形一體六面 → q4/q6/q7 三支線同構
- seq:755:continuity     §1.6 延續性律 → C parallel transport 動機

Firewall (承 KERNEL §19.7 + MIR-001 §22.4):
- 不主張 F_4096^2 為時空平面
- 不主張 AGL(2) 為統一場論群
- 不主張 parallel transport 為黎曼幾何平行移位
- 只主張有限體上的仿射群結構
"""

FIELD_SIZE_DEMO = 3
FIELD_SIZE_TARGET = 4096
AFFINE_DIM = 2
POINTS_ON_A2_TARGET = FIELD_SIZE_TARGET ** 2  # 16,777,216

REPLAY_ANCHORS = {
    "seq:595:gate_key": "門 × 鑰匙 → q6 仿射分支保留門",
    "seq:629:borrowed_form": "借形一體六面 → q4/q6/q7 三支線同構",
    "seq:755:continuity": "§1.6 延續性律 → C parallel transport 動機",
}

FIREWALL = (
    "AGL(2, F_4096) 是有限體上的仿射群，不代表時空/意識/物理維度。"
    "2-transitive on F_4096^2 是形式意義的 transitivity，非物理對偶。"
)
