import os
from dotenv import load_dotenv

load_dotenv()

print("EMAIL_SENDER:", os.getenv("EMAIL_SENDER"))
print("EMAIL_PASSWORD:", "SET" if os.getenv("EMAIL_PASSWORD") else "MISSING")
print("EMAIL_RECEIVER:", os.getenv("EMAIL_RECEIVER"))

print("TELEGRAM_BOT_TOKEN:", "SET" if os.getenv("TELEGRAM_BOT_TOKEN") else "MISSING")
print("TELEGRAM_CHAT_ID:", os.getenv("TELEGRAM_CHAT_ID"))
