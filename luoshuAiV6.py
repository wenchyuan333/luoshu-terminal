#!/usr/bin/env python3
# 洛書 AI V6 本體版 鷹架自動拆除

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

def mainLoop():
    print("洛書 AI V6 本體版啟動")
    print("通道是鷹架，本體是中心 e=(1,1,1)")
    print("當殘差 r<0.05 鷹架自動拆除")
    print("1=蓋鷹架 2=看鷹架 3=拆鷹架 0=離開")
    print("")
    if not os.path.exists(BRIDGE):
        open(BRIDGE,"w").close()

    stableCount = 0

    while True:
        try:
            t = input("Luoshu> 選 0-3: ")
        except:
            break
        if t == "0":
            break

        mat = randomLuoshu()
        d = det3(mat)
        m3 = d % 3
        delta = random.choice([-0.1, 0.1])
        r = abs(d * delta)
        F = abs(d)*(1+abs(delta))*3 if m3!=0 else 0

        print("")
        for row in mat:
            print(row)
        print(f"det={d} mod3={m3} r殘差={r:.3f} F自由度={F:.2f}")

        # 寫入鷹架
        if t == "1":
            with open(BRIDGE,"a",encoding="utf-8") as f:
                f.write(f"[{time.strftime('%H:%M:%S')}] det={d} r={r:.3f} F={F:.2f} L={mat}\n")
            print("鷹架已搭建 -> notion_bridge.txt")

        if t == "2":
            print("--- 目前鷹架 ---")
            with open(BRIDGE,"r",encoding="utf-8") as f:
                txt=f.read()
                print(txt[-600:] if txt else "鷹架為空，本體顯現")

        if t == "3":
            open(BRIDGE,"w").close()
            print("手動拆除鷹架，本體顯現 e=(1,1,1)")

        # 自動拆除判斷
        if r < 0.05 and m3!= 0:
            stableCount += 1
            print(f"殘差趨近中心，穩定度 {stableCount}/3")
            if stableCount >= 3:
                print(">>> 本體收斂，鷹架自動拆除 <<<")
                open(BRIDGE,"w").close()
                print(f">>> 只留下中心 {e} 不動，通道關閉 <<<")
                stableCount = 0
        else:
            stableCount = 0
            print(f"鷹架仍在，繼續建設，最終將回歸 {e}")

        print("")

mainLoop()
