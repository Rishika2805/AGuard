# notification/dispatcher.py

from notification.console import notify_console
from notification.email import notify_email
from notification.telegram import notify_telegram


def dispatch_notification(item: dict):
    """
    Decide which channels to use.
    This is the ONLY place where routing logic exists.
    """
    print("📨 DISPATCHING:", item["id"])
    notify_console(item)
    notify_email(item)
    notify_telegram(item)


