import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def _send(message: str):
    try:
        import telegram
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print(f"[TELEGRAM] Alert sent.")
    except Exception as e:
        print(f"[TELEGRAM] Failed to send: {e}")

def send_alert(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[TELEGRAM] Not configured — skipping. Message was: {message}")
        return
    asyncio.run(_send(message))