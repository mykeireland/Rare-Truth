from telegram import Update
from telegram.ext import ContextTypes
from utils import fetch_price_rsi_volume, format_snapshot
from config import CONFIG

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        result = fetch_price_rsi_volume()
        if result is None:
            await update.message.reply_text("⚠️ Failed to fetch market data.")
            return

        price, rsi, momentum, volume = result

        lo, hi = float(CONFIG["buy_zone_low"]), float(CONFIG["buy_zone_high"])
        msg = format_snapshot(price, rsi, momentum, volume, lo, hi)
        await update.message.reply_text(msg, parse_mode='HTML')

    except Exception as e:
        await update.message.reply_text(f"Snapshot error: {e}")
