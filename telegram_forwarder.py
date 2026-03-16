# telegram_forwarder_ready.py
from telethon import TelegramClient, events
import os

# ====== متغیرهای محیطی ======
API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
PHONE = os.environ["TELEGRAM_PHONE"]  # شماره تلگرام با +98 یا +1

# ====== کانال‌های مبدا ======
SOURCE_CHANNELS = [
    'nerkhYabkhorasanMarket',
    'aqbazjgani',
    'dollar_tehran3bze',
    'KabulMarkets',
    'nerkhedolar1'
]

# ====== کانال مقصد ======
DEST_CHANNEL = 'KhorasanMarkets'  # حساب تلگرام باید ادمین باشد

# ====== ایجاد کلاینت ======
client = TelegramClient('user_session', API_ID, API_HASH)

# ====== رویداد دریافت پیام‌های جدید ======
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    msg_text = event.message.message or ""
    
    # فیلتر تبلیغات یا پیام‌های ناخواسته
    if any(keyword in msg_text.lower() for keyword in ["buy now", "ad:", "تبلیغ"]):
        return
    
    # فورواد پیام به کانال مقصد
    await client.send_message(DEST_CHANNEL, event.message)

# ====== اجرای ربات ======
print("Bot is running...")
client.start(phone=PHONE)  # شماره از متغیر محیطی
client.run_until_disconnected()
