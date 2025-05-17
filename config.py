import os

CONFIG = {
    # Telegram credentials (set these as env vars in your deployment)
    "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
    "CHAT_ID": os.getenv("CHAT_ID"),

    # Trading pair for price/volume and RSI
    "binance_symbol": "RUNEUSDT",
    "symbol": "RUNE",

    # Polling & alert intervals (seconds)
    "poll_interval": 60,
    "reminder_interval": 300,

    # RSI settings
    "rsi_enabled": True,
    "rsi_period": 14,

    # Minimum 24h USDT volume for watch alerts
    "volume_threshold": 50_000_000,

    # Defined trading zones (USD)
    "zones": {
        "accumulation": {"min": 1.60, "max": 1.66},
        "watch":        {"min": 1.66, "max": 1.74},
        "breakout":     {"min": 1.74, "max": 1.84},
        "trim1":        {"min": 1.84, "max": 2.05},
        "trim2":        {"min": 2.05, "max": 2.40},
    }
}
