from notification.telegram import notify_telegram

from notification.telegram import notify_telegram
from notification.email import notify_email

item = {
    "title": "Manual test",
    "summary": "If you see this, notifications work.",
    "reason": "Debug",
    "source": "system",
    "url": ""
}

notify_telegram(item)
notify_email(item)

