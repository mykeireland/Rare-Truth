import os, time, requests
from telegram import Bot
from telegram.constants import ParseMode
from config import CONFIG
from utils import calculate_rsi

class StrategyEngine:
    def __init__(self):
        token = os.getenv("TELEGRAM_TOKEN")
        self.bot = Bot(token=token)
        self.chat_id = os.getenv("CHAT_ID")
        self.config = CONFIG
        self.history = []
        self.last_alert = {}

    def fetch_market(self):
        try:
            data = requests.get(f"https://api.coingecko.com/api/v3/coins/{self.config['coin_id']}").json()['market_data']
            return data['current_price']['usd'], data['total_volume']['usd']
        except:
            return None, None

    async def evaluate(self):
        price, volume = self.fetch_market()
        if price is None:
            return
        now = time.time()

        # RSI
        self.history.append(price)
        self.history = self.history[-self.config['rsi_period']:]
        rsi = None
        if self.config['rsi_enabled'] and len(self.history) >= 2:
            rsi = calculate_rsi(self.history, self.config['rsi_period'])

        z = self.config['zones']
        zone = msg = None
        if z['accumulation']['min'] <= price <= z['accumulation']['max']:
            zone, msg = 'accumulation', f"📥 ACCUMULATION ZONE: ${price:.4f}"
        elif z['watch']['min'] <= price <= z['watch']['max']:
            lvl = 'strong 🔥' if volume >= self.config['volume_threshold'] else 'low ⚠️'
            zone, msg = 'watch', f"👀 WATCH ZONE: ${price:.4f} | Volume {lvl}"
        elif z['breakout']['min'] <= price <= z['breakout']['max']:
            zone, msg = 'breakout', f"🚀 BREAKOUT forming: ${price:.4f}"
        elif z['trim1']['min'] <= price <= z['trim1']['max']:
            zone, msg = 'trim1', f"💰 TRIM 1 ZONE: ${price:.4f} — take 25%"
        elif z['trim2']['min'] <= price <= z['trim2']['max']:
            zone, msg = 'trim2', f"🟥 TRIM 2 ZONE: ${price:.4f} — max profit"

        if zone and msg:
            last_time = self.last_alert.get(zone, 0)
            if now - last_time >= self.config['reminder_interval']:
                if isinstance(rsi, (int, float)):
                    msg += f" | RSI: {rsi:.1f}"
                await self.bot.send_message(chat_id=self.chat_id, text=msg, parse_mode=ParseMode.HTML)
                self.last_alert[zone] = now