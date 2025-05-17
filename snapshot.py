import os, requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import CONFIG
from utils import calculate_rsi

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Fetch market data
    try:
        data = requests.get(
            f"https://api.coingecko.com/api/v3/coins/{CONFIG['coin_id']}"
        ).json()['market_data']
        price = data['current_price']['usd']
        volume = data['total_volume']['usd']
    except Exception:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Error fetching data."
        )
        return

    # Maintain price history
    history = context.bot_data.get('price_history', [])
    history.append(price)
    history = history[-CONFIG['rsi_period']:]
    context.bot_data['price_history'] = history

    # Compute RSI
    rsi = None
    if CONFIG['rsi_enabled'] and len(history) >= 2:
        rsi = calculate_rsi(history, CONFIG['rsi_period'])
    try:
        rsi_text = f"{float(rsi):.1f}"
    except Exception:
        rsi_text = "n/a"

    # Determine zone label
    zlab = 'Out of Range'
    for key, (lo, hi) in CONFIG['zones'].items():
        if lo <= price <= hi:
            # human-friendly name mapping
            if key == 'accumulation': zlab = 'Accumulation'
            elif key == 'watch':       zlab = 'Watch'
            elif key == 'breakout':    zlab = 'Breakout'
            elif key == 'trim1':       zlab = 'Trim 1'
            elif key == 'trim2':       zlab = 'Trim 2'
            break

    # Build and send message
    msg = (
        f"📡 <b>{CONFIG['symbol']} Snapshot</b>\n"
        f"Price: <b>${price:.4f}</b>\n"
        f"RSI: <b>{rsi_text}</b>\n"
        f"24h Vol: <b>${volume:,.0f}</b>\n"
        f"🔹 Zone: <b>{zlab}</b>\n\n"
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
