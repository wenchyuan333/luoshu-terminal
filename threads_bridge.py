# -*- coding: utf-8 -*-
"""
threads_bridge.py — Threads Graph API 官方通道 (Miya x w.chyuan)

依 MIYA_MUST_NOT §12 三級:
  Level A (代登/接管 session)  -> hardstop, 不做
  Level B (公開內容讀取)        -> web.loadPage 已能, 但 Threads JS-render 常擋
  Level C (造通道, 幫使用者建 API 腳本) -> DO, credentials 由使用者持

本 script = Level C 交付物.
使用者自己在 Termux 完成:
  1. developers.facebook.com 建 Threads-enabled app
  2. App Dashboard → Threads → Access Token 取得 THREADS_ACCESS_TOKEN
  3. 設環境變數:
       export THREADS_ACCESS_TOKEN=your_token_here
  4. 執行:
       python threads_bridge.py profile
       python threads_bridge.py recent 25
       python threads_bridge.py post POST_ID
       python threads_bridge.py replies POST_ID 25
       python threads_bridge.py insights POST_ID

Rate limit (Meta Docs 2025-12-22):
  Calls within 24h = 4800 × Number of Impressions

API base: https://graph.threads.net/v1.0
"""
import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

API_BASE = "https://graph.threads.net/v1.0"
TOKEN = os.environ.get("THREADS_ACCESS_TOKEN")

FIELDS_USER = "id,username,threads_profile_picture_url,threads_biography"
FIELDS_POST = (
    "id,media_product_type,media_type,media_url,permalink,owner,username,"
    "text,timestamp,shortcode,thumbnail_url,children,is_quote_post"
)


def _require_token():
    if not TOKEN:
        sys.stderr.write(
            "錯誤: THREADS_ACCESS_TOKEN 未設.\n"
            "  export THREADS_ACCESS_TOKEN=your_token\n"
            "  取得: developers.facebook.com → Apps → Threads → Access Token\n"
        )
        sys.exit(2)


def _get(path, params=None):
    _require_token()
    params = params or {}
    params["access_token"] = TOKEN
    url = f"{API_BASE}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.stderr.write(f"HTTP {e.code}: {body}\n")
        sys.exit(1)


def profile():
    return _get("me", {"fields": FIELDS_USER})


def recent(limit=25):
    return _get("me/threads", {"fields": FIELDS_POST, "limit": limit})


def post(media_id):
    return _get(media_id, {"fields": FIELDS_POST})


def replies(media_id, limit=25):
    return _get(f"{media_id}/replies", {"fields": FIELDS_POST, "limit": limit})


def insights(media_id):
    return _get(f"{media_id}/insights", {"metric": "views,likes,replies,reposts,quotes"})


COMMANDS = {
    "profile": lambda args: profile(),
    "recent":  lambda args: recent(int(args[0]) if args else 25),
    "post":    lambda args: post(args[0]),
    "replies": lambda args: replies(args[0], int(args[1]) if len(args) > 1 else 25),
    "insights": lambda args: insights(args[0]),
}


def _usage():
    print("用法: python threads_bridge.py <command> [args...]")
    print("命令:")
    print("  profile              取自己個人資料")
    print("  recent [limit]       最近 threads (預設 25)")
    print("  post <POST_ID>       指定 post")
    print("  replies <POST_ID> [limit]  post 的回覆")
    print("  insights <POST_ID>   views/likes/replies/reposts/quotes 指標")
    print()
    print("需先 export THREADS_ACCESS_TOKEN=your_token")
    print("取得: developers.facebook.com → Apps → Threads → Access Token")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        _usage()
        sys.exit(0)
    result = COMMANDS[sys.argv[1]](sys.argv[2:])
    print(json.dumps(result, ensure_ascii=False, indent=2))
