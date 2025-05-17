import requests
from config import CONFIG

def fetch_price_rsi_volume():
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{CONFIG['coin_id']}?localization=false&tickers=false&market_data=true"
        res = requests.get(url).json()
        price = float(res["market_data"]["current_price"]["usd"])
        volume = float(res["market_data"]["total_volume"]["usd"])
        rsi = res.get("rsi_14") or None  # Placeholder; replace with real RSI source
        momentum = res.get("momentum") or None  # Placeholder; replace with real source
        return price, rsi, momentum, volume
    except Exception as e:
        print("Error fetching price data:", e)
        return None

def format_snapshot(price, rsi, momentum, volume, lo, hi):
    msg = f"📡 <b>{CONFIG['symbol']} Snapshot</b>
"
    msg += f"💰 Price: <b>${price:.4f}</b>
"
    msg += f"📈 RSI: <b>{rsi if rsi is not None else 'n/a'}</b>
"
    msg += f"⚡ Momentum: <b>{momentum if momentum is not None else 'n/a'}</b>
"
    msg += f"📊 Volume (24h): <b>${volume:,.0f}</b>
"

    if lo <= price <= hi:
        msg += f"🔔 <b>IN BUY ZONE</b> – between ${lo} and ${hi}"
    else:
        msg += f"📎 Outside buy zone (${lo}–${hi})"

    return msg
