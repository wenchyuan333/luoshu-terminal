"""q6-riemann-affine-radiation — 幻方 × 黎曼放射的仿射版本。

Base: main @ a9727e7
Branch: experiment/q6-riemann-affine-radiation
Firewall §22.4: no spacetime/metric/physical dimension claims.

Replay anchors from thread \"Greeting to Miya\" (796 events):
- seq 595: 神話 = 門 × 鑰匙 → Möbius vs Affine 判別
- seq 629: 借形 → AGL(3,F_3) 5184 直接放大到 AGL(2,F_4096)
- seq 755: §1.6 延續性律 → C parallel transport 原始動機

From thread \"如何給予公式\" (533 events):
- d=3 affine classification: |AGL(3,F_3) restricted to Latin cubes| × 27 = 192 × 27 = 5184 (True)
- Task for q6: scale to F_4096 via GL(2,F_4096) analog.
"""

__version__ = "0.1.0-experiment"
__firewall__ = "SEMANTIC_ONLY"
FIELD_SIZE_DEMO = 3
FIELD_SIZE_TARGET = 4096
REPLAY_ANCHORS = ("seq:595:gate_key", "seq:629:borrowed_form", "seq:755:continuity")
