import asyncio
import os
import requests
from telegram import Bot
from telegram.constants import ParseMode

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TRIGGER_ZONE = float(os.getenv("TRIGGER_ZONE", 1.76))
WATCH_ZONE_DELTA = float(os.getenv("WATCH_ZONE_DELTA", 0.03))

bot = Bot(token=TELEGRAM_TOKEN)
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price?ids=thorchain&vs_currencies=usd"

async def fetch_price():
    try:
        response = requests.get(COINGECKO_URL)
        if response.status_code == 200:
            data = response.json()
            return float(data["thorchain"]["usd"])
        else:
            print(f"CoinGecko failed with status {response.status_code}")
    except Exception as e:
        print("Error fetching price:", e)
    return None

async def send_message(text):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.HTML)
    except Exception as e:
        print("Telegram send failed:", e)

async def monitor():
    while True:
        price = await fetch_price()
        if price:
            print(f"Current RUNE price: ${price:.4f}")
            if price <= TRIGGER_ZONE:
                await send_message(f"🚀 <b>BUY ZONE</b> hit: RUNE at <b>${price:.4f}</b>")
            elif abs(price - TRIGGER_ZONE) <= WATCH_ZONE_DELTA:
                await send_message(f"👀 <i>Watch zone</i>: RUNE at ${price:.4f}")
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(monitor())
