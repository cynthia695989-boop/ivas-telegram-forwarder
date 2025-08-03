import time
import requests
import re
from bs4 import BeautifulSoup
import telegram

BOT_TOKEN = '7807393497:AAES2bCHYdRtmx9PM6F35LjlyB8aVqrnKTA'
CHAT_ID = '-1002828113680'
COOKIE = 'eyJpdiI6IkFrcjhibDFCajQ1a3ArREVBUyt0eHc9PSIsInZhbHVlIjoiRmN6NFpVVDdIZnZnMDQ3VzRsYWdLSDZRc1AvYnRtRUZ6YVV5V3U0VFNEVHpEeW9IMmdRTHpDTFZRQWMxK3ZuY0FKOWU4SloxSGd5YXA0TmtzVnBERENXTmpJeHBSWGJyMzBlb2ZCZGhRN0p1Zi9rSmFCVHExa3Baam5qbXM4TjkiLCJtYWMiOiI4Y2FlNDRhM2Q1NzE3NDI4MmU0YTFjNjFkMjA1MTExMzk3MjRlYTBkZTgxM2Y0NjExMTI2NzVhZWYxNTI5ZjYwIiwidGFnIjoiIn0%3D'

bot = telegram.Bot(token=BOT_TOKEN)

def extract_code(text):
    match = re.search(r'\b\d{4,8}\b', text)
    return match.group(0) if match else None

def fetch_otp():
    headers = {
        "Cookie": f"laravel_session={COOKIE}",
        "User-Agent": "Mozilla/5.0"
    }
    url = "https://www.ivasms.com/portal/live/my_sms"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select("tbody tr")
    messages = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            number = cols[1].text.strip()
            message = cols[2].text.strip()
            if message and number:
                messages.append((number, message))
    return messages

sent_cache = set()

while True:
    try:
        messages = fetch_otp()
        for number, message in messages:
            key = number + message
            if key not in sent_cache:
                otp = extract_code(message)
                if otp:
                    text = f"🔔 OTP from {number}\n\n🔑 Code: {otp}\n✉️ Message: {message}\n\n👨‍💻 Developer: @asik_2_0_bd"
                    bot.send_message(chat_id=CHAT_ID, text=text)
                    sent_cache.add(key)
        time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
