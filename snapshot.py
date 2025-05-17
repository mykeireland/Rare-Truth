import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import CONFIG
from utils import calculate_rsi

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1️⃣ Fetch current price & volume
    try:
        resp = requests.get(
            f"https://api.coingecko.com/api/v3/coins/{CONFIG['coin_id']}"
        )
        m = resp.json()["market_data"]
        price  = float(m["current_price"]["usd"])
        volume = float(m["total_volume"]["usd"])
    except Exception:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Error fetching market data."
        )
        return

    # 2️⃣ Pull 24h of hourly prices to seed RSI calculation
    rsi = None
    if CONFIG["rsi_enabled"]:
        try:
            chart = requests.get(
                f"https://api.coingecko.com/api/v3/coins/{CONFIG['coin_id']}/market_chart",
                params={"vs_currency":"usd","days":1,"interval":"hourly"}
            ).json()
            prices = [p[1] for p in chart["prices"]]
            if len(prices) >= CONFIG["rsi_period"] + 1:
                rsi = calculate_rsi(prices[-(CONFIG["rsi_period"]+1):], CONFIG["rsi_period"])
        except Exception:
            rsi = None

    # 3️⃣ Format RSI and Momentum
    rsi_text = f"{rsi:.1f}" if isinstance(rsi, (int,float)) else "n/a"
    if isinstance(rsi, (int,float)):
        if rsi > 70:      momentum = "Strong 🚀"
        elif rsi >= 45:   momentum = "Neutral ⚖️"
        else:             momentum = "Weak 🐻"
    else:
        momentum = "n/a"

    # 4️⃣ Determine your zone
    zone = "Out of Range"
    for key,(lo,hi) in CONFIG["zones"].items():
        lo,hi = float(lo), float(hi)
        if lo <= price <= hi:
            names = {
              "accumulation":"Accumulation",
              "watch":"Watch",
              "breakout":"Breakout",
              "trim1":"Trim 1",
              "trim2":"Trim 2"
            }
            zone = names.get(key, key.capitalize())
            break

    # 5️⃣ Build & send the message
    msg = (
      f"📡 <b>{CONFIG['symbol']} Snapshot</b>\n"
      f"Price: <b>${price:.4f}</b>\n"
      f"RSI: <b>{rsi_text}</b>\n"
      f"24h Vol: <b>${volume:,.0f}</b>\n"
      f"🔹 Zone: <b>{zone}</b>\n"
      f"🔹 Momentum: <b>{momentum}</b>\n\n"
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
