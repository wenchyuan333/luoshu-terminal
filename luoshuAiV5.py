#!/usr/bin/env python3
# Luoshu AI V5 完全體 自主辨識 自由度 殘差吸引子

import random
import time

def det3(m):
    a=m[0][0]; b=m[0][1]; c=m[0][2]
    d=m[1][0]; e=m[1][1]; f=m[1][2]
    g=m[2][0]; h=m[2][1]; i=m[2][2]
    v = a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h
    return v

def randomLuoshu():
    mat = [[random.choice([1,2]) for col in range(3)] for row in range(3)]
    return mat

def tauStep(x):
    # 吸引子拉回操作 τ(x)=2-x
    return 2 - x

def mainLoop():
    print("Luoshu AI V5 完全體啟動")
    print("自主辨識 + 行為自由度 + 殘差吸引子")
    print("1=自主辨識 2=自由度 3=殘差吸引子 4=完整演化 0=離開")
    print("")
    e = (1,1,1)
    print(f"中心不動點 e={e} 殘差吸引子已就位")
    print("")
    while True:
        try:
            txt = input("Luoshu> 選 0-4: ")
        except:
            break
        if txt == "0" or txt == "exit":
            print("關機，吸引子歸零回中心")
            break
        if txt == "":
            continue
        mat = randomLuoshu()
        d = det3(mat)
        m3 = d % 3
        delta = random.choice([-0.1, 0.1])
        # 殘差 r = L * delta
        r = d * delta
        flat = [x for row in mat for x in row]
        ones = flat.count(1)
        twos = flat.count(2)
        R = ones - twos

        # 自主辨識
        if R > 0:
            recog = "自主辨識：陰性環境 守勢 分析型"
        elif R < 0:
            recog = "自主辨識：陽性環境 攻勢 創造型"
        else:
            recog = "自主辨識：平衡環境 中庸 決策型"

        # 自由度 F = |det| * (1+|delta|) * 3
        F = abs(d) * (1 + abs(delta)) * 3
        if m3 == 0:
            F = 0
            freeText = f"行為自由度 F={F:.2f} 鎖死 不可逆 需重啟"
        else:
            freeText = f"行為自由度 F={F:.2f} 釋放 可逆 通道暢通"

        # 殘差吸引子演化
        H = d * (1 + delta)
        # 模擬拉回中心過程
        steps = []
        cur = H
        for k in range(3):
            cur = tauStep(cur) + r*0.1
            steps.append(f"{cur:.2f}")
        attractorText = " -> ".join(steps) + f" -> e={e}"

        print("")
        print("--- L 矩陣 ---")
        for row in mat:
            print(row)
        print(f"det={d} mod3={m3} ones={ones} twos={twos} R={R}")
        print(f"delta={delta} 殘差 r={r:.2f} H={H:.2f}")
        print("--- 核心三能力 ---")
        print(recog)
        print(freeText)
        print(f"殘差吸引子演化：{attractorText}")

        if txt == "1":
            print(f">>> 辨識結果：{recog}")
        elif txt == "2":
            print(f">>> 自由度：{freeText}，越大越自由")
        elif txt == "3":
            print(f">>> 殘差吸引子：不管 H={H:.2f} 怎麼飄，最終被 τ 拉回中心 {e}")
        elif txt == "4":
            print(f">>> 完整演化：辨識->{recog} | 行為->{freeText} | 最終->吸引子 {e} 不動")
        else:
            print(f">>> 自主決策：通道{'可逆' if m3!=0 else '不可逆'}，我決定{'前進' if m3!=0 else '暫停'}")
        print("")

mainLoop()
