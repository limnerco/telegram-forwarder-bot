# telegram_forwarder.py
from telethon import TelegramClient, events
import os

# ====== متغیرهای محیطی ======
API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# ====== کانال‌ها ======
SOURCE_CHANNELS = [
    '@nerkhYabkhorasanMarket',
    '@aqbazjgani',
    '@dollar_tehran3bze',
    '@KabulMarkets'
    '@nerkhedolar1'
]
]

DEST_CHANNEL = '@KhorasanMarkets'

# ====== ایجاد کلاینت ربات ======
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ====== رویداد دریافت پیام‌های جدید از کانال‌های مبدا ======
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    msg_text = event.message.message or ""
    
    # ====== فیلتر تبلیغات یا پیام‌های ناخواسته ======
    if any(keyword in msg_text.lower() for keyword in ["buy now", "ad:", "تبلیغ"]):
        return  # پیام نادیده گرفته می‌شود
    
    # ====== فورواد پیام به کانال مقصد ======
    await client.send_message(DEST_CHANNEL, event.message)

# ====== اجرای ربات ======
print("Bot is running...")
client.run_until_disconnected()
