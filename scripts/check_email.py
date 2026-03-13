from notification.email import notify_email

test_item = {
    "title": "Email test",
    "reason": "Testing email notifier",
    "confidence": 0.99,
    "source": "system",
    "url": "https://example.com"
}

notify_email(test_item)
