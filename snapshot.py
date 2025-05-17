import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import CONFIG
from utils import calculate_rsi, fetch_ticker, fetch_klines

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, volume = fetch_ticker(CONFIG["binance_symbol"])
    # RSI
    rsi = None
    if CONFIG["rsi_enabled"]:
        closes = fetch_klines(CONFIG["binance_symbol"], CONFIG["rsi_period"])
        rsi = calculate_rsi(closes, CONFIG["rsi_period"])
    # Momentum
    if isinstance(rsi, (int, float)):
        momentum = "Strong 🚀" if rsi > 70 else "Neutral ⚖️" if rsi >= 45 else "Weak 🐻"
    else:
        momentum = "n/a"
    # Zone
    zone = "Out of Range"
    for k,b in CONFIG["zones"].items():
        if b["min"] <= price <= b["max"]:
            zone = k.capitalize()
            break
    # Build message
    msg = (
        f"📡 <b>{CONFIG['symbol']} Snapshot</b>\n"
        f"Price: <b>${price:.4f}</b>   24h Vol: <b>${volume:,.0f}</b>\n"
        f"RSI: <b>{rsi:.1f if rsi else 'n/a'}</b>   Momentum: <b>{momentum}</b>\n"
        f"Zone: <b>{zone}</b>"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        parse_mode=ParseMode.HTML
    )
