import os
import feedparser
import requests
from deep_translator import GoogleTranslator

# دریافت متغیرهای محیطی
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# اگر متغیرها وجود نداشت، خطا بده
if not BOT_TOKEN or not CHANNEL_ID:
    print("❌ BOT_TOKEN or CHANNEL_ID not found!")
    exit(1)

# لیست خوراک‌های خبری
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
        print(f"Translation error: {e}")
        return text

def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ساخت پیام
message = "📰 <b>خلاصه اخبار</b>\n\n"
count = 0
MAX_NEWS = 15
SECURITY_NEWS_LIMIT = 5

# اخبار فارسی
print("📥 Fetching Persian news...")
for feed_url in FA_FEEDS:
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            if count >= MAX_NEWS - SECURITY_NEWS_LIMIT:
                break
            title = escape_html(entry.title)
            message += f"🔹 {title}\n<a href=\"{entry.link}\">🔗 لینک خبر</a>\n\n"
            count += 1
            print(f"✅ Added: {entry.title[:50]}...")
    except Exception as e:
        print(f"❌ Error in {feed_url}: {e}")

# اخبار امنیتی
message += "🛡 <b>اخبار امنیت سایبری و هک</b>\n\n"
print("📥 Fetching security news...")
for feed_url in SECURITY_FEEDS:
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:SECURITY_NEWS_LIMIT]:
            translated_title = escape_html(translate_safe(entry.title))
            message += f"🔸 {translated_title}\n<a href=\"{entry.link}\">🔗 لینک خبر</a>\n\n"
            count += 1
            print(f"✅ Added: {entry.title[:50]}...")
    except Exception as e:
        print(f"❌ Error in {feed_url}: {e}")

# محدودیت طول پیام
if len(message) > 4000:
    message = message[:4000] + "..."
    print("⚠️ Message truncated to 4000 chars")

print(f"📊 Total news: {count}, Message length: {len(message)}")

# ارسال به تلگرام
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
try:
    print("📤 Sending to Telegram...")
    response = requests.post(url, data={
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }, timeout=30)
    
    print(f"📡 Status: {response.status_code}")
    print(f"📄 Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Message sent successfully!")
    else:
        print("❌ Failed to send!")
except Exception as e:
    print(f"❌ Error: {e}")
