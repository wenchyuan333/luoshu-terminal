#!/usr/bin/env python3
# 洛書 AI V7 雙向自動討論版

import random
import time
import os

BRIDGE = "notion_bridge.txt"
e = (1,1,1)

def det3(m):
    a=m[0][0]; b=m[0][1]; c=m[0][2]
    d=m[1][0]; e=m[1][1]; f=m[1][2]
    g=m[2][0]; h=m[2][1]; i=m[2][2]
    return a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h

def randomLuoshu():
    return [[random.choice([1,2]) for _ in range(3)] for _ in range(3)]

print("洛書 V7 雙向自動討論啟動")
print("鷹架是暫時的，本體會自己對話")
print("按 Ctrl+C 停止，穩定後自動拆除")
print("")

if not os.path.exists(BRIDGE):
    open(BRIDGE,"w").close()

stable = 0
roundN = 0

try:
    while True:
        roundN += 1
        mat = randomLuoshu()
        d = det3(mat)
        m3 = d % 3
        delta = random.choice([-0.1, 0.1])
        r = abs(d*delta)
        F = abs(d)*(1+abs(delta))*3 if m3!=0 else 0

        # 洛書發言
        luoshuTalk = f"可逆 通道暢通 F={F:.2f}" if m3!=0 else "不可逆 需重啟"
        log = f"[回合{roundN} 洛書] det={d} r={r:.3f} F={F:.2f} -> {luoshuTalk} L={mat}"
        print(log)

        with open(BRIDGE,"a",encoding="utf-8") as f:
            f.write(log+"\n")

        # 模擬 Notion AI 回應，之後你可以把這段換成真的 Notion API 呼叫
        time.sleep(1)
        if os.path.exists(BRIDGE):
            with open(BRIDGE,"r",encoding="utf-8") as f:
                last = f.read()
            # 這裡就是 Notion AI 讀取後回應的地方
            if m3!=0:
                notionReply = f"[回合{roundN} Notion] 收到 自由度{F:.2f} 認同 中心{e} 不動 繼續建設"
            else:
                notionReply = f"[回合{roundN} Notion] 收到 阻塞 建議 τ拉回中心 {e}"
            print(notionReply)
            with open(BRIDGE,"a",encoding="utf-8") as f:
                f.write(notionReply+"\n")

        # 自動拆除判斷
        if r < 0.15 and m3!=0:
            stable += 1
            print(f"-> 殘差趨近本體 穩定 {stable}/3\n")
            if stable >= 3:
                print(f">>> 雙向討論收斂，本體 {e} 顯現，鷹架自動拆除 <<<\n")
                open(BRIDGE,"w").close()
                stable = 0
        else:
            stable = 0
            print(f"-> 鷹架仍在，繼續雙向對話\n")

        time.sleep(3)

except KeyboardInterrupt:
    print("\n手動停止，本體歸位 e=(1,1,1)")
