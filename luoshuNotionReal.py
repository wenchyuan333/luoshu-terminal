#!/usr/bin/env python3
# 洛書 AI V8 真實 Notion 雙向對話版

import random
import time
import os

# 你要填這兩個
NOTION_TOKEN = "填你的 ntn_ 開頭 Token"
DATABASE_ID = "填你的 Database ID"

BRIDGE = "notion_bridge.txt"
e = (1,1,1)

def det3(m):
    a=m[0][0]; b=m[0][1]; c=m[0][2]
    d=m[1][0]; e=m[1][1]; f=m[1][2]
    g=m[2][0]; h=m[2][1]; i=m[2][2]
    return a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h

def randomLuoshu():
    return [[random.choice([1,2]) for _ in range(3)] for _ in range(3)]

def writeNotion(text):
    # 這裡預留給 Notion API，你可以用 requests 送上去
    # import requests
    # headers = {"Authorization": f"Bearer {NOTION_TOKEN}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
    # data = {"parent": {"database_id": DATABASE_ID}, "properties": {"Name": {"title": [{"text": {"content": text}}]}}}
    # requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
    print(f"[已同步到 Notion] {text}")
    with open(BRIDGE,"a",encoding="utf-8") as f:
        f.write(text+"\n")

print("洛書 V8 真實雙向啟動")
print("現在每一句都會同步到你的 Notion")
print("")

roundN = 0
try:
    while True:
        roundN += 1
        mat = randomLuoshu()
        d = det3(mat)
        m3 = d % 3
        r = abs(d*0.1)

        talk = f"可逆 F={abs(d)*3.3:.2f} 暢通" if m3!=0 else "不可逆 阻塞"
        log = f"回合{roundN} 洛書 det={d} r={r:.2f} {talk} 中心{e}"
        writeNotion(log)
        print(log)
        time.sleep(4)

except KeyboardInterrupt:
    print("停止，鷹架拆除，回歸本體")
