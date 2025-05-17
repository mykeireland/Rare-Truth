import time
from telegram import Bot
from telegram.constants import ParseMode
from config import CONFIG
from utils import (
    fetch_ticker,
    fetch_klines,
    calculate_rsi,
    should_notify,
    record_notification
)

class StrategyEngine:
    def __init__(self):
        self.bot     = Bot(token=CONFIG["TELEGRAM_TOKEN"])
        self.chat_id = CONFIG["CHAT_ID"]

    async def evaluate(self):
        price, volume = fetch_ticker(CONFIG["binance_symbol"])
        # RSI calculation
        rsi = None
        if CONFIG["rsi_enabled"]:
            closes = fetch_klines(CONFIG["binance_symbol"], CONFIG["rsi_period"])
            rsi = calculate_rsi(closes, CONFIG["rsi_period"])
        # Determine status
        status = None
        for zone, bounds in CONFIG["zones"].items():
            lo, hi = bounds["min"], bounds["max"]
            if lo <= price <= hi:
                status = zone.capitalize()
                break
        # Format alert message
        if status and should_notify(status, price):
            msg = f"📈 <b>{CONFIG['symbol']} Alert</b> — {status} @ ${price:.4f}"
            if isinstance(rsi, (int, float)):
                msg += f" | RSI: {rsi:.1f}"
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=msg,
                parse_mode=ParseMode.HTML
            )
            record_notification(status, price)
