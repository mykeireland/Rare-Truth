import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import CONFIG
from utils import fetch_ticker, fetch_klines, calculate_rsi

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Fetch price & volume
    price, volume = fetch_ticker(CONFIG["binance_symbol"])

    # Compute RSI
    rsi = None
    if CONFIG["rsi_enabled"]:
        closes = fetch_klines(CONFIG["binance_symbol"], CONFIG["rsi_period"])
        rsi = calculate_rsi(closes, CONFIG["rsi_period"])

    # Format fields
    rsi_text = f"{rsi:.1f}" if isinstance(rsi, (int, float)) else "n/a"
    momentum = (
        "Strong 🚀" if rsi > 70 else
        "Neutral ⚖️" if rsi >= 45 else
        "Weak 🐻" if rsi is not None else
        "n/a"
    )

    # Determine zone label
    zone_label = "Out of Range"
    for key, bounds in CONFIG["zones"].items():
        lo, hi = bounds["min"], bounds["max"]
        if lo <= price <= hi:
            zone_label = key.capitalize()
            break

    # Build & send
    msg = (
        f"📡 <b>{CONFIG['symbol']} Snapshot</b>\n"
        f"Price: <b>${price:.4f}</b> | Vol: <b>${volume:,.0f}</b>\n"
        f"RSI: <b>{rsi_text}</b> | Momentum: <b>{momentum}</b>\n"
        f"Zone: <b>{zone_label}</b>\n\n"
        "Next: Buy under ${:.2f}, Trim above ${:.2f}, Breakout at ${:.2f}".format(
            CONFIG['zones']['accumulation']['max'],
            CONFIG['zones']['trim1']['min'],
            CONFIG['zones']['breakout']['min']
        )
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        parse_mode=ParseMode.HTML
    )
