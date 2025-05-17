import os

CONFIG = {
    # Telegram (env vars in your deployment)
    "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
    "CHAT_ID": os.getenv("CHAT_ID"),

    # Binance pair
    "binance_symbol": "RUNEUSDT",

    # Polling & alerts intervals
    "poll_interval": 60,           # seconds between checks
    "reminder_interval": 300,      # seconds before repeating alerts

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
