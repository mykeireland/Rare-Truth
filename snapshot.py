from telegram.ext import ContextTypes
from telegram import Update
from telegram.constants import ParseMode
from config import CONFIG
from utils import calculate_rsi
import requests

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin_id = CONFIG["coin_id"]
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}")
        j = r.json()
        price = j["market_data"]["current_price"]["usd"]
        volume = j["market_data"]["total_volume"]["usd"]
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error fetching data.")
        return

    history = context.bot_data.get("price_history", [])
    history.append(price)
    history = history[-CONFIG["rsi_period"]:]
    context.bot_data["price_history"] = history
    rsi = calculate_rsi(history) if len(history) >= 2 else None

    z = CONFIG["zones"]
    zone = "Out of Range"
    if z["accumulation"]["min"] <= price <= z["accumulation"]["max"]:
        zone = "Accumulation"
    elif z["watch"]["min"] <= price <= z["watch"]["max"]:
        zone = "Watch"
    elif z["breakout"]["min"] <= price <= z["breakout"]["max"]:
        zone = "Breakout"
    elif z["trim1"]["min"] <= price <= z["trim1"]["max"]:
        zone = "Trim 1"
    elif z["trim2"]["min"] <= price <= z["trim2"]["max"]:
        zone = "Trim 2"

    msg = f"""📡 <b>RUNE Market Snapshot</b>
Price: <b>${price:.4f}</b>
rsi_text = f"{rsi:.1f}" if rsi is not None else "n/a"
24h Volume: <b>${volume:,.0f}</b>

🔹 Zone: <b>{zone}</b>
🔹 Momentum: {"Strong" if rsi and rsi > 70 else "Neutral" if rsi and 45 <= rsi <= 70 else "Weak"}

Next:
- Scale in <b>under ${z["accumulation"]["max"]:.2f}</b>
- Trim profits <b>above ${z["trim1"]["min"]:.2f}</b>
- Breakout expected <b>above ${z["breakout"]["min"]:.2f}</b>
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=ParseMode.HTML)
