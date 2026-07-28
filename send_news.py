import os
import feedparser
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

RSS_FEEDS = [
    "https://www.isna.ir/rss",
]

message = "📰 خلاصه اخبار\n\n"

for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        message += "🔹 " + title + "\n" + link + "\n\n"

if len(message) > 4000:
    message = message[:4000] + "..."

url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
response = requests.post(url, data={
    "chat_id": CHANNEL_ID,
    "text": message,
    "disable_web_page_preview": False
})

print(response.status_code, response.text)
