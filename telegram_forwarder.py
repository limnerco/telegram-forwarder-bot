# telegram_forwarder_railway.py
from telethon import TelegramClient, events
import os

# ====== متغیرهای محیطی ======
API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
PHONE = os.environ["TELEGRAM_PHONE"]  # شماره تلگرام با +98 یا +1

# ====== کانال‌ها ======
SOURCE_CHANNELS = [
    'nerkhYabkhorasanMarket',
    'aqbazjgani',
    'dollar_tehran3bze',
    'KabulMarkets',
    'nerkhedolar1'
]

DEST_CHANNEL = 'KhorasanMarkets'  # کانال مقصد، حساب تلگرام باید ادمین باشد

# ====== ایجاد کلاینت با شماره واقعی ======
client = TelegramClient('user_session', API_ID, API_HASH)

async def main():
    # ورود با شماره تلگرام از متغیر محیطی
    await client.start(phone=PHONE)
    print("Bot is running...")

    # ====== دریافت پیام‌های جدید از کانال‌های مبدا ======
    @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def handler(event):
        msg_text = event.message.message or ""
        
        # ====== فیلتر تبلیغات ======
        if any(keyword in msg_text.lower() for keyword in ["buy now", "ad:", "تبلیغ"]):
            return  # پیام نادیده گرفته می‌شود
        
        # ====== فورواد پیام به کانال مقصد ======
        await client.send_message(DEST_CHANNEL, event.message)

    await client.run_until_disconnected()

# ====== اجرای ربات ======
with client:
    client.loop.run_until_complete(main())
