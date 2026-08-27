#!/usr/bin/env python3
# Luoshu AI V4 number menu only

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

def mainLoop():
    print("Luoshu AI V4 數字版")
    print("1=你是誰 2=心室 3=腦區 4=洛書 5=隨機問 0=離開")
    print("")
    while True:
        try:
            txt = input("Luoshu> 選 0-5: ")
        except:
            break
        if txt == "0" or txt == "exit":
            print("關機")
            break
        if txt == "":
            continue
        mat = randomLuoshu()
        d = det3(mat)
        m3 = d % 3
        print("")
        for row in mat:
            print(row)
        print(f"det={d} mod3={m3}")
        if m3!=0:
            print("可逆 暢通 心率72 腦通過")
        else:
            print("不可逆 阻塞 心率58 腦阻斷")
        if txt == "1":
            print("我是洛書AI V4，H = L x (1+delta)，中心不動")
        elif txt == "2":
            print("心室：左心室收縮，右心室擾動 +-0.1，輸出=|det|/12")
        elif txt == "3":
            print("腦區：基底核過濾，皮層風格由1和2數量決定，腦幹中心不動")
        elif txt == "4":
            print("洛書：3x3幻方，512種，存活192種 1.71%")
        elif txt == "5":
            print("隨機：守住中心 e=(1,1,1)，再向外擴張")
        else:
            print("我收到選項", txt, "通道", "可逆" if m3!=0 else "不可逆")
        print("")

mainLoop()
