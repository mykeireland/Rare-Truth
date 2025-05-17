import os
print("🛠️ Booting up... token=", os.getenv("TELEGRAM_TOKEN"))

import asyncio
import os
from telegram.ext import Application, CommandHandler
from snapshot import snapshot

async def main():
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("snapshot", snapshot))
    await app.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
