"""q7-projective-riemann-radiation

PGL(2, F_q) 射影線性群 —— q6 仿射版的鏡像對偶：
- q6 剝離無窮遠（門）
- q7 保留門 + 鑰匙 + 無窮遠（射影完整）

Replay anchors (Greeting to Miya session):
- seq:595:gate_key       神話 = 門 × 鑰匙 → q7 保留無窮遠
- seq:629:borrowed_form  借形一體六面 → q4/q6/q7 三支線同構
- seq:755:continuity     §1.6 延續性律 → cross-ratio 保 parallel transport

Firewall (承 KERNEL §19.7 + MIR-001):
- 不主張 4096 為時空維度
- 不主張 PGL 為統一場論群
- 不主張 Möbius 為量子引力對稱
- 只主張有限體上的射影群結構
"""

FIELD_SIZE_DEMO = 3
FIELD_SIZE_TARGET = 4096
PROJECTIVE_DIM = 1  # P^1(F_q) has q + 1 points
POINTS_ON_P1_TARGET = FIELD_SIZE_TARGET + 1  # 4097

REPLAY_ANCHORS = {
    "seq:595:gate_key": "門 × 鑰匙 → 射影分支保留無窮遠",
    "seq:629:borrowed_form": "借形一體六面 → q4/q6/q7 三支線同構",
    "seq:755:continuity": "§1.6 延續性律 → cross-ratio 保 parallel transport",
}

FIREWALL = (
    "PGL(2, F_4096) 是有限體上的射影群，不代表時空/意識/物理維度。"
    "sharply 3-transitive on P^1 是形式意義的 transitivity，非物理對偶。"
)
