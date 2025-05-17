import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import CONFIG
from utils import calculate_rsi

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1) Fetch price & volume
    try:
        resp = requests.get(f"https://api.coingecko.com/api/v3/coins/{CONFIG['coin_id']}")
        m = resp.json()["market_data"]
        price  = float(m["current_price"]["usd"])
        volume = float(m["total_volume"]["usd"])
    except Exception as e:
        print("Fetch error:", e)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Error fetching market data."
        )
        return

    # 2) Pull last 24h of hourly prices for RSI
    rsi = None
    if CONFIG["rsi_enabled"]:
        try:
            chart = requests.get(
                f"https://api.coingecko.com/api/v3/coins/{CONFIG['coin_id']}/market_chart",
                params={"vs_currency": "usd", "days": 1, "interval": "hourly"}
            ).json()
            prices = [p[1] for p in chart.get("prices", [])]
            if len(prices) >= CONFIG["rsi_period"] + 1:
                rsi = calculate_rsi(prices[-(CONFIG["rsi_period"] + 1):], CONFIG["rsi_period"])
        except Exception as e:
            print("RSI fetch error:", e)
            rsi = None

    # 3) Format RSI text
    rsi_text = f"{rsi:.1f}" if isinstance(rsi, (int, float)) else "n/a"

    # 4) Compute Momentum
    if isinstance(rsi, (int, float)):
        if rsi > 70:
            momentum = "Strong 🚀"
        elif rsi >= 45:
            momentum = "Neutral ⚖️"
        else:
            momentum = "Weak 🐻"
    else:
        momentum = "n/a"

    # 5) Determine current zone (robust float‐casting)
    zone_label = "Out of Range"
    for key, bounds in CONFIG["zones"].items():
        try:
            lo = float(bounds["min"])
            hi = float(bounds["max"])
        except (TypeError, ValueError):
            print(f"⚠️ Skipping malformed zone {key}: {bounds}")
            continue

        if lo <= price <= hi:
            zone_label = {
                "accumulation": "Accumulation",
                "watch":        "Watch",
                "breakout":     "Breakout",
                "trim1":        "Trim 1",
                "trim2":        "Trim 2"
            }[key]
            break

    # 6) Build & send the snapshot
    msg = (
        f"📡 <b>{CONFIG['symbol']} Snapshot</b>\n"
        f"Price: <b>${price:.4f}</b>\n"
        f"RSI: <b>{rsi_text}</b>\n"
        f"24h Vol: <b>${volume:,.0f}</b>\n"
        f"🔹 Zone: <b>{zone_label}</b>\n"
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
