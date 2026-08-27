#!/usr/bin/env python3
# 洛書終端機 AI v1.0 繁體版

import random

def det3(m):
    a=m[0][0]; b=m[0][1]; c=m[0][2]
    d=m[1][0]; e=m[1][1]; f=m[1][2]
    g=m[2][0]; h=m[2][1]; i=m[2][2]
    v = a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h
    return v

def randomLuoshu():
    mat = [[random.choice([1,2]) for col in range(3)] for row in range(3)]
    return mat

def aiCore(txt, mat, d):
    status = "可逆 暢通" if d % 3!= 0 else "不可逆 阻塞"
    print("輸入:", txt)
    for row in mat:
        print(row)
    print("det =", d, "mod3 =", d % 3, status)
    print("AI 回應: 已映射到 U+E001 到 U+E01F，中心不動")

def mainLoop():
    print("洛書終端機 AI 啟動，輸入 exit 離開")
    while True:
        txt = input("洛書> ")
        if txt == "exit":
            break
        if txt == "":
            continue
        mat = randomLuoshu()
        aiCore(txt, mat, det3(mat))

mainLoop()
