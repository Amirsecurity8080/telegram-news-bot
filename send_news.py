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
    except Exception:
        return text

def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

message = "📰 <b>خلاصه اخبار</b>\n\n"
count = 0
MAX_NEWS = 15

for feed_url in FA_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        if count >= MAX_NEWS:
            break
        title = escape_html(entry.title)
        message += f"🔹 {title}\n<a href=\"{entry.link}\">🔗 لینک خبر</a>\n\n"
        count += 1

message += "🛡 <b>اخبار امنیت سایبری و هک</b>\n\n"
for feed_url in SECURITY_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:5]:
        translated_title = escape_html(translate_safe(entry.title))
        message += f"🔸 {translated_title}\n<a href=\"{entry.link}\">🔗 لینک خبر</a>\n\n"
        count += 1

if len(message) > 4000:
    message = message[:4000] + "..."

url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
response = requests.post(url, data={
    "chat_id": CHANNEL_ID,
    "text": message,
    "parse_mode": "HTML",
    "disable_web_page_preview": True
})

print(response.status_code, response.text)
