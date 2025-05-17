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
```python
CONFIG = {
    # Telegram
    "TELEGRAM_TOKEN": "YOUR_TELEGRAM_TOKEN",
    "CHAT_ID": "YOUR_CHAT_ID",

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
