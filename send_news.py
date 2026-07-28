import feedparser
import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

# می‌تونی چند تا RSS اضافه کنی
RSS_FEEDS = [
    "https://www.isna.ir/rss",
]

message = "📰 خلاصه اخبار\n\n"

for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:5]:  # ۵ خبر اول هر فید
        title = entry.title
        link = entry.link
        message += f"🔹 {title}\n{link}\n\n"

# تلگرام محدودیت طول پیام داره (۴۰۹۶ کاراکتر)
if len(message) > 4000:
    message = message[:4000] + "..."

response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHANNEL_ID,
        "text": message,
        "disable_web_page_preview": False
    }
)

print(response.status_code, response.text)
