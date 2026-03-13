# notification/telegram.py

import os
import time
import requests
from dotenv import load_dotenv
from graph.logger import logger

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def notify_telegram(item: dict):
    """
    Sends Notification message to telegram chat
    """

    if not TOKEN or not CHAT_ID:
        print("⚠️ Telegram not configured")
        return False

    title = item.get("title", "AGuard Alert")
    summary = item.get("summary", "")
    source = item.get("source", "unknown")
    url = item.get("url")
    content_id = item.get("id")

    if summary and len(summary) > 300:
        summary = summary[:300] + "..."

    message = f"""
🔔 *AGuard Alert*

*Title:* {title}

*Summary:* {summary}

*Source:* {source}
""".strip()

    buttons = []

    # View button
    if url:
        buttons.append([{"text": "🔎 View", "url": str(url)}])

    # Ignore button
    buttons.append([
        {"text": "❌ Ignore", "callback_data": f"ignore:{content_id}"}
    ])

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": buttons
        }
    }

    r = requests.post(f"{BASE_URL}/sendMessage", json=payload)

    if r.status_code == 200:
        logger.info("Telegram notification sent")
        return True
    else:
        logger.error(f"Telegram failed: {r.text}")
        return False


def delete_message(chat_id, message_id):

    payload = {
        "chat_id": chat_id,
        "message_id": message_id
    }

    requests.post(f"{BASE_URL}/deleteMessage", json=payload)


def handle_callback(callback):

    data = callback["data"]
    chat_id = callback["message"]["chat"]["id"]
    message_id = callback["message"]["message_id"]

    action, content_id = data.split(":")

    if action == "ignore":
        delete_message(chat_id, message_id)
        print(f"❌ Ignored {content_id}")


def poll_updates():

    offset = None

    print("🤖 Telegram bot listening...")

    while True:

        params = {"timeout": 30}

        if offset:
            params["offset"] = offset

        r = requests.get(f"{BASE_URL}/getUpdates", params=params)

        data = r.json()

        for update in data.get("result", []):

            offset = update["update_id"] + 1

            if "callback_query" in update:
                callback = update["callback_query"]
                handle_callback(callback)

        time.sleep(1)