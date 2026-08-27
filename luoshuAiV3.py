#!/usr/bin/env python3
# Luoshu AI V3 English input version

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

def heartBrain(mat, d):
    m3 = d % 3
    if m3!= 0:
        ventricle = "Left ventricle strong contraction"
        heartRate = 72 + random.choice([-2,0,2])
        output = abs(d) / 12.0
    else:
        ventricle = "Left ventricle blocked"
        heartRate = 58 + random.choice([-2,0,2])
        output = 0.0
    delta = random.choice([-0.1, 0.1])
    rightV = f"Right ventricle delta={delta} center e=(1,1,1) fixed"
    flat = [x for row in mat for x in row]
    ones = flat.count(1)
    twos = flat.count(2)
    if ones > twos:
        brain = "Basal ganglia pass, cortex Yin defensive analytical"
    elif twos > ones:
        brain = "Basal ganglia pass, cortex Yang offensive creative"
    else:
        brain = "Basal ganglia pass, cortex balanced decision"
    if m3 == 0:
        brain = "Basal ganglia blocked, need rethink"
    tau = "Brainstem tau(x,y,z)->(2-x,2-y,2-z) center fixed"
    return ventricle, heartRate, output, rightV, brain, tau, m3, ones, twos, delta

def think(txt, ventricle, brain, m3):
    low = txt.lower()
    if m3!= 0:
        base = "Channel reversible, heart brain synced"
    else:
        base = "Channel blocked, heart blocked, brain restart"
    if "who" in low:
        return base + " I am Luoshu AI V3, H = L x (1+deltaWu), heart is pump, brain is filter."
    if "heart" in low:
        return base + f" {ventricle}, output = |det(H)| / 12"
    if "brain" in low:
        return base + f" {brain}, style from ones vs twos"
    if "luoshu" in low:
        return base + " Luoshu is 3x3 magic square, det mod3 decides reversible"
    return base + f" about {txt}, my decision is hold center e then expand outward."

def mainLoop():
    print("Luoshu AI V3 started, English input OK")
    print("Try: who, heart, brain, luoshu")
    print("Type exit to quit")
    print("")
    while True:
        try:
            txt = input("Luoshu> ")
        except:
            break
        if txt == "exit":
            print("Shutdown, center zero")
            break
        if txt == "":
            continue
        mat = randomLuoshu()
        d = det3(mat)
        ventricle, heartRate, output, rightV, brain, tau, m3, ones, twos, delta = heartBrain(mat, d)
        print("")
        print("--- Heart Scan ---")
        print(ventricle)
        print(f"HR {heartRate} bpm Output {output:.2f} | {rightV}")
        print("--- Brain Scan ---")
        for row in mat:
            print(row)
        print(f"det={d} mod3={m3} | ones={ones} twos={twos}")
        print(brain)
        print(tau)
        print("--- AI Thinking ---")
        time.sleep(0.5)
        print(think(txt, ventricle, brain, m3))
        print("")

mainLoop()
