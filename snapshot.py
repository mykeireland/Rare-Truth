import os
import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import CONFIG
from utils import calculate_rsi

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ─── Fetch market data safely ─────────────────────────────────────────────
    try:
        resp = requests.get(
            f"https://api.coingecko.com/api/v3/coins/{CONFIG['coin_id']}"
        )
        data = resp.json()["market_data"]
        price  = float(data["current_price"]["usd"])
        volume = float(data["total_volume"]["usd"])

    except Exception:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Error fetching market data."
        )
        return

    # ─── Maintain RSI history ──────────────────────────────────────────────────
    history = context.bot_data.get("price_history", [])
    history.append(price)
    history = history[-CONFIG["rsi_period"]:]
    context.bot_data["price_history"] = history

    # ─── Compute RSI with safe fallback ────────────────────────────────────────
    rsi = None
    if CONFIG["rsi_enabled"] and len(history) >= 2:
        try:
            rsi = calculate_rsi(history, CONFIG["rsi_period"])
        except Exception:
            rsi = None
    try:
        rsi_text = f"{rsi:.1f}" if isinstance(rsi, (int, float)) else "n/a"
    except Exception:
        rsi_text = "n/a"

    # ─── Determine current zone label ─────────────────────────────────────────
    zone_label = "Out of Range"
    for key, (lo, hi) in CONFIG["zones"].items():
        if lo <= price <= hi:
            if key == "accumulation":
                zone_label = "Accumulation"
            elif key == "watch":
                zone_label = "Watch"
            elif key == "breakout":
                zone_label = "Breakout"
            elif key == "trim1":
                zone_label = "Trim 1"
            elif key == "trim2":
                zone_label = "Trim 2"
            break

    # ─── Build and send the snapshot message ─────────────────────────────────
    msg = (
        f"📡 <b>{CONFIG['symbol']} Snapshot</b>\n"
        f"Price: <b>${price:.4f}</b>\n"
        f"RSI: <b>{rsi_text}</b>\n"
        f"24h Vol: <b>${volume:,.0f}</b>\n"
        f"🔹 Zone: <b>{zone_label}</b>\n\n"
        "Next:\n"
        f"- Buy under <b>${CONFIG['zones']['accumulation']['max']:.2f}</b>\n"
        f"- Trim above <b>${CONFIG['zones']['trim1']['min']:.2f}</b>\n"
        f"- Breakout at <b>${CONFIG['zones']['breakout']['min']:.2f}</b>"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        parse_mode=ParseMode.HTML
    )
