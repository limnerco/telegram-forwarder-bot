import asyncio
import os
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread
import logging

# -------------------------
# Keep-alive server for Replit
# -------------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -------------------------
# Logging
# -------------------------
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# -------------------------
# Telegram credentials
# -------------------------
API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
PHONE = os.environ["TELEGRAM_PHONE"]

# -------------------------
# Channels
# -------------------------
SOURCE_CHANNELS = [
    "@nerkhYabkhorasanMarket",
    "@aqbazjgani",
    "@dollar_tehran3bze",
    "@nerkhedolar1",
    "@KabulMarkets"  # کانال تستی
]

TARGET_CHANNEL = "@KhorasanMarkets"

# -------------------------
# Allowed keywords/messages
# -------------------------
ALLOWED_KEYWORDS = {
    "@nerkhYabkhorasanMarket": [
        "هرات تومان بانکی", "هرات تومان چک", "هرات دالر به افغانی",
        "هرات یورو به افغانی", "هرات کلدار افغانی"
    ],
    "@aqbazjgani": [
        "کندهار", "کابل", "مزاره", "جلال اباد", "غزنی", "ڪابل دالر به ڪلدار"
    ],
    "@dollar_tehran3bze": [
        "دلار نـــقـدی تهران"
    ],
    "@nerkhedolar1": [
        "دلار فردایی تهران"
    ],
    "@KabulMarkets": None  # برای کانال تستی، همه پیام‌ها فورواد می‌شوند
}

# -------------------------
# Telegram client
# -------------------------
client = TelegramClient("forwarder", API_ID, API_HASH)

# -------------------------
# Main bot logic
# -------------------------
async def main():
    await client.start(phone=PHONE)
    target = await client.get_entity(TARGET_CHANNEL)

    source_entities = []
    for ch in SOURCE_CHANNELS:
        entity = await client.get_entity(ch)
        source_entities.append(entity)
        log.info(f"Monitoring: {ch}")

    @client.on(events.NewMessage(chats=source_entities))
    async def handler(event):
        chat_username = event.chat.username
        message_text = event.raw_text

        # کانال تستی: همه پیام‌ها
        if chat_username == "KabulMarkets" or chat_username == "@KabulMarkets":
            await client.send_message(target, message_text)
            log.info(f"[Test channel] Message forwarded: {message_text}")
            return

        # کانال‌های اصلی: فقط پیام‌های شامل کلیدواژه‌ها
        if chat_username in ALLOWED_KEYWORDS and ALLOWED_KEYWORDS[chat_username]:
            keywords = ALLOWED_KEYWORDS[chat_username]
            if any(keyword in message_text for keyword in keywords):
                await client.send_message(target, message_text)
                log.info(f"Message forwarded from {chat_username}: {message_text}")

    log.info("Bot started and running...")
    await client.run_until_disconnected()

# -------------------------
# Start everything
# -------------------------
keep_alive()

if __name__ == "__main__":
    asyncio.run(main())