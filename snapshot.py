import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import CONFIG
from utils import calculate_rsi

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1) Fetch & cast to floats
    try:
        resp = requests.get(
            f"https://api.coingecko.com/api/v3/coins/{CONFIG['coin_id']}"
        )
        data   = resp.json()["market_data"]
        price  = float(data["current_price"]["usd"])
        volume = float(data["total_volume"]["usd"])
        print(f"🔍 snapshot debug – price type: {type(price)}, value: {price}")
    except Exception as e:
        print("Fetch error:", e)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Error fetching market data."
        )
        return

    # 2) Maintain history
    history = context.bot_data.get("price_history", [])
    history.append(price)
    history = history[-CONFIG["rsi_period"]:]
    context.bot_data["price_history"] = history

    # 3) Compute RSI
    rsi = None
    if CONFIG["rsi_enabled"] and len(history) >= 2:
        try:
            rsi = calculate_rsi(history, CONFIG["rsi_period"])
        except Exception as e:
            print("RSI error:", e)
            rsi = None
    rsi_text = f"{rsi:.1f}" if isinstance(rsi, (int, float)) else "n/a"
    
    # ─── Compute Momentum 
    if isinstance(rsi, (int, float)):
        if rsi > 70:
            momentum = "Strong 🚀"
        elif rsi >= 45:
            momentum = "Neutral ⚖️"
        else:
            momentum = "Weak 🐻"
        else:
            momentum = "n/a"

    # 4) Determine zone label with float casts
    zone_label = "Out of Range"
    for key, bounds in CONFIG["zones"].items():
        try:
            lo = float(bounds["min"])
            hi = float(bounds["max"])
        except Exception as e:
            print(f"Zone parse error for {key}:", e)
            continue

        # debug each zone comparison
        print(f"🔍 comparing price {price} against zone '{key}' [{lo}, {hi}]")
        if lo <= price <= hi:
            mapping = {
                "accumulation": "Accumulation",
                "watch":        "Watch",
                "breakout":     "Breakout",
                "trim1":        "Trim 1",
                "trim2":        "Trim 2"
            }
            zone_label = mapping.get(key, key.capitalize())
            break

    # 5) Build & send message
    msg = (
        f"📡 <b>{CONFIG['symbol']} Snapshot</b>\n"
        f"Price: <b>${price:.4f}</b>\n"
        f"RSI: <b>{rsi_text}</b>\n"
        f"24h Vol: <b>${volume:,.0f}</b>\n"
        f"🔹 Zone: <b>{zone_label}</b>\n\n"
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

