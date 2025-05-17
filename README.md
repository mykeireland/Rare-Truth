# Rare Truth Bot v3

### 🎯 Features:
- CoinGecko-powered live price + volume
- RSI calculation based on recent price history
- Zone-aware messaging logic:
  - Accumulation / Watch / Breakout / Trim 1 / Trim 2
- 5-minute cooldown to prevent spam
- Configurable zones and volume thresholds
- Clean Telegram alerts with confidence signals

### 📦 Config via `config.py`
Set your zone prices, volume thresholds, and RSI options easily in one file.

### 📬 Telegram
- Set `TELEGRAM_TOKEN` and `CHAT_ID` in Railway env

Bot checks every 60s and alerts when new zone reached or when a zone holds after 5 mins.