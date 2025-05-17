import requests
import time
from state import (
    last_signal_status,
    last_notified_price,
    last_notification_time,
    COOLDOWN_SECONDS,
    PRICE_DELTA_ABS,
    PRICE_DELTA_PCT
)

# Calculate standard RSI
def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        delta = prices[i] - prices[i-1]
        if delta > 0:
            gains.append(delta)
        else:
            losses.append(abs(delta))
    avg_gain = sum(gains[-period:]) / period if gains else 0
    avg_loss = sum(losses[-period:]) / period if losses else 0
    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# Fetch current price & volume from Binance 24h ticker
def fetch_ticker(symbol):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    r = requests.get(url, params={"symbol": symbol})
    d = r.json()
    return float(d["lastPrice"]), float(d["quoteVolume"])

# Fetch last (period+1) hourly closes for RSI
def fetch_klines(symbol, period):
    url = "https://api.binance.com/api/v3/klines"
    r = requests.get(url, params={
        "symbol": symbol,
        "interval": "1h",
        "limit": period + 1
    })
    kl = r.json()
    return [float(k[4]) for k in kl]

# Throttle logic
def should_notify(current_status: str, current_price: float) -> bool:
    global last_signal_status, last_notified_price, last_notification_time
    now = time.time()
    # Always notify on status change
    if current_status != last_signal_status:
        return True
    # Enforce cooldown
    if now - last_notification_time < COOLDOWN_SECONDS:
        return False
    # Require minimum price movement
    if last_notified_price is not None:
        delta = abs(current_price - last_notified_price)
        threshold = max(PRICE_DELTA_ABS, PRICE_DELTA_PCT * last_notified_price)
        if delta < threshold:
            return False
    return True

def record_notification(current_status: str, current_price: float):
    global last_signal_status, last_notified_price, last_notification_time
    last_signal_status = current_status
    last_notified_price = current_price
    last_notification_time = time.time()
