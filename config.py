import os

CONFIG = {
    # Telegram (set these as environment variables in your deployment)
    "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),  # e.g. "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    "CHAT_ID": os.getenv("CHAT_ID"),                # your numeric chat ID or group ID

    # Binance symbols
    "binance_symbol": "RUNEUSDT",

    # Polling & alerts
    "poll_interval": 60,           # seconds between zone checks
    "reminder_interval": 300,      # seconds before repeating same alert

    # RSI settings
    "rsi_enabled": True,
    "rsi_period": 14,

    # Volume threshold for watch alerts
    "volume_threshold": 50_000_000,

    # Trading zones
    "zones": {
        "accumulation": {"min": 1.60, "max": 1.66},
        "watch":        {"min": 1.66, "max": 1.74},
        "breakout":     {"min": 1.74, "max": 1.84},
        "trim1":        {"min": 1.84, "max": 2.05},
        "trim2":        {"min": 2.05, "max": 2.40},
    }
}


---

## 2) `utils.py`

```python
import requests

# Calculate standard RSI
def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        delta = prices[i] - prices[i-1]
        if delta > 0:
            gains.append(delta)
        elif delta < 0:
            losses.append(abs(delta))
    avg_gain = sum(gains[-period:]) / period if gains else 0
    avg_loss = sum(losses[-period:]) / period if losses else 0
    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# Fetch latest price & volume from Binance
def fetch_ticker(symbol):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    r = requests.get(url, params={"symbol": symbol})
    d = r.json()
    return float(d["lastPrice"]), float(d["quoteVolume"])

# Fetch last (period+1) closes for RSI
def fetch_klines(symbol, period):
    url = "https://api.binance.com/api/v3/klines"
    r = requests.get(url, params={
        "symbol": symbol,
        "interval": "1h",
        "limit": period + 1
    })
    kl = r.json()
    return [float(k[4]) for k in kl]
