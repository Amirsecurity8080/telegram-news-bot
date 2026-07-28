import feedparser
import requests
import os

BOT_TOKEN = os.environ["8938523902:AAHNQknqLLk1DWmhHdwF0ZEDCq4F-PP3_jU"]
CHANNEL_ID = os.environ["-1003274837538"]

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
    f"https://api.telegram.org/bot{8938523902:AAHNQknqLLk1DWmhHdwF0ZEDCq4F-PP3_jU}/sendMessage",
    data={
        "chat_id": CHANNEL_ID,
        "text": message,
        "disable_web_page_preview": False
    }
)

print(response.status_code, response.text)
