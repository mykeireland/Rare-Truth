# snapshot.py

import requests
import os
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import CONFIG
from utils import calculate_rsi

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🛠️ Fetch data
    coin_id = CONFIG["coin_id"]
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}")
        data = r.json()
        price = data["market_data"]["current_price"]["usd"]
        volume = data["market_data"]["total_volume"]["usd"]
    except Exception:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Error fetching market data."
        )
        return

    # 🔄 Maintain price history for RSI
    history = context.bot_data.get("price_history", [])
    history.append(price)
    history = history[-CONFIG["rsi_period"]:]
    context.bot_data["price_history"] = history

    # ⚙️ Calculate RSI safely
    rsi = None
    if CONFIG["rsi_enabled"] and len(history) >= 2:
        try:
            rsi = calculate_rsi(history)
        except Exception:
            rsi = None

    # 🛡️ Format RSI text without ever crashing
    try:
        rsi_text = f"{float(rsi):.1f}"
    except Exception:
        rsi_text = "n/a"

    # 🔍 Determine current zone
    z = CONFIG["zones"]
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
    else:
        zone = "Out of Range"

    # ✉️ Build and send the message
    msg = (
        f"📡 <b>RUNE Market Snapshot</b>\n"
        f"Price: <b>${price:.4f}</b>\n"
        f"RSI (14): <b>{rsi_text}</b>\n"
        f"24h Volume: <b>${volume:,.0f}</b>\n\n"
        f"🔹 Zone: <b>{zone}</b>\n"
        f"🔹 Momentum: "
        f"{'Strong' if rsi and rsi > 70 else 'Neutral' if rsi and 45 <= rsi <= 70 else 'Weak'}\n\n"
        f"Next:\n"
        f"- Scale in under <b>${z['accumulation']['max']:.2f}</b>\n"
        f"- Trim profits above <b>${z['trim1']['min']:.2f}</b>\n"
        f"- Breakout expected above <b>${z['breakout']['min']:.2f}</b>"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        parse_mode=ParseMode.HTML
    )
