import requests, os, time
from telegram import Bot
from telegram.constants import ParseMode
from config import CONFIG
from utils import calculate_rsi

class StrategyEngine:
    def __init__(self):
        self.config = CONFIG
        self.bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
        self.chat_id = os.getenv("CHAT_ID")
        self.history = []
        self.last_alert_type = None
        self.last_alert_time = 0

    def fetch_data(self):
        url = f"https://api.coingecko.com/api/v3/coins/{self.config['coin_id']}"
        try:
            res = requests.get(url)
            data = res.json()
            price = data["market_data"]["current_price"]["usd"]
            volume = data["market_data"]["total_volume"]["usd"]
            return price, volume
        except Exception as e:
            print("Error fetching CoinGecko data:", e)
            return None, None

    async def send(self, msg):
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            print("Telegram send failed:", e)

    async def evaluate(self):
        price, volume = self.fetch_data()
        if not price:
            return

        print(f"Price: ${price:.4f}, Volume: ${volume:,}")
        now = time.time()
        self.history.append(price)
        self.history = self.history[-self.config["rsi_period"]:]  # Keep latest prices

        rsi = calculate_rsi(self.history) if self.config["rsi_enabled"] and len(self.history) >= 2 else None
        msg = None
        zone = None

        z = self.config["zones"]
        if z["accumulation"]["min"] <= price <= z["accumulation"]["max"]:
            zone = "accumulation"
            msg = f"📥 <b>ACCUMULATION ZONE</b>: ${price:.4f}"
        elif z["watch"]["min"] <= price <= z["watch"]["max"]:
            zone = "watch"
            if volume >= self.config["volume_threshold"]:
                msg = f"👀 <b>WATCH ZONE</b>: ${price:.4f} | Volume strong 🔥"
            else:
                msg = f"👀 <b>WATCH ZONE</b>: ${price:.4f} | Volume low ⚠️"
        elif z["breakout"]["min"] <= price <= z["breakout"]["max"]:
            zone = "breakout"
            msg = f"🚀 <b>BREAKOUT</b> forming: ${price:.4f}"
        elif z["trim1"]["min"] <= price <= z["trim1"]["max"]:
            zone = "trim1"
            msg = f"💰 <b>TRIM 1 ZONE</b>: ${price:.4f} — consider taking 25%"
        elif z["trim2"]["min"] <= price <= z["trim2"]["max"]:
            zone = "trim2"
            msg = f"🟥 <b>TRIM 2 ZONE</b>: ${price:.4f} — max profits zone"

        if msg:
            if self.last_alert_type != zone or (now - self.last_alert_time) > self.config["reminder_interval"]:
                rsi_txt = f" | RSI: {rsi:.1f}" if rsi else ""
                await self.send(msg + rsi_txt)
                self.last_alert_type = zone
                self.last_alert_time = now