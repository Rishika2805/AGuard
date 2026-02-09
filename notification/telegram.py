# notification/telegram.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def notify_telegram(item: dict):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("⚠️ Telegram not configured, skipping")
        return False

    title = item.get("title", "AGuard Alert")
    summary = item.get("summary", "")
    reason = item.get("reason", "")
    source = item.get("source", "unknown")
    url = item.get("url", "")

    message = f"""
🔔 AGuard Alert

{title}

{summary}

Why: {reason}
Source: {source}

{url}
""".strip()

    api_url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        r = requests.post(api_url, json=payload, timeout=5)
        if r.status_code == 200:
            print("✅ Telegram sent")
            return True
        else:
            print("❌ Telegram failed:", r.text)
            return False
    except Exception as e:
        print("❌ Telegram error:", e)
        return False


