import time

# Notification state and thresholds
last_signal_status     = None    # e.g., "Watch", "Breakout"
last_notified_price    = None    # price at last alert
last_notification_time = 0       # epoch seconds

# Throttle settings
COOLDOWN_SECONDS = 300           # 5-minute silence after alert
PRICE_DELTA_ABS  = 0.01          # $0.01 minimum move
PRICE_DELTA_PCT  = 0.005         # 0.5% minimum move
