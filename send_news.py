import os
import feedparser
import requests
from deep_translator import GoogleTranslator

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

# اخبار عمومی فارسی
FA_FEEDS = [
    "https://www.isna.ir/rss",
]

# اخبار هک و امنیت سایبری (خارجی، به انگلیسی)
SECURITY_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
]

translator = GoogleTranslator(source="en", target="fa")

def translate_safe(text):
    try:
        return translator.translate(text)
    except Exception:
        return text  # اگه ترجمه خطا داد، متن اصلی رو نگه دار

message = "📰 خلاصه اخبار\n\n"
count = 0
MAX_NEWS = 15

# ابتدا اخبار فارسی
for feed_url in FA_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        if count >= MAX_NEWS:
            break
        message += "🔹 " + entry.title + "\n" + entry.link + "\n\n"
        count += 1

# سپس اخبار امنیتی/هکری (ترجمه‌شده)
message += "🛡 اخبار امنیت سایبری و هک\n\n"
for feed_url in SECURITY_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:5]:  # از هر منبع ۵ تا
        if count >= MAX_NEWS + 10:  # سقف کلی پیام
            break
        translated_title = translate_safe(entry.title)
        message += "🔸 " + translated_title + "\n" + entry.link + "\n\n"
        count += 1

if len(message) > 4000:
    message = message[:4000] + "..."

url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
response = requests.post(url, data={
    "chat_id": CHANNEL_ID,
    "text": message,
    "disable_web_page_preview": True  # پیش‌نمایش بزرگ خاموش، لینک همچنان هست
})

print(response.status_code, response.text)
