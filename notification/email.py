# notification/email.py

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def notify_email(item: dict):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not sender or not password or not receiver:
        print("⚠️ Email not configured, skipping")
        return False

    title = item.get("title", "AGuard Alert")
    summary = item.get("summary", "")
    reason = item.get("reason", "")
    source = item.get("source", "unknown")
    url = item.get("url", "")

    body = f"""
{summary}

Why: {reason}
Source: {source}

{url}
""".strip()

    msg = EmailMessage()
    msg["Subject"] = f"[AGuard] {title}"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)

        print("✅ Email sent")
        return True
    except Exception as e:
        print("❌ Email failed:", e)
        return False
