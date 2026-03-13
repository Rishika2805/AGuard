# notification/email.py

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

from graph.logger import logger

load_dotenv()

sender = os.getenv("EMAIL_SENDER")
password = os.getenv("EMAIL_PASSWORD")
receiver = os.getenv("EMAIL_RECEIVER")




def notify_email(items):
    title = items.get("title", "AGuard Alert")
    summary = items.get("summary", "")
    source = items.get("source", "unknown")
    url = items.get("url", "")

    # Plain text fallback
    body_text = f"""
{summary}

Source: {source}

{url}
""".strip()

    # HTML version
    body_html = f"""
<html>
  <body style="font-family: Arial, sans-serif; background:#f4f6f8; padding:20px;">

    <div style="
        max-width:600px;
        margin:auto;
        background:white;
        padding:20px;
        border-radius:8px;
        box-shadow:0 2px 6px rgba(0,0,0,0.1);
    ">

      <h2 style="color:#2c3e50;">🚨 AGuard Alert</h2>

      <h3>{title}</h3>

      <p>{summary}</p>

      <hr style="border:none;border-top:1px solid #eee;">

      <p><strong>Source:</strong> {source}</p>

      <p style="margin-top:20px;">
        <a href="{url}" 
           style="
             background-color:#3498db;
             color:white;
             padding:12px 18px;
             text-decoration:none;
             border-radius:6px;
             font-weight:bold;
           ">
           View Content
        </a>
      </p>

      <hr style="border:none;border-top:1px solid #eee; margin-top:30px;">

      <p style="font-size:12px; color:gray;">
        Sent by <strong>AGuard AI Monitoring System</strong>
      </p>

    </div>

  </body>
</html>
"""

    msg = EmailMessage()
    msg["Subject"] = f"[AGuard] {title}"
    msg["From"] = sender
    msg["To"] = receiver

    msg.set_content(body_text)
    msg.add_alternative(body_html, subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
            logger.info("Email notification sent")
        return True

    except Exception as e:
        logger.error("Email notification failed")
        return False