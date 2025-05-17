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
