import os
import feedparser
import requests
from deep_translator import GoogleTranslator

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

FA_FEEDS = [
    "https://www.isna.ir/rss",
]

SECURITY_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
]

translator = GoogleTranslator(source="en", target="fa")

def translate_safe(text):
    try:
        return translator.translate(text)
    except Exception as e:
        print(f"Translation error: {e}")  # برای دیباگ
        return text

def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

message = "📰 <b>خلاصه اخبار</b>\n\n"
count = 0
MAX_NEWS = 15
SECURITY_NEWS_LIMIT = 5  # تعداد اخبار امنیتی

# اخبار فارسی
for feed_url in FA_FEEDS:
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            if count >= MAX_NEWS - SECURITY_NEWS_LIMIT:  # جا برای اخبار امنیتی
                break
            title = escape_html(entry.title)
            message += f"🔹 {title}\n<a href=\"{entry.link}\">🔗 لینک خبر</a>\n\n"
            count += 1
    except Exception as e:
        print(f"Error processing {feed_url}: {e}")

# اخبار امنیتی
message += "🛡 <b>اخبار امنیت سایبری و هک</b>\n\n"
for feed_url in SECURITY_FEEDS:
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:SECURITY_NEWS_LIMIT]:
            translated_title = escape_html(translate_safe(entry.title))
            message += f"🔸 {translated_title}\n<a href=\"{entry.link}\">🔗 لینک خبر</a>\n\n"
            count += 1
    except Exception as e:
        print(f"Error processing {feed_url}: {e}")

# محدودیت طول پیام
if len(message) > 4000:
    message = message[:4000] + "..."

# ارسال به تلگرام
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
try:
    response = requests.post(url, data={
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    })
    print(response.status_code, response.text)
except Exception as e:
    print(f"Error sending message: {e}")
