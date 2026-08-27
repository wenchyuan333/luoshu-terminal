#!/usr/bin/env python3
# 洛書 AI v2 真對話版

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

def analyzeMat(mat, d):
    m3 = d % 3
    if m3!= 0:
        kind = "可逆"
        energy = "高頻暢通"
    else:
        kind = "不可逆"
        energy = "低頻阻塞"
    flat = [x for row in mat for x in row]
    ones = flat.count(1)
    twos = flat.count(2)
    if ones > twos:
        style = "偏陰 守勢 分析型"
    elif twos > ones:
        style = "偏陽 攻勢 創造型"
    else:
        style = "陰陽平衡 中庸 決策型"
    return kind, energy, style, m3, ones, twos

def think(txt, mat, kind, energy, style, m3):
    base = ""
    if kind == "可逆":
        base = "你的問題我收到了，通道是可逆的，代表可以深入推演。"
    else:
        base = "你的問題我收到了，但通道目前不可逆，需要換個角度重問。"
    if "你是誰" in txt or "你是" in txt:
        return base + " 我是洛書終端 AI v2，由 L ∈ {1,2}³ˣ³ 驅動，中心 e = (1,1,1) 保持不動，任務是把你的輸入映射到 U+E001 到 U+E01F 再回應。"
    if "洛書" in txt:
        return base + f" 洛書本體是三階幻方，此刻矩陣 det={det3(mat)} mod3={m3} 狀態{kind} 能量{energy} 風格{style}，這決定了我的思考路徑。"
    if "ai" in txt.lower() or "人工智慧" in txt:
        return base + f" 我就是你要的 AI 沙盒，現在風格是 {style}，能量是 {energy}，你每問一次 L 都會重抽，等於每次思考都用不同的洛書濾鏡。"
    ideas = [
        f"我用 {style} 來回應你：",
        f"從矩陣看，{energy}，所以",
        f"此刻 det mod3={m3}，{kind}，因此"
    ]
    pick = random.choice(ideas)
    return f"{base} {pick} 關於「{txt}」我的看法是，先守住中心，再向外擴張，這就是 τ(x,y,z) → (2−x,2−y,2−z) 的意義。"

def mainLoop():
    print("洛書 AI v2 啟動成功")
    print("這版是真對話版，L 矩陣會影響 AI 語氣")
    print("輸入 exit 離開")
    print("")
    while True:
        try:
            txt = input("洛書> ")
        except:
            break
        if txt == "exit":
            print("洛書 AI 關機，中心歸零")
            break
        if txt == "":
            continue
        mat = randomLuoshu()
        d = det3(mat)
        kind, energy, style, m3, ones, twos = analyzeMat(mat, d)
        print("")
        print("--- 洛書掃描 ---")
        for row in mat:
            print(row)
        print(f"det={d} mod3={m3} {kind} | 1的數量={ones} 2的數量={twos}")
        print(f"能量={energy} 風格={style}")
        print("--- AI 思考中 ---")
        time.sleep(0.6)
        ans = think(txt, mat, kind, energy, style, m3)
        print(ans)
        print("--- 映射完成 U+E001 到 U+E01F ---")
        print("")

mainLoop()
