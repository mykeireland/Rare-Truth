import time
from telegram import Bot
from telegram.constants import ParseMode
from config import CONFIG
from utils import fetch_ticker, fetch_klines, calculate_rsi

class StrategyEngine:
    def __init__(self):
        self.bot = Bot(token=CONFIG["TELEGRAM_TOKEN"])
        self.chat_id = CONFIG["CHAT_ID"]
        self.last_alert = {}

    async def evaluate(self):
        price, volume = fetch_ticker(CONFIG["binance_symbol"])
        now = time.time()

        # RSI
        rsi = None
        if CONFIG["rsi_enabled"]:
            closes = fetch_klines(CONFIG["binance_symbol"], CONFIG["rsi_period"])
            rsi = calculate_rsi(closes, CONFIG["rsi_period"])

        # Determine zone and message
        msg = None
        for zone, bounds in CONFIG["zones"].items():
            lo, hi = bounds["min"], bounds["max"]
            if lo <= price <= hi:
                if zone == "accumulation":
                    msg = f"📥 Accumulation zone: ${price:.4f}"
                elif zone == "watch":
                    lvl = "high 🔥" if volume >= CONFIG["volume_threshold"] else "low ⚠️"
                    msg = f"👀 Watch zone: ${price:.4f} | Vol {lvl}"
                elif zone == "breakout":
                    msg = f"🚀 Breakout zone: ${price:.4f}"
                elif zone == "trim1":
                    msg = f"💰 Trim 1 zone: ${price:.4f} — consider 25%"
                elif zone == "trim2":
                    msg = f"🟥 Trim 2 zone: ${price:.4f} — max profit"
                break

        if msg:
            last = self.last_alert.get(msg, 0)
            if now - last >= CONFIG["reminder_interval"]:
                if isinstance(rsi, (int, float)):
                    msg += f" | RSI: {rsi:.1f}"
                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=msg,
                    parse_mode=ParseMode.HTML
                )
                self.last_alert[msg] = now
