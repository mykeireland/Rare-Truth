import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import CONFIG
from utils import calculate_rsi, fetch_ticker, fetch_klines

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Fetch current price & volume
    price, volume = fetch_ticker(CONFIG["binance_symbol"])

    # Calculate RSI
    rsi = None
    if CONFIG["rsi_enabled"]:
        closes = fetch_klines(CONFIG["binance_symbol"], CONFIG["rsi_period"])
        rsi = calculate_rsi(closes, CONFIG["rsi_period"])

    # Determine momentum
    if isinstance(rsi, (int, float)):
        if rsi > 70:
            momentum = "Strong 🚀"
        elif rsi >= 45:
            momentum = "Neutral ⚖️"
        else:
            momentum = "Weak 🐻"
    else:
        momentum = "n/a"

    # Determine zone label
    zone = "Out of Range"
    for key, bounds in CONFIG["zones"].items():
        if bounds["min"] <= price <= bounds["max"]:
            zone = key.capitalize()
            break

    # Format RSI text separately to avoid invalid f-string
    rsi_text = f"{rsi:.1f}" if isinstance(rsi, (int, float)) else "n/a"

    # Build and send the snapshot message
    msg = (
        f"📡 <b>{CONFIG['symbol']} Snapshot</b>
"
        f"Price: <b>${price:.4f}</b>   24h Vol: <b>${volume:,.0f}</b>
"
        f"RSI: <b>{rsi_text}</b>   Momentum: <b>{momentum}</b>
"
        f"Zone: <b>{zone}</b>"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        parse_mode=ParseMode.HTML
    )
