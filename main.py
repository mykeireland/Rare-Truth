import os
from telegram.ext import Application, CommandHandler
from snapshot import snapshot

print("🛠️ Booting up... token =", os.getenv("TELEGRAM_TOKEN"))

# Build the app
app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()

# Register commands
app.add_handler(CommandHandler("snapshot", snapshot))

# Start polling (no asyncio.run / no manual loop mgmt)
app.run_polling()
