CONFIG = {
    "binance_symbol":    "RUNEUSDT",    # Pair to pull data from Binance
    "symbol":            "RUNE",        # For display
    "poll_interval":     60,            # Seconds between engine checks
    "rsi_enabled":       True,
    "rsi_period":        14,
    "volume_threshold":  50_000_000,    # 24h USDT volume filter
    "reminder_interval": 300,           # Seconds before repeating alerts
    "zones": {
        "accumulation": {"min": 1.60, "max": 1.66},
        "watch":        {"min": 1.66, "max": 1.74},
        "breakout":     {"min": 1.74, "max": 1.84},
        "trim1":        {"min": 1.84, "max": 2.05},
        "trim2":        {"min": 2.05, "max": 2.40}
    }
}
