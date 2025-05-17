import os, requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import CONFIG
from utils import calculate_rsi

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, volume = None, None
    try:
        data = requests.get(f"https://api.coingecko.com/api/v3/coins/{CONFIG['coin_id']}").json()['market_data']
        price, volume = data['current_price']['usd'], data['total_volume']['usd']
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Error fetching data.")
        return

    history = context.bot_data.get('price_history', []) + [price]
    history = history[-CONFIG['rsi_period']:]
    context.bot_data['price_history'] = history
    rsi = calculate_rsi(history, CONFIG['rsi_period']) if CONFIG['rsi_enabled'] and len(history)>=2 else None
    try:
        rsi_text = f"{float(rsi):.1f}"
    except:
        rsi_text = "n/a"

    zlab = 'Out of Range'
    for key, (lo, hi) in CONFIG['zones'].items():
        if lo <= price <= hi:
            zlab = key.capitalize()
    msg = (
        f"📡 <b>{CONFIG['symbol']} Snapshot</b>
"
        f"Price: <b>${price:.4f}</b>
"
        f"RSI: <b>{rsi_text}</b>
"
        f"24h Vol: <b>${volume:,.0f}</b>
"
        f"🔹 Zone: <b>{zlab}</b>

"
        f"Next:
"
        f"- Buy under <b>${CONFIG['zones']['accumulation']['max']:.2f}</b>
"
        f"- Trim above <b>${CONFIG['zones']['trim1']['min']:.2f}</b>
"
        f"- Breakout at <b>${CONFIG['zones']['breakout']['min']:.2f}</b>"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=ParseMode.HTML)