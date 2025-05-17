CONFIG = {
    "coin_id": "thorchain",
    "symbol": "RUNE",
    "chat_id": "",  # Set via Railway env
    "telegram_token": "",  # Set via Railway env
    "poll_interval": 60,  # Seconds
    "zones": {
        "accumulation": {"min": 1.60, "max": 1.66},
        "watch": {"min": 1.66, "max": 1.74},
        "breakout": {"min": 1.74, "max": 1.84},
        "trim1": {"min": 1.84, "max": 2.05},
        "trim2": {"min": 2.05, "max": 2.40}
    },
    "rsi_enabled": True,
    "rsi_period": 14,
    "volume_threshold": 50000000,  # 24h volume in USD
    "reminder_interval": 300  # 5 minutes
}