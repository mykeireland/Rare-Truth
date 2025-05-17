import asyncio
import os
import requests
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_URL = "https://api.dexscreener.com/latest/dex/pairs/arbitrum/0xf0f1613c"
THRESHOLD_PRICE = 1.76
WATCH_ZONE_DELTA = 0.02

bot = Bot(token=TELEGRAM_TOKEN)

def fetch_price():
    try:
        response = requests.get(API_URL)
        data = response.json()
        price = float(data['pair']['priceUsd'])
        return price
    except Exception as e:
        return None

async def send_alert(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

async def monitor():
    while True:
        price = fetch_price()
        if price:
            if price <= THRESHOLD_PRICE:
                await send_alert(f"🔔 BUY ZONE HIT: RUNE at ${price:.4f} - ACT NOW")
            elif abs(price - THRESHOLD_PRICE) <= WATCH_ZONE_DELTA:
                await send_alert(f"👀 Watch zone: RUNE at ${price:.4f}")
        await asyncio.sleep(300)  # 5 minutes

if __name__ == "__main__":
    asyncio.run(monitor())
