def calculate_rsi(prices, period=14):
    if len(prices) < 2:
        return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        delta = prices[i] - prices[i-1]
        if delta > 0:
            gains.append(delta)
        elif delta < 0:
            losses.append(abs(delta))
    avg_gain = sum(gains[-period:]) / period if len(gains) >= period else (sum(gains)/period if gains else 0)
    avg_loss = sum(losses[-period:]) / period if len(losses) >= period else (sum(losses)/period if losses else 0)
    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))