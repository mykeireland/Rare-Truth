import asyncio
import os
import requests
from telegram import Bot
from telegram.constants import ParseMode

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

DEX_URL = "https://api.dexscreener.com/latest/dex/pairs/thorchain/USDT-RUNE"
TRIGGER_ZONE = 1.76
WATCH_ZONE_DELTA = 0.03

async def fetch_price():
    try:
        response = requests.get("https://api.dexscreener.com/latest/dex/pairs/thorchain/USDT-RUNE")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'pairs' in data:
                return float(data['pairs'][0]['priceUsd'])
            else:
                print("Unexpected API structure:", data)
        else:
            print(f"Dex API failed with status code {response.status_code}")
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
            if price <= TRIGGER_ZONE:
                await send_message(f"🚀 <b>BUY ZONE</b> hit: RUNE at ${price:.4f}")
            elif abs(price - TRIGGER_ZONE) <= WATCH_ZONE_DELTA:
                await send_message(f"👀 <i>Watch zone</i>: RUNE at ${price:.4f}")
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(monitor())
