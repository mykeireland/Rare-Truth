import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import CONFIG
from utils import calculate_rsi

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1️⃣ Fetch 24h stats from Binance
    try:
        ticker = requests.get(
            "https://api.binance.com/api/v3/ticker/24hr",
            params={"symbol": CONFIG["binance_symbol"]}
        ).json()
        price           = float(ticker["lastPrice"])
        volume          = float(ticker["quoteVolume"])
        open_price      = float(ticker["openPrice"])
        high_price      = float(ticker["highPrice"])
        low_price       = float(ticker["lowPrice"])
        price_change    = float(ticker["priceChange"])
        price_pct       = float(ticker["priceChangePercent"])
        weighted_avg    = float(ticker["weightedAvgPrice"])
        trade_count     = int(ticker["count"])
        bid_price       = float(ticker["bidPrice"])
        ask_price       = float(ticker["askPrice"])
    except Exception as e:
        print("❌ Binance fetch error:", e)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Error fetching Binance data."
        )
        return

    # 2️⃣ Fetch RSI from Binance hourly klines
    rsi = None
    if CONFIG["rsi_enabled"]:
        try:
            klines = requests.get(
                "https://api.binance.com/api/v3/klines",
                params={
                    "symbol":   CONFIG["binance_symbol"],
                    "interval": "1h",
                    "limit":    CONFIG["rsi_period"] + 1
                }
            ).json()
            closes = [float(k[4]) for k in klines]
            if len(closes) >= CONFIG["rsi_period"] + 1:
                rsi = calculate_rsi(closes, CONFIG["rsi_period"])
        except Exception as e:
            print("⚠️ RSI fetch error:", e)
            rsi = None

    # 3️⃣ Format RSI & momentum
    rsi_text = f"{rsi:.1f}" if isinstance(rsi, (int, float)) else "n/a"
    if isinstance(rsi, (int, float)):
        momentum = "Strong 🚀"   if rsi > 70  else \
                   "Neutral ⚖️"  if rsi >= 45 else \
                   "Weak 🐻"
    else:
        momentum = "n/a"

    # 4️⃣ Determine current zone
    zone_label = "Out of Range"
    for key, bounds in CONFIG["zones"].items():
        lo, hi = float(bounds["min"]), float(bounds["max"])
        if lo <= price <= hi:
            zone_label = {
                "accumulation":"Accumulation",
                "watch":       "Watch",
                "breakout":    "Breakout",
                "trim1":       "Trim 1",
                "trim2":       "Trim 2"
            }[key]
            break

    # 5️⃣ Build & send the enriched snapshot
    msg = (
        f"📡 <b>{CONFIG['symbol']} Snapshot</b>\n"
        f"Price: <b>${price:.4f}</b>   24h Vol: <b>${volume:,.0f}</b>\n"
        f"Open: <b>${open_price:.4f}</b>   High: <b>${high_price:.4f}</b>   Low: <b>${low_price:.4f}</b>\n"
        f"Change: <b>{price_change:.4f} ({price_pct:.2f}%)</b>   Wtd Avg: <b>${weighted_avg:.4f}</b>\n"
        f"Bid/Ask: <b>${bid_price:.4f}/${ask_price:.4f}</b>   Trades: <b>{trade_count}</b>\n\n"
        f"🔹 RSI (14): <b>{rsi_text}</b>   🔹 Momentum: <b>{momentum}</b>\n"
        f"🔹 Zone: <b>{zone_label}</b>\n\n"
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
