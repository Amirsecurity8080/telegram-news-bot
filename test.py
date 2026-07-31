import os
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# ارسال یک پیام ساده
response = requests.post(url, data={
    "chat_id": CHANNEL_ID,
    "text": "🧪 این یک پیام تست ساده است",
})

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

# اگر خطا داشت، دلیل را نشان بده
if response.status_code != 200:
    print("❌ Error details:", response.json())
